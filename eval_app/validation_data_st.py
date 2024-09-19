import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

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

# Function to connect to the Cloud SQL PostgreSQL instance using SQLAlchemy
def connect_to_db():
    try:
        # Create the SQLAlchemy connection string using the environment variables
        db_url = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Function to load data into a Pandas DataFrame
def load_data():
    engine = connect_to_db()
    if engine:
        query = "SELECT * FROM validation;"
        try:
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

# Function to display the Validation Data tab
def show():
    data = load_data()
    if data is not None:
        st.dataframe(data)
    else:
        st.write("No data to display.")
