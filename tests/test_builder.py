import os
import tempfile
import types
from pathlib import Path
from unittest import TestCase

import numpy as np
import pytest
from multiprocess.pool import Pool

from datasets.arrow_dataset import Dataset
from datasets.arrow_writer import ArrowWriter
from datasets.builder import BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from datasets.dataset_dict import DatasetDict
from datasets.features import Features, Value
from datasets.info import DatasetInfo, PostProcessedInfo
from datasets.splits import Split, SplitDict, SplitGenerator, SplitInfo
from datasets.utils.download_manager import GenerateMode

from .utils import assert_arrow_memory_doesnt_increase, assert_arrow_memory_increases, require_faiss


class DummyBuilder(DatasetBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _prepare_split(self, split_generator, **kwargs):
        fname = f"{self.name}-{split_generator.name}.arrow"
        with ArrowWriter(features=self.info.features, path=os.path.join(self._cache_dir, fname)) as writer:
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
        self.times = times


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


class DummyBuilderWithDownload(DummyBuilder):
    def __init__(self, *args, rel_path=None, abs_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._rel_path = rel_path
        self._abs_path = abs_path

    def _split_generators(self, dl_manager):
        if self._rel_path is not None:
            assert os.path.exists(dl_manager.download(self._rel_path)), "dl_manager must support relative paths"
        if self._abs_path is not None:
            assert os.path.exists(dl_manager.download(self._abs_path)), "dl_manager must support absolute paths"
        return [SplitGenerator(name=Split.TRAIN)]


class DummyBuilderWithManualDownload(DummyBuilderWithMultipleConfigs):
    @property
    def manual_download_instructions(self):
        return "To use the dataset you have to download some stuff manually and pass the data path to data_dir"

    def _split_generators(self, dl_manager):
        if not os.path.exists(self.config.data_dir):
            raise FileNotFoundError(f"data_dir {self.config.data_dir} doesn't exist.")
        return [SplitGenerator(name=Split.TRAIN)]


def _run_concurrent_download_and_prepare(tmp_dir):
    dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
    dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.REUSE_DATASET_IF_EXISTS)
    return dummy_builder


class BuilderTest(TestCase):
    def test_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow"))
            )
            self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
            self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dataset_info.json"))
            )

    def test_concurrent_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            processes = 2
            with Pool(processes=processes) as pool:
                jobs = [
                    pool.apply_async(_run_concurrent_download_and_prepare, kwds={"tmp_dir": tmp_dir})
                    for _ in range(processes)
                ]
                dummy_builders = [job.get() for job in jobs]
                for dummy_builder in dummy_builders:
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dummy_builder-train.arrow")
                        )
                    )
                    self.assertDictEqual(dummy_builder.info.features, Features({"text": Value("string")}))
                    self.assertEqual(dummy_builder.info.splits["train"].num_examples, 100)
                    self.assertTrue(
                        os.path.exists(os.path.join(tmp_dir, "dummy_builder", "dummy", "0.0.0", "dataset_info.json"))
                    )

    def test_download_and_prepare_with_base_path(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            rel_path = "dummy1.data"
            abs_path = os.path.join(tmp_dir, "dummy2.data")
            # test relative path is missing
            dummy_builder = DummyBuilderWithDownload(cache_dir=tmp_dir, name="dummy", rel_path=rel_path)
            with self.assertRaises(FileNotFoundError):
                dummy_builder.download_and_prepare(
                    try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD, base_path=tmp_dir
                )
            # test absolute path is missing
            dummy_builder = DummyBuilderWithDownload(cache_dir=tmp_dir, name="dummy", abs_path=abs_path)
            with self.assertRaises(FileNotFoundError):
                dummy_builder.download_and_prepare(
                    try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD, base_path=tmp_dir
                )
            # test that they are both properly loaded when they exist
            open(os.path.join(tmp_dir, rel_path), "w")
            open(abs_path, "w")
            dummy_builder = DummyBuilderWithDownload(
                cache_dir=tmp_dir, name="dummy", rel_path=rel_path, abs_path=abs_path
            )
            dummy_builder.download_and_prepare(
                try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD, base_path=tmp_dir
            )
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir,
                        "dummy_builder_with_download",
                        "dummy",
                        "0.0.0",
                        "dummy_builder_with_download-train.arrow",
                    )
                )
            )

    def test_as_dataset_with_post_process(self):
        def _post_process(self, dataset, resources_paths):
            def char_tokenize(example):
                return {"tokens": list(example["text"])}

            return dataset.map(char_tokenize, cache_file_name=resources_paths["tokenized_dataset"])

        def _post_processing_resources(self, split):
            return {"tokenized_dataset": f"tokenized_dataset-{split}.arrow"}

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
                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"tokenized_dataset-{split}.arrow"),
                    features=Features({"text": Value("string"), "tokens": [Value("string")]}),
                ) as writer:
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

            dset = dummy_builder.as_dataset("all")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test")
            self.assertEqual(len(dset), 20)
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
                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
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
            return {"index": f"Flat-{split}.faiss"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
            os.makedirs(dummy_builder.cache_dir)

            dummy_builder.info.splits = SplitDict()
            dummy_builder.info.splits.add(SplitInfo("train", num_examples=10))
            dummy_builder.info.splits.add(SplitInfo("test", num_examples=10))

            for split in dummy_builder.info.splits:
                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
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
            return {"tokenized_dataset": f"tokenized_dataset-{split}.arrow"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.info.post_processed = PostProcessedInfo(
                features=Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
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
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
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
            return {"index": f"Flat-{split}.faiss"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder._post_process = types.MethodType(_post_process, dummy_builder)
            dummy_builder._post_processing_resources = types.MethodType(_post_processing_resources, dummy_builder)
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
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
                ValueError,
                dummy_builder.download_and_prepare,
                try_from_hf_gcs=False,
                download_mode=GenerateMode.FORCE_REDOWNLOAD,
            )
            self.assertRaises(AssertionError, dummy_builder.as_dataset)

    def test_generator_based_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy")
            dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
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

    def test_cache_dir_no_args(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, name="dummy", data_dir=None, data_files=None)
            relative_cache_dir_parts = Path(dummy_builder._relative_data_dir()).parts
            self.assertEqual(relative_cache_dir_parts, ("dummy_generator_based_builder", "dummy", "0.0.0"))

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
            # create config on the fly
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

        with tempfile.TemporaryDirectory() as tmp_dir:
            # overwrite an existing config
            dummy_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a", content="foo", times=2)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a", times=2, content="foo")
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            self.assertIn("content=foo", dummy_builder.cache_dir)
            self.assertIn("times=2", dummy_builder.cache_dir)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a", content="bar", times=2)
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a", content="foo")
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)

    def test_config_names(self):
        with tempfile.TemporaryDirectory() as tmp_dir:

            with self.assertRaises(ValueError) as error_context:
                DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, data_files=None, data_dir=None)
            self.assertIn("Please pick one among the available configs", str(error_context.exception))

            dummy_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="a")
            self.assertEqual(dummy_builder.config.name, "a")

            dummy_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, name="b")
            self.assertEqual(dummy_builder.config.name, "b")

            with self.assertRaises(ValueError):
                DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir)

            dummy_builder = DummyBuilderWithDefaultConfig(cache_dir=tmp_dir)
            self.assertEqual(dummy_builder.config.name, "a")

    def test_cache_dir_for_data_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir, tempfile.TemporaryDirectory() as data_dir:
            dummy_builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, name="a", data_dir=data_dir)
            other_builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, name="a", data_dir=data_dir)
            self.assertEqual(dummy_builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, name="a", data_dir=tmp_dir)
            self.assertNotEqual(dummy_builder.cache_dir, other_builder.cache_dir)


