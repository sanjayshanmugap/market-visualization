"""
Script to generate comprehensive housing data stories and visualizations.

This script creates a thorough EDA of the House Prices dataset with multiple
stories covering different aspects of the data to help predict SalePrice.
"""

import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.viz.data_loaders.housing_loader import HousingDataLoader
from src.viz.generators.plotly_gen import PlotlyGenerator
from src.viz.exporters.plotly_exporter import PlotlyExporter
import plotly.graph_objects as go

# Feature name mappings for better axis labels
FEATURE_LABELS = {
    'SalePrice': 'Sale Price ($)',
    'OverallQual': 'Overall Quality Rating (1-10)',
    'OverallCond': 'Overall Condition Rating (1-10)',
    'GrLivArea': 'Above Grade Living Area (sq ft)',
    'TotalBsmtSF': 'Total Basement Area (sq ft)',
    'GarageArea': 'Garage Area (sq ft)',
    'GarageCars': 'Garage Size (car capacity)',
    '1stFlrSF': 'First Floor Area (sq ft)',
    'FullBath': 'Full Bathrooms',
    'TotRmsAbvGrd': 'Total Rooms Above Grade',
    'YearBuilt': 'Year Built',
    'YearRemodAdd': 'Year Remodeled',
    'YrSold': 'Year Sold',
    'LotArea': 'Lot Area (sq ft)',
    'LotFrontage': 'Lot Frontage (linear feet)',
    'BedroomAbvGr': 'Bedrooms Above Grade',
    'KitchenAbvGr': 'Kitchens Above Grade',
    'Fireplaces': 'Number of Fireplaces',
    'Neighborhood': 'Neighborhood',
    'HouseStyle': 'House Style',
    'BldgType': 'Building Type',
    'GarageType': 'Garage Type',
    'Foundation': 'Foundation Type',
    'MSSubClass': 'Building Class',
    'MSZoning': 'Zoning Classification',
}

def get_feature_label(feature_name):
    """Get a descriptive label for a feature name."""
    return FEATURE_LABELS.get(feature_name, feature_name.replace('_', ' ').title())


def create_price_distribution_story(loader, generator, exporter, df):
    """Create Story 1: Price Distribution & Summary Statistics."""
    print("Creating price distribution story...")
    
    # Histogram of SalePrice
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df['SalePrice'],
        nbinsx=50,
        name='Sale Price',
        marker_color='steelblue'
    ))
    fig_hist.update_layout(
        title='Distribution of House Sale Prices',
        xaxis_title='Sale Price ($)',
        yaxis_title='Frequency',
        template='plotly_white'
    )
    exporter.export_figure(fig_hist, "price_distribution_histogram")
    
    # Box plot by OverallQual
    if 'OverallQual' in df.columns:
        fig_box = go.Figure()
        quality_labels = {
            1: 'Very Poor', 2: 'Poor', 3: 'Fair', 4: 'Below Average',
            5: 'Average', 6: 'Above Average', 7: 'Good', 8: 'Very Good',
            9: 'Excellent', 10: 'Very Excellent'
        }
        for qual in sorted(df['OverallQual'].unique()):
            prices = df[df['OverallQual'] == qual]['SalePrice']
            qual_label = quality_labels.get(qual, f'Quality {qual}')
            fig_box.add_trace(go.Box(
                y=prices,
                name=f'{qual} - {qual_label}',
                boxpoints='outliers'
            ))
        fig_box.update_layout(
            title='Sale Price Distribution by Overall Quality Rating',
            xaxis_title='Overall Quality Rating (1 = Very Poor, 10 = Very Excellent)',
            yaxis_title='Sale Price ($)',
            template='plotly_white'
        )
        exporter.export_figure(fig_box, "price_by_quality_box")
    
    # Summary statistics
    summary_stats = {
        'mean': float(df['SalePrice'].mean()),
        'median': float(df['SalePrice'].median()),
        'std': float(df['SalePrice'].std()),
        'min': float(df['SalePrice'].min()),
        'max': float(df['SalePrice'].max()),
        'q25': float(df['SalePrice'].quantile(0.25)),
        'q75': float(df['SalePrice'].quantile(0.75)),
    }
    
    story = {
        'id': 'price_distribution',
        'slug': 'house-price-distribution',
        'title': 'House Price Distribution & Summary Statistics',
        'description': 'Understanding the distribution and basic statistics of house sale prices',
        'domain': 'housing',
        'narrative': f'''This analysis examines the distribution of house sale prices in the dataset.

Key Statistics:
- Mean Price: ${summary_stats['mean']:,.0f}
- Median Price: ${summary_stats['median']:,.0f}
- Standard Deviation: ${summary_stats['std']:,.0f}
- Price Range: ${summary_stats['min']:,.0f} - ${summary_stats['max']:,.0f}
- 25th Percentile: ${summary_stats['q25']:,.0f}
- 75th Percentile: ${summary_stats['q75']:,.0f}

The distribution shows that house prices are right-skewed, with most houses priced below the mean. The price distribution by overall quality reveals a clear positive relationship - higher quality houses command significantly higher prices.

Understanding this distribution is crucial for predictive modeling, as it helps identify outliers and informs feature engineering decisions.''',
        'visualizations': [
            {
                'id': 'price_distribution_histogram',
                'title': 'Sale Price Distribution',
                'type': 'plotly',
                'description': 'Histogram showing the distribution of house sale prices',
            },
            {
                'id': 'price_by_quality_box',
                'title': 'Price Distribution by Overall Quality',
                'type': 'plotly',
                'description': 'Box plots showing price distributions across different quality levels',
            }
        ]
    }
    
    return story


