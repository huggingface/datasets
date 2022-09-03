import contextlib
import itertools
from dataclasses import dataclass
from sqlite3 import connect
from typing import Dict, List, Optional, Sequence, Union

import pandas as pd
import pyarrow as pa
from typing_extensions import Literal

import datasets
import datasets.config
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class SqlConfig(datasets.BuilderConfig):
    """BuilderConfig for SQL."""

    index_col: Optional[Union[int, str, List[int], List[str]]] = None
    table_name: str = "Dataset"
    coerce_float: bool = True
    params: Optional[Union[Sequence, Dict]] = None
    parse_dates: Optional[Union[List, Dict]] = None
    columns: Optional[List[str]] = None
    chunksize: int = 10_000
    features: Optional[datasets.Features] = None
    encoding_errors: Optional[str] = "strict"
    on_bad_lines: Literal["error", "warn", "skip"] = "error"

    @property
    def read_sql_kwargs(self):
        read_sql_kwargs = dict(
            index_col=self.index_col,
            columns=self.columns,
            params=self.params,
            coerce_float=self.coerce_float,
            parse_dates=self.parse_dates,
            chunksize=self.chunksize,
        )
        return read_sql_kwargs


class Sql(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = SqlConfig

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
            files = [dl_manager.iter_files(file) for file in files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files = [dl_manager.iter_files(file) for file in files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            schema = self.config.features.arrow_schema
            if all(not require_storage_cast(feature) for feature in self.config.features.values()):
                # cheaper cast
                pa_table = pa.Table.from_arrays([pa_table[field.name] for field in schema], schema=schema)
            else:
                # more expensive cast; allows str <-> int/float or str to Audio for example
                pa_table = table_cast(pa_table, schema)
        return pa_table

    def _generate_tables(self, files):
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            with contextlib.closing(connect(file)) as conn:
                sql_file_reader = pd.read_sql(
                    f"SELECT * FROM `{self.config.table_name}`", conn, **self.config.read_sql_kwargs
                )
                try:
                    for batch_idx, df in enumerate(sql_file_reader):
                        # Drop index column as it is not relevant.
                        pa_table = pa.Table.from_pandas(df.drop("index", axis=1, errors="ignore"))
                        # Uncomment for debugging (will print the Arrow table size and elements)
                        # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                        # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                        yield (file_idx, batch_idx), self._cast_table(pa_table)
                except ValueError as e:
                    logger.error(f"Failed to read file '{file}' with error {type(e)}: {e}")
                    raise
