# L5 走查笔记 — 类

> 材料来源：`examples/class/` 下 **12** 个文件。L5 教程页不存在。
> 这一轮的概念密度最高，也是我从 JS `class` 迁移过来摩擦最多的地方。

## 家底盘点

| 文件 | 讲什么 |
|------|--------|
| `class/define.py` | 最简类 + 类上调用方法 |
| `class/instance.py` | `self` 与实例调用 |
| `class/init.py` | `__init__` 初始化实例属性 |
| `class/class-attr.py` | 类属性 vs 实例属性遮蔽 |
| `class/class-attr-over.py` | 未遮蔽时实例透传到类属性 |
| `class/method.py` / `method_assign.py` | 方法绑定：实例取 vs 类取 |
| `class/method_define_outside.py` | 类体外函数赋给类属性 |
| `class/extends.py` | 继承 + `super().__init__` |
| `class/class_attr_doc.py` | 类的 `__doc__` |
| `class/class_attr_class.py` | `实例.__class__` 与 `类.__class__` |
| `class/define-with-statement.py` | 类体语句在定义时执行 |

---

## 概念 1：`class`、`__init__`、`self`

### 逐个符号

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name} eat")

tom = Person('tom', 10)
```

| 符号 | 含义 | JS 对应 |
|------|------|---------|
| `class Person:` | 定义类，括号可省略（无父类时） | `class Person {` |
| `__init__` | 构造器，`Person('tom', 10)` 时自动调用 | `constructor` |
| `self` | **显式**写出「当前实例」，每个方法第一个参数 | 隐式的 `this` |
| `self.name = name` | 在实例上建属性 | `this.name = name` |
| `tom = Person(...)` | 实例化，**必须带括号** | `new Person(...)` |

### 预测 vs 实际

```python
print(f"{tom.name}, age:{tom.age}")
tom.eat()
```

```
tom, age:10
tom eat
```

### 新例子：`self` 是显式参数，所以能「从外面传」

```python
class C:
    def __init__(self, name):
        self.name = name

    def hi(self):
        return f"hi {self.name}"

c = C('tom')
print(C.hi(c))      # hi tom  —— 手动把实例当 self 传进去
```

JS 里做不到这一点（`this` 由调用方式决定，不是参数）。

### 反例：忘了写 `self`

```python
class C:
    def hi():
        return "hi"

print(C.hi())        # hi       —— 类上调用可以
C().hi()             # TypeError: C.hi() takes 0 positional arguments but 1 was given
```

`C().hi()` 时 Python 自动把实例当第一个参数传进去，但 `hi` 一个参数都不收，
于是报「多给了一个」。`class/define.py` 只演示了能通的那种调用，
**把会炸的那种留给了学习者自己撞**。已在走查笔记里补全（不算教程缺陷，
但属素材缺口）。

### 怎样证明我理解了

1. 能说出 `self` 和 JS `this` 的区别（显式参数 vs 隐式绑定）。
2. 能说出 `C().hi()` 在 `def hi():` 下为什么报错。
3. 能说出 `Person('tom', 10)` 和 `new Person('tom', 10)` 的差别（无 `new`）。

---

## 概念 2：类属性 vs 实例属性 —— 遮蔽只发生在实例上

### 逐个符号

```python
class C:
    type = 'C'              # 类属性：写在类体里，所有实例共享

    def __init__(self, foo):
        self.type = foo     # 实例属性：只属于这一个实例
```

| 访问 | 走哪条路 |
|------|---------|
| `C.type` | 直接取类属性 |
| `C('c1').type` | 先看实例 `__dict__`，有就用；没有才回落到类 |

### 预测 vs 实际

```
C.type        → C        ← 猜对
C('c1').type  → c1       ← 猜对（实例属性盖住了类属性）
```

### 新例子：遮蔽不改类，别的实例也不受影响

```python
class C:
    type = 'C'
    def __init__(self, foo):
        self.type = foo

a = C('a')
b = C('b')
print(C.type, a.type, b.type)        # C a b
print('type' in C.__dict__)          # True  —— 类上还在
print('type' in a.__dict__)          # True  —— 实例上也有一份自己的
```

### 反例：不赋值时就透传到类属性

`class-attr-over.py` 的 `Person.type = 'person'` 从不在 `__init__` 里被
`self.type = ...` 覆盖，所以：

```python
print(Person.type, tom.type, jack.type)    # person person person
```

三个都是类属性那份。**「遮蔽」不是默认行为，是 `self.type = ...` 主动造成的。**

### 怎样证明我理解了

1. 能说出 `C('c1').type` 的查找顺序（实例 `__dict__` → 类）。
2. 能说出给实例属性赋值会不会影响类（不会）。
3. 能说出什么时候实例读到的是类属性（实例自己没有同名属性时）。

---

## 概念 3：方法绑定 —— 实例上取到的是「绑定方法」

这是我从 JS 迁移过来**最意外**的一条。

### 逐个符号

```python
c1 = C1('tom')
g = c1.hi        # 取出方法，赋给变量
g()              # hi tom
h = C1.hi        # 从类上取
h(c1)           # hi tom
```

| 写法 | 拿到什么 | 调用方式 |
|------|---------|---------|
| `c1.hi` | **绑定方法**（bound method），`self` 已固定 | `g()` |
| `C1.hi` | 普通函数，`self` 要自己传 | `h(c1)` |

### 预测 vs 实际

```
g = c1.hi; g()   → hi tom      ← 猜对
h = C1.hi; h(c1) → hi tom      ← 猜对，但我不确定为什么两个都能跑
```

### 新例子：绑定方法的 `__self__` 就是那个实例

```python
class C:
    def __init__(self, name):
        self.name = name
    def hi(self):
        return f"hi {self.name}"

c = C('tom')
g = c.hi
print(g.__self__ is c)      # True
```

### 反例：从类上取到的不是绑定方法

```python
print(C.hi)          # <function C.hi at 0x...>   —— 普通函数
print(c.hi)          # <bound method C.hi of ...>  —— 绑定方法
```

**同一个 `hi`，两种形态。** JS 里 `obj.method` 取出来就是函数，
`this` 在调用时才决定；Python 在「取出来」这一步就已经绑好了。
这也是为什么 Python 里 `const g = obj.hi; g()` 不会丢 `this`，
而 JS 里会。

### 怎样证明我理解了

1. 能说出 `c1.hi` 和 `C1.hi` 的区别（绑定方法 vs 普通函数）。
2. 能说出为什么 `g = c1.hi; g()` 不会丢实例（取出时已绑定）。
3. 能说出 `g.__self__ is c1` 的结果（`True`）。

---

## 概念 4：类体外定义的函数也能当方法

`method_define_outside.py` 把模块级函数直接赋给类属性，然后列了五种调用方式：

```python
def hi(self):
    print(f"hi {self.name}")

class C1:
    def __init__(self, name):
        self.name = name
    hi = hi            # 把模块级函数挂成类属性
```

| # | 调用 | 结果 |
|---|------|------|
| 1 | `c1.hi()` | `hi tom` |
| 2 | `g = c1.hi; g()` | `hi tom` |
| 3 | `C1.hi(c1)` | `hi tom` |
| 4 | `h = C1.hi; h(c1)` | `hi tom` |
| 5 | `hi(c1)` | `hi tom` |

### 新例子：`C1.hi is hi` 为 `True`

```python
def hi(self):
    return "hi"

class C:
    hi = hi

print(C.hi is hi)      # True  —— 就是同一个函数对象，没有包装
```

这说明「方法」在 Python 里**不是一种特殊的函数**，而是「放在类里的普通函数」，
绑定行为发生在**访问时**（描述符协议），不是定义时。

### 怎样证明我理解了

1. 能说出 `C1.hi is hi` 的结果和原因（`True`，未包装）。
2. 能说出五种调用方式为什么都能通（都是同一个函数，只是 `self` 来源不同）。

---

## 概念 5：继承与 `super().__init__`

### 逐个符号

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, school):
        super().__init__(name)      # 先建父类那部分
        self.school = school
```

| 符号 | 含义 | JS 对应 |
|------|------|---------|
| `class Student(Person):` | 继承，括号里写父类 | `extends Person` |
| `super()` | 父类代理对象 | `super` |
| `super().__init__(name)` | 调父类构造器 | `super(name)` |
| `self` | **`super().__init__` 里也要显式传 self 吗**——不用，`super()` 已经知道 |

### 预测 vs 实际

```
tom.name    → tom        ← 猜对（父类建的）
tom.school  → s1         ← 猜对（自己建的）
```

### 反例：不调 `super().__init__` 就少一半属性

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, school):
        self.school = school        # 忘了 super()

