import json
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
from components import kpi_row, intersection_panel, time_series_panel, video_panel

st.set_page_config(page_title="Traffic Dashboard", layout="wide")
st.title("🚦 AI Traffic Management Dashboard")

DATA_FILE = Path(__file__).parents[1] / "data" / "dashboard_data.json"

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Sidebar
refresh = st.sidebar.slider("Refresh interval (sec)", 0.5, 5.0, 1.0, 0.5)
st.sidebar.write("Data source:", DATA_FILE)

# Load JSON
data = load_data()
if not data:
    st.warning("⚠️ No data yet… waiting for simulator/dummy writer")
    st.stop()

# Layout: KPIs top
kpi_row(data)

# Layout: two columns
left, right = st.columns([3, 2])

with left:
    video_panel(data)

with right:
    intersection_panel(data)
    time_series_panel(data)
