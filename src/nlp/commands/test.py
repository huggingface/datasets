from argparse import ArgumentParser

from nlp.commands import BaseTransformersCLICommand
from nlp.load import builder, HF_DATASETS_CACHE
from nlp.builder import DatasetBuilder


def test_command_factory(args):
    return TestCommand(args.datasets, args.cache_dir, args.force)


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
        download_parser.add_argument("datasets", type=str, help="Name of the datasets to download")
        download_parser.set_defaults(func=test_command_factory)

    def __init__(self, datasets: str, cache: str, force: bool):
        self._datasets = datasets
        self._cache = cache
        self._force = force

    def run(self):
        ds: DatasetBuilder = builder(self._datasets)
        print(ds.builder_config)
        
        
