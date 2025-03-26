import streamlit as st
import pandas as pd
import altair as alt
from visualizer.utils import csv_parser, chart_utils

st.title("CSV File Analysis")

csv_file = st.file_uploader("Upload a CSV File", type=["csv"], key="ca_csv")
if csv_file:
    df = csv_parser.auto_read_csv(csv_file)
    st.subheader("Data Table")
    st.dataframe(df)
    columns = list(df.columns)
    x_axis = st.selectbox("Select X Axis (optional)", [
                          "(none)"] + columns, key="ca_x")
    y_axis = st.selectbox("Select Y Axis (optional)", [
                          "(none)"] + columns, key="ca_y")
    chart_type = st.radio(
        "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="ca_chart")
    if st.button("Generate Chart", key="ca_generate"):
        if x_axis != "(none)" and y_axis != "(none)":
            chart_df = df[[x_axis, y_axis]].dropna().copy()
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)
            chart = chart_utils.build_chart(
                chart_df, x_axis, y_axis, chart_type, options={})
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Axes selection is optional.")
