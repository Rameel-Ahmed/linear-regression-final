# Linear Regression Model with Real-Time Training

A complete linear regression implementation with real-time training visualization, built using FastAPI, custom gradient descent, and modern web technologies.

## 🏗️ Project Architecture

This project follows a clean, modular architecture with clear separation of concerns:

- **Frontend**: HTML/CSS/JavaScript for user interaction
- **API Layer**: FastAPI server handling HTTP requests
- **Backend**: Modular Python classes for ML operations
- **Real-time Updates**: Server-Sent Events for live training progress

## 📁 File Structure & Purpose

### 🌐 Frontend Files (`static/`)

#### `static/index.html`
- **Purpose**: Main landing page with CSV upload interface
- **Features**: 
  - File upload form with column selection
  - Data cleaning options configuration
  - Navigation to training and results pages
- **Key Elements**: Upload form, column dropdowns, cleaning options

#### `static/training.html`
- **Purpose**: Real-time training visualization page
- **Features**:
  - Training parameter controls (learning rate, epochs, etc.)
  - Live training progress display
  - Training control buttons (pause, resume, stop)
- **Key Elements**: Parameter inputs, progress charts, control buttons

#### `static/results.html`
- **Purpose**: Display final training results and model performance
- **Features**:
  - Final model parameters and equation
  - Performance metrics (RMSE, MAE, R²)
  - Sklearn comparison results
- **Key Elements**: Results summary, metrics display, comparison charts

#### `static/css/styles.css`
- **Purpose**: Global styling and responsive design
- **Features**: Modern UI design, responsive layouts, consistent theming

#### `static/js/script.js`
- **Purpose**: Main frontend logic and API communication
- **Features**:
  - CSV upload handling
  - Data processing coordination
  - Page navigation management

#### `static/js/training.js`
- **Purpose**: Training page specific functionality
- **Features**:
  - Real-time training progress updates via SSE
  - Training parameter validation
  - Training control operations

#### `static/js/results.js`
- **Purpose**: Results page specific functionality
- **Features**:
  - Results data processing and display
  - Chart generation and visualization
  - Export functionality

### 🚀 API Server (`api_server.py`)

#### **Main Purpose**: FastAPI server that orchestrates the entire ML pipeline

**Key Responsibilities**:
- **HTTP Endpoint Management**: RESTful API for all operations
- **Request Routing**: Directs requests to appropriate backend modules
- **Session Management**: Maintains application state across requests
- **Error Handling**: Provides consistent error responses
- **CORS Configuration**: Enables cross-origin requests

**API Endpoints**:
- `POST /api/v1/process-data`: CSV processing and cleaning
- `POST /api/v1/start-training`: Initiates model training with streaming
- `POST /api/v1/pause-training`: Pauses ongoing training
- `POST /api/v1/resume-training`: Resumes paused training
- `POST /api/v1/stop-training`: Stops training completely

**Dependencies**: FastAPI, Uvicorn, CORS middleware

### 🔧 Backend Modules (`backend/`)

#### `backend/api/v1_helpers.py`
- **Purpose**: Business logic layer that keeps the API server clean
- **Key Responsibilities**:
  - CSV file reading and processing
  - Training setup and coordination
  - Real-time training stream management
  - Response data preparation
  - Session data management

**Main Methods**:
- `read_csv_file()`: Reads and parses CSV content
- `setup_training()`: Prepares model and data for training
- `training_stream()`: Generates real-time training updates
- `store_processed_data()`: Manages session data storage

#### `backend/csv_loader.py`
- **Purpose**: Data preprocessing and cleaning operations
- **Key Responsibilities**:
  - CSV data validation and cleaning
  - Outlier removal using IQR method
  - Missing value handling
  - String column filtering
  - Data quality validation

**Main Methods**:
- `clean_data()`: Applies all cleaning operations
- `get_cleaning_summary()`: Reports cleaning statistics
- `_remove_outliers()`: IQR-based outlier detection
- `_handle_missing_values()`: Missing data processing

#### `backend/linear_regression.py`
- **Purpose**: Main model orchestration and training coordination
- **Key Responsibilities**:
  - Model initialization and setup
  - Training data management
  - Training process coordination
  - Model evaluation and summary
  - Prediction generation

**Main Methods**:
- `train_test_split()`: Data splitting for training/validation
- `train_epoch_by_epoch()`: Training loop with real-time updates
- `predict()`: Makes predictions on new data
- `get_model_summary()`: Comprehensive model information

#### `backend/linear_regression.py`
- **Purpose**: Complete linear regression implementation with internal components
- **Key Responsibilities**:
  - Model initialization and setup
  - Training data management
  - Training process coordination
  - Model evaluation and summary
  - Prediction generation
  - Data normalization and denormalization
  - Gradient descent optimization

**Main Classes**:
- `DataNormalizer`: Handles data scaling and parameter conversion
- `GradientDescent`: Implements optimization algorithm
- `LinearRegressionModel`: Main model orchestration

**Main Methods**:
- `train_test_split()`: Data splitting for training/validation
- `train_epoch_by_epoch()`: Training loop with real-time updates
- `predict()`: Makes predictions on new data
- `get_model_summary()`: Comprehensive model information

