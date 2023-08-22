from fastapi import APIRouter, Form, Query
from fastapi.responses import RedirectResponse, Response
import pandas as pd
import requests
import traceback
from app.logger import setup_logger 
from app.csv_processor import CSVProcessor
from app.metrics import Metrics

logger = setup_logger()
router = APIRouter()

@router.get("/")
def root():
    return RedirectResponse(url="/docs")

@router.post("/upload-csv/")
def upload_csv(
    target_table: str = Form(...),
    csv_url: str = Form(...),
):
    try:
        
        CSVProcessor.process_csv(csv_url, target_table)

        return {"message": f"CSV data loaded from {csv_url} into {target_table} table"}

    except requests.exceptions.RequestException as req_exception:
        return {"error": f"HTTP Request Error: {req_exception}"}

    except pd.errors.EmptyDataError:
        return {"error": "CSV file is empty or invalid"}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    
@router.get("/metrics/employees-by-job-dept")
def employees_by_job_dept(
    year: int = Query(..., description="Year for which to retrieve metrics"),
    response_format: str = Query("json", description="Response format: 'json' or 'csv'")
):
    try:
        if response_format not in ["json", "csv"]:
            return {"error": "Invalid response format. Use 'json' or 'csv'"}
        
        metrics_data = Metrics.employees_by_job_dept(year)
        if response_format == "csv":
            csv_content = pd.DataFrame(metrics_data).to_csv(index=False)
            return Response(content=csv_content, media_type="text/csv")

        return metrics_data

    except Exception as e:
        logger.error(traceback.format_exc())
        return {"error": str(e)}
    
@router.get("/metrics/higher-hiring-depts")
def departments_hiring_above_mean(
    year: int = Query(..., description="Year for which to retrieve metrics"),
    response_format: str = Query("json", description="Response format: 'json' or 'csv'")
):
    try:
        if response_format not in ["json", "csv"]:
            return {"error": "Invalid response format. Use 'json' or 'csv'"}
        metrics_data = Metrics.departments_hiring_above_mean(year)
        if response_format == "csv":
            csv_content = pd.DataFrame(metrics_data).to_csv(index=False)
            return Response(content=csv_content, media_type="text/csv")

        return metrics_data

    except Exception as e:
        logger.error(traceback.format_exc())
        return {"error": str(e)}