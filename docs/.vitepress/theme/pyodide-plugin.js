// Pyodide Markdown Plugin - transforms python code blocks into interactive demos

function pyodidePlugin(md) {
  const defaultFence = md.renderer.rules.fence || function(tokens, idx, options, env, self) {
    return self.renderToken(tokens, idx, options)
  })

  md.renderer.rules.fence = function(tokens, idx, options, env, self) {
    const token = tokens[idx]
    const lang = token.info.trim().toLowerCase()

    if (lang === 'python' || lang === 'py') {
      const code = token.content
      const encoded = encodeURIComponent(code)
      return '<div class="py-demo" data-code="' + encoded + '">' +
        '<div class="py-demo-header">' +
        '<span>🐍 Python</span>' +
        '<button class="py-demo-run" onclick="window.__runPyDemo(this)">▶ 运行</button>' +
        '</div>' +
        '<pre class="language-python"><code>' + escapeHtml(code) + '</code></pre>' +
        '<div class="py-demo-output">点击「运行」查看输出</div>' +
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

module.exports = { pyodidePlugin }
