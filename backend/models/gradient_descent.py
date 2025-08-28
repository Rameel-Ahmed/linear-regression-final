"""
Gradient Descent Optimization Module for Linear Regression.

Provides cost and gradient calculations for the simple linear
model h(x) = theta0 + theta1 * x. The computations assume the
input x_data and y_data have already been prepared (for example,
normalized) and are numeric 1-D arrays.
"""

import numpy as np


class GradientDescent:
    """Compute cost and gradients for y = θ₀ + θ₁·x.

    Parameters
    ----------
    x_data, y_data : np.ndarray
        *Normalized* 1-D arrays.

    Example
    -------
    >>> gd = GradientDescent(x_norm, y_norm)
    >>> theta = np.array([0.0, 0.0])
    >>> cost  = gd.compute_cost(theta)
    >>> grad0, grad1 = gd.compute_gradients(theta)
    """

    def __init__(self, x_data: np.ndarray, y_data: np.ndarray) -> None:
        """Build internal design matrix and store references."""
        self.__x_data: np.ndarray = np.asarray(x_data, dtype=float)
        self.__y_data: np.ndarray = np.asarray(y_data, dtype=float)
        self.__m: int = int(len(self.__x_data))
        # Design matrix with bias term (m x 2)
        self.__X: np.ndarray = np.column_stack([np.ones(self.__m), self.__x_data])

    def compute_cost(self, theta: np.ndarray) -> float:
        """Return the mean squared cost J(θ) = (1/2m) Σ(h - y)^2."""
        try:
            theta_arr: np.ndarray = np.asarray(theta, dtype=float)
            preds: np.ndarray = self.__hypothesis(theta_arr)
            cost: float = (1.0 / (2.0 * self.__m)) * np.sum((preds - self.__y_data) ** 2)
            return float(cost)
        except Exception as exc:
            raise RuntimeError(f"Cost computation failed: {exc}") from exc

    def compute_gradients(self, theta: np.ndarray) -> tuple[float, float]:
        """Return gradients for theta0 and theta1 as floats."""
        try:
            theta_arr: np.ndarray = np.asarray(theta, dtype=float)
            preds: np.ndarray = self.__hypothesis(theta_arr)
            error: np.ndarray = preds - self.__y_data
            grad0: float = (1.0 / self.__m) * np.sum(error)
            grad1: float = (1.0 / self.__m) * np.sum(error * self.__x_data)
            return float(grad0), float(grad1)
        except Exception as exc:
            raise RuntimeError(f"Gradient computation failed: {exc}") from exc

    def __hypothesis(self, theta: np.ndarray) -> np.ndarray:
        """Return vector h = X @ theta."""
        return self.__X @ np.asarray(theta, dtype=float)
