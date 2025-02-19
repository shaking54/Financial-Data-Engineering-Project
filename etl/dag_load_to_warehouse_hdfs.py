from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging
from datetime import datetime, timedelta

# DAG Configuration
DAG_ID = "etl_spark_hdfs_pipeline"
HDFS_INPUT_PATH = "hdfs://hdfs-namenode:8020/data/data/raw/"  # Input File
HDFS_OUTPUT_PATH = "hdfs://hdfs-namenode:8020/data/data/processed/"  # Output Directory

# Default Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

# Initialize DAG
dag = DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="A Spark-based ETL pipeline with HDFS and Airflow",
    catchup=False,
)

# Create Spark Session
def get_spark_session():
    return SparkSession.builder \
        .appName("FinancialTransactionsETL") \
        .master("spark://spark-master-2:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://hdfs-namenode:8020") \
        .getOrCreate()


# Task 1: Extract Data from HDFS using Spark
def extract_data():
    logging.info("Starting data extraction from HDFS...")
    spark = get_spark_session()
    
    df = spark.read.csv(HDFS_INPUT_PATH+"transactions.csv", header=True, inferSchema=True)
    df.show()
    
    df.write.save("/tmp/raw_data.parquet", format="parquet", mode="overwrite")
    logging.info("Extraction complete. Data saved to /tmp/raw_data.parquet")


extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)


# Task 2: Transform Data with Spark
def transform_data():
    logging.info("Starting data transformation...")
    spark = get_spark_session()

    df = spark.read.parquet("/tmp/raw_data.parquet")

    # Data Cleaning: Remove duplicates, filter age > 25, increase salary by 10%
    df = df.dropDuplicates()
    df = df.filter(col("age") > 25)
    df = df.withColumn("salary", col("salary") * 1.1)

    df.write.mode("overwrite").parquet("/tmp/processed_data.parquet")
    logging.info("Transformation complete. Data saved to /tmp/processed_data.parquet")


transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag,
)


# Task 3: Load Processed Data to HDFS & S3
# def load_data():
#     logging.info("Uploading transformed data to HDFS and S3...")
#     spark = get_spark_session()

#     df = spark.read.parquet("/tmp/processed_data.parquet")

#     # Save to HDFS
#     df.write.mode("overwrite").parquet(HDFS_OUTPUT_PATH)
#     logging.info("Data uploaded to HDFS: %s", HDFS_OUTPUT_PATH)


# load_task = PythonOperator(
#     task_id="load_data",
#     python_callable=load_data,
#     dag=dag,
# )

# Define DAG dependencies
extract_task >> transform_task
