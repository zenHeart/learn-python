# 练习证据

> 只保留**可复核**的记录：每条都有命令、输出和复现方式。
> 原始日志在 `.walkthrough/evidence/`。

## 复现方式

```bash
bash .walkthrough/run-all.sh          # 重新生成本页除浏览器外的全部证据
node .walkthrough/check-links.js      # 链接门禁（需先 npm run docs:build）
```

浏览器/Pyodide 证据需按 `.walkthrough/evidence/browser-podide-runs.md`
记录的步骤用 Playwright 复跑（需要 dev server + 浏览器）。

> ⚠️ **本轮（第三轮）没有复跑浏览器证据**：Playwright MCP 服务本次会话连接失败
> （`CONNECTION_CLOSED`），无法真实点击「▶ 运行」按钮。
> 因此本轮新增的 5 个走查笔记页面里的 `python` 代码块，
> **只在本地 CPython 3.11.9 下验证过**（与 Pyodide 0.24.1 的 Python 3.11 同版本），
> 未在浏览器里实测。这不满足本笔记自己定的
> 「浏览器/Pyodide 练习真实点击，不用静态检查冒充完成」标准，
> 所以这 5 页的交互块状态标为 **未验证**，不冒充已通过。
> 等 MCP 恢复后需按 `browser-podide-runs.md` 的步骤补跑。

---

## 一、examples/ 全部 66 个文件

命令（`run-all.sh` 内部）：

```bash
for f in $(find examples -name '*.py' | sort); do python "$f" </dev/null; done
```

### 汇总

| 状态 | 数量 |
|------|------|
| 直接运行通过 | 58 |
| 需要交互 stdin | 7 |
| 需要正确的模块调用方式 | 1 |
| 合计 | 66 |

> 「直接运行通过」从 61 降到 58、「需要交互 stdin」从 5 升到 7：
> `statement/try.py` 和 `statement/finally.py` 原本用裸 `except:` 把 `EOFError`
> 吞掉，所以在 `/dev/null` 下也显示 exit 0；改成正确的 `except ValueError:` 之后
> EOF 正常逃出（D-26）。**数字变了，但更诚实。**

### 需要交互 stdin 的 7 个（已用管道送值验证通过，不是缺陷）

| 文件 | `echo 7 \| python <file>` 的输出 |
|------|------------------------------|
| `examples/statement/if.py` | `enter a number: `（7 是奇数故无第二行） |
| `examples/statement/elif.py` | `enter a number: positive` |
| `examples/statement/else.py` | `enter a number: a is odd number` |
| `examples/statement/try.py` | `Please enter a number: x is a valid number: 7` |
| `examples/statement/finally.py` | `Please enter a number: x is a valid number: 7` / `over` |
| `examples/function/def.py` | `enter a number:0 1 1 2 3 5 8 ` |
| `examples/_draft/31-if.py` | `please enter a number: x is odd number` |

`try.py` 送 `abc` 时输出 `Please enter a number: Oops! That was not a valid number.`
（`except ValueError` 生效，退出码 0）——反向确认窄捕获仍然工作。

### mnist 的调用方式

```
$ python examples/mnist/main.py
ModuleNotFoundError: No module named 'mnist'      # 直接按路径跑，examples/ 不在 sys.path

$ cd examples && python -m mnist.main
训练集图片: [1, 2, 3]
训练集标签: [0, 1, 2]
测试集图片: [4, 5]
测试集标签: [1, 0]

--- 结构验证 ---
train_images 类型: list
train_labels 类型: list
训练集数量: 3
测试集数量: 2
```

### 修掉的真实缺陷：`examples/statement/for-else.py`

原文件只有三行且不完整（本身就是语法错误，所以用 `text` 标注）：

```text
try:
  a+b
except
```

`python examples/statement/for-else.py` 直接
`SyntaxError: expected ':'`（`except` 缺异常类型与冒号，函数体为空）。
已补成完整演示，修复后该文件运行通过。这是全部示例文件里唯一的语法错误。

---

## 二、浏览器 / Pyodide 交互块

启动：

```bash
npm install
npm run docs:dev        # ➜ Local: http://localhost:5173/
```

驱动：Playwright 逐个点击 `.py-demo-run`，等待按钮脱离 `running` 类后
读取 `.py-demo-output` 文本。

### 汇总（修复后复跑，覆盖全部 14 个页面）

| 页面 | 交互块 | 正常 | 教程主动标注的错误演示 | 非预期报错 |
|------|-------|------|---------------------|-----------|
| `/` | 1 | 1 | 0 | 0 |
| `/progress` | 1 | 1 | 0 | 0 |
| `/tutorial/begin`（L1） | 9 | 9 | 0 | 0 |
| `/tutorial/annotation` | 0 | — | — | 0 |
| `/tutorial/gaps` | 0 | — | — | 0 |
| `/tutorial/unpack` | 10 | 8 | 2 | 0 |
| `/walkthrough/*`（8 页） | 12 | 11 | 0 | 0 |
| **合计** | **33** | **30** | **3** | **0** |

