"""
Analytics Components
Contains time series and performance analytics components
"""

import streamlit as st
import plotly.graph_objects as go


def time_series_panel(d):
    """Modern dark-themed performance analytics with FontAwesome icons"""
    
    ts = d.get("time_series", {})
    if ts and ts.get("t"):
        # Create modern dark-themed time series plot
        fig = go.Figure()
        
        # Add AI performance line with modern styling
        fig.add_trace(go.Scatter(
            x=ts["t"],
            y=ts["rl_avg_travel_time"],
            mode='lines+markers',
            name='AI Optimized',
            line=dict(color='#4f46e5', width=3, shape='spline'),
            marker=dict(size=8, symbol='circle', color='#4f46e5'),
            hovertemplate='<b>AI Optimized</b><br>Time: %{x}s<br>Travel Time: %{y:.1f}s<extra></extra>'
        ))
        
        # Add baseline line with modern styling
        fig.add_trace(go.Scatter(
            x=ts["t"],
            y=ts["baseline_avg_travel_time"],
            mode='lines+markers',
            name='Traditional Control',
            line=dict(color='#ef4444', width=3, dash='dash', shape='spline'),
            marker=dict(size=8, symbol='diamond', color='#ef4444'),
            hovertemplate='<b>Traditional Control</b><br>Time: %{x}s<br>Travel Time: %{y:.1f}s<extra></extra>'
        ))
        
        # Modern dark layout
        fig.update_layout(
            title=dict(
                text="Performance Comparison",
                font=dict(size=16, color='white'),
                x=0.02
            ),
            xaxis_title="Time (seconds)",
            yaxis_title="Travel Time (seconds)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='white'),
            height=320,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='white')
            ),
            xaxis=dict(
                gridcolor='rgba(64, 64, 64, 0.3)',
                tickfont=dict(color='white'),
                title=dict(font=dict(color='white'))
            ),
            yaxis=dict(
                gridcolor='rgba(64, 64, 64, 0.3)', 
                tickfont=dict(color='white'),
                title=dict(font=dict(color='white'))
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Modern performance summary cards
        current_improvement = (ts["baseline_avg_travel_time"][-1] - ts["rl_avg_travel_time"][-1]) / ts["baseline_avg_travel_time"][-1] * 100
        avg_improvement = sum((b - r) / b * 100 for b, r in zip(ts["baseline_avg_travel_time"], ts["rl_avg_travel_time"])) / len(ts["t"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            improvement_class = "delta-positive" if current_improvement > 0 else "delta-negative"
            improvement_icon = "fa-chart-line-up" if current_improvement > 0 else "fa-chart-line-down"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas {improvement_icon}"></i>
                </div>
                <div class="metric-label">Current Improvement</div>
                <div class="metric-value">{current_improvement:.1f}%</div>
                <div class="metric-delta {improvement_class}">
                    <i class="fas fa-rocket"></i> Real-time gain
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_class = "delta-positive" if avg_improvement > 0 else "delta-negative"
            avg_icon = "fa-trophy" if avg_improvement > 0 else "fa-chart-line-down"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">
                    <i class="fas {avg_icon}"></i>
                </div>
                <div class="metric-label">Average Improvement</div>
                <div class="metric-value">{avg_improvement:.1f}%</div>
                <div class="metric-delta {avg_class}">
                    <i class="fas fa-brain"></i> Session average
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%); 
                    border: 1px solid #404040; border-radius: 12px; 
                    padding: 3rem; text-align: center;">
            <div style="font-size: 3rem; color: #f59e0b; margin-bottom: 1rem;">
                <i class="fas fa-chart-line"></i>
            </div>
            <h3 style="color: #ffffff; margin-bottom: 1rem;">Collecting Analytics Data</h3>
            <p style="color: #9ca3af;">Performance trends will appear here once the system starts collecting metrics</p>
            <div style="margin-top: 1.5rem;">
                <div class="status-indicator status-warning">
                    <i class="fas fa-hourglass-half"></i> Initializing
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