def create_feature_relationships_story(loader, generator, exporter, df):
    """Create Story 2: Feature Relationships & Correlations."""
    print("Creating feature relationships story...")
    
    # Calculate correlations
    corr_df = loader.calculate_price_correlations(df, top_n=15)
    
    # Correlation heatmap (top features)
    top_features = corr_df['Feature'].head(15).tolist()
    corr_matrix = df[top_features + ['SalePrice']].corr()
    
    # Create descriptive labels for the heatmap
    feature_labels_map = {feat: get_feature_label(feat) for feat in corr_matrix.columns}
    corr_matrix_labeled = corr_matrix.rename(columns=feature_labels_map, index=feature_labels_map)
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix_labeled.values,
        x=corr_matrix_labeled.columns,
        y=corr_matrix_labeled.index,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix_labeled.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 9},
        colorbar=dict(title="Correlation Coefficient")
    ))
    fig_heatmap.update_layout(
        title='Correlation Heatmap: Top Features vs Sale Price',
        xaxis_title='Features',
        yaxis_title='Features',
        template='plotly_white',
        height=600
    )
    exporter.export_figure(fig_heatmap, "feature_correlation_heatmap")
    
    # Feature importance bar chart
    fig_bar = go.Figure()
    # Use descriptive labels for features
    feature_labels = [get_feature_label(feat) for feat in corr_df['Feature']]
    fig_bar.add_trace(go.Bar(
        x=corr_df['Abs_Correlation'],
        y=feature_labels,
        orientation='h',
        marker_color='steelblue',
        text=corr_df['Correlation'].round(3),
        textposition='outside'
    ))
    fig_bar.update_layout(
        title='Top Features Correlated with Sale Price',
        xaxis_title='Absolute Correlation Coefficient with Sale Price',
        yaxis_title='Feature',
        template='plotly_white',
        height=500
    )
    exporter.export_figure(fig_bar, "feature_importance_ranking")
    
    # Scatter plots for top features
    top_3_features = corr_df.head(3)['Feature'].tolist()
    
    for i, feature in enumerate(top_3_features):
        if feature in df.columns:
            feature_label = get_feature_label(feature)
            fig_scatter = go.Figure()
            fig_scatter.add_trace(go.Scatter(
                x=df[feature],
                y=df['SalePrice'],
                mode='markers',
                marker=dict(
                    size=5,
                    opacity=0.6,
                    color='steelblue'
                ),
                name=feature_label
            ))
            fig_scatter.update_layout(
                title=f'{feature_label} vs Sale Price',
                xaxis_title=feature_label,
                yaxis_title='Sale Price ($)',
                template='plotly_white'
            )
            exporter.export_figure(fig_scatter, f"scatter_{feature.lower()}_price")
    
    top_features_list = corr_df.head(10)['Feature'].tolist()
    
    story = {
        'id': 'feature_relationships',
        'slug': 'feature-relationships-correlations',
        'title': 'Feature Relationships & Correlations with Sale Price',
        'description': 'Identifying which features most strongly correlate with house prices',
        'domain': 'housing',
        'narrative': f'''This analysis explores which features are most strongly correlated with house sale prices.

Top Correlated Features:
{chr(10).join([f"- {feat}: {corr_df[corr_df['Feature']==feat]['Correlation'].values[0]:.3f}" for feat in top_features_list[:5]])}

Key Insights:
- {top_features_list[0]} shows the strongest correlation with sale price
- Living area and quality metrics are among the most important predictors
- Understanding these relationships helps prioritize features for predictive modeling
- Some features may require transformation (e.g., log transformation) to improve linear relationships

The correlation heatmap reveals both positive and negative relationships. Features like overall quality, living area, and garage size show strong positive correlations, while features like year built (older houses) may show different patterns.

These insights guide feature engineering and model selection for price prediction.''',
        'visualizations': [
            {
                'id': 'feature_correlation_heatmap',
                'title': 'Feature Correlation Heatmap',
                'type': 'plotly',
                'description': 'Heatmap showing correlations between top features and sale price',
            },
            {
                'id': 'feature_importance_ranking',
                'title': 'Feature Importance Ranking',
                'type': 'plotly',
                'description': 'Bar chart ranking features by correlation strength with sale price',
            },
            {
                'id': f'scatter_{top_3_features[0].lower()}_price',
                'title': f'{top_3_features[0]} vs Sale Price',
                'type': 'plotly',
                'description': f'Scatter plot showing relationship between {top_3_features[0]} and sale price',
            }
        ]
    }
    
    return story


