# Linear Regression Platform - COMPLETE Sequence Diagram

## System Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    ┌─────────────────┐    │   Backend       │
│   (Browser)     │◄──►│   FastAPI       │◄──►│   ML Models     │
│                 │    │   Server        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## COMPLETE User Journey Sequence

### 1. Application Initialization & State Management
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    U->>B: Navigate to localhost:8000
    B->>S: GET /
    S->>C: serve_homepage()
    C->>S: Return static/index.html
    S->>B: HTML Response
    
    B->>B: Load CSS/JS files
    B->>B: Initialize theme (light/dark)
    B->>B: Setup event listeners
    B->>B: Check localStorage for saved state
    
    alt Has saved training data
        B->>B: Load saved state from localStorage
        B->>B: Restore cleaned data and statistics
        B->>B: Show visualization section
        B->>B: Create charts with saved data
        B->>B: Enable "Proceed to Training"
    else No saved state
        B->>B: Reset to initial state
        B->>B: Show upload interface
    end
    
    B->>B: Setup file drag & drop handlers
    B->>B: Setup file input change handler
    B->>B: Setup column selection change handlers
    B->>B: Display upload interface
```

### 2. File Upload & CSV Processing
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    U->>B: Upload CSV file (drag & drop or file picker)
    
    alt File validation checks
        B->>B: Check file extension (.csv)
        B->>B: Check file size (< 10MB limit)
        
        alt File size exceeds limit
            B->>B: Show error: "File size exceeds 10MB limit"
            B->>B: Stop processing
        else File size OK
            B->>B: Continue processing
        end
    end
    
    B->>B: FileReader.readAsText(file)
    B->>B: parseCSV(csvText)
    
    alt CSV parsing validation
        B->>B: Split by lines and check minimum rows (2)
        
        alt Insufficient rows
            B->>B: Show error: "CSV must have at least 2 rows"
            B->>B: Stop processing
        else Sufficient rows
            B->>B: Detect separator (comma, semicolon, tab)
            B->>B: Parse headers and trim quotes
            B->>B: Parse data rows (limit to 1000 rows)
            
            loop For each data row
                B->>B: Split by separator
                B->>B: Convert to numeric where possible
                B->>B: Store in csvData array
            end
            
            alt No valid data rows
                B->>B: Show error: "No valid data rows found"
                B->>B: Stop processing
            else Valid data found
                B->>B: updateDataPreview()
                B->>B: populateColumnSelectors()
                B->>B: Show preview section
            end
        end
    end
    
    B->>B: resetWorkflow() - Clear previous state
    B->>B: Destroy existing charts
    B->>B: Clear stored data
    B->>B: Reset button states
```

### 3. Column Selection & Validation
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    B->>B: populateColumnSelectors()
    
    loop For each header column
        B->>B: Count numeric values in column
        alt Column has numeric data
            B->>B: Add to numericColumns array
        end
    end
    
    alt Insufficient numeric columns
        B->>B: Show error: "Need at least 2 numeric columns"
        B->>B: Stop column selection
    else Sufficient columns
        B->>B: Populate X and Y dropdowns
        B->>B: Show column selection section
    end
    
    U->>B: Select X column from dropdown
    U->>B: Select Y column from dropdown
    
    B->>B: checkColumnSelection()
    
    alt Column validation
        B->>B: Check if both columns selected
        B->>B: Check if columns are different
        
        alt Same column selected
            B->>B: Show error: "X and Y columns must be different"
            B->>B: Disable analyze button
        else Different columns selected
            B->>B: Enable analyze button
        end
    end
