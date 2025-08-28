import { setupSidebarToggle } from "./helping_functions.js";
import { loadState, advanceStep } from "./state.js";

// Function to get current theme colors
function getThemeColors() {
  const currentTheme =
    document.documentElement.getAttribute("data-theme") || "light";
  console.log("🎨 Current theme detected:", currentTheme);

  if (currentTheme === "dark") {
    return {
      textPrimary: "#ffffff",
      textSecondary: "#e2e8f0",
      cardBg: "rgba(45, 55, 72, 0.8)",
      borderColor: "rgba(74, 85, 104, 0.3)",
    };
  } else {
    return {
      textPrimary: "#000000",
      textSecondary: "#4a5568",
      cardBg: "rgba(255, 255, 255, 0.8)",
      borderColor: "rgba(0, 0, 0, 0.1)",
    };
  }
}
const stPage = loadState();
if (!localStorage.getItem("trainingData") && stPage.trainingData) {
  localStorage.setItem("trainingData", JSON.stringify(stPage.trainingData));
}

// Global variables for collapsible summary
let summaryExpanded = false;

// Function to toggle summary section
function toggleSummary() {
  const summaryContent = document.getElementById("summaryContent");
  const toggleIcon = document.getElementById("summaryToggleIcon");

  summaryExpanded = !summaryExpanded;

  if (summaryExpanded) {
    summaryContent.classList.remove("collapsed");
    toggleIcon.textContent = "↓";
    toggleIcon.classList.remove("rotated");
  } else {
    summaryContent.classList.add("collapsed");
    toggleIcon.textContent = "→";
    toggleIcon.classList.add("rotated");
  }
}

// Simple function to toggle parameters panel
function toggleSimpleParams() {
  const paramsPanel = document.getElementById("simpleParamsPanel");
  const paramsBtn = document.getElementById("paramsToggleBtn");

  if (paramsPanel.classList.contains("open")) {
    // Close panel
    paramsPanel.classList.remove("open");
    paramsBtn.textContent = "⚙️ Params";
    console.log("🔄 Parameters panel closed");
  } else {
    // Open panel
    paramsPanel.classList.add("open");
    paramsBtn.textContent = "✕ Close";

    // Sync values from main form
    syncSimpleValues();

    console.log("✅ Parameters panel opened");
  }
}

// Sync values from main form to simple panel
function syncSimpleValues() {
  const mainLR = document.getElementById("learningRate").value;
  const mainEpochs = document.getElementById("epochs").value;
  const mainEarlyStop = document.getElementById("earlyStop").checked;

  document.getElementById("simpleLR").value = mainLR;
  document.getElementById("simpleLRInput").value = mainLR;
  document.getElementById("simpleEpochs").value = mainEpochs;
  document.getElementById("simpleEpochsInput").value = mainEpochs;
  document.getElementById("simpleEarlyStop").checked = mainEarlyStop;

  // Update mode buttons
  const activeMode = document.querySelector(".mode-btn.active");
  if (activeMode) {
    document
      .querySelectorAll(".simple-mode-btn")
      .forEach((btn) => btn.classList.remove("active"));
    const simpleBtn = document.querySelector(
      `.simple-mode-btn[onclick*="${activeMode.dataset.mode}"]`
    );
    if (simpleBtn) simpleBtn.classList.add("active");
  }
}

// Set training mode in simple panel
function setSimpleMode(mode) {
  // Update simple panel buttons
  document
    .querySelectorAll(".simple-mode-btn")
    .forEach((btn) => btn.classList.remove("active"));
  const activeBtn = document.querySelector(
    `.simple-mode-btn[onclick*="${mode}"]`
  );
  if (activeBtn) activeBtn.classList.add("active");

  // Update main form mode
  document
    .querySelectorAll(".mode-btn")
    .forEach((btn) => btn.classList.remove("active"));
  const mainBtn = document.querySelector(`.mode-btn[data-mode="${mode}"]`);
  if (mainBtn) mainBtn.classList.add("active");

  // Set the training mode
  setTrainingMode(mode);

  console.log("✅ Simple panel training mode set to:", mode);
}

// Function to sync sidebar values with main form
function syncSidebarValues() {
  // Sync from main form to sidebar
  const mainLearningRate = document.getElementById("learningRate").value;
  const mainEpochs = document.getElementById("epochs").value;
  const mainTolerance = document.getElementById("tolerance").value;
  const mainTrainSplit = document.getElementById("trainSplit").value;
  const mainTrainingSpeed = document.getElementById("trainingSpeed").value;
  const mainEarlyStop = document.getElementById("earlyStop").checked;

  // Update sidebar inputs
  document.getElementById("sidebarLearningRate").value = mainLearningRate;
  document.getElementById("sidebarLearningRateInput").value = mainLearningRate;
  document.getElementById("sidebarEpochs").value = mainEpochs;
  document.getElementById("sidebarEpochsInput").value = mainEpochs;
  document.getElementById("sidebarTolerance").value = mainTolerance;
  document.getElementById("sidebarToleranceInput").value = mainTolerance;
  document.getElementById("sidebarTrainSplit").value = mainTrainSplit;
  document.getElementById("sidebarTrainSplitInput").value = mainTrainSplit;
  document.getElementById("sidebarTrainingSpeed").value = mainTrainingSpeed;
  document.getElementById("sidebarTrainingSpeedInput").value =
    mainTrainingSpeed;
  document.getElementById("sidebarEarlyStop").checked = mainEarlyStop;

  // Update sidebar mode buttons
  const activeMode = document.querySelector(".mode-btn.active");
  if (activeMode) {
    document
      .querySelectorAll("#paramsPanelSidebar .mode-btn")
      .forEach((btn) => btn.classList.remove("active"));
    const sidebarBtn = document.querySelector(
      `#paramsPanelSidebar .mode-btn[data-mode="${activeMode.dataset.mode}"]`
    );
    if (sidebarBtn) sidebarBtn.classList.add("active");
  }

  console.log("🔄 Sidebar values synced with main form");
}

// Function to set training mode in sidebar
function setSidebarTrainingMode(mode) {
  // Update sidebar mode buttons
  document
    .querySelectorAll("#paramsPanelSidebar .mode-btn")
    .forEach((btn) => btn.classList.remove("active"));
  const activeBtn = document.querySelector(
    `#paramsPanelSidebar .mode-btn[data-mode="${mode}"]`
  );
  if (activeBtn) activeBtn.classList.add("active");

  // Also update main form mode
  document
    .querySelectorAll(".mode-btn")
    .forEach((btn) => btn.classList.remove("active"));
  const mainBtn = document.querySelector(`.mode-btn[data-mode="${mode}"]`);
  if (mainBtn) mainBtn.classList.add("active");

  // Set the training mode
  setTrainingMode(mode);

  console.log("✅ Sidebar training mode set to:", mode);
}

// Function to setup sidebar input synchronization
function setupSidebarSync() {
  const sidebarInputs = [
    "sidebarLearningRate",
    "sidebarLearningRateInput",
    "sidebarEpochs",
    "sidebarEpochsInput",
    "sidebarTolerance",
    "sidebarToleranceInput",
    "sidebarTrainSplit",
    "sidebarTrainSplitInput",
    "sidebarTrainingSpeed",
    "sidebarTrainingSpeedInput",
    "sidebarEarlyStop",
  ];

  sidebarInputs.forEach((inputId) => {
    const element = document.getElementById(inputId);
    if (element) {
      if (element.type === "checkbox") {
        element.addEventListener("change", function () {
          // Sync to main form
          const mainId = inputId.replace("sidebar", "").toLowerCase();
          const mainElement = document.getElementById(mainId);
          if (mainElement) {
            mainElement.checked = this.checked;
            // Trigger parameter change check
            checkAndSwitchToCustom();
          }
        });
      } else {
        element.addEventListener("input", function () {
          // Sync to main form
          const mainId = inputId.replace("sidebar", "").toLowerCase();
          const mainElement = document.getElementById(mainId);
          if (mainElement) {
            mainElement.value = this.value;
            // Trigger parameter change check
            checkAndSwitchToCustom();
          }
        });
      }
    }
  });

  console.log("✅ Sidebar input synchronization setup complete");
}

// Make toggleSummary available globally
window.toggleSummary = toggleSummary;

// Make simple functions available globally
window.toggleSimpleParams = toggleSimpleParams;
window.setSimpleMode = setSimpleMode;

