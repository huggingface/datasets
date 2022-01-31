# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""To write records into Parquet files."""
import errno
import json
import os
import sys
from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pyarrow as pa

from datasets.features.features import FeatureType, Value

from . import config, utils
from .features import (
    Features,
    Image,
    _ArrayXDExtensionType,
    cast_to_python_objects,
    generate_from_arrow_type,
    get_nested_type,
    list_of_np_array_to_pyarrow_listarray,
    numpy_to_pyarrow_listarray,
)
from .info import DatasetInfo
from .keyhash import DuplicatedKeysError, KeyHasher
from .table import array_cast, cast_array_to_feature, table_cast
from .utils import logging
from .utils.file_utils import hash_url_to_filename
from .utils.py_utils import first_non_null_value


logger = logging.get_logger(__name__)

type_ = type  # keep python's type function


class TypedSequence:
    """
    This data container generalizes the typing when instantiating pyarrow arrays, tables or batches.

    More specifically it adds several features:
    - Support extension types like ``datasets.features.Array2DExtensionType``:
        By default pyarrow arrays don't return extension arrays. One has to call
        ``pa.ExtensionArray.from_storage(type, pa.array(data, type.storage_type))``
        in order to get an extension array.
    - Support for ``try_type`` parameter that can be used instead of ``type``:
        When an array is transformed, we like to keep the same type as before if possible.
        For example when calling :func:`datasets.Dataset.map`, we don't want to change the type
        of each column by default.
    - Better error message when a pyarrow array overflows.

    Example::

        from datasets.features import Array2D, Array2DExtensionType, Value
        from datasets.arrow_writer import TypedSequence
        import pyarrow as pa

        arr = pa.array(TypedSequence([1, 2, 3], type=Value("int32")))
        assert arr.type == pa.int32()

        arr = pa.array(TypedSequence([1, 2, 3], try_type=Value("int32")))
        assert arr.type == pa.int32()

        arr = pa.array(TypedSequence(["foo", "bar"], try_type=Value("int32")))
        assert arr.type == pa.string()

        arr = pa.array(TypedSequence([[[1, 2, 3]]], type=Array2D((1, 3), "int64")))
        assert arr.type == Array2DExtensionType((1, 3), "int64")

        table = pa.Table.from_pydict({
            "image": TypedSequence([[[1, 2, 3]]], type=Array2D((1, 3), "int64"))
        })
        assert table["image"].type == Array2DExtensionType((1, 3), "int64")

    """

    def __init__(
        self,
        data: Iterable,
        type: Optional[FeatureType] = None,
        try_type: Optional[FeatureType] = None,
        optimized_int_type: Optional[FeatureType] = None,
    ):
        # assert type is None or try_type is None,
        if type is not None and try_type is not None:
            raise ValueError("You cannot specify both type and try_type")
        # set attributes
        self.data = data
        self.type = type
        self.try_type = try_type  # is ignored if it doesn't match the data
        self.optimized_int_type = optimized_int_type
        # when trying a type (is ignored if data is not compatible)
        self.trying_type = self.try_type is not None
        self.trying_int_optimization = optimized_int_type is not None and type is None and try_type is None
        # used to get back the inferred type after __arrow_array__() is called once
        self._inferred_type = None

    def get_inferred_type(self) -> FeatureType:
        """Return the inferred feature type.
        This is done by converting the sequence to an Arrow array, and getting the corresponding
        feature type.

        Since building the Arrow array can be expensive, the value of the inferred type is cached
        as soon as pa.array is called on the typed sequence.

        Returns:
            FeatureType: inferred feature type of the sequence.
        """
        if self._inferred_type is None:
            self._inferred_type = generate_from_arrow_type(pa.array(self).type)
        return self._inferred_type

    @staticmethod
    def _infer_custom_type_and_encode(data: Iterable) -> Tuple[Iterable, Optional[FeatureType]]:
        """Implement type inference for custom objects like PIL.Image.Image -> Image type.

        This function is only used for custom python objects that can't be direclty passed to build
        an Arrow array. In such cases is infers the feature type to use, and it encodes the data so
        that they can be passed to an Arrow array.

        Args:
            data (Iterable): array of data to infer the type, e.g. a list of PIL images.

        Returns:
            Tuple[Iterable, Optional[FeatureType]]: a tuple with:
                - the (possibly encoded) array, if the inferred feature type requires encoding
                - the inferred feature type if the array is made of supported custom objects like
                    PIL images, else None.
        """
        if config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            non_null_idx, non_null_value = first_non_null_value(data)
            if isinstance(non_null_value, PIL.Image.Image):
                return [Image().encode_example(value) for value in data], Image()
        return data, None

    def __arrow_array__(self, type: Optional[pa.DataType] = None):
        """This function is called when calling pa.array(typed_sequence)"""

        if type is not None:
            raise ValueError("TypedSequence is supposed to be used with pa.array(typed_sequence, type=None)")
        del type  # make sure we don't use it
        data = self.data
        # automatic type inference for custom objects
        if self.type is None and self.try_type is None:
            data, self._inferred_type = self._infer_custom_type_and_encode(data)
        if self._inferred_type is None:
            type = self.try_type if self.trying_type else self.type
        else:
            type = self._inferred_type
        pa_type = get_nested_type(type) if type is not None else None
        optimized_int_pa_type = (
            get_nested_type(self.optimized_int_type) if self.optimized_int_type is not None else None
        )
        try:
            # custom pyarrow types
            if isinstance(pa_type, _ArrayXDExtensionType):
                if isinstance(data, np.ndarray):
                    storage = numpy_to_pyarrow_listarray(data, type=pa_type.value_type)
                elif isinstance(data, list) and data and isinstance(first_non_null_value(data)[1], np.ndarray):
                    storage = list_of_np_array_to_pyarrow_listarray(data, type=pa_type.value_type)
                else:
                    storage = pa.array(data, pa_type.storage_dtype)
                return pa.ExtensionArray.from_storage(pa_type, storage)

            # efficient np array to pyarrow array
            if isinstance(data, np.ndarray):
                out = numpy_to_pyarrow_listarray(data)
            elif isinstance(data, list) and data and isinstance(first_non_null_value(data)[1], np.ndarray):
                out = list_of_np_array_to_pyarrow_listarray(data)
            else:
                out = pa.array(cast_to_python_objects(data, only_1d_for_numpy=True))

            # use smaller integer precisions if possible
            if self.trying_int_optimization:
                if pa.types.is_int64(out.type):
                    out = out.cast(optimized_int_pa_type)
                elif pa.types.is_list(out.type):
                    if pa.types.is_int64(out.type.value_type):
                        out = array_cast(out, pa.list_(optimized_int_pa_type))
                    elif pa.types.is_list(out.type.value_type) and pa.types.is_int64(out.type.value_type.value_type):
                        out = array_cast(out, pa.list_(pa.list_(optimized_int_pa_type)))
            # otherwise we can finally use the user's type
            elif type is not None:
                # We use array_cast_to_feature to support casting to custom types like Audio and Image
                # Also, when trying type "string", we don't want to convert integers or floats to "string".
                # We only do it if trying_type is False - since this is what the user asks for.
                out = cast_array_to_feature(out, type, allow_number_to_str=not self.trying_type)
            return out
        except (TypeError, pa.lib.ArrowInvalid) as e:  # handle type errors and overflows
            if self.trying_type:
                try:  # second chance
                    if isinstance(data, np.ndarray):
                        return numpy_to_pyarrow_listarray(data)
                    elif isinstance(data, list) and data and any(isinstance(value, np.ndarray) for value in data):
                        return list_of_np_array_to_pyarrow_listarray(data)
                    else:
                        return pa.array(cast_to_python_objects(data, only_1d_for_numpy=True))
                except pa.lib.ArrowInvalid as e:
                    if "overflow" in str(e):
                        raise OverflowError(
                            f"There was an overflow with type {type_(data)}. Try to reduce writer_batch_size to have batches smaller than 2GB.\n({e})"
                        ) from None
                    elif self.trying_int_optimization and "not in range" in str(e):
                        optimized_int_pa_type_str = np.dtype(optimized_int_pa_type.to_pandas_dtype()).name
                        logger.info(
                            f"Failed to cast a sequence to {optimized_int_pa_type_str}. Falling back to int64."
                        )
                        return out
                    else:
                        raise
            elif "overflow" in str(e):
                raise OverflowError(
                    f"There was an overflow with type {type_(data)}. Try to reduce writer_batch_size to have batches smaller than 2GB.\n({e})"
                ) from None
            elif self.trying_int_optimization and "not in range" in str(e):
                optimized_int_pa_type_str = np.dtype(optimized_int_pa_type.to_pandas_dtype()).name
                logger.info(f"Failed to cast a sequence to {optimized_int_pa_type_str}. Falling back to int64.")
                return out
            else:
                raise


