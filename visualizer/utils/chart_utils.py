import altair as alt


def build_chart(df, x_col, y_col, chart_type, options):
    """
    Build an Altair chart from DataFrame `df` using x_col and y_col.
    chart_type: one of "Line", "Bar", "Area", "Scatter"
    options: dictionary for additional customization (if needed)
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
