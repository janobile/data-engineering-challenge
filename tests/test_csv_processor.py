import pytest
import pandas as pd
from app.csv_processor import CSVProcessor
from unittest.mock import patch

# Mocking the insert_csv function to avoid database interactions
@patch('app.csv_processor.insert_csv')
def test_process_chunk(mock_insert_csv):
    # Sample DataFrame chunk for testing
    sample_chunk_df = pd.DataFrame({
        "id": [1, 2, 3],
        "department_name": ["HR", "Engineering", "Sales"]
    })

    target_table = "departments"
    
    # Call the function with the sample_chunk_df
    CSVProcessor.process_chunk(sample_chunk_df, target_table)
    
    # Assertions
    assert mock_insert_csv.call_count == 1
    args, kwargs = mock_insert_csv.call_args
    inserted_df = args[0]
    assert inserted_df.equals(sample_chunk_df)
    assert args[1] == target_table
