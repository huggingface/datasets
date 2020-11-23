import os
from argparse import ArgumentParser

from pathlib import Path

from datasets.commands import BaseTransformersCLICommand
from datasets.load import import_main_class, prepare_module
from datasets.utils import MockDownloadManager
from datasets.utils.download_manager import DownloadManager
from datasets.utils.logging import get_logger
from datasets.utils.py_utils import map_nested


logger = get_logger(__name__)


def test_command_factory(args):
    return DummyDataCommand(
        args.path_to_dataset,
        args.requires_manual,
        args.auto_generate,
        args.n_lines,
    )


class DummyDataGeneratorDownloadManager(DownloadManager):

    def __init__(self, mock_download_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mock_download_manager = mock_download_manager
        self.downloaded_paths = []
        self.expected_dummy_paths = []

    def download(self, url_or_urls):
        output = super().download(url_or_urls)
        dummy_output = self.mock_download_manager.download(url_or_urls)
        map_nested(self.downloaded_paths.append, output, map_tuple=True)
        map_nested(self.expected_dummy_paths.append, dummy_output, map_tuple=True)
        return output

    def _auto_generate_dummy_data_folder(self):
        raise NotImplementedError()

    def _zip_auto_generated_dummy_data_folder(self):
        raise NotImplementedError()


class DummyDataCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        test_parser = parser.add_parser("dummy_data")
        test_parser.add_argument("--requires_manual", action="store_true", help="Dataset requires manual data")
        test_parser.add_argument("--auto_generate", action="store_true", help="Try to automatically generate dummy data")
        test_parser.add_argument("--n_lines", type=int, default=10, help="number of lines used when auto-generating dummy data")
        test_parser.add_argument("path_to_dataset", type=str, help="Name of the dataset to download")
        test_parser.set_defaults(func=test_command_factory)

    def __init__(
        self,
        path_to_dataset: str,
        requires_manual: bool,
        auto_generate: bool,
        n_lines: int,
    ):
        self._path_to_dataset = path_to_dataset
        self._requires_manual = requires_manual
        self._dataset_name = path_to_dataset.replace(os.sep, "/").split("/")[-2]
        self._auto_generate = auto_generate
        self._n_lines = n_lines

    def run(self):
        module_path, hash = prepare_module(self._path_to_dataset)
        builder_cls = import_main_class(module_path)

        # use `None` as config if no configs
        configs = builder_cls.BUILDER_CONFIGS or [None]

        for config in configs:
            if config is None:
                name = None
                version = builder_cls.VERSION
            else:
                version = config.version
                name = config.name

            dataset_builder = builder_cls(name=name, hash=hash)

            if self._auto_generate:
                self._autogenerate_dummy_data(dataset_builder=dataset_builder, config=config, version=version)
            else:
                self._print_dummy_data_instructions(dataset_builder=dataset_builder, config=config, version=version)

    def _autogenerate_dummy_data(self, dataset_builder, config, version):
        mock_dl_manager = MockDownloadManager(
            dataset_name=self._dataset_name, config=config, version=version, is_local=True
        )
        dl_manager = DummyDataGeneratorDownloadManager(dataset_name=self._dataset_name, mock_download_manager=mock_dl_manager)
        generator_splits = dataset_builder._split_generators(dl_manager)
        downloaded_paths = dl_manager.downloaded_paths
        expected_dummy_paths = dl_manager.expected_dummy_paths
        dummy_data_folder = os.path.join("datasets", self._dataset_name)
        print(downloaded_paths)
        print(expected_dummy_paths)

    def _print_dummy_data_instructions(self, dataset_builder, config, version):
        mock_dl_manager = MockDownloadManager(
            dataset_name=self._dataset_name, config=config, version=version, is_local=True
        )

        dummy_data_folder = os.path.join(self._path_to_dataset, mock_dl_manager.dummy_data_folder)
        logger.info(f"Creating dummy folder structure for {dummy_data_folder}... ")
        os.makedirs(dummy_data_folder, exist_ok=True)

        try:
            generator_splits = dataset_builder._split_generators(mock_dl_manager)
        except FileNotFoundError as e:

            print(
                f"Dataset {self._dataset_name} with config {config} seems to already open files in the method `_split_generators(...)`. You might consider to instead only open files in the method `_generate_examples(...)` instead. If this is not possible the dummy data has to be created with less guidance. Make sure you create the file {e.filename}."
            )

        files_to_create = set()
        split_names = []
        dummy_file_name = mock_dl_manager.dummy_file_name

        for split in generator_splits:
            logger.info(f"Collecting dummy data file paths to create for {split.name}")
            split_names.append(split.name)
            gen_kwargs = split.gen_kwargs
            generator = dataset_builder._generate_examples(**gen_kwargs)

            try:
                dummy_data_guidance_print = "\n" + 30 * "=" + "DUMMY DATA INSTRUCTIONS" + 30 * "=" + "\n"
                config_string = f"config {config.name} of " if config is not None else ""
                dummy_data_guidance_print += (
                    "- In order to create the dummy data for "
                    + config_string
                    + f"{self._dataset_name}, please go into the folder '{dummy_data_folder}' with `cd {dummy_data_folder}` . \n\n"
                )

                # trigger generate function
                for key, record in generator:
                    pass

                dummy_data_guidance_print += f"- It appears that the function `_generate_examples(...)` expects one or more files in the folder {dummy_file_name} using the function `glob.glob(...)`. In this case, please refer to the `_generate_examples(...)` method to see under which filename the dummy data files should be created. \n\n"

            except FileNotFoundError as e:
                files_to_create.add(e.filename)

        split_names = ", ".join(split_names)
        if len(files_to_create) > 0:
            # no glob.glob(...) in `_generate_examples(...)`
            if len(files_to_create) == 1 and next(iter(files_to_create)) == dummy_file_name:
                dummy_data_guidance_print += f"- Please create a single dummy data file called '{next(iter(files_to_create))}' from the folder '{dummy_data_folder}'. Make sure that the dummy data file provides at least one example for the split(s) '{split_names}' \n\n"
                files_string = dummy_file_name
            else:
                files_string = ", ".join(files_to_create)
                dummy_data_guidance_print += f"- Please create the following dummy data files '{files_string}' from the folder '{dummy_data_folder}'\n\n"

                dummy_data_guidance_print += f"- For each of the splits '{split_names}', make sure that one or more of the dummy data files provide at least one example \n\n"

            dummy_data_guidance_print += f"- If the method `_generate_examples(...)` includes multiple `open()` statements, you might have to create other files in addition to '{files_string}'. In this case please refer to the `_generate_examples(...)` method \n\n"

        if len(files_to_create) == 1 and next(iter(files_to_create)) == dummy_file_name:
            dummy_data_guidance_print += f"-After the dummy data file is created, it should be zipped to '{dummy_file_name}.zip' with the command `zip {dummy_file_name}.zip {dummy_file_name}` \n\n"

            dummy_data_guidance_print += (
                f"-You can now delete the file '{dummy_file_name}' with the command `rm {dummy_file_name}` \n\n"
            )

            dummy_data_guidance_print += f"- To get the file '{dummy_file_name}' back for further changes to the dummy data, simply unzip {dummy_file_name}.zip with the command `unzip {dummy_file_name}.zip` \n\n"
        else:
            dummy_data_guidance_print += f"-After all dummy data files are created, they should be zipped recursively to '{dummy_file_name}.zip' with the command `zip -r {dummy_file_name}.zip {dummy_file_name}/` \n\n"

            dummy_data_guidance_print += f"-You can now delete the folder '{dummy_file_name}' with the command `rm -r {dummy_file_name}` \n\n"

            dummy_data_guidance_print += f"- To get the folder '{dummy_file_name}' back for further changes to the dummy data, simply unzip {dummy_file_name}.zip with the command `unzip {dummy_file_name}.zip` \n\n"

        dummy_data_guidance_print += (
            f"- Make sure you have created the file '{dummy_file_name}.zip' in '{dummy_data_folder}' \n"
        )

        dummy_data_guidance_print += 83 * "=" + "\n"

        print(dummy_data_guidance_print)
