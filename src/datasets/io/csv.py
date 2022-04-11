import multiprocessing
import os
from typing import BinaryIO, Optional, Union

from .. import Dataset, Features, NamedSplit, config
from ..formatting import query_table
from ..packaged_modules.csv.csv import Csv
from ..utils import logging
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
        **kwargs,
    ):
        super().__init__(
            path_or_paths, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        )
        path_or_paths = path_or_paths if isinstance(path_or_paths, dict) else {self.split: path_or_paths}
        self.builder = Csv(
            cache_dir=cache_dir,
            data_files=path_or_paths,
            features=features,
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


class CsvDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        num_proc: Optional[int] = None,
        **to_csv_kwargs,
    ):

        if num_proc is not None and num_proc <= 0:
            raise ValueError(f"num_proc {num_proc} must be an integer > 0.")

        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
        self.num_proc = num_proc
        self.encoding = "utf-8"
        self.to_csv_kwargs = to_csv_kwargs

    def write(self) -> int:
        _ = self.to_csv_kwargs.pop("path_or_buf", None)

        if isinstance(self.path_or_buf, (str, bytes, os.PathLike)):
            with open(self.path_or_buf, "wb+") as buffer:
                written = self._write(file_obj=buffer, **self.to_csv_kwargs)
        else:
            written = self._write(file_obj=self.path_or_buf, **self.to_csv_kwargs)
        return written

    def _batch_csv(self, args):
        offset, header, to_csv_kwargs = args

        batch = query_table(
            table=self.dataset.data,
            key=slice(offset, offset + self.batch_size),
            indices=self.dataset._indices,
        )
        csv_str = batch.to_pandas().to_csv(
            path_or_buf=None, header=header if (offset == 0) else False, **to_csv_kwargs
        )
        return csv_str.encode(self.encoding)

    def _write(self, file_obj: BinaryIO, header: bool = True, **to_csv_kwargs) -> int:
        """Writes the pyarrow table as CSV to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0

        if self.num_proc is None or self.num_proc == 1:
            for offset in logging.tqdm(
                range(0, len(self.dataset), self.batch_size),
                unit="ba",
                disable=not logging.is_progress_bar_enabled(),
                desc="Creating CSV from Arrow format",
            ):
                csv_str = self._batch_csv((offset, header, to_csv_kwargs))
                written += file_obj.write(csv_str)

        else:
            num_rows, batch_size = len(self.dataset), self.batch_size
            with multiprocessing.Pool(self.num_proc) as pool:
                for csv_str in logging.tqdm(
                    pool.imap(
                        self._batch_csv,
                        [(offset, header, to_csv_kwargs) for offset in range(0, num_rows, batch_size)],
                    ),
                    total=(num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size,
                    unit="ba",
                    disable=not logging.is_progress_bar_enabled(),
                    desc="Creating CSV from Arrow format",
                ):
                    written += file_obj.write(csv_str)

        return written