class OptimizedTypedSequence(TypedSequence):
    def __init__(
        self,
        data,
        type: Optional[FeatureType] = None,
        try_type: Optional[FeatureType] = None,
        col: Optional[str] = None,
        optimized_int_type: Optional[FeatureType] = None,
    ):
        optimized_int_type_by_col = {
            "attention_mask": Value("int8"),  # binary tensor
            "special_tokens_mask": Value("int8"),
            "input_ids": Value("int32"),  # typical vocab size: 0-50k (max ~500k, never > 1M)
            "token_type_ids": Value(
                "int8"
            ),  # binary mask; some (XLNetModel) use an additional token represented by a 2
        }
        if type is None and try_type is None:
            optimized_int_type = optimized_int_type_by_col.get(col, None)
        super().__init__(data, type=type, try_type=try_type, optimized_int_type=optimized_int_type)


class ArrowWriter:
    """Shuffles and writes Examples to Arrow files."""

    def __init__(
        self,
        schema: Optional[pa.Schema] = None,
        features: Optional[Features] = None,
        path: Optional[str] = None,
        stream: Optional[pa.NativeFile] = None,
        fingerprint: Optional[str] = None,
        writer_batch_size: Optional[int] = None,
        hash_salt: Optional[str] = None,
        check_duplicates: Optional[bool] = False,
        disable_nullable: bool = False,
        update_features: bool = False,
        with_metadata: bool = True,
        unit: str = "examples",
    ):
        if path is None and stream is None:
            raise ValueError("At least one of path and stream must be provided.")
        if features is not None:
            self._features = features
            self._schema = None
        elif schema is not None:
            self._schema: pa.Schema = schema
            self._features = Features.from_arrow_schema(self._schema)
        else:
            self._features = None
            self._schema = None

        if hash_salt is not None:
            # Create KeyHasher instance using split name as hash salt
            self._hasher = KeyHasher(hash_salt)
        else:
            self._hasher = KeyHasher("")

        self._check_duplicates = check_duplicates
        self._disable_nullable = disable_nullable

        self._path = path
        if stream is None:
            self.stream = pa.OSFile(self._path, "wb")
            self._closable_stream = True
        else:
            self.stream = stream
            self._closable_stream = False

        self.fingerprint = fingerprint
        self.disable_nullable = disable_nullable
        self.writer_batch_size = writer_batch_size or config.DEFAULT_MAX_BATCH_SIZE
        self.update_features = update_features
        self.with_metadata = with_metadata
        self.unit = unit

        self._num_examples = 0
        self._num_bytes = 0
        self.current_examples: List[Tuple[Dict[str, Any], str]] = []
        self.current_rows: List[pa.Table] = []
        self.pa_writer: Optional[pa.RecordBatchStreamWriter] = None
        self.hkey_record = []

    def __len__(self):
        """Return the number of writed and staged examples"""
        return self._num_examples + len(self.current_examples) + len(self.current_rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        # Try closing if opened; if closed: pyarrow.lib.ArrowInvalid: Invalid operation on closed file
        if self.pa_writer:  # it might be None
            try:
                self.pa_writer.close()
            except Exception:  # pyarrow.lib.ArrowInvalid, OSError
                pass
        if self._closable_stream and not self.stream.closed:
            self.stream.close()  # This also closes self.pa_writer if it is opened

    def _build_writer(self, inferred_schema: pa.Schema):
        schema = self.schema
        inferred_features = Features.from_arrow_schema(inferred_schema)
        if self._features is not None:
            if self.update_features:  # keep original features it they match, or update them
                fields = {field.name: field for field in self._features.type}
                for inferred_field in inferred_features.type:
                    name = inferred_field.name
                    if name in fields:
                        if inferred_field == fields[name]:
                            inferred_features[name] = self._features[name]
                self._features = inferred_features
                schema: pa.Schema = inferred_schema
        else:
            self._features = inferred_features
            schema: pa.Schema = inferred_schema
        if self.disable_nullable:
            schema = pa.schema(pa.field(field.name, field.type, nullable=False) for field in schema)
        if self.with_metadata:
            schema = schema.with_metadata(self._build_metadata(DatasetInfo(features=self._features), self.fingerprint))
        self._schema = schema
        self.pa_writer = pa.RecordBatchStreamWriter(self.stream, schema)

    @property
    def schema(self):
        _schema = (
            self._schema
            if self._schema is not None
            else (pa.schema(self._features.type) if self._features is not None else None)
        )
        if self._disable_nullable and _schema is not None:
            _schema = pa.schema(pa.field(field.name, field.type, nullable=False) for field in _schema)
        return _schema if _schema is not None else []

    @staticmethod
    def _build_metadata(info: DatasetInfo, fingerprint: Optional[str] = None) -> Dict[str, str]:
        info_keys = ["features"]  # we can add support for more DatasetInfo keys in the future
        info_as_dict = asdict(info)
        metadata = {}
        metadata["info"] = {key: info_as_dict[key] for key in info_keys}
        if fingerprint is not None:
            metadata["fingerprint"] = fingerprint
        return {"huggingface": json.dumps(metadata)}

    def write_examples_on_file(self):
        """Write stored examples from the write-pool of examples. It makes a table out of the examples and write it."""
        if not self.current_examples:
            return

        # order the columns properly
        cols = (
            [col for col in self.schema.names if col in self.current_examples[0][0]]
            + [col for col in self.current_examples[0][0].keys() if col not in self.schema.names]
            if self.schema
            else self.current_examples[0][0].keys()
        )
        batch_examples = {}
        for col in cols:
            # Since current_examples contains (example, key) tuples
            batch_examples[col] = [row[0][col] for row in self.current_examples]
        self.write_batch(batch_examples=batch_examples)
        self.current_examples = []

    def write_rows_on_file(self):
        """Write stored rows from the write-pool of rows. It concatenates the single-row tables and it writes the resulting table."""
        if not self.current_rows:
            return
        table = pa.concat_tables(self.current_rows).combine_chunks()
        self.write_table(table)
        self.current_rows = []

    def write(
        self,
        example: Dict[str, Any],
        key: Optional[Union[str, int, bytes]] = None,
        writer_batch_size: Optional[int] = None,
    ):
        """Add a given (Example,Key) pair to the write-pool of examples which is written to file.

        Args:
            example: the Example to add.
            key: Optional, a unique identifier(str, int or bytes) associated with each example
        """
        # Utilize the keys and duplicate checking when `self._check_duplicates` is passed True
        if self._check_duplicates:
            # Create unique hash from key and store as (key, example) pairs
            hash = self._hasher.hash(key)
            self.current_examples.append((example, hash))
            # Maintain record of keys and their respective hashes for checking duplicates
            self.hkey_record.append((hash, key))
        else:
            # Store example as a tuple so as to keep the structure of `self.current_examples` uniform
            self.current_examples.append((example, ""))

        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if writer_batch_size is not None and len(self.current_examples) >= writer_batch_size:
            if self._check_duplicates:
                self.check_duplicate_keys()
                # Re-intializing to empty list for next batch
                self.hkey_record = []

            self.write_examples_on_file()

    def check_duplicate_keys(self):
        """Raises error if duplicates found in a batch"""
        tmp_record = set()
        for hash, key in self.hkey_record:
            if hash in tmp_record:
                raise DuplicatedKeysError(key)
            else:
                tmp_record.add(hash)

    def write_row(self, row: pa.Table, writer_batch_size: Optional[int] = None):
        """Add a given single-row Table to the write-pool of rows which is written to file.

        Args:
            row: the row to add.
        """
        self.current_rows.append(row)
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if writer_batch_size is not None and len(self.current_rows) >= writer_batch_size:
            self.write_rows_on_file()

    def write_batch(
        self,
        batch_examples: Dict[str, List[Any]],
        writer_batch_size: Optional[int] = None,
    ):
        """Write a batch of Example to file.
        Ignores the batch if it appears to be empty,
        preventing a potential schema update of unknown types.

        Args:
            batch_examples: the batch of examples to add.
        """
        if batch_examples and len(next(iter(batch_examples.values()))) == 0:
            return
        features = None if self.pa_writer is None and self.update_features else self._features
        try_features = self._features if self.pa_writer is None and self.update_features else None
        arrays = []
        inferred_features = Features()
        cols = (
            [col for col in self.schema.names if col in batch_examples]
            + [col for col in batch_examples.keys() if col not in self.schema.names]
            if self.schema
            else batch_examples.keys()
        )
        for col in cols:
            col_type = features[col] if features else None
            col_try_type = try_features[col] if try_features is not None and col in try_features else None
            typed_sequence = OptimizedTypedSequence(batch_examples[col], type=col_type, try_type=col_try_type, col=col)
            arrays.append(pa.array(typed_sequence))
            inferred_features[col] = typed_sequence.get_inferred_type()
        schema = inferred_features.arrow_schema if self.pa_writer is None else self.schema
        pa_table = pa.Table.from_arrays(arrays, schema=schema)
        self.write_table(pa_table, writer_batch_size)

    def write_table(self, pa_table: pa.Table, writer_batch_size: Optional[int] = None):
        """Write a Table to file.

        Args:
            example: the Table to add.
        """
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if self.pa_writer is None:
            self._build_writer(inferred_schema=pa_table.schema)
        pa_table = table_cast(pa_table, self._schema)
        batches: List[pa.RecordBatch] = pa_table.to_batches(max_chunksize=writer_batch_size)
        self._num_bytes += sum(batch.nbytes for batch in batches)
        self._num_examples += pa_table.num_rows
        for batch in batches:
            self.pa_writer.write_batch(batch)

    def finalize(self, close_stream=True):
        self.write_rows_on_file()
        # In case current_examples < writer_batch_size, but user uses finalize()
        if self._check_duplicates:
            self.check_duplicate_keys()
            # Re-intializing to empty list for next batch
            self.hkey_record = []
        self.write_examples_on_file()
        if self.pa_writer is None:
            if self.schema:
                self._build_writer(self.schema)
            else:
                raise ValueError("Please pass `features` or at least one example when writing data")
        self.pa_writer.close()
        if close_stream:
            self.stream.close()
        logger.debug(
            f"Done writing {self._num_examples} {self.unit} in {self._num_bytes} bytes {self._path if self._path else ''}."
        )
        return self._num_examples, self._num_bytes


class BeamWriter:
    """
    Shuffles and writes Examples to Arrow files.
    The Arrow files are converted from Parquet files that are the output of Apache Beam pipelines.
    """

    def __init__(
        self,
        features: Optional[Features] = None,
        schema: Optional[pa.Schema] = None,
        path: Optional[str] = None,
        namespace: Optional[str] = None,
        cache_dir: Optional[str] = None,
    ):
        if features is None and schema is None:
            raise ValueError("At least one of features and schema must be provided.")
        if path is None:
            raise ValueError("Path must be provided.")

        if features is not None:
            self._features: Features = features
            self._schema: pa.Schema = features.arrow_schema
        else:
            self._schema: pa.Schema = schema
            self._features: Features = Features.from_arrow_schema(schema)

        self._path = path
        self._parquet_path = os.path.splitext(path)[0]  # remove extension
        self._namespace = namespace or "default"
        self._num_examples = None
        self._cache_dir = cache_dir or config.HF_DATASETS_CACHE

    def write_from_pcollection(self, pcoll_examples):
        """Add the final steps of the beam pipeline: write to parquet files."""
        import apache_beam as beam

        def inc_num_examples(example):
            beam.metrics.Metrics.counter(self._namespace, "num_examples").inc()

        # count examples
        _ = pcoll_examples | "Count N. Examples" >> beam.Map(inc_num_examples)

        # save dataset
        simplified_schema = pa.schema({field.name: pa.string() for field in self._schema})
        return (
            pcoll_examples
            | "Get values" >> beam.Values()
            | "simplify" >> beam.Map(lambda ex: {k: json.dumps(v) for k, v in ex.items()})
            | "Save to parquet"
            >> beam.io.parquetio.WriteToParquet(
                self._parquet_path, simplified_schema, shard_name_template="-SSSSS-of-NNNNN.parquet"
            )
        )

    def finalize(self, metrics_query_result: dict):
        """
        Run after the pipeline has finished.
        It converts the resulting parquet files to arrow and it completes the info from the pipeline metrics.

        Args:
            metrics_query_result: `dict` obtained from pipeline_results.metrics().query(m_filter). Make sure
                that the filter keeps only the metrics for the considered split, under the namespace `split_name`.
        """
        import apache_beam as beam

        from .utils import beam_utils

        # Convert to arrow
        logger.info(f"Converting parquet file {self._parquet_path} to arrow {self._path}")
        shards = [
            metadata.path
            for metadata in beam.io.filesystems.FileSystems.match([self._parquet_path + "*.parquet"])[0].metadata_list
        ]
        try:  # stream conversion
            sources = [beam.io.filesystems.FileSystems.open(shard) for shard in shards]
            with beam.io.filesystems.FileSystems.create(self._path) as dest:
                parquet_to_arrow(sources, dest)
        except OSError as e:  # broken pipe can happen if the connection is unstable, do local conversion instead
            if e.errno != errno.EPIPE:  # not a broken pipe
                raise
            logger.warning("Broken Pipe during stream conversion from parquet to arrow. Using local convert instead")
            local_convert_dir = os.path.join(self._cache_dir, "beam_convert")
            os.makedirs(local_convert_dir, exist_ok=True)
            local_arrow_path = os.path.join(local_convert_dir, hash_url_to_filename(self._parquet_path) + ".arrow")
            local_shards = []
            for shard in shards:
                local_parquet_path = os.path.join(local_convert_dir, hash_url_to_filename(shard) + ".parquet")
                local_shards.append(local_parquet_path)
                beam_utils.download_remote_to_local(shard, local_parquet_path)
            parquet_to_arrow(local_shards, local_arrow_path)
            beam_utils.upload_local_to_remote(local_arrow_path, self._path)

        # Save metrics
        counters_dict = {metric.key.metric.name: metric.result for metric in metrics_query_result["counters"]}
        self._num_examples = counters_dict["num_examples"]
        output_file_metadata = beam.io.filesystems.FileSystems.match([self._path], limits=[1])[0].metadata_list[0]
        self._num_bytes = output_file_metadata.size_in_bytes
        return self._num_examples, self._num_bytes


def parquet_to_arrow(sources, destination):
    """Convert parquet files to arrow file. Inputs can be str paths or file-like objects"""
    stream = None if isinstance(destination, str) else destination
    disable = bool(logging.get_verbosity() == logging.NOTSET)
    with ArrowWriter(path=destination, stream=stream) as writer:
        for source in utils.tqdm(sources, unit="sources", disable=disable):
            pf = pa.parquet.ParquetFile(source)
            for i in utils.tqdm(range(pf.num_row_groups), unit="row_groups", leave=False, disable=disable):
                df = pf.read_row_group(i).to_pandas()
                for col in df.columns:
                    df[col] = df[col].apply(json.loads)
                reconstructed_table = pa.Table.from_pandas(df)
                writer.write_table(reconstructed_table)
    return destination
