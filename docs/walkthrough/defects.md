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
这是全部示例文件里唯一的语法错误。

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

## 第二轮走查补充发现

第一轮漏掉了 `begin.md` 的两张表格（「Python 模块导入语法」、
「对比 Python 内置数据类型」）和 `unpack.md` 第八节「应用场景」的三行。
补齐时各写一条断言，又抓出两个问题。

### D-16 教程自己的导入表示例跑不通

**现象**：`begin.md` 导入语法表第四行写 `from mnist.data import a, b`。
实测（`cd examples` 后）：

```
ImportError: cannot import name 'a' from 'mnist.data'
```

`mnist.data` 实际只导出 `load_data`：

```bash
cd examples
python -c "import mnist.data as d; print([n for n in dir(d) if not n.startswith('_')])"
# ['load_data']
```

**根因**：表格把「通用语法形式」写成了「对着 mnist 能跑的代码」，
学习者照抄就报错。

**修复**：表格里注明前四行是通用形式、不是都能对 `mnist` 跑通，
并给出上面那条可自行验证的命令。

**验证**：`.walkthrough/evidence/concepts-round2-audit.py` 形式4 反例断言
确认这行确实抛 `ImportError`。

---

### D-17 星号解包的结果类型教程没说，容易搞错

**现象**：`unpack.md` 第六节只说 `middle = [2, 3, 4]`，没说这个列表
是**必然**的。我原以为 `rest` 的类型会跟着右侧容器走。

**证据**：右侧分别是元组、字符串、range 时，星号目标收集到的都仍是 `list`：

```
列表     a=1   rest=[2, 3, 4]   type(rest)=list
元组     a=1   rest=[2, 3, 4]   type(rest)=list
字符串    a='a' rest=['b','c','d'] type(rest)=list
range   a=0   rest=[1, 2, 3]   type(rest)=list
```

**修复**：在第六节补一段说明「星号目标收集到的永远是 list」，
并补上 `a, *b, c = [1]` 的 `ValueError` 边界情况。

---

### D-18 数据类型表只说结论、不给验证手段

**现象**：`begin.md`「对比 Python 内置数据类型」是一张四行表，
写「元组（不可变）」「列表（可变）」「集合 无序、去重」，
但没有任何可运行代码，学习者只能选择信或不信。

**修复**：表后补一段可运行代码，把四条性质各自演示一遍
（元组改元素抛 `TypeError`、列表可改可加、集合去重且不可下标、
字典按键取值可增键），并补一条「空 `{}` 是 dict 不是 set」。

**验证**：浏览器实测该块输出
`列表 -> [99, 2, 3]` / `集合长度 -> 3 元素 -> {1, 2, 3}` / `字典 -> {'x': 1, 'y': 2}`。


---

## 第三轮走查补充发现

第三轮把 `examples/` 下 **66** 个文件逐条核对（前两轮只核对了 `docs/` 教程正文，
`run-all.sh` 也只证明「进程退出码为 0」，不证明注释里写的结论是对的）。
每条结论写进了 `.walkthrough/evidence/examples-claims-audit.py`，共 **256** 条断言。

### D-19 `examples/number/converter.py` 注释写的值和实际输出不符

**现象**：第一行注释写 `print(1.1 + 1.2) # 1.3`。

**证据**：实测输出 `2.3`。

```
教程声称: '1.3'
实际得到: '2.3'
```

**同类两处**：`print(1e5) # 100000` 实际输出 `100000.0`（科学计数法字面量
**类型就是 float**，注释漏了 `.0`，会让人以为是 int）；
`1j * 1j` / `1j / 1j` 的注释写 `-1 + 0j` / `1 + 0j`，实际 repr 带括号
`(-1+0j)` / `(1+0j)`。

**修复**：四处注释按实测改正，并给 `1e5` 补类型说明。

**验证**：`examples-claims-audit.py` A1–A17 全 PASS。

---

### D-20 `examples/string/quote.py` 注释给输出加了不存在的反斜杠

