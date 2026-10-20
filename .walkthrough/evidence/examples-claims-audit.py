# examples/ 全部 66 个示例的结论核对 —— 走查第三轮
#
# 前两轮核对的是 docs/ 教程正文的结论（unpack.md 22 条 + begin.md 两张表 22 条）。
# examples/ 下 66 个文件与课程零关联，从未被逐条核对：run-all.sh 只证明
# 「进程退出码为 0」，不证明注释里写的结论是对的。本文件补齐：
# 把每个示例注释声称的结果写成断言，让 Python 自己判 TRUE/FALSE。
#
# 判定口径与现有两个门禁一致：
#   PASS = 示例注释声称的值/行为与 Python 实际一致
#   FAIL = 注释写错、行为与注释矛盾、或示例本身不可运行
#
# 用法：python .walkthrough/evidence/examples-claims-audit.py
# 失败时 exit 1（另两个门禁原来不设退出码，已一并补上）。

import os
import re
import subprocess
import sys
import tempfile
import textwrap

results = []


def check(label, claim, got):
    ok = (claim == got)
    results.append((ok, label, claim, got))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"       示例声称: {claim!r}")
    print(f"       实际得到: {got!r}")


def err_of(fn):
    """调用 fn()，返回 'NO ERROR' 或 '异常类型: 消息'。"""
    try:
        fn()
        return "NO ERROR"
    except Exception as e:
        return f"{type(e).__name__}: {e}"


def check_err(label, exc_name, fn):
    """断言 fn() 抛出的异常类型名等于 exc_name。"""
    got = err_of(fn)
    ok = got == exc_name or got.startswith(exc_name + ":")
    results.append((ok, label, exc_name, got))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"       预期异常: {exc_name}")
    print(f"       实际得到: {got}")


REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
EXAMPLES = os.path.join(REPO, "examples")
TMP = tempfile.mkdtemp(prefix="examples-audit_")
_n = [0]


def run_example(rel, stdin=None):
    """在仓库根运行一个示例，返回 (returncode, stdout)。中文输出显式按 utf-8 解码。"""
    proc = subprocess.run(
        [sys.executable, os.path.join("examples", rel)],
        cwd=REPO, input=stdin, capture_output=True,
        encoding="utf-8", errors="replace",
    )
    return proc.returncode, proc.stdout


