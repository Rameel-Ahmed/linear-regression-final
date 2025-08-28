"""
API Helper Functions for Linear Regression API Server.

Provides utility methods for:
- Reading and validating uploaded CSVs
- Analyzing data quality
- Storing processed/cleaned data
- Preparing structured API responses
- Orchestrating model training (setup, epoch streaming, lifecycle management)
- Computing final metrics and performing sklearn comparison

This module abstracts away implementation details so the API
layer can stay clean and consistent.
"""

import asyncio
import logging
import io
import json

import numpy as np
import pandas as pd
from fastapi import UploadFile

from backend.utils import CSVLoader
from backend.models import LinearRegressionModel
from backend.utils import SklearnComparison

logger = logging.getLogger(__name__)


class APIHelper:
    """Helper class for FastAPI routes and training orchestration."""

    def __init__(self, session_data: dict[str, object]) -> None:
        """Keep a reference to a session-style dict for state."""
        # session_data is external and intentionally public
        self.session_data: dict[str, object] = session_data

    async def read_csv_file(self, file: UploadFile) -> pd.DataFrame:
        """Read uploaded CSV bytes into a pandas DataFrame."""
        try:
            content = await file.read()
            logger.info("Read CSV upload: %s bytes", len(content))
            return pd.read_csv(io.StringIO(content.decode("utf-8")))
        except Exception as exc:
            logger.exception("Failed to read CSV upload")
            raise RuntimeError(f"Failed to read CSV upload: {exc}") from exc

    def analyze_data_quality(self, df: pd.DataFrame, x_column: str, y_column: str) -> dict[str, object]:
        """Use CSVLoader to analyze data quality and return the result."""
        loader = CSVLoader(x_column, y_column)
        result = loader.analyze_data_quality(df)
        if isinstance(result, dict) and result.get("error"):
            logger.warning("Data quality analysis returned error: %s", result.get("message"))
        else:
            logger.info("Data quality analysis complete for columns x=%s, y=%s", x_column, y_column)
        return result

    def store_processed_data(
        self,
        filename: str,
        df: pd.DataFrame,
        df_clean: pd.DataFrame,
        loader: CSVLoader,
        cleaning_options: dict[str, object]
    ) -> None:
        """Store cleaned data, loader and options into session_data."""
        self.session_data.update({
            "csv_data": df,
            "columns": df.columns.tolist(),
            "filename": filename,
            "cleaned_data": df_clean,
            "csv_loader": loader,
            "cleaning_options": cleaning_options
        })
        logger.info("Stored processed data for filename=%s; cleaned_shape=%s", filename, tuple(df_clean.shape))

    def prepare_process_response(
        self,
        filename: str,
        df: pd.DataFrame,
        df_clean: pd.DataFrame,
        loader: CSVLoader
    ) -> dict[str, object]:
        """Prepare a structured response after processing an uploaded CSV."""
        cleaning_options = self.session_data.get("cleaning_options", {})  # type: ignore
        x_column = cleaning_options.get("x_column")
        y_column = cleaning_options.get("y_column")

        return {
            "message": "Data processed successfully!",
            "file_info": {"filename": filename, "original_shape": df.shape, "cleaned_shape": df_clean.shape},
            "columns": {"x_column": x_column, "y_column": y_column, "all_columns": df.columns.tolist()},
            "cleaning_summary": loader.get_cleaning_summary(),
            "statistics": {
                "x_data": df_clean[x_column].values.tolist() if x_column in df_clean.columns else [],
                "y_data": df_clean[y_column].values.tolist() if y_column in df_clean.columns else [],
                "x_mean": float(df_clean[x_column].mean()) if x_column in df_clean.columns else 0.0,
                "y_mean": float(df_clean[y_column].mean()) if y_column in df_clean.columns else 0.0,
                "x_std": float(df_clean[x_column].std()) if x_column in df_clean.columns else 0.0,
                "y_std": float(df_clean[y_column].std()) if y_column in df_clean.columns else 0.0
            },
            "model_summary": {"data_quality": "clean", "total_features": 2, "data_type": "numerical", "ready_for_training": True},
            "next_step": "ready_for_training"
        }

    def setup_training(self, train_split: float) -> dict[str, object]:
        """Initialize the LinearRegressionModel and store training state."""
        if "cleaned_data" not in self.session_data:
            logger.warning("Attempted to start training without cleaned data")
            raise ValueError("No cleaned data available for training")

        df_clean: pd.DataFrame = self.session_data["cleaned_data"]  # type: ignore
        cleaning_options: dict[str, str] = self.session_data.get("cleaning_options", {})  # type: ignore
        x_column = cleaning_options.get("x_column")
        y_column = cleaning_options.get("y_column")

        x_data = df_clean[x_column].values
        y_data = df_clean[y_column].values

        model = LinearRegressionModel(x_data, y_data)
        split_result = model.train_test_split(train_ratio=train_split)
        model.set_training_data(split_result["x_train"], split_result["y_train"])

        self._initialize_training_state(model)
        logger.info("Training setup complete: train_ratio=%.2f, train_size=%d", train_split, len(split_result["x_train"]))

        return {"model": model, "x_data": x_data, "y_data": y_data, "split_result": split_result}

    async def training_stream(
        self,
        model: LinearRegressionModel,
        x_data: np.ndarray,
        y_data: np.ndarray,
        split_result: dict[str, np.ndarray],
        learning_rate: float,
        epochs: int,
        tolerance: float,
        early_stopping: bool,
        training_speed: float
    ):
        """
        Async generator that yields SSE-style strings for each epoch.

        The generator yields JSON payloads wrapped with the 'data:'
        prefix expected by a simple server-sent-events client.
        """
        try:
            logger.info("Training stream started: epochs=%d, lr=%.6f, early_stopping=%s", epochs, learning_rate, early_stopping)
            x_test = split_result["x_test"]
            y_test = split_result["y_test"]
            x_train_orig = split_result["x_train"]
            y_train_orig = split_result["y_train"]

            epoch_delay = self._get_training_delay(training_speed)

            for epoch_data in model.train_epoch_by_epoch(
                learning_rate=learning_rate,
                max_epochs=epochs,
                tolerance=tolerance,
                early_stopping=early_stopping
            ):
                if not self._should_continue_training():
                    logger.info("Training stream stopped by request")
                    break

                await self._handle_training_pause()

                response_data = self._prepare_epoch_response(epoch_data, model, x_train_orig, y_train_orig)
                yield f"data: {json.dumps(response_data)}\n\n"

                if not epoch_data.get("is_complete", False):
                    await asyncio.sleep(epoch_delay)

            final_data = await self._prepare_final_results(model, x_data, y_data, x_test, y_test)
            logger.info("Training stream completed")
            yield f"data: {json.dumps(final_data)}\n\n"

        except Exception as exc:
            logger.exception("Training stream failed")
            yield f"data: {json.dumps({'error': True, 'message': str(exc)})}\n\n"
        finally:
            self._cleanup_training_state()

    # Internal training lifecycle helpers

    def _initialize_training_state(self, model: LinearRegressionModel) -> None:
        """Mark training active and store model in session."""
        self.session_data.update({"training_active": True, "training_paused": False, "training_model": model})

    @staticmethod
    def _get_training_delay(training_speed: float) -> float:
        """Map user speed to a sensible per-epoch delay (seconds)."""
        speed_delays: dict[float, float] = {1.0: 0.1, 0.8: 0.3, 0.6: 0.6, 0.4: 1.0, 0.2: 1.5}
        closest = min(speed_delays.keys(), key=lambda x: abs(x - training_speed))
        return speed_delays[closest]

    def _should_continue_training(self) -> bool:
        """Return whether training is still active according to session."""
        return bool(self.session_data.get("training_active", False))

    async def _handle_training_pause(self) -> None:
        """Await while the session indicates training should remain paused."""
        while self.session_data.get("training_paused", False) and self.session_data.get("training_active", False):
            logger.info("Training paused; waiting...")
            await asyncio.sleep(0.5)

    def _prepare_epoch_response(
        self,
        epoch_data: dict[str, object],
        model: LinearRegressionModel,
        x_train_orig: np.ndarray,
        y_train_orig: np.ndarray
    ) -> dict[str, object]:
        """Assemble a typed response dict for a training epoch."""
        original_params = model.get_original_scale_parameters()

        if epoch_data["epoch"] % 10 == 0 or epoch_data.get("is_complete", False):  # type: ignore
            try:
                train_predictions = model.predict(x_train_orig)
                original_cost = float(np.mean((train_predictions - y_train_orig) ** 2))
            except Exception:
                original_cost = float(epoch_data.get("cost", 0.0))  # type: ignore
        else:
            original_cost = float(epoch_data.get("cost", 0.0))  # type: ignore

        return {
            "epoch": int(epoch_data["epoch"]),  # type: ignore
            "max_epochs": int(epoch_data["max_epochs"]),  # type: ignore
            "theta0": float(original_params["theta0"]),
            "theta1": float(original_params["theta1"]),
            "cost": float(original_cost),
            "converged": bool(epoch_data.get("converged", False)),
            "is_complete": bool(epoch_data.get("is_complete", False)),
            "rmse": float(epoch_data.get("rmse", 0.0)),
            "mae": float(epoch_data.get("mae", 0.0)),
            "r2": float(epoch_data.get("r2", 0.0))
        }

    async def _prepare_final_results(
        self,
        model: LinearRegressionModel,
        x_data: np.ndarray,
        y_data: np.ndarray,
        x_test: np.ndarray,
        y_test: np.ndarray
    ) -> dict[str, object]:
        """Compute final metrics, run sklearn comparison, and return payload."""
        try:
            test_predictions = model.predict(x_test)
            test_mse = float(np.mean((test_predictions - y_test) ** 2))
            ss_res = float(np.sum((y_test - test_predictions) ** 2))
            ss_tot = float(np.sum((y_test - np.mean(y_test)) ** 2))
            test_r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0.0 else 0.0
        except Exception:
            logger.exception("Final results computation failed; defaulting metrics")
            test_mse = 0.0
            test_r2 = 0.0

        final_params = model.get_original_scale_parameters()
        final_metrics = model.get_latest_metrics()
        metrics_summary = model.get_model_summary()

        sklearn_results = await self._calculate_sklearn_comparison(x_data, y_data)

        # Store trained model reference for later retrieval
        self.session_data["trained_model"] = model

        return {
            "training_complete": True,
            "final_theta0": final_params["theta0"],
            "final_theta1": final_params["theta1"],
            "equation": f"y = {final_params['theta0']:.4f} + {final_params['theta1']:.4f} * x",
            "test_mse": test_mse,
            "test_r2": test_r2,
            "x_range": [float(np.min(x_data)), float(np.max(x_data))],
            "y_range": [float(np.min(y_data)), float(np.max(y_data))],
            "final_rmse": final_metrics.get("rmse", 0.0),
            "final_mae": final_metrics.get("mae", 0.0),
            "final_r2": final_metrics.get("r2", 0.0),
            "metrics_summary": metrics_summary,
            "sklearn_comparison": {"sklearn_results": sklearn_results, "status": "success" if sklearn_results else "failed"}
        }

    async def _calculate_sklearn_comparison(self, x_data: np.ndarray, y_data: np.ndarray) -> dict[str, object] | None:
        """Safely run sklearn comparison and return results or None."""
        try:
            comp = SklearnComparison()
            return comp.calculate_sklearn_results(x_data, y_data)
        except Exception:
            logger.exception("Sklearn comparison failed")
            return None

    def _cleanup_training_state(self) -> None:
        """Clear training-related flags in session_data."""
        self.session_data.update({"training_active": False, "training_paused": False})
        logger.info("Training state cleaned up")
