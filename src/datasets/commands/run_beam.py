import os
from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile
from typing import List

from datasets import config
from datasets.builder import DatasetBuilder
from datasets.commands import BaseDatasetsCLICommand
from datasets.load import dataset_module_factory, import_main_class
from datasets.utils.download_manager import DownloadConfig, DownloadMode


def run_beam_command_factory(args):
    return RunBeamCommand(
        args.dataset,
        args.name,
        args.cache_dir,
        args.beam_pipeline_options,
        args.data_dir,
        args.all_configs,
        args.save_infos,
        args.ignore_verifications,
        args.force_redownload,
    )


class RunBeamCommand(BaseDatasetsCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        run_beam_parser = parser.add_parser("run_beam", help="Run a Beam dataset processing pipeline.")
        run_beam_parser.add_argument("--name", type=str, default=None, help="Dataset processing name")
        run_beam_parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="Cache directory where the datasets are stored.",
        )
        run_beam_parser.add_argument(
            "--beam_pipeline_options",
            type=str,
            default="",
            help="Beam pipeline options, separated by commas. Example:: `--beam_pipeline_options=job_name=my-job,project=my-project`",
        )
        run_beam_parser.add_argument(
            "--data_dir",
            type=str,
            default=None,
            help="Can be used to specify a manual directory to get the files from.",
        )
        run_beam_parser.add_argument("--all_configs", action="store_true", help="Test all dataset configurations")
        run_beam_parser.add_argument("--save_infos", action="store_true", help="Save the dataset infos file")
        run_beam_parser.add_argument(
            "--ignore_verifications", action="store_true", help="Run the test without checksums and splits checks"
        )
        run_beam_parser.add_argument("--force_redownload", action="store_true", help="Force dataset redownload")
        run_beam_parser.add_argument("dataset", type=str, help="Name of the dataset to download")
        run_beam_parser.set_defaults(func=run_beam_command_factory)

    def __init__(
        self,
        dataset: str,
        name: str,
        cache_dir: str,
        beam_pipeline_options: str,
        data_dir: str,
        all_configs: bool,
        save_infos: bool,
        ignore_verifications: bool,
        force_redownload: bool,
    ):
        self._dataset = dataset
        self._name = name
        self._cache_dir = cache_dir
        self._beam_pipeline_options = beam_pipeline_options
        self._data_dir = data_dir
        self._all_configs = all_configs
        self._save_infos = save_infos
        self._ignore_verifications = ignore_verifications
        self._force_redownload = force_redownload

    def run(self):
        import apache_beam as beam

        if self._name is not None and self._all_configs:
            print("Both parameters `name` and `all_configs` can't be used at once.")
            exit(1)
        path, name = self._dataset, self._name
        dataset_module = dataset_module_factory(path)
        builder_cls = import_main_class(dataset_module.module_path)
        builders: List[DatasetBuilder] = []
        if self._beam_pipeline_options:
            beam_options = beam.options.pipeline_options.PipelineOptions(
                flags=[f"--{opt.strip()}" for opt in self._beam_pipeline_options.split(",") if opt]
            )
        else:
            beam_options = None
        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            for builder_config in builder_cls.BUILDER_CONFIGS:
                builders.append(
                    builder_cls(
                        name=builder_config.name,
                        data_dir=self._data_dir,
                        hash=dataset_module.hash,
                        beam_options=beam_options,
                        cache_dir=self._cache_dir,
                        base_path=dataset_module.builder_kwargs.get("base_path"),
                        namespace=dataset_module.builder_kwargs.get("namespace"),
                    )
                )
        else:
            builders.append(
                builder_cls(
                    name=name,
                    data_dir=self._data_dir,
                    beam_options=beam_options,
                    cache_dir=self._cache_dir,
                    base_path=dataset_module.builder_kwargs.get("base_path"),
                    namespace=dataset_module.builder_kwargs.get("namespace"),
                )
            )

        for builder in builders:
            builder.download_and_prepare(
                download_mode=DownloadMode.REUSE_CACHE_IF_EXISTS
                if not self._force_redownload
                else DownloadMode.FORCE_REDOWNLOAD,
                download_config=DownloadConfig(cache_dir=config.DOWNLOADED_DATASETS_PATH),
                save_infos=self._save_infos,
                ignore_verifications=self._ignore_verifications,
                try_from_hf_gcs=False,
            )

        print("Apache beam run successful.")

        # If save_infos=True, the dataset infos file is created next to the loaded module file.
        # Let's move it to the original directory of the dataset script, to allow the user to
        # upload them on S3 at the same time afterwards.
        if self._save_infos:
            dataset_infos_path = os.path.join(builder_cls.get_imported_module_dir(), config.DATASETDICT_INFOS_FILENAME)

            name = Path(path).name + ".py"

            combined_path = os.path.join(path, name)
            if os.path.isfile(path):
                dataset_dir = os.path.dirname(path)
            elif os.path.isfile(combined_path):
                dataset_dir = path
            else:  # in case of a remote dataset
                print(f"Dataset Infos file saved at {dataset_infos_path}")
                exit(1)

            # Move datasetinfo back to the user
            user_dataset_infos_path = os.path.join(dataset_dir, config.DATASETDICT_INFOS_FILENAME)
            copyfile(dataset_infos_path, user_dataset_infos_path)
            print(f"Dataset Infos file saved at {user_dataset_infos_path}")
