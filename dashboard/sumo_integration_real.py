#!/usr/bin/env python3
"""
SUMO Integration Module for Streamlit Dashboard - REAL SUMO VERSION
Provides real-time data from SUMO simulation to Streamlit frontend
"""

import os
import sys
import time
import threading
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import streamlit as st
from dataclasses import dataclass
from enum import Enum
import random

# Add SUMO traffic simulation path
SUMO_PATH = os.path.join(os.path.dirname(__file__), "..", "sumo", "Traffic-simulation-rl")
sys.path.append(SUMO_PATH)

# Try to import SUMO modules first
SUMO_AVAILABLE = False
try:
    from traci_manager import TraciManager, TrafficState, SimulationState
    from live_metrics import MetricsCollector, LiveMetrics
    from signal_controller import SignalController
    SUMO_AVAILABLE = True
    print("✅ Real SUMO modules loaded successfully!")
except ImportError as e:
    print(f"⚠️ SUMO modules not available: {e}")
    SUMO_AVAILABLE = False

# Define fallback classes if SUMO modules are not available
if not SUMO_AVAILABLE:
    @dataclass
    class TrafficState:
        """Fallback TrafficState class"""
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

    class SimulationState(Enum):
        """Fallback SimulationState enum"""
        STOPPED = "stopped"
        RUNNING = "running"
        PAUSED = "paused"
        ERROR = "error"

    @dataclass
    class LiveMetrics:
        """Fallback LiveMetrics class"""
        timestamp: float
        simulation_time: float
        vehicle_count: int
        waiting_vehicles: int
        avg_waiting_time: float
        avg_speed: float
        queue_length: int
        current_phase: int
        phase_duration: float
        efficiency_score: float
        congestion_level: str
        throughput: float
        density: float

    class FallbackTraciManager:
        """Mock TraCI manager for demo purposes"""
        def __init__(self):
            self.simulation_state = SimulationState.STOPPED
            self.is_running = False
            self._simulation_time = 0
            self._step_count = 0
            
        def start_simulation(self, config_file: str) -> bool:
            st.warning("⚠️ SUMO not available - using simulation mode")
            self.simulation_state = SimulationState.RUNNING
            self.is_running = True
            self._step_count = 0
            return True
        
        def stop_simulation(self):
            self.simulation_state = SimulationState.STOPPED
            self.is_running = False
        
        def step_simulation(self, steps: int = 1) -> bool:
            self._simulation_time += steps
            self._step_count += steps
            return True
        
        def is_simulation_running(self) -> bool:
            return self.is_running
        
        def get_traffic_state(self) -> Optional[TrafficState]:
            if not self.is_running:
                return None
            
            # Generate more realistic simulated traffic data that changes over time
            time_factor = (self._step_count % 120) / 120.0  # 2-minute cycles
            rush_hour = 0.5 + 0.5 * abs(0.5 - time_factor)  # Traffic intensity
            
            base_vehicles = int(80 + 40 * rush_hour + random.randint(-10, 10))
            base_waiting = int(base_vehicles * 0.15 + random.randint(0, 8))
            
            return TrafficState(
                timestamp=self._simulation_time,
                vehicle_count=base_vehicles,
                waiting_vehicles=base_waiting,
                avg_waiting_time=15.0 + 25.0 * rush_hour + random.uniform(-5, 5),
                avg_speed=45.0 - 15.0 * rush_hour + random.uniform(-3, 3),
                queue_length=base_waiting,
                current_phase=random.randint(0, 3),
                phase_duration=random.uniform(20, 45),
                per_lane_queues={f"lane_{i}": random.randint(0, 8) for i in range(1, 5)},
                per_lane_waiting_times={f"lane_{i}": random.uniform(10, 40) for i in range(1, 5)},
                per_lane_vehicle_counts={f"lane_{i}": random.randint(5, 15) for i in range(1, 5)},
                directional_flow={f"dir_{i}": random.uniform(0.3, 0.8) for i in range(4)},
                emergency_vehicles=[],
                pedestrian_waiting=random.randint(0, 3)
            )
        
        def get_signal_info(self) -> Dict[str, Any]:
            phases = ["rrrr", "GGrr", "yyrr", "rrGG", "rryy"]
            return {
                "state": random.choice(phases),
                "phase_name": f"Phase {random.randint(0, 4)}",
                "remaining_time": random.uniform(10, 30)
            }

    class FallbackMetricsCollector:
        """Mock metrics collector"""
        def __init__(self, traci_manager):
            self.traci_manager = traci_manager
            
        def get_current_metrics(self) -> Optional[LiveMetrics]:
            if not self.traci_manager.is_running:
                return None
                
            traffic_state = self.traci_manager.get_traffic_state()
            if not traffic_state:
                return None
                
            return LiveMetrics(
                timestamp=time.time(),
                simulation_time=traffic_state.timestamp,
                vehicle_count=traffic_state.vehicle_count,
                waiting_vehicles=traffic_state.waiting_vehicles,
                avg_waiting_time=traffic_state.avg_waiting_time,
                avg_speed=traffic_state.avg_speed,
                queue_length=traffic_state.queue_length,
                current_phase=traffic_state.current_phase,
                phase_duration=traffic_state.phase_duration,
                efficiency_score=85.0 + random.uniform(-5, 10),  # Mock AI efficiency
                congestion_level="moderate",
                throughput=traffic_state.vehicle_count * 0.8,
                density=traffic_state.vehicle_count / 100.0
            )
        
        def stop_collection(self):
            pass

    class FallbackSignalController:
        """Mock signal controller"""
        def __init__(self, traci_manager):
            self.traci_manager = traci_manager
            
        def make_decision(self, traffic_state) -> Dict[str, Any]:
            return {"phase": random.randint(0, 3), "duration": 30}
            
        def execute_decision(self, decision):
            pass
            
        def change_signal_phase(self, phase_id: int, duration: float) -> bool:
            return True

