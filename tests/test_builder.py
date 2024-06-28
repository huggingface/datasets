import importlib
import os
import tempfile
import types
from contextlib import nullcontext as does_not_raise
from multiprocessing import Process
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from multiprocess.pool import Pool

from datasets.arrow_dataset import Dataset
from datasets.arrow_writer import ArrowWriter
from datasets.builder import (
    ArrowBasedBuilder,
    BuilderConfig,
    DatasetBuilder,
    GeneratorBasedBuilder,
    InvalidConfigName,
)
from datasets.data_files import DataFilesList
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.download.download_manager import DownloadMode
from datasets.features import Features, Value
from datasets.info import DatasetInfo, PostProcessedInfo
from datasets.iterable_dataset import IterableDataset
from datasets.load import configure_builder_class
from datasets.splits import Split, SplitDict, SplitGenerator, SplitInfo
from datasets.streaming import xjoin
from datasets.utils.file_utils import is_local_path
from datasets.utils.info_utils import VerificationMode
from datasets.utils.logging import INFO, get_logger

from .utils import (
    assert_arrow_memory_doesnt_increase,
    assert_arrow_memory_increases,
    require_faiss,
    set_current_working_directory_to_temp_dir,
)


class DummyBuilder(DatasetBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _prepare_split(self, split_generator, **kwargs):
        fname = f"{self.dataset_name}-{split_generator.name}.arrow"
        with ArrowWriter(features=self.info.features, path=os.path.join(self._output_dir, fname)) as writer:
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


class DummyArrowBasedBuilder(ArrowBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_tables(self):
        for i in range(10):
            yield i, pa.table({"text": ["foo"] * 10})


class DummyGeneratorBasedBuilderWithIntegers(GeneratorBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_examples(self):
        for i in range(100):
            yield i, {"id": i}


class DummyGeneratorBasedBuilderConfig(BuilderConfig):
    def __init__(self, content="foo", times=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = content
        self.times = times


class DummyGeneratorBasedBuilderWithConfig(GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = DummyGeneratorBasedBuilderConfig

    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN)]

    def _generate_examples(self):
        for i in range(100):
            yield i, {"text": self.config.content * self.config.times}


class DummyBuilderWithMultipleConfigs(DummyBuilder):
    BUILDER_CONFIGS = [
        DummyGeneratorBasedBuilderConfig(name="a"),
        DummyGeneratorBasedBuilderConfig(name="b"),
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


class DummyArrowBasedBuilderWithShards(ArrowBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8"), "filepath": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN, gen_kwargs={"filepaths": [f"data{i}.txt" for i in range(4)]})]

    def _generate_tables(self, filepaths):
        idx = 0
        for filepath in filepaths:
            for i in range(10):
                yield idx, pa.table({"id": range(10 * i, 10 * (i + 1)), "filepath": [filepath] * 10})
                idx += 1


class DummyGeneratorBasedBuilderWithShards(GeneratorBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8"), "filepath": Value("string")}))

    def _split_generators(self, dl_manager):
        return [SplitGenerator(name=Split.TRAIN, gen_kwargs={"filepaths": [f"data{i}.txt" for i in range(4)]})]

    def _generate_examples(self, filepaths):
        idx = 0
        for filepath in filepaths:
            for i in range(100):
                yield idx, {"id": i, "filepath": filepath}
                idx += 1


class DummyArrowBasedBuilderWithAmbiguousShards(ArrowBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8"), "filepath": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(
                name=Split.TRAIN,
                gen_kwargs={
                    "filepaths": [f"data{i}.txt" for i in range(4)],
                    "dummy_kwarg_with_different_length": [f"dummy_data{i}.txt" for i in range(3)],
                },
            )
        ]

    def _generate_tables(self, filepaths, dummy_kwarg_with_different_length):
        idx = 0
        for filepath in filepaths:
            for i in range(10):
                yield idx, pa.table({"id": range(10 * i, 10 * (i + 1)), "filepath": [filepath] * 10})
                idx += 1


class DummyGeneratorBasedBuilderWithAmbiguousShards(GeneratorBasedBuilder):
    def _info(self):
        return DatasetInfo(features=Features({"id": Value("int8"), "filepath": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(
                name=Split.TRAIN,
                gen_kwargs={
                    "filepaths": [f"data{i}.txt" for i in range(4)],
                    "dummy_kwarg_with_different_length": [f"dummy_data{i}.txt" for i in range(3)],
                },
            )
        ]

    def _generate_examples(self, filepaths, dummy_kwarg_with_different_length):
        idx = 0
        for filepath in filepaths:
            for i in range(100):
                yield idx, {"id": i, "filepath": filepath}
                idx += 1


def _run_concurrent_download_and_prepare(tmp_dir):
    builder = DummyBuilder(cache_dir=tmp_dir)
    builder.download_and_prepare(download_mode=DownloadMode.REUSE_DATASET_IF_EXISTS)
    return builder


def check_streaming(builder):
    builders_module = importlib.import_module(builder.__module__)
    assert builders_module._patched_for_streaming
    assert builders_module.os.path.join is xjoin


class BuilderTest(TestCase):
    def test_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.arrow"
                    )
                )
            )
            self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
            self.assertEqual(builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))
            )

    def test_download_and_prepare_checksum_computation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            builder_no_verification = DummyBuilder(cache_dir=tmp_dir)
            builder_no_verification.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                all(v["checksum"] is not None for _, v in builder_no_verification.info.download_checksums.items())
            )
            builder_with_verification = DummyBuilder(cache_dir=tmp_dir)
            builder_with_verification.download_and_prepare(
                download_mode=DownloadMode.FORCE_REDOWNLOAD,
                verification_mode=VerificationMode.ALL_CHECKS,
            )
            self.assertTrue(
                all(v["checksum"] is None for _, v in builder_with_verification.info.download_checksums.items())
            )

    def test_concurrent_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            processes = 2
            with Pool(processes=processes) as pool:
                jobs = [
                    pool.apply_async(_run_concurrent_download_and_prepare, kwds={"tmp_dir": tmp_dir})
                    for _ in range(processes)
                ]
                builders = [job.get() for job in jobs]
                for builder in builders:
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(
                                tmp_dir,
                                builder.dataset_name,
                                "default",
                                "0.0.0",
                                f"{builder.dataset_name}-train.arrow",
                            )
                        )
                    )
                    self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
                    self.assertEqual(builder.info.splits["train"].num_examples, 100)
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json")
                        )
                    )

    def test_download_and_prepare_with_base_path(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            rel_path = "dummy1.data"
            abs_path = os.path.join(tmp_dir, "dummy2.data")
            # test relative path is missing
            builder = DummyBuilderWithDownload(cache_dir=tmp_dir, rel_path=rel_path)
            with self.assertRaises(FileNotFoundError):
                builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD, base_path=tmp_dir)
            # test absolute path is missing
            builder = DummyBuilderWithDownload(cache_dir=tmp_dir, abs_path=abs_path)
            with self.assertRaises(FileNotFoundError):
                builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD, base_path=tmp_dir)
            # test that they are both properly loaded when they exist
            open(os.path.join(tmp_dir, rel_path), "w")
            open(abs_path, "w")
            builder = DummyBuilderWithDownload(cache_dir=tmp_dir, rel_path=rel_path, abs_path=abs_path)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD, base_path=tmp_dir)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir,
                        builder.dataset_name,
                        "default",
                        "0.0.0",
                        f"{builder.dataset_name}-train.arrow",
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
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder.info.post_processed = PostProcessedInfo(
                features=Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            builder._post_process = types.MethodType(_post_process, builder)
            builder._post_processing_resources = types.MethodType(_post_processing_resources, builder)
            os.makedirs(builder.cache_dir)

            builder.info.splits = SplitDict()
            builder.info.splits.add(SplitInfo("train", num_examples=10))
            builder.info.splits.add(SplitInfo("test", num_examples=10))

            for split in builder.info.splits:
                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"{builder.dataset_name}-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"tokenized_dataset-{split}.arrow"),
                    features=Features({"text": Value("string"), "tokens": [Value("string")]}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10, "tokens": [list("foo")] * 10})
                    writer.finalize()

            dsets = builder.as_dataset()
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

            dset = builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"text": Value("string"), "tokens": [Value("string")]}))
            self.assertListEqual(dset.column_names, ["text", "tokens"])
            self.assertGreater(builder.info.post_processing_size, 0)
            self.assertGreater(
                builder.info.post_processed.resources_checksums["train"]["tokenized_dataset"]["num_bytes"], 0
            )
            del dset

            dset = builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test[:30%]")
            self.assertEqual(len(dset), 13)
            self.assertDictEqual(dset.features, Features({"text": Value("string"), "tokens": [Value("string")]}))
            self.assertListEqual(dset.column_names, ["text", "tokens"])
            del dset

            dset = builder.as_dataset("all")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train+test")
            self.assertEqual(len(dset), 20)
            self.assertDictEqual(dset.features, Features({"text": Value("string"), "tokens": [Value("string")]}))
            self.assertListEqual(dset.column_names, ["text", "tokens"])
            del dset

        def _post_process(self, dataset, resources_paths):
            return dataset.select([0, 1], keep_in_memory=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder._post_process = types.MethodType(_post_process, builder)
            os.makedirs(builder.cache_dir)

            builder.info.splits = SplitDict()
            builder.info.splits.add(SplitInfo("train", num_examples=10))
            builder.info.splits.add(SplitInfo("test", num_examples=10))

            for split in builder.info.splits:
                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"{builder.dataset_name}-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 2})
                    writer.finalize()

            dsets = builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)
            self.assertListEqual(list(dsets.keys()), ["train", "test"])
            self.assertEqual(len(dsets["train"]), 2)
            self.assertEqual(len(dsets["test"]), 2)
            self.assertDictEqual(dsets["train"].features, Features({"text": Value("string")}))
            self.assertDictEqual(dsets["test"].features, Features({"text": Value("string")}))
            self.assertListEqual(dsets["train"].column_names, ["text"])
            self.assertListEqual(dsets["test"].column_names, ["text"])
            del dsets

            dset = builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 2)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            del dset

            dset = builder.as_dataset("train+test[:30%]")
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
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder._post_process = types.MethodType(_post_process, builder)
            builder._post_processing_resources = types.MethodType(_post_processing_resources, builder)
            os.makedirs(builder.cache_dir)

            builder.info.splits = SplitDict()
            builder.info.splits.add(SplitInfo("train", num_examples=10))
            builder.info.splits.add(SplitInfo("test", num_examples=10))

            for split in builder.info.splits:
                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"{builder.dataset_name}-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 10})
                    writer.finalize()

                with ArrowWriter(
                    path=os.path.join(builder.cache_dir, f"small_dataset-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                ) as writer:
                    writer.write_batch({"text": ["foo"] * 2})
                    writer.finalize()

            dsets = builder.as_dataset()
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
            self.assertGreater(builder.info.post_processing_size, 0)
            self.assertGreater(builder.info.post_processed.resources_checksums["train"]["index"]["num_bytes"], 0)
            del dsets

            dset = builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)
            self.assertEqual(dset.split, "train")
            self.assertEqual(len(dset), 10)
            self.assertDictEqual(dset.features, Features({"text": Value("string")}))
            self.assertListEqual(dset.column_names, ["text"])
            self.assertListEqual(dset.list_indexes(), ["my_index"])
            del dset

            dset = builder.as_dataset("train+test[:30%]")
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
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder.info.post_processed = PostProcessedInfo(
                features=Features({"text": Value("string"), "tokens": [Value("string")]})
            )
            builder._post_process = types.MethodType(_post_process, builder)
            builder._post_processing_resources = types.MethodType(_post_processing_resources, builder)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.arrow"
                    )
                )
            )
            self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
            self.assertDictEqual(
                builder.info.post_processed.features,
                Features({"text": Value("string"), "tokens": [Value("string")]}),
            )
            self.assertEqual(builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))
            )

        def _post_process(self, dataset, resources_paths):
            return dataset.select([0, 1], keep_in_memory=True)

        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder._post_process = types.MethodType(_post_process, builder)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.arrow"
                    )
                )
            )
            self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
            self.assertIsNone(builder.info.post_processed)
            self.assertEqual(builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))
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
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder._post_process = types.MethodType(_post_process, builder)
            builder._post_processing_resources = types.MethodType(_post_processing_resources, builder)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.arrow"
                    )
                )
            )
            self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
            self.assertIsNone(builder.info.post_processed)
            self.assertEqual(builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))
            )

    def test_error_download_and_prepare(self):
        def _prepare_split(self, split_generator, **kwargs):
            raise ValueError()

        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyBuilder(cache_dir=tmp_dir)
            builder._prepare_split = types.MethodType(_prepare_split, builder)
            self.assertRaises(
                ValueError,
                builder.download_and_prepare,
                download_mode=DownloadMode.FORCE_REDOWNLOAD,
            )
            self.assertRaises(FileNotFoundError, builder.as_dataset)

    def test_generator_based_download_and_prepare(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir)
            builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_dir,
                        builder.dataset_name,
                        "default",
                        "0.0.0",
                        f"{builder.dataset_name}-train.arrow",
                    )
                )
            )
            self.assertDictEqual(builder.info.features, Features({"text": Value("string")}))
            self.assertEqual(builder.info.splits["train"].num_examples, 100)
            self.assertTrue(
                os.path.exists(os.path.join(tmp_dir, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))
            )

        # Test that duplicated keys are ignored if verification_mode is "no_checks"
        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir)
            with patch("datasets.builder.ArrowWriter", side_effect=ArrowWriter) as mock_arrow_writer:
                builder.download_and_prepare(
                    download_mode=DownloadMode.FORCE_REDOWNLOAD, verification_mode=VerificationMode.NO_CHECKS
                )
                mock_arrow_writer.assert_called_once()
                args, kwargs = mock_arrow_writer.call_args_list[0]
                self.assertFalse(kwargs["check_duplicates"])

                mock_arrow_writer.reset_mock()

                builder.download_and_prepare(
                    download_mode=DownloadMode.FORCE_REDOWNLOAD, verification_mode=VerificationMode.BASIC_CHECKS
                )
                mock_arrow_writer.assert_called_once()
                args, kwargs = mock_arrow_writer.call_args_list[0]
                self.assertTrue(kwargs["check_duplicates"])

    def test_cache_dir_no_args(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_dir=None, data_files=None)
            relative_cache_dir_parts = Path(builder._relative_data_dir()).parts
            self.assertTupleEqual(relative_cache_dir_parts, (builder.dataset_name, "default", "0.0.0"))

    def test_cache_dir_for_data_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_data1 = os.path.join(tmp_dir, "dummy_data1.txt")
            with open(dummy_data1, "w", encoding="utf-8") as f:
                f.writelines("foo bar")
            dummy_data2 = os.path.join(tmp_dir, "dummy_data2.txt")
            with open(dummy_data2, "w", encoding="utf-8") as f:
                f.writelines("foo bar\n")

            builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=dummy_data1)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=dummy_data1)
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data1])
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files={"train": dummy_data1})
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files={Split.TRAIN: dummy_data1})
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files={"train": [dummy_data1]})
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files={"test": dummy_data1})
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=dummy_data2)
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data2])
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data1, dummy_data2])
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

            builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data1, dummy_data2])
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data1, dummy_data2])
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(cache_dir=tmp_dir, data_files=[dummy_data2, dummy_data1])
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

            builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, data_files={"train": dummy_data1, "test": dummy_data2}
            )
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, data_files={"train": dummy_data1, "test": dummy_data2}
            )
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, data_files={"train": [dummy_data1], "test": dummy_data2}
            )
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir, data_files={"train": dummy_data1, "validation": dummy_data2}
            )
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilder(
                cache_dir=tmp_dir,
                data_files={"train": [dummy_data1, dummy_data2], "test": dummy_data2},
            )
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

    def test_cache_dir_for_features(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            f1 = Features({"id": Value("int8")})
            f2 = Features({"id": Value("int32")})
            builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, features=f1)
            other_builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, features=f1)
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithIntegers(cache_dir=tmp_dir, features=f2)
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

    def test_cache_dir_for_config_kwargs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # create config on the fly
            builder = DummyGeneratorBasedBuilderWithConfig(cache_dir=tmp_dir, content="foo", times=2)
            other_builder = DummyGeneratorBasedBuilderWithConfig(cache_dir=tmp_dir, times=2, content="foo")
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            self.assertIn("content=foo", builder.cache_dir)
            self.assertIn("times=2", builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithConfig(cache_dir=tmp_dir, content="bar", times=2)
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyGeneratorBasedBuilderWithConfig(cache_dir=tmp_dir, content="foo")
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

        with tempfile.TemporaryDirectory() as tmp_dir:
            # overwrite an existing config
            builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="a", content="foo", times=2)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="a", times=2, content="foo")
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            self.assertIn("content=foo", builder.cache_dir)
            self.assertIn("times=2", builder.cache_dir)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="a", content="bar", times=2)
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="a", content="foo")
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

    def test_config_names(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(ValueError) as error_context:
                DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, data_files=None, data_dir=None)
            self.assertIn("Please pick one among the available configs", str(error_context.exception))

            builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="a")
            self.assertEqual(builder.config.name, "a")

            builder = DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir, config_name="b")
            self.assertEqual(builder.config.name, "b")

            with self.assertRaises(ValueError):
                DummyBuilderWithMultipleConfigs(cache_dir=tmp_dir)

            builder = DummyBuilderWithDefaultConfig(cache_dir=tmp_dir)
            self.assertEqual(builder.config.name, "a")

    def test_cache_dir_for_data_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir, tempfile.TemporaryDirectory() as data_dir:
            builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, config_name="a", data_dir=data_dir)
            other_builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, config_name="a", data_dir=data_dir)
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = DummyBuilderWithManualDownload(cache_dir=tmp_dir, config_name="a", data_dir=tmp_dir)
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)

    def test_cache_dir_for_configured_builder(self):
        with tempfile.TemporaryDirectory() as tmp_dir, tempfile.TemporaryDirectory() as data_dir:
            builder_cls = configure_builder_class(
                DummyBuilderWithManualDownload,
                builder_configs=[BuilderConfig(data_dir=data_dir)],
                default_config_name=None,
                dataset_name="dummy",
            )
            builder = builder_cls(cache_dir=tmp_dir, hash="abc")
            other_builder = builder_cls(cache_dir=tmp_dir, hash="abc")
            self.assertEqual(builder.cache_dir, other_builder.cache_dir)
            other_builder = builder_cls(cache_dir=tmp_dir, hash="def")
            self.assertNotEqual(builder.cache_dir, other_builder.cache_dir)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = BuilderConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = BuilderConfig(name="name", data_files=data_files)


