import inspect
import os
from argparse import ArgumentParser
from shutil import copyfile

from nlp.builder import REUSE_CACHE_IF_EXISTS, DatasetBuilder
from nlp.commands import BaseTransformersCLICommand
from nlp.hf_api import HfApi
from nlp.load import builder
from nlp.utils import DownloadConfig
from nlp.utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME


def test_command_factory(args):
    return TestCommand(
        args.dataset,
        args.name,
        args.cache_dir,
        args.force,
        args.register_checksums,
        args.ignore_checksums,
        args.organization,
    )


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--name", type=str, default=None, help="Dataset processing name")
        test_parser.add_argument("--cache-dir", type=str, default=None, help="Path to location to store the datasets")
        test_parser.add_argument(
            "--force", action="store_true", help="Force the datasets to be download even if already in cache-dir"
        )
        test_parser.add_argument("--register_checksums", action="store_true", help="Save the checksums file on S3")
        test_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        test_parser.add_argument("--organization", type=str, help="Optional: organization namespace.")
        test_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self,
        dataset: str,
        name: str,
        cache: str,
        force: bool,
        register_checksums: bool,
        ignore_checksums: bool,
        organization: str,
    ):
        self._dataset = dataset
        self._name = name
        self._cache = cache
        self._force = force
        self._register_checksums = register_checksums
        self._ignore_checksums = ignore_checksums
        self._organization = organization
        self._api = HfApi()

    def run(self):
        db: DatasetBuilder = builder(self._dataset, self._name)
        db.download_and_prepare(
            download_config=DownloadConfig(
                download_mode=REUSE_CACHE_IF_EXISTS,
                register_checksums=self._register_checksums,
                ignore_checksums=self._ignore_checksums,
            )
        )
        print("Test successful.")
        # If register_checksums=True, the checksums file is created next to the loaded module file.
        # Let's move it to the original directory of the dataset script, to allow the user to
        # upload them on S3 at the same time afterwards.
        if self._register_checksums:
            path = self._dataset
            name = self._name

            urls_checksums_dir = db._urls_checksums_dir
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
