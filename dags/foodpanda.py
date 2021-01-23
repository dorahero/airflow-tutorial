from __future__ import print_function
import time
from builtins import range
from pprint import pprint
from airflow.models.dagrun import DagRun
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator


ARGS = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='foodpanda_docker',
    default_args=ARGS,
    schedule_interval='55 11 * * *',
    tags=['docker_remotely']
)


docker = DockerOperator(
    task_id='foodpanda_scrapy',
    # docker_url='tcp://172.16.16.139:2375',
    auto_remove=True,
    container_name="foodpanda_scrapy",
    image='dorahero2727/foodpanda_scrapy:v1',
    command=["crawl", "foodpanda"],
    network_mode='bridge',
    dag=dag
)

docker