import streamlit as st

st.set_page_config(page_title="GAIA Benchmark LLM Evaluation Tool", layout="wide")

st.title("GAIA Benchmark LLM Evaluation Tool")
st.subheader("A Comprehensive Platform for Evaluating General AI Assistants")
st.write("""
Welcome to the GAIA Benchmark Evaluation Tool!

The GAIA benchmark aims to push the boundaries of AI research by proposing real-world questions that challenge the fundamental abilities of general AI assistants. These questions test key capabilities such as reasoning, multi-modality handling, web browsing, and tool-use proficiency.

### Overview
- **Purpose:** To assess the robustness and generalization capabilities of AI systems on real-world tasks that are conceptually simple for humans but challenging for current AI models.
- **Benchmark Scope:** The benchmark consists of questions designed to evaluate AI performance across various domains and functionalities.

### Features
- **Reasoning:** Test the logical and deductive reasoning skills of AI models with contextually rich scenarios.

### How to Use the Tool
1. **GAIA_Data:** Explore the dataset containing validation prompts and metadata.
2. **GAIA_LLM_Validation_Tool:** Select a validation prompt, obtain the AI model's response, and refine it with additional metadata to improve accuracy.
3. **GAIA_LLM_Validation_metrics:** View detailed LLM evaluation metrics.

### Getting Started
- Use the sidebar to navigate through different sections of the tool.
- Begin by exploring the **Validation Data** section to get familiar with the dataset and questions.
- Proceed to the **GAIA_LLM_Validation_Tool** to interact with the AI model and refine its responses.
- Check the **GAIA_LLM_Validation_metrics** to analyze the AI's performance across different tasks.

### Resources
- **GAIA Leaderboard:** [Leaderboard on Hugging Face](https://huggingface.co/gaia-benchmark)
         
""")