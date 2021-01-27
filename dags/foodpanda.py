from datetime import timedelta, datetime
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
import pendulum

local_tz = pendulum.timezone("Asia/Taipei")

ARGS = {
    'owner': 'Airflow',
    # 'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1, 
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='foodpanda_docker',
    default_args=ARGS,
    schedule_interval='0 0 * * *',
    tags=['crawl', 'foodpanda', 'docker']
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