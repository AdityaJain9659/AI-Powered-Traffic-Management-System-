import json
import streamlit as st

# Import configuration
from config import DASHBOARD_CONFIG, DATA_FILE

# Import modular components
from styles import get_main_css
from kpi_components import kpi_row
from intersection_components import intersection_panel, intersection_map
from analytics_components import time_series_panel
from video_components import video_panel
from layout_components import (
    render_header, 
    render_sidebar, 
    render_data_loading_placeholder,
    render_section_header,
    render_dashboard_card_wrapper
)

# Enhanced page configuration with dark theme
st.set_page_config(**DASHBOARD_CONFIG)

# Apply modern dark theme CSS
st.markdown(get_main_css(), unsafe_allow_html=True)

# Render modern header
render_header()

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Render modern sidebar with controls
refresh = render_sidebar(DATA_FILE)

# Load JSON data
data = load_data()
if not data:
    render_data_loading_placeholder()
    st.stop()

# Modern KPI cards layout
render_dashboard_card_wrapper(kpi_row, data)

# Modern navigation tabs with CSS FontAwesome icons
tab1, tab2, tab3 = st.tabs([
    "Smart Traffic Control", 
    "Live Camera Feeds", 
    "AI Performance Analytics"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_section_header("fa-map-marked-alt", "Live Intersection Map")
        intersection_map(data)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_section_header("fa-traffic-light", "Signal Control")
        intersection_panel(data)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_section_header("fa-video", "Traffic Camera Feeds")
    video_panel(data)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_section_header("fa-chart-area", "AI Performance Analytics")
    time_series_panel(data)
    st.markdown('</div>', unsafe_allow_html=True)
