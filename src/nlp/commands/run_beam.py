from argparse import ArgumentParser
from typing import List

import apache_beam as beam

from nlp.builder import FORCE_REDOWNLOAD, REUSE_CACHE_IF_EXISTS, DatasetBuilder, DownloadConfig
from nlp.commands import BaseTransformersCLICommand
from nlp.load import import_main_class, prepare_module


def run_beam_command_factory(args):
    return RunBeamCommand(
        args.dataset,
        args.config,
        args.cache_dir,
        args.beam_pipeline_options,
        args.data_dir,
        args.all_configs,
        args.save_infos,
        args.ignore_verifications,
        args.force_redownload,
    )


class RunBeamCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        run_beam_parser = parser.add_parser("run_beam")
        run_beam_parser.add_argument("--config", type=str, default=None, help="Dataset processing config")
        run_beam_parser.add_argument(
            "--cache_dir", type=str, default=None, help="Cache directory where the datasets are stored.",
        )
        run_beam_parser.add_argument(
            "--beam_pipeline_options",
            type=str,
            default="",
            help="Beam pipeline options, separated by commas. Example: `--beam_pipeline_options=job_name=my-job,project=my-project`",
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
        config: str,
        cache_dir: str,
        beam_pipeline_options: str,
        data_dir: str,
        all_configs: bool,
        save_infos: bool,
        ignore_verifications: bool,
        force_redownload: bool,
    ):
        self._dataset = dataset
        self._config = config
        self._cache_dir = cache_dir
        self._beam_pipeline_options = beam_pipeline_options
        self._data_dir = data_dir
        self._all_configs = all_configs
        self._save_infos = save_infos
        self._ignore_verifications = ignore_verifications
        self._force_redownload = force_redownload

    def run(self):
        if self._config is not None and self._all_configs:
            print("Both parameters `config` and `all_configs` can't be used at once.")
            exit(1)
        path, config = self._dataset, self._config
        module_path = prepare_module(path)
        builder_cls = import_main_class(module_path)
        builders: List[DatasetBuilder] = []
        if self._beam_pipeline_options:
            beam_options = beam.options.pipeline_options.PipelineOptions(
                flags=["--%s" % opt.strip() for opt in self._beam_pipeline_options.split(",") if opt]
            )
        else:
            beam_options = None
        if self._all_configs and len(builder_cls.BUILDER_CONFIGS) > 0:
            for config in builder_cls.BUILDER_CONFIGS:
                builders.append(builder_cls(config=config, data_dir=self._data_dir, beam_options=beam_options))
        else:
            builders.append(builder_cls(config=config, data_dir=self._data_dir, beam_options=beam_options))

        for builder in builders:
            builder.download_and_prepare(
                download_config=DownloadConfig(cache_dir=self._cache_dir),
                download_mode=REUSE_CACHE_IF_EXISTS if not self._force_redownload else FORCE_REDOWNLOAD,
                save_infos=self._save_infos,
                ignore_verifications=self._ignore_verifications,
            )

        print("Apache beam run successful.")
