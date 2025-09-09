# 🚦 AI Traffic Management - RL Demo Dashboard

A production-style Streamlit dashboard for visualizing reinforcement learning traffic signal control performance.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Model
Place a trained DQN model at:
```
Traffic-simulation-rl/models/demo_rl.pth
```

Or use the existing trained model:
```
Traffic-simulation-rl/trained_models/dqn_final.pth
```

### 3. Run Dashboard
```bash
streamlit run app.py
```

### 4. Use the Dashboard
1. Open http://localhost:8505 in your browser
2. In the sidebar, click **"🚀 Run RL Demo"**
3. Explore the KPIs, charts, and data tables

## 📊 Features

### KPI Cards
- **Avg Reward (episode)** - Mean reward across all steps
- **Avg Waiting Time (s)** - Average vehicle waiting time
- **Peak Queue Length** - Maximum queue length observed
- **Actions Used (unique)** - Number of different actions taken
- **Steps Simulated** - Total simulation steps

### Interactive Charts
- **Reward & Wait Time** - Time series of performance metrics
- **Queue Length** - Traffic queue evolution over time
- **Action Distribution** - Bar chart of action usage
- **Throughput** - Vehicle throughput (if available)
- **Junction Analysis** - Per-junction performance (if available)

### Data Tables
- **Raw Episode Data** - Complete simulation data
- **Action Aggregates** - Performance by action type

## 🎛️ Controls

### Model Selection
- **Default Demo Model**: Uses `models/demo_rl.pth`
- **Custom Path**: Specify any model path
- **Upload File**: Upload your own `.pth` file

### Simulation Parameters
- **Max Steps**: Control simulation length (10-500 steps)

## 🔧 Troubleshooting

### "Model not found" Error
1. Ensure `Traffic-simulation-rl/models/demo_rl.pth` exists
2. Or use "Custom Path" option with `trained_models/dqn_final.pth`
3. Or upload a model file using the file uploader

### Missing Data Columns
The dashboard adapts to available data:
- Missing `avg_wait_time` → Shows 0.0 in KPIs
- Missing `queue_length` → Omits queue charts
- Missing `junction_id` → Skips junction analysis

### Performance Issues
- Use fewer simulation steps for faster results
- The dashboard caches results for better performance
- Clear cache by refreshing the page

## 🏗️ Architecture

### File Structure
```
AI-Powered-Traffic-Management-System-/
├── app.py                          # Main Streamlit dashboard
├── traffic_rl/
│   ├── api_rl.py                   # RL API wrapper
│   └── _vendored_api_rl.py         # Fallback stub
├── .streamlit/
│   └── config.toml                 # Dark theme config
├── requirements.txt                # Dependencies
└── README_RL_DEMO.md              # This file
```

### Data Schema
Required columns:
- `time` - Simulation step
- `action` - Action taken (0-3)
- `reward` - Step reward
- `avg_wait_time` - Average waiting time
- `queue_length` - Queue length

Optional columns:
- `junction_id` - Junction identifier
- `phase` - Traffic light phase
- `waiting_time` - Individual waiting time
- `throughput` - Vehicle throughput

## 🔗 Integration

This dashboard integrates with the `Traffic-simulation-rl` repository:
- Imports RL API functions
- Uses trained DQN models
- Supports SUMO traffic simulation data

## 📈 Future Enhancements

- Real-time data streaming
- Multiple junction support
- Historical data comparison
- Export functionality
- Advanced filtering options
