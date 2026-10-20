# examples 全量走查清单

> 这一页是 `examples/` 下 **66** 个 Python 文件的走查总账：
> 每个文件的结论都写成了可执行断言（256 条，见
> [练习证据](/walkthrough/evidence)），本页只放总账、跨文件的反模式，
> 和不属于 L2–L5 的剩余素材。

## 目录总账（实测，不是计划）

| 目录 | 文件数 | 对应课程计划 | 走查状态 |
|------|-------|-------------|---------|
| `examples/number/` | 3 | L2 数据类型 | ✅ [L2 笔记](/walkthrough/l2-types) |
| `examples/string/` | 8 | L2 数据类型 | ✅ 同上 |
| `examples/list/` | 6 | L2 数据类型 | ✅ 同上 |
| `examples/map/` | 5 | L2 数据类型 | ✅ 同上 |
| `examples/comprehension/` | 2 | L2 数据类型 | ✅ 同上 |
| `examples/statement/` | 10 | L3 控制流 | ✅ [L3 笔记](/walkthrough/l3-flow) |
| `examples/function/` | 6 | L4 函数 | ✅ [L4 笔记](/walkthrough/l4-function) |
| `examples/class/` | 12 | L5 类 | ✅ [L5 笔记](/walkthrough/l5-class) |
| `examples/api/` | 3 | L2/L7 边缘 | ✅ 本页 |
| `examples/_draft/` | 9 | 未归类草稿 | ✅ 本页（原 10 个，删掉 1 个空文件） |
| `examples/tutorial/` | 1 | L1 | ✅ 本页 |
| `examples/mnist/` | 2 | L1 | ✅ 本页 |
| **合计** | **66** | | |

> `find examples -name '*.py' | wc -l` = 66，与上表逐格相加一致。
> （原为 67：`_draft/11-define-variable.py` 是 0 字节空文件，本轮删除，D-29。）
> 上一版笔记把 `number` 写成 6、`list`/`function` 写成 7、`_draft` 写成 10，
> 合计声称 27（L2 范围）——实测 24。已按磁盘改正（D-34）。

## 运行状态总账

| 状态 | 数量 | 说明 |
|------|------|------|
| 直接运行通过（stdin 接 `/dev/null`） | 59 | 门禁 `run-all.sh` 实测 |
| 需要交互 stdin | 7 | `if/else/elif/finally/try.py`、`function/def.py`、`_draft/31-if.py` |
| 需要 `-m` 调用 | 1 | `mnist/main.py`（`cd examples && python -m mnist.main`） |
| **合计** | **66** | |

> 「需要交互 stdin」从走查早期的 5 个变成 7 个：`try.py` 和 `finally.py`
> 原本用裸 `except:` 把 `EOFError` 吞掉，所以在 `/dev/null` 下也显示 exit 0。
> 改成正确的 `except ValueError:` 之后，EOF 会正常逃出来——**这反而更诚实**，
> 它们确实需要输入（D-26）。

---

## 一、`examples/api/` — 3 个文件

### `os.py`：路径拼接跟着操作系统变

```python
import os
print(os.path.join('/a', 'b', 'c'))      # Windows: /a\b\c   POSIX: /a/b/c
print(os.path.isabs('/a/b/c'))           # True
print(os.path.isabs('./a'))              # False
```

**逐个符号**：

| 符号 | 含义 |
|------|------|
| `os.path.join` | 用**当前平台**的分隔符拼接，不是写死 `/` |
| `os.getcwd()` | 当前工作目录 |
| `os.path.abspath` | 相对路径 → 绝对路径 |
| `os.path.isabs` | 是否是绝对路径 |

