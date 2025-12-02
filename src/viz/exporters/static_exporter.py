"""
Static Image Exporter

Exports visualizations as static images (PNG, SVG, PDF) from matplotlib/seaborn.
"""

from pathlib import Path
from typing import Optional, Union
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


class StaticExporter:
    """Exports matplotlib/seaborn figures as static images."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("data/viz/static")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_figure(
        self,
        fig: plt.Figure,
        filename: str,
        format: str = "png",
        dpi: int = 300,
        bbox_inches: str = "tight",
        **kwargs
    ) -> Path:
        """
        Export a matplotlib figure to a static image file.
        
        Args:
            fig: Matplotlib figure object
            filename: Output filename (without extension)
            format: Image format (png, svg, pdf, jpg)
            dpi: Resolution for raster formats
            bbox_inches: Bounding box setting
            **kwargs: Additional arguments for savefig
            
        Returns:
            Path to saved file
        """
        output_path = self.output_dir / f"{filename}.{format}"
        
        fig.savefig(
            output_path,
            format=format,
            dpi=dpi,
            bbox_inches=bbox_inches,
            **kwargs
        )
        
        plt.close(fig)  # Close figure to free memory
        
        return output_path
    
    def export_seaborn_plot(
        self,
        fig: plt.Figure,
        filename: str,
        format: str = "png",
        dpi: int = 300,
    ) -> Path:
        """
        Export a seaborn plot (which is also a matplotlib figure).
        
        Args:
            fig: Matplotlib figure from seaborn
            filename: Output filename
            format: Image format
            dpi: Resolution
            
        Returns:
            Path to saved file
        """
        return self.export_figure(fig, filename, format, dpi)
    
    def export_multiple_formats(
        self,
        fig: plt.Figure,
        filename: str,
        formats: list = ["png", "svg"],
        dpi: int = 300,
    ) -> list[Path]:
        """
        Export figure in multiple formats.
        
        Args:
            fig: Matplotlib figure
            filename: Base filename
            formats: List of formats to export
            dpi: Resolution for raster formats
            
        Returns:
            List of paths to saved files
        """
        paths = []
        for fmt in formats:
            path = self.export_figure(fig, filename, fmt, dpi)
            paths.append(path)
        return paths

