import streamlit as st
import pandas as pd
import altair as alt
from visualizer.utils import json_parser, chart_utils

st.title("JSON Files Comparison")

# Upload two JSON files
json_file1 = st.file_uploader("Upload JSON File 1", type=[
                              "json"], key="jc_json1")
json_file2 = st.file_uploader("Upload JSON File 2", type=[
                              "json"], key="jc_json2")

if json_file1 and json_file2:
    data1 = json_parser.load_json_data(json_file1)
    data2 = json_parser.load_json_data(json_file2)

    tables1 = json_parser.extract_json_tables(data1)
    tables2 = json_parser.extract_json_tables(data2)

    selected_table = st.selectbox(
        "Select Table (from File 1)", list(tables1.keys()), key="jc_table")
    table_data1 = tables1[selected_table]
    table_data2 = tables2.get(selected_table, [])

    df1 = pd.DataFrame(table_data1)
    df2 = pd.DataFrame(table_data2) if table_data2 else pd.DataFrame()

    st.subheader("File 1 Data")
    st.dataframe(df1)
    st.subheader("File 2 Data")
    st.dataframe(df2)

    # Axis selection (optional)
    columns = json_parser.extract_json_columns(table_data1)
    x_axis = st.selectbox("Select X Axis (optional)", [
                          "(none)"] + columns, key="jc_x")
    y_axis = st.selectbox("Select Y Axis (optional)", [
                          "(none)"] + columns, key="jc_y")
    chart_type = st.radio(
        "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="jc_chart")

    if st.button("Generate Comparison Chart", key="jc_generate"):
        if x_axis != "(none)" and y_axis != "(none)":
            # Build separate DataFrames for each file and add a "File" column.
            df1_chart = pd.DataFrame(table_data1)[
                [x_axis, y_axis]].dropna().copy()
            df1_chart["File"] = "File 1"
            df2_chart = pd.DataFrame(table_data2)[[x_axis, y_axis]].dropna(
            ).copy() if table_data2 else pd.DataFrame()
            if not df2_chart.empty:
                df2_chart["File"] = "File 2"

            # Combine data from both files
            chart_df = pd.concat([df1_chart, df2_chart], ignore_index=True)

            # Convert x-axis if it appears numeric and contains "timestamp"
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)

            options = {}
            if chart_type == "Line":
                options["show_markers"] = st.checkbox(
                    "Show Markers", value=True, key="jc_show_markers")

            # Build the comparison chart using our updated function
            chart = chart_utils.build_comparison_chart(
                chart_df, x_axis, y_axis, chart_type, options)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Axes selection is optional.")