// Global variables
let trainingData = null;
let scatterChart = null;
let costChart = null;
let isTraining = false;
let isPaused = false;
let trainingId = null;
let isExpanded = false;

// Initialize
async function loadTrainingData() {
  if (window.__restoredFromCache) {
    console.log("🔄 Skipping normal load - using cached data");
    return;
  }
  try {
    console.log("🔄 Loading training data...");

    // Get data from localStorage (set by first page)
    const trainingDataStr = localStorage.getItem("trainingData");

    if (!trainingDataStr) {
      console.error("❌ No training data found in localStorage");
      alert("No training data found. Please process data first.");
      window.location.href = "/";
      return;
    }

    trainingData = JSON.parse(trainingDataStr);
    console.log("📊 Training data loaded:", trainingData);
    console.log("📋 Training data keys:", Object.keys(trainingData));

    // Debug data structure
    if (trainingData.cleaned_data) {
      console.log("📊 Cleaned data structure:", {
        length: trainingData.cleaned_data.length,
        columns: Object.keys(trainingData.cleaned_data[0] || {}),
        xColumn: trainingData.xColumn,
        yColumn: trainingData.yColumn,
      });
    }

    // Add error handling for each function
    try {
      updateDataSummary();
      console.log("✅ Summary updated successfully");
    } catch (e) {
      console.error("❌ Error updating summary:", e);
    }

    // Initialize summary in collapsed state
    const summaryContent = document.getElementById("summaryContent");
    const toggleIcon = document.getElementById("summaryToggleIcon");
    if (summaryContent && toggleIcon) {
      summaryContent.classList.add("collapsed");
      toggleIcon.textContent = "→";
      toggleIcon.classList.add("rotated");
      console.log("📊 Summary initialized in collapsed state");
    }

    try {
      createDataVisualizations();
      console.log("✅ Visualizations created successfully");
    } catch (e) {
      console.error("❌ Error creating visualizations:", e);
    }

    // >>> Restore final charts if we already have results in state
    // REMOVED: This was causing duplicate restore logic

    try {
      updateTrainingStatus("Data loaded and ready for training", "✅");
      console.log("✅ Status updated successfully");
    } catch (e) {
      console.error("❌ Error updating status:", e);
    }
  } catch (error) {
    console.error("❌ Failed to load training data:", error);
    alert("Failed to load training data. Please try again.");
    window.location.href = "/";
  }
}

// Auto-load when page loads
document.addEventListener("DOMContentLoaded", function () {
  console.log("🚀 Page loaded, initializing...");
  initializeTheme();
  loadTrainingData();
  setupEventListeners(); // Add this line to connect button events
  setupSidebarToggle(); // Add this line to initialize sidebar toggle

  // Ensure charts are created when page loads
  setTimeout(() => {
    if (!window.costChart) {
      console.log("🔄 Creating cost chart on page load...");
      createCostChart();
    }
    if (!window.scatterChart) {
      console.log("🔄 Creating scatter chart on page load...");
      createScatterPlot();
    }

    // Initialize performance metrics if data is available
    if (trainingData && trainingData.cleaned_data) {
      console.log(
        "🔄 Performance metrics will be initialized when charts are shown"
      );
    }
  }, 1000); // Small delay to ensure DOM is fully ready

  // === Restore cached final view === (moved here)
  const st = loadState();
  if (st.step === 3 && st.resultsData) {
    console.log("🔄 Restoring cached training results");

    // Prepare data for scatter/cost charts
    const xArr = st.trainingData?.statistics?.x_data || [];
    const yArr = st.trainingData?.statistics?.y_data || [];
    const xCol = st.trainingData?.columns?.x_column || "X";
    const yCol = st.trainingData?.columns?.y_column || "Y";
    const csvLike = xArr.map((xv, i) => ({ [xCol]: xv, [yCol]: yArr[i] }));

    // Draw visualizations once
    createScatterPlot(csvLike, xCol, yCol);
    createCostChart();

    // If cost history saved, repopulate chart
    // Clear existing data first
    if (window.costChart) {
      window.costChart.data.labels = [];
      window.costChart.data.datasets[0].data = [];
      window.costChart.update();
    }

    if (st.resultsData.cost_history?.length) {
      window.costChart.data.labels = st.resultsData.cost_history.map(
        (p) => p[0]
      );
      window.costChart.data.datasets[0].data = st.resultsData.cost_history.map(
        (p) => p[1]
      );
      window.costChart.update();
    }

    // Fix epoch count - use training params as fallback
    const tp = st.trainingParams || {};
    const epochCount =
      st.resultsData.total_epochs ||
      st.resultsData.epoch ||
      tp.epochs ||
      st.resultsData.cost_history?.length ||
      1;

    // Restore early stopping toggle state
    if (tp.early_stopping !== undefined) {
      const earlyStopToggle = document.getElementById("earlyStop");
      if (earlyStopToggle) {
        earlyStopToggle.checked = tp.early_stopping;
        console.log("✅ Early stopping toggle restored:", tp.early_stopping);
      }
    }

    const costVal = st.resultsData.final_cost || st.resultsData.test_mse || 0;

    const viewData = {
      theta0: st.resultsData.final_theta0 || 0,
      theta1: st.resultsData.final_theta1 || 0,
      rmse: st.resultsData.final_rmse || 0,
      mae: st.resultsData.final_mae || 0,
      r2: st.resultsData.final_r2 || 0,
      cost: costVal,
      epoch: epochCount,
      max_epochs: epochCount,
      is_complete: true,
    };

    updateTrainingDisplay(viewData);
    // updateCostChart(viewData);  // REMOVED: already populated chart manually above
    updatePerformanceMetrics(viewData);
    updateProgressBar(viewData);

    // Force progress bar text and fill to 100%
    const progFill = document.getElementById("progressFill");
    const progText = document.getElementById("progressText");
    if (progFill) progFill.style.width = "100%";
    if (progText) progText.textContent = `Epoch ${epochCount}/${epochCount}`;

    updateStatus("Training complete (cached)");
  }
});

function initializeTheme() {
  console.log("🎨 Initializing theme...");
  const themeBtn = document.getElementById("themeBtn");
  const savedTheme = localStorage.getItem("theme") || "light";

  console.log("🌙 Saved theme:", savedTheme);
  console.log("🔘 Theme button found:", !!themeBtn);

  document.documentElement.setAttribute("data-theme", savedTheme);
  if (themeBtn) {
    themeBtn.textContent = savedTheme === "light" ? "🌙" : "☀️";
    themeBtn.onclick = function () {
      const current =
        document.documentElement.getAttribute("data-theme") || "light";
      const newTheme = current === "light" ? "dark" : "light";
      console.log("🔄 Switching theme from", current, "to", newTheme);

      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
      this.textContent = newTheme === "light" ? "🌙" : "☀️";

      console.log("✅ Theme updated to:", newTheme);
      console.log(
        "🎨 HTML data-theme attribute:",
        document.documentElement.getAttribute("data-theme")
      );

      // Update chart colors when theme changes
      updateChartColors();
    };
  } else {
    console.error("❌ Theme button not found!");
  }
}

function updateDataSummary() {
  try {
    if (!trainingData) {
      console.log("❌ No training data available for summary");
      return;
    }

    console.log("📊 Updating data summary with:", trainingData);

    // Update X and Y variable names
    const xVariableElement = document.getElementById("xVariable");
    const yVariableElement = document.getElementById("yVariable");

    if (xVariableElement && trainingData.columns?.x_column) {
      xVariableElement.textContent = trainingData.columns.x_column;
    }

    if (yVariableElement && trainingData.columns?.y_column) {
      yVariableElement.textContent = trainingData.columns.y_column;
    }

    // Update statistics
    const xMeanElement = document.getElementById("xMean");
    const xStdElement = document.getElementById("xStd");
    const yMeanElement = document.getElementById("yMean");
    const yStdElement = document.getElementById("yStd");

    if (xMeanElement && trainingData.statistics?.x_mean !== undefined) {
      xMeanElement.textContent = trainingData.statistics.x_mean.toFixed(4);
    }

    if (xStdElement && trainingData.statistics?.x_std !== undefined) {
      xStdElement.textContent = trainingData.statistics.x_std.toFixed(4);
    }

    if (yMeanElement && trainingData.statistics?.y_mean !== undefined) {
      yMeanElement.textContent = trainingData.statistics.y_mean.toFixed(4);
    }

    if (yStdElement && trainingData.statistics?.y_std !== undefined) {
      yStdElement.textContent = trainingData.statistics.y_std.toFixed(4);
    }

    // Update row counts
    const originalRowsElement = document.getElementById("originalRows");
    const cleanedRowsElement = document.getElementById("cleanedRows");
    const rowsRemovedElement = document.getElementById("rowsRemoved");

    if (
      originalRowsElement &&
      trainingData.file_info?.original_shape?.[0] !== undefined
    ) {
      originalRowsElement.textContent =
        trainingData.file_info.original_shape[0].toLocaleString();
    }

    if (
      cleanedRowsElement &&
      trainingData.file_info?.cleaned_shape?.[0] !== undefined
    ) {
      cleanedRowsElement.textContent =
        trainingData.file_info.cleaned_shape[0].toLocaleString();
    }

    if (
      rowsRemovedElement &&
      trainingData.cleaning_summary?.samples_removed !== undefined
    ) {
      rowsRemovedElement.textContent =
        trainingData.cleaning_summary.samples_removed.toLocaleString();
    }

    console.log("✅ Data summary updated successfully");
  } catch (error) {
    console.error("❌ Error updating summary:", error);
  }
}

