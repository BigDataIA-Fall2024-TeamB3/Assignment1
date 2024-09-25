import streamlit as st
import pandas as pd
from openai import OpenAI
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load database configuration from environment variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Check if the API key is successfully loaded
if not openai_api_key:
    st.error("OpenAI API key not found. Please set the API key in the .env file.")
else:
    client = OpenAI(api_key=openai_api_key)

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

# Function to create gaia_benchmark_results table if it doesn't exist
def create_results_table():
    conn = connect_to_db()
    if conn:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS gaia_benchmark_results (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            expected_answer TEXT NOT NULL,
            generated_response TEXT NOT NULL,
            result TEXT
        );
        """
        try:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                print("Table 'gaia_benchmark_results' created or already exists.")
        except Exception as e:
            print(f"Error creating table gaia_benchmark_results: {e}")  # Use print instead of st.error
        finally:
            conn.close()
            print("Database connection closed after table creation.")
    else:
        print("Failed to connect to the database for table creation.")  # Use print instead of st.error

create_results_table()

# Function to insert result into gaia_benchmark_results table without number
def insert_result(question, expected_answer, generated_response, result):
    conn = connect_to_db()
    if conn:
        insert_query = """
        INSERT INTO gaia_benchmark_results (question, expected_answer, generated_response, result)
        VALUES (%s, %s, %s, %s);
        """
        try:
            # Convert numpy types to native Python types if necessary
            question = str(question) if not isinstance(question, str) else question
            expected_answer = str(expected_answer) if not isinstance(expected_answer, str) else expected_answer
            generated_response = str(generated_response) if not isinstance(generated_response, str) else generated_response
            result = str(result) if not isinstance(result, str) else result
            
            with conn.cursor() as cur:
                cur.execute(insert_query, (question, expected_answer, generated_response, result))
                conn.commit()
                print("Data inserted successfully.")
                print("Data inserted successfully into 'gaia_benchmark_results'.")
        except Exception as e:
            st.error(f"Error inserting data: {e}")
            print(f"Error inserting data: {e}")
        finally:
            conn.close()
            print("Database connection closed after data insertion.")
    else:
        st.error("Failed to connect to the database.")
        print("Failed to connect to the database for data insertion.")


# Function to load validation data into a Pandas DataFrame
def load_validation_data():
    conn = connect_to_db()
    if conn:
        query = "SELECT * FROM validation;"  # Adjust your query as needed
        try:
            df = pd.read_sql_query(query, conn)
            conn.close()  # Close the connection after loading data
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            conn.close()  # Close the connection on error
            print(f"Error loading data: {e}")
    else:
        print("Failed to connect to the database for loading validation data.")
    return None

# Function to get the answer from OpenAI API using the chat format
def get_openai_chat_response(messages):
    try:
        # Create the chat completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your desired model (e.g., gpt-3.5-turbo, gpt-4)
            messages=messages
        )
        # Access the response content
        message_content = completion.choices[0].message.content.strip()
        return message_content
    except Exception as e:
        st.error(f"Error fetching response from OpenAI: {e}")
        print(f"Error fetching response from OpenAI: {e}")
        return None

# Function to reset session state for a new question
def reset_session_state():
    st.session_state.openai_response = None
    st.session_state.show_metadata = False
    st.session_state.cot_response = None

# Function to initialize session state variables
def initialize_session_state():
    if 'openai_response' not in st.session_state:
        st.session_state.openai_response = None
    if 'show_metadata' not in st.session_state:
        st.session_state.show_metadata = False
    if 'cot_response' not in st.session_state:
        st.session_state.cot_response = None
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = None

# Function to display the Validation Tool tab
def show():
    st.set_page_config(page_title="GAIA Benchmark LLM Validation Tool", layout="wide")
    st.title("GAIA Benchmark LLM Validation Tool")

    # Add an introductory section with some context
    st.markdown("""
    ## Welcome to the GAIA Benchmark Validation Tool!
    
    This tool is designed to help you interactively evaluate and validate the performance of general AI models. 
    Select a question from the dropdown below, view the expected answer, and compare it with responses generated by the AI model.
    
    **Steps:**
    1. Select a validation prompt.
    2. Ask OpenAI for a response.
    3. Compare the response with the expected answer.
    4. Optionally, provide additional metadata for a more refined response.
    
    Use the buttons to record your observations and analyze the results.
    """)

    # Initialize session state variables
    initialize_session_state()

    # Load the data
    data = load_validation_data()

    if data is not None:

        # Dropdown box for selecting a validation prompt (question)
        questions = data['question'].tolist()

        # Check if a question is already selected in the session state
        if st.session_state.selected_question is None:
            st.session_state.selected_question = questions[0]

        # Display the dropdown and update the selected question
        selected_question = st.selectbox("Select a Validation Prompt", questions, index=questions.index(st.session_state.selected_question))
        
        # Reset session state if the selected question changes
        if selected_question != st.session_state.selected_question:
            st.session_state.selected_question = selected_question
            reset_session_state()

        # Filter the selected question's data
        question_data = data[data['question'] == selected_question].iloc[0]
        question = question_data['question']
        expected_answer = question_data['final_answer']  # Use final_answer as the expected answer

        # Display the selected question as a non-editable prompt
        st.subheader("📝 Validation Prompt")
        st.markdown(f"**{selected_question}**")

        # Display the expected answer from the 'final_answer' column
        st.subheader("✅ Expected Answer")
        st.write(expected_answer)

        # Display the source text if 'file_name' exists and 'source_text' is not null
        file_name = question_data['file_name']
        source_text = question_data['source_text']
        if pd.notna(file_name) and pd.notna(source_text):
            st.subheader("📄 Source Context")
            st.text_area("Source Text", value=source_text, height=150, help="Context extracted from the source document.")

        # Step 1: Button to ask OpenAI with the question and optionally the source text
        if st.session_state.openai_response is None:
            if st.button("Ask OpenAI 🚀"):
                with st.spinner("Fetching response from OpenAI..."):
                    # Create messages with or without source text
                    regular_messages = [
                        {"role": "system", "content": "You are a helpful assistant. Only give me the final answer without any explanation and description."}
                    ]
                    if pd.notna(source_text):
                        # Include source text if available
                        regular_messages.append({"role": "user", "content": f"Question: {selected_question}\n\nSource Context: {source_text}"})
                    else:
                        # Just include the question
                        regular_messages.append({"role": "user", "content": selected_question})
                    
                    st.session_state.openai_response = get_openai_chat_response(regular_messages)
        
        # Step 2: Display OpenAI response if available
        if st.session_state.openai_response and not st.session_state.cot_response:
            st.subheader("🤖 OpenAI Response")
            st.write(st.session_state.openai_response)

            # Show only the "ASIS" button after first OpenAI response
            if st.button("Record Response as 'ASIS' 📝"):
                # Insert the result with "ASIS"
                insert_result(question, expected_answer, st.session_state.openai_response, "ASIS")
                st.success("Response recorded as 'ASIS'.")

            # Show the button to ask with Chain of Thought
            if st.button("Ask with Chain of Thought 🔗"):
                st.session_state.show_metadata = True

        # Step 3: Show the editable text area for annotator metadata and CoT response
        if st.session_state.show_metadata:
            annotator_metadata = question_data['annotator_metadata']
            annotator_metadata_input = st.text_area("Annotator Metadata (Chain of Thought)", value=annotator_metadata, height=150, help="Provide additional context or logic to guide the AI's response.")

            # Step 4: Button to send with CoT
            if st.button("Send with Chain of Thought to OpenAI ✨"):
                with st.spinner("Fetching response with Chain of Thought..."):
                    cot_messages = [
                        {"role": "system", "content": "You are a helpful assistant. Only give me the final answer without any explanation and description."},
                    ]

                    # Check if source text is available and append it to the Chain of Thought prompt
                    if pd.notna(source_text):
                        cot_messages.append(
                            {"role": "user", "content": f"Question: {selected_question}\n\nSource Context: {source_text}\n\nChain of Thought: {annotator_metadata_input}"}
                        )
                    else:
                        cot_messages.append(
                            {"role": "user", "content": f"Question: {selected_question}\n\nChain of Thought: {annotator_metadata_input}"}
                        )

                    st.session_state.cot_response = get_openai_chat_response(cot_messages)
        
        # Step 5: Display CoT response if available
        if st.session_state.cot_response:
            st.subheader("🧠 OpenAI Response with Chain of Thought")
            st.write(st.session_state.cot_response)

            # Show "With Instructions" and "Unable to Answer" buttons
            col1, col2 = st.columns(2)
            if col1.button("Record as 'With Instructions' ✅"):
                insert_result(question, expected_answer, st.session_state.cot_response, "With Instructions")
                st.success("Response recorded as 'With Instructions'.")

            if col2.button("Record as 'Unable to Answer' ❌"):
                insert_result(question, expected_answer, st.session_state.cot_response, "Unable to Answer")
                st.success("Response recorded as 'Unable to Answer'.")
    else:
        st.warning("No data available in the database. Please ensure the data is correctly loaded.")

# Call the show function to display in the Streamlit app
if __name__ == "__main__":
    show()