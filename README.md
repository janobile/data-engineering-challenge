# Data Engineering Challenge: REST API for CSV Data Migration

Welcome to the Data Engineering Challenge repository! This project aims to solve a data engineering challenge by building a REST API for migrating historical data from CSV files into a SQL database.

## Features

- Upload historical CSV data to a database.
- Insert data in batch.
- Use the FastAPI framework to create a user-friendly REST API.

## Tech Stack

- Language: Python
- Framework: FastAPI
- Version Control: Git (hosted on GitHub)

## Project Structure
``` bash
.
├── app/                  # The main application directory.
│   ├── __init__.py       # Empty file to treat 'app' directory as a package.
│   ├── main.py           # FastAPI application code.
├── tests/                # Directory containing test files.
├── .env                  # Environment variable configuration file.
├── README.md             # This file.
└── requirements.txt      # List of project dependencies.
```
## Getting Started

1. Clone this repository to your local machine:
```
git clone git@github.com:janobile/data-engineering-challenge.git
```
2. Create and activate a virtual environment (optional but recommended):

Linux or MaxOS:
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
uvicorn app.main:app --reload
```
6. Access the FastAPI Swagger documentation at:
http://localhost:8000/docs

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