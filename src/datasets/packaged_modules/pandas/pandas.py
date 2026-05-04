import warnings
from dataclasses import dataclass
from typing import Optional

import pandas as pd
import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.table import table_cast


@dataclass
class PandasConfig(datasets.BuilderConfig):
    """BuilderConfig for Pandas."""

    features: Optional[datasets.Features] = None

    def __post_init__(self):
        super().__post_init__()


class Pandas(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = PandasConfig

    def _info(self):
        warnings.warn(
            "The Pandas builder is deprecated and will be removed in the next major version of datasets.",
            FutureWarning,
        )
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.config.features.arrow_schema)
        return pa_table

    def _generate_shards(self, files):
        yield from files

    def _generate_tables(self, files):
        for i, file in enumerate(files):
            with open(file, "rb") as f:
                pa_table = pa.Table.from_pandas(pd.read_pickle(f))
                yield Key(i, 0), self._cast_table(pa_table)
