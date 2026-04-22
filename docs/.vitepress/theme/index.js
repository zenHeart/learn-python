import DefaultTheme from 'vitepress/theme'
import './pyodide.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // Load Pyodide dynamically on first run
    window.__loadPyodide = async () => {
      if (window.__pyodideInstance) return window.__pyodideInstance
      
      outputEl.textContent = '正在加载 Python 引擎...'
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'
      document.head.appendChild(script)
      
      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
      
      window.__pyodideInstance = await window.loadPyodide()
      return window.__pyodideInstance
    }
  }
}

// Run handler - attached to window for onclick inline handlers
if (typeof window !== 'undefined') {
  window.__runPyDemo = async function(button) {
    const container = button.closest('.py-demo')
    if (!container) return
    
    if (button.classList.contains('running')) return
    
    const code = decodeURIComponent(container.dataset.code || '')
    const outputEl = container.querySelector('.py-demo-output')
    const preEl = container.querySelector('pre code')
    
    // Get code from hidden pre element (safe HTML encoded)
    const safeCode = preEl ? preEl.textContent : code
    
    button.classList.add('running')
    button.textContent = '⏳ 运行中...'
    outputEl.textContent = '等待执行...'
    outputEl.classList.remove('error')
    
    try {
      const py = await window.__loadPyodide()
      outputEl.textContent = '执行中...'
      const result = await py.runPythonAsync(safeCode)
      outputEl.textContent = result || '(无输出)'
    } catch (e) {
      outputEl.textContent = 'Error: ' + e.message
      outputEl.classList.add('error')
    } finally {
      button.classList.remove('running')
      button.textContent = '▶ 运行'
    }
  }
}
