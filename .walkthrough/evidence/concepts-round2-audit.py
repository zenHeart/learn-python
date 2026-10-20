# begin.md 「Python 模块导入语法」+「对比 Python 内置数据类型」
# unpack.md 「八、拆包在 Python 中的应用场景」—— 走查补充核对
#
# 这三个表格在 begin.md / unpack.md 里存在，但第一轮走查没把它们过概念循环。
# 本文件补齐：每条声称写成断言，让 Python 自己判定。

import os
import sys
import tempfile
import textwrap

results = []

def check(label, claim, got):
    ok = (claim == got)
    results.append((ok, label, claim, got))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"       教程声称: {claim!r}")
    print(f"       实际得到: {got!r}")

print("=" * 72)
print("A. begin.md 「Python 模块导入语法」5 种形式")
print("=" * 72)

# 用一个临时包测相对导入，不污染仓库
TMP = tempfile.mkdtemp(prefix="importtest_")
PKG = os.path.join(TMP, "demopkg")
os.makedirs(PKG)
with open(os.path.join(PKG, "__init__.py"), "w", encoding="utf-8") as f:
    f.write("PACKAGE_MARKER = 'i am demopkg'\n")
with open(os.path.join(PKG, "data.py"), "w", encoding="utf-8") as f:
    f.write(textwrap.dedent('''
        VALUE = 41
        OTHER = 42
        def load_data():
            return (1, 2), (3, 4)
    '''))
with open(os.path.join(PKG, "main.py"), "w", encoding="utf-8") as f:
    f.write(textwrap.dedent('''
        # 相对导入：在包内部用 . 指当前包
        from . import data as rel_data
        from .data import load_data as rel_load
        RESULT = (rel_data.VALUE, rel_load())
    '''))

# --- 形式 1: import 模块名 -> import demopkg ---
sys.path.insert(0, TMP)
try:
    import demopkg
    check("形式1 import demopkg 后可用 demopkg.PACKAGE_MARKER",
          "i am demopkg", demopkg.PACKAGE_MARKER)
except Exception as e:
    check("形式1 import demopkg", "no error", f"{type(e).__name__}: {e}")

# --- 形式 2: from 模块 import 函数 ---
try:
    from demopkg.data import load_data
    check("形式2 from demopkg.data import load_data",
          ((1, 2), (3, 4)), load_data())
except Exception as e:
    check("形式2", "no error", f"{type(e).__name__}: {e}")

# --- 形式 3: from 模块 import 函数 as 别名 ---
try:
    from demopkg.data import load_data as ld
    check("形式3 from demopkg.data import load_data as ld",
          ((1, 2), (3, 4)), ld())
    check("形式3 别名 ld 与原名等价", True, ld is load_data)
except Exception as e:
    check("形式3", "no error", f"{type(e).__name__}: {e}")

# --- 形式 4: from 模块 import a, b ---
try:
    from demopkg.data import VALUE, OTHER
    check("形式4 from demopkg.data import VALUE, OTHER",
          (41, 42), (VALUE, OTHER))
except Exception as e:
    check("形式4", "no error", f"{type(e).__name__}: {e}")

# 教程示例写的是 `from mnist.data import a, b`——mnist.data 里并没有 a/b。
# 注意：必须能从 examples/ 目录 import 到 mnist 才算测到点子上，
# 所以这里用子进程并设置 cwd，而不是靠 sys.path 猜。
import subprocess

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
examples_dir = os.path.join(repo_root, "examples")

proc = subprocess.run(
    [sys.executable, "-c", "from mnist.data import a, b"],
    cwd=examples_dir, capture_output=True, text=True
)
last = (proc.stderr.strip().splitlines() or [""])[-1]
check("形式4 反例：教程字面示例 from mnist.data import a, b 应报错",
      "raises", "raises" if proc.returncode != 0 else "NO ERROR")
print(f"       异常明细: {last}")

# 顺带确认 mnist.data 到底导出了什么
proc2 = subprocess.run(
    [sys.executable, "-c",
     "import mnist.data as d; print(sorted(n for n in dir(d) if not n.startswith('_')))"],
    cwd=examples_dir, capture_output=True, text=True
)
print(f"       mnist.data 实际导出: {proc2.stdout.strip()}")

# --- 形式 5: 相对导入 from . import sibling ---
# 相对导入不能在顶层脚本用，必须在包内模块里用
try:
    import demopkg.main
    check("形式5 包内 from . import data / from .data import ... ",
          (41, ((1, 2), (3, 4))), demopkg.main.RESULT)
