# L3 走查笔记 — 控制流

> 材料来源：`examples/statement/` 下 **10** 个文件。L3 教程页不存在。
> 每个概念标注来自哪个示例文件。

## 家底盘点

| 文件 | 讲什么 |
|------|--------|
| `statement/for.py` | `for` 遍历列表 |
| `statement/while.py` | `while` + 手写下标 |
| `statement/if.py` / `else.py` / `elif.py` | 三分支 |
| `statement/break.py` | `break` |
| `statement/continue.py` | `continue` |
| `statement/for-else.py` | `for/else` + `try/except/else/finally` |
| `statement/try.py` / `finally.py` | 异常捕获 |

---

## 概念 1：`for` 遍历的是**可迭代对象**，不是下标

### 逐个符号

| 符号 | 含义 |
|------|------|
| `for i in [1,2,3]:` | `i` 依次绑定到每个**元素**，不是下标 |
| `:` + 缩进 | Python 用缩进分块，没有 `{}` |
| `len(l)` | 元素个数 |

### 预测 vs 实际

```python
for i in [1, 2, 3]:
    print(i)
```

```
1
2
3
```

**和 JS 的 `for (const i of arr)` 一致**，和 `for (let i = 0; ...)` 不同。
要下标得自己写 `for i in range(len(l))` 或用 `enumerate`：

```python
for idx, val in enumerate(['a', 'b']):
    print(idx, val)        # 0 a / 1 b
```

`examples/statement/while.py` 就是「JS 思维」的写法——手动维护 `i` 和 `i += 1`。
它能跑，但 Python 里通常是多余的。

---

## 概念 2：`if / elif / else`

### 逐个符号

| 符号 | 含义 | JS 对应 |
|------|------|---------|
| `if a % 2 == 0 :` | 条件后可加空格，`:` 结束 | `if (...)` |
| `elif` | **else if 的合并词**，没有 `else if` | `else if` |
| `%` | 取模，`a % 2 == 0` 判偶 | 同 |

### 新例子：三分支写全

```python
def classify(n):
    if n < 0:
        return 'negative'
    elif n == 0:
        return 'zero'
    else:
        return 'positive'

for n in (-5, 0, 7):
    print(n, classify(n))
```

### 反例：`elif` 写不成 `else if`

```text
if a:
    ...
else if b:      # SyntaxError: expected 'except' or finally'
    ...
```

Python 没有 `else if`，只有 `elif`。这是从 JS 迁移第一个会撞的语法墙。

### 关于 `input()`

`statement/if.py`、`else.py`、`elif.py`、`finally.py`、`try.py`、
`function/def.py`、`_draft/31-if.py` 共 7 个示例都用 `input()` 读键盘。
`input()` **永远返回 str**，所以要 `int(input(...))` 才能比较大小。

这些块在浏览器里点「▶ 运行」没有 stdin，会直接抛 `EOFError`——
所以本页涉及 `input()` 的片段一律用 `text` 标注，不当成可运行块。

---

## 概念 3：`break` 和 `continue`

### 逐个符号

| 符号 | 作用范围 |
|------|---------|
| `break` | 立刻**跳出整个循环**，后面的迭代不做了 |
| `continue` | 立刻**结束本次迭代**，进入下一次 |

### `break.py` 逐步拆

```python
l = [1, 2, 3, 4]
i = 0
while i < len(l):
    if l[i] > 2:
        print("first element greater 2 index: ", i)
        break
    i += 1
```

| 轮次 | `i` | `l[i] > 2` | 发生什么 |
|------|-----|-----------|---------|
| 1 | 0 | `1 > 2` False | 不走 if，`i` 变 1 |
| 2 | 1 | `2 > 2` False | 不走 if，`i` 变 2 |
| 3 | 2 | `3 > 2` True | 打印 `2`，`break` 跳出，`i += 1` **没执行** |

输出：`first element greater 2 index:  2`

> ⚠️ 原注释写 `# jump to loop`，字面意思是「跳到循环」——**语义是反的**，
> `break` 是离开循环。已改成「跳出整个循环」（D-25）。

### `continue.py` 的反例：`continue` 之后的代码永远不执行

```python
for num in [1, 2, 3, 4]:
    if num % 2 == 0:
        print("even number: ", num)
        continue
        print("this code never execute")
    print("odd number: ", num)
```

输出：

```
odd number:  1
even number:  2
odd number:  3
even number:  4
```

`this code never execute` 一次都没打印——这正是这个示例想教的事。
但把它写成「死代码」而不是注释，初学者会以为那行有用。已加注释说明。

### 怎样证明我理解了

1. 能说出 `break` 和 `continue` 的区别，各用一个例子。
2. 能预测 `break.py` 里 `i` 最终的值（2，因为 `i += 1` 在 break 之后没执行）。
3. 能说出 `continue` 后面那行为什么不执行。

---

## 概念 4：`for/else` — 没被 `break` 才执行 `else`

这是 L3 里**最反直觉**的语法，`for-else.py` 用两个循环正反演示。

### 逐个符号

```python
for i in range(3):
    print("i =", i)
else:
    print("循环正常结束，未被 break 打断")
```

| 部分 | 含义 |
|------|------|
| `else:` 挂在 `for` 上 | 循环**自然耗尽**（没遇到 `break`）才执行 |
| `break` | 一旦执行，`else` 整块跳过 |

