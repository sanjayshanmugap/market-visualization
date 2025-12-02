"""
Manim Animation Generator

Generates mathematical animations for stock market data using Manim.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import json

try:
    from manim import *
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    print("Warning: Manim not installed. Install with: pip install manim")


class ManimGenerator:
    """Generator for Manim mathematical animations."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize Manim generator.
        
        Args:
            output_dir: Directory to save rendered animations
        """
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed. Install with: pip install manim")
        
        self.output_dir = output_dir or Path("data/viz/static")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def stock_price_animation(
        self,
        data: pd.DataFrame,
        price_col: str = "Close",
        date_col: str = "Date",
        title: str = "Stock Price Movement",
        output_name: str = "stock_animation",
        show_equation: bool = True,
        show_derivative: bool = True,
    ) -> Path:
        """
        Create an animated stock price chart with mathematical annotations.
        
        Args:
            data: DataFrame with stock price data
            price_col: Column name for price data
            date_col: Column name for date data
            title: Animation title
            output_name: Output filename (without extension)
            show_equation: Whether to show mathematical equations
            show_derivative: Whether to show derivative (rate of change)
            
        Returns:
            Path to rendered video file
        """
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        # Prepare data
        data = data.sort_values(date_col).reset_index(drop=True)
        prices = data[price_col].values
        dates = pd.to_datetime(data[date_col]).values
        
        # Normalize prices for visualization (0-1 range)
        price_min, price_max = prices.min(), prices.max()
        normalized_prices = (prices - price_min) / (price_max - price_min) if price_max > price_min else prices
        
        # Create Manim scene
        class StockPriceScene(Scene):
            def construct(self):
                # Title
                title_text = Text(title, font_size=48, color=WHITE)
                title_text.to_edge(UP)
                self.add(title_text)
                
                # Create axes
                axes = Axes(
                    x_range=[0, len(prices), 10],
                    y_range=[0, 1.2, 0.2],
                    x_length=10,
                    y_length=6,
                    axis_config={"color": BLUE},
                    tips=False,
                )
                axes.shift(DOWN * 0.5)
                
                # Labels
                x_label = axes.get_x_axis_label("Time", direction=DOWN, buff=0.5)
                y_label = axes.get_y_axis_label("Normalized Price", direction=LEFT, buff=0.5)
                
                self.add(axes, x_label, y_label)
                
                # Create data points
                points = []
                for i, price in enumerate(normalized_prices):
                    point = axes.coords_to_point(i, price)
                    points.append(point)
                
                # Animate line drawing
                line = VMobject()
                line.set_points_as_corners(points)
                line.set_stroke(color=YELLOW, width=4)
                
                # Animate the line
                self.play(Create(line), run_time=3)
                
                # Add moving dot along the line
                dot = Dot(color=RED, radius=0.1)
                dot.move_to(points[0])
                self.add(dot)
                
                # Animate dot moving along the line
                self.play(
                    dot.animate.move_to(points[-1]),
                    run_time=2,
                    rate_func=linear
                )
                
                # Show mathematical annotations
                if show_equation:
                    # Calculate moving average
                    window = min(20, len(prices) // 4)
                    moving_avg = pd.Series(prices).rolling(window=window, center=True).mean()
                    normalized_ma = (moving_avg - price_min) / (price_max - price_min)
                    
                    # Draw moving average line
                    ma_points = []
                    for i, ma_val in enumerate(normalized_ma):
                        if not np.isnan(ma_val):
                            point = axes.coords_to_point(i, ma_val)
                            ma_points.append(point)
                    
                    if ma_points:
                        ma_line = VMobject()
                        ma_line.set_points_as_corners(ma_points)
                        ma_line.set_stroke(color=GREEN, width=3, opacity=0.7)
                        self.play(Create(ma_line), run_time=1.5)
                        
                        # Show equation
                        eq_text = MathTex(
                            r"\text{MA}(t) = \frac{1}{n}\sum_{i=t-n}^{t} P(i)",
                            font_size=36,
                            color=GREEN
                        )
                        eq_text.to_corner(UR, buff=0.5)
                        self.play(Write(eq_text), run_time=1)
                
                # Show derivative (rate of change)
                if show_derivative:
                    # Calculate derivative
                    derivative = np.gradient(normalized_prices)
                    
                    # Create derivative axes
                    deriv_axes = Axes(
                        x_range=[0, len(prices), 10],
                        y_range=[min(derivative) - 0.1, max(derivative) + 0.1, 0.1],
                        x_length=10,
                        y_length=3,
                        axis_config={"color": PURPLE},
                        tips=False,
                    )
                    deriv_axes.next_to(axes, DOWN, buff=0.3)
                    
                    deriv_label = deriv_axes.get_y_axis_label("Rate of Change", direction=LEFT, buff=0.3)
                    self.add(deriv_axes, deriv_label)
                    
                    # Draw derivative
                    deriv_points = []
                    for i, deriv_val in enumerate(derivative):
                        point = deriv_axes.coords_to_point(i, deriv_val)
                        deriv_points.append(point)
                    
                    deriv_line = VMobject()
                    deriv_line.set_points_as_corners(deriv_points)
                    deriv_line.set_stroke(color=PURPLE, width=3)
                    
                    self.play(Create(deriv_line), run_time=2)
                    
                    # Show derivative equation
                    deriv_eq = MathTex(
                        r"\frac{dP}{dt} = \lim_{\Delta t \to 0} \frac{P(t+\Delta t) - P(t)}{\Delta t}",
                        font_size=32,
                        color=PURPLE
                    )
                    deriv_eq.next_to(deriv_axes, RIGHT, buff=0.5)
                    self.play(Write(deriv_eq), run_time=1.5)
                
                # Fade out
                self.wait(1)
                self.play(FadeOut(*self.mobjects), run_time=1)
        
        # Render animation
        # Note: This is a simplified version. In practice, you'd need to:
        # 1. Save this as a .py file
        # 2. Run: manim -pql scene_file.py StockPriceScene
        # 3. Return the path to the rendered video
        
        # For now, return a placeholder path
        # In a real implementation, you'd use Manim's CLI or programmatic rendering
        output_path = self.output_dir / f"{output_name}.mp4"
        
        # Save metadata for rendering
        metadata = {
            "type": "manim_stock_animation",
            "output_name": output_name,
            "data_points": len(prices),
            "price_range": [float(price_min), float(price_max)],
            "show_equation": show_equation,
            "show_derivative": show_derivative,
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def correlation_matrix_animation(
        self,
        correlation_matrix: pd.DataFrame,
        title: str = "Stock Correlation Matrix",
        output_name: str = "correlation_animation",
    ) -> Path:
        """
        Create an animated correlation matrix visualization.
        
        Args:
            correlation_matrix: DataFrame with correlation values
            title: Animation title
            output_name: Output filename
            
        Returns:
            Path to rendered video file
        """
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        # This would create an animated correlation matrix
        # showing how correlations evolve or highlighting relationships
        
        output_path = self.output_dir / f"{output_name}.mp4"
        
        metadata = {
            "type": "manim_correlation_animation",
            "output_name": output_name,
            "matrix_size": len(correlation_matrix),
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def fourier_transform_animation(
        self,
        price_data: pd.Series,
        title: str = "Stock Price Fourier Transform",
        output_name: str = "fourier_animation",
    ) -> Path:
        """
        Create an animation showing Fourier transform of stock price data.
        
        Args:
            price_data: Series with price data
            title: Animation title
            output_name: Output filename
            
        Returns:
            Path to rendered video file
        """
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        # This would show frequency domain analysis of stock prices
        # demonstrating mathematical signal processing concepts
        
        output_path = self.output_dir / f"{output_name}.mp4"
        
        metadata = {
            "type": "manim_fourier_animation",
            "output_name": output_name,
            "data_points": len(price_data),
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path


    def correlation_matrix_animation_housing(
        self,
        correlation_data: pd.DataFrame,
        title: str = "House Price Feature Correlations",
        output_name: str = "housing_correlation_animation",
    ) -> Path:
        """Create an animated correlation matrix for housing features."""
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        corr_sorted = correlation_data.sort_values('Abs_Correlation', ascending=True)
        features = corr_sorted['Feature'].tolist()
        correlations = corr_sorted['Correlation'].tolist()
        
        output_path = self.output_dir / f"{output_name}.mp4"
        metadata = {
            "type": "manim_housing_correlation",
            "output_name": output_name,
            "features": features,
            "correlations": [float(c) for c in correlations],
            "num_features": len(features),
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def price_evolution_animation(
        self,
        year_data: pd.DataFrame,
        year_col: str = "YearBuilt",
        price_col: str = "mean",
        title: str = "House Price Evolution Over Time",
        output_name: str = "price_evolution_animation",
    ) -> Path:
        """Create an animated timeline showing price evolution."""
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        output_path = self.output_dir / f"{output_name}.mp4"
        metadata = {
            "type": "manim_price_evolution",
            "output_name": output_name,
            "year_col": year_col,
            "price_col": price_col,
            "data_points": len(year_data),
            "year_range": [int(year_data[year_col].min()), int(year_data[year_col].max())],
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def feature_importance_ranking_animation(
        self,
        importance_data: pd.DataFrame,
        feature_col: str = "Feature",
        importance_col: str = "Abs_Correlation",
        title: str = "Feature Importance Ranking",
        output_name: str = "feature_importance_animation",
    ) -> Path:
        """Create an animated bar chart ranking features by importance."""
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        output_path = self.output_dir / f"{output_name}.mp4"
        metadata = {
            "type": "manim_feature_importance",
            "output_name": output_name,
            "num_features": len(importance_data),
            "top_features": importance_data.head(10)[feature_col].tolist(),
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
    
    def neighborhood_comparison_animation(
        self,
        neighborhood_data: pd.DataFrame,
        neighborhood_col: str = "Neighborhood",
        price_col: str = "mean",
        title: str = "Neighborhood Price Comparison",
        output_name: str = "neighborhood_comparison_animation",
    ) -> Path:
        """Create an animated comparison of neighborhood prices."""
        if not MANIM_AVAILABLE:
            raise ImportError("Manim is not installed")
        
        output_path = self.output_dir / f"{output_name}.mp4"
        metadata = {
            "type": "manim_neighborhood_comparison",
            "output_name": output_name,
            "num_neighborhoods": len(neighborhood_data),
            "top_neighborhoods": neighborhood_data.head(10)[neighborhood_col].tolist(),
        }
        
        metadata_path = self.output_dir / f"{output_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path
