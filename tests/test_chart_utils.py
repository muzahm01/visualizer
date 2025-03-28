import pandas as pd

from visualizer.utils import chart_utils


def test_build_plotly_chart_line():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    options = {"show_markers": True, "smooth_lines": True, "fill_area": True}
    fig = chart_utils.build_plotly_chart(df, "x", "y", "Line Chart", options)
    # For a line chart with fill_area enabled, check that traces are filled.
    for trace in fig.data:
        assert trace.fill == "tozeroy"


def test_build_comparison_chart_histogram():
    df = pd.DataFrame({
        "x": [1, 2, 3, 1, 2, 3],
        "y": [10, 20, 30, 15, 25, 35],
        "File": ["File 1", "File 1", "File 1", "File 2", "File 2", "File 2"]
    })
    options = {"histnorm": "count"}
    fig = chart_utils.build_comparison_chart(df, "x", "y", "Histogram", options)
    # Ensure the histnorm is set to the empty string (for "count")
    for trace in fig.data:
        assert trace.histnorm == ""
