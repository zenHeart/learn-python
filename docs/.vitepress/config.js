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

var pyodideBase = isDev ? 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/' : '/learn-python/pyodide/'

module.exports = {
  title: 'learn-python',
  description: 'Python Agent 与后端岗位能力学习站',
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
      { text: '统一课程', link: '/tutorial/course-portal' },
      { text: '能力路径', link: '/tutorial/learning-path' },
      { text: '诊断', link: '/tutorial/diagnostic' },
      { text: '知识盲点', link: '/tutorial/gaps' },
      { text: '进度', link: '/progress' }
    ],
    sidebar: [
      {
        text: '🧭 能力路线',
        items: [
          { text: '统一课程入口', link: '/tutorial/course-portal' },
          { text: '能力路径', link: '/tutorial/learning-path' },
          { text: '诊断与掌握', link: '/tutorial/diagnostic' },
          { text: 'Python 后端底座', link: '/tutorial/backend-foundation' },
          { text: '知识库 Agent 案例', link: '/tutorial/knowledge-base-agent' }
        ]
      },
      {
        text: '🌐 跨语言课程',
        items: [
          { text: 'Java 后端与 Agent', link: 'https://github.com/zenHeart/learn-java' },
          { text: 'Go Agent 平台', link: 'https://github.com/zenHeart/learn-engineering/tree/main/docs/go' },
          { text: 'LLM 原理与实践', link: 'https://github.com/zenHeart/learn-llm' },
          { text: '面试证据合同', link: 'https://github.com/zenHeart/web-interview/pull/42' }
        ]
      },
      {
        text: '📖 机制与练习',
        items: [
          { text: 'L1 Hello Python', link: '/tutorial/begin' },
          { text: '标注规范', link: '/tutorial/annotation' },
          { text: '知识盲点', link: '/tutorial/gaps' },
          { text: '拆包语法', link: '/tutorial/unpack' },
          { text: 'JS/Python 对照', link: '/tutorial/js-syntax-diff' },
          { text: '手写 Agent Loop', link: '/tutorial/agent-loop' },
          { text: '检索链路', link: '/tutorial/retrieval-pipeline' },
          { text: '评测与回归门禁', link: '/tutorial/eval-regression-gate' }
        ]
      }
    ]
  }
}
