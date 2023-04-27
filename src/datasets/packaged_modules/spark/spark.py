import os
import posixpath
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, Optional, Tuple, Union

import pyarrow as pa

import datasets
from datasets.arrow_writer import ArrowWriter, ParquetWriter
from datasets.config import MAX_SHARD_SIZE
from datasets.filesystems import (
    is_remote_filesystem,
    rename,
)
from datasets.utils.py_utils import convert_file_size_to_int


logger = datasets.utils.logging.get_logger(__name__)

if TYPE_CHECKING:
    import pyspark


@dataclass
class SparkConfig(datasets.BuilderConfig):
    """BuilderConfig for Spark."""

    features: Optional[datasets.Features] = None


class Spark(datasets.DatasetBuilder):
    BUILDER_CONFIG_CLASS = SparkConfig

    def __init__(
        self,
        df: "pyspark.sql.DataFrame",
        cache_dir: str = None,
        **config_kwargs,
    ):
        import pyspark

        self._spark = pyspark.sql.SparkSession.builder.getOrCreate()
        self.df = df
        self._validate_cache_dir(cache_dir)

        super().__init__(
            cache_dir=cache_dir,
            config_name=str(self.df.semanticHash()),
            **config_kwargs,
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
            probe = (
                self._spark.sparkContext.parallelize(range(1), 1).mapPartitions(create_cache_and_write_probe).collect()
            )
            if os.path.isfile(probe[0]):
                return

        raise ValueError(
            "When using Dataset.from_spark on a multi-node cluster, the driver and all workers should be able to access cache_dir"
        )

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager: datasets.download.download_manager.DownloadManager):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN)]

    def _prepare_split_single(
        self,
        fpath: str,
        file_format: str,
        max_shard_size: int,
    ) -> Iterable[Tuple[int, bool, Union[int, tuple]]]:
        import pyspark

        writer_class = ParquetWriter if file_format == "parquet" else ArrowWriter
        embed_local_files = file_format == "parquet"

        # Define these so that we don't reference self in write_arrow, which will result in a pickling error due to
        # pickling the SparkContext.
        features = self.config.features
        writer_batch_size = self._writer_batch_size
        storage_options = self._fs.storage_options

        def write_arrow(it):
            # Within the same SparkContext, no two task attempts will share the same attempt ID.
            task_id = pyspark.TaskContext().taskAttemptId()
            first_batch = next(it, None)
            if first_batch is None:
                # Some partitions might not receive any data.
                return pa.RecordBatch.from_arrays(
                    [[task_id], [0], [0]],
                    names=["task_id", "num_examples", "num_bytes"],
                )
            shard_id = 0
            writer = writer_class(
                features=features,
                path=fpath.replace("SSSSS", f"{shard_id:05d}").replace("TTTTT", f"{task_id:05d}"),
                writer_batch_size=writer_batch_size,
                storage_options=storage_options,
                embed_local_files=embed_local_files,
            )
            table = pa.Table.from_batches([first_batch])
            writer.write_table(table)
            for batch in it:
                if max_shard_size is not None and writer._num_bytes >= max_shard_size:
                    num_examples, num_bytes = writer.finalize()
                    writer.close()
                    yield pa.RecordBatch.from_arrays(
                        [[task_id], [num_examples], [num_bytes]],
                        names=["task_id", "num_examples", "num_bytes"],
                    )
                    shard_id += 1
                    writer = writer_class(
                        features=writer._features,
                        path=fpath.replace("SSSSS", f"{shard_id:05d}").replace("TTTTT", f"{task_id:05d}"),
                        writer_batch_size=writer_batch_size,
                        storage_options=storage_options,
                        embed_local_files=embed_local_files,
                    )
                table = pa.Table.from_batches([batch])
                writer.write_table(table)

            if writer._num_bytes > 0:
                num_examples, num_bytes = writer.finalize()
                writer.close()
                yield pa.RecordBatch.from_arrays(
                    [[task_id], [num_examples], [num_bytes]],
                    names=["task_id", "num_examples", "num_bytes"],
                )

        stats = (
            self.df.mapInArrow(write_arrow, "task_id: long, num_examples: long, num_bytes: long")
            .groupBy("task_id")
            .agg(
                pyspark.sql.functions.sum("num_examples").alias("total_num_examples"),
                pyspark.sql.functions.sum("num_bytes").alias("total_num_bytes"),
                pyspark.sql.functions.count("num_bytes").alias("num_shards"),
                pyspark.sql.functions.collect_list("num_examples").alias("shard_lengths"),
            )
            .collect()
        )
        for row in stats:
            yield row.task_id, (row.total_num_examples, row.total_num_bytes, row.num_shards, row.shard_lengths)

    def _prepare_split(
        self,
        split_generator: "datasets.SplitGenerator",
        file_format: str = "arrow",
        max_shard_size: Optional[Union[str, int]] = None,
        num_proc: Optional[int] = None,
        **kwargs,
    ):
        max_shard_size = convert_file_size_to_int(max_shard_size or MAX_SHARD_SIZE)
        is_local = not is_remote_filesystem(self._fs)
        path_join = os.path.join if is_local else posixpath.join

        SUFFIX = "-TTTTT-SSSSS-of-NNNNN"
        fname = f"{self.name}-{split_generator.name}{SUFFIX}.{file_format}"
        fpath = path_join(self._output_dir, fname)

        total_num_examples = 0
        total_num_bytes = 0
        total_shards = 0
        task_id_and_num_shards = []
        all_shard_lengths = []

        for task_id, content in self._prepare_split_single(fpath, file_format, max_shard_size):
            (
                num_examples,
                num_bytes,
                num_shards,
                shard_lengths,
            ) = content
            if num_bytes > 0:
                total_num_examples += num_examples
                total_num_bytes += num_bytes
                total_shards += num_shards
                task_id_and_num_shards.append((task_id, num_shards))
                all_shard_lengths.extend(shard_lengths)

        split_generator.split_info.num_examples = total_num_examples
        split_generator.split_info.num_bytes = total_num_bytes

        # should rename everything at the end
        logger.debug(f"Renaming {total_shards} shards.")
        if total_shards > 1:
            split_generator.split_info.shard_lengths = all_shard_lengths

            # Define fs outside of _rename_shard so that we don't reference self in the function, which will result in a
            # pickling error due to pickling the SparkContext.
            fs = self._fs

            # use the -SSSSS-of-NNNNN pattern
            def _rename_shard(
                task_id: int,
                shard_id: int,
                global_shard_id: int,
            ):
                rename(
                    fs,
                    fpath.replace("SSSSS", f"{shard_id:05d}").replace("TTTTT", f"{task_id:05d}"),
                    fpath.replace("TTTTT-SSSSS", f"{global_shard_id:05d}").replace("NNNNN", f"{total_shards:05d}"),
                )

            args = []
            global_shard_id = 0
            for i in range(len(task_id_and_num_shards)):
                task_id, num_shards = task_id_and_num_shards[i]
                for shard_id in range(num_shards):
                    args.append([task_id, shard_id, global_shard_id])
                    global_shard_id += 1
            self._spark.sparkContext.parallelize(args, len(args)).map(lambda args: _rename_shard(*args)).collect()
        else:
            # don't use any pattern
            shard_id = 0
            task_id = task_id_and_num_shards[0][0]
            self._rename(
                fpath.replace("SSSSS", f"{shard_id:05d}").replace("TTTTT", f"{task_id:05d}"),
                fpath.replace(SUFFIX, ""),
            )
