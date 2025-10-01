import itertools
from dataclasses import dataclass
from typing import Optional, Union

import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

import datasets
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


def _is_nested_type(pa_type):
    """Check if a PyArrow type contains nested structures."""
    return (
        pa.types.is_list(pa_type)
        or pa.types.is_large_list(pa_type)
        or pa.types.is_struct(pa_type)
        or pa.types.is_map(pa_type)
        or pa.types.is_union(pa_type)
    )


def _handle_nested_chunked_conversion(pa_table):
    """Handle PyArrow nested data conversion issues by combining chunks selectively."""
    try:
        # Check if any columns have multiple chunks with nested data
        needs_combining = False
        for column_name in pa_table.column_names:
            column = pa_table.column(column_name)
            if isinstance(column, pa.ChunkedArray) and column.num_chunks > 1:
                # Check if column contains nested types
                if _is_nested_type(column.type):
                    needs_combining = True
                    break

        if needs_combining:
            # Combine chunks only for problematic columns to minimize memory impact
            combined_columns = {}
            for column_name in pa_table.column_names:
                column = pa_table.column(column_name)
                if (
                    isinstance(column, pa.ChunkedArray)
                    and column.num_chunks > 1
                    and _is_nested_type(column.type)
                ):
                    combined_columns[column_name] = column.combine_chunks()
                else:
                    combined_columns[column_name] = column

            return pa.table(combined_columns)

        return pa_table

    except Exception as e:
        # Fallback: combine all chunks if selective approach fails
        logger.warning(
            f"Selective chunk combining failed, using full combine_chunks(): {e}"
        )
        return pa_table.combine_chunks()


@dataclass
class ParquetConfig(datasets.BuilderConfig):
    """BuilderConfig for Parquet."""

    batch_size: Optional[int] = None
    columns: Optional[list[str]] = None
    features: Optional[datasets.Features] = None
    filters: Optional[Union[ds.Expression, list[tuple], list[list[tuple]]]] = None

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
            raise ValueError(
                f"At least one data file must be specified, but got data_files={self.config.data_files}"
            )
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            # Use `dl_manager.iter_files` to skip hidden files in an extracted archive
            files = [dl_manager.iter_files(file) for file in files]
            # Infer features if they are stored in the arrow schema
            if self.info.features is None:
                for file in itertools.chain.from_iterable(files):
                    with open(file, "rb") as f:
                        self.info.features = datasets.Features.from_arrow_schema(
                            pq.read_schema(f)
                        )
                    break
            splits.append(
                datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files})
            )
        if self.config.columns is not None and set(self.config.columns) != set(
            self.info.features
        ):
            self.info.features = datasets.Features(
                {
                    col: feat
                    for col, feat in self.info.features.items()
                    if col in self.config.columns
                }
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        if self.config.features is not None and self.config.columns is not None:
            if sorted(field.name for field in self.info.features.arrow_schema) != sorted(
                self.config.columns
            ):
                raise ValueError(
                    f"Tried to load parquet data with columns '{self.config.columns}' with mismatching features '{self.info.features}'"
                )
        filter_expr = (
            pq.filters_to_expression(self.config.filters)
            if isinstance(self.config.filters, list)
            else self.config.filters
        )
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            with open(file, "rb") as f:
                parquet_fragment = ds.ParquetFileFormat().make_fragment(f)
                if parquet_fragment.row_groups:
                    batch_size = (
                        self.config.batch_size or parquet_fragment.row_groups[0].num_rows
                    )
                    try:
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
                            yield f"{file_idx}_{batch_idx}", self._cast_table(pa_table)
                    except pa.ArrowNotImplementedError as e:
                        if (
                            "Nested data conversions not implemented for chunked array outputs"
                            in str(e)
                        ):
                            # Fallback for nested data: bypass fragment reading entirely
                            logger.warning(
                                f"Using fallback for nested data in file '{file}': {e}"
                            )
                            try:
                                # Reset file pointer and use direct parquet file reading
                                f.seek(0)
                                parquet_file = pq.ParquetFile(f)

                                # Read row groups one by one to avoid chunking issues
                                tables = []
                                for row_group_idx in range(
                                    parquet_file.num_row_groups
                                ):
                                    try:
                                        # Read single row group
                                        rg_table = parquet_file.read_row_group(
                                            row_group_idx,
                                            columns=self.config.columns,
                                            use_pandas_metadata=False,
                                        )

                                        # Apply filter if needed
                                        if filter_expr is not None:
                                            rg_table = rg_table.filter(filter_expr)

                                        # Immediately combine chunks
                                        if rg_table.num_rows > 0:
                                            rg_table = (
                                                _handle_nested_chunked_conversion(
                                                    rg_table
                                                )
                                            )
                                            tables.append(rg_table)

                                    except pa.ArrowNotImplementedError as rg_error:
                                        if (
                                            "Nested data conversions not implemented"
                                            in str(rg_error)
                                        ):
                                            logger.warning(
                                                f"Skipping row group {row_group_idx} due to nested data issues: {rg_error}"
                                            )
                                            continue
                                        else:
                                            raise

                                if not tables:
                                    logger.error(
                                        f"Could not read any row groups from file '{file}'"
                                    )
                                    continue

                                # Combine all readable row groups
                                full_table = (
                                    pa.concat_tables(tables)
                                    if len(tables) > 1
                                    else tables[0]
                                )

                                # Split into batches manually
                                for batch_idx in range(
                                    0, full_table.num_rows, batch_size
                                ):
                                    end_idx = min(
                                        batch_idx + batch_size, full_table.num_rows
                                    )
                                    batch_table = full_table.slice(
                                        batch_idx, end_idx - batch_idx
                                    )
                                    yield f"{file_idx}_{batch_idx // batch_size}", (
                                        self._cast_table(batch_table)
                                    )

                            except Exception as fallback_error:
                                logger.error(
                                    f"Fallback approach also failed for file '{file}': {fallback_error}"
                                )
                                raise
                        else:
                            # Re-raise if it's a different Arrow error
                            raise
