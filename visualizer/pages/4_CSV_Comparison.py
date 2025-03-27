import streamlit as st
import pandas as pd
from visualizer.utils import csv_parser, chart_utils

st.title("CSV Files Comparison")

# Upload two CSV files (auto-detect delimiter)
csv_file1 = st.file_uploader("Upload CSV File 1", type=["csv"], key="cc_csv1")
csv_file2 = st.file_uploader("Upload CSV File 2", type=["csv"], key="cc_csv2")

if csv_file1 and csv_file2:
    # Auto-detect delimiter and load CSV files.
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
        x_axis = st.selectbox("Select X Axis (optional)", ["(none)"] + common_cols, key="cc_x")
        y_axis = st.selectbox("Select Y Axis (optional)", ["(none)"] + common_cols, key="cc_y")
        chart_type = st.radio("Chart Type",
                              ["Line Chart", "Bar Chart", "Scatter Chart",
                               "Area Chart", "Box Plot", "Histogram", "Violin Plot", "Pie Chart"],
                              key="cc_chart")

        # Additional chart options.
        options = {}
        if chart_type == "Line Chart":
            options["show_markers"] = st.checkbox("Show Markers", value=True, key="cc_show_markers")
            options["smooth_lines"] = st.checkbox("Smooth Lines (spline)", value=False, key="cc_smooth")
            options["fill_area"] = st.checkbox("Fill Area", value=False, key="cc_fill")
        elif chart_type == "Bar Chart":
            options["barmode"] = st.radio("Bar Mode", ["group", "stack"], index=0, key="cc_barmode")
        elif chart_type == "Scatter Chart":
            options["show_markers"] = st.checkbox("Show Markers", value=True, key="cc_scatter_marker")
            options["opacity"] = st.slider("Opacity", 0.0, 1.0, 0.8, key="cc_opacity")
        elif chart_type == "Area Chart":
            options["smooth_lines"] = st.checkbox("Smooth Lines (spline)", value=False, key="cc_area_smooth")
        elif chart_type == "Box Plot":
            options["notched"] = st.checkbox("Notched", value=False, key="cc_notched")
            options["points"] = st.radio("Show Points", ["all", "outliers", "none"], index=1, key="cc_box_points")
        elif chart_type == "Histogram":
            options["histnorm"] = st.radio("Normalization",
                                           ["count", "percent", "probability", "density", "probability density"],
                                           index=0, key="cc_histnorm")
        elif chart_type == "Violin Plot":
            options["box"] = st.checkbox("Show Box", value=True, key="cc_violin_box")
            options["points"] = st.radio("Show Points", ["all", "outliers", "none"], index=1, key="cc_violin_points")
            options["meanline"] = st.checkbox("Show Mean Line", value=False, key="cc_violin_mean")
        elif chart_type == "Pie Chart":
            options["donut"] = st.slider("Donut Hole Size", 0.0, 1.0, 0.0, step=0.1, key="cc_donut")

        # Auto-generate chart if both axes are selected.
        if x_axis != "(none)" and y_axis != "(none)":
            # Build individual DataFrames and tag them with file names.
            df1_chart = df1[[x_axis, y_axis]].dropna().copy()
            df1_chart["File"] = "File 1"
            df2_chart = df2[[x_axis, y_axis]].dropna().copy()
            df2_chart["File"] = "File 2"
            # Combine the DataFrames for comparison.
            chart_df = pd.concat([df1_chart, df2_chart], ignore_index=True)

            # Convert x-axis to datetime if its name suggests a timestamp.
            if "timestamp" in x_axis.lower() and pd.api.types.is_numeric_dtype(chart_df[x_axis]):
                unit = "ms" if chart_df[x_axis].iloc[0] > 1e10 else "s"
                chart_df[x_axis] = pd.to_datetime(chart_df[x_axis], unit=unit)

            if chart_type != "Pie Chart":
                fig = chart_utils.build_comparison_chart(chart_df, x_axis, y_axis, chart_type, options)
                st.plotly_chart(fig, use_container_width=True, key="cc_chart_nonpie")
            else:
                fig1 = chart_utils.build_plotly_chart(df1_chart, x_axis, y_axis, "Pie Chart", options)
                fig2 = chart_utils.build_plotly_chart(df2_chart, x_axis, y_axis, "Pie Chart", options)
                st.write("#### File 1 - Pie Chart")
                st.plotly_chart(fig1, use_container_width=True, key="cc_pie_chart1")
                st.write("#### File 2 - Pie Chart")
                st.plotly_chart(fig2, use_container_width=True, key="cc_pie_chart2")

            st.subheader("Combined Data Table")
            st.dataframe(chart_df)

            # Statistical Analysis Section.
            st.subheader("Statistical Analysis")
            # Identify numeric columns from each file.
            numeric_cols_file1 = [col for col in df1.columns if pd.api.types.is_numeric_dtype(df1[col])]
            numeric_cols_file2 = [col for col in df2.columns if pd.api.types.is_numeric_dtype(df2[col])]
            common_numeric_cols = sorted(list(set(numeric_cols_file1).intersection(set(numeric_cols_file2))))
            # Multiselect with empty default.
            selected_stats_cols = st.multiselect("Select numeric columns for analysis", common_numeric_cols, default=[],
                                                 key="cc_stats")
            if selected_stats_cols:
                stats_results = []
                for col in selected_stats_cols:
                    if col in df1.columns and col in df2.columns:
                        try:
                            comp_df = pd.concat([
                                df1[[col]].rename(columns={col: "File 1"}),
                                df2[[col]].rename(columns={col: "File 2"})
                            ], axis=1, join="inner").dropna()
                        except KeyError as e:
                            st.warning(f"Column {col} is missing in one of the files: {e}")
                            continue
                        if not comp_df.empty:
                            # Convert values to numeric.
                            actual = pd.to_numeric(comp_df["File 1"], errors="coerce")
                            forecast = pd.to_numeric(comp_df["File 2"], errors="coerce")
                            nonzero = actual != 0
                            mape = (abs((actual[nonzero] - forecast[nonzero]) / actual[
                                nonzero])).mean() * 100 if nonzero.sum() > 0 else None
                            mae = (abs(actual - forecast)).mean()
                            rmse = ((actual - forecast) ** 2).mean() ** 0.5
                            stats_results.append({
                                "Column": col,
                                "MAPE (%)": mape,
                                "MAE": mae,
                                "RMSE": rmse,
                                "Count": len(comp_df)
                            })
                if stats_results:
                    st.dataframe(pd.DataFrame(stats_results))
                else:
                    st.info("No overlapping numeric data found for statistical analysis.")
            else:
                st.info("No numeric columns selected for analysis.")
        else:
            st.info("Please select both X and Y axes to generate a chart.")
