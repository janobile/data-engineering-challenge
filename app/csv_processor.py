import pandas as pd
from app.database import insert_csv
from app.logger import setup_logger
from app.config import DEFAULT_CSV_CHUNK_SIZE

migration_tables = ['departments', 'jobs', 'employees']
table_columns = {
    "departments": {
        "id": "int64",
        "department_name": "string"
    },
    "jobs": {
        "id": "int64",
        "job_name": "string"
    },
    "employees": {
        "id": "int64",
        "name": "string",
        "start_date": "datetime64",
        "department_id": "int64",
        "job_id": "int64"
    }
}

logger = setup_logger()

class CSVProcessor:

    @staticmethod
    def process_chunk(chunk_df, target_table):
        columns = table_columns.get(target_table)
        chunk_df.columns = columns
        #Assign data types
        for col, dtype in columns.items():
            chunk_df[col] = chunk_df[col].astype(dtype, errors='ignore')
        # Process the chunk and load it into BigQuery
        min_id = chunk_df['id'].min()
        max_id = chunk_df['id'].max()
        logger.info(f"Processing records from {min_id} to {max_id}")
        insert_csv(chunk_df, target_table)
    
    @staticmethod
    def process_csv(csv_url, target_table):
        
        # Get the schema for the target table
        if target_table not in migration_tables:
            return {"error": f"Target table '{target_table}' not found"}

        with pd.read_csv(csv_url, chunksize=DEFAULT_CSV_CHUNK_SIZE, header=None) as csv_reader:
            for chunk_df in csv_reader:
                CSVProcessor.process_chunk(chunk_df, target_table)
