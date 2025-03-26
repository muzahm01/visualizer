import streamlit as st
import pandas as pd
from visualizer.utils import json_parser, chart_utils

st.title("JSON File Analysis")

# Upload one JSON file.
json_file = st.file_uploader("Upload a JSON File", type=[
                             "json"], key="ja_json")
if json_file:
    data = json_parser.load_json_data(json_file)
    tables = json_parser.extract_json_tables(data)
    if tables:
        selected_table = st.selectbox(
            "Select Table", list(tables.keys()), key="ja_table")
        table_data = tables[selected_table]
        df = pd.DataFrame(table_data)
        st.subheader("Data Table")
        st.dataframe(df)

        # Optional axis selection.
        columns = json_parser.extract_json_columns(table_data)
        x_axis = st.selectbox("Select X Axis (optional)", [
                              "(none)"] + columns, key="ja_x")
        y_axis = st.selectbox("Select Y Axis (optional)", [
                              "(none)"] + columns, key="ja_y")
        chart_type = st.radio(
            "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="ja_chart")
        if st.button("Generate Chart", key="ja_generate"):
            if x_axis != "(none)" and y_axis != "(none)":
                chart_df = df[[x_axis, y_axis]].dropna().copy()
                # If x-axis seems like a timestamp and numeric, convert it.
                if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                    unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                    chart_df[x_axis] = pd.to_datetime(
                        chart_df[x_axis], unit=unit)
                chart = chart_utils.build_chart(
                    chart_df, x_axis, y_axis, chart_type, options={})
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No chart generated (axes selection is optional).")
    else:
        st.error("No valid table found in the JSON file.")
