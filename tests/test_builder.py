import os
import tempfile
import types
from unittest import TestCase

from nlp.arrow_dataset import Dataset
from nlp.arrow_writer import ArrowWriter
from nlp.builder import FORCE_REDOWNLOAD, DatasetBuilder, GeneratorBasedBuilder
from nlp.dataset_dict import DatasetDict
from nlp.features import Features, Value
from nlp.info import DatasetInfo
from nlp.splits import Split, SplitDict, SplitGenerator, SplitInfo


class DummyBuilder(DatasetBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _prepare_split(self, split_generator, **kwargs):
        fname = "{}-{}.arrow".format(self.name, split_generator.name)
        writer = ArrowWriter(features=self.info.features, path=os.path.join(self._cache_dir, fname))
        writer.write_batch({"text": ["foo"] * 100})
        num_examples, num_bytes = writer.finalize()
        split_generator.split_info.num_examples = num_examples
        split_generator.split_info.num_bytes = num_bytes


class DummyGeneratorBasedBuilder(GeneratorBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_examples(self):
        for i in range(100):
            yield i, {"text": "foo"}


class BuilderTest(TestCase):
    def test_as_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            os.makedirs(dummy_builder.cache_dir)

            dummy_builder.info.splits = SplitDict()
            dummy_builder.info.splits.add(SplitInfo("train", num_examples=10))
            dummy_builder.info.splits.add(SplitInfo("test", num_examples=10))

            for split in dummy_builder.info.splits:
                writer = ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                )
                writer.write_batch({"text": ["foo"] * 10})
                writer.finalize()

            dsets = dummy_builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)
            self.assertListEqual(list(dsets.keys()), ["train", "test"])
            self.assertEqual(len(dsets["train"]), 10)
            self.assertEqual(len(dsets["test"]), 10)

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 13)

    def test_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow"))
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dataset_info.json"))
            )

    def test_error_download_and_prepare(self):
        def _prepare_split(self, split_generator, **kwargs):
            raise ValueError()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._prepare_split = types.MethodType(_prepare_split, dummy_builder)
            self.assertRaises(
                ValueError, dummy_builder.download_and_prepare, try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD
            )
            self.assertRaises(AssertionError, dummy_builder.as_dataset)

    def test_generator_based_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir,
                        "dummy_generator_based_builder",
                        "dummy",
                        "0.0.0",
                        "dummy_generator_based_builder-train.arrow",
                    )
                )
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(
                    os.path.join(tmp_dir, "dummy_generator_based_builder", "dummy", "0.0.0", "dataset_info.json")
                )
            )
