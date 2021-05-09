const isDev = process.env.npm_lifecycle_script  === 'vitepress dev docs';

module.exports = {
  title: 'learn-python',
  description: 'python learning',
  base: isDev? '/':'/learn-python/',
  themeConfig: {
    nav: [
      { text: 'tutorial', link: '/', activeMatch: '^/$|^/tutorial/' },
    ],
    sidebar: {
      '/tutorial/' : getTutorialSidebar(),
      '/' : getTutorialSidebar(),
    }
  }
};

function getTutorialSidebar() {
  return [
    { 
      text: '快速入门', 
      children: [
        { text: '安装', link: '/tutorial/begin' }
      ]
    },
    {
      text: '语言基础',
      children:  [
        { text: '类型', link: '/tutorial/types' },
        { text: '语句', link: '/tutorial/statement' },
        { text: '函数', link: '/tutorial/function' },
        { text: '类', link: '/tutorial/class' },
      ]
    },
    {
      text: '草稿',
      children:  [
        { text: '工具', link: '/_draft/api'},
      ]
    },
  ]
}