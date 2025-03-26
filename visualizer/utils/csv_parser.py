import pandas as pd
import io
import streamlit as st


@st.cache_data
def auto_read_csv(uploaded_file):
    """
    Loads CSV data from an uploaded file by allowing pandas to auto-detect the delimiter.
    This uses the Python engine by setting sep=None.
    """
    raw_data = uploaded_file.getvalue().decode("utf-8", errors="replace")
    try:
        df = pd.read_csv(io.StringIO(raw_data), sep=None, engine='python')
    except Exception as e:
        st.error(f"Failed to parse CSV file: {e}")
        df = pd.DataFrame()
    return df
