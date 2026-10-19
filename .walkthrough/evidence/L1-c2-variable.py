# L1-概念2 变量赋值
# 学习者前置知识：JS 的 let / const。
#
# 符号逐个解释：
#   name          -> 变量名（标识符），指向右侧的对象
#   =             -> 赋值运算符，把右侧的值"绑定"到左侧名字；不是"相等"
#   "Python"      -> str
#   18            -> int
#   True          -> bool 字面量，注意首字母大写（JS 是小写 true）
#   f"..."        -> f-string，{} 内是表达式，会被求值后替换成文本
#   {name} {age}  -> 花括号内直接写变量名即可，不需要 $ 或 +
#
# 预测（运行前写下）：
#   我叫Python，今年18岁
#
# 关键差异（相对 JS 心智模型）：
#   JS 的变量是"盒子"，Python 的变量是"贴在对象上的名字"（引用语义）。

# --- 教程原文示例 ---
name = "Python"
age = 18
is_student = True
print(f"我叫{name}，今年{age}岁")

# --- 我的新例子：证明我理解 f-string 里可以放表达式 ---
print(f"明年 {age + 1} 岁, is_student={is_student}, 类型={type(is_student).__name__}")

# --- 我的新例子：证明我理解 = 是绑定不是相等（别名共享同一对象）---
a = [1, 2, 3]
b = a
b.append(4)
print("a =", a, "| b =", b, "| a is b ->", a is b)

# --- 反例：int 是不可变的，重新赋值不会影响旧名字 ---
x = 5
y = x
y = 99
print("x =", x, "| y =", y, "| x is y ->", x is y)

# --- 反例：证明 True 首字母必须大写 ---
try:
    bad = true
except NameError as e:
    print("小写 true ->", type(e).__name__, ":", e)
