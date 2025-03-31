from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
from etl_x import run_twitter_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2023, 1, 1),  # Dynamically set the start date to 1 day ago
    'email': ['delldevice11@gmail.com'],  # Replace with your email
    'email_on_failure': True,  # Enable email notifications on failure
    'email_on_retry': True,  # Enable email notifications on retry
    'retries': 3,  # Increase retries to 3 for better fault tolerance
    'retry_delay': timedelta(minutes=5),  # Increase retry delay to 5 minutes
    'catchup': False  # Disable backfilling of missed runs
}

dag = DAG(
    'x-dag',
    default_args=default_args,
    description='A simple DAG to run Twitter ETL',
)

run_twitter_etl = PythonOperator(
    task_id='run_twitter_etl',
    python_callable=run_twitter_etl,
    dag=dag,
) 

run_twitter_etl