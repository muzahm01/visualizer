import streamlit as st
from visualizer import json_tab, csv_tab

st.set_page_config(page_title="Visualizer", layout="wide")
st.title("Visualizer - Data Visualization")

tabs = st.tabs(["JSON", "CSV"])
with tabs[0]:
    json_tab.render_json_tab()
with tabs[1]:
    csv_tab.render_csv_tab()