def test_arrow_based_download_and_prepare(tmp_path):
    builder = DummyArrowBasedBuilder(cache_dir=tmp_path)
    builder.download_and_prepare()
    assert os.path.exists(
        os.path.join(
            tmp_path,
            builder.dataset_name,
            "default",
            "0.0.0",
            f"{builder.dataset_name}-train.arrow",
        )
    )
    assert builder.info.features, Features({"text": Value("string")})
    assert builder.info.splits["train"].num_examples == 100
    assert os.path.exists(os.path.join(tmp_path, builder.dataset_name, "default", "0.0.0", "dataset_info.json"))


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
    builder = DummyBuilder(cache_dir=cache_dir)
    os.makedirs(builder.cache_dir)

    builder.info.splits = SplitDict()
    builder.info.splits.add(SplitInfo("train", num_examples=10))
    builder.info.splits.add(SplitInfo("test", num_examples=10))

    for info_split in builder.info.splits:
        with ArrowWriter(
            path=os.path.join(builder.cache_dir, f"{builder.dataset_name}-{info_split}.arrow"),
            features=Features({"text": Value("string")}),
        ) as writer:
            writer.write_batch({"text": ["foo"] * 10})
            writer.finalize()

    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset = builder.as_dataset(split=split, in_memory=in_memory)
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
    builder = DummyGeneratorBasedBuilder(cache_dir=cache_dir)
    builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
    with assert_arrow_memory_increases() if in_memory else assert_arrow_memory_doesnt_increase():
        dataset = builder.as_dataset("train", in_memory=in_memory)
    assert dataset.data.to_pydict() == {"text": ["foo"] * 100}


@pytest.mark.parametrize(
    "writer_batch_size, default_writer_batch_size, expected_chunks", [(None, None, 1), (None, 5, 20), (10, None, 10)]
)
def test_custom_writer_batch_size(tmp_path, writer_batch_size, default_writer_batch_size, expected_chunks):
    cache_dir = str(tmp_path)
    if default_writer_batch_size:
        DummyGeneratorBasedBuilder.DEFAULT_WRITER_BATCH_SIZE = default_writer_batch_size
    builder = DummyGeneratorBasedBuilder(cache_dir=cache_dir, writer_batch_size=writer_batch_size)
    assert builder._writer_batch_size == (writer_batch_size or default_writer_batch_size)
    builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
    dataset = builder.as_dataset("train")
    assert len(dataset.data[0].chunks) == expected_chunks


def test_builder_as_streaming_dataset(tmp_path):
    dummy_builder = DummyGeneratorBasedBuilder(cache_dir=str(tmp_path))
    check_streaming(dummy_builder)
    dsets = dummy_builder.as_streaming_dataset()
    assert isinstance(dsets, IterableDatasetDict)
    assert isinstance(dsets["train"], IterableDataset)
    assert len(list(dsets["train"])) == 100
    dset = dummy_builder.as_streaming_dataset(split="train")
    assert isinstance(dset, IterableDataset)
    assert len(list(dset)) == 100


