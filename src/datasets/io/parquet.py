import json
import os
from typing import BinaryIO, Optional, Union

import fsspec
import pyarrow as pa
import pyarrow.parquet as pq
from packaging import version

from .. import Dataset, Features, NamedSplit, config
from ..arrow_writer import get_writer_batch_size_from_data_size, get_writer_batch_size_from_features
from ..features.features import require_storage_embed
from ..formatting import query_table
from ..packaged_modules import _PACKAGED_DATASETS_MODULES
from ..packaged_modules.parquet.parquet import Parquet
from ..utils import tqdm as hf_tqdm
from ..utils.typing import NestedDataStructureLike, PathLike
from .abc import AbstractDatasetReader


def _get_parquet_features(features: Features, **writer_options) -> Features:
    """Round-trip feature metadata through the schema conversion used by the Parquet reader."""
    buffer = pa.BufferOutputStream()
    pq.write_metadata(features.arrow_schema, buffer, **writer_options)
    return Features.from_arrow_schema(pq.read_schema(pa.BufferReader(buffer.getvalue())))


def _get_parquet_temporal_writer_options(metadata: pq.FileMetaData) -> dict:
    """Recover temporal annotations from every physical leaf, including nested columns."""
    logical_types = [json.loads(metadata.schema.column(i).logical_type.to_json()) for i in range(metadata.num_columns)]
    options = {}
    if any(logical.get("Type") == "Time" and logical["isAdjustedToUTC"] for logical in logical_types):
        options["write_time_adjusted_to_utc"] = True
    timestamp_units = {logical["timeUnit"] for logical in logical_types if logical.get("Type") == "Timestamp"}
    if len(timestamp_units) == 1:
        unit = {"milliseconds": "ms", "microseconds": "us"}.get(next(iter(timestamp_units)))
        if unit is not None:
            # The footer stores the effective precision, not the original truncation
            # policy. Quantize new values to that precision, as the original writer did.
            options.update(coerce_timestamps=unit, allow_truncated_timestamps=True)
    return options


def _append_parquet_file(dataset: Dataset, original: str, destination: str) -> None:
    """Preserve the encoded row groups and page indexes, then append rows and a combined footer."""
    metadata = pq.read_metadata(original)
    schema = metadata.schema.to_arrow_schema()
    row_group_size = max(
        (metadata.row_group(i).num_rows for i in range(metadata.num_row_groups)),
        default=0,
    ) or get_writer_batch_size_from_data_size(len(dataset), dataset._estimate_nbytes())
    writer_options = (
        {"use_content_defined_chunking": True} if config.PYARROW_VERSION >= version.parse("21.0.0") else {}
    )
    writer_options.update(_get_parquet_temporal_writer_options(metadata))
    # Preserve the physical list schema of shards produced before Arrow's compliant-list default.
    writer_options["use_compliant_nested_type"] = not any(
        ".list." in metadata.schema.column(i).path
        and metadata.schema.column(i).path.split(".list.", 1)[1].split(".")[0] != "element"
        for i in range(metadata.num_columns)
    )
    writer_options["use_deprecated_int96_timestamps"] = any(
        metadata.schema.column(i).physical_type == "INT96" for i in range(metadata.num_columns)
    )
    writer_options["store_decimal_as_integer"] = any(
        metadata.schema.column(i).converted_type == "DECIMAL"
        and metadata.schema.column(i).physical_type in {"INT32", "INT64"}
        for i in range(metadata.num_columns)
    )
    writer_options["version"] = metadata.format_version
    if metadata.num_row_groups:
        # Properties are per physical leaf, including nested columns. Reuse the
        # tail's codecs and encodings rather than the Dataset writer's defaults.
        row_group = metadata.row_group(metadata.num_row_groups - 1)
        columns = [row_group.column(i) for i in range(metadata.num_columns)]
        dictionary_columns = [
            column.path_in_schema
            for column in columns
            if {"PLAIN_DICTIONARY", "RLE_DICTIONARY"}.intersection(column.encodings)
        ]
        writer_options.update(
            compression={
                column.path_in_schema: "none" if column.compression == "UNCOMPRESSED" else column.compression.lower()
                for column in columns
            },
            use_dictionary=dictionary_columns,
            column_encoding={
                column.path_in_schema: encoding
                for column in columns
                if column.path_in_schema not in dictionary_columns
                for encoding in column.encodings
                if encoding
                in {"PLAIN", "BYTE_STREAM_SPLIT", "DELTA_BINARY_PACKED", "DELTA_LENGTH_BYTE_ARRAY", "DELTA_BYTE_ARRAY"}
            },
            write_statistics=[column.path_in_schema for column in columns if column.is_stats_set],
            write_page_index=any(column.has_column_index or column.has_offset_index for column in columns),
        )
    new_metadata = []
    with open(original, "rb") as source, pa.OSFile(destination, "wb") as sink:
        source.seek(-8, os.SEEK_END)
        footer_size = int.from_bytes(source.read(4), "little")
        prefix_size = source.tell() - 4 - footer_size
        source.seek(4)  # The writer emits the initial PAR1 magic itself.
        with pq.ParquetWriter(
            sink,
            schema=schema,
            metadata_collector=new_metadata,
            **writer_options,
        ) as writer:
            # Write through the same Arrow sink so the new column/page offsets include the old bytes.
            # Re-encoding old row groups would move their page indexes and could change their encoding.
            remaining = prefix_size - 4
            while remaining:
                block = source.read(min(remaining, 1024 * 1024))
                if not block:
                    raise ValueError("Unexpected end of the existing Parquet shard")
                sink.write(block)
                remaining -= len(block)
            for batch in dataset.with_format("arrow").iter(batch_size=row_group_size):
                writer.write_table(
                    batch.select(schema.names).cast(
                        schema, safe=not writer_options.get("allow_truncated_timestamps", False)
                    ),
                    row_group_size=row_group_size,
                )

    metadata.append_row_groups(new_metadata[0])
    footer = pa.BufferOutputStream()
    metadata.write_metadata_file(footer)
    # Replace the new-only footer with the combined footer. All column and page-index offsets
    # already refer to their final positions; neither the old nor new data needs to be moved.
    with open(destination, "r+b") as output:
        output.seek(-8, os.SEEK_END)
        footer_size = int.from_bytes(output.read(4), "little")
        output.seek(-footer_size - 8, os.SEEK_END)
        output.write(footer.getvalue().slice(4))  # Skip the metadata-only file's PAR1 header.
        output.truncate()


class ParquetDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        path_or_paths: NestedDataStructureLike[PathLike],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        streaming: bool = False,
        num_proc: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(
            path_or_paths,
            split=split,
            features=features,
            cache_dir=cache_dir,
            keep_in_memory=keep_in_memory,
            streaming=streaming,
            num_proc=num_proc,
            **kwargs,
        )
        path_or_paths = path_or_paths if isinstance(path_or_paths, dict) else {self.split: path_or_paths}
        hash = _PACKAGED_DATASETS_MODULES["parquet"][1]
        self.builder = Parquet(
            cache_dir=cache_dir,
            data_files=path_or_paths,
            features=features,
            hash=hash,
            **kwargs,
        )

    def read(self):
        # Build iterable dataset
        if self.streaming:
            dataset = self.builder.as_streaming_dataset(split=self.split)
        # Build regular (map-style) dataset
        else:
            download_config = None
            download_mode = None
            verification_mode = None
            base_path = None

            self.builder.download_and_prepare(
                download_config=download_config,
                download_mode=download_mode,
                verification_mode=verification_mode,
                base_path=base_path,
                num_proc=self.num_proc,
            )
            dataset = self.builder.as_dataset(split=self.split, in_memory=self.keep_in_memory)
        return dataset


class ParquetDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        storage_options: Optional[dict] = None,
        use_content_defined_chunking: Union[bool, dict] = True,
        write_page_index: bool = True,
        **parquet_writer_kwargs,
    ):
        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.batch_size = (
            batch_size
            or get_writer_batch_size_from_features(dataset.features)
            or get_writer_batch_size_from_data_size(len(dataset), dataset._estimate_nbytes())
        )
        self.storage_options = storage_options or {}
        self.parquet_writer_kwargs = parquet_writer_kwargs
        if use_content_defined_chunking is True:
            use_content_defined_chunking = config.DEFAULT_CDC_OPTIONS
        self.use_content_defined_chunking = use_content_defined_chunking
        self.write_page_index = write_page_index

    def write(self) -> int:
        if isinstance(self.path_or_buf, (str, bytes, os.PathLike)):
            with fsspec.open(self.path_or_buf, "wb", **(self.storage_options or {})) as buffer:
                written = self._write(
                    file_obj=buffer,
                    batch_size=self.batch_size,
                    **self.parquet_writer_kwargs,
                )
        else:
            written = self._write(
                file_obj=self.path_or_buf,
                batch_size=self.batch_size,
                **self.parquet_writer_kwargs,
            )
        return written

    def _write(self, file_obj: BinaryIO, batch_size: int, **parquet_writer_kwargs) -> int:
        """Writes the pyarrow table as Parquet to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0
        _ = parquet_writer_kwargs.pop("path_or_buf", None)
        schema = self.dataset.features.arrow_schema

        writer = pq.ParquetWriter(
            file_obj,
            schema=schema,
            use_content_defined_chunking=self.use_content_defined_chunking,
            write_page_index=self.write_page_index,
            compression={
                col: "none" if require_storage_embed(feature) else "snappy"
                for col, feature in self.dataset.features.items()
            },
            use_dictionary=[
                col for col, feature in self.dataset.features.items() if not require_storage_embed(feature)
            ],
            column_encoding={
                col: "PLAIN" for col, feature in self.dataset.features.items() if require_storage_embed(feature)
            },
            **parquet_writer_kwargs,
        )

        for offset in hf_tqdm(
            range(0, len(self.dataset), batch_size),
            unit="ba",
            desc="Creating parquet from Arrow format",
        ):
            batch = query_table(
                table=self.dataset._data,
                key=slice(offset, offset + batch_size),
                indices=self.dataset._indices,
            )
            writer.write_table(batch)
            written += batch.nbytes

        # TODO(kszucs): we may want to persist multiple parameters
        if self.use_content_defined_chunking is not False:
            writer.add_key_value_metadata({"content_defined_chunking": json.dumps(self.use_content_defined_chunking)})

        writer.close()
        return written
