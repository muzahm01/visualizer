import json

import streamlit as st


@st.cache_data
def load_json_data(uploaded_file):
    """Load JSON data from an uploaded file."""
    return json.load(uploaded_file)


def extract_json_tables(json_data):
    """Return a dict mapping table names to table data (top-level keys with list-of-dict values)."""
    tables = {}
    for key, value in json_data.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            tables[key] = value
    return tables


def extract_json_columns(table_data):
    """Return a list of column names from the first row of table_data."""
    if table_data and isinstance(table_data[0], dict):
        return list(table_data[0].keys())
    return []


def infer_col_info(table_data, col):
    """
    Infer a column's type and extra info (for strings, maximum length)
    using a sample of rows.
    Returns a tuple: (col_type, extra)
    """
    sample = table_data[:10]
    col_type = "unknown"
    extra = ""
    for row in sample:
        if col in row and row[col] is not None:
            v = row[col]
            if isinstance(v, (int, float)):
                col_type = "numeric"
            elif isinstance(v, str):
                col_type = "string"
                lengths = [len(str(r.get(col, "")))
                           for r in sample if r.get(col) is not None]
                extra = f"max len: {max(lengths) if lengths else 0}"
            else:
                col_type = type(v).__name__
            break
    return col_type, extra


def get_numeric_data(table_data, col):
    """Extract numeric values from a column; if conversion fails, substitute 0."""
    result = []
    for row in table_data:
        try:
            result.append(float(row.get(col, 0)))
        except (ValueError, TypeError):
            result.append(0)
    return result
