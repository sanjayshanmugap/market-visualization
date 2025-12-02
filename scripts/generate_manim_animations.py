"""
Script to generate Manim animations for stock market data visualizations.

This script creates mathematical animations showing:
- Stock price movements with derivatives
- Moving averages with equations
- Fourier transforms of price data
- Correlation matrix animations
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.viz.data_loaders.financial_loader import FinancialDataLoader
from src.viz.generators.manim_gen import ManimGenerator


def create_stock_price_animation():
    """Create an animated stock price chart with mathematical annotations."""
    print("Creating stock price animation...")
    
    loader = FinancialDataLoader()
    generator = ManimGenerator()
    
    # Load stock data
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    stock_data = loader.load_stock_data(symbols, period='6mo')
    
    if not stock_data or len(stock_data) == 0:
        print("Warning: No stock data loaded, using sample data")
        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 2)
        stock_data = pd.DataFrame({
            'Date': dates,
            'Close': prices
        })
    else:
        # Use first symbol's data
        stock_data = stock_data[stock_data['Symbol'] == symbols[0]] if 'Symbol' in stock_data.columns else stock_data
    
    # Create animation
    output_path = generator.stock_price_animation(
        data=stock_data,
        price_col='Close',
        date_col='Date',
        title='Stock Price Movement with Mathematical Analysis',
        output_name='stock_price_manim',
        show_equation=True,
        show_derivative=True,
    )
    
    print(f"Animation metadata saved to: {output_path}")
    print("Note: To render the actual video, you'll need to:")
    print("  1. Install Manim: pip install manim")
    print("  2. Create a Manim scene file from the metadata")
    print("  3. Run: manim -pql scene_file.py SceneName")
    
    return output_path


def create_correlation_animation():
    """Create an animated correlation matrix."""
    print("Creating correlation matrix animation...")
    
    loader = FinancialDataLoader()
    generator = ManimGenerator()
    
    # Load stock data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stock_data = loader.load_stock_data(symbols, period='1y')
    
    if not stock_data:
        print("Warning: No stock data loaded")
        return None
    
    # Calculate correlation matrix
    corr_matrix = loader.calculate_correlation_matrix(stock_data)
    
    if corr_matrix is not None and not corr_matrix.empty:
        output_path = generator.correlation_matrix_animation(
            correlation_matrix=corr_matrix,
            title='Stock Correlation Matrix Animation',
            output_name='correlation_manim',
        )
        print(f"Animation metadata saved to: {output_path}")
        return output_path
    
    return None


def main():
    """Generate all Manim animations."""
    print("🎬 Generating Manim animations for stock market data...\n")
    
    try:
        # Check if Manim is available
        from manim import Scene
        print("✓ Manim is installed\n")
    except ImportError:
        print("⚠ Manim is not installed. Install with: pip install manim")
        print("This script will still create metadata files for animations.\n")
    
    animations = []
    
    # Generate stock price animation
    try:
        price_anim = create_stock_price_animation()
        if price_anim:
            animations.append(price_anim)
    except Exception as e:
        print(f"Error creating stock price animation: {e}")
    
    print()
    
    # Generate correlation animation
    try:
        corr_anim = create_correlation_animation()
        if corr_anim:
            animations.append(corr_anim)
    except Exception as e:
        print(f"Error creating correlation animation: {e}")
    
    print(f"\n✅ Generated metadata for {len(animations)} animations")
    print("\nTo render the actual videos:")
    print("  1. Ensure Manim is installed: pip install manim")
    print("  2. Create Manim scene files based on the metadata")
    print("  3. Render with: manim -pql scene_file.py SceneName")
    print("\nFor more information, see: https://docs.manim.community/")


if __name__ == "__main__":
    main()

