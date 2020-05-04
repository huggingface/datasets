import os
from argparse import ArgumentParser
from shutil import copyfile
from typing import List

from nlp.builder import REUSE_CACHE_IF_EXISTS, DatasetBuilder
from nlp.commands import BaseTransformersCLICommand
from nlp.load import _dataset_name_and_kwargs_from_name_str, load_dataset_module
from nlp.utils import DownloadConfig
from nlp.utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME


def test_command_factory(args):
    return TestCommand(args.dataset, args.name, args.all_configs, args.save_checksums, args.ignore_checksums,)


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--name", type=str, default=None, help="Dataset processing name")
        test_parser.add_argument("--all_configs", action="store_true", help="Test all dataset configurations")
        test_parser.add_argument("--save_checksums", action="store_true", help="Save the checksums file on S3")
        test_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        test_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self, dataset: str, name: str, all_configs: bool, save_checksums: bool, ignore_checksums: bool,
    ):
        self._dataset = dataset
        self._name = name
        self._all_configs = all_configs
        self._save_checksums = save_checksums
        self._ignore_checksums = ignore_checksums

    def run(self):
        if self._name is not None:
            name, builder_kwargs = _dataset_name_and_kwargs_from_name_str(self._name)
            if self._all_configs:
                print("Both parameters `name` and `all_configs` can't be used at once.")
        else:
            name, builder_kwargs = self._name, {}
        builder_cls = load_dataset_module(self._dataset, name=name)
        builders: List[DatasetBuilder] = []
        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            for config in builder_cls.BUILDER_CONFIGS:
                configured_builder_kwargs = builder_kwargs.copy()
                configured_builder_kwargs["config"] = config
                builders.append(builder_cls(**configured_builder_kwargs))
        else:
            builders.append(builder_cls(**builder_kwargs))

        for builder in builders:
            builder.download_and_prepare(
                download_config=DownloadConfig(
                    download_mode=REUSE_CACHE_IF_EXISTS,
                    save_checksums=self._save_checksums,
                    ignore_checksums=self._ignore_checksums,
                )
            )

        print("Test successful.")
        # If save_checksums=True, the checksums file is created next to the loaded module file.
        # Let's move it to the original directory of the dataset script, to allow the user to
        # upload them on S3 at the same time afterwards.
        if self._save_checksums:
            path = self._dataset
            name = self._name

            urls_checksums_dir = os.path.join(builder_cls.get_imported_module_dir(), URLS_CHECKSUMS_FOLDER_NAME)
            checksums_file_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)

            if name is None:
                name = list(filter(lambda x: x, path.split("/")))[-1] + ".py"

            if not name.endswith(".py") or "/" in name:
                raise ValueError("The provided name should be the filename of a python script (ends with '.py')")

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
            os.makedirs(user_urls_checksums_dir, exist_ok=True)
            copyfile(checksums_file_path, user_checksums_file_path)
            print("Checksums file saved at {}".format(user_checksums_file_path))
