import json
import os
from typing import BinaryIO, Optional, Union

import fsspec
import pyarrow.parquet as pq

from .. import Dataset, Features, NamedSplit, config
from ..arrow_writer import get_writer_batch_size_from_data_size, get_writer_batch_size_from_features
from ..formatting import query_table
from ..packaged_modules import _PACKAGED_DATASETS_MODULES
from ..packaged_modules.parquet.parquet import Parquet
from ..utils import tqdm as hf_tqdm
from ..utils.typing import NestedDataStructureLike, PathLike
from .abc import AbstractDatasetReader


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
            dataset = self.builder.as_dataset(
                split=self.split, verification_mode=verification_mode, in_memory=self.keep_in_memory
            )
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
