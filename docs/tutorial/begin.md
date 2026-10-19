# L1 — Hello Python

> 本节目标：掌握 print、变量、注释、模块导入，理解嵌套拆包语法。

---

## 基础概念

### 1. print 输出

```python
print("Hello world!")
print(1 + 2)
```

**运行结果：**
- `Hello world!`
- `3`

---

### 2. 变量赋值

```python
name = "Python"
age = 18
is_student = True
print(f"我叫{name}，今年{age}岁")
```

---

### 3. 注释

```python
# 这是单行注释
"""
这是多行注释，
通常用于文档字符串
"""
```

> 严格说，`#` 才是注释——解释器会直接丢掉它。
> 三引号包起来的是**字符串**，不是注释：放在函数第一行时它叫 docstring，
> 会被保留下来并可通过 `help()` / `__doc__` 读到。写成「多行注释」是常见
> 简化说法，但别以为它和 `#` 一样不占内存。这段代码点「▶ 运行」没有任何
> 输出，正说明它是个求值后丢弃的表达式。

---

## 🎯 理解嵌套拆包：从 MNIST 数据加载说起

### 先在浏览器里跑通一次

浏览器里没有 `mnist` 包，所以先用一个**自包含**版本看到真实结果。
这段可以直接点「▶ 运行」：

```python
def load_data():
    """模拟 mnist.load_data()：返回 (训练集, 测试集)，各自又是 (图片, 标签)"""
    train_images = [1, 2, 3]
    train_labels = [0, 1, 2]
    test_images = [4, 5]
    test_labels = [1, 0]
    return (train_images, train_labels), (test_images, test_labels)

(train_images, train_labels), (test_images, test_labels) = load_data()

print("训练集图片:", train_images)
print("训练集标签:", train_labels)
print("测试集图片:", test_images)
print("测试集标签:", test_labels)
```

> 先记住这个形状：`load_data()` 吐出来的是 `((图片, 标签), (图片, 标签))`，
> 两层括号对两层拆包。下面所有写法都只是把它换种方式拆开。

### 目标代码（TensorFlow 真实写法）

```text
from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
```

这行代码出自 TensorFlow 的 MNIST 教程。真实项目里 `load_data()` 来自
`tensorflow.keras.datasets`，返回的是 numpy 数组；本教程用纯 Python 模拟
同样的**嵌套结构**，因为浏览器端的 Pyodide 不支持 numpy 这类 C 扩展库。

### 多文件模块结构

仓库里的真实布局（`examples/mnist/`）：

```
examples/
└── mnist/
    ├── data.py           # 定义 load_data()
    └── main.py           # 导入并使用
```

> 仓库里**没有** `__init__.py`。Python 3 的命名空间包不需要它，
> `python -m mnist.main` 一样能跑。

**data.py** — 定义数据加载函数：

```python
def load_data():
    """返回格式：(训练集, 测试集)；训练集 = (训练图片, 训练标签)"""
    train_images = [1, 2, 3]
    train_labels = [0, 1, 2]
    test_images = [4, 5]
    test_labels = [1, 0]
    return (train_images, train_labels), (test_images, test_labels)
```

**main.py** — 导入并拆包：

```text
from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
```

在本地跑它（注意是 `-m`，不是直接跑文件路径）：

```bash
cd examples
python -m mnist.main
```

直接 `python examples/mnist/main.py` 会报
`ModuleNotFoundError: No module named 'mnist'`——因为脚本所在目录不会
被加进模块搜索路径，`mnist` 包找不到。`-m` 会把当前目录加进去。

---

### 嵌套拆包语法拆解

```text
# load_data() 返回的是嵌套元组：
((train_images, train_labels), (test_images, test_labels))

# 左侧有两层结构 → 对应两层拆包
(train_images, train_labels), (test_images, test_labels) = ...
          ↑ 第一层                    ↑ 第一层
            ↑ 第二层                      ↑ 第二层
```

### 等价的逐步写法

把上面那段自包含的 `load_data()` 粘到开头，这段就能直接运行：

```python
def load_data():
    train_images = [1, 2, 3]
    train_labels = [0, 1, 2]
    test_images = [4, 5]
    test_labels = [1, 0]
    return (train_images, train_labels), (test_images, test_labels)

# 原始返回值
result = load_data()
print("result =", result)

# 外层拆包：分出训练集和测试集
train_set, test_set = result
print("train_set =", train_set)
print("test_set  =", test_set)

# 内层拆包：分出图片和标签
train_images, train_labels = train_set
test_images, test_labels = test_set
print("train_images =", train_images, "| train_labels =", train_labels)
print("test_images  =", test_images, "| test_labels  =", test_labels)
```

