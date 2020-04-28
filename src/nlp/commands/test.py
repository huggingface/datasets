from argparse import ArgumentParser
import inspect
import os
import sys
from typing import List

from nlp.builder import DatasetBuilder, REUSE_CACHE_IF_EXISTS
from nlp.commands import BaseTransformersCLICommand
from nlp.load import HF_DATASETS_CACHE, builder
from nlp.utils import DownloadConfig
from nlp.utils.file_utils import hf_bucket_url, path_to_py_script_name
from nlp.hf_api import HfApi, HfFolder


UPLOAD_MAX_FILES = 15


def test_command_factory(args):
    return TestCommand(args.datasets, args.name, args.cache_dir, args.force, args.register_checksums, args.ignore_checksums, args.organization)


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
        test_parser.add_argument(
            "--name", type=str, default=None, help="Dataset variant name"
        )
        test_parser.add_argument(
            "--cache-dir", type=str, default=None, help="Path to location to store the datasets"
        )
        test_parser.add_argument(
            "--force", action="store_true", help="Force the datasets to be download even if already in cache-dir"
        )
        test_parser.add_argument(
            "--register_checksums", action="store_true", help="Save the checksums file on S3"
        )
        test_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        test_parser.add_argument("--organization", type=str, help="Optional: organization namespace.")
        test_parser.add_argument("datasets", type=str, help="Name of the datasets to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(self, datasets: str, name: str, cache: str, force: bool, register_checksums: bool, ignore_checksums: bool, organization: str):
        self._datasets = datasets
        self._name = name
        self._cache = cache
        self._force = force
        self._register_checksums = register_checksums
        self._ignore_checksums = ignore_checksums
        self._organization = organization
        self._api = HfApi()

    def run(self):
        path = self._datasets
        db: DatasetBuilder = builder(path, self._name)
        db.download_and_prepare(download_config=DownloadConfig(
            download_mode=REUSE_CACHE_IF_EXISTS,
            register_checksums=self._register_checksums,
            ignore_checksums=self._ignore_checksums
        ))
        print("Test successful.")
        if self._register_checksums:
            token = HfFolder.get_token()
            if token is None:
                print("Not logged in. Couln't upload registered checksums.")
                exit(1)
            urls_checksums_dir = os.path.dirname(inspect.getfile(db.__class__))
            urls_checksums_dir = os.path.join(urls_checksums_dir, "urls_checksums")
            full_name = db.info.full_name
            filename = full_name.replace("/", ":") + ".txt"
            checksums_path = os.path.join(urls_checksums_dir, filename)
            remote_checksums_dir = db.info.name + "/" + "urls_checksums"
            
            # Upload

            local_path = os.path.abspath(checksums_path)
            if os.path.isfile(local_path):
                filename = os.path.basename(local_path)
                files = [(local_path, os.path.join(remote_checksums_dir, filename))]
            else:
                raise ValueError("Not a valid directory: {}".format(local_path))

            if sys.platform == "win32":
                files = [(filepath, filename.replace(os.sep, "/")) for filepath, filename in files]

            if len(files) > UPLOAD_MAX_FILES:
                print(
                    "About to upload {} files to S3. This is probably wrong. Please filter files before uploading.".format(
                        ANSI.bold(len(files))
                    )
                )
                exit(1)

            user, _ = self._api.whoami(token)
            namespace = self._organization if self._organization is not None else user

            for filepath, filename in files:
                print(
                    "About to upload checksums file {} to S3 under filename {} and namespace {}".format(
                        ANSI.bold(filepath), ANSI.bold(filename), ANSI.bold(namespace)
                    )
                )

            choice = input("Proceed? [Y/n] ").lower()
            if not (choice == "" or choice == "y" or choice == "yes"):
                print("Abort")
                exit()
            print(ANSI.bold("Uploading..."))
            for filepath, filename in files:
                access_url = self._api.presign_and_upload(
                    token=token, filename=filename, filepath=filepath, organization=self._organization
                )
                print("Your file now lives at:")
                print(access_url)
