from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import tempfile
import shutil
import sys
import time

# Add RL repo to path for imports
rl_repo_path = Path(__file__).resolve().parent.parent / "Traffic-simulation-rl"
if str(rl_repo_path) not in sys.path:
    sys.path.insert(0, str(rl_repo_path))

from traffic_rl.api_rl import load_rl, simulate_episode, make_dummy_episode

# Page configuration with enhanced styling
st.set_page_config(
    page_title="🚦 AI Traffic Management System", 
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# AI-Powered Traffic Management System\nThis dashboard demonstrates reinforcement learning for intelligent traffic control."
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors - Dark Professional Theme */
    :root {
        --primary-color: #4f46e5;
        --secondary-color: #f59e0b;
        --success-color: #10b981;
        --warning-color: #ef4444;
        --info-color: #06b6d4;
        --light-bg: #1f2937;
        --dark-bg: #111827;
        --card-bg: #374151;
        --border-color: #4b5563;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --gradient-primary: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        --gradient-secondary: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        --shadow-hover: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: var(--dark-bg);
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, var(--dark-bg) 0%, var(--light-bg) 100%);
    }
    
    /* Main content area */
    .main {
        background: var(--dark-bg);
    }
    
    /* Custom header styling */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem 0;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow);
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* KPI Cards styling */
    .kpi-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-hover);
    }
    
    .kpi-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--light-bg) 0%, var(--dark-bg) 100%);
    }
    
    .sidebar .sidebar-content {
        background: var(--light-bg);
    }
    
    /* Sidebar elements */
    .sidebar .stSelectbox > div > div {
        background-color: var(--card-bg);
        color: var(--text-primary);
    }
    
    .sidebar .stTextInput > div > div > input {
        background-color: var(--card-bg);
        color: var(--text-primary);
        border-color: var(--border-color);
    }
    
    .sidebar .stNumberInput > div > div > input {
        background-color: var(--card-bg);
        color: var(--text-primary);
        border-color: var(--border-color);
    }
    
    .sidebar .stCheckbox > div > div {
        background-color: var(--card-bg);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    
    /* Metric styling */
    .metric-container {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary-color);
    }
    
    /* Chart containers */
    .chart-container {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--light-bg);
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid #ffeaa7;
        border-radius: 8px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #bee5eb;
        border-radius: 8px;
    }
    
    /* Loading spinner */
    .stSpinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .kpi-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def _cached_load(model_path: str = "models/demo_rl.pth"):
    """Cache the loaded RL model and environment."""
    return load_rl(model_path)


