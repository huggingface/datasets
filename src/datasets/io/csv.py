import multiprocessing
import os
from contextlib import ExitStack
from typing import BinaryIO, Optional, Union

import fsspec
from pandas.io.common import get_compression_method, get_handle, infer_compression

from .. import Dataset, Features, NamedSplit, config
from ..formatting import query_table
from ..packaged_modules.csv.csv import Csv
from ..utils import tqdm as hf_tqdm
from ..utils.typing import NestedDataStructureLike, PathLike
from .abc import AbstractDatasetReader


class CsvDatasetReader(AbstractDatasetReader):
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
        self.builder = Csv(
            cache_dir=cache_dir,
            data_files=path_or_paths,
            features=features,
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


class CsvDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        num_proc: Optional[int] = None,
        storage_options: Optional[dict] = None,
        **to_csv_kwargs,
    ):
        if num_proc is not None and num_proc <= 0:
            raise ValueError(f"num_proc {num_proc} must be an integer > 0.")

        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
        self.num_proc = num_proc
        self.encoding = "utf-8"
        self.storage_options = storage_options or {}
        self.to_csv_kwargs = to_csv_kwargs

    def write(self) -> int:
        _ = self.to_csv_kwargs.pop("path_or_buf", None)
        header = self.to_csv_kwargs.pop("header", True)
        index = self.to_csv_kwargs.pop("index", False)

        is_path = isinstance(self.path_or_buf, (str, bytes, os.PathLike))
        compression = self.to_csv_kwargs.pop("compression", "infer")
        if is_path and "compression" in self.storage_options:
            if compression not in [None, "infer"]:
                raise ValueError("Specify compression either as a keyword argument or in storage_options, not both.")
            # fsspec already owns this compression stream; do not infer a second layer.
            compression = None
        compression, compression_options = get_compression_method(compression)
        compression = infer_compression(self.path_or_buf, compression)
        compression_options = {"method": compression, **compression_options}
        if compression == "tar" and is_path:
            # Keep filename-based tar compression and archive naming with an fsspec handle.
            compression_options.setdefault("name", os.fsdecode(self.path_or_buf))

        with ExitStack() as stack:
            buffer = (
                stack.enter_context(fsspec.open(self.path_or_buf, "wb", **(self.storage_options or {})))
                if is_path
                else self.path_or_buf
            )
            # All batches share one compression stream, including when they are generated in parallel.
            handles = stack.enter_context(get_handle(buffer, "wb", compression=compression_options, is_text=False))
            written = self._write(file_obj=handles.handle, header=header, index=index, **self.to_csv_kwargs)
        return written

    def _batch_csv(self, args):
        offset, header, index, to_csv_kwargs = args

        batch = query_table(
            table=self.dataset.data,
            key=slice(offset, offset + self.batch_size),
            indices=self.dataset._indices,
        )
        csv_str = batch.to_pandas(integer_object_nulls=True).to_csv(
            path_or_buf=None, header=header if (offset == 0) else False, index=index, **to_csv_kwargs
        )
        return csv_str.encode(self.encoding)

    def _write(self, file_obj: BinaryIO, header, index, **to_csv_kwargs) -> int:
        """Writes the pyarrow table as CSV to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0

        if self.num_proc is None or self.num_proc == 1:
            for offset in hf_tqdm(
                range(0, len(self.dataset), self.batch_size),
                unit="ba",
                desc="Creating CSV from Arrow format",
            ):
                csv_str = self._batch_csv((offset, header, index, to_csv_kwargs))
                num_bytes = file_obj.write(csv_str)
                written += len(csv_str) if num_bytes is None else num_bytes

        else:
            num_rows, batch_size = len(self.dataset), self.batch_size
            with multiprocessing.Pool(self.num_proc) as pool:
                for csv_str in hf_tqdm(
                    pool.imap(
                        self._batch_csv,
                        [(offset, header, index, to_csv_kwargs) for offset in range(0, num_rows, batch_size)],
                    ),
                    total=(num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size,
                    unit="ba",
                    desc="Creating CSV from Arrow format",
                ):
                    num_bytes = file_obj.write(csv_str)
                    written += len(csv_str) if num_bytes is None else num_bytes

        return written
