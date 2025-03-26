import streamlit as st
import pandas as pd
import altair as alt
from visualizer.utils import csv_parser, chart_utils

st.title("CSV Files Comparison")

# Upload two CSV files (auto-detect delimiter)
csv_file1 = st.file_uploader("Upload CSV File 1", type=["csv"], key="cc_csv1")
csv_file2 = st.file_uploader("Upload CSV File 2", type=["csv"], key="cc_csv2")

if csv_file1 and csv_file2:
    df1 = csv_parser.auto_read_csv(csv_file1)
    df2 = csv_parser.auto_read_csv(csv_file2)

    st.subheader("File 1 Data")
    st.dataframe(df1)
    st.subheader("File 2 Data")
    st.dataframe(df2)

    # Find common columns.
    common_cols = sorted(list(set(df1.columns).intersection(set(df2.columns))))
    if not common_cols:
        st.error("No common columns found between the two CSV files.")
    else:
        x_axis = st.selectbox("Select X Axis (optional)", [
                              "(none)"] + common_cols, key="cc_x")
        y_axis = st.selectbox("Select Y Axis (optional)", [
                              "(none)"] + common_cols, key="cc_y")
        chart_type = st.radio(
            "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="cc_chart")

        if st.button("Generate Comparison Chart", key="cc_generate"):
            if x_axis != "(none)" and y_axis != "(none)":
                df1_chart = df1[[x_axis, y_axis]].dropna().copy()
                df1_chart["File"] = "File 1"
                df2_chart = df2[[x_axis, y_axis]].dropna().copy()
                df2_chart["File"] = "File 2"

                chart_df = pd.concat([df1_chart, df2_chart], ignore_index=True)

                if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                    unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                    chart_df[x_axis] = pd.to_datetime(
                        chart_df[x_axis], unit=unit)

                options = {}
                if chart_type == "Line":
                    options["show_markers"] = st.checkbox(
                        "Show Markers", value=True, key="cc_show_markers")

                chart = chart_utils.build_comparison_chart(
                    chart_df, x_axis, y_axis, chart_type, options)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Axes selection is optional.")