function setupEventListeners() {
  // Slider synchronization
  syncSliders();

  // Train split slider and input synchronization
  const trainSplitSlider = document.getElementById("trainSplit");
  const trainSplitValue = document.getElementById("trainSplitInput");

  if (trainSplitSlider && trainSplitValue) {
    trainSplitSlider.addEventListener("input", function () {
      trainSplitValue.value = this.value;
    });

    trainSplitValue.addEventListener("input", function () {
      const value = this.value;
      if (value >= 0.1 && value <= 1.0) {
        trainSplitSlider.value = value;
      }
    });
  }

  // Training speed slider and input synchronization
  const trainingSpeedSlider = document.getElementById("trainingSpeed");
  const trainingSpeedValue = document.getElementById("trainingSpeedInput");

  if (trainingSpeedSlider && trainingSpeedValue) {
    trainingSpeedSlider.addEventListener("input", function () {
      trainingSpeedValue.value = this.value;
    });

    trainingSpeedValue.addEventListener("input", function () {
      const value = this.value;
      if (value >= 0.1 && value <= 3.0) {
        trainingSpeedSlider.value = value;
      }
    });
  }

  // Removed old updateSpeed controls - now using single trainingSpeed control

  // Mode buttons
  document.querySelectorAll(".mode-btn").forEach((btn) => {
    btn.onclick = function () {
      document
        .querySelectorAll(".mode-btn")
        .forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
      setTrainingMode(this.dataset.mode);
    };
  });

  // Set Accurate mode as active by default
  const accurateBtn = document.querySelector('.mode-btn[data-mode="accurate"]');
  if (accurateBtn) {
    accurateBtn.classList.add("active");
    console.log("✅ Accurate mode set as default");

    // Also set the default values to match Accurate preset
    setTrainingMode("accurate");
  }

  // Initialize early stopping toggle
  const earlyStopToggle = document.getElementById("earlyStop");
  if (earlyStopToggle) {
    // Set default state (unchecked)
    earlyStopToggle.checked = false;
    console.log("✅ Early stopping toggle initialized");
  }

  // Control buttons
  document.getElementById("startBtn").onclick = startTraining;
  document.getElementById("pauseBtn").onclick = pauseTraining;
  document.getElementById("resumeBtn").onclick = resumeTraining;
  document.getElementById("stopBtn").onclick = stopTraining;
  document.getElementById("restartBtn").onclick = restartTraining;

  // View Results button - now directly clickable
  const viewResultsBtn = document.getElementById("viewResults");
  if (viewResultsBtn) {
    console.log("✅ View Results button found and ready");
  } else {
    console.error("❌ View Results button not found");
  }

  // Expand/Close buttons
  const expandBtn = document.getElementById("expandChartsBtn");
  const closeExpandBtn = document.getElementById("closeExpandBtn");

  if (expandBtn) {
    expandBtn.onclick = expandCharts;
    console.log("✅ Expand button connected");
  }

  if (closeExpandBtn) {
    closeExpandBtn.onclick = closeExpandedView;
    console.log("✅ Close expand button connected");
  }
}

function syncSliders() {
  // Learning Rate
  const lr = document.getElementById("learningRate");
  const lrInput = document.getElementById("learningRateInput");
  lr.oninput = () => (lrInput.value = lr.value);
  lrInput.oninput = () => {
    const value = parseFloat(lrInput.value);
    if (value < 0.001) lrInput.value = 0.001;
    if (value > 1) lrInput.value = 1;
    lr.value = lrInput.value;
  };

  // Epochs
  const epochs = document.getElementById("epochs");
  const epochsInput = document.getElementById("epochsInput");
  epochs.oninput = () => (epochsInput.value = epochs.value);
  epochsInput.oninput = () => {
    const value = parseInt(epochsInput.value);
    if (value < 5) epochsInput.value = 5;
    if (value > 200) epochsInput.value = 200;
    epochs.value = epochsInput.value;
  };

  // Tolerance
  const tolerance = document.getElementById("tolerance");
  const toleranceInput = document.getElementById("toleranceInput");
  tolerance.oninput = () => (toleranceInput.value = tolerance.value);
  toleranceInput.oninput = () => {
    const value = parseFloat(toleranceInput.value);
    if (value < 0) toleranceInput.value = 0;
    if (value > 0.01) toleranceInput.value = 0.01;
    tolerance.value = toleranceInput.value;
  };

  // Train Split
  const trainSplit = document.getElementById("trainSplit");
  const trainSplitInput = document.getElementById("trainSplitInput");
  if (trainSplit && trainSplitInput) {
    trainSplit.oninput = () => (trainSplitInput.value = trainSplit.value);
    trainSplitInput.oninput = () => {
      const value = parseFloat(trainSplitInput.value);
      if (value < 0.3) trainSplitInput.value = 0.3;
      if (value > 0.99) trainSplitInput.value = 0.99;
      trainSplit.value = trainSplitInput.value;
    };
  }

  // Training Speed
  const trainingSpeed = document.getElementById("trainingSpeed");
  const trainingSpeedInput = document.getElementById("trainingSpeedInput");
  if (trainingSpeed && trainingSpeedInput) {
    trainingSpeed.oninput = () =>
      (trainingSpeedInput.value = trainingSpeed.value);
    trainingSpeedInput.oninput = () => {
      const value = parseFloat(trainingSpeedInput.value);
      if (value < 0.2) trainingSpeedInput.value = 0.2;
      if (value > 1.0) trainingSpeedInput.value = 1.0;
      trainingSpeed.value = trainingSpeedInput.value;
    };
  }

  // Monitor parameter changes and auto-switch to Custom mode
  monitorParameterChanges();
}

function setTrainingMode(mode) {
  const presets = {
    accurate: {
      lr: 0.3,
      epochs: 150,
      tolerance: 0.00001,
      earlyStop: true,
      trainSplit: 0.99,
      trainingSpeed: 0.4,
    },
    custom: null,
  };

  if (presets[mode]) {
    // Set flag to prevent auto-switch during preset application
    isSettingPreset = true;

    document.getElementById("learningRate").value = presets[mode].lr;
    document.getElementById("learningRateInput").value = presets[mode].lr;
    document.getElementById("epochs").value = presets[mode].epochs;
    document.getElementById("epochsInput").value = presets[mode].epochs;
    document.getElementById("tolerance").value = presets[mode].tolerance;
    document.getElementById("toleranceInput").value = presets[mode].tolerance;
    document.getElementById("trainSplit").value = presets[mode].trainSplit;
    document.getElementById("trainSplitInput").value = presets[mode].trainSplit;
    document.getElementById("earlyStop").checked = presets[mode].earlyStop;
    document.getElementById("trainingSpeed").value =
      presets[mode].trainingSpeed;
    document.getElementById("trainingSpeedInput").value =
      presets[mode].trainingSpeed;

    // Reset flag after a short delay to allow parameter monitoring to resume
    setTimeout(() => {
      isSettingPreset = false;
      console.log("🔄 Parameter monitoring resumed after preset application");
    }, 200);
  }
}

// Global flag to prevent auto-switch during preset application
let isSettingPreset = false;

