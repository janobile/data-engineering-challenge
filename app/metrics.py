import pandas as pd
import app.database as db 
from app.config import DEFAULT_PROJECT_ID, DEFAULT_DATASET_ID
from app.logger import setup_logger

logger = setup_logger()

class Metrics:

    @staticmethod
    def employees_by_job_dept(year):

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
        metrics_data = db.execute_query(query)
        return metrics_data
    
    @staticmethod
    def departments_hiring_above_mean(year):

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
        metrics_data = db.execute_query(query)
        return metrics_data
