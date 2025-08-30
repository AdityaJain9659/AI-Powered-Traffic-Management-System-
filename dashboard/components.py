# dashboard/components.py
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def kpi_row(d):
    baseline = d.get("baseline_avg_travel_time") or 1e-9
    delta = (1 - d["avg_travel_time"]/baseline) * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg travel time (s)", f"{d['avg_travel_time']:.1f}", f"{delta:.1f}% vs baseline")
    c2.metric("Avg wait time (s)", f"{d['avg_wait_time']:.1f}")
    c3.metric("Vehicles", d["vehicles_in_system"])

def intersection_panel(d):
    ints = list(d["intersections"].keys())
    picked = st.selectbox("Intersection", ints, index=ints.index(d.get("selected_intersection", ints[0])))
    node = d["intersections"][picked]
    st.write(f"**Current phase:** {node['current_phase']}")
    df = pd.DataFrame({"lane": range(len(node["queues"])), "waiting": node["queues"]}).set_index("lane")
    st.bar_chart(df)

def time_series_panel(d):
    ts = d.get("time_series", {})
    if ts and ts.get("t"):
        df = pd.DataFrame({
            "t": ts["t"],
            "RL avg travel": ts["rl_avg_travel_time"],
            "Baseline": ts["baseline_avg_travel_time"],
        }).set_index("t")
        st.line_chart(df)
    else:
        st.info("No time-series yet.")

def video_panel(d):
    p = d.get("latest_frame_path")
    if p and Path(p).exists():
        st.image(Image.open(p), caption="Live frame", use_column_width=True)
    else:
        st.info("No frame available yet.")

