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
        '<div class="py-demo-header"><span>Python</span><button class="py-demo-run" type="button">▶ 运行</button></div>' +
        '<pre class="language-python"><code>' + escapeHtml(code) + '</code></pre>' +
        '<div class="py-demo-output">点击「▶ 运行」查看输出</div>' +
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

// Base path for Pyodide files
var pyodideBase = isDev ? 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/' : '/learn-python/pyodide/'

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
    ['script', { src: pyodideBase + 'pyodide.js', defer: true }]
  ],
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '学习进度', link: '/progress' },
      { text: '🔍 学习走查', link: '/walkthrough/' }
    ],
    sidebar: [
      {
        text: '📖 教程',
        items: [
          { text: 'L1 Hello Python', link: '/tutorial/begin' },
          { text: '🔖 标注规范', link: '/tutorial/annotation' },
          { text: '❓ 知识盲点', link: '/tutorial/gaps' },
          { text: '📐 拆包语法完全指南', link: '/tutorial/unpack' }
        ]
      },
      {
        text: '🔍 学习走查',
        collapsed: false,
        items: [
          { text: '总览', link: '/walkthrough/' },
          { text: '覆盖总账', link: '/walkthrough/coverage' },
          { text: 'L1 走查笔记', link: '/walkthrough/l1' },
          { text: 'L2 数据类型', link: '/walkthrough/l2-types' },
          { text: 'L3 控制流', link: '/walkthrough/l3-flow' },
          { text: 'L4 函数', link: '/walkthrough/l4-function' },
          { text: 'L5 类', link: '/walkthrough/l5-class' },
          { text: 'examples 全量清单', link: '/walkthrough/examples-audit' },
          { text: '拆包断言核对', link: '/walkthrough/unpack' },
          { text: '练习证据', link: '/walkthrough/evidence' },
          { text: '发现的问题', link: '/walkthrough/defects' },
          { text: 'careers 对齐', link: '/walkthrough/careers' },
          { text: '未解决与恢复点', link: '/walkthrough/open' }
        ]
      }
    ]
  }
}
