from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
from psycopg2 import sql

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

# Create the connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # Enable autocommit mode for the connection
    print("Connected to the database successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Read the CSV file into a DataFrame
df = pd.read_csv(CSV_FILE_PATH)

# Define the table name
TABLE_NAME = 'validation'

# Function to create table with specified schema
def create_table(conn, table_name):
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
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

# Function to insert data into the table
def insert_data(conn, df, table_name):
    # Ensure DataFrame columns match the table schema
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

    # Insert data row by row
    insert_query = sql.SQL("""
        INSERT INTO {table} (task_id, question, level, final_answer, file_name, annotator_metadata)
        VALUES (%s, %s, %s, %s, %s, %s);
    """).format(table=sql.Identifier(table_name))

    try:
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                cursor.execute(insert_query, tuple(row))
            print(f"Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

# Function to truncate the table
def truncate_table(conn, table_name):
    truncate_query = f"TRUNCATE TABLE {table_name};"
    try:
        with conn.cursor() as cursor:
            cursor.execute(truncate_query)
            print(f"Table '{table_name}' truncated successfully.")
    except Exception as e:
        print(f"Error truncating table: {e}")

# Create the table
create_table(conn, TABLE_NAME)

# Optional: Truncate the table before inserting new data
truncate_table(conn, TABLE_NAME)

# Insert data into the table
insert_data(conn, df, TABLE_NAME)

# Close the database connection
conn.close()