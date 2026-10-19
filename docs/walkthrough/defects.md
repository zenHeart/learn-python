# 发现的问题

> 每条都有：现象 → 证据 → 修复 → 验证。只列走查中真实遇到的。

## 教程内容错误

### D-01 `unpack.md` 嵌套星号解包结论错误（严重，两处）

**现象**：教程写

```python
(a, *rest), b = ([1, 2, 3], 4)
# a = [1, 2, 3], rest = [2, 3], b = 4
```

**证据**：`.walkthrough/evidence/unpack-claims-audit.py`

```
教程声称: ([1, 2, 3], [2, 3], 4)
实际得到: (1, [2, 3], 4)
```

外层目标 `(a, *rest)` 收到 `[1,2,3]` 后**还要再拆一次**，`a` 拿到 `1`。

**位置**：`docs/tutorial/unpack.md` 第六节「嵌套中用星号」+ 第七节速查表。

**修复**：两处都改为 `a=1, rest=[2,3], b=4`，并补一句「外层先拆、内层再拆」。
断言脚本同步改为断言正确值，成为回归门禁。

**验证**：22 条断言全 PASS；`npm run docs:build` 通过。

---

### D-02 错误原因诊断与实际报错不符

**现象**：教程称 `(a, b), c = (1, 2, 3)` 错误原因是「左侧2层，右侧只有1层」。

**证据**：实测 `ValueError: too many values to unpack (expected 2)`。
是**外层**目标数 2 < 右侧元素数 3，内层根本没拆到。

**修复**：改为「外层只有 2 个目标，右侧却有 3 个元素」，并注明报错点。

---

### D-03 「完整 BNF 范式」名不副实 + 括号层级误导

**现象**：教程给出两行 BNF 并称「完整」，且多处写「左侧有几个 `(...)` 右侧
就有几层」。

**证据**：四类合法目标形式未被覆盖（方括号 / 属性 / 下标 / 星号），
`a, (b, c) = 1, (2, 3)` 合法说明括号可省略。

**修复**：改名「简化 BNF 范式」，补未覆盖形式表格与括号说明；
「层级对应」改为「结构对应」。

---

## 交互块不可运行

走查时真实点击全部「▶ 运行」按钮，**27 个块中 11 个非预期报错**。
修复后 **20 个块中 0 个非预期报错**（另 2 个是教程主动标注的错误演示）。

### D-04 L1 MNIST 段整段跑不起来（最严重）

**现象**：`begin.md` 的「目标代码」「main.py」「等价的逐步写法」「练习」
四个块点击后分别报 `ModuleNotFoundError: No module named 'mnist'` 或
`NameError: name '训练集图片' is not defined`。

**根因**：浏览器里没有 `mnist` 包，而所有示例都直接从
`from mnist.data import load_data` 起手；`data.py` 示例里的四个中文名字
从未定义。

**修复**：MNIST 段开头加自包含可运行版本；TF 真实写法与 `main.py`
改 ```text；`data.py` 换成 `examples/mnist/data.py` 真实内容；
「逐步写法」与「练习」各自补可运行定义并加 print。

**验证**：L1 页面 8 个交互块全部真实点击通过，输出见
[练习证据](/walkthrough/evidence)。

---

### D-05 ASCII 箭头示意图被当 Python 执行

**现象**：`begin.md`「嵌套拆包语法拆解」块含 `↑ 第一层` 箭头行，
点击报 `IndentationError: unexpected indent`。

**修复**：该块改 ```text。

---

### D-06 标注符号 `❓` 被当 Python 执行

**现象**：`annotation.md` 两处代码块含 `❓[语法] ...`，
点击报 `SyntaxError: invalid character '❓' (U+2753)`。
标注规范页自己产出了不可运行代码。

**修复**：两处改 ```text，并说明「标注符号不是 Python 语法，要运行就得
先去掉标注」。

---

### D-07 `unpack.md` 伪代码被当 Python 执行

**现象**：4 个块报错——「完全形式」`SyntaxError: cannot assign to ellipsis`、
「(外层变量1,...) = 嵌套元组」`NameError`、MNIST 案例 `NameError: mnist`、
BNF `SyntaxError: invalid syntax`。

**修复**：4 个块改 ```text；MNIST 案例补一句指向 L1 可运行版本的链接。

---

### D-08 `examples/mnist/main.py` 从任何文档载明的 cwd 都跑不起来

**现象**：`python examples/mnist/main.py` 与 `cd examples && python mnist/main.py`
均报 `ModuleNotFoundError: No module named 'mnist'`。

**根因**：直接按路径运行时 Python 只把脚本所在目录加进 `sys.path`。
文档从未说明正确调用方式。

**修复**：`begin.md` 补 `cd examples && python -m mnist.main` 及原因解释。

---

### D-09 三引号被称作「多行注释」

**现象**：`begin.md` §3 把 `"""..."""` 叫「多行注释」，
与 `#` 混为一谈，会引出「它不占内存」的误解。

