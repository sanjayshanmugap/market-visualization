"""
Plotly JSON Exporter

Exports Plotly figures as JSON for use with react-plotly.js.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import plotly.graph_objects as go
import plotly.express as px


class PlotlyExporter:
    """Exports Plotly figures as JSON for frontend rendering."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("data/viz/data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_figure(
        self,
        fig: go.Figure,
        filename: str,
        include_data: bool = True,
    ) -> Path:
        """
        Export a Plotly figure as JSON.
        
        Args:
            fig: Plotly figure object
            filename: Output filename (without extension)
            include_data: Whether to include full data in JSON
            
        Returns:
            Path to saved JSON file
        """
        output_path = self.output_dir / f"{filename}.json"
        
        # Convert to dict
        fig_dict = fig.to_dict()
        
        # Optionally remove data to reduce file size (data can be loaded separately)
        if not include_data:
            # Keep only layout and config, remove data
            fig_dict = {
                'layout': fig_dict.get('layout', {}),
                'config': fig_dict.get('config', {}),
            }
        
        # Save as JSON
        with open(output_path, 'w') as f:
            json.dump(fig_dict, f, indent=2, default=str)
        
        return output_path
    
    def export_static_image(
        self,
        fig: go.Figure,
        filename: str,
        format: str = "png",
        width: int = 1200,
        height: int = 800,
        scale: int = 2,
    ) -> Optional[Path]:
        """
        Export Plotly figure as static image using kaleido.
        
        Args:
            fig: Plotly figure
            filename: Output filename
            format: Image format (png, jpg, svg, pdf, webp)
            width: Image width
            height: Image height
            scale: Scale factor for higher resolution
            
        Returns:
            Path to saved image, or None if kaleido not available
        """
        try:
            import kaleido
        except ImportError:
            print("Kaleido not installed. Install with: pip install kaleido")
            return None
        
        output_path = Path("data/viz/static") / f"{filename}.{format}"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fig.write_image(
            str(output_path),
            format=format,
            width=width,
            height=height,
            scale=scale,
        )
        
        return output_path
    
    def get_figure_json(self, fig: go.Figure) -> Dict[str, Any]:
        """
        Get figure as JSON dict without saving.
        
        Args:
            fig: Plotly figure
            
        Returns:
            Figure as dictionary
        """
        return fig.to_dict()

