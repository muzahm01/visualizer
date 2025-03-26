import streamlit as st
import pandas as pd
from visualizer.utils import csv_parser, chart_utils

st.title("CSV File Analysis")

# Upload one CSV file (auto-detect delimiter).
csv_file = st.file_uploader("Upload a CSV File", type=["csv"], key="ca_csv")
if csv_file:
    df = csv_parser.auto_read_csv(csv_file)
    st.subheader("Data Table")
    st.dataframe(df)

    # Get list of columns.
    columns = list(df.columns)
    x_axis = st.selectbox("Select X Axis (optional)", [
                          "(none)"] + columns, key="ca_x")
    y_axis = st.selectbox("Select Y Axis (optional)", [
                          "(none)"] + columns, key="ca_y")
    chart_type = st.radio("Chart Type",
                          ["Line Chart", "Bar Chart", "Scatter Chart", "Area Chart",
                           "Box Plot", "Histogram", "Violin Plot", "Pie Chart"],
                          key="ca_chart")

    if x_axis != "(none)" and y_axis != "(none)":
        chart_df = df[[x_axis, y_axis]].dropna().copy()
        # If the x-axis appears to be a timestamp and its values are numeric, convert it.
        if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
            try:
                unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)
            except Exception as e:
                st.error(f"Timestamp conversion failed: {e}")
        fig = chart_utils.build_plotly_chart(
            chart_df, x_axis, y_axis, chart_type, options={})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select both X and Y axes to generate a chart.")