**修复**：补一段说明它是字符串表达式（函数首行时是 docstring，
可被 `__doc__` 读到），并指出「运行无输出」正说明它是求值后丢弃的表达式。

---

### D-10 `examples/statement/for-else.py` 语法错误

**现象**：文件只有 `try:` / `a+b` / `except` 三行，
`python examples/statement/for-else.py` 报 `SyntaxError: expected ':'`。

**修复**：补成完整的 for-else 与 try/except/else/finally 演示。
这是 67 个示例文件里唯一的语法错误。

---

## 死链 / 链接指错

### D-11 首页 frontmatter 死链

**现象**：`docs/index.md` hero 的「查看学习路径」指向 `/tutorial/types`，
该页不存在。真实浏览器点击 `http://localhost:5173/tutorial/types.html`
返回 404 页。

**为什么一直没被发现**：链接在 frontmatter 里，VitePress 的死链检查只覆盖
Markdown 正文，所以 `npm run docs:build` 始终通过——死链直接发布上线。

**修复**：改为 `/progress`。新增 `node .walkthrough/check-links.js` 门禁，
同时收集 frontmatter link 与正文链接，对照 dist 真实产物判定。
已做反向验证：改回 `/tutorial/types` 时门禁 exit 1，改回来 exit 0。

---

### D-12 进度页「进入第 1 课」指回首页

**现象**：`docs/progress.md` 末尾 `[进入第 1 课：Hello Python](/)`，
点过去是首页而不是第 1 课。

**修复**：改为 `/tutorial/begin`。

---

## 界面 / 代码不一致

### D-13 按钮文案与文档指引不符

**现象**：`docs/index.md` 教用户「点击蓝色的『▶ 运行』按钮」，
实际渲染的按钮文本是 `Run`；运行结束后又变成 `▶ Run`，与初始态也不一致。

**修复**：统一为「▶ 运行」（`config.js` 初始态、`theme/index.js` 恢复态、
输出区占位符），并把 Loading / Running / Error / (no output) 一并中文化。

**验证**：`dist/tutorial/begin.html` 中按钮全部为「▶ 运行」；
浏览器点击后标签运行前后一致，输出 `Hello world!\n3`。

---

## 死代码

### D-14 `docs/.vitepress/theme/pyodide-plugin.js` 失联且有语法错误

**现象**：

```bash
$ node --check docs/.vitepress/theme/pyodide-plugin.js
SyntaxError: Unexpected token ')'      # 第 6 行多余右括号

$ grep -rn "pyodidePlugin" docs/
docs/.vitepress/theme/pyodide-plugin.js:3:function pyodidePlugin(md) {
docs/.vitepress/theme/pyodide-plugin.js:36:module.exports = { pyodidePlugin }
```

只有自身定义与导出，无任何 import。它想做的事 `config.js` 已在内联实现，
且那一份没有语法错误。

**修复**：删除。`client.js` 与 `config.js` 均通过 `node --check`，行为不变。

---

## 内容宣称与事实不符

### D-15 首页宣称「15 节课」但只有 1 课存在

**现象**：`docs/index.md` feature 卡写「从基础语法到 Agent 开发，
15 节课逐步深入」。实测 `docs/` 只有 6 个 Markdown，其中教程页 4 个，
L2–L15 全部不存在（`begin.md` 末尾写「⚠️ L2 数据类型 — 敬请期待」）。

**状态**：**未修**。这属于把计划当现状宣传，改它要么删掉「15 节课」的
表述，要么把课写出来。写课超出本次走查范围，已记为待决项。

---

## 仓库卫生（记录，未改）

| 项 | 实测 | 说明 |
|----|------|------|
| `docs/.vitepress/cache/` 已被 git 跟踪 | `git ls-files docs/.vitepress` 有 12 个文件 | `.gitignore` 里写了 `.vitepress/cache`，但**已跟踪的文件不受 gitignore 约束**，所以 dev server 每次都会弄脏工作区。走查中我多次 `git checkout --` 恢复它以免混入提交 |
| Pyodide 二进制重复两份 | `docs/public/pyodide/` 19M + `docs/public/learn-python/pyodide/` 19M | dev 用前者、prod 用后者；产物 dist 里同样各一份，共约 76M |
| `docs/public/learn-python/pyodide-init.js` 失联 | `grep -rn pyodide-init` 无引用 | 是修复 stdout 捕获之前的老版本运行时代码，易被误认成生效版本 |
| 两个部署 workflow 并存 | `.github/workflows/main.yml` + `deploy.yml` | 都在 push 到 master 时构建并部署 GitHub Pages，用的是两套不同 action，存在相互覆盖风险 |
| Pyodide 被加载两次 | 页面 script 列表同时有 `/pyodide/pyodide.js` 与 CDN `pyodide.js` | `config.js` head 注入 CDN，`theme/index.js` 又注入本地。当前版本一致（0.24.1）但存在漂移风险，且浪费一次下载 |
