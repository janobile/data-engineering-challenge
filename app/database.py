from google.cloud import bigquery
from pandas import DataFrame
from app.config import DEFAULT_PROJECT_ID
from app.config import DEFAULT_DATASET_ID

# Initialize the BigQuery client
client = bigquery.Client(project=DEFAULT_PROJECT_ID)

table_schemas = {
    "departments": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("department_name", "STRING")
    ],
    "jobs": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("job_name", "STRING")
    ],
    "employees": [
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("start_date", "TIMESTAMP"),
        bigquery.SchemaField("department_id", "INTEGER"),
        bigquery.SchemaField("job_id", "INTEGER")
    ]
}

def insert_csv(df : DataFrame, table_id : str):

    # Load data into BigQuery in chunks
    table_ref = client.dataset(DEFAULT_DATASET_ID).table(table_id)

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.schema = table_schemas.get(table_id)

    load_job = client.load_table_from_dataframe(
        df, table_ref, job_config=job_config
    )
    load_job.result()  # Wait for the job to complete

def execute_query(query):
    # Execute a BigQuery query and return the results
    query_job = client.query(query)
    results = query_job.result()
    return [dict(row) for row in results]