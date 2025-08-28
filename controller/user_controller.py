# controllers/user_controller.py

from typing import Any
import logging
import numpy as np
from fastapi import UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from backend.api_helpers import APIHelper
from backend.utils import CSVLoader


class UserController:
    """Handle user-facing API endpoints.

    The controller keeps short-lived *session_data* (a simple `dict`) that
    stores state for a single client session – uploaded data, training
    flags, and trained model reference.  All heavy lifting is delegated to
    :class:`backend.api_helpers.APIHelper` to preserve thin route logic.

    Example
    -------
    >>> from controller.user_controller import UserController
    >>> ctrl = UserController()
    >>> # In an async FastAPI route: await ctrl.pause_training()
    """

    def __init__(self) -> None:
        """Create an empty *session_data* dict and helper facade."""
        self.session_data: dict[str, Any] = {}
        self.api_helpers = APIHelper(self.session_data)
        self._logger = logging.getLogger(__name__)

    async def serve_homepage(self) -> HTMLResponse:
        """Return the front-end landing page.

        Returns
        -------
        HTMLResponse
            The contents of *static/index.html*.
        """
        try:
            self._logger.info("Serving index.html via controller")
            with open("static/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Main page not found")

    async def analyze_data_quality(
        self,
        file: UploadFile,
        x_column: str = Form(...),
        y_column: str = Form(...),
    ) -> dict[str, Any]:
        """Return a quick data-quality report.

        Parameters
        ----------
        file : UploadFile
            CSV file uploaded by the client.
        x_column, y_column : str
            Names of the independent / dependent variables.

        Returns
        -------
        dict
            A summary constructed by :meth:`backend.api_helpers.APIHelper.analyze_data_quality`.
        """
        try:
            self._logger.info(
                "Analyze data quality requested: x=%s, y=%s", x_column, y_column
            )
            df = await self.api_helpers.read_csv_file(file)
            return self.api_helpers.analyze_data_quality(df, x_column, y_column)
        except Exception as e:
            self._logger.exception("Analysis failed")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    # --- Data Processing -----------------------------------------------------

    async def process_data(
        self,
        file: UploadFile,
        x_column: str = Form(...),
        y_column: str = Form(...),
        remove_duplicates: bool = Form(True),
        remove_outliers: bool = Form(False),
        handle_missing: str = Form("remove"),
        remove_strings: bool = Form(True),
    ) -> dict[str, Any]:
        """Clean the uploaded CSV and return a structured response.

        The heavy lifting is performed by :class:`backend.utils.csv_loader.CSVLoader`.
        The cleaned DataFrame is stored in *session_data* for later training.
        """
        try:
            self._logger.info("Process data requested: x=%s, y=%s", x_column, y_column)
            df = await self.api_helpers.read_csv_file(file)
            loader = CSVLoader(x_column, y_column)
            df_clean = loader.clean_data(
                df, remove_duplicates, remove_outliers, handle_missing, remove_strings
            )

            self.api_helpers.store_processed_data(
                file.filename,
                df,
                df_clean,
                loader,
                {
                    "x_column": x_column,
                    "y_column": y_column,
                    "remove_duplicates": remove_duplicates,
                    "remove_outliers": remove_outliers,
                    "handle_missing": handle_missing,
                    "remove_strings": remove_strings,
                },
            )

            return self.api_helpers.prepare_process_response(
                file.filename, df, df_clean, loader
            )

        except Exception as e:
            self._logger.exception("Processing failed")
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    # --- Training lifecycle --------------------------------------------------

    async def start_training(
        self,
        learning_rate: float = Form(...),
        epochs: int = Form(...),
        tolerance: float = Form(...),
        early_stopping: bool = Form(True),
        train_split: float = Form(0.8),
        training_speed: float = Form(1.0),
    ) -> StreamingResponse:
        """Kick off model training and stream epoch updates.

        Returns
        -------
        StreamingResponse
            Server-sent events stream (``text/plain``) suitable for EventSource.
        """
        try:
            self._logger.info(
                "Start training requested: lr=%s, epochs=%s, tol=%s, early_stopping=%s, split=%.2f, speed=%s",
                learning_rate,
                epochs,
                tolerance,
                early_stopping,
                train_split,
                training_speed,
            )
            training_setup = self.api_helpers.setup_training(train_split)
            return StreamingResponse(
                self.api_helpers.training_stream(
                    training_setup["model"],
                    training_setup["x_data"],
                    training_setup["y_data"],
                    training_setup["split_result"],
                    learning_rate,
                    epochs,
                    tolerance,
                    early_stopping,
                    training_speed,
                ),
                media_type="text/plain",
            )
        except Exception as e:
            self._logger.exception("Training failed to start")
            raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

    async def pause_training(self) -> dict[str, str]:
        """Pause a running training stream (idempotent)."""
        try:
            if self.session_data.get(
                "training_active", False
            ) and not self.session_data.get("training_paused", False):
                self.session_data["training_paused"] = True
                self._logger.info("Training paused")
                return {"message": "Training paused"}
            elif self.session_data.get("training_paused", False):
                return {"message": "Training already paused"}
            else:
                return {"message": "No active training to pause"}
        except Exception as e:
            self._logger.exception("Failed to pause training")
            raise HTTPException(
                status_code=500, detail=f"Failed to pause training: {str(e)}"
            )

    async def resume_training(self) -> dict[str, str]:
        """Resume a previously paused training session."""
        try:
            if self.session_data.get(
                "training_active", False
            ) and self.session_data.get("training_paused", False):
                self.session_data["training_paused"] = False
                self._logger.info("Training resumed")
                return {"message": "Training resumed"}
            elif not self.session_data.get("training_paused", False):
                return {"message": "Training not paused"}
            else:
                return {"message": "No active training to resume"}
        except Exception as e:
            self._logger.exception("Failed to resume training")
            raise HTTPException(
                status_code=500, detail=f"Failed to resume training: {str(e)}"
            )

    async def stop_training(self) -> dict[str, str]:
        """Request graceful shutdown of an active training session."""
        try:
            if self.session_data.get("training_active", False):
                self.session_data["training_active"] = False
                self.session_data["training_paused"] = False
                self._logger.info("Training stop requested")
                return {"message": "Training stop requested"}
            else:
                return {"message": "No active training to stop"}
        except Exception as e:
            self._logger.exception("Failed to stop training")
            raise HTTPException(
                status_code=500, detail=f"Failed to stop training: {str(e)}"
            )
