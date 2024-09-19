import json
import csv
import os

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

# File paths
jsonl_file = os.path.join('GAIA_data', '2023_validation_metadata.jsonl')
csv_file = os.path.join('GAIA_data', '2023_validation_metadata.csv')

# Convert the JSONL file to CSV
convert_jsonl_to_csv(jsonl_file, csv_file)
