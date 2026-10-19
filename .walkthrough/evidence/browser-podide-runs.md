# 浏览器 / Pyodide 真实运行记录
#
# 环境：Windows 11, Node v24.16.0, VitePress v1.6.4, Pyodide v0.24.1
# 启动命令：npm run docs:dev  （➜ Local: http://localhost:5173/）
# 驱动方式：Playwright 真实点击每个 `.py-demo-run` 按钮，读取 `.py-demo-output` 文本
# 抓取时间：2026-10-20
#
# 判定口径：
#   PASS   = 真实输出，且与教程声称的结果一致
#   NOOUT  = 代码合法执行但无 print（本身不是缺陷，但学习者无法确认是否成功）
#   INTENDED = 教程主动标注「❌ 错误」的演示，报错即预期
#   BROKEN = 非预期报错，学习者被卡住

## 汇总

| 页面 | 可运行块 | PASS | NOOUT | INTENDED | BROKEN |
|------|---------|------|-------|----------|--------|
| / (index.md) | 1 | 1 | 0 | 0 | 0 |
| /progress.html | 1 | 1 | 0 | 0 | 0 |
| /tutorial/begin.html (L1) | 9 | 2 | 2 | 0 | 5 |
| /tutorial/annotation.html | 2 | 0 | 0 | 0 | 2 |
| /tutorial/gaps.html | 0 | 0 | 0 | 0 | 0 |
| /tutorial/unpack.html | 14 | 0 | 8 | 2 | 4 |
| **合计** | **27** | **4** | **10** | **2** | **11** |

结论：27 个交互块中 11 个（40.7%）在真实浏览器里非预期报错。
站点在 progress.md 自称「浏览器端运行 Python ✅ 完成」。


## 逐块明细

### / (index.md) — 1 块
[1] PASS
代码:
    # 试试修改下面的代码，然后点击运行
    name = "Python"
    print(f"Hello, {name}! Welcome to learn-python.")
输出:
    Hello, Python! Welcome to learn-python.


### /progress.html — 1 块
[1] PASS
代码:
    # 第一个 Python 程序
    name = "Python"
    print(f"Hello, {name}!")
    print("Welcome to learn-python!")
输出:
    Hello, Python!
    Welcome to learn-python!


### /tutorial/begin.html (L1) — 9 块
[1] PASS
代码: print("Hello world!") / print(1 + 2)
输出: Hello world!
      3

[2] PASS
代码: name = "Python" / age = 18
输出: 我叫Python，今年18岁

[3] NOOUT   （仅注释，合法；无输出符合预期）
代码: # 这是单行注释 / """
输出: (no output)

[4] BROKEN
代码: from mnist.data import load_data
      (train_images, train_labels), (test_images, test_labels) = load_data()
输出: ModuleNotFoundError: No module named 'mnist'
说明: L1 的头号目标代码在浏览器里无法运行。教程只说「MNIST 示例使用纯 Python
      模拟返回值结构」，但从未给出在浏览器里定义 load_data 的办法。

[5] NOOUT   （只有 def，合法；但函数体里的 训练集图片 是未定义名字）
代码: def load_data(): /     return (训练集图片, 训练集标签), (测试集图片, 测试集标签)
输出: (no output)
说明: 教程把这段当作「data.py — 定义数据加载函数」展示，但它不是可运行代码。

[6] BROKEN
代码: from mnist.data import load_data / (train_images, train_labels), ... = load_data()
输出: ModuleNotFoundError: No module named 'mnist'

[7] BROKEN
代码: # load_data() 返回的是嵌套元组：
      ((train_images, train_labels), (test_images, test_labels))
      ...
          ↑ 第一层                    ↑ 第一层