def intersection_map(d):
    """
    Creates an interactive 4-road intersection map with traffic-based road coloring
    and traffic light visualization
    """
    st.subheader("🗺️ Intersection Map")
    
    # Get intersection data
    selected_int = d.get("selected_intersection", list(d["intersections"].keys())[0])
    intersection_data = d["intersections"][selected_int]
    
    # Traffic queues for each road (North, East, South, West)
    queues = intersection_data["queues"]
    current_phase = intersection_data["current_phase"]
    
    # Define traffic light phases
    # Phase 0: North-South Green, East-West Red
    # Phase 1: North-South Red, East-West Green
    # Phase 2: All Red (transition phase)
    traffic_light_colors = {
        0: {"NS": "green", "EW": "red"},
        1: {"NS": "red", "EW": "green"},
        2: {"NS": "red", "EW": "red"},
        3: {"NS": "yellow", "EW": "red"},
        4: {"NS": "red", "EW": "yellow"}
    }
    
    # Get current light colors
    lights = traffic_light_colors.get(current_phase, {"NS": "red", "EW": "red"})
    
    # Create figure
    fig = go.Figure()
    
    # Define intersection center
    center_x, center_y = 0, 0
    road_width = 0.3
    road_length = 2.0
    
    # Define color scale based on traffic density
    def get_road_color(queue_length):
        if queue_length <= 2:
            return "lightgreen"  # Low traffic
        elif queue_length <= 5:
            return "yellow"      # Medium traffic
        elif queue_length <= 8:
            return "orange"      # High traffic
        else:
            return "red"         # Very high traffic
    
    # Draw roads with traffic-based coloring
    # North Road
    north_color = get_road_color(queues[0])
    fig.add_shape(
        type="rect",
        x0=center_x - road_width/2, y0=center_y,
        x1=center_x + road_width/2, y1=center_y + road_length,
        fillcolor=north_color, opacity=0.7,
        line=dict(color="black", width=2)
    )
    
    # East Road
    east_color = get_road_color(queues[1])
    fig.add_shape(
        type="rect",
        x0=center_x, y0=center_y - road_width/2,
        x1=center_x + road_length, y1=center_y + road_width/2,
        fillcolor=east_color, opacity=0.7,
        line=dict(color="black", width=2)
    )
    
    # South Road
    south_color = get_road_color(queues[2])
    fig.add_shape(
        type="rect",
        x0=center_x - road_width/2, y0=center_y - road_length,
        x1=center_x + road_width/2, y1=center_y,
        fillcolor=south_color, opacity=0.7,
        line=dict(color="black", width=2)
    )
    
    # West Road
    west_color = get_road_color(queues[3])
    fig.add_shape(
        type="rect",
        x0=center_x - road_length, y0=center_y - road_width/2,
        x1=center_x, y1=center_y + road_width/2,
        fillcolor=west_color, opacity=0.7,
        line=dict(color="black", width=2)
    )
    
    # Draw intersection center (gray square)
    fig.add_shape(
        type="rect",
        x0=center_x - road_width/2, y0=center_y - road_width/2,
        x1=center_x + road_width/2, y1=center_y + road_width/2,
        fillcolor="lightgray", opacity=0.8,
        line=dict(color="black", width=2)
    )
    
    # Add traffic lights
    light_size = 0.08
    
    # North traffic light (controls north-south traffic)
    ns_light_color = lights["NS"]
    fig.add_shape(
        type="circle",
        x0=center_x - road_width/2 - light_size, y0=center_y + road_width/2,
        x1=center_x - road_width/2, y1=center_y + road_width/2 + light_size,
        fillcolor=ns_light_color, opacity=0.9,
        line=dict(color="black", width=2)
    )
    
    # East traffic light (controls east-west traffic)
    ew_light_color = lights["EW"]
    fig.add_shape(
        type="circle",
        x0=center_x + road_width/2, y0=center_y + road_width/2,
        x1=center_x + road_width/2 + light_size, y1=center_y + road_width/2 + light_size,
        fillcolor=ew_light_color, opacity=0.9,
        line=dict(color="black", width=2)
    )
    
    # South traffic light (same as north for NS direction)
    fig.add_shape(
        type="circle",
        x0=center_x + road_width/2, y0=center_y - road_width/2 - light_size,
        x1=center_x + road_width/2 + light_size, y1=center_y - road_width/2,
        fillcolor=ns_light_color, opacity=0.9,
        line=dict(color="black", width=2)
    )
    
    # West traffic light (same as east for EW direction)
    fig.add_shape(
        type="circle",
        x0=center_x - road_width/2 - light_size, y0=center_y - road_width/2 - light_size,
        x1=center_x - road_width/2, y1=center_y - road_width/2,
        fillcolor=ew_light_color, opacity=0.9,
        line=dict(color="black", width=2)
    )
    
    # Add road labels and queue information
    fig.add_annotation(x=0, y=1.5, text=f"NORTH<br>Queue: {queues[0]}", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=1.5, y=0, text=f"EAST<br>Queue: {queues[1]}", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=0, y=-1.5, text=f"SOUTH<br>Queue: {queues[2]}", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=-1.5, y=0, text=f"WEST<br>Queue: {queues[3]}", showarrow=False, font=dict(size=12))
    
    # Add phase information
    phase_names = {
        0: "North-South Green",
        1: "East-West Green", 
        2: "All Red",
        3: "North-South Yellow",
        4: "East-West Yellow"
    }
    current_phase_name = phase_names.get(current_phase, f"Phase {current_phase}")
    fig.add_annotation(
        x=0, y=-2.5, 
        text=f"Current Phase: {current_phase_name}",
        showarrow=False, 
        font=dict(size=14, color="blue"),
        bgcolor="white",
        bordercolor="blue",
        borderwidth=1
    )
    
    # Configure layout
    fig.update_layout(
        title=f"Intersection: {selected_int}",
        xaxis=dict(range=[-2.5, 2.5], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-3, 2.5], showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        plot_bgcolor="lightblue",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Add traffic legend
    st.markdown("""
    **Traffic Density Legend:**
    - 🟢 **Green**: Low traffic (≤2 vehicles)
    - 🟡 **Yellow**: Medium traffic (3-5 vehicles)  
    - 🟠 **Orange**: High traffic (6-8 vehicles)
    - 🔴 **Red**: Very high traffic (>8 vehicles)
    
    **Traffic Lights:**
    - 🔴 **Red Light**: Stop
    - 🟡 **Yellow Light**: Caution
    - 🟢 **Green Light**: Go
    """)
    
    # Display queue statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("North Queue", queues[0], delta=None)
    with col2:
        st.metric("East Queue", queues[1], delta=None)
    with col3:
        st.metric("South Queue", queues[2], delta=None)
    with col4:
        st.metric("West Queue", queues[3], delta=None)
