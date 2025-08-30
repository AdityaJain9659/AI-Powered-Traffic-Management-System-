# dashboard/components.py
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def kpi_row(d):
    """Enhanced KPI metrics with better styling"""
    st.markdown("### 📊 Real-Time Performance Metrics")
    
    # Custom CSS for metrics
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    .metric-delta {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .positive-delta {
        color: #4CAF50;
    }
    .negative-delta {
        color: #FF5722;
    }
    </style>
    """, unsafe_allow_html=True)
    
    baseline = d.get("baseline_avg_travel_time") or 1e-9
    delta = (1 - d["avg_travel_time"]/baseline) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_class = "positive-delta" if delta > 0 else "negative-delta"
        delta_icon = "📈" if delta > 0 else "📉"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🚗 Average Travel Time</div>
            <div class="metric-value">{d['avg_travel_time']:.1f}s</div>
            <div class="metric-delta {delta_class}">{delta_icon} {delta:.1f}% vs baseline</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        wait_status = "🟢" if d['avg_wait_time'] < 20 else "🟡" if d['avg_wait_time'] < 40 else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⏱️ Average Wait Time</div>
            <div class="metric-value">{d['avg_wait_time']:.1f}s</div>
            <div class="metric-delta">{wait_status} Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        vehicle_density = "Low" if d['vehicles_in_system'] < 300 else "Medium" if d['vehicles_in_system'] < 600 else "High"
        density_icon = "🟢" if vehicle_density == "Low" else "🟡" if vehicle_density == "Medium" else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🚙 Vehicles in System</div>
            <div class="metric-value">{d['vehicles_in_system']}</div>
            <div class="metric-delta">{density_icon} {vehicle_density} Density</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        efficiency = (baseline - d['avg_travel_time']) / baseline * 100
        efficiency_icon = "🎯" if efficiency > 10 else "⚡" if efficiency > 0 else "⚠️"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚡ AI Efficiency</div>
            <div class="metric-value">{efficiency:.1f}%</div>
            <div class="metric-delta">{efficiency_icon} Optimization</div>
        </div>
        """, unsafe_allow_html=True)

