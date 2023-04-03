import pyspark

from ..packaged_modules.spark.spark import Spark
from .abc import AbstractDatasetReader


class SparkDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        **kwargs,
    ):
        super().__init__(
            path_or_paths="unused",
            **kwargs,
        )
        self.builder = Spark(
            df=df,
            **kwargs,
        )

    def read(self):
        self.builder.download_and_prepare()
        return self.builder.as_dataset()