@st.cache_data(show_spinner=False)
def _cached_simulate(model_path: str, max_steps: int = 100, use_dummy: bool = False) -> pd.DataFrame:
    """Cache the simulation results."""
    if use_dummy:
        return make_dummy_episode(max_steps)
    else:
        env, agent = _cached_load(model_path)
        return simulate_episode(agent, env, max_steps=max_steps)


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute key performance indicators from the episode data."""
    if df.empty:
        return {
            "avg_reward": 0.0,
            "avg_wait_time": 0.0,
            "peak_queue_length": 0,
            "unique_actions": 0,
            "steps_simulated": 0
        }
    
    return {
        "avg_reward": float(df["reward"].mean()) if "reward" in df.columns else 0.0,
        "avg_wait_time": float(df["avg_wait_time"].mean()) if "avg_wait_time" in df.columns and df["avg_wait_time"].notna().any() else 0.0,
        "peak_queue_length": int(df["queue_length"].max()) if "queue_length" in df.columns and df["queue_length"].notna().any() else 0,
        "unique_actions": int(df["action"].nunique()) if "action" in df.columns else 0,
        "steps_simulated": len(df)
    }


def render_kpi_cards(kpis: dict):
    """Render enhanced KPI cards at the top of the dashboard."""
    st.markdown("""
    <div class="chart-container">
        <h2 style="font-family: 'Inter', sans-serif; font-weight: 600; color: #2c3e50; margin-bottom: 1.5rem; text-align: center;">
            📊 Episode Performance KPIs
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create enhanced KPI cards with icons and better styling
    col1, col2, col3, col4, col5 = st.columns(5)
    
    kpi_data = [
        {
            "icon": "🎯",
            "label": "Avg Reward",
            "value": f"{kpis['avg_reward']:.2f}",
            "suffix": "",
            "color": "#4f46e5"
        },
        {
            "icon": "⏱️",
            "label": "Avg Wait Time",
            "value": f"{kpis['avg_wait_time']:.1f}",
            "suffix": "s",
            "color": "#f59e0b"
        },
        {
            "icon": "🚗",
            "label": "Peak Queue",
            "value": kpis['peak_queue_length'],
            "suffix": "",
            "color": "#10b981"
        },
        {
            "icon": "🎮",
            "label": "Actions Used",
            "value": kpis['unique_actions'],
            "suffix": "",
            "color": "#ef4444"
        },
        {
            "icon": "📈",
            "label": "Steps Simulated",
            "value": kpis['steps_simulated'],
            "suffix": "",
            "color": "#06b6d4"
        }
    ]
    
    for i, (col, kpi) in enumerate(zip([col1, col2, col3, col4, col5], kpi_data)):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {kpi['color']};">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{kpi['icon']}</div>
                <div class="kpi-value" style="color: {kpi['color']};">{kpi['value']}{kpi['suffix']}</div>
                <div class="kpi-label">{kpi['label']}</div>
            </div>
            """, unsafe_allow_html=True)


def render_charts(df: pd.DataFrame):
    """Render enhanced performance charts with better styling."""
    if df.empty:
        st.markdown("""
        <div class="chart-container">
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #6c757d; font-family: 'Inter', sans-serif;">No data available for charts</h3>
                <p style="color: #6c757d;">Run a simulation to see performance visualizations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div class="chart-container">
        <h2 style="font-family: 'Inter', sans-serif; font-weight: 600; color: #2c3e50; margin-bottom: 1.5rem; text-align: center;">
            📈 Performance Analytics
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create enhanced tabs for different chart types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Reward & Wait Time", "🚗 Queue Length", "🎮 Action Distribution", 
        "📊 Throughput", "🚦 Junction Analysis"
    ])
    
    with tab1:
        # Enhanced Reward and Wait Time over Time
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("🎯 Reward over Time", "⏱️ Average Wait Time over Time"),
            vertical_spacing=0.15
        )
        
        if "reward" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df["time"], 
                    y=df["reward"], 
                    mode="lines+markers", 
                    name="Reward",
                    line=dict(color='#4f46e5', width=3),
                    marker=dict(size=6, color='#4f46e5'),
                    fill='tonexty'
                ),
                row=1, col=1
            )
        
        if "avg_wait_time" in df.columns and df["avg_wait_time"].notna().any():
            fig.add_trace(
                go.Scatter(
                    x=df["time"], 
                    y=df["avg_wait_time"], 
                    mode="lines+markers", 
                    name="Wait Time",
                    line=dict(color='#f59e0b', width=3),
                    marker=dict(size=6, color='#f59e0b'),
                    fill='tonexty'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            height=600, 
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            title_font=dict(size=16, family="Inter"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Enhanced Queue Length over Time
        if "queue_length" in df.columns and df["queue_length"].notna().any():
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["time"], 
                y=df["queue_length"], 
                mode="lines+markers",
                name="Queue Length",
                line=dict(color='#10b981', width=3),
                marker=dict(size=6, color='#10b981'),
                fill='tonexty'
            ))
            fig.update_layout(
                title="🚗 Queue Length over Time",
                xaxis_title="Time",
                yaxis_title="Queue Length",
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12),
                title_font=dict(size=16, family="Inter")
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🚗</div>
                    <h3 style="color: #6c757d; font-family: 'Inter', sans-serif;">Queue length data not available</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Enhanced Action Distribution
        if "action" in df.columns:
            action_counts = df["action"].value_counts().sort_index()
            colors = ['#4f46e5', '#f59e0b', '#10b981', '#ef4444', '#06b6d4', '#8b5cf6', '#f97316', '#ec4899']
            
            fig = go.Figure(data=[
                go.Bar(
                    x=action_counts.index, 
                    y=action_counts.values,
                    marker=dict(
                        color=colors[:len(action_counts)],
                        line=dict(color='white', width=2)
                    ),
                    text=action_counts.values,
                    textposition='auto',
                )
            ])
            fig.update_layout(
                title="🎮 Action Distribution",
                xaxis_title="Action",
                yaxis_title="Count",
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12),
                title_font=dict(size=16, family="Inter")
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">🎮</div>
                    <h3 style="color: #6c757d; font-family: 'Inter', sans-serif;">Action data not available</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Throughput over Time (if available)
        if "throughput" in df.columns and df["throughput"].notna().any():
            fig = px.line(df, x="time", y="throughput", title="Throughput over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Throughput data not available.")
    
    with tab5:
        # Junction Analysis (if available)
        if "junction_id" in df.columns and df["junction_id"].notna().any():
            junction_stats = df.groupby("junction_id").agg({
                "avg_wait_time": "mean",
                "queue_length": "mean"
            }).reset_index()
            
            fig = px.bar(
                junction_stats, 
                x="junction_id", 
                y=["avg_wait_time", "queue_length"],
                title="Per-Junction Performance",
                barmode="group"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Junction data not available.")


def render_tables(df: pd.DataFrame):
    """Render data tables."""
    st.subheader("📋 Data Tables")
    
    tab1, tab2 = st.tabs(["Raw Episode Data", "Action Aggregates"])
    
    with tab1:
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        if "action" in df.columns and not df.empty:
            action_agg = df.groupby("action").agg({
                "reward": "mean",
                "avg_wait_time": "mean",
                "queue_length": "mean"
            }).round(2)
            st.dataframe(action_agg, use_container_width=True)
        else:
            st.info("No action data available for aggregation.")


def handle_file_upload() -> str | None:
    """Handle file upload for custom model."""
    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom Model (.pth)", 
        type=['pth'],
        help="Upload a custom trained model file"
    )
    
    if uploaded_file is not None:
        # Save uploaded file to RL repo models directory
        rl_models_dir = rl_repo_path / "models"
        rl_models_dir.mkdir(exist_ok=True)
        uploaded_path = rl_models_dir / "uploaded_demo.pth"
        
        with open(uploaded_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return str(uploaded_path.relative_to(rl_repo_path))
    
    return None


def main():
    # Beautiful header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>🚦 AI-Powered Traffic Management System</h1>
        <p>Intelligent Reinforcement Learning Dashboard for Smart Traffic Control</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar with better styling
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-family: 'Inter', sans-serif; font-weight: 600;">🎛️ Control Panel</h2>
        <p style="color: white; margin: 0.5rem 0 0 0; opacity: 0.9; font-family: 'Inter', sans-serif;">Configure your simulation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model configuration section
    st.sidebar.markdown("""
    <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid var(--border-color);">
        <h3 style="color: var(--text-primary); font-family: 'Inter', sans-serif; font-weight: 600; margin: 0 0 1rem 0;">🤖 Model Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Model path selection
    model_path = st.sidebar.text_input(
        "📁 Model Path",
        value="models/demo_rl.pth",
        help="Path relative to Traffic-simulation-rl repo"
    )
    
    # File uploader
    uploaded_path = handle_file_upload()
    if uploaded_path:
        model_path = uploaded_path
        st.sidebar.success(f"✅ Uploaded model: {uploaded_path}")
    
    # Dummy agent fallback
    use_dummy = st.sidebar.checkbox(
        "🎭 Use dummy agent if weights missing",
        value=True,
        help="Generate realistic dummy data when model is not available"
    )
    
    # Simulation parameters section
    st.sidebar.markdown("""
    <div style="background: var(--card-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 1px solid var(--border-color);">
        <h3 style="color: var(--text-primary); font-family: 'Inter', sans-serif; font-weight: 600; margin: 0 0 1rem 0;">⚙️ Simulation Parameters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    max_steps = st.sidebar.number_input(
        "📊 Max Steps",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Maximum number of simulation steps"
    )
    
    # Enhanced run button
    st.sidebar.markdown("""
    <div style="margin-top: 2rem;">
    """, unsafe_allow_html=True)
    
    run_demo = st.sidebar.button("🚀 Run RL Demo", use_container_width=True, type="primary")
    
    st.sidebar.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    if run_demo:
        try:
            with st.spinner("Loading RL model and running simulation..."):
                df = _cached_simulate(model_path, max_steps, use_dummy=False)
            
            if df.empty:
                st.warning("No data returned from simulate_episode().")
                return
            
            # Compute and display KPIs
            kpis = compute_kpis(df)
            render_kpi_cards(kpis)
            
            # Render charts
            render_charts(df)
            
            # Render tables
            render_tables(df)
            
            st.success(f"✅ Simulation completed successfully! Processed {len(df)} steps.")
            
        except FileNotFoundError as e:
            if use_dummy:
                st.warning("⚠️ Model not found, using dummy agent fallback...")
                with st.spinner("Generating dummy episode data..."):
                    df = _cached_simulate(model_path, max_steps, use_dummy=True)
                
                # Compute and display KPIs
                kpis = compute_kpis(df)
                render_kpi_cards(kpis)
                
                # Render charts
                render_charts(df)
                
                # Render tables
                render_tables(df)
                
                st.info("📊 **Demo Mode**: Showing realistic dummy data. To use real values, place demo_rl.pth in Traffic-simulation-rl/models/ or use the uploader.")
            else:
                st.error(f"❌ Model not found: {e}")
                st.info("💡 **How to fix:**\n"
                       "1. Place a demo model at `Traffic-simulation-rl/models/demo_rl.pth`\n"
                       "2. Or use the file uploader above\n"
                       "3. Or enable 'Use dummy agent if weights missing' for demo data")
        
        except Exception as e:
            st.error(f"❌ Error running simulation: {e}")
            st.exception(e)
    
    else:
        # Enhanced welcome message
        st.markdown("""
        <div class="chart-container">
            <div style="text-align: center; padding: 3rem 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🚦</div>
                <h2 style="color: var(--text-primary); font-family: 'Inter', sans-serif; font-weight: 600; margin-bottom: 1rem;">
                    Welcome to AI Traffic Management
                </h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.6;">
                    Ready to explore intelligent traffic control? Click the <strong>🚀 Run RL Demo</strong> button in the sidebar to start your simulation!
                </p>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 2rem 0;">
                    <h3 style="margin: 0 0 0.5rem 0; font-family: 'Inter', sans-serif;">🎯 What You'll Experience</h3>
                    <p style="margin: 0; opacity: 0.9;">Real-time traffic simulation with AI-powered signal control and comprehensive performance analytics</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced instructions
        with st.expander("📖 How to Use This Dashboard", expanded=False):
            st.markdown("""
            <div style="font-family: 'Inter', sans-serif;">
                <h3 style="color: var(--text-primary); font-weight: 600;">🚀 Getting Started</h3>
                <ol style="color: var(--text-secondary); line-height: 1.8;">
                    <li><strong>Default Model</strong>: Uses <code>Traffic-simulation-rl/models/demo_rl.pth</code></li>
                    <li><strong>Custom Path</strong>: Specify a different model path in the sidebar</li>
                    <li><strong>Upload File</strong>: Upload your own <code>.pth</code> model file</li>
                    <li><strong>Dummy Agent</strong>: Generate realistic demo data when model is missing</li>
                </ol>
                
                <h3 style="color: var(--text-primary); font-weight: 600; margin-top: 2rem;">📊 What You'll See</h3>
                <ul style="color: var(--text-secondary); line-height: 1.8;">
                    <li><strong>KPI Cards</strong>: Episode performance metrics with beautiful visualizations</li>
                    <li><strong>Interactive Charts</strong>: Reward, wait time, queue length, action distribution</li>
                    <li><strong>Data Tables</strong>: Raw data and action aggregates for detailed analysis</li>
                </ul>
                
                <h3 style="color: var(--text-primary); font-weight: 600; margin-top: 2rem;">🔧 Troubleshooting</h3>
                <ul style="color: var(--text-secondary); line-height: 1.8;">
                    <li>If you see "Model not found", enable "Use dummy agent" for demo data</li>
                    <li>The dashboard works with any DQN model trained with the Traffic-simulation-rl repo</li>
                    <li>Charts adapt to available data columns automatically</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a footer
        st.markdown("""
        <div class="footer">
            <p>🚦 AI-Powered Traffic Management System | Built with Streamlit & Reinforcement Learning</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


