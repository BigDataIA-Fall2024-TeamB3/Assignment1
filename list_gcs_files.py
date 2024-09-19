from google.cloud import storage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can securely access the environment variable
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def list_files(bucket_name):
    # Create a storage client
    storage_client = storage.Client()
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    # List all objects in the bucket and print their names
    blobs = bucket.list_blobs()
    file_names = [blob.name for blob in blobs]
    print("Files in the bucket:")
    for name in file_names:
        print(name)

    return file_names

files_contents = list_files('gaia_files')