**现象**：`print('"Isn\'t," they said.') # "Isn\'t," they said.`

**证据**：实际输出 `"Isn't," they said.`——`\'` 的转义在词法阶段就处理掉了，
反斜杠不出现在输出里。注释让人以为输出带反斜杠。

**修复**：注释改为真实输出，并注明「`\'` 的转义不出现在输出里」。

---

### D-21 `examples/string/slice.py` 唯一一行没有注释的结果是空行

**现象**：`print(a[7:9])` 上方只有一句「不报错，返回空」，
点运行后输出区是一个空行。

**为什么是缺陷**：站点大量交互块的「空输出」已被学习者反馈过分不清
「成功但没 print」和「坏了」（见 O-07）。这里连注释都没说清，
初学者看到空行会以为程序出错。

**修复**：注释补明「下标越界会抛 `IndexError`，但切片越界不报错，
返回空字符串」，行尾加 `# （空）`。

---

### D-22 `examples/list/list_order.py` 两处注释词不达意

**现象 1**：`# 字典排序,注意 list 必须为同一类型否则会报错`
——「字典排序」想说的是「按字符编码排序」，但字面读起来像「用字典排」。

**现象 2**：`# sorted 不该边原始排序`——「不该边」是错别字，
整句无法解读（应为「不会改变原列表」）。

**证据**：实测 `sorted(['A','tom','jerry','jack','1'])`
→ `['1', 'A', 'jack', 'jerry', 'tom']`，顺序来自码位
`'1'`(49) < `'A'`(65) < `'a'`(97) < `'j'`(106)，
**和人类字典序不是一回事**（数字 < 大写 < 小写）。

**修复**：改成「按字符编码（码位）排序」并补混类型的 `TypeError` 全文；
第二处改成「`sorted()` 不改变原列表，返回排好序的新列表」。

**验证**：断言 C17–C23。

---

### D-23 `examples/list/list_search.py` 错别字「第一各元素」

**现象**：`# 第一各元素`，应为「第一个元素」。

**修复**：改正。同类小错不影响运行，但教程素材里出现错别字会削弱可信度。

---

### D-24 `examples/api/string-operation.py` 打印标签拼错方法名

**现象**：`print("str.rstripe():", ...)`——真实方法名是 `rstrip`。

**证据**：`hasattr(str, 'rstripe')` → `False`，`hasattr(str, 'rstrip')` → `True`。

**修复**：标签改为 `str.rstrip()`。

---

### D-25 `examples/statement/break.py` 注释语义与代码相反

**现象**：`break` 上方写 `# jump to loop`（跳到循环）。

**证据**：`break` 是**跳出**整个循环。该示例输出
`first element greater 2 index:  2` 之后循环就结束了。

**修复**：改成「`break` 跳出整个 while 循环，后面的迭代不再执行」。

---

### D-26 `statement/try.py` / `finally.py` 裸 `except:` + 输入合法时文案说非法

**现象 1**：裸 `except:` 捕获一切。
**证据**：子进程实测——

```
try:
    raise KeyboardInterrupt
except:
    print('swallowed')
→ swallowed（exit 0）
```

Ctrl+C 被吃掉，程序停不下来。

**现象 2**：`print('x is illegal number')` 在 `try` 里、`int(input())`
**成功之后**执行。送 `7` 进去走的就是这行——**数字是合法的，文案却说它非法**。
另外 `"Oops!  That was no valid number."` 语法也不对。

**修复**：两处都改成 `except ValueError:`（附注释说明为什么不能用裸 except），
文案改成 `'x is a valid number:'` 和 `"Oops! That was not a valid number."`。

**代价（如实记录）**：改成窄捕获后，`input()` 遇到 EOF 不再被吞，
`run-all.sh`（stdin 接 `/dev/null`）里这两个文件的退出码从 0 变成 1。
「需要交互 stdin」的示例数因此从 5 个变成 7 个——**这反而更诚实**：
它们确实需要输入，此前只是被裸 except 掩盖了。

