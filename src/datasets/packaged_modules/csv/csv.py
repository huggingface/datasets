import io
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

import pandas as pd
import pyarrow as pa

import datasets
import datasets.config
from datasets.builder import Key
from datasets.features.features import require_storage_cast
from datasets.table import table_cast
from datasets.utils.py_utils import Literal


logger = datasets.utils.logging.get_logger(__name__)

_PANDAS_READ_CSV_NO_DEFAULT_PARAMETERS = ["names", "prefix"]
_PANDAS_READ_CSV_DEPRECATED_PARAMETERS = ["warn_bad_lines", "error_bad_lines", "mangle_dupe_cols"]
_PANDAS_READ_CSV_NEW_1_3_0_PARAMETERS = ["encoding_errors", "on_bad_lines"]
_PANDAS_READ_CSV_NEW_2_0_0_PARAMETERS = ["date_format"]
_PANDAS_READ_CSV_DEPRECATED_2_2_0_PARAMETERS = ["verbose"]


@dataclass
class CsvConfig(datasets.BuilderConfig):
    """BuilderConfig for CSV."""

    sep: str = ","
    delimiter: Optional[str] = None
    header: Optional[Union[int, list[int], str]] = "infer"
    names: Optional[list[str]] = None
    column_names: Optional[list[str]] = None
    index_col: Optional[Union[int, str, list[int], list[str]]] = None
    usecols: Optional[Union[list[int], list[str]]] = None
    prefix: Optional[str] = None
    mangle_dupe_cols: bool = True
    engine: Optional[Literal["c", "python", "pyarrow"]] = None
    converters: dict[Union[int, str], Callable[[Any], Any]] = None
    true_values: Optional[list] = None
    false_values: Optional[list] = None
    skipinitialspace: bool = False
    skiprows: Optional[Union[int, list[int]]] = None
    nrows: Optional[int] = None
    na_values: Optional[Union[str, list[str]]] = None
    keep_default_na: bool = True
    na_filter: bool = True
    verbose: bool = False
    skip_blank_lines: bool = True
    thousands: Optional[str] = None
    decimal: str = "."
    lineterminator: Optional[str] = None
    quotechar: str = '"'
    quoting: int = 0
    escapechar: Optional[str] = None
    comment: Optional[str] = None
    encoding: Optional[str] = None
    dialect: Optional[str] = None
    error_bad_lines: bool = True
    warn_bad_lines: bool = True
    skipfooter: int = 0
    doublequote: bool = True
    memory_map: bool = False
    float_precision: Optional[str] = None
    chunksize: int = 10_000
    features: Optional[datasets.Features] = None
    encoding_errors: Optional[str] = "strict"
    on_bad_lines: Literal["error", "warn", "skip"] = "error"
    date_format: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.delimiter is not None:
            self.sep = self.delimiter
        if self.column_names is not None:
            self.names = self.column_names

    @property
    def pd_read_csv_kwargs(self):
        pd_read_csv_kwargs = {
            "sep": self.sep,
            "header": self.header,
            "names": self.names,
            "index_col": self.index_col,
            "usecols": self.usecols,
            "prefix": self.prefix,
            "mangle_dupe_cols": self.mangle_dupe_cols,
            "engine": self.engine,
            "converters": self.converters,
            "true_values": self.true_values,
            "false_values": self.false_values,
            "skipinitialspace": self.skipinitialspace,
            "skiprows": self.skiprows,
            "nrows": self.nrows,
            "na_values": self.na_values,
            "keep_default_na": self.keep_default_na,
            "na_filter": self.na_filter,
            "verbose": self.verbose,
            "skip_blank_lines": self.skip_blank_lines,
            "thousands": self.thousands,
            "decimal": self.decimal,
            "lineterminator": self.lineterminator,
            "quotechar": self.quotechar,
            "quoting": self.quoting,
            "escapechar": self.escapechar,
            "comment": self.comment,
            "encoding": self.encoding,
            "dialect": self.dialect,
            "error_bad_lines": self.error_bad_lines,
            "warn_bad_lines": self.warn_bad_lines,
            "skipfooter": self.skipfooter,
            "doublequote": self.doublequote,
            "memory_map": self.memory_map,
            "float_precision": self.float_precision,
            "chunksize": self.chunksize,
            "encoding_errors": self.encoding_errors,
            "on_bad_lines": self.on_bad_lines,
            "date_format": self.date_format,
        }

        # some kwargs must not be passed if they don't have a default value
        # some others are deprecated and we can also not pass them if they are the default value
        for pd_read_csv_parameter in _PANDAS_READ_CSV_NO_DEFAULT_PARAMETERS + _PANDAS_READ_CSV_DEPRECATED_PARAMETERS:
            if pd_read_csv_kwargs[pd_read_csv_parameter] == getattr(CsvConfig(), pd_read_csv_parameter):
                del pd_read_csv_kwargs[pd_read_csv_parameter]

        # Remove 1.3 new arguments
        if not (datasets.config.PANDAS_VERSION.major >= 1 and datasets.config.PANDAS_VERSION.minor >= 3):
            for pd_read_csv_parameter in _PANDAS_READ_CSV_NEW_1_3_0_PARAMETERS:
                del pd_read_csv_kwargs[pd_read_csv_parameter]

        # Remove 2.0 new arguments
        if not (datasets.config.PANDAS_VERSION.major >= 2):
            for pd_read_csv_parameter in _PANDAS_READ_CSV_NEW_2_0_0_PARAMETERS:
                del pd_read_csv_kwargs[pd_read_csv_parameter]

        # Remove 2.2 deprecated arguments
        if datasets.config.PANDAS_VERSION.release >= (2, 2):
            for pd_read_csv_parameter in _PANDAS_READ_CSV_DEPRECATED_2_2_0_PARAMETERS:
                if pd_read_csv_kwargs[pd_read_csv_parameter] == getattr(CsvConfig(), pd_read_csv_parameter):
                    del pd_read_csv_kwargs[pd_read_csv_parameter]

        return pd_read_csv_kwargs


