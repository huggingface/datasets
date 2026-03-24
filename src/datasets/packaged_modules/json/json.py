import io
import os
from dataclasses import dataclass
from typing import Literal, Optional

import pandas as pd
import pyarrow as pa
import pyarrow.json as paj

import datasets
import datasets.config
from datasets.builder import Key
from datasets.table import table_cast
from datasets.utils.file_utils import readline
from datasets.utils.json import (
    find_mixed_struct_types_field_paths,
    get_json_field_path_from_pyarrow_json_error,
    get_json_field_paths_from_feature,
    insert_json_field_path,
    json_encode_field,
    json_encode_fields_in_json_lines,
    set_json_types_in_feature,
    ujson_dumps,
    ujson_loads,
)


logger = datasets.utils.logging.get_logger(__name__)


def pandas_read_json(path_or_buf, **kwargs):
    if datasets.config.PANDAS_VERSION.major >= 2:
        kwargs["dtype_backend"] = "pyarrow"
    return pd.read_json(path_or_buf, **kwargs)


class FullReadDisallowed(Exception):
    pass


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
    on_mixed_types: Optional[Literal["use_json"]] = "use_json"

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
        if self.info.features is None:
            try:
                pa_table = next(iter(self._generate_tables(**splits[0].gen_kwargs, allow_full_read=False)))[1]
                self.info.features = datasets.Features.from_arrow_schema(pa_table.schema)
            except FullReadDisallowed:
                pass
        return splits

    def _cast_table(self, pa_table: pa.Table, json_field_paths=()) -> pa.Table:
        if self.info.features is not None:
            # adding missing columns
            for column_name in set(self.info.features) - set(pa_table.column_names):
                type = self.info.features.arrow_schema.field(column_name).type
                pa_table = pa_table.append_column(column_name, pa.array([None] * len(pa_table), type=type))
            # convert to string when needed
            for i, column_name in enumerate(pa_table.column_names):
                if pa.types.is_struct(pa_table[column_name].type) and self.info.features.get(
                    column_name, None
                ) == datasets.Value("string"):
                    jsonl = (
                        pa_table[column_name]
                        .to_pandas(types_mapper=pd.ArrowDtype)
                        .to_json(orient="records", lines=True)
                    )
                    string_array = pa.array(
                        (None if x.strip() == "null" else x.strip() for x in jsonl.split("\n") if x.strip()),
                        type=pa.string(),
                    )
                    pa_table = pa_table.set_column(i, column_name, string_array)
            # more expensive cast to support nested structures with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        elif json_field_paths:
            features = datasets.Features.from_arrow_schema(pa_table.schema)
            features = set_json_types_in_feature(features, json_field_paths)
            pa_table = table_cast(pa_table, features.arrow_schema)
        return pa_table

    def _generate_shards(self, base_files, files_iterables):
        yield from base_files

    def _estimate_line_count(self, file, max_bytes=20 << 20):
        """Estimate the number of lines in a JSON Lines file by reading the first max_bytes (default 20MB).
        
        Args:
            file: Path to the file
            max_bytes: Maximum bytes to read (default 20MB)
            
        Returns:
            Estimated line count
        """
        try:
            with open(file, "rb") as f:
                line_count = 0
                bytes_read = 0
                
                while bytes_read < max_bytes:
                    line = f.readline()
                    if not line:
                        break
                    line_count += 1
                    bytes_read += len(line)
                
                # If we hit the byte limit, estimate the total based on file size
                if bytes_read >= max_bytes:
                    try:
                        file_size = os.path.getsize(file)
                        if bytes_read > 0:
                            estimated_line_count = int((file_size / bytes_read) * line_count)
                        else:
                            estimated_line_count = line_count
                    except OSError:
                        estimated_line_count = line_count
                else:
                    estimated_line_count = line_count
                return estimated_line_count
        except Exception:
            return 0

    def _generate_more_gen_kwargs(self, base_files, files_iterables, num_shards=None):
        """Generate more gen_kwargs for resharding.
        
        When num_shards is specified, create that many shards.
        When num_shards is None, maximize sharding by aiming for self.config.chunksize bytes per shard.
        """
        for base_file, files_iterable in zip(base_files, files_iterables):
            files_list = list(files_iterable)
            
            if not files_list:
                continue
            
            # Check if the file is a JSON Lines file (one JSON object per line)
            # For single JSON object files, we can't split them further
            if self.config.field is not None:
                for file in files_list:
                    yield {
                        "base_files": [base_file],
                        "files_iterables": [[(file, 0, None)]],
                    }
                continue
            
            # Estimate total line count from the first file only (assuming similar structure)
            total_line_count = 0
            for file in files_list:
                line_count = self._estimate_line_count(file)
                if line_count > 0:
                    # If we got a good estimate from the first file, use it for all files
                    # This avoids expensive line counting on every file
                    total_line_count = line_count
                    break
            
            # Determine target number of shards
            if num_shards is None:
                # Maximum sharding: aim for self.config.chunksize bytes per shard (10MB by default)
                # We use line count as a proxy: assume average line size and target for chunksize bytes
                target_num_shards = max(1, (total_line_count + (self.config.chunksize // 100) - 1) // (self.config.chunksize // 100))
            else:
                target_num_shards = num_shards if total_line_count == 0 else min(num_shards, total_line_count)
            
            # If only one shard, return the original gen_kwargs
            if target_num_shards <= 1:
                for file in files_list:
                    yield {
                        "base_files": [base_file],
                        "files_iterables": [[(file, 0, None)]],
                    }
                continue
            
            # Calculate lines per shard
            lines_per_shard = (total_line_count + target_num_shards - 1) // target_num_shards
            
            # Generate gen_kwargs for each shard
            for shard_idx in range(target_num_shards):
                shard_start = shard_idx * lines_per_shard
                shard_end = (shard_idx + 1) * lines_per_shard
                
                # Distribute files across shards, keeping shard info with files
                yield {
                    "base_files": [base_file],
                    "files_iterables": [[(file, shard_start, shard_end) for file in files_list]],
                }

    def _generate_tables(
        self, base_files, files_iterables, allow_full_read=True, shard_start_line=0, shard_end_line=None
    ):
        json_field_paths = []

        if self.info.features is not None:
            json_field_paths = get_json_field_paths_from_feature(self.info.features)

        # Handle list parameters (from resharding) - kept for backward compatibility
        if isinstance(shard_start_line, list):
            shard_start_line = shard_start_line[0]
        if isinstance(shard_end_line, list):
            shard_end_line = shard_end_line[0]

        for shard_idx, files_iterable in enumerate(files_iterables):
            for file_item in files_iterable:
                # Handle both tuple format (file, shard_start, shard_end) and plain file format
                if isinstance(file_item, tuple):
                    file, shard_start, shard_end = file_item
                else:
                    file = file_item
                    shard_start = shard_start_line
                    shard_end = shard_end_line
                
                # If the file is one json object and if we need to look at the items in one specific field
                if self.config.field is not None:
                    if not allow_full_read:
                        raise FullReadDisallowed()
                    with open(file, encoding=self.config.encoding, errors=self.config.encoding_errors) as f:
                        dataset = ujson_loads(f.read())
                    # We keep only the field we are interested in
                    dataset = dataset[self.config.field]
                    df = pandas_read_json(io.StringIO(ujson_dumps(dataset)))
                    if df.columns.tolist() == [0]:
                        df.columns = list(self.config.features) if self.config.features else ["text"]
                    pa_table = pa.Table.from_pandas(df, preserve_index=False)
                    yield Key(shard_idx, 0), self._cast_table(pa_table)

                # If the file has one json object per line
                else:
                    with open(file, "rb") as f:
                        batch_idx = 0
                        # Use block_size equal to the chunk size divided by 32 to leverage multithreading
                        # Set a default minimum value of 16kB if the chunk size is really small
                        block_size = max(self.config.chunksize // 32, 16 << 10)
                        encoding_errors = (
                            self.config.encoding_errors if self.config.encoding_errors is not None else "strict"
                        )

                        # Skip lines until shard_start_line
                        current_line = 0
                        if shard_start_line > 0:
                            while current_line < shard_start_line:
                                line = f.readline()
                                if not line:
                                    break
                                current_line += 1

                        while True:
                            batch = f.read(self.config.chunksize)
                            if not batch:
                                break
                            if batch.startswith(b"["):
                                if not allow_full_read:
                                    raise FullReadDisallowed()
                                else:
                                    # convert to JSON Lines
                                    full_data = batch + f.read()
                                    if b"{" in batch[:100].split(b'"', 1)[0]:  # list of objects
                                        batch = "\n".join(ujson_dumps(x) for x in ujson_loads(full_data)).encode()
                                    else:  # list of strings
                                        batch = "\n".join(
                                            ujson_dumps({"text": x}) for x in ujson_loads(full_data)
                                        ).encode()
                            # Finish current line
                            try:
                                batch += f.readline()
                            except (AttributeError, io.UnsupportedOperation):
                                batch += readline(f)

                            # Count lines in batch and respect shard_end_line
                            lines = batch.splitlines()
                            if shard_end_line is not None:
                                remaining_lines = shard_end_line - current_line
                                if remaining_lines <= 0:
                                    break
                                if len(lines) > remaining_lines:
                                    lines = lines[:remaining_lines]
                                    batch = b"\n".join(lines) + b"\n"
                            current_line += len(lines)

                            # PyArrow only accepts utf-8 encoded bytes
                            if self.config.encoding != "utf-8":
                                batch = batch.decode(self.config.encoding, errors=encoding_errors).encode("utf-8")
                            # On first batch we check for lists of objects with arbitrary fields
                            if (
                                shard_idx == 0
                                and batch_idx == 0
                                and self.info.features is None
                                and self.config.on_mixed_types == "use_json"
                            ):
                                examples = [ujson_loads(line) for line in batch.splitlines()]
                                json_field_paths += find_mixed_struct_types_field_paths(examples)
                            # Re-encode JSON fields
                            original_batch = batch
                            if json_field_paths:
                                examples = [ujson_loads(line) for line in batch.splitlines()]
                                for json_field_path in json_field_paths:
                                    examples = [json_encode_field(examples, json_field_path) for examples in examples]
                                batch = "\n".join(ujson_dumps(example) for example in examples).encode()
                            # Disable parallelism if block size is ~ len(batch) to avoid segfault
                            block_size = len(batch) if len(batch) // 8 > block_size else block_size
                            try:
                                while True:
                                    try:
                                        pa_table = paj.read_json(
                                            io.BytesIO(batch), read_options=paj.ReadOptions(block_size=block_size)
                                        )
                                        break
                                    except (pa.ArrowInvalid, pa.ArrowNotImplementedError) as e:
                                        if batch.startswith(b"["):  # paj.read_json only supports json lines
                                            raise
                                        elif self.config.on_mixed_types == "use_json" and (
                                            isinstance(e, pa.ArrowInvalid)
                                            and "JSON parse error: Column(" in str(e)
                                            and ") changed from" in str(e)
                                        ):
                                            json_field_path = get_json_field_path_from_pyarrow_json_error(str(e))
                                            insert_json_field_path(json_field_paths, json_field_path)
                                            batch = json_encode_fields_in_json_lines(original_batch, json_field_paths)
                                        elif (
                                            "straddling" in str(e) or "JSON conversion to" in str(e)
                                        ) and block_size < len(batch):
                                            # Increase the block size in case it was too small.
                                            # The block size will be reset for the next file.
                                            # this is needed in case of "stradding" or for some JSON conversions (see https://github.com/huggingface/datasets/issues/2799)
                                            logger.debug(
                                                f"Batch of {len(batch)} bytes couldn't be parsed with block_size={block_size}. Retrying with block_size={block_size * 2}."
                                            )
                                            block_size *= 2
                                        else:
                                            raise
                            except pa.ArrowInvalid as e:
                                if not allow_full_read:
                                    raise FullReadDisallowed()
                                try:
                                    with open(
                                        file, encoding=self.config.encoding, errors=self.config.encoding_errors
                                    ) as f:
                                        # Skip lines until shard_start_line
                                        if shard_start_line > 0:
                                            for _ in range(shard_start_line):
                                                f.readline()
                                        # Read until shard_end_line
                                        lines = []
                                        current_line = shard_start_line
                                        while True:
                                            line = f.readline()
                                            if not line:
                                                break
                                            if shard_end_line is not None and current_line >= shard_end_line:
                                                break
                                            lines.append(line)
                                            current_line += 1
                                        df = pandas_read_json(io.StringIO("".join(lines)))
                                except ValueError:
                                    logger.error(f"Failed to load JSON from file '{file}' with error {type(e)}: {e}")
                                    raise e
                                if df.columns.tolist() == [0]:
                                    df.columns = list(self.config.features) if self.config.features else ["text"]
                                try:
                                    pa_table = pa.Table.from_pandas(df, preserve_index=False)
                                except pa.ArrowInvalid as e:
                                    logger.error(
                                        f"Failed to convert pandas DataFrame to Arrow Table from file '{file}' with error {type(e)}: {e}"
                                    )
                                    raise ValueError(
                                        f"Failed to convert pandas DataFrame to Arrow Table from file {file}."
                                    ) from None
                                yield Key(shard_idx, 0), self._cast_table(pa_table)
                                break
                            yield (
                                Key(shard_idx, batch_idx),
                                self._cast_table(pa_table, json_field_paths=json_field_paths),
                            )
                            batch_idx += 1

                            # Stop if we've reached shard_end_line
                            if shard_end_line is not None and current_line >= shard_end_line:
                                break
