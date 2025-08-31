"""
UI Layout Components
Contains header, sidebar, and layout helper components
"""

import streamlit as st
from pathlib import Path


def render_header():
    """Render the main dashboard header with navigation"""
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="main-title">
                    <i class="fas fa-traffic-light"></i> AI TRAFFIC CONTROL
                </h1>
                <p class="main-subtitle">
                    <i class="fas fa-brain"></i> Intelligent Traffic Optimization & Real-time Analytics
                </p>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div class="status-indicator status-online">
                    <i class="fas fa-circle"></i> System Online
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; 
                            border-radius: 20px; border: 1px solid rgba(255,255,255,0.2);">
                    <i class="fas fa-user-circle"></i> Admin Panel
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(data_file_path, refresh_rate=1.0):
    """Render the modern dark sidebar with controls"""
    
    # Modern dark sidebar header
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #333;">
        <h2 style="color: white; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-cog"></i> Control Panel
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Refresh rate control
    refresh = st.sidebar.slider("🔄 Refresh Rate (sec)", 0.5, 5.0, refresh_rate, 0.5)

    # Modern system status indicators
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%); 
                padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 1px solid #333;">
        <h4 style="color: white; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-chart-line"></i> System Status
        </h4>
        <div class="status-indicator status-online">
            <i class="fas fa-brain"></i> AI Engine
        </div>
        <div class="status-indicator status-online">
            <i class="fas fa-stream"></i> Data Pipeline
        </div>
        <div class="status-indicator status-online">
            <i class="fas fa-satellite-dish"></i> Traffic Sensors
        </div>
        <div class="status-indicator status-warning">
            <i class="fas fa-video"></i> Camera Feed
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data source information
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%); 
                padding: 1.5rem; border-radius: 12px; color: white; border: 1px solid #333;">
        <h4 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-database"></i> Data Source
        </h4>
        <p style="font-size: 0.8rem; color: #9ca3af; word-wrap: break-word; margin: 0;">
            {Path(data_file_path).name}
        </p>
        <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(16, 185, 129, 0.1); 
                    border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
            <small style="color: #10b981;">
                <i class="fas fa-check-circle"></i> Connected
            </small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return refresh


def render_data_loading_placeholder():
    """Render placeholder when data is not available"""
    st.markdown("""
    <div class="dashboard-card" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; color: #f59e0b; margin-bottom: 1rem;">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <h2 style="color: #ffffff; margin-bottom: 1rem;">System Initializing</h2>
        <div style="color: #9ca3af; margin-bottom: 2rem;">
            <i class="fas fa-spinner fa-spin"></i> Waiting for data stream...
        </div>
        <p style="color: #6b7280;">The AI traffic management system is starting up. Data will appear shortly.</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(icon, title):
    """Render a modern section header"""
    st.markdown(f"""
    <div class="section-header">
        <i class="fas {icon} section-icon"></i>
        <h2 class="section-title">{title}</h2>
    </div>
    """, unsafe_allow_html=True)


def render_dashboard_card_wrapper(content_func, *args, **kwargs):
    """Wrapper function to render content inside a dashboard card"""
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    content_func(*args, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)
