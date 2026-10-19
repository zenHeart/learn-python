# L1-概念1 print() 输出
# 学习者前置知识：JS 的 console.log()。
#
# 符号逐个解释：
#   print            -> 内建函数名，把内容写到标准输出（stdout）
#   ( ... )          -> 函数调用，括号内是"参数"
#   "Hello world!"   -> 字符串字面量（str），引号是语法的一部分，不属于内容
#   1 + 2            -> 两个 int 相加，先求值再传入
#   ,                -> 多个参数的分隔符
#   默认 end="\n"    -> 每次调用结束自动补一个换行
#
# 预测（运行前写下）：
#   print("Hello world!")  -> Hello world!
#   print(1 + 2)           -> 3        （先算 1+2=3，再输出 3，没有引号）
#   print("a", "b")        -> a b      （多参数默认用单个空格连接）
#   print(1, 2)            -> 1 2      （数字也会被转成文本再输出）

# --- 教程原文示例 ---
print("Hello world!")
print(1 + 2)

# --- 我的新例子：证明我理解"引号不是内容的一部分" ---
print("引号外", '单引号也可以')

# --- 我的新例子：证明我理解 end 参数 ---
print("不换行", end="")
print("接在后面")

# --- 反例：证明我理解 print 不会返回值到屏幕上，只写 stdout ---
result = print("被赋值的 print")
print("print 的返回值是:", repr(result), "类型:", type(result).__name__)
