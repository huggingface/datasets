from dataclasses import dataclass
from typing import Optional

import pandas as pd
import pyarrow as pa

import datasets
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


@dataclass
class PandasConfig(datasets.BuilderConfig):
    """BuilderConfig for Pandas."""

    features: Optional[datasets.Features] = None

    @property
    def schema(self):
        return self.features.arrow_schema if self.features is not None else None


class Pandas(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = PandasConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            schema = self.config.schema
            if all(not require_storage_cast(feature) for feature in self.config.features.values()):
                # cheaper cast
                pa_table = pa.Table.from_arrays([pa_table[field.name] for field in schema], schema=schema)
            else:
                # more expensive cast; allows str <-> int/float or str to Audio for example
                pa_table = table_cast(pa_table, schema)
        return pa_table

    def _generate_tables(self, files):
        for i, file in enumerate(files):
            with open(file, "rb") as f:
                pa_table = pa.Table.from_pandas(pd.read_pickle(f))
                yield i, self._cast_table(pa_table)
