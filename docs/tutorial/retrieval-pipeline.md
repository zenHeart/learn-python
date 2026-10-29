# 检索链路：切块、向量化、召回、重排

> 面向有 JS/TS 经验、第一次用 Python 搭 RAG 检索链路的工程师。示例只用标准库，按顺序拼成同一个 `mini_rag.py` 即可在 Python 3.11 / 3.12 运行（`math.sumprod` 为 3.12 新增，代码里带回退）。各段依赖前面定义的名称，因此用 `text` 围栏展示，请整体复制运行。

---

## 一、一句话结论

检索链路是 **切块 → 向量化 → 召回 → 重排**：标准库足够搭出四段都能运行的骨架，上线时只需把 `embed()` 与 `rerank()` 换成厂商模型或服务。

- 切块的原因：embedding 的输入上限按 token 计，而不是按字符串长度计。
- 稠密召回：用余弦相似度取 top-N。
- 混合召回：BM25 与稠密召回的分数量纲不同，用 RRF（Reciprocal Rank Fusion，只看排名）融合。
- 重排：cross-encoder 把 `(query, doc)` 成对打分，更准但更贵，只对召回后的短列表使用。

```text
长文 ──切块──▶ chunks ──向量化──▶ vectors ──召回──▶ top-K 候选 ──重排──▶ top-k ──▶ 交给 LLM
```

---

## 二、与 JS/TS 的对照

| 环节 | Python | JS/TS 里的等价写法 | 注意点 |
|------|--------|--------------------|--------|
| 匹配 / 粗分词 | `re.findall(r"...", s)` | `s.match(/.../g)` | 返回全部不重叠匹配 |
| 词频统计 | `Counter(tokens)` | `Map` + `reduce` | `Counter` 是 `dict` 子类，缺失键返回 `0` 而不抛 `KeyError` |
| 按宽折行 | `textwrap.wrap(s, width=40)` | 手写 `slice` / 正则 | 每行至多 `width` 个字符 |
| 点积 | `math.sumprod(a, b)`（3.12）或 `sum(x*y ...)` | `reduce` / 手写循环 | 3.12 新增 |
| 范数 / 对数 | `math.sqrt` / `math.log` | `Math.hypot` / `Math.log` | `math.log(x)` 单参数为自然对数 |
| 哈希 | `hashlib.sha256(data).hexdigest()` | `crypto.subtle.digest` | `digest()` 返回字节，`hexdigest()` 返回十六进制字符串 |
| 排序 | `sorted(xs, key=...)` | `[...xs].sort(...)` | `sorted` 返回新列表；Python 排序稳定，同键保持原相对顺序 |
| 生成 embedding | `client.embeddings.create(input=..., model=...).data[0].embedding` | `await client.embeddings.create({...})` | `text-embedding-3-small` 上限 8191 tokens，示例输出 1536 维 |
| 混合融合 | RRF：`sum(1 / (k + rank))` | 手写 rank 融合 | Elasticsearch 的 `rank_constant` 默认 `60` |

---

## 三、四个示例

### 示例 0：语料与分词

