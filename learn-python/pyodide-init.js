// Inline initialization script for Pyodide
// This file is injected into the HTML <head>

(function() {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Initialize pyodide instance
    window.__pyodideInstance = null;

    window.__loadPyodide = async function() {
      if (window.__pyodideInstance) return window.__pyodideInstance;
      if (typeof window.loadPyodide === 'undefined') {
        throw new Error('Pyodide is not loaded yet. Please wait.');
      }
      var basePath = window.location.pathname.startsWith('/learn-python/') 
        ? '/learn-python/pyodide/' 
        : '/pyodide/';
      window.__pyodideInstance = await window.loadPyodide({ indexURL: basePath });
      return window.__pyodideInstance;
    };

    window.__runPyDemo = async function(b) {
      var c = b.closest('.py-demo');
      if (!c || b.classList.contains('running')) return;
      var o = c.querySelector('.py-demo-output'),
          p = c.querySelector('pre code'),
          s = p ? p.textContent : '';
      b.classList.add('running');
      b.textContent = 'Running...';
      o.textContent = 'Loading...';
      o.classList.remove('error');
      try {
        var py = await window.__loadPyodide();
        o.textContent = 'Running...';
        var r = await py.runPythonAsync(s);
        o.textContent = r || '(no output)';
      } catch(e) {
        o.textContent = 'Error: ' + e.message;
        o.classList.add('error');
      } finally {
        b.classList.remove('running');
        b.textContent = 'Run';
      }
    };

    // Event delegation for click handler
    document.addEventListener('click', function(e) {
      var b = e.target.closest('.py-demo-run');
      if (b && window.__runPyDemo) window.__runPyDemo(b);
    });
  }
})();
