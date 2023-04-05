import pyspark

from ..download import DownloadMode
from ..packaged_modules.spark.spark import Spark
from .abc import AbstractDatasetReader


class SparkDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        cache_dir: str = None,
        **kwargs,
    ):
        super().__init__(
            path_or_paths="unused",
            cache_dir=cache_dir,
            **kwargs,
        )
        self.builder = Spark(
            df=df,
            cache_dir=cache_dir,
            **kwargs,
        )

    def read(self):
        self.builder.download_and_prepare(download_mode=DownloadMode.FORCE_REDOWNLOAD)
        return self.builder.as_dataset()
