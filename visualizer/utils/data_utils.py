import json
import logging
import pandas as pd

from visualizer.utils.security import (
    check_flatten_size,
    get_json_depth,
    sanitize_column_name,
    MAX_JSON_DEPTH
)

logger = logging.getLogger(__name__)


def flatten_json_column(df, col):
    """
    Checks if the given DataFrame column contains JSON strings or dicts.
    If so, it flattens that column into new columns with names like <col>.<key>
    and drops the original column.

    Returns the updated DataFrame and a list of new column names.

    Args:
        df: pandas DataFrame
        col: Column name to flatten

    Returns:
        Tuple of (updated DataFrame, list of new column names)

    Raises:
        ValueError: If DataFrame is too large or JSON is too complex
    """
    new_cols = []

    # Check DataFrame size before processing
    try:
        check_flatten_size(len(df))
    except ValueError as e:
        logger.warning(f"Flatten operation skipped for column '{col}': {e}")
        raise

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

        # Validate JSON depth
        depth = get_json_depth(sample_dict)
        if depth > MAX_JSON_DEPTH:
            logger.warning(f"Column '{col}' has JSON depth {depth} exceeding limit {MAX_JSON_DEPTH}")
            raise ValueError(f"JSON in column '{col}' is too deeply nested to safely flatten")

    except json.decoder.JSONDecodeError:
        # Not a valid JSON, return the DataFrame as is.
        return df, new_cols
    except ValueError:
        # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Error parsing JSON in column '{col}': {e}")
        return df, new_cols

    if isinstance(sample_dict, dict):
        try:
            # Flatten the column using json_normalize with error handling.
            def safe_parse(x):
                try:
                    if isinstance(x, str):
                        parsed = json.loads(x)
                        # Validate depth for each row
                        if get_json_depth(parsed) > MAX_JSON_DEPTH:
                            return None
                        return parsed
                    return x
                except:
                    return None

            flat_df = pd.json_normalize(df[col].apply(safe_parse))

            # Sanitize new column names
            sanitized_prefix = sanitize_column_name(col)
            flat_df = flat_df.add_prefix(f"{sanitized_prefix}.")

            # Sanitize individual column names too
            flat_df.columns = [sanitize_column_name(c) for c in flat_df.columns]

            new_cols = flat_df.columns.tolist()
            # Drop the original column and join the new flattened columns.
            df = df.drop(columns=[col]).join(flat_df)
        except Exception as e:
            logger.error(f"Error flattening column '{col}': {e}")
            raise ValueError(f"Unable to flatten column '{col}'. The data structure may be too complex.")

    return df, new_cols
