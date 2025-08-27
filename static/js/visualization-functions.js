// ============================================================================
// VISUALIZATION FUNCTIONS MODULE - Using Plotly.js with Backend Statistics
// ============================================================================

// Function to get current theme colors
function getThemeColors() {
  const root = document.documentElement;
  const colors = {
    textPrimary:
      getComputedStyle(root).getPropertyValue("--text-primary") || "#1a202c",
    textSecondary:
      getComputedStyle(root).getPropertyValue("--text-secondary") || "#4a5568",
    cardBg:
      getComputedStyle(root).getPropertyValue("--card-bg") ||
      "rgba(255,255,255,0.8)",
    borderColor:
      getComputedStyle(root).getPropertyValue("--border-color") ||
      "rgba(0,0,0,0.1)",
  };

  console.log("🎨 Theme colors loaded:", colors);
  return colors;
}

// Only keep median calculation since backend doesn't provide it
export function calculateMedian(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0
    ? sorted[mid]
    : (sorted[mid - 1] + sorted[mid]) / 2;
}

export function showVisualizationSection() {
  const section = document.getElementById("visualizationSection");
  if (section) section.style.display = "block";
}

/**
 * Creates an enhanced scatter plot with regression line using Plotly.js
 */
export function createScatterPlot() {
  const container = document.getElementById("scatterChart");
  if (!container) return;

  const { x_values, y_values } = window.cleanedData;
  const { x_column, y_column } = window.cleanedDataColumns;

  // Calculate simple linear regression for trend line
  const n = x_values.length;
  const sumX = x_values.reduce((a, b) => a + b, 0);
  const sumY = y_values.reduce((a, b) => a + b, 0);
  const sumXY = x_values.reduce((sum, x, i) => sum + x * y_values[i], 0);
  const sumXX = x_values.reduce((sum, x) => sum + x * x, 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  // Create trend line data
  const minX = Math.min(...x_values);
  const maxX = Math.max(...x_values);
  const trendLineX = [minX, maxX];
  const trendLineY = [slope * minX + intercept, slope * maxX + intercept];

  // Create traces for Plotly
  const traces = [
    {
      x: x_values,
      y: y_values,
      mode: "markers",
      type: "scatter",
      name: `${y_column} vs ${x_column}`,
      marker: {
        size: 6,
        color: "rgba(59, 130, 246, 0.7)",
        line: {
          color: "rgba(59, 130, 246, 1)",
          width: 1,
        },
      },
      hovertemplate:
        `<b>${x_column}</b>: %{x:.3f}<br>` +
        `<b>${y_column}</b>: %{y:.3f}<br>` +
        `<extra></extra>`,
    },
  ];

  const colors = getThemeColors();
  const layout = {
    title: {
      text: `${y_column} vs ${x_column} - Distribution & Trend`,
      font: { size: 16, color: colors.textPrimary },
    },
    xaxis: {
      title: {
        text: x_column,
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    yaxis: {
      title: {
        text: y_column,
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    hovermode: "closest",
    showlegend: true,
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: colors.cardBg,
      bordercolor: colors.borderColor,
      borderwidth: 1,
    },
    margin: { l: 60, r: 30, t: 60, b: 60 },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
  };

  const config = {
    responsive: true,
    displayModeBar: "hover",
    modeBarButtonsToRemove: ["pan2d", "lasso2d", "select2d"],
    displaylogo: false,
  };

  // Create the plot
  Plotly.newPlot(container, traces, layout, config).then(() => {
    // Add click event for data points
    container.on("plotly_click", function (data) {
      const point = data.points[0];
      if (point.curveNumber === 0) {
        const x = point.x;
        const y = point.y;
        console.log(
          `Clicked point: ${x_column}=${x.toFixed(3)}, ${y_column}=${y.toFixed(
            3
          )}`
        );

        // Highlight the clicked point
        const update = {
          "marker.size": Array(x_values.length)
            .fill(6)
            .map((size, i) =>
              Math.abs(x_values[i] - x) < 0.001 &&
              Math.abs(y_values[i] - y) < 0.001
                ? 12
                : 6
            ),
        };
        Plotly.restyle(container, update);
      }
    });
  });
}

/**
 * Creates a density heatmap using Plotly.js
 */
export function createDensityPlot() {
  const container = document.getElementById("densityChart");
  if (!container) return;

  const { x_values, y_values } = window.cleanedData;
  const { x_column, y_column } = window.cleanedDataColumns;

  const trace = {
    x: x_values,
    y: y_values,
    type: "histogram2d",
    colorscale: "Viridis",
    nbinsx: 30,
    nbinsy: 30,
    hoverongaps: false,
    hovertemplate:
      `<b>Density</b>: %{z}<br>` +
      `<b>${x_column}</b>: %{x:.3f}<br>` +
      `<b>${y_column}</b>: %{y:.3f}<br>` +
      `<extra></extra>`,
  };

  const colors = getThemeColors();
  const layout = {
    title: {
      text: `${y_column} vs ${x_column} - Density Heatmap`,
      font: { size: 16, color: colors.textPrimary },
    },
    xaxis: {
      title: {
        text: x_column,
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    yaxis: {
      title: {
        text: y_column,
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    hovermode: "closest",
    margin: { l: 60, r: 30, t: 60, b: 60 },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
  };

  const config = {
    responsive: true,
    displayModeBar: "hover",
    modeBarButtonsToRemove: ["pan2d", "lasso2d", "select2d"],
    displaylogo: false,
  };

  Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Creates a range analysis chart using backend data
 */
export function createRangePlot() {
  const container = document.getElementById("rangeChart");
  if (!container) return;

  const { x_values, y_values } = window.cleanedData;
  const { x_column, y_column } = window.cleanedDataColumns;

  const xMin = Math.min(...x_values);
  const xMax = Math.max(...x_values);
  const yMin = Math.min(...y_values);
  const yMax = Math.max(...y_values);

  const xRange = xMax - xMin;
  const yRange = yMax - yMin;

  const trace = {
    x: [x_column, y_column],
    y: [xRange, yRange],
    type: "bar",
    marker: {
      color: ["rgba(168, 85, 247, 0.8)", "rgba(236, 72, 153, 0.8)"],
      line: {
        color: ["rgba(168, 85, 247, 1)", "rgba(236, 72, 153, 1)"],
        width: 2,
      },
    },
    hovertemplate:
      `<b>%{x}</b><br>` +
      `<b>Range</b>: %{y:.3f}<br>` +
      `<b>Min</b>: ${
        x_column === "%{x}" ? xMin.toFixed(3) : yMin.toFixed(3)
      }<br>` +
      `<b>Max</b>: ${
        x_column === "%{x}" ? xMax.toFixed(3) : yMax.toFixed(3)
      }<br>` +
      `<extra></extra>`,
  };

  const colors = getThemeColors();
  const layout = {
    title: {
      text: "Min-Max Range Analysis",
      font: { size: 16, color: colors.textPrimary },
    },
    xaxis: {
      title: {
        text: "Variables",
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
    },
    yaxis: {
      title: {
        text: "Range Value",
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    margin: { l: 60, r: 30, t: 60, b: 60 },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
  };

  const config = {
    responsive: true,
    displayModeBar: "hover",
    modeBarButtonsToRemove: ["pan2d", "lasso2d", "select2d"],
    displaylogo: false,
  };

  Plotly.newPlot(container, [trace], layout, config);
}

/**
 * Creates statistical summary using pre-calculated backend statistics
 * Much more efficient than recalculating
 */
export function createStatisticalSummary() {
  const container = document.getElementById("statsChart");
  if (!container) return;

  const { x_values, y_values } = window.cleanedData;
  const { x_column, y_column } = window.cleanedDataColumns;

  // Use pre-calculated statistics from backend
  const stats = window.cleanedStats;
  const xMean = stats.x_mean;
  const yMean = stats.y_mean;
  const xStdDev = stats.x_std;
  const yStdDev = stats.y_std;

  // Calculate medians (not provided by backend)
  const xMedian = calculateMedian(x_values);
  const yMedian = calculateMedian(y_values);

  const trace = {
    x: ["Mean", "Median", "Std Dev"],
    y: [xMean, xMedian, xStdDev],
    type: "bar",
    name: x_column,
    marker: {
      color: "rgba(34, 197, 94, 0.8)",
      line: {
        color: "rgba(34, 197, 94, 1)",
        width: 2,
      },
    },
    hovertemplate:
      `<b>${x_column}</b><br>` +
      `<b>%{x}</b>: %{y:.3f}<br>` +
      `<extra></extra>`,
  };

  const trace2 = {
    x: ["Mean", "Median", "Std Dev"],
    y: [yMean, yMedian, yStdDev],
    type: "bar",
    name: y_column,
    marker: {
      color: "rgba(59, 130, 246, 0.8)",
      line: {
        color: "rgba(59, 130, 246, 1)",
        width: 2,
      },
    },
    hovertemplate:
      `<b>${y_column}</b><br>` +
      `<b>%{x}</b>: %{y:.3f}<br>` +
      `<extra></extra>`,
  };

  const colors = getThemeColors();
  const layout = {
    title: {
      text: "Statistical Summary Comparison",
      font: { size: 16, color: colors.textPrimary },
    },
    xaxis: {
      title: {
        text: "Statistics",
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
    },
    yaxis: {
      title: {
        text: "Value",
        font: { size: 14, color: colors.textPrimary, weight: "bold" },
      },
      tickfont: { color: colors.textPrimary },
      gridcolor: "rgba(0,0,0,0.1)",
      zeroline: false,
    },
    barmode: "group",
    hovermode: "closest",
    showlegend: true,
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: colors.cardBg,
      bordercolor: colors.borderColor,
      borderwidth: 1,
    },
    margin: { l: 60, r: 30, t: 60, b: 60 },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
  };

  const config = {
    responsive: true,
    displayModeBar: "hover",
    modeBarButtonsToRemove: ["pan2d", "lasso2d", "select2d"],
    displaylogo: false,
  };

  Plotly.newPlot(container, [trace, trace2], layout, config);
}