@pytest.mark.parametrize(
    "split, expected_dataset_class, expected_dataset_length",
    [
        (None, DatasetDict, 10),
        ("train", Dataset, 10),
        ("train+test[:30%]", Dataset, 13),
    ],
)
@pytest.mark.parametrize("in_memory", [False, True])
def test_builder_as_dataset(split, expected_dataset_class, expected_dataset_length, in_memory, tmp_path):
    cache_dir = str(tmp_path)
    dummy_builder = DummyBuilder(cache_dir=cache_dir, name="dummy")
    os.makedirs(dummy_builder.cache_dir)

    dummy_builder.info.splits = SplitDict()
    dummy_builder.info.splits.add(SplitInfo("train", num_examples=10))
    dummy_builder.info.splits.add(SplitInfo("test", num_examples=10))

    for info_split in dummy_builder.info.splits:
        with ArrowWriter(
            path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{info_split}.arrow"),
            features=Features({"text": Value("string")}),
        ) as writer:
            writer.write_batch({"text": ["foo"] * 10})
            writer.finalize()

    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset = dummy_builder.as_dataset(split=split, in_memory=in_memory)
    assert isinstance(dataset, expected_dataset_class)
    if isinstance(dataset, DatasetDict):
        assert list(dataset.keys()) == ["train", "test"]
        datasets = dataset.values()
        expected_splits = ["train", "test"]
    elif isinstance(dataset, Dataset):
        datasets = [dataset]
        expected_splits = [split]
    for dataset, expected_split in zip(datasets, expected_splits):
        assert dataset.split == expected_split
        assert len(dataset) == expected_dataset_length
        assert dataset.features == Features({"text": Value("string")})
        dataset.column_names == ["text"]


@pytest.mark.parametrize("in_memory", [False, True])
def test_generator_based_builder_as_dataset(in_memory, tmp_path):
    cache_dir = tmp_path / "data"
    cache_dir.mkdir()
    cache_dir = str(cache_dir)
    dummy_builder = DummyGeneratorBasedBuilder(cache_dir=cache_dir, name="dummy")
    dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset = dummy_builder.as_dataset("train", in_memory=in_memory)
    assert dataset.data.to_pydict() == {"text": ["foo"] * 100}


@pytest.mark.parametrize(
    "writer_batch_size, default_writer_batch_size, expected_chunks", [(None, None, 1), (None, 5, 20), (10, None, 10)]
)
def test_custom_writer_batch_size(tmp_path, writer_batch_size, default_writer_batch_size, expected_chunks):
    cache_dir = str(tmp_path)
    if default_writer_batch_size:
        DummyGeneratorBasedBuilder.DEFAULT_WRITER_BATCH_SIZE = default_writer_batch_size
    dummy_builder = DummyGeneratorBasedBuilder(cache_dir=cache_dir, name="dummy", writer_batch_size=writer_batch_size)
    assert dummy_builder._writer_batch_size == (writer_batch_size or default_writer_batch_size)
    dummy_builder.download_and_prepare(try_from_hf_gcs=False, download_mode=GenerateMode.FORCE_REDOWNLOAD)
    dataset = dummy_builder.as_dataset("train")
    assert len(dataset.data[0].chunks) == expected_chunks
