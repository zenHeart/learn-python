#!/usr/bin/env bash
# 学习走查证据复现脚本
#
# 用法：bash .walkthrough/run-all.sh
#
# 重新生成本目录 evidence/ 下全部证据文件。任何结论都应能用本脚本复现，
# 不能复现的结论不写进学习笔记。
#
# 依赖：python（3.11 实测）、node/npm（构建门禁）
# 浏览器/Pyodide 部分需要 Playwright MCP 驱动，见 evidence/browser-podide-runs.md
# 头部记录的环境与操作步骤；脚本只覆盖命令行可复现的部分。

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EV="$ROOT/.walkthrough/evidence"
mkdir -p "$EV"

PY="${PYTHON:-python}"
command -v "$PY" >/dev/null 2>&1 || { echo "找不到 python，设置 PYTHON=... 重试" >&2; exit 1; }

echo "== python: $($PY --version 2>&1) =="
echo "== cwd:    $ROOT =="

# ---------------------------------------------------------------- examples
# 逐个运行 examples/ 下所有 .py，记录命令与原始输出。
# stdin 重定向自 /dev/null：examples/ 里有 6 个文件调用 input()，
# 不关掉 stdin 脚本会卡在等待输入上。关掉后它们以 EOFError 结束，
# 这是"需要交互输入"的固有属性，在证据里如实记录。
{
  echo "########## RUN MANIFEST ##########"
  echo "date: $(date -Iseconds)"
  echo "python: $($PY --version 2>&1)"
  echo "cwd: $ROOT"
  echo "note: stdin 来自 /dev/null，调用 input() 的示例会以 EOFError 结束"
  echo
  for f in $(find examples -name '*.py' | sort); do
    echo "================================================================"
    echo "### FILE: $f"
    echo "### CMD: python \"$f\" < /dev/null"
    out=$($PY "$f" </dev/null 2>&1); rc=$?
    echo "--- stdout/stderr (exit=$rc) ---"
    echo "$out"
  done
} > "$EV/examples-run.md"
echo "-> examples-run.md"

# ------------------------------------------------------- L1 概念验证脚本
{
  echo "########## L1 概念验证运行记录 ##########"
  echo "python: $($PY --version 2>&1)"
  echo "cwd: $ROOT"
  echo
  for f in "$EV"/L1-c1-print.py "$EV"/L1-c2-variable.py; do
    echo "================================================================"
    echo "### CMD: $PY ${f#$ROOT/}"
    echo "--- output ---"
    $PY "$f" 2>&1
    echo "--- exit=$? ---"
  done
} > "$EV/L1-concepts.md"
echo "-> L1-concepts.md"

# --------------------------------------------- unpack.md 断言回归门禁
# 把教程里的结论写成可执行断言。教程改错 -> 这里立刻 FAIL。
$PY "$EV/unpack-claims-audit.py" > "$EV/unpack-claims-audit.md" 2>&1
rc=$?
echo "-> unpack-claims-audit.md (exit=$rc)"
if [ "$rc" -ne 0 ]; then
  echo "!! unpack 断言门禁失败，查看 $EV/unpack-claims-audit.md" >&2
  exit "$rc"
fi

# ------------------------- begin.md 导入语法 / 数据类型 / unpack 应用场景
# 第二轮走查补齐：这三张表第一轮漏掉了。
$PY "$EV/concepts-round2-audit.py" > "$EV/concepts-round2-audit.md" 2>&1
rc=$?
echo "-> concepts-round2-audit.md (exit=$rc)"
if [ "$rc" -ne 0 ]; then
  echo "!! 第二轮概念断言门禁失败，查看 $EV/concepts-round2-audit.md" >&2
  exit "$rc"
fi

# ------------------------------------- examples/ 全部 66 个示例的注释结论
# 第三轮走查：examples/ 与课程零关联，前两轮只证明了「能跑」，
# 没证明注释里写的结果是对的。这里把每条结论写成断言。
$PY "$EV/examples-claims-audit.py" > "$EV/examples-claims-audit.md" 2>&1
rc=$?
echo "-> examples-claims-audit.md (exit=$rc)"
if [ "$rc" -ne 0 ]; then
  echo "!! examples 断言门禁失败，查看 $EV/examples-claims-audit.md" >&2
  exit "$rc"
fi

echo
echo "全部命令行证据已重新生成。浏览器/Pyodide 证据需按 "
echo "evidence/browser-podide-runs.md 的步骤用 Playwright 复跑。"
