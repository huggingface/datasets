from dataclasses import dataclass
import pyspark
from typing import Iterable, Tuple, Union

import pyarrow as pa

import datasets
from datasets.arrow_writer import ArrowWriter
from datasets.features import Features


@dataclass
class SparkConfig(datasets.BuilderConfig):
    """BuilderConfig for Spark."""

    pass


class Spark(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = SparkConfig

    def __init__(
        self,
        df: pyspark.sql.DataFrame,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.df = df

    def _info(self):
        return datasets.DatasetInfo()

    def _split_generators(self, dl_manager: datasets.download.download_manager.DownloadManager):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN)]

    def _prepare_split_single(
        self,
        gen_kwargs: dict,
        fpath: str,
        file_format: str,
        max_shard_size: int,
        job_id: int
    ) -> Iterable[Tuple[int, bool, Union[int, tuple]]]:
        def write_arrow(it):
            partition_id = pyspark.TaskContext().partitionId()
            batch_id = 0
            for batch in it:
                table = pa.Table.from_batches([batch])
                writer = ArrowWriter(
                    features=Features.from_arrow_schema(batch.schema),
                    path=fpath.replace("SSSSS", f"{batch_id:05d}").replace("JJJJJ", f"{partition_id:05d}"),
                    writer_batch_size=self._writer_batch_size,
                    storage_options=self._fs.storage_options,
                )
                writer.write_table(table)
                num_examples, num_bytes = writer.finalize()
                writer.close()
                batch_id += 1
                yield pa.RecordBatch.from_arrays(
                    [[partition_id], [num_examples], [num_bytes]],
                    names=["partition_id", "num_examples", "num_bytes"],
                )

        total_num_examples = 0
        total_num_bytes = 0
        max_partition_id = 0
        shard_lengths = []

        stats = self.df.mapInArrow(
            write_arrow,
            "partition_id: long, num_examples: long, num_bytes: long"
        ).collect()
        for row in stats:
            if row.partition_id > max_partition_id:
                max_partition_id = row.partition_id
            total_num_examples += row.num_examples
            total_num_bytes += row.num_bytes
            shard_lengths.append(row.num_bytes)

        yield 0, True, (total_num_examples, total_num_bytes, None, max_partition_id, shard_lengths)
