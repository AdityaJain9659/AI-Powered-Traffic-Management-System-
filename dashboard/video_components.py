"""
Video Components
Contains video feed and camera monitoring components
"""

import streamlit as st
from pathlib import Path
from PIL import Image


def video_panel(d):
    """Modern dark-themed video feed panel with FontAwesome icons"""
    
    p = d.get("latest_frame_path")
    if p and Path(p).exists():
        # Modern video container
        st.markdown("""
        <div style="border: 2px solid #404040; border-radius: 12px; 
                    background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%); 
                    padding: 1rem; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">
        """, unsafe_allow_html=True)
        
        st.image(Image.open(p), caption="", use_column_width=True)
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    margin-top: 1rem; padding: 0.75rem; background: rgba(45, 45, 45, 0.5); 
                    border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5rem; color: #ef4444;">
                <i class="fas fa-circle" style="font-size: 0.5rem; animation: pulse 2s infinite;"></i>
                <span style="font-weight: 600;">LIVE</span>
            </div>
            <div style="color: #9ca3af; font-size: 0.85rem;">
                <i class="fas fa-video"></i> Real-time traffic monitoring
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Modern status indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="status-indicator status-online">
                <i class="fas fa-eye"></i> Object Detection
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="status-indicator status-online">
                <i class="fas fa-brain"></i> AI Processing
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="status-indicator status-warning">
                <i class="fas fa-signal"></i> Stream Quality
            </div>
            """, unsafe_allow_html=True)
            
    else:
        # Modern placeholder when no video available
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%); 
                    border: 2px dashed #404040; border-radius: 12px; 
                    padding: 3rem; text-align: center; color: white;">
            <div style="font-size: 4rem; color: #6b7280; margin-bottom: 1rem;">
                <i class="fas fa-video-slash"></i>
            </div>
            <h2 style="color: #ffffff; margin-bottom: 1rem;">Camera Feed</h2>
            <div style="color: #9ca3af; margin-bottom: 1.5rem;">
                <i class="fas fa-spinner fa-spin"></i> Initializing camera connection...
            </div>
            <p style="color: #6b7280;">Traffic monitoring will begin shortly</p>
            <div style="margin-top: 1.5rem;">
                <div class="status-indicator status-error">
                    <i class="fas fa-exclamation-circle"></i> OFFLINE
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
