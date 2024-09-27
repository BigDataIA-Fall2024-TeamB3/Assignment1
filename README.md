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

### Features:
The solution will not only streamline the process of test case selection and comparison but also ensure seamless data integration. This will enable users to refine and process data more effectively, capturing and visualizing feedback accurately. By incorporating visual reports, the tool provides a comprehensive understanding of model performance.

## Process Outline:

**1.Data Integration**: Automate the process of extracting data from Hugging Face and transferring it to a GCP bucket. This data is then made available in a VS Code environment for further processing within the Streamlit application.

**2.Data Quality**: Apply validation checks during data transfer to ensure data integrity and consistency, with an emphasis on schema validation and error handling.

**3.Model Evaluation**: Leverage the OpenAI API within the Streamlit app to produce responses for selected test cases from the GAIA dataset. Users can refine queries and update annotations based on the model's performance.

**4.Feedback and Reporting**: Develop a module to capture user feedback and produce comprehensive visual reports, providing insights into model performance and highlighting areas for enhancement.

## Project Tree:
```
Assignment1/
├── .devcontainer/
│   └── devcontainer.json
├── data_handle/
│   ├── datatransfer_gcpbucket.py
│   ├── datatransfer_gcpsql.py
│   ├── json_csv_gaia.py
│   ├── main_data_transfer.py
│   └── source_text_extract.py
├── GAIA/
│   └── 2023/
├── GAIA.py
├── README.md
├── GAIA_Benchmark_app/
│   └── pages/
│       └── GAIA_Benchmark_LLM.py
├── requirements.txt
├── terraform_IaC/
│   ├── main.tf
│   └── variables.tf
├── venv/
│   ├── bin/
│   ├── docx-template/
│   ├── etc/
│   ├── include/
│   ├── lib/
│   └── share/
├── .env
├── .gitignore
└── bigdata-8989-caf46d240143.json
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
