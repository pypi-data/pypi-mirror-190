# airflow-kaldea

This is a collection of [Airflow](https://airflow.apache.org/) operators to provide integration with [Kaldea](https://www.kaldea.com).

```py
from airflow.models import DAG
from airflow_kaldea.operators.kaldea_job_operator import KaldeaJobOperator

default_args = {}

dag = DAG(
    dag_id='data_dag',
    default_args=default_args,
    schedule_interval='0 * * * *',
)

kaldea_job = KaldeaJobOperator(
    task_id='kaldea_job',
    kaldea_job_id='kaldea_job_id',
    kaldea_task_id='kaldea_task_id',
    dag=dag,
)
```

## Installation

Install from PyPI:

```sh
pip install airflow-kaldea
```
