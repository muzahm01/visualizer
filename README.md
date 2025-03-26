# Visualizer

Visualizer is a multipage Streamlit app for interactively analyzing and comparing JSON and CSV files.

It provides four pages:
- **JSON Analysis:** Upload and analyze a single JSON file.
- **JSON Comparison:** Upload two JSON files and compare them.
- **CSV Analysis:** Upload and analyze a single CSV file.
- **CSV Comparison:** Upload two CSV files and compare them.

Each page allows optional selection of X‑axis and Y‑axis columns (if desired) and lets you choose a chart type (Line, Bar, Area, or Scatter). After you press "Generate Chart," an interactive Altair chart is displayed along with the data table.

## Setup

1. Install the project in editable mode:
   ```bash
   pip install -e .
