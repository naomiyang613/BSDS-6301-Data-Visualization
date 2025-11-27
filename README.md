# BSDS-6301-Data-Visualization
Final project

# US State-to-State Migration Visualizer (Python/Plotly Version)

This is a Python implementation of the US State-to-State Migration Visualizer using Plotly and Dash.

## Features

- Interactive choropleth map of US states
- Three visualization modes:
  - **Net Migration**: Red (loss) to Green (gain) - diverging color scale
  - **Inflow**: Sequential blue color scale
  - **Outflow**: Sequential orange color scale
- Click on any state to see:
  - Total inflow, outflow, and net migration statistics
  - Top 10 origin states (where people are moving from)
  - Top 10 destination states (where people are moving to)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas plotly dash dash-bootstrap-components
```

## Running the Application

```bash
python app.py
```

Then open your browser to: http://127.0.0.1:8050

## Data Source

U.S. Census Bureau, American Community Survey (ACS) 1-Year Estimates, 2023

## Files

- `app.py` - Main Dash application
- `requirements.txt` - Python package dependencies
- `data/state_totals_2023.csv` - State-level migration totals
- `data/state_to_state_flows_2023.csv` - State-to-state migration flows

## Technical Details

- **Framework**: Dash (Flask-based)
- **Visualization**: Plotly
- **UI Components**: Dash Bootstrap Components
- **Data Processing**: Pandas

## Differences from D3.js Version

The Python version provides:
- Server-side rendering and callbacks
- Easier deployment options
- Better integration with Python data science ecosystem
- Responsive Bootstrap-based layout

## Notes

- The application filters out non-state entries (e.g., "Foreign Country", "Puerto Rico") from the choropleth to ensure proper color scaling
- Negative net migration values are displayed in red on the diverging color scale
- The map uses the Albers USA projection for accurate state representation
