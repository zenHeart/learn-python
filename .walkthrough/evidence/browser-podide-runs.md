# 浏览器 / Pyodide 真实运行记录

环境：Windows 11, Node v24.16.0, VitePress v1.6.4, Pyodide v0.24.1
启动命令：`npm run docs:dev`  （➜ Local: http://localhost:5173/）
驱动方式：Playwright 真实点击每个 `.py-demo-run` 按钮，读取 `.py-demo-output` 文本
抓取时间：2026-10-20

判定口径：
  PASS      = 真实输出，且与教程声称的结果一致
  NOOUT     = 代码合法执行但无 print（本身不是缺陷，但学习者无法确认是否成功）
  INTENDED  = 教程主动标注「❌ 错误」的演示，报错即预期
  BROKEN    = 非预期报错，学习者被卡住

## 最终状态（全部修复后复跑）

覆盖全部 14 个页面（6 个原有 + 8 个走查笔记）：

| 指标 | 数值 |
|------|------|
| 交互块总数 | 30 |
| 正常运行 | 27 |
| 教程主动标注的错误演示（报错即预期） | 3 |
| **非预期报错** | **0** |

## 修复前的状态

27 个交互块中 11 个（40.7%）非预期报错。站点在 progress.md 自称
「浏览器端运行 Python ✅ 完成」。


## 逐页明细（最终状态）

### / (index.md) — 1 块
[1] PASS   输出: Hello, Python! Welcome to learn-python.

### /progress.html — 1 块
[1] PASS   输出: Hello, Python! / Welcome to learn-python!

### /tutorial/begin.html (L1) — 8 块
[1] PASS   输出: Hello world! / 3
[2] PASS   输出: 我叫Python，今年18岁
[3] NOOUT  输出: (运行完成，但没有 print 输出——这段代码只做赋值)
[4] PASS   输出: 训练集图片: [1, 2, 3] / 训练集标签: [0, 1, 2] / 测试集图片: [4, 5] / 测试集标签: [1, 0]
[5] NOOUT  输出: (运行完成，但没有 print 输出——这段代码只做赋值)
[6] PASS   输出: result = (([1, 2, 3], [0, 1, 2]), ([4, 5], [1, 0]))
                 train_set = ([1, 2, 3], [0, 1, 2])
                 test_set  = ([4, 5], [1, 0])
                 train_images = [1, 2, 3] | train_labels = [0, 1, 2]
                 test_images  = [4, 5] | test_labels  = [1, 0]
[7] PASS   输出: 整体结构: tuple / 第1个元素（训练集）: ([1, 2, 3], [0, 1, 2])
                 第2个元素（测试集）: ([4, 5], [1, 0]) / 一共几层: 2
[8] PASS   输出: 训练图片: [1, 2, 3] / 训练标签: [0, 1, 2] / 测试图片: [4, 5]
                 测试标签: [1, 0] / 拆包结果与整体结构一致: True

### /tutorial/annotation.html — 0 块（❓ 标注块已改 text）
### /tutorial/gaps.html — 0 块

### /tutorial/unpack.html — 10 块
[1]  NOOUT  a, b = (1, 2)
[2]  NOOUT  a, b = [1, 2] / a, b = "xy" / a, b, c = range(3)
[3]  NOOUT  (a, b), (c, d) = ((1, 2), (3, 4))
[4]  NOOUT  (point1, point2), (point3, point4) = ((1, 2), (3, 4))
[5]  NOOUT  def get_user_group(): ...
[6]  NOOUT  (a, (b, c)), (d, e) = ((1, (2, 3)), (4, 5))
[7]  INTENDED  a, b, c = (1, 2) → ValueError: not enough values to unpack (expected 3, got 2)
[8]  INTENDED  (a, b), c = (1, 2, 3) → ValueError: too many values to unpack (expected 2)
[9]  NOOUT  first, *middle, last = [1, 2, 3, 4, 5]
[10] NOOUT  (a, *rest), b = ([1, 2, 3], 4)

### /walkthrough/* — 11 块，全部 PASS（含 L1 走查笔记里的概念验证片段）


## 附带发现（非练习，但影响学习路径）

1. 按钮文案与文档不一致（已修）
   - 修复前实际渲染按钮文本：Run；docs/index.md 教用户点「▶ 运行」
   - 运行结束后又变成 "▶ Run"，与初始态不一致
   - 已统一为「▶ 运行」，浏览器实测运行前后标签一致

2. Pyodide 被加载两次（未修，见 docs/walkthrough/open.md O-04）
   页面 script 列表同时存在：
     - http://localhost:5173/pyodide/pyodide.js        （theme/index.js 注入）
     - https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js（config.js head 注入）
   两者版本目前一致（0.24.1），但存在版本漂移风险且浪费一次 19MB 级下载。

3. 死链（真实点击验证，已修）
   - http://localhost:5173/tutorial/types.html → 404 页
   - 来源：docs/index.md hero.actions[1].link: /tutorial/types
   - 该链接位于 frontmatter，VitePress 的死链检查不覆盖，docs:build 通过。

4. docs/.vitepress/theme/pyodide-plugin.js 第 6 行有语法错误（多余右括号），
   且该文件未被任何地方 import，是死代码 + 语法错误。已删除。
   复核命令：
       node --check docs/.vitepress/theme/pyodide-plugin.js
       → SyntaxError: Unexpected token ')'  (line 6)
       grep -rn "pyodidePlugin" docs/ → 仅自身定义与导出，无任何引用
   注意：真正生效的是 docs/.vitepress/config.js 内联的同名逻辑（那一份没有语法错误）。
   client.js 与 config.js 均通过 node --check，无语法错误。

5. 响应式（375px 视口实测）
   coverage 页有两张表宽于视口（522px / 419px vs 360px）。
   VitePress 默认给 markdown 表格设 display:block; overflow-x:auto，
   表格内部横向滚动，无页面级溢出、无裁剪。走查笔记沿用该模式，
   未新增自定义样式。