**我的困惑**：`os.path.join('/a', 'b', 'c')` 在 Windows 上输出 `/a\b\c`——
第一个参数的前导 `/` 被保留，后面用 `\` 拼。这和「反正都是斜杠」的直觉不同。

**证据不可复现**：`getcwd()` 和 `abspath('./a')` 的输出含本机绝对路径，
换机器就变。这一条已记为已知限制（O-03 同类），不当作缺陷。

### `string-operation.py`：字符串方法三连 + 去空白

```python
text = "hello world"
print(text.title())                    # Hello World
print(text.upper())                    # HELLO WORLD
print(text.lower())                    # hello world
print('a' 'b')                         # ab（相邻字面量拼接）
print('1' + text)                      # 1hello world
print(('\t' + text + '\t').rstrip())   # \thello world（只删右侧）
```

**反例**：`lstrip` 只删左侧，`strip` 删两侧——三个方法必须分清。

```python
s = '  x  '
print(repr(s.lstrip()), repr(s.rstrip()), repr(s.strip()))
# 'x  ' '  x' 'x'
```

**已修的缺陷**：打印标签原写 `str.rstripe()`，方法名拼错（`rstripe` → `rstrip`，D-24）。

### `list-operation.py`：`len` 在 `append` 之前求值

```python
items = [1, 2, 3, 4]
items.append(len(items) + 1)      # len 先算得 4，append 5
```

**这条教了一个通用规则**：函数参数的求值发生在调用之前。
`len(items)` 拿到的是 append 之前的长度。

---

## 二、`examples/_draft/` — 9 个文件（草稿区）

这个目录没有对应任何课程计划，文件名编号（`11-`、`21.`、`4x-`）像是
某份外部教程的章节号。逐个看完后的问题：

| 文件 | 内容 | 问题 |
|------|------|------|
| `11-define-variable.py` | **0 字节，空的** | 运行无输出，学习者会以为坏了。已删除（D-29） |
| `12-use-variable.py` | int/float/complex 运算 | 内容没问题，与 `number/` 重复 |
| `21.types-number.py` | 基本运算符 | 注释说 `//` 「return a integer」——错，`3//2.` 返回 `1.0`（D-28） |
| `23.types-list.py` | 列表与二维 | 注释 `two dimesion size array` 拼写错误；`arr = [1,2],[3,4]` 是**元组套列表**不是二维数组 |
| `31-if.py` | if/else | 与 `statement/if.py` + `else.py` 重复 |
| `32-for.py` | **斐波那契函数** | 文件名写 `for`，内容没有任何 for 循环（D-33） |
| `41-function.py` | 闭包 `make_incrementor` | L4 缺的「函数是一等对象」正好在这，却在 `_draft` 里没人引 |
| `42-function-attributes.py` | 函数属性 `__doc__/__name__/__defaults__/...` | 打印 `__globals__` 和 `__code__`，把本机绝对路径和内存地址写进提交物（D-27） |
| `4x-lambda.py` | **for 循环打印单词长度** | 文件名写 `lambda`，内容没有任何 lambda（D-33） |

### 值得提升的素材：闭包

`41-function.py` 是全仓库唯一一个闭包示例，正好补上 L4 的缺口：

```python
def make_incrementor(n):
    return lambda x: x + n

f1 = make_incrementor(1)
print(f1(0), f1(1), f1(2))        # 1 2 3
print(f1.__closure__[0].cell_contents)     # 1  —— 闭包细胞存住了 n
```

**「闭包细胞」这个概念没有任何教程讲**，但它是理解装饰器和回调的前置。

### 已修的缺陷：`__globals__` 泄漏本机路径

`42-function-attributes.py` 原第 20 行左右：

```text
print(hi.__globals__)
print(say.__code__)
```

实测输出把 `C:\Users\cheng\...\examples\_draft\42-function-attributes.py`
这样的绝对路径和 `0x00000278...` 内存地址直接写进了
`.walkthrough/evidence/examples-run.md` 并提交。已改成确定性的
`say.__code__.co_varnames`，删掉 `__globals__` 打印（D-27）。

---

