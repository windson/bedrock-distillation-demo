import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_to_s3(file_path):
    """
    Upload a file to an S3 bucket under the specified prefix
    
    Args:
        file_path (str): Path to the local file to upload
    """
    # Get bucket name from environment variables
    bucket_name = os.getenv('S3_BUCKET_NAME')
    s3_prefix = os.getenv('S3_PREFIX')
    try:
        region = os.getenv('AWS_REGION', 'us-west-2')
        
        s3_client = boto3.client('s3', region_name=region)
        file_name = os.path.basename(file_path)
        s3_key = f"{s3_prefix.strip('/')}/{file_name}"
        
        # Upload file to S3
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {file_name} to s3://{bucket_name}/{s3_key}")
        
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        raise