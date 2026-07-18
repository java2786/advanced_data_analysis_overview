# c:/Users/Name/airflow/dags/...
# /Users/Name/airflow/dags/...


# /Users/arunkumar/airflow/dags/swiftkart_daily.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import sqlite3

def extract():
    df = pd.read_csv("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/3_ETL_Pipelines/daily_sales_raw.csv")
    df.to_csv("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/tmp/extracted.csv", index=False)

def transform():
    df = pd.read_csv("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/tmp/extracted.csv")
    df = df.drop_duplicates(subset="order_id")
    df["city"] = df["city"].str.strip().str.title()
    df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())
    df["revenue"] = df["quantity"] * df["unit_price"] * (1 - df["discount_percent"] / 100)
    df.to_csv("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/tmp/transformed.csv", index=False)

def load():
    df = pd.read_csv("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/tmp/transformed.csv")
    conn = sqlite3.connect("/Users/arunkumar/Documents/shared/thispc_host/advanced_data_analysis/tmp/swiftkart.db")
    df.to_sql("clean_sales", conn, if_exists="append", index=False)
    conn.close()

def notify():
    print("Swiftkart daily ETL done.")

with DAG(
    dag_id="swiftkart_daily_etl",
    start_date=datetime(2026,4,15),
    schedule="0 1 * * *",  # daily 1:00 AM
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t4 = PythonOperator(task_id="notify", python_callable=notify)

    t1 >> t2 >> t3 >> t4
