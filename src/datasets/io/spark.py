from typing import Optional

import pyspark

from .. import Features, NamedSplit
from ..download import DownloadMode
from ..packaged_modules.spark.spark import Spark
from .abc import AbstractDatasetReader


class SparkDatasetReader(AbstractDatasetReader):
    """A dataset reader that reads from a Spark DataFrame.

    When caching, cache materialization is parallelized over Spark; an NFS that is accessible to the driver must be
    provided. Streaming is not currently supported.
    """

    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        load_from_cache_file: bool = True,
        file_format: str = "arrow",
        **kwargs,
    ):
        super().__init__(
            split=split,
            features=features,
            cache_dir=cache_dir,
            **kwargs,
        )
        self._load_from_cache_file = load_from_cache_file
        self._file_format = file_format
        self.builder = Spark(
            df=df,
            features=features,
            cache_dir=cache_dir,
            **kwargs,
        )

    def read(self):
        if self.streaming:
            # TODO: Support as_streaming_dataset.
            raise ValueError("SparkDatasetReader is not streamable.")
        download_mode = None if self._load_from_cache_file else DownloadMode.FORCE_REDOWNLOAD
        self.builder.download_and_prepare(
            download_mode=download_mode,
            file_format=self._file_format,
        )
        return self.builder.as_dataset(split=self.split)
