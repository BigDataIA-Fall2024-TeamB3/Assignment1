# upload_to_cloudsql.py

from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Database credentials from environment variables
DB_USERNAME = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')

# CSV file path
CSV_FILE_PATH = 'GAIA/2023/validation/metadata.csv'

# Create the database connection URL
DATABASE_URL = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Read the CSV file into a DataFrame
df = pd.read_csv(CSV_FILE_PATH)

# Define the table name
TABLE_NAME = 'validation'

# Function to create table with specified schema and insert data
def create_table_and_insert_data(engine, df, table_name):
    # Create the table with the specified schema
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        task_id VARCHAR(255),
        question TEXT,
        level TEXT,
        final_answer VARCHAR(255),
        file_name VARCHAR(255),
        annotator_metadata TEXT
    );
    """
    
    with engine.connect() as conn:
        # Create the table
        conn.execute(text(create_table_query))
        print(f"Table '{table_name}' created successfully.")
        
        # Optional: Clear existing data
        conn.execute(text(f"TRUNCATE TABLE {table_name};"))
        print(f"Table '{table_name}' truncated.")

    # Ensure DataFrame columns match the table schema
    # Rename columns in DataFrame to match the table columns
    df.rename(columns={
        'task_id': 'task_id',
        'Question': 'question',
        'Level': 'level',
        'Final answer': 'final_answer',
        'file_name': 'file_name',
        'Annotator Metadata': 'annotator_metadata'
    }, inplace=True)

    # Select the required columns
    expected_columns = ['task_id', 'question', 'level', 'final_answer', 'file_name', 'annotator_metadata']
    df = df[expected_columns]

    # Insert data into the table
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

# Call the function
create_table_and_insert_data(engine, df, TABLE_NAME)