```

### 4. Data Quality Analysis
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant L as CSV Loader

    U->>B: Click "Analyze Data Quality"
    
    alt Pre-analysis validation
        B->>B: Check if columns selected
        B->>B: Check if file uploaded
        
        alt Validation failed
            B->>B: Show error: "Please select different X and Y columns"
            B->>B: Stop analysis
        else Validation passed
            B->>B: Continue with analysis
        end
    end
    
    B->>B: analyzeDataQualityAPI(xCol, yCol)
    B->>B: Create FormData with file and columns
    B->>S: POST /api/v1/analyze-data-quality
    
    alt API response handling
        alt Response successful
            S->>C: analyze_data_quality()
            C->>H: read_csv_file()
            H->>C: Return DataFrame
            C->>H: analyze_data_quality()
            H->>C: Return quality report
            C->>S: Return analysis results
            S->>B: Data quality report
            
            B->>B: displayDataQualityReport(analysis)
            B->>B: Store analysis results in window.dataQualityAnalysis
            B->>B: showQualityToast(analysis)
            
            alt Quality report display
                B->>B: Determine toast type (warning/success)
                B->>B: Create toast with formatted issues
                B->>B: Show toast with animation
                B->>B: Auto-remove after 15 seconds
            end
            
            B->>B: showCleaningOptions()
            
        else Response failed
            S->>B: Error response
            B->>B: showDataQualityError("Error analyzing data: " + error.detail)
            B->>B: Show retry button
        end
    end
```

### 5. Data Cleaning Configuration
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    B->>B: showCleaningOptions()
    B->>B: Hide quality section, show cleaning section
    B->>B: setCleaningDefaults()
    
    alt Smart defaults based on quality report
        B->>B: Check if issues exist in analysis
        
        alt No issues found
            B->>B: Show "no issues" message
            B->>B: Hide issue-specific options
            B->>B: Show outliers option (default: keep)
        else Issues found
            B->>B: Hide "no issues" message
            
            loop For each issue in analysis
                alt Missing values detected
                    B->>B: Show missing values option
                    B->>B: Calculate missing percentage
                    
                    alt Missing > 20%
                        B->>B: Set default: "fill with mean"
                    else Missing ≤ 20%
                        B->>B: Set default: "remove rows"
                    end
                end
                
                alt Outliers detected
                    B->>B: Show outliers option
                    B->>B: Set default: "keep outliers"
                end
                
                alt Duplicates detected
                    B->>B: Show duplicates option
                    B->>B: Set default: "remove duplicates"
                end
            end
        end
    end
    
    U->>B: Configure cleaning options:
    Note over U,B: • Missing values: remove/fill mean
    Note over U,B: • Outliers: remove/keep
    Note over U,B: • Duplicates: remove/keep
    Note over U,B: • Strings: always remove
    
    U->>B: Click "Process & Clean Data"
```

### 6. Data Cleaning Execution
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant L as CSV Loader

    B->>B: cleanData()
    
    alt Pre-cleaning validation
        B->>B: Check if cleaning options selected
        
        alt Missing options
            B->>B: Show error: "Please choose how to handle missing values and outliers"
            B->>B: Stop cleaning
        else All options selected
            B->>B: Continue with cleaning
        end
    end
    
    B->>B: Disable clean button (prevent double-click)
    B->>B: cleanDataAPI()
    B->>B: Create FormData with all cleaning parameters
    B->>S: POST /api/v1/process-data
    
    alt API response handling
        alt Response successful
            S->>C: process_data()
            C->>H: read_csv_file()
            H->>C: Return DataFrame
            C->>L: clean_data()
            
            Note over L: Data cleaning operations:
            Note over L: • Remove duplicates (if selected)
            Note over L: • Handle missing values (remove/fill)
            Note over L: • Remove outliers (if selected)
            Note over L: • Filter string columns
            Note over L: • Z-score normalization
            
            L->>C: Return cleaned DataFrame
            C->>H: store_processed_data()
            C->>S: Return processing results
            S->>B: Cleaned data + statistics
            
            B->>B: showCleaningResults(result)
            B->>B: Update cleaning preview with actual results
            B->>B: Store cleaned data in window variables
            B->>B: Store statistics from backend
            B->>B: showSuccessToast("Data cleaned successfully!")
            B->>B: Store in localStorage for training page
            B->>B: advanceStep(2, { trainingData: result })
            
        else Response failed
            S->>B: Error response
            B->>B: showErrorToast("Error cleaning data: " + error.detail)
        end
    end
    
    B->>B: Re-enable clean button
    B->>B: showVisualizations()
```

