from pyspark.sql import SparkSession

_spark_session = None

def get_spark_session():
    global _spark_session
    if _spark_session is None:
        _spark_session = SparkSession.builder \
            .appName("F1RaceData") \
            .master("local[*]") \
            .getOrCreate()
    return _spark_session

def stop_spark_session():
    global _spark_session
    if _spark_session:
        _spark_session.stop()
        _spark_session = None