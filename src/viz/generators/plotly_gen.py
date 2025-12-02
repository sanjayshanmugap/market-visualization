"""
Plotly Generator

Generates interactive web visualizations using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, Dict, Any, List
import numpy as np


class PlotlyGenerator:
    """Generator for Plotly interactive visualizations."""
    
    def __init__(self, template: str = "plotly_white"):
        """
        Initialize Plotly generator.
        
        Args:
            template: Plotly template name
        """
        self.template = template
    
    def line_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_cols: List[str],
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive line chart.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_cols: List of column names for y-axis
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        for y_col in y_cols:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode='lines',
                name=y_col,
                hovertemplate=f'<b>{y_col}</b><br>' +
                            f'{xlabel}: %{{x}}<br>' +
                            f'{ylabel}: %{{y}}<extra></extra>',
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            template=self.template,
            hovermode='x unified',
            **kwargs
        )
        
        return fig
    
    def scatter_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: Optional[str] = None,
        size_col: Optional[str] = None,
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive scatter chart.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            color_col: Optional column for color mapping
            size_col: Optional column for size mapping
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            title=title,
            template=self.template,
            **kwargs
        )
        
        return fig
    
    def bar_chart(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: str = "",
        orientation: str = "v",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive bar chart.
        
        Args:
            data: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            orientation: 'v' for vertical, 'h' for horizontal
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            title=title,
            template=self.template,
            orientation=orientation,
            **kwargs
        )
        
        return fig
    
    def heatmap(
        self,
        data: pd.DataFrame,
        title: str = "",
        colorscale: str = "Viridis",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive heatmap.
        
        Args:
            data: DataFrame (correlation matrix or similar)
            title: Chart title
            colorscale: Color scale name
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale=colorscale,
            text=data.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            **kwargs
        ))
        
        fig.update_layout(
            title=title,
            template=self.template,
            xaxis_title="",
            yaxis_title="",
        )
        
        return fig
    
    def candlestick(
        self,
        data: pd.DataFrame,
        title: str = "Candlestick Chart",
        **kwargs
    ) -> go.Figure:
        """
        Create a candlestick chart for financial data.
        
        Args:
            data: DataFrame with OHLC columns
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=go.Candlestick(
            x=data.index if isinstance(data.index, pd.DatetimeIndex) else data.get('Date', data.index),
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            **kwargs
        ))
        
        fig.update_layout(
            title=title,
            template=self.template,
            xaxis_rangeslider_visible=False,
        )
        
        return fig
    
    def sunburst(
        self,
        data: pd.DataFrame,
        path_cols: List[str],
        values_col: str,
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a sunburst chart.
        
        Args:
            data: DataFrame with hierarchical data
            path_cols: List of column names defining hierarchy
            values_col: Column name with values
            title: Chart title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.sunburst(
            data,
            path=path_cols,
            values=values_col,
            title=title,
            template=self.template,
            **kwargs
        )
        
        return fig

