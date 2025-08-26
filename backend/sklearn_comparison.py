"""
Sklearn Comparison Module for Linear Regression Models.
Compares custom implementation with sklearn's linear regression.
"""

import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class SklearnComparison:
    """A class to compare custom linear regression with sklearn implementation."""
    
    def __init__(self):
        """Initialize the sklearn comparison."""
        self._sklearn_model = LinearRegression()
    
    def calculate_sklearn_results(self, x_data: np.ndarray, y_data: np.ndarray) -> Dict[str, Any]:
        """Calculate sklearn linear regression results for comparison."""
        try:
            # Reshape data for sklearn (expects 2D array)
            X = x_data.reshape(-1, 1)
            
            # Fit sklearn model
            self._sklearn_model.fit(X, y_data)
            
            # Make predictions
            y_pred = self._sklearn_model.predict(X)
            
            # Calculate metrics
            metrics = self._calculate_comparison_metrics(y_data, y_pred)
            print(metrics)
            
            return {
                'sklearn_coefficients': {
                    'intercept': float(self._sklearn_model.intercept_),
                    'slope': float(self._sklearn_model.coef_[0])
                },
                'predictions': y_pred.tolist(),
                'metrics': metrics,
                'equation': f"y = {self._sklearn_model.intercept_:.4f} + {self._sklearn_model.coef_[0]:.4f} * x"
            }
            
        except Exception as e:
            return {
                'error': True,
                'message': f"Sklearn comparison failed: {str(e)}"
            }
    
    # Private helper methods
    def _calculate_comparison_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate metrics for sklearn predictions."""
        return {
            'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'mae': float(mean_absolute_error(y_true, y_pred)),
            'r2': float(r2_score(y_true, y_pred))
        }
