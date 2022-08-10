import os
from typing import BinaryIO, Optional, Union

import pyarrow as pa
import pyarrow.parquet as pq

from .. import Dataset, Features, NamedSplit, config
from ..formatting import query_table
from ..packaged_modules import _PACKAGED_DATASETS_MODULES
from ..packaged_modules.parquet.parquet import Parquet
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
        **kwargs,
    ):
        super().__init__(
            path_or_paths, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
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
        download_config = None
        download_mode = None
        ignore_verifications = False
        use_auth_token = None
        base_path = None

        self.builder.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            ignore_verifications=ignore_verifications,
            # try_from_hf_gcs=try_from_hf_gcs,
            base_path=base_path,
            use_auth_token=use_auth_token,
        )

        # Build dataset for splits
        dataset = self.builder.as_dataset(
            split=self.split, ignore_verifications=ignore_verifications, in_memory=self.keep_in_memory
        )
        return dataset


class ParquetDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        **parquet_writer_kwargs,
    ):
        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.batch_size = batch_size
        self.parquet_writer_kwargs = parquet_writer_kwargs

    def write(self) -> int:
        batch_size = self.batch_size if self.batch_size else config.DEFAULT_MAX_BATCH_SIZE

        if isinstance(self.path_or_buf, (str, bytes, os.PathLike)):
            with open(self.path_or_buf, "wb+") as buffer:
                written = self._write(file_obj=buffer, batch_size=batch_size, **self.parquet_writer_kwargs)
        else:
            written = self._write(file_obj=self.path_or_buf, batch_size=batch_size, **self.parquet_writer_kwargs)
        return written

    def _write(self, file_obj: BinaryIO, batch_size: int, **parquet_writer_kwargs) -> int:
        """Writes the pyarrow table as Parquet to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0
        _ = parquet_writer_kwargs.pop("path_or_buf", None)
        schema = pa.schema(self.dataset.features.type)
        writer = pq.ParquetWriter(file_obj, schema=schema, **parquet_writer_kwargs)

        for offset in range(0, len(self.dataset), batch_size):
            batch = query_table(
                table=self.dataset._data,
                key=slice(offset, offset + batch_size),
                indices=self.dataset._indices if self.dataset._indices is not None else None,
            )
            writer.write_table(batch)
            written += batch.nbytes
        writer.close()
        return written
