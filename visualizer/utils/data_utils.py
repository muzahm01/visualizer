import json
import pandas as pd


def flatten_json_column(df, col):
    """
    Checks if the given DataFrame column contains JSON strings or dicts.
    If so, it flattens that column into new columns with names like <col>.<key>
    and drops the original column.

    Returns the updated DataFrame and a list of new column names.
    """
    new_cols = []
    # Skip if column is not object type.
    if df[col].dtype != "object":
        return df, new_cols

    # Find the first non-null value.
    sample_series = df[col].dropna()
    if sample_series.empty:
        return df, new_cols

    sample = sample_series.iloc[0]
    try:
        # Parse if the sample is a string.
        if isinstance(sample, str):
            sample_dict = json.loads(sample)
        elif isinstance(sample, dict):
            sample_dict = sample
        else:
            return df, new_cols
    except json.decoder.JSONDecodeError:
        # Not a valid JSON, return the DataFrame as is.
        return df, new_cols

    if isinstance(sample_dict, dict):
        # Flatten the column using json_normalize.
        flat_df = pd.json_normalize(df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x))
        # Prefix new column names with the original column name.
        flat_df = flat_df.add_prefix(f"{col}.")
        new_cols = flat_df.columns.tolist()
        # Drop the original column and join the new flattened columns.
        df = df.drop(columns=[col]).join(flat_df)
    return df, new_cols