```text
from __future__ import annotations

import hashlib
import math
import re
import textwrap
from collections import Counter
from dataclasses import dataclass

TOKEN_RE = re.compile(r"[a-z0-9_]+|[\u4e00-\u9fff]")


@dataclass(frozen=True)
class Doc:
    doc_id: str
    text: str


def tokenize(text: str) -> list[str]:
    """英文/数字按词切；连续中文按字切后再拼成二元组。"""
    raw = TOKEN_RE.findall(text.lower())
    tokens: list[str] = []
    run: list[str] = []

    def flush() -> None:
        if len(run) == 1:
            tokens.append(run[0])
        elif len(run) >= 2:
            tokens.extend(run[i] + run[i + 1] for i in range(len(run) - 1))
        run.clear()

    for piece in raw:
        if "一" <= piece <= "鿿":
            run.append(piece)
        else:
            flush()
            tokens.append(piece)
    flush()
    return tokens


CORPUS = [
    Doc("Q001", "什么是 Python 的 GIL？\n\nGIL 是 CPython 的全局解释器锁。同一进程内，同一时刻只有一个线程执行 Python 字节码。I/O 密集任务可以用线程，CPU 密集任务通常用多进程，或者用释放 GIL 的 C 扩展。"),
    Doc("Q002", "Python 的 list 和 tuple 有什么区别？\n\nlist 可变，支持增删改；tuple 不可变，元素都可哈希时 tuple 也可哈希，因此能作为 dict 的 key。tuple 通常更省内存。"),
    Doc("Q003", "Python 装饰器是什么？\n\n装饰器是接收函数并返回新函数的可调用对象，常用于日志、缓存和权限校验。使用 functools.wraps 可以保留原函数的名称和文档字符串。"),
    Doc("Q004", "async/await 适合什么场景？\n\nasync/await 由事件循环调度协程，await 时让出控制权，适合网络和磁盘等 I/O 密集场景。它不会自动利用多核，CPU 密集任务仍应使用多进程。"),
    Doc("Q005", "JS 的 event loop 和微任务是什么？\n\nJS 事件循环先执行同步代码，再清空微任务队列（Promise 回调），然后取一个宏任务（如 setTimeout）。每轮宏任务结束后都会再次清空微任务。"),
    Doc("Q006", "React useEffect 的清理函数什么时候执行？\n\nuseEffect 的清理函数在组件卸载时执行，也会在下一次 effect 运行前执行。依赖数组决定 effect 是否重新运行；空数组表示只在挂载和卸载时运行。"),
    Doc("Q007", "数据库索引为什么能加速查询？\n\nB+ 树索引把 key 有序组织，减少扫描行数。联合索引遵循最左前缀原则；查询列都在索引里时可以走覆盖索引，避免回表。"),
    Doc("Q008", "HTTP 缓存有哪些关键字段？\n\nCache-Control 控制新鲜度和缓存位置，ETag 配合 If-None-Match 做协商缓存，命中时服务器返回 304，浏览器继续使用本地副本。"),
    Doc("Q009", "Python 的浅拷贝和深拷贝有什么区别？\n\ncopy.copy 只复制最外层容器，内部可变对象仍然共享；copy.deepcopy 递归复制嵌套对象。嵌套列表或字典需要独立修改时要用深拷贝。"),
    Doc("Q010", "TypeScript 泛型有什么用？\n\n泛型把类型作为参数，让函数和类在保持类型安全的同时复用逻辑。可以用 extends 约束类型参数，也可以给泛型提供默认类型。"),
]
```

中文分词采用「单字 + 相邻二元组」的轻量方案，目的是让链路可运行，不替代正式的中文分词器。

### 示例 1：切块

```text
BOUNDARY = "。！？；!?;\n "


def chunk_text(text: str, size: int = 160, overlap: int = 32) -> list[str]:
    """按字符切块，优先在句末或空格断开，并保留 overlap 个字符的重叠。"""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must satisfy 0 <= overlap < size")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    chunks: list[str] = []
    for paragraph in paragraphs:
        start = 0
        while start < len(paragraph):
            end = min(start + size, len(paragraph))
            if end < len(paragraph):
                window = paragraph[start:end]
                cut = max(window.rfind(ch) for ch in BOUNDARY)
                if cut >= size // 3:
                    end = start + cut + 1
            piece = paragraph[start:end].strip()
            if piece:
                chunks.append(piece)
            if end >= len(paragraph):
                break
            next_start = max(end - overlap, start + 1)
            while next_start < end and paragraph[next_start] not in BOUNDARY:
                next_start += 1
            start = next_start
    return chunks


TEXT = CORPUS[0].text + "\n\n" + CORPUS[1].text
for i, chunk in enumerate(chunk_text(TEXT, size=48, overlap=8), 1):
    print(f"[{i}] {chunk!r}")

print("token:", tokenize("Python 的 GIL 是什么？"))
print("textwrap:", textwrap.wrap("GIL is a global interpreter lock.", width=18))
```

输出：

```text
[1] '什么是 Python 的 GIL？'
[2] 'GIL 是 CPython 的全局解释器锁。同一进程内，同一时刻只有一个线程执行 Python'
[3] 'Python 字节码。I/O 密集任务可以用线程，CPU 密集任务通常用多进程，或者用释放'
[4] 'GIL 的 C 扩展。'
[5] 'Python 的 list 和 tuple 有什么区别？'
[6] 'list 可变，支持增删改；tuple 不可变，元素都可哈希时 tuple'
[7] 'tuple 也可哈希，因此能作为 dict 的 key。tuple 通常更省内存。'
token: ['python', '的', 'gil', '是什', '什么']
textwrap: ['GIL is a global', 'interpreter lock.']
```

要点：

- `size` 是**字符数**，不是 token 数；生产环境应换成目标模型对应的 tokenizer。
- 链路顺序是「先切块，再 embedding」：OpenAI cookbook 对超长文本的做法之一就是切成 chunk 后逐块 embedding。
- `overlap` 缓解「答案刚好被切在边界上」，代价是索引变大、召回可能重复。它是需要评测的参数，不是固定数值。