def intersection_panel(d):
    """Enhanced intersection selection panel with modern styling"""
    st.markdown("### 🚦 Intersection Control Panel")
    
    # Custom styling for the panel
    st.markdown("""
    <style>
    .intersection-card {
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .phase-indicator {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.8rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    .queue-bar {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    ints = list(d["intersections"].keys())
    
    # Intersection selector with enhanced styling
    st.markdown("**Select Intersection:**")
    picked = st.selectbox(
        "Choose intersection to monitor:",
        ints, 
        index=ints.index(d.get("selected_intersection", ints[0])),
        label_visibility="collapsed"
    )
    
    node = d["intersections"][picked]
    intersection_name = node.get("name", picked.replace("_", " ").title())
    
    # Display intersection info in a styled card
    st.markdown(f"""
    <div class="intersection-card">
        <h3>🏗️ {intersection_name}</h3>
        <div class="phase-indicator">
            <h4>Current Traffic Phase</h4>
            <h2>Phase {node['current_phase']}</h2>
            <p>{get_phase_description(node['current_phase'])}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced queue visualization
    st.markdown("**🚗 Lane Queue Status**")
    directions = ["North", "East", "South", "West"]
    queue_data = []
    
    for i, (direction, queue_len) in enumerate(zip(directions, node["queues"])):
        queue_data.append({
            "Direction": direction,
            "Queue Length": queue_len,
            "Status": get_queue_status(queue_len)
        })
    
    df = pd.DataFrame(queue_data)
    
    # Create enhanced bar chart
    fig = px.bar(
        df, 
        x="Direction", 
        y="Queue Length",
        color="Queue Length",
        color_continuous_scale=["green", "yellow", "orange", "red"],
        title="Vehicle Queue by Direction",
        text="Queue Length"
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=2
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Queue status indicators
    cols = st.columns(4)
    for i, (direction, queue_len) in enumerate(zip(directions, node["queues"])):
        with cols[i]:
            status_color = get_queue_color(queue_len)
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; background: {status_color}; 
                        border-radius: 8px; color: white; font-weight: bold;">
                {direction}<br>
                <span style="font-size: 1.5rem;">{queue_len}</span><br>
                <small>{get_queue_status(queue_len)}</small>
            </div>
            """, unsafe_allow_html=True)

def get_phase_description(phase):
    """Get human-readable phase description"""
    descriptions = {
        0: "🟢 North-South traffic flowing",
        1: "🟢 East-West traffic flowing", 
        2: "🔴 All directions stopped",
        3: "🟡 North-South preparing to stop",
        4: "🟡 East-West preparing to stop"
    }
    return descriptions.get(phase, f"Phase {phase}")

def get_queue_status(queue_len):
    """Get queue status description"""
    if queue_len <= 2:
        return "Free Flow"
    elif queue_len <= 5:
        return "Moderate"
    elif queue_len <= 8:
        return "Congested"
    else:
        return "Severe"

def get_queue_color(queue_len):
    """Get color based on queue length"""
    if queue_len <= 2:
        return "#4CAF50"  # Green
    elif queue_len <= 5:
        return "#FF9800"  # Orange
    elif queue_len <= 8:
        return "#FF5722"  # Red-orange
    else:
        return "#D32F2F"  # Red

def time_series_panel(d):
    """Enhanced time series visualization with better styling"""
    st.markdown("### 📈 Performance Trends")
    
    ts = d.get("time_series", {})
    if ts and ts.get("t"):
        # Create enhanced time series plot
        fig = go.Figure()
        
        # Add RL performance line
        fig.add_trace(go.Scatter(
            x=ts["t"],
            y=ts["rl_avg_travel_time"],
            mode='lines+markers',
            name='AI Optimized',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, symbol='circle'),
            hovertemplate='<b>AI Optimized</b><br>Time: %{x}s<br>Travel Time: %{y:.1f}s<extra></extra>'
        ))
        
        # Add baseline line
        fig.add_trace(go.Scatter(
            x=ts["t"],
            y=ts["baseline_avg_travel_time"],
            mode='lines+markers',
            name='Traditional Control',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate='<b>Traditional Control</b><br>Time: %{x}s<br>Travel Time: %{y:.1f}s<extra></extra>'
        ))
        
        fig.update_layout(
            title="Travel Time Comparison",
            xaxis_title="Time (seconds)",
            yaxis_title="Average Travel Time (seconds)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance summary
        current_improvement = (ts["baseline_avg_travel_time"][-1] - ts["rl_avg_travel_time"][-1]) / ts["baseline_avg_travel_time"][-1] * 100
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4CAF50, #45a049); 
                    padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-top: 1rem;">
            <h4>🎯 Current AI Improvement</h4>
            <h2>{current_improvement:.1f}%</h2>
            <p>Faster than traditional control</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffeaa7, #fab1a0); 
                    padding: 2rem; border-radius: 15px; text-align: center; color: #2d3436;">
            <h3>📊 Collecting Performance Data...</h3>
            <p>Time series data will appear here once the system starts collecting metrics</p>
        </div>
        """, unsafe_allow_html=True)

def video_panel(d):
    """Enhanced video/camera feed panel with better styling"""
    st.markdown("### 📹 Live Traffic Feed")
    
    p = d.get("latest_frame_path")
    if p and Path(p).exists():
        # Display image with enhanced styling
        st.markdown("""
        <style>
        .video-container {
            border: 3px solid #667eea;
            border-radius: 15px;
            padding: 1rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.image(Image.open(p), caption="🔴 LIVE - Real-time traffic monitoring", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Add status indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background: #4CAF50; padding: 0.5rem; border-radius: 8px; 
                        text-align: center; color: white; font-weight: bold;">
                🟢 Camera Online
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #2196F3; padding: 0.5rem; border-radius: 8px; 
                        text-align: center; color: white; font-weight: bold;">
                🎥 HD Quality
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background: #FF9800; padding: 0.5rem; border-radius: 8px; 
                        text-align: center; color: white; font-weight: bold;">
                📊 AI Analysis ON
            </div>
            """, unsafe_allow_html=True)
    else:
        # Enhanced placeholder when no video available
        st.markdown("""
        <div style="background: linear-gradient(135deg, #636e72, #2d3436); 
                    padding: 3rem; border-radius: 15px; text-align: center; 
                    color: white; border: 2px dashed #74b9ff;">
            <h2>📷 Camera Feed</h2>
            <h4>🔄 Initializing camera connection...</h4>
            <p>Traffic monitoring will begin shortly</p>
            <div style="margin-top: 1rem;">
                <span style="background: #e17055; padding: 0.3rem 1rem; 
                            border-radius: 20px; font-size: 0.8rem;">
                    🔴 OFFLINE
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def intersection_map(d):
    """
    Enhanced interactive 4-road intersection map with modern styling
    """
    st.markdown("### 🗺️ Smart Intersection Map")
    
    # Get intersection data
    selected_int = d.get("selected_intersection", list(d["intersections"].keys())[0])
    intersection_data = d["intersections"][selected_int]
    intersection_name = intersection_data.get("name", selected_int.replace("_", " ").title())
    
    # Traffic queues for each road (North, East, South, West)
    queues = intersection_data["queues"]
    current_phase = intersection_data["current_phase"]
    
    # Define traffic light phases with enhanced colors
    traffic_light_colors = {
        0: {"NS": "#4CAF50", "EW": "#F44336"},  # Green, Red
        1: {"NS": "#F44336", "EW": "#4CAF50"},  # Red, Green
        2: {"NS": "#F44336", "EW": "#F44336"},  # Red, Red
        3: {"NS": "#FFC107", "EW": "#F44336"},  # Yellow, Red
        4: {"NS": "#F44336", "EW": "#FFC107"}   # Red, Yellow
    }
    
    # Get current light colors
    lights = traffic_light_colors.get(current_phase, {"NS": "#F44336", "EW": "#F44336"})
    
    # Create enhanced figure with better styling
    fig = go.Figure()
    
    # Define intersection parameters
    center_x, center_y = 0, 0
    road_width = 0.4
    road_length = 2.5
    
    # Enhanced color scale with better gradients
    def get_road_color(queue_length):
        colors = {
            "low": "#4CAF50",      # Green - free flow
            "medium": "#FFC107",    # Yellow - moderate
            "high": "#FF9800",     # Orange - congested
            "severe": "#F44336"    # Red - severe congestion
        }
        
        if queue_length <= 2:
            return colors["low"]
        elif queue_length <= 5:
            return colors["medium"]
        elif queue_length <= 8:
            return colors["high"]
        else:
            return colors["severe"]
    
    # Enhanced road drawing with shadows and better styling
    road_configs = [
        # (x0, y0, x1, y1, direction)
        (center_x - road_width/2, center_y, center_x + road_width/2, center_y + road_length, "North"),
        (center_x, center_y - road_width/2, center_x + road_length, center_y + road_width/2, "East"),
        (center_x - road_width/2, center_y - road_length, center_x + road_width/2, center_y, "South"),
        (center_x - road_length, center_y - road_width/2, center_x, center_y + road_width/2, "West")
    ]
    
    # Draw roads with enhanced styling
    for i, (x0, y0, x1, y1, direction) in enumerate(road_configs):
        road_color = get_road_color(queues[i])
        
        # Add road shadow
        fig.add_shape(
            type="rect",
            x0=x0+0.05, y0=y0-0.05, x1=x1+0.05, y1=y1-0.05,
            fillcolor="rgba(0,0,0,0.2)", line=dict(width=0)
        )
        
        # Add main road
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=road_color, opacity=0.8,
            line=dict(color="#2c3e50", width=3)
        )
        
        # Add road markings (center line)
        if direction in ["North", "South"]:
            fig.add_shape(
                type="line",
                x0=center_x, y0=y0, x1=center_x, y1=y1,
                line=dict(color="white", width=2, dash="dash")
            )
        else:
            fig.add_shape(
                type="line",
                x0=x0, y0=center_y, x1=x1, y1=center_y,
                line=dict(color="white", width=2, dash="dash")
            )
    
    # Enhanced intersection center
    fig.add_shape(
        type="rect",
        x0=center_x - road_width/2, y0=center_y - road_width/2,
        x1=center_x + road_width/2, y1=center_y + road_width/2,
        fillcolor="#34495e", opacity=0.9,
        line=dict(color="#2c3e50", width=3)
    )
    
    # Add crosswalk markings
    crosswalk_configs = [
        (center_x - road_width/2 - 0.1, center_y + road_width/2, center_x - road_width/2, center_y + road_width/2 + 0.2),
        (center_x + road_width/2, center_y + road_width/2, center_x + road_width/2 + 0.1, center_y + road_width/2 + 0.2),
        (center_x + road_width/2, center_y - road_width/2 - 0.2, center_x + road_width/2 + 0.1, center_y - road_width/2),
        (center_x - road_width/2 - 0.1, center_y - road_width/2 - 0.2, center_x - road_width/2, center_y - road_width/2)
    ]
    
    for x0, y0, x1, y1 in crosswalk_configs:
        for i in range(5):
            offset = i * 0.04
            fig.add_shape(
                type="line",
                x0=x0 + (offset if abs(x1-x0) > abs(y1-y0) else 0), 
                y0=y0 + (offset if abs(y1-y0) > abs(x1-x0) else 0),
                x1=x1 + (offset if abs(x1-x0) > abs(y1-y0) else 0), 
                y1=y1 + (offset if abs(y1-y0) > abs(x1-x0) else 0),
                line=dict(color="white", width=3)
            )
    
    # Enhanced traffic lights with realistic positioning
    light_size = 0.12
    light_positions = [
        (center_x - road_width/2 - light_size*1.5, center_y + road_width/2 + light_size/2, lights["NS"], "North"),
        (center_x + road_width/2 + light_size/2, center_y + road_width/2 + light_size*1.5, lights["EW"], "East"),
        (center_x + road_width/2 + light_size*1.5, center_y - road_width/2 - light_size/2, lights["NS"], "South"),
        (center_x - road_width/2 - light_size/2, center_y - road_width/2 - light_size*1.5, lights["EW"], "West")
    ]
    
    for x, y, color, direction in light_positions:
        # Traffic light pole
        fig.add_shape(
            type="rect",
            x0=x - light_size/4, y0=y - light_size*2, x1=x + light_size/4, y1=y + light_size,
            fillcolor="#2c3e50", line=dict(color="#34495e", width=1)
        )
        
        # Traffic light housing
        fig.add_shape(
            type="rect",
            x0=x - light_size/2, y0=y - light_size/2, x1=x + light_size/2, y1=y + light_size/2,
            fillcolor="#2c3e50", line=dict(color="#34495e", width=2)
        )
        
        # Active light
        fig.add_shape(
            type="circle",
            x0=x - light_size/3, y0=y - light_size/3, x1=x + light_size/3, y1=y + light_size/3,
            fillcolor=color, opacity=0.9,
            line=dict(color="white", width=2)
        )
    
    # Enhanced annotations with better styling
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    positions = [(0, 2.0), (2.0, 0.3), (0, -2.0), (-2.0, 0.3)]
    
    for i, (direction, (x, y)) in enumerate(zip(directions, positions)):
        queue_status = get_queue_status(queues[i])
        status_color = get_queue_color(queues[i])
        
        fig.add_annotation(
            x=x, y=y, 
            text=f"<b>{direction}</b><br>Queue: {queues[i]} vehicles<br><span style='color:{status_color}'>{queue_status}</span>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#2c3e50",
            ax=0, ay=-30 if direction in ["NORTH", "SOUTH"] else (-30 if direction == "WEST" else 30),
            bgcolor="white",
            bordercolor="#2c3e50",
            borderwidth=2,
            borderpad=8,
            font=dict(size=11, color="#2c3e50")
        )
    
    # Enhanced phase information
    phase_names = {
        0: "🟢 North-South Flow",
        1: "🟢 East-West Flow", 
        2: "🔴 All-Way Stop",
        3: "🟡 North-South Caution",
        4: "🟡 East-West Caution"
    }
    current_phase_name = phase_names.get(current_phase, f"Phase {current_phase}")
    
    fig.add_annotation(
        x=0, y=-3.2, 
        text=f"<b>Current Phase: {current_phase_name}</b><br>Intersection: {intersection_name}",
        showarrow=False, 
        font=dict(size=14, color="white"),
        bgcolor="rgba(44, 62, 80, 0.9)",
        bordercolor="#3498db",
        borderwidth=2,
        borderpad=10
    )
    
    # Enhanced layout configuration
    fig.update_layout(
        title=dict(
            text=f"<b>🚦 {intersection_name}</b>",
            x=0.5,
            font=dict(size=20, color="#2c3e50")
        ),
        xaxis=dict(
            range=[-3, 3], 
            showgrid=False, 
            zeroline=False, 
            showticklabels=False,
            fixedrange=True
        ),
        yaxis=dict(
            range=[-3.5, 3], 
            showgrid=False, 
            zeroline=False, 
            showticklabels=False,
            fixedrange=True
        ),
        showlegend=False,
        plot_bgcolor="#ecf0f1",
        paper_bgcolor="white",
        height=600,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    
    # Display the enhanced plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced legend and statistics
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); 
                    padding: 1rem; border-radius: 10px; color: white;">
            <h4>🚦 Traffic Status Legend</h4>
            <div style="margin: 0.5rem 0;">🟢 <strong>Free Flow:</strong> ≤2 vehicles</div>
            <div style="margin: 0.5rem 0;">🟡 <strong>Moderate:</strong> 3-5 vehicles</div>
            <div style="margin: 0.5rem 0;">🟠 <strong>Congested:</strong> 6-8 vehicles</div>
            <div style="margin: 0.5rem 0;">🔴 <strong>Severe:</strong> >8 vehicles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_vehicles = sum(queues)
        avg_queue = total_vehicles / 4
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fd79a8, #e84393); 
                    padding: 1rem; border-radius: 10px; color: white;">
            <h4>📊 Intersection Statistics</h4>
            <div style="margin: 0.5rem 0;"><strong>Total Queued:</strong> {total_vehicles} vehicles</div>
            <div style="margin: 0.5rem 0;"><strong>Average Queue:</strong> {avg_queue:.1f} vehicles</div>
            <div style="margin: 0.5rem 0;"><strong>Peak Direction:</strong> {directions[queues.index(max(queues))]}</div>
            <div style="margin: 0.5rem 0;"><strong>Status:</strong> {get_intersection_status(avg_queue)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Real-time queue metrics
    st.markdown("### 📈 Real-time Queue Metrics")
    directions = ["North", "East", "South", "West"]
    cols = st.columns(4)
    for i, (direction, queue_len) in enumerate(zip(directions, queues)):
        with cols[i]:
            status_color = get_queue_color(queue_len)
            trend_icon = "📈" if queue_len > avg_queue else "📉" if queue_len < avg_queue else "➡️"
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: {status_color}; 
                        border-radius: 10px; color: white; font-weight: bold; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h4>{direction}</h4>
                <h2>{queue_len}</h2>
                <p>{get_queue_status(queue_len)} {trend_icon}</p>
            </div>
            """, unsafe_allow_html=True)

def get_intersection_status(avg_queue):
    """Get overall intersection status"""
    if avg_queue <= 3:
        return "🟢 Optimal"
    elif avg_queue <= 6:
        return "🟡 Moderate"
    else:
        return "🔴 Congested"
