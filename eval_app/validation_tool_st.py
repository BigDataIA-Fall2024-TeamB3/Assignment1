import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from google.cloud import storage
from openai import OpenAI
import pytesseract
from PIL import Image
import PyPDF2
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from environment variables
#openai_api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = openai_api_key

# Load Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ... (rest of your existing code) ...
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

# Function to read file from GCS into memory
def read_file_from_gcs(bucket_name, file_name):
    """Reads a file from GCS and returns its content as bytes."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_content = blob.download_as_bytes()
    return file_content

# Functions to process different file types
def process_text_file(file_bytes):
    content = file_bytes.decode('utf-8')
    return content

def process_csv_file(file_bytes):
    df = pd.read_csv(BytesIO(file_bytes))
    return df.to_string()

def process_excel_file(file_bytes):
    df = pd.read_excel(BytesIO(file_bytes))
    return df.to_string()

def process_image_file(file_bytes):
    image = Image.open(BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

def process_pdf_file(file_bytes):
    text = ''
    pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_audio_file(file_bytes):
    # Convert mp3 bytes to wav bytes
    audio = AudioSegment.from_file(BytesIO(file_bytes), format='mp3')
    wav_io = BytesIO()
    audio.export(wav_io, format='wav')
    wav_io.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    return text

def create_prompt(question, file_content):
    prompt = f"""
    Question:
    {question}

    Additional Information:
    {file_content}

    Answer:
    """
    return prompt

# Update your show() function
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

        # Assume 'associated_files' is a list of filenames in your DataFrame
        associated_files = question_data.get('associated_files', [])
        if associated_files:
            st.subheader("Associated Files")
            selected_files = st.multiselect("Select files to include in the prompt:", associated_files)

            file_contents = ''
            for file_name in selected_files:
                file_bytes = read_file_from_gcs('your_bucket_name', file_name)

                file_extension = os.path.splitext(file_name)[1].lower()
                if file_extension in ['.txt', '.py']:
                    content = process_text_file(file_bytes)
                elif file_extension == '.csv':
                    content = process_csv_file(file_bytes)
                elif file_extension == '.xlsx':
                    content = process_excel_file(file_bytes)
                elif file_extension in ['.jpeg', '.jpg', '.png']:
                    content = process_image_file(file_bytes)
                elif file_extension == '.pdf':
                    content = process_pdf_file(file_bytes)
                elif file_extension == '.mp3':
                    content = process_audio_file(file_bytes)
                else:
                    content = ''
                    st.warning(f"Unsupported file type: {file_extension}")

                file_contents += f"\nContent from {file_name}:\n{content}\n"

            prompt = create_prompt(selected_question, file_contents)

            if st.button("Ask OpenAI with Files"):
                with st.spinner("Fetching response from OpenAI..."):
                    response = get_openai_chat_response(prompt)
                    if response:
                        st.subheader("OpenAI Response")
                        st.write(response)
        else:
            # Proceed without associated files
            if st.session_state.openai_response is None:
                if st.button("Ask OpenAI"):
                    with st.spinner("Fetching response from OpenAI..."):
                        regular_messages = [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": selected_question}
                        ]
                        st.session_state.openai_response = get_openai_chat_response(selected_question)

            if st.session_state.openai_response:
                st.subheader("OpenAI Response")
                st.write(st.session_state.openai_response)

    else:
        st.write("No data available to load questions.")
