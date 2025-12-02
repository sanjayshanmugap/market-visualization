"""
Housing Data Loader

Loads and processes the House Prices Advanced Regression Techniques dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import json


class HousingDataLoader:
    """Loader for housing/real estate data."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize housing data loader.
        
        Args:
            data_dir: Directory containing the dataset
        """
        if data_dir is None:
            # Look for dataset in project root
            project_root = Path(__file__).parent.parent.parent.parent
            data_dir = project_root / "house-prices-advanced-regression-techniques"
        
        self.data_dir = Path(data_dir)
        self.train_path = self.data_dir / "train.csv"
        self.test_path = self.data_dir / "test.csv"
    
    def load_train_data(self) -> pd.DataFrame:
        """
        Load training data.
        
        Returns:
            DataFrame with training data including SalePrice
        """
        if not self.train_path.exists():
            raise FileNotFoundError(f"Training data not found at {self.train_path}")
        
        df = pd.read_csv(self.train_path)
        return df
    
    def load_test_data(self) -> pd.DataFrame:
        """
        Load test data.
        
        Returns:
            DataFrame with test data (no SalePrice)
        """
        if not self.test_path.exists():
            raise FileNotFoundError(f"Test data not found at {self.test_path}")
        
        df = pd.read_csv(self.test_path)
        return df
    
    def get_numerical_features(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of numerical feature columns.
        
        Args:
            df: DataFrame
            
        Returns:
            List of numerical column names
        """
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_categorical_features(self, df: pd.DataFrame) -> List[str]:
        """
        Get list of categorical feature columns.
        
        Args:
            df: DataFrame
            
        Returns:
            List of categorical column names
        """
        return df.select_dtypes(include=['object']).columns.tolist()
    
    def analyze_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze missing data patterns.
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with missing data statistics
        """
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        
        missing_df = pd.DataFrame({
            'Feature': missing.index,
            'Missing_Count': missing.values,
            'Missing_Percentage': missing_pct.values
        })
        
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
            'Missing_Count', ascending=False
        )
        
        return missing_df
    
    def calculate_price_correlations(
        self,
        df: pd.DataFrame,
        top_n: int = 20
    ) -> pd.DataFrame:
        """
        Calculate correlations with SalePrice.
        
        Args:
            df: DataFrame with SalePrice column
            top_n: Number of top features to return
            
        Returns:
            DataFrame with correlations sorted by absolute value
        """
        if 'SalePrice' not in df.columns:
            raise ValueError("DataFrame must contain 'SalePrice' column")
        
        # Get numerical features
        numerical_cols = self.get_numerical_features(df)
        numerical_cols = [col for col in numerical_cols if col != 'SalePrice' and col != 'Id']
        
        # Calculate correlations
        correlations = df[numerical_cols + ['SalePrice']].corr()['SalePrice'].drop('SalePrice')
        correlations = correlations.sort_values(key=abs, ascending=False)
        
        # Create DataFrame
        corr_df = pd.DataFrame({
            'Feature': correlations.index,
            'Correlation': correlations.values,
            'Abs_Correlation': correlations.abs().values
        }).sort_values('Abs_Correlation', ascending=False)
        
        return corr_df.head(top_n)
    
    def get_neighborhood_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get statistics by neighborhood.
        
        Args:
            df: DataFrame with Neighborhood and SalePrice columns
            
        Returns:
            DataFrame with neighborhood statistics
        """
        if 'Neighborhood' not in df.columns or 'SalePrice' not in df.columns:
            raise ValueError("DataFrame must contain 'Neighborhood' and 'SalePrice' columns")
        
        stats = df.groupby('Neighborhood')['SalePrice'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max')
        ]).reset_index()
        
        stats = stats.sort_values('mean', ascending=False)
        
        return stats
    
    def get_temporal_analysis(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Analyze temporal trends.
        
        Args:
            df: DataFrame with YearBuilt, YearRemodAdd, YrSold, SalePrice
            
        Returns:
            Dictionary with temporal analysis DataFrames
        """
        if 'SalePrice' not in df.columns:
            raise ValueError("DataFrame must contain 'SalePrice' column")
        
        results = {}
        
        # Price by YearBuilt
        if 'YearBuilt' in df.columns:
            year_built = df.groupby('YearBuilt')['SalePrice'].agg([
                ('count', 'count'),
                ('mean', 'mean'),
                ('median', 'median')
            ]).reset_index()
            year_built = year_built.sort_values('YearBuilt')
            results['year_built'] = year_built
        
        # Price by YrSold
        if 'YrSold' in df.columns:
            yr_sold = df.groupby('YrSold')['SalePrice'].agg([
                ('count', 'count'),
                ('mean', 'mean'),
                ('median', 'median')
            ]).reset_index()
            yr_sold = yr_sold.sort_values('YrSold')
            results['yr_sold'] = yr_sold
        
        # Remodeling analysis
        if 'YearRemodAdd' in df.columns and 'YearBuilt' in df.columns:
            df_copy = df.copy()
            df_copy['Remodeled'] = df_copy['YearRemodAdd'] != df_copy['YearBuilt']
            remodel_stats = df_copy.groupby('Remodeled')['SalePrice'].agg([
                ('count', 'count'),
                ('mean', 'mean'),
                ('median', 'median')
            ]).reset_index()
            results['remodel'] = remodel_stats
        
        return results
    
    def get_categorical_price_stats(
        self,
        df: pd.DataFrame,
        categorical_col: str
    ) -> pd.DataFrame:
        """
        Get price statistics by categorical feature.
        
        Args:
            df: DataFrame with categorical column and SalePrice
            categorical_col: Name of categorical column
            
        Returns:
            DataFrame with price statistics by category
        """
        if categorical_col not in df.columns:
            raise ValueError(f"Column '{categorical_col}' not found in DataFrame")
        if 'SalePrice' not in df.columns:
            raise ValueError("DataFrame must contain 'SalePrice' column")
        
        stats = df.groupby(categorical_col)['SalePrice'].agg([
            ('count', 'count'),
            ('mean', 'mean'),
            ('median', 'median'),
            ('std', 'std'),
            ('min', 'min'),
            ('max', 'max')
        ]).reset_index()
        
        stats = stats.sort_values('mean', ascending=False)
        
        return stats
    
    def prepare_feature_importance_data(
        self,
        df: pd.DataFrame,
        top_n: int = 15
    ) -> pd.DataFrame:
        """
        Prepare data for feature importance visualization.
        
        Args:
            df: DataFrame with SalePrice
            top_n: Number of top features
            
        Returns:
            DataFrame ready for visualization
        """
        corr_df = self.calculate_price_correlations(df, top_n=top_n)
        return corr_df

