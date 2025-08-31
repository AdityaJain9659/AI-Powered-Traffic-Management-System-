"""
Configuration settings for the AI Traffic Management Dashboard
"""

from pathlib import Path

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "page_title": "AI Traffic Management",
    "page_icon": "🚦", 
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}

# File Paths
DATA_DIR = Path(__file__).parents[1] / "data"
DATA_FILE = DATA_DIR / "dashboard_data.json"

# Refresh Settings
DEFAULT_REFRESH_RATE = 1.0
MIN_REFRESH_RATE = 0.5
MAX_REFRESH_RATE = 5.0

# Status Colors
STATUS_COLORS = {
    "online": "#10b981",
    "warning": "#f59e0b", 
    "error": "#ef4444",
    "neutral": "#6b7280"
}

# Traffic Status Thresholds
TRAFFIC_THRESHOLDS = {
    "free_flow": 2,
    "moderate": 5,
    "congested": 8
}

# Performance Metrics
PERFORMANCE_THRESHOLDS = {
    "good_efficiency": 10,
    "acceptable_efficiency": 0,
    "low_wait_time": 20,
    "moderate_wait_time": 40,
    "low_density_vehicles": 300,
    "medium_density_vehicles": 600
}

# Chart Configuration
CHART_CONFIG = {
    "height": {
        "kpi": 280,
        "time_series": 320,
        "intersection_map": 550
    },
    "colors": {
        "ai_optimized": "#4f46e5",
        "traditional": "#ef4444",
        "free_flow": "#10b981",
        "moderate": "#f59e0b",
        "congested": "#ef4444",
        "severe": "#dc2626"
    }
}