def create_neighborhood_story(loader, generator, exporter, df):
    """Create Story 3: Neighborhood Analysis."""
    print("Creating neighborhood story...")
    
    # Neighborhood statistics
    neighborhood_stats = loader.get_neighborhood_stats(df)
    
    # Average price by neighborhood (bar chart)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=neighborhood_stats['mean'],
        y=neighborhood_stats['Neighborhood'],
        orientation='h',
        marker_color='steelblue',
        text=[f'${x:,.0f}' for x in neighborhood_stats['mean']],
        textposition='outside'
    ))
    fig_bar.update_layout(
        title='Average Sale Price by Neighborhood',
        xaxis_title='Average Sale Price ($)',
        yaxis_title='Neighborhood',
        template='plotly_white',
        height=800
    )
    exporter.export_figure(fig_bar, "neighborhood_avg_price")
    
    # Box plot for top neighborhoods
    top_neighborhoods = neighborhood_stats.head(10)['Neighborhood'].tolist()
    fig_box = go.Figure()
    for neighborhood in top_neighborhoods:
        prices = df[df['Neighborhood'] == neighborhood]['SalePrice']
        fig_box.add_trace(go.Box(
            y=prices,
            name=neighborhood,
            boxpoints='outliers'
        ))
    fig_box.update_layout(
        title='Price Distribution: Top 10 Neighborhoods by Average Price',
        xaxis_title='Neighborhood',
        yaxis_title='Sale Price ($)',
        template='plotly_white',
        height=500
    )
    exporter.export_figure(fig_box, "neighborhood_price_distribution")
    
    # Count by neighborhood
    neighborhood_counts = df['Neighborhood'].value_counts().reset_index()
    neighborhood_counts.columns = ['Neighborhood', 'Count']
    neighborhood_counts = neighborhood_counts.sort_values('Count', ascending=True)
    
    fig_count = go.Figure()
    fig_count.add_trace(go.Bar(
        x=neighborhood_counts['Count'],
        y=neighborhood_counts['Neighborhood'],
        orientation='h',
        marker_color='lightblue'
    ))
    fig_count.update_layout(
        title='Number of Houses by Neighborhood',
        xaxis_title='Number of Houses',
        yaxis_title='Neighborhood',
        template='plotly_white',
        height=800
    )
    exporter.export_figure(fig_count, "neighborhood_counts")
    
    top_5 = neighborhood_stats.head(5)['Neighborhood'].tolist()
    bottom_5 = neighborhood_stats.tail(5)['Neighborhood'].tolist()
    
    story = {
        'id': 'neighborhood_analysis',
        'slug': 'neighborhood-price-analysis',
        'title': 'Neighborhood Impact on House Prices',
        'description': 'Analyzing how different neighborhoods affect house sale prices',
        'domain': 'housing',
        'narrative': f'''This analysis examines the impact of neighborhood location on house sale prices.

Premium Neighborhoods (Top 5 by Average Price):
{chr(10).join([f"- {n}: ${neighborhood_stats[neighborhood_stats['Neighborhood']==n]['mean'].values[0]:,.0f}" for n in top_5])}

Affordable Neighborhoods (Bottom 5 by Average Price):
{chr(10).join([f"- {n}: ${neighborhood_stats[neighborhood_stats['Neighborhood']==n]['mean'].values[0]:,.0f}" for n in bottom_5])}

Key Insights:
- Location is one of the strongest predictors of house price
- Premium neighborhoods can command prices 2-3x higher than average
- Price distributions vary significantly between neighborhoods
- Some neighborhoods have more price variability than others

Understanding neighborhood effects is crucial for accurate price prediction, as location often outweighs many physical features of the house itself.''',
        'visualizations': [
            {
                'id': 'neighborhood_avg_price',
                'title': 'Average Price by Neighborhood',
                'type': 'plotly',
                'description': 'Bar chart showing average sale price for each neighborhood',
            },
            {
                'id': 'neighborhood_price_distribution',
                'title': 'Price Distribution by Neighborhood',
                'type': 'plotly',
                'description': 'Box plots showing price distributions for top neighborhoods',
            },
            {
                'id': 'neighborhood_counts',
                'title': 'House Count by Neighborhood',
                'type': 'plotly',
                'description': 'Number of houses in each neighborhood',
            }
        ]
    }
    
    return story