s = Student('tom', 's1')
s.name        # AttributeError: 'Student' object has no attribute 'name'
```

**Python 不会自动调父类构造器**（JS 的 `class` 字段在某些情况下会）。
忘记 `super().__init__()` 是最常见的继承 bug，素材里没有反例，我自己补的。

### 怎样证明我理解了

1. 能说出 `super().__init__(name)` 做了什么（用父类逻辑初始化 `self`）。
2. 能预测不写它会导致什么（`AttributeError`）。
3. 能说出 `class Student(Person)` 和 JS `extends` 的对应关系。

---

## 概念 6：`__doc__` 和 `__class__`

### `__doc__`

```python
class D:
    """doc of D"""

print(D.__doc__)          # doc of D
print(D().__doc__)        # doc of D  —— 实例读到的是同一份
print(D.__doc__ is D().__doc__)    # True
```

没有 docstring 的类，`__doc__` 是 `None`。这和 L1 概念 3 的三引号/docstring
是同一条规则在类上的体现。

### `__class__`

`class_attr_class.py` 这两行是全组最绕的：

```python
print(C.__class__ == C)        # False
c1 = C()
print(c1.__class__ == C)       # True
```

| 表达式 | 实际值 | 和 `C` 比 |
|--------|--------|----------|
| `C.__class__` | `type`（类也是对象，它的类是 `type`） | `False` |
| `c1.__class__` | `C` | `True` |

**类本身也是一个对象**，它的类是 `type`。这条在 JS 里没有对应物
（JS 的 `class` 不是值，`C.constructor` 语义也不同）。

### 怎样证明我理解了

1. 能说出 `D.__doc__` 和 `D().__doc__` 的关系（同一个对象）。
2. 能说出 `C.__class__` 为什么是 `type` 而不是 `C`。
3. 能说出 `c1.__class__ is C` 的结果（`True`）。

---

## 概念 7：类体语句在**定义时**执行

`define-with-statement.py` 的类体里有 `print`、`for`、`if`：

```python
class C1:
    print("test")
    for i in range(1, 10):
        print(i)
    if __name__ == '__main__':
        print('main')
