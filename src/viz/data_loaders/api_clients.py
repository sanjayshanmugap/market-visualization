"""
Generic API Client Utilities

Provides reusable utilities for fetching data from various APIs.
"""

import requests
import time
from typing import Dict, Any, Optional
from pathlib import Path
import json
import pandas as pd


class APIClient:
    """Base class for API clients with rate limiting and caching."""
    
    def __init__(
        self,
        base_url: str,
        rate_limit: float = 1.0,  # seconds between requests
        cache_dir: Optional[Path] = None,
    ):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.cache_dir = cache_dir or Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _rate_limit(self):
        """Enforce rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()
    
    def _get_cache_path(self, endpoint: str, params: Dict[str, Any]) -> Path:
        """Generate cache file path from endpoint and params."""
        cache_key = f"{endpoint}_{hash(str(sorted(params.items())))}"
        return self.cache_dir / f"{cache_key}.json"
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        Make a GET request with rate limiting and optional caching.
        
        Args:
            endpoint: API endpoint (relative to base_url)
            params: Query parameters
            use_cache: Whether to use cached data if available
            timeout: Request timeout in seconds
            
        Returns:
            JSON response as dictionary
        """
        params = params or {}
        cache_path = self._get_cache_path(endpoint, params)
        
        # Check cache
        if use_cache and cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        # Make request
        self._rate_limit()
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            # Cache response
            if use_cache:
                with open(cache_path, 'w') as f:
                    json.dump(data, f, indent=2)
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def get_dataframe(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """
        Make a GET request and return as pandas DataFrame.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            use_cache: Whether to use cached data
            
        Returns:
            DataFrame
        """
        data = self.get(endpoint, params, use_cache)
        
        # Try to convert to DataFrame
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            # Try common keys
            for key in ['data', 'results', 'items', 'records']:
                if key in data:
                    return pd.DataFrame(data[key])
            # If dict has list values, try to convert
            return pd.DataFrame([data])
        else:
            raise ValueError(f"Cannot convert {type(data)} to DataFrame")