def create_temporal_trends_story(loader, generator, exporter, df):
    """Create Story 4: Temporal Trends."""
    print("Creating temporal trends story...")
    
    temporal_data = loader.get_temporal_analysis(df)
    
    # Price by YearBuilt
    if 'year_built' in temporal_data:
        year_built = temporal_data['year_built']
        fig_year = go.Figure()
        fig_year.add_trace(go.Scatter(
            x=year_built['YearBuilt'],
            y=year_built['mean'],
            mode='lines+markers',
            name='Mean Price',
            line=dict(color='steelblue', width=2),
            marker=dict(size=4)
        ))
        fig_year.add_trace(go.Scatter(
            x=year_built['YearBuilt'],
            y=year_built['median'],
            mode='lines+markers',
            name='Median Price',
            line=dict(color='orange', width=2, dash='dash'),
            marker=dict(size=4)
        ))
        fig_year.update_layout(
            title='House Prices by Year Built',
            xaxis_title='Year Built',
            yaxis_title='Sale Price ($)',
            template='plotly_white',
            hovermode='x unified'
        )
        exporter.export_figure(fig_year, "price_by_year_built")
    
    # Price by YrSold
    if 'yr_sold' in temporal_data:
        yr_sold = temporal_data['yr_sold']
        fig_sold = go.Figure()
        fig_sold.add_trace(go.Bar(
            x=yr_sold['YrSold'],
            y=yr_sold['mean'],
            name='Mean Price',
            marker_color='steelblue'
        ))
        fig_sold.update_layout(
            title='Average Sale Price by Year Sold',
            xaxis_title='Year Sold',
            yaxis_title='Average Sale Price ($)',
            template='plotly_white'
        )
        exporter.export_figure(fig_sold, "price_by_year_sold")
    
    # Remodeling impact
    if 'remodel' in temporal_data:
        remodel = temporal_data['remodel']
        fig_remodel = go.Figure()
        fig_remodel.add_trace(go.Bar(
            x=['Not Remodeled', 'Remodeled'],
            y=[remodel[remodel['Remodeled']==False]['mean'].values[0] if len(remodel[remodel['Remodeled']==False]) > 0 else 0,
               remodel[remodel['Remodeled']==True]['mean'].values[0] if len(remodel[remodel['Remodeled']==True]) > 0 else 0],
            marker_color=['lightcoral', 'steelblue']
        ))
        fig_remodel.update_layout(
            title='Average Price: Remodeled vs Not Remodeled',
            xaxis_title='Remodeling Status',
            yaxis_title='Average Sale Price ($)',
            template='plotly_white'
        )
        exporter.export_figure(fig_remodel, "remodel_impact")
    
    story = {
        'id': 'temporal_trends',
        'slug': 'temporal-price-trends',
        'title': 'Temporal Trends in House Prices',
        'description': 'How construction year, sale year, and remodeling affect prices',
        'domain': 'housing',
        'narrative': '''This analysis explores how time-related factors influence house sale prices.

Key Findings:
- Older houses (pre-1950) may have lower base prices but can be valuable if well-maintained
- Newer construction (2000+) generally commands premium prices
- Remodeled houses show significant price premiums over non-remodeled houses
- Sale year trends may reflect market conditions during the sale period

Understanding temporal patterns helps account for:
- Age-related depreciation
- Market timing effects
- Value added through remodeling
- Historical appreciation trends

These insights inform feature engineering for predictive models, such as creating age features and remodeling indicators.''',
        'visualizations': [
            {
                'id': 'price_by_year_built',
                'title': 'Price Trends by Year Built',
                'type': 'plotly',
                'description': 'Line chart showing how prices vary by construction year',
            },
            {
                'id': 'price_by_year_sold',
                'title': 'Price Trends by Year Sold',
                'type': 'plotly',
                'description': 'Bar chart showing average prices by sale year',
            },
            {
                'id': 'remodel_impact',
                'title': 'Remodeling Impact on Price',
                'type': 'plotly',
                'description': 'Comparison of prices for remodeled vs non-remodeled houses',
            }
        ]
    }
    
    return story


