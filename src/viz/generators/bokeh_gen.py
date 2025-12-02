"""
Bokeh Generator

Generates interactive dashboards using Bokeh.
Note: Bokeh charts are typically embedded in HTML or served via Bokeh server.
This generator creates Bokeh figures that can be exported or served.
"""

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column, row
import pandas as pd
from typing import Optional, Dict, Any, List


class BokehGenerator:
    """Generator for Bokeh interactive visualizations."""
    
    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize Bokeh generator.
        
        Args:
            width: Default figure width
            height: Default figure height
        """
        self.width = width
        self.height = height
    
    def line_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_cols: List[str],
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        **kwargs
    ) -> figure:
        """
        Create a line chart using Bokeh.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_cols: List of column names for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            **kwargs: Additional arguments
            
        Returns:
            Bokeh figure
        """
        p = figure(
            width=self.width,
            height=self.height,
            title=title,
            x_axis_label=xlabel,
            y_axis_label=ylabel,
            tools="pan,wheel_zoom,box_zoom,reset,save",
            **kwargs
        )
        
        source = ColumnDataSource(data)
        
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        for i, y_col in enumerate(y_cols):
            p.line(
                x=x_col,
                y=y_col,
                source=source,
                legend_label=y_col,
                line_width=2,
                color=colors[i % len(colors)],
            )
        
        p.legend.location = "top_left"
        p.add_tools(HoverTool(tooltips=[(x_col, f"@{x_col}"), ("Value", f"$y")]))
        
        return p
    
    def scatter_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        title: str = "",
        **kwargs
    ) -> figure:
        """
        Create a scatter chart using Bokeh.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            color_col: Optional column for color mapping
            size_col: Optional column for size mapping
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Bokeh figure
        """
        p = figure(
            width=self.width,
            height=self.height,
            title=title,
            tools="pan,wheel_zoom,box_zoom,reset,save",
            **kwargs
        )
        
        source = ColumnDataSource(data)
        
        size = size_col if size_col else 10
        
        p.circle(
            x=x_col,
            y=y_col,
            source=source,
            size=size,
            alpha=0.6,
            color='blue' if not color_col else color_col,
        )
        
        p.add_tools(HoverTool(tooltips=[(x_col, f"@{x_col}"), (y_col, f"@{y_col}")]))
        
        return p
    
    def bar_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "",
        **kwargs
    ) -> figure:
        """
        Create a bar chart using Bokeh.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Bokeh figure
        """
        p = figure(
            width=self.width,
            height=self.height,
            title=title,
            x_range=data[x_col].tolist(),
            tools="pan,wheel_zoom,box_zoom,reset,save",
            **kwargs
        )
        
        source = ColumnDataSource(data)
        
        p.vbar(
            x=x_col,
            top=y_col,
            source=source,
            width=0.9,
            color='steelblue',
        )
        
        p.xaxis.major_label_orientation = "vertical"
        p.add_tools(HoverTool(tooltips=[(x_col, f"@{x_col}"), (y_col, f"@{y_col}")]))
        
        return p