def _run_test_builder_streaming_works_in_subprocesses(builder):
    check_streaming(builder)
    dset = builder.as_streaming_dataset(split="train")
    assert isinstance(dset, IterableDataset)
    assert len(list(dset)) == 100


def test_builder_streaming_works_in_subprocess(tmp_path):
    dummy_builder = DummyGeneratorBasedBuilder(cache_dir=str(tmp_path))
    p = Process(target=_run_test_builder_streaming_works_in_subprocesses, args=(dummy_builder,))
    p.start()
    p.join()


class DummyBuilderWithVersion(GeneratorBasedBuilder):
    VERSION = "2.0.0"

    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        pass

    def _generate_examples(self):
        pass


class DummyBuilderWithBuilderConfigs(GeneratorBasedBuilder):
    BUILDER_CONFIGS = [BuilderConfig(name="custom", version="2.0.0")]

    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        pass

    def _generate_examples(self):
        pass


class CustomBuilderConfig(BuilderConfig):
    def __init__(self, date=None, language=None, version="2.0.0", **kwargs):
        name = f"{date}.{language}"
        super().__init__(name=name, version=version, **kwargs)
        self.date = date
        self.language = language


class DummyBuilderWithCustomBuilderConfigs(GeneratorBasedBuilder):
    BUILDER_CONFIGS = [CustomBuilderConfig(date="20220501", language="en")]
    BUILDER_CONFIG_CLASS = CustomBuilderConfig

    def _info(self):
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        pass

    def _generate_examples(self):
        pass