def create_categorical_impact_story(loader, generator, exporter, df):
    """Create Story 5: Categorical Feature Impact."""
    print("Creating categorical impact story...")
    
    categorical_features = ['OverallQual', 'OverallCond', 'HouseStyle', 'BldgType', 'GarageType', 'Foundation']
    visualizations = []
    
    for cat_feature in categorical_features:
        if cat_feature in df.columns:
            stats = loader.get_categorical_price_stats(df, cat_feature)
            
            # Box plot
            feature_label = get_feature_label(cat_feature)
            fig_box = go.Figure()
            
            # Special handling for OverallQual and OverallCond to show descriptions
            quality_labels = {
                1: 'Very Poor', 2: 'Poor', 3: 'Fair', 4: 'Below Average',
                5: 'Average', 6: 'Above Average', 7: 'Good', 8: 'Very Good',
                9: 'Excellent', 10: 'Very Excellent'
            }
            
            for category in stats[cat_feature].head(10):  # Top 10 by mean
                prices = df[df[cat_feature] == category]['SalePrice']
                # Use descriptive name for quality ratings
                if cat_feature == 'OverallQual' and category in quality_labels:
                    display_name = f'{category} - {quality_labels[category]}'
                elif cat_feature == 'OverallCond' and category in quality_labels:
                    display_name = f'{category} - {quality_labels[category]}'
                else:
                    display_name = str(category)
                
                fig_box.add_trace(go.Box(
                    y=prices,
                    name=display_name,
                    boxpoints='outliers'
                ))
            fig_box.update_layout(
                title=f'Sale Price by {feature_label}',
                xaxis_title=feature_label,
                yaxis_title='Sale Price ($)',
                template='plotly_white',
                height=500
            )
            viz_id = f"categorical_{cat_feature.lower()}_box"
            exporter.export_figure(fig_box, viz_id)
            visualizations.append({
                'id': viz_id,
                'title': f'Price Distribution by {cat_feature}',
                'type': 'plotly',
                'description': f'Box plots showing price distributions across {cat_feature} categories',
            })
    
    story = {
        'id': 'categorical_impact',
        'slug': 'categorical-feature-impact',
        'title': 'Categorical Feature Impact on Prices',
        'description': 'How categorical features like quality, style, and type influence house prices',
        'domain': 'housing',
        'narrative': '''This analysis examines how categorical features influence house sale prices.

Key Categorical Features:
- Overall Quality: Strongest predictor - quality ratings directly correlate with price
- Overall Condition: Houses in better condition command higher prices
- House Style: 2-story and newer styles tend to be more valuable
- Building Type: Single-family detached homes are typically most valuable
- Garage Type: Attached and built-in garages add more value
- Foundation: Poured concrete foundations are associated with higher prices

Key Insights:
- Quality and condition ratings show clear step-wise price increases
- Some categorical features may need encoding (one-hot, ordinal, or target encoding)
- Feature interactions between categoricals can be important
- Missing values in categoricals often represent "None" (e.g., no garage, no basement)

Understanding these relationships helps in feature engineering and model selection for price prediction.''',
        'visualizations': visualizations[:6]  # Limit to 6 visualizations
    }
    
    return story