**验证**：断言 F18–F21 + F13–F15；反向验证 `except ValueError` 仍能抓住 `'abc'`。

---

### D-27 `examples/_draft/42-function-attributes.py` 把本机绝对路径和内存地址写进提交物

**现象**：示例打印 `hi.__globals__` 和 `say.__code__`。

**证据**：`.walkthrough/evidence/examples-run.md` 里因此出现

```
<code object say at 0x0000027811FE0A80, file "C:\Users\cheng\...\42-function-attributes.py", line 16>
{'__name__': '__main__', ..., '__file__': 'C:\\Users\\cheng\\...', ...}
```

内存地址每次运行都变，绝对路径随机器变——**这两行让「可复现证据」变成不可复现**，
还把开发机路径提交进了仓库。

**修复**：删掉 `print(hi.__globals__)`；`say.__code__` 换成确定性的
`say.__code__.co_varnames`（输出 `('tom',)`）。

---

### D-28 `examples/_draft/21.types-number.py` 注释说 `//` 总返回 int

**现象**：`# // divide operatr always a floor divide,return a integer`

**证据**：`3 // 2` → `1`（int），但 `3 // 2.` → `1.0`（**float**）。
**有一边是 float 时 `//` 返回 float。**

**修复**：注释改明「两边都是 int 才返回 int；有一边是 float 时返回 float」。
同类规则在 `_draft/12-use-variable.py` 里也有（`17.0 // 3` → `5.0`），已一并核对。

---

### D-29 `examples/_draft/11-define-variable.py` 是 0 字节空文件

**现象**：`wc -c` 得 0。运行后无任何输出、退出码 0。

**为什么是缺陷**：一个「定义了却什么都不做」的示例，
学习者点运行看到空输出，无法区分「成功」和「坏了」（同 D-21）。

**修复**：删除。`examples/` 文件数因此从 67 变为 **66**，
所有笔记里的计数已同步改正。

---

### D-30 13 个示例用 `list` / `map` / `str` 当变量名，遮蔽内建

**现象**：`examples/list/*`（6 个）、`examples/map/*`（5 个）、
`examples/api/*`（2 个）共 13 个文件写 `list = [...]` / `map = {...}` / `str = "..."`。

**证据**：子进程实测——

```
list = [1, 2, 3]
list('abc')        # TypeError: 'list' object is not callable
```

学习者照抄后，同一脚本里再用内建 `list()` / `map()` / `str()` 就炸。
这是「教语法时顺带教了坏习惯」。

**修复**：`list` → `items`、`map` → `profile`、`str` → `text`，
共重写 12 个文件（`list_order.py` 单独补改）。打印标签里描述**语法**的
（如 `'list[0]:'`）保留不变，只改变量名。

**验证**：门禁新增回归断言「用内建名当变量名的示例文件应为 0 个」；
`grep -rn "^\s*\(list\|map\|str\)\s*=" examples/` 实测 0 处。

---

### D-31 三个断言门禁原来都不设退出码，`run-all.sh` 的失败判断是死代码

**现象**：`unpack-claims-audit.py` 和 `concepts-round2-audit.py`
只在屏幕上打印 `FAIL 明细`，然后**正常结束**（exit 0）。

**证据**：`grep -n "sys.exit\|exit(" 两个文件` → 无匹配。
而 `run-all.sh` 里写着

```bash
$PY "$EV/unpack-claims-audit.py" > ...
rc=$?
if [ "$rc" -ne 0 ]; then ... exit "$rc"; fi
```

`rc` 永远为 0，**这个 if 从来没有生效过**。`npm run check` 也就永远通过——
教程改错了，门禁照绿。

**修复**：两个门禁都在 FAIL 分支补 `sys.exit(1)`；新增的
`examples-claims-audit.py` 一开始就带退出码。

**验证（反向验证）**：把 `examples-claims-audit.py` 里 A1 的期望值从 `2.3`
改回教程原来的错误值 `1.3`，门禁 exit 1、报 255 PASS / 1 FAIL；
改回来 exit 0。已做。