// Function to monitor parameter changes and auto-switch to Custom mode
function monitorParameterChanges() {
  const parameters = [
    "learningRate",
    "learningRateInput",
    "epochs",
    "epochsInput",
    "tolerance",
    "toleranceInput",
    "trainSplit",
    "trainSplitInput",
    "trainingSpeed",
    "trainingSpeedInput",
    "earlyStop",
  ];

  parameters.forEach((paramId) => {
    const element = document.getElementById(paramId);
    if (element) {
      if (element.type === "checkbox") {
        element.addEventListener("change", checkAndSwitchToCustom);
      } else {
        element.addEventListener("input", checkAndSwitchToCustom);
      }
    }
  });
}

// Function to check if parameters match Accurate preset and switch to Custom if needed
function checkAndSwitchToCustom() {
  // Don't auto-switch if we're currently setting preset values
  if (isSettingPreset) {
    console.log("⏸️ Skipping auto-switch check (preset being applied)");
    return;
  }

  const accuratePreset = {
    lr: 0.3,
    epochs: 150,
    tolerance: 0.00001,
    earlyStop: true,
    trainSplit: 0.99,
    trainingSpeed: 0.4,
  };

  const currentValues = {
    lr: parseFloat(document.getElementById("learningRate").value),
    epochs: parseInt(document.getElementById("epochs").value),
    tolerance: parseFloat(document.getElementById("tolerance").value),
    earlyStop: document.getElementById("earlyStop").checked,
    trainSplit: parseFloat(document.getElementById("trainSplit").value),
    trainingSpeed: parseFloat(document.getElementById("trainingSpeed").value),
  };

  // Check if current values match Accurate preset
  const isAccurate =
    Math.abs(currentValues.lr - accuratePreset.lr) < 0.001 &&
    currentValues.epochs === accuratePreset.epochs &&
    Math.abs(currentValues.tolerance - accuratePreset.tolerance) < 0.000001 &&
    currentValues.earlyStop === accuratePreset.earlyStop &&
    Math.abs(currentValues.trainSplit - accuratePreset.trainSplit) < 0.001 &&
    Math.abs(currentValues.trainingSpeed - accuratePreset.trainingSpeed) <
      0.001;

  // Get current active mode
  const activeMode = document.querySelector(".mode-btn.active");

  if (!isAccurate && activeMode && activeMode.dataset.mode === "accurate") {
    // Switch to Custom mode
    const customBtn = document.querySelector('.mode-btn[data-mode="custom"]');
    if (customBtn) {
      activeMode.classList.remove("active");
      customBtn.classList.add("active");
      console.log("🔄 Auto-switched to Custom mode due to parameter change");
    }
  } else if (isAccurate && activeMode && activeMode.dataset.mode === "custom") {
    // Switch back to Accurate mode
    const accurateBtn = document.querySelector(
      '.mode-btn[data-mode="accurate"]'
    );
    if (accurateBtn) {
      activeMode.classList.remove("active");
      accurateBtn.classList.add("active");
      console.log("✅ Auto-switched back to Accurate mode");
    }
  }
}

function setupCharts() {
  createScatterChart();
  createCostChart();
}

function createScatterChart() {
  const ctx = document.getElementById("scatterChart").getContext("2d");

  // Get clean data
  const validData = trainingData.csvData.filter(
    (row) =>
      typeof row[trainingData.xColumn] === "number" &&
      typeof row[trainingData.yColumn] === "number"
  );

  const scatterData = validData.map((row) => ({
    x: row[trainingData.xColumn],
    y: row[trainingData.yColumn],
  }));

  scatterChart = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: "Data Points",
          data: scatterData,
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(59, 130, 246, 1)",
          pointRadius: 3,
        },
        {
          label: "Regression Line",
          data: [],
          borderColor: "rgba(239, 68, 68, 1)",
          backgroundColor: "transparent",
          borderWidth: 3,
          type: "line",
          pointRadius: 0,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false },
      scales: {
        x: {
          title: {
            display: true,
            text: trainingData.xColumn,
            font: { weight: "bold" },
          },
        },
        y: {
          title: {
            display: true,
            text: trainingData.yColumn,
            font: { weight: "bold" },
          },
        },
      },
      plugins: {
        title: {
          display: true,
          text: "Data & Regression Line",
          font: { size: 16, weight: "bold" },
        },
        legend: { position: "bottom" },
      },
    },
  });
}

// Update createDataVisualizations to use the stored data
function createDataVisualizations() {
  if (!trainingData) {
    console.log("❌ No training data available");
    return;
  }

  try {
    console.log("🔄 Creating data visualizations...");
    console.log("📊 Training data structure:", trainingData);

    const xData = trainingData.statistics.x_data;
    const yData = trainingData.statistics.y_data;
    const xColumn = trainingData.columns.x_column;
    const yColumn = trainingData.columns.y_column;

    console.log("📈 Data for plotting:", {
      xData: xData ? xData.length : "undefined",
      yData: yData ? yData.length : "undefined",
      xColumn,
      yColumn,
    });

    if (xData && yData && xData.length > 0 && yData.length > 0) {
      // Create data array in the same format as script.js
      const validData = xData.map((x, i) => ({
        [xColumn]: x,
        [yColumn]: yData[i],
      }));

      console.log("✅ Valid data created:", {
        length: validData.length,
        sample: validData.slice(0, 3),
      });

      // Create plots using the same functions as script.js
      createScatterPlot(validData, xColumn, yColumn);
      createCostChart(); // Also create the cost chart

      console.log("📊 Charts created with stored data");
    } else {
      console.error("❌ Invalid data for plotting:", {
        xData,
        yData,
        xColumn,
        yColumn,
      });
    }
  } catch (error) {
    console.error("❌ Error creating visualizations:", error);
  }
}

// Use the exact same plotting functions as script.js
function createScatterPlot(data, xCol, yCol) {
  const ctx = document.getElementById("scatterChart");
  if (!ctx) return;

  if (
    window.scatterChart &&
    typeof window.scatterChart.destroy === "function"
  ) {
    window.scatterChart.destroy();
  }

  const chartData = data.map((row) => ({ x: row[xCol], y: row[yCol] }));
  const colors = getThemeColors();

  console.log("🎨 Scatter plot using colors:", colors);

  window.scatterChart = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: `${yCol} vs ${xCol}`,
          data: chartData,
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(59, 130, 246, 1)",
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: xCol,
            color: colors.textPrimary,
            font: { weight: "bold" },
          },
          ticks: { color: colors.textPrimary },
          grid: { color: colors.borderColor },
        },
        y: {
          title: {
            display: true,
            text: yCol,
            color: colors.textPrimary,
            font: { weight: "bold" },
          },
          ticks: { color: colors.textPrimary },
          grid: { color: colors.borderColor },
        },
      },
      plugins: {
        title: {
          display: true,
          text: "Data & Regression Line",
          color: colors.textPrimary,
          font: { size: 16, weight: "bold" },
        },
        legend: { display: false },
      },
    },
  });
}

function createCostChart() {
  console.log("🔄 Creating cost chart...");

  const ctx = document.getElementById("costChart");
  if (!ctx) {
    console.error("❌ Cost chart canvas not found!");
    return;
  }

  console.log("✅ Found cost chart canvas");

  // Destroy existing chart if it exists
  if (window.costChart && typeof window.costChart.destroy === "function") {
    window.costChart.destroy();
    console.log("🗑️ Destroyed existing cost chart");
  }

  try {
    const colors = getThemeColors();
    console.log("🎨 Cost chart using colors:", colors);
    window.costChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Training Cost",
            data: [],
            borderColor: "rgba(16, 185, 129, 1)",
            backgroundColor: "rgba(16, 185, 129, 0.1)",
            borderWidth: 2,
            fill: true,
            tension: 0.1,
            pointRadius: 2,
            pointHoverRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false },
        animation: {
          duration: 300, // Enable animations for user to see plotting
          easing: "easeOutQuart",
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Epochs",
              color: colors.textPrimary,
              font: { weight: "bold" },
            },
            ticks: { color: colors.textPrimary },
            grid: { color: colors.borderColor },
          },
          y: {
            title: {
              display: true,
              text: "Cost Function",
              color: colors.textPrimary,
              font: { weight: "bold" },
            },
            ticks: { color: colors.textPrimary },
            beginAtZero: false,
            grid: { color: colors.borderColor },
          },
        },
        plugins: {
          title: {
            display: true,
            text: "Training Cost Over Time",
            color: colors.textPrimary,
            font: { size: 16, weight: "bold" },
          },
          legend: { display: false },
          tooltip: {
            mode: "index",
            intersect: false,
            callbacks: {
              title: function (context) {
                return `Epoch ${context[0].label}`;
              },
              label: function (context) {
                return `Cost: ${context.parsed.y.toFixed(6)}`;
              },
            },
          },
        },
      },
    });
    console.log("✅ Cost chart created successfully");
  } catch (error) {
    console.error("❌ Error creating cost chart:", error);
  }
}

