import os
import logging
import kaggle
import psycopg2

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'nba_players_pipeline',
    default_args=default_args,
    description='A pipeline to download NBA data and upload to PostgreSQL',
    schedule_interval=None,
)

def download_dataset():
    logging.info("Setting Kaggle API credentials")
    os.environ['KAGGLE_USERNAME'] = Variable.get("username")
    os.environ['KAGGLE_KEY'] = Variable.get("key")
    logging.info("Authenticating Kaggle API")
    kaggle.api.authenticate()
    logging.info("Downloading dataset")
    kaggle.api.dataset_download_files('justinas/nba-players-data', path='/tmp', unzip=True)
    logging.info("Dataset downloaded successfully")

def upload_to_postgres():
    logging.info("Connecting to PostgreSQL database...")
    conn = psycopg2.connect(
        dbname=Variable.get("db_name"),
        user=Variable.get("db_user"),
        password=Variable.get("db_password"),
        host=Variable.get("db_host"),
        port=Variable.get("db_port")
    )
    cur = conn.cursor()
    logging.info("Connection established.")

    logging.info("Truncating table nba_players...")
    cur.execute("TRUNCATE TABLE nba_players RESTART IDENTITY;")
    logging.info("Table truncated successfully.")

    csv_file_path = '/tmp/all_seasons.csv'
    with open(csv_file_path, 'r') as f:
        next(f)
        cur.copy_expert(sql="COPY nba_players FROM STDIN WITH CSV HEADER", file=f)

    conn.commit()
    logging.info("Data uploaded successfully.")
    cur.close()
    conn.close()


download_task = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    retries=1,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_to_postgres',
    python_callable=upload_to_postgres,
    retries=1,
    dag=dag,
)

download_task >> upload_task

