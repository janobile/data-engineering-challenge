# Data Engineering Challenge: REST API for CSV Data Migration

Welcome to the Data Engineering Challenge repository! This project aims to solve a data engineering challenge by building a REST API for migrating historical data from CSV files into a SQL database.

## Features

- Upload historical CSV data to a database.
- Insert data in batch.
- Retrieve metrics about employees by job and department.
- Identify departments hiring above the mean.
- Use the FastAPI framework to create a user-friendly REST API.

## Tech Stack

- Language: Python
- Framework: FastAPI
- Version Control: Git (hosted on GitHub)
- Cloud Platform: Google Cloud Platform (GCP)
    - Bigquery
    - Cloud Run
    - Cloud Build
    - Artifact Registry


## Project Structure
```bash
.
├── app/                  # The main application directory.
│   ├── __init__.py       # Empty file to treat 'app' directory as a package.
│   ├── config.py         # Configuration settings and environment variables.
│   ├── logger.py         # Logger setup for the application.
│   ├── metrics.py        # Metrics class for handling metric-related queries.
│   ├── csv_processor.py  # CSVProcessor class for processing CSV data.
│   ├── routes.py         # FastAPI router for defining API endpoints.
│   ├── database.py       # Database utility for working with BigQuery.
│   ├── main.py           # FastAPI application entry point.
├── tests/                # Directory containing test files.
├── .env                  # Environment variable configuration file.
├── README.md             # This file.
├── requirements.txt      # List of project dependencies.
└── cloudbuild.yaml       # Cloud Build configuration for Docker image and Cloud Run deployment.
```
## Getting Started

1. Clone this repository to your local machine:
```
git clone git@github.com:janobile/data-engineering-challenge.git
```
2. Create and activate a virtual environment (optional but recommended):

Linux or macOS:

``` 
python3 -m venv venv
source venv/bin/activate 
```
Windows: 

```
venv\Scripts\activate
```
3. Install project dependencies using `pip`:
```
pip install -r requirements.txt
```
4. Set up your environment variables:
Create a `.env` file in the root directory and add your environment variables, such as
```
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

5. Run the FastAPI application:
```
uvicorn main:app --reload
```
6. Access the FastAPI Swagger documentation at:
http://localhost:8000/docs

## Functionality and How to Use

### Uploading CSV Data

To upload historical CSV data to the database, follow these steps:

1. Access the API endpoint `/upload-csv/` using a tool like `curl` or an API client (e.g., Postman).

2. Provide the following parameters as form data:
   - `target_table`: The target table name (e.g., "departments", "jobs", "employees").
   - `csv_url`: The URL of the CSV file to be uploaded.

3. Submit the request. The API will process the CSV data and load it into the specified table in the database.

### Retrieving Metrics

To retrieve metrics about employees by job and department, as well as departments hiring above the mean, follow these steps:

1. Access the corresponding API endpoints:
   - `/metrics/employees-by-job-dept`: Retrieves employee metrics by job and department.
   - `/metrics/higher-hiring-depts`: Retrieves departments hiring above the mean.

2. Provide the required query parameters, such as `year` for the desired year of metrics.

3. Choose the response format (`json` or `csv`), and submit the request. You will receive the requested metrics in the specified format.

## Accessing API Documentation

The API is documented using Swagger UI, which provides an interactive interface for exploring the available endpoints and their documentation.

1. Run the FastAPI application using the command:
```
uvicorn main:app --reload
```

2. Access the Swagger documentation by opening your web browser and navigating to:
[http://localhost:8000/docs](http://localhost:8000/docs)

3. Explore the API endpoints, view their documentation, and even test them directly through the Swagger UI.

## Cloud Deployment

The API is now available on Google Cloud Platform (GCP) and can be accessed at the following URL:
[https://data-engineering-challenge-hit5uiuwdq-uc.a.run.app](https://data-engineering-challenge-hit5uiuwdq-uc.a.run.app)

Feel free to interact with the API remotely to upload CSV data, retrieve metrics, and explore its functionality.

## Adding GCP Credentials for Local Execution

To execute the FastAPI application locally and access Google BigQuery services, you'll need to provide your own GCP service account credentials. Follow these steps:

1. Sign in to your Google Cloud Console and create a new service account:
   - Go to the [IAM & Admin](https://console.cloud.google.com/iam-admin/) section.
   - Click "Service accounts" from the left navigation.
   - Create a new service account with the roles "BigQuery Data Editor" and "BigQuery Job User".

2. After creating the service account, generate a JSON key (credentials) for the service account:
   - Go to the "Keys" tab of the service account you created.
   - Click "Add Key" and select "JSON" format.
   - Save the downloaded JSON key file as `credentials.json` in the root directory of this project.

3. This `credentials.json` file will provide the necessary credentials to authenticate with Google Cloud services when running the FastAPI application locally.

Remember to keep your credentials secure and never commit them to version control systems.
## Deployment

This project is designed for deployment on Google Cloud Platform (GCP). The included `cloudbuild.yaml` file automates the building of the Docker container image and deployment to Cloud Run.

1. Set up a GCP project and enable the necessary APIs (Cloud Build, Container Registry, and Cloud Run).
2. Configure your GCP credentials and project ID.
3. Trigger a build and deployment using Cloud Build:
```
gcloud builds submit --config cloudbuild.yaml .
```
4. Access the deployed API on Cloud Run.

## Future Steps

While the current implementation covers a significant portion of the challenge requirements, there are several areas where further improvements and enhancements can be made:

1. **Authentication and Security:** Strengthen the API's security by implementing authentication mechanisms such as JWT tokens to protect sensitive data and restrict unauthorized access.

2. **API Documentation Improvement:** Enhance the API documentation in the Swagger UI by providing more comprehensive explanations of endpoints, query parameters, and response formats.

3. **Environment Setup Automation:** Streamline the setup process by providing scripts or instructions that automate the installation of dependencies and configuration of environment variables.

4. **Error Handling and Error Messages:** Improve user experience by enhancing error handling and providing meaningful error messages in API responses for easier debugging.

5. **User Input Validation:** Implement validation for user inputs to ensure adherence to expected formats, preventing invalid data from causing issues.

6. **API Versioning:** Implement versioning for the API to facilitate future updates without disrupting existing clients.

7. **Data Validation and Cleaning:** Validate and sanitize data being migrated from CSV files to maintain data integrity and accuracy in the database.

8. **Container Image Versioning:** Include version tags for Docker images to manage different application versions and ensure consistency.

9. **Automated Testing:** Establish a comprehensive set of automated tests to thoroughly validate the functionality and performance of the API codebase. Include unit tests and integration tests to ensure the functionality, performance, and security of the API.

10. **Cloud-Based Testing Environment:** Create and configure a cloud-based testing environment, leveraging cloud services to simulate real-world usage scenarios and assess the system's behavior under various conditions.

These future steps will contribute to enhancing the project's robustness, usability, and scalability as it evolves.

## Contributing

1. Fork this repository.

2. Create a new branch for your feature or bug fix:
``` 
git checkout -b feature/your-feature-name
```
3. Make your changes and commit them:
```
git commit -m "Add your commit message"
```

4. Push your changes to your fork:
```
git push origin feature/your-feature-name
```
5. Create a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.