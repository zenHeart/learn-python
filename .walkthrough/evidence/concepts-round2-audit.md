========================================================================
A. begin.md 「Python 模块导入语法」5 种形式
========================================================================
[PASS] 形式1 import demopkg 后可用 demopkg.PACKAGE_MARKER
       教程声称: 'i am demopkg'
       实际得到: 'i am demopkg'
[PASS] 形式2 from demopkg.data import load_data
       教程声称: ((1, 2), (3, 4))
       实际得到: ((1, 2), (3, 4))
[PASS] 形式3 from demopkg.data import load_data as ld
       教程声称: ((1, 2), (3, 4))
       实际得到: ((1, 2), (3, 4))
[PASS] 形式3 别名 ld 与原名等价
       教程声称: True
       实际得到: True
[PASS] 形式4 from demopkg.data import VALUE, OTHER
       教程声称: (41, 42)
       实际得到: (41, 42)
[PASS] 形式4 反例：教程字面示例 from mnist.data import a, b 应报错
       教程声称: 'raises'
       实际得到: 'raises'
       异常明细: ImportError: cannot import name 'a' from 'mnist.data' (C:\Users\cheng\code\github\.worktrees\learn-python-stepfun-20261020\examples\mnist\data.py)
       mnist.data 实际导出: ['load_data']
[PASS] 形式5 包内 from . import data / from .data import ... 
       教程声称: (41, ((1, 2), (3, 4)))
       实际得到: (41, ((1, 2), (3, 4)))
[PASS] 形式5 反例：包外写 from . import data 应报错
       教程声称: 'raises'
       实际得到: 'raises'
       异常明细: ImportError: attempted relative import with no known parent package

========================================================================
B. begin.md 「对比 Python 内置数据类型」4 种容器
========================================================================
[PASS] B1 元组 (a, b) 声称不可变
       教程声称: 'raises'
       实际得到: 'raises'
       异常明细: TypeError: 'tuple' object does not support item assignment
[PASS] B2 列表 [a, b] 声称可变（改元素 + append）
       教程声称: [99, 2, 3]
       实际得到: [99, 2, 3]
[PASS] B3a 集合 {a, b} 声称去重
       教程声称: 3
       实际得到: 3
[PASS] B3b 集合元素为 1,2,3
       教程声称: {1, 2, 3}
       实际得到: {1, 2, 3}
[PASS] B3c 集合声称无序（无下标访问）
       教程声称: 'raises'
       实际得到: 'raises'
       异常明细: TypeError: 'set' object is not subscriptable
[PASS] B4a 字典 {'x': a} 按键取值
       教程声称: 1
       实际得到: 1
[PASS] B4b 字典可增键
       教程声称: {'x': 1, 'y': 2}
       实际得到: {'x': 1, 'y': 2}
[PASS] B5 空 {} 的类型是 dict 不是 set
       教程声称: 'dict'
       实际得到: 'dict'
[PASS] B6 非空 {1, 2} 的类型是 set
       教程声称: 'set'
       实际得到: 'set'

========================================================================
C. unpack.md 「八、拆包在 Python 中的应用场景」5 行
========================================================================
[PASS] C1 x, y = divmod(10, 3)
       教程声称: (3, 1)
       实际得到: (3, 1)
[PASS] C2 for k, v in dict.items()
       教程声称: [('a', 1), ('b', 2)]
       实际得到: [('a', 1), ('b', 2)]
[PASS] C3 a, b = b, a
       教程声称: (2, 1)
       实际得到: (2, 1)
[PASS] C4 host, port, *rest = args
       教程声称: ('localhost', '8080', ['extra1', 'extra2'])
       实际得到: ('localhost', '8080', ['extra1', 'extra2'])
[PASS] C5 (train, val), test = split_data(data)
       教程声称: (([1, 2], [3, 4]), [5, 6])
       实际得到: (([1, 2], [3, 4]), [5, 6])

========================================================================
总计 22 条断言: 22 PASS / 0 FAIL
