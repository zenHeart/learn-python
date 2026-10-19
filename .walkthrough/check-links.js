#!/usr/bin/env node
// 文档链接门禁
//
// VitePress 的死链检查只覆盖 Markdown 正文里的链接，不覆盖 frontmatter 中的
// link 字段（例如 index.md 的 hero.actions[].link）。本次走查就抓到过一个
// 只存在于 frontmatter 的死链：/tutorial/types。
//
// 本脚本把两类链接都收集起来，对照 docs/.vitepress/dist 里的真实产物判定死活。
//
// 用法：node .walkthrough/check-links.js   （需先 npm run docs:build）

const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '..')
const DOCS = path.join(ROOT, 'docs')
const DIST = path.join(DOCS, '.vitepress', 'dist')

if (!fs.existsSync(DIST)) {
  console.error('找不到 docs/.vitepress/dist，请先运行 npm run docs:build')
  process.exit(2)
}

/** 递归收集 srcDir 下的 .md 文件 */
function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name)
    const st = fs.statSync(p)
    if (st.isDirectory()) {
      if (name === '.vitepress' || name === 'public' || name === 'cache') continue
      walk(p, out)
    } else if (name.endsWith('.md')) {
      out.push(p)
    }
  }
  return out
}

/** 站内路由 -> dist 中的实际文件 */
function routeExists(route) {
  // 去掉 hash / query
  const clean = route.split('#')[0].split('?')[0]
  if (clean === '' || clean === '/') {
    return fs.existsSync(path.join(DIST, 'index.html'))
  }
  const rel = clean.replace(/^\/+/, '')
  const asHtml = path.join(DIST, rel + '.html')
  const asIndex = path.join(DIST, rel, 'index.html')
  const asFile = path.join(DIST, rel)
  if (fs.existsSync(asHtml) || fs.existsSync(asIndex)) return true
  if (fs.existsSync(asFile) && fs.statSync(asFile).isFile()) return true
  return false
}

const mdFiles = walk(DOCS)
const problems = []
let checked = 0

for (const file of mdFiles) {
  const text = fs.readFileSync(file, 'utf8')
  const rel = path.relative(ROOT, file).replace(/\\/g, '/')

  // 1) frontmatter 中的 link 字段
  const fmMatch = text.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  if (fmMatch) {
    for (const m of fmMatch[1].matchAll(/^\s*(?:-\s*)?link:\s*['"]?([^'"\s]+)['"]?\s*$/gm)) {
      const link = m[1]
      if (/^https?:|^mailto:|^\/\//.test(link)) continue
      checked++
      if (!routeExists(link)) problems.push(`${rel}  [frontmatter link] -> ${link}`)
    }
  }

  // 2) 正文 Markdown 链接  [text](target)
  const body = fmMatch ? text.slice(fmMatch[0].length) : text
  for (const m of body.matchAll(/\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g)) {
    const link = m[1]
    if (/^https?:|^mailto:|^\/\//.test(link)) continue
    if (link.startsWith('#')) continue
    checked++
    if (!routeExists(link)) problems.push(`${rel}  [body link] -> ${link}`)
  }
}

console.log(`检查 ${mdFiles.length} 个 Markdown 文件，${checked} 个站内链接。`)
if (problems.length) {
  console.error(`\n发现 ${problems.length} 个死链：`)
  for (const p of problems) console.error('  ' + p)
  process.exit(1)
}
console.log('没有死链。')
