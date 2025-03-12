"""
### Ingestion of shopify configuration data

Ingestion Dag 

#### DAG configuration schema

     - logical_date (date)       [ℹ End of the data time range.]

→ **Example of payload**

    {
        "logical_date": "2021-09-01",
    }
"""
from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.models.param import Param
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from tools.spark_submit_helper import get_cluster_size

DEFAULT_ARGS = {
     "depends_on_past" : False
}

with DAG("ingestion_shopify_configuration",
         catchup=True,
         max_active_runs=1,
         default_args=DEFAULT_ARGS,
         start_date=datetime(2019, 4, 1),
         end_date=datetime(2019, 4, 8),
         schedule="0 3 * * *",
         params={
              "logical_date": Param(None, type=["null", "string"])
              },
         doc_md=__doc__) as dag:

    submit_job = SparkSubmitOperator(
         task_id='spark_job_ingestion_shopify_configuration',
         application='/opt/airflow/etl/process_shopify_configuration.py',
         py_files='/opt/airflow/dist/xxx.zip',
         application_args=["--s3_bucket", Variable.get("S3_BUCKET"),
                           "--logical_date", "{{ params.logical_date if params.logical_date else ds }}",
                           "--filename", "{{ params.logical_date if params.logical_date else ds }}.csv",
                           "--aws_key_id", Variable.get("AWS_ACCESS_KEY_ID"),
                           "--aws_key_secret", Variable.get("AWS_SECRET_ACCESS_KEY"),
                           "--psql_ip", Variable.get("PSQL_IP"),
                           "--psql_db", Variable.get("PSQL_DB"),
                           "--psql_table", Variable.get("PSQL_TABLE"),
                           "--psql_user", Variable.get("PSQL_USER"),
                           "--psql_pwd", Variable.get("PSQL_SECRET")
                           ],
         conn_id='spark_default',
         **get_cluster_size('etl/config/spark_size.yaml', 'x-small'),
         verbose=False
     )
