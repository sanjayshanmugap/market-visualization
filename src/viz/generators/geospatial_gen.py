"""
Geospatial Generator

Generates map visualizations using folium and plotly.
"""

import folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any, List
from pathlib import Path


class GeospatialGenerator:
    """Generator for geospatial visualizations."""
    
    def __init__(self):
        """Initialize geospatial generator."""
        pass
    
    def choropleth_map(
        self,
        data: pd.DataFrame,
        geojson: Optional[Dict] = None,
        location_col: str = "Country",
        value_col: str = "Value",
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a choropleth map using Plotly.
        
        Args:
            data: DataFrame with location and value data
            geojson: Optional GeoJSON data
            location_col: Column name for locations
            value_col: Column name for values
            title: Map title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.choropleth(
            data,
            locations=location_col,
            color=value_col,
            title=title,
            **kwargs
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        return fig
    
    def scatter_map(
        self,
        data: pd.DataFrame,
        lat_col: str = "Latitude",
        lon_col: str = "Longitude",
        size_col: Optional[str] = None,
        color_col: Optional[str] = None,
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a scatter map.
        
        Args:
            data: DataFrame with lat/lon data
            lat_col: Column name for latitude
            lon_col: Column name for longitude
            size_col: Optional column for marker size
            color_col: Optional column for marker color
            title: Map title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = px.scatter_geo(
            data,
            lat=lat_col,
            lon=lon_col,
            size=size_col,
            color=color_col,
            title=title,
            **kwargs
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            )
        )
        
        return fig
    
    def folium_map(
        self,
        data: pd.DataFrame,
        lat_col: str = "Latitude",
        lon_col: str = "Longitude",
        popup_col: Optional[str] = None,
        color_col: Optional[str] = None,
        center: Optional[List[float]] = None,
        zoom_start: int = 5,
        save_path: Optional[Path] = None,
    ) -> folium.Map:
        """
        Create a Folium interactive map.
        
        Args:
            data: DataFrame with location data
            lat_col: Column name for latitude
            lon_col: Column name for longitude
            popup_col: Optional column for popup text
            color_col: Optional column for marker color
            center: Map center [lat, lon]
            zoom_start: Initial zoom level
            save_path: Optional path to save HTML file
            
        Returns:
            Folium map object
        """
        # Determine center if not provided
        if center is None:
            center = [data[lat_col].mean(), data[lon_col].mean()]
        
        # Create map
        m = folium.Map(location=center, zoom_start=zoom_start)
        
        # Add markers
        for idx, row in data.iterrows():
            popup_text = str(row[popup_col]) if popup_col else f"Point {idx}"
            
            # Determine color
            if color_col:
                # Simple color mapping (can be enhanced)
                value = row[color_col]
                color = 'red' if value > data[color_col].median() else 'blue'
            else:
                color = 'blue'
            
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=popup_text,
                icon=folium.Icon(color=color),
            ).add_to(m)
        
        # Save if path provided
        if save_path:
            m.save(str(save_path))
        
        return m
    
    def heatmap_map(
        self,
        data: pd.DataFrame,
        lat_col: str = "Latitude",
        lon_col: str = "Longitude",
        weight_col: str = "Weight",
        title: str = "",
        **kwargs
    ) -> go.Figure:
        """
        Create a heatmap on a map.
        
        Args:
            data: DataFrame with location and weight data
            lat_col: Column name for latitude
            lon_col: Column name for longitude
            weight_col: Column name for heatmap weights
            title: Map title
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(go.Densitymapbox(
            lat=data[lat_col],
            lon=data[lon_col],
            z=data[weight_col],
            radius=10,
            **kwargs
        ))
        
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=data[lat_col].mean(),
                    lon=data[lon_col].mean()
                ),
                zoom=5
            ),
            title=title,
        )
        
        return fig

