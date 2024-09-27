# GAIA Benchmark LLM Evaluation Tool
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)


## Description:

This project has built a model evaluation tool using Streamlit to assess OpenAI model performance with validation test cases from the GAIA dataset. It streamlines the data transfer process, automating the movement of data from Hugging Face to a Google Cloud Platform (GCP) bucket and then into a VS Code environment for seamless integration. Users can interactively select and compare test cases, evaluate model outputs against ground truth, adjust metadata annotations to enhance model accuracy, and provide feedback. The tool offers thorough evaluation through detailed reports and visualizations.

Documenatation - https://codelabs-preview.appspot.com/?file_id=1oVTbU2Amu7eV3ubZ5p0GjSx5g8veuKaBHyUCSX16VVU#0

## Architecture:
![gaia_benchmark_llm_evaluation_tool](https://github.com/user-attachments/assets/cf7d4c65-dfa2-461e-8a19-8c7780d6f3f1)

## About:
The problem revolves around developing a seamless, efficient, and user-focused evaluation tool for comparing OpenAI model outputs against predefined validation test cases. The tool must enable user interactions for refining inputs and capturing feedback, which ultimately enhances the model's performance while maintaining an intuitive user experience.

### Scope:
The evaluation tool should be capable of handling large datasets and automating data transfer processes, specifically from Hugging Face to a Google Cloud Platform (GCP) environment. Streamlit will serve as the primary user interface, allowing users to select test cases, compare outputs with ground truth data, and modify metadata annotations. This interaction will facilitate iterative evaluations, helping improve the accuracy and efficiency of AI models while providing clear, actionable insights through detailed reports and visualizations.

### Outcomes:
The solution will not only streamline the process of test case selection and comparison but also ensure seamless data integration. This will enable users to refine and process data more effectively, capturing and visualizing feedback accurately. By incorporating visual reports, the tool provides a comprehensive understanding of model performance.

## Application Workflow:
The GAIA Benchmark LLM Evaluation Tool integrates several components, including data preprocessing, infrastructure setup using Terraform, and a multi-page Streamlit application. The workflow is organized into multiple steps:

**1.Infrastructure Setup Using Terraform**:
  
  Cloud SQL Setup: Terraform is used to automate the setup of a PostgreSQL instance in Google Cloud SQL. This involves defining necessary resources and optimizing settings for performance and cost.
  
  Google Cloud Storage (GCS) Setup: Creates a GCS bucket using Terraform for storing datasets and configuration files.

**2.Data Handling and Preprocessing**:
  
  JSON to CSV Conversion: Converts Metadata in GCloud Bucket from a JSON format to CSV to simplify data ingestion. This ensures integrity and consistency during the data transformation process.
  
  Data Transfer from Bucket to GCP Cloud SQL: Uses Python libraries (e.g., psycopg2) to connect and upload the Metadata CSV data to Cloud SQL. It includes error handling to manage issues during the connection and upload processes.

  Data Handling for Context of Prompts: After creating a metadata table in GCloud SQL, we select the files related to prompts (context) from the bucket and process them into text, add them as a new column in our table.

**3.Streamlit Application Pages**:
  
  GAIA LLM Validation Tool: Provides an interactive UI for users to select test cases, generate model responses, and provide feedback. It enables users to refine and re-evaluate model outputs.
  
  GAIA LLM Validation Metrics: Displays various performance metrics, such as accuracy and response time, using interactive visualizations to help users analyze model performance.
  
  GAIA Data Overview: Allows users to explore the GAIA dataset, including metadata, with filtering and search capabilities.


**4.Main Application Mechanism**: 
  
  In the GAIA LLM Validation Tool page, We can select the prompts from GAIA Dataset based on different criteria (like levels of the questions or prompts with attachments only etc..) and send the prompt along with it's context (if it has any context or attachment) to openAI API.
  
  OpenAI API returns an answer for us to validate, we'll check if the returned answer is matching with the expected answer from the GAIA Dataset (that's displayed in the application), if we find it matching then we'll consider this case as 'ASIS', if not we'll use the Chain of Thought prompting with the annotator data (in editable format to remove the answer).
  
  If the answer matches after Chain of Thought prompting then we'll count this case to be 'correct answer with instructions' else it'll be counted as 'Unable to answer'

**4.Intelligence Analytics**:
  
  In GAIA LLM Validation Metrics page, we'll display all the recorded data for different categories (ASIS, Correct answer with instructions or Unable to answer) that gives us the capability of the LLM Model in a visual manner.
  

## Project Tree:
```
Assignment1/
├── .devcontainer/
│   └── devcontainer.json
├── GAIA_Benchmark_app/
│   ├── pages/
│   ├── GAIA_Benchmark_LLM.py
│   └── requirements.txt
├── data_handle/
│   ├── datatransfer_gcpbucket.py
│   ├── datatransfer_gcpsql.py
│   ├── json_csv_gaia.py
│   ├── main_data_transfer.py
│   └── source_text_extract.py
├── terraform_IaC/
│   ├── main.tf
│   └── variables.tf
├── .DS_Store
├── .gitignore
├── README.md
└── requirements.txt
```


## Set Up Application locally:

To run the application locally, follow these steps:

1. Clone the repository to get all the source code on your machine.

2. Use make install, make server, make streamlit to create the environment by setting up venv.

3. Login to your GCP. Spin up a DB and create a bucket with the terraform file to handle the GAIA Data

4. Create a .env file in the root directory with the following variables:
```
GOOGLE_APPLICATION_CREDENTIALS="your GCP Service Account json file"
OPENAI_API_KEY="your openAI API Key"
DB_HOST="your host IP"
DB_PORT=5432
DB_NAME="your DB name"
DB_USER="your DB username"
DB_PASSWORD="your DB password"
```

4. Clone GAIA Data repo to the root directory location.
```
git lfs install
```
```
# When prompted for a password, use an access token with write permissions.
# Generate one from your settings: https://huggingface.co/settings/tokens
git clone https://huggingface.co/datasets/gaia-benchmark/GAIA
```
5. Open Terminal at root directory and run the below commands in the given order:
```
pip install requirements.txt
```
```
cd data_handle
```
```
python3 main_data_transfer.py
```
```
streamlit run GAIA_Benchmark_LLM.py
```

6. Application Starts running in your local for you to validate!

## Accessing application via Streamlit Cloud:

After deploying application through github on Strealit Cloud, you can use the application at url: 
https://gaia-benchmark-llm.streamlit.app/
