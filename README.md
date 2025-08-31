# AI Traffic Management Dashboard - Modular Structure

This dashboard has been reorganized into a modular, maintainable structure for better code organization and scalability.

## 📁 Project Structure

```
dashboard/
├── __init__.py                    # Package initialization
├── dashboard.py                   # Main application entry point
├── config.py                      # Configuration settings
├── styles.py                      # CSS styles and theming
├── layout_components.py           # UI layout and navigation helpers
├── kpi_components.py             # Key Performance Indicators
├── intersection_components.py     # Traffic intersection controls & map
├── analytics_components.py       # Performance analytics & charts
└── video_components.py           # Camera feeds & video monitoring
```

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install streamlit plotly pandas pillow
   ```

2. **Run the Dashboard:**
   ```bash
   streamlit run dashboard.py --server.port 8505
   ```

3. **Access Dashboard:**
   - Local: http://localhost:8505
   - Network: http://192.168.1.5:8505

## 📦 Module Breakdown

### `dashboard.py`
Main application entry point that:
- Configures Streamlit settings
- Orchestrates all components
- Handles data loading and routing
- Manages tab navigation

### `config.py`
Centralized configuration including:
- Dashboard settings (title, layout, etc.)
- File paths and data sources
- Status color schemes
- Traffic thresholds
- Chart configuration

### `styles.py`
Complete CSS theming system:
- Dark theme styling
- FontAwesome icon integration
- Component-specific styles
- Responsive design elements

### `layout_components.py`
UI layout helpers:
- Header rendering
- Sidebar controls
- Section headers
- Card wrapper functions

### `kpi_components.py`
Key Performance Indicator displays:
- Travel time metrics
- Wait time analysis
- Vehicle density tracking
- AI efficiency indicators

### `intersection_components.py`
Traffic intersection management:
- Real-time intersection map
- Traffic light control panel
- Queue status visualization
- Road condition monitoring

### `analytics_components.py`
Performance analytics:
- Time series charts
- AI vs traditional comparison
- Performance improvement metrics
- System efficiency tracking

### `video_components.py`
Video monitoring system:
- Camera feed display
- Stream status indicators
- Object detection status
- Recording controls

## ⚙️ Configuration

### Dashboard Settings
```python
DASHBOARD_CONFIG = {
    "page_title": "AI Traffic Management",
    "page_icon": "🚦", 
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
}
```

### Traffic Thresholds
```python
TRAFFIC_THRESHOLDS = {
    "free_flow": 2,
    "moderate": 5, 
    "congested": 8
}
```

### Status Colors
```python
STATUS_COLORS = {
    "online": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444", 
    "neutral": "#6b7280"
}
```

## 🎨 Theming

The dashboard uses a modern dark theme with:
- **Primary Colors:** Blue-purple gradient (#4f46e5 to #06b6d4)
- **Background:** Dark gradient (#0c0c0c to #262626)
- **Cards:** Gradient backgrounds with hover effects
- **Icons:** FontAwesome 6.0 integration
- **Typography:** Modern sans-serif with proper hierarchy

## 🔧 Customization

### Adding New Components
1. Create a new `.py` file in the dashboard directory
2. Import required dependencies (streamlit, plotly, etc.)
3. Define your component functions
4. Import and use in `dashboard.py`

### Modifying Styles
1. Edit `styles.py`
2. Add new CSS classes or modify existing ones
3. Use CSS custom properties for consistency

### Updating Configuration
1. Modify values in `config.py`
2. Import and use in relevant components
3. Restart the application

## 🚦 Features

### Real-time Monitoring
- Live traffic intersection maps
- Real-time KPI updates
- Dynamic chart updates
- Status indicator monitoring

### AI Integration
- AI vs traditional control comparison
- Performance optimization tracking
- Predictive analytics display
- Efficiency metrics

### Modern UI
- Responsive design
- Dark theme with gradients
- Smooth animations and transitions
- Professional iconography

### Modular Architecture  
- Separation of concerns
- Easy maintenance and updates
- Scalable component system
- Configuration management

## 📊 Data Format

The dashboard expects JSON data in the following format:

```json
{
    "avg_travel_time": 25.5,
    "avg_wait_time": 15.2,
    "vehicles_in_system": 450,
    "baseline_avg_travel_time": 30.0,
    "intersections": {
        "intersection_1": {
            "name": "Main & Broadway",
            "current_phase": 1,
            "queues": [3, 7, 2, 5]
        }
    },
    "time_series": {
        "t": [0, 1, 2, 3],
        "rl_avg_travel_time": [25, 24, 23, 22],
        "baseline_avg_travel_time": [30, 30, 30, 30]
    }
}
```

## 🔍 Troubleshooting

### Common Issues
1. **Import Errors:** Ensure all dependencies are installed in the Python environment
2. **Port Conflicts:** Change the port number in the run command
3. **Data Loading:** Verify `dashboard_data.json` exists in the `data/` directory
4. **Styling Issues:** Clear browser cache and refresh

### Performance Tips
- Use appropriate refresh rates (0.5-5.0 seconds)
- Monitor system resources during heavy usage
- Optimize chart data for large datasets

## 📝 Development

### Code Style
- Follow PEP 8 conventions
- Use descriptive variable names
- Add docstrings to all functions
- Keep components focused and modular

### Testing
```bash
python -c "import dashboard; print('All imports successful')"
```

### Version Control
- Commit modular changes separately
- Use descriptive commit messages
- Test thoroughly before deployment

---

**Version:** 1.0.0  
**Last Updated:** August 31, 2025  
**Authors:** AI Traffic Management Team