class Csv(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = CsvConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        base_data_files = dl_manager.download(self.config.data_files)
        extracted_data_files = dl_manager.extract(base_data_files)
        splits = []
        for split_name, extracted_files in extracted_data_files.items():
            files_iterables = [dl_manager.iter_files(extracted_file) for extracted_file in extracted_files]
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"files_iterables": files_iterables, "base_files": base_data_files[split_name]},
                )
            )
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

    def _generate_shards(self, base_files, files_iterables):
        yield from base_files

    def _estimate_byte_size_per_line(self, file, max_bytes=20 << 20):
        """Estimate the byte size per line by reading the first max_bytes (default 20MB)."""
        try:
            with open(
                file,
                "r",
                encoding=self.config.encoding or "utf-8",
                errors=self.config.encoding_errors or "strict",
            ) as f:
                line_count = 0
                bytes_read = 0

                while bytes_read < max_bytes:
                    line = f.readline()
                    if not line:
                        break
                    line_count += 1
                    bytes_read += len(line.encode())
                if line_count > 0:
                    return bytes_read // line_count
                else:
                    return 0
        except Exception:
            return 0

    def _generate_more_gen_kwargs(self, base_files, files_iterables, num_shards=None):
        """Generate more gen_kwargs for resharding.
        When num_shards is specified, create that many shards.
        When num_shards is None, maximize sharding by aiming for self.config.chunksize lines per shard.
        """
        for base_file, files_iterable in zip(base_files, files_iterables):
            files_list = list(files_iterable)

            if not files_list:
                continue

            # Estimate total line count from the first file only (assuming similar structure)
            line_size = 0
            for file in files_list:
                file_size = os.path.getsize(file)
                if line_size == 0:
                    line_size = self._estimate_byte_size_per_line(file)
                    if line_size == 0:
                        yield {"base_files": [base_file], "files_iterables": [[(file, 0, file_size)]]}
                        continue

                # Calculate shard size and number of shards
                # If num_shards is specified, use that number of shards
                # If num_shards is None, aim use self.config.chunksize lines per shard
                if num_shards is None:
                    target_num_shards = max(1, file_size // (self.config.chunksize * line_size))
                else:
                    target_num_shards = max(1, num_shards)
                shard_size = max(1, file_size // target_num_shards)

                if target_num_shards <= 1:
                    yield {
                        "base_files": [base_file],
                        "files_iterables": [[(file, 0, file_size)]],
                    }
                    continue

                for i in range(target_num_shards):
                    start = i * shard_size
                    if start >= file_size:
                        break

                    end = (i + 1) * shard_size if i < target_num_shards - 1 else file_size

                    if end > file_size:
                        end = file_size

                    yield {
                        "base_files": [base_file],
                        "files_iterables": [[(file, start, end)]],
                    }
                    if end >= file_size:
                        break

    def _generate_tables(self, base_files, files_iterables):
        schema = self.config.features.arrow_schema if self.config.features else None
        # dtype allows reading an int column as str
        dtype = (
            {
                name: dtype.to_pandas_dtype() if not require_storage_cast(feature) else object
                for name, dtype, feature in zip(schema.names, schema.types, self.config.features.values())
            }
            if schema is not None
            else None
        )

        for shard_idx, files_iterable in enumerate(files_iterables):
            for file_item in files_iterable:
                if isinstance(file_item, tuple):
                    file, start_byte, end_byte = file_item
                else:
                    file, start_byte, end_byte = file_item, 0, None
                file_path = file
                with open(file, "rb") as f:
                    header_line = f.readline()
                    header_end_pos = f.tell()
                    if start_byte > 0:
                        # If start_byte is before the header, skip the header
                        if start_byte < header_end_pos:
                            f.seek(header_end_pos)
                        else:
                            f.seek(start_byte)
                        f.readline()

                    current_pos = f.tell()

                    if end_byte is not None and current_pos >= end_byte:
                        if not (start_byte < header_end_pos and current_pos == header_end_pos):
                            continue

                    if end_byte is not None:
                        bytes_to_read = max(0, end_byte - current_pos)
                        content = f.read(bytes_to_read)
                        if f.tell() < os.path.getsize(file):
                            content += f.readline()
                    else:
                        content = f.read()

                    if not content or not content.strip(b"\r\n "):
                        continue
                    shard_data = header_line + content
                    file = io.BytesIO(shard_data)

                read_csv_kwargs = self.config.pd_read_csv_kwargs.copy()
                csv_file_reader = pd.read_csv(file, iterator=True, dtype=dtype, **read_csv_kwargs)
                try:
                    for batch_idx, df in enumerate(csv_file_reader):
                        pa_table = pa.Table.from_pandas(df)
                        # Uncomment for debugging (will print Arrow table size and elements)
                        # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                        # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                        yield Key(shard_idx, batch_idx), self._cast_table(pa_table)
                except ValueError as e:
                    logger.error(f"Failed to read file '{file_path}' with error {type(e)}: {e}")
                    raise
