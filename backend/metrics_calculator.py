"""
Metrics Calculator for Linear Regression Models.
Calculates and tracks performance metrics during training.
"""

import numpy as np
from typing import Dict, List


class MetricsCalculator:
    """A class to calculate various performance metrics for linear regression models."""
    
    def __init__(self):
        """Initialize the metrics calculator."""
        self._metrics_history = {
            'rmse': [],
            'mae': [],
            'r2': [],
            'epochs': []
        }
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, epoch: int) -> Dict[str, float]:
        """Calculate all performance metrics for given predictions."""
        metrics = {
            'rmse': self._calculate_rmse(y_true, y_pred),
            'mae': self._calculate_mae(y_true, y_pred),
            'r2': self._calculate_r2(y_true, y_pred)
        }
        
        # Store metrics in history
        self._store_metrics(metrics, epoch)
        
        return metrics
    
    def get_latest_metrics(self) -> Dict[str, float]:
        """Get the most recent metrics."""
        if not self._metrics_history['epochs']:
            return {}
        
        return {
            'rmse': self._metrics_history['rmse'][-1],
            'mae': self._metrics_history['mae'][-1],
            'r2': self._metrics_history['r2'][-1],
            'epoch': self._metrics_history['epochs'][-1]
        }
    
    def get_metrics_summary(self) -> Dict[str, Dict[str, float]]:
        """Get a summary of metrics including min, max, and trends."""
        if not self._metrics_history['epochs']:
            return {}
        
        summary = {}
        
        for metric_name in ['rmse', 'mae', 'r2']:
            values = self._metrics_history[metric_name]
            summary[metric_name] = {
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'current': float(values[-1]),
                'improvement': float(values[0] - values[-1]) if len(values) > 1 else 0.0
            }
        
        return summary
    
    def get_metrics_history(self) -> Dict[str, List[float]]:
        """Get the complete metrics history."""
        return self._metrics_history.copy()
    
    # Private helper methods
    def _calculate_rmse(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Root Mean Square Error."""
        return np.sqrt(np.mean((y_true - y_pred) ** 2))
    
    def _calculate_mae(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Error."""
        return np.mean(np.abs(y_true - y_pred))
    
    def _calculate_r2(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Coefficient of Determination (R²)."""
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        return 1 - (ss_res / ss_tot)
    
    def _store_metrics(self, metrics: Dict[str, float], epoch: int):
        """Store metrics in history for tracking."""
        self._metrics_history['rmse'].append(metrics['rmse'])
        self._metrics_history['mae'].append(metrics['mae'])
        self._metrics_history['r2'].append(metrics['r2'])
        self._metrics_history['epochs'].append(epoch)
