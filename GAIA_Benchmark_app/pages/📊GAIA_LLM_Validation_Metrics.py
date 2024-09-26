import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

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

        # Display the total number of questions and responses
        total_questions = df['question'].nunique()
        total_responses = len(df)
        asis_count = len(df[df['result'] == 'ASIS'])
        with_instructions_count = len(df[df['result'] == 'With Instructions'])
        unable_to_answer_count = len(df[df['result'] == 'Unable to Answer'])

        st.subheader("Summary Statistics")
        st.write(f"**Total Questions Asked:** {total_questions}")
        st.write(f"**Total Responses Recorded:** {total_responses}")
        st.write(f"**Responses Recorded as 'ASIS':** {asis_count}")
        st.write(f"**Responses Recorded as 'With Instructions':** {with_instructions_count}")
        st.write(f"**Responses Recorded as 'Unable to Answer':** {unable_to_answer_count}")

        # Display the count of results by type using a horizontal bar chart
        result_counts = df['result'].value_counts().reset_index()
        result_counts.columns = ['Result Type', 'Count']
        st.subheader("Result Type Counts")

        # Create a horizontal bar chart with adjusted width
        fig = px.bar(result_counts, y='Result Type', x='Count',
                     orientation='h',
                     labels={'Count': 'Number of Responses', 'Result Type': 'Result Type'},
                     title='Distribution of Result Types (Horizontal)')

        # Update layout to adjust the width of bars
        fig.update_traces(marker=dict(line=dict(width=0.5, color='black')))
        fig.update_layout(
            xaxis_title='Number of Responses',
            yaxis_title='Result Type',
            height=300,  # Reduced height
            width=600,   # Adjusted width
            bargap=0.4   # Increase space between bars
        )

        # Adjust the y-axis to reduce the height of each bar
        fig.update_yaxes(tickson="boundaries", range=[-0.5, len(result_counts)-0.5])

        # Display the chart in Streamlit
        st.plotly_chart(fig)

        # Display a detailed pie chart for result distribution
        st.subheader("Result Distribution")
        st.write("The pie chart below shows the distribution of responses recorded by type.")

        # Calculate percentages
        result_counts['Percentage'] = result_counts['Count'] / result_counts['Count'].sum() * 100

        # Create a more detailed pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=result_counts['Result Type'],
            values=result_counts['Count'],
            text=result_counts['Percentage'].apply(lambda x: f'{x:.1f}%'),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{text}<extra></extra>",
            textinfo='label+percent',
            insidetextorientation='radial'
        )])

        fig_pie.update_layout(
            title='Percentage Distribution of Results',
            height=500,
            width=700
        )

        st.plotly_chart(fig_pie)

        # Display additional details about the pie chart
        st.subheader("Detailed Breakdown")
        for _, row in result_counts.iterrows():
            st.write(f"**{row['Result Type']}**:")
            st.write(f"- Count: {row['Count']}")
            st.write(f"- Percentage: {row['Percentage']:.2f}%")

    else:
        st.write("No data available in gaia_benchmark_results.")

# Call the show function to display in the Streamlit app
if __name__ == "__main__":
    show()