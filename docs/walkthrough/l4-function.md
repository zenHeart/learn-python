# L4 走查笔记 — 函数

> 材料来源：`examples/function/` 下 **6** 个文件。L4 教程页不存在。
> （上一版笔记写「7 个文件」，实测 6 个，已改正。）

## 家底盘点

| 文件 | 讲什么 |
|------|--------|
| `function/def.py` | 斐波那契，`while` + `print(end=' ')` |
| `function/def_return.py` | `return` + 字符串方法 `.title()` |
| `function/def_default_arg.py` | 默认参数 |
| `function/def_key_arg.py` | 关键字实参 |
| `function/def_tuple.py` | `*args` |
| `function/def_map.py` | `**kwargs` |

---

## 概念 1：`def`、参数、`return`

### 逐个符号

```python
def fullname(firstname, middlename, lastname):
    fullname = firstname + ' ' + middlename + ' ' + lastname
    return fullname.title()
```

| 符号 | 含义 |
|------|------|
| `def` | 定义函数，函数名小写 + 下划线（PEP 8） |
| `firstname, ...` | 形参，调用时按位置绑定 |
| `return X` | 返回值；**没有 `return` 就等于 `return None`** |
| `.title()` | str 方法，每个单词首字母大写，返回**新**字符串 |
| 局部变量 `fullname` | 和函数同名**但不冲突**——函数名在模块作用域，局部变量在函数作用域 |

### 预测 vs 实际

```python
def fullname(firstname, middlename, lastname):
    fullname = firstname + ' ' + middlename + ' ' + lastname
    return fullname.title()

print(fullname('tom', 'lee', 'hooker'))
```

```
Tom Lee Hooker
```

### 新例子：没有 `return` 的函数返回 `None`

```python
def no_return():
    x = 1

print(no_return())          # None
print(no_return() is None)  # True
```

### 反例：`str` 不可变，`.title()` 不改原串

```python
s = 'tom lee hooker'
t = s.title()
print(s, t)      # tom lee hooker / Tom Lee Hooker  —— s 没变
```

**这和 JS 一样**（`'abc'.toUpperCase()` 也不改原串），是字符串的共有性质。

### 怎样证明我理解了

1. 能说出 `def f(): pass` 之后 `f()` 的返回值（`None`）。
2. 能说出为什么函数内局部变量能和函数同名（作用域不同）。
3. 能说出 `s.title()` 之后 `s` 变不变（不变）。

---

## 概念 2：默认参数 —— 以及**可变默认参数**这个坑

### 逐个符号

```python
def hi(name, time='morning'):
    print(time + " " + name)

hi('tom')
```

| 符号 | 含义 |
|------|------|
| `time='morning'` | 默认值，调用时不传就用它 |
| 默认值存放位置 | 函数的 `__defaults__` 属性，**定义时求值一次** |

### 预测 vs 实际

```
hi('tom')  →  morning tom        ← 猜对
```

### 新例子：默认值在 `__defaults__` 里

```python
def hi(name, time='morning'):
    return time + " " + name

print(hi.__defaults__)        # ('morning',)
```

### 反例（重点）：可变默认参数跨调用共享

这是教程完全没讲、但我认为**最该讲**的一条：

```python
def f(x=[]):
    x.append(1)
    return x

print(f())      # [1]
print(f())      # [1, 1]      ← 不是 [1]！
print(f())      # [1, 1, 1]
```

**根因**：默认值 `[]` 在 `def` 执行时**只创建一次**，之后每次调用都复用同一个
列表对象。正确写法是用 `None` 哨兵：

```python
def f(x=None):
    if x is None:
        x = []
    x.append(1)
    return x

print(f(), f())     # [1] [1]
```

`def_default_arg.py` 用的是字符串默认值（不可变），所以碰不到这个坑——
但学习者把 `'morning'` 换成 `[]` 就会中招。

### 怎样证明我理解了

1. 能说出默认值什么时候求值（`def` 执行时，一次）。
2. 能预测三次 `f()` 的返回值（`[1]` / `[1,1]` / `[1,1,1]`）。
3. 能说出正确的规避写法（`None` 哨兵）。

---

## 概念 3：关键字实参 —— 顺序无关

### 逐个符号

```python
def hi(time, name):
    print(time + " " + name)

hi(time='morning', name="tom")
hi(name='tom', time="morning")
```

| 符号 | 含义 |
|------|------|
| `time='morning'`（调用处） | 指名传给哪个形参，顺序自由 |
| `time='morning'`（定义处） | 默认值。**同一个写法，两个位置，两个意思** |

### 预测 vs 实际

```
两次调用都输出 morning tom        ← 猜对
```

### 反例：位置参数不能跟在关键字参数后面

```text
def f(a, b):
    pass

f(a=1, 2)        # SyntaxError: positional argument follows keyword argument
```

