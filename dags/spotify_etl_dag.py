from include.spotify_client import extract_and_transform, load_to_sqlite
from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
import os

# Força o Airflow a reconhecer a pasta include
sys.path.append('/usr/local/airflow')


default_args = {
    'owner': 'daniel',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    dag_id='spotify_hourly_etl',
    default_args=default_args,
    schedule='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['spotify', 'etl_profissional']
)
def spotify_pipeline():

    @task
    def run_etl():
        df = extract_and_transform()
        load_to_sqlite(df)

    run_etl()


spotify_dag_obj = spotify_pipeline()
