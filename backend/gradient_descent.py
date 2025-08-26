"""
Gradient Descent Optimization Module for Linear Regression.
Handles gradient descent optimization algorithm.
"""

import numpy as np
from typing import Tuple


class GradientDescent:
    """Handles gradient descent optimization."""
    
    def __init__(self, x_data: np.ndarray, y_data: np.ndarray):
        """Initialize with training data."""
        self._x_data = x_data
        self._y_data = y_data
        self._m = len(x_data)
        self._X = np.column_stack([np.ones(self._m), x_data])
    
    def compute_cost(self, theta: np.ndarray) -> float:
        """Compute cost function: J(θ) = (1/2m) * Σ(h(x) - y)²"""
        predictions = self._hypothesis(theta)
        cost = (1 / (2 * self._m)) * np.sum((predictions - self._y_data) ** 2)
        return float(cost)
    
    def compute_gradients(self, theta: np.ndarray) -> Tuple[float, float]:
        """Compute gradients for θ₀ and θ₁"""
        predictions = self._hypothesis(theta)
        error = predictions - self._y_data
        
        grad_theta0 = (1 / self._m) * np.sum(error)
        grad_theta1 = (1 / self._m) * np.sum(error * self._x_data)
        
        return float(grad_theta0), float(grad_theta1)
    
    def _hypothesis(self, theta: np.ndarray) -> np.ndarray:
        """Compute hypothesis: h(x) = θ₀ + θ₁x"""
        return self._X @ theta
