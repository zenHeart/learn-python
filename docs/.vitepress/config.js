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
      var encoded = encodeURIComponent(code)
      return '<div class="py-demo" data-code="' + encoded + '">' +
        '<div class="py-demo-header">' +
        '<span>Python</span>' +
        '<button class="py-demo-run" onclick="window.__runPyDemo(this)">Run</button>' +
        '</div>' +
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

module.exports = {
  title: 'learn-python',
  description: 'Python Interactive Learning',
  base: isDev ? '/' : '/learn-python/',
  markdown: {
    config: function(md) {
      md.use(createPyodidePlugin)
    }
  },
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Quick Start', link: '/tutorial/begin' }
    ],
    sidebar: [
      {
        text: 'Quick Start',
        link: '/tutorial/begin'
      },
      {
        text: 'Basics',
        children: [
          { text: 'Types', link: '/tutorial/types' },
          { text: 'Statements', link: '/tutorial/statement' },
          { text: 'Functions', link: '/tutorial/function' },
          { text: 'Classes', link: '/tutorial/class' }
        ]
      }
    ]
  }
}
