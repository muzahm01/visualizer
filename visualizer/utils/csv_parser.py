import pandas as pd
import csv
import io


def load_csv_data(uploaded_file, delimiter=","):
    """
    Loads CSV data from an uploaded file using the given delimiter.
    """
    return pd.read_csv(uploaded_file, sep=delimiter)


def auto_read_csv(uploaded_file):
    """
    Attempts to auto-detect the CSV delimiter using csv.Sniffer.
    Falls back to comma if detection fails.
    """
    raw_data = uploaded_file.getvalue().decode("utf-8", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(raw_data[:1024])
        sep = dialect.delimiter
        return pd.read_csv(io.StringIO(raw_data), sep=sep)
    except Exception:
        return pd.read_csv(io.StringIO(raw_data))
