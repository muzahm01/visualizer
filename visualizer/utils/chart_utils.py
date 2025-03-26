import altair as alt


def build_chart(df, x_col, y_col, chart_type, options):
    """
    Build an Altair chart from DataFrame `df` using x_col and y_col.
    chart_type: one of "Line", "Bar", "Area", "Scatter".
    options: a dict of additional options (e.g. show_markers).
    """
    base = alt.Chart(df).encode(
        x=alt.X(x_col, title=x_col),
        y=alt.Y(y_col, title=y_col)
    )

    if chart_type == "Line":
        chart = base.mark_line(point=options.get(
            "show_markers", False)).interactive()
    elif chart_type == "Bar":
        chart = base.mark_bar().interactive()
    elif chart_type == "Area":
        chart = base.mark_area().interactive()
    elif chart_type == "Scatter":
        chart = base.mark_point().interactive()
    else:
        chart = base
    return chart


def build_comparison_chart(df, x_col, y_col, chart_type, options):
    """
    Build a comparison Altair chart from DataFrame `df` that includes a "File" column.
    The chart encodes color based on the "File" column and adds a legend that is interactive,
    allowing users to select/deselect File 1 and File 2 traces.

    chart_type: one of "Line", "Bar", "Area", or "Scatter".
    options: a dict of additional options (e.g. show_markers).
    """
    # Create an interactive selection bound to the legend.
    legend_selection = alt.selection_multi(fields=["File"], bind="legend")

    base = alt.Chart(df).encode(
        x=alt.X(x_col, title=x_col),
        y=alt.Y(y_col, title=y_col),
        color=alt.Color("File:N", title="File")
    ).add_selection(
        legend_selection
    ).transform_filter(
        legend_selection
    )

    if chart_type == "Line":
        chart = base.mark_line(point=options.get(
            "show_markers", False)).interactive()
    elif chart_type == "Bar":
        chart = base.mark_bar().interactive()
    elif chart_type == "Area":
        chart = base.mark_area().interactive()
    elif chart_type == "Scatter":
        chart = base.mark_point().interactive()
    else:
        chart = base
    return chart
