import io

import pandas as pd
import streamlit as st


@st.cache_data
def auto_read_csv(uploaded_file):
    """
    Loads CSV data from an uploaded file by allowing pandas to auto-detect the delimiter.
    Uses the Python engine by setting sep=None.
    """
    raw_data = uploaded_file.getvalue()
    # If raw_data is bytes, decode it; if it's already a string, use it directly.
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode("utf-8", errors="replace")
    try:
        df = pd.read_csv(io.StringIO(raw_data), sep=None, engine='python')
    except Exception as e:
        st.error(f"Failed to parse CSV file: {e}")
        df = pd.DataFrame()
    return df