class SumoStreamlitIntegration:
    """Real-time SUMO integration for Streamlit dashboard"""
    
    def __init__(self):
        self.traci_manager = None
        self.metrics_collector = None
        self.signal_controller = None
        self.is_running = False
        self.simulation_thread = None
        self.data_lock = threading.Lock()
        self.current_data = None
        self.simulation_configs = {
            "uniform": "Sumo_env/Single intersection lhd/uniform_simulation.sumocfg",
            "tidal": "Sumo_env/Single intersection lhd/tidal_simulation.sumocfg",
            "asymmetric": "Sumo_env/Single intersection lhd/asymmetric_simulation.sumocfg",
            "congested": "Sumo_env/Single intersection lhd/congested_simulation.sumocfg",
            "random": "Sumo_env/Single intersection lhd/random_simulation.sumocfg",
            "enhanced": "Sumo_env/Single intersection lhd/cross_enhanced.sumocfg"
        }
        
    def initialize_components(self):
        """Initialize SUMO components"""
        try:
            if SUMO_AVAILABLE:
                # Use real SUMO classes
                print("🚦 Initializing real SUMO components...")
                self.traci_manager = TraciManager()
                self.metrics_collector = MetricsCollector(self.traci_manager)
                self.signal_controller = SignalController(self.traci_manager)
                st.info("✅ Real SUMO components initialized!")
            else:
                # Use fallback classes
                print("🔄 Initializing fallback simulation components...")
                self.traci_manager = FallbackTraciManager()
                self.metrics_collector = FallbackMetricsCollector(self.traci_manager)
                self.signal_controller = FallbackSignalController(self.traci_manager)
                st.warning("🔄 Using fallback simulation components")
            return True
        except Exception as e:
            st.error(f"Failed to initialize SUMO components: {e}")
            print(f"Error details: {e}")
            return False
    
    def start_simulation(self, scenario: str = "uniform", duration: int = 3600, control_mode: str = "adaptive") -> bool:
        """Start SUMO simulation with specified parameters"""
        try:
            # Initialize components
            if not self.initialize_components():
                return False
            
            if SUMO_AVAILABLE:
                # Use real SUMO simulation
                st.success("🚦 Starting REAL SUMO simulation!")
                
                # Get config file for scenario
                config_file = self.simulation_configs.get(scenario)
                if not config_file:
                    st.error(f"Unknown scenario: {scenario}")
                    return False
                
                # Build full path to config
                full_config_path = os.path.join(SUMO_PATH, config_file)
                if not os.path.exists(full_config_path):
                    st.error(f"Config file not found: {full_config_path}")
                    return False
                
                # Start real SUMO simulation
                success = self.traci_manager.start_simulation(full_config_path)
                if not success:
                    st.error("Failed to start SUMO simulation")
                    return False
                
                # Set running state
                self.is_running = True
                
                # Start real simulation thread
                self.simulation_thread = threading.Thread(
                    target=self._run_real_simulation_loop,
                    args=(duration, control_mode),
                    daemon=True
                )
                self.simulation_thread.start()
                
            else:
                # Use fallback mock simulation
                st.warning("🔄 Starting simulation in DEMO mode with mock data")
                
                # Set running state
                self.is_running = True
                
                # Start mock simulation thread
                self.simulation_thread = threading.Thread(
                    target=self._run_mock_simulation_loop,
                    args=(duration, control_mode),
                    daemon=True
                )
                self.simulation_thread.start()
                
            return True
            
        except Exception as e:
            st.error(f"Failed to start simulation: {e}")
            print(f"Simulation start error: {e}")
            return False

    def _run_real_simulation_loop(self, duration: int, control_mode: str):
        """Real SUMO simulation loop"""
        try:
            print(f"🚦 Starting REAL SUMO simulation loop for {duration}s in {control_mode} mode")
            current_time = 0
            
            # Initialize with some data immediately
            initial_state = self.traci_manager.get_traffic_state()
            initial_metrics = self.metrics_collector.get_current_metrics()
            if initial_state and initial_metrics:
                self._update_dashboard_data(initial_state, initial_metrics)
            
            while current_time < duration and self.is_running:
                # Step SUMO simulation
                self.traci_manager.step_simulation(1)
                current_time += 1
                
                # Get real traffic state from SUMO
                traffic_state = self.traci_manager.get_traffic_state()
                if traffic_state:
                    # Get real metrics from SUMO
                    live_metrics = self.metrics_collector.get_current_metrics()
                    
                    # Apply traffic control based on mode
                    if control_mode == "adaptive" and live_metrics:
                        decision = self.signal_controller.make_decision(traffic_state)
                        self.signal_controller.execute_decision(decision)
                    
                    # Update dashboard data
                    self._update_dashboard_data(traffic_state, live_metrics)
                
                # Real-time logging every 10 seconds
                if current_time % 10 == 0:
                    print(f"⏱️  REAL SUMO Time {current_time}s: Vehicles={traffic_state.vehicle_count if traffic_state else 0}, Wait={traffic_state.avg_waiting_time if traffic_state else 0:.1f}s, Efficiency={live_metrics.efficiency_score if live_metrics else 0:.1f}%")
                
                time.sleep(0.5)  # Faster update for real SUMO
                
        except Exception as e:
            print(f"Real SUMO simulation error: {e}")
            st.error(f"Real simulation error: {e}")
        finally:
            print("🛑 Real SUMO simulation stopped")
            self.is_running = False

    def _run_mock_simulation_loop(self, duration: int, control_mode: str):
        """Mock simulation loop for demo mode"""
        try:
            print(f"🚦 Starting mock simulation loop for {duration}s in {control_mode} mode")
            current_time = 0
            
            # Initialize with some data immediately
            initial_state = self.traci_manager.get_traffic_state()
            initial_metrics = self.metrics_collector.get_current_metrics()
            if initial_state and initial_metrics:
                self._update_dashboard_data(initial_state, initial_metrics)
            
            while current_time < duration and self.is_running:
                # Step simulation
                self.traci_manager.step_simulation(1)
                current_time += 1
                
                # Get mock traffic state
                traffic_state = self.traci_manager.get_traffic_state()
                if traffic_state:
                    # Get mock metrics
                    live_metrics = self.metrics_collector.get_current_metrics()
                    
                    # Update dashboard data
                    self._update_dashboard_data(traffic_state, live_metrics)
                
                # Logging every 10 seconds
                if current_time % 10 == 0:
                    print(f"⏱️  Mock Time {current_time}s: Vehicles={traffic_state.vehicle_count if traffic_state else 0}, Wait={traffic_state.avg_waiting_time if traffic_state else 0:.1f}s, Efficiency={live_metrics.efficiency_score if live_metrics else 0:.1f}%")
                
                time.sleep(1.0)  # 1 second delay for demo
                
        except Exception as e:
            print(f"Mock simulation error: {e}")
        finally:
            print("🛑 Mock simulation stopped")
            self.is_running = False
    
    def _update_dashboard_data(self, traffic_state, live_metrics = None):
        """Update dashboard data with current simulation state"""
        with self.data_lock:
            try:
                # Get signal information
                signal_info = self.traci_manager.get_signal_info()
                
                # Create dashboard data structure
                dashboard_data = {
                    "timestamp": datetime.now().isoformat(),
                    "simulation_time": traffic_state.timestamp,
                    "status": "running" if self.is_running else "stopped",
                    
                    # KPI Data
                    "kpi_data": {
                        "ai_efficiency": live_metrics.efficiency_score if live_metrics else 85.0,
                        "traditional_efficiency": max(0, (live_metrics.efficiency_score - 15) if live_metrics else 70.0),
                        "avg_wait_time": traffic_state.avg_waiting_time,
                        "avg_speed": traffic_state.avg_speed * 3.6,  # Convert m/s to km/h
                        "vehicle_count": traffic_state.vehicle_count,
                        "queue_length": traffic_state.queue_length,
                        "congestion_level": self._get_congestion_level(traffic_state.queue_length)
                    },
                    
                    # Intersection Data
                    "intersection_data": {
                        "current_phase": traffic_state.current_phase,
                        "phase_duration": traffic_state.phase_duration,
                        "signal_state": signal_info.get("state", "rrrr"),
                        "phase_name": signal_info.get("phase_name", f"Phase {traffic_state.current_phase}"),
                        "waiting_vehicles": traffic_state.waiting_vehicles,
                        "per_lane_queues": traffic_state.per_lane_queues or {},
                        "per_lane_waiting_times": traffic_state.per_lane_waiting_times or {},
                        "directional_flow": traffic_state.directional_flow or {}
                    },
                    
                    # Time Series Data
                    "time_series_data": {
                        "timestamps": [datetime.now().isoformat()],
                        "efficiency_scores": [live_metrics.efficiency_score if live_metrics else 85.0],
                        "wait_times": [traffic_state.avg_waiting_time],
                        "vehicle_counts": [traffic_state.vehicle_count],
                        "queue_lengths": [traffic_state.queue_length],
                        "speeds": [traffic_state.avg_speed * 3.6]
                    },
                    
                    # Enhanced metrics
                    "enhanced_metrics": {
                        "per_lane_vehicle_counts": traffic_state.per_lane_vehicle_counts or {},
                        "congestion_per_lane": traffic_state.congestion_per_lane or {},
                        "emergency_vehicles": traffic_state.emergency_vehicles or [],
                        "pedestrian_waiting": traffic_state.pedestrian_waiting or 0,
                        "signal_phase_timing": traffic_state.signal_phase_timing or {}
                    },
                    
                    # Video/Camera simulation (placeholder)
                    "camera_feeds": [
                        {"id": "cam_1", "location": "North Approach", "status": "online", "frame": None},
                        {"id": "cam_2", "location": "South Approach", "status": "online", "frame": None},
                        {"id": "cam_3", "location": "East Approach", "status": "online", "frame": None},
                        {"id": "cam_4", "location": "West Approach", "status": "online", "frame": None}
                    ]
                }
                
                self.current_data = dashboard_data
                
            except Exception as e:
                st.error(f"Error updating dashboard data: {e}")
                # Create minimal fallback data
                self.current_data = {
                    "timestamp": datetime.now().isoformat(),
                    "simulation_time": 0,
                    "status": "error",
                    "kpi_data": {
                        "ai_efficiency": 0,
                        "traditional_efficiency": 0,
                        "avg_wait_time": 0,
                        "avg_speed": 0,
                        "vehicle_count": 0,
                        "queue_length": 0,
                        "congestion_level": "unknown"
                    }
                }
    
    def _get_congestion_level(self, queue_length: int) -> str:
        """Get congestion level based on queue length"""
        if queue_length <= 2:
            return "free_flow"
        elif queue_length <= 5:
            return "moderate"
        elif queue_length <= 8:
            return "congested"
        else:
            return "severe"
    
    def _get_default_dashboard_data(self) -> Dict[str, Any]:
        """Provide default dashboard data when simulation is not running"""
        from datetime import datetime
        
        return {
            "timestamp": datetime.now().isoformat(),
            "simulation_time": 0.0,
            "status": "stopped",
            
            # Default KPI Data
            "kpi_data": {
                "ai_efficiency": 0.0,
                "traditional_efficiency": 0.0,
                "avg_wait_time": 0.0,
                "avg_speed": 0.0,
                "vehicle_count": 0,
                "queue_length": 0.0,
                "congestion_level": "None"
            },
            
            # Default Intersection Data
            "intersection_data": {
                "current_phase": 0,
                "phase_duration": 0.0,
                "signal_state": "rrrr",
                "phase_name": "Stopped",
                "waiting_vehicles": 0,
                "per_lane_queues": {},
                "per_lane_waiting_times": {},
                "directional_flow": {}
            },
            
            # Default Time Series Data
            "time_series_data": {
                "timestamps": [datetime.now().isoformat()],
                "efficiency_scores": [0.0],
                "wait_times": [0.0],
                "vehicle_counts": [0],
                "queue_lengths": [0.0],
                "speeds": [0.0]
            },
            
            # Default Additional Metrics
            "additional_metrics": {
                "total_vehicles_processed": 0,
                "emergency_stops": 0,
                "signal_changes": 0,
                "peak_queue_length": 0.0,
                "simulation_progress": 0.0
            }
        }
    
    def get_current_data(self) -> Optional[Dict[str, Any]]:
        """Get current dashboard data (thread-safe)"""
        with self.data_lock:
            if self.current_data:
                return self.current_data.copy()
            else:
                # Provide default data when simulation hasn't started
                return self._get_default_dashboard_data()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        
        if self.metrics_collector:
            self.metrics_collector.stop_collection()
        
        if self.traci_manager:
            self.traci_manager.stop_simulation()
        
        if self.simulation_thread:
            self.simulation_thread.join(timeout=2.0)
    
    def change_signal_manually(self, phase_id: int, duration: float = 30.0) -> bool:
        """Manually change traffic signal phase"""
        if self.signal_controller and self.is_running:
            return self.signal_controller.change_signal_phase(phase_id, duration)
        return False
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """Get current simulation status"""
        return {
            "is_running": self.is_running,
            "simulation_state": self.traci_manager.simulation_state.value if self.traci_manager else "stopped",
            "available_scenarios": list(self.simulation_configs.keys()),
            "sumo_available": SUMO_AVAILABLE
        }
    
    def emergency_stop(self):
        """Emergency stop - immediately halt simulation"""
        self.is_running = False
        try:
            if self.traci_manager:
                self.traci_manager.stop_simulation()
        except Exception as e:
            st.error(f"Error during emergency stop: {e}")

# Global instance for Streamlit session state
@st.cache_resource
def get_sumo_integration():
    """Get or create SUMO integration instance"""
    return SumoStreamlitIntegration()

def initialize_sumo_integration():
    """Initialize SUMO integration in Streamlit session state"""
    if 'sumo_integration' not in st.session_state:
        st.session_state.sumo_integration = SumoStreamlitIntegration()
    
    return st.session_state.sumo_integration
