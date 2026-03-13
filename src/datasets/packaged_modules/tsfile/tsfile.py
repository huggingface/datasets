# Copyright 2025 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Apache TsFile dataset builder for time-series data."""

import itertools
from dataclasses import dataclass
from typing import Optional

import pyarrow as pa

import datasets
from datasets.builder import Key


logger = datasets.utils.logging.get_logger(__name__)

EXTENSIONS = [".tsfile"]


@dataclass
class TsFileConfig(datasets.BuilderConfig):
    """BuilderConfig for Apache TsFile.

    Args:
        batch_size (`int`, *optional*, defaults to 10000):
            Number of rows per batch when reading from TsFile.
        features (`Features`, *optional*):
            Cast the data to `features`.
        table_name (`str`, *optional*):
            Name of the table to query in table-model TsFiles.
            If None, the first table found will be used.
        columns (`list[str]`, *optional*):
            List of columns to load. If None, all columns are loaded.
        start_time (`int`, *optional*):
            Start timestamp for time-range filtering (inclusive).
            If None, reads from the beginning.
        end_time (`int`, *optional*):
            End timestamp for time-range filtering (inclusive).
            If None, reads until the end.

    Example:

    Load a TsFile dataset:

    ```python
    >>> ds = load_dataset("tsfile", data_files=["data.tsfile"])
    ```

    Load with time-range filtering:

    ```python
    >>> ds = load_dataset("tsfile", data_files=["data.tsfile"], start_time=1609459200000, end_time=1640995200000)
    ```

    Load specific columns:

    ```python
    >>> ds = load_dataset("tsfile", data_files=["data.tsfile"], columns=["temperature", "humidity"])
    ```
    """

    batch_size: int = 10000
    features: Optional[datasets.Features] = None
    table_name: Optional[str] = None
    columns: Optional[list[str]] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None

    def __post_init__(self):
        super().__post_init__()


class TsFile(datasets.ArrowBasedBuilder):
    """ArrowBasedBuilder for Apache TsFile time-series data format.

    TsFile is a columnar storage file format designed for time-series data,
    providing efficient compression and high query performance.
    """

    BUILDER_CONFIG_CLASS = TsFileConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """Handle string, list and dicts in datafiles."""

        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []

        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]

            files = [dl_manager.iter_files(file) for file in files]

            # Infer features from first file if not provided
            if self.info.features is None:
                for first_file in itertools.chain.from_iterable(files):
                    try:
                        self.info.features = self._infer_features_from_file(first_file)
                        break
                    except Exception as e:
                        logger.warning(f"Failed to infer features from '{first_file}': {e}")

            if self.info.features is None:
                raise ValueError(
                    "Could not infer features from data files. "
                    "Please specify features explicitly or ensure data files are valid TsFiles."
                )

            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))

        return splits

    def _infer_features_from_file(self, file_path: str) -> datasets.Features:
        """Infer features from a TsFile's schema."""
        from tsfile import TSDataType, TsFileReader

        # Map TsFile data type values (integers) to HuggingFace datasets Value types
        # TSDataType enum values: BOOLEAN=0, INT32=1, INT64=2, FLOAT=3, DOUBLE=4, TEXT=5, etc.
        dtype_mapping = {
            TSDataType.BOOLEAN.value: "bool",
            TSDataType.INT32.value: "int32",
            TSDataType.INT64.value: "int64",
            TSDataType.FLOAT.value: "float32",
            TSDataType.DOUBLE.value: "float64",
            TSDataType.TEXT.value: "string",
            TSDataType.STRING.value: "string",
            TSDataType.TIMESTAMP.value: "int64",
            TSDataType.DATE.value: "int32",
            TSDataType.BLOB.value: "binary",
        }

        features_dict = {}

        with TsFileReader(file_path) as reader:
            # Try table-model first
            table_schemas = reader.get_all_table_schemas()
            if table_schemas:
                # Use specified table or first available
                table_name = self.config.table_name
                if table_name is None:
                    table_name = list(table_schemas.keys())[0]

                if table_name not in table_schemas:
                    raise ValueError(f"Table '{table_name}' not found. Available tables: {list(table_schemas.keys())}")

                schema = table_schemas[table_name]
                for column in schema.columns:
                    col_name = column.column_name
                    if self.config.columns is None or col_name in self.config.columns:
                        # data_type is an integer matching TSDataType enum values
                        hf_dtype = dtype_mapping.get(column.data_type, "string")
                        features_dict[col_name] = datasets.Value(hf_dtype)

                # Add time column
                features_dict["time"] = datasets.Value("int64")

            else:
                # Fall back to tree-model (timeseries)
                timeseries_schemas = reader.get_all_timeseries_schemas()
                for ts in timeseries_schemas:
                    column_name = f"{ts.device_id}.{ts.measurement_id}"
                    if self.config.columns is None or column_name in self.config.columns:
                        hf_dtype = dtype_mapping.get(ts.data_type, "string")
                        features_dict[column_name] = datasets.Value(hf_dtype)

                # Add time column
                features_dict["time"] = datasets.Value("int64")

        if not features_dict:
            raise ValueError(f"No features could be inferred from '{file_path}'")

        return datasets.Features(features_dict)

    def _generate_tables(self, files):
        """Generate PyArrow tables from TsFile data."""
        from tsfile import to_dataframe

        batch_size = self.config.batch_size or 10000

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            try:
                # Use to_dataframe with iterator for memory efficiency
                df_iterator = to_dataframe(
                    file_path=file,
                    table_name=self.config.table_name,
                    column_names=self.config.columns,
                    start_time=self.config.start_time,
                    end_time=self.config.end_time,
                    max_row_num=batch_size,
                    as_iterator=True,
                )

                for batch_idx, df in enumerate(df_iterator):
                    if df.empty:
                        continue

                    # Convert pandas DataFrame to PyArrow Table
                    pa_table = pa.Table.from_pandas(df, preserve_index=False)

                    # Cast to features if specified
                    if self.info.features is not None:
                        # Filter columns to match expected features
                        available_cols = set(pa_table.column_names)
                        expected_cols = set(self.info.features.keys())
                        cols_to_keep = available_cols & expected_cols

                        if cols_to_keep:
                            pa_table = pa_table.select(list(cols_to_keep))

                    yield Key(file_idx, batch_idx), pa_table

            except Exception as e:
                logger.error(f"Failed to read file '{file}' with error {type(e).__name__}: {e}")
                raise
