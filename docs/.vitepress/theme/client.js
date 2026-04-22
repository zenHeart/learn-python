// This file only runs in the browser (VitePress client-side)
// Load Pyodide and register the run button handler

// Load Pyodide
var script = document.createElement('script')
script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'
script.defer = true
document.head.appendChild(script)

// Register run handler when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  window.__loadPyodide = async function() {
    if (window.__pyodideInstance) return window.__pyodideInstance
    window.__pyodideInstance = await window.loadPyodide()
    return window.__pyodideInstance
  }

  window.__runPyDemo = async function(button) {
    var container = button.closest('.py-demo')
    if (!container || button.classList.contains('running')) return
    var outputEl = container.querySelector('.py-demo-output')
    var preEl = container.querySelector('pre code')
    var safeCode = preEl ? preEl.textContent : ''
    button.classList.add('running')
    button.textContent = '⏳ Running...'
    outputEl.textContent = 'Loading...'
    outputEl.classList.remove('error')
    try {
      var py = await window.__loadPyodide()
      outputEl.textContent = 'Running...'
      var result = await py.runPythonAsync(safeCode)
      outputEl.textContent = result || '(no output)'
    } catch (e) {
      outputEl.textContent = 'Error: ' + e.message
      outputEl.classList.add('error')
    } finally {
      button.classList.remove('running')
      button.textContent = 'Run'
    }
  }
})