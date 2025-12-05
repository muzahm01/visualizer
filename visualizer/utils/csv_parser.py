import io
import logging

import pandas as pd
import streamlit as st

from visualizer.utils.security import (
    validate_file_size,
    validate_csv_content,
    check_dataframe_size
)

logger = logging.getLogger(__name__)


@st.cache_data
def auto_read_csv(uploaded_file):
    """
    Loads CSV data from an uploaded file by allowing pandas to auto-detect the delimiter.
    Uses the Python engine by setting sep=None with security validation.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        pandas DataFrame

    Raises:
        ValueError: If file validation fails
    """
    try:
        # Validate file size
        validate_file_size(uploaded_file)

        # Validate CSV content
        raw_data = validate_csv_content(uploaded_file)

        # Decode if bytes
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8", errors="replace")

        # Parse CSV with pandas
        df = pd.read_csv(io.StringIO(raw_data), sep=None, engine='python')

        # Validate resulting DataFrame size
        check_dataframe_size(len(df), "CSV processing")

        return df
    except ValueError as e:
        # Re-raise validation errors
        logger.error(f"CSV validation failed: {e}")
        raise
    except pd.errors.ParserError as e:
        # Handle pandas parsing errors
        logger.error(f"CSV parsing failed: {e}")
        raise ValueError("Unable to parse CSV file. Please check the file format.")
    except Exception as e:
        # Log detailed error, show generic message
        logger.error(f"Unexpected error reading CSV: {e}", exc_info=True)
        raise ValueError("Unable to read CSV file. Please verify the file format.")