// Function to update training metrics dashboard

function startTraining() {
  if (isTraining) return;

  // Get training parameters
  const learningRate = parseFloat(
    document.getElementById("learningRate").value
  );
  const epochs = parseInt(document.getElementById("epochs").value);
  const tolerance = parseFloat(document.getElementById("tolerance").value);
  const earlyStopping = document.getElementById("earlyStop").checked;
  const trainingSpeed = parseFloat(
    document.getElementById("trainingSpeed").value
  );
  const trainSplit = parseFloat(document.getElementById("trainSplit").value);

  // Validate parameters with proper range checking
  if (learningRate < 0.001 || learningRate > 1) {
    alert("Learning Rate must be between 0.001 and 1");
    return;
  }
  if (epochs < 5 || epochs > 200) {
    alert("Max Epochs must be between 5 and 200");
    return;
  }
  if (tolerance < 0 || tolerance > 0.01) {
    alert("Convergence Tolerance must be between 0 and 0.01");
    return;
  }
  if (trainSplit < 0.3 || trainSplit > 0.99) {
    alert("Train/Test Split must be between 0.3 and 0.99");
    return;
  }
  if (trainingSpeed < 0.2 || trainingSpeed > 1.0) {
    alert("Training Speed must be between 0.2 and 1.0");
    return;
  }

  console.log("🚀 Starting training with parameters:", {
    learningRate,
    epochs,
    tolerance,
    earlyStopping,
    trainingSpeed,
    trainSplit,
  });

  // Ensure cost chart is ready for training
  if (!window.costChart) {
    console.log("🔄 Cost chart not found, creating it...");
    createCostChart();
  }

  // Ensure cost chart container is visible and active
  const costContainer = document.getElementById("costContainer");
  if (costContainer) {
    costContainer.style.display = "block";
    console.log("✅ Cost chart container made visible");

    // Also show the cost chart tab as active
    const costTab = document.querySelector("[onclick=\"showChart('cost')\"]");
    if (costTab) {
      document
        .querySelectorAll(".tab-btn")
        .forEach((btn) => btn.classList.remove("active"));
      costTab.classList.add("active");
      console.log("✅ Cost chart tab activated");
    }
  }

  // Cancel any existing animations before starting new training
  cancelAllAnimations();

  // Initialize animation variables for smooth transitions
  window.currentTheta0 = 0;
  window.currentTheta1 = 0;
  console.log("🎬 Animation variables initialized");

  // Clear previous training data from cost chart
  if (window.costChart && typeof window.costChart.data !== "undefined") {
    window.costChart.data.labels = [];
    window.costChart.data.datasets[0].data = [];
    window.costChart.update("none");
    console.log("🗑️ Cost chart cleared for new training");

    // Force chart to redraw with empty data
    setTimeout(() => {
      if (window.costChart) {
        window.costChart.update("none");
        console.log("🔄 Cost chart redrawn with empty data");
      }
    }, 100);
  }

  // Store training parameters in localStorage for next page
  const trainingParams = {
    learning_rate: learningRate,
    epochs: epochs,
    tolerance: tolerance,
    early_stopping: earlyStopping,
    training_speed: trainingSpeed,
    train_split: trainSplit,
    timestamp: new Date().toISOString(),
    x_column: trainingData?.columns?.x_column || "X",
    y_column: trainingData?.columns?.y_column || "Y",
  };

  localStorage.setItem("trainingParams", JSON.stringify(trainingParams));
  console.log("💾 Training parameters stored in localStorage:", trainingParams);

  // Create form data
  const formData = new FormData();
  formData.append("learning_rate", learningRate);
  formData.append("epochs", epochs);
  formData.append("tolerance", tolerance);
  formData.append("early_stopping", earlyStopping);
  formData.append("training_speed", trainingSpeed);
  formData.append("train_split", trainSplit);

  // Show equation display when training starts
  const equationDisplay = document.getElementById("equationDisplay");
  if (equationDisplay) {
    equationDisplay.style.display = "block";
    console.log("📊 Equation display shown");
  }

  // Auto-expand charts when training starts
  if (!isExpanded) {
    expandCharts();
    console.log("📈 Auto-expanded charts for training");
  }

  // Start streaming training
  startStreamingTraining(formData);

  // Update initial training status
  const trainingStatus = document.getElementById("trainingStatus");
  if (trainingStatus) {
    trainingStatus.textContent = "Starting training...";
  }
}

