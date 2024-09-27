from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.gcp.storage import GCS
from diagrams.custom import Custom

# Paths to custom icons
streamlit_icon = "streamlit_icon.png"
hf_icon = "hf-icon.png"
openaiAPI = "openai.png"
terraform_icon = "terraform-icon.png"

# Create the diagram and specify a black theme using Graphviz attributes
graph_attr = {
    "bgcolor": "black",  # Set the background color to black
    "fontcolor": "white",  # Font color for the title
    "fontsize": "20",      # Font size for the title
}

node_attr = {
    "style": "filled",
    "fillcolor": "#2D2D2D",  # Dark gray fill color for nodes
    "fontcolor": "white",    # White text in the nodes
    "color": "white",        # White outline for nodes
}

edge_attr = {
    "color": "white",  # White edges (arrows) to contrast with the black background
}

# Create the diagram
with Diagram("GAIA Benchmark LLM Evaluation Tool", show=True, direction="LR"):
    # User
    user = User("User")

    # Streamlit App
    streamlit_app = Custom("Streamlit App",streamlit_icon)

    # Hugging Face (Data Source)
    huggingface = Custom("HuggingFace",hf_icon)
    #terraform = Custom("Terraform", terraform_icon)

    # GCloud SQL (Represented by PostgreSQL)
    with Cluster("GCloud SQL + Storage", direction="LR"):
            gcloud_sql = PostgreSQL("PostgreSQL")
            gcloud_storage = GCS("GCS")

    # OpenAI API
    openai_api = Custom("OpenAI API",openaiAPI)

    # Define the flow of data and connections
    user >> streamlit_app
    streamlit_app >> openai_api
    streamlit_app << openai_api
    streamlit_app >> gcloud_sql
    streamlit_app << gcloud_sql
    gcloud_storage >> gcloud_sql
    huggingface >> gcloud_storage
    with Cluster("Infrastructure as Code", direction="LR"):
        terraform = Custom("Terraform", terraform_icon)
        gcloud_sql << terraform
    

