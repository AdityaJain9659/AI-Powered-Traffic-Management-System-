#!/usr/bin/env python3
"""
Quick test to start simulation and verify data flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sumo_integration import SumoStreamlitIntegration
import time

def test_simulation_data():
    print("🚦 Testing SUMO Integration with Real-time Data...")
    
    # Create integration instance
    integration = SumoStreamlitIntegration()
    
    print("📊 Getting initial data (should show default zeros)...")
    initial_data = integration.get_current_data()
    if initial_data:
        kpi = initial_data['kpi_data']
        print(f"Initial: Vehicles={kpi['vehicle_count']}, Wait={kpi['avg_wait_time']:.1f}s, Speed={kpi['avg_speed']:.1f} km/h")
    
    print("\n▶️ Starting mock simulation...")
    success = integration.start_simulation("uniform", duration=60, control_mode="adaptive")
    
    if success:
        print("✅ Simulation started successfully!")
        
        # Wait a moment for data to start flowing
        time.sleep(2)
        
        print("\n📈 Real-time data updates:")
        for i in range(10):
            data = integration.get_current_data()
            if data and data['status'] == 'running':
                kpi = data['kpi_data']
                print(f"Update {i+1}: Vehicles={kpi['vehicle_count']}, Wait={kpi['avg_wait_time']:.1f}s, Speed={kpi['avg_speed']:.1f} km/h, Efficiency={kpi['ai_efficiency']:.1f}%")
            else:
                print(f"Update {i+1}: No data or simulation stopped")
            
            time.sleep(1)
        
        print("\n⏹️ Stopping simulation...")
        integration.stop_simulation()
        print("✅ Test completed successfully!")
        
    else:
        print("❌ Failed to start simulation")

if __name__ == "__main__":
    test_simulation_data()
