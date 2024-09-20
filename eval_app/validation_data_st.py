import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import PyPDF2
import docx
import speech_recognition as sr
from pydub import AudioSegment
from sqlalchemy import create_engine
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

# Text extraction functions
def extract_text_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ""
    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        text = extract_text_from_docx(file_path)
    elif file_extension == ".xlsx":
        text = extract_text_from_excel(file_path)
    elif file_extension == ".mp3":
        text = extract_text_from_audio(file_path)
    else:
        st.warning(f"Unsupported file type: {file_extension}")
    return text
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""
    
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return ""    
def extract_text_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        text = df.to_string(index=False)
        return text
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return ""

def extract_text_from_audio(file_path):
    try:
        # Convert MP3 to WAV format
        audio = AudioSegment.from_mp3(file_path)
        wav_path = file_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
        
        # Recognize text from audio using SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Remove temporary WAV file
        os.remove(wav_path)
        
        return text
    except Exception as e:
        st.error(f"Error processing audio file: {e}")
        return ""
# Function to display the Validation Data tab with file processing
def show():
    st.header("Validation Data")
    # Load the data
    data = load_data()
    if data is not None:
        st.dataframe(data)
        # File processing section
        st.subheader("Extract Text from Files")
        file_dir = st.text_input("Enter the directory path of the files to process:")
        
        if st.button("Extract Text"):
            if os.path.isdir(file_dir):
                file_list = os.listdir(file_dir)
                file_texts = {}
                # Extract text from each file
                for file_name in file_list:
                    file_path = os.path.join(file_dir, file_name)
                    file_text = extract_text_from_file(file_path)
                    file_texts[file_name] = file_text
                # Create a DataFrame with file names and their corresponding extracted text
                extracted_df = pd.DataFrame(list(file_texts.items()), columns=['file_name', 'extracted_text'])
                st.dataframe(extracted_df)
                # Save to CSV if needed
                extracted_df.to_csv("extracted_texts.csv", index=False)
                st.success("Text extraction completed and saved to 'extracted_texts.csv'.")
            else:
                st.error("Invalid directory path. Please enter a valid path.")
    else:
        st.write("No data to display.")
