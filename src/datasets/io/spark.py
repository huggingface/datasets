import pyspark

from ..download import DownloadMode
from ..packaged_modules.spark.spark import Spark
from .abc import AbstractDatasetReader


class SparkDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        cache_dir: str = None,
        redownload: bool = False,
        **kwargs,
    ):
        super().__init__(
            path_or_paths="unused",
            cache_dir=cache_dir,
            **kwargs,
        )
        self._redownload = redownload
        self.builder = Spark(
            df=df,
            cache_dir=cache_dir,
            **kwargs,
        )

    def read(self):
        download_mode = DownloadMode.FORCE_REDOWNLOAD if self._redownload else None
        self.builder.download_and_prepare(download_mode=download_mode)
        # TODO: Support as_streaming_dataset.
        return self.builder.as_dataset()