### 示例 2：向量化与稠密召回

```text
DIM = 256


def embed(text: str, dim: int = DIM) -> list[float]:
    """标准库版特征哈希：相同 token 总落到同一维，再做 L2 归一化。"""
    vector = [0.0] * dim
    for token, count in Counter(tokenize(text)).items():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dim
        sign = 1.0 if digest[4] & 1 else -1.0
        vector[index] += sign * (1.0 + math.log(count))
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def dot(left: list[float], right: list[float]) -> float:
    if hasattr(math, "sumprod"):
        return math.sumprod(left, right)
    return sum(a * b for a, b in zip(left, right))


def cosine(left: list[float], right: list[float]) -> float:
    denominator = math.sqrt(dot(left, left)) * math.sqrt(dot(right, right))
    return dot(left, right) / denominator if denominator else 0.0


def dense_search(query: str, docs: list[Doc], top_k: int = 5) -> list[int]:
    query_vector = embed(query)
    scored = [(cosine(query_vector, embed(doc.text)), i) for i, doc in enumerate(docs)]
    scored.sort(key=lambda pair: (-pair[0], docs[pair[1]].doc_id))
    return [index for _, index in scored[:top_k]]


QUERY = "GIL 是什么？CPU 密集为什么用多进程？"
print("dim:", len(embed(QUERY)))
for i in dense_search(QUERY, CORPUS, top_k=3):
    print(f"{cosine(embed(QUERY), embed(CORPUS[i].text)):.4f}", CORPUS[i].doc_id)
```

输出：

```text
dim: 256
0.2762 Q004
0.2688 Q001
0.1447 Q006
```

要点：

- `embed()` 是特征哈希（hashing trick）：每个 token 经 SHA-256 映射到固定维度，再用符号位减少碰撞偏差。它不需要训练，但不是语义模型，只用来让示例跑通。
- 稠密召回就是按余弦相似度降序取 top-N，与 OpenAI 语义检索 cookbook 的做法一致。

生产替换点（可选依赖 `openai`，不属于上面的标准库示例）：

```text
# pip install openai
# 运行前设置环境变量 OPENAI_API_KEY，不要把 key 写进代码
from openai import OpenAI

client = OpenAI()


def embed_remote(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding
```

不要把本页 256 维的特征哈希向量与真实模型向量放进同一个索引。

### 示例 3：BM25 与 RRF 混合召回

```text
class BM25:
    def __init__(self, docs: list[Doc], k1: float = 1.2, b: float = 0.75) -> None:
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.tfs = [Counter(tokenize(doc.text)) for doc in docs]
        self.lengths = [sum(tf.values()) for tf in self.tfs]
        self.avgdl = sum(self.lengths) / max(1, len(self.lengths))
        self.df: Counter[str] = Counter()
        for tf in self.tfs:
            self.df.update(tf.keys())
        self.N = len(docs)

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query: str, doc_index: int) -> float:
        query_terms = set(tokenize(query))
        tf = self.tfs[doc_index]
        length = self.lengths[doc_index] or 1
        total = 0.0
        for term in query_terms:
            freq = tf.get(term, 0)
            if not freq:
                continue
            denominator = freq + self.k1 * (1 - self.b + self.b * length / self.avgdl)
            total += self.idf(term) * freq * (self.k1 + 1) / denominator
        return total

    def search(self, query: str, top_k: int = 5) -> list[int]:
        order = sorted(range(self.N), key=lambda i: (-self.score(query, i), self.docs[i].doc_id))
        return order[:top_k]


def rrf(rankings: list[list[int]], k: int = 60, top_k: int = 5) -> list[int]:
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc_index in enumerate(ranking, start=1):
            scores[doc_index] = scores.get(doc_index, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda i: (-scores[i], i))[:top_k]


bm25 = BM25(CORPUS)
sparse = bm25.search(QUERY, top_k=3)
dense = dense_search(QUERY, CORPUS, top_k=3)
print("bm25:", [CORPUS[i].doc_id for i in sparse])
print("dense:", [CORPUS[i].doc_id for i in dense])
print("rrf:", [CORPUS[i].doc_id for i in rrf([dense, sparse], k=60, top_k=3)])
```

输出：

```text
bm25: ['Q001', 'Q004', 'Q010']
dense: ['Q004', 'Q001', 'Q006']
rrf: ['Q001', 'Q004', 'Q006']
```

