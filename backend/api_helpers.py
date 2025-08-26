"""
API Helper Functions for Linear Regression API Server.
Contains all helper functions to keep the main API server clean.
"""

import asyncio
import io
import json
from typing import Dict, Any

import numpy as np
import pandas as pd
from fastapi import UploadFile

from .csv_loader import CSVLoader
from .linear_regression import LinearRegressionModel
from .sklearn_comparison import SklearnComparison


class APIHelpers:
    """Helper class for API server operations."""
    
    def __init__(self, session_data: Dict[str, Any]):
        """Initialize with session data reference."""
        self.session_data = session_data
    
    # Public interface methods
    async def read_csv_file(self, file: UploadFile) -> pd.DataFrame:
        """Read CSV file content into DataFrame."""
        content = await file.read()
        return pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    def analyze_data_quality(self, df: pd.DataFrame, x_column: str, y_column: str) -> Dict[str, Any]:
        """Analyze data quality by calling CSVLoader method."""
        # Create CSV loader instance for analysis
        loader = CSVLoader(x_column, y_column)
        
        # Call the analyze method from CSVLoader (no need to pass columns again)
        return loader.analyze_data_quality(df)
    
    def store_processed_data(self, filename: str, df: pd.DataFrame, 
                           df_clean: pd.DataFrame, loader: CSVLoader, 
                           cleaning_options: Dict[str, Any]):
        """Store processed data in session."""
        self.session_data.update({
            'csv_data': df,
            'columns': df.columns.tolist(),
            'filename': filename,
            'cleaned_data': df_clean,
            'csv_loader': loader,
            'cleaning_options': cleaning_options
        })
    
    def prepare_process_response(self, filename: str, df: pd.DataFrame, 
                               df_clean: pd.DataFrame, loader: CSVLoader) -> Dict[str, Any]:
        """Prepare response data for processed CSV."""
        cleaning_options = self.session_data['cleaning_options']
        x_column = cleaning_options['x_column']
        y_column = cleaning_options['y_column']
        
        return {
            "message": "Data processed successfully!",
            "file_info": {
                "filename": filename, 
                "original_shape": df.shape, 
                "cleaned_shape": df_clean.shape
            },
            "columns": {
                "x_column": x_column, 
                "y_column": y_column, 
                "all_columns": df.columns.tolist()
            },
            "cleaning_summary": loader.get_cleaning_summary(df, df_clean),
            "statistics": {
                "x_data": df_clean[x_column].values.tolist(),
                "y_data": df_clean[y_column].values.tolist(),
                "x_mean": float(df_clean[x_column].mean()),
                "y_mean": float(df_clean[y_column].mean()),
                "x_std": float(df_clean[x_column].std()),
                "y_std": float(df_clean[y_column].std())
            },
            "model_summary": {
                "data_quality": "clean",
                "total_features": 2,
                "data_type": "numerical",
                "ready_for_training": True
            },
            "next_step": "ready_for_training"
        }
    
    def setup_training(self, train_split: float) -> Dict[str, Any]:
        """Setup training by initializing model and splitting data."""
        # Validate prerequisites
        if 'cleaned_data' not in self.session_data:
            raise ValueError("No cleaned data available for training")
        
        # Get training data
        df_clean = self.session_data['cleaned_data']
        cleaning_options = self.session_data['cleaning_options']
        x_column, y_column = cleaning_options['x_column'], cleaning_options['y_column']
        
        x_data = df_clean[x_column].values
        y_data = df_clean[y_column].values
        
        # Initialize model and split data
        model = LinearRegressionModel(x_data, y_data)
        split_result = model.train_test_split(train_ratio=train_split)
        model.set_training_data(split_result['x_train'], split_result['y_train'])
        
        # Store training state
        self._initialize_training_state(model)
        
        return {
            'model': model,
            'x_data': x_data,
            'y_data': y_data,
            'split_result': split_result
        }
    
    async def training_stream(self, model: LinearRegressionModel, x_data: np.ndarray,
                            y_data: np.ndarray, split_result: Dict[str, np.ndarray],
                            learning_rate: float, epochs: int, tolerance: float,
                            early_stopping: bool, training_speed: float):
        """Stream training progress."""
        try:
            x_test, y_test = split_result['x_test'], split_result['y_test']
            x_train_orig, y_train_orig = split_result['x_train'], split_result['y_train']
            
            epoch_delay = self._get_training_delay(training_speed)
            
            for epoch_data in model.train_epoch_by_epoch(
                learning_rate=learning_rate,
                max_epochs=epochs,
                tolerance=tolerance,
                early_stopping=early_stopping
            ):
                # Check training control state
                if not self._should_continue_training():
                    break
                
                # Wait if paused
                await self._handle_training_pause()
                
                # Prepare epoch response
                response_data = self._prepare_epoch_response(
                    epoch_data, model, x_train_orig, y_train_orig
                )
                
                yield f"data: {json.dumps(response_data)}\n\n"
                
                # Add delay between epochs
                if not epoch_data['is_complete']:
                    await asyncio.sleep(epoch_delay)
            
            # Send final results
            final_data = await self._prepare_final_results(model, x_data, y_data, x_test, y_test)
            yield f"data: {json.dumps(final_data)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': True, 'message': str(e)})}\n\n"
        finally:
            self._cleanup_training_state()
    
    # Private helper methods (internal implementation)
    def _initialize_training_state(self, model: LinearRegressionModel):
        """Initialize training state variables."""
        self.session_data.update({
            'training_active': True,
            'training_paused': False,
            'training_model': model
        })
    
    def _get_training_delay(self, training_speed: float) -> float:
        """Get epoch delay based on training speed setting."""
        speed_delays = {
            1.0: 0.1,    # Fast: 100ms between epochs
            0.8: 0.3,    # Fast-Medium: 300ms between epochs
            0.6: 0.6,    # Medium: 600ms between epochs
            0.4: 1.0,    # Slow: 1s between epochs
            0.2: 1.5     # Very Slow: 1.5s between epochs
        }
        
        current_speed = min(speed_delays.keys(), key=lambda x: abs(x - training_speed))
        return speed_delays[current_speed]
    
    def _should_continue_training(self) -> bool:
        """Check if training should continue."""
        return self.session_data.get('training_active', False)
    
    async def _handle_training_pause(self):
        """Handle training pause state."""
        while (self.session_data.get('training_paused', False) and 
               self.session_data.get('training_active', False)):
            await asyncio.sleep(0.5)
    
    def _prepare_epoch_response(self, epoch_data: Dict[str, Any], 
                              model: LinearRegressionModel, x_train_orig: np.ndarray,
                              y_train_orig: np.ndarray) -> Dict[str, Any]:
        """Prepare response data for each training epoch."""
        original_params = model.get_original_scale_parameters()
        
        # Calculate original scale cost every 10 epochs for performance
        if epoch_data['epoch'] % 10 == 0 or epoch_data['is_complete']:
            train_predictions = model.predict(x_train_orig)
            original_cost = np.mean((train_predictions - y_train_orig) ** 2)
        else:
            original_cost = epoch_data['cost']
        
        return {
            "epoch": int(epoch_data['epoch']),
            "max_epochs": int(epoch_data['max_epochs']),
            "theta0": float(original_params['theta0']),
            "theta1": float(original_params['theta1']),
            "cost": float(original_cost),
            "converged": bool(epoch_data['converged']),
            "is_complete": bool(epoch_data['is_complete']),
            "rmse": float(epoch_data.get('rmse', 0.0)),
            "mae": float(epoch_data.get('mae', 0.0)),
            "r2": float(epoch_data.get('r2', 0.0))
        }
    
    async def _prepare_final_results(self, model: LinearRegressionModel, 
                                   x_data: np.ndarray, y_data: np.ndarray,
                                   x_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Prepare final training results."""
        # Calculate test metrics
        test_predictions = model.predict(x_test)
        test_mse = np.mean((test_predictions - y_test) ** 2)
        
        ss_res = np.sum((y_test - test_predictions) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        test_r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Get final parameters and metrics
        final_params = model.get_original_scale_parameters()
        final_metrics = model.get_latest_metrics()
        metrics_summary = model.get_model_summary()
        
        # Calculate sklearn comparison
        sklearn_results = await self._calculate_sklearn_comparison(x_data, y_data)
        
        # Store trained model
        self.session_data['trained_model'] = model
        
        return {
            "training_complete": True,
            "final_theta0": final_params['theta0'],
            "final_theta1": final_params['theta1'],
            "equation": f"y = {final_params['theta0']:.4f} + {final_params['theta1']:.4f} * x",
            "test_mse": test_mse,
            "test_r2": test_r2,
            "x_range": [float(np.min(x_data)), float(np.max(x_data))],
            "y_range": [float(np.min(y_data)), float(np.max(y_data))],
            "final_rmse": final_metrics.get('rmse', 0.0),
            "final_mae": final_metrics.get('mae', 0.0),
            "final_r2": final_metrics.get('r2', 0.0),
            "metrics_summary": metrics_summary,
            "sklearn_comparison": {
                "sklearn_results": sklearn_results,
                "status": "success" if sklearn_results else "failed"
            }
        }
    
    async def _calculate_sklearn_comparison(self, x_data: np.ndarray, 
                                          y_data: np.ndarray) -> Dict[str, Any]:
        """Calculate sklearn comparison results."""
        try:
            sklearn_comp = SklearnComparison()
            return sklearn_comp.calculate_sklearn_results(x_data, y_data)
        except Exception:
            return None
    
    def _cleanup_training_state(self):
        """Clean up training state variables."""
        self.session_data.update({
            'training_active': False,
            'training_paused': False
        })