### 预测 vs 实际

```
循环 1（无 break）  → 打印 i = 0/1/2，然后 else 执行
循环 2（i==1 break）→ 打印 i = 0，然后 break，else 不执行
```

实测与预测一致。**注意 `else` 和 `if` 里的 `else` 完全不是一回事**——
它表达的是「没被 break 打断」。

### 新例子：`while/else` 同理

```python
i = 0
while i < 2:
    print("body", i)
    i += 1
else:
    print("else")
# body 0 / body 1 / else
```

### 反例：`else` 里 `break` 之前的部分仍算「自然结束」

```python
for i in range(3):
    if i == 1:
        continue
else:
    print("else runs")      # 会执行 —— continue 不算打断
```

`continue` 不阻止 `else`，只有 `break` 阻止。这一点示例没讲，我自己测的。

### 怎样证明我理解了

1. 能说出 `for/else` 的 `else` 什么时候执行（循环自然耗尽）。
2. 能预测「循环里有 `continue`」时 `else` 是否执行（执行）。
3. 能说出为什么这个语法叫 `else` 而不是 `nobreak`（历史原因，官方文档也承认反直觉）。

---

## 概念 5：`try / except / else / finally` 的执行顺序

### 逐个符号

| 子句 | 什么时候执行 |
|------|-------------|
| `try` | 总是第一个 |
| `except X` | `try` 里抛出匹配 `X` 的异常时 |
| `else` | `try` **没抛异常**时（在 finally 之前） |
| `finally` | **总是**最后执行，即使 try 里 return 了 |

### 预测 vs 实际（用日志列表把顺序显式打出来）

```python
log = []
try:
    log.append('try')
    1 / 0
except ZeroDivisionError:
    log.append('except')
else:
    log.append('else')
finally:
    log.append('finally')
print(log)
```

```
['try', 'except', 'finally']        ← 有异常：不走 else
```

去掉 `1 / 0` 再跑：

```
['try', 'else', 'finally']          ← 无异常：走 else，不走 except
```

**「有无异常」决定走 except 还是 else，两者互斥；finally 永远走。**

### 新例子：`finally` 在 `return` 之前仍然执行

```python
def f():
    try:
        return 'from try'
    finally:
        print('finally still runs')

print(f())
```

```
finally still runs
from try
```

`finally` 在函数返回**前**执行——这是它做资源清理（关文件、放锁）的根据。

### 反例 1：裸 `except:` 会吞掉一切

`statement/try.py` 和 `finally.py` 写的是裸 `except:`。实测：

```python
try:
    raise KeyboardInterrupt
except:
    print('swallowed')
```

```
swallowed            ← Ctrl+C 被吃掉了，程序停不下来
```

裸 `except:` 连 `KeyboardInterrupt` / `SystemExit` 都捕获。**已改成
`except ValueError:`**（D-26）。代价是 `input()` 遇到 EOF 时不再被吞，
`run-all.sh` 里这两个文件的退出码从 0 变成 1——这反而更诚实：
它们确实需要交互输入。

### 反例 2：输入合法时文案说「非法」

`try.py` 原文：

```text
try:
    x = int(input("Please enter a number: "))
    print('x is illegal number')      # 数字合法，却说 illegal
except:
    print("Oops!  That was no valid number.")
```

送 `7` 进去，走的是 `print('x is illegal number')`——**数字是合法的，
文案却说它非法**。已改成 `print('x is a valid number:', x)`，
并把 `"Oops!  That was no valid number."` 改成语法正确的
`"Oops! That was not a valid number."`。

### 怎样证明我理解了

1. 能说出四个子句各自的触发条件和执行顺序。
2. 能说出裸 `except:` 的隐患（吞 `KeyboardInterrupt`）。
3. 能说出 `finally` 在 `return` 时的行为（return 之前执行）。

---

## 这一轮记下的困惑与解决

| # | 困惑 | 怎么解决的 |
|---|------|-----------|
| C-19 | `for/else` 的 `else` 到底是「循环结束」还是「没 break」 | 写成两个循环对照跑。是「没 break」，`continue` 不影响它 |
| C-20 | `try` 的 `else` 和 `if` 的 `else` 是一回事吗 | 不是。try 的 else = 「try 没抛异常」，位置在 except 之后、finally 之前 |
| C-21 | 裸 `except:` 有什么问题 | 用子进程抛 `KeyboardInterrupt` 验证，确认被吞。已改 `except ValueError` |
| C-22 | `break.py` 里 `i` 最后是几 | 2。`break` 在 `i += 1` 之前，所以最后一轮没自增 |
| C-23 | `input()` 返回什么类型 | `str`。所以示例都写 `int(input(...))`。浏览器里没有 stdin，这些块点运行会 EOFError |

## 我认为 L3 素材缺的练习

1. **没有 `enumerate` / `zip` 的示例**：`while.py` 用手写下标，
   但更 Pythonic 的两种写法完全没出现。
2. **没有「finally 里 return 会覆盖 try 的 return」这个经典坑**。
3. **没有异常层级演示**：`except ValueError` 抓不到 `KeyError`，
   「先具体后宽泛」的顺序规则没有素材。
4. **`for-else.py` 把 for-else 和 try/except/else/finally 塞在一个文件里**，
   两个无关概念互相干扰，拆开更利于单点突破。
