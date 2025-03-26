import streamlit as st
import pandas as pd
import altair as alt
from visualizer.utils import csv_parser, chart_utils

st.title("CSV Files Comparison")

csv_file1 = st.file_uploader("Upload CSV File 1", type=["csv"], key="cc_csv1")
csv_file2 = st.file_uploader("Upload CSV File 2", type=["csv"], key="cc_csv2")
if csv_file1 and csv_file2:
    df1 = csv_parser.auto_read_csv(csv_file1)
    df2 = csv_parser.auto_read_csv(csv_file2)
    st.subheader("File 1 Data")
    st.dataframe(df1)
    st.subheader("File 2 Data")
    st.dataframe(df2)

    common_cols = sorted(list(set(df1.columns).intersection(set(df2.columns))))
    if common_cols:
        x_axis = st.selectbox("Select X Axis (optional)", [
                              "(none)"] + common_cols, key="cc_x")
        y_axis = st.selectbox("Select Y Axis (optional)", [
                              "(none)"] + common_cols, key="cc_y")
        chart_type = st.radio(
            "Chart Type", ["Line", "Bar", "Area", "Scatter"], key="cc_chart")
        if st.button("Generate Comparison Chart", key="cc_generate"):
            if x_axis != "(none)" and y_axis != "(none)":
                df1_chart = df1[[x_axis, y_axis]].dropna().copy()
                df2_chart = df2[[x_axis, y_axis]].dropna().copy()
                if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(df1_chart[x_axis]):
                    unit = "ms" if df1_chart[x_axis].iloc[0] > 1e10 else "s"
                    df1_chart[x_axis] = pd.to_datetime(
                        df1_chart[x_axis], unit=unit)
                    df2_chart[x_axis] = pd.to_datetime(
                        df2_chart[x_axis], unit=unit)
                chart1 = alt.Chart(df1_chart).mark_line(point=True).encode(
                    x=alt.X(x_axis, title=f"{x_axis} (File 1)"),
                    y=alt.Y(y_axis, title=y_axis),
                    color=alt.value("blue")
                )
                chart2 = alt.Chart(df2_chart).mark_line(point=True).encode(
                    x=alt.X(x_axis, title=f"{x_axis} (File 2)"),
                    y=alt.Y(y_axis, title=y_axis),
                    color=alt.value("red")
                )
                chart = alt.layer(chart1, chart2).properties(
                    title=f"Comparison of {y_axis} by {x_axis}"
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Axes selection is optional.")
    else:
        st.error("No common columns found between the two CSV files.")
