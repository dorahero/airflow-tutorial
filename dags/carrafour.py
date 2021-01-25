from datetime import timedelta, datetime
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
import pendulum

local_tz = pendulum.timezone("Asia/Taipei")
ARGS = {
    'owner': 'Airflow',
    'start_date': datetime(2021, 1, 25, tzinfo=local_tz),
    'retries': 1, 
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='carrafour_docker',
    default_args=ARGS,
    schedule_interval='45 17 * * *',
    tags=['crawl', 'carrefour', 'docker']
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