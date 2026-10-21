# 语法差异速通：对照 JS

> 面向有 JS/TS 经验、第一次写 Python 3.12 的读者。覆盖列表、字典、推导式、解包、f-string 五组语法差异。

**一句话结论：** 字典的键名、解包里的星号、f-string 的版本线，是 JS 开发者最容易写错的三处。

---

## 一、与 JS 的对照表

| 关注点 | Python 3.12 | JavaScript |
|--------|-------------|------------|
| 列表字面量 | `[1, 2, 3]`；`list(iterable)` 从可迭代对象构造 | `[1, 2, 3]` |
| 列表推导式 | `[x * x for x in xs if x > 0]`（PEP 202，2.0 起） | 无对应语法，惯用 `xs.filter(...).map(...)` |
| 字典字面量 | `{"a": 1}`；键位是表达式，字符串键必须加引号，`{a: 1}` 以**变量 a 的值**为键 | `{a: 1}` 的属性名就是字符串 `"a"` |
| 字典推导式 | `{k: v * 10 for k, v in pairs}`（PEP 274） | 无对应语法，惯用 `Object.fromEntries(...)` |
| 对象解构 `...rest` | 赋值目标**不支持** `**rest`；用 `d["k"]`、`d.get()`，或 3.10+ 的 `match` 映射模式 | `const {x, y, ...rest} = obj` |
| 序列解包 | `a, *b, c = seq`，星号可出现在任意位置，收集结果是 list（PEP 3132） | `const [first, ...rest] = seq`，`...rest` 只能在末尾 |
| 字典顺序 | 3.7 起语言规范保证插入顺序 | `for-in` 先按数值升序遍历整数索引键，再按创建顺序遍历字符串键 |
| 模板字符串 | `f"{name}"`（PEP 498，3.6 起） | `` `${name}` `` |
| 自文档化 | `f"{name=}"`（3.8 新增 `=` 指定符） | 无 |
| 同种引号嵌套 | 表达式部分可复用与外层相同的引号（PEP 701，3.12 起；3.11 及以前是 `SyntaxError`），见示例 3 | — |
| bytes 格式化 | 没有 `.format()`，也没有 f-string；3.5 起支持 `%`（PEP 461） | — |

---

## 二、可运行示例

示例均只用标准库，输出为 Python 3.12 实测结果。

::: warning 运行环境
本站在线运行器使用的 Pyodide 版本对应 Python 3.11。示例 3 中的 3.12 专有写法会在在线运行器里报 `SyntaxError`，请在本机 Python 3.12 执行，因此该示例用 `text` 围栏展示。
:::

### 示例 1：字面量与推导式

```python
sqs = [x * x for x in range(5)]
print(sqs)

a = "hello"
print({a: 1})  # 键是变量 a 的值

pairs = [("x", 1), ("y", 2), ("z", 3)]
print({k: v * 10 for k, v in pairs})
print(list("abc"))
```

输出：

```text
[0, 1, 4, 9, 16]
{'hello': 1}
{'x': 10, 'y': 20, 'z': 30}
['a', 'b', 'c']
```

### 示例 2：解包与 `**rest` 的替代写法

```python
seq = [10, 20, 30, 40, 50]

first, *middle, last = seq
print(first, middle, last)

*_, a, b = seq  # a、b 是最后两个元素
print(a, b, _)

# x, y, **rest = obj 是非法语法
try:
    compile("x, y, **rest = {'x': 1, 'y': 2}", "<demo>", "exec")
except SyntaxError as e:
    print(type(e).__name__, e.msg)

# 3.10+ 的 match 映射模式：** 必须是最后一项
obj = {"x": 1, "y": 2, "z": 3, "extra": 99}
match obj:
    case {"x": x, "y": y, **rest}:
        print(x, y, rest)

d = {"x": 1}
print(d["x"], d.get("missing", "default"))
```

输出：

```text
10 [20, 30, 40] 50
40 50 [10, 20, 30]
SyntaxError invalid syntax
1 2 {'z': 3, 'extra': 99}
1 default
```

JS 对照：

```js
const [first, ...rest] = [10, 20, 30, 40, 50];
const last = rest.pop(); // 取末尾元素需再 pop 一次
const { x, y, ...restObj } = { x: 1, y: 2, z: 3, extra: 99 };
```

### 示例 3：f-string 的三条版本线

三个特性容易混淆：f-string 本身是 3.6（PEP 498），`{expr=}` 是 3.8，同种引号嵌套是 3.12（PEP 701）。

```text
import datetime

name, age = "fred", 50
member_since = datetime.date(1975, 7, 31)
print(f"My name is {name}, my age next year is {age + 1}.")   # 3.6
print(f"{name=}, {member_since=}")                            # 3.8
print(f"{"a" + "b"}")                                         # 3.12 起
print(b"x=%i y=%f" % (1, 2.5))                                # bytes 用 %，3.5 起
print(hasattr(b"x", "format"))                                # False
```

