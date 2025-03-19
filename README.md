# Spotify ETL Pipeline with Airflow

<p float="left">
  <img src="https://raw.githubusercontent.com/yunusgrgz1/spotify-etl-pipeline-airflow/refs/heads/main/images/apache%20airflow.png" width="45%" />
  <img src="https://raw.githubusercontent.com/yunusgrgz1/spotify-etl-pipeline-airflow/refs/heads/main/images/spotfiy.jpg" width="50%" height="410½" />
</p>


This project implements an Airflow-based data pipeline for processing and uploading Spotify data. The pipeline includes extraction, transformation, and uploading to an S3 bucket. Additionally, it sends an email notification upon completion.

## Project Structure

1. **DAG Definition**: Defines the Directed Acyclic Graph (DAG) to schedule and execute tasks in a specific sequence.
2. **Tasks**: The pipeline consists of several tasks:
   - **Transformation**: Transforms the Spotify data using the `spotify_transformation` module.
   - **Upload to S3**: Uploads the processed data to a designated S3 bucket using the `spotify_s3_upload` module.
   - **Email Notification**: Sends an email notification upon successful completion of the pipeline.
   - **Dummy Tasks**: Represent the start and end points of the DAG, ensuring the workflow runs in sequence.

## Requirements

- **Airflow**: Version: 2.10.5 Apache Airflow to manage the pipeline.
- **Pandas**: Version: 2.2.3 Required for data manipulation.
- **AWS SDK**: Boto3 library for interacting with AWS S3. (Boto3 Version 1.37.15)
- **Spotify Data**: Transformation of Spotify-related data (this part is assumed to be provided by the `spotify_transformation` module).

## Setup

### 1. Install Dependencies

Ensure the following Python packages are installed:
```bash
pip install apache-airflow pandas boto3
```

### 2. Airflow Setup

- Install and configure Apache Airflow on your system.
- Initialize the Airflow database:
  ```bash
  airflow db init
  ```

### 3. Set Airflow Variables

Airflow Variables are used to store dynamic values such as the S3 bucket name, S3 file key, and email recipient.

To set the variables, use the Airflow UI or CLI:

- Example

![Grid Image](https://raw.githubusercontent.com/yunusgrgz1/spotify-etl-pipeline-airflow/refs/heads/main/images/grid1.png)


#### Using the UI:

![Grid Image](https://raw.githubusercontent.com/yunusgrgz1/spotify-etl-pipeline-airflow/refs/heads/main/images/grid.png)

- Navigate to `Admin > Variables` in the Airflow UI.
- Add the following variables:
  - `s3_bucket_name`: Your S3 bucket name (e.g., `my-s3-bucket`).
  - `s3_key`: The S3 object key (e.g., `spotify_data.csv`).
  - `email_recipient`: The recipient email address for the completion notification.

#### Using the CLI:
```bash
airflow variables set s3_bucket_name <your-s3-bucket>
airflow variables set s3_key <your-s3-key>
airflow variables set email_recipient <recipient@example.com>
```

### 4. DAG Configuration

The pipeline runs daily (`@daily`) and processes the data as follows:
- **Extract & Transform**: Fetches the data and transforms it.
- **Upload to S3**: Uploads the transformed data to your S3 bucket.
- **Email Notification**: Sends a notification to the specified email upon successful completion.

## DAG Execution

To start the DAG, trigger it from the Airflow UI or CLI:

#### From the UI:
- Navigate to the DAGs page and click on the play button for the `spotify_data_pipeline` DAG.

#### From the CLI:
```bash
airflow dags trigger spotify_data_pipeline
```

## Task Flow

1. **Start Task**: A dummy task that marks the beginning of the pipeline.
2. **Transformation Task**: The Spotify data is transformed using the `spotify_transformation` module.
3. **Upload Task**: The transformed data is uploaded to the specified S3 bucket.
4. **End Task**: A dummy task that marks the end of the pipeline.
5. **Email Notification**: Sends an email upon successful execution of the pipeline.

## Logs

Logs for each task can be viewed in the Airflow UI, which helps to debug and monitor the pipeline execution.

## Monitoring

Airflow provides a built-in UI for monitoring and managing DAGs. You can monitor task execution, check logs, and troubleshoot any issues directly from the Airflow dashboard.

## Conclusion

This pipeline automates the process of transforming and uploading Spotify data to AWS S3. You can extend the pipeline to include other steps like data analysis or additional transformation logic.
