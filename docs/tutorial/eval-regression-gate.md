# 评测脚本：评测集、命中率与回归门禁

> 面向有 JS/TS 经验、要为检索或问答链路写评测脚本的工程师。示例只用标准库，在 Python 3.11 / 3.12 实测可运行。示例 1–4 与练习依赖本机文件读写与命令行参数，因此用 `text` 围栏展示，请保存为同名文件后运行。

---

## 一、一句话结论

用标准库就能搭起评测流水线：**用 `json` + `dataclass` 定义并加载评测集 → 用可替换的打分函数做 top-k 检索 → 用 `statistics.fmean` 汇总命中率、recall@k、MRR → 与基线比对，不达标就 `sys.exit(1)` 让 CI 判红。**

- 评测集定义「什么算对」；
- 命中率衡量「对的有没有被捞进 top-k」；
- 回归门禁用退出码把「指标下滑」变成一次「失败的构建」。

---

## 二、与 JS/TS 的对照

| 关注点 | JS/TS | Python 标准库 | 注意点 |
|--------|-------|---------------|--------|
| 数据序列化 | `JSON.parse` / `JSON.stringify` | `json.loads` / `json.dumps`；文件对象用 `json.load` / `json.dump` | 坏 JSON 抛 `json.JSONDecodeError` |
| 记录 / 结构体 | `interface` + `class`（类型运行时擦除） | `@dataclass`，字段用类型注解声明 | 自动生成 `__init__`、`__repr__` |
| 可变默认字段 | 类字段默认 `[]` 易共享 | `field(default_factory=list)` | 直接写 `= []` 会被 dataclass 拒绝 |
| 求平均 | `reduce` 后除以长度 | `statistics.fmean(vals)` | 总是返回 float；空数据抛 `StatisticsError` |
| 命令行参数 | `process.argv` / `commander` | `argparse`（`type=`、`default=`，自动生成 help） | 参数由 `argparse` 从 `sys.argv` 解析 |
| 文件路径 | `path.join` + `fs.readFileSync` | `pathlib.Path` + `read_text()` | 跨平台路径语义 |
| 进程退出码 | `process.exit(1)` | `sys.exit(1)` | `0` 表示成功，非零表示异常退出 |

