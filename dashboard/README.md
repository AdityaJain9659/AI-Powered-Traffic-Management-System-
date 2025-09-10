# AI Traffic Management Dashboard with SUMO Integration

A real-time traffic management dashboard that integrates with SUMO (Simulation of Urban Mobility) for live traffic data visualization and control.

## 🚀 Features

- **Real-time SUMO Integration**: Connect to live SUMO simulations for real-time traffic data
- **Interactive Dashboard**: Modern Streamlit-based interface with live updates
- **Traffic Control**: Manual and AI-powered traffic signal control
- **Multiple Scenarios**: Support for various traffic scenarios (uniform, tidal, asymmetric, congested)
- **Emergency Controls**: Kill switch and emergency stop functionality
- **Live Analytics**: Real-time performance metrics and visualizations

## 📋 Prerequisites

1. **SUMO Installation**:

   - Download and install SUMO from [https://sumo.dlr.de/](https://sumo.dlr.de/)
   - Ensure SUMO_HOME environment variable is set
   - Verify Python TraCI bindings are available

2. **Python Requirements**:
   - Python 3.8 or higher
   - pip package manager

## 🛠️ Installation

### Quick Start (Windows)

1. **Run the startup script**:
   ```cmd
   cd dashboard
   start_dashboard.bat
   ```

### Manual Setup

1. **Install Python dependencies**:

   ```bash
   cd dashboard
   pip install -r requirements_dashboard.txt
   ```

2. **Setup environment**:

   ```bash
   python run_dashboard.py --setup-only --install-deps
   ```

3. **Start the dashboard**:
   ```bash
   python run_dashboard.py
   ```

## 🎮 Usage

### Starting the Dashboard

1. **Launch the dashboard**:

   ```bash
   cd dashboard
   python run_dashboard.py --port 8501
   ```

2. **Open browser**: Navigate to `http://localhost:8501`

### Using the Dashboard

1. **System Control Tab**:

   - Select traffic scenario (uniform, tidal, asymmetric, congested)
   - Set simulation duration and control mode
   - Start/stop simulation with real-time controls

2. **Smart Traffic Control Tab**:

   - View live intersection map
   - Monitor signal phases and timing
   - See real-time traffic flow

3. **Live Camera Feeds Tab**:

   - Simulated camera feed display
   - Multi-angle intersection monitoring

4. **AI Performance Analytics Tab**:
   - Real-time performance charts
   - Efficiency metrics comparison
   - Historical data analysis

### Emergency Controls

- **Emergency Stop Button**: Immediately halt simulation
- **Kill Switch**: Terminate all processes (in sidebar)
- **Manual Override**: Take manual control of traffic signals

## 🔧 Configuration

### SUMO Scenarios

The dashboard supports multiple traffic scenarios located in:

```
sumo/Traffic-simulation-rl/Sumo_env/Single intersection lhd/
```

Available scenarios:

- `uniform_simulation.sumocfg` - Even traffic distribution
- `tidal_simulation.sumocfg` - Rush hour patterns
- `asymmetric_simulation.sumocfg` - Uneven traffic flow
- `congested_simulation.sumocfg` - Heavy traffic conditions
- `random_simulation.sumocfg` - Random traffic patterns

### Dashboard Configuration

Edit `config.py` to customize:

- Refresh rates
- Color schemes
- Threshold values
- Chart configurations

## 📊 Data Flow

1. **SUMO Simulation** → TraCI Manager → Metrics Collector
2. **Real-time Data** → SUMO Integration → Streamlit Dashboard
3. **User Controls** → Dashboard → Signal Controller → SUMO

## 🚨 Troubleshooting

### Common Issues

1. **SUMO not found**:

   - Ensure SUMO is installed and SUMO_HOME is set
   - Check that `traci` and `sumolib` are available in Python

2. **Dashboard won't start**:

   - Install missing dependencies: `pip install -r requirements_dashboard.txt`
   - Check port availability (default: 8501)

3. **No real-time data**:

   - Verify SUMO simulation is running
   - Check TraCI connection in System Control tab

4. **Simulation won't start**:
   - Ensure SUMO configuration files exist
   - Check file paths in `sumo_integration.py`

### Debug Mode

Run with debug logging:

```bash
python run_dashboard.py --debug
```

## 🔄 Development

### File Structure

```
dashboard/
├── dashboard.py              # Main Streamlit app
├── sumo_integration.py       # SUMO connection & data handling
├── control_components.py     # UI controls for simulation
├── config.py                # Configuration settings
├── styles.py                # CSS styling
├── kpi_components.py         # KPI widgets
├── intersection_components.py # Traffic intersection UI
├── analytics_components.py   # Charts and analytics
├── video_components.py       # Camera feed simulation
├── layout_components.py      # Layout helpers
├── run_dashboard.py          # Launcher script
├── start_dashboard.bat       # Windows startup script
└── requirements_dashboard.txt # Python dependencies
```

### Adding New Features

1. **New SUMO Scenarios**: Add `.sumocfg` files and update `simulation_configs` in `sumo_integration.py`
2. **Custom Metrics**: Extend `TrafficState` dataclass and update data collection
3. **UI Components**: Create new component files following the modular structure

## 📈 Performance

- **Update Rate**: Configurable 0.5-5.0 seconds
- **Data Processing**: Multi-threaded for real-time performance
- **Memory Usage**: Optimized data structures with cleanup
- **Scalability**: Designed for single intersection, extensible to networks

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

This project is part of the AI-Powered Traffic Management System. See main repository for license details.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review SUMO documentation: [https://sumo.dlr.de/docs/](https://sumo.dlr.de/docs/)
3. Open an issue in the repository

---

**Happy Traffic Managing! 🚦🤖**
