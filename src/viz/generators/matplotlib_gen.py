"""
Matplotlib Generator

Generates static publication-quality charts using matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List
from pathlib import Path


class MatplotlibGenerator:
    """Generator for matplotlib visualizations."""
    
    def __init__(self, style_name: str = "seaborn-v0_8"):
        """
        Initialize matplotlib generator.
        
        Args:
            style_name: Matplotlib style to use
        """
        try:
            plt.style.use(style_name)
        except:
            plt.style.use('default')
        self.style_name = style_name
    
    def line_plot(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_cols: List[str],
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a line plot.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_cols: List of column names for y-axis
            title: Plot title
            xlabel: X-axis label
            ylabel: Y-axis label
            figsize: Figure size
            **kwargs: Additional arguments for plot
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for y_col in y_cols:
            ax.plot(data[x_col], data[y_col], label=y_col, **kwargs)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def scatter_plot(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        title: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a scatter plot.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            color_col: Optional column for color mapping
            size_col: Optional column for size mapping
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for scatter
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        scatter_kwargs = kwargs.copy()
        
        if color_col:
            scatter = ax.scatter(
                data[x_col],
                data[y_col],
                c=data[color_col],
                s=data[size_col] if size_col else 50,
                cmap='viridis',
                alpha=0.6,
                **scatter_kwargs
            )
            plt.colorbar(scatter, ax=ax, label=color_col)
        else:
            ax.scatter(
                data[x_col],
                data[y_col],
                s=data[size_col] if size_col else 50,
                alpha=0.6,
                **scatter_kwargs
            )
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def bar_plot(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a bar plot.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for bar
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.bar(data[x_col], data[y_col], **kwargs)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def heatmap(
        self,
        data: pd.DataFrame,
        title: str = "",
        figsize: tuple = (10, 8),
        cmap: str = "viridis",
        **kwargs
    ) -> plt.Figure:
        """
        Create a heatmap.
        
        Args:
            data: DataFrame (will be used as correlation matrix or similar)
            title: Plot title
            figsize: Figure size
            cmap: Colormap
            **kwargs: Additional arguments for imshow
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        im = ax.imshow(data.values, cmap=cmap, aspect='auto', **kwargs)
        
        # Set ticks
        ax.set_xticks(np.arange(len(data.columns)))
        ax.set_yticks(np.arange(len(data.index)))
        ax.set_xticklabels(data.columns, rotation=45, ha='right')
        ax.set_yticklabels(data.index)
        
        # Add colorbar
        plt.colorbar(im, ax=ax)
        
        # Add text annotations
        for i in range(len(data.index)):
            for j in range(len(data.columns)):
                text = ax.text(
                    j, i, f'{data.iloc[i, j]:.2f}',
                    ha="center", va="center", color="white", fontsize=8
                )
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def histogram(
        self,
        data: pd.Series,
        title: str = "",
        bins: int = 30,
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a histogram.
        
        Args:
            data: Series with data
            title: Plot title
            bins: Number of bins
            figsize: Figure size
            **kwargs: Additional arguments for hist
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, **kwargs)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(data.name or 'Value')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig

