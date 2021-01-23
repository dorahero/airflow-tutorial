from __future__ import print_function
import time
from builtins import range
from pprint import pprint
from airflow.models.dagrun import DagRun
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator

ARGS = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='carrafour_docker',
    default_args=ARGS,
    schedule_interval='45 17 * * *',
    tags=['docker_remotely']
)


docker = DockerOperator(
    task_id='carrefour_scrapy',
    # docker_url='tcp://172.16.16.139:2375',
    auto_remove=True,
    container_name="carrefour_scrapy",
    image='dorahero2727/carrefour_scrapy:v3',
    command=["crawl", "carrefour"],
    network_mode='bridge',
    dag=dag
)

docker