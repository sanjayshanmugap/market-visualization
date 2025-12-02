"""
Seaborn Generator

Generates statistical visualizations using seaborn.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional, Dict, Any, List
import numpy as np


class SeabornGenerator:
    """Generator for seaborn visualizations."""
    
    def __init__(self, style: str = "whitegrid", palette: str = "husl"):
        """
        Initialize seaborn generator.
        
        Args:
            style: Seaborn style
            palette: Color palette
        """
        sns.set_style(style)
        sns.set_palette(palette)
        self.style = style
        self.palette = palette
    
    def correlation_heatmap(
        self,
        data: pd.DataFrame,
        title: str = "Correlation Heatmap",
        figsize: tuple = (10, 8),
        annot: bool = True,
        **kwargs
    ) -> plt.Figure:
        """
        Create a correlation heatmap.
        
        Args:
            data: DataFrame (numeric columns will be used)
            title: Plot title
            figsize: Figure size
            annot: Whether to annotate with correlation values
            **kwargs: Additional arguments for heatmap
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate correlation
        corr = data.select_dtypes(include=[np.number]).corr()
        
        sns.heatmap(
            corr,
            annot=annot,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax,
            **kwargs
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def pair_plot(
        self,
        data: pd.DataFrame,
        hue: Optional[str] = None,
        title: str = "Pair Plot",
        **kwargs
    ) -> plt.Figure:
        """
        Create a pair plot.
        
        Args:
            data: DataFrame with numeric columns
            hue: Optional column for color grouping
            title: Plot title
            **kwargs: Additional arguments for pairplot
            
        Returns:
            Matplotlib figure
        """
        fig = sns.pairplot(data, hue=hue, **kwargs)
        fig.fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        return fig.fig
    
    def violin_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a violin plot.
        
        Args:
            data: DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            hue: Optional column for grouping
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for violinplot
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.violinplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            **kwargs
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def box_plot(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        title: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a box plot.
        
        Args:
            data: DataFrame
            x: Column name for x-axis
            y: Column name for y-axis
            hue: Optional column for grouping
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for boxplot
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.boxplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            **kwargs
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def distribution_plot(
        self,
        data: pd.Series,
        title: str = "",
        figsize: tuple = (10, 6),
        **kwargs
    ) -> plt.Figure:
        """
        Create a distribution plot (histogram + KDE).
        
        Args:
            data: Series with data
            title: Plot title
            figsize: Figure size
            **kwargs: Additional arguments for distplot
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.histplot(data, kde=True, ax=ax, **kwargs)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(data.name or 'Value')
        ax.set_ylabel('Density')
        plt.tight_layout()
        return fig

