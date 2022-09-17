import contextlib
import multiprocessing
import os
from sqlite3 import Connection, connect
from typing import Optional, Union

from .. import Dataset, Features, config
from ..formatting import query_table
from ..packaged_modules.sql.sql import Sql
from ..utils import logging
from ..utils.typing import NestedDataStructureLike, PathLike
from .abc import AbstractDatasetInputStream


class SqlDatasetReader(AbstractDatasetInputStream):
    def __init__(
        self,
        conn: NestedDataStructureLike[Union[PathLike, Connection]],
        table_name: str,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        super().__init__(features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs)
        conn = conn if isinstance(conn, dict) else {"train": conn}
        self.builder = Sql(
            cache_dir=cache_dir,
            conn=conn,
            features=features,
            table_name=table_name,
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
            split="train", ignore_verifications=ignore_verifications, in_memory=self.keep_in_memory
        )
        return dataset


class SqlDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, Connection],
        table_name: str,
        batch_size: Optional[int] = None,
        num_proc: Optional[int] = None,
        **to_sql_kwargs,
    ):

        if num_proc is not None and num_proc <= 0:
            raise ValueError(f"num_proc {num_proc} must be an integer > 0.")

        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.table_name = table_name
        self.batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
        self.num_proc = num_proc
        self.encoding = "utf-8"
        self.to_sql_kwargs = to_sql_kwargs

    def write(self) -> int:
        _ = self.to_sql_kwargs.pop("path_or_buf", None)

        if isinstance(self.path_or_buf, (str, bytes, os.PathLike)):
            with contextlib.closing(connect(self.path_or_buf)) as conn:
                written = self._write(conn=conn, **self.to_sql_kwargs)
        else:
            written = self._write(conn=self.path_or_buf, **self.to_sql_kwargs)
        return written

    def _batch_sql(self, offset):
        batch = query_table(
            table=self.dataset.data,
            key=slice(offset, offset + self.batch_size),
            indices=self.dataset._indices,
        )
        return batch.to_pandas()

    def _write(self, conn: Connection, **to_sql_kwargs) -> int:
        """Writes the pyarrow table as SQL to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0

        if self.num_proc is None or self.num_proc == 1:
            for offset in logging.tqdm(
                range(0, len(self.dataset), self.batch_size),
                unit="ba",
                disable=not logging.is_progress_bar_enabled(),
                desc="Creating SQL from Arrow format",
            ):
                df = self._batch_sql(offset)
                written += df.to_sql(
                    self.table_name, conn, **to_sql_kwargs, if_exists="replace" if offset == 0 else "append"
                ) or len(df)

        else:
            num_rows, batch_size = len(self.dataset), self.batch_size
            with multiprocessing.Pool(self.num_proc) as pool:
                for idx, df in logging.tqdm(
                    enumerate(
                        pool.imap(
                            self._batch_sql,
                            [offset for offset in range(0, num_rows, batch_size)],
                        )
                    ),
                    total=(num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size,
                    unit="ba",
                    disable=not logging.is_progress_bar_enabled(),
                    desc="Creating SQL from Arrow format",
                ):
                    written += df.to_sql(
                        self.table_name, conn, **to_sql_kwargs, if_exists="replace" if idx == 0 else "append"
                    ) or len(df)

        return written
