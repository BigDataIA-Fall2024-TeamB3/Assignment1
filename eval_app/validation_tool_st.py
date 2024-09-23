
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI
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
# Function to get the answer from OpenAI API using the chat format
def get_openai_chat_response(messages):
    try:
        # Create the chat completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your desired model (e.g., gpt-3.5-turbo, gpt-4)
            messages=messages
        )
        # Correct way to access the response content
        message_content = completion.choices[0].message.content.strip()
        return message_content
    except Exception as e:
        st.error(f"Error fetching response from OpenAI: {e}")
        return None
# Function to reset session state for a new question
def reset_session_state():
    st.session_state.openai_response = None
    st.session_state.show_metadata = False
# Function to initialize session state variables
def initialize_session_state():
    if 'openai_response' not in st.session_state:
        st.session_state.openai_response = None
    if 'show_metadata' not in st.session_state:
        st.session_state.show_metadata = False
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = None
# Function to display the Validation Tool tab
def show():
    st.title("Validation Tool")
    # Initialize session state variables
    initialize_session_state()
    # Load the data
    data = load_data()
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
        # Display the selected question as a non-editable prompt
        st.subheader("Validation Prompt")
        st.markdown(f"**{selected_question}**")
        # Display the expected answer from the 'final_answer' column
        expected_answer = question_data['final_answer']
        st.subheader("Expected Answer")
        st.write(expected_answer)
        # Step 1: Button to ask OpenAI with only the question
        if st.session_state.openai_response is None:
            if st.button("Ask OpenAI"):
                with st.spinner("Fetching response from OpenAI..."):
                    regular_messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": selected_question}
                    ]
                    st.session_state.openai_response = get_openai_chat_response(regular_messages)
        
        # Step 2: Display OpenAI response if available
        if st.session_state.openai_response:
            st.subheader("OpenAI Response")
            st.write(st.session_state.openai_response)
            # Step 3: Button to show and edit annotator metadata
            if st.button("Ask with Chain of Thought"):
                st.session_state.show_metadata = True
            # Step 4: Show the editable text area for annotator metadata
            if st.session_state.show_metadata:
                annotator_metadata = question_data['annotator_metadata']
                annotator_metadata_input = st.text_area("Annotator Metadata (Chain of Thought)", value=annotator_metadata, height=150)
                # Step 5: Final button to send with CoT
                if st.button("Send with Chain of Thought to OpenAI"):
                    with st.spinner("Fetching response with Chain of Thought..."):
                        cot_messages = [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": f"Question: {selected_question}\n\nChain of Thought: {annotator_metadata_input}"}
                        ]
                        cot_response = get_openai_chat_response(cot_messages)
                        if cot_response:
                            st.subheader("OpenAI Response with Chain of Thought")
                            st.write(cot_response)
    else:
        st.write("No data available to load questions.")
