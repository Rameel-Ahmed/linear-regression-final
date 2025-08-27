// helpers/sidebar.js

export function setupSidebarToggle() {
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.querySelector(".sidebar");
  const mainContent = document.querySelector(".main-content");

  console.log("🔍 Sidebar toggle setup:", {
    sidebarToggle,
    sidebar,
    mainContent,
  });

  if (sidebarToggle && sidebar && mainContent) {
    console.log("✅ Sidebar toggle elements found, adding event listeners");

    sidebarToggle.addEventListener("click", () => {
      console.log("🔄 Sidebar toggle clicked");
      sidebar.classList.toggle("collapsed");
      mainContent.classList.toggle("sidebar-collapsed");

      // Update button text based on state
      sidebarToggle.textContent = sidebar.classList.contains("collapsed")
        ? "→"
        : "☰";

      console.log(
        "📱 Sidebar collapsed:",
        sidebar.classList.contains("collapsed")
      );
    });
  } else {
    console.error("❌ Sidebar toggle elements not found:", {
      sidebarToggle,
      sidebar,
      mainContent,
    });
  }
}

// ============================================================================
// TOAST NOTIFICATION FUNCTIONS
// ============================================================================

export function showSuccessToast(message, cleanedRows) {
  const toastContainer = document.getElementById("toastContainer");
  const template = document.querySelector(".toast-success-template");

  const toast = template.cloneNode(true);
  toast.classList.remove("toast-success-template");

  toast.querySelector(".toast-title").textContent = message;
  toast.querySelector(
    ".toast-content"
  ).textContent = `${cleanedRows} rows ready for training`;

  toastContainer.appendChild(toast);

  // Show toast with animation
  setTimeout(() => toast.classList.add("show"), 100);

  // Auto-remove toast after 8 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }
  }, 8000);
}

export function showErrorToast(message) {
  const toastContainer = document.getElementById("toastContainer");
  const template = document.querySelector(".toast-error-template");

  const toast = template.cloneNode(true);
  toast.classList.remove("toast-error-template");

  toast.querySelector(".toast-title").textContent = "Error";
  toast.querySelector(".toast-content").textContent = message.includes(",")
    ? message
        .split(",")
        .map((m) => m.trim())
        .join("\n")
    : message;

  toastContainer.appendChild(toast);

  // Show toast with animation
  setTimeout(() => toast.classList.add("show"), 100);

  // Auto-remove toast after 8 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }
  }, 8000);
}

export function showWarningToast(title, message) {
  const toastContainer = document.getElementById("toastContainer");
  const template = document.querySelector(".toast-warning-template");

  const toast = template.cloneNode(true);
  toast.classList.remove("toast-warning-template");

  toast.querySelector(".toast-title").textContent = title;
  toast.querySelector(".toast-content").textContent = message;

  toastContainer.appendChild(toast);

  // Show toast with animation
  setTimeout(() => toast.classList.add("show"), 100);

  // Auto-remove toast after 10 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }
  }, 10000);
}

export function showInfoToast(title, message) {
  const toastContainer = document.getElementById("toastContainer");

  // Create a simple info toast (can use success template)
  const template = document.querySelector(".toast-success-template");
  const toast = template.cloneNode(true);
  toast.classList.remove("toast-success-template");
  toast.classList.remove("success");
  toast.classList.add("info");

  toast.querySelector(".toast-title").textContent = title;
  toast.querySelector(".toast-content").textContent = message;

  toastContainer.appendChild(toast);

  // Show toast with animation
  setTimeout(() => toast.classList.add("show"), 100);

  // Auto-remove toast after 6 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }
  }, 6000);
}

// =========================================================================
// WORKFLOW SIDEBAR ACCESS
// =========================================================================
import { loadState } from "./state.js";

export function applySidebarAccess() {
  const state = loadState();
  const items = document.querySelectorAll(".sidebar .nav-item[data-step]");
  items.forEach((el) => {
    const needed = Number(el.dataset.step);
    if (state.step >= needed) {
      el.classList.remove("disabled");
      // leave as link
    } else {
      el.classList.add("disabled");
      el.addEventListener("click", (e) => {
        e.preventDefault();
        alert("Complete previous steps first.");
      });
    }
  });
}
