from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
import pendulum

local_tz = pendulum.timezone("Asia/Taipei")

ARGS = {
    'owner': 'Airflow',
    # 'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1, 
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='proxy_pool',
    default_args=ARGS,
    schedule_interval='0 */3 * * *',
    tags=['crawl', 'proxy', 'check', 'docker']
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