@pytest.mark.parametrize(
    "builder_class, kwargs",
    [
        (DummyBuilderWithVersion, {}),
        (DummyBuilderWithBuilderConfigs, {"config_name": "custom"}),
        (DummyBuilderWithCustomBuilderConfigs, {"config_name": "20220501.en"}),
        (DummyBuilderWithCustomBuilderConfigs, {"date": "20220501", "language": "ca"}),
    ],
)
def test_builder_config_version(builder_class, kwargs, tmp_path):
    cache_dir = str(tmp_path)
    builder = builder_class(cache_dir=cache_dir, **kwargs)
    assert builder.config.version == "2.0.0"


def test_builder_download_and_prepare_with_absolute_output_dir(tmp_path):
    builder = DummyGeneratorBasedBuilder()
    output_dir = str(tmp_path)
    builder.download_and_prepare(output_dir)
    assert builder._output_dir.startswith(tmp_path.resolve().as_posix())
    assert os.path.exists(os.path.join(output_dir, "dataset_info.json"))
    assert os.path.exists(os.path.join(output_dir, f"{builder.dataset_name}-train.arrow"))
    assert not os.path.exists(os.path.join(output_dir + ".incomplete"))


def test_builder_download_and_prepare_with_relative_output_dir():
    with set_current_working_directory_to_temp_dir():
        builder = DummyGeneratorBasedBuilder()
        output_dir = "test-out"
        builder.download_and_prepare(output_dir)
        assert Path(builder._output_dir).resolve().as_posix().startswith(Path(output_dir).resolve().as_posix())
        assert os.path.exists(os.path.join(output_dir, "dataset_info.json"))
        assert os.path.exists(os.path.join(output_dir, f"{builder.dataset_name}-train.arrow"))
        assert not os.path.exists(os.path.join(output_dir + ".incomplete"))


