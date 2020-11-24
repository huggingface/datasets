import os
import shutil
from tempfile import TemporaryDirectory
from unittest import TestCase

from datasets.builder import DatasetInfo, DownloadConfig, GeneratorBasedBuilder, Split, SplitGenerator
from datasets.commands.dummy_data import DummyDataGeneratorDownloadManager, MockDownloadManager
from datasets.features import Features, Value
from datasets.utils.version import Version


class DummyBuilder(GeneratorBasedBuilder):
    def __init__(self, tmp_test_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmp_test_dir = tmp_test_dir

    def _info(self) -> DatasetInfo:
        return DatasetInfo(features=Features({"text": Value("string")}))

    def _split_generators(self, dl_manager):
        to_dl = {
            "train": os.path.abspath(os.path.join(self.tmp_test_dir, "train.txt")),
            "test": os.path.abspath(os.path.join(self.tmp_test_dir, "test.txt")),
        }
        downloaded_files = dl_manager.download_and_extract(to_dl)
        return [
            SplitGenerator(Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            SplitGenerator(Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath, **kwargs):
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                yield i, {"text": line.strip()}


class DummyDataAutoGenerationTest(TestCase):
    def test_dummy_data_autogenerate(self):
        n_lines = 5

        with TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, "train.txt"), "w", encoding="utf-8") as f:
                f.write("foo\nbar\n" * 10)
            with open(os.path.join(tmp_dir, "test.txt"), "w", encoding="utf-8") as f:
                f.write("foo\nbar\n" * 10)

            class MockDownloadManagerWithCustomDatasetsScriptsDir(MockDownloadManager):
                datasets_scripts_dir = os.path.join(tmp_dir, "datasets")

            cache_dir = os.path.join(tmp_dir, "cache")
            os.makedirs(cache_dir, exist_ok=True)
            dataset_builder = DummyBuilder(tmp_test_dir=tmp_dir, cache_dir=cache_dir)
            mock_dl_manager = MockDownloadManagerWithCustomDatasetsScriptsDir(
                dataset_name=dataset_builder.name,
                config=None,
                version=Version("0.0.0"),
                is_local=True,
                cache_dir=cache_dir,
                load_existing_dummy_data=False,  # dummy data don't exist yet
            )
            download_config = DownloadConfig(cache_dir=os.path.join(tmp_dir, "downloads"))
            dl_manager = DummyDataGeneratorDownloadManager(
                dataset_name=dataset_builder.name,
                mock_download_manager=mock_dl_manager,
                download_config=download_config,
            )
            dataset_builder.download_and_prepare(dl_manager=dl_manager)
            shutil.rmtree(dataset_builder._cache_dir)

            dl_manager.auto_generate_dummy_data_folder(n_lines=n_lines)
            path_do_dataset = os.path.join(mock_dl_manager.datasets_scripts_dir, mock_dl_manager.dataset_name)
            dl_manager.compress_autogenerated_dummy_data(path_do_dataset)

            mock_dl_manager.load_existing_dummy_data = True
            dataset_builder.download_and_prepare(dl_manager=mock_dl_manager, ignore_verifications=True)
            dataset = dataset_builder.as_dataset(split="train")
            self.assertEqual(len(dataset), n_lines)
            del dataset