> `/walkthrough/*` 那 12 块里有 1 块是走查笔记自己写错的片段（依赖不存在的
> `demopkg` 包），第二轮自查时改成 `text`，所以正常数是 11 不是 12。

> 修复前原有 6 个页面是 **27 个块中 11 个非预期报错**。

### L1 逐块输出（修复后）

| # | 代码首行 | 输出 |
|---|---------|------|
| 1 | `print("Hello world!")` | `Hello world!` / `3` |
| 2 | `name = "Python"` | `我叫Python，今年18岁` |
| 3 | `# 这是单行注释` | `(运行完成，但没有 print 输出——这段代码只做赋值)` |
| 4 | `def load_data():`（自包含版） | `训练集图片: [1, 2, 3]` / `训练集标签: [0, 1, 2]` / `测试集图片: [4, 5]` / `测试集标签: [1, 0]` |
| 5 | `def load_data():`（data.py 内容） | `(运行完成，但没有 print 输出——这段代码只做赋值)` |
| 6 | `def load_data():`（逐步写法） | `result = (([1, 2, 3], [0, 1, 2]), ([4, 5], [1, 0]))` / `train_set = ([1, 2, 3], [0, 1, 2])` / `test_set  = ([4, 5], [1, 0])` / `train_images = [1, 2, 3] \| train_labels = [0, 1, 2]` / `test_images  = [4, 5] \| test_labels  = [1, 0]` |
| 7 | 练习 1 | `整体结构: tuple` / `第1个元素（训练集）: ([1, 2, 3], [0, 1, 2])` / `第2个元素（测试集）: ([4, 5], [1, 0])` / `一共几层: 2` |
| 8 | 练习 2 | `训练图片: [1, 2, 3]` / `训练标签: [0, 1, 2]` / `测试图片: [4, 5]` / `测试标签: [1, 0]` / `拆包结果与整体结构一致: True` |

### unpack.html 两个「报错即预期」的块

| # | 代码 | 输出 |
|---|------|------|
| 7 | `a, b, c = (1, 2)` | `ValueError: not enough values to unpack (expected 3, got 2)` |
| 8 | `(a, b), c = (1, 2, 3)` | `ValueError: too many values to unpack (expected 2)` |

教程在 `## 五、常见错误` 里主动用这两段演示错误，所以报错是**预期行为**。
但输出区把完整 traceback 直接铺开，对初学者是噪音——已记为待改进项
（见 [未解决与恢复点](/walkthrough/open)）。

---

## 三、门禁

| 门禁 | 命令 | 当前结果 |
|------|------|---------|
| 文档构建 | `npm run docs:build` | ✅ 通过 |
| 链接（含 frontmatter） | `node .walkthrough/check-links.js` | ✅ 通过（含反向验证） |
| 拆包断言 | `python .walkthrough/evidence/unpack-claims-audit.py` | ✅ 22 PASS / 0 FAIL |
| 概念断言（第二轮：导入 / 数据类型 / 应用场景） | `python .walkthrough/evidence/concepts-round2-audit.py` | ✅ 22 PASS / 0 FAIL |
| **examples 断言（第三轮：66 个文件的注释结论）** | `python .walkthrough/evidence/examples-claims-audit.py` | ✅ **256 PASS / 0 FAIL** |
| examples 运行 | `bash .walkthrough/run-all.sh` | ✅ 58 通过 / 8 需交互或特定调用方式 |
| 浏览器交互块 | Playwright 逐块点击 | ⚠️ 上轮 33 块 0 非预期报错；**本轮未复跑**（MCP 连接失败） |

> 仓库**没有** pytest / 单元测试，`package.json` 原有脚本只有
> `docs:dev` / `docs:build` / `docs:serve`。上表后五项是走查新增的门禁，
> 已接进 `npm run check`。

### 门禁自身的问题（D-31）

前两个 Python 门禁原来**只打印 FAIL 却不设退出码**，所以 `run-all.sh` 里的

```bash
rc=$?
if [ "$rc" -ne 0 ]; then ... exit "$rc"; fi
```

是**死代码**——`rc` 永远是 0，`npm run check` 永远通过，教程改错了也照绿。
本轮给两个门禁补上 `sys.exit(1)`，新增的 examples 门禁一开始就带退出码。

**反向验证**：把 examples 门禁里 A1 的期望值改回教程原来的错误值 `1.3`，
门禁 exit 1、报 `255 PASS / 1 FAIL`；改回来 exit 0、`256 PASS`。

