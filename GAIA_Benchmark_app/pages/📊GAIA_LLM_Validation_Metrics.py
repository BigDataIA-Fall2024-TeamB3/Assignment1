import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import os
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

# Function to load the data from gaia_benchmark_results into a Pandas DataFrame
def load_results_data():
    conn = connect_to_db()
    if conn:
        query = "SELECT * FROM gaia_benchmark_results;"
        try:
            df = pd.read_sql_query(query, conn)
            conn.close()  # Close the connection after loading data
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            conn.close()  # Close the connection on error
    return None

# Function to display the metrics data in the tab
def show():
    st.set_page_config(page_title="GAIA Benchmark LLM Validation Metrics", layout="wide")
    st.title("GAIA Benchmark LLM Validation Metrics")

    # Load and display the data
    df = load_results_data()

    if df is not None:
        st.subheader("Benchmark Results Data")
        st.dataframe(df)  # Display the dataframe in Streamlit

        # Display the count of results by type
        result_counts = df['result'].value_counts().reset_index()
        result_counts.columns = ['Result Type', 'Count']
        st.subheader("Result Type Counts")
        st.bar_chart(result_counts.set_index('Result Type'))
    else:
        st.write("No data available in gaia_benchmark_results.")

# Call the show function to display in the Streamlit app
if __name__ == "__main__":
    show()