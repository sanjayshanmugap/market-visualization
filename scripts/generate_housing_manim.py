"""
Script to generate Manim animations for housing data visualizations.

This script creates mathematical animations showing:
- Correlation matrix building up
- Price evolution over time
- Feature importance rankings
- Neighborhood price comparisons
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.viz.data_loaders.housing_loader import HousingDataLoader
from src.viz.generators.manim_gen import ManimGenerator


def create_correlation_animation():
    """Create correlation matrix animation."""
    print("Creating correlation matrix animation...")
    
    loader = HousingDataLoader()
    generator = ManimGenerator()
    
    # Load data
    df = loader.load_train_data()
    
    # Calculate correlations
    corr_df = loader.calculate_price_correlations(df, top_n=15)
    
    # Create animation
    output_path = generator.correlation_matrix_animation_housing(
        correlation_data=corr_df,
        title="House Price Feature Correlations",
        output_name="housing_correlation_animation",
    )
    
    print(f"✓ Correlation animation metadata saved to: {output_path}")
    return output_path


def create_price_evolution_animation():
    """Create price evolution over time animation."""
    print("Creating price evolution animation...")
    
    loader = HousingDataLoader()
    generator = ManimGenerator()
    
    # Load data
    df = loader.load_train_data()
    
    # Get temporal data
    temporal_data = loader.get_temporal_analysis(df)
    
    if 'year_built' in temporal_data:
        year_built = temporal_data['year_built']
        
        output_path = generator.price_evolution_animation(
            year_data=year_built,
            year_col='YearBuilt',
            price_col='mean',
            title="House Price Evolution by Year Built",
            output_name="price_evolution_animation",
        )
        
        print(f"✓ Price evolution animation metadata saved to: {output_path}")
        return output_path
    
    return None


def create_feature_importance_animation():
    """Create feature importance ranking animation."""
    print("Creating feature importance animation...")
    
    loader = HousingDataLoader()
    generator = ManimGenerator()
    
    # Load data
    df = loader.load_train_data()
    
    # Calculate feature importance
    importance_df = loader.calculate_price_correlations(df, top_n=12)
    
    output_path = generator.feature_importance_ranking_animation(
        importance_data=importance_df,
        feature_col='Feature',
        importance_col='Abs_Correlation',
        title="Feature Importance Ranking",
        output_name="feature_importance_animation",
    )
    
    print(f"✓ Feature importance animation metadata saved to: {output_path}")
    return output_path


def create_neighborhood_comparison_animation():
    """Create neighborhood price comparison animation."""
    print("Creating neighborhood comparison animation...")
    
    loader = HousingDataLoader()
    generator = ManimGenerator()
    
    # Load data
    df = loader.load_train_data()
    
    # Get neighborhood stats
    neighborhood_stats = loader.get_neighborhood_stats(df)
    
    output_path = generator.neighborhood_comparison_animation(
        neighborhood_data=neighborhood_stats.head(12),
        neighborhood_col='Neighborhood',
        price_col='mean',
        title="Neighborhood Price Comparison",
        output_name="neighborhood_comparison_animation",
    )
    
    print(f"✓ Neighborhood comparison animation metadata saved to: {output_path}")
    return output_path


def main():
    """Generate all Manim animations."""
    print("🎬 Generating Manim animations for housing data...\n")
    
    try:
        # Check if Manim is available
        from manim import Scene
        print("✓ Manim is installed\n")
    except ImportError:
        print("⚠ Manim is not installed. Install with: pip install manim")
        print("This script will still create metadata files for animations.\n")
    
    animations = []
    
    # Generate animations
    try:
        anim1 = create_correlation_animation()
        if anim1:
            animations.append(anim1)
    except Exception as e:
        print(f"Error creating correlation animation: {e}")
    
    print()
    
    try:
        anim2 = create_price_evolution_animation()
        if anim2:
            animations.append(anim2)
    except Exception as e:
        print(f"Error creating price evolution animation: {e}")
    
    print()
    
    try:
        anim3 = create_feature_importance_animation()
        if anim3:
            animations.append(anim3)
    except Exception as e:
        print(f"Error creating feature importance animation: {e}")
    
    print()
    
    try:
        anim4 = create_neighborhood_comparison_animation()
        if anim4:
            animations.append(anim4)
    except Exception as e:
        print(f"Error creating neighborhood comparison animation: {e}")
    
    print(f"\n✅ Generated metadata for {len(animations)} animations")
    print("\nTo render the actual videos:")
    print("  1. Ensure Manim is installed: pip install manim")
    print("  2. Create Manim scene files based on the metadata")
    print("  3. Render with: manim -pql scene_file.py SceneName")
    print("\nFor more information, see: https://docs.manim.community/")


if __name__ == "__main__":
    main()

