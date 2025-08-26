"""
Linear Regression Model for Backend Training.
Handles gradient descent with real-time updates.
"""

import numpy as np
from typing import Dict, Any, Generator
from .metrics_calculator import MetricsCalculator
from .data_normalizer import DataNormalizer
from .gradient_descent import GradientDescent


class LinearRegressionModel:
    """Linear Regression model with gradient descent training."""
    
    def __init__(self, x_data: np.ndarray, y_data: np.ndarray):
        """Initialize the linear regression model."""
        self._x_original = x_data.flatten()
        self._y_original = y_data.flatten()
        
        # Initialize components
        self._normalizer = DataNormalizer(self._x_original, self._y_original)
        self._metrics_calculator = MetricsCalculator()
        
        # Initialize parameters
        self._theta0 = 0.0
        self._theta1 = 0.0
        
        # Initialize gradient descent with normalized data
        x_norm, y_norm = self._normalizer.normalize(self._x_original, self._y_original)
        self._gradient_descent = GradientDescent(x_norm, y_norm)
    
    def train_test_split(self, train_ratio: float = 0.8) -> Dict[str, np.ndarray]:
        """Split data into training and testing sets."""
        if not 0.0 < train_ratio < 1.0:
            raise ValueError("train_ratio must be between 0.0 and 1.0")
        
        n_samples = len(self._x_original)
        n_train = int(n_samples * train_ratio)
        
        # Create random permutation of indices
        indices = np.random.permutation(n_samples)
        train_indices = indices[:n_train]
        test_indices = indices[n_train:]
        
        return {
            'x_train': self._x_original[train_indices],
            'y_train': self._y_original[train_indices],
            'x_test': self._x_original[test_indices],
            'y_test': self._y_original[test_indices]
        }
    
    def set_training_data(self, x_train: np.ndarray, y_train: np.ndarray):
        """Set specific training data and update components."""
        self._x_original = x_train.flatten()
        self._y_original = y_train.flatten()
        
        # Update normalizer and gradient descent
        self._normalizer = DataNormalizer(self._x_original, self._y_original)
        x_norm, y_norm = self._normalizer.normalize(self._x_original, self._y_original)
        self._gradient_descent = GradientDescent(x_norm, y_norm)
    
    def train_epoch_by_epoch(
        self, 
        learning_rate: float, 
        max_epochs: int, 
        tolerance: float = 1e-6,
        early_stopping: bool = True
    ) -> Generator[Dict[str, Any], None, None]:
        """Train the model epoch by epoch with real-time updates."""
        theta = np.array([self._theta0, self._theta1])
        prev_cost = float('inf')
        no_improvement_count = 0
        
        for epoch in range(1, max_epochs + 1):
            # Compute current cost and gradients
            current_cost = self._gradient_descent.compute_cost(theta)
            grad_theta0, grad_theta1 = self._gradient_descent.compute_gradients(theta)
            
            # Update parameters
            theta[0] -= learning_rate * grad_theta0
            theta[1] -= learning_rate * grad_theta1
            
            # Check for numerical explosion
            if np.isnan(theta).any() or np.isinf(theta).any():
                break
            
            # Update instance variables
            self._theta0 = theta[0]
            self._theta1 = theta[1]
            
            # Check for convergence
            cost_change = abs(prev_cost - current_cost)
            converged = cost_change < tolerance
            
            # Early stopping logic
            if early_stopping and cost_change < tolerance:
                no_improvement_count += 1
                if no_improvement_count >= 15:
                    break
            else:
                no_improvement_count = 0
            
            # Calculate performance metrics
            predictions = self.predict_original_scale(self._x_original)
            metrics = self._metrics_calculator.calculate_metrics(
                y_true=self._y_original,
                y_pred=predictions,
                epoch=epoch
            )
            
            # Yield current state with metrics
            yield {
                "epoch": epoch,
                "max_epochs": max_epochs,
                "theta0": self._theta0,
                "theta1": self._theta1,
                "cost": current_cost,
                "cost_change": cost_change,
                "converged": converged,
                "is_complete": epoch >= max_epochs or converged,
                "rmse": metrics['rmse'],
                "mae": metrics['mae'],
                "r2": metrics['r2']
            }
            
            prev_cost = current_cost
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get summary of the trained model."""
        orig_params = self.get_original_scale_parameters()
        
        try:
            metrics_summary = self._metrics_calculator.get_metrics_summary()
        except Exception:
            metrics_summary = {}
        
        return {
            "normalized_theta0": self._theta0,
            "normalized_theta1": self._theta1,
            "original_theta0": orig_params['theta0'],
            "original_theta1": orig_params['theta1'],
            "equation_normalized": f"y_norm = {self._theta0:.4f} + {self._theta1:.4f}·x_norm",
            "equation_original": f"y = {orig_params['theta0']:.4f} + {orig_params['theta1']:.4f}·x",
            "training_examples": len(self._x_original),
            "final_cost": self._gradient_descent.compute_cost(np.array([self._theta0, self._theta1])),
            "metrics_summary": metrics_summary
        }
    
    def get_latest_metrics(self) -> Dict[str, float]:
        """Get the most recent metrics from training."""
        return self._metrics_calculator.get_latest_metrics()

    def get_original_scale_parameters(self) -> Dict[str, float]:
        """Get the parameters in the original data scale."""
        return self._normalizer.get_original_scale_parameters(self._theta0, self._theta1)

    def predict(self, x_values: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model on original scale data."""
        return self.predict_original_scale(x_values)
    
    def predict_original_scale(self, x_values: np.ndarray) -> np.ndarray:
        """Make predictions on original scale data."""
        x_values = np.asarray(x_values).flatten()
        
        # Normalize input data
        x_norm = self._normalizer.normalize_input(x_values)
        
        # Make prediction on normalized data
        predictions_norm = self._theta0 + self._theta1 * x_norm
        
        # Denormalize predictions back to original scale
        return self._normalizer.denormalize_predictions(predictions_norm)