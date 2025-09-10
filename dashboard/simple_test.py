#!/usr/bin/env python3
"""
Simple test script without Streamlit dependencies
"""

import sys
import os
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import random
import json

# Define classes locally for testing
class SimulationState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class TrafficState:
    timestamp: float
    vehicle_count: int
    waiting_vehicles: int
    avg_waiting_time: float
    avg_speed: float
    queue_length: int
    current_phase: int
    phase_duration: float
    per_lane_queues: Dict[str, int] = None
    per_lane_waiting_times: Dict[str, float] = None
    per_lane_vehicle_counts: Dict[str, int] = None
    directional_flow: Dict[str, float] = None
    signal_phase_timing: Dict[str, float] = None
    congestion_per_lane: Dict[str, str] = None
    emergency_vehicles: List[str] = None
    pedestrian_waiting: int = None

@dataclass
class LiveMetrics:
    efficiency_score: float
    simulation_time: float

class SimpleTrafficSimulator:
    """Simple traffic simulator for testing"""
    def __init__(self):
        self.is_running = False
        self.simulation_state = SimulationState.STOPPED
        self._step_count = 0
        self.current_data = None
        self.data_lock = threading.Lock()
        
    def start_simulation(self, scenario="uniform", duration=60):
        """Start the simulation"""
        self.simulation_state = SimulationState.RUNNING
        self.is_running = True
        self._step_count = 0
        
        # Start simulation thread
        self.sim_thread = threading.Thread(
            target=self._simulation_loop,
            args=(duration,),
            daemon=True
        )
        self.sim_thread.start()
        
        return True
    
    def _simulation_loop(self, duration):
        """Simulation loop"""
        start_time = time.time()
        
        while self.is_running and (time.time() - start_time) < duration:
            self._step_count += 1
            
            # Generate traffic data
            time_factor = (self._step_count % 120) / 120.0
            rush_hour = 0.5 + 0.5 * abs(0.5 - time_factor)
            
            base_vehicles = int(80 + 40 * rush_hour + random.randint(-10, 10))
            base_waiting = int(base_vehicles * 0.15 + random.randint(0, 8))
            
            traffic_state = TrafficState(
                timestamp=time.time() - start_time,
                vehicle_count=base_vehicles,
                waiting_vehicles=base_waiting,
                avg_waiting_time=15.0 + 25.0 * rush_hour + random.uniform(-5, 5),
                avg_speed=45.0 - 15.0 * rush_hour + random.uniform(-3, 3),
                queue_length=int(3 + 8 * rush_hour + random.randint(-2, 3)),
                current_phase=int(self._step_count / 30) % 4,
                phase_duration=30.0,
                per_lane_queues={
                    "1i_0": random.randint(0, int(5 * rush_hour) + 1),
                    "2i_0": random.randint(0, int(3 * rush_hour) + 1),
                    "3i_0": random.randint(0, int(4 * rush_hour) + 1),
                    "4i_0": random.randint(0, int(5 * rush_hour) + 1)
                },
                directional_flow={
                    "NS": 30 + 30 * rush_hour + random.uniform(-5, 5),
                    "EW": 25 + 25 * rush_hour + random.uniform(-4, 4),
                    "NE": 5 + 15 * rush_hour + random.uniform(-2, 2)
                }
            )
            
            # Calculate efficiency
            base_efficiency = 95.0
            waiting_penalty = min(20.0, traffic_state.avg_waiting_time * 0.5)
            queue_penalty = min(15.0, traffic_state.queue_length * 1.5)
            efficiency = max(60.0, base_efficiency - waiting_penalty - queue_penalty)
            
            live_metrics = LiveMetrics(
                efficiency_score=efficiency,
                simulation_time=time.time() - start_time
            )
            
            # Update dashboard data
            self._update_data(traffic_state, live_metrics)
            
            time.sleep(1.0)
        
        self.is_running = False
        self.simulation_state = SimulationState.STOPPED
    
    def _update_data(self, traffic_state, live_metrics):
        """Update the dashboard data"""
        with self.data_lock:
            self.current_data = {
                "timestamp": datetime.now().isoformat(),
                "simulation_time": traffic_state.timestamp,
                "status": "running" if self.is_running else "stopped",
                "kpi_data": {
                    "ai_efficiency": live_metrics.efficiency_score,
                    "traditional_efficiency": max(0, live_metrics.efficiency_score - 15),
                    "avg_wait_time": traffic_state.avg_waiting_time,
                    "avg_speed": traffic_state.avg_speed,
                    "vehicle_count": traffic_state.vehicle_count,
                    "queue_length": traffic_state.queue_length,
                    "congestion_level": "moderate"
                },
                "intersection_data": {
                    "current_phase": traffic_state.current_phase,
                    "phase_duration": traffic_state.phase_duration,
                    "waiting_vehicles": traffic_state.waiting_vehicles,
                    "per_lane_queues": traffic_state.per_lane_queues,
                    "directional_flow": traffic_state.directional_flow
                }
            }
    
    def get_current_data(self):
        """Get current data (thread-safe)"""
        with self.data_lock:
            return self.current_data.copy() if self.current_data else None
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False

def test_traffic_simulator():
    """Test the traffic simulator"""
    print("🧪 Testing Simple Traffic Simulator")
    print("=" * 50)
    
    simulator = SimpleTrafficSimulator()
    
    print("📊 Starting simulation...")
    success = simulator.start_simulation("uniform", 10)
    
    if success:
        print("✅ Simulation started successfully!")
        
        # Let it run for a few seconds and check data
        for i in range(6):
            time.sleep(1)
            data = simulator.get_current_data()
            if data:
                print(f"[{i+1}s] 🚗 Vehicles: {data['kpi_data']['vehicle_count']}, "
                      f"⏱️ Wait: {data['kpi_data']['avg_wait_time']:.1f}s, "
                      f"🤖 Efficiency: {data['kpi_data']['ai_efficiency']:.1f}%")
            else:
                print(f"[{i+1}s] ❌ No data")
        
        # Stop simulation
        simulator.stop_simulation()
        print("🛑 Simulation stopped")
        
        # Final data check
        final_data = simulator.get_current_data()
        if final_data:
            print(f"📊 Final Status: {final_data['status']}")
    else:
        print("❌ Failed to start simulation")
    
    print("\n🎯 Test complete!")

if __name__ == "__main__":
    test_traffic_simulator()