#### `backend/metrics_calculator.py`
- **Purpose**: Performance metrics computation and tracking
- **Key Responsibilities**:
  - Real-time metrics calculation
  - Training history tracking
  - Performance summaries
  - Metric storage and retrieval

**Main Methods**:
- `calculate_metrics()`: Computes RMSE, MAE, R²
- `get_latest_metrics()`: Retrieves current metrics
- `get_metrics_summary()`: Provides comprehensive metrics overview

#### `backend/sklearn_comparison.py`
- **Purpose**: Benchmarking against scikit-learn implementation
- **Key Responsibilities**:
  - Sklearn model training
  - Performance comparison
  - Coefficient validation
  - Accuracy assessment

**Main Methods**:
- `calculate_sklearn_results()`: Trains sklearn model and computes metrics
- `_calculate_comparison_metrics()`: Computes sklearn performance metrics

### 📊 Jupyter Notebook (`Linear_Regression_Model.ipynb`)
- **Purpose**: Interactive development and testing environment
- **Features**: 
  - Model testing and validation
  - Parameter experimentation
  - Performance analysis
  - Development workflow

### 📋 Configuration Files

#### `requirements.txt`
- **Purpose**: Python dependency specification
- **Key Dependencies**:
  - FastAPI: Web framework
  - Uvicorn: ASGI server
  - Pandas: Data manipulation
  - NumPy: Numerical computing
  - Scikit-learn: Comparison baseline

#### `test.py`
- **Purpose**: Basic testing and validation
- **Features**: Simple functionality tests

## 🔄 Data Flow

### 1. **Data Upload & Processing**
```
CSV Upload → CSVLoader → Data Cleaning → Session Storage
```

### 2. **Training Pipeline**
```
Training Setup → Data Normalization → Gradient Descent → Real-time Updates
```

### 3. **Results Generation**
```
Model Evaluation → Metrics Calculation → Sklearn Comparison → Results Display
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd linear-regression-model

# Install dependencies
pip install -r requirements.txt

# Run the server
python api_server.py
```

### Usage
1. **Upload CSV**: Navigate to the main page and upload your dataset
2. **Configure**: Select X/Y columns and cleaning options
3. **Train**: Set training parameters and start training
4. **Monitor**: Watch real-time training progress
5. **Analyze**: Review results and model performance

## 🎯 Key Features

- **Real-time Training**: Live updates during model training
- **Interactive Controls**: Pause, resume, and stop training
- **Data Cleaning**: Automated preprocessing and validation
- **Performance Metrics**: Comprehensive model evaluation
- **Sklearn Comparison**: Benchmarking against industry standard
- **Responsive UI**: Modern, mobile-friendly interface
- **Modular Architecture**: Clean, maintainable codebase

## 🔧 Technical Details

### **Real-time Updates**
- Uses Server-Sent Events (SSE) for live training progress
- Efficient streaming without polling
- Real-time metrics and parameter updates

### **Data Processing**
- Automated outlier detection using IQR method
- Missing value handling strategies
- Data type validation and conversion

### **Model Training**
- Custom gradient descent implementation
- Early stopping and convergence detection
- Learning rate and tolerance controls

### **Performance Optimization**
- Vectorized operations using NumPy
- Efficient matrix operations
- Memory-conscious data handling

## 🧪 Testing & Validation

### **Model Validation**
- Train/test split for unbiased evaluation
- Multiple performance metrics (RMSE, MAE, R²)
- Sklearn comparison for accuracy validation

### **Data Validation**
- Input data type checking
- Column existence validation
- Data quality assessment

## 🔮 Future Enhancements

- **Additional Algorithms**: Support for other optimization methods
- **Advanced Preprocessing**: More sophisticated data cleaning options
- **Model Persistence**: Save and load trained models
- **Batch Processing**: Handle larger datasets efficiently
- **API Documentation**: Interactive API documentation
- **Authentication**: User management and model sharing

## 🤝 Contributing

This project follows clean code principles:
- **OOP Design**: Proper encapsulation and inheritance
- **PEP8 Compliance**: Python style guide adherence
- **Single Responsibility**: Each class has one clear purpose
- **Error Handling**: Comprehensive exception management
- **Documentation**: Clear docstrings and comments

## 📄 License

This project is open source and available under the MIT License.

---

**Built with using modern Python and web technologies**
├── .gitignore
├── README.md
├── backend
    ├── api_helpers.py
    ├── models
    │   ├── data_normalizer.py
    │   ├── gradient_descent.py
    │   ├── linear_regression.py
    │   └── metrics_calculator.py
    └── utils
    │   ├── csv_loader.py
    │   └── sklearn_comparison.py
├── controller
    └── user_controller.py
├── main.py
├── requirements.txt
├── routes
    └── user_routes.py
└── static
    ├── css
        └── styles.css
    ├── index.html
    ├── js
        ├── helping_functions.js
        ├── results.js
        ├── script.js
        ├── state.js
        ├── training.js
        └── visualization-functions.js
    ├── results.html
    └── training.html