"""
3D Visualization Generator

Generates 3D visualizations using Plotly and matplotlib.
"""

import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List


class ThreeDGenerator:
    """Generator for 3D visualizations."""
    
    def __init__(self):
        """Initialize 3D generator."""
        pass
    
    def scatter_3d(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        z_col: str,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a 3D scatter plot using Plotly.
        
        Args:
            data: DataFrame with 3D coordinates
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            z_col: Column name for z-axis
            color_col: Optional column for color mapping
            size_col: Optional column for size mapping
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.scatter_3d(
            data,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col,
            size=size_col,
            title=title,
            **kwargs
        )
        
        return fig
    
    def surface_3d(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        title: str = "3D Surface",
        colorscale: str = "Viridis",
        **kwargs
    ) -> go.Figure:
        """
        Create a 3D surface plot using Plotly.
        
        Args:
            x: X coordinates (2D array)
            y: Y coordinates (2D array)
            z: Z values (2D array)
            title: Chart title
            colorscale: Color scale name
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=[go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale=colorscale,
            **kwargs
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
            )
        )
        
        return fig
    
    def line_3d(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        z_col: str,
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a 3D line plot using Plotly.
        
        Args:
            data: DataFrame with 3D coordinates
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            z_col: Column name for z-axis
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=go.Scatter3d(
            x=data[x_col],
            y=data[y_col],
            z=data[z_col],
            mode='lines',
            line=dict(color='blue', width=2),
            **kwargs
        ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
            )
        )
        
        return fig
    
    def matplotlib_scatter_3d(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        z_col: str,
        color_col: Optional[str] = None,
        title: str = "",
        figsize: tuple = (10, 8),
        **kwargs
    ) -> plt.Figure:
        """
        Create a 3D scatter plot using matplotlib.
        
        Args:
            data: DataFrame with 3D coordinates
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            z_col: Column name for z-axis
            color_col: Optional column for color mapping
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments
            
        Returns:
            Matplotlib figure
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        if color_col:
            scatter = ax.scatter(
                data[x_col],
                data[y_col],
                data[z_col],
                c=data[color_col],
                cmap='viridis',
                **kwargs
            )
            plt.colorbar(scatter, ax=ax, label=color_col)
        else:
            ax.scatter(
                data[x_col],
                data[y_col],
                data[z_col],
                **kwargs
            )
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def matplotlib_surface_3d(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        title: str = "3D Surface",
        figsize: tuple = (10, 8),
        **kwargs
    ) -> plt.Figure:
        """
        Create a 3D surface plot using matplotlib.
        
        Args:
            x: X coordinates (2D array)
            y: Y coordinates (2D array)
            z: Z values (2D array)
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments
            
        Returns:
            Matplotlib figure
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(x, y, z, cmap='viridis', **kwargs)
        fig.colorbar(surf, ax=ax, shrink=0.5)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig

