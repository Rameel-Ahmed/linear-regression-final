"""backend.utils.sklearn_comparison
+------------------------------------------------
Run a quick check by fitting scikit-learn’s ``LinearRegression`` to
the same dataset and reporting coefficients + metrics.

Example
-------
>>> from backend.utils.sklearn_comparison import SklearnComparison
>>> x = np.arange(10)
>>> y = 2 * x + 1
>>> comp = SklearnComparison()
>>> comp.calculate_sklearn_results(x, y)["metrics"]["r2"]
1.0
"""

import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class SklearnComparison:
    """Compare custom linear regression with sklearn's LinearRegression."""

    def __init__(self) -> None:
        """Create a fresh sklearn LinearRegression instance."""
        self.__sklearn_model: LinearRegression = LinearRegression()

    def calculate_sklearn_results(self, x_data: np.ndarray, y_data: np.ndarray) -> dict[str, object]:
        """Fit sklearn model and compute predictions and metrics."""
        try:
            X: np.ndarray = np.asarray(x_data, dtype=float).reshape(-1, 1)
            y: np.ndarray = np.asarray(y_data, dtype=float)
            self.__sklearn_model.fit(X, y)
            y_pred: np.ndarray = self.__sklearn_model.predict(X)
            metrics: dict[str, float] = self._calculate_comparison_metrics(y, y_pred)
            return {
                "sklearn_coefficients": {
                    "intercept": float(self.__sklearn_model.intercept_),
                    "slope": float(self.__sklearn_model.coef_[0])
                },
                "predictions": y_pred.tolist(),
                "metrics": metrics,
                "equation": f"y = {self.__sklearn_model.intercept_:.4f} + "
                            f"{self.__sklearn_model.coef_[0]:.4f} * x"
            }
        except Exception as exc:
            return {"error": True, "message": f"Sklearn comparison failed: {exc}"}

    @staticmethod
    def _calculate_comparison_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
        """Return RMSE, MAE, and R² for sklearn predictions (static)."""
        try:
            return {
                "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
                "mae": float(mean_absolute_error(y_true, y_pred)),
                "r2": float(r2_score(y_true, y_pred)),
            }
        except Exception:
            return {"rmse": 0.0, "mae": 0.0, "r2": 0.0}
