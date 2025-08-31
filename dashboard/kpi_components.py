"""
KPI Components
Contains KPI metric display components for the dashboard
"""

import streamlit as st


def kpi_row(d):
    """Modern dark-themed KPI metrics with FontAwesome icons"""
    
    baseline = d.get("baseline_avg_travel_time") or 1e-9
    delta = (1 - d["avg_travel_time"]/baseline) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_class = "delta-positive" if delta > 0 else "delta-negative"
        delta_icon = "fa-arrow-up" if delta > 0 else "fa-arrow-down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-route"></i>
            </div>
            <div class="metric-label">Average Travel Time</div>
            <div class="metric-value">{d['avg_travel_time']:.1f}s</div>
            <div class="metric-delta {delta_class}">
                <i class="fas {delta_icon}"></i> {abs(delta):.1f}% vs baseline
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        wait_status = "delta-positive" if d['avg_wait_time'] < 20 else "delta-neutral" if d['avg_wait_time'] < 40 else "delta-negative"
        wait_icon = "fa-check" if d['avg_wait_time'] < 20 else "fa-exclamation" if d['avg_wait_time'] < 40 else "fa-times"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-clock"></i>
            </div>
            <div class="metric-label">Average Wait Time</div>
            <div class="metric-value">{d['avg_wait_time']:.1f}s</div>
            <div class="metric-delta {wait_status}">
                <i class="fas {wait_icon}"></i> Status
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        vehicle_density = "Low" if d['vehicles_in_system'] < 300 else "Medium" if d['vehicles_in_system'] < 600 else "High"
        density_class = "delta-positive" if vehicle_density == "Low" else "delta-neutral" if vehicle_density == "Medium" else "delta-negative"
        density_icon = "fa-leaf" if vehicle_density == "Low" else "fa-balance-scale" if vehicle_density == "Medium" else "fa-exclamation-triangle"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-car"></i>
            </div>
            <div class="metric-label">Vehicles in System</div>
            <div class="metric-value">{d['vehicles_in_system']}</div>
            <div class="metric-delta {density_class}">
                <i class="fas {density_icon}"></i> {vehicle_density} Density
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        efficiency = (baseline - d['avg_travel_time']) / baseline * 100
        efficiency_class = "delta-positive" if efficiency > 10 else "delta-neutral" if efficiency > 0 else "delta-negative"
        efficiency_icon = "fa-rocket" if efficiency > 10 else "fa-chart-line" if efficiency > 0 else "fa-exclamation"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fas fa-brain"></i>
            </div>
            <div class="metric-label">AI Efficiency</div>
            <div class="metric-value">{efficiency:.1f}%</div>
            <div class="metric-delta {efficiency_class}">
                <i class="fas {efficiency_icon}"></i> Optimization
            </div>
        </div>
        """, unsafe_allow_html=True)