要点：

- IDF 采用 Lucene BM25 的公式 `log(1 + (docCount - docFreq + 0.5) / (docFreq + 0.5))`；`k1 = 1.2`、`b = 0.75` 是 Elasticsearch 文档给出的默认值。
- BM25 擅长 `GIL`、`ETag`、`304` 这类稀有标识符；稠密向量擅长意思相近但用词不同的查询，两路排名常不一致。
- RRF 只用排名，每个文档的得分是各列表 `1 / (k + rank)` 之和，因此不必把 BM25 分数与余弦分数校准到同一量纲。

### 示例 4：重排

```text
def rerank(query: str, docs: list[Doc], candidates: list[int], top_k: int = 3) -> list[tuple[float, int]]:
    """轻量交叉特征：同时看 query 与文档，模拟 cross-encoder 的成对打分。"""
    query_tokens = tokenize(query)
    query_set = set(query_tokens)
    query_bigrams = set(zip(query_tokens, query_tokens[1:]))
    scored: list[tuple[float, int]] = []
    for index in candidates:
        doc_tokens = tokenize(docs[index].text)
        doc_set = set(doc_tokens)
        doc_bigrams = set(zip(doc_tokens, doc_tokens[1:]))
        coverage = len(query_set & doc_set) / max(1, len(query_set))
        phrase = len(query_bigrams & doc_bigrams) / max(1, len(query_bigrams))
        density = sum(1 for token in doc_tokens if token in query_set) / max(1, len(doc_tokens))
        score = 0.55 * coverage + 0.30 * phrase + 0.15 * density
        scored.append((score, index))
    scored.sort(key=lambda pair: (-pair[0], docs[pair[1]].doc_id))
    return scored[:top_k]


fused = rrf([dense, sparse], k=60, top_k=6)
for score, index in rerank(QUERY, CORPUS, fused, top_k=3):
    print(f"{score:.4f}", CORPUS[index].doc_id)
```

输出：

```text
0.4580 Q001
0.4032 Q004
0.1327 Q010
```

要点：

- 这里的 `rerank()` 是教学用的交叉特征（词覆盖、bigram 短语命中、命中密度），便宜且可解释，但不是神经 cross-encoder。
- 生产中的 cross-encoder 把 `(query, document)` 拼在一起联合编码，比 query 与 document 各自编码的 bi-encoder 更准，但不能预先计算文档向量，因此只适合重排召回后的短列表。
- top-k 不是越大越好：「Lost in the Middle」的实验显示，相关信息位于上下文中间时模型表现明显下降。

---

## 四、练习：面经检索问答

### 任务

用示例中的 `CORPUS` 做一个面经检索问答：

1. 对每个问题分别用 BM25 与稠密向量召回 top-6；
2. 用 RRF 融合两路排名；
3. 对融合后的候选做 `rerank`，取 top-3；
4. 返回 top-1 作为答案，并给出 top-3 引用；
5. 用 5 条带标准答案的问题计算 `hit@1`；
6. 调整一个参数（`recall_k`、`chunk_text` 的 `size/overlap` 或 rerank 权重），观察 top-1 是否变化并解释原因。

验收标准：代码可运行；5 条问题都能打印 top-1 与 top-3；能说明为什么某题由 BM25 命中、另一题由稠密召回命中。

### 参考答案

接在示例 4 之后，保存在同一个 `mini_rag.py`：

```text
def hybrid_answer(question: str, docs: list[Doc], recall_k: int = 6, final_k: int = 3) -> tuple[Doc, list[tuple[float, int]]]:
    bm25 = BM25(docs)
    dense = dense_search(question, docs, top_k=recall_k)
    sparse = bm25.search(question, top_k=recall_k)
    fused = rrf([dense, sparse], k=60, top_k=recall_k)
    ranked = rerank(question, docs, fused, top_k=final_k)
    if not ranked:
        raise LookupError("no candidate retrieved")
    return docs[ranked[0][1]], ranked


QUESTIONS = [
    ("GIL 是什么？CPU 密集为什么用多进程？", "Q001"),
    ("tuple 为什么能作为 dict 的 key？", "Q002"),
    ("React useEffect 的清理函数什么时候执行？", "Q006"),
    ("HTTP 缓存的 ETag 和 304 是什么？", "Q008"),
    ("TypeScript 泛型的 extends 约束是什么？", "Q010"),
]

hits = 0
for question, gold in QUESTIONS:
    best, ranked = hybrid_answer(question, CORPUS)
    hit = best.doc_id == gold
    hits += int(hit)
    top3 = [CORPUS[index].doc_id for _, index in ranked]
    print(f"{question}\n  top1={best.doc_id} gold={gold} hit={hit} top3={top3}")

print(f"hit@1: {hits}/{len(QUESTIONS)}")
```

