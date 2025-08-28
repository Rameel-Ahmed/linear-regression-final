"""
Metrics Calculator for Linear Regression Models.

Calculates RMSE, MAE, and R² and stores a per-epoch history
so callers can inspect how metrics evolved during training.
"""

import numpy as np


class MetricsCalculator:
    """Calculate and store regression metrics across epochs."""

    def __init__(self) -> None:
        """Initialize internal history structure."""
        self.__metrics_history: dict[str, list[float] | list[int]] = {
            "rmse": [], "mae": [], "r2": [], "epochs": []
        }

    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, epoch: int) -> dict[str, float]:
        """Compute RMSE, MAE, R² and append values to internal history."""
        try:
            rmse: float = self._calculate_rmse(y_true, y_pred)
            mae: float = self._calculate_mae(y_true, y_pred)
            r2: float = self._calculate_r2(y_true, y_pred)
            metrics: dict[str, float] = {"rmse": rmse, "mae": mae, "r2": r2}
            self.__store_metrics(metrics, epoch)
            return metrics
        except Exception:
            return {"rmse": 0.0, "mae": 0.0, "r2": 0.0}

    def get_latest_metrics(self) -> dict[str, float]:
        """Return the most recent metrics; empty dict if none exist."""
        if not self.__metrics_history["epochs"]:
            return {}
        return {
            "rmse": float(self.__metrics_history["rmse"][-1]),
            "mae": float(self.__metrics_history["mae"][-1]),
            "r2": float(self.__metrics_history["r2"][-1]),
            "epoch": int(self.__metrics_history["epochs"][-1])
        }

    def get_metrics_summary(self) -> dict[str, dict[str, float]]:
        """Provide min, max, current, and improvement from first recorded value."""
        if not self.__metrics_history["epochs"]:
            return {}

        summary: dict[str, dict[str, float]] = {}
        for metric in ("rmse", "mae", "r2"):
            vals: list[float] = list(self.__metrics_history[metric])
            summary[metric] = {
                "min": float(np.min(vals)),
                "max": float(np.max(vals)),
                "current": float(vals[-1]),
                "improvement": float(vals[0] - vals[-1]) if len(vals) > 1 else 0.0
            }
        return summary

    def get_metrics_history(self) -> dict[str, list[float] | list[int]]:
        """Return a shallow copy of the stored metrics history."""
        return dict(self.__metrics_history)


    @staticmethod
    def _calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute root mean squared error (static)."""
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)
        return float(np.sqrt(np.mean((y_t - y_p) ** 2)))

    @staticmethod
    def _calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute mean absolute error (static)."""
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)
        return float(np.mean(np.abs(y_t - y_p)))

    @staticmethod
    def _calculate_r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute coefficient of determination (R²) (static)."""
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)
        ss_res = float(np.sum((y_t - y_p) ** 2))
        ss_tot = float(np.sum((y_t - np.mean(y_t)) ** 2))
        if ss_tot == 0.0:
            return 0.0
        return float(1.0 - (ss_res / ss_tot))

    def __store_metrics(self, metrics: dict[str, float], epoch: int) -> None:
        """Append the computed metrics to internal history lists."""
        self.__metrics_history["rmse"].append(float(metrics["rmse"]))
        self.__metrics_history["mae"].append(float(metrics["mae"]))
        self.__metrics_history["r2"].append(float(metrics["r2"]))
        self.__metrics_history["epochs"].append(int(epoch))
