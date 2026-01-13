from dataclasses import dataclass
from typing import Literal, Optional, Union

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

import datasets
from datasets.builder import Key
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ParquetConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Parquet.

    Args:
        batch_size (`int`, *optional*):
            Size of the RecordBatches to iterate on.
            The default is the row group size (defined by the first row group).
        columns (`list[str]`, *optional*)
            List of columns to load, the other ones are ignored.
            All columns are loaded by default.
        features: (`Features`, *optional*):
            Cast the data to `features`.
        filters (`Union[pyarrow.dataset.Expression, list[tuple], list[list[tuple]]]`, *optional*):
            Return only the rows matching the filter.
            If possible the predicate will be pushed down to exploit the partition information
            or internal metadata found in the data source, e.g. Parquet statistics.
            Otherwise filters the loaded RecordBatches before yielding them.
        fragment_scan_options (`pyarrow.dataset.ParquetFragmentScanOptions`, *optional*)
            Scan-specific options for Parquet fragments.
            This is especially useful to configure buffering and caching.

            <Added version="4.2.0"/>
        on_bad_files (`Literal["error", "warn", "skip"]`, *optional*, defaults to "error")
            Specify what to do upon encountering a bad file (a file that can't be read). Allowed values are :
            * 'error', raise an Exception when a bad file is encountered.
            * 'warn', raise a warning when a bad file is encountered and skip that file.
            * 'skip', skip bad files without raising or warning when they are encountered.

            <Added version="4.2.0"/>

    Example:

    Load a subset of columns:

    ```python
    >>> ds = load_dataset(parquet_dataset_id, columns=["col_0", "col_1"])
    ```

    Stream data and efficiently filter data, possibly skipping entire files or row groups:

    ```python
    >>> filters = [("col_0", "==", 0)]
    >>> ds = load_dataset(parquet_dataset_id, streaming=True, filters=filters)
    ```

    Increase the minimum request size when streaming from 32MiB (default) to 128MiB and enable prefetching:

    ```python
    >>> import pyarrow
    >>> import pyarrow.dataset
    >>> fragment_scan_options = pyarrow.dataset.ParquetFragmentScanOptions(
    ...     cache_options=pyarrow.CacheOptions(
    ...         prefetch_limit=1,
    ...         range_size_limit=128 << 20
    ...     ),
    ... )
    >>> ds = load_dataset(parquet_dataset_id, streaming=True, fragment_scan_options=fragment_scan_options)
    ```

    """

    batch_size: Optional[int] = None
    columns: Optional[list[str]] = None
    features: Optional[datasets.Features] = None
    filters: Optional[Union[ds.Expression, list[tuple], list[list[tuple]]]] = None
    fragment_scan_options: Optional[ds.ParquetFragmentScanOptions] = None
    on_bad_files: Literal["error", "warn", "skip"] = "error"

    def __post_init__(self):
        super().__post_init__()


class Parquet(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = ParquetConfig

    def _info(self):
        if (
            self.config.columns is not None
            and self.config.features is not None
            and set(self.config.columns) != set(self.config.features)
        ):
            raise ValueError(
                "The columns and features argument must contain the same columns, but got ",
                f"{self.config.columns} and {self.config.features}",
            )
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            # Infer features if they are stored in the arrow schema
            if self.info.features is None:
                for file in files:
                    try:
                        with open(file, "rb") as f:
                            self.info.features = datasets.Features.from_arrow_schema(pq.read_schema(f))
                            break
                    except pa.ArrowInvalid as e:
                        if self.config.on_bad_files == "error":
                            logger.error(f"Failed to read schema from '{file}' with error {type(e).__name__}: {e}")
                            raise
                        elif self.config.on_bad_files == "warn":
                            logger.warning(f"Skipping bad schema from '{file}'. {type(e).__name__}: {e}`")
                        else:
                            logger.debug(f"Skipping bad schema from '{file}'. {type(e).__name__}: {e}`")
            if self.info.features is None:
                raise ValueError(
                    f"At least one valid data file must be specified, all the data_files are invalid: {self.config.data_files}"
                )
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        if self.config.columns is not None and set(self.config.columns) != set(self.info.features):
            self.info.features = datasets.Features(
                {col: feat for col, feat in self.info.features.items() if col in self.config.columns}
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_shards(self, files):
        yield from files

    def _generate_tables(self, files):
        if self.config.features is not None and self.config.columns is not None:
            if sorted(field.name for field in self.info.features.arrow_schema) != sorted(self.config.columns):
                raise ValueError(
                    f"Tried to load parquet data with columns '{self.config.columns}' with mismatching features '{self.info.features}'"
                )
        filter_expr = (
            pq.filters_to_expression(self.config.filters)
            if isinstance(self.config.filters, list)
            else self.config.filters
        )
        parquet_file_format = ds.ParquetFileFormat(default_fragment_scan_options=self.config.fragment_scan_options)
        for file_idx, file in enumerate(files):
            try:
                with open(file, "rb") as f:
                    parquet_fragment = parquet_file_format.make_fragment(f)
                    if parquet_fragment.row_groups:
                        batch_size = self.config.batch_size or parquet_fragment.row_groups[0].num_rows
                        for batch_idx, record_batch in enumerate(
                            parquet_fragment.to_batches(
                                batch_size=batch_size,
                                columns=self.config.columns,
                                filter=filter_expr,
                                batch_readahead=0,
                                fragment_readahead=0,
                            )
                        ):
                            pa_table = pa.Table.from_batches([record_batch])
                            # Uncomment for debugging (will print the Arrow table size and elements)
                            # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                            # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                            yield Key(file_idx, batch_idx), self._cast_table(pa_table)
            except (pa.ArrowInvalid, ValueError) as e:
                if self.config.on_bad_files == "error":
                    logger.error(f"Failed to read file '{file}' with error {type(e).__name__}: {e}")
                    raise
                elif self.config.on_bad_files == "warn":
                    logger.warning(f"Skipping bad file '{file}'. {type(e).__name__}: {e}`")
                else:
                    logger.debug(f"Skipping bad file '{file}'. {type(e).__name__}: {e}`")
