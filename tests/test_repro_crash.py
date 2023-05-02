import pyspark


def test_from_spark():
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