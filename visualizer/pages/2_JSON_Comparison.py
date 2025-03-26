import streamlit as st
import pandas as pd
import altair as alt
from visualizer.utils import json_parser, chart_utils

st.title("JSON Files Comparison")

json_file1 = st.file_uploader("Upload JSON File 1", type=[
                              "json"], key="jc_json1")
json_file2 = st.file_uploader("Upload JSON File 2", type=[
                              "json"], key="jc_json2")

if json_file1 and json_file2:
    data1 = json_parser.load_json_data(json_file1)
    data2 = json_parser.load_json_data(json_file2)
    tables1 = json_parser.extract_json_tables(data1)
    tables2 = json_parser.extract_json_tables(data2)
    # For comparison, ignore schema matching; use the tables from file1.
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

    columns = json_parser.extract_json_columns(table_data1)
    x_axis = st.selectbox("Select X Axis (optional)", [
                          "(none)"] + columns, key="jc_x")
    y_axis = st.selectbox("Select Y Axis (optional)", [
                          "(none)"] + columns, key="jc_y")
    chart_type = st.radio(
        "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="jc_chart")
    if st.button("Generate Comparison Chart", key="jc_generate"):
        if x_axis != "(none)" and y_axis != "(none)":
            df1_chart = pd.DataFrame(table_data1)[
                [x_axis, y_axis]].dropna().copy()
            df2_chart = pd.DataFrame(table_data2)[[x_axis, y_axis]].dropna(
            ).copy() if table_data2 else pd.DataFrame()
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(df1_chart[x_axis]):
                unit = "ms" if df1_chart[x_axis].iloc[0] > 1e10 else "s"
                df1_chart[x_axis] = pd.to_datetime(
                    df1_chart[x_axis], unit=unit)
                if not df2_chart.empty:
                    df2_chart[x_axis] = pd.to_datetime(
                        df2_chart[x_axis], unit=unit)
            # Overlay two Altair charts.
            chart1 = alt.Chart(df1_chart).mark_line(point=True).encode(
                x=alt.X(x_axis, title=f"{x_axis} (File 1)"),
                y=alt.Y(y_axis, title=y_axis),
                color=alt.value("blue")
            )
            if not df2_chart.empty:
                chart2 = alt.Chart(df2_chart).mark_line(point=True).encode(
                    x=alt.X(x_axis, title=f"{x_axis} (File 2)"),
                    y=alt.Y(y_axis, title=y_axis),
                    color=alt.value("red")
                )
                chart = alt.layer(chart1, chart2).properties(
                    title=f"Comparison of {y_axis} by {x_axis}"
                ).interactive()
            else:
                chart = chart1.properties(
                    title=f"File 1: {y_axis} by {x_axis}").interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Axes selection is optional.")
