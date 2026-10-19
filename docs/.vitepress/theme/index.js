import DefaultTheme from 'vitepress/theme'
import './pyodide.css'
import { inBrowser } from 'vitepress'

if (inBrowser) {
  // Determine base path for Pyodide files
  const isProd = window.location.pathname.startsWith('/learn-python/')
  const pyodideBase = isProd ? '/learn-python/pyodide/' : '/pyodide/'

  // Load Pyodide script
  const script = document.createElement('script')
  script.src = pyodideBase + 'pyodide.js'
  script.defer = true
  document.head.appendChild(script)

  // Initialize global functions after DOM is ready
  window.addEventListener('DOMContentLoaded', function initPyodide() {
    window.__pyodideInstance = null

    window.__loadPyodide = async function() {
      if (window.__pyodideInstance) return window.__pyodideInstance
      if (typeof window.loadPyodide === 'undefined') {
        throw new Error('Pyodide not loaded yet')
      }
      window.__pyodideInstance = await window.loadPyodide({ indexURL: pyodideBase })
      return window.__pyodideInstance
    }

    window.__runPyDemo = async function(b) {
      var c = b.closest('.py-demo')
      if (!c || b.classList.contains('running')) return
      var o = c.querySelector('.py-demo-output'),
          p = c.querySelector('pre code'),
          s = p ? p.textContent : ''
      b.classList.add('running')
      b.textContent = '⏳ 运行中…'
      o.textContent = '加载中…'
      o.classList.remove('error')
      try {
        var py = await window.__loadPyodide()
        o.textContent = '运行中…'

        // Capture stdout so print() output is captured
        var lines = []
        py.setStdout({
          batched: function(line) {
            lines.push(line)
          }
        })

        await py.runPythonAsync(s)

        var output = lines.join('\n')
        o.textContent = output || '(运行完成，但没有 print 输出——这段代码只做赋值)'
      } catch(e) {
        o.textContent = '错误: ' + e.message
        o.classList.add('error')
      } finally {
        b.classList.remove('running')
        b.textContent = '▶ 运行'
      }
    }

    // Event delegation
    document.addEventListener('click', function(e) {
      var b = e.target.closest('.py-demo-run')
      if (b && window.__runPyDemo) window.__runPyDemo(b)
    })
  }, { once: true })
}

export default {
  extends: DefaultTheme
}