---

### D-32 `class/define-with-statement.py` 用 `__module__` 判断主模块

**现象**：类体里写 `if __module__ == '__main__':`。

**证据**：实测两种写法行为完全一致（都打印 `main`）——
`__module__` 在**类体里**能取到模块名（模块层取不到，`__module__` 不是模块级全局）。
但惯用写法是 `__name__`，`__module__` 是描述符/类内部属性，
用它做入口判断会让学习者以为这是标准写法。

**修复**：改成 `if __name__ == '__main__':`，输出不变。

---

### D-33 `_draft/32-for.py` 与 `_draft/4x-lambda.py` 文件名和内容不符

**现象**：

| 文件 | 文件名暗示 | 实际内容 |
|------|-----------|---------|
| `_draft/32-for.py` | for 循环 | 斐波那契**函数**（内部用 while） |
| `_draft/4x-lambda.py` | lambda | `for w, len(w)` 循环，**没有任何 lambda** |

**为什么是缺陷**：学习者按文件名找「for 循环示例」会找到函数示例，
按「lambda」找到 for 循环。文件名是这仓库唯一的索引。

**处理**：**未改名**。`_draft/` 是草稿区，改名属于内容规划决策；
已在 [examples 全量走查清单](/walkthrough/examples-audit) 里标注真实内容，
等维护者决定这批草稿的去留（见 O-09）。

---

### D-34 走查笔记自己的目录计数对不上磁盘

**现象**：`open.md` 写「`examples/number/`（6 个文件）、`string/`（7 个）、
`list/`（7 个）、`map/`（5 个）、`comprehension/`（2 个）」，合计声称 27 个；
`_draft/` 写 10 个、`function/` 写 7 个。

**证据**：`find examples -name '*.py' | wc -l` 逐目录实测：

| 目录 | 笔记声称 | 实测 |
|------|---------|------|
| `number/` | 6 | **3** |
| `string/` | 7 | **8** |
| `list/` | 7 | **6** |
| `map/` | 5 | 5 |
| `comprehension/` | 2 | 2 |
| `_draft/` | 10 | **9** |
| `function/` | 7 | **6** |
| 合计 | — | **66** |

**为什么是缺陷**：笔记第一行就写「声明数量必须等于实测数量」，
结果自己的数字是估的。用估算数字做覆盖面判断，会漏掉整个目录。

**修复**：全部按 `find` 实测改正；在 [L2 走查笔记](/walkthrough/l2-types)
开头把「笔记数字也曾错过」这件事本身记录下来，作为方法论教训。

---

### D-35 `docs/.vitepress/theme/client.js` 是从未被加载的死代码

**现象**：`theme/` 下有两个文件都定义 `window.__runPyDemo` /
`window.__loadPyodide`，且都往 `<head>` 注入 Pyodide `<script>`：

| 文件 | 按钮文案 | 输出区占位符 |
|------|---------|-------------|
| `theme/index.js` | `⏳ 运行中…` / `▶ 运行` | `(运行完成，但没有 print 输出——这段代码只做赋值)` |
| `theme/client.js` | `⏳ Running...` / `Run` | `(no output)` |

**证据（都来自构建产物，不是读代码的印象）**：

```bash
# 1. 构建产物的 theme chunk 里只有 index.js 的中文文案
grep -o "⏳ 运行中…\|⏳ Running\.\.\." docs/.vitepress/dist/assets/chunks/theme.*.js
# → ⏳ 运行中…        （没有任何 Running...）

# 2. app 入口没有引用 client.js
grep -o "client\.[a-z]*\.js" docs/.vitepress/dist/assets/app.*.js
# → 无输出
```

**根因**：VitePress 的主题入口只有 `.vitepress/theme/index.{js,ts}`，
`client.js` 不是约定文件名，也没有被 `index.js` import，所以**根本不进 bundle**。
`node --check` 通过、语法没问题，但它一次都没执行过。

