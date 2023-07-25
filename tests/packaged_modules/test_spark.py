from unittest.mock import patch

import pyspark

from datasets.packaged_modules.spark.spark import (
    Spark,
    SparkExamplesIterable,
    _generate_iterable_examples,
)

from ..utils import (
    require_dill_gt_0_3_2,
    require_not_windows,
)


def _get_expected_row_ids_and_row_dicts_for_partition_order(df, partition_order):
    expected_row_ids_and_row_dicts = []
    for part_id in partition_order:
        partition = df.where(f"SPARK_PARTITION_ID() = {part_id}").collect()
        for row_idx, row in enumerate(partition):
            expected_row_ids_and_row_dicts.append((f"{part_id}_{row_idx}", row.asDict()))
    return expected_row_ids_and_row_dicts


@require_not_windows
@require_dill_gt_0_3_2
def test_repartition_df_if_needed():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(100).repartition(1)
    spark_builder = Spark(df)
    # The id ints will be converted to Pyarrow int64s, so each row will be 8 bytes. Setting a max_shard_size of 16 means
    # that each partition can hold 2 rows.
    spark_builder._repartition_df_if_needed(max_shard_size=16)
    # Given that the dataframe has 100 rows and each partition has 2 rows, we expect 50 partitions.
    assert spark_builder.df.rdd.getNumPartitions() == 50


@require_not_windows
@require_dill_gt_0_3_2
def test_generate_iterable_examples():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(10).repartition(2)
    partition_order = [1, 0]
    generate_fn = _generate_iterable_examples(df, partition_order)  # Reverse the partitions.
    expected_row_ids_and_row_dicts = _get_expected_row_ids_and_row_dicts_for_partition_order(df, partition_order)

    for i, (row_id, row_dict) in enumerate(generate_fn()):
        expected_row_id, expected_row_dict = expected_row_ids_and_row_dicts[i]
        assert row_id == expected_row_id
        assert row_dict == expected_row_dict


@require_not_windows
@require_dill_gt_0_3_2
def test_spark_examples_iterable():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(10).repartition(1)
    it = SparkExamplesIterable(df)
    assert it.n_shards == 1
    for i, (row_id, row_dict) in enumerate(it):
        assert row_id == f"0_{i}"
        assert row_dict == {"id": i}


@require_not_windows
@require_dill_gt_0_3_2
def test_spark_examples_iterable_shuffle():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(30).repartition(3)
    # Mock the generator so that shuffle reverses the partition indices.
    with patch("numpy.random.Generator") as generator_mock:
        generator_mock.shuffle.side_effect = lambda x: x.reverse()
        expected_row_ids_and_row_dicts = _get_expected_row_ids_and_row_dicts_for_partition_order(df, [2, 1, 0])

        shuffled_it = SparkExamplesIterable(df).shuffle_data_sources(generator_mock)
        assert shuffled_it.n_shards == 3
        for i, (row_id, row_dict) in enumerate(shuffled_it):
            expected_row_id, expected_row_dict = expected_row_ids_and_row_dicts[i]
            assert row_id == expected_row_id
            assert row_dict == expected_row_dict


@require_not_windows
@require_dill_gt_0_3_2
def test_spark_examples_iterable_shard():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(20).repartition(4)

    # Partitions 0 and 2
    shard_it_1 = SparkExamplesIterable(df).shard_data_sources(worker_id=0, num_workers=2)
    assert shard_it_1.n_shards == 2
    expected_row_ids_and_row_dicts_1 = _get_expected_row_ids_and_row_dicts_for_partition_order(df, [0, 2])
    for i, (row_id, row_dict) in enumerate(shard_it_1):
        expected_row_id, expected_row_dict = expected_row_ids_and_row_dicts_1[i]
        assert row_id == expected_row_id
        assert row_dict == expected_row_dict

    # Partitions 1 and 3
    shard_it_2 = SparkExamplesIterable(df).shard_data_sources(worker_id=1, num_workers=2)
    assert shard_it_2.n_shards == 2
    expected_row_ids_and_row_dicts_2 = _get_expected_row_ids_and_row_dicts_for_partition_order(df, [1, 3])
    for i, (row_id, row_dict) in enumerate(shard_it_2):
        expected_row_id, expected_row_dict = expected_row_ids_and_row_dicts_2[i]
        assert row_id == expected_row_id
        assert row_dict == expected_row_dict


@require_not_windows
@require_dill_gt_0_3_2
def test_repartition_df_if_needed_max_num_df_rows():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    df = spark.range(100).repartition(1)
    spark_builder = Spark(df)
    # Choose a small max_shard_size for maximum partitioning.
    spark_builder._repartition_df_if_needed(max_shard_size=1)
    # The new number of partitions should not be greater than the number of rows.
    assert spark_builder.df.rdd.getNumPartitions() == 100
