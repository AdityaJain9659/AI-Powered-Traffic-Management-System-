#!/usr/bin/env python3
"""
Test Real SUMO Integration - Verify connection to actual SUMO simulation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sumo_integration import initialize_sumo_integration, SUMO_AVAILABLE
import time

def test_real_sumo_integration():
    print("🚦 Testing REAL SUMO Integration...")
    
    if not SUMO_AVAILABLE:
        print("❌ SUMO modules not available - cannot test real integration")
        return
    
    print("✅ SUMO modules loaded successfully!")
    
    # Create integration instance
    integration = initialize_sumo_integration()
    
    # Get status
    status = integration.get_simulation_status()
    print(f"📊 Simulation Status: {status}")
    
    print("\n▶️ Attempting to start REAL SUMO simulation...")
    try:
        success = integration.start_simulation("uniform", duration=30, control_mode="adaptive")
        
        if success:
            print("🎉 REAL SUMO simulation started successfully!")
            
            # Wait for data to flow
            time.sleep(3)
            
            print("\n📈 Real-time SUMO data:")
            for i in range(10):
                data = integration.get_current_data()
                if data and data['status'] == 'running':
                    kpi = data['kpi_data']
                    print(f"REAL Update {i+1}: Vehicles={kpi['vehicle_count']}, Wait={kpi['avg_wait_time']:.1f}s, Speed={kpi['avg_speed']:.1f} km/h, Efficiency={kpi['ai_efficiency']:.1f}%")
                else:
                    print(f"Update {i+1}: No REAL data yet or simulation stopped")
                
                time.sleep(2)
            
            print("\n⏹️ Stopping REAL SUMO simulation...")
            integration.stop_simulation()
            print("✅ REAL SUMO test completed!")
            
        else:
            print("❌ Failed to start REAL SUMO simulation")
            print("💡 This might be due to missing SUMO config files or SUMO not being properly installed")
            
    except Exception as e:
        print(f"❌ Error testing REAL SUMO: {e}")
        print("💡 Make sure SUMO is properly installed and config files exist")

if __name__ == "__main__":
    test_real_sumo_integration()
