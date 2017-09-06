from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Stan_MD',
    'depends_on_the_past': False,
    'start_date': datetime(2017, 8, 1),
    'email': 'stanley@brighthive.io',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    # Changing this to seconds for development purposes
    'retry_delay': timedelta(seconds=15)
}

dag = DAG('tpot', default_args=default_args)

# A task must have owner and task_id arguments

# Task One for tagging the csv in the s3 bucket for reference
task_one = BashOperator(
    task_id='tag_csv',
    bash_command='',
    dag=dag)

# Task Two for converting the file in s3 to the Transactional DB
task_two = BashOperator(
    task_id='s3_tdb',
    bash_command='',
    retries=3,
    dag=dag)

# Task Three for starting the analysis engine run by Abacus
task_three = BashOperator(
    task_id='abacus_analysis',
    bash_command='',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

# Task Four triggered by an API query whose data request is not in the TDB
# thereby triggering task three with particular parameters
task_four = BashOperator(
    task_id='api_query',
    bash_command=templated_command,
    params={'my_param': "Parameter I passed in"},
    dag=dag)

task_three.set_upstream(task_two)
task_four.set_upstream(task_three)
