import os
from argparse import ArgumentParser
from shutil import copyfile
from typing import List

from nlp.builder import FORCE_REDOWNLOAD, REUSE_CACHE_IF_EXISTS, DatasetBuilder
from nlp.commands import BaseTransformersCLICommand
from nlp.info import DATASET_INFOS_DICT_FILE_NAME
from nlp.load import import_main_class, prepare_module


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
    )


class TestCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("test")
        test_parser.add_argument("--name", type=str, default=None, help="Dataset processing name")
        test_parser.add_argument(
            "--cache_dir", type=str, default=None, help="Cache directory where the datasets are stored.",
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
    ):
        self._dataset = dataset
        self._name = name
        self._cache_dir = cache_dir
        self._data_dir = data_dir
        self._all_configs = all_configs
        self._save_infos = save_infos
        self._ignore_verifications = ignore_verifications
        self._force_redownload = force_redownload

    def run(self):
        if self._name is not None and self._all_configs:
            print("Both parameters `config` and `all_configs` can't be used at once.")
            exit(1)
        path, name = self._dataset, self._name
        module_path, hash = prepare_module(path)
        builder_cls = import_main_class(module_path)
        builders: List[DatasetBuilder] = []
        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            for config in builder_cls.BUILDER_CONFIGS:
                builders.append(
                    builder_cls(name=config.name, hash=hash, cache_dir=self._cache_dir, data_dir=self._data_dir)
                )
        else:
            builders.append(builder_cls(name=name, hash=hash, cache_dir=self._cache_dir, data_dir=self._data_dir))

        for builder in builders:
            builder.download_and_prepare(
                download_mode=REUSE_CACHE_IF_EXISTS if not self._force_redownload else FORCE_REDOWNLOAD,
                ignore_verifications=self._ignore_verifications,
                try_from_hf_gcs=False,
            )
            builder.as_dataset()
            if self._save_infos:
                builder._save_infos()

        print("Test successful.")
        # If save_infos=True, the dataset infos file is created next to the loaded module file.
        # Let's move it to the original directory of the dataset script, to allow the user to
        # upload them on S3 at the same time afterwards.
        if self._save_infos:
            dataset_infos_path = os.path.join(builder_cls.get_imported_module_dir(), DATASET_INFOS_DICT_FILE_NAME)

            name = list(filter(lambda x: x, path.split("/")))[-1] + ".py"

            combined_path = os.path.join(path, name)
            if os.path.isfile(path):
                dataset_dir = os.path.dirname(path)
            elif os.path.isfile(combined_path):
                dataset_dir = path
            else:  # in case of a remote dataset
                print("Dataset Infos file saved at {}".format(dataset_infos_path))
                exit(1)

            # Move datasetinfo back to the user
            user_dataset_infos_path = os.path.join(dataset_dir, DATASET_INFOS_DICT_FILE_NAME)
            copyfile(dataset_infos_path, user_dataset_infos_path)
            print("Dataset Infos file saved at {}".format(user_dataset_infos_path))
