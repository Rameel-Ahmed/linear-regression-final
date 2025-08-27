// Minimal workflow state helper
const KEY = "workflowState";

export function loadState() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {};
  } catch (_) {
    return {};
  }
}

export function saveState(state) {
  localStorage.setItem(KEY, JSON.stringify(state));
}

export function resetState() {
  localStorage.removeItem(KEY);
}

export function advanceStep(step, payload = {}) {
  if (step === 1) {
    // Full reset when a new file is chosen
    resetState();
  }
  const current = loadState();
  saveState({ ...current, ...payload, step });
}

// Make available globally for quick debugging
window.__workflowState = { loadState, saveState, resetState, advanceStep };
