import json
import csv
import os
from google.cloud import storage

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def convert_jsonl_to_csv(jsonl_file, csv_file):
    """Reads a JSONL file and converts it to a CSV file."""
    
    # Open the JSONL file and read the lines
    with open(jsonl_file, 'r') as jsonl_fp, open(csv_file, 'w', newline='') as csv_fp:
        writer = None

        # Read each line from the JSONL file
        for line in jsonl_fp:
            # Parse the JSON data
            data = json.loads(line)

            # Initialize the CSV writer with headers based on the first JSON object
            if writer is None:
                headers = data.keys()  # Get the JSON keys to use as CSV headers
                writer = csv.DictWriter(csv_fp, fieldnames=headers)
                writer.writeheader()

            # Write the JSON data to CSV row by row
            writer.writerow(data)
    
    print(f"Converted {jsonl_file} to {csv_file}.")

def process_jsonl_to_csv_in_gcs(bucket_name, jsonl_blob_path, csv_blob_path):
    """Downloads JSONL file from GCS, converts it to CSV, and uploads CSV back to GCS."""
    
    # Temporary file paths for local storage
    temp_jsonl_file = '/tmp/temp_metadata.jsonl'
    temp_csv_file = '/tmp/temp_metadata.csv'
    
    # Step 1: Download the JSONL file from GCS to a local temporary file
    download_blob(bucket_name, jsonl_blob_path, temp_jsonl_file)
    
    # Step 2: Convert the JSONL file to CSV
    convert_jsonl_to_csv(temp_jsonl_file, temp_csv_file)
    
    # Step 3: Upload the CSV file back to GCS
    upload_blob(bucket_name, temp_csv_file, csv_blob_path)

# Set the GCS bucket and file paths
bucket_name = 'gaia_files'
jsonl_blob_path = 'metadata.jsonl'  # Path to JSONL in GCS
csv_blob_path = 'metadata.csv'      # Path where CSV will be saved in GCS

# Process JSONL to CSV in GCS
process_jsonl_to_csv_in_gcs(bucket_name, jsonl_blob_path, csv_blob_path)
