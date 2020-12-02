import os
import tempfile
import types
from unittest import TestCase

import numpy as np

from datasets.arrow_dataset import Dataset
from datasets.arrow_writer import ArrowWriter
from datasets.builder import FORCE_REDOWNLOAD, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from datasets.dataset_dict import DatasetDict
from datasets.features import Features, Value
from datasets.info import DatasetInfo, PostProcessedInfo
from datasets.splits import Split, SplitDict, SplitGenerator, SplitInfo

from .utils import require_faiss


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


class DummyGeneratorBasedBuilderWithIntegers(GeneratorBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_examples(self):
        for i in range(100):
            yield i, {"id": i}


class DummyGeneratorBasedBuilderWithConfigConfig(BuilderConfig):
    def __init__(self, content="foo", times=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content


class DummyGeneratorBasedBuilderWithConfig(GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = DummyGeneratorBasedBuilderWithConfigConfig

    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_examples(self):
        for i in range(100):
            yield i, {"text": self.config.content * self.config.times}


class DummyBuilderWithMultipleConfigs(DummyBuilder):
    BUILDER_CONFIGS = [
        DummyGeneratorBasedBuilderWithConfigConfig(name="a"),
        DummyGeneratorBasedBuilderWithConfigConfig(name="b"),
    ]


class DummyBuilderWithDefaultConfig(DummyBuilderWithMultipleConfigs):
    DEFAULT_CONFIG_NAME = "a"


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
            self.assertDictEqual(dsets["train"].features, Features({"text": Value("string")}))
            self.assertDictEqual(dsets["test"].features, Features({"text": Value("string")}))
            self.assertListEqual(dsets["train"].column_names, ["text"])
            self.assertListEqual(dsets["test"].column_names, ["text"])
            del dsets

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            del dset

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 13)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            del dset

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

    def test_as_dataset_with_post_process(self):
        def _post_process(self, dataset, resources_paths):
            def char_tokenize(example):
                return {"tokens": list(example["text"])}

            return dataset.map(char_tokenize, cache_file_name=resources_paths["tokenized_dataset"])

        def _post_processing_resources(self, split):
            return {"tokenized_dataset": "tokenized_dataset-{split}.arrow".format(split=split)}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.info.post_processed = PostProcessedInfo(
                features=Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
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

                writer = ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"tokenized_dataset-{split}.arrow"),
                    features=Features({"text": Value("string"), "tokens": [Value("string")]}),
                )
                writer.write_batch({"text": ["foo"] * 10, "tokens": [list("foo")] * 10})
                writer.finalize()

            dsets = dummy_builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)
            self.assertListEqual(list(dsets.keys()), ["train", "test"])
            self.assertEqual(len(dsets["train"]), 10)
            self.assertEqual(len(dsets["test"]), 10)
            self.assertDictEqual(
                dsets["train"].features, Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            self.assertDictEqual(
                dsets["test"].features, Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            self.assertListEqual(dsets["train"].column_names, ["text", "tokens"])
            self.assertListEqual(dsets["test"].column_names, ["text", "tokens"])
            del dsets

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"text": Value("string"), "tokens": [Value("string")]}))
            self.assertListEqual(dset.column_names, ["text", "tokens"])
            self.assertGreater(dummy_builder.info.post_processing_size, 0)
            self.assertGreater(
                dummy_builder.info.post_processed.resources_checksums["train"]["tokenized_dataset"]["num_bytes"], 0
            )
            del dset

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 13)
            self.assertDictEqual(dset.features, Features({"text": Value("string"), "tokens": [Value("string")]}))
            self.assertListEqual(dset.column_names, ["text", "tokens"])
            del dset

        def _post_process(self, dataset, resources_paths):
            return dataset.select([0, 1], keep_in_memory=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
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

                writer = ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                )
                writer.write_batch({"text": ["foo"] * 2})
                writer.finalize()

            dsets = dummy_builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)
            self.assertListEqual(list(dsets.keys()), ["train", "test"])
            self.assertEqual(len(dsets["train"]), 2)
            self.assertEqual(len(dsets["test"]), 2)
            self.assertDictEqual(dsets["train"].features, Features({"text": Value("string")}))
            self.assertDictEqual(dsets["test"].features, Features({"text": Value("string")}))
            self.assertListEqual(dsets["train"].column_names, ["text"])
            self.assertListEqual(dsets["test"].column_names, ["text"])
            del dsets

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 2)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            del dset

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 2)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            del dset

    @require_faiss
    def test_as_dataset_with_post_process_with_index(self):
        def _post_process(self, dataset, resources_paths):
            if os.path.exists(resources_paths["index"]):
                dataset.load_faiss_index("my_index", resources_paths["index"])
                return dataset
            else:
                dataset.add_faiss_index_from_external_arrays(
                    external_arrays=np.ones((len(dataset), 8)), string_factory="Flat", index_name="my_index"
                )
                dataset.save_faiss_index("my_index", resources_paths["index"])
                return dataset

        def _post_processing_resources(self, split):
            return {"index": "Flat-{split}.faiss".format(split=split)}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
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

                writer = ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                )
                writer.write_batch({"text": ["foo"] * 2})
                writer.finalize()

            dsets = dummy_builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)
            self.assertListEqual(list(dsets.keys()), ["train", "test"])
            self.assertEqual(len(dsets["train"]), 10)
            self.assertEqual(len(dsets["test"]), 10)
            self.assertDictEqual(dsets["train"].features, Features({"text": Value("string")}))
            self.assertDictEqual(dsets["test"].features, Features({"text": Value("string")}))
            self.assertListEqual(dsets["train"].column_names, ["text"])
            self.assertListEqual(dsets["test"].column_names, ["text"])
            self.assertListEqual(dsets["train"].list_indexes(), ["my_index"])
            self.assertListEqual(dsets["test"].list_indexes(), ["my_index"])
            self.assertGreater(dummy_builder.info.post_processing_size, 0)
            self.assertGreater(dummy_builder.info.post_processed.resources_checksums["train"]["index"]["num_bytes"], 0)
            del dsets

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            self.assertListEqual(dset.list_indexes(), ["my_index"])
            del dset

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 13)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            self.assertListEqual(dset.list_indexes(), ["my_index"])
            del dset

    def test_download_and_prepare_with_post_process(self):
        def _post_process(self, dataset, resources_paths):
            def char_tokenize(example):
                return {"tokens": list(example["text"])}

            return dataset.map(char_tokenize, cache_file_name=resources_paths["tokenized_dataset"])

        def _post_processing_resources(self, split):
            return {"tokenized_dataset": "tokenized_dataset-{split}.arrow".format(split=split)}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.info.post_processed = PostProcessedInfo(
                features=Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow"))
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertDictEqual(
                dummy_builder.info.post_processed.features,
                Features({"text": Value("string"), "tokens": [Value("string")]}),
            )
            self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dataset_info.json"))
            )

        def _post_process(self, dataset, resources_paths):
            return dataset.select([0, 1], keep_in_memory=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow"))
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertIsNone(dummy_builder.info.post_processed)
            self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dataset_info.json"))
            )

        def _post_process(self, dataset, resources_paths):
            if os.path.exists(resources_paths["index"]):
                dataset.load_faiss_index("my_index", resources_paths["index"])
                return dataset
            else:
                dataset = dataset.add_faiss_index_from_external_arrays(
                    external_arrays=np.ones((len(dataset), 8)), string_factory="Flat", index_name="my_index"
                )
                dataset.save_faiss_index("my_index", resources_paths["index"])
                return dataset

        def _post_processing_resources(self, split):
            return {"index": "Flat-{split}.faiss".format(split=split)}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow"))
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertIsNone(dummy_builder.info.post_processed)
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

    def test_cache_dir_for_data_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_data1 = os.path.join(tmp_dir, "dummy_data1.txt")
            with open(dummy_data1, "w", encoding="utf-8") as f:
                f.writelines("foo bar")
            dummy_data2 = os.path.join(tmp_dir, "dummy_data2.txt")
            with open(dummy_data2, "w", encoding="utf-8") as f:
                f.writelines("foo bar\n")

            dummy_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_files=dummy_data1)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_files=dummy_data1)
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_files=[dummy_data1])
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": dummy_data1}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={Split.TRAIN: dummy_data1}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": [dummy_data1]}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"test": dummy_data1}
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_files=dummy_data2)
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_files=[dummy_data2])
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files=[dummy_data1, dummy_data2]
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

            dummy_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files=[dummy_data1, dummy_data2]
            )
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files=[dummy_data1, dummy_data2]
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files=[dummy_data2, dummy_data1]
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

            dummy_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": dummy_data1, "test": dummy_data2}
            )
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": dummy_data1, "test": dummy_data2}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": [dummy_data1], "test": dummy_data2}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"test": dummy_data2, "train": dummy_data1}
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": dummy_data1, "validation": dummy_data2}
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, name="dummy", data_files={"train": [dummy_data1, dummy_data2], "test": dummy_data2}
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

    def test_cache_dir_for_features(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            f1 = Features({"id": Value("int8")})
            f2 = Features({"id": Value("int32")})
            dummy_builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, name="dummy", features=f1)
            other_builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, name="dummy", features=f1)
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, name="dummy", features=f2)
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

    def test_cache_dir_for_config_kwargs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyGeneratorBasedBuilderWithConfig(
                cache_dir=tmp_dir, name="dummy", content="foo", times=2
            )
            other_builder = DummyGeneratorBasedBuilderWithConfig(
                cache_dir=tmp_dir, name="dummy", times=2, content="foo"
            )
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            self.assertIn("content=foo", dummy_builder.cache_dir)
            self.assertIn("times=2", dummy_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithConfig(
                cache_dir=tmp_dir, name="dummy", content="bar", times=2
            )
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithConfig(cache_dir=tmp_dir, name="dummy", content="foo")
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

    def test_custom_writer_batch_size(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.assertEqual(DummyGeneratorBasedBuilder._writer_batch_size, None)
            dummy_builder1 = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir,
                name="dummy1",
            )
            DummyGeneratorBasedBuilder._writer_batch_size = 5
            dummy_builder2 = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir,
                name="dummy2",
            )
            dummy_builder3 = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy3", writer_batch_size=10)
            dummy_builder1.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            dummy_builder2.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            dummy_builder3.download_and_prepare(try_from_hf_gcs=False, download_mode=FORCE_REDOWNLOAD)
            dataset1 = dummy_builder1.as_dataset("train")
            self.assertEqual(len(dataset1._data[0].chunks), 1)
            dataset2 = dummy_builder2.as_dataset("train")
            self.assertEqual(len(dataset2._data[0].chunks), 20)
            dataset3 = dummy_builder3.as_dataset("train")
            self.assertEqual(len(dataset3._data[0].chunks), 10)
            del dataset1, dataset2, dataset3

    def test_config_names(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a")
            self.assertEqual(dummy_builder.config.name, "a")

            dummy_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="b")
            self.assertEqual(dummy_builder.config.name, "b")

            with self.assertRaises(ValueError):
                DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir)

            dummy_builder = DummyBuilderWithDefaultConfig(cache_dir=tmp_dir)
            self.assertEqual(dummy_builder.config.name, "a")