### 7. Data Visualization Creation
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    B->>B: showVisualizations()
    B->>B: Hide cleaning section, show visualization section
    B->>B: Scroll to visualization section
    
    B->>B: createDataVisualizations()
    
    alt Data validation for visualization
        B->>B: Check if training data exists
        B->>B: Check if x_data and y_data arrays exist
        B->>B: Check if arrays have data
        
        alt Data validation failed
            B->>B: Log error: "Invalid data for plotting"
            B->>B: Stop visualization
        else Data validation passed
            B->>B: Create valid data array format
            B->>B: createScatterPlot(validData, xColumn, yColumn)
            B->>B: createDensityPlot(validData, xColumn, yColumn)
            B->>B: createRangePlot(validData, xColumn, yColumn)
            B->>B: createStatisticalSummary(validData, xColumn, yColumn)
        end
    end
    
    B->>B: Enable "Proceed to Training" button
    B->>B: Store navigation flag in sessionStorage
```

### 8. Training Page Navigation & Setup
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    U->>B: Click "Proceed to Training"
    B->>B: Navigate to training.html
    B->>B: Load training interface
    
    alt State restoration
        B->>B: Check localStorage for training data
        
        alt Has training data
            B->>B: Load training data from localStorage
            B->>B: Restore cleaned data and statistics
            B->>B: createDataVisualizations()
            B->>B: Setup charts with stored data
        else No training data
            B->>B: Redirect back to upload page
            B->>B: Show error: "No training data found"
        end
    end
    
    B->>B: Initialize training interface
    B->>B: setupCharts()
    B->>B: createScatterChart()
    B->>B: createCostChart()
    B->>B: Display parameter controls
    B->>B: Initialize performance metrics
    B->>B: Setup parameter presets (Accurate/Custom)
    
    U->>B: Configure training parameters:
    Note over U,B: • Learning rate (0.001 - 0.1)
    Note over U,B: • Max epochs (100 - 2000)
    Note over U,B: • Tolerance (1e-6 - 1e-2)
    Note over U,B: • Early stopping (true/false)
    Note over U,B: • Train split (0.7 - 0.9)
    Note over U,B: • Training speed (0.2 - 1.0)
    
    U->>B: Select training mode (Accurate/Custom)
    B->>B: Update parameter presets
    B->>B: Validate parameter ranges
    B->>B: Enable "Start Training" button
```