def test_builder_with_filesystem_download_and_prepare(tmp_path, mockfs):
    builder = DummyGeneratorBasedBuilder(cache_dir=tmp_path)
    builder.download_and_prepare("mock://my_dataset", storage_options=mockfs.storage_options)
    assert builder._output_dir.startswith("mock://my_dataset")
    assert is_local_path(builder._cache_downloaded_dir)
    assert isinstance(builder._fs, type(mockfs))
    assert builder._fs.storage_options == mockfs.storage_options
    assert mockfs.exists("my_dataset/dataset_info.json")
    assert mockfs.exists(f"my_dataset/{builder.dataset_name}-train.arrow")
    assert not mockfs.exists("my_dataset.incomplete")


def test_builder_with_filesystem_download_and_prepare_reload(tmp_path, mockfs, caplog):
    builder = DummyGeneratorBasedBuilder(cache_dir=tmp_path)
    mockfs.makedirs("my_dataset")
    DatasetInfo().write_to_directory("mock://my_dataset", storage_options=mockfs.storage_options)
    mockfs.touch(f"my_dataset/{builder.dataset_name}-train.arrow")
    caplog.clear()
    with caplog.at_level(INFO, logger=get_logger().name):
        builder.download_and_prepare("mock://my_dataset", storage_options=mockfs.storage_options)
    assert "Found cached dataset" in caplog.text