---

## Python 模块导入语法

| 场景 | 语法 | 示例 |
|------|------|------|
| 导入模块 | `import 模块名` | `import mnist`（之后写 `mnist.data.load_data()`） |
| 从模块导入函数 | `from 模块 import 函数` | `from mnist.data import load_data` |
| 导入并改名 | `from 模块 import 函数 as 别名` | `from mnist.data import load_data as ld` |
| 导入多个 | `from 模块 import a, b` | 需模块里真有 `a` 和 `b`；`mnist.data` 只导出了 `load_data`，所以对它写这行会报 `ImportError: cannot import name 'a'` |
| 相对导入（包内） | `from . import sibling` | `from . import data`（只能在包内部的模块里用；在普通脚本里写会报 `ImportError: attempted relative import with no known parent package`） |

> 前四行是**通用语法形式**，不是都能对着 `mnist` 包跑通的代码。
> `mnist.data` 实际只导出 `load_data` 一个名字，可以在 `examples/` 下验证：
>
> ```bash
> cd examples
> python -c "import mnist.data as d; print([n for n in dir(d) if not n.startswith('_')])"
> # ['load_data']
> ```

---

## 对比 Python 内置数据类型

| 语法 | 类型 | 类比 |
|------|------|------|
| `(a, b)` | 元组（不可变） | 固定顺序的容器 |
| `[a, b]` | 列表（可变） | 随时可变的容器 |
| `{a, b}` | 集合 | 无序、去重 |
| `{'x': a}` | 字典 | 键值对 |

四条性质都可以亲手验证：

```python
# 元组不可变：改元素会抛 TypeError: 'tuple' object does not support item assignment
t = (1, 2)

# 列表可变：能改元素也能追加
lst = [1, 2]
lst[0] = 99
lst.append(3)
print("列表 ->", lst)

# 集合去重且无序：重复元素只剩一个，且不能用下标访问
s = {1, 2, 2, 3, 3, 3}
print("集合长度 ->", len(s), "元素 ->", s)

# 字典按键取值、可增键
d = {'x': 1}
d['y'] = 2
print("字典 ->", d)
```

> 容易混的一点：**空 `{}` 是字典，不是集合**。要空集合得写 `set()`。
> 非空的 `{1, 2}` 才是集合。

---

## 练习

下面两题都可以直接点「▶ 运行」。

**练习 1**：用一个变量接住整个返回值，打印它的结构。

```python
def load_data():
    train_images = [1, 2, 3]
    train_labels = [0, 1, 2]
    test_images = [4, 5]
    test_labels = [1, 0]
    return (train_images, train_labels), (test_images, test_labels)

data = load_data()
print("整体结构:", type(data).__name__)
print("第1个元素（训练集）:", data[0])
print("第2个元素（测试集）:", data[1])
print("一共几层:", len(data))
```

**练习 2**：改用拆包语法一次拿到四个变量，然后验证它们和上面的 `data` 一致。

```python
def load_data():
    train_images = [1, 2, 3]
    train_labels = [0, 1, 2]
    test_images = [4, 5]
    test_labels = [1, 0]
    return (train_images, train_labels), (test_images, test_labels)

(ti, tl), (ei, el) = load_data()
print("训练图片:", ti)
print("训练标签:", tl)
print("测试图片:", ei)
print("测试标签:", el)

# 反过来的验证：拆包前后的数据必须指向同一批对象
data = load_data()
# 注意这里要再套一层括号：== 的优先级高于逗号。
# 写成 (ti, tl), (ei, el) == data 会被解释成两项——(ti, tl) 和 (ei, el) == data。
print("拆包结果与整体结构一致:", ((ti, tl), (ei, el)) == data)
```

**练习 3（自己想）**：把 `load_data()` 的返回值改成三层嵌套，例如
`((a, (b, c)), (d, e))`，然后用一条赋值语句全部拆开。想不出来就回看
[嵌套拆包完全指南](/tutorial/unpack) 的「任意深度嵌套」。

---

> ⚠️ 本教程使用 Pyodide（浏览器端 Python），不支持 `tensorflow`、`numpy` 等 C 扩展库。MNIST 示例使用纯 Python 模拟返回值结构。

---

> ⚠️ L2 数据类型 — 敬请期待
