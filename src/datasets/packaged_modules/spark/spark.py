from dataclasses import dataclass
import os
import pyspark
from typing import Iterable, Tuple, Union
import uuid

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
        cache_dir: str = None,
        **kwargs,
    ):
        self._spark = pyspark.sql.SparkSession.builder.getOrCreate()
        self.df = df
        self._validate_cache_dir(cache_dir)

        super().__init__(
            cache_dir=cache_dir,
            **kwargs,
        )

    def _validate_cache_dir(self, cache_dir):
        # Returns the path of the created file.
        def create_cache_and_write_probe(context):
            # makedirs with exist_ok will recursively create the directory. It will not throw an error if directories
            # already exist.
            os.makedirs(cache_dir, exist_ok=True)
            probe_file = os.path.join(cache_dir, "fs_test" + uuid.uuid4().hex)
            # Opening the file in append mode will create a new file unless it already exists, in which case it will not
            # change the file contents.
            open(probe_file, "a")
            return [probe_file]

        if self._spark.conf.get("spark.master", "").startswith("local"):
            return

        # If the cluster is multi-node, make sure that the user provided a cache_dir and that it is on an NFS
        # accessible to the driver.
        # TODO: Stream batches to the driver using ArrowCollectSerializer instead of throwing an error.
        if cache_dir:
            probe = self._spark.sparkContext.parallelize(range(1), 1).mapPartitions(create_cache_and_write_probe).collect()
            if os.path.isfile(probe[0]):
                return

        raise ValueError("When using Dataset.from_spark on a multi-node cluster, cache_dir must specify an NFS")

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
        # Declare these so that we don't reference self in write_arrow, which will result in a pickling error due to
        # pickling the SparkContext.
        writer_batch_size = self._writer_batch_size
        storage_options = self._fs.storage_options

        def write_arrow(it):
            partition_id = pyspark.TaskContext().partitionId()
            batch_id = 0
            for batch in it:
                table = pa.Table.from_batches([batch])
                writer = ArrowWriter(
                    features=Features.from_arrow_schema(batch.schema),
                    path=fpath.replace("SSSSS", f"{batch_id:05d}").replace("JJJJJ", f"{partition_id:05d}"),
                    writer_batch_size=writer_batch_size,
                    storage_options=storage_options,
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