输出（Python 3.12）：

```text
My name is fred, my age next year is 51.
name='fred', member_since=datetime.date(1975, 7, 31)
ab
b'x=1 y=2.500000'
False
```

### 示例 4：dict 的插入顺序

```python
d = {}
for key in ["b", "a", "c"]:
    d[key] = key.upper()
print(list(d))

d["a"] = "A2"   # 重新赋值不改变顺序
print(list(d))

del d["a"]
d["a"] = "A3"   # 删除后重新插入，排到末尾
print(list(d))
```

输出：

```text
['b', 'a', 'c']
['b', 'a', 'c']
['b', 'c', 'a']
```

JS 一侧：`for (const k in o)` 会把整数索引键（如 `"2"`、`"10"`）按数值升序排在前面，其余字符串键按创建顺序排列，与 Python 的纯插入序不同。

---

## 三、练习：面经检索问答

给定 FAQ 列表，每条形如 `{"q": 问题文本, "kw": [关键词, ...]}`，实现 `search(qa_list, keyword)`：

- 大小写不敏感，命中问题文本或任一关键词即算命中（子串匹配）；
- 按原始顺序返回全部命中条目的 `(索引, 问题文本)`；
- 0 命中时 `raise ValueError`。

**参考答案**

```python
FAQ = [
    {"q": "如何在 Python 里交换两个变量？", "kw": ["tuple", "swap"]},
    {"q": "dict 出现次数最多的 3 个键怎么求？", "kw": ["dict", "Counter"]},
    {"q": "f-string 里能用同一个引号吗？", "kw": ["fstring", "3.12"]},
]

def search(qa_list, keyword):
    k = keyword.lower()
    hits = []
    for i, qa in enumerate(qa_list):
        in_q = k in qa["q"].lower()
        in_kw = any(k in w.lower() for w in qa["kw"])
        if in_q or in_kw:
            hits.append((i, qa["q"]))
    if not hits:
        raise ValueError(f"no faq matches {keyword!r}")
    return hits

print(search(FAQ, "dict"))
print(search(FAQ, "PYTHON"))
try:
    search(FAQ, "graphql")
except ValueError as e:
    print("ValueError:", e)
```

输出：

```text
[(1, 'dict 出现次数最多的 3 个键怎么求？')]
[(0, '如何在 Python 里交换两个变量？')]
ValueError: no faq matches 'graphql'
```

`search` 用异常表达「找不到」，与 `d["missing"]` 抛 `KeyError` 的风格一致；JS 的 `Array.prototype.find` 不命中时返回 `undefined`。

---

## 四、面试追问

**1. Python 能像 JS 一样写 `const {x, y, ...rest} = obj` 吗？**

赋值语句不行。赋值目标的文法只有 `"*" target`，没有 `"**" target`，`x, y, **rest = obj` 是 `SyntaxError`；PEP 3132 也规定左侧最多一个单星号表达式。对位写法是 3.10+ 的 `match` 映射模式（PEP 634），`**rest` 最多一个且必须放最后。

**2. `{expr=}` 和 3.12 的同引号嵌套是一回事吗？**

不是。`{expr=}` 是 3.8 新增的指定符；同种引号嵌套是 3.12 的 PEP 701，3.11 及以前会报 `SyntaxError`。bytes 既没有 `.format()` 也没有 f-string，格式化走 3.5 起的 `%`（PEP 461）。

**3. Python dict 有顺序吗？和 JS 对象一样吗？**

3.7 起 dict 保持插入顺序是语言规范的一部分，`list(d)` 按插入顺序给出键。JS 的 `for-in` 会先按数值升序遍历整数索引键，再按创建顺序遍历字符串键，两者不同。

---

## 五、未下结论的点

- 「dict 删除后重新插入排到末尾」只有示例 4 的实测输出，未找到 docs.python.org 3.12 的原文，不作文档级结论。
- ECMA-262 的属性键顺序算法原文未获取，JS 顺序结论引用 MDN `for...in` 页面。
- 不做性能比较。

---

## 六、参考

- Python 官方：[PEP 202](https://peps.python.org/pep-0202/)、[PEP 274](https://peps.python.org/pep-0274/)、[PEP 3132](https://peps.python.org/pep-3132/)、[PEP 448](https://peps.python.org/pep-0448/)、[PEP 461](https://peps.python.org/pep-0461/)、[PEP 498](https://peps.python.org/pep-0498/)、[PEP 634](https://peps.python.org/pep-0634/)、[PEP 701](https://peps.python.org/pep-0701/)
- What's New：[3.5](https://docs.python.org/3.12/whatsnew/3.5.html)、[3.7](https://docs.python.org/3.12/whatsnew/3.7.html)、[3.8](https://docs.python.org/3.12/whatsnew/3.8.html)、[3.12](https://docs.python.org/3.12/whatsnew/3.12.html)
- JS 一侧：[MDN for...in](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for...in)、[MDN 解构赋值](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring)
