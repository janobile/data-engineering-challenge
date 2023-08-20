from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import pandas as pd
from google.cloud import bigquery
import requests
import io
from dotenv import load_dotenv
import traceback
import logging

load_dotenv()
app = FastAPI()
client = bigquery.Client()
CHUNK_SIZE = 1000

# Configuration
DEFAULT_DATASET_ID = "globant"
DEFAULT_CSV_CHUNK_SIZE = 1000

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Adjust log level as needed

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

def process_csv_chunk(chunk_df, table_ref, schema):
    """Process a chunk of CSV data and load it into BigQuery."""
    chunk_df.columns = [field.name for field in schema]

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.schema = schema

    load_job = client.load_table_from_dataframe(
        chunk_df, table_ref, job_config=job_config
    )
    load_job.result()  # Wait for the job to complete

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.post("/upload-csv/")
def upload_csv(
    target_table: str = Form(...),
    csv_url: str = Form(...),
):
    try:
        # Download CSV data from the provided URL
        response = requests.get(csv_url)
        response.raise_for_status()
        csv_content = response.content

        # Create an iterator for reading CSV in chunks
        csv_stream = io.StringIO(csv_content.decode("utf-8"))

        # Get the schema for the target table
        schema = table_schemas.get(target_table)
        if schema is None:
            return {"error": f"Target table '{target_table}' not found"}

        # Load data into BigQuery in chunks
        dataset_id = DEFAULT_DATASET_ID
        table_id = target_table
        table_ref = client.dataset(dataset_id).table(table_id)

        csv_reader = pd.read_csv(csv_stream, chunksize=DEFAULT_CSV_CHUNK_SIZE)

        chunk_count = 0

        for chunk_df in csv_reader:
            chunk_count += 1
            chunk_start_line = (chunk_count - 1) * DEFAULT_CSV_CHUNK_SIZE + 1
            chunk_end_line = chunk_start_line + len(chunk_df) - 1
            logger.info(f"Iteration {chunk_count}: Processing lines {chunk_start_line}-{chunk_end_line}")
            process_csv_chunk(chunk_df, table_ref, schema)

        return {"message": f"CSV data loaded from {csv_url} into {target_table} table"}

    except requests.exceptions.RequestException as req_exception:
        return {"error": f"HTTP Request Error: {req_exception}"}

    except pd.errors.EmptyDataError:
        return {"error": "CSV file is empty or invalid"}

    except Exception as e:
        logger.error(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
