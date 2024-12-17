from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.transform import transform_data
from scripts.load import load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
}

with DAG(
    'load_to_warehouse',
    default_args=default_args,
    params={
        'raw': 'data/raw',
        'processed': 'data/processed',
        'star': 'data/star',
        'db_url': 'jdbc:postgresql://localhost:5432/finance_dw',
        'db_properties': {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"},
        'spark_host': 'local[*]'
    },
    description='Run PySpark jobs using Airflow',
    catchup=False,
) as dag:

    # Run python script
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data
    )

    # Run python script
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data
    )

    transform_task >> load_task