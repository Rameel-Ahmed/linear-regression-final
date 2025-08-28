# controllers/user_controller.py

from typing import Any
import numpy as np
from fastapi import UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from backend.api_helpers import APIHelper
from backend.utils.csv_loader import CSVLoader


class UserController:
    def __init__(self):
        self.session_data: dict[str, Any] = {}
        self.api_helpers = APIHelper(self.session_data)

    async def serve_homepage(self) -> HTMLResponse:
        try:
            with open("static/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Main page not found")

    async def analyze_data_quality(
        self, file: UploadFile, x_column: str = Form(...), y_column: str = Form(...)
    ) -> dict[str, Any]:
        try:
            df = await self.api_helpers.read_csv_file(file)
            return self.api_helpers.analyze_data_quality(df, x_column, y_column)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    async def process_data(
        self,
        file: UploadFile,
        x_column: str = Form(...),
        y_column: str = Form(...),
        remove_duplicates: bool = Form(True),
        remove_outliers: bool = Form(False),
        handle_missing: str = Form("remove"),
        remove_strings: bool = Form(True)
    ) -> dict[str, Any]:
        try:
            df = await self.api_helpers.read_csv_file(file)
            loader = CSVLoader(x_column, y_column)
            df_clean = loader.clean_data(df, remove_duplicates, remove_outliers,
                                         handle_missing, remove_strings)

            self.api_helpers.store_processed_data(
                file.filename, df, df_clean, loader, {
                    'x_column': x_column, 'y_column': y_column,
                    'remove_duplicates': remove_duplicates,
                    'remove_outliers': remove_outliers,
                    'handle_missing': handle_missing,
                    'remove_strings': remove_strings
                })

            return self.api_helpers.prepare_process_response(file.filename, df, df_clean, loader)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    async def start_training(
        self,
        learning_rate: float = Form(...),
        epochs: int = Form(...),
        tolerance: float = Form(...),
        early_stopping: bool = Form(True),
        train_split: float = Form(0.8),
        training_speed: float = Form(1.0)
    ) -> StreamingResponse:
        try:
            training_setup = self.api_helpers.setup_training(train_split)
            return StreamingResponse(
                self.api_helpers.training_stream(
                    training_setup['model'],
                    training_setup['x_data'],
                    training_setup['y_data'],
                    training_setup['split_result'],
                    learning_rate, epochs, tolerance,
                    early_stopping, training_speed
                ),
                media_type="text/plain"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

    async def pause_training(self) -> dict[str, str]:
        try:
            if (self.session_data.get('training_active', False) and
                not self.session_data.get('training_paused', False)):
                self.session_data['training_paused'] = True
                return {"message": "Training paused"}
            elif self.session_data.get('training_paused', False):
                return {"message": "Training already paused"}
            else:
                return {"message": "No active training to pause"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to pause training: {str(e)}")

    async def resume_training(self) -> dict[str, str]:
        try:
            if (self.session_data.get('training_active', False) and
                self.session_data.get('training_paused', False)):
                self.session_data['training_paused'] = False
                return {"message": "Training resumed"}
            elif not self.session_data.get('training_paused', False):
                return {"message": "Training not paused"}
            else:
                return {"message": "No active training to resume"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to resume training: {str(e)}")

    async def stop_training(self) -> dict[str, str]:
        try:
            if self.session_data.get('training_active', False):
                self.session_data['training_active'] = False
                self.session_data['training_paused'] = False
                return {"message": "Training stop requested"}
            else:
                return {"message": "No active training to stop"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to stop training: {str(e)}")
