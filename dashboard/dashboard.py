import json
import streamlit as st
import time

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

# Import SUMO integration components
from sumo_integration import initialize_sumo_integration
from control_components import (
    simulation_control_panel,
    real_time_status_bar,
    simulation_progress_indicator,
    kill_switch_panel
)

# Enhanced page configuration with dark theme
st.set_page_config(**DASHBOARD_CONFIG)

# Apply modern dark theme CSS
st.markdown(get_main_css(), unsafe_allow_html=True)

# Render modern header
render_header()

# Initialize SUMO integration
sumo_integration = initialize_sumo_integration()

def load_data():
    """Load data from either SUMO simulation or fallback JSON file"""
    # Try to get real-time data from SUMO first
    sumo_data = sumo_integration.get_current_data()
    if sumo_data:
        # Flatten SUMO data to match expected format
        flattened_data = flatten_sumo_data(sumo_data)
        return flattened_data
    
    # Fallback to JSON file if SUMO is not running
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def flatten_sumo_data(sumo_data):
    """Convert SUMO integration data to flat format expected by components"""
    if not sumo_data:
        return None
    
    kpi = sumo_data.get('kpi_data', {})
    intersection = sumo_data.get('intersection_data', {})
    
    # Create flat structure matching original format
    flat_data = {
        # Basic metrics (flatten from kpi_data)
        "avg_travel_time": kpi.get('avg_wait_time', 0.0),  # Use wait time as travel time approximation
        "avg_wait_time": kpi.get('avg_wait_time', 0.0),
        "vehicles_in_system": kpi.get('vehicle_count', 0),
        "baseline_avg_travel_time": kpi.get('avg_wait_time', 0.0) * 1.2,  # Baseline 20% higher
        
        # Simulation info
        "ts": sumo_data.get('simulation_time', 0),
        "timestamp": sumo_data.get('timestamp', ''),
        "status": sumo_data.get('status', 'stopped'),
        
        # Intersection data
        "selected_intersection": "intersection_1",
        "intersections": {
            "intersection_1": {
                "current_phase": intersection.get('current_phase', 0),
                "queues": [
                    intersection.get('per_lane_queues', {}).get('lane_1', 3),
                    intersection.get('per_lane_queues', {}).get('lane_2', 5),
                    intersection.get('per_lane_queues', {}).get('lane_3', 4),
                    intersection.get('per_lane_queues', {}).get('lane_4', 2)
                ],
                "name": intersection.get('phase_name', 'Main Intersection')
            }
        },
        
        # Time series (simplified for now)
        "time_series": sumo_data.get('time_series_data', {
            "t": [0],
            "rl_avg_travel_time": [kpi.get('avg_wait_time', 0.0)],
            "baseline_avg_travel_time": [kpi.get('avg_wait_time', 0.0) * 1.2]
        }),
        
        # Additional data
        "latest_frame_path": "",
        "traffic_phases": {
            "0": "North-South Green",
            "1": "East-West Green", 
            "2": "All Red (Transition)",
            "3": "North-South Yellow",
            "4": "East-West Yellow"
        },
        
        # Pass through the nested data for advanced components
        "sumo_raw": sumo_data
    }
    
    return flat_data

# Render modern sidebar with controls and simulation control
refresh = render_sidebar(DATA_FILE)

# Show kill switch in sidebar
emergency_stop = kill_switch_panel()
if emergency_stop:
    sumo_integration.emergency_stop()
    st.rerun()

# Load data (real-time from SUMO or fallback JSON)
data = load_data()
if not data:
    render_data_loading_placeholder()
    st.info("💡 **Tip:** Start a SUMO simulation for real-time data, or add sample data to dashboard_data.json")
    st.stop()

# Simulation progress indicator
simulation_progress_indicator(data)
st.markdown("---")

# Modern KPI cards layout
render_dashboard_card_wrapper(kpi_row, data)

# Modern navigation tabs with CSS FontAwesome icons
tab1, tab2, tab3, tab4 = st.tabs([
    "Smart Traffic Control", 
    "Live Camera Feeds", 
    "AI Performance Analytics",
    "System Control"
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

with tab4:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    render_section_header("fa-cogs", "System Control & Monitoring")
    
    # Detailed simulation control
    st.markdown("### 🎮 Advanced Simulation Control")
    control_config = simulation_control_panel(sumo_integration)
    
    st.markdown("### 📊 System Status")
    status = sumo_integration.get_simulation_status()
    
    col1, col2 = st.columns(2)
    with col1:
        st.json({
            "simulation_state": status["simulation_state"],
            "is_running": status["is_running"],
            "available_scenarios": status["available_scenarios"]
        })
    
    with col2:
        if data:
            st.json({
                "current_data_source": "SUMO Real-time" if sumo_integration.is_running else "JSON Fallback",
                "last_update": data.get("timestamp", "Unknown"),
                "data_keys": list(data.keys())
            })
    
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh functionality
if 'control_config' in locals() and control_config.get("auto_refresh", True) and control_config.get("is_running", False):
    time.sleep(control_config.get("update_interval", 1.0))
    st.rerun()
