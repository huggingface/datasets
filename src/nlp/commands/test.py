import inspect
import os
from argparse import ArgumentParser
from shutil import copyfile

from nlp.builder import REUSE_CACHE_IF_EXISTS, DatasetBuilder
from nlp.commands import BaseTransformersCLICommand
from nlp.load import builder
from nlp.utils import DownloadConfig
from nlp.utils.checksums_utils import CHECKSUMS_FILE_NAME, URLS_CHECKSUMS_FOLDER_NAME


UPLOAD_MAX_FILES = 15


def test_command_factory(args):
    return TestCommand(
        args.datasets,
        args.name,
        args.cache_dir,
        args.force,
        args.register_checksums,
        args.ignore_checksums,
        args.organization,
    )


class ANSI:
    """
    Helper for en.wikipedia.org/wiki/ANSI_escape_code
    """

    _bold = "\u001b[1m"
    _reset = "\u001b[0m"

    @classmethod
    def bold(cls, s):
        return "{}{}{}".format(cls._bold, s, cls._reset)


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--name", type=str, default=None, help="Dataset variant name")
        test_parser.add_argument("--cache-dir", type=str, default=None, help="Path to location to store the datasets")
        test_parser.add_argument(
            "--force", action="store_true", help="Force the datasets to be download even if already in cache-dir"
        )
        test_parser.add_argument("--register_checksums", action="store_true", help="Save the checksums file on S3")
        test_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        test_parser.add_argument("--organization", type=str, help="Optional: organization namespace.")
        test_parser.add_argument("datasets", type=str, help="Name of the datasets to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self,
        datasets: str,
        name: str,
        cache: str,
        force: bool,
        register_checksums: bool,
        ignore_checksums: bool,
        organization: str,
    ):
        self._datasets = datasets
        self._name = name
        self._cache = cache
        self._force = force
        self._register_checksums = register_checksums
        self._ignore_checksums = ignore_checksums
        self._organization = organization
        self._api = HfApi()

    def _check_ownership(self, datasets_identifier: str, token: str):
        user, orgas = self._api.whoami(token)
        if self._organization is not None and self._organization not in orgas:
            raise ValueError("You are not part of organization {}.".format(self._organization))
        user_namespace = self._organization if self._organization is not None else user
        datasets_namespace = datasets_identifier.split("/")[0] if "/" in datasets_identifier else None
        if datasets_namespace is not None and datasets_namespace != user_namespace:
            raise ValueError(
                "You don't seem to own the namespace {}. Yours is {}.".format(datasets_namespace, user_namespace)
            )

    def run(self):
        db: DatasetBuilder = builder(self._datasets, self._name)
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
            path = self._datasets
            name = self._name

            urls_checksums_dir = os.path.dirname(inspect.getfile(db.__class__))
            urls_checksums_dir = os.path.join(urls_checksums_dir, URLS_CHECKSUMS_FOLDER_NAME)
            checksums_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)

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
                print("Checksums file saved at {}".format(checksums_path))
                exit(1)

            user_urls_checksums_dir = os.path.join(dataset_dir, URLS_CHECKSUMS_FOLDER_NAME)
            user_checksums_path = os.path.join(user_urls_checksums_dir, CHECKSUMS_FILE_NAME)
            os.makedirs(user_urls_checksums_dir, exist_ok=True)
            copyfile(checksums_path, user_checksums_path)
            print("Checksums file saved at {}".format(user_checksums_path))
