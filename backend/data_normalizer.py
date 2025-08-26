"""
Data Normalization Module for Linear Regression.
Handles data normalization and denormalization.
"""

import numpy as np
from typing import Dict, Tuple


class DataNormalizer:
    """Handles data normalization and denormalization."""
    
    def __init__(self, x_data: np.ndarray, y_data: np.ndarray):
        """Initialize with data for normalization."""
        self._x_mean = np.mean(x_data)
        self._x_std = np.std(x_data)
        self._y_mean = np.mean(y_data)
        self._y_std = np.std(y_data)
        
        # Handle zero variance
        if self._x_std == 0:
            self._x_std = 1.0
        if self._y_std == 0:
            self._y_std = 1.0
    
    def normalize(self, x_data: np.ndarray, y_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Normalize data for training."""
        x_norm = (x_data - self._x_mean) / self._x_std
        y_norm = (y_data - self._y_mean) / self._y_std
        return x_norm, y_norm
    
    def denormalize_predictions(self, predictions_norm: np.ndarray) -> np.ndarray:
        """Convert normalized predictions back to original scale."""
        return predictions_norm * self._y_std + self._y_mean
    
    def get_original_scale_parameters(self, theta0_norm: float, theta1_norm: float) -> Dict[str, float]:
        """Convert normalized parameters to original scale."""
        theta1_orig = theta1_norm * (self._y_std / self._x_std)
        theta0_orig = theta0_norm * self._y_std + self._y_mean - theta1_orig * self._x_mean
        
        return {'theta0': theta0_orig, 'theta1': theta1_orig}
    
    def normalize_input(self, x_values: np.ndarray) -> np.ndarray:
        """Normalize input data for prediction."""
        return (x_values - self._x_mean) / self._x_std
