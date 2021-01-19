# coding=utf-8

import logging
from dataclasses import dataclass
from typing import List, Optional, Union

import pandas as pd
import pyarrow as pa

import datasets


logger = logging.getLogger(__name__)


@dataclass
class CsvConfig(datasets.BuilderConfig):
    """BuilderConfig for CSV."""

    sep: str = ","
    delimiter: Optional[str] = None
    header: Optional[Union[int, List[int], str]] = "infer"
    names: Optional[List[str]] = None
    column_names: Optional[List[str]] = None
    index_col: Optional[Union[int, str, List[int], List[str]]] = None
    usecols: Optional[Union[List[int], List[str]]] = None
    prefix: Optional[str] = None
    mangle_dupe_cols: bool = True
    engine: Optional[str] = None
    true_values: Optional[list] = None
    false_values: Optional[list] = None
    skipinitialspace: bool = False
    skiprows: Optional[Union[int, List[int]]] = None
    nrows: Optional[int] = None
    na_values: Optional[Union[str, List[str]]] = None
    keep_default_na: bool = True
    na_filter: bool = True
    verbose: bool = False
    skip_blank_lines: bool = True
    thousands: Optional[str] = None
    decimal: str = b"."
    lineterminator: Optional[str] = None
    quotechar: str = '"'
    quoting: int = 0
    escapechar: Optional[str] = None
    comment: Optional[str] = None
    encoding: Optional[str] = None
    dialect: str = None
    error_bad_lines: bool = True
    warn_bad_lines: bool = True
    skipfooter: int = 0
    doublequote: bool = True
    memory_map: bool = False
    float_precision: Optional[str] = None
    chunksize: int = 10_000
    features: datasets.Features = None

    def __post_init__(self):
        if self.delimiter is not None:
            self.sep = self.delimiter
        if self.column_names is not None:
            self.names = self.column_names


class Csv(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = CsvConfig

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

    def _generate_tables(self, files):
        schema = pa.schema(self.config.features.type) if self.config.features is not None else None
        for file_idx, file in enumerate(files):
            csv_file_reader = pd.read_csv(
                file,
                iterator=True,
                sep=self.config.sep,
                header=self.config.header,
                names=self.config.names,
                index_col=self.config.index_col,
                usecols=self.config.usecols,
                prefix=self.config.prefix,
                mangle_dupe_cols=self.config.mangle_dupe_cols,
                engine=self.config.engine,
                true_values=self.config.true_values,
                false_values=self.config.false_values,
                skipinitialspace=self.config.skipinitialspace,
                skiprows=self.config.skiprows,
                nrows=self.config.nrows,
                na_values=self.config.na_values,
                keep_default_na=self.config.keep_default_na,
                na_filter=self.config.na_filter,
                verbose=self.config.verbose,
                skip_blank_lines=self.config.skip_blank_lines,
                thousands=self.config.thousands,
                decimal=self.config.decimal,
                lineterminator=self.config.lineterminator,
                quotechar=self.config.quotechar,
                quoting=self.config.quoting,
                escapechar=self.config.escapechar,
                comment=self.config.comment,
                encoding=self.config.encoding,
                dialect=self.config.dialect,
                error_bad_lines=self.config.error_bad_lines,
                warn_bad_lines=self.config.warn_bad_lines,
                skipfooter=self.config.skipfooter,
                doublequote=self.config.doublequote,
                memory_map=self.config.memory_map,
                float_precision=self.config.float_precision,
                chunksize=self.config.chunksize,
            )
            for batch_idx, df in enumerate(csv_file_reader):
                pa_table = pa.Table.from_pandas(df, schema=schema)
                # Uncomment for debugging (will print the Arrow table size and elements)
                # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                yield (file_idx, batch_idx), pa_table
