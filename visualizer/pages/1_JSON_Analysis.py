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
        chart_type = st.radio("Chart Type",
                              ["Line Chart", "Bar Chart", "Scatter Chart", "Area Chart",
                               "Box Plot", "Histogram", "Violin Plot", "Pie Chart"],
                              key="ja_chart")

        # Additional chart options based on chart type.
        options = {}
        if chart_type == "Line Chart":
            options["show_markers"] = st.checkbox(
                "Show Markers", value=True, key="ja_marker")
            options["smooth_lines"] = st.checkbox(
                "Smooth Lines (spline)", value=False, key="ja_smooth")
            options["fill_area"] = st.checkbox(
                "Fill Area", value=False, key="ja_fill")
        elif chart_type == "Bar Chart":
            options["barmode"] = st.radio(
                "Bar Mode", ["group", "stack"], index=0, key="ja_barmode")
        elif chart_type == "Scatter Chart":
            options["show_markers"] = st.checkbox(
                "Show Markers", value=True, key="ja_scatter_marker")
        elif chart_type == "Area Chart":
            options["smooth_lines"] = st.checkbox(
                "Smooth Lines (spline)", value=False, key="ja_area_smooth")
        elif chart_type == "Box Plot":
            options["notched"] = st.checkbox(
                "Notched", value=False, key="ja_notched")
            options["points"] = st.radio(
                "Show Points", ["all", "outliers", "none"], index=1, key="ja_box_points")
        elif chart_type == "Histogram":
            options["histnorm"] = st.radio("Normalization", [
                                           "count", "percent", "density", "probability"], index=0, key="ja_histnorm")
        elif chart_type == "Violin Plot":
            options["box"] = st.checkbox(
                "Show Box", value=True, key="ja_violin_box")
            options["points"] = st.radio(
                "Show Points", ["all", "outliers", "none"], index=1, key="ja_violin_points")
            options["meanline"] = st.checkbox(
                "Show Mean Line", value=False, key="ja_violin_mean")
        elif chart_type == "Pie Chart":
            options["donut"] = st.slider(
                "Donut Hole Size", 0.0, 1.0, 0.0, step=0.1, key="ja_donut")

        # Auto-generate chart if both axes are selected.
        if x_axis != "(none)" and y_axis != "(none)":
            chart_df = df[[x_axis, y_axis]].dropna().copy()
            # If x-axis appears to be a timestamp and is numeric, convert it.
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                try:
                    unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                    chart_df[x_axis] = pd.to_datetime(
                        chart_df[x_axis], unit=unit)
                except Exception as e:
                    st.error(f"Timestamp conversion failed: {e}")
            # Build the chart using Plotly Express via chart_utils.
            fig = chart_utils.build_plotly_chart(
                chart_df, x_axis, y_axis, chart_type, options)
            # For Line Charts with Fill Area selected, update the traces to fill the area.
            if chart_type == "Line Chart" and options.get("fill_area", False):
                fig.update_traces(fill="tozeroy")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select both X and Y axes to generate a chart.")
    else:
        st.error("No valid table found in the JSON file.")
