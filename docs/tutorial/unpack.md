# 嵌套拆包完全指南

> 从简单到复杂，全面理解 Python 的解包赋值语法。

---

## 一、基本解包（单层）

### 语法

```python
a, b = (1, 2)
```

### 完全形式

```python
(变量1, 变量2, ...) = (值1, 值2, ...)
```

等号右侧可以是**任意可迭代对象**：

```python
a, b = [1, 2]      # 列表
a, b = "xy"        # 字符串
a, b, c = range(3) # range 对象
```

---

## 二、多层嵌套解包

### 语法

```python
(a, b), (c, d) = ((1, 2), (3, 4))
```

### 完全形式

```python
(外层变量1, 外层变量2), (外层变量3, 外层变量4) = 嵌套元组
```

### 核心规则

| 规则 | 说明 |
|------|------|
| **层级对应** | 左侧有几个 `(...)`，右侧就有几个嵌套层级 |
| **数量匹配** | 每层括号内的变量数 = 该层元组的元素数 |
| **递归展开** | 从最外层往里拆，每层都是独立解包 |

---

## 三、实际案例

### 案例 1：MNIST 数据加载

```python
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

展开过程：

```
mnist.load_data()
    ↓
((train_images, train_labels), (test_images, test_labels))  ← 嵌套元组
    ↓ 第一层拆包
train_set = (train_images, train_labels)   → 第1个元素
test_set  = (test_images, test_labels)     → 第2个元素
    ↓ 第二层拆包
train_images, train_labels = train_set
test_images, test_labels  = test_set
```

### 案例 2：坐标点列表

```python
(point1, point2), (point3, point4) = ((1, 2), (3, 4))
# point1 = 1, point2 = 2, point3 = 3, point4 = 4
```

### 案例 3：函数返回嵌套数据

```python
def get_user_group():
    return ("Alice", "admin"), ("Bob", "viewer")

(user1_name, user1_role), (user2_name, user2_role) = get_user_group()
# user1_name = "Alice", user1_role = "admin"
# user2_name = "Bob", user2_role = "viewer"
```

---

## 四、完全语法形式

### 完整 BNF 范式

```python
目标表达式 := 变量 | (目标表达式, 目标表达式, ...)
赋值 := 目标表达式 = 可迭代对象
```

简化理解：

```
左边是几层括号，右边就有几层元组
每层括号里的变量数 = 对应层级的元素数
```

### 任意深度嵌套

```python
# 三层嵌套
(a, (b, c)), (d, e) = ((1, (2, 3)), (4, 5))
# a=1, b=2, c=3, d=4, e=5
```

---

## 五、常见错误

### 数量不匹配

```python
# ❌ 错误：左侧需要3个变量，右侧只有2个元素
a, b, c = (1, 2)

# ✅ 正确
a, b = (1, 2)
```

### 嵌套层级不匹配

```python
# ❌ 错误：左侧2层，右侧只有1层
(a, b), c = (1, 2, 3)

# ✅ 正确
a, b, c = (1, 2, 3)
```

---

## 六、星号解包（扩展）

### 剩余值收集

```python
first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5
```

### 嵌套中用星号

```python
(a, *rest), b = ([1, 2, 3], 4)
# a = [1, 2, 3], rest = [2, 3], b = 4
```

---

## 七、速查表

| 场景 | 语法 | 示例 |
|------|------|------|
| 基本解包 | `a, b = iterable` | `a, b = [1, 2]` |
| 嵌套解包 | `(a, b), (c, d) = nested` | `(a, b), (c, d) = ((1, 2), (3, 4))` |
| 丢弃不需要的值 | `a, _, c = ...` | `a, _, c = (1, 99, 3)` |
| 星号收集 | `a, *rest = ...` | `a, *rest = [1, 2, 3, 4]` |
| 嵌套+星号 | `(a, *rest), b = ...` | `(a, *rest), b = ([1, 2, 3], 4)` |

---

## 八、拆包在 Python 中的应用场景

| 场景 | 示例 |
|------|------|
| 函数返回多个值 | `x, y = divmod(10, 3)` |
| 循环解包 | `for k, v in dict.items():` |
| 交换变量 | `a, b = b, a` |
| 解析配置 | `host, port, *rest = args` |
| 数据处理 | `(train, val), test = split_data(data)` |

---

**总结：嵌套拆包的核心就是「层级对应，数量匹配」，有几层括号就有几层元组。**