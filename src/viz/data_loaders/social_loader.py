"""
Social/Economic Data Loader

Loads social and economic data from public sources:
- World Bank API
- UN Data
- Census data
- Economic indicators
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
from .api_clients import APIClient


class SocialDataLoader:
    """Loader for social and economic data."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data")
        # World Bank API
        self.worldbank_client = APIClient(
            base_url="https://api.worldbank.org/v2",
            rate_limit=1.0,
        )
    
    def load_economic_inequality_data(self, country: str = "USA") -> pd.DataFrame:
        """
        Load economic inequality data (Gini coefficient, income distribution).
        
        Args:
            country: Country code (e.g., 'USA', 'CHN')
            
        Returns:
            DataFrame with inequality metrics
        """
        # Sample data structure - in production would fetch from World Bank API
        # World Bank API endpoint: /v2/country/{country}/indicator/SI.POV.GINI
        
        years = list(range(2000, 2023))
        import numpy as np
        np.random.seed(42)
        
        # Sample Gini coefficients (0-100 scale)
        gini_values = np.random.uniform(35, 45, len(years)) + np.linspace(0, 2, len(years))
        
        df = pd.DataFrame({
            'Year': years,
            'Country': country,
            'Gini_Coefficient': gini_values,
            'Income_Share_Top_10': 100 - gini_values * 0.8,  # Rough estimate
            'Income_Share_Bottom_10': gini_values * 0.3,  # Rough estimate
        })
        
        return df
    
    def load_population_data(self, countries: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load population data for countries.
        
        Args:
            countries: List of country codes (default: major countries)
            
        Returns:
            DataFrame with population data
        """
        if countries is None:
            countries = ['USA', 'CHN', 'IND', 'JPN', 'DEU', 'GBR', 'FRA', 'BRA']
        
        # Sample population data structure
        years = list(range(2000, 2023))
        
        # Sample population data (in millions)
        population_data = {
            'USA': [282, 285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330, 333, 336, 339, 342, 345, 348],
            'CHN': [1267, 1276, 1285, 1294, 1303, 1312, 1321, 1330, 1339, 1348, 1357, 1366, 1375, 1384, 1393, 1402, 1411, 1420, 1429, 1438, 1447, 1456, 1465],
            'IND': [1053, 1071, 1089, 1107, 1125, 1143, 1161, 1179, 1197, 1215, 1233, 1251, 1269, 1287, 1305, 1323, 1341, 1359, 1377, 1395, 1413, 1431, 1449],
        }
        
        data = []
        for country in countries:
            if country in population_data:
                pops = population_data[country]
            else:
                # Generate sample data
                import numpy as np
                np.random.seed(hash(country) % 1000)
                base_pop = np.random.uniform(50, 500)
                pops = [base_pop * (1.01 ** (y - 2000)) for y in years]
            
            for year, pop in zip(years, pops):
                data.append({
                    'Year': year,
                    'Country': country,
                    'Population_Millions': pop,
                })
        
        return pd.DataFrame(data)
    
    def load_migration_data(self) -> pd.DataFrame:
        """
        Load migration flow data.
        
        Returns:
            DataFrame with migration data
        """
        # Sample migration data
        migration_flows = [
            {
                'Year': 2020,
                'Origin': 'Mexico',
                'Destination': 'USA',
                'Migrants': 1200000,
                'Origin_Lat': 23.6345,
                'Origin_Lon': -102.5528,
                'Dest_Lat': 39.8283,
                'Dest_Lon': -98.5795,
            },
            {
                'Year': 2020,
                'Origin': 'Syria',
                'Destination': 'Germany',
                'Migrants': 800000,
                'Origin_Lat': 34.8021,
                'Origin_Lon': 38.9968,
                'Dest_Lat': 51.1657,
                'Dest_Lon': 10.4515,
            },
            # Add more migration flows
        ]
        
        return pd.DataFrame(migration_flows)
    
    def get_economic_indicators(self, country: str = "USA") -> Dict[str, Any]:
        """
        Get economic indicators for a country.
        
        Args:
            country: Country code
            
        Returns:
            Dictionary with economic indicators
        """
        # Sample indicators - in production would fetch from World Bank/IMF APIs
        return {
            'GDP_Growth': 2.5,
            'Unemployment_Rate': 3.7,
            'Inflation_Rate': 3.2,
            'Gini_Coefficient': 41.5,
        }

