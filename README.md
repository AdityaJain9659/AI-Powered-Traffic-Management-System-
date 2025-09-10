# 🚦 AI-Powered Traffic Management System

An intelligent traffic management system that integrates real-time SUMO simulation with an AI-powered dashboard for dynamic traffic control and optimization.

## 🌟 Features

### Core Dashboard Features
- **Real-time Traffic Monitoring** with live KPI displays
- **Interactive Traffic Control** with signal phase management
- **AI Performance Analytics** with trend analysis
- **Live Camera Feeds** simulation
- **Modern Dark Theme UI** with responsive design

### SUMO Integration Features
- **Live SUMO Simulation** with real-time traffic data
- **Adaptive Signal Control** using AI algorithms
- **Multiple Traffic Scenarios** (uniform, tidal, asymmetric, congested)
- **Manual Signal Override** for traffic operators
- **Performance Metrics Collection** with historical analysis
- **Real-time Decision Logging** for AI transparency

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- SUMO Traffic Simulator (install from [https://eclipse.org/sumo/](https://eclipse.org/sumo/))
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Powered-Traffic-Management-System-
   ```

2. **Run the setup script**
   ```bash
   python setup_dashboard.py
   ```
   This will:
   - Check SUMO installation
   - Install required Python packages
   - Setup the environment
   - Create initial data files

3. **Install dependencies manually (if needed)**
   ```bash
   pip install -r "1. requirements.txt"
   ```

4. **Start the dashboard**
   ```bash
   streamlit run dashboard/dashboard.py
   ```

## 📁 Project Structure

```
AI-Powered-Traffic-Management-System-/
├── dashboard/                          # Main dashboard application
│   ├── dashboard.py                   # Main dashboard entry point
│   ├── config.py                     # Configuration settings
│   ├── styles.py                     # CSS styling
│   ├── sumo_integration.py          # SUMO bridge module
│   ├── sumo_components.py           # SUMO-specific UI components
│   ├── kpi_components.py            # KPI display components
│   ├── intersection_components.py    # Intersection visualization
│   ├── analytics_components.py      # Analytics and charts
│   ├── video_components.py          # Video feed components
│   └── layout_components.py         # Layout and UI helpers
├── sumo/                             # SUMO simulation system
│   └── Traffic-simulation-rl/        # RL-based traffic simulation
│       ├── traci_manager.py         # SUMO connection manager
│       ├── live_metrics.py          # Real-time metrics collection
│       ├── signal_controller.py     # AI signal control logic
│       ├── live_dashboard.py        # Standalone SUMO dashboard
│       └── Sumo_env/                # SUMO configuration files
├── data/                            # Data storage
│   └── dashboard_data.json         # Live dashboard data
├── setup_dashboard.py              # Automated setup script
└── 1. requirements.txt             # Python dependencies
```

## 🔧 Usage Guide

### Starting the System

1. **Launch Dashboard**: Run `streamlit run dashboard/dashboard.py`
2. **SUMO Integration**: Use the sidebar to start SUMO simulation
3. **Select Scenario**: Choose from uniform, tidal, asymmetric, or congested traffic patterns
4. **Monitor Performance**: View real-time metrics and AI decisions

### Dashboard Tabs

#### 1. Smart Traffic Control
- View intersection status and signal phases
- Monitor queue lengths and traffic flow
- See traditional vs AI-optimized performance

#### 2. Live Camera Feeds  
- Simulated traffic camera views
- Real-time traffic density visualization
- Emergency vehicle detection status

#### 3. AI Performance Analytics
- Performance trends over time
- Efficiency metrics comparison
- System optimization insights

#### 4. SUMO Simulation (when connected)
- Live simulation metrics (efficiency, congestion, throughput)
- Detailed intersection view with queue visualization
- Performance trend charts
- AI decision history

#### 5. SUMO Control Panel (when connected)
- Start/stop simulation controls
- Scenario switching
- Manual signal control override
- Custom phase timing controls

### Manual Traffic Control

When SUMO is connected, you can manually override the AI system:

- **North-South Green**: Force N-S direction to green
- **East-West Green**: Force E-W direction to green  
- **Extend Phase**: Add 15 seconds to current phase
- **Skip Phase**: Skip to next phase immediately
- **Custom Control**: Set specific phase ID and duration

## 🔗 SUMO Integration Architecture

### Components

1. **SUMODataBridge** (`sumo_integration.py`)
   - Bridges SUMO simulation data with Streamlit dashboard
   - Handles real-time data updates
   - Manages simulation lifecycle

2. **TraciManager** (`sumo/Traffic-simulation-rl/traci_manager.py`)
   - Manages SUMO simulation connection via TraCI API
   - Provides traffic state data collection
   - Handles signal control commands

3. **MetricsCollector** (`sumo/Traffic-simulation-rl/live_metrics.py`)
   - Collects real-time traffic metrics
   - Calculates efficiency scores and congestion levels
   - Maintains performance history

4. **SignalController** (`sumo/Traffic-simulation-rl/signal_controller.py`)
   - Implements AI-based adaptive signal control
   - Makes intelligent phase timing decisions
   - Handles emergency and congestion scenarios

### Data Flow

```
SUMO Simulation → TraciManager → MetricsCollector → SUMODataBridge → Dashboard
                       ↓
                SignalController → AI Decisions → Signal Changes
```

## 📊 Metrics and KPIs

### Real-time Metrics
- **Efficiency Score** (0-100): Overall system performance
- **Congestion Level**: LOW/MODERATE/HIGH/SEVERE
- **Throughput**: Vehicles per hour
- **Average Wait Time**: Seconds
- **Queue Length**: Number of waiting vehicles
- **Average Speed**: Meters per second

### Performance Indicators
- **Travel Time Reduction**: vs baseline system
- **Wait Time Optimization**: compared to fixed timing
- **Throughput Improvement**: traffic flow efficiency
- **Emergency Response**: priority vehicle handling

## 🛠️ Configuration

### Dashboard Configuration (`dashboard/config.py`)
- Refresh rates and update intervals
- Performance thresholds and color coding
- Chart dimensions and styling
- Status indicators and alerts

### SUMO Configuration (`sumo/Traffic-simulation-rl/Sumo_env/`)
- Network topology files (`.net.xml`)
- Route definitions (`.rou.xml`) 
- Simulation configurations (`.sumocfg`)
- Detector and signal definitions

## 🔍 Troubleshooting

### Common Issues

1. **SUMO Not Found**
   - Install SUMO from official website
   - Add SUMO bin directory to system PATH
   - Restart terminal/command prompt

2. **Import Errors**
   - Run `python setup_dashboard.py` to check dependencies
   - Install missing packages: `pip install -r "1. requirements.txt"`
   - Ensure Python 3.8+ is being used

3. **Simulation Won't Start**
   - Check SUMO config files exist in `sumo/Traffic-simulation-rl/Sumo_env/`
   - Verify file permissions
   - Check error messages in dashboard sidebar

4. **Dashboard Not Updating**
   - Check SUMO connection status in sidebar
   - Verify data file permissions in `data/` directory
   - Restart dashboard if needed

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export SUMO_DEBUG=1
streamlit run dashboard/dashboard.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and test thoroughly
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [SUMO](https://eclipse.org/sumo/) - Open Source Traffic Simulation
- [Streamlit](https://streamlit.io/) - Web App Framework
- [Plotly](https://plotly.com/) - Interactive Visualization
- Eclipse Foundation for SUMO development and support
