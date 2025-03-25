import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from visualizer.utils import csv_parser, graph_utils


def render_csv_tab():
    st.header("CSV Files")
    col_left, col_center, col_right = st.columns(3)

    with col_left:
        st.subheader("Chart Options")
        csv_graph_type = st.radio(
            "Graph Type", ["Line Chart", "Bar Chart", "Pie Chart"], key="csv_graph_type")
        csv_options = {}
        if csv_graph_type in ["Line Chart", "Bar Chart"]:
            if csv_graph_type == "Line Chart":
                csv_options["show_markers"] = st.checkbox(
                    "Show Markers", value=True, key="csv_show_markers")
                csv_options["show_lines"] = st.checkbox(
                    "Show Lines", value=True, key="csv_show_lines")
                csv_options["smooth_lines"] = st.checkbox(
                    "Smooth Lines (spline)", value=False, key="csv_smooth_lines")
                csv_options["fill_area"] = st.checkbox(
                    "Fill Area", value=False, key="csv_fill_area")
            csv_options["show_grid"] = st.checkbox(
                "Show Grid", value=True, key="csv_show_grid")
            csv_options["log_x"] = st.checkbox(
                "Log Scale X", value=False, key="csv_log_x")
            csv_options["log_y"] = st.checkbox(
                "Log Scale Y", value=False, key="csv_log_y")
            csv_options["show_legend"] = st.checkbox(
                "Show Legend", value=True, key="csv_show_legend")
        else:
            st.info("No extra options for Pie Chart.")

    with col_center:
        st.subheader("Upload Files")
        csv_file1 = st.file_uploader("Upload CSV File 1", type=[
                                     "csv"], key="csv_file1")
        csv_file2 = st.file_uploader("Upload CSV File 2", type=[
                                     "csv"], key="csv_file2")
        csv_output_placeholder = st.empty()

    with col_right:
        st.subheader("Axis Selection")
        if csv_file1 and csv_file2:
            # Always use auto-detected delimiter.
            df_csv1 = csv_parser.auto_read_csv(csv_file1)
            df_csv2 = csv_parser.auto_read_csv(csv_file2)
            # Assume both CSVs have common columns.
            common_cols = sorted(
                list(set(df_csv1.columns).intersection(set(df_csv2.columns))))
            csv_x_axis = st.selectbox(
                "Select X Axis", common_cols, key="csv_x_axis")
            csv_y_axis = st.selectbox(
                "Select Y Axis", common_cols, key="csv_y_axis")

    if csv_file1 and csv_file2 and csv_x_axis and csv_y_axis:
        df1 = df_csv1.copy()
        df2 = df_csv2.copy()
        x_data_csv1 = df1[csv_x_axis]
        x_data_csv2 = df2[csv_x_axis]
        # If x-axis column appears to be a timestamp, convert it.
        if "timestamp" in csv_x_axis.lower() and pd.api.types.is_numeric_dtype(x_data_csv1):
            try:
                unit = "ms" if x_data_csv1.iloc[0] > 1e10 else "s"
                x_data_csv1 = pd.to_datetime(x_data_csv1, unit=unit)
                x_data_csv2 = pd.to_datetime(x_data_csv2, unit=unit)
            except Exception as e:
                st.error(f"Timestamp conversion failed: {e}")
        # For a line or bar chart, we need to pass x-data as a tuple for File 1 and File 2.
        # Y-axis selection is now a single string.
        y_data_csv1 = pd.to_numeric(
            df1[csv_y_axis], errors='coerce').fillna(0).tolist()
        y_data_csv2 = pd.to_numeric(
            df2[csv_y_axis], errors='coerce').fillna(0).tolist()
        x_tuple = (x_data_csv1, x_data_csv2)
        y_tuple = (y_data_csv1, y_data_csv2)
        y_label = csv_y_axis  # Single Y axis label

        if csv_graph_type in ["Line Chart", "Bar Chart"]:
            fig_csv = graph_utils.build_graph(x_tuple, y_tuple, csv_x_axis, [
                                              y_label], csv_graph_type, csv_options)
            if pd.api.types.is_datetime64_any_dtype(x_data_csv1):
                fig_csv.update_xaxes(type="date")
            csv_output_placeholder.plotly_chart(
                fig_csv, use_container_width=True)
        elif csv_graph_type == "Pie Chart":
            # For Pie Chart, we'll generate separate pie charts for each file.
            fig_csv1 = go.Figure(go.Pie(
                labels=[str(x) for x in x_data_csv1],
                values=y_data_csv1,
                name="File 1",
                hole=0.3
            ))
            fig_csv2 = go.Figure(go.Pie(
                labels=[str(x) for x in x_data_csv2],
                values=y_data_csv2,
                name="File 2",
                hole=0.3
            ))
            csv_output_placeholder.write("#### File 1 - Pie Chart")
            csv_output_placeholder.plotly_chart(
                fig_csv1, use_container_width=True)
            csv_output_placeholder.write("#### File 2 - Pie Chart")
            csv_output_placeholder.plotly_chart(
                fig_csv2, use_container_width=True)

        # Prepare display for the data table.
        if pd.api.types.is_datetime64_any_dtype(x_data_csv1):
            if isinstance(x_data_csv1, pd.DatetimeIndex):
                x_disp_csv1 = x_data_csv1.strftime(
                    '%Y-%m-%d %H:%M:%S').tolist()
                x_disp_csv2 = x_data_csv2.strftime(
                    '%Y-%m-%d %H:%M:%S').tolist()
            else:
                x_disp_csv1 = x_data_csv1.dt.strftime(
                    '%Y-%m-%d %H:%M:%S').tolist()
                x_disp_csv2 = x_data_csv2.dt.strftime(
                    '%Y-%m-%d %H:%M:%S').tolist()
        else:
            x_disp_csv1 = x_data_csv1.tolist() if hasattr(
                x_data_csv1, "tolist") else x_data_csv1
            x_disp_csv2 = x_data_csv2.tolist() if hasattr(
                x_data_csv2, "tolist") else x_data_csv2

        df_csv1_display = pd.DataFrame({csv_x_axis: x_disp_csv1})
        df_csv1_display[csv_y_axis] = pd.to_numeric(
            df1[csv_y_axis], errors='coerce').fillna(0)
        df_csv2_display = pd.DataFrame({csv_x_axis: x_disp_csv2})
        df_csv2_display[csv_y_axis] = pd.to_numeric(
            df2[csv_y_axis], errors='coerce').fillna(0)
        max_rows_csv = max(len(df_csv1_display), len(df_csv2_display))
        df_csv1_display = df_csv1_display.reindex(range(max_rows_csv))
        df_csv2_display = df_csv2_display.reindex(range(max_rows_csv))
        df_csv_combined = pd.concat([df_csv1_display.add_prefix(
            "File 1 - "), df_csv2_display.add_prefix("File 2 - ")], axis=1)
        st.write("### Data Table")
        st.dataframe(df_csv_combined)