except Exception as e:
    check("形式5", "no error", f"{type(e).__name__}: {e}")

# 相对导入的反面：在包外（普通脚本）写 from . import x 会报错。
# 用真实文件测，不用 exec——exec 配空 globals 会报 KeyError: '__name__'，
# 那个消息是测试方法的产物，不是 Python 的真实行为。
relout = os.path.join(TMP, "relout.py")
with open(relout, "w", encoding="utf-8") as f:
    f.write("from . import data\n")
proc3 = subprocess.run([sys.executable, relout],
                       capture_output=True, text=True)
last3 = (proc3.stderr.strip().splitlines() or [""])[-1]
check("形式5 反例：包外写 from . import data 应报错",
      "raises", "raises" if proc3.returncode != 0 else "NO ERROR")
print(f"       异常明细: {last3}")

print()
print("=" * 72)
print("B. begin.md 「对比 Python 内置数据类型」4 种容器")
print("=" * 72)

# --- 元组（不可变）---
t = (1, 2)
try:
    t[0] = 99
    check("B1 元组 (a, b) 声称不可变", "raises", "NO ERROR")
except Exception as e:
    check("B1 元组 (a, b) 声称不可变", "raises", "raises")
    print(f"       异常明细: {type(e).__name__}: {e}")

# --- 列表（可变）---
l = [1, 2]
l[0] = 99
l.append(3)
check("B2 列表 [a, b] 声称可变（改元素 + append）", [99, 2, 3], l)

# --- 集合：无序、去重 ---
s = {1, 2, 2, 3, 3, 3}
check("B3a 集合 {a, b} 声称去重", 3, len(s))
check("B3b 集合元素为 1,2,3", {1, 2, 3}, s)
# 无序：没有下标访问
try:
    s[0]
    check("B3c 集合声称无序（无下标访问）", "raises", "NO ERROR")
except Exception as e:
    check("B3c 集合声称无序（无下标访问）", "raises", "raises")
    print(f"       异常明细: {type(e).__name__}: {e}")

# --- 字典：键值对 ---
d = {'x': 1}
check("B4a 字典 {'x': a} 按键取值", 1, d['x'])
d['y'] = 2
check("B4b 字典可增键", {'x': 1, 'y': 2}, d)

# --- 教程表格没提但容易混淆的一点：{} 是字典，不是集合 ---
check("B5 空 {} 的类型是 dict 不是 set", "dict", type({}).__name__)
check("B6 非空 {1, 2} 的类型是 set", "set", type({1, 2}).__name__)

print()
print("=" * 72)
print("C. unpack.md 「八、拆包在 Python 中的应用场景」5 行")
print("=" * 72)

# C1 函数返回多个值 —— 第一轮已验证，这里复述
x, y = divmod(10, 3)
check("C1 x, y = divmod(10, 3)", (3, 1), (x, y))

# C2 循环解包
d = {'a': 1, 'b': 2}
pairs = []
for k, v in d.items():
    pairs.append((k, v))
check("C2 for k, v in dict.items()", [('a', 1), ('b', 2)], pairs)

# C3 交换变量 —— 第一轮已验证
a, b = 1, 2
a, b = b, a
check("C3 a, b = b, a", (2, 1), (a, b))

# C4 解析配置
args = ["localhost", "8080", "extra1", "extra2"]
host, port, *rest = args
check("C4 host, port, *rest = args",
      ("localhost", "8080", ["extra1", "extra2"]), (host, port, rest))

# C5 数据处理
def split_data(data):
    return (data[:2], data[2:4]), data[4:]
data = [1, 2, 3, 4, 5, 6]
(train, val), test = split_data(data)
check("C5 (train, val), test = split_data(data)",
      (([1, 2], [3, 4]), [5, 6]), ((train, val), test))

print()
print("=" * 72)
passed = sum(1 for r in results if r[0])
failed = [r for r in results if not r[0]]
print(f"总计 {len(results)} 条断言: {passed} PASS / {len(failed)} FAIL")
if failed:
    print()
    print(">>> FAIL 明细:")
    for _, label, claim, got in failed:
        print(f"    - {label}")
        print(f"        声称 {claim!r} / 实际 {got!r}")
    # 门禁必须能失败：原来只打印 FAIL 却始终 exit 0，run-all.sh 的 rc 判断是死代码。
    sys.exit(1)
