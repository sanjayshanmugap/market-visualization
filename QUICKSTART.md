# Quick Start Guide

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd market-visualization
   ```

2. **Run setup script:**
   ```bash
   ./setup.sh
   ```

   Or manually:
   ```bash
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

## Running the Application

### Start the Backend API

In one terminal:
```bash
source venv/bin/activate  # If not already activated
npm run api
# Or: uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

In another terminal:
```bash
cd src/ui
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Generating Visualizations

To generate sample data stories and visualizations:

```bash
source venv/bin/activate
python scripts/generate_stories.py
```

This will:
- Load data from various sources
- Generate visualizations using Python libraries
- Export them in appropriate formats
- Create story metadata files

## Project Structure

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
├── scripts/              # Utility scripts
└── requirements.txt      # Python dependencies
```

## Next Steps

1. Explore the gallery at `http://localhost:3000/gallery`
2. Read data stories at `http://localhost:3000/stories`
3. Check out the About page at `http://localhost:3000/about`
4. Create your own visualizations by adding new stories!

