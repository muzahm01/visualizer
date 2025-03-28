import io
import json

import pandas as pd

from visualizer.utils import json_parser
from visualizer.utils.data_utils import flatten_json_column


def test_load_json_data():
    sample = '{"table1": [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]}'
    file_obj = io.StringIO(sample)
    data = json_parser.load_json_data(file_obj)
    assert "table1" in data


def test_extract_json_tables():
    sample = '{"table1": [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}], "notatable": "foo"}'
    data = json.loads(sample)
    tables = json_parser.extract_json_tables(data)
    assert "table1" in tables
    assert "notatable" not in tables


def test_extract_json_columns():
    table_data = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    cols = json_parser.extract_json_columns(table_data)
    assert set(cols) == {"a", "b"}


def test_flatten_json_column():
    df = pd.DataFrame({
        "meta": ['{"updated_at": 1740570440135, "version": 0}', '{"updated_at": 1740570440140, "version": 1}'],
        "value": [10, 20]
    })
    df_flat, new_cols = flatten_json_column(df, "meta")
    # Check that new flattened columns exist and "meta" is dropped.
    assert "meta.updated_at" in new_cols
    assert "meta.version" in new_cols
    assert "meta" not in df_flat.columns
    assert df_flat["meta.updated_at"].iloc[0] == 1740570440135