编译期就报错，不是运行期。

### 怎样证明我理解了

1. 能说出 `hi('tom')` 和 `hi(name='tom')` 的区别（后者指名，前者按位置）。
2. 能说出定义处 `x=1` 和调用处 `x=1` 的不同含义。

---

## 概念 4：`*args` 收成元组，`**kwargs` 收成字典

### 逐个符号

| 写法 | 收集成 | 类型 | 来自 |
|------|--------|------|------|
| `def f(*names)` | 多余的位置实参 | `tuple` | `def_tuple.py` |
| `def f(**info)` | 多余的关键字实参 | `dict` | `def_map.py` |

### 预测 vs 实际

```python
def show_name(*names):
    for name in names:
        print("name:", name)

show_name('tom', 'locke', 'jerry')
```

```
name: tom
name: locke
name: jerry
```

```python
def user_profile(name, age, **info):
    user = {'name': name, 'age': age}
    for key, value in info.items():
        user[key] = value
    return user

print(user_profile(name='tom', age=10, city='berlin', sex='man'))
```

```
{'name': 'tom', 'age': 10, 'city': 'berlin', 'sex': 'man'}
```

**星号个数就是类型**：一个星号 → 元组，两个星号 → 字典。

### 新例子：两者可以同时出现

```python
def f(*args, **kwargs):
    return args, kwargs

print(f('a', b=1))        # (('a',), {'b': 1})
```

### 反例：`*args` 是元组，所以没有列表方法

```python
def f(*args):
    return args.append(1)     # AttributeError: 'tuple' object has no attribute 'append'

f(1, 2)
```

要列表得自己转：`list(args)`。

### 怎样证明我理解了

1. 能说出 `*args` 和 `**kwargs` 分别收集什么、类型是什么。
2. 能预测 `f('a', b=1)` 在 `def f(*args, **kwargs)` 下的返回值。
3. 能说出为什么 `args.append` 会报错（元组不可变）。

---

## 概念 5：`fib` 里的同步赋值

`def.py` 的斐波那契用了一行 Python 味很重的写法：

```python
a, b = b, a + b
```

### 逐个符号

| 部分 | 含义 |
|------|------|
| 右侧 `b, a + b` | 先用**旧值**求出完整元组 |
| 左侧 `a, b` | 再一次性绑定 |

等价于 JS 里的解构交换 `[a, b] = [b, a + b]`。**右侧先全部求值，再赋值**，
所以不会出现「`a` 已经被改，然后拿新 `a` 去算」的问题。

### 新例子：正因为先求值，才能一行交换

```python
a, b = 1, 2
a, b = b, a
print(a, b)        # 2 1
```

JS 里同样的解构交换 `[a, b] = [b, a]` 也是 2 1。**这一点两种语言一致。**

### 反例：如果不先求值就会错

```python
a, b = 1, 2
a = b          # a 变成 2
b = a          # b 也变成 2 —— 拿到的已经是新 a
print(a, b)    # 2 2
```

拆成两行写就丢了「同步」语义。

### 怎样证明我理解了

1. 能说出 `a, b = b, a + b` 为什么不会互相污染（右侧先求值成元组）。
2. 能预测 `fib(10)` 的输出（`0 1 1 2 3 5 8`）。

---

## 这一轮记下的困惑与解决

| # | 困惑 | 怎么解决的 |
|---|------|-----------|
| C-24 | `def f(x=[])` 为什么第二次调用结果变长 | 写成子进程连跑三次，看到 `[1]/[1,1]/[1,1,1]`。默认值只创建一次 |
| C-25 | 定义处 `time='morning'` 和调用处 `time='morning'` 长得一样，怎么区分 | 看位置：在 `def` 括号里是默认值，在调用括号里是关键字实参 |
| C-26 | `*args` 为什么不能 `.append` | 打印 `type(args).__name__` 得 `tuple`。一个星号给元组，两个才给字典 |
| C-27 | `a, b = b, a+b` 为什么不会乱 | 先构造右侧元组再拆包，和 L1 的拆包规则是同一条 |
| C-28 | `fullname` 函数里又有个 `fullname` 变量，不冲突吗 | 不冲突。函数名在模块作用域，局部变量在函数作用域，函数体内先见局部 |

## 我认为 L4 素材缺的练习

1. **没有可变默认参数的示例**——最经典的坑，素材用字符串默认值绕开了。
2. **没有「函数是一等对象」的示例**（把函数当参数传、当返回值）。
   `_draft/41-function.py` 有一个闭包例子，但放在 `_draft` 里没被引用。
3. **没有作用域演示**：局部 / 全局 / `nonlocal` / `global` 一个都没有。
4. **没有类型注解**：现代 Python 代码到处是 `def f(x: int) -> str`，
   素材里 0 处。
