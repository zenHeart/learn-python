# L1 — Hello Python

> 本节目标：掌握 print、变量、注释的用法，理解这行 TensorFlow 代码的语法结构。

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

## 🎯 理解这行 TensorFlow 代码

```python
from tensorflow.keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

这是**元组拆包**（Tuple Unpacking）。

### 拆解步骤

**Step 1** — `mnist.load_data()` 返回什么？

它返回一个**嵌套元组**：

```
(
  (train_images, train_labels),   ← 第1个元素
  (test_images, test_labels)       ← 第2个元素
)
```

**Step 2** — 外层拆包

```python
(train_set, test_set) = mnist.load_data()
# train_set  = (train_images, train_labels)
# test_set   = (test_images, test_labels)
```

**Step 3** — 内层拆包

```python
train_images, train_labels = train_set
test_images, test_labels    = test_set
```

**Step 4** — 合并为一行（常用写法）

```python
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

---

## 等价的逐步写法

```python
# 原始返回值
result = mnist.load_data()
print(type(result))  # <class 'tuple'>
print(len(result))   # 2

# 外层拆包
train_set, test_set = result

# 内层拆包
train_images, train_labels = train_set
test_images, test_labels  = test_set

print(train_images.shape)  # (60000, 28, 28)
print(train_labels.shape)  # (60000,)
```

---

## 对比 Python 内置数据类型

| 语法 | 类型 | 类比 |
|------|------|------|
| `(a, b)` | 元组（不可变） | 固定顺序的容器 |
| `[a, b]` | 列表（可变） | 随时可变的容器 |
| `{a, b}` | 集合 | 无序、去重 |
| `{'x': a}` | 字典 | 键值对 |

TensorFlow 的 `load_data()` 用的是**嵌套元组**，左侧用**嵌套拆包**接收。

---

## 练习

```python
# 1. 尝试用一个变量接住整个返回值，打印它的结构
data = mnist.load_data()
print(type(data))
print(data[0][0].shape if hasattr(data[0][0], 'shape') else len(data))

# 2. 用拆包语法赋值，观察每个变量的类型和 shape
# (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

> ⚠️ 本教程使用 Pyodide（浏览器端 Python），不包含 TensorFlow。如需运行真正的 MNIST 示例，请在本地 `pip install tensorflow` 后执行。

> ⚠️ L2 数据类型 — 敬请期待