输出: IndentationError: unexpected indent  （行 6: ↑ 第一层）
说明: 教程把 ASCII 箭头示意图放进 ```python 代码块，导致交互引擎把它当 Python 执行。

[8] BROKEN
代码: # 原始返回值
      result = load_data()
输出: NameError: name '训练集图片' is not defined
      （File "<exec>", line 2, in load_data）

[9] BROKEN
代码: # 1. 尝试用一个变量接住整个返回值，打印它的结构
      data = load_data()
输出: NameError: name '训练集图片' is not defined
说明: 这是 L1 的正式「练习」区，两行练习都跑不起来。


### /tutorial/annotation.html — 2 块
[1] BROKEN
代码: # 标注 + 分类
      ❓[语法] from tensorflow.keras.datasets import mnist
输出: SyntaxError: invalid character '❓' (U+2753)
说明: 标注符号 ❓ 被直接写进 ```python 代码块。标注规范页自己产出了不可运行代码。

[2] BROKEN
代码: # L1 代码示例
      print("hello")  # ✅ 理解
      ❓[语法] (a, b), (c, d) = nested_tuple()  # 嵌套拆包
输出: SyntaxError: invalid character '❓' (U+2753)


### /tutorial/gaps.html — 0 块
无交互代码。


### /tutorial/unpack.html — 14 块
[1]  NOOUT  a, b = (1, 2)
[2]  BROKEN (变量1, 变量2, ...) = (值1, 值2, ...)
      → SyntaxError: cannot assign to ellipsis
      说明: 「完全形式」是伪代码，被放进 ```python 后不可执行。
[3]  NOOUT  a, b = [1, 2] / a, b = "xy" / a, b, c = range(3)
[4]  NOOUT  (a, b), (c, d) = ((1, 2), (3, 4))
[5]  BROKEN (外层变量1, 外层变量2), ... = 嵌套元组
      → NameError: name '嵌套元组' is not defined
[6]  BROKEN (train_images, train_labels), ... = mnist.load_data()
      → NameError: name 'mnist' is not defined
[7]  NOOUT  (point1, point2), (point3, point4) = ((1, 2), (3, 4))
[8]  NOOUT  def get_user_group(): ...
[9]  BROKEN 目标表达式 := 变量 | (目标表达式, 目标表达式, ...)
      → SyntaxError: invalid syntax
      说明: BNF 范式不是 Python，放进 ```python 必然报错。
[10] NOOUT  (a, (b, c)), (d, e) = ((1, (2, 3)), (4, 5))
[11] INTENDED a, b, c = (1, 2) → ValueError: not enough values to unpack (expected 3, got 2)
[12] INTENDED (a, b), c = (1, 2, 3) → ValueError: too many values to unpack (expected 2)
[13] NOOUT  first, *middle, last = [1, 2, 3, 4, 5]
[14] NOOUT  (a, *rest), b = ([1, 2, 3], 4)
      注意: 该块注释声称 `a = [1, 2, 3]`，实际 a = 1。见 unpack-claims-audit.log。


## 附带发现（非练习，但影响学习路径）

1. 按钮文案与文档不一致
   - 实际渲染按钮文本：Run
   - docs/index.md L47 教用户：「点击蓝色的『▶ 运行』按钮」
   - docs/.vitepress/theme/pyodide-plugin.js 里写的才是「▶ 运行」，但该文件未被
     index.js 导入，是死代码。

2. Pyodide 被加载两次
   页面 script 列表同时存在：
     - http://localhost:5173/pyodide/pyodide.js        （theme/index.js 注入）
     - https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js（config.js head 注入）
   两者版本目前一致（0.24.1），但存在版本漂移风险且浪费一次 19MB 级下载。

3. 死链（真实点击验证）
   - http://localhost:5173/tutorial/types.html → 404 页
   - 来源：docs/index.md hero.actions[1].link: /tutorial/types
   - 该链接位于 frontmatter，VitePress 的死链检查不覆盖，`npm run docs:build` 通过。

4. docs/.vitepress/theme/pyodide-plugin.js 第 6 行有语法错误（多余右括号），
   且该文件未被任何地方 import，是死代码 + 语法错误。
   复核命令：
       node --check docs/.vitepress/theme/pyodide-plugin.js
       → SyntaxError: Unexpected token ')'  (line 6)
       grep -rn "pyodidePlugin" docs/ → 仅自身定义与导出，无任何引用
   注意：真正生效的是 docs/.vitepress/config.js 内联的同名逻辑（那一份没有语法错误）。
   client.js 与 config.js 均通过 node --check，无语法错误。
