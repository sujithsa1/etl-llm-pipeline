from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='etl_llm_customer_pipeline',
    default_args=default_args,
    description='ETL pipeline with LLM-powered data cleaning',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'llm', 'groq', 'postgres'],
) as dag:

    generate_data = BashOperator(
        task_id='generate_raw_data',
        bash_command='cd /opt/airflow && python3 scripts/generate_data.py',
    )

    clean_data = BashOperator(
        task_id='llm_clean_data',
        bash_command='cd /opt/airflow && python3 scripts/llm_cleaner.py',
        env={
            'GROQ_API_KEY': os.environ.get('GROQ_API_KEY', ''),
            'PATH': os.environ.get('PATH', ''),
        },
    )

    load_data = BashOperator(
        task_id='load_to_postgres',
        bash_command='cd /opt/airflow && python3 scripts/db_loader.py',
        env={
            'POSTGRES_HOST': 'postgres',
            'POSTGRES_PORT': '5432',
            'PATH': os.environ.get('PATH', ''),
        },
    )

    quality_check = BashOperator(
        task_id='data_quality_check',
        bash_command="""cd /opt/airflow && python3 -c "
import psycopg2
conn = psycopg2.connect(host='postgres', port=5432, database='etldb', user='etluser', password='etlpassword')
cur = conn.cursor()
cur.execute('''SELECT COUNT(*) as total, SUM(CASE WHEN email LIKE chr(37)||'@unknown.com' THEN 1 ELSE 0 END) as invalid_emails, SUM(CASE WHEN zip = '00000' THEN 1 ELSE 0 END) as missing_zips, SUM(CASE WHEN LENGTH(state) = 2 THEN 1 ELSE 0 END) as valid_states FROM customers''')
row = cur.fetchone()
print('Quality Check Results:')
print('  Total records :', row[0])
print('  Invalid emails:', row[1])
print('  Missing zips  :', row[2])
print('  Valid states  :', row[3])
assert row[0] == 50, 'Expected 50 records!'
assert row[3] == 50, 'Not all states are valid!'
print('All checks passed!')
conn.close()
"
""",
    )

    generate_data >> clean_data >> load_data >> quality_check