# examples/ 运行状态总账（命令行）

复现命令：`bash .walkthrough/run-all.sh`
环境：Python 3.11.9，Windows 11，仓库根目录为 cwd。

## 汇总

| 状态 | 数量 | 说明 |
|------|------|------|
| 直接运行通过 | 61 | `python <file>` 退出码 0 |
| 需要交互 stdin | 5 | 调用 `input()`，管道送值即可通过，不是缺陷 |
| 需要正确的模块调用方式 | 1 | `examples/mnist/main.py`，须用 `python -m mnist.main` |
| **合计** | **67** | `find examples -name '*.py' \| wc -l` = 67 |

## 需要交互 stdin 的 5 个（已用 `echo 7 | python <file>` 验证通过）

| 文件 | 送 7 的输出 | 退出码 |
|------|------------|--------|
| examples/statement/if.py | `enter a number: `（7 是奇数，不打印） | 0 |
| examples/statement/elif.py | `enter a number: positive` | 0 |
| examples/statement/else.py | `enter a number: a is odd number` | 0 |
| examples/function/def.py | `enter a number:0 1 1 2 3 5 ` | 0 |
| examples/_draft/31-if.py | `please enter a number: x is odd number` | 0 |

> 自动化门禁里它们以 `EOFError: EOF when reading a line` 结束，因为
> `run-all.sh` 把 stdin 接到了 /dev/null。这是交互式示例的固有属性。

## mnist：调用方式问题，不是代码问题

错误：

```
$ python examples/mnist/main.py
ModuleNotFoundError: No module named 'mnist'
```

原因：直接按路径运行脚本时，Python 只把**脚本所在目录**（`examples/mnist/`）
加入 `sys.path`，不会把 `examples/` 加进去，所以 `mnist` 包找不到。

正确方式（已写入 `docs/tutorial/begin.md`）：

```
$ cd examples && python -m mnist.main
训练集图片: [1, 2, 3]
训练集标签: [0, 1, 2]
测试集图片: [4, 5]
测试集标签: [1, 0]

--- 结构验证 ---
train_images 类型: list
train_labels 类型: list
训练集数量: 3
测试集数量: 2
```

## 本次修掉的真实缺陷

`examples/statement/for-else.py` 原本只有三行且不完整：

```python
try:
  a+b
except
```

`node`/`python` 均报 `SyntaxError: expected ':'`——`except` 缺异常类型和冒号，
函数体也为空。已补成完整的 for-else + try/except/else/finally 演示，
运行通过（见 examples-run.md 中该文件的记录）。

修复前 60 通过 / 7 失败；修复后 61 通过 / 6 失败（余下 6 个均为交互或
调用方式问题，不是代码缺陷）。
