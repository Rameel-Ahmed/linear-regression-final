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
    B->>B: Check for saved state
    B->>B: Display upload interface
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant L as CSV Loader

    U->>B: Upload CSV file
    B->>B: Parse CSV content
    B->>B: Display data preview
    B->>B: Populate column selectors
    U->>B: Select X & Y columns
    U->>B: Configure cleaning options
    U->>B: Click "Analyze Data Quality"

    B->>S: POST /api/v1/analyze-data-quality
    S->>C: analyze_data_quality()
    C->>H: read_csv_file()
    H->>C: Return DataFrame
    C->>H: analyze_data_quality()
    H->>C: Return quality report
    C->>S: Return analysis results
    S->>B: Data quality report

    U->>B: Click "Process & Clean Data"
    B->>S: POST /api/v1/process-data
    S->>C: process_data()
    C->>H: read_csv_file()
    H->>C: Return DataFrame
    C->>L: clean_data()
    L->>C: Return cleaned DataFrame
    C->>H: store_processed_data()
    C->>S: Return processing results
    S->>B: Cleaned data + statistics

    B->>B: Create data visualizations
    B->>B: Display scatter plots
    B->>B: Show statistical summary
    B->>B: Enable "Proceed to Training"



    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper

    U->>B: Click "Proceed to Training"
    B->>B: Navigate to training.html
    B->>B: Load training interface
    B->>B: Initialize charts (scatter + cost)
    B->>B: Display parameter controls

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
    B->>S: POST /api/v1/start-training
    S->>C: start_training()
    C->>H: setup_training()
    H->>M: Create LinearRegressionModel
    M->>N: Normalize training data
    M->>M: Split train/test data
    M->>G: Initialize gradient descent

    Note over M: Training Loop (Epoch by Epoch)
    loop For each epoch until convergence
        M->>G: compute_cost(theta)
        G->>M: Return current cost
        M->>G: compute_gradients(theta)
        G->>M: Return gradients
        M->>M: Update parameters:
        Note over M: theta_0 := theta_0 - alpha * grad_0
        Note over M: theta_1 := theta_1 - alpha * grad_1

        M->>M: Check convergence criteria
        M->>MC: calculate_metrics()
        MC->>M: Return RMSE, MAE, R²

        M->>H: Yield epoch data
        H->>C: Stream epoch update
        C->>S: StreamingResponse
        S->>B: Server-Sent Event

        B->>B: Update cost chart
        B->>B: Update regression line
        B->>B: Update parameter displays
        B->>B: Update performance metrics
        B->>B: Update equation display

        alt Training paused
            U->>B: Click "Pause"
            B->>S: POST /api/v1/pause-training
            S->>C: pause_training()
            C->>H: Set pause flag
            Note over M: Training loop continues but no updates sent
        end

        alt Training resumed
            U->>B: Click "Resume"
            B->>S: POST /api/v1/resume-training
            S->>C: resume_training()
            C->>H: Clear pause flag
            Note over M: Resume sending updates
        end

        alt Training stopped
            U->>B: Click "Stop"
            B->>S: POST /api/v1/stop-training
            S->>C: stop_training()
            C->>H: Set stop flag
            Note over M: Break training loop
        end
    end

    M->>M: Training complete
    M->>H: Final model summary
    H->>C: Training completion
    C->>S: Final response
    S->>B: Training results
    B->>B: Display final metrics
    B->>B: Enable "View Results" button
    participant U as User
    participant B as Browser
    participant S as Server
    participant C as Controller
    participant H as API Helper
    participant M as Linear Regression Model

    U->>B: Click "View Results"
    B->>B: Navigate to results.html
    B->>B: Load results interface
    B->>B: Display final model equation
    B->>B: Show performance metrics
    B->>B: Display sklearn comparison

    U->>B: Enter new X values for prediction
    B->>B: Validate input data
    B->>B: Calculate predictions using:
    Note over B: y = theta_0 + theta_1 * x

    B->>B: Display prediction results
    B->>B: Show confidence intervals
    B->>B: Enable export functionality

    U->>B: Export model parameters
    B->>B: Download results as JSON/CSV
