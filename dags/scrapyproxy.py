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
    dag_id='proxy_pool',
    default_args=ARGS,
    schedule_interval='15 */3 * * *',
    tags=['docker_remotely']
)


docker_scrapy = DockerOperator(
    task_id='docker_scrapy',
    # docker_url='tcp://172.16.16.139:2375',
    auto_remove=True,
    container_name="docker_scrapy",
    image='dorahero2727/proxy_scrapy:v1',
    command=["crawl", "proxy"],
    network_mode='bridge',
    dag=dag
)

docker_checker = DockerOperator(
    task_id='docker_checker',
    # docker_url='tcp://172.16.16.139:2375',
    auto_remove=True,
    container_name="docker_checker",
    image='dorahero2727/proxy_checker:v2' ,
    network_mode='bridge',
    dag=dag
)

docker_scrapy >> docker_checker