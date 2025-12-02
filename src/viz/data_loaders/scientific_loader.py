"""
Scientific Data Loader

Loads scientific datasets from various sources:
- Kaggle datasets
- UCI Machine Learning Repository
- Scientific paper data
- Research metrics
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
import json


class ScientificDataLoader:
    """Loader for scientific datasets."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
    
    def load_paper_citation_network(self) -> pd.DataFrame:
        """
        Load scientific paper citation network data.
        
        Returns:
            DataFrame with paper citations
        """
        # Sample citation network data
        # In production, would fetch from arXiv, PubMed, or other sources
        
        citations = [
            {
                'Paper_ID': 'P001',
                'Title': 'Deep Learning for Computer Vision',
                'Year': 2020,
                'Citations': 150,
                'Authors': 'Smith, J., Doe, A.',
                'Cited_By': ['P002', 'P003', 'P004'],
            },
            {
                'Paper_ID': 'P002',
                'Title': 'Neural Networks in Practice',
                'Year': 2021,
                'Citations': 80,
                'Authors': 'Johnson, B., Lee, C.',
                'Cited_By': ['P005', 'P006'],
            },
            {
                'Paper_ID': 'P003',
                'Title': 'Transformer Architectures',
                'Year': 2022,
                'Citations': 200,
                'Authors': 'Brown, T., White, S.',
                'Cited_By': ['P007', 'P008', 'P009', 'P010'],
            },
            # Add more papers
        ]
        
        return pd.DataFrame(citations)
    
    def load_tool_ecosystem_data(self) -> pd.DataFrame:
        """
        Load data science tool ecosystem data (libraries, frameworks, relationships).
        
        Returns:
            DataFrame with tool relationships
        """
        # Sample tool ecosystem data
        tools = [
            {
                'Tool': 'Python',
                'Category': 'Language',
                'Users_Millions': 15,
                'Dependencies': ['NumPy', 'Pandas', 'Matplotlib'],
                'Dependents': ['TensorFlow', 'PyTorch', 'Scikit-learn'],
            },
            {
                'Tool': 'TensorFlow',
                'Category': 'ML Framework',
                'Users_Millions': 2,
                'Dependencies': ['Python', 'NumPy'],
                'Dependents': ['Keras'],
            },
            {
                'Tool': 'PyTorch',
                'Category': 'ML Framework',
                'Users_Millions': 1.5,
                'Dependencies': ['Python', 'NumPy'],
                'Dependents': ['FastAI'],
            },
            {
                'Tool': 'Pandas',
                'Category': 'Data Processing',
                'Users_Millions': 10,
                'Dependencies': ['Python', 'NumPy'],
                'Dependents': ['Dask', 'Polars'],
            },
            # Add more tools
        ]
        
        return pd.DataFrame(tools)
    
    def load_research_metrics(self) -> pd.DataFrame:
        """
        Load research metrics and statistics.
        
        Returns:
            DataFrame with research metrics
        """
        # Sample research metrics
        years = list(range(2010, 2024))
        
        import numpy as np
        np.random.seed(42)
        
        # Simulate growing research output
        papers_published = [int(100000 * (1.08 ** (y - 2010)) + np.random.normal(0, 5000)) for y in years]
        citations = [int(p * np.random.uniform(5, 15)) for p in papers_published]
        
        df = pd.DataFrame({
            'Year': years,
            'Papers_Published': papers_published,
            'Total_Citations': citations,
            'Avg_Citations_Per_Paper': [c / p for c, p in zip(citations, papers_published)],
            'AI_Papers': [int(p * np.random.uniform(0.1, 0.2)) for p in papers_published],
        })
        
        return df
    
    def create_citation_edges(self, papers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create edge list for citation network visualization.
        
        Args:
            papers_df: DataFrame with paper citation data
            
        Returns:
            DataFrame with source, target edges
        """
        edges = []
        
        for _, paper in papers_df.iterrows():
            paper_id = paper['Paper_ID']
            cited_by = paper.get('Cited_By', [])
            
            if isinstance(cited_by, str):
                # If stored as string, parse it
                cited_by = json.loads(cited_by) if cited_by.startswith('[') else [cited_by]
            
            for cited_paper in cited_by:
                edges.append({
                    'Source': paper_id,
                    'Target': cited_paper,
                    'Type': 'cites',
                })
        
        return pd.DataFrame(edges)
    
    def create_tool_network_edges(self, tools_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create edge list for tool dependency network.
        
        Args:
            tools_df: DataFrame with tool data
            
        Returns:
            DataFrame with source, target edges
        """
        edges = []
        
        for _, tool in tools_df.iterrows():
            tool_name = tool['Tool']
            
            # Dependencies: tool depends on these
            deps = tool.get('Dependencies', [])
            if isinstance(deps, str):
                deps = json.loads(deps) if deps.startswith('[') else [deps]
            
            for dep in deps:
                edges.append({
                    'Source': dep,
                    'Target': tool_name,
                    'Type': 'depends_on',
                    'Weight': 1,
                })
            
            # Dependents: these depend on tool
            dependents = tool.get('Dependents', [])
            if isinstance(dependents, str):
                dependents = json.loads(dependents) if dependents.startswith('[') else [dependents]
            
            for dependent in dependents:
                edges.append({
                    'Source': tool_name,
                    'Target': dependent,
                    'Type': 'used_by',
                    'Weight': 1,
                })
        
        return pd.DataFrame(edges)