async function startStreamingTraining(formData) {
  try {
    console.log("📡 Starting streaming training...");

    // Update UI to show training is starting
    isTraining = true;
    isPaused = false;
    updateControlButtons();
    updateStatus("Starting training...");

    // Send POST request to start training
    const response = await fetch("/api/v1/start-training", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log("✅ Training started, beginning streaming...");
    updateStatus("Training in progress...");

    // Handle streaming response with speed control
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Removed: No longer needed with backend control
    let trainingSpeed = parseFloat(
      document.getElementById("trainingSpeed").value
    );

    // Speed control is now handled by backend

    // Set up page unload handler to stop training
    const handlePageUnload = () => {
      if (isTraining) {
        console.log("🛑 Page unloading - stopping training");
        fetch("/api/v1/stop-training", { method: "POST" }).catch(() => {});
      }
    };
    window.addEventListener("beforeunload", handlePageUnload);

    // Set up speed display updates
    const speedSlider = document.getElementById("trainingSpeed");
    const speedInput = document.getElementById("trainingSpeedInput");

    const updateSpeedDisplay = () => {
      trainingSpeed = parseFloat(speedSlider.value);
      if (speedInput) speedInput.value = trainingSpeed;

      // Update speed display
      const currentSpeedDisplay = document.getElementById("currentSpeed");
      if (currentSpeedDisplay) {
        let speedText = "";
        if (trainingSpeed >= 0.8) {
          speedText = "⚡ Speed 1.0 (Fast)";
        } else if (trainingSpeed >= 0.6) {
          speedText = "🚀 Speed 0.8 (Fast-Medium)";
        } else if (trainingSpeed >= 0.4) {
          speedText = "🐌 Speed 0.6 (Medium)";
        } else if (trainingSpeed >= 0.2) {
          speedText = "🐌 Speed 0.4 (Slow)";
        } else {
          speedText = "🐌 Speed 0.2 (Very Slow)";
        }
        currentSpeedDisplay.textContent = speedText;
      }
      console.log("⚡ Speed updated to:", trainingSpeed);
    };

    speedSlider.addEventListener("input", updateSpeedDisplay);
    if (speedInput) {
      speedInput.addEventListener("input", () => {
        const value = parseFloat(speedInput.value);
        if (value >= 0.2 && value <= 1.0) {
          // Snap to nearest valid step (0.2, 0.4, 0.6, 0.8, 1.0)
          const snappedValue = Math.round(value * 5) / 5;
          speedSlider.value = snappedValue;
          trainingSpeed = snappedValue;
          updateSpeedDisplay();
        }
      });
    }

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log("📡 Training stream ended");
        break;
      }

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          try {
            const epochData = JSON.parse(line.slice(6));
            console.log("📊 Epoch data received:", epochData);

            if (epochData.error) {
              console.error("❌ Training error:", epochData.message);
              // Remove page unload handler
              window.removeEventListener("beforeunload", handlePageUnload);
              updateStatus("Training error: " + epochData.message);
              isTraining = false;
              updateControlButtons();
              return;
            }

            if (epochData.training_complete) {
              console.log("✅ Training completed:", epochData);
              console.log("🔍 Training response structure:", {
                has_final_theta0: "final_theta0" in epochData,
                has_final_theta1: "final_theta1" in epochData,
                has_equation: "equation" in epochData,
                has_sklearn_comparison: "sklearn_comparison" in epochData,
                keys: Object.keys(epochData),
              });

              // Remove page unload handler
              window.removeEventListener("beforeunload", handlePageUnload);

              // Store ALL the essential data we need for results page
              const trainingParams = JSON.parse(
                localStorage.getItem("trainingParams") || "{}"
              );
              const essentialTrainingData = {
                // Final model parameters
                final_theta0: epochData.final_theta0,
                final_theta1: epochData.final_theta1,
                equation: epochData.equation,

                // Performance metrics
                final_rmse: epochData.final_rmse,
                final_mae: epochData.final_mae,
                final_r2: epochData.final_r2,
                test_mse: epochData.test_mse,
                test_r2: epochData.test_r2,

                // Training info
                total_epochs:
                  epochData.total_epochs || epochData.epoch || "Unknown",

                // Training parameters
                learning_rate: trainingParams.learning_rate,
                epochs: trainingParams.epochs,
                tolerance: trainingParams.tolerance,
                early_stopping: trainingParams.early_stopping,
                training_speed: trainingParams.training_speed,
                train_split: trainingParams.train_split,
                x_column: trainingParams.x_column,
                y_column: trainingParams.y_column,

                // Sklearn comparison
                sklearn_comparison: epochData.sklearn_comparison,
              };

              console.log(
                "🔍 About to store essential training data:",
                essentialTrainingData
              );
              console.log("🔍 epochData keys:", Object.keys(epochData));
              console.log("🔍 epochData.final_theta0:", epochData.final_theta0);
              console.log("🔍 epochData.final_theta1:", epochData.final_theta1);

              localStorage.setItem(
                "allTrainingData",
                JSON.stringify(essentialTrainingData)
              );
              console.log(
                "💾 Essential training data stored (clean structure):",
                essentialTrainingData
              );

              // Verify what was actually stored
              const storedData = localStorage.getItem("allTrainingData");
              console.log(
                "🔍 Verification - what was actually stored:",
                storedData
              );
              console.log(
                "🔍 Verification - parsed stored data:",
                JSON.parse(storedData)
              );

              // Add a marker to prove our code ran
              localStorage.setItem("NEW_CODE_EXECUTED", "YES");
              console.log("🚨 NEW CODE EXECUTED - MARKER SET");

              // Call completeTraining for UI updates
              completeTraining(epochData);
              return;
            }

            // Debug: Log what we're receiving
            console.log("🔍 Epoch data received:", {
              epoch: epochData.epoch,
              training_complete: epochData.training_complete,
              is_complete: epochData.is_complete,
              converged: epochData.converged,
            });

            // Speed-controlled UI updates for visual elements
            // Backend-controlled speed: Update immediately when data arrives
            if (trainingSpeed > 0) {
              // Backend is already controlling the speed, so update immediately
              console.log(
                `🎨 Epoch ${epochData.epoch} received from backend - updating immediately`
              );

              // Update all visual elements immediately
              updateTrainingDisplay(epochData);
              updateCostChart(epochData);
              updateProgressBar(epochData);

              // Update performance metrics
              updatePerformanceMetrics(epochData);

              // Show current speed to user
              const speedInfo = document.getElementById("currentSpeed");
              if (speedInfo) {
                let speedText = "";
                if (trainingSpeed >= 0.8) {
                  speedText = "⚡ Speed 1.0 (Fast)";
                } else if (trainingSpeed >= 0.6) {
                  speedText = "🚀 Speed 0.8 (Fast-Medium)";
                } else if (trainingSpeed >= 0.4) {
                  speedText = "🐌 Speed 0.6 (Medium)";
                } else if (trainingSpeed >= 0.2) {
                  speedText = "🐌 Speed 0.4 (Slow)";
                } else {
                  speedText = "🐌 Speed 0.2 (Very Slow)";
                }

                // Add pause indicator if training is paused
                if (isPaused) {
                  speedText += " ⏸️ (Paused)";
                }

                speedInfo.textContent = speedText;
              }
            }
            // If speed = 0, don't update visual elements (paused)

            // Show training progress in status
            const trainingStatus = document.getElementById("trainingStatus");
            if (trainingStatus) {
              trainingStatus.textContent = `Training Epoch ${epochData.epoch}...`;
            }
          } catch (parseError) {
            console.error("❌ Error parsing epoch data:", parseError);
          }
        }
      }
    }
  } catch (error) {
    console.error("❌ Streaming training error:", error);
    // Remove page unload handler
    if (typeof handlePageUnload !== "undefined") {
      window.removeEventListener("beforeunload", handlePageUnload);
    }
    updateStatus("Training error: " + error.message);
    isTraining = false;
    updateControlButtons();
  }
}

// Function to update cost chart - ALWAYS called regardless of speed
function updateCostChart(epochData) {
  try {
    if (window.costChart && typeof window.costChart.data !== "undefined") {
      // Ensure epoch and cost are valid numbers
      const epoch = parseInt(epochData.epoch);
      const cost = parseFloat(epochData.cost);

      if (!isNaN(epoch) && !isNaN(cost)) {
        // Add new data point
        window.costChart.data.labels.push(epoch);
        window.costChart.data.datasets[0].data.push(cost);

        // Keep only last 200 points for performance (optional)
        if (window.costChart.data.labels.length > 200) {
          window.costChart.data.labels.shift();
          window.costChart.data.datasets[0].data.shift();
        }

        // Update chart with new data - show animation for user to see plotting
        window.costChart.update("active"); // Use 'active' instead of 'none' to show animation
        console.log(
          `📊 Cost chart updated: Epoch ${epoch}, Cost ${cost.toFixed(
            6
          )} (total points: ${window.costChart.data.labels.length})`
        );
      } else {
        console.warn("⚠️ Invalid epoch or cost data:", {
          epoch: epochData.epoch,
          cost: epochData.cost,
        });
      }
    } else {
      console.warn("⚠️ Cost chart not available for update");
    }
  } catch (error) {
    console.error("❌ Error updating cost chart:", error);
  }
}

// Global function to cancel all running animations
function cancelAllAnimations() {
  if (window.currentAnimationId) {
    clearTimeout(window.currentAnimationId);
    window.currentAnimationId = null;
    console.log("🛑 All animations cancelled");
  }
}

// Function to initialize performance metrics
function initializePerformanceMetrics() {
  console.log("📊 Initializing performance metrics...");

  // Set initial metric values
  const rmseMetric = document.getElementById("rmseMetric");
  if (rmseMetric) {
    rmseMetric.textContent = "0";
    rmseMetric.style.color = "#6b7280";
  }

  const maeMetric = document.getElementById("maeMetric");
  if (maeMetric) {
    maeMetric.textContent = "0";
    maeMetric.style.color = "#6b7280";
  }

  const r2Metric = document.getElementById("r2Metric");
  if (r2Metric) {
    r2Metric.textContent = "0";
    r2Metric.style.color = "#6b7280";
  }

  console.log("✅ Performance metrics initialized");
}

// Function to update performance metrics during training
function updatePerformanceMetrics(epochData) {
  console.log("📊 Updating performance metrics with:", epochData);

  // Use metrics from backend (more accurate and efficient)
  if (
    epochData.rmse !== undefined &&
    epochData.mae !== undefined &&
    epochData.r2 !== undefined
  ) {
    const rmse = epochData.rmse;
    const mae = epochData.mae;
    const r2 = epochData.r2;

    // Update metric displays
    const rmseMetric = document.getElementById("rmseMetric");
    if (rmseMetric) {
      rmseMetric.textContent = rmse.toFixed(4);
      rmseMetric.style.color =
        rmse < 1 ? "#10b981" : rmse < 5 ? "#f59e0b" : "#ef4444";
    }

    const maeMetric = document.getElementById("maeMetric");
    if (maeMetric) {
      maeMetric.textContent = mae.toFixed(4);
      maeMetric.style.color =
        mae < 1 ? "#10b981" : mae < 5 ? "#f59e0b" : "#ef4444";
    }

    const r2Metric = document.getElementById("r2Metric");
    if (r2Metric) {
      r2Metric.textContent = r2.toFixed(4);
      r2Metric.style.color =
        r2 > 0.8 ? "#10b981" : r2 > 0.6 ? "#f59e0b" : "#ef4444";
    }

    console.log("📊 Performance metrics updated from backend:", {
      rmse,
      mae,
      r2,
    });
  } else {
    console.warn("⚠️ Metrics not available in epoch data");
  }
}

