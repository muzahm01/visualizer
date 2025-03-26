import plotly.express as px
import plotly.graph_objects as go


def build_plotly_chart(df, x_col, y_col, chart_type, options):
    """
    Build a Plotly Express chart for a single file.
    Supported chart types:
      - "Line Chart"
      - "Bar Chart"
      - "Scatter Chart"
      - "Area Chart"
      - "Box Plot"
      - "Histogram"
      - "Violin Plot"
      - "Pie Chart"
    """
    if chart_type == "Line Chart":
        line_shape = "spline" if options.get(
            "smooth_lines", False) else "linear"
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=options.get("show_markers", False),
            line_shape=line_shape,
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Bar Chart":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Scatter Chart":
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Area Chart":
        fig = px.area(
            df,
            x=x_col,
            y=y_col,
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Box Plot":
        fig = px.box(
            df,
            x=x_col,
            y=y_col,
            title=f"{chart_type}: {y_col} by {x_col}"
        )
    elif chart_type == "Histogram":
        fig = px.histogram(
            df,
            x=x_col,
            title=f"{chart_type}: {x_col} distribution"
        )
    elif chart_type == "Violin Plot":
        fig = px.violin(
            df,
            x=x_col,
            y=y_col,
            box=True,
            title=f"{chart_type}: {y_col} by {x_col}"
        )
    elif chart_type == "Pie Chart":
        fig = px.pie(
            df,
            names=x_col,
            values=y_col,
            title=f"{chart_type}: {y_col} by {x_col}"
        )
    else:
        # Default fallback to a line chart.
        line_shape = "spline" if options.get(
            "smooth_lines", False) else "linear"
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=options.get("show_markers", False),
            line_shape=line_shape,
            title=f"Line Chart: {y_col} vs {x_col}"
        )
    return fig


def build_comparison_chart(df, x_col, y_col, chart_type, options):
    """
    Build a comparison Plotly Express chart for two files.
    Expects `df` to have a "File" column that distinguishes the data.
    Supported chart types are similar to build_plotly_chart.
    """
    if chart_type == "Line Chart":
        line_shape = "spline" if options.get(
            "smooth_lines", False) else "linear"
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color="File",
            markers=options.get("show_markers", False),
            line_shape=line_shape,
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Bar Chart":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color="File",
            barmode="group",
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Scatter Chart":
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color="File",
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Area Chart":
        fig = px.area(
            df,
            x=x_col,
            y=y_col,
            color="File",
            title=f"{chart_type}: {y_col} vs {x_col}"
        )
    elif chart_type == "Box Plot":
        fig = px.box(
            df,
            x=x_col,
            y=y_col,
            color="File",
            title=f"{chart_type}: {y_col} by {x_col}"
        )
    elif chart_type == "Histogram":
        fig = px.histogram(
            df,
            x=x_col,
            color="File",
            barmode="overlay",
            title=f"{chart_type}: {x_col} distribution by File"
        )
    elif chart_type == "Violin Plot":
        fig = px.violin(
            df,
            x=x_col,
            y=y_col,
            color="File",
            box=True,
            title=f"{chart_type}: {y_col} by {x_col}"
        )
    elif chart_type == "Pie Chart":
        # For comparisons, it's common to generate separate pie charts.
        fig = None
    else:
        line_shape = "spline" if options.get(
            "smooth_lines", False) else "linear"
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color="File",
            markers=options.get("show_markers", False),
            line_shape=line_shape,
            title=f"Line Chart: {y_col} vs {x_col}"
        )

    # Update hover template for each trace if x and y data exist.
    if fig is not None:
        for trace in fig.data:
            if hasattr(trace, "x") and trace.x is not None and hasattr(trace, "y") and trace.y is not None:
                # Use double braces to create literal placeholders for Plotly.
                trace.hovertemplate = (
                    "File: %{customdata}<br>" +
                    f"{x_col}: %{{x}}<br>" +
                    f"{y_col}: %{{y}}<extra></extra>"
                )
                trace.customdata = [trace.name] * len(trace.x)
    return fig
