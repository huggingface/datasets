import logging
import os
from argparse import ArgumentParser
from collections.abc import Generator
from shutil import rmtree

import datasets.config
from datasets.builder import DatasetBuilder
from datasets.commands import BaseDatasetsCLICommand
from datasets.download.download_manager import DownloadMode
from datasets.info import DatasetInfosDict
from datasets.load import dataset_module_factory, get_dataset_builder_class
from datasets.utils.info_utils import VerificationMode
from datasets.utils.logging import ERROR, get_logger


logger = get_logger(__name__)


def _test_command_factory(args):
    return TestCommand(
        args.dataset,
        args.name,
        args.cache_dir,
        args.data_dir,
        args.all_configs,
        args.save_info or args.save_infos,
        args.ignore_verifications,
        args.force_redownload,
        args.clear_cache,
        args.num_proc,
    )


class TestCommand(BaseDatasetsCLICommand):
    __test__ = False  # to tell pytest it's not a test class

    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test", help="Test dataset loading.")
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
        test_parser.add_argument(
            "--save_info", action="store_true", help="Save the dataset infos in the dataset card (README.md)"
        )
        test_parser.add_argument(
            "--ignore_verifications",
            action="store_true",
            help="Run the test without checksums and splits checks.",
        )
        test_parser.add_argument("--force_redownload", action="store_true", help="Force dataset redownload")
        test_parser.add_argument(
            "--clear_cache",
            action="store_true",
            help="Remove downloaded files and cached datasets after each config test",
        )
        test_parser.add_argument("--num_proc", type=int, default=None, help="Number of processes")
        # aliases
        test_parser.add_argument("--save_infos", action="store_true", help="alias to save_info")
        test_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=_test_command_factory)

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
        num_proc: int,
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
        self._num_proc = num_proc
        if clear_cache and not cache_dir:
            print(
                "When --clear_cache is used, specifying a cache directory is mandatory.\n"
                "The 'download' folder of the cache directory and the dataset builder cache will be deleted after each configuration test.\n"
                "Please provide a --cache_dir that will be used to test the dataset."
            )
            exit(1)
        if save_infos:
            self._ignore_verifications = True

    def run(self):
        logging.getLogger("filelock").setLevel(ERROR)
        if self._name is not None and self._all_configs:
            print("Both parameters `config` and `all_configs` can't be used at once.")
            exit(1)
        path, config_name = self._dataset, self._name
        module = dataset_module_factory(path)
        builder_cls = get_dataset_builder_class(module)
        n_builders = len(builder_cls.BUILDER_CONFIGS) if self._all_configs and builder_cls.BUILDER_CONFIGS else 1

        def get_builders() -> Generator[DatasetBuilder, None, None]:
            if self._all_configs and builder_cls.BUILDER_CONFIGS:
                for i, config in enumerate(builder_cls.BUILDER_CONFIGS):
                    if "config_name" in module.builder_kwargs:
                        yield builder_cls(
                            cache_dir=self._cache_dir,
                            data_dir=self._data_dir,
                            **module.builder_kwargs,
                        )
                    else:
                        yield builder_cls(
                            config_name=config.name,
                            cache_dir=self._cache_dir,
                            data_dir=self._data_dir,
                            **module.builder_kwargs,
                        )
            else:
                if "config_name" in module.builder_kwargs:
                    yield builder_cls(cache_dir=self._cache_dir, data_dir=self._data_dir, **module.builder_kwargs)
                else:
                    yield builder_cls(
                        config_name=config_name,
                        cache_dir=self._cache_dir,
                        data_dir=self._data_dir,
                        **module.builder_kwargs,
                    )

        for j, builder in enumerate(get_builders()):
            print(f"Testing builder '{builder.config.name}' ({j + 1}/{n_builders})")
            builder._record_infos = os.path.exists(
                os.path.join(builder.get_imported_module_dir(), datasets.config.DATASETDICT_INFOS_FILENAME)
            )  # record checksums only if we need to update a (deprecated) dataset_infos.json
            builder.download_and_prepare(
                download_mode=DownloadMode.REUSE_CACHE_IF_EXISTS
                if not self._force_redownload
                else DownloadMode.FORCE_REDOWNLOAD,
                verification_mode=VerificationMode.NO_CHECKS
                if self._ignore_verifications
                else VerificationMode.ALL_CHECKS,
                num_proc=self._num_proc,
            )
            builder.as_dataset()

            # If save_infos=True, we create the dataset card (README.md)
            # The dataset_infos are saved in the YAML part of the README.md
            # This is to allow the user to upload them on HF afterwards.
            if self._save_infos:
                save_infos_dir = os.path.basename(path) if not os.path.isdir(path) else path
                os.makedirs(save_infos_dir, exist_ok=True)
                DatasetInfosDict(**{builder.config.name: builder.info}).write_to_directory(save_infos_dir)
                print(f"Dataset card saved at {os.path.join(save_infos_dir, datasets.config.REPOCARD_FILENAME)}")

            # If clear_cache=True, the download folder and the dataset builder cache directory are deleted
            if self._clear_cache:
                if os.path.isdir(builder._cache_dir):
                    logger.warning(f"Clearing cache at {builder._cache_dir}")
                    rmtree(builder._cache_dir)
                download_dir = os.path.join(self._cache_dir, datasets.config.DOWNLOADED_DATASETS_DIR)
                if os.path.isdir(download_dir):
                    logger.warning(f"Clearing cache at {download_dir}")
                    rmtree(download_dir)

        print("Test successful.")
