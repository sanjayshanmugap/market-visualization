"""
FastAPI Main Application

Main FastAPI application for the data visualization portfolio backend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

app = FastAPI(
    title="Data Visualization Portfolio API",
    description="API for serving visualization data and metadata",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
VIZ_DATA_DIR = Path("data/viz/data")
VIZ_STATIC_DIR = Path("data/viz/static")
STORIES_DIR = Path("data/viz/stories")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Data Visualization Portfolio API",
        "version": "0.1.0",
        "endpoints": {
            "list": "/api/viz/list",
            "stories": "/api/viz/stories",
            "viz_data": "/api/viz/{viz_id}/data",
            "viz_static": "/api/viz/{viz_id}/static",
            "viz_plotly": "/api/viz/{viz_id}/plotly",
        }
    }


@app.get("/api/viz/list")
async def list_visualizations(
    domain: Optional[str] = None,
    tool: Optional[str] = None,
    viz_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List all available visualizations with optional filtering.
    
    Args:
        domain: Filter by domain (financial, climate, social, scientific)
        tool: Filter by tool (matplotlib, plotly, etc.)
        viz_type: Filter by type (static, interactive, 3d, network, geospatial)
        
    Returns:
        List of visualization metadata
    """
    visualizations = []
    
    # Try to load from visualization index first
    viz_index_path = VIZ_DATA_DIR / "viz_index.json"
    if viz_index_path.exists():
        try:
            with open(viz_index_path, 'r') as f:
                visualizations = json.load(f)
        except Exception as e:
            print(f"Error loading viz index: {e}")
    
    # Fallback: Load from stories metadata if index not available
    if not visualizations and STORIES_DIR.exists():
        for story_file in STORIES_DIR.glob("*.json"):
            try:
                with open(story_file, 'r') as f:
                    story_data = json.load(f)
                    if 'visualizations' in story_data:
                        for viz in story_data['visualizations']:
                            visualizations.append({
                                **viz,
                                'domain': story_data.get('domain'),
                                'tool': 'plotly',  # Default, could be determined from type
                                'slug': story_data.get('slug'),
                            })
            except Exception as e:
                print(f"Error loading story {story_file}: {e}")
    
    # Apply filters
    if domain:
        visualizations = [v for v in visualizations if v.get('domain') == domain]
    if tool:
        visualizations = [v for v in visualizations if v.get('tool') == tool]
    if viz_type:
        visualizations = [v for v in visualizations if v.get('type') == viz_type]
    
    return visualizations


@app.get("/api/viz/stories")
async def list_stories() -> List[Dict[str, Any]]:
    """
    List all data stories.
    
    Returns:
        List of story metadata
    """
    stories = []
    
    if STORIES_DIR.exists():
        for story_file in STORIES_DIR.glob("*.json"):
            try:
                with open(story_file, 'r') as f:
                    story_data = json.load(f)
                    # Extract story metadata
                    story_meta = {
                        'id': story_data.get('id'),
                        'title': story_data.get('title'),
                        'domain': story_data.get('domain'),
                        'description': story_data.get('description'),
                        'slug': story_data.get('slug'),
                    }
                    stories.append(story_meta)
            except Exception as e:
                print(f"Error loading story {story_file}: {e}")
    
    return stories


@app.get("/api/viz/stories/{story_slug}")
async def get_story(story_slug: str) -> Dict[str, Any]:
    """
    Get a specific story by slug.
    
    Args:
        story_slug: Story slug identifier
        
    Returns:
        Story data with visualizations
    """
    story_file = STORIES_DIR / f"{story_slug}.json"
    
    if not story_file.exists():
        raise HTTPException(status_code=404, detail="Story not found")
    
    try:
        with open(story_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading story: {e}")


@app.get("/api/viz/{viz_id}/data")
async def get_viz_data(viz_id: str) -> Dict[str, Any]:
    """
    Get visualization data (JSON) for interactive charts.
    
    Args:
        viz_id: Visualization ID
        
    Returns:
        Visualization data as JSON
    """
    data_file = VIZ_DATA_DIR / f"{viz_id}.json"
    
    if not data_file.exists():
        raise HTTPException(status_code=404, detail="Visualization data not found")
    
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {e}")


@app.get("/api/viz/{viz_id}/static")
async def get_viz_static(viz_id: str, format: str = "png"):
    """
    Get static visualization image.
    
    Args:
        viz_id: Visualization ID
        format: Image format (png, svg, jpg)
        
    Returns:
        Image file
    """
    static_file = VIZ_STATIC_DIR / f"{viz_id}.{format}"
    
    if not static_file.exists():
        raise HTTPException(status_code=404, detail="Static visualization not found")
    
    return FileResponse(
        static_file,
        media_type=f"image/{format}",
        filename=f"{viz_id}.{format}"
    )


@app.get("/api/viz/{viz_id}/plotly")
async def get_viz_plotly(viz_id: str) -> Dict[str, Any]:
    """
    Get Plotly JSON specification for a visualization.
    
    Args:
        viz_id: Visualization ID
        
    Returns:
        Plotly figure JSON
    """
    # Try the exact viz_id first (in case it already includes _plotly)
    plotly_file = VIZ_DATA_DIR / f"{viz_id}.json"
    
    # If not found, try with _plotly suffix
    if not plotly_file.exists():
        plotly_file = VIZ_DATA_DIR / f"{viz_id}_plotly.json"
    
    if not plotly_file.exists():
        raise HTTPException(status_code=404, detail=f"Plotly visualization not found: {viz_id}")
    
    try:
        with open(plotly_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading Plotly data: {e}")


@app.post("/api/viz/generate")
async def generate_visualization(
    story_id: str,
    viz_id: str,
    force: bool = False,
) -> Dict[str, Any]:
    """
    Trigger visualization generation (placeholder for future implementation).
    
    Args:
        story_id: Story ID
        viz_id: Visualization ID
        force: Force regeneration even if exists
        
    Returns:
        Generation status
    """
    # This would trigger Python visualization generation
    # For now, return a placeholder response
    return {
        "status": "queued",
        "message": "Visualization generation is queued",
        "story_id": story_id,
        "viz_id": viz_id,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

