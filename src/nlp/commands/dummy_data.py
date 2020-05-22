import logging
import os
from argparse import ArgumentParser

from nlp.commands import BaseTransformersCLICommand
from nlp.load import import_main_class, prepare_module
from nlp.utils import MockDownloadManager


logger = logging.getLogger(__name__)


def test_command_factory(args):
    return DummyDataCommand(args.path_to_dataset, args.requires_manual,)


class DummyDataCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("dummy_data")
        test_parser.add_argument("--requires_manual", action="store_true", help="Dataset requires manual data")
        test_parser.add_argument("path_to_dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self, path_to_dataset: str, requires_manual: bool,
    ):
        self._path_to_dataset = path_to_dataset
        self._requires_manual = requires_manual
        self._dataset_name = path_to_dataset.split("/")[-2]

    def run(self):
        module_path = prepare_module(self._dataset)
        builder_cls = import_main_class(module_path)

        # use `None` as config if no configs
        configs = builder_cls.BUILDER_CONFIGS or [None]

        for config in configs:
            if config is None:
                version = builder_cls.VERSION
            else:
                version = config.version

            dataset_builder = builder_cls(config=config)
            mock_dl_manager = MockDownloadManager(
                dataset_name=self._dataset_name, config=config, version=version, is_local=True
            )

            dummy_data_folder = mock_dl_manager.dummy_data_folder
            logger.info(f"Creating dummy folder structure for {dummy_data_folder}... ")
            os.makedirs(os.path(self._path_to_dataset, dummy_data_folder), exist_ok=True)

            generator_splits = dataset_builder._split_generators(mock_dl_manager)
            import ipdb

            ipdb.set_trace()
            pass