输出：

```text
GIL 是什么？CPU 密集为什么用多进程？
  top1=Q001 gold=Q001 hit=True top3=['Q001', 'Q004', 'Q010']
tuple 为什么能作为 dict 的 key？
  top1=Q002 gold=Q002 hit=True top3=['Q002', 'Q007', 'Q001']
React useEffect 的清理函数什么时候执行？
  top1=Q006 gold=Q006 hit=True top3=['Q006', 'Q003', 'Q010']
HTTP 缓存的 ETag 和 304 是什么？
  top1=Q008 gold=Q008 hit=True top3=['Q008', 'Q003', 'Q005']
TypeScript 泛型的 extends 约束是什么？
  top1=Q010 gold=Q010 hit=True top3=['Q010', 'Q003', 'Q005']
hit@1: 5/5
```

5/5 只说明这 5 条在这个小语料上通过，不代表真实效果。真实项目需要标注集、失败样本分析以及延迟与成本指标。

可继续改进：

1. 用 `chunk_text()` 把长答案切块，在块级别召回后按 `doc_id` 聚合分数；
2. 给 `tokenize()` 换成正式的中文分词器；
3. 把 `rerank()` 的权重当作超参数，在验证集上搜索；
4. 记录每次召回的 BM25 排名、稠密排名与最终排名，区分「召回没进来」与「重排排错了」。

---

## 五、面试常问的三个追问

### 追问 1：切块大小和 overlap 怎么定？

先看模型上限：`text-embedding-3-small` 的上下文为 8191 tokens，实际切块要留余量。从「固定长度 + 小重叠」的基线开始，用带标注的问题集观察 `hit@k`、MRR 与端到端答案质量。overlap 太小会切断跨块语义，太大则索引膨胀、召回重复。所引官方资料中没有可直接照搬的统一 `size/overlap` 数值，所以不给「最佳值」。

### 追问 2：BM25 与向量召回的分数尺度不同，怎么融合？

最稳妥的起点是 RRF：不碰原始分数，只用排名，得分为各列表 `1/(k+rank)` 之和，Elasticsearch 的默认 `rank_constant` 为 60。代价是丢掉「分数有多高」的信息；若业务需要权重，应在验证集上学习融合权重或做分数校准，而不是直接相加两种分数。

### 追问 3：已经有向量召回了，为什么还要重排？

bi-encoder 对 query 与 document 各自编码，交互信息被压进两个向量；cross-encoder 联合编码 `(query, document)`，通常更准，但计算量大、不能预先算好所有文档，因此只对召回后的短列表重排。另外送入生成器的候选并非越多越好，应由评测决定 top-k。

---

## 六、参考资料

| 来源 | 覆盖内容 |
|------|----------|
| Python 3.12 官方文档：[re](https://docs.python.org/3.12/library/re.html)、[collections](https://docs.python.org/3.12/library/collections.html)、[textwrap](https://docs.python.org/3.12/library/textwrap.html)、[math](https://docs.python.org/3.12/library/math.html)、[hashlib](https://docs.python.org/3.12/library/hashlib.html)、[排序指南](https://docs.python.org/3.12/howto/sorting.html) | 标准库行为与排序稳定性 |
| [OpenAI Cookbook](https://github.com/openai/openai-cookbook)（Embedding long inputs、Semantic text search using embeddings、Search reranking with cross-encoders） | token 上限、切块、SDK 调用形状、余弦召回、cross-encoder 重排 |
| [Elasticsearch：Reciprocal rank fusion](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html) | RRF 公式与默认 `rank_constant` |
| [Apache Lucene](https://github.com/apache/lucene)（`BM25Similarity`）与 Elastic 博客 *Practical BM25* | BM25 的 IDF 公式与 `k1`、`b` 默认值 |
| [Lost in the Middle（arXiv:2307.03172）](https://arxiv.org/abs/2307.03172) | 长上下文中间位置信息利用下降 |

**未覆盖**：Python 3.12 `str.split` 的官方段落未抓取成功，本页不对其边界行为下结论；统一的切块 size/overlap 最佳值与具体 rerank 服务的 API 未找到可核验的官方来源，本页只实现标准库启发式重排，不虚构接口。