def create_living_space_story(loader, generator, exporter, df):
    """Create Story 6: Living Space & Quality Analysis."""
    print("Creating living space story...")
    
    # GrLivArea vs SalePrice colored by OverallQual
    if 'GrLivArea' in df.columns and 'OverallQual' in df.columns:
        quality_labels = {
            1: 'Very Poor', 2: 'Poor', 3: 'Fair', 4: 'Below Average',
            5: 'Average', 6: 'Above Average', 7: 'Good', 8: 'Very Good',
            9: 'Excellent', 10: 'Very Excellent'
        }
        fig_scatter = go.Figure()
        for qual in sorted(df['OverallQual'].unique()):
            subset = df[df['OverallQual'] == qual]
            qual_label = quality_labels.get(qual, f'Quality {qual}')
            fig_scatter.add_trace(go.Scatter(
                x=subset['GrLivArea'],
                y=subset['SalePrice'],
                mode='markers',
                name=f'Quality {qual} ({qual_label})',
                marker=dict(size=5, opacity=0.6)
            ))
        fig_scatter.update_layout(
            title='Living Area vs Sale Price (by Overall Quality Rating)',
            xaxis_title='Above Grade Living Area (square feet)',
            yaxis_title='Sale Price ($)',
            template='plotly_white',
            hovermode='closest'
        )
        exporter.export_figure(fig_scatter, "livarea_quality_scatter")
    
    # TotalBsmtSF vs SalePrice
    if 'TotalBsmtSF' in df.columns:
        fig_basement = go.Figure()
        fig_basement.add_trace(go.Scatter(
            x=df['TotalBsmtSF'],
            y=df['SalePrice'],
            mode='markers',
            marker=dict(size=5, opacity=0.6, color='steelblue')
        ))
        fig_basement.update_layout(
            title='Total Basement Area vs Sale Price',
            xaxis_title='Total Basement Area (sq ft)',
            yaxis_title='Sale Price ($)',
            template='plotly_white'
        )
        exporter.export_figure(fig_basement, "basement_area_scatter")
    
    # Room count analysis
    if 'TotRmsAbvGrd' in df.columns:
        room_stats = loader.get_categorical_price_stats(df, 'TotRmsAbvGrd')
        fig_rooms = go.Figure()
        fig_rooms.add_trace(go.Bar(
            x=room_stats['TotRmsAbvGrd'],
            y=room_stats['mean'],
            marker_color='steelblue',
            text=[f'${x:,.0f}' for x in room_stats['mean']],
            textposition='outside'
        ))
        fig_rooms.update_layout(
            title='Average Sale Price by Total Rooms Above Grade',
            xaxis_title='Total Rooms Above Grade',
            yaxis_title='Average Sale Price ($)',
            template='plotly_white'
        )
        exporter.export_figure(fig_rooms, "price_by_rooms")
    
    story = {
        'id': 'living_space',
        'slug': 'living-space-quality-analysis',
        'title': 'Living Space & Quality Analysis',
        'description': 'Relationship between house size, quality, and sale price',
        'domain': 'housing',
        'narrative': '''This analysis explores how living space and quality interact to determine house prices.

Key Relationships:
- Larger living areas generally command higher prices, but quality matters more
- The relationship between size and price is non-linear - diminishing returns at larger sizes
- Basement area adds value, especially when finished
- Room count shows a positive relationship with price up to a point

Key Insights:
- Quality amplifies the value of living space - a small high-quality house can be worth more than a large low-quality one
- There are optimal size ranges that maximize value per square foot
- Outliers in living area may indicate data quality issues or special properties
- Feature interactions between size and quality are important for prediction

Understanding these relationships helps create better features for predictive modeling, such as:
- Size per quality ratios
- Optimal size indicators
- Quality-adjusted size metrics''',
        'visualizations': [
            {
                'id': 'livarea_quality_scatter',
                'title': 'Living Area vs Price by Quality',
                'type': 'plotly',
                'description': 'Scatter plot showing living area vs price, colored by overall quality',
            },
            {
                'id': 'basement_area_scatter',
                'title': 'Basement Area vs Sale Price',
                'type': 'plotly',
                'description': 'Scatter plot showing relationship between basement area and price',
            },
            {
                'id': 'price_by_rooms',
                'title': 'Price by Room Count',
                'type': 'plotly',
                'description': 'Bar chart showing average price by number of rooms',
            }
        ]
    }
    
    return story