function updateTrainingDisplay(epochData) {
  try {
    console.log("🔄 Updating training display with:", epochData);
    console.log("📊 Cost chart status:", {
      exists: !!window.costChart,
      hasData: window.costChart ? !!window.costChart.data : false,
      labelsLength: window.costChart?.data?.labels?.length || 0,
      dataLength: window.costChart?.data?.datasets?.[0]?.data?.length || 0,
    });

    // Update displays
    const equationDisplay = document.getElementById("equationDisplay");
    if (equationDisplay) {
      equationDisplay.textContent = `y = ${epochData.theta0.toFixed(
        4
      )} + ${epochData.theta1.toFixed(4)}x`;
    }

    const theta0Display = document.getElementById("theta0Display");
    if (theta0Display) {
      theta0Display.textContent = epochData.theta0.toFixed(6);
    }

    const theta1Display = document.getElementById("theta1Display");
    if (theta1Display) {
      theta1Display.textContent = epochData.theta1.toFixed(6);
    }

    const trainingStatus = document.getElementById("trainingStatus");
    if (trainingStatus) {
      trainingStatus.textContent = `Training (Epoch ${epochData.epoch}/${epochData.max_epochs})`;
    }

    // Cost chart is now updated separately via updateCostChart() function
    // This function only updates visual elements (equation, theta values, regression line)

    // FIXED: Correct regression line calculation
    if (window.scatterChart) {
      console.log("🔍 Scatter chart found, updating regression line...");
      const scatterData = window.scatterChart.data.datasets[0].data;
      if (scatterData && scatterData.length > 0) {
        // Get actual X range from data points
        const xValues = scatterData.map((point) => point.x);
        const minX = Math.min(...xValues);
        const maxX = Math.max(...xValues);

        // Calculate regression line endpoints
        const y1 = epochData.theta0 + epochData.theta1 * minX;
        const y2 = epochData.theta0 + epochData.theta1 * maxX;

        console.log(
          `📐 Regression line: (${minX}, ${y1}) to (${maxX}, ${y2}) with θ₀=${epochData.theta0}, θ₁=${epochData.theta1}`
        );

        // Find or create regression line dataset
        let regressionDataset = window.scatterChart.data.datasets.find(
          (ds) => ds.label === "Regression Line"
        );

        if (regressionDataset) {
          // Update existing line
          regressionDataset.data = [
            { x: minX, y: y1 },
            { x: maxX, y: y2 },
          ];
          console.log("✅ Updated existing regression line");
        } else {
          // Create new line
          window.scatterChart.data.datasets.push({
            label: "Regression Line",
            data: [
              { x: minX, y: y1 },
              { x: maxX, y: y2 },
            ],
            type: "line",
            borderColor: "red",
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
            tension: 0,
          });
          console.log("✅ Created new regression line");
        }

        window.scatterChart.update("none");
        console.log("🔄 Scatter chart updated");
      } else {
        console.warn("⚠️ No scatter data found for regression line");
      }
    } else {
      console.warn("⚠️ Scatter chart not found for regression line update");
    }
  } catch (error) {
    console.error("Error updating training display:", error);
  }
}

function updateProgressBar(epochData) {
  try {
    // Update progress bar and text (always smooth)
    const progressFill = document.getElementById("progressFill");
    const progressText = document.getElementById("progressText");
    if (progressFill && progressText) {
      const progress = (epochData.epoch / epochData.max_epochs) * 100;
      progressFill.style.width = progress + "%";
      progressText.textContent = `Epoch ${epochData.epoch}/${epochData.max_epochs}`;
    }

    // Update cost value (always smooth)
    const costValue = document.getElementById("costValue");
    if (costValue) {
      costValue.textContent = `Cost: ${epochData.cost.toFixed(6)}`;
    }
  } catch (error) {
    console.error("❌ Error updating progress bar:", error);
  }
}

function updateTrainingStatus(message, icon = "✅") {
  try {
    const statusElement = document.getElementById("trainingStatus");
    if (statusElement) {
      statusElement.innerHTML = `
                <div class="status-message">
                    <span class="status-icon">${icon}</span>
                    <span class="status-text">${message}</span>
                </div>
            `;
    }
  } catch (error) {
    console.error("Error in updateTrainingStatus:", error);
  }
}

async function pauseTraining() {
  if (!isTraining || isPaused) return;

  try {
    const response = await fetch("/api/v1/pause-training", {
      method: "POST",
    });
    if (response.ok) {
      isPaused = true;
      updateControlButtons();
      updateStatus("Training paused");
      console.log("⏸️ Training paused");
    }
  } catch (error) {
    console.error("❌ Error pausing training:", error);
  }
}

async function resumeTraining() {
  if (!isTraining || !isPaused) return;

  try {
    const response = await fetch("/api/v1/resume-training", {
      method: "POST",
    });
    if (response.ok) {
      isPaused = false;
      updateControlButtons();
      updateStatus("Training resumed");
      console.log("▶️ Training resumed");
    }
  } catch (error) {
    console.error("❌ Error resuming training:", error);
  }
}

async function stopTraining() {
  if (!isTraining) return;
  isTraining = false;
  isPaused = false;
  updateControlButtons();

  // Cancel any running animations immediately
  if (window.currentAnimationId) {
    clearTimeout(window.currentAnimationId);
    window.currentAnimationId = null;
    console.log("🛑 Cancelled running animation on stop");
  }

  // Clear pending epochs (no longer needed with backend control)
  if (window.pendingEpochs) {
    window.pendingEpochs = [];
    console.log("🛑 Cleared pending epochs on stop");
  }

  // Stop backend training
  try {
    const response = await fetch("/api/v1/stop-training", {
      method: "POST",
    });
    if (response.ok) {
      console.log("🛑 Backend training stopped");
    }
  } catch (error) {
    console.error("❌ Error stopping backend training:", error);
  }

  // Hide equation display when training stops
  const equationDisplay = document.getElementById("equationDisplay");
  if (equationDisplay) {
    equationDisplay.style.display = "none";
    console.log("📊 Equation display hidden");
  }

  updateStatus("Training stopped");
}

async function restartTraining() {
  await stopTraining();

  // Reset pause state
  isPaused = false;

  // Cancel any running animations immediately
  if (window.currentAnimationId) {
    clearTimeout(window.currentAnimationId);
    window.currentAnimationId = null;
    console.log("🛑 Cancelled running animation on restart");
  }

  // Clear pending epochs (no longer needed with backend control)
  if (window.pendingEpochs) {
    window.pendingEpochs = [];
    console.log("🛑 Cleared pending epochs on restart");
  }

  // Animation variables no longer needed

  // Reset UI
  document.getElementById("equationDisplay").textContent = "y = NaN + NaN·x";
  document.getElementById("progressFill").style.width = "0%";
  document.getElementById("progressText").textContent = "Ready to start";
  document.getElementById("costValue").textContent = "Cost: -";

  // Clear scatter chart - remove regression line only (keep original data)
  if (window.scatterChart) {
    // Remove regression line dataset if it exists
    const regressionIndex = window.scatterChart.data.datasets.findIndex(
      (ds) => ds.label === "Regression Line"
    );
    if (regressionIndex !== -1) {
      window.scatterChart.data.datasets.splice(regressionIndex, 1);
    }
    window.scatterChart.update();
  }

  // Clear cost chart - remove all training data
  if (window.costChart && typeof window.costChart.data !== "undefined") {
    try {
      window.costChart.data.labels = [];
      window.costChart.data.datasets[0].data = [];
      window.costChart.update("none");
      console.log("🗑️ Cost chart cleared successfully");
    } catch (error) {
      console.error("❌ Error clearing cost chart:", error);
    }
  }

  // Keep density chart data - don't clear it
  // The density chart shows your original data, not training results

  updateStatus("Ready to train");
  console.log("🔄 Training restart complete - all animations stopped");
}

