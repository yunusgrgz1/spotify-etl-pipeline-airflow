# spotify_s3_upload.py

import boto3
import logging
import pandas as pd
from airflow.exceptions import AirflowException

def upload_to_s3(df, bucket_name, s3_key):
    """Uploads data to S3."""
    if df.empty:
        logging.warning("No data to upload.")
        return
    
    # Save to S3 in CSV format
    csv_buffer = df.to_csv(index=False)

    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer)
        logging.info(f"Data uploaded to S3: {s3_key}")
    except Exception as e:
        raise AirflowException(f"Error uploading data to S3: {e}")
