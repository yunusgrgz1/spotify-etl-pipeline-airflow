from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator  # Dummy task
from datetime import datetime
from spotify_transformation import transform_data  # Import Transformation module
from spotify_s3_upload import upload_to_s3  # Import S3 upload module
from airflow.models import Variable
from airflow.operators.email_operator import EmailOperator  # For email notifications
import logging

# Define Airflow DAG
with DAG(
    dag_id='spotify_data_pipeline',
    start_date=datetime(2025, 3, 19),
    schedule_interval='@daily',  # Set to run daily
    catchup=False,  # Prevent backfilling past data
) as dag:

    # Use Airflow Variables
    # Airflow Variables allow storing and managing dynamic configuration values such as S3 bucket names, file keys, and email recipients.
    # These variables can be set in the Airflow UI under Admin > Variables or through the CLI using 'airflow variables set'.
    # You are free to set these variables arbitrarily writing the code, but Airflow Variables gives elasticity.

    bucket_name = Variable.get("s3_bucket_name", default_var="my-s3-bucket")
    s3_key = Variable.get("s3_key", default_var="spotify_data.csv")
    email_recipient = Variable.get("email_recipient", default_var="your_email@example.com")

    # Function for Extraction and Transformation
    def extract_and_transform(**context):
        """Fetch and process Spotify data."""
        df = transform_data(**context)  # Transform the data
        
        # XCom (Cross-communication) allows passing data between tasks in Airflow.
        # Here, we push the processed data into XCom so that the next task can retrieve it.
        context['ti'].xcom_push(key='processed_data', value=df.to_dict(orient='records'))
        return df

    # Start task (Dummy Task)
    start_task = DummyOperator(
        task_id='start_task'
    )

    # Transformation task
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=extract_and_transform,  # Extraction and Transformation
    )

    # Function to upload data to S3
    def upload_to_s3_task(**context):
        """Retrieve data from XCom and upload to S3."""
        ti = context['ti']
        
        # XCom pull retrieves the processed data pushed by the previous task
        processed_data = ti.xcom_pull(key='processed_data', task_ids='transform_data')

        if processed_data:
            df = pd.DataFrame(processed_data)  # Convert data to DataFrame
            upload_to_s3(df, bucket_name, s3_key)  # Upload to S3
        else:
            logging.warning("No processed data to upload to S3.")

    # S3 Upload task
    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3_task,  # S3 upload process
        provide_context=True  # Ensure context is passed
    )

    # Dummy End task
    end_task = DummyOperator(
        task_id='end_task'
    )

    # Email Notification task
    email_notification = EmailOperator(
        task_id='send_email_notification',
        to=email_recipient,
        subject="Spotify Data Pipeline Job Finished",
        html_content="""<h3>Spotify Data Pipeline has completed successfully.</h3>""",
    )

    # Task order
    start_task >> transform_task >> upload_task >> end_task  # Transform data, upload to S3, then finish
    end_task >> email_notification  # Send email after completion