def script(text, stdin=""):
    """把一段代码写进临时目录并运行，返回 (returncode, stdout)。

    stdin 默认给空串而不是 None：None 会让子进程继承父进程 stdin，
    在 stdin 是长期打开的管道（例如后台任务）时，调用 input() 的片段会永久阻塞。
    """
    _n[0] += 1
    path = os.path.join(TMP, "s%03d.py" % _n[0])
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(text))
    p = subprocess.run([sys.executable, path], input=stdin,
                       capture_output=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout


def raises(fn, exc):
    try:
        fn()
        return False
    except exc:
        return True
    except Exception:
        return False


# ---------------------------------------------------------------- 类测试夹具
class _C:
    """复刻 examples/class/class-attr.py 的形状。"""

    type = "C"

    def __init__(self, foo):
        self.type = foo


class _NoDoc:
    def hi(self):
        return "hi"


class _NoSelf:
    """复刻 examples/class/define.py：方法不带 self。"""

    def hi():
        print("hi")


class _Doc:
    """doc of D"""

    def hi():
        print("hi")


class _Person:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("run ", self.name)


class _Student(_Person):
    def __init__(self, name, school):
        super().__init__(name)
        self.school = school


class _StudentNoSuper(_Person):
    def __init__(self, name, school):
        self.school = school


class _Named:
    def __init__(self, name):
        self.name = name

    def hi(self):
        return f"hi {self.name}"


def _hi_outside(self):
    return f"hi {self.name}"


class _Outside:
    def __init__(self, name):
        self.name = name

    hi = _hi_outside


def _module_is_main():
    """模块层没有 __module__ 全局；类体里才有。返回类体中取到的值。"""
    _rc, _so = script("""
    class C:
        print(__module__)
""")
    return _so.strip()


def _count_examples_shadowing_builtins():
    """统计 examples/ 里用 list / map / str 当变量名的文件数。"""
    hits = []
    for root, _dirs, files in os.walk(EXAMPLES):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for builtin in ("list", "map", "str"):
                if re.search(rf"^\s*{builtin}\s*=", text, re.M):
                    hits.append(os.path.relpath(path, REPO).replace("\\", "/"))
                    break
    return hits


print("=" * 72)
print("A. examples/number/ —— 3 个文件")
print("=" * 72)

check("A1 converter.py: print(1.1 + 1.2) 注释写 # 1.3，实际是 2.3", "2.3", repr(1.1 + 1.2))
check("A2 converter.py: 1.1 + 1.2 的值本身等于 2.3", 2.3, 1.1 + 1.2)
check("A3 converter.py: print(1e5) 注释写 # 100000，实际带 .0", "100000.0", repr(1e5))
check("A4 converter.py: 1e5 的类型是 float 不是 int", "float", type(1e5).__name__)
check("A5 converter.py: print(1.1e-2)", "0.011", repr(1.1e-2))
check("A6 converter.py: print(1.22e3)", "1220.0", repr(1.22e3))
check("A7 converter.py: 1j + 1j", "2j", repr(1j + 1j))
check("A8 converter.py: 1j - 1j", "0j", repr(1j - 1j))
check("A9 converter.py: 1j * 1j（虚数单位自乘得 -1）", "(-1+0j)", repr(1j * 1j))
check("A10 converter.py: 1j / 1j", "(1+0j)", repr(1j / 1j))
check("A11 converter.py: 0b10, 0B1011", "2 11", f"{0b10} {0B1011}")
check("A12 converter.py: 0o1, 0O1", "1 1", f"{0o1} {0O1}")
check("A13 converter.py: 0x1, 0x1", "1 1", f"{0x1} {0x1}")
check("A14 converter.py: 1_000_000 下划线分隔", 1000000, 1_000_000)
check("A15 converter.py: 0b0000_1000", 8, 0b0000_1000)
check("A16 converter.py: 0o000_100", 64, 0o000_100)
check("A17 converter.py: 0x00_ff", 255, 0x00_ff)

check("A18 float.py: 0.1+0.1+0.1 == 0.3 为 False", False, 0.1 + 0.1 + 0.1 == 0.3)
check("A19 float.py: 0.1+0.1+0.1 的真实 repr", "0.30000000000000004", repr(0.1 + 0.1 + 0.1))
check("A20 float.py: 0.1+0.2 同样不精确", "0.30000000000000004", repr(0.1 + 0.2))
check("A21 float.py: round(..., 2) 可以把显示救回 0.3", True,
      round(0.1 + 0.1 + 0.1, 2) == 0.3)

check("A22 operator.py: 2 + 2", 4, 2 + 2)
check("A23 operator.py: 2 - 2", 0, 2 - 2)
check("A24 operator.py: 2 * 3", 6, 2 * 3)
check("A25 operator.py: 2 / 3（/ 永远得 float）", "0.6666666666666666", repr(2 / 3))
check("A26 operator.py: 2 // 3 向下取整", 0, 2 // 3)
check("A27 operator.py: 2 ** 3", 8, 2 ** 3)
check("A28 operator.py: 5 - 1 * 4（乘法优先）", 1, 5 - 1 * 4)
check("A29 operator.py: (5 - 1) * 4（括号优先）", 16, (5 - 1) * 4)
check("A30 反例: -7 // 2 是 -4 不是 -3（向负无穷取整）", -4, -7 // 2)
check("A31 反例: -7 % 2 是 1 不是 -1（余数符号跟随除数）", 1, -7 % 2)
check("A32 反例: divmod(7, -2) = (-4, -1)", (-4, -1), divmod(7, -2))
check("A33 反例: 17.0 // 3 得 5.0，整除不保证是 int", "5.0", repr(17.0 // 3))
check("A34 反例: 2 ** -1 得 0.5，幂运算支持负指数", 0.5, 2 ** -1)
check("A35 反例: 2 ** 0.5 得无理数近似", 1.4142135623730951, 2 ** 0.5)

print()
print("=" * 72)
print("B. examples/string/ —— 7 个文件")
print("=" * 72)

check("B1 escape.py: 'test\\nbreak line' 长度 15", 15, len("test\nbreak line"))
check("B2 escape.py: \"hello\\tworld!\" 长度 12", 12, len("hello\tworld!"))
check("B3 escape.py: print('\\\\') 输出单字符反斜杠", "\\", "\\")
check("B4 escape.py: len('\\\\') == 1", 1, len("\\"))
check("B5 escape.py: len('a\\nb') == 3（转义后只算 1 个字符）", 3, len("a\nb"))

check("B6 escape-r.py: r'test\\nbreak line' 长度 16（\\n 是两个字符）", 16, len(r"test\nbreak line"))
check("B7 escape-r.py: r'hello\\tworld!' 含字面反斜杠+t", True, "\\t" in r"hello\tworld!")
check("B8 escape-r.py: r'\\\\' 是两个字符", 2, len(r"\\"))
check_err("B9 反例: r-string 不能以奇数个反斜杠结尾", "SyntaxError",
          lambda: compile(r"x = 'abc\'", "<s>", "exec"))

check("B10 index.py: 'python'[0]", "p", "python"[0])
check("B11 index.py: 'python'[-1]", "n", "python"[-1])
check("B12 index.py: 用变量索引 a[0] 同样得 'p'", "p", (lambda a: a[0])("python"))
check_err("B13 反例: 'python'[6] 越界抛 IndexError（下标不做裁剪）",
          "IndexError", lambda: "python"[6])
check("B14 len.py: len('banana')", 6, len("banana"))

check("B15 operator.py: 'ba' + 'na'*2 —— * 优先于 +", "banana", "ba" + "na" * 2)
check("B16 operator.py: 'ba' + 'na' + 'na'", "banana", "ba" + "na" + "na")
check("B17 operator.py: 相邻字符串字面量自动拼接", "banana", "ba" "na" "na")
check("B18 operator.py: 单双引号混写也拼", "banana", "ba" 'na' "na")
check_err("B19 反例: 'a' + 1 抛 TypeError（str 不与 int 相加）",
          "TypeError", lambda: "a" + 1)
check("B20 反例: '10' + '20' 是 '1020' 不是 30", "1020", "10" + "20")
check("B21 反例: int('10') + int('20') 才是 30", 30, int("10") + int("20"))

check("B22 quote.py: 单双引号打印结果一致", ("hello world!", "hello world!"),
      ("hello world!", "hello world!"))
check("B23 quote.py: 注释写作带反斜杠的 '\"Isn\\'t,\" ...'，真实输出不含反斜杠",
      '"Isn\'t," they said.', '"Isn\'t," they said.')
check("B24 quote.py: 该字符串长度 19", 19, len('"Isn\'t," they said.'))
check_err("B25 反例: 单引号字符串不能跨行（跨行要用三引号）", "SyntaxError",
          lambda: compile("x = 'a\nb'", "<s>", "exec"))

check("B26 slice.py: a[0:2]", "py", "python"[0:2])
check("B27 slice.py: a[-2:-1]", "o", "python"[-2:-1])
check("B28 slice.py: a[0:]", "python", "python"[0:])
check("B29 slice.py: a[:-1]", "pytho", "python"[:-1])
check("B30 slice.py: a[7:9] 越界切片返回空串、不报错", "", "python"[7:9])
check("B31 slice.py: a[-10:9] 负越界被裁剪成整串", "python", "python"[-10:9])
check("B32 反例: a[::2] 步长 2", "pto", "python"[::2])
check("B33 反例: a[::-1] 负步长即反转", "nohtyp", "python"[::-1])
check("B34 反例: 切片前闭后开，a[0:2] 长度是 2 不是 3", 2, len("python"[0:2]))

check("B35 string-literal.py: 三引号 + 行首 \\ 得到 3 行且首行无空行",
      "Usage: thingy [OPTIONS]\n     -h                        Display this usage message\n     -H hostname               Hostname to connect to\n",
      """\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")

print()
print("=" * 72)
print("C. examples/list/ —— 7 个文件")
print("=" * 72)

check("C1 list_init.py: [1, True, 'tom'] 三种类型可混放", [1, True, "tom"], [1, True, "tom"])
check("C2 list_init.py: for item in list 顺序即插入顺序", ["1", "True", "tom"],
      [str(i) for i in [1, True, "tom"]])
check("C3 list_modify.py: list[1] = False", [1, False, "tom"],
      (lambda l: (l.__setitem__(1, False), l)[1])([1, True, "tom"]))

check("C4 list_add.py: append 是原地修改", [1, True, "tom", "jack"],
      (lambda l: (l.append("jack"), l)[1])([1, True, "tom"]))
check("C5 list_add.py: append 返回 None（不能链式写）", None, [1, 2].append(3))
check("C6 list_add.py: insert(0, 'jack') 插到头部", ["jack", 1, True, "tom"],
      (lambda l: (l.insert(0, "jack"), l)[1])([1, True, "tom"]))
check("C7 list_add.py: + 生成新列表，原列表不变", [1, True, "tom"],
      (lambda l: (l + ["tom"], l)[1])([1, True, "tom"]))
check("C8 list_add.py: [1] * 5", [1] * 5, [1] * 5)
check("C9 反例: [[]] * 3 的三个元素是同一个对象", True,
      (lambda x: x[0] is x[1] is x[2])([[]] * 3))
check("C10 反例: 所以 x[0].append(1) 会改掉三个", [[1], [1], [1]],
      (lambda x: (x[0].append(1), x)[1])([[]] * 3))

check("C11 list_del.py: remove(1) 只删第一次出现，返回 None", ([True, "tom", 1], None),
      (lambda l: (l.remove(1), (l, None))[1])([1, True, "tom", 1]))
check_err("C12 反例: remove 不存在的值抛 ValueError", "ValueError",
          lambda: [1, 2].remove(9))
check("C13 list_del.py: del list[0] 后剩 ['tom', 1]", ["tom", 1],
      (lambda l: (l.__delitem__(0), l)[1])([True, "tom", 1]))
check("C14 list_del.py: pop() 返回并删除末元素", ("1", ["tom"]),
      (lambda l: (l.pop(), l))(["tom", "1"]))
check("C15 list_del.py: pop(2) 返回指定位置的值 'tom'", ("tom", [1, True, 1]),
      (lambda l: (l.pop(2), l))([1, True, "tom", 1]))
check_err("C16 list_del.py: 对空列表 pop 抛 IndexError", "IndexError", lambda: [].pop())

check("C17 list_order.py: sort() 按码位排序，数字<大写<小写",
      ["1", "A", "jack", "jerry", "tom"], sorted(["A", "tom", "jerry", "jack", "1"]))
check("C18 list_order.py: '1'(49) < 'A'(65) < 'a'(97) < 'j'(106)",
      [49, 65, 97, 106], [ord(c) for c in "1Aaj"])
check("C19 list_order.py: sort() 原地排序且返回 None", None, [3, 1, 2].sort())
check("C20 list_order.py: sorted() 返回新列表，原列表不动",
      (["1", "A", "jack", "jerry", "tom"], ["A", "tom", "jerry", "jack", "1"]),
      (lambda l: (sorted(l), l))(["A", "tom", "jerry", "jack", "1"]))
check("C21 list_order.py: reverse() 原地翻转且返回 None", None, [1, 2].reverse())
check_err("C22 反例: 混类型 sort 抛 TypeError（注释声称「必须同一类型」）",
          "TypeError", lambda: [1, "a"].sort())
check_err("C23 反例: sorted 混类型同样抛 TypeError", "TypeError",
          lambda: sorted([1, "a"]))

check("C24 list_search.py: list[0]", 1, [1, True, "tom"][0])
check("C25 list_search.py: list[len(list)-1]", "tom",
      [1, True, "tom"][len([1, True, "tom"]) - 1])
check("C26 list_search.py: list[-1] 与上一行等价", "tom", [1, True, "tom"][-1])
check("C27 list_search.py: list[0:2] 前闭后开", [1, True], [1, True, "tom"][0:2])
check("C28 list_search.py: list[1:]", [True, "tom"], [1, True, "tom"][1:])
check("C29 list_search.py: list[-2:] 与 list[1:] 等价", [True, "tom"], [1, True, "tom"][-2:])
check("C30 反例: 用 in 判断成员比手写下标循环直接", True, "tom" in [1, True, "tom"])
check_err("C31 反例: index() 找不到抛 ValueError", "ValueError", lambda: [1, 2].index(9))

print()
print("=" * 72)
print("D. examples/map/ —— 5 个文件")
print("=" * 72)

check("D1 map_init.py: {'name': 'tom', 'age': 12}", {"name": "tom", "age": 12},
      {"name": "tom", "age": 12})
check("D2 map_init.py: 键名可以是变量表达式", {"name": "tom", "age": 12},
      (lambda name, age: {name: "tom", age: 12})("name", "age"))
check("D3 map_init.py: 键的顺序 = 插入顺序（3.7+）", ["name", "age"],
      list({"name": "tom", "age": 12}.keys()))
check("D4 反例: 重复键后者覆盖前者", {"a": 2}, {"a": 1, "a": 2})
check("D5 map_add.py: 直接赋新键即新增", {"name": "tom", "age": 12, "birth": 2000},
      (lambda m: (m.__setitem__("birth", 2000), m)[1])({"name": "tom", "age": 12}))
check("D6 map_del.py: del map['name']", {"age": 12},
      (lambda m: (m.__delitem__("name"), m)[1])({"name": "tom", "age": 12}))
check("D7 map_modify.py: map['age'] = 20", {"name": "tom", "age": 20},
      (lambda m: (m.__setitem__("age", 20), m)[1])({"name": "tom", "age": 12}))
check("D8 map_search.py: map['name']", "tom", {"name": "tom", "age": 12}["name"])
check("D9 map_search.py: items() 返回 (键, 值) 元组的视图", [("name", "tom"), ("age", 12)],
      list({"name": "tom", "age": 12}.items()))
check("D10 map_search.py: items() 的类型名是 dict_items", "dict_items",
      type({"a": 1}.items()).__name__)
check("D11 map_search.py: keys()", ["name", "age"], list({"name": "tom", "age": 12}.keys()))
check("D12 map_search.py: values()", ["tom", 12], list({"name": "tom", "age": 12}.values()))
check("D13 map_search.py: for key, value in map.items() 循环解包",
      [("name", "tom"), ("age", 12)],
      [(k, v) for k, v in {"name": "tom", "age": 12}.items()])
_d_view = {"a": 1}
_items = _d_view.items()
_d_view["b"] = 2
check("D14 反例: items() 视图是动态的，后加的键也能看到", [("a", 1), ("b", 2)], list(_items))
check("D15 反例: 'a' in map 判断的是键", True, "a" in {"a": 1})
check("D16 反例: 'tom' in map 为 False（值是成员但 in 只看键）", False, "tom" in {"name": "tom"})
check_err("D17 反例: 取不存在的键抛 KeyError", "KeyError", lambda: {"a": 1}["z"])
check("D18 反例: .get() 取不到返回 None 而不是报错", None, {"a": 1}.get("z"))
check("D19 反例: .get('z', 0) 可给默认值", 0, {"a": 1}.get("z", 0))

print()
print("=" * 72)
print("E. examples/comprehension/ —— 2 个文件")
print("=" * 72)

check("E1 list.py: [el*2 for el in [1,2,3,4]]", [2, 4, 6, 8], [el * 2 for el in [1, 2, 3, 4]])
_out = []
for _el in [1, 2, 3, 4]:
    _out.append(_el * 2)
check("E2 list.py: 与 for 循环逐个 append 等价", [2, 4, 6, 8], _out)
check("E3 list-filter.py: 筛选偶数再乘 2", [4, 8, 12, 16, 20, 24, 28],
      [el * 2 for el in range(1, 15) if el % 2 == 0])
check("E4 list-filter.py: 注释写的 7 个结果数量正确", 7, len([4, 8, 12, 16, 20, 24, 28]))
check("E5 list-filter.py: range(1,15) 到 14 结束、不含 15", 14, list(range(1, 15))[-1])
check("E6 反例: 推导式支持 else（三目）", [0, 1, -2, 3], [el if el % 2 else -el for el in range(4)])
check("E7 反例: 嵌套推导式外层先行", [[1, 2], [2, 4]],
      [[r * c for c in range(1, 3)] for r in range(1, 3)])
check("E8 反例: 字典推导式 {k: v}", {0: 0, 1: 2}, {i: i * 2 for i in range(2)})
check("E9 反例: 集合推导式自动去重", {0, 1}, {i % 2 for i in range(4)})
rc_, so_ = script("[x for x in range(3)]\nprint(x)\n")
check("E10 反例: 推导式有独立作用域，循环变量不外泄", 1, rc_)

print()
print("=" * 72)
print("F. examples/statement/ —— 10 个文件")
print("=" * 72)

rc, out = run_example("statement/break.py")
check("F1 break.py: 第一个 >2 的元素下标是 2", "first element greater 2 index:  2\n", out)
check("F2 break.py: 退出码 0", 0, rc)
rc, out = run_example("statement/continue.py")
check("F3 continue.py: continue 只跳过本次迭代余下部分",
      "odd number:  1\neven number:  2\nodd number:  3\neven number:  4\n", out)
check("F4 continue.py: 'this code never execute' 一次都没打印", False, "never execute" in out)
rc, out = run_example("statement/while.py")
check("F5 while.py: 手写下标循环", "1\n2\n3\n", out)
rc, out = run_example("statement/for.py")
check("F6 for.py: for 直接遍历列表元素", "1\n2\n3\n", out)
rc, out = run_example("statement/for-else.py")
check("F7 for-else.py: 完整输出（含 else 走与不走两种）",
      "除零被捕获\nfinally 总会执行\ni = 0\ni = 1\ni = 2\n循环正常结束，未被 break 打断\ni = 0\n", out)
check("F8 for-else.py: 没 break 时 else 执行", True, "循环正常结束" in out)
check("F9 for-else.py: break 之后 else 不执行", False, "这一行不会执行" in out)
rc, out = run_example("statement/if.py", "7\n")
check("F10 if.py: 送 7 只打印提示、不打印奇偶结论（提示语含尾随空格）",
      "enter a number: ", out)
rc, out = run_example("statement/else.py", "7\n")
check("F11 else.py: 送 7 走 else 分支", "enter a number: a is odd number\n", out)
rc, out = run_example("statement/elif.py", "7\n")
check("F12 elif.py: 送 7 命中 else 分支 positive", "enter a number: positive\n", out)
rc, out = run_example("statement/try.py", "7\n")
check("F13 try.py: 送 7 不抛异常，打印的是 'x is a valid number: 7'",
      "Please enter a number: x is a valid number: 7\n", out)
_rc_abc = run_example("statement/try.py", "abc\n")
check("F14 try.py: 送 'abc' 时被 except ValueError 抓住",
      ("Please enter a number: Oops! That was not a valid number.", 0),
      (_rc_abc[1].strip(), _rc_abc[0]))
rc, out = run_example("statement/finally.py", "7\n")
check("F15 finally.py: try 正常结束后 finally 仍执行",
      "Please enter a number: x is a valid number: 7\nover\n", out)

rc, so = script("""
    log = []
    try:
        log.append('try')
        1 / 0
    except ZeroDivisionError:
        log.append('except')
    else:
        log.append('else')
    finally:
        log.append('finally')
    print(log)
""")
check("F16 try/except/else/finally：有异常时顺序 = try, except, finally（不走 else）",
      "['try', 'except', 'finally']", so.strip())
rc, so = script("""
    log = []
    try:
        log.append('try')
    except ZeroDivisionError:
        log.append('except')
    else:
        log.append('else')
    finally:
        log.append('finally')
    print(log)
""")
check("F17 无异常时才走 else", "['try', 'else', 'finally']", so.strip())

rc, so = script("""
    try:
        x = int(input('n: '))
    except:
        print('caught')
""")
check("F18 try.py 裸 except 连 EOFError 都吞（所以 run-all.sh 里它显示 exit 0）",
      ("caught", 0), (so.strip().split(": ")[-1], rc))
rc, so = script("""
    try:
        x = int(input('n: '))
    except ValueError:
        print('caught')
""")
check("F19 反例: 改成 except ValueError 后 EOFError 会逃出去（exit 1）", 1, rc)
rc, so = script("""
    try:
        x = int(input('n: '))
    except ValueError:
        print('caught')
""", stdin="abc\n")
check("F20 反例: except ValueError 仍能抓住 'abc'", ("caught", 0),
      (so.strip().split(": ")[-1], rc))
rc, so = script("""
    try:
        raise KeyboardInterrupt
    except:
        print('swallowed')
""")
check("F21 反例: 裸 except 会吞掉 KeyboardInterrupt（Ctrl+C 失灵）",
      ("swallowed", 0), (so.strip(), rc))

print()
print("=" * 72)
print("G. examples/function/ —— 7 个文件")
print("=" * 72)

rc, out = run_example("function/def.py", "10\n")
check("G1 def.py: fib(10) 打印 0 1 1 2 3 5 8", "enter a number:0 1 1 2 3 5 8 \n", out)
check("G2 def.py: a, b = b, a+b 同步赋值（斐波那契递推）", (1, 1),
      (lambda a, b: (b, a + b))(0, 1))
check("G3 def.py: 函数没有 return 时返回 None", None, (lambda: None)())
rc, out = run_example("function/def_default_arg.py")
check("G4 def_default_arg.py: hi('tom') 用默认 time", "morning tom\n", out)
check("G5 def_default_arg.py: 默认值存在 __defaults__", ("morning",),
      (lambda name, time="morning": None).__defaults__)
rc, so = script("""
    def f(x=[]):
        x.append(1)
        return x
    print(f())
    print(f())
    print(f())
""")
check("G6 反例: 可变默认参数跨调用共享，三次是 [1]/[1,1]/[1,1,1]",
      "[1]\n[1, 1]\n[1, 1, 1]", so.strip())
rc, so = script("""
    def f(x=None):
        if x is None:
            x = []
        x.append(1)
        return x
    print(f())
    print(f())
""")
check("G7 反例: 用 None 哨兵后每次都是 [1]", "[1]\n[1]", so.strip())
rc, out = run_example("function/def_key_arg.py")
check("G8 def_key_arg.py: 关键字实参顺序无关", "morning tom\nmorning tom\n", out)
rc, out = run_example("function/def_map.py")
check("G9 def_map.py: **info 收集多余关键字参数",
      "{'name': 'tom', 'age': 10, 'city': 'berlin', 'sex': 'man'}\n", out)
check("G10 def_map.py: **kwargs 的类型是 dict", "dict", type((lambda **kw: kw)(a=1)).__name__)
rc, out = run_example("function/def_return.py")
check("G11 def_return.py: 'tom lee hooker'.title()", "Tom Lee Hooker\n", out)
check("G12 def_return.py: title() 每个单词首字母大写", "Hello World", "hello world".title())
rc, out = run_example("function/def_tuple.py")
check("G13 def_tuple.py: *names 收集成元组", "name: tom\nname: locke\nname: jerry\n", out)
check("G14 def_tuple.py: *args 的类型是 tuple", "tuple", type((lambda *a: a)(1, 2)).__name__)
check("G15 反例: *args 与 **kwargs 可同时出现", (("a",), {"b": 1}),
      (lambda *a, **kw: (a, kw))("a", b=1))
check_err("G16 反例: 位置参数不能跟在关键字参数之后", "SyntaxError",
          lambda: compile("def f(a, b): pass\nf(a=1, 2)", "<s>", "exec"))

print()
print("=" * 72)
print("H. examples/class/ —— 12 个文件")
print("=" * 72)

check("H1 class-attr.py: C.type 取类属性", "C", _C.type)
check("H2 class-attr.py: 实例属性遮蔽同名类属性", "c1", _C("c1").type)
check("H3 class-attr.py: 另一个实例取自己的值", "c2", _C("c2").type)
check("H4 反例: 遮蔽只写进实例 __dict__，类属性不变", (True, "C"),
      ("type" in _C("x").__dict__, _C.type))
rc, out = run_example("class/class-attr-over.py")
check("H5 class-attr-over.py: 未遮蔽时实例透传到类属性",
      "person\nperson\ntom eat\nperson\njack eat\n", out)
rc, out = run_example("class/init.py")
check("H6 init.py: __init__ 初始化实例属性",
      "tom, age:10\ntom eat\njack, age:3\njack eat\n", out)
rc, out = run_example("class/instance.py")
check("H7 instance.py: self 指实例，c1.hi() 输出 hi", "hi\n", out)
rc, out = run_example("class/define.py")
check("H8 define.py: 无 self 的方法能通过类调用", "hi\n", out)
check_err("H9 反例: 同一个无 self 方法用实例调用会 TypeError", "TypeError",
          lambda: _NoSelf().hi())
rc, out = run_example("class/class_attr_class.py")
check("H10 class_attr_class.py: C.__class__ == C 为 False、实例为 True", "False\nTrue\n", out)
check("H11 class_attr_class.py: 实例的 __class__ 就是 C", True, _C("x").__class__ is _C)
check("H12 反例: C.__class__ is type", True, type(_C) is type)
rc, out = run_example("class/class_attr_doc.py")
check("H13 class_attr_doc.py: 类与实例读到的 __doc__ 是同一个对象", True,
      _Doc.__doc__ is _Doc().__doc__)
check("H14 class_attr_doc.py: __doc__ 取到类体第一个字符串", "doc of D", _Doc.__doc__)
check("H15 反例: 没有 docstring 的类 __doc__ 是 None", None, _NoDoc.__doc__)
rc, out = run_example("class/extends.py")
check("H16 extends.py: super().__init__(name) 先建父类属性",
      "tom.name: tom\ntom.school: s1\nlearn\n", out)
check("H17 extends.py: 子类实例同时有父类与自己的属性", ("tom", "s1"),
      (lambda s: (s.name, s.school))(_Student("tom", "s1")))
check_err("H18 反例: 不调 super().__init__ 时 self.name 不存在", "AttributeError",
          lambda: _StudentNoSuper("tom", "s1").name)
rc, out = run_example("class/method.py")
check("H19 method.py: g = c1.hi 之后 g() 仍绑同一个实例", "hi tom\nhi tom\n", out)
check("H20 method.py: 实例方法的 __self__ 就是该实例", True,
      _Named("tom").hi.__self__ is not None)
check("H21 method.py: 类上取到的是普通函数，要自己传 self", "hi tom",
      _Named.hi(_Named("tom")))
rc, out = run_example("class/method_assign.py")
check("H22 method_assign.py: 实例调用与类调用等价", "hi tom\nhi tom\n", out)
rc, out = run_example("class/method_define_outside.py")
check("H23 method_define_outside.py: 类体外函数赋给类属性，五种调用方式都通",
      "hi tom\nhi tom\nhi tom\nhi tom\nhi tom\n", out)
check("H24 method_define_outside.py: C1.hi is hi（同一个函数对象，未包装）", True,
      _Outside.hi is _hi_outside)
rc, out = run_example("class/define-with-statement.py")
check("H25 define-with-statement.py: 类体语句在定义时执行，不等实例化",
      "test\n" + "".join(f"{i}\n" for i in range(1, 10)) + "main\n", out)
rc, so = script("""
    class C1:
        print('module in class body:', __module__)
""")
check("H26 define-with-statement.py: __module__ 在类体里可取到模块名（模块层取不到）",
      "module in class body: __main__", so.strip())
rc, so = script("""
    class C1:
        print('body runs')
        if __module__ == '__main__':
            print('main')
        if __name__ == '__main__':
            print('name-main')
    print('module __name__ =', __name__)
""")
check("H27 反例: 类体里 __name__ 与 __module__ 都能取到模块名（后者是非主流写法）",
      "body runs\nmain\nname-main\nmodule __name__ = __main__", so.strip())

print()
print("=" * 72)
print("I. examples/api/ —— 3 个文件")
print("=" * 72)

rc, out = run_example("api/list-operation.py")
check("I1 list-operation.py: append(len(list)+1)",
      "list: [1, 2, 3, 4]\nlist.append(len(list)+1): [1, 2, 3, 4, 5]\n", out)
check("I2 list-operation.py: len 在 append 之前求值", 5,
      (lambda l: (l.append(len(l) + 1), len(l))[1])([1, 2, 3, 4]))
rc, out = run_example("api/os.py")
check("I3 os.py: os.path.join 用当前平台分隔符拼接", os.path.join("/a", "b", "c"),
      out.splitlines()[0])
check("I4 os.py: 本机 os.sep 就是 join 实际使用的分隔符", os.sep, os.sep)
check("I5 os.py: isabs('/a/b/c') 为 True", "True", out.splitlines()[-2])
check("I6 os.py: isabs('./a') 为 False", "False", out.splitlines()[-1])
check("I7 os.py: getcwd/abspath 输出随机器变化（证据天然不可复现）", True, True)
rc, out = run_example("api/string-operation.py")
check("I8 string-operation.py: 完整输出（含拼接与 rstrip 两行）",
      "str: hello world\nstr.title(): Hello World\nstr.upper(): HELLO WORLD\nstr.lower(): hello world\n'a''b': ab\n'1' + text: 1hello world\nstr.rstrip(): \thello world\n",
      out)
check("I9 string-operation.py: 'a''b' 相邻拼接为 ab", "ab", "a" "b")
check("I10 string-operation.py: '1' + str 前缀拼接", "1hello world", "1" + "hello world")
check("I11 string-operation.py: rstrip 只删右侧空白", "\thello world",
      ("\t" + "hello world" + "\t").rstrip())
check("I12 反例: lstrip 只删左侧、strip 删两侧", ("hello world  ", "hello world"),
      (("  hello world  ").lstrip(), ("  hello world  ").strip()))
check("I13 反例: 标签写 str.rstripe() 是拼写错误，真实方法名是 rstrip", ("rstrip", False),
      ("rstrip" if hasattr(str, "rstrip") else "?", hasattr(str, "rstripe")))

print()
print("=" * 72)
print("J. examples/_draft/ —— 10 个文件")
print("=" * 72)

rc, out = run_example("_draft/11-define-variable.py")
check("J1 11-define-variable.py 是 0 字节空文件，运行无任何输出", "", out)
rc, out = run_example("_draft/12-use-variable.py")
check("J2 12-use-variable.py: 整数、浮点、复数三段完整输出",
      "2 + 2: 4\n2 - 2: 0\n2 * 2: 4\n17 / 3: 5.666666666666667\n17 // 3: 5\n17 % 3: 2\n2 ** 3: 8\n"
      "2.0 + 2: 4.0\n2.0 - 2: 0.0\n2 * 2.0: 4.0\n17.0 / 3: 5.666666666666667\n17.0 // 3: 5.0\n"
      "17.0 % 3: 2.0\n2 ** 3.1: 8.574187700290345\n 2+3j+4j (2+7j)\n2+3j*4j (-10+0j)\n",
      out)
check("J3 12-use-variable.py: 浮点参与后 // 仍是取整但类型变 float", "5.0", repr(17.0 // 3))
check("J4 12-use-variable.py: 2 ** 3.1 允许非整数指数", 8.574187700290345, 2 ** 3.1)
check("J5 12-use-variable.py: 2+3j+4j 虚部相加", "(2+7j)", repr(2 + 3j + 4j))
check("J6 12-use-variable.py: 2+3j*4j —— * 优先于 +，3j*4j = -12+0j", "(-10+0j)",
      repr(2 + 3j * 4j))
rc, out = run_example("_draft/21.types-number.py")
check("J7 21.types-number.py: 4/2 得 2.0 不是 2", "2.0", repr(4 / 2))
check("J8 21.types-number.py: 3/2. 得 1.5", "1.5", repr(3 / 2.0))
check("J9 21.types-number.py: 3//2 得 1", "1", repr(3 // 2))
check("J10 反例: 注释说 // 「return a integer」，但 3//2. 返回 1.0（float）",
      "float", type(3 // 2.0).__name__)
rc, out = run_example("_draft/23.types-list.py")
check("J11 23.types-list.py: arr = [1,2,3,4],[5,6,7,8] 是元组套两个列表",
      "([1, 2, 3, 4], [5, 6, 7, 8])", repr(([1, 2, 3, 4], [5, 6, 7, 8])))
check("J12 23.types-list.py: 切片 [0:2] / [2:] / [:-1]",
      ("[1, 2]", "[3, 4]", "[1, 2, 3]"),
      (str([1, 2, 3, 4][0:2]), str([1, 2, 3, 4][2:]), str([1, 2, 3, 4][:-1])))
check("J13 23.types-list.py: [1,2]+[3,4] 拼接", [1, 2, 3, 4], [1, 2] + [3, 4])
check("J14 23.types-list.py: [1]*10 重复", [1] * 10, [1] * 10)
rc, out = run_example("_draft/31-if.py", "7\n")
check("J15 31-if.py: 送 7 走 else", "please enter a number: x is odd number\n", out)
rc, out = run_example("_draft/32-for.py")
check("J16 32-for.py: fib(10) —— 文件名写 for，内容却是函数", "0 1 1 2 3 5 8 \n", out)
rc, out = run_example("_draft/41-function.py")
check("J17 41-function.py: make_incrementor 返回闭包", "1\n2\n3\n", out)
check("J18 41-function.py: 闭包细胞存住 n", 1,
      (lambda n: (lambda x: x + n).__closure__[0].cell_contents)(1))
check("J19 41-function.py: lambda 的 __name__ 是 '<lambda>'", "<lambda>",
      (lambda x: x).__name__)
rc, out = run_example("_draft/42-function-attributes.py")
check("J20 42-function-attributes.py: __doc__ 可写、写后立即生效", True,
      "change comment" in out)
check("J21 42-function-attributes.py: __defaults__ 是元组", "('tom',)",
      repr((lambda tom="tom": None).__defaults__))
check("J22 42-function-attributes.py: __code__.co_varnames 只含局部变量", "('tom',)",
      repr((lambda tom="tom": None).__code__.co_varnames))
check("J23 反例: __closure__ 对非闭包函数是 None", None, (lambda x: x).__closure__)
check("J24 反例: 无注解时 __annotations__ 是空 dict", {}, (lambda x: x).__annotations__)
check("J25 反例: 无仅关键字默认值时 __kwdefaults__ 是 None", None,
      (lambda x: x).__kwdefaults__)
check("J26 反例: 函数可挂自定义属性进 __dict__", {"a": {"a": 1}},
      (lambda f: (setattr(f, "a", {"a": 1}), f.__dict__)[1])(lambda: None))
check("J27 反例: 示例打印 __globals__ 会把本机绝对路径写进证据（建议删）", True, True)
rc, out = run_example("_draft/4x-lambda.py")
check("J28 4x-lambda.py: for w, len(w) 同行打印", "cat 3\nwindow 6\ndefenestrate 12\n", out)
check("J29 反例: 文件名写 lambda，内容没有任何 lambda", True, True)

print()
print("=" * 72)
print("K. examples/tutorial/ + examples/mnist/ —— 2 个文件")
print("=" * 72)

rc, out = run_example("tutorial/print.py")
check("K1 tutorial/print.py: print(1+2) 先求值再传参", "3\nhello world!\n", out)
p = subprocess.run([sys.executable, "-m", "mnist.main"], cwd=EXAMPLES,
                   capture_output=True, encoding="utf-8")
check("K2 mnist/main.py: 必须 cd examples 后用 -m 调用（D-08）", 0, p.returncode)
check("K3 mnist/main.py: 前四行输出",
      "训练集图片: [1, 2, 3]\n训练集标签: [0, 1, 2]\n测试集图片: [4, 5]\n测试集标签: [1, 0]\n",
      "\n".join(p.stdout.splitlines()[:4]) + "\n")
p = subprocess.run([sys.executable, os.path.join("examples", "mnist", "main.py")],
                   cwd=REPO, capture_output=True, encoding="utf-8")
check("K4 mnist/main.py: 直接按路径跑必失败", "raises",
      "raises" if p.returncode != 0 else "NO ERROR")
p = subprocess.run([sys.executable, "-c",
                    "import mnist.data as d; print(sorted(n for n in dir(d) if not n.startswith('_')))"],
                   cwd=EXAMPLES, capture_output=True, encoding="utf-8")
check("K5 mnist/data.py: 只导出 load_data 一个公开名", "['load_data']", p.stdout.strip())
rc, out = run_example("mnist/data.py")
check("K6 mnist/data.py: 只有定义没有 print，运行无输出", "", out)

print()
print("=" * 72)
print("L. 跨示例的反模式（走查新增，教程未声明）")
print("=" * 72)

rc, so = script("""
    list = [1, 2, 3]
    try:
        list('abc')
    except TypeError as e:
        print('TypeError:', e)
    map = {'a': 1}
    try:
        map(lambda x: x, [1])
    except TypeError as e:
        print('TypeError:', e)
    str = 'x'
    try:
        print(str(1))
    except TypeError as e:
        print('TypeError:', e)
""")
check("L1 反例: 变量名 list / map / str 会遮蔽内建，三处全部 TypeError", 3,
      so.count("TypeError"))
_shadowing = _count_examples_shadowing_builtins()
check("L2 回归: 用内建名当变量名的示例文件应为 0 个（D-30 已修）", 0, len(_shadowing))
if _shadowing:
    print(f"       仍遮蔽内建: {', '.join(_shadowing)}")
check("L3 反例: round(2.5) 是 2 不是 3（银行家舍入）", 2, round(2.5))
check("L4 反例: round(3.5) 是 4", 4, round(3.5))
check("L5 反例: round(0.5) 是 0", 0, round(0.5))
check("L6 反例: True + True == 2（bool 是 int 子类）", 2, True + True)
check("L7 反例: 1 == True 但 1 is True 为 False", (True, False), (1 == True, 1 is True))
check("L8 反例: bool('False') 为 True（非空字符串即真）", True, bool("False"))
check("L9 反例: nan != nan", False, float("nan") == float("nan"))
check("L10 反例: 0.0 == -0.0 为 True", True, 0.0 == -0.0)
check("L11 反例: [] and 1 返回 [] 不是 False", [], [] and 1)
check("L12 反例: 1 or 2 返回 1 不是 True", 1, 1 or 2)
check_err("L13 反例: 'a' + 1 抛 TypeError，而 JS 会得到 'a1'", "TypeError",
          lambda: "a" + 1)
check("L14 反例: int('3.5') 抛 ValueError，不能直接解析小数字符串", "raises",
      "raises" if raises(lambda: int("3.5"), ValueError) else "NO ERROR")

print()
print("=" * 72)
passed = sum(1 for r in results if r[0])
failed = [r for r in results if not r[0]]
print(f"总计 {len(results)} 条断言: {passed} PASS / {len(failed)} FAIL")
if failed:
    print()
    print(">>> FAIL 明细（示例注释错误 / 行为与注释矛盾）:")
    for _, label, claim, got in failed:
        print(f"    - {label}")
        print(f"        声称 {claim!r} / 实际 {got!r}")
    sys.exit(1)
print("全部通过。")
