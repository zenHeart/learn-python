# unpack.md 全量断言核对
# 学习者方法：把教程里每一条"结果 = xxx"的断言写成可执行断言，
# 用 Python 自己判定 TRUE / FALSE，不靠我读代码的印象。

results = []

def check(label, claim, got):
    ok = (claim == got)
    results.append((ok, label, claim, got))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"       教程声称: {claim!r}")
    print(f"       实际得到: {got!r}")

def check_raises(label, fn):
    """教程声称某段代码会报错 -> 只要真的抛异常即 PASS，并记录异常类型与消息。"""
    try:
        fn()
    except Exception as e:
        check(label, "raises", "raises")
        print(f"       异常明细: {type(e).__name__}: {e}")
        return
    check(label, "raises", "NO ERROR — 教程断言错误")

print("=" * 70)
print("一、基本解包（单层）  unpack.md L11-27")
print("=" * 70)

a, b = [1, 2]
check("L24  a, b = [1, 2]", (1, 2), (a, b))

a, b = "xy"
check("L25  a, b = \"xy\"", ("x", "y"), (a, b))

a, b, c = range(3)
check("L26  a, b, c = range(3)", (0, 1, 2), (a, b, c))

print()
print("=" * 70)
print("二、多层嵌套解包  unpack.md L36 / L80 / L88-93 / L117")
print("=" * 70)

(a, b), (c, d) = ((1, 2), (3, 4))
check("L36  (a,b),(c,d) = ((1,2),(3,4))", (1, 2, 3, 4), (a, b, c, d))

(point1, point2), (point3, point4) = ((1, 2), (3, 4))
check("L80  案例2 坐标点", (1, 2, 3, 4), (point1, point2, point3, point4))

def get_user_group():
    return ("Alice", "admin"), ("Bob", "viewer")

(user1_name, user1_role), (user2_name, user2_role) = get_user_group()
check("L90  案例3 get_user_group",
      ("Alice", "admin", "Bob", "viewer"),
      (user1_name, user1_role, user2_name, user2_role))

(a, (b, c)), (d, e) = ((1, (2, 3)), (4, 5))
check("L117 三层嵌套 (a,(b,c)),(d,e)", (1, 2, 3, 4, 5), (a, b, c, d, e))

print()
print("=" * 70)
print('三、常见错误  unpack.md L129 / L139 —— 断言「确实会报错」')
print("=" * 70)

def _l129():
    a, b, c = (1, 2)
check_raises("L129 a, b, c = (1, 2) 应报错", _l129)

def _l139():
    (a, b), c = (1, 2, 3)
check_raises("L139 (a, b), c = (1, 2, 3) 应报错", _l139)

print()
print("=" * 70)
print("六、星号解包  unpack.md L152 / L159")
print("=" * 70)

first, *middle, last = [1, 2, 3, 4, 5]
check("L152 first,*middle,last = [1,2,3,4,5]",
      (1, [2, 3, 4], 5), (first, middle, last))

(a, *rest), b = ([1, 2, 3], 4)
# 修正后的正确结论（2026-10-20 走查）：外层 (a, *rest) 收到 [1,2,3]，
# 内层再拆：a = 1（第一个元素），rest = [2, 3]（星号收集剩余）。
# 教程 2026-10-20 之前写作 a = [1, 2, 3]，那是错的。
check("L159 (a, *rest), b = ([1,2,3], 4)",
      (1, [2, 3], 4), (a, rest, b))

print()
print("=" * 70)
print("七、速查表  unpack.md L171 / L173")
print("=" * 70)

a, _, c = (1, 99, 3)
check("L171 a, _, c = (1, 99, 3)", (1, 3), (a, c))

(a, *rest), b = ([1, 2, 3], 4)
check("L173 速查表 嵌套+星号",
      (1, [2, 3], 4), (a, rest, b))

print()
print("=" * 70)
print("八、应用场景  unpack.md L181 / L183")
print("=" * 70)

x, y = divmod(10, 3)
check("L181 x, y = divmod(10, 3)", (3, 1), (x, y))

a, b = 1, 2
a, b = b, a
check("L183 交换变量 a, b = b, a", (2, 1), (a, b))

print()
print("=" * 70)
print("九、教程未覆盖但 BNF 自称'完整'的边界（我主动构造的反例）")
print("=" * 70)

# 教程 L101-103 自称"完整 BNF 范式": 目标表达式 := 变量 | (目标表达式, ...)
# 反例 1: 方括号列表目标
[a, b] = [1, 2]
check("反例A 方括号目标 [a, b] = [1, 2]（BNF 未覆盖）", (1, 2), (a, b))

# 反例 2: 属性目标
class Box:
    pass
box = Box()
box.x, box.y = 10, 20
check("反例B 属性目标 box.x, box.y = 10, 20（BNF 未覆盖）",
      (10, 20), (box.x, box.y))

# 反例 3: 下标目标
lst = [0, 0]
lst[0], lst[1] = 7, 8
check("反例C 下标目标 lst[0], lst[1] = 7, 8（BNF 未覆盖）",
      (7, 8), (lst[0], lst[1]))

# 反例 4: 括号是可选的 —— 教程"左侧有几个 (...) 就有几层"表述不精确
a, (b, c) = 1, (2, 3)
check("反例D 无外层括号 a, (b, c) = 1, (2, 3)（层级靠结构不靠括号）",
      (1, 2, 3), (a, b, c))

# 反例 5: 右侧是迭代器（一次性）也能拆包
it = iter([1, 2, 3])
p, q, r = it
check("反例E 迭代器目标 p, q, r = iter([1,2,3])", (1, 2, 3), (p, q, r))

# 反例 6: 星号在中间且数量不足时
def _f():
    a, *b, c = [1]
check_raises("反例F a, *b, c = [1] 应报错", _f)

# 反例 7: 集合也能拆包，但顺序不保证（教程说右侧"任意可迭代对象"，未提顺序）
s = {1, 2}
u, v = s
check("反例G 集合拆包 u, v = {1, 2} —— 能拆但顺序不保证",
      "能拆包", "能拆包")

print()
print("=" * 70)
passed = sum(1 for r in results if r[0])
failed = [r for r in results if not r[0]]
print(f"总计 {len(results)} 条断言: {passed} PASS / {len(failed)} FAIL")
if failed:
    print()
    print(">>> FAIL 明细（教程内容错误 / 表述不精确）:")
    for _, label, claim, got in failed:
        print(f"    - {label}")
        print(f"        声称 {claim!r} / 实际 {got!r}")
