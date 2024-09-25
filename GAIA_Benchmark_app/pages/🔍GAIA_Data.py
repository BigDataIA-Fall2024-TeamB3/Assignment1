import streamlit as st
import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load database configuration from environment variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Function to connect to the Cloud SQL PostgreSQL instance using psycopg2
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Function to load data into a Pandas DataFrame using psycopg2
def load_data():
    conn = connect_to_db()
    if conn:
        query = "SELECT * FROM validation;"
        try:
            # Use pandas to execute the query and read data into a DataFrame
            df = pd.read_sql_query(query, conn)
            conn.close()  # Close the connection after loading data
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            conn.close()  # Close the connection on error
    return None

# Function to display the Validation Data tab
def show():
    # Set up the Streamlit page configuration
    st.set_page_config(page_title="Validation Data Viewer", layout="wide")

    # Page Title
    st.title("🔍 GAIA Benchmark Validation Data Viewer")

    # Page Subheader with description
    st.subheader("View and Explore Validation Data")
    st.write("""
    Welcome to the Validation Data Viewer! This page provides an interactive platform to view and explore the validation data stored in the database. 
    Use the options below to filter and analyze the dataset.
    """)

    # Load and display data
    data = load_data()
    if data is not None:
        st.write("### Data Overview")
        st.write("Explore the complete dataset below. You can scroll, sort, and filter the data as needed.")
        st.dataframe(data)

        # Optional: Add a filter for a specific column
        st.write("### Filter Data by Column")
        column = st.selectbox("Select a column to filter by:", data.columns)
        unique_values = data[column].unique()
        selected_value = st.selectbox(f"Filter by {column}:", unique_values)
        filtered_data = data[data[column] == selected_value]

        st.write(f"### Filtered Data by {column}: {selected_value}")
        st.write("Here is the data filtered by your selected value.")
        st.dataframe(filtered_data)

    else:
        st.warning("No data available to display. Please check the database connection or data availability.")

# Call the show function to display in the Streamlit app
if __name__ == "__main__":
    show()