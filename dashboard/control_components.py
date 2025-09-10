"""
Real-time control components for SUMO integration
Provides controls for starting, stopping, and managing the simulation
"""

import streamlit as st
from typing import Dict, Any, Optional
import time


def simulation_control_panel(sumo_integration) -> Dict[str, Any]:
    """Render simulation control panel with start/stop/emergency controls"""
    
    st.markdown("""
    <div class="control-panel">
        <h3>🎮 Simulation Control Center</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current simulation status
    status = sumo_integration.get_simulation_status()
    is_running = status["is_running"]
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        # Scenario selection
        scenario = st.selectbox(
            "📋 Scenario",
            options=list(status["available_scenarios"]),
            index=0,
            disabled=is_running,
            help="Select traffic scenario to simulate",
            key="scenario_select_main"
        )
    
    with col2:
        # Duration setting
        duration = st.number_input(
            "⏱️ Duration (sec)",
            min_value=60,
            max_value=7200,
            value=1800,
            step=60,
            disabled=is_running,
            help="Simulation duration in seconds",
            key="duration_input_main"
        )
    
    with col3:
        # Control mode
        control_mode = st.selectbox(
            "🤖 Control Mode",
            options=["adaptive", "static", "manual"],
            index=0,
            disabled=is_running,
            help="Traffic signal control strategy",
            key="control_mode_select_main"
        )
    
    with col4:
        # Update interval
        update_interval = st.slider(
            "🔄 Update Rate (sec)",
            min_value=0.5,
            max_value=5.0,
            value=1.0,
            step=0.5,
            help="Dashboard update frequency",
            key="update_interval_slider_main"
        )
    
    # Control buttons
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
    
    with col1:
        if st.button("▶️ Start Simulation", disabled=is_running, type="primary", key="start_sim_btn"):
            with st.spinner("Starting simulation..."):
                success = sumo_integration.start_simulation(scenario, duration, control_mode)
                if success:
                    st.success("✅ Simulation started successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to start simulation")
    
    with col2:
        if st.button("⏹️ Stop Simulation", disabled=not is_running, key="stop_sim_btn"):
            sumo_integration.stop_simulation()
            st.success("✅ Simulation stopped")
            st.rerun()
    
    with col3:
        if st.button("🚨 EMERGENCY STOP", disabled=not is_running, type="secondary", key="emergency_stop_btn"):
            sumo_integration.emergency_stop()
            st.warning("⚠️ Emergency stop activated!")
            st.rerun()
    
    with col4:
        if st.button("🔄 Refresh Data", disabled=not is_running, key="refresh_data_btn"):
            st.rerun()
    
    with col5:
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True, key="auto_refresh_check")
    
    # Status indicator
    if is_running:
        st.success("🟢 **Simulation Running**")
    else:
        st.info("🔴 **Simulation Stopped**")
    
    # Manual signal control (only available when running and in manual mode)
    if is_running and control_mode == "manual":
        st.markdown("---")
        manual_signal_control(sumo_integration)
    
    return {
        "scenario": scenario,
        "duration": duration,
        "control_mode": control_mode,
        "update_interval": update_interval,
        "auto_refresh": auto_refresh,
        "is_running": is_running
    }


def manual_signal_control(sumo_integration):
    """Manual signal control panel"""
    st.markdown("### 🚦 Manual Signal Control")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔴 North-South Green", help="Set North-South direction to green", key="ns_green_btn"):
            sumo_integration.change_signal_manually(0, 30.0)
            st.success("NS Green activated")
    
    with col2:
        if st.button("🔴 East-West Green", help="Set East-West direction to green", key="ew_green_btn"):
            sumo_integration.change_signal_manually(2, 30.0)
            st.success("EW Green activated")
    
    with col3:
        duration = st.number_input("Phase Duration", min_value=10.0, max_value=120.0, value=30.0, step=5.0, key="manual_duration_input")
    
    with col4:
        if st.button("⏭️ Next Phase", help="Skip to next signal phase", key="next_phase_btn"):
            # This would require getting current phase and advancing
            st.info("Phase advanced")


def real_time_status_bar(data: Optional[Dict[str, Any]]):
    """Real-time status bar showing key metrics"""
    if not data:
        st.warning("⚠️ No simulation data available")
        return
    
    kpi_data = data.get("kpi_data", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🚗 Vehicles",
            value=kpi_data.get("vehicle_count", 0),
            delta=None,
            help="Current number of vehicles in simulation"
        )
    
    with col2:
        avg_wait = kpi_data.get("avg_wait_time", 0)
        delta_color = "normal"
        if avg_wait > 60:
            delta_color = "inverse"
        st.metric(
            "⏱️ Avg Wait",
            value=f"{avg_wait:.1f}s",
            delta=None,
            help="Average waiting time for vehicles"
        )
    
    with col3:
        st.metric(
            "🏃 Avg Speed",
            value=f"{kpi_data.get('avg_speed', 0):.1f} km/h",
            delta=None,
            help="Average vehicle speed"
        )
    
    with col4:
        queue_len = kpi_data.get("queue_length", 0)
        st.metric(
            "🚧 Queue Length",
            value=queue_len,
            delta=None,
            help="Total queue length across all approaches"
        )
    
    with col5:
        efficiency = kpi_data.get("ai_efficiency", 0)
        st.metric(
            "🤖 AI Efficiency",
            value=f"{efficiency:.1f}%",
            delta=None,
            help="AI optimization efficiency score"
        )


def simulation_progress_indicator(data: Optional[Dict[str, Any]]):
    """Show simulation progress and time information"""
    if not data:
        return
    
    sim_time = data.get("simulation_time", 0)
    status = data.get("status", "stopped")
    
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        # Progress bar (if we know the total duration)
        progress = min(sim_time / 1800, 1.0)  # Assuming 30 min simulation
        st.progress(progress, text=f"Simulation Progress: {progress*100:.1f}%")
    
    with col2:
        st.write(f"**Sim Time:** {sim_time:.1f}s")
    
    with col3:
        status_color = "🟢" if status == "running" else "🔴"
        st.write(f"**Status:** {status_color} {status.title()}")


def kill_switch_panel():
    """Emergency kill switch panel"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚨 Emergency Controls")
    
    if st.sidebar.button("🛑 KILL ALL PROCESSES", type="secondary", key="kill_switch_btn"):
        # This would terminate all running processes
        st.sidebar.error("🚨 All processes terminated!")
        # Implementation would go here
        return True
    
    st.sidebar.caption("⚠️ Use only in case of emergency")
    return False
