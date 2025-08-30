import json
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
from components import kpi_row, intersection_panel, time_series_panel, video_panel, intersection_map

# Enhanced page configuration
st.set_page_config(
    page_title="AI Traffic Management System", 
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for overall dashboard styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .dashboard-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .online { background-color: #4CAF50; }
    .offline { background-color: #F44336; }
    .warning { background-color: #FF9800; }
</style>
""", unsafe_allow_html=True)

# Enhanced main title with status indicators
st.markdown("""
<div class="main-header">
    <h1>🚦 AI-Powered Traffic Management System</h1>
    <h3>🤖 Intelligent Traffic Optimization Dashboard</h3>
    <p>Real-time monitoring and AI-driven traffic signal control</p>
</div>
""", unsafe_allow_html=True)

DATA_FILE = Path(__file__).parents[1] / "data" / "dashboard_data.json"

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# Enhanced Sidebar with better styling
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); 
            border-radius: 10px; margin-bottom: 1rem;">
    <h2 style="color: white;">⚙️ Control Panel</h2>
</div>
""", unsafe_allow_html=True)

refresh = st.sidebar.slider("🔄 Refresh interval (sec)", 0.5, 5.0, 1.0, 0.5)

# System status in sidebar
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
    <h4 style="color: white;">📊 System Status</h4>
    <div style="color: white; margin: 0.5rem 0;">
        <span class="status-indicator online"></span>AI Engine: Online
    </div>
    <div style="color: white; margin: 0.5rem 0;">
        <span class="status-indicator online"></span>Data Pipeline: Active
    </div>
    <div style="color: white; margin: 0.5rem 0;">
        <span class="status-indicator online"></span>Traffic Sensors: Connected
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; color: white;">
    <h4>📁 Data Source</h4>
    <p style="font-size: 0.8rem; word-wrap: break-word;">{DATA_FILE}</p>
</div>
""", unsafe_allow_html=True)

# Load JSON
data = load_data()
if not data:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffeaa7, #fab1a0); 
                padding: 3rem; border-radius: 20px; text-align: center; 
                color: #2d3436; margin: 2rem 0;">
        <h2>⚠️ System Initializing</h2>
        <h4>🔄 Waiting for data stream...</h4>
        <p>The traffic management system is starting up. Data will appear shortly.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Enhanced layout with better spacing and organization
st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
kpi_row(data)
st.markdown('</div>', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["🗺️ Live Map", "📹 Traffic Feed", "📊 Analytics"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        intersection_map(data)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
        intersection_panel(data)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    video_panel(data)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    time_series_panel(data)
    st.markdown('</div>', unsafe_allow_html=True)
