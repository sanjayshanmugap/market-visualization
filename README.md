# Data Visualization Portfolio

A comprehensive data visualization portfolio showcasing technical skills in Python visualization libraries, data storytelling, and visual design across multiple domains.

## 🎯 Project Goals

- **Technical Skills**: Demonstrate proficiency with Python visualization libraries (matplotlib, seaborn, plotly, bokeh, altair, dash)
- **Data Storytelling**: Create compelling narratives with data across diverse domains
- **Visual Design**: Produce beautiful, polished visualizations in multiple formats (static, interactive, 3D, network, geospatial)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Python Viz     │    │   FastAPI       │    │   Next.js       │
│  Generators     │───►│   Backend       │───►│   Frontend      │
│  (matplotlib,   │    │   (API)         │    │   (Gallery,     │
│   plotly, etc.) │    │                 │    │    Stories)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Visualization Domains

- **Financial**: Stock market analysis, correlation networks, trading patterns
- **Climate**: Temperature trends, climate change impact, weather events
- **Social/Economic**: Economic inequality, population dynamics, social trends
- **Scientific**: Paper networks, tool ecosystems, 3D data exploration

## 🛠️ Tech Stack

### Python Backend
- **Visualization**: matplotlib, seaborn, plotly, bokeh, altair
- **Geospatial**: folium, plotly maps
- **Network**: networkx
- **3D**: plotly 3D, matplotlib 3D
- **Web Framework**: FastAPI

### Frontend
- **Framework**: Next.js 14
- **Visualization**: react-plotly.js, D3.js, Three.js
- **Maps**: Leaflet, react-leaflet
- **Styling**: Tailwind CSS

## 🚀 Quick Start

### Setup

```bash
# Clone repository
git clone https://github.com/sanjayshanmugap/market-visualization.git
cd market-visualization

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd src/ui
npm install
cd ../..
```

### Development

```bash
# Start FastAPI backend
uvicorn src.api.main:app --reload --port 8000

# Start Next.js frontend (in another terminal)
cd src/ui
npm run dev
```

## 📁 Project Structure

```
market-visualization/
├── src/
│   ├── viz/              # Visualization module
│   │   ├── generators/   # Visualization generators
│   │   ├── data_loaders/ # Data fetching
│   │   ├── exporters/    # Export utilities
│   │   └── stories/      # Story definitions
│   ├── api/              # FastAPI backend
│   └── ui/               # Next.js frontend
├── data/
│   └── viz/              # Visualization outputs
└── requirements.txt      # Python dependencies
```

## 📝 License

MIT License

