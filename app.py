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

# Add RL repo to path for imports
rl_repo_path = Path(__file__).resolve().parent.parent / "Traffic-simulation-rl"
if str(rl_repo_path) not in sys.path:
    sys.path.insert(0, str(rl_repo_path))

from traffic_rl.api_rl import load_rl, simulate_episode, make_dummy_episode


st.set_page_config(
    page_title="AI Traffic Management - RL Demo", 
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    """Render KPI cards at the top of the dashboard."""
    st.subheader("📊 Episode Performance KPIs")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Avg Reward (episode)",
            value=f"{kpis['avg_reward']:.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Avg Waiting Time (s)",
            value=f"{kpis['avg_wait_time']:.1f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Peak Queue Length",
            value=kpis['peak_queue_length'],
            delta=None
        )
    
    with col4:
        st.metric(
            label="Actions Used (unique)",
            value=kpis['unique_actions'],
            delta=None
        )
    
    with col5:
        st.metric(
            label="Steps Simulated",
            value=kpis['steps_simulated'],
            delta=None
        )


def render_charts(df: pd.DataFrame):
    """Render all the performance charts."""
    if df.empty:
        st.warning("No data available for charts.")
        return
    
    st.subheader("📈 Performance Charts")
    
    # Create tabs for different chart types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Reward & Wait Time", "Queue Length", "Action Distribution", 
        "Throughput", "Junction Analysis"
    ])
    
    with tab1:
        # Reward and Wait Time over Time
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Reward over Time", "Average Wait Time over Time"),
            vertical_spacing=0.1
        )
        
        if "reward" in df.columns:
            fig.add_trace(
                go.Scatter(x=df["time"], y=df["reward"], mode="lines", name="Reward"),
                row=1, col=1
            )
        
        if "avg_wait_time" in df.columns and df["avg_wait_time"].notna().any():
            fig.add_trace(
                go.Scatter(x=df["time"], y=df["avg_wait_time"], mode="lines", name="Wait Time"),
                row=2, col=1
            )
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Queue Length over Time
        if "queue_length" in df.columns and df["queue_length"].notna().any():
            fig = px.line(df, x="time", y="queue_length", title="Queue Length over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Queue length data not available.")
    
    with tab3:
        # Action Distribution
        if "action" in df.columns:
            action_counts = df["action"].value_counts().sort_index()
            fig = px.bar(
                x=action_counts.index, 
                y=action_counts.values,
                title="Action Distribution",
                labels={"x": "Action", "y": "Count"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Action data not available.")
    
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
    st.title("🚦 AI-Powered Traffic Management System")
    st.markdown("**Reinforcement Learning Demo Dashboard**")
    
    # Sidebar controls
    st.sidebar.header("🎛️ RL Demo")
    
    # Model path selection
    model_path = st.sidebar.text_input(
        "Model Path",
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
        "Use dummy agent if weights missing",
        value=True,
        help="Generate realistic dummy data when model is not available"
    )
    
    # Simulation parameters
    st.sidebar.subheader("Simulation Parameters")
    max_steps = st.sidebar.number_input(
        "Max Steps",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )
    
    # Run simulation button
    run_demo = st.sidebar.button("🚀 Run RL Demo", use_container_width=True, type="primary")
    
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
        # Welcome message
        st.info("👆 Click **'Run RL Demo'** in the sidebar to start the simulation.")
        
        # Instructions
        with st.expander("📖 How to Use This Dashboard"):
            st.markdown("""
            ### Getting Started
            
            1. **Default Model**: Uses `Traffic-simulation-rl/models/demo_rl.pth`
            2. **Custom Path**: Specify a different model path
            3. **Upload File**: Upload your own `.pth` model file
            4. **Dummy Agent**: Generate realistic demo data when model is missing
            
            ### What You'll See
            
            - **KPI Cards**: Episode performance metrics
            - **Charts**: Reward, wait time, queue length, action distribution
            - **Tables**: Raw data and action aggregates
            
            ### Troubleshooting
            
            - If you see "Model not found", enable "Use dummy agent" for demo data
            - The dashboard works with any DQN model trained with the Traffic-simulation-rl repo
            - Charts adapt to available data columns automatically
            """)


if __name__ == "__main__":
    main()


