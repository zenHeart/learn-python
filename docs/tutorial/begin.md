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

---

## 🎯 理解嵌套拆包：从 MNIST 数据加载说起

### 目标代码

```python
from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
```

### 多文件模块结构

```
examples/
└── mnist/
    ├── __init__.py       # 包入口（可省略）
    ├── data.py           # 定义 load_data()
    └── main.py           # 导入并使用
```

**data.py** — 定义数据加载函数：

```python
def load_data():
    return (训练集图片, 训练集标签), (测试集图片, 测试集标签)
```

**main.py** — 导入并拆包：

```python
from mnist.data import load_data
(train_images, train_labels), (test_images, test_labels) = load_data()
```

---

### 嵌套拆包语法拆解

```python
# load_data() 返回的是嵌套元组：
((train_images, train_labels), (test_images, test_labels))

# 左侧有两层括号 → 对应两层拆包
(train_images, train_labels), (test_images, test_labels) = ...
          ↑ 第一层                    ↑ 第一层
            ↑ 第二层                      ↑ 第二层
```

### 等价的逐步写法

```python
# 原始返回值
result = load_data()
# result = ((train_images, train_labels), (test_images, test_labels))

# 外层拆包：分出训练集和测试集
train_set, test_set = result

# 内层拆包：分出图片和标签
train_images, train_labels = train_set
test_images, test_labels = test_set
```

---

## Python 模块导入语法

| 场景 | 语法 | 示例 |
|------|------|------|
| 导入模块 | `import 模块名` | `import mnist` |
| 从模块导入函数 | `from 模块 import 函数` | `from mnist.data import load_data` |
| 导入并改名 | `from 模块 import 函数 as 别名` | `from mnist.data import load_data as ld` |
| 导入多个 | `from 模块 import a, b` | `from mnist.data import a, b` |
| 相对导入（包内） | `from . import sibling` | `from . import data` |

---

## 对比 Python 内置数据类型

| 语法 | 类型 | 类比 |
|------|------|------|
| `(a, b)` | 元组（不可变） | 固定顺序的容器 |
| `[a, b]` | 列表（可变） | 随时可变的容器 |
| `{a, b}` | 集合 | 无序、去重 |
| `{'x': a}` | 字典 | 键值对 |

---

## 练习

```python
# 1. 尝试用一个变量接住整个返回值，打印它的结构
data = load_data()
print("整体结构:", type(data))
print("第1个元素（训练集）:", data[0])
print("第2个元素（测试集）:", data[1])

# 2. 用拆包语法赋值
# (train_images, train_labels), (test_images, test_labels) = load_data()
```

---

> ⚠️ 本教程使用 Pyodide（浏览器端 Python），不支持 `tensorflow`、`numpy` 等 C 扩展库。MNIST 示例使用纯 Python 模拟返回值结构。

---

> ⚠️ L2 数据类型 — 敬请期待
