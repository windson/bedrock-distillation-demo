import json
import os
import unittest
from unittest.mock import MagicMock, patch

import jsonschema
import pandas as pd
import pytest

from s3_upload import upload_to_s3


def load_csv():
    return pd.read_csv('data/data.csv')

def validate_tool_config_schema(config_str):
    # Define the expected schema for your actual JSON structure
    schema = {
        "type": "object",
        "properties": {
            "tools": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "toolSpec": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "json": {
                                            "type": "object",
                                            "properties": {
                                                "type": {"type": "string"},
                                                "properties": {
                                                    "type": "object",
                                                    "properties": {
                                                        "amount": {
                                                            "type": "object",
                                                            "properties": {
                                                                "type": {"type": "string"},
                                                                "description": {"type": "string"}
                                                            }
                                                        },
                                                        "card_number": {
                                                            "type": "object",
                                                            "properties": {
                                                                "type": {"type": "string"},
                                                                "description": {"type": "string"}
                                                            }
                                                        }
                                                    }
                                                },
                                                "required": {
                                                    "type": "array",
                                                    "items": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "required": ["name", "description", "inputSchema"]
                        }
                    }
                }
            }
        },
        "required": ["tools"]
    }

    try:
        # Parse the JSON string
        config_json = json.loads(config_str)
        # Validate against schema
        jsonschema.validate(instance=config_json, schema=schema)
        return True
    except (json.JSONDecodeError, jsonschema.exceptions.ValidationError) as e:
        print(f"Validation error: {str(e)}")  # Added for debugging
        return False

class TestCSVStructure:
    @pytest.fixture(scope="class")
    def df(self):
        return load_csv()

    def test_column_existence(self, df):
        expected_columns = ["User Query", "Tool Config Example", "Selected Tool"]
        assert list(df.columns) == expected_columns, "CSV should have exactly three columns with correct names"

    def test_column_types(self, df):
        # Check if all columns are string (object) type
        assert df["User Query"].dtype == 'object', "User Query column should be string type"
        assert df["Tool Config Example"].dtype == 'object', "Tool Config Example column should be string type"
        assert df["Selected Tool"].dtype == 'object', "Selected Tool column should be string type"

    def test_non_empty_values(self, df):
        # Check for non-empty values
        assert not df["User Query"].isnull().any(), "User Query column should not have null values"
        assert not df["Tool Config Example"].isnull().any(), "Tool Config Example column should not have null values"
        assert not df["Selected Tool"].isnull().any(), "Selected Tool column should not have null values"

    def test_tool_config_json_structure(self, df):
        # Test each row in Tool Config Example
        for idx, config in df["Tool Config Example"].items():
            assert validate_tool_config_schema(config), f"Invalid JSON structure at row {idx}"

class TestJSONLStructure:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for JSONL tests."""
        from main import convert_to_jsonl
        convert_to_jsonl('data/data.csv', 'data/test_distillation_data.jsonl')
        yield
        import os
        if os.path.exists('data/test_distillation_data.jsonl'):
            os.remove('data/test_distillation_data.jsonl')

    def test_jsonl_output_structure(self):
        """Test the structure of the generated JSONL file."""
        with open('data/test_distillation_data.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                # Verify schema structure
                assert record['schemaVersion'] == 'bedrock-conversation-2024'
                assert 'system' in record
                assert isinstance(record['system'], list)
                assert 'text' in record['system'][0]
                assert 'messages' in record
                assert len(record['messages']) == 1
                assert record['messages'][0]['role'] == 'user'
                ## assert record['messages'][1]['role'] == 'assistant'

class TestS3Upload(unittest.TestCase):

    def test_upload_to_s3_boto3_client_error(self):
        """
        Test the upload_to_s3 function when boto3 client raises an error.
        This test verifies that the function properly handles and re-raises
        exceptions thrown by the boto3 client.
        """
        with patch.dict(os.environ, {"S3_BUCKET_NAME": "XXXXXXXXXXX", "S3_PREFIX": "test-prefix", "AWS_REGION": "us-west-2"}):
            with patch('boto3.client') as mock_client:
                mock_s3 = MagicMock()
                mock_s3.upload_file.side_effect = Exception("Boto3 error")
                mock_client.return_value = mock_s3

                with pytest.raises(Exception, match="Boto3 error"):
                    upload_to_s3("test_file.txt")

    def test_upload_to_s3_missing_environment_variables(self):
        """
        Test the upload_to_s3 function when required environment variables are missing.
        This test verifies that the function raises an exception when S3_BUCKET_NAME
        or S3_PREFIX environment variables are not set.
        """
        with patch.dict(os.environ, clear=True):
            with pytest.raises(Exception):
                upload_to_s3("test_file.txt")
                
    def test_upload_to_s3_successful(self):
        """
        Test successful upload to S3.
        Verify that the file is uploaded correctly and the success message is printed.
        """
        with patch('boto3.client') as mock_boto_client, \
             patch('os.getenv') as mock_getenv, \
             patch('builtins.print') as mock_print:

            # Mock environment variables
            mock_getenv.side_effect = lambda x, default=None: {
                'S3_BUCKET_NAME': 'test-bucket',
                'S3_PREFIX': 'test-prefix',
                'AWS_REGION': 'us-west-2'
            }.get(x, default)

            # Mock S3 client
            mock_s3 = MagicMock()
            mock_boto_client.return_value = mock_s3

            # Call the function
            upload_to_s3('/path/to/test_file.txt')

            # Assertions
            mock_s3.upload_file.assert_called_once_with(
                '/path/to/test_file.txt', 'test-bucket', 'test-prefix/test_file.txt'
            )
            mock_print.assert_called_once_with(
                "Successfully uploaded test_file.txt to s3://test-bucket/test-prefix/test_file.txt"
            )


if __name__ == "__main__":
    pytest.main(["-v"])
