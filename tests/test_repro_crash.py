import pyspark

from datasets.arrow_writer import ArrowWriter


def test_this_is_fine():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")

    def f(it):
        for batch in it:
            yield batch

    df.mapInArrow(f, df.schema).collect()


def test_crash_from_map_in_arrow_group_by():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")

    def f(it):
        for batch in it:
            yield batch

    df.mapInArrow(f, df.schema).orderBy("col_1").collect()


def test_crash_from_map_in_arrow_order_by():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")

    def f(it):
        for batch in it:
            yield batch

    df.mapInArrow(f, df.schema).groupBy("col_1").count().collect()


def test_crash_from_map_in_arrow_arrow_writer():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")

    def f(it):
        for batch in it:
            ArrowWriter(path="dummy.txt")
            yield batch

    df.mapInArrow(f, df.schema).collect()


def test_crash_from_order_by_partition():
    spark = pyspark.sql.SparkSession.builder.master("local[*]").appName("pyspark").getOrCreate()
    data = [
        ("0", 0, 0.0),
        ("1", 1, 1.0),
        ("2", 2, 2.0),
        ("3", 3, 3.0),
    ]
    df = spark.createDataFrame(data, "col_1: string, col_2: int, col_3: float")

    df.orderBy(pyspark.sql.functions.spark_partition_id()).collect()
