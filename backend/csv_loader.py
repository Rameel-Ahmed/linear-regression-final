"""
CSV Loader and Data Cleaning Module.
Handles CSV file loading, cleaning, and preprocessing.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class CSVLoader:
    """A class to load and clean CSV data for linear regression."""
    
    def __init__(self, x_column: str, y_column: str):
        """Initialize the CSV loader with column specifications."""
        self._x_column = x_column
        self._y_column = y_column
        self._cleaning_summary = {}

    def analyze_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data quality without cleaning, return simple summary."""
        analysis = {
            'total_rows': len(df),
            'x_column': self._x_column,
            'y_column': self._y_column,
            'summary': []
        }
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            analysis['summary'].append(f'{duplicates} rows have duplicates')
        
        # Check for missing values
        x_missing = df[self._x_column].isna().sum()
        y_missing = df[self._y_column].isna().sum()
        
        if x_missing > 0:
            analysis['summary'].append(f'{x_missing} rows have NaN in X column')
        if y_missing > 0:
            analysis['summary'].append(f'{y_missing} rows have NaN in Y column')
        
        # Check for string values (smart check that handles object dtype properly)
        x_col = df[self._x_column]
        y_col = df[self._y_column]
        
        # Count truly non-numeric strings (skip numeric strings like "20")
        x_strings = sum(1 for val in x_col if isinstance(val, str) and not str(val).replace('.', '').replace('-', '').isdigit())
        y_strings = sum(1 for val in y_col if isinstance(val, str) and not str(val).replace('.', '').replace('-', '').isdigit())
        
        if x_strings > 0:
            if x_strings == len(df):
                analysis['summary'].append('X column is all string')
            else:
                analysis['summary'].append(f'{x_strings} rows have string in X column')
        
        if y_strings > 0:
            if y_strings == len(df):
                analysis['summary'].append('Y column is all string')
            else:
                analysis['summary'].append(f'{y_strings} rows have string in Y column')
        
        # If no issues found
        if not analysis['summary']:
            analysis['summary'].append('Data looks clean!')
        
        return analysis
    
    def clean_data(self, df: pd.DataFrame, remove_duplicates: bool = True, 
                   remove_outliers: bool = False, handle_missing: str = "remove",
                   remove_strings: bool = True) -> pd.DataFrame:
        """Clean the data based on specified options."""
        df_clean = df.copy()
        
        # Apply cleaning operations
        if remove_duplicates:
            df_clean = self._remove_duplicates(df_clean)
        
        if remove_outliers:
            df_clean = self._remove_outliers(df_clean)
        
        if handle_missing == "remove":
            df_clean = self._handle_missing_values(df_clean)
        
        if remove_strings:
            df_clean = self._remove_string_columns(df_clean)
        
        # Validate final data
        self._validate_cleaned_data(df_clean)
        
        # Update cleaning summary
        self._update_cleaning_summary(df, df_clean, {
            'remove_duplicates': remove_duplicates,
            'remove_outliers': remove_outliers,
            'handle_missing': handle_missing,
            'remove_strings': remove_strings
        })
        
        return df_clean
    
    def get_cleaning_summary(self, df: pd.DataFrame, df_clean: pd.DataFrame) -> Dict[str, Any]:
        """Get a summary of the cleaning operations performed."""
        return self._cleaning_summary
    
    # Private helper methods
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows from the dataframe."""
        initial_count = len(df)
        df_clean = df.drop_duplicates()
        removed_count = initial_count - len(df_clean)
        
        if removed_count > 0:
            self._cleaning_summary['duplicates_removed'] = removed_count
        
        return df_clean
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove outliers using IQR method."""
        df_clean = df.copy()
        initial_count = len(df_clean)
        
        for col in [self._x_column, self._y_column]:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df_clean = df_clean[
                (df_clean[col] >= lower_bound) & 
                (df_clean[col] <= upper_bound)
            ]
        
        removed_count = initial_count - len(df_clean)
        if removed_count > 0:
            self._cleaning_summary['outliers_removed'] = removed_count
        
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values by dropping rows with any missing data."""
        initial_count = len(df)
        df_clean = df.dropna(subset=[self._x_column, self._y_column])
        removed_count = initial_count - len(df_clean)
        
        if removed_count > 0:
            self._cleaning_summary['missing_values_removed'] = removed_count
        
        return df_clean
    
    def _remove_string_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove non-numeric columns but ensure x/y are numeric (coerce if needed)."""
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Always try to convert x and y to numeric
        for col in [self._x_column, self._y_column]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if col not in numeric_columns:
                    numeric_columns.append(col)

        df_clean = df[numeric_columns].dropna(subset=[self._x_column, self._y_column])

        removed_count = len(df.columns) - len(df_clean.columns)
        if removed_count > 0:
            self._cleaning_summary['string_columns_removed'] = removed_count
        
        return df_clean
    
    def _validate_cleaned_data(self, df: pd.DataFrame):
        """Validate that cleaned data meets requirements."""
        if df.empty:
            raise ValueError("Cleaning resulted in empty dataset")
        
        if len(df) < 10:
            raise ValueError("Cleaned dataset too small (minimum 10 samples required)")
        
        # Check for infinite values
        if np.isinf(df[self._x_column]).any() or np.isinf(df[self._y_column]).any():
            raise ValueError("Data contains infinite values")
        
        # Check for NaN values
        if df[self._x_column].isna().any() or df[self._y_column].isna().any():
            raise ValueError("Data contains NaN values after cleaning")
    
    def _update_cleaning_summary(self, df_original: pd.DataFrame, df_clean: pd.DataFrame, 
                                cleaning_options: Dict[str, Any]):
        """Update the cleaning summary with operation results."""
        self._cleaning_summary.update({
            'original_shape': df_original.shape,
            'cleaned_shape': df_clean.shape,
            'samples_removed': len(df_original) - len(df_clean),
            'cleaning_options_applied': cleaning_options,
            'final_columns': df_clean.columns.tolist()
        })