### 9. Model Training & Real-time Updates (COMPLETE)
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant M as Linear Regression Model
    participant G as Gradient Descent
    participant N as Data Normalizer
    participant MC as Metrics Calculator

    U->>B: Click "Start Training"
    B->>B: Disable start button, enable pause/stop
    B->>B: Initialize training state variables
    B->>B: Setup page unload handler
    B->>B: POST /api/v1/start-training
    
    alt API response handling
        alt Response successful
            S->>C: start_training()
            C->>H: setup_training()
            H->>M: Create LinearRegressionModel
            
            M->>N: Normalize training data (Z-score)
            M->>M: Split train/test data (80/20 default)
            M->>G: Initialize gradient descent
            M->>M: Set initial parameters: theta_0 = 0, theta_1 = 0
            
            Note over M: MAIN TRAINING LOOP - Epoch by Epoch
            loop For each epoch until convergence
                M->>G: compute_cost(theta)
                G->>M: Return current cost J(theta_0, theta_1)
                M->>G: compute_gradients(theta)
                G->>M: Return gradients (grad_0, grad_1)
                
                M->>M: Update parameters using gradient descent:
                Note over M: theta_0 := theta_0 - alpha * grad_0
                Note over M: theta_1 := theta_1 - alpha * grad_1
                
                M->>M: Check for numerical issues (NaN/Inf)
                
                alt Numerical issues detected
                    M->>M: Break training loop
                    M->>M: Log error: "Numerical failure detected"
                else Parameters valid
                    M->>M: Check convergence criteria
                    M->>M: Calculate cost change |Δcost|
                    
                    alt Convergence check
                        alt Cost change < tolerance
                            M->>M: Set converged = true
                            M->>M: Check early stopping
                            
                            alt Early stopping enabled
                                M->>M: Increment no_improve counter
                                
                                alt No improvement for 15 epochs
                                    M->>M: Break training loop
                                end
                            end
                        else Cost change ≥ tolerance
                            M->>M: Set converged = false
                            M->>M: Reset no_improve counter
                        end
                    end
                    
                    M->>M: Calculate metrics on original scale
                    M->>MC: calculate_metrics(y_true, y_pred, epoch)
                    MC->>M: Return RMSE, MAE, R²
                    
                    M->>H: Yield epoch data with all metrics
                    H->>C: Stream epoch update
                    C->>S: StreamingResponse
                    S->>B: Server-Sent Event
                    
                    alt Training speed control
                        alt Speed = 0 (paused)
                            B->>B: Don't update visual elements
                        else Speed > 0
                            B->>B: Update cost chart (always)
                            B->B: Update regression line
                            B->>B: Update parameter displays
                            B->>B: Update performance metrics
                            B->>B: Update equation display
                            B->>B: Update progress bar
                            B->>B: Update training status
                        end
                    end
                    
                    alt User interaction during training
                        alt Pause clicked
                            U->>B: Click "Pause"
                            B->>B: pauseTraining()
                            B->>S: POST /api/v1/pause-training
                            S->>C: pause_training()
                            C->>H: Set pause flag
                            B->>B: Update button states
                            B->>B: Show "Training paused" status
                            Note over M: Training continues but no updates sent
                        end
                        
                        alt Resume clicked
                            U->>B: Click "Resume"
                            B->>B: resumeTraining()
                            B->>S: POST /api/v1/resume-training
                            S->>C: resume_training()
                            C->>H: Clear pause flag
                            B->>B: Update button states
                            B->>B: Show "Training resumed" status
                            Note over M: Resume sending updates
                        end
                        
                        alt Stop clicked
                            U->>B: Click "Stop"
                            B->>B: stopTraining()
                            B->>S: POST /api/v1/stop-training
                            S->>C: stop_training()
                            C->>H: Set stop flag
                            M->>M: Break training loop
                            B->>B: Cancel all animations
                            B->>B: Clear pending epochs
                            B->>B: Update button states
                            B->>B: Hide equation display
                            B->>B: Show "Training stopped" status
                        end
                    end
                end
                
                alt Training completion check
                    alt Epoch >= max_epochs OR converged
                        M->>M: Break training loop
                    end
                end
            end
            
            M->>M: Training complete
            M->>H: Final model summary
            H->>C: Training completion
            C->>S: Final response
            S->>B: Training results
            
        else Response failed
            S->>B: Error response
            B->>B: Show error: "Training failed to start"
            B->>B: Re-enable start button
        end
    end
    
    B->>B: Display final metrics
    B->>B: Enable "View Results" button
    B->>B: Remove page unload handler
