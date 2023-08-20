from fastapi import FastAPI, Form, Query
from fastapi.responses import RedirectResponse, Response
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
DEFAULT_PROJECT_ID = "effortless-lock-396523"
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
    min_id = chunk_df['id'].min()
    max_id = chunk_df['id'].max()
    logger.info(f"Records from {min_id} to {max_id} id")
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

        csv_reader = pd.read_csv(csv_stream, chunksize=DEFAULT_CSV_CHUNK_SIZE, header=None)

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

@app.get("/metrics/employees-by-job-dept")
def employees_by_job_dept(
    year: int = Query(..., description="Year for which to retrieve metrics"),
    response_format: str = Query("json", description="Response format: 'json' or 'csv'")
):
    try:
        if response_format not in ["json", "csv"]:
            return {"error": "Invalid response format. Use 'json' or 'csv'"}

        # Query BigQuery to get the required metrics
        query = f"""
            SELECT
                d.department_name as department,
                job_name as job,
                SUM(IF(EXTRACT(QUARTER FROM start_date) = 1, 1, 0)) AS Q1,
                SUM(IF(EXTRACT(QUARTER FROM start_date) = 2, 1, 0)) AS Q2,
                SUM(IF(EXTRACT(QUARTER FROM start_date) = 3, 1, 0)) AS Q3,
                SUM(IF(EXTRACT(QUARTER FROM start_date) = 4, 1, 0)) AS Q4
            FROM
                `{DEFAULT_PROJECT_ID}.{DEFAULT_DATASET_ID}.employees` as e
            LEFT JOIN
                 `{DEFAULT_PROJECT_ID}.{DEFAULT_DATASET_ID}.departments` as d ON e.department_id = d.id
            LEFT JOIN
                 `{DEFAULT_PROJECT_ID}.{DEFAULT_DATASET_ID}.jobs` as j ON e.job_id = j.id
            WHERE
                EXTRACT(YEAR FROM start_date) = {year}
            GROUP BY
                department_id, department_name, job_id, job_name
            ORDER BY
                department_name, job_name
        """
        print(query)
        query_job = client.query(query)
        results = query_job.result()

        # Convert query results to a list of dictionaries
        metrics_data = [dict(row) for row in results]

        if response_format == "csv":
            csv_content = pd.DataFrame(metrics_data).to_csv(index=False)
            return Response(content=csv_content, media_type="text/csv")

        return metrics_data

    except Exception as e:
        logger.error(traceback.format_exc())
        return {"error": str(e)}

@app.get("/metrics/higher-hiring-depts")
def departments_hiring_above_mean(
    year: int = Query(..., description="Year for which to retrieve metrics"),
    response_format: str = Query("json", description="Response format: 'json' or 'csv'")
):
    try:
        # Query BigQuery to get the required metrics
        query = f"""
            WITH department_metrics AS (
                SELECT
                    e.department_id,
                    d.department_name,
                    COUNT(*) AS hired
                FROM
                    `{DEFAULT_PROJECT_ID}.{DEFAULT_DATASET_ID}.employees` as e
                LEFT JOIN
                    `{DEFAULT_PROJECT_ID}.{DEFAULT_DATASET_ID}.departments` as d ON e.department_id = d.id
                WHERE
                    EXTRACT(YEAR FROM start_date) = {year}
                GROUP BY
                    department_id, department_name
            )

            SELECT
                dm.department_id,
                dm.department_name,
                dm.hired
            FROM
                department_metrics dm
            JOIN (
                SELECT
                    AVG(hired) AS mean_hired
                FROM
                    department_metrics
            ) avg_metrics ON dm.hired > avg_metrics.mean_hired
            ORDER BY
                dm.hired DESC
        """

        query_job = client.query(query)
        results = query_job.result()

        # Convert query results to a list of dictionaries
        metrics_data = [dict(row) for row in results]

        if response_format == "csv":
            csv_content = pd.DataFrame(metrics_data).to_csv(index=False)
            return Response(content=csv_content, media_type="text/csv")

        return metrics_data

    except Exception as e:
        logger.error(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
