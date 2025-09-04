import io
import itertools
from dataclasses import dataclass
from typing import Optional

import pandas as pd
import pyarrow as pa
import pyarrow.json as paj

import datasets
import datasets.config
from datasets.table import table_cast
from datasets.utils.file_utils import readline


logger = datasets.utils.logging.get_logger(__name__)


def ujson_dumps(*args, **kwargs):
    try:
        return pd.io.json.ujson_dumps(*args, **kwargs)
    except AttributeError:
        # Before pandas-2.2.0, ujson_dumps was renamed to dumps: import ujson_dumps as dumps
        return pd.io.json.dumps(*args, **kwargs)


def ujson_loads(*args, **kwargs):
    try:
        return pd.io.json.ujson_loads(*args, **kwargs)
    except AttributeError:
        # Before pandas-2.2.0, ujson_loads was renamed to loads: import ujson_loads as loads
        return pd.io.json.loads(*args, **kwargs)


def pandas_read_json(path_or_buf, **kwargs):
    if datasets.config.PANDAS_VERSION.major >= 2:
        kwargs["dtype_backend"] = "pyarrow"
    return pd.read_json(path_or_buf, **kwargs)


@dataclass
class JsonConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    features: Optional[datasets.Features] = None
    encoding: str = "utf-8"
    encoding_errors: Optional[str] = None
    field: Optional[str] = None
    use_threads: bool = True  # deprecated
    block_size: Optional[int] = None  # deprecated
    chunksize: int = 10 << 20  # 10MB
    newlines_in_values: Optional[bool] = None
    columns: Optional[List[str]] = None

    def __post_init__(self):
        super().__post_init__()


class Json(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = JsonConfig

    def _info(self):
        if self.config.block_size is not None:
            logger.warning("The JSON loader parameter `block_size` is deprecated. Please use `chunksize` instead")
            self.config.chunksize = self.config.block_size
        if self.config.use_threads is not True:
            logger.warning(
                "The JSON loader parameter `use_threads` is deprecated and doesn't have any effect anymore."
            )
        if self.config.newlines_in_values is not None:
            raise ValueError("The JSON loader parameter `newlines_in_values` is no longer supported")
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files = [dl_manager.iter_files(file) for file in files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            # adding missing columns
            for column_name in set(self.config.features) - set(pa_table.column_names):
                type = self.config.features.arrow_schema.field(column_name).type
                pa_table = pa_table.append_column(column_name, pa.array([None] * len(pa_table), type=type))
            # convert to string when needed
            for i, column_name in enumerate(pa_table.column_names):
                if pa.types.is_struct(pa_table[column_name].type) and self.config.features.get(
                    column_name, None
                ) == datasets.Value("string"):
                    jsonl = (
                        pa_table[column_name]
                        .to_pandas(types_mapper=pd.ArrowDtype)
                        .to_json(orient="records", lines=True)
                    )
                    string_array = pa.array(
                        ("{" + x.rstrip() for x in ("\n" + jsonl).split("\n{") if x), type=pa.string()
                    )
                    pa_table = pa_table.set_column(i, column_name, string_array)
            # more expensive cast to support nested structures with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.config.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            if self.config.field is not None:
                # Load JSON with field selection
                try:
                    import ijson
                    for batch_idx, json_obj in enumerate(
                        ijson.items(
                            open(
                                file,
                                encoding=self.config.encoding,
                                errors=self.config.encoding_errors,
                            ),
                            self.config.field,
                        )
                    ):
                        pa_table = pa.Table.from_pandas(pd.DataFrame(json_obj))
                        # Apply columns filtering if requested
                        if self.config.columns is not None:
                            missing_cols = set(self.config.columns) - set(pa_table.column_names)
                            for col in missing_cols:
                                pa_table = pa_table.append_column(col, pa.array([None] * pa_table.num_rows))
                            pa_table = pa_table.select(self.config.columns)
                        yield (file_idx, batch_idx), self._cast_table(pa_table)

                except Exception as e:
                    raise datasets.DatasetGenerationError(
                        f"Failed to parse JSON with field {self.config.field}: {e}"
                    ) from e

            else:
                # Load JSON line by line
                batch_idx = 0
                try:
                    pa_table = paj.read_json(
                        file,
                        read_options=paj.ReadOptions(
                            use_threads=True,
                            block_size=1 << 20,  # 1MB default
                        ),
                        parse_options=paj.ParseOptions(explicit_schema=None),
                    )
                except pa.ArrowInvalid:
                    # Pandas fallback only if Arrow fails
                    with open(
                        file,
                        encoding=self.config.encoding,
                        errors=self.config.encoding_errors,
                    ) as f:
                        df = pandas_read_json(f)
                    pa_table = pa.Table.from_pandas(df)
                except StopIteration:
                    # End of file
                    return

                # Apply columns filtering if requested
                if self.config.columns is not None:
                    missing_cols = set(self.config.columns) - set(pa_table.column_names)
                    for col in missing_cols:
                        pa_table = pa_table.append_column(col, pa.array([None] * pa_table.num_rows))
                    pa_table = pa_table.select(self.config.columns)

                yield (file_idx, batch_idx), self._cast_table(pa_table)

