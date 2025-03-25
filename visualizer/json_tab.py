import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from visualizer.utils import json_parser, graph_utils


def render_json_tab():
    st.header("JSON Files")
    col_left, col_center, col_right = st.columns(3)

    # Left Column: Chart Options.
    with col_left:
        st.subheader("Chart Options")
        json_graph_type = st.radio(
            "Graph Type", ["Line Chart", "Bar Chart", "Pie Chart"], key="json_graph_type")
        json_options = {}
        if json_graph_type in ["Line Chart", "Bar Chart"]:
            if json_graph_type == "Line Chart":
                json_options["show_markers"] = st.checkbox(
                    "Show Markers", value=True, key="json_show_markers")
                json_options["show_lines"] = st.checkbox(
                    "Show Lines", value=True, key="json_show_lines")
                json_options["smooth_lines"] = st.checkbox(
                    "Smooth Lines (spline)", value=False, key="json_smooth_lines")
                json_options["fill_area"] = st.checkbox(
                    "Fill Area", value=False, key="json_fill_area")
            json_options["show_grid"] = st.checkbox(
                "Show Grid", value=True, key="json_show_grid")
            json_options["log_x"] = st.checkbox(
                "Log Scale X", value=False, key="json_log_x")
            json_options["log_y"] = st.checkbox(
                "Log Scale Y", value=False, key="json_log_y")
            json_options["show_legend"] = st.checkbox(
                "Show Legend", value=True, key="json_show_legend")

    # Center Column: File Uploaders & Output.
    with col_center:
        st.subheader("Upload Files & Output")
        json_file1 = st.file_uploader("Upload JSON File 1", type=[
                                      "json"], key="json_file1")
        json_file2 = st.file_uploader("Upload JSON File 2", type=[
                                      "json"], key="json_file2")
        json_output_placeholder = st.empty()

    # Right Column: Axis Selection.
    with col_right:
        st.subheader("Axis Selection")
        if json_file1 and json_file2:
            json1 = json_parser.load_json_data(json_file1)
            json2 = json_parser.load_json_data(json_file2)
            tables1 = json_parser.extract_json_tables(json1)
            tables2 = json_parser.extract_json_tables(json2)
            common_tables = sorted(
                list(set(tables1.keys()).intersection(set(tables2.keys()))))
            selected_table = st.selectbox(
                "Select Table", common_tables, key="json_table")
            table_data1 = tables1[selected_table]
            table_data2 = tables2[selected_table]
            json_columns = json_parser.extract_json_columns(table_data1)
            if json_columns:
                col_options = []
                mapping = {}
                for col in json_columns:
                    col_type, extra = json_parser.infer_col_info(
                        table_data1, col)
                    disp = f"{col} ({col_type}{', ' + extra if extra else ''})"
                    col_options.append(disp)
                    mapping[disp] = col
                json_x_axis_disp = st.selectbox(
                    "Select X Axis", col_options, key="json_x_axis")
                json_y_axis_disp = st.selectbox(
                    "Select Y Axis", col_options, key="json_y_axis")
            else:
                st.error("No columns found in the selected table.")

    # Render graph and data table.
    if json_file1 and json_file2 and selected_table and json_columns and json_x_axis_disp and json_y_axis_disp:
        x_axis_col = mapping[json_x_axis_disp]
        y_axis_col = mapping[json_y_axis_disp]

        def get_type(data, col):
            for row in data:
                if col in row and row[col] is not None:
                    if isinstance(row[col], (int, float)):
                        return "numeric"
                    elif isinstance(row[col], str):
                        return "string"
                    else:
                        return type(row[col]).__name__
            return "unknown"

        x_type = get_type(table_data1, x_axis_col)
        if x_type == "numeric":
            x_data1 = json_parser.get_numeric_data(table_data1, x_axis_col)
            x_data2 = json_parser.get_numeric_data(table_data2, x_axis_col)
            if "timestamp" in x_axis_col.lower() and isinstance(x_data1[0], (int, float)):
                try:
                    unit = "ms" if x_data1[0] > 1e10 else "s"
                    x_data1 = pd.to_datetime(x_data1, unit=unit)
                    x_data2 = pd.to_datetime(x_data2, unit=unit)
                except Exception as e:
                    st.error(f"Timestamp conversion failed: {e}")
        else:
            x_data1 = list(range(len(table_data1)))
            x_data2 = list(range(len(table_data2)))

        y_data1 = json_parser.get_numeric_data(table_data1, y_axis_col)
        y_data2 = json_parser.get_numeric_data(table_data2, y_axis_col)

        # Build graph: add two traces (one per file)
        fig = go.Figure()
        if json_graph_type == "Line Chart":
            if json_options.get("show_markers") and json_options.get("show_lines"):
                mode = "lines+markers"
            elif json_options.get("show_markers"):
                mode = "markers"
            elif json_options.get("show_lines"):
                mode = "lines"
            else:
                mode = "lines"
            line_shape = "spline" if json_options.get(
                "smooth_lines") else "linear"
            fill_val = "tozeroy" if json_options.get("fill_area") else None
            fig.add_trace(go.Scatter(
                x=x_data1, y=y_data1, mode=mode, name=f"{y_axis_col} - File 1",
                line=dict(shape=line_shape), marker=dict(opacity=0.8), fill=fill_val
            ))
            fig.add_trace(go.Scatter(
                x=x_data2, y=y_data2, mode=mode, name=f"{y_axis_col} - File 2",
                line=dict(shape=line_shape), marker=dict(opacity=0.8), fill=fill_val
            ))
        elif json_graph_type == "Bar Chart":
            fig.add_trace(go.Bar(
                x=x_data1, y=y_data1, name=f"{y_axis_col} - File 1"
            ))
            fig.add_trace(go.Bar(
                x=x_data2, y=y_data2, name=f"{y_axis_col} - File 2"
            ))
        elif json_graph_type == "Pie Chart":
            fig1 = go.Figure(go.Pie(
                labels=[str(x) for x in x_data1],
                values=y_data1,
                name="File 1",
                hole=0.3
            ))
            fig2 = go.Figure(go.Pie(
                labels=[str(x) for x in x_data2],
                values=y_data2,
                name="File 2",
                hole=0.3
            ))
            json_output_placeholder.write("#### File 1 - Pie Chart")
            json_output_placeholder.plotly_chart(
                fig1, use_container_width=True)
            json_output_placeholder.write("#### File 2 - Pie Chart")
            json_output_placeholder.plotly_chart(
                fig2, use_container_width=True)
            fig = None

        if fig is not None:
            if pd.api.types.is_datetime64_any_dtype(x_data1):
                fig.update_xaxes(type="date")
            else:
                fig.update_xaxes(type="log" if json_options.get(
                    "log_x") else "linear", showgrid=json_options.get("show_grid"))
            fig.update_yaxes(type="log" if json_options.get(
                "log_y") else "linear", showgrid=json_options.get("show_grid"))
            fig.update_layout(title=f"{json_graph_type} for Table '{selected_table}'<br>X: {x_axis_col} & Y: {y_axis_col}",
                              showlegend=json_options.get("show_legend"))
            json_output_placeholder.plotly_chart(fig, use_container_width=True)

        # Data Table
        if pd.api.types.is_datetime64_any_dtype(x_data1):
            if isinstance(x_data1, pd.DatetimeIndex):
                x_disp1 = x_data1.strftime('%Y-%m-%d %H:%M:%S').tolist()
                x_disp2 = x_data2.strftime('%Y-%m-%d %H:%M:%S').tolist()
            else:
                x_disp1 = x_data1.dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
                x_disp2 = x_data2.dt.strftime('%Y-%m-%d %H:%M:%S').tolist()


        else:
            x_disp1 = x_data1
            x_disp2 = x_data2

        # For Y axis, use safe_convert so that non-numeric values are preserved.
        df1 = pd.DataFrame({x_axis_col: x_disp1})
        df1[y_axis_col] = [safe_convert(row.get(y_axis_col, 0)) for row in table_data1]

        df2 = pd.DataFrame({x_axis_col: x_disp2})
        df2[y_axis_col] = [safe_convert(row.get(y_axis_col, 0)) for row in table_data2]

        max_rows = max(len(df1), len(df2))
        df1 = df1.reindex(range(max_rows))
        df2 = df2.reindex(range(max_rows))
        df_combined = pd.concat(
            [df1.add_prefix("File 1 - "), df2.add_prefix("File 2 - ")], axis=1)
        st.write("### Data Table")
        st.dataframe(df_combined)


def safe_convert(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return val
