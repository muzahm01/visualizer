import streamlit as st
import pandas as pd
from visualizer.utils import json_parser, chart_utils

st.title("JSON Files Comparison")

# Upload two JSON files.
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
        "Select Table", list(tables1.keys()), key="jc_table")
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
    chart_type = st.radio("Chart Type",
                          ["Line Chart", "Bar Chart", "Scatter Chart",
                           "Area Chart", "Box Plot", "Histogram", "Violin Plot", "Pie Chart"],
                          key="jc_chart")

    # Additional options based on chart type.
    options = {}
    if chart_type == "Line Chart":
        options["show_markers"] = st.checkbox(
            "Show Markers", value=True, key="jc_show_markers")
        options["smooth_lines"] = st.checkbox(
            "Smooth Lines (spline)", value=False, key="jc_smooth")
        options["fill_area"] = st.checkbox(
            "Fill Area", value=False, key="jc_fill")
    elif chart_type == "Bar Chart":
        options["barmode"] = st.radio(
            "Bar Mode", ["group", "stack"], index=0, key="jc_barmode")
    elif chart_type == "Scatter Chart":
        options["show_markers"] = st.checkbox(
            "Show Markers", value=True, key="jc_scatter_marker")
        options["opacity"] = st.slider(
            "Opacity", 0.0, 1.0, 0.8, key="jc_opacity")
    elif chart_type == "Area Chart":
        options["smooth_lines"] = st.checkbox(
            "Smooth Lines (spline)", value=False, key="jc_area_smooth")
    elif chart_type == "Box Plot":
        options["notched"] = st.checkbox(
            "Notched", value=False, key="jc_notched")
        options["points"] = st.radio(
            "Show Points", ["all", "outliers", "none"], index=1, key="jc_box_points")
    elif chart_type == "Histogram":
        options["histnorm"] = st.radio("Normalization", ["", "percent", "probability", "density", "probability density"],
                                       index=0, key="jc_histnorm")
    elif chart_type == "Violin Plot":
        options["box"] = st.checkbox(
            "Show Box", value=True, key="jc_violin_box")
        options["points"] = st.radio(
            "Show Points", ["all", "outliers", "none"], index=1, key="jc_violin_points")
        options["meanline"] = st.checkbox(
            "Show Mean Line", value=False, key="jc_violin_mean")
    elif chart_type == "Pie Chart":
        options["donut"] = st.slider(
            "Donut Hole Size", 0.0, 1.0, 0.0, step=0.1, key="jc_donut")

    # Auto-generate chart if both axes are selected.
    if x_axis != "(none)" and y_axis != "(none)":
        # Build DataFrames and add a "File" column.
        df1_chart = pd.DataFrame(table_data1)[[x_axis, y_axis]].dropna().copy()
        df1_chart["File"] = "File 1"
        df2_chart = pd.DataFrame(table_data2)[[x_axis, y_axis]].dropna(
        ).copy() if table_data2 else pd.DataFrame()
        if not df2_chart.empty:
            df2_chart["File"] = "File 2"
        chart_df = pd.concat([df1_chart, df2_chart], ignore_index=True)

        # Convert x-axis to datetime if its name suggests a timestamp.
        if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
            unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
            chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)

        if chart_type != "Pie Chart":
            fig = chart_utils.build_comparison_chart(
                chart_df, x_axis, y_axis, chart_type, options)
            st.plotly_chart(fig, use_container_width=True,
                            key="jc_chart_nonpie")
        else:
            # For Pie Chart, build separate charts for each file.
            fig1 = chart_utils.build_plotly_chart(
                df1_chart, x_axis, y_axis, "Pie Chart", options)
            fig2 = chart_utils.build_plotly_chart(
                df2_chart, x_axis, y_axis, "Pie Chart", options)
            st.write("#### File 1 - Pie Chart")
            st.plotly_chart(fig1, use_container_width=True,
                            key="jc_pie_chart1")
            st.write("#### File 2 - Pie Chart")
            st.plotly_chart(fig2, use_container_width=True,
                            key="jc_pie_chart2")

        st.subheader("Combined Data Table")
        st.dataframe(chart_df)
    else:
        st.info("Please select both X and Y axes to generate a chart.")
