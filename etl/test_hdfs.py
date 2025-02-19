from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging
from datetime import datetime, timedelta

# DAG Configuration
DAG_ID = "etl_spark_hdfs_pipeline"
HDFS_INPUT_PATH = "hdfs://hdfs-namenode:8020/data/raw/"  # Input File
HDFS_OUTPUT_PATH = "hdfs://hdfs-namenode:8020/data/processed/"  # Output Directory

# Create Spark Session
def get_spark_session():
    return SparkSession.builder \
        .appName("ETL_Pipeline") \
        .master("spark://172.26.0.2:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://hdfs-namenode:8020") \
        .getOrCreate()


if __name__ == '__main__':
    spark = get_spark_session()
    df = spark.read.csv(HDFS_INPUT_PATH+"transactions.csv", header=True, inferSchema=True)
    df.cache()  # Cache for better performance
    df.show()

    