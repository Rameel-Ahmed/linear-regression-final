"""
Linear Regression API Server
FastAPI-based server for linear regression model training and prediction.
Clean API layer that uses backend helpers for business logic.
"""

from typing import Dict, Any

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from backend.api_helpers import APIHelpers
from backend.csv_loader import CSVLoader


# Global session storage (shared across endpoints)
session_data: Dict[str, Any] = {}

# Initialize API helpers
api_helpers = APIHelpers(session_data)

# Create FastAPI app
app = FastAPI(title="Linear Regression API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve the main HTML page."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Main page not found")

@app.post("/api/analyze-data-quality")
async def analyze_data_quality(
    file: UploadFile = File(...),
    x_column: str = Form(...),
    y_column: str = Form(...)
) -> Dict[str, Any]:
    """Analyze data quality without cleaning."""
    try:
        # Read CSV file
        df = await api_helpers.read_csv_file(file)
        quality_report = api_helpers.analyze_data_quality(df, x_column, y_column)
        
        return quality_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
@app.post("/api/process-data")
async def process_data(
    file: UploadFile = File(...),
    x_column: str = Form(...),
    y_column: str = Form(...),
    remove_duplicates: bool = Form(True),
    remove_outliers: bool = Form(False),
    handle_missing: str = Form("remove"),
    remove_strings: bool = Form(True)
) -> Dict[str, Any]:
    """Process CSV data with cleaning options."""
    try:
        # Read CSV file
        df = await api_helpers.read_csv_file(file)
        
        # Create CSV loader and process data
        loader = CSVLoader(x_column, y_column)
        df_clean = loader.clean_data(
            df, remove_duplicates, remove_outliers, 
            handle_missing, remove_strings
        )
        
        # Store processed data in session
        api_helpers.store_processed_data(file.filename, df, df_clean, loader, {
            'x_column': x_column, 'y_column': y_column,
            'remove_duplicates': remove_duplicates, 
            'remove_outliers': remove_outliers,
            'handle_missing': handle_missing, 
            'remove_strings': remove_strings
        })
        
        # Return response
        return api_helpers.prepare_process_response(file.filename, df, df_clean, loader)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/api/start-training")
async def start_training(
    learning_rate: float = Form(...),
    epochs: int = Form(...),
    tolerance: float = Form(...),
    early_stopping: bool = Form(True),
    train_split: float = Form(0.8),
    training_speed: float = Form(1.0)
) -> StreamingResponse:
    """Start linear regression training with streaming response."""
    try:
        # Setup training using helper
        training_setup = api_helpers.setup_training(train_split)
        
        return StreamingResponse(
            api_helpers.training_stream(
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


@app.post("/api/pause-training")
async def pause_training() -> Dict[str, str]:
    """Pause ongoing training."""
    try:
        if (session_data.get('training_active', False) and 
            not session_data.get('training_paused', False)):
            session_data['training_paused'] = True
            return {"message": "Training paused"}
        elif session_data.get('training_paused', False):
            return {"message": "Training already paused"}
        else:
            return {"message": "No active training to pause"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pause training: {str(e)}")


@app.post("/api/resume-training")
async def resume_training() -> Dict[str, str]:
    """Resume paused training."""
    try:
        if (session_data.get('training_active', False) and 
            session_data.get('training_paused', False)):
            session_data['training_paused'] = False
            return {"message": "Training resumed"}
        elif not session_data.get('training_paused', False):
            return {"message": "Training not paused"}
        else:
            return {"message": "No active training to resume"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume training: {str(e)}")


@app.post("/api/stop-training")
async def stop_training() -> Dict[str, str]:
    """Stop ongoing training."""
    try:
        if session_data.get('training_active', False):
            session_data['training_active'] = False
            session_data['training_paused'] = False
            return {"message": "Training stop requested"}
        else:
            return {"message": "No active training to stop"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop training: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)