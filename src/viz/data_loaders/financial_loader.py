"""
Financial Data Loader

Loads financial and market data from various sources:
- yfinance for stock data
- Existing market data files
- Financial APIs
"""

import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json


class FinancialDataLoader:
    """Loader for financial and market data."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
    
    def load_stock_data(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y",
    ) -> Dict[str, pd.DataFrame]:
        """
        Load stock data from yfinance.
        
        Args:
            symbols: List of stock symbols (e.g., ['AAPL', 'GOOGL'])
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            period: Period if dates not specified (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            Dictionary mapping symbol to DataFrame with OHLCV data
        """
        data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                
                if start_date and end_date:
                    df = ticker.history(start=start_date, end=end_date)
                else:
                    df = ticker.history(period=period)
                
                if not df.empty:
                    data[symbol] = df.reset_index()
            except Exception as e:
                print(f"Error loading data for {symbol}: {e}")
        
        return data
    
    def load_existing_market_data(self, symbol: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Load existing market data from parquet files.
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            Dictionary mapping symbol to DataFrame
        """
        data = {}
        synthetic_dir = self.data_dir / "synthetic"
        
        if not synthetic_dir.exists():
            return data
        
        # Look for price_data_*.parquet files
        pattern = f"price_data_{symbol}.parquet" if symbol else "price_data_*.parquet"
        
        for file_path in synthetic_dir.glob(pattern):
            try:
                symbol_name = file_path.stem.replace("price_data_", "")
                df = pd.read_parquet(file_path)
                data[symbol_name] = df
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        return data
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get stock information and metadata.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock info
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
        except Exception as e:
            print(f"Error getting info for {symbol}: {e}")
            return {}
    
    def calculate_returns(self, df: pd.DataFrame, price_col: str = "Close") -> pd.DataFrame:
        """
        Calculate returns and volatility metrics.
        
        Args:
            df: DataFrame with price data
            price_col: Column name for price
            
        Returns:
            DataFrame with additional return columns
        """
        import numpy as np
        df = df.copy()
        df['Returns'] = df[price_col].pct_change()
        df['Log_Returns'] = np.log(df[price_col]).diff()
        df['Volatility'] = df['Returns'].rolling(window=20).std() * (252 ** 0.5)  # Annualized
        return df
    
    def calculate_correlation_matrix(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate correlation matrix for multiple stocks.
        
        Args:
            data: Dictionary of symbol -> DataFrame
            
        Returns:
            Correlation matrix DataFrame
        """
        # Align all dataframes by date
        closes = {}
        for symbol, df in data.items():
            if 'Date' in df.columns:
                df = df.set_index('Date')
            elif 'Datetime' in df.columns:
                df = df.set_index('Datetime')
            
            if 'Close' in df.columns:
                closes[symbol] = df['Close']
        
        if not closes:
            return pd.DataFrame()
        
        # Combine and calculate correlation
        combined = pd.DataFrame(closes)
        return combined.corr()

