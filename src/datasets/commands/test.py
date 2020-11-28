import os
from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile, rmtree
from typing import Generator

from datasets.builder import FORCE_REDOWNLOAD, REUSE_CACHE_IF_EXISTS, DatasetBuilder
from datasets.commands import BaseTransformersCLICommand
from datasets.info import DATASET_INFOS_DICT_FILE_NAME
from datasets.load import import_main_class, prepare_module
from datasets.utils.logging import get_logger


logger = get_logger(__name__)


def test_command_factory(args):
    return TestCommand(
        args.dataset,
        args.name,
        args.cache_dir,
        args.data_dir,
        args.all_configs,
        args.save_infos,
        args.ignore_verifications,
        args.force_redownload,
        args.clear_cache,
    )


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--name", type=str, default=None, help="Dataset processing name")
        test_parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="Cache directory where the datasets are stored.",
        )
        test_parser.add_argument(
            "--data_dir",
            type=str,
            default=None,
            help="Can be used to specify a manual directory to get the files from.",
        )
        test_parser.add_argument("--all_configs", action="store_true", help="Test all dataset configurations")
        test_parser.add_argument("--save_infos", action="store_true", help="Save the dataset infos file")
        test_parser.add_argument(
            "--ignore_verifications", action="store_true", help="Run the test without checksums and splits checks"
        )
        test_parser.add_argument("--force_redownload", action="store_true", help="Force dataset redownload")
        test_parser.add_argument(
            "--clear_cache",
            action="store_true",
            help="Remove downloaded files and cached datasets after each config test",
        )
        test_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self,
        dataset: str,
        name: str,
        cache_dir: str,
        data_dir: str,
        all_configs: bool,
        save_infos: bool,
        ignore_verifications: bool,
        force_redownload: bool,
        clear_cache: bool,
    ):
        self._dataset = dataset
        self._name = name
        self._cache_dir = cache_dir
        self._data_dir = data_dir
        self._all_configs = all_configs
        self._save_infos = save_infos
        self._ignore_verifications = ignore_verifications
        self._force_redownload = force_redownload
        self._clear_cache = clear_cache
        if clear_cache and not cache_dir:
            print(
                "When --clear_cache is used, specifying a cache directory is mandatory.\n"
                "The 'download' folder of the cache directory and the dataset builder cache will be deleted after each configuration test.\n"
                "Please provide a --cache_dir that will be used to test the dataset script."
            )
            exit(1)

    def run(self):
        if self._name is not None and self._all_configs:
            print("Both parameters `config` and `all_configs` can't be used at once.")
            exit(1)
        path, name = self._dataset, self._name
        module_path, hash = prepare_module(path)
        builder_cls = import_main_class(module_path)

        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            n_builders = len(builder_cls.BUILDER_CONFIGS)
        else:
            n_builders = 1

        def get_builders() -> Generator[DatasetBuilder, None, None]:
            if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
                for config in builder_cls.BUILDER_CONFIGS:
                    yield builder_cls(name=config.name, hash=hash, cache_dir=self._cache_dir, data_dir=self._data_dir)
            else:
                yield builder_cls(name=name, hash=hash, cache_dir=self._cache_dir, data_dir=self._data_dir)

        for i, builder in enumerate(get_builders()):
            print(f"Testing builder '{builder.config.name}' ({i + 1}/{n_builders})")
            builder.download_and_prepare(
                download_mode=REUSE_CACHE_IF_EXISTS if not self._force_redownload else FORCE_REDOWNLOAD,
                ignore_verifications=self._ignore_verifications,
                try_from_hf_gcs=False,
            )
            builder.as_dataset()
            if self._save_infos:
                builder._save_infos()

            # If save_infos=True, the dataset infos file is created next to the loaded module file.
            # Let's move it to the original directory of the dataset script, to allow the user to
            # upload them on S3 at the same time afterwards.
            if self._save_infos:
                dataset_infos_path = os.path.join(builder_cls.get_imported_module_dir(), DATASET_INFOS_DICT_FILE_NAME)
                name = Path(path).name + ".py"
                combined_path = os.path.join(path, name)
                if os.path.isfile(path):
                    dataset_dir = os.path.dirname(path)
                elif os.path.isfile(combined_path):
                    dataset_dir = path
                else:  # in case of a remote dataset
                    dataset_dir = None
                    print("Dataset Infos file saved at {}".format(dataset_infos_path))

                # Move dataset_info back to the user
                if dataset_dir is not None:
                    user_dataset_infos_path = os.path.join(dataset_dir, DATASET_INFOS_DICT_FILE_NAME)
                    copyfile(dataset_infos_path, user_dataset_infos_path)
                    print("Dataset Infos file saved at {}".format(user_dataset_infos_path))

            # If clear_cache=True, the download forlder and the dataset builder cache directory are deleted
            if self._clear_cache:
                if os.path.isdir(builder._cache_dir):
                    logger.warning(f"Clearing cache at {builder._cache_dir}")
                    rmtree(builder._cache_dir)
                download_dir = os.path.join(self._cache_dir, "downloads")
                if os.path.isdir(download_dir):
                    logger.warning(f"Clearing cache at {download_dir}")
                    rmtree(download_dir)

        print("Test successful.")
