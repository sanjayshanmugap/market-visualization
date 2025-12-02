"""
Network Generator

Generates network/graph visualizations using networkx and plotly.
"""

import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any, List
import numpy as np


class NetworkGenerator:
    """Generator for network/graph visualizations."""
    
    def __init__(self):
        """Initialize network generator."""
        pass
    
    def create_network_from_edges(
        self,
        edges_df: pd.DataFrame,
        source_col: str = "Source",
        target_col: str = "Target",
        weight_col: Optional[str] = None,
    ) -> nx.Graph:
        """
        Create a NetworkX graph from edge list.
        
        Args:
            edges_df: DataFrame with edges
            source_col: Column name for source nodes
            target_col: Column name for target nodes
            weight_col: Optional column for edge weights
            
        Returns:
            NetworkX graph
        """
        if weight_col:
            edges = [
                (row[source_col], row[target_col], {'weight': row[weight_col]})
                for _, row in edges_df.iterrows()
            ]
            G = nx.Graph()
            G.add_edges_from(edges)
        else:
            G = nx.from_pandas_edgelist(
                edges_df,
                source=source_col,
                target=target_col,
                create_using=nx.Graph
            )
        
        return G
    
    def plotly_network(
        self,
        G: nx.Graph,
        layout: str = "spring",
        title: str = "Network Graph",
        node_size_col: Optional[str] = None,
        node_color_col: Optional[str] = None,
        edge_weight_col: Optional[str] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive network visualization with Plotly.
        
        Args:
            G: NetworkX graph
            layout: Layout algorithm (spring, circular, kamada_kawai, etc.)
            title: Chart title
            node_size_col: Optional node attribute for size
            node_color_col: Optional node attribute for color
            edge_weight_col: Optional edge attribute for weight
            **kwargs: Additional arguments
            
        Returns:
            Plotly figure
        """
        # Calculate layout
        if layout == "spring":
            pos = nx.spring_layout(G, k=1, iterations=50)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G)
        
        # Extract node positions
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                showlegend=False,
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_info = []
        node_sizes = []
        node_colors = []
        
        for node in G.nodes():
            node_info.append(f"Node: {node}<br>")
            if node_size_col and node_size_col in G.nodes[node]:
                node_sizes.append(G.nodes[node][node_size_col] * 10)
            else:
                node_sizes.append(10)
            
            if node_color_col and node_color_col in G.nodes[node]:
                node_colors.append(G.nodes[node][node_color_col])
            else:
                node_colors.append(1)
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node for node in G.nodes()],
            textposition="middle center",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=2, color='white'),
            ),
        )
        
        # Create figure
        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002,
                        xanchor="left", yanchor="bottom",
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                **kwargs
            )
        )
        
        return fig
    
    def network_metrics(self, G: nx.Graph) -> Dict[str, Any]:
        """
        Calculate network metrics.
        
        Args:
            G: NetworkX graph
            
        Returns:
            Dictionary with network metrics
        """
        return {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
            'avg_clustering': nx.average_clustering(G),
            'is_connected': nx.is_connected(G),
        }

