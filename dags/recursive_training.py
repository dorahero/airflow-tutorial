from __future__ import print_function
import time
from builtins import range
from pprint import pprint
from airflow.models.dagrun import DagRun
from airflow.utils.dates import days_ago
from airflow.contrib.operators.ssh_operator import  SSHOperator 
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='yolov5_red',
    default_args=args,
    schedule_interval=None,
    tags=['yolov5', 'cv1', 'data preparation']
)

# Step1
dump_image_from_cvat = SSHOperator(
    task_id="Dump_image_from_cvat",
    ssh_conn_id="cv1",
    command="cd red; mkdir -p zip/{{dag_run.conf['cvat_dump_keyword']}}; ./export.sh {{dag_run.conf['cvat_dump_keyword']}}",
    dag=dag
)

# Step 2. Data preparation
unzip_dumped_image_zips = SSHOperator(
    task_id="unzip_dumped_image_zips",
    ssh_conn_id="cv1",
    command="cd /home/ub/red/zip; ./init_unzip_n.sh {{dag_run.conf['cvat_dump_keyword']}}",    
    dag=dag
)

cv1_trainer = SSHOperator(
    task_id="yolov5_training",
    ssh_conn_id="cv1",
    command="docker -H 172.16.16.88 run --rm --gpus all \
    -v /home/ub/red/yolo_data:/home/ub/red/yolo_data \
    -v /home/ub/red/data_original:/home/ub/red/data_original \
    -v /home/ub/red/yolov5_training/{{dag_run.conf['cvat_dump_keyword']}}/runs:/home/ub/red/yolo_new/runs \
    -v /home/ub/red/yolov5_training/tmp:/home/ub/red/yolov5_training/tmp \
    -v /home/ub/red/yolov5_training/templates:/home/ub/red/yolov5_training/templates \
    --shm-size 16g \
    dorahero2727/yolov5:v3 \
    bash train_for_docker.sh {{dag_run.conf['cvat_dump_keyword']}}",    
    dag=dag
)

# cv1_trainer = DockerOperator(
#     task_id="yolov5_training",
#     docker_url="tcp://172.16.16.88:2375",    
#     image='arthurtibame/yolov5',
#     command='python3 train.py --weights yolov5{{var.json.yolov5_testing.weight_size}}.pt --cfg yolov5{{var.json.yolov5_testing.weight_size}}.yaml --epochs {{var.json.yolov5_testing.epochs}} --batch_size {{var.json.yolov5_testing.batch_size}}',
#     container_name='yolov5_training',
#     volumes=[
#         '/home/ub/yolov5_training/yolo_data:/usr/src/yolo_data', # images
#         '/home/ub/yolov5_training/dm1204/coco128.yaml:/usr/src/app/data/coco128.yaml',#coco128.yaml
#         '/home/ub/yolov5_training/dm1204/hyp.scratch.yaml:/usr/src/app/data/hyp.scratch.yaml', #hyp.scratch.yaml
#         '/home/ub/yolov5_training/dm1204/yolov5{{var.json.yolov5_testing.weight_size}}.yaml:/usr/src/app/models/yolov5{{var.json.yolov5_testing.wegiht_size}}.yaml',
#         '/home/ub/yolov5_training/dm1204/runs:/usr/src/app/runs' # model saved
#     ],
#     auto_remove=True,
#     mem_limit="16g",
#     dag=dag
# )
dump_image_from_cvat >> unzip_dumped_image_zips >> cv1_trainer