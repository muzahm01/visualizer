import streamlit as st
import pandas as pd
from visualizer.utils import json_parser, chart_utils
from visualizer.utils.data_utils import flatten_json_column

st.title("JSON File Analysis")

# Upload one JSON file.
json_file = st.file_uploader("Upload a JSON File", type=["json"], key="ja_json")
if json_file:
    data = json_parser.load_json_data(json_file)
    tables = json_parser.extract_json_tables(data)
    if tables:
        selected_table = st.selectbox("Select Table", list(tables.keys()), key="ja_table")
        table_data = tables[selected_table]
        df = pd.DataFrame(table_data)
        st.subheader("Data Table")
        st.dataframe(df)

        # Checkbox: Ask user whether to flatten nested JSON columns.
        flatten = st.checkbox("Flatten nested JSON columns", value=True, key="ja_flatten")

        # If flattening is enabled, iterate through columns and flatten any JSON string columns.
        if flatten:
            new_flat_cols = []
            for col in list(df.columns):
                df, flat_cols = flatten_json_column(df, col)
                new_flat_cols.extend(flat_cols)
            st.write("Flattened columns:", new_flat_cols)

        # Use updated DataFrame columns for axis selection.
        available_columns = list(df.columns)
        x_axis = st.selectbox("Select X Axis (optional)", ["(none)"] + available_columns, key="ja_x")
        y_axis = st.selectbox("Select Y Axis (optional)", ["(none)"] + available_columns, key="ja_y")
        chart_type = st.radio("Chart Type",
                              ["Line Chart", "Bar Chart", "Scatter Chart", "Area Chart",
                               "Box Plot", "Histogram", "Violin Plot", "Pie Chart"],
                              key="ja_chart")

        if x_axis != "(none)" and y_axis != "(none)":
            chart_df = df[[x_axis, y_axis]].dropna().copy()
            # If x-axis appears to be a timestamp and is numeric, convert it.
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                try:
                    unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                    chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)
                except Exception as e:
                    st.error(f"Timestamp conversion failed: {e}")
            fig = chart_utils.build_plotly_chart(chart_df, x_axis, y_axis, chart_type, options={})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select both X and Y axes to generate a chart.")
    else:
        st.error("No valid table found in the JSON file.")
