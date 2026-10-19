# 嵌套拆包完全指南

> 从简单到复杂，全面理解 Python 的解包赋值语法。

---

## 一、基本解包（单层）

### 语法

```python
a, b = (1, 2)
```

### 完全形式

```text
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

```text
(外层变量1, 外层变量2), (外层变量3, 外层变量4) = 嵌套元组
```

### 核心规则

| 规则 | 说明 |
|------|------|
| **层级对应** | 目标有几层嵌套结构，右侧就有几层嵌套（括号可省略，看结构） |
| **数量匹配** | 每层目标的数量 = 该层可迭代对象的元素数 |
| **递归展开** | 从最外层往里拆，每层都是独立解包 |

---

## 三、实际案例

### 案例 1：MNIST 数据加载

```text
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
```

> 这是 TensorFlow 的真实写法，浏览器端没有 `mnist` 模块，所以这里只作示意。
> 可运行版本见 [L1 教程](/tutorial/begin) 的「浏览器可运行版本」。

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

### 简化 BNF 范式

```text
目标表达式 := 变量 | (目标表达式, 目标表达式, ...)
赋值 := 目标表达式 = 可迭代对象
```

> ⚠️ 上面是**简化 BNF，只覆盖本教程用到的形式**，不是 Python 赋值的完整语法。
> 以下目标形式它没有表达，但都合法：
>
> | 未覆盖的形式 | 示例 |
> |---|---|
> | 方括号列表目标 | `[a, b] = [1, 2]` |
> | 属性目标 | `obj.x, obj.y = 10, 20` |
> | 下标目标 | `lst[0], lst[1] = 7, 8` |
> | 星号收集目标 | `a, *rest = [1, 2, 3]` |
>
> 另外括号只是分组符号、可省略：`a, (b, c) = 1, (2, 3)` 与
> `(a, (b, c)) = (1, (2, 3))` 等价。层级靠**目标的结构**决定，不靠括号数量。

简化理解：

```text
目标有几层嵌套结构，右侧就要有几层可迭代对象
每一层的目标数量 = 对应层级的元素数
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
# ❌ 错误：外层只有 2 个目标，右侧却有 3 个元素
(a, b), c = (1, 2, 3)
# 实际报错：ValueError: too many values to unpack (expected 2)
# 注意：报错发生在最外层数量比对，内层 (a, b) 还没被拆到

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

> ⚠️ **星号目标收集到的永远是 `list`**，不跟着右侧容器类型走。
> 这一点很容易搞错——右侧是元组时，`rest` 仍然是列表：
>
> ```python
> a, *rest = (1, 2, 3, 4)      # rest == [2, 3, 4]，类型 list，不是 tuple
> a, *rest = "abcd"            # rest == ['b', 'c', 'd']
> a, *rest = range(4)          # rest == [1, 2, 3]
> ```
>
> 另外星号两侧至少要各有一个非星号目标，否则收集不到东西：
> `a, *b, c = [1]` 会报
> `ValueError: not enough values to unpack (expected at least 2, got 1)`。

### 嵌套中用星号

```python
(a, *rest), b = ([1, 2, 3], 4)
# 外层先拆：第一个目标 (a, *rest) 收到 [1, 2, 3]，第二个目标 b 收到 4
# 内层再拆 [1, 2, 3]：a = 1，rest = [2, 3]
# a = 1, rest = [2, 3], b = 4
```

---

## 七、速查表

| 场景 | 语法 | 示例 |
|------|------|------|
| 基本解包 | `a, b = iterable` | `a, b = [1, 2]` |
| 嵌套解包 | `(a, b), (c, d) = nested` | `(a, b), (c, d) = ((1, 2), (3, 4))` |
| 丢弃不需要的值 | `a, _, c = ...` | `a, _, c = (1, 99, 3)` |
| 星号收集 | `a, *rest = ...` | `a, *rest = [1, 2, 3, 4]` |
| 嵌套+星号 | `(a, *rest), b = ...` | `(a, *rest), b = ([1, 2, 3], 4)` → `a=1, rest=[2,3], b=4` |

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

**总结：嵌套拆包的核心是「结构对应，数量匹配」——左侧目标的嵌套结构决定右侧要拆几层，括号只是分组符号、可省略。**