function completeTraining(epochData) {
  isTraining = false;
  isPaused = false;
  updateControlButtons();
  updateStatus("Training completed!");

  console.log("🎯 Starting completeTraining function...");
  console.log("🔍 completeTraining received epochData:", epochData);
  console.log("🔍 completeTraining epochData keys:", Object.keys(epochData));

  console.log("🎉 Training completed with final results:", epochData);

  // Update final training status and values
  const trainingStatus = document.getElementById("trainingStatus");
  if (trainingStatus) {
    trainingStatus.textContent = "Training Complete!";
  }

  // Update final equation and theta values
  const equationDisplay = document.getElementById("equationDisplay");
  if (equationDisplay) {
    equationDisplay.textContent = `y = ${epochData.final_theta0.toFixed(
      4
    )} + ${epochData.final_theta1.toFixed(4)}x`;
  }

  const theta0Display = document.getElementById("theta0Display");
  if (theta0Display) {
    theta0Display.textContent = epochData.final_theta0.toFixed(6);
  }

  const theta1Display = document.getElementById("theta1Display");
  if (theta1Display) {
    theta1Display.textContent = epochData.final_theta1.toFixed(6);
  }

  // Persist in workflow state
  // capture cost history
  let costHistory = [];
  if (window.costChart) {
    const labels = window.costChart.data.labels;
    const values = window.costChart.data.datasets[0].data;
    costHistory = labels.map((l, idx) => [l, values[idx]]);
  }
  const resultsToStore = { ...epochData, cost_history: costHistory };
  advanceStep(3, { resultsData: resultsToStore });

  // NOTE: We don't store training results here anymore because the streaming response
  // already stores the complete data in allTrainingData. This function only updates the UI.
  console.log(
    "💾 No need to store training results - streaming response already did that"
  );

  // Check if our new code ran
  const newCodeExecuted = localStorage.getItem("NEW_CODE_EXECUTED");
  console.log("🔍 Did our new code execute?", newCodeExecuted);

  // Check what's currently in allTrainingData
  const currentAllTrainingData = localStorage.getItem("allTrainingData");
  console.log(
    "🔍 Current allTrainingData after completeTraining:",
    currentAllTrainingData
  );

  // Training completed - View Results button is already clickable
  console.log("✅ Training flow completed successfully");
}

function updateControlButtons() {
  const startBtn = document.getElementById("startBtn");
  const pauseBtn = document.getElementById("pauseBtn");
  const resumeBtn = document.getElementById("resumeBtn");
  const stopBtn = document.getElementById("stopBtn");
  const restartBtn = document.getElementById("restartBtn");

  if (startBtn) startBtn.disabled = isTraining;
  if (pauseBtn) pauseBtn.disabled = !isTraining || isPaused;
  if (resumeBtn) resumeBtn.disabled = !isTraining || !isPaused;
  if (stopBtn) stopBtn.disabled = !isTraining;
  if (restartBtn) restartBtn.disabled = false; // Always enabled
}

function updateStatus(text) {
  const statusText = document.getElementById("statusText");
  if (statusText) {
    statusText.textContent = text;
  }

  // Also update training status display
  const trainingStatus = document.getElementById("trainingStatus");
  if (trainingStatus) {
    trainingStatus.textContent = text;
  }
}

window.prepareAndGoToResults = prepareAndGoToResults;

async function prepareAndGoToResults() {
  try {
    console.log("🚀 Preparing to go to results page...");

    // Check if we have training data
    const allTrainingData = localStorage.getItem("allTrainingData");
    if (!allTrainingData) {
      alert("No training data found. Please complete training first.");
      return;
    }

    console.log("🔍 Training data found, preparing comprehensive results...");
    console.log("🔍 Raw allTrainingData:", allTrainingData);

    // Parse training data to get sklearn comparison
    const trainingData = JSON.parse(allTrainingData);
    console.log("🔍 Parsed training data:", trainingData);
    console.log("🔍 Training data keys:", Object.keys(trainingData));

    const sklearnComparison = trainingData.sklearn_comparison;
    console.log("🔍 Sklearn comparison from training:", sklearnComparison);

    // Check if our new data structure is working
    const trainingDataStored = localStorage.getItem("TRAINING_DATA_STORED");
    console.log("🔍 Did we store training data?", trainingDataStored);

    // Store comprehensive training session data
    const comprehensiveData = {
      trainingData: trainingData,
      trainingParams: JSON.parse(
        localStorage.getItem("trainingParams") || "{}"
      ),
      allTrainingData: allTrainingData, // This now contains the actual training response
      sklearnResults: sklearnComparison,
      sessionTimestamp: new Date().toISOString(),
    };

    localStorage.setItem(
      "comprehensiveResults",
      JSON.stringify(comprehensiveData)
    );
    console.log("💾 Comprehensive results stored:", comprehensiveData);

    // Navigate to results page
    console.log("📊 Navigating to results page...");
    window.location.href = "/static/results.html";
  } catch (error) {
    console.error("❌ Error preparing results:", error);
    alert("Error preparing results. Please try again.");
  }
}

// Expand/Close functions
function expandCharts() {
  console.log("📈 Expanding charts to fullscreen...");

  const vizCard = document.querySelector(".viz-card");
  const trainingLayout = document.querySelector(".training-layout");
  const expandBtn = document.getElementById("expandChartsBtn");
  const closeExpandBtn = document.getElementById("closeExpandBtn");

  if (vizCard && trainingLayout) {
    // Add expanded classes
    vizCard.classList.add("expanded");
    trainingLayout.classList.add("charts-expanded");

    // Update button visibility
    if (expandBtn) expandBtn.style.display = "none";
    if (closeExpandBtn) closeExpandBtn.style.display = "flex";

    // Update global state
    isExpanded = true;

    // Show simple parameters button
    const paramsToggleBtn = document.getElementById("paramsToggleBtn");
    console.log("🔍 Looking for params button:", paramsToggleBtn);
    console.log("🔍 Button element found:", !!paramsToggleBtn);
    console.log("🔍 Button current display:", paramsToggleBtn?.style.display);

    if (paramsToggleBtn) {
      paramsToggleBtn.style.display = "block";
      console.log("✅ Simple parameters button shown");
      console.log(
        "🔍 Button display after setting:",
        paramsToggleBtn.style.display
      );
    } else {
      console.error("❌ Simple parameters button not found!");
    }

    // Force chart resize after expansion
    setTimeout(() => {
      if (window.costChart) window.costChart.resize();
      if (window.scatterChart) window.scatterChart.resize();
    }, 300);

    console.log("✅ Charts expanded to fullscreen");
  }
}

function closeExpandedView() {
  console.log("🔄 Closing expanded view...");

  const vizCard = document.querySelector(".viz-card");
  const trainingLayout = document.querySelector(".training-layout");
  const expandBtn = document.getElementById("expandChartsBtn");
  const closeExpandBtn = document.getElementById("closeExpandBtn");

  if (vizCard && trainingLayout) {
    // Remove expanded classes
    vizCard.classList.remove("expanded");
    trainingLayout.classList.remove("charts-expanded");

    // Update button visibility
    if (expandBtn) expandBtn.style.display = "flex";
    if (closeExpandBtn) closeExpandBtn.style.display = "none";

    // Update global state
    isExpanded = false;

    // Hide simple parameters button and panel
    const paramsToggleBtn = document.getElementById("paramsToggleBtn");
    if (paramsToggleBtn) {
      paramsToggleBtn.style.display = "none";
      console.log("🔄 Simple parameters button hidden");
    }

    // Hide parameters panel if it's open
    const paramsPanel = document.getElementById("simpleParamsPanel");
    if (paramsPanel && paramsPanel.classList.contains("open")) {
      paramsPanel.classList.remove("open");
      console.log("🔄 Simple parameters panel closed");
    }

    // Force chart resize after closing
    setTimeout(() => {
      if (window.costChart) window.costChart.resize();
      if (window.scatterChart) window.scatterChart.resize();
    }, 300);

    console.log("✅ Expanded view closed");
  }
}

// Auto-expand when training starts
function startTrainingWithExpand() {
  if (!isExpanded) {
    expandCharts();
  }
}

// guard access
const st = loadState();
if (!st.step || st.step < 2) {
  window.location.href = "/static/index.html";
}

// ============================================================================
// CHART THEME UPDATES
// ============================================================================

function updateChartColors() {
  const colors = getThemeColors();
  console.log("🎨 Updating chart colors to:", colors);

  // Update scatter chart colors
  if (window.scatterChart) {
    window.scatterChart.options.scales.x.title.color = colors.textPrimary;
    window.scatterChart.options.scales.y.title.color = colors.textPrimary;
    window.scatterChart.options.scales.x.ticks.color = colors.textPrimary;
    window.scatterChart.options.scales.y.ticks.color = colors.textPrimary;
    window.scatterChart.options.plugins.title.color = colors.textPrimary;
    window.scatterChart.update("none");
  }

  // Update cost chart colors
  if (window.costChart) {
    window.costChart.options.scales.x.title.color = colors.textPrimary;
    window.costChart.options.scales.y.title.color = colors.textPrimary;
    window.costChart.options.scales.x.ticks.color = colors.textPrimary;
    window.costChart.options.scales.y.ticks.color = colors.textPrimary;
    window.costChart.options.plugins.title.color = colors.textPrimary;
    window.costChart.update("none");
  }
}
