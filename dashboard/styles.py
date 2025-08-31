"""
Dashboard Styles
Contains all CSS styling for the AI Traffic Management Dashboard
"""

def get_main_css():
    """Returns the main CSS styles for the dashboard"""
    return """
<style>
    /* Import modern icons font */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #262626 100%);
        color: #ffffff;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Card styling */
    .dashboard-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        border: 1px solid #404040;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #4f46e5;
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4f46e5, #06b6d4);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .delta-positive {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .delta-negative {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    .delta-neutral {
        background: rgba(107, 114, 128, 0.1);
        color: #6b7280;
        border: 1px solid rgba(107, 114, 128, 0.2);
    }
    
    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #262626 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #9ca3af;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(79, 70, 229, 0.1);
        color: #4f46e5;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #06b6d4) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    /* FontAwesome icons for tabs using CSS */
    .stTabs [data-baseweb="tab"]:nth-child(1)::before {
        content: "\\f1e6";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    .stTabs [data-baseweb="tab"]:nth-child(2)::before {
        content: "\\f03d";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    .stTabs [data-baseweb="tab"]:nth-child(3)::before {
        content: "\\f201";
        font-family: "Font Awesome 6 Free";
        font-weight: 900;
        margin-right: 8px;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-online {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    
    /* Queue status cards */
    .queue-card {
        background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #404040;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .queue-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    
    .queue-free::before { background: #10b981; }
    .queue-moderate::before { background: #f59e0b; }
    .queue-congested::before { background: #ef4444; }
    
    .queue-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .queue-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .queue-label {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #262626 100%);
        border-right: 1px solid #333;
    }
    
    /* Plotly charts dark theme */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #333;
    }
    
    .section-icon {
        font-size: 1.5rem;
        background: linear-gradient(135deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    
    /* Timeline styling */
    .timeline-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        border-radius: 12px;
        border: 1px solid #404040;
    }
    
    .timeline-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4f46e5;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #06b6d4;
    }
</style>
"""
