from argparse import ArgumentParser

from nlp.builder import DatasetBuilder, REUSE_CACHE_IF_EXISTS
from nlp.commands import BaseTransformersCLICommand
from nlp.load import HF_DATASETS_CACHE, builder
from nlp.utils import DownloadConfig
from nlp.utils.file_utils import hf_bucket_url, path_to_py_script_name


def test_command_factory(args):
    return TestCommand(args.datasets, args.cache_dir, args.force, args.register_checksums, args.ignore_checksums)


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        download_parser = parser.add_parser("test")
        download_parser.add_argument(
            "--cache-dir", type=str, default=None, help="Path to location to store the datasets"
        )
        download_parser.add_argument(
            "--force", action="store_true", help="Force the datasets to be download even if already in cache-dir"
        )
        download_parser.add_argument(
            "--register_checksums", action="store_true", help="Save the checksums file on S3"
        )
        download_parser.add_argument(
            "--ignore_checksums", action="store_true", help="Run the test without checksums checks"
        )
        download_parser.add_argument("datasets", type=str, help="Name of the datasets to download")
        download_parser.set_defaults(func=test_command_factory)

    def __init__(self, datasets: str, cache: str, force: bool, register_checksums: bool, ignore_checksums: bool):
        self._datasets = datasets
        self._cache = cache
        self._force = force
        self._register_checksums = register_checksums
        self._ignore_checksums = ignore_checksums

    def run(self):
        path = self._datasets
        ds: DatasetBuilder = builder(path)
        ds.download_and_prepare(download_config=DownloadConfig(
            download_mode=REUSE_CACHE_IF_EXISTS,
            register_checksums=self._register_checksums,
            ignore_checksums=self._ignore_checksums
        ))
