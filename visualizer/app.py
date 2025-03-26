import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Visualizer", layout="wide")

# Home page content
st.title("Visualizer")
st.markdown(
    """
    Welcome to Visualizer, a multipage data visualization app for JSON and CSV files.

    **Pages Available:**
    - **JSON Analysis:** Upload and analyze a single JSON file.
    - **JSON Comparison:** Compare two JSON files.
    - **CSV Analysis:** Upload and analyze a single CSV file.
    - **CSV Comparison:** Compare two CSV files.

    Use the sidebar to navigate between pages. Each page provides options for selecting chart types, axis (x and y) selection (optional), and additional chart options.
    """
)
