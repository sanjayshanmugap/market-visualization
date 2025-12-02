"""
Data Exporter

Exports processed data as JSON/CSV for frontend consumption.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Optional, Union, Dict, Any, List


class DataExporter:
    """Exports data in various formats for frontend use."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("data/viz/data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_dataframe_json(
        self,
        df: pd.DataFrame,
        filename: str,
        orient: str = "records",
        date_format: str = "iso",
    ) -> Path:
        """
        Export DataFrame as JSON.
        
        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            orient: JSON orientation (records, index, values, table)
            date_format: Date format (iso, epoch)
            
        Returns:
            Path to saved JSON file
        """
        output_path = self.output_dir / f"{filename}.json"
        
        json_str = df.to_json(orient=orient, date_format=date_format)
        
        with open(output_path, 'w') as f:
            f.write(json_str)
        
        return output_path
    
    def export_dataframe_csv(
        self,
        df: pd.DataFrame,
        filename: str,
        index: bool = False,
    ) -> Path:
        """
        Export DataFrame as CSV.
        
        Args:
            df: DataFrame to export
            filename: Output filename (without extension)
            index: Whether to include index
            
        Returns:
            Path to saved CSV file
        """
        output_path = self.output_dir / f"{filename}.csv"
        
        df.to_csv(output_path, index=index)
        
        return output_path
    
    def export_dict_json(
        self,
        data: Dict[str, Any],
        filename: str,
    ) -> Path:
        """
        Export dictionary as JSON.
        
        Args:
            data: Dictionary to export
            filename: Output filename (without extension)
            
        Returns:
            Path to saved JSON file
        """
        output_path = self.output_dir / f"{filename}.json"
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return output_path
    
    def export_list_json(
        self,
        data: List[Any],
        filename: str,
    ) -> Path:
        """
        Export list as JSON.
        
        Args:
            data: List to export
            filename: Output filename (without extension)
            
        Returns:
            Path to saved JSON file
        """
        output_path = self.output_dir / f"{filename}.json"
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return output_path