```

### 10. Results & Predictions
```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant M as Linear Regression Model

    U->>B: Click "View Results"
    B->>B: Navigate to results.html
    B->>B: Load results interface
    
    alt State restoration
        B->>B: Check localStorage for training data
        
        alt Has training data
            B->>B: Load training data and results
            B->>B: Display final model equation
            B->>B: Show performance metrics (RMSE, MAE, R²)
            B->>B: Display sklearn comparison
            B->>B: Show prediction interface
        else No training data
            B->>B: Redirect back to training page
            B->>B: Show error: "No results found"
        end
    end
    
    U->>B: Enter new X values for prediction
    B->>B: Validate input data (numeric, range check)
    
    alt Input validation
        alt Invalid input
            B->>B: Show error: "Please enter valid numeric values"
            B->>B: Stop prediction
        else Valid input
            B->>B: Calculate predictions using model equation
            Note over B: y = theta_0 + theta_1 * x
            
            B->>B: Display prediction results
            B->>B: Show confidence intervals
            B->>B: Enable export functionality
        end
    end
    
    U->>B: Export model parameters
    B->>B: Download results as JSON/CSV
    B->>B: Include model equation, parameters, and metrics
```

## Key Loops & Conditional Flows

### Training Loop with ALL Conditions
```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETE TRAINING LOOP                   │
├─────────────────────────────────────────────────────────────┤
│ 1. Initialize: theta_0 = 0, theta_1 = 0                   │
│ 2. For epoch = 1 to max_epochs:                            │
│    ├─ Compute cost: J(theta_0, theta_1)                   │
│    ├─ Compute gradients: ∂J/∂theta_0, ∂J/∂theta_1         │
│    ├─ Update parameters:                                   │
│    │   theta_0 := theta_0 - α * ∂J/∂theta_0              │
│    │   theta_1 := theta_1 - α * ∂J/∂theta_1              │
│    ├─ Check for NaN/Inf values                            │
│    ├─ Check convergence: |Δcost| < tolerance               │
│    ├─ Early stopping check (15 epochs no improvement)      │
│    ├─ Calculate metrics: RMSE, MAE, R²                     │
│    ├─ Stream update to frontend                            │
│    ├─ Handle user interactions (pause/resume/stop)         │
│    ├─ Update visualizations based on training speed        │
│    └─ Check completion criteria                            │
│ 3. Return final parameters and metrics                     │
└─────────────────────────────────────────────────────────────┘
```

### Data Processing Pipeline with ALL Checks
```
┌─────────────────────────────────────────────────────────────┐
│                COMPLETE DATA PROCESSING PIPELINE            │
├─────────────────────────────────────────────────────────────┤
│ 1. File Upload & Validation                                │
│    ├─ Extension check (.csv)                               │
│    ├─ Size check (< 10MB)                                  │
│    ├─ Content validation (min 2 rows)                      │
│    └─ Data type validation                                 │
│ 2. CSV Parsing & Processing                                │
│    ├─ Separator detection (comma, semicolon, tab)          │
│    ├─ Header parsing and cleaning                          │
│    ├─ Row parsing (limit 1000 rows)                        │
│    └─ Numeric conversion where possible                    │
│ 3. Column Selection & Validation                           │
│    ├─ Numeric column detection                             │
│    ├─ Minimum column count check (2)                       │
│    ├─ Different column validation                          │
│    └─ Dropdown population                                  │
│ 4. Data Quality Analysis                                   │
│    ├─ Missing value detection                              │
│    ├─ Outlier identification                               │
│    ├─ Duplicate detection                                  │
│    └─ Quality report generation                            │
│ 5. Data Cleaning Configuration                             │
│    ├─ Smart defaults based on quality report               │
│    ├─ Missing value handling (remove/fill mean)            │
│    ├─ Outlier handling (remove/keep)                       │
│    ├─ Duplicate handling (remove/keep)                     │
│    └─ String column filtering                              │
│ 6. Data Cleaning Execution                                 │
│    ├─ Apply cleaning operations                            │
│    ├─ Z-score normalization                                │
│    ├─ Train/test split (80/20)                             │
│    └─ Statistics calculation                               │
│ 7. Visualization Creation                                  │
│    ├─ Data validation for plotting                         │
│    ├─ Chart creation (scatter, density, range)             │
│    ├─ Statistical summary                                  │
│    └─ State storage for training                           │
└─────────────────────────────────────────────────────────────┘
```

### Error Handling & Recovery (ALL Scenarios)
```
┌─────────────────────────────────────────────────────────────┐
│                COMPLETE ERROR HANDLING FLOW                 │
├─────────────────────────────────────────────────────────────┤
│ 1. File Upload Errors                                      │
│    ├─ Invalid file type (not .csv)                         │
│    ├─ File too large (> 10MB)                              │
│    ├─ Empty or corrupted file                              │
│    └─ Network upload failures                              │
│ 2. CSV Parsing Errors                                      │
│    ├─ Insufficient rows (< 2)                              │
│    ├─ Inconsistent column count                            │
│    ├─ Invalid data types                                   │
│    └─ Encoding issues                                      │
│ 3. Data Validation Errors                                  │
│    ├─ Insufficient numeric columns (< 2)                   │
│    ├─ Same column selected for X and Y                     │
│    ├─ No valid data rows                                   │
│    └─ All missing values in columns                        │
│ 4. API Communication Errors                                │
│    ├─ Network failures                                     │
│    ├─ Server errors (500)                                  │
│    ├─ Validation errors (422)                              │
│    └─ Timeout errors                                       │
│ 5. Training Errors                                         │
│    ├─ Numerical instability (NaN/Inf)                      │
│    ├─ Convergence failures                                 │
│    ├─ Memory issues                                        │
│    └─ Interruption handling                                │
│ 6. State Management Errors                                 │
│    ├─ Missing training data                                │
│    ├─ Corrupted localStorage                               │
│    ├─ Session expiration                                   │
│    └─ Navigation state loss                                │
│ 7. Recovery Mechanisms                                     │
│    ├─ Automatic retry for network errors                   │
│    ├─ Graceful degradation for UI errors                   │
│    ├─ State restoration from localStorage                  │
│    ├─ User-friendly error messages                         │
│    └─ Fallback to previous working state                   │
└─────────────────────────────────────────────────────────────┘
```

### Real-time Update Flow (ALL Conditions)
```
┌─────────────────────────────────────────────────────────────┐
│                COMPLETE REAL-TIME UPDATE FLOW               │
├─────────────────────────────────────────────────────────────┤
│ 1. Training Speed Control                                  │
│    ├─ Speed = 0.2 (Very Slow)                             │
│    ├─ Speed = 0.4 (Slow)                                  │
│    ├─ Speed = 0.6 (Medium)                                │
│    ├─ Speed = 0.8 (Fast-Medium)                           │
│    └─ Speed = 1.0 (Fast)                                  │
│ 2. Update Throttling                                       │
│    ├─ Cost chart updates (always)                          │
│    ├─ Regression line updates (speed-dependent)            │
│    ├─ Parameter display updates (speed-dependent)          │
│    ├─ Progress bar updates (speed-dependent)               │
│    └─ Status updates (speed-dependent)                     │
│ 3. Chart Performance Management                            │
│    ├─ Limit cost chart to 200 data points                 │
│    ├─ Smooth animations for user experience                │
│    ├─ Memory cleanup for old chart instances               │
│    ├─ Responsive chart updates                             │
│    └─ Theme-aware color schemes                            │
│ 4. User Interaction Handling                               │
│    ├─ Pause: Continue training, stop updates               │
│    ├─ Resume: Resume sending updates                       │
│    ├─ Stop: Break training loop, cleanup                   │
│    ├─ Speed change: Adjust update frequency                │
│    └─ Page unload: Cancel training, cleanup                │
│ 5. Error Recovery in Updates                               │
│    ├─ Invalid epoch data handling                          │
│    ├─ Chart update failures                                │
│    ├─ Memory overflow protection                           │
│    ├─ Network interruption recovery                        │
│    └─ Graceful degradation                                 │
└─────────────────────────────────────────────────────────────┘
```

This COMPLETE sequence diagram now includes EVERY detail, loop, conditional flow, error handling, and edge case that I missed in the first version. It shows the true complexity and robustness of your Linear Regression platform!
