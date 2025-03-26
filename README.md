# Visualizer

Visualizer is a multipage Streamlit application for interactive data analysis and comparison of JSON and CSV files. With Visualizer, you can analyze a single file or compare two files side-by-side using a wide variety of customizable charts.

## Features

- **JSON File Analysis:**  
  Upload a JSON file, choose a table from its data, and generate interactive charts with options such as markers, smoothing, and fill area. If the X‑axis contains numeric timestamps, they are automatically converted to datetime.

- **JSON Files Comparison:**  
  Compare two JSON files by selecting a common table. Visualizer combines data from both files (tagging each row with a file identifier) and generates comparison charts (including separate Pie Charts for each file) with extensive customization options.

- **CSV File Analysis:**  
  Upload a CSV file (with auto-detected delimiters), view its data table, and create interactive charts. The app supports optional axis selection and automatically converts timestamp-like columns to datetime.

- **CSV Files Comparison:**  
  Compare two CSV files by auto-detecting common columns, and then select one X‑axis and one Y‑axis to generate a comparison chart. Visualizer provides various chart types (Line, Bar, Scatter, Area, Box, Histogram, Violin, Pie) with customizable options for each chart.

- **Chart Customization:**  
  For each chart type, Visualizer exposes additional options:
  - **Line Chart:** Toggle markers, smooth lines (spline vs. linear), and fill area under the line.
  - **Bar Chart:** Choose between grouped or stacked bars.
  - **Scatter Chart:** Adjust marker visibility and opacity.
  - **Area Chart:** Option for smooth lines.
  - **Box Plot:** Choose to display notched boxes and determine which points to show.
  - **Histogram:** Select normalization options (count, percent, probability, density, probability density).
  - **Violin Plot:** Enable a box plot overlay, control point display, and optionally show the mean line.
  - **Pie Chart:** Adjust the donut hole size.

- **Caching & Performance:**  
  File-loading functions are cached using Streamlit’s session-based caching (`@st.cache_data`), which helps improve performance with larger files.

- **Auto-Detection of CSV Delimiters:**  
  CSV files are automatically parsed using a robust auto-detection mechanism for delimiters, so you don’t need to specify the delimiter manually.

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:muzahm01/visualizer.git
   cd visualizer
   ```
2. Install the project in editable mode using pip:
   ```bash
   pip install -e .
   ```
Make sure you have Python 3.8 or newer, along with the following dependencies:
   * Streamlit (>= 1.18.0)
   * Pandas (>= 1.4.0)
   * Plotly (>= 5.0.0)

## Running the App
   ```bash
   streamlit run visualizer/app.py
   ```
Your default web browser will open the Visualizer application, where you can navigate between the following pages:

* JSON File Analysis: Analyze a single JSON file.
* JSON Files Comparison: Compare two JSON files.
* CSV File Analysis: Analyze a single CSV file.
* CSV Files Comparison: Compare two CSV files.

## Usage Instructions

### JSON File Analysis
- **Upload a JSON File:**  
  Use the file uploader to load your JSON file. Visualizer automatically extracts table-like data from the JSON.
- **Select a Table:**  
  Choose a table from the dropdown list. The data from that table is then displayed.
- **Axis & Chart Type Selection:**  
  Optionally select one column as the X‑axis and one as the Y‑axis. Then choose a chart type (e.g., Line Chart, Bar Chart, Scatter Chart, Area Chart, Box Plot, Histogram, Violin Plot, or Pie Chart).
- **Additional Chart Options:**  
  Depending on the chart type, additional widgets appear (e.g., markers, smooth lines, fill area for Line Charts; bar mode for Bar Charts; etc.).
- **Chart Generation:**  
  Once both axes are selected, the chart is generated automatically. If the X‑axis column appears to contain numeric timestamps, it’s converted to datetime.
- **Output:**  
  The generated interactive chart and the corresponding data table are displayed on the page.

### JSON Files Comparison
- **Upload Two JSON Files:**  
  Use the provided uploaders to load two JSON files. Visualizer extracts tables from both files.
- **Select a Common Table:**  
  Choose a table (using the first file’s keys) to compare the data. Data from both files are shown side by side.
- **Axis & Chart Type Selection:**  
  Optionally select an X‑axis and a Y‑axis column from the available columns, and choose a chart type.
- **Additional Options:**  
  Additional options appear based on the chart type (such as markers, smoothing, normalization, etc.). For Pie Charts, separate charts are generated for each file.
- **Comparison Chart:**  
  A combined comparison chart (overlaying data from both files) is generated automatically if both axes are selected, and a combined data table is displayed.

### CSV File Analysis
- **Upload a CSV File:**  
  Use the file uploader to load a CSV file. The delimiter is auto-detected.
- **Data Display:**  
  The CSV data is shown as a complete table.
- **Axis & Chart Type Selection:**  
  Optionally select an X‑axis and a Y‑axis column from the list of CSV columns, and then select a chart type.
- **Additional Chart Options:**  
  Additional settings specific to the chart type (such as markers, smoothing, fill area, normalization, etc.) appear.
- **Timestamp Conversion:**  
  If the X‑axis column appears to be numeric and its name contains “timestamp”, it is converted to datetime.
- **Chart Generation:**  
  The chart is automatically generated and displayed along with the data table.

### CSV Files Comparison
- **Upload Two CSV Files:**  
  Load two CSV files using the uploaders. The delimiter is auto-detected for both files.
- **Data Display & Common Columns:**  
  The data from each file is displayed separately, and Visualizer computes the common columns.
- **Axis & Chart Type Selection:**  
  Select one common column as the X‑axis and one as the Y‑axis, and then choose a chart type.
- **Additional Options:**  
  Additional customization options appear based on the chosen chart type (such as markers, smooth lines, bar mode, normalization, donut size for Pie Charts, etc.).
- **Comparison Chart:**  
  A combined comparison chart is generated automatically using the data from both files (with separate traces for File 1 and File 2). For Pie Charts, separate charts are generated for each file.
- **Output:**  
  The combined chart and a combined data table are displayed for review.
## Caching and Performance

Visualizer employs Streamlit’s session-based caching (using `@st.cache_data`) to efficiently load and parse files. This means that once a file is uploaded and processed, the resulting data is stored in memory for the duration of the user session—reducing repeated file reads and speeding up performance, even when working with larger files. This caching is designed to improve responsiveness without consuming excessive system storage.

## Limitations and Security

- **File Paths and Metadata:**  
  Due to browser security restrictions, Visualizer only has access to the file name and content—not the full local file path. This ensures user privacy but may limit certain metadata availability.

- **Data Privacy:**  
  Visualizer processes files locally (or on a secured server) and does not transmit your data externally unless explicitly configured. Users should ensure that any sensitive data is handled in a secure environment.

- **Browser Limitations:**  
  The auto-detection mechanisms (e.g., for CSV delimiters) rely on sampling a portion of the file, which may occasionally lead to issues with certain file formats or very large files. Always verify that the parsed data appears correct.

## Contributions and License

Contributions to Visualizer are welcome! If you have suggestions, encounter issues, or want to contribute new features, please feel free to open an issue or submit a pull request via the project's GitHub repository.

Visualizer is licensed under the [MIT License](LICENSE). This permissive license allows for free use, modification, and distribution of the code with minimal restrictions.
