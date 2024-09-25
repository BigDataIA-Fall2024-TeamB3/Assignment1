from dotenv import load_dotenv
import os
from google.cloud import storage

# Load environment variables from .env file
load_dotenv()

# Now you can securely access the environment variable
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def upload_to_gcs(bucket_name, local_folder):
    """Uploads all files in a local folder to the specified GCS bucket only if they don't already exist in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # List all files in the local folder
    for local_file in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, local_file)
        
        # Check if it's a file and not a directory
        if os.path.isfile(local_file_path):
            # Exclude '2023_validation_metadata.json' and '2023_validation_metadata.csv' from renaming
            if local_file in ['2023_validation_metadata.jsonl', '2023_validation_metadata.csv']:
                destination_blob_name = local_file
            else:
                # Remove '2023_validation_' prefix if present
                if local_file.startswith('2023_validation_'):
                    destination_blob_name = local_file[len('2023_validation_'):]
                else:
                    destination_blob_name = local_file  # Keep the original filename if prefix not present

            blob = bucket.blob(destination_blob_name)
            
            # Check if the blob already exists in GCS
            if not blob.exists():
                # Upload the file
                blob.upload_from_filename(local_file_path)
                print(f"Uploaded {local_file} as {destination_blob_name} in bucket {bucket_name}.")
            else:
                print(f"File {destination_blob_name} already exists in the bucket. Skipping upload.")

    print("All files have been processed.")

# Specify your bucket name and local folder path
upload_to_gcs('gaia_files', 'GAIA/2023/validation')
