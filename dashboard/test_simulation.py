#!/usr/bin/env python3
"""
Test script to verify SUMO integration and mock simulation
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sumo_integration import SumoStreamlitIntegration
import time

def test_mock_simulation():
    """Test the mock simulation functionality"""
    print("🧪 Testing Mock Simulation Integration")
    print("=" * 50)
    
    # Create integration instance
    integration = SumoStreamlitIntegration()
    
    print("📊 Testing simulation startup...")
    success = integration.start_simulation("uniform", 60, "adaptive")
    
    if success:
        print("✅ Simulation started successfully!")
        
        # Let it run for a few seconds
        print("⏱️ Running simulation for 5 seconds...")
        time.sleep(5)
        
        # Check data
        data = integration.get_current_data()
        if data:
            print("✅ Data retrieved successfully!")
            print(f"📈 Vehicle Count: {data['kpi_data']['vehicle_count']}")
            print(f"⏱️ Avg Wait Time: {data['kpi_data']['avg_wait_time']:.1f}s")
            print(f"🏃 Avg Speed: {data['kpi_data']['avg_speed']:.1f} km/h")
            print(f"🤖 AI Efficiency: {data['kpi_data']['ai_efficiency']:.1f}%")
            print(f"🚦 Current Phase: {data['intersection_data']['current_phase']}")
            print(f"📊 Status: {data['status']}")
        else:
            print("❌ No data retrieved")
        
        # Stop simulation
        integration.stop_simulation()
        print("🛑 Simulation stopped")
        
    else:
        print("❌ Failed to start simulation")
    
    print("\n🎯 Test complete!")

if __name__ == "__main__":
    test_mock_simulation()