def test_generator_based_builder_download_and_prepare_as_parquet(tmp_path):
    builder = DummyGeneratorBasedBuilder(cache_dir=tmp_path)
    builder.download_and_prepare(file_format="parquet")
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.parquet"
    )
    assert os.path.exists(parquet_path)
    assert pq.ParquetFile(parquet_path) is not None


def test_generator_based_builder_download_and_prepare_sharded(tmp_path):
    writer_batch_size = 25
    builder = DummyGeneratorBasedBuilder(cache_dir=tmp_path, writer_batch_size=writer_batch_size)
    with patch("datasets.config.MAX_SHARD_SIZE", 1):  # one batch per shard
        builder.download_and_prepare(file_format="parquet")
    expected_num_shards = 100 // writer_batch_size
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.parquet",
    )
    assert os.path.exists(parquet_path)
    parquet_files = [
        pq.ParquetFile(parquet_path)
        for parquet_path in Path(tmp_path).rglob(
            f"{builder.dataset_name}-train-*-of-{expected_num_shards:05d}.parquet"
        )
    ]
    assert len(parquet_files) == expected_num_shards
    assert sum(parquet_file.metadata.num_rows for parquet_file in parquet_files) == 100


def test_generator_based_builder_download_and_prepare_with_max_shard_size(tmp_path):
    writer_batch_size = 25
    builder = DummyGeneratorBasedBuilder(cache_dir=tmp_path, writer_batch_size=writer_batch_size)
    builder.download_and_prepare(file_format="parquet", max_shard_size=1)  # one batch per shard
    expected_num_shards = 100 // writer_batch_size
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.parquet",
    )
    assert os.path.exists(parquet_path)
    parquet_files = [
        pq.ParquetFile(parquet_path)
        for parquet_path in Path(tmp_path).rglob(
            f"{builder.dataset_name}-train-*-of-{expected_num_shards:05d}.parquet"
        )
    ]
    assert len(parquet_files) == expected_num_shards
    assert sum(parquet_file.metadata.num_rows for parquet_file in parquet_files) == 100


def test_generator_based_builder_download_and_prepare_with_num_proc(tmp_path):
    builder = DummyGeneratorBasedBuilderWithShards(cache_dir=tmp_path)
    builder.download_and_prepare(num_proc=2)
    expected_num_shards = 2
    assert builder.info.splits["train"].num_examples == 400
    assert builder.info.splits["train"].shard_lengths == [200, 200]
    arrow_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.arrow",
    )
    assert os.path.exists(arrow_path)
    ds = builder.as_dataset("train")
    assert len(ds) == 400
    assert ds.to_dict() == {
        "id": [i for _ in range(4) for i in range(100)],
        "filepath": [f"data{i}.txt" for i in range(4) for _ in range(100)],
    }


