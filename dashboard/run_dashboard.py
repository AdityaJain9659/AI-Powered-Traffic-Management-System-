#!/usr/bin/env python3
"""
Startup script for AI Traffic Management Dashboard
Handles SUMO integration setup and launches the Streamlit dashboard
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_sumo_installation():
    """Check if SUMO is properly installed"""
    try:
        import traci
        import sumolib
        print("✅ SUMO Python libraries found")
        return True
    except ImportError:
        print("❌ SUMO Python libraries not found")
        print("Please install SUMO with Python support")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dashboard_requirements():
    """Install dashboard-specific requirements"""
    req_file = Path(__file__).parent / "requirements_dashboard.txt"
    if req_file.exists():
        print("Installing dashboard requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        print("✅ Dashboard requirements installed")
    else:
        print("⚠️ Dashboard requirements file not found")

def setup_environment():
    """Setup environment variables and paths"""
    # Add SUMO tools to path if needed
    if "SUMO_HOME" in os.environ:
        sumo_tools = os.path.join(os.environ["SUMO_HOME"], "tools")
        if sumo_tools not in sys.path:
            sys.path.append(sumo_tools)
            print(f"✅ Added SUMO tools to path: {sumo_tools}")
    else:
        print("⚠️ SUMO_HOME environment variable not set")
        print("Please set SUMO_HOME to your SUMO installation directory")

def create_sample_data():
    """Create sample data file if it doesn't exist"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    sample_data_file = data_dir / "dashboard_data.json"
    
    if not sample_data_file.exists():
        sample_data = {
            "timestamp": "2025-09-02T10:00:00",
            "simulation_time": 0,
            "status": "demo",
            "kpi_data": {
                "ai_efficiency": 85.0,
                "traditional_efficiency": 70.0,
                "avg_wait_time": 25.5,
                "avg_speed": 45.2,
                "vehicle_count": 150,
                "queue_length": 5,
                "congestion_level": "moderate"
            },
            "intersection_data": {
                "current_phase": 0,
                "phase_duration": 30.0,
                "signal_state": "GGrrGGrr",
                "phase_name": "North-South Green",
                "waiting_vehicles": 12,
                "per_lane_queues": {
                    "1i_0": 3, "1i_1": 2,
                    "2i_0": 1, "2i_1": 2,
                    "3i_0": 4, "3i_1": 1,
                    "4i_0": 2, "4i_1": 3
                },
                "directional_flow": {
                    "NS": 45.0, "EW": 38.0, "NE": 12.0,
                    "NW": 8.0, "SE": 15.0, "SW": 10.0
                }
            },
            "time_series_data": {
                "timestamps": ["2025-09-02T10:00:00"],
                "efficiency_scores": [85.0],
                "wait_times": [25.5],
                "vehicle_counts": [150],
                "queue_lengths": [5],
                "speeds": [45.2]
            },
            "camera_feeds": [
                {"id": "cam_1", "location": "North Approach", "status": "online"},
                {"id": "cam_2", "location": "South Approach", "status": "online"},
                {"id": "cam_3", "location": "East Approach", "status": "online"},
                {"id": "cam_4", "location": "West Approach", "status": "online"}
            ]
        }
        
        import json
        with open(sample_data_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✅ Created sample data file: {sample_data_file}")

def launch_dashboard(port=8501, debug=False):
    """Launch the Streamlit dashboard"""
    dashboard_path = Path(__file__).parent / "dashboard.py"
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(dashboard_path),
        "--server.port", str(port),
        "--server.address", "localhost"
    ]
    
    if debug:
        cmd.extend(["--logger.level", "debug"])
    
    print(f"🚀 Launching dashboard on http://localhost:{port}")
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="AI Traffic Management Dashboard Launcher")
    parser.add_argument("--port", type=int, default=8501, help="Port to run dashboard on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies")
    parser.add_argument("--setup-only", action="store_true", help="Setup environment only, don't launch")
    
    args = parser.parse_args()
    
    print("🚦 AI Traffic Management Dashboard Setup")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        install_dashboard_requirements()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies")
        return 1
    
    # Check SUMO
    sumo_available = check_sumo_installation()
    if not sumo_available:
        print("⚠️ SUMO not available - dashboard will run in demo mode")
    
    # Setup environment
    setup_environment()
    
    # Create sample data
    create_sample_data()
    
    if args.setup_only:
        print("✅ Setup complete")
        return 0
    
    # Launch dashboard
    try:
        launch_dashboard(args.port, args.debug)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
