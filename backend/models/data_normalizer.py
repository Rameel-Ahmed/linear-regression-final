"""
Data Normalization Module for Linear Regression.

Computes normalization statistics (mean, std) for x and y and
provides methods to normalize inputs before training and to
denormalize predictions afterward.

Why normalize then denormalize?
Normalizing (zero mean, unit variance) stabilizes gradient
descent numerics and speeds convergence. After training on
normalized data, denormalizing maps model outputs back to the
original measurement units so results are human-readable.
"""

import numpy as np


class DataNormalizer:
    """Handles normalization and conversion back to original scale.

    Example
    -------
    >>> import numpy as np
    >>> x = np.array([1, 2, 3, 4])
    >>> y = np.array([2, 4, 6, 8])
    >>> norm = DataNormalizer(x, y)
    >>> x_n, y_n = norm.normalize(x, y)
    >>> preds_orig = norm.denormalize_predictions(y_n)
    """

    def __init__(self, x_data: np.ndarray, y_data: np.ndarray) -> None:
        """Compute and stash means and standard deviations."""
        x: np.ndarray = np.asarray(x_data, dtype=float)
        y: np.ndarray = np.asarray(y_data, dtype=float)

        if x.size == 0 or y.size == 0:
            raise ValueError("x_data and y_data must be non-empty")

        self.__x_mean: float = float(np.mean(x))
        self.__x_std: float = float(np.std(x))
        self.__y_mean: float = float(np.mean(y))
        self.__y_std: float = float(np.std(y))

        # Prevent division by zero for zero-va riance arrays
        if self.__x_std == 0.0:
            self.__x_std = 1.0
        if self.__y_std == 0.0:
            self.__y_std = 1.0

    def normalize(self, x_data: np.ndarray, y_data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return (x_norm, y_norm) arrays using stored stats."""
        try:
            x_arr: np.ndarray = np.asarray(x_data, dtype=float)
            y_arr: np.ndarray = np.asarray(y_data, dtype=float)
            x_norm: np.ndarray = (x_arr - self.__x_mean) / self.__x_std
            y_norm: np.ndarray = (y_arr - self.__y_mean) / self.__y_std
            return x_norm, y_norm
        except Exception as exc:
            raise RuntimeError(f"Normalization failed: {exc}") from exc

    def denormalize_predictions(self, predictions_norm: np.ndarray) -> np.ndarray:
        """Map normalized predictions back to the original y scale."""
        try:
            preds: np.ndarray = np.asarray(predictions_norm, dtype=float)
            return preds * self.__y_std + self.__y_mean
        except Exception as exc:
            raise RuntimeError(f"Denormalization failed: {exc}") from exc

    def get_original_scale_parameters(self, theta0_norm: float, theta1_norm: float) -> dict[str, float]:
        """
        Convert normalized linear parameters to original data scale.

        theta1_orig = theta1_norm * (y_std / x_std)
        theta0_orig = theta0_norm * y_std + y_mean - theta1_orig * x_mean
        """
        try:
            theta1_orig: float = float(theta1_norm * (self.__y_std / self.__x_std))
            theta0_orig: float = float(
                theta0_norm * self.__y_std + self.__y_mean - theta1_orig * self.__x_mean
            )
            return {"theta0": theta0_orig, "theta1": theta1_orig}
        except Exception as exc:
            raise RuntimeError(f"Parameter denormalization failed: {exc}") from exc

    def normalize_input(self, x_values: np.ndarray) -> np.ndarray:
        """Normalize new x values for prediction using stored stats."""
        try:
            x_arr: np.ndarray = np.asarray(x_values, dtype=float)
            return (x_arr - self.__x_mean) / self.__x_std
        except Exception as exc:
            raise RuntimeError(f"Input normalization failed: {exc}") from exc