@pytest.mark.parametrize(
    "num_proc, expectation", [(None, does_not_raise()), (1, does_not_raise()), (2, pytest.raises(RuntimeError))]
)
def test_generator_based_builder_download_and_prepare_with_ambiguous_shards(num_proc, expectation, tmp_path):
    builder = DummyGeneratorBasedBuilderWithAmbiguousShards(cache_dir=tmp_path)
    with expectation:
        builder.download_and_prepare(num_proc=num_proc)


def test_arrow_based_builder_download_and_prepare_as_parquet(tmp_path):
    builder = DummyArrowBasedBuilder(cache_dir=tmp_path)
    builder.download_and_prepare(file_format="parquet")
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path, builder.dataset_name, "default", "0.0.0", f"{builder.dataset_name}-train.parquet"
    )
    assert os.path.exists(parquet_path)
    assert pq.ParquetFile(parquet_path) is not None


def test_arrow_based_builder_download_and_prepare_sharded(tmp_path):
    builder = DummyArrowBasedBuilder(cache_dir=tmp_path)
    with patch("datasets.config.MAX_SHARD_SIZE", 1):  # one batch per shard
        builder.download_and_prepare(file_format="parquet")
    expected_num_shards = 10
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.parquet",
    )
    assert os.path.exists(parquet_path)
    parquet_files = [
        pq.ParquetFile(parquet_path)
        for parquet_path in Path(tmp_path).rglob(
            f"{builder.dataset_name}-train-*-of-{expected_num_shards:05d}.parquet"
        )
    ]
    assert len(parquet_files) == expected_num_shards
    assert sum(parquet_file.metadata.num_rows for parquet_file in parquet_files) == 100


def test_arrow_based_builder_download_and_prepare_with_max_shard_size(tmp_path):
    builder = DummyArrowBasedBuilder(cache_dir=tmp_path)
    builder.download_and_prepare(file_format="parquet", max_shard_size=1)  # one table per shard
    expected_num_shards = 10
    assert builder.info.splits["train"].num_examples == 100
    parquet_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.parquet",
    )
    assert os.path.exists(parquet_path)
    parquet_files = [
        pq.ParquetFile(parquet_path)
        for parquet_path in Path(tmp_path).rglob(
            f"{builder.dataset_name}-train-*-of-{expected_num_shards:05d}.parquet"
        )
    ]
    assert len(parquet_files) == expected_num_shards
    assert sum(parquet_file.metadata.num_rows for parquet_file in parquet_files) == 100


def test_arrow_based_builder_download_and_prepare_with_num_proc(tmp_path):
    builder = DummyArrowBasedBuilderWithShards(cache_dir=tmp_path)
    builder.download_and_prepare(num_proc=2)
    expected_num_shards = 2
    assert builder.info.splits["train"].num_examples == 400
    assert builder.info.splits["train"].shard_lengths == [200, 200]
    arrow_path = os.path.join(
        tmp_path,
        builder.dataset_name,
        "default",
        "0.0.0",
        f"{builder.dataset_name}-train-00000-of-{expected_num_shards:05d}.arrow",
    )
    assert os.path.exists(arrow_path)
    ds = builder.as_dataset("train")
    assert len(ds) == 400
    assert ds.to_dict() == {
        "id": [i for _ in range(4) for i in range(100)],
        "filepath": [f"data{i}.txt" for i in range(4) for _ in range(100)],
    }


@pytest.mark.parametrize(
    "num_proc, expectation", [(None, does_not_raise()), (1, does_not_raise()), (2, pytest.raises(RuntimeError))]
)
def test_arrow_based_builder_download_and_prepare_with_ambiguous_shards(num_proc, expectation, tmp_path):
    builder = DummyArrowBasedBuilderWithAmbiguousShards(cache_dir=tmp_path)
    with expectation:
        builder.download_and_prepare(num_proc=num_proc)
