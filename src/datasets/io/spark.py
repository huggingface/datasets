from typing import Optional

import pyspark

from .. import Features, NamedSplit
from ..download import DownloadMode
from ..packaged_modules.spark.spark import Spark
from .abc import AbstractDatasetReader


class SparkDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        force_download: bool = False,
        **kwargs,
    ):
        super().__init__(
            split=split,
            features=features,
            cache_dir=cache_dir,
            **kwargs,
        )
        self._force_download = force_download
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
        download_mode = DownloadMode.FORCE_REDOWNLOAD if self._force_download else None
        self.builder.download_and_prepare(download_mode=download_mode)
        return self.builder.as_dataset(split=self.split)
