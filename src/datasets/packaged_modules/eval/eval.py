import json
import os
from itertools import islice
from typing import Iterable

import pyarrow as pa

import datasets
from datasets.builder import Key


logger = datasets.utils.logging.get_logger(__name__)


class Eval(datasets.GeneratorBasedBuilder):
    NUM_EXAMPLES_FOR_FEATURES_INFERENCE = 5

    def _info(self):
        return datasets.DatasetInfo()

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        base_data_files = dl_manager.download(self.config.data_files)
        extracted_data_files = dl_manager.extract(base_data_files)
        splits = []
        for split_name, logs in extracted_data_files.items():
            logs_files_iterables = [dl_manager.iter_files(log) for log in logs]
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "logs_files_iterables": logs_files_iterables,
                        "base_files": base_data_files[split_name],
                    },
                )
            )
        if not self.info.features:
            first_examples = list(
                islice(
                    self._iter_samples_from_log_files(logs_files_iterables[0]),
                    self.NUM_EXAMPLES_FOR_FEATURES_INFERENCE,
                )
            )
            pa_tables = [pa.Table.from_pylist([example]) for example in first_examples]
            inferred_arrow_schema = pa.concat_tables(pa_tables, promote_options="default").schema
            self.info.features = datasets.Features.from_arrow_schema(inferred_arrow_schema)

        return splits

    def _sort_samples_key(self, sample_path: str):
        # looks like "{sample_idx}_epoch_{epoch_idx}""
        (sample_idx_str, epoch_idx_str) = os.path.splitext(os.path.basename(sample_path))[0].split("_epoch_")
        return (int(epoch_idx_str), int(sample_idx_str))

    def _iter_samples_from_log_files(self, log_files: Iterable[str]):
        sample_files = [log_file for log_file in log_files if os.path.basename(os.path.dirname(log_file)) == "samples"]
        sample_files.sort(key=self._sort_samples_key)
        for sample_file in sample_files:
            with open(sample_file) as f:
                sample = json.load(f)
                for field in sample:
                    if isinstance(sample[field], dict):
                        sample[field] = json.dumps(sample[field])
                    if isinstance(sample[field], list):
                        sample[field] = [json.dumps(x) for x in sample[field]]
                yield sample

    def _generate_shards(self, base_files, logs_files_iterables):
        yield from base_files

    def _generate_examples(self, base_files, logs_files_iterables):
        for file_idx, log_files in enumerate(logs_files_iterables):
            for sample_idx, sample in enumerate(self._iter_samples_from_log_files(log_files)):
                yield Key(file_idx, sample_idx), sample