def create_missing_data_story(loader, generator, exporter, df):
    """Create Story 7: Missing Data Patterns."""
    print("Creating missing data story...")
    
    missing_df = loader.analyze_missing_data(df)
    
    # Missing data percentage bar chart
    if len(missing_df) > 0:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=missing_df['Missing_Percentage'],
            y=missing_df['Feature'],
            orientation='h',
            marker_color='coral',
            text=[f"{x:.1f}%" for x in missing_df['Missing_Percentage']],
            textposition='outside'
        ))
        fig_bar.update_layout(
            title='Missing Data Percentage by Feature',
            xaxis_title='Missing Data Percentage (%)',
            yaxis_title='Feature',
            template='plotly_white',
            height=600
        )
        exporter.export_figure(fig_bar, "missing_data_percentage")
        
        # Missing data heatmap (top features with missing data)
        top_missing = missing_df.head(20)['Feature'].tolist()
        missing_matrix = df[top_missing].isnull().astype(int)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=missing_matrix.T.values,
            x=missing_matrix.index[:100],  # Sample first 100 rows for performance
            y=missing_matrix.columns,
            colorscale='Reds',
            showscale=True
        ))
        fig_heatmap.update_layout(
            title='Missing Data Pattern (Sample)',
            xaxis_title='House Index',
            yaxis_title='Feature',
            template='plotly_white',
            height=500
        )
        exporter.export_figure(fig_heatmap, "missing_data_heatmap")
        
        top_missing_list = missing_df.head(10)['Feature'].tolist()
        
        story = {
            'id': 'missing_data',
            'slug': 'missing-data-patterns',
            'title': 'Missing Data Patterns',
            'description': 'Understanding data completeness and missing value patterns',
            'domain': 'housing',
            'narrative': f'''This analysis examines missing data patterns in the dataset.

Features with Most Missing Data:
{chr(10).join([f"- {feat}: {missing_df[missing_df['Feature']==feat]['Missing_Percentage'].values[0]:.1f}%" for feat in top_missing_list[:5]])}

Key Insights:
- Many missing values represent "None" or "Not Applicable" (e.g., no pool, no garage, no basement)
- Some features have systematic missingness that should be encoded as a separate category
- Missing data patterns can reveal feature relationships (e.g., if no garage, GarageArea is missing)
- Understanding missingness is crucial for proper imputation or encoding strategies

Handling Missing Data:
- Categorical: Encode "NA" as a category (e.g., "No Garage", "No Pool")
- Numerical: May need imputation or indicator variables
- Some missingness may be informative (e.g., missing basement = no basement)

Proper handling of missing data is essential for accurate price prediction.''',
            'visualizations': [
                {
                    'id': 'missing_data_percentage',
                    'title': 'Missing Data by Feature',
                    'type': 'plotly',
                    'description': 'Bar chart showing percentage of missing data for each feature',
                },
                {
                    'id': 'missing_data_heatmap',
                    'title': 'Missing Data Pattern',
                    'type': 'plotly',
                    'description': 'Heatmap showing missing data patterns across features',
                }
            ]
        }
    else:
        story = {
            'id': 'missing_data',
            'slug': 'missing-data-patterns',
            'title': 'Missing Data Patterns',
            'description': 'Understanding data completeness and missing value patterns',
            'domain': 'housing',
            'narrative': 'No significant missing data patterns found in the dataset.',
            'visualizations': []
        }
    
    return story


