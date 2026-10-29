import{_ as n,o as a,c as e,ae as p}from"./chunks/framework.DJK_dC0-.js";const h=JSON.parse('{"title":"检索链路：切块、向量化、召回、重排","description":"","frontmatter":{},"headers":[],"relativePath":"tutorial/retrieval-pipeline.md","filePath":"tutorial/retrieval-pipeline.md"}'),t={name:"tutorial/retrieval-pipeline.md"};function l(i,s,o,c,r,d){return a(),e("div",null,[...s[0]||(s[0]=[p(`<h1 id="检索链路-切块、向量化、召回、重排" tabindex="-1">检索链路：切块、向量化、召回、重排 <a class="header-anchor" href="#检索链路-切块、向量化、召回、重排" aria-label="Permalink to &quot;检索链路：切块、向量化、召回、重排&quot;">​</a></h1><blockquote><p>面向有 JS/TS 经验、第一次用 Python 搭 RAG 检索链路的工程师。示例只用标准库，按顺序拼成同一个 <code>mini_rag.py</code> 即可在 Python 3.11 / 3.12 运行（<code>math.sumprod</code> 为 3.12 新增，代码里带回退）。各段依赖前面定义的名称，因此用 <code>text</code> 围栏展示，请整体复制运行。</p></blockquote><hr><h2 id="一、一句话结论" tabindex="-1">一、一句话结论 <a class="header-anchor" href="#一、一句话结论" aria-label="Permalink to &quot;一、一句话结论&quot;">​</a></h2><p>检索链路是 <strong>切块 → 向量化 → 召回 → 重排</strong>：标准库足够搭出四段都能运行的骨架，上线时只需把 <code>embed()</code> 与 <code>rerank()</code> 换成厂商模型或服务。</p><ul><li>切块的原因：embedding 的输入上限按 token 计，而不是按字符串长度计。</li><li>稠密召回：用余弦相似度取 top-N。</li><li>混合召回：BM25 与稠密召回的分数量纲不同，用 RRF（Reciprocal Rank Fusion，只看排名）融合。</li><li>重排：cross-encoder 把 <code>(query, doc)</code> 成对打分，更准但更贵，只对召回后的短列表使用。</li></ul><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>长文 ──切块──▶ chunks ──向量化──▶ vectors ──召回──▶ top-K 候选 ──重排──▶ top-k ──▶ 交给 LLM</span></span></code></pre></div><hr><h2 id="二、与-js-ts-的对照" tabindex="-1">二、与 JS/TS 的对照 <a class="header-anchor" href="#二、与-js-ts-的对照" aria-label="Permalink to &quot;二、与 JS/TS 的对照&quot;">​</a></h2><table tabindex="0"><thead><tr><th>环节</th><th>Python</th><th>JS/TS 里的等价写法</th><th>注意点</th></tr></thead><tbody><tr><td>匹配 / 粗分词</td><td><code>re.findall(r&quot;...&quot;, s)</code></td><td><code>s.match(/.../g)</code></td><td>返回全部不重叠匹配</td></tr><tr><td>词频统计</td><td><code>Counter(tokens)</code></td><td><code>Map</code> + <code>reduce</code></td><td><code>Counter</code> 是 <code>dict</code> 子类，缺失键返回 <code>0</code> 而不抛 <code>KeyError</code></td></tr><tr><td>按宽折行</td><td><code>textwrap.wrap(s, width=40)</code></td><td>手写 <code>slice</code> / 正则</td><td>每行至多 <code>width</code> 个字符</td></tr><tr><td>点积</td><td><code>math.sumprod(a, b)</code>（3.12）或 <code>sum(x*y ...)</code></td><td><code>reduce</code> / 手写循环</td><td>3.12 新增</td></tr><tr><td>范数 / 对数</td><td><code>math.sqrt</code> / <code>math.log</code></td><td><code>Math.hypot</code> / <code>Math.log</code></td><td><code>math.log(x)</code> 单参数为自然对数</td></tr><tr><td>哈希</td><td><code>hashlib.sha256(data).hexdigest()</code></td><td><code>crypto.subtle.digest</code></td><td><code>digest()</code> 返回字节，<code>hexdigest()</code> 返回十六进制字符串</td></tr><tr><td>排序</td><td><code>sorted(xs, key=...)</code></td><td><code>[...xs].sort(...)</code></td><td><code>sorted</code> 返回新列表；Python 排序稳定，同键保持原相对顺序</td></tr><tr><td>生成 embedding</td><td><code>client.embeddings.create(input=..., model=...).data[0].embedding</code></td><td><code>await client.embeddings.create({...})</code></td><td><code>text-embedding-3-small</code> 上限 8191 tokens，示例输出 1536 维</td></tr><tr><td>混合融合</td><td>RRF：<code>sum(1 / (k + rank))</code></td><td>手写 rank 融合</td><td>Elasticsearch 的 <code>rank_constant</code> 默认 <code>60</code></td></tr></tbody></table><hr><h2 id="三、四个示例" tabindex="-1">三、四个示例 <a class="header-anchor" href="#三、四个示例" aria-label="Permalink to &quot;三、四个示例&quot;">​</a></h2><h3 id="示例-0-语料与分词" tabindex="-1">示例 0：语料与分词 <a class="header-anchor" href="#示例-0-语料与分词" aria-label="Permalink to &quot;示例 0：语料与分词&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>from __future__ import annotations</span></span>
<span class="line"><span></span></span>
<span class="line"><span>import hashlib</span></span>
<span class="line"><span>import math</span></span>
<span class="line"><span>import re</span></span>
<span class="line"><span>import textwrap</span></span>
<span class="line"><span>from collections import Counter</span></span>
<span class="line"><span>from dataclasses import dataclass</span></span>
<span class="line"><span></span></span>
<span class="line"><span>TOKEN_RE = re.compile(r&quot;[a-z0-9_]+|[\\u4e00-\\u9fff]&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>@dataclass(frozen=True)</span></span>
<span class="line"><span>class Doc:</span></span>
<span class="line"><span>    doc_id: str</span></span>
<span class="line"><span>    text: str</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def tokenize(text: str) -&gt; list[str]:</span></span>
<span class="line"><span>    &quot;&quot;&quot;英文/数字按词切；连续中文按字切后再拼成二元组。&quot;&quot;&quot;</span></span>
<span class="line"><span>    raw = TOKEN_RE.findall(text.lower())</span></span>
<span class="line"><span>    tokens: list[str] = []</span></span>
<span class="line"><span>    run: list[str] = []</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def flush() -&gt; None:</span></span>
<span class="line"><span>        if len(run) == 1:</span></span>
<span class="line"><span>            tokens.append(run[0])</span></span>
<span class="line"><span>        elif len(run) &gt;= 2:</span></span>
<span class="line"><span>            tokens.extend(run[i] + run[i + 1] for i in range(len(run) - 1))</span></span>
<span class="line"><span>        run.clear()</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    for piece in raw:</span></span>
<span class="line"><span>        if &quot;一&quot; &lt;= piece &lt;= &quot;鿿&quot;:</span></span>
<span class="line"><span>            run.append(piece)</span></span>
<span class="line"><span>        else:</span></span>
<span class="line"><span>            flush()</span></span>
<span class="line"><span>            tokens.append(piece)</span></span>
<span class="line"><span>    flush()</span></span>
<span class="line"><span>    return tokens</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>CORPUS = [</span></span>
<span class="line"><span>    Doc(&quot;Q001&quot;, &quot;什么是 Python 的 GIL？\\n\\nGIL 是 CPython 的全局解释器锁。同一进程内，同一时刻只有一个线程执行 Python 字节码。I/O 密集任务可以用线程，CPU 密集任务通常用多进程，或者用释放 GIL 的 C 扩展。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q002&quot;, &quot;Python 的 list 和 tuple 有什么区别？\\n\\nlist 可变，支持增删改；tuple 不可变，元素都可哈希时 tuple 也可哈希，因此能作为 dict 的 key。tuple 通常更省内存。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q003&quot;, &quot;Python 装饰器是什么？\\n\\n装饰器是接收函数并返回新函数的可调用对象，常用于日志、缓存和权限校验。使用 functools.wraps 可以保留原函数的名称和文档字符串。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q004&quot;, &quot;async/await 适合什么场景？\\n\\nasync/await 由事件循环调度协程，await 时让出控制权，适合网络和磁盘等 I/O 密集场景。它不会自动利用多核，CPU 密集任务仍应使用多进程。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q005&quot;, &quot;JS 的 event loop 和微任务是什么？\\n\\nJS 事件循环先执行同步代码，再清空微任务队列（Promise 回调），然后取一个宏任务（如 setTimeout）。每轮宏任务结束后都会再次清空微任务。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q006&quot;, &quot;React useEffect 的清理函数什么时候执行？\\n\\nuseEffect 的清理函数在组件卸载时执行，也会在下一次 effect 运行前执行。依赖数组决定 effect 是否重新运行；空数组表示只在挂载和卸载时运行。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q007&quot;, &quot;数据库索引为什么能加速查询？\\n\\nB+ 树索引把 key 有序组织，减少扫描行数。联合索引遵循最左前缀原则；查询列都在索引里时可以走覆盖索引，避免回表。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q008&quot;, &quot;HTTP 缓存有哪些关键字段？\\n\\nCache-Control 控制新鲜度和缓存位置，ETag 配合 If-None-Match 做协商缓存，命中时服务器返回 304，浏览器继续使用本地副本。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q009&quot;, &quot;Python 的浅拷贝和深拷贝有什么区别？\\n\\ncopy.copy 只复制最外层容器，内部可变对象仍然共享；copy.deepcopy 递归复制嵌套对象。嵌套列表或字典需要独立修改时要用深拷贝。&quot;),</span></span>
<span class="line"><span>    Doc(&quot;Q010&quot;, &quot;TypeScript 泛型有什么用？\\n\\n泛型把类型作为参数，让函数和类在保持类型安全的同时复用逻辑。可以用 extends 约束类型参数，也可以给泛型提供默认类型。&quot;),</span></span>
<span class="line"><span>]</span></span></code></pre></div><p>中文分词采用「单字 + 相邻二元组」的轻量方案，目的是让链路可运行，不替代正式的中文分词器。</p><h3 id="示例-1-切块" tabindex="-1">示例 1：切块 <a class="header-anchor" href="#示例-1-切块" aria-label="Permalink to &quot;示例 1：切块&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>BOUNDARY = &quot;。！？；!?;\\n &quot;</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def chunk_text(text: str, size: int = 160, overlap: int = 32) -&gt; list[str]:</span></span>
<span class="line"><span>    &quot;&quot;&quot;按字符切块，优先在句末或空格断开，并保留 overlap 个字符的重叠。&quot;&quot;&quot;</span></span>
<span class="line"><span>    if size &lt;= 0:</span></span>
<span class="line"><span>        raise ValueError(&quot;size must be positive&quot;)</span></span>
<span class="line"><span>    if not 0 &lt;= overlap &lt; size:</span></span>
<span class="line"><span>        raise ValueError(&quot;overlap must satisfy 0 &lt;= overlap &lt; size&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    paragraphs = [p.strip() for p in re.split(r&quot;\\n\\s*\\n&quot;, text.strip()) if p.strip()]</span></span>
<span class="line"><span>    chunks: list[str] = []</span></span>
<span class="line"><span>    for paragraph in paragraphs:</span></span>
<span class="line"><span>        start = 0</span></span>
<span class="line"><span>        while start &lt; len(paragraph):</span></span>
<span class="line"><span>            end = min(start + size, len(paragraph))</span></span>
<span class="line"><span>            if end &lt; len(paragraph):</span></span>
<span class="line"><span>                window = paragraph[start:end]</span></span>
<span class="line"><span>                cut = max(window.rfind(ch) for ch in BOUNDARY)</span></span>
<span class="line"><span>                if cut &gt;= size // 3:</span></span>
<span class="line"><span>                    end = start + cut + 1</span></span>
<span class="line"><span>            piece = paragraph[start:end].strip()</span></span>
<span class="line"><span>            if piece:</span></span>
<span class="line"><span>                chunks.append(piece)</span></span>
<span class="line"><span>            if end &gt;= len(paragraph):</span></span>
<span class="line"><span>                break</span></span>
<span class="line"><span>            next_start = max(end - overlap, start + 1)</span></span>
<span class="line"><span>            while next_start &lt; end and paragraph[next_start] not in BOUNDARY:</span></span>
<span class="line"><span>                next_start += 1</span></span>
<span class="line"><span>            start = next_start</span></span>
<span class="line"><span>    return chunks</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>TEXT = CORPUS[0].text + &quot;\\n\\n&quot; + CORPUS[1].text</span></span>
<span class="line"><span>for i, chunk in enumerate(chunk_text(TEXT, size=48, overlap=8), 1):</span></span>
<span class="line"><span>    print(f&quot;[{i}] {chunk!r}&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>print(&quot;token:&quot;, tokenize(&quot;Python 的 GIL 是什么？&quot;))</span></span>
<span class="line"><span>print(&quot;textwrap:&quot;, textwrap.wrap(&quot;GIL is a global interpreter lock.&quot;, width=18))</span></span></code></pre></div><p>输出：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>[1] &#39;什么是 Python 的 GIL？&#39;</span></span>
<span class="line"><span>[2] &#39;GIL 是 CPython 的全局解释器锁。同一进程内，同一时刻只有一个线程执行 Python&#39;</span></span>
<span class="line"><span>[3] &#39;Python 字节码。I/O 密集任务可以用线程，CPU 密集任务通常用多进程，或者用释放&#39;</span></span>
<span class="line"><span>[4] &#39;GIL 的 C 扩展。&#39;</span></span>
<span class="line"><span>[5] &#39;Python 的 list 和 tuple 有什么区别？&#39;</span></span>
<span class="line"><span>[6] &#39;list 可变，支持增删改；tuple 不可变，元素都可哈希时 tuple&#39;</span></span>
<span class="line"><span>[7] &#39;tuple 也可哈希，因此能作为 dict 的 key。tuple 通常更省内存。&#39;</span></span>
<span class="line"><span>token: [&#39;python&#39;, &#39;的&#39;, &#39;gil&#39;, &#39;是什&#39;, &#39;什么&#39;]</span></span>
<span class="line"><span>textwrap: [&#39;GIL is a global&#39;, &#39;interpreter lock.&#39;]</span></span></code></pre></div><p>要点：</p><ul><li><code>size</code> 是<strong>字符数</strong>，不是 token 数；生产环境应换成目标模型对应的 tokenizer。</li><li>链路顺序是「先切块，再 embedding」：OpenAI cookbook 对超长文本的做法之一就是切成 chunk 后逐块 embedding。</li><li><code>overlap</code> 缓解「答案刚好被切在边界上」，代价是索引变大、召回可能重复。它是需要评测的参数，不是固定数值。</li></ul><h3 id="示例-2-向量化与稠密召回" tabindex="-1">示例 2：向量化与稠密召回 <a class="header-anchor" href="#示例-2-向量化与稠密召回" aria-label="Permalink to &quot;示例 2：向量化与稠密召回&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>DIM = 256</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def embed(text: str, dim: int = DIM) -&gt; list[float]:</span></span>
<span class="line"><span>    &quot;&quot;&quot;标准库版特征哈希：相同 token 总落到同一维，再做 L2 归一化。&quot;&quot;&quot;</span></span>
<span class="line"><span>    vector = [0.0] * dim</span></span>
<span class="line"><span>    for token, count in Counter(tokenize(text)).items():</span></span>
<span class="line"><span>        digest = hashlib.sha256(token.encode(&quot;utf-8&quot;)).digest()</span></span>
<span class="line"><span>        index = int.from_bytes(digest[:4], &quot;big&quot;) % dim</span></span>
<span class="line"><span>        sign = 1.0 if digest[4] &amp; 1 else -1.0</span></span>
<span class="line"><span>        vector[index] += sign * (1.0 + math.log(count))</span></span>
<span class="line"><span>    norm = math.sqrt(sum(value * value for value in vector))</span></span>
<span class="line"><span>    return [value / norm for value in vector] if norm else vector</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def dot(left: list[float], right: list[float]) -&gt; float:</span></span>
<span class="line"><span>    if hasattr(math, &quot;sumprod&quot;):</span></span>
<span class="line"><span>        return math.sumprod(left, right)</span></span>
<span class="line"><span>    return sum(a * b for a, b in zip(left, right))</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def cosine(left: list[float], right: list[float]) -&gt; float:</span></span>
<span class="line"><span>    denominator = math.sqrt(dot(left, left)) * math.sqrt(dot(right, right))</span></span>
<span class="line"><span>    return dot(left, right) / denominator if denominator else 0.0</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def dense_search(query: str, docs: list[Doc], top_k: int = 5) -&gt; list[int]:</span></span>
<span class="line"><span>    query_vector = embed(query)</span></span>
<span class="line"><span>    scored = [(cosine(query_vector, embed(doc.text)), i) for i, doc in enumerate(docs)]</span></span>
<span class="line"><span>    scored.sort(key=lambda pair: (-pair[0], docs[pair[1]].doc_id))</span></span>
<span class="line"><span>    return [index for _, index in scored[:top_k]]</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>QUERY = &quot;GIL 是什么？CPU 密集为什么用多进程？&quot;</span></span>
<span class="line"><span>print(&quot;dim:&quot;, len(embed(QUERY)))</span></span>
<span class="line"><span>for i in dense_search(QUERY, CORPUS, top_k=3):</span></span>
<span class="line"><span>    print(f&quot;{cosine(embed(QUERY), embed(CORPUS[i].text)):.4f}&quot;, CORPUS[i].doc_id)</span></span></code></pre></div><p>输出：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>dim: 256</span></span>
<span class="line"><span>0.2762 Q004</span></span>
<span class="line"><span>0.2688 Q001</span></span>
<span class="line"><span>0.1447 Q006</span></span></code></pre></div><p>要点：</p><ul><li><code>embed()</code> 是特征哈希（hashing trick）：每个 token 经 SHA-256 映射到固定维度，再用符号位减少碰撞偏差。它不需要训练，但不是语义模型，只用来让示例跑通。</li><li>稠密召回就是按余弦相似度降序取 top-N，与 OpenAI 语义检索 cookbook 的做法一致。</li></ul><p>生产替换点（可选依赖 <code>openai</code>，不属于上面的标准库示例）：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span># pip install openai</span></span>
<span class="line"><span># 运行前设置环境变量 OPENAI_API_KEY，不要把 key 写进代码</span></span>
<span class="line"><span>from openai import OpenAI</span></span>
<span class="line"><span></span></span>
<span class="line"><span>client = OpenAI()</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def embed_remote(text: str) -&gt; list[float]:</span></span>
<span class="line"><span>    response = client.embeddings.create(</span></span>
<span class="line"><span>        input=text,</span></span>
<span class="line"><span>        model=&quot;text-embedding-3-small&quot;,</span></span>
<span class="line"><span>    )</span></span>
<span class="line"><span>    return response.data[0].embedding</span></span></code></pre></div><p>不要把本页 256 维的特征哈希向量与真实模型向量放进同一个索引。</p><h3 id="示例-3-bm25-与-rrf-混合召回" tabindex="-1">示例 3：BM25 与 RRF 混合召回 <a class="header-anchor" href="#示例-3-bm25-与-rrf-混合召回" aria-label="Permalink to &quot;示例 3：BM25 与 RRF 混合召回&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>class BM25:</span></span>
<span class="line"><span>    def __init__(self, docs: list[Doc], k1: float = 1.2, b: float = 0.75) -&gt; None:</span></span>
<span class="line"><span>        self.docs = docs</span></span>
<span class="line"><span>        self.k1 = k1</span></span>
<span class="line"><span>        self.b = b</span></span>
<span class="line"><span>        self.tfs = [Counter(tokenize(doc.text)) for doc in docs]</span></span>
<span class="line"><span>        self.lengths = [sum(tf.values()) for tf in self.tfs]</span></span>
<span class="line"><span>        self.avgdl = sum(self.lengths) / max(1, len(self.lengths))</span></span>
<span class="line"><span>        self.df: Counter[str] = Counter()</span></span>
<span class="line"><span>        for tf in self.tfs:</span></span>
<span class="line"><span>            self.df.update(tf.keys())</span></span>
<span class="line"><span>        self.N = len(docs)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def idf(self, term: str) -&gt; float:</span></span>
<span class="line"><span>        n = self.df.get(term, 0)</span></span>
<span class="line"><span>        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def score(self, query: str, doc_index: int) -&gt; float:</span></span>
<span class="line"><span>        query_terms = set(tokenize(query))</span></span>
<span class="line"><span>        tf = self.tfs[doc_index]</span></span>
<span class="line"><span>        length = self.lengths[doc_index] or 1</span></span>
<span class="line"><span>        total = 0.0</span></span>
<span class="line"><span>        for term in query_terms:</span></span>
<span class="line"><span>            freq = tf.get(term, 0)</span></span>
<span class="line"><span>            if not freq:</span></span>
<span class="line"><span>                continue</span></span>
<span class="line"><span>            denominator = freq + self.k1 * (1 - self.b + self.b * length / self.avgdl)</span></span>
<span class="line"><span>            total += self.idf(term) * freq * (self.k1 + 1) / denominator</span></span>
<span class="line"><span>        return total</span></span>
<span class="line"><span></span></span>
<span class="line"><span>    def search(self, query: str, top_k: int = 5) -&gt; list[int]:</span></span>
<span class="line"><span>        order = sorted(range(self.N), key=lambda i: (-self.score(query, i), self.docs[i].doc_id))</span></span>
<span class="line"><span>        return order[:top_k]</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>def rrf(rankings: list[list[int]], k: int = 60, top_k: int = 5) -&gt; list[int]:</span></span>
<span class="line"><span>    scores: dict[int, float] = {}</span></span>
<span class="line"><span>    for ranking in rankings:</span></span>
<span class="line"><span>        for rank, doc_index in enumerate(ranking, start=1):</span></span>
<span class="line"><span>            scores[doc_index] = scores.get(doc_index, 0.0) + 1.0 / (k + rank)</span></span>
<span class="line"><span>    return sorted(scores, key=lambda i: (-scores[i], i))[:top_k]</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>bm25 = BM25(CORPUS)</span></span>
<span class="line"><span>sparse = bm25.search(QUERY, top_k=3)</span></span>
<span class="line"><span>dense = dense_search(QUERY, CORPUS, top_k=3)</span></span>
<span class="line"><span>print(&quot;bm25:&quot;, [CORPUS[i].doc_id for i in sparse])</span></span>
<span class="line"><span>print(&quot;dense:&quot;, [CORPUS[i].doc_id for i in dense])</span></span>
<span class="line"><span>print(&quot;rrf:&quot;, [CORPUS[i].doc_id for i in rrf([dense, sparse], k=60, top_k=3)])</span></span></code></pre></div><p>输出：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>bm25: [&#39;Q001&#39;, &#39;Q004&#39;, &#39;Q010&#39;]</span></span>
<span class="line"><span>dense: [&#39;Q004&#39;, &#39;Q001&#39;, &#39;Q006&#39;]</span></span>
<span class="line"><span>rrf: [&#39;Q001&#39;, &#39;Q004&#39;, &#39;Q006&#39;]</span></span></code></pre></div><p>要点：</p><ul><li>IDF 采用 Lucene BM25 的公式 <code>log(1 + (docCount - docFreq + 0.5) / (docFreq + 0.5))</code>；<code>k1 = 1.2</code>、<code>b = 0.75</code> 是 Elasticsearch 文档给出的默认值。</li><li>BM25 擅长 <code>GIL</code>、<code>ETag</code>、<code>304</code> 这类稀有标识符；稠密向量擅长意思相近但用词不同的查询，两路排名常不一致。</li><li>RRF 只用排名，每个文档的得分是各列表 <code>1 / (k + rank)</code> 之和，因此不必把 BM25 分数与余弦分数校准到同一量纲。</li></ul><h3 id="示例-4-重排" tabindex="-1">示例 4：重排 <a class="header-anchor" href="#示例-4-重排" aria-label="Permalink to &quot;示例 4：重排&quot;">​</a></h3><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>def rerank(query: str, docs: list[Doc], candidates: list[int], top_k: int = 3) -&gt; list[tuple[float, int]]:</span></span>
<span class="line"><span>    &quot;&quot;&quot;轻量交叉特征：同时看 query 与文档，模拟 cross-encoder 的成对打分。&quot;&quot;&quot;</span></span>
<span class="line"><span>    query_tokens = tokenize(query)</span></span>
<span class="line"><span>    query_set = set(query_tokens)</span></span>
<span class="line"><span>    query_bigrams = set(zip(query_tokens, query_tokens[1:]))</span></span>
<span class="line"><span>    scored: list[tuple[float, int]] = []</span></span>
<span class="line"><span>    for index in candidates:</span></span>
<span class="line"><span>        doc_tokens = tokenize(docs[index].text)</span></span>
<span class="line"><span>        doc_set = set(doc_tokens)</span></span>
<span class="line"><span>        doc_bigrams = set(zip(doc_tokens, doc_tokens[1:]))</span></span>
<span class="line"><span>        coverage = len(query_set &amp; doc_set) / max(1, len(query_set))</span></span>
<span class="line"><span>        phrase = len(query_bigrams &amp; doc_bigrams) / max(1, len(query_bigrams))</span></span>
<span class="line"><span>        density = sum(1 for token in doc_tokens if token in query_set) / max(1, len(doc_tokens))</span></span>
<span class="line"><span>        score = 0.55 * coverage + 0.30 * phrase + 0.15 * density</span></span>
<span class="line"><span>        scored.append((score, index))</span></span>
<span class="line"><span>    scored.sort(key=lambda pair: (-pair[0], docs[pair[1]].doc_id))</span></span>
<span class="line"><span>    return scored[:top_k]</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>fused = rrf([dense, sparse], k=60, top_k=6)</span></span>
<span class="line"><span>for score, index in rerank(QUERY, CORPUS, fused, top_k=3):</span></span>
<span class="line"><span>    print(f&quot;{score:.4f}&quot;, CORPUS[index].doc_id)</span></span></code></pre></div><p>输出：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>0.4580 Q001</span></span>
<span class="line"><span>0.4032 Q004</span></span>
<span class="line"><span>0.1327 Q010</span></span></code></pre></div><p>要点：</p><ul><li>这里的 <code>rerank()</code> 是教学用的交叉特征（词覆盖、bigram 短语命中、命中密度），便宜且可解释，但不是神经 cross-encoder。</li><li>生产中的 cross-encoder 把 <code>(query, document)</code> 拼在一起联合编码，比 query 与 document 各自编码的 bi-encoder 更准，但不能预先计算文档向量，因此只适合重排召回后的短列表。</li><li>top-k 不是越大越好：「Lost in the Middle」的实验显示，相关信息位于上下文中间时模型表现明显下降。</li></ul><hr><h2 id="四、练习-面经检索问答" tabindex="-1">四、练习：面经检索问答 <a class="header-anchor" href="#四、练习-面经检索问答" aria-label="Permalink to &quot;四、练习：面经检索问答&quot;">​</a></h2><h3 id="任务" tabindex="-1">任务 <a class="header-anchor" href="#任务" aria-label="Permalink to &quot;任务&quot;">​</a></h3><p>用示例中的 <code>CORPUS</code> 做一个面经检索问答：</p><ol><li>对每个问题分别用 BM25 与稠密向量召回 top-6；</li><li>用 RRF 融合两路排名；</li><li>对融合后的候选做 <code>rerank</code>，取 top-3；</li><li>返回 top-1 作为答案，并给出 top-3 引用；</li><li>用 5 条带标准答案的问题计算 <code>hit@1</code>；</li><li>调整一个参数（<code>recall_k</code>、<code>chunk_text</code> 的 <code>size/overlap</code> 或 rerank 权重），观察 top-1 是否变化并解释原因。</li></ol><p>验收标准：代码可运行；5 条问题都能打印 top-1 与 top-3；能说明为什么某题由 BM25 命中、另一题由稠密召回命中。</p><h3 id="参考答案" tabindex="-1">参考答案 <a class="header-anchor" href="#参考答案" aria-label="Permalink to &quot;参考答案&quot;">​</a></h3><p>接在示例 4 之后，保存在同一个 <code>mini_rag.py</code>：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>def hybrid_answer(question: str, docs: list[Doc], recall_k: int = 6, final_k: int = 3) -&gt; tuple[Doc, list[tuple[float, int]]]:</span></span>
<span class="line"><span>    bm25 = BM25(docs)</span></span>
<span class="line"><span>    dense = dense_search(question, docs, top_k=recall_k)</span></span>
<span class="line"><span>    sparse = bm25.search(question, top_k=recall_k)</span></span>
<span class="line"><span>    fused = rrf([dense, sparse], k=60, top_k=recall_k)</span></span>
<span class="line"><span>    ranked = rerank(question, docs, fused, top_k=final_k)</span></span>
<span class="line"><span>    if not ranked:</span></span>
<span class="line"><span>        raise LookupError(&quot;no candidate retrieved&quot;)</span></span>
<span class="line"><span>    return docs[ranked[0][1]], ranked</span></span>
<span class="line"><span></span></span>
<span class="line"><span></span></span>
<span class="line"><span>QUESTIONS = [</span></span>
<span class="line"><span>    (&quot;GIL 是什么？CPU 密集为什么用多进程？&quot;, &quot;Q001&quot;),</span></span>
<span class="line"><span>    (&quot;tuple 为什么能作为 dict 的 key？&quot;, &quot;Q002&quot;),</span></span>
<span class="line"><span>    (&quot;React useEffect 的清理函数什么时候执行？&quot;, &quot;Q006&quot;),</span></span>
<span class="line"><span>    (&quot;HTTP 缓存的 ETag 和 304 是什么？&quot;, &quot;Q008&quot;),</span></span>
<span class="line"><span>    (&quot;TypeScript 泛型的 extends 约束是什么？&quot;, &quot;Q010&quot;),</span></span>
<span class="line"><span>]</span></span>
<span class="line"><span></span></span>
<span class="line"><span>hits = 0</span></span>
<span class="line"><span>for question, gold in QUESTIONS:</span></span>
<span class="line"><span>    best, ranked = hybrid_answer(question, CORPUS)</span></span>
<span class="line"><span>    hit = best.doc_id == gold</span></span>
<span class="line"><span>    hits += int(hit)</span></span>
<span class="line"><span>    top3 = [CORPUS[index].doc_id for _, index in ranked]</span></span>
<span class="line"><span>    print(f&quot;{question}\\n  top1={best.doc_id} gold={gold} hit={hit} top3={top3}&quot;)</span></span>
<span class="line"><span></span></span>
<span class="line"><span>print(f&quot;hit@1: {hits}/{len(QUESTIONS)}&quot;)</span></span></code></pre></div><p>输出：</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>GIL 是什么？CPU 密集为什么用多进程？</span></span>
<span class="line"><span>  top1=Q001 gold=Q001 hit=True top3=[&#39;Q001&#39;, &#39;Q004&#39;, &#39;Q010&#39;]</span></span>
<span class="line"><span>tuple 为什么能作为 dict 的 key？</span></span>
<span class="line"><span>  top1=Q002 gold=Q002 hit=True top3=[&#39;Q002&#39;, &#39;Q007&#39;, &#39;Q001&#39;]</span></span>
<span class="line"><span>React useEffect 的清理函数什么时候执行？</span></span>
<span class="line"><span>  top1=Q006 gold=Q006 hit=True top3=[&#39;Q006&#39;, &#39;Q003&#39;, &#39;Q010&#39;]</span></span>
<span class="line"><span>HTTP 缓存的 ETag 和 304 是什么？</span></span>
<span class="line"><span>  top1=Q008 gold=Q008 hit=True top3=[&#39;Q008&#39;, &#39;Q003&#39;, &#39;Q005&#39;]</span></span>
<span class="line"><span>TypeScript 泛型的 extends 约束是什么？</span></span>
<span class="line"><span>  top1=Q010 gold=Q010 hit=True top3=[&#39;Q010&#39;, &#39;Q003&#39;, &#39;Q005&#39;]</span></span>
<span class="line"><span>hit@1: 5/5</span></span></code></pre></div><p>5/5 只说明这 5 条在这个小语料上通过，不代表真实效果。真实项目需要标注集、失败样本分析以及延迟与成本指标。</p><p>可继续改进：</p><ol><li>用 <code>chunk_text()</code> 把长答案切块，在块级别召回后按 <code>doc_id</code> 聚合分数；</li><li>给 <code>tokenize()</code> 换成正式的中文分词器；</li><li>把 <code>rerank()</code> 的权重当作超参数，在验证集上搜索；</li><li>记录每次召回的 BM25 排名、稠密排名与最终排名，区分「召回没进来」与「重排排错了」。</li></ol><hr><h2 id="五、面试常问的三个追问" tabindex="-1">五、面试常问的三个追问 <a class="header-anchor" href="#五、面试常问的三个追问" aria-label="Permalink to &quot;五、面试常问的三个追问&quot;">​</a></h2><h3 id="追问-1-切块大小和-overlap-怎么定" tabindex="-1">追问 1：切块大小和 overlap 怎么定？ <a class="header-anchor" href="#追问-1-切块大小和-overlap-怎么定" aria-label="Permalink to &quot;追问 1：切块大小和 overlap 怎么定？&quot;">​</a></h3><p>先看模型上限：<code>text-embedding-3-small</code> 的上下文为 8191 tokens，实际切块要留余量。从「固定长度 + 小重叠」的基线开始，用带标注的问题集观察 <code>hit@k</code>、MRR 与端到端答案质量。overlap 太小会切断跨块语义，太大则索引膨胀、召回重复。所引官方资料中没有可直接照搬的统一 <code>size/overlap</code> 数值，所以不给「最佳值」。</p><h3 id="追问-2-bm25-与向量召回的分数尺度不同-怎么融合" tabindex="-1">追问 2：BM25 与向量召回的分数尺度不同，怎么融合？ <a class="header-anchor" href="#追问-2-bm25-与向量召回的分数尺度不同-怎么融合" aria-label="Permalink to &quot;追问 2：BM25 与向量召回的分数尺度不同，怎么融合？&quot;">​</a></h3><p>最稳妥的起点是 RRF：不碰原始分数，只用排名，得分为各列表 <code>1/(k+rank)</code> 之和，Elasticsearch 的默认 <code>rank_constant</code> 为 60。代价是丢掉「分数有多高」的信息；若业务需要权重，应在验证集上学习融合权重或做分数校准，而不是直接相加两种分数。</p><h3 id="追问-3-已经有向量召回了-为什么还要重排" tabindex="-1">追问 3：已经有向量召回了，为什么还要重排？ <a class="header-anchor" href="#追问-3-已经有向量召回了-为什么还要重排" aria-label="Permalink to &quot;追问 3：已经有向量召回了，为什么还要重排？&quot;">​</a></h3><p>bi-encoder 对 query 与 document 各自编码，交互信息被压进两个向量；cross-encoder 联合编码 <code>(query, document)</code>，通常更准，但计算量大、不能预先算好所有文档，因此只对召回后的短列表重排。另外送入生成器的候选并非越多越好，应由评测决定 top-k。</p><hr><h2 id="六、参考资料" tabindex="-1">六、参考资料 <a class="header-anchor" href="#六、参考资料" aria-label="Permalink to &quot;六、参考资料&quot;">​</a></h2><table tabindex="0"><thead><tr><th>来源</th><th>覆盖内容</th></tr></thead><tbody><tr><td>Python 3.12 官方文档：<a href="https://docs.python.org/3.12/library/re.html" target="_blank" rel="noreferrer">re</a>、<a href="https://docs.python.org/3.12/library/collections.html" target="_blank" rel="noreferrer">collections</a>、<a href="https://docs.python.org/3.12/library/textwrap.html" target="_blank" rel="noreferrer">textwrap</a>、<a href="https://docs.python.org/3.12/library/math.html" target="_blank" rel="noreferrer">math</a>、<a href="https://docs.python.org/3.12/library/hashlib.html" target="_blank" rel="noreferrer">hashlib</a>、<a href="https://docs.python.org/3.12/howto/sorting.html" target="_blank" rel="noreferrer">排序指南</a></td><td>标准库行为与排序稳定性</td></tr><tr><td><a href="https://github.com/openai/openai-cookbook" target="_blank" rel="noreferrer">OpenAI Cookbook</a>（Embedding long inputs、Semantic text search using embeddings、Search reranking with cross-encoders）</td><td>token 上限、切块、SDK 调用形状、余弦召回、cross-encoder 重排</td></tr><tr><td><a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html" target="_blank" rel="noreferrer">Elasticsearch：Reciprocal rank fusion</a></td><td>RRF 公式与默认 <code>rank_constant</code></td></tr><tr><td><a href="https://github.com/apache/lucene" target="_blank" rel="noreferrer">Apache Lucene</a>（<code>BM25Similarity</code>）与 Elastic 博客 <em>Practical BM25</em></td><td>BM25 的 IDF 公式与 <code>k1</code>、<code>b</code> 默认值</td></tr><tr><td><a href="https://arxiv.org/abs/2307.03172" target="_blank" rel="noreferrer">Lost in the Middle（arXiv:2307.03172）</a></td><td>长上下文中间位置信息利用下降</td></tr></tbody></table><p><strong>未覆盖</strong>：Python 3.12 <code>str.split</code> 的官方段落未抓取成功，本页不对其边界行为下结论；统一的切块 size/overlap 最佳值与具体 rerank 服务的 API 未找到可核验的官方来源，本页只实现标准库启发式重排，不虚构接口。</p>`,68)])])}const f=n(t,[["render",l]]);export{h as __pageData,f as default};
