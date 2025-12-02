"""
Script to generate sample data stories and visualizations.

This script demonstrates how to create data stories with visualizations
across different domains.
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.viz.data_loaders.financial_loader import FinancialDataLoader
from src.viz.data_loaders.climate_loader import ClimateDataLoader
from src.viz.data_loaders.social_loader import SocialDataLoader
from src.viz.data_loaders.scientific_loader import ScientificDataLoader

from src.viz.generators.matplotlib_gen import MatplotlibGenerator
from src.viz.generators.seaborn_gen import SeabornGenerator
from src.viz.generators.plotly_gen import PlotlyGenerator
from src.viz.generators.geospatial_gen import GeospatialGenerator
from src.viz.generators.network_gen import NetworkGenerator
# Note: 3d_gen cannot be imported directly due to Python naming restrictions
# Use importlib if ThreeDGenerator is needed: import importlib; three_d = importlib.import_module('src.viz.generators.3d_gen')

from src.viz.exporters.static_exporter import StaticExporter
from src.viz.exporters.plotly_exporter import PlotlyExporter
from src.viz.exporters.data_exporter import DataExporter


def create_financial_story():
    """Create a financial data story."""
    print("Creating financial story...")
    
    loader = FinancialDataLoader()
    generator = PlotlyGenerator()
    exporter = PlotlyExporter()
    
    # Load stock data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_data = loader.load_stock_data(symbols, period='1y')
    
    if not stock_data:
        print("Warning: No stock data loaded, using sample data structure")
        return None
    
    # Create correlation matrix
    corr_matrix = loader.calculate_correlation_matrix(stock_data)
    
    # Create visualization
    fig = generator.heatmap(corr_matrix, title="Stock Correlation Matrix")
    
    # Export
    exporter.export_figure(fig, "stock_correlation_plotly")
    
    # Create story metadata
    story = {
        'id': 'stock_correlation',
        'slug': 'stock-market-correlation',
        'title': 'Stock Market Correlation Analysis',
        'description': 'Analyzing correlations between major tech stocks',
        'domain': 'financial',
        'narrative': '''This visualization explores the correlation between major technology stocks over the past year.
        
Correlation analysis helps investors understand how stocks move together. High positive correlation (close to 1) means stocks tend to move in the same direction, while negative correlation means they move in opposite directions.

Key insights:
- Tech stocks generally show high positive correlation, especially during market-wide movements
- Understanding correlations helps in portfolio diversification
- Sector-specific events can cause temporary correlation changes''',
        'visualizations': [
            {
                'id': 'stock_correlation_plotly',
                'title': 'Stock Correlation Heatmap',
                'type': 'plotly',
                'description': 'Interactive heatmap showing correlation coefficients between stocks',
            }
        ]
    }
    
    return story


def create_climate_story():
    """Create a climate data story."""
    print("Creating climate story...")
    
    loader = ClimateDataLoader()
    generator = PlotlyGenerator()
    exporter = PlotlyExporter()
    
    # Load temperature data
    temp_data = loader.load_global_temperature_data()
    
    # Create line chart
    fig = generator.line_chart(
        temp_data,
        x_col='Date',
        y_cols=['Temperature_Anomaly'],
        title='Global Temperature Anomaly Over Time',
        xlabel='Date',
        ylabel='Temperature Anomaly (°C)',
    )
    
    # Export
    exporter.export_figure(fig, "temperature_trend_plotly")
    
    # Create story metadata
    story = {
        'id': 'temperature_trend',
        'slug': 'global-temperature-trends',
        'title': 'Global Temperature Trends',
        'description': 'Long-term temperature anomaly trends showing climate change',
        'domain': 'climate',
        'narrative': '''This visualization shows global temperature anomalies over more than a century of data.
        
Temperature anomalies represent deviations from a baseline average, making it easier to see long-term trends regardless of absolute temperature values.

Key observations:
- Clear upward trend in temperature anomalies over time
- Natural variability is present but the overall trend is unmistakable
- Recent decades show the most significant warming
- This data supports the scientific consensus on climate change''',
        'visualizations': [
            {
                'id': 'temperature_trend_plotly',
                'title': 'Temperature Anomaly Timeline',
                'type': 'plotly',
                'description': 'Interactive line chart showing temperature anomalies over time',
            }
        ]
    }
    
    return story


def create_social_story():
    """Create a social/economic data story."""
    print("Creating social story...")
    
    loader = SocialDataLoader()
    generator = PlotlyGenerator()
    exporter = PlotlyExporter()
    
    # Load inequality data
    inequality_data = loader.load_economic_inequality_data('USA')
    
    # Create line chart
    fig = generator.line_chart(
        inequality_data,
        x_col='Year',
        y_cols=['Gini_Coefficient'],
        title='Economic Inequality (Gini Coefficient) Over Time',
        xlabel='Year',
        ylabel='Gini Coefficient',
    )
    
    # Export
    exporter.export_figure(fig, "inequality_trend_plotly")
    
    # Create story metadata
    story = {
        'id': 'economic_inequality',
        'slug': 'economic-inequality-trends',
        'title': 'Economic Inequality Trends',
        'description': 'Analyzing changes in economic inequality using Gini coefficient',
        'domain': 'social',
        'narrative': '''This visualization examines economic inequality using the Gini coefficient, a measure of income distribution.
        
The Gini coefficient ranges from 0 (perfect equality) to 1 (perfect inequality). Higher values indicate greater inequality.

Key insights:
- Economic inequality has been a topic of increasing concern
- The Gini coefficient provides a quantitative measure of inequality
- Understanding trends helps inform policy discussions
- Multiple factors contribute to changes in inequality over time''',
        'visualizations': [
            {
                'id': 'inequality_trend_plotly',
                'title': 'Gini Coefficient Over Time',
                'type': 'plotly',
                'description': 'Interactive chart showing inequality trends',
            }
        ]
    }
    
    return story


def create_scientific_story():
    """Create a scientific data story."""
    print("Creating scientific story...")
    
    loader = ScientificDataLoader()
    generator = NetworkGenerator()
    exporter = PlotlyExporter()
    
    # Load paper citation data
    papers_df = loader.load_paper_citation_network()
    edges_df = loader.create_citation_edges(papers_df)
    
    if not edges_df.empty:
        # Create network graph
        G = generator.create_network_from_edges(edges_df)
        fig = generator.plotly_network(G, title="Scientific Paper Citation Network")
        
        # Export
        exporter.export_figure(fig, "citation_network_plotly")
        
        # Create story metadata
        story = {
            'id': 'citation_network',
            'slug': 'scientific-citation-network',
            'title': 'Scientific Paper Citation Network',
            'description': 'Visualizing relationships between scientific papers through citations',
            'domain': 'scientific',
            'narrative': '''This network visualization shows how scientific papers are connected through citations.
        
Citation networks reveal the structure of scientific knowledge, showing which papers are central to a field and how ideas flow between researchers.

Key insights:
- Highly cited papers form hubs in the network
- Network structure reveals research communities
- Citation patterns show the evolution of scientific fields
- Understanding citation networks helps identify influential research''',
            'visualizations': [
                {
                    'id': 'citation_network_plotly',
                    'title': 'Citation Network Graph',
                    'type': 'network',
                    'description': 'Interactive network visualization of paper citations',
                }
            ]
        }
        
        return story
    
    return None


def main():
    """Generate all stories."""
    stories_dir = Path("data/viz/stories")
    stories_dir.mkdir(parents=True, exist_ok=True)
    
    stories = []
    
    # Generate stories
    financial_story = create_financial_story()
    if financial_story:
        stories.append(financial_story)
        with open(stories_dir / f"{financial_story['slug']}.json", 'w') as f:
            json.dump(financial_story, f, indent=2)
    
    climate_story = create_climate_story()
    if climate_story:
        stories.append(climate_story)
        with open(stories_dir / f"{climate_story['slug']}.json", 'w') as f:
            json.dump(climate_story, f, indent=2)
    
    social_story = create_social_story()
    if social_story:
        stories.append(social_story)
        with open(stories_dir / f"{social_story['slug']}.json", 'w') as f:
            json.dump(social_story, f, indent=2)
    
    scientific_story = create_scientific_story()
    if scientific_story:
        stories.append(scientific_story)
        with open(stories_dir / f"{scientific_story['slug']}.json", 'w') as f:
            json.dump(scientific_story, f, indent=2)
    
    print(f"\nGenerated {len(stories)} stories:")
    for story in stories:
        print(f"  - {story['title']} ({story['slug']})")
    
    # Create index of all visualizations for API
    all_viz = []
    for story in stories:
        all_viz.extend([
            {
                'id': viz['id'],
                'title': viz['title'],
                'description': story['description'],
                'domain': story['domain'],
                'tool': 'plotly',  # Could be determined from viz type
                'type': viz['type'],
                'slug': story['slug'],
            }
            for viz in story['visualizations']
        ])
    
    # Save visualization index
    viz_index_path = Path("data/viz/data/viz_index.json")
    viz_index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(viz_index_path, 'w') as f:
        json.dump(all_viz, f, indent=2)
    
    print(f"\nCreated visualization index with {len(all_viz)} visualizations")


if __name__ == "__main__":
    main()