def main():
    """Generate all housing stories."""
    print("🏠 Generating comprehensive housing data analysis stories...\n")
    
    # Initialize components
    loader = HousingDataLoader()
    generator = PlotlyGenerator()
    exporter = PlotlyExporter()
    
    # Load data
    print("Loading training data...")
    df = loader.load_train_data()
    print(f"Loaded {len(df)} houses with {len(df.columns)} features\n")
    
    # Create output directories
    stories_dir = Path("data/viz/stories")
    stories_dir.mkdir(parents=True, exist_ok=True)
    
    stories = []
    
    # Generate all stories
    try:
        story1 = create_price_distribution_story(loader, generator, exporter, df)
        if story1:
            stories.append(story1)
            with open(stories_dir / f"{story1['slug']}.json", 'w') as f:
                json.dump(story1, f, indent=2)
    except Exception as e:
        print(f"Error creating price distribution story: {e}")
    
    try:
        story2 = create_feature_relationships_story(loader, generator, exporter, df)
        if story2:
            stories.append(story2)
            with open(stories_dir / f"{story2['slug']}.json", 'w') as f:
                json.dump(story2, f, indent=2)
    except Exception as e:
        print(f"Error creating feature relationships story: {e}")
    
    try:
        story3 = create_neighborhood_story(loader, generator, exporter, df)
        if story3:
            stories.append(story3)
            with open(stories_dir / f"{story3['slug']}.json", 'w') as f:
                json.dump(story3, f, indent=2)
    except Exception as e:
        print(f"Error creating neighborhood story: {e}")
    
    try:
        story4 = create_temporal_trends_story(loader, generator, exporter, df)
        if story4:
            stories.append(story4)
            with open(stories_dir / f"{story4['slug']}.json", 'w') as f:
                json.dump(story4, f, indent=2)
    except Exception as e:
        print(f"Error creating temporal trends story: {e}")
    
    try:
        story5 = create_categorical_impact_story(loader, generator, exporter, df)
        if story5:
            stories.append(story5)
            with open(stories_dir / f"{story5['slug']}.json", 'w') as f:
                json.dump(story5, f, indent=2)
    except Exception as e:
        print(f"Error creating categorical impact story: {e}")
    
    try:
        story6 = create_living_space_story(loader, generator, exporter, df)
        if story6:
            stories.append(story6)
            with open(stories_dir / f"{story6['slug']}.json", 'w') as f:
                json.dump(story6, f, indent=2)
    except Exception as e:
        print(f"Error creating living space story: {e}")
    
    try:
        story7 = create_missing_data_story(loader, generator, exporter, df)
        if story7:
            stories.append(story7)
            with open(stories_dir / f"{story7['slug']}.json", 'w') as f:
                json.dump(story7, f, indent=2)
    except Exception as e:
        print(f"Error creating missing data story: {e}")
    
    print(f"\n✅ Generated {len(stories)} stories:")
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
                'tool': 'plotly',
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
    
    print(f"\n✅ Created visualization index with {len(all_viz)} visualizations")


if __name__ == "__main__":
    main()

