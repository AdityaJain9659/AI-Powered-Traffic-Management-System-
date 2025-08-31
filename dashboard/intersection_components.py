"""
Intersection Components
Contains intersection control and map components for traffic management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_phase_info(phase):
    """Get modern phase information with colors and icons"""
    phase_data = {
        0: {
            "description": "North-South Flow Active",
            "icon": "fas fa-arrow-up",
            "bg_color": "rgba(16, 185, 129, 0.1)",
            "border_color": "rgba(16, 185, 129, 0.3)",
            "text_color": "#10b981"
        },
        1: {
            "description": "East-West Flow Active", 
            "icon": "fas fa-arrow-right",
            "bg_color": "rgba(16, 185, 129, 0.1)",
            "border_color": "rgba(16, 185, 129, 0.3)",
            "text_color": "#10b981"
        },
        2: {
            "description": "All Directions Stopped",
            "icon": "fas fa-stop",
            "bg_color": "rgba(239, 68, 68, 0.1)",
            "border_color": "rgba(239, 68, 68, 0.3)",
            "text_color": "#ef4444"
        },
        3: {
            "description": "North-South Prepare to Stop",
            "icon": "fas fa-exclamation-triangle",
            "bg_color": "rgba(245, 158, 11, 0.1)",
            "border_color": "rgba(245, 158, 11, 0.3)",
            "text_color": "#f59e0b"
        },
        4: {
            "description": "East-West Prepare to Stop",
            "icon": "fas fa-exclamation-triangle",
            "bg_color": "rgba(245, 158, 11, 0.1)",
            "border_color": "rgba(245, 158, 11, 0.3)",
            "text_color": "#f59e0b"
        }
    }
    return phase_data.get(phase, phase_data[0])


def get_queue_status_info(queue_len):
    """Get queue status with modern styling info"""
    if queue_len <= 2:
        return {
            "label": "Free Flow",
            "class": "free",
            "color": "#10b981",
            "icon": "fa-check-circle"
        }
    elif queue_len <= 5:
        return {
            "label": "Moderate",
            "class": "moderate", 
            "color": "#f59e0b",
            "icon": "fa-exclamation-circle"
        }
    else:
        return {
            "label": "Congested",
            "class": "congested",
            "color": "#ef4444", 
            "icon": "fa-times-circle"
        }


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


def intersection_panel(d):
    """Modern dark-themed intersection control panel with FontAwesome icons"""
    
    ints = list(d["intersections"].keys())
    
    # Modern intersection selector
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <label style="color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; 
                      letter-spacing: 0.5px; margin-bottom: 0.5rem; display: block;">
            <i class="fas fa-map-marker-alt"></i> Select Intersection
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    picked = st.selectbox(
        "Choose intersection:",
        ints, 
        index=ints.index(d.get("selected_intersection", ints[0])),
        label_visibility="collapsed"
    )
    
    node = d["intersections"][picked]
    intersection_name = node.get("name", picked.replace("_", " ").title())
    
    # Modern intersection info card
    current_phase = node['current_phase']
    phase_info = get_phase_info(current_phase)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%); 
                border: 1px solid #404040; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
        <h3 style="color: #ffffff; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-intersection"></i> {intersection_name}
        </h3>
        <div style="background: {phase_info['bg_color']}; border: 1px solid {phase_info['border_color']}; 
                    border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="color: {phase_info['text_color']}; font-size: 1rem; margin-bottom: 0.5rem;">
                <i class="{phase_info['icon']}"></i> Current Phase
            </div>
            <div style="color: #ffffff; font-size: 1.5rem; font-weight: 700;">
                Phase {current_phase}
            </div>
            <div style="color: {phase_info['text_color']}; font-size: 0.9rem; margin-top: 0.5rem;">
                {phase_info['description']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern queue visualization
    st.markdown("""
    <div style="margin: 1.5rem 0 1rem 0;">
        <h4 style="color: #ffffff; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-road"></i> Lane Queue Status
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    directions = ["North", "East", "South", "West"]
    direction_icons = ["fa-arrow-up", "fa-arrow-right", "fa-arrow-down", "fa-arrow-left"]
    
    # Enhanced bar chart with dark theme
    queue_data = []
    for i, (direction, queue_len) in enumerate(zip(directions, node["queues"])):
        queue_data.append({
            "Direction": direction,
            "Queue Length": queue_len,
            "Status": get_queue_status(queue_len)
        })
    
    df = pd.DataFrame(queue_data)
    
    # Create modern bar chart
    fig = px.bar(
        df, 
        x="Direction", 
        y="Queue Length",
        color="Queue Length",
        color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
        title="",
        text="Queue Length"
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont=dict(color='white', size=12),
        marker_line_color='#404040',
        marker_line_width=1
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            gridcolor='rgba(64, 64, 64, 0.3)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(64, 64, 64, 0.3)',
            tickfont=dict(color='white')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Modern queue status cards
    cols = st.columns(4)
    for i, (direction, queue_len, icon) in enumerate(zip(directions, node["queues"], direction_icons)):
        with cols[i]:
            status_info = get_queue_status_info(queue_len)
            st.markdown(f"""
            <div class="queue-card queue-{status_info['class']}">
                <div class="queue-icon">
                    <i class="fas {icon}"></i>
                </div>
                <div class="queue-label">{direction}</div>
                <div class="queue-value">{queue_len}</div>
                <div style="color: {status_info['color']}; font-size: 0.8rem; font-weight: 600;">
                    <i class="fas {status_info['icon']}"></i> {status_info['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def get_intersection_status(avg_queue):
    """Get overall intersection status with modern styling"""
    if avg_queue <= 3:
        return "Optimal Flow"
    elif avg_queue <= 6:
        return "Moderate Traffic"
    else:
        return "Heavy Congestion"


def intersection_map(d):
    """
    Modern dark-themed interactive 4-road intersection map with FontAwesome icons
    """
    
    # Get intersection data
    selected_int = d.get("selected_intersection", list(d["intersections"].keys())[0])
    intersection_data = d["intersections"][selected_int]
    intersection_name = intersection_data.get("name", selected_int.replace("_", " ").title())
    
    # Traffic queues for each road (North, East, South, West)
    queues = intersection_data["queues"]
    current_phase = intersection_data["current_phase"]
    
    # Modern traffic light phases with better colors
    traffic_light_colors = {
        0: {"NS": "#10b981", "EW": "#ef4444"},  # Green, Red
        1: {"NS": "#ef4444", "EW": "#10b981"},  # Red, Green
        2: {"NS": "#ef4444", "EW": "#ef4444"},  # Red, Red
        3: {"NS": "#f59e0b", "EW": "#ef4444"},  # Yellow, Red
        4: {"NS": "#ef4444", "EW": "#f59e0b"}   # Red, Yellow
    }
    
    # Get current light colors
    lights = traffic_light_colors.get(current_phase, {"NS": "#ef4444", "EW": "#ef4444"})
    
    # Create modern dark-themed figure
    fig = go.Figure()
    
    # Define intersection parameters
    center_x, center_y = 0, 0
    road_width = 0.4
    road_length = 2.5
    
    # Modern color scale for roads
    def get_modern_road_color(queue_length):
        if queue_length <= 2:
            return "#10b981"  # Green for free flow
        elif queue_length <= 5:
            return "#f59e0b"  # Yellow for moderate
        elif queue_length <= 8:
            return "#ef4444"  # Red for congested
        else:
            return "#dc2626"  # Dark red for severe
    
    # Enhanced road configurations
    road_configs = [
        (center_x - road_width/2, center_y, center_x + road_width/2, center_y + road_length, "North"),
        (center_x, center_y - road_width/2, center_x + road_length, center_y + road_width/2, "East"),
        (center_x - road_width/2, center_y - road_length, center_x + road_width/2, center_y, "South"),
        (center_x - road_length, center_y - road_width/2, center_x, center_y + road_width/2, "West")
    ]
    
    # Draw roads with modern styling and shadows
    for i, (x0, y0, x1, y1, direction) in enumerate(road_configs):
        road_color = get_modern_road_color(queues[i])
        
        # Add subtle road shadow
        fig.add_shape(
            type="rect",
            x0=x0+0.03, y0=y0-0.03, x1=x1+0.03, y1=y1-0.03,
            fillcolor="rgba(0,0,0,0.3)", line=dict(width=0)
        )
        
        # Add main road with gradient effect
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=road_color, opacity=0.8,
            line=dict(color="#1a1a1a", width=2)
        )
        
        # Add modern road markings
        if direction in ["North", "South"]:
            # Vertical lane divider
            fig.add_shape(
                type="line",
                x0=center_x, y0=y0, x1=center_x, y1=y1,
                line=dict(color="white", width=2, dash="dash")
            )
        else:
            # Horizontal lane divider  
            fig.add_shape(
                type="line",
                x0=x0, y0=center_y, x1=x1, y1=center_y,
                line=dict(color="white", width=2, dash="dash")
            )
    
    # Modern intersection center
    fig.add_shape(
        type="rect",
        x0=center_x - road_width/2, y0=center_y - road_width/2,
        x1=center_x + road_width/2, y1=center_y + road_width/2,
        fillcolor="#1a1a1a", opacity=0.9,
        line=dict(color="#404040", width=2)
    )
    
    # Modern traffic lights with better positioning
    light_size = 0.15
    light_positions = [
        (center_x - road_width/2 - light_size*1.2, center_y + road_width/2 + light_size/2, lights["NS"], "North"),
        (center_x + road_width/2 + light_size/2, center_y + road_width/2 + light_size*1.2, lights["EW"], "East"),
        (center_x + road_width/2 + light_size*1.2, center_y - road_width/2 - light_size/2, lights["NS"], "South"),
        (center_x - road_width/2 - light_size/2, center_y - road_width/2 - light_size*1.2, lights["EW"], "West")
    ]
    
    for x, y, color, direction in light_positions:
        # Modern traffic light pole
        fig.add_shape(
            type="rect",
            x0=x - light_size/6, y0=y - light_size*1.5, x1=x + light_size/6, y1=y + light_size/2,
            fillcolor="#2d2d2d", line=dict(color="#404040", width=1)
        )
        
        # Modern traffic light housing with shadow
        fig.add_shape(
            type="rect",
            x0=x - light_size/2, y0=y - light_size/2, x1=x + light_size/2, y1=y + light_size/2,
            fillcolor="#1a1a1a", line=dict(color="#404040", width=2)
        )
        
        # Active light with glow effect
        fig.add_shape(
            type="circle",
            x0=x - light_size/3, y0=y - light_size/3, x1=x + light_size/3, y1=y + light_size/3,
            fillcolor=color, opacity=0.9,
            line=dict(color="white", width=1)
        )
    
    # Modern annotations with dark theme
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    positions = [(0, 2.2), (2.2, 0.3), (0, -2.2), (-2.2, 0.3)]
    
    for i, (direction, (x, y)) in enumerate(zip(directions, positions)):
        queue_status_info = get_queue_status_info(queues[i])
        
        fig.add_annotation(
            x=x, y=y, 
            text=f"<b>{direction}</b><br>Queue: {queues[i]} vehicles<br><span style='color:{queue_status_info['color']}'>{queue_status_info['label']}</span>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#4f46e5",
            ax=0, ay=-25 if direction in ["NORTH", "SOUTH"] else (-25 if direction == "WEST" else 25),
            bgcolor="rgba(26, 26, 26, 0.95)",
            bordercolor="#4f46e5",
            borderwidth=1,
            borderpad=8,
            font=dict(size=10, color="white")
        )
    
    # Modern phase information
    phase_info = get_phase_info(current_phase)
    
    fig.add_annotation(
        x=0, y=-3.0, 
        text=f"<b>{phase_info['description']}</b><br>{intersection_name}",
        showarrow=False, 
        font=dict(size=12, color="white"),
        bgcolor="rgba(26, 26, 26, 0.9)",
        bordercolor=phase_info['border_color'].replace('rgba', 'rgb').replace(', 0.3)', ')'),
        borderwidth=2,
        borderpad=10
    )
    
    # Modern dark layout
    fig.update_layout(
        title=dict(
            text=f"<b>Smart Intersection: {intersection_name}</b>",
            x=0.5,
            font=dict(size=18, color="white")
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
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="rgba(0,0,0,0)",
        height=550,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    
    # Display the modern plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Modern statistics cards
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="margin-bottom: 1rem;">
                <h4 style="color: #ffffff; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-info-circle"></i> Traffic Status Legend
                </h4>
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 16px; height: 16px; background: #10b981; border-radius: 4px;"></div>
                    <span style="color: #9ca3af;">Free Flow (≤2 vehicles)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 16px; height: 16px; background: #f59e0b; border-radius: 4px;"></div>
                    <span style="color: #9ca3af;">Moderate (3-5 vehicles)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 16px; height: 16px; background: #ef4444; border-radius: 4px;"></div>
                    <span style="color: #9ca3af;">Congested (6+ vehicles)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_vehicles = sum(queues)
        avg_queue = total_vehicles / 4
        peak_direction = directions[queues.index(max(queues))]
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="margin-bottom: 1rem;">
                <h4 style="color: #ffffff; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-chart-bar"></i> Intersection Stats
                </h4>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #9ca3af;">
                <div>
                    <div style="color: #ffffff; font-size: 1.5rem; font-weight: 700;">{total_vehicles}</div>
                    <div style="font-size: 0.8rem;">Total Queued</div>
                </div>
                <div>
                    <div style="color: #ffffff; font-size: 1.5rem; font-weight: 700;">{avg_queue:.1f}</div>
                    <div style="font-size: 0.8rem;">Average Queue</div>
                </div>
                <div style="grid-column: span 2;">
                    <div style="color: #4f46e5; font-weight: 600;">Peak: {peak_direction}</div>
                    <div style="color: {get_queue_status_info(avg_queue)['color']}; font-size: 0.9rem; font-weight: 600;">
                        <i class="fas {get_queue_status_info(avg_queue)['icon']}"></i> {get_intersection_status(avg_queue)}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
