import streamlit as st
import validation_data_st
import validation_metrics_st
import validation_tool_st

# Create tabs for navigation
tabs = st.tabs(["Validation Data", "Validation Tool", "Validation Metrics"])

# Tab 1 - Validation Data
with tabs[0]:
    validation_data_st.show()

# Tab 2 - Validation Tool
with tabs[1]:
    validation_tool_st.show()

# Tab 3 - Validation Metrics
with tabs[2]:
    validation_metrics_st.show()
