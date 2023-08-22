from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app_config = {
    'host': '0.0.0.0',
    'port': 8000
}

DEFAULT_PROJECT_ID = "effortless-lock-396523"
DEFAULT_DATASET_ID = "globant"
DEFAULT_CSV_CHUNK_SIZE = 1000