## 三、`examples/tutorial/print.py` 与 `examples/mnist/`

### `tutorial/print.py`

```python
print(1 + 2)              # 3     —— 先求值再传参
print("hello world!")     # hello world!
```

全仓库最小的示例，和 L1 §1 完全重复。它是「教程第一课」的原始素材。

### `mnist/`

`data.py` 只定义 `load_data()`，无输出；`main.py` 导入并使用。
**这两个文件必须 `cd examples && python -m mnist.main` 才能跑**，
直接按路径跑一定 `ModuleNotFoundError`（D-08，已在 L1 教程写清原因）。

断言门禁里固化了这条：

```
K4 mnist/main.py: 直接按路径跑必失败        → raises
K2 mnist/main.py: -m 调用成功              → exit 0
K5 mnist/data.py: 只导出 load_data         → ['load_data']
```

---

## 四、跨示例反模式总表

这些不是某一个文件的缺陷，是**散布在多个示例里的共性误区**。
全部写进了断言门禁的 L 段。

| # | 反模式 | 证据 | 影响范围 |
|---|--------|------|---------|
| 1 | 用 `list` / `map` / `str` 当变量名，遮蔽内建 | 原 13 个文件；`list('abc')` 抛 `TypeError`。**本轮已全部改名** | `list/*` 6 个、`map/*` 5 个、`api/*` 2 个 |
| 2 | 以为 `//` 总返回 int | `17.0 // 3` → `5.0`（float） | `_draft/21.types-number.py` 注释写错 |
| 3 | 以为 `%` 和 JS 同语义 | `-7 % 2` → `1`（JS 是 -1） | 无示例覆盖负数取模 |
| 4 | 用 `==` 直接比浮点 | `0.1+0.1+0.1 == 0.3` → `False` | 只有 `float.py` 一行，没给解法 |
| 5 | 以为 `[x] * n` 是深拷贝 | `[[]]*3` 三个元素是同一对象 | 无示例覆盖 |
| 6 | 以为 `round` 是四舍五入 | `round(2.5)` → `2`（银行家舍入） | 无示例覆盖 |
| 7 | 以为 `bool` 和 int 无关 | `True + True` → `2`，`1 == True` → `True` | 无示例覆盖 |
| 8 | 以为 `and`/`or` 返回 bool | `[] and 1` → `[]`，`1 or 2` → `1` | 无示例覆盖 |
| 9 | 以为 `'a' + 1` 像 JS 那样拼 | `TypeError` | 无示例覆盖 |
| 10 | 以为 `nan` 可以和自己比 | `nan == nan` → `False` | 无示例覆盖 |
| 11 | 裸 `except:` | 吞掉 `KeyboardInterrupt` | `statement/try.py`、`finally.py`（本轮已改 `except ValueError`） |
| 12 | 可变默认参数 | `def f(x=[])` 跨调用共享 | 无示例覆盖（已补进 L4 笔记） |

**模式**：12 条里有 8 条「无示例覆盖」（2 条本轮已修）。也就是说这些坑不是示例教错了，
而是**素材根本没到那个粒度**。走查能补的是把规则写进笔记和断言门禁，
让后面写课的人有据可依。

---

## 五、素材与课程零关联（未解决）

`examples/` 66 个文件里，**只有 `examples/mnist/` 被 `begin.md` 引用过一次**
（还是在讲 `-m` 调用方式时）。其余 65 个与 `docs/` 零关联：

- `docs/` 里搜不到 `examples/number`、`examples/string`、`examples/list` 等路径；
- 课程计划 L2–L5 的页面不存在，所以这些素材**没有消费方**；
- 结果是：学习者打开站点，只能看到 L1 一课，然后撞上「⚠️ L2 敬请期待」。

**这不是走查能单方面解决的**（要么补教程引用，要么明确它们是素材库），
已记为待决项，见 [未解决与恢复点](/walkthrough/open) O-09。
