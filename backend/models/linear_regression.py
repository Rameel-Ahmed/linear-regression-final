"""
Linear Regression Model for Backend Training.

This module wraps gradient descent, normalization, and metric
tracking. Data is normalized before training to improve numeric
stability; after training we convert parameters and predictions
back to original units so callers get interpretable results.
The train_epoch_by_epoch method yields training updates which
can be streamed to a client.
"""

import numpy as np
from typing import Generator, Any, Tuple

from .metrics_calculator import MetricsCalculator
from .data_normalizer import DataNormalizer
from .gradient_descent import GradientDescent


class LinearRegressionModel:
    """Linear regression model with gradient-descent training."""

    def __init__(self, x_data: np.ndarray, y_data: np.ndarray) -> None:
        """Store original arrays and initialize helper instances."""
        self.__x_original: np.ndarray = np.asarray(x_data, dtype=float).flatten()
        self.__y_original: np.ndarray = np.asarray(y_data, dtype=float).flatten()

        # Components are internal -> double-underscore
        self.__normalizer: DataNormalizer = DataNormalizer(
            self.__x_original, self.__y_original
        )
        self.__metrics_calculator: MetricsCalculator = MetricsCalculator()

        # Normalized parameters (theta0, theta1)
        self.__theta0: float = 0.0
        self.__theta1: float = 0.0

        # GradientDescent uses normalized data
        x_norm, y_norm = self.__normalizer.normalize(
            self.__x_original, self.__y_original
        )
        self.__gradient_descent: GradientDescent = GradientDescent(x_norm, y_norm)

    def train_test_split(self, train_ratio: float = 0.8) -> dict[str, np.ndarray]:
        """Split original data into training and testing sets randomly."""
        if not 0.0 < train_ratio < 1.0:
            raise ValueError("train_ratio must be between 0.0 and 1.0")

        n_samples: int = len(self.__x_original)
        n_train: int = int(n_samples * train_ratio)
        indices: np.ndarray = np.random.permutation(n_samples)
        train_idx, test_idx = indices[:n_train], indices[n_train:]

        return {
            "x_train": self.__x_original[train_idx],
            "y_train": self.__y_original[train_idx],
            "x_test": self.__x_original[test_idx],
            "y_test": self.__y_original[test_idx],
        }

    def set_training_data(self, x_train: np.ndarray, y_train: np.ndarray) -> None:
        """Set training data and reinitialize normalizer and optimizer."""
        self.__x_original = np.asarray(x_train, dtype=float).flatten()
        self.__y_original = np.asarray(y_train, dtype=float).flatten()
        self.__normalizer = DataNormalizer(self.__x_original, self.__y_original)
        x_norm, y_norm = self.__normalizer.normalize(
            self.__x_original, self.__y_original
        )
        self.__gradient_descent = GradientDescent(x_norm, y_norm)

    def train_epoch_by_epoch(
        self,
        learning_rate: float,
        max_epochs: int,
        tolerance: float = 1e-6,
        early_stopping: bool = True,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Generator that yields training state after each epoch.

        Yields a dict with epoch, parameters (normalized), cost,
        simple convergence flags, and metrics on the original scale.
        """
        theta: np.ndarray = np.array([self.__theta0, self.__theta1], dtype=float)
        prev_cost: float = float("inf")
        no_improve: int = 0

        for epoch in range(1, max_epochs + 1):
            try:
                current_cost: float = self.__gradient_descent.compute_cost(theta)
                grad0, grad1 = self.__gradient_descent.compute_gradients(theta)
            except Exception:
                # Stop training on internal numerical failure
                break

            theta[0] -= learning_rate * grad0
            theta[1] -= learning_rate * grad1

            if np.isnan(theta).any() or np.isinf(theta).any():
                break

            self.__theta0 = float(theta[0])
            self.__theta1 = float(theta[1])

            cost_change: float = abs(prev_cost - current_cost)
            converged: bool = cost_change < tolerance

            if early_stopping and cost_change < tolerance:
                no_improve += 1
                if no_improve >= 15:
                    break
            else:
                no_improve = 0

            # Compute metrics on original-scale predictions
            try:
                preds: np.ndarray = self.predict_original_scale(self.__x_original)
                metrics: dict[str, float] = self.__metrics_calculator.calculate_metrics(
                    y_true=self.__y_original, y_pred=preds, epoch=epoch
                )
            except Exception:
                metrics = {"rmse": 0.0, "mae": 0.0, "r2": 0.0}

            yield {
                "epoch": epoch,
                "max_epochs": max_epochs,
                "theta0": self.__theta0,
                "theta1": self.__theta1,
                "cost": current_cost,
                "cost_change": cost_change,
                "converged": converged,
                "is_complete": epoch >= max_epochs or converged,
                "rmse": metrics.get("rmse", 0.0),
                "mae": metrics.get("mae", 0.0),
                "r2": metrics.get("r2", 0.0),
            }

            prev_cost = current_cost

    def get_model_summary(self) -> dict[str, Any]:
        """Return summary including denormalized params and metrics."""
        orig_params: dict[str, float] = self.get_original_scale_parameters()
        try:
            metrics_summary: dict[str, float] = (
                self.__metrics_calculator.get_metrics_summary()
            )
        except Exception:
            metrics_summary = {}

        try:
            final_cost: float = self.__gradient_descent.compute_cost(
                np.array([self.__theta0, self.__theta1])
            )
        except Exception:
            final_cost = float("nan")

        return {
            "normalized_theta0": self.__theta0,
            "normalized_theta1": self.__theta1,
            "original_theta0": orig_params["theta0"],
            "original_theta1": orig_params["theta1"],
            "equation_normalized": f"y_norm = {self.__theta0:.4f} + {self.__theta1:.4f}·x_norm",
            "equation_original": f"y = {orig_params['theta0']:.4f} + {orig_params['theta1']:.4f}·x",
            "training_examples": len(self.__x_original),
            "final_cost": final_cost,
            "metrics_summary": metrics_summary,
        }

    def get_latest_metrics(self) -> dict[str, float]:
        """Return the most recent metrics recorded by the calculator."""
        return self.__metrics_calculator.get_latest_metrics()

    def get_original_scale_parameters(self) -> dict[str, float]:
        """Return denormalized (original-scale) theta0 and theta1."""
        return self.__normalizer.get_original_scale_parameters(
            self.__theta0, self.__theta1
        )

    @property
    def theta0(self) -> float:  # noqa: D401 – simple property doc
        """Current θ₀ on the original data scale (read-only)."""
        return self.get_original_scale_parameters()["theta0"]

    @property
    def theta1(self) -> float:
        """Current θ₁ on the original data scale (read-only)."""
        return self.get_original_scale_parameters()["theta1"]

    def predict(self, x_values: np.ndarray) -> np.ndarray:
        """Alias kept for backward compatibility: predicts on original scale."""
        return self.predict_original_scale(x_values)

    def predict_original_scale(self, x_values: np.ndarray) -> np.ndarray:
        """
        Predict y for given x values on the original data scale.

        The method normalizes inputs with the stored normalizer, then
        predicts in normalized space and denormalizes the outputs.
        """
        try:
            x_values = np.asarray(x_values, dtype=float).flatten()
            x_norm: np.ndarray = self.__normalizer.normalize_input(x_values)
            preds_norm: np.ndarray = self.__theta0 + self.__theta1 * x_norm
            return self.__normalizer.denormalize_predictions(preds_norm)
        except Exception as exc:
            raise RuntimeError(f"Prediction failed: {exc}") from exc
