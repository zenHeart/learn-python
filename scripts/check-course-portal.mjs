import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const portal = fs.readFileSync(path.join(root, 'docs/tutorial/course-portal.md'), 'utf8')
const requiredLocal = [
  'docs/tutorial/learning-path.md',
  'docs/tutorial/diagnostic.md',
  'docs/tutorial/backend-foundation.md',
  'docs/tutorial/agent-loop.md',
  'docs/tutorial/retrieval-pipeline.md',
  'docs/tutorial/knowledge-base-agent.md',
  'docs/tutorial/pi-agent-runtime.md',
]
for (const file of requiredLocal) {
  if (!fs.existsSync(path.join(root, file))) throw new Error(`missing local course file: ${file}`)
}
for (const url of [
  'https://github.com/zenHeart/learn-java',
  'https://github.com/zenHeart/learn-engineering/tree/main/docs/go',
  'https://github.com/zenHeart/learn-llm',
  'https://github.com/zenHeart/evals/tree/main/data/eval-specs',
]) {
  if (!portal.includes(url)) throw new Error(`missing cross-course link: ${url}`)
}
console.log('course portal contract passed')
