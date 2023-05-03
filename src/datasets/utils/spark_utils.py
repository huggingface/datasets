import os
import uuid


def validate_cache_dir(cache_dir, spark_function_name):
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

    import pyspark

    spark = pyspark.sql.SparkSession.builder.getOrCreate()

    if spark.conf.get("spark.master", "").startswith("local"):
        return

    # If the cluster is multi-node, make sure that the user provided a cache_dir and that it is on an NFS
    # accessible to the driver.
    # TODO: Stream batches to the driver using ArrowCollectSerializer instead of throwing an error.
    if cache_dir:
        probe = spark.sparkContext.parallelize(range(1), 1).mapPartitions(create_cache_and_write_probe).collect()
        if os.path.isfile(probe[0]):
            return

    raise ValueError(
        f"When using {spark_function_name} on a multi-node cluster, the driver and all workers should be able to access "
        "cache_dir "
    )
