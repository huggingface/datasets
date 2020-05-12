import os
from argparse import ArgumentParser
from shutil import copyfile
from typing import List

from nlp.builder import FORCE_REDOWNLOAD, REUSE_CACHE_IF_EXISTS, DatasetBuilder
from nlp.commands import BaseTransformersCLICommand
from nlp.load import import_main_class, prepare_module
from nlp.utils.checksums_utils import CACHED_SIZES_FILE_NAME, CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME


def test_command_factory(args):
    return TestCommand(
        args.dataset, args.config, args.all_configs, args.save_checksums, args.ignore_checksums, args.force_redownload
    )


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--config", type=str, default=None, help="Dataset processing config")
        test_parser.add_argument("--all_configs", action="store_true", help="Test all dataset configurations")
        test_parser.add_argument(
            "--save_checksums", action="store_true", help="Save the checksums file and cached file sizes"
        )
        test_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        test_parser.add_argument("--force_redownload", action="store_true", help="Force dataset redownload")
        test_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self,
        dataset: str,
        config: str,
        all_configs: bool,
        save_checksums: bool,
        ignore_checksums: bool,
        force_redownload: bool,
    ):
        self._dataset = dataset
        self._config = config
        self._all_configs = all_configs
        self._save_checksums = save_checksums
        self._ignore_checksums = ignore_checksums
        self._force_redownload = force_redownload

    def run(self):
        if self._config is not None and self._all_configs:
            print("Both parameters `config` and `all_configs` can't be used at once.")
            exit(1)
        path, config = self._dataset, self._config
        module_path = prepare_module(path)
        builder_cls = import_main_class(module_path)
        builders: List[DatasetBuilder] = []
        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            for config in builder_cls.BUILDER_CONFIGS:
                builders.append(builder_cls(config=config))
        else:
            builders.append(builder_cls(config=config))

        for builder in builders:
            builder.download_and_prepare(
                download_mode=REUSE_CACHE_IF_EXISTS if not self._force_redownload else FORCE_REDOWNLOAD,
                save_checksums=self._save_checksums,
                ignore_checksums=self._ignore_checksums,
            )

        print("Test successful.")
        # If save_checksums=True, the checksums file is created next to the loaded module file.
        # Let's move it to the original directory of the dataset script, to allow the user to
        # upload them on S3 at the same time afterwards.
        if self._save_checksums:
            urls_checksums_dir = os.path.join(builder_cls.get_imported_module_dir(), URLS_CHECKSUMS_FOLDER_NAME)
            checksums_file_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)
            cached_sizes_file_path = os.path.join(urls_checksums_dir, CACHED_SIZES_FILE_NAME)

            name = list(filter(lambda x: x, path.split("/")))[-1] + ".py"

            combined_path = os.path.join(path, name)
            if os.path.isfile(path):
                dataset_dir = os.path.dirname(path)
            elif os.path.isfile(combined_path):
                dataset_dir = path
            else:  # in case of a remote dataset
                print("Checksums file saved at {}".format(checksums_file_path))
                exit(1)

            user_urls_checksums_dir = os.path.join(dataset_dir, URLS_CHECKSUMS_FOLDER_NAME)
            user_checksums_file_path = os.path.join(user_urls_checksums_dir, CHECKSUMS_FILE_NAME)
            user_cached_sizes_file_path = os.path.join(user_urls_checksums_dir, CACHED_SIZES_FILE_NAME)
            os.makedirs(user_urls_checksums_dir, exist_ok=True)
            copyfile(checksums_file_path, user_checksums_file_path)
            copyfile(cached_sizes_file_path, user_cached_sizes_file_path)
            print("Checksums file saved at {}".format(user_checksums_file_path))
