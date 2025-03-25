import plotly.graph_objects as go


def build_graph(x_data, y_data_list, x_label, y_labels, graph_type, options):
    """
    Build a Plotly graph (Line, Bar, or Pie) using the provided data and options.

    For Line and Bar charts, it expects x_data as a tuple: (x_data_file1, x_data_file2)
    and y_data_list as a tuple: (y_data_file1, y_data_file2).
    """
    fig = go.Figure()
    if graph_type in ["Line Chart", "Bar Chart"]:
        if graph_type == "Line Chart":
            if options.get("show_markers") and options.get("show_lines"):
                mode = "lines+markers"
            elif options.get("show_markers"):
                mode = "markers"
            elif options.get("show_lines"):
                mode = "lines"
            else:
                mode = "lines"
            line_shape = "spline" if options.get("smooth_lines") else "linear"
            fill_val = "tozeroy" if options.get("fill_area") else None
            # Expecting one Y column; plot one trace per file.
            fig.add_trace(go.Scatter(
                x=x_data[0], y=y_data_list[0], mode=mode, name=f"{y_labels[0]} - File 1",
                line=dict(shape=line_shape), marker=dict(opacity=0.8), fill=fill_val
            ))
            fig.add_trace(go.Scatter(
                x=x_data[1], y=y_data_list[1], mode=mode, name=f"{y_labels[0]} - File 2",
                line=dict(shape=line_shape), marker=dict(opacity=0.8), fill=fill_val
            ))
        elif graph_type == "Bar Chart":
            fig.add_trace(go.Bar(
                x=x_data[0], y=y_data_list[0], name=f"{y_labels[0]} - File 1"
            ))
            fig.add_trace(go.Bar(
                x=x_data[1], y=y_data_list[1], name=f"{y_labels[0]} - File 2"
            ))
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_labels[0],
            hovermode="x unified",
            showlegend=options.get("show_legend", True)
        )
        fig.update_xaxes(showgrid=options.get("show_grid", True),
                         type="log" if options.get("log_x") else "linear")
        fig.update_yaxes(showgrid=options.get("show_grid", True),
                         type="log" if options.get("log_y") else "linear")
    elif graph_type == "Pie Chart":
        # Pie charts are handled separately in the tab.
        fig = None
    return fig