```

运行这个文件，`test`、`1`–`9`、`main` **立刻全部打印**，不需要实例化。
因为 `class C1:` 这行本身就是一条可执行语句，类体是它的代码块。

### 反例：`if __module__ == '__main__'` 是非主流写法

原文用 `__module__` 判断主模块。实测两种写法行为一致：

```python
class C1:
    if __module__ == '__main__':
        print('main')
    if __name__ == '__main__':
        print('name-main')
```

```
main
name-main
```

`__module__` 在**类体里**能取到模块名（模块层取不到），但惯用写法是 `__name__`。
已把示例改成 `__name__`（行为不变，D-32）。

### 怎样证明我理解了

1. 能说出类体里的 `print` 什么时候执行（定义类时，不等实例化）。
2. 能说出判断「是不是主模块」的惯用写法（`__name__ == '__main__'`）。

---

## 这一轮记下的困惑与解决

| # | 困惑 | 怎么解决的 |
|---|------|-----------|
| C-29 | `c1.hi` 赋给 `g` 之后为什么还不丢实例 | 打印 `g.__self__ is c1` 得 `True`。Python 在取值时就绑定了，JS 是调用时才定 |
| C-30 | `C1.hi(c1)` 手动传 self，感觉很怪 | 想通「方法就是类里的普通函数」之后就合理了。`C1.hi is hi` 为 `True` 是决定性证据 |
| C-31 | `def hi():` 没有 self，为什么 `C1.hi()` 能跑 | 类上调用不传实例。改成 `C1().hi()` 就 TypeError——同一个方法两种命运 |
| C-32 | 类属性被实例「盖住」之后，类属性变了吗 | 没变。`C.__dict__` 里还在，`'type' in C.__dict__` 为 `True` |
| C-33 | 继承时不写 `super().__init__` 会怎样 | 自己造了个 `StudentNoSuper` 复现，得 `AttributeError: no attribute 'name'` |
| C-34 | `C.__class__ == C` 为什么 False | `C.__class__` 是 `type`。类也是对象，它的类是 type |

## 我认为 L5 素材缺的练习

1. **没有 `__str__` / `__repr__`**：`print(实例)` 出来是
   `<__main__.Person object at 0x...>`，学习者完全不知道怎么控制。
2. **没有 `@property` / `@classmethod` / `@staticmethod`** 三种装饰器方法。
3. **没有多态与 MRO 演示**：`extends.py` 只有一个父类一层。
4. **没有「实例属性 vs 类属性」的对照表**：两个示例各讲一半，
   没有并排说明「什么时候读到哪一个」。
5. **没有忘记 `super().__init__` 的反例**（我自己补了，见上）。
