const isDev = process.env.npm_lifecycle_event === 'vitepress:dev' || process.env.npm_lifecycle_script && process.env.npm_lifecycle_script.includes('dev docs')

function createPyodidePlugin(md) {
  var defaultFence = md.renderer.rules.fence || function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options)
  }

  md.renderer.rules.fence = function(tokens, idx, options, env, self) {
    var token = tokens[idx]
    var lang = token.info.trim().toLowerCase()

    if (lang === 'python' || lang === 'py') {
      var code = token.content
      return '<div class="py-demo">' +
        '<div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">Run</button></div>' +
        '<pre class="language-python"><code>' + escapeHtml(code) + '</code></pre>' +
        '<div class="py-demo-output">Click Run to see output</div>' +
        '</div>'
    }

    return defaultFence(tokens, idx, options, env, self)
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

var pyodideLoader = 'window.__loadPyodide=async function(){if(window.__pyodideInstance)return window.__pyodideInstance;window.__pyodideInstance=await window.loadPyodide();return window.__pyodideInstance};'
var runDemo = 'window.__runPyDemo=async function(b){var c=b.closest(".py-demo");if(!c||b.classList.contains("running"))return;var o=c.querySelector(".py-demo-output"),p=c.querySelector("pre code"),s=p?p.textContent:"";b.classList.add("running");b.textContent="Running...";o.textContent="Loading...";o.classList.remove("error");try{var py=await window.__loadPyodide();o.textContent="Running...";var r=await py.runPythonAsync(s);o.textContent=r||"(no output)"}catch(e){o.textContent="Error: "+e.message;o.classList.add("error")}finally{b.classList.remove("running");b.textContent="Run"}}'
var eventBinder = 'document.addEventListener("click",function(e){var b=e.target.closest(".py-demo-run");if(b&&window.__runPyDemo)window.__runPyDemo(b)})'

module.exports = {
  title: 'learn-python',
  description: 'Python 交互式学习站 — 边学边练，掌握 Agent 开发能力',
  base: isDev ? '/' : '/learn-python/',
  markdown: {
    config: function(md) {
      md.use(createPyodidePlugin)
    }
  },
  head: [
    ['script', { src: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js', defer: true }],
    ['script', { text: pyodideLoader + runDemo }],
    ['script', { text: eventBinder }]
  ],
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '学习进度', link: '/progress' }
    ]
  }
}