**为什么重要**：它和上一轮删掉的 `pyodide-plugin.js`（D-14）是同一类问题——
看起来在跑、实际没人加载。留着会让下一个人改错文件
（改 `client.js` 的文案毫无效果，因为生效的是 `index.js`）。

**修复**：删除。构建后 `npm run check` 全部门禁仍通过，按钮行为不变
（文案本来就来自 `index.js`）。

**顺带修正 O-04 的诊断**：此前记录「Pyodide 被加载两次（CDN + 本地），
一个是 `client.js` 注入的 CDN」——**这个归因是错的**，`client.js` 从未执行。
真正的两次注入来自 `config.js` 的 `head`（dev 用 CDN）和
`theme/index.js`（dev 用本地 `/pyodide/`）。dead code 删除不影响加载次数。

---

### D-36 `.gitignore` 的 `.vitepress/cache` 匹配不到真实路径，缓存因此被提交

**现象**：`.gitignore` 第 8 行写 `.vitepress/cache`，但仓库里
`docs/.vitepress/cache/` 下 **12 个文件已被 git 跟踪**，
且每次 `docs:build` / `docs:dev` 都会把它们弄脏。

**证据**：

```bash
$ git check-ignore -v --no-index docs/.vitepress/cache/deps/vue.js
（修改前）无输出 —— 该路径不被任何规则忽略

$ git check-ignore -v docs/.vitepress/dist/index.html
.gitignore:7:dist	docs/.vitepress/dist/index.html
```

**根因**：gitignore 模式里**带斜杠的规则锚定仓库根目录**。
`.vitepress/cache` 含一个斜杠，所以只匹配 `<root>/.vitepress/cache`，
匹配不到 `docs/.vitepress/cache`。而同行的 `dist` 不含斜杠，
在任何层级都生效——所以 `docs/.vitepress/dist` 反而被正确忽略了。
一行之差，一个生效一个不生效。

**修复**：`.gitignore` 补 `docs/.vitepress/cache/` 与 `docs/.vitepress/dist/`
（原行保留，避免影响根级路径）。修复后：

```bash
$ git check-ignore -v --no-index docs/.vitepress/cache/deps/vue.js
.gitignore:12:docs/.vitepress/cache/	docs/.vitepress/cache/deps/vue.js
```

**未做**：已跟踪的那 12 个缓存文件**没有取消跟踪**（`git rm --cached`）。
那是一次仓库级变更，按 O-02 的结论留给维护者确认后单独处理。
本轮走查中我用 `git checkout -- docs/.vitepress/cache/` 恢复它们，
没有把构建产生的缓存改动混进提交。


---

## 仓库卫生（记录，未改）

| 项 | 实测 | 说明 |
|----|------|------|
| `docs/.vitepress/cache/` 已被 git 跟踪 | `git ls-files docs/.vitepress` 有 12 个文件 | `.gitignore` 里写了 `.vitepress/cache`，但**已跟踪的文件不受 gitignore 约束**，所以 dev server 每次都会弄脏工作区。走查中我多次 `git checkout --` 恢复它以免混入提交 |
| Pyodide 二进制重复两份 | `docs/public/pyodide/` 19M + `docs/public/learn-python/pyodide/` 19M | dev 用前者、prod 用后者；产物 dist 里同样各一份，共约 76M |
| `docs/public/learn-python/pyodide-init.js` 失联 | `grep -rn pyodide-init` 无引用 | 是修复 stdout 捕获之前的老版本运行时代码，易被误认成生效版本 |
| 两个部署 workflow 并存 | `.github/workflows/main.yml` + `deploy.yml` | 都在 push 到 master 时构建并部署 GitHub Pages，用的是两套不同 action，存在相互覆盖风险 |
| Pyodide 被加载两次 | 页面 script 列表同时有 `/pyodide/pyodide.js` 与 CDN `pyodide.js` | `config.js` head 注入 CDN，`theme/index.js` 又注入本地。当前版本一致（0.24.1）但存在漂移风险，且浪费一次下载 |