对应官方文档：[dataclasses](https://docs.python.org/3.12/library/dataclasses.html)、[statistics](https://docs.python.org/3.12/library/statistics.html)、[json](https://docs.python.org/3.12/library/json.html)、[argparse](https://docs.python.org/3.12/library/argparse.html)、[pathlib](https://docs.python.org/3.12/library/pathlib.html)、[sys.exit](https://docs.python.org/3.12/library/sys.html#sys.exit)、[PEP 563](https://peps.python.org/pep-0563/)。

---

## 三、四个示例

四个示例各自独立，可直接 `python 文件名.py` 运行：先有数据，再有检索，再算指标，最后上门禁。

### 示例 1：用 dataclass + json 定义并加载评测集（`ex1.py`）

评测集就是「问题 → 被认为相关的文档 id」的清单。

```text
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Example:
    query: str                       # 用户问题
    relevant: list = field(default_factory=list)  # 相关文档 id 列表

def load_examples(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Example(r["query"], list(r["relevant"])) for r in rows]

# 先写一份评测集文件
Path("eval.json").write_text(json.dumps([
    {"query": "字节 前端 React hooks", "relevant": ["d1"]},
    {"query": "MySQL 索引 事务", "relevant": ["d4"]},
], ensure_ascii=False), encoding="utf-8")

examples = load_examples("eval.json")
print(examples)                       # dataclass 自带 __repr__
print(examples[0].query, examples[0].relevant)

# 非法 JSON 会被明确抛出，便于在 CI 里给出可读报错
try:
    json.loads("{ 坏 JSON")
except json.JSONDecodeError as exc:
    print("解析失败：", exc.msg)
```

输出：

```text
[Example(query='字节 前端 React hooks', relevant=['d1']), Example(query='MySQL 索引 事务', relevant=['d4'])]
字节 前端 React hooks ['d1']
解析失败： Expecting property name enclosed in double quotes
```

要点：`relevant` 这类可变默认值必须走 `field(default_factory=list)`；`from __future__ import annotations` 让注解延迟求值（PEP 563），写法在 3.8 以后一致。

### 示例 2：纯标准库 TF-IDF 检索器（`ex2.py`）

把「语料 → 排序 → 取前 k 个 id」封装成一个类。生产环境可把 `rank()` 换成向量检索，指标与门禁代码不变。

```text
from __future__ import annotations
import re, math
from collections import Counter

_ASCII = re.compile(r"[a-z0-9]+")
_CJK = re.compile(r"[一-鿿]+")

def tokenize(text):
    text = text.lower()
    out = list(_ASCII.findall(text))
    for run in _CJK.findall(text):                       # 中文按二元切分
        out.extend([run] if len(run) == 1 else [run[i:i+2] for i in range(len(run)-1)])
    return out

class TfidfRetriever:
    def __init__(self, docs):
        self.ids = list(docs)
        self.tf = [Counter(tokenize(docs[i])) for i in self.ids]
        self.df = Counter(t for vec in self.tf for t in vec)
        self.n = len(self.ids)
    def _idf(self, term):
        return math.log((1 + self.n) / (1 + self.df[term])) + 1.0
    def _vec(self, counts):
        v = {t: (1 + math.log(c)) * self._idf(t) for t, c in counts.items()}
        norm = math.sqrt(sum(x*x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}
    def rank(self, query, k):
        qv = self._vec(Counter(tokenize(query)))
        scored = sorted(
            ((sum(qv[t] * self._vec(c).get(t, 0.0) for t in qv), i)
             for i, c in zip(self.ids, self.tf)),
            key=lambda x: (-x[0], x[1]))
        return [i for _, i in scored[:k]]

corpus = {
    "d1": "字节跳动 前端 二面 问了 React hooks 原理和虚拟 DOM diff",
    "d2": "腾讯 后端 一面 Golang 协程调度和垃圾回收",
    "d3": "阿里巴巴 前端 一面 CSS 盒模型 和 事件循环",
    "d4": "美团 后端 二面 MySQL 索引和事务隔离级别",
    "d5": "字节跳动 前端 三面 系统设计 短链服务",
}
r = TfidfRetriever(corpus)
print(r.rank("字节 前端 React hooks", 3))   # ['d1', 'd5', 'd3']
print(r.rank("MySQL 索引 事务", 3))          # ['d4', 'd1', 'd2']
```

输出：

```text
['d1', 'd5', 'd3']
['d4', 'd1', 'd2']
```

### 示例 3：命中率、recall@k、MRR（`ex3.py`）

用固定排序的假检索器，把注意力集中在指标计算上。

```text
from statistics import fmean

def reciprocal_rank(ranked, relevant):
    rel = set(relevant)
    for pos, doc_id in enumerate(ranked, start=1):
        if doc_id in rel:
            return 1.0 / pos
    return 0.0

# 演示用的假排序（真实排序见示例 2 / 小项目）
def fake_rank(query, k):
    return ["d3", "d4", "d1", "d2", "d5"][:k]

examples = [
    ("字节 前端 React hooks", ["d1"]),  # 相关文档排在第 3 位
    ("MySQL 索引 事务", ["d4"]),         # 相关文档排在第 2 位
    ("短链 系统设计", ["d9"]),           # top-k 内没有相关文档
]
hits, recalls, rrs = [], [], []
for query, relevant in examples:
    ranked = fake_rank(query, 3)
    rel = set(relevant)
    hits.append(1.0 if rel & set(ranked) else 0.0)      # 命中率单条值：在不在 top-k
    recalls.append(len(rel & set(ranked)) / len(rel))   # recall@k 单条值
    rrs.append(reciprocal_rank(ranked, relevant))       # MRR 单条值：排得多前

print("hit_rate", round(fmean(hits), 3))     # 0.667：3 条里 2 条命中
print("recall@3", round(fmean(recalls), 3))  # 0.667
print("mrr", round(fmean(rrs), 3))           # (1/3 + 1/2 + 0)/3 = 0.278：体现排序质量
```

输出：

```text
hit_rate 0.667
recall@3 0.667
mrr 0.278
```

指标定义（信息检索的通用定义）：

- **命中率 Hit Rate@K**：top-k 中是否出现任一相关文档（二值），按查询聚合为「至少命中一次的问题占比」。
- **Recall@K** = top-K 中的相关文档数 / 相关文档总数，越低说明漏检越多。
- **Precision@K** = top-K 中的相关文档数 / K，用来观察噪声；与 Recall 此消彼长，调整 `k` 就是在两者间取舍。
- **MRR** = 各查询「首个相关文档排名的倒数」的平均值：第 1 位 1.0、第 2 位 0.5、第 3 位 0.33……

本例三条查询各只有一个相关文档，所以 `hit_rate == recall@3 == 0.667`，而 `mrr = 0.278`：命中率只问「在不在」，MRR 还问「排多前」。

> 参考（非官方）：[RAG Quality Metrics Reference](https://github.com/letuhao/lore-weave/blob/main/docs/05_qa/rag_quality_metrics.md) 对上述指标的整理；正式引用请以信息检索教材或所用评测框架的文档为准。

### 示例 4：回归门禁（`ex4.py`）

门禁 =「当前指标 vs 基线」+ 退出码。

```text
import argparse, sys

def gate(current, baseline, min_hit, tol):
    ok = True
    if current["hit_rate"] < min_hit:
        print(f"[FAIL] hit_rate {current['hit_rate']:.3f} < 下限 {min_hit}")
        ok = False
    if current["hit_rate"] < baseline["hit_rate"] - tol:
        print(f"[FAIL] hit_rate 低于基线 {baseline['hit_rate']:.3f} - 容差 {tol}")
        ok = False
    if ok:
        print("[OK] 无回归")
    return ok

def main(argv=None):
    p = argparse.ArgumentParser(description="回归门禁演示")
    p.add_argument("--min-hit", type=float, default=0.8, help="命中率下限")
    p.add_argument("--tol", type=float, default=0.05, help="相对基线允许的跌幅")
    args = p.parse_args(argv)

    baseline = {"hit_rate": 0.95}   # 上一次验收的指标
    current = {"hit_rate": 0.90}    # 本次评测算出（演示用固定值）
    return 0 if gate(current, baseline, args.min_hit, args.tol) else 1

if __name__ == "__main__":
    sys.exit(main())
```

运行：

```text
$ python ex4.py                 # 默认下限 0.8：通过
[OK] 无回归                     # 退出码 0

$ python ex4.py --min-hit 0.95  # 下限抬到 0.95：不达标
[FAIL] hit_rate 0.900 < 下限 0.95
                                # 退出码 1
```

`sys.exit(arg)` 通过抛出 `SystemExit` 退出；整数参数 `0` 表示成功，非零表示异常终止。CI 读取进程退出码：`0` 放行，非零判红。

---

## 四、练习：面经检索评测 CLI

### 任务

1. 新建 `retrieval_eval.py`，用 `argparse` 支持 `--corpus`、`--eval`、`--baseline`、`--k`（默认 3）、`--min-hit`（默认 0.8）、`--tol`（默认 0.05）、`--update-baseline`（开关）。
2. `corpus.json` 为 `{"d1": "面经正文", ...}`；评测集为 `[{"query": "...", "relevant": ["d1"]}, ...]`。
3. 复用示例 2 的 `TfidfRetriever` 与示例 3 的指标函数；`--update-baseline` 时用 `json.dumps` 把当前指标写成基线文件，否则读取基线并调用 `gate()`。
4. 通过时打印指标并 `return 0`；任一门禁不满足打印 `[FAIL] ...` 并 `return 1`；`main()` 的返回值交给 `sys.exit()`。
5. 自测三种退出码：更新基线 → 0；指标不变再跑 → 0；往评测集加一条检索不到的 query → 命中率下滑 → 1。

### 数据文件

`corpus.json`：

```json
{
  "d1": "字节跳动 前端 二面 问了 React hooks 原理和虚拟 DOM diff",
  "d2": "腾讯 后端 一面 Golang 协程调度和垃圾回收",
  "d3": "阿里巴巴 前端 一面 CSS 盒模型 和 事件循环",
  "d4": "美团 后端 二面 MySQL 索引和事务隔离级别",
  "d5": "字节跳动 前端 三面 系统设计 短链服务"
}
```

`evalset.json`（评测集）：

```json
[
  {"query": "字节 前端 React hooks", "relevant": ["d1"]},
  {"query": "MySQL 索引 事务", "relevant": ["d4"]},
  {"query": "CSS 盒模型", "relevant": ["d3"]},
  {"query": "Golang 协程", "relevant": ["d2"]}
]
```

### 参考答案（`retrieval_eval.py`）

```text
from __future__ import annotations
import re, math, json, sys, argparse
from collections import Counter
from dataclasses import dataclass, field, asdict
from statistics import fmean
from pathlib import Path

_ASCII = re.compile(r"[a-z0-9]+")
_CJK = re.compile(r"[一-鿿]+")

def tokenize(text):
    text = text.lower()
    out = list(_ASCII.findall(text))
    for run in _CJK.findall(text):
        out.extend([run] if len(run) == 1 else [run[i:i + 2] for i in range(len(run) - 1)])
    return out

@dataclass
class Example:
    query: str
    relevant: list = field(default_factory=list)

@dataclass
class Metrics:
    hit_rate: float
    recall_at_k: float
    mrr: float
    k: int
    per_query: list = field(default_factory=list)

class TfidfRetriever:
    """纯标准库 TF-IDF 检索器；生产环境可把 rank() 换成向量/嵌入模型（可选依赖）。"""
    def __init__(self, docs):
        self.ids = list(docs)
        self.tf = [Counter(tokenize(docs[i])) for i in self.ids]
        self.df = Counter(t for vec in self.tf for t in vec)
        self.n = len(self.ids)
    def _idf(self, t):
        return math.log((1 + self.n) / (1 + self.df[t])) + 1.0
    def _vec(self, counts):
        v = {t: (1 + math.log(c)) * self._idf(t) for t, c in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}
    def rank(self, query, k):
        qv = self._vec(Counter(tokenize(query)))
        scored = sorted(
            ((sum(qv[t] * self._vec(c).get(t, 0.0) for t in qv), i)
             for i, c in zip(self.ids, self.tf)),
            key=lambda x: (-x[0], x[1]))
        return [i for _, i in scored[:k]]

def reciprocal_rank(ranked, relevant):
    rel = set(relevant)
    for pos, doc_id in enumerate(ranked, start=1):
        if doc_id in rel:
            return 1.0 / pos
    return 0.0

def evaluate(retriever, examples, k):
    hits, recalls, rrs, per = [], [], [], []
    for ex in examples:
        ranked = retriever.rank(ex.query, k)
        rel = set(ex.relevant)
        hit = 1.0 if rel & set(ranked) else 0.0
        rec = len(rel & set(ranked)) / len(rel) if rel else 0.0
        rr = reciprocal_rank(ranked, ex.relevant)
        hits.append(hit); recalls.append(rec); rrs.append(rr)
        per.append({"query": ex.query, "hit": hit, "recall": rec, "rr": rr})
    return Metrics(fmean(hits), fmean(recalls), fmean(rrs), k, per)

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def gate(current, baseline, min_hit, tol):
    ok = True
    if current.hit_rate < min_hit:
        print(f"[FAIL] hit_rate {current.hit_rate:.3f} < 下限 {min_hit}")
        ok = False
    if current.hit_rate < baseline["hit_rate"] - tol:
        print(f"[FAIL] hit_rate 低于基线 {baseline['hit_rate']:.3f} - 容差 {tol}")
        ok = False
    if ok:
        print("[OK] 无回归")
    return ok

def main(argv=None):
    p = argparse.ArgumentParser(description="面经检索评测 + 回归门禁")
    p.add_argument("--corpus", required=True)
    p.add_argument("--eval", required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--min-hit", type=float, default=0.8)
    p.add_argument("--tol", type=float, default=0.05)
    p.add_argument("--update-baseline", action="store_true")
    args = p.parse_args(argv)

    docs = load_json(args.corpus)
    examples = [Example(r["query"], list(r["relevant"])) for r in load_json(args.eval)]
    m = evaluate(TfidfRetriever(docs), examples, args.k)
    print(f"hit_rate={m.hit_rate:.3f}  recall@{m.k}={m.recall_at_k:.3f}  mrr={m.mrr:.3f}")
    for row in m.per_query:
        print(f"  {row['hit']:.0f}/{row['recall']:.2f}/{row['rr']:.2f}  {row['query']}")

    if args.update_baseline:
        Path(args.baseline).write_text(
            json.dumps(asdict(m), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] 基线已写入 {args.baseline}")
        return 0

    baseline = load_json(args.baseline)
    return 0 if gate(m, baseline, args.min_hit, args.tol) else 1

if __name__ == "__main__":
    sys.exit(main())
```

### 三种退出码的实测输出

```text
$ python retrieval_eval.py --corpus corpus.json --eval evalset.json --baseline baseline.json --update-baseline
hit_rate=1.000  recall@3=1.000  mrr=1.000
  1/1.00/1.00  字节 前端 React hooks
  1/1.00/1.00  MySQL 索引 事务
  1/1.00/1.00  CSS 盒模型
  1/1.00/1.00  Golang 协程
[OK] 基线已写入 baseline.json            # 退出码 0

$ python retrieval_eval.py --corpus corpus.json --eval evalset.json --baseline baseline.json
hit_rate=1.000  recall@3=1.000  mrr=1.000
  ...（同上）
[OK] 无回归                              # 退出码 0

# 评测集追加一条 {"query": "Python 装饰器", "relevant": ["d9"]}（语料中没有 d9）后再跑
hit_rate=0.800  recall@3=0.800  mrr=0.800
  ...（前四条均命中）
  0/0.00/0.00  Python 装饰器
[FAIL] hit_rate 低于基线 1.000 - 容差 0.05   # 退出码 1
```

最后一次的命中率为 4/5 = 0.8，`0.8 < 0.8` 不成立，因此「低于下限」分支不触发，只有「低于基线」分支报错。要同时触发两条，可把 `--min-hit` 调到 0.85。

接 CI 时，在流水线里跑这条命令即可：退出码非零就判红，拦住会让检索质量下滑的提交。

---

## 五、面试常问的三个追问

### 追问 1：命中率、recall@k、precision@k、MRR 有什么区别？检索问答为什么盯命中率？

命中率是二值指标，只看 top-k 里有没有相关文档；recall@k 看相关文档被取回的比例，衡量漏检；precision@k 看 top-k 里相关的比例，衡量噪声；MRR 看首个相关文档排得多前。在「检索 + 生成」的问答里，生成模型读的是 top-k 拼出的上下文，「需要的证据在不在上下文里」往往比「第一条对不对」更关键，所以门禁优先盯命中率与 recall@k，用 precision@k 观察噪声、用 MRR 观察排序。这是工程判断，不是文档结论。

### 追问 2：为什么用 `statistics.fmean` 而不是 `sum(...)/len(...)`？

`fmean` 把数据转为 float 并总是返回 float，空数据会抛 `StatisticsError`，让「评测集为空或加载失败」这类问题尽早暴露；`sum([]) / len([])` 则是 `ZeroDivisionError`，数据异常时还可能悄悄算出误导性的 0。它属于标准库，评测脚本在 CI 里无需额外安装依赖；超大规模评测再考虑 numpy 等。

### 追问 3：回归门禁在 CI 里怎么卡住一次提交？阈值怎么定？

不达标时 `sys.exit(1)`，CI 读到非零退出码就把构建判红。判据通常两条并行：**绝对下限**（命中率不得低于某值）与**相对基线容差**（低于「基线 − 容差」视为回退）。基线是上一次验收的指标，用 `--update-baseline` 落盘更新。阈值先取当前稳定值作基线，再逐步收紧下限、缩小容差；容差用来吸收评测集的小幅波动，避免门禁过于敏感。

---

## 六、参考资料

| 来源 | 覆盖内容 |
|------|----------|
| [Python 3.12 官方文档](https://docs.python.org/3.12/)：dataclasses、statistics、json、argparse、pathlib、sys | 标准库行为与退出码约定 |
| [PEP 563](https://peps.python.org/pep-0563/) | `from __future__ import annotations` |
| [RAG Quality Metrics Reference](https://github.com/letuhao/lore-weave/blob/main/docs/05_qa/rag_quality_metrics.md)（非官方参考） | Hit Rate / Recall@K / Precision@K / MRR 的整理 |

**未覆盖**：本页不调用任何外部模型接口，不涉及具体厂商 API；「可把 `rank()` 换成向量检索」仅说明可替换的接缝。
