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

    # Show additional options based on chart type.
    options = {}
    if chart_type == "Line Chart":
        options["show_markers"] = st.checkbox(
            "Show Markers", value=True, key="ca_marker")
        options["smooth_lines"] = st.checkbox(
            "Smooth Lines (spline)", value=False, key="ca_smooth")
        options["fill_area"] = st.checkbox(
            "Fill Area", value=False, key="ca_fill")
    elif chart_type == "Bar Chart":
        options["barmode"] = st.radio(
            "Bar Mode", ["group", "stack"], index=0, key="ca_barmode")
    elif chart_type == "Scatter Chart":
        options["show_markers"] = st.checkbox(
            "Show Markers", value=True, key="ca_scatter_marker")
        options["opacity"] = st.slider(
            "Opacity", 0.0, 1.0, 0.8, key="ca_opacity")
    elif chart_type == "Area Chart":
        options["smooth_lines"] = st.checkbox(
            "Smooth Lines (spline)", value=False, key="ca_area_smooth")
    elif chart_type == "Box Plot":
        options["notched"] = st.checkbox(
            "Notched", value=False, key="ca_notched")
        options["points"] = st.radio(
            "Show Points", ["all", "outliers", "none"], index=1, key="ca_box_points")
    elif chart_type == "Histogram":
        options["histnorm"] = st.radio("Normalization",
                                       ["count", "percent", "probability",
                                           "density", "probability density"],
                                       index=0, key="ca_histnorm")
    elif chart_type == "Violin Plot":
        options["box"] = st.checkbox(
            "Show Box", value=True, key="ca_violin_box")
        options["points"] = st.radio(
            "Show Points", ["all", "outliers", "none"], index=1, key="ca_violin_points")
        options["meanline"] = st.checkbox(
            "Show Mean Line", value=False, key="ca_violin_mean")
    elif chart_type == "Pie Chart":
        options["donut"] = st.slider(
            "Donut Hole Size", 0.0, 1.0, 0.0, step=0.1, key="ca_donut")

    # Auto-generate chart if both axes are selected.
    if x_axis != "(none)" and y_axis != "(none)":
        chart_df = df[[x_axis, y_axis]].dropna().copy()
        # If x-axis appears to be a timestamp and its values are numeric, convert it.
        if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
            try:
                unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)
            except Exception as e:
                st.error(f"Timestamp conversion failed: {e}")
        fig = chart_utils.build_plotly_chart(
            chart_df, x_axis, y_axis, chart_type, options)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select both X and Y axes to generate a chart.")
