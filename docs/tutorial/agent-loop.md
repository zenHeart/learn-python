# 手写 Agent Loop 与工具调用

> 面向有 JS/TS 经验、第一次用 Python 写 LLM Agent 的工程师。示例只用标准库，在线运行器（Python 3.11）与本机 Python 3.12 均可运行；需要网络或线程、子进程的示例用 `text` 围栏展示。

---

## 一、一句话结论

**Agent Loop 就是一个循环：把「截至目前」的完整消息列表 `messages` 发给模型；如果返回的 assistant 消息带有 `tool_calls`（`finish_reason` 为 `tool_calls`），就在本地执行这些函数，把结果包成 `role="tool"`、带 `tool_call_id` 的消息接回列表，直到模型不再请求工具。** 模型只决定「调哪个工具、传什么参数」，真正执行工具的是你的代码。

用 Python 实现这一切只需要标准库：`dict` 承载 JSON，`json` 解析模型生成的参数字符串，`inspect` 校验参数，`asyncio` 管理并发。

依据：[DeepSeek Tool Calls 指南](https://api-docs.deepseek.com/guides/tool_calls)与 [Chat Completions API 参考](https://api-docs.deepseek.com/api/create-chat-completion)（OpenAI 兼容协议）。

---

## 二、与 JS/TS 的对照

| 主题 | JS/TS | Python | 注意点 |
|------|-------|--------|--------|
| 序列化 | `JSON.stringify` | `json.dumps` | `ensure_ascii` 默认为 `True`，中文会被转义，需要原样输出时传 `ensure_ascii=False` |
| 解析失败 | `JSON.parse` 抛 `SyntaxError` | `json.loads` 抛 `json.JSONDecodeError` | 模型生成的 `arguments` 属于不可信输入，解析前先限制长度 |
| 真假值 | 空数组、空对象为真 | 空序列、空集合、空 dict 为假 | `if []` 在两边结果相反 |
| 默认参数 | 每次调用重新求值 | 定义函数时只求值一次 | `def f(acc=[])` 的可变默认值会在调用间共享 |
| 类型注解 | TS 类型编译后擦除 | 注解运行时不强制 | 两边都需要运行时校验外部输入 |
| 子进程 | `exec` 经由 shell，`execFile` 不经 shell | `subprocess.run` 的 `shell` 默认为 `False` | `shell=True` 拼接用户输入有命令注入风险 |
| 并发聚合 | `Promise.all` | `asyncio.TaskGroup` | 任一子任务异常会取消其余任务，异常聚合为 `ExceptionGroup`，用 `except*` 捕获 |
| 超时 | `AbortController` 配合竞速 | `asyncio.timeout` | 超时抛 `TimeoutError`，要在上下文管理器外部捕获 |
| 阻塞调用 | `worker_threads` | `asyncio.to_thread` | 阻塞函数放进线程，避免卡住事件循环 |

对应官方文档：

- Python：[json](https://docs.python.org/3.12/library/json.html)、[asyncio 任务](https://docs.python.org/3.12/library/asyncio-task.html)、[subprocess](https://docs.python.org/3.12/library/subprocess.html)、[真值检测](https://docs.python.org/3.12/library/stdtypes.html#truth-value-testing)、[inspect.Signature.bind](https://docs.python.org/3.12/library/inspect.html#inspect.Signature.bind)
- JS：[MDN Falsy](https://developer.mozilla.org/en-US/docs/Glossary/Falsy)、[MDN JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)、[Node.js child_process](https://nodejs.org/docs/latest/api/child_process.html)

---

## 三、四个示例

### 示例 1：最小 Agent Loop

协议要点（依据 DeepSeek 文档）：

- 请求体的 `messages` 是截至目前的完整对话，每一轮都要重发全部历史；
- `tools` 描述可调用的函数，`parameters` 用 JSON Schema，`description` 帮助模型判断何时调用；
- 模型想调工具时，assistant 消息带 `tool_calls`，每次调用有唯一 `id`；
- 工具结果以 `role="tool"` 回传，用 `tool_call_id` 指明对应哪一次调用；
- `finish_reason` 为 `tool_calls` 表示模型发起了工具调用。

下面用一个规则驱动的「假模型」离线跑通协议：

```python
import json

# 1. 工具描述：就是普通 dict，序列化后原样进入请求体
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_interview_qa",
            "description": "在面经库里检索与 query 最相关的问答片段，返回 JSON 数组。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "检索关键词"},
                    "top_k": {"type": "integer", "description": "返回条数，取值 1-5"},
                },
                "required": ["query"],
            },
        },
    }
]

# 2. 本地工具实现：模型只「点菜」，做菜的是我们自己的代码
CORPUS = [
    {"id": "Q1", "q": "Python 的 GIL 是什么？",
     "a": "GIL 是全局解释器锁，同一时刻只允许一个线程执行 Python 字节码；"
          "因此多线程适合 IO 密集，CPU 密集要用多进程。"},
    {"id": "Q2", "q": "装饰器是怎么实现的？",
     "a": "装饰器是接收函数并返回新函数的高阶函数，@decorator 语法只是语法糖，"
          "常用于日志、鉴权、缓存等横切逻辑。"},
    {"id": "Q3", "q": "列表去重有哪些方法？",
     "a": "可用 dict.fromkeys 保序去重，或 set 去重（不保序）；数据量大时注意复杂度。"},
]


def search_interview_qa(query, top_k=3):
    """极简检索：按 query 与题目文本的字重合度打分（教学用）。"""
    scored = []
    for doc in CORPUS:
        score = sum(ch in doc["q"] for ch in query if not ch.isspace())
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [{"id": doc["id"], "q": doc["q"], "a": doc["a"], "score": score}
            for score, doc in scored[:top_k] if score > 0]


TOOL_IMPL = {"search_interview_qa": search_interview_qa}


# 3. 假模型：用规则模拟「模型决定调用工具」，离线可跑、行为确定。
#    真实响应里 finish_reason 在 choice 上，这里为教学合并进消息 dict。
def fake_model(messages, tools):
    already_called = any(m["role"] == "tool" for m in messages)
    last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if not already_called and "面经" in last_user:
        return {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": "call_001",
                "type": "function",
                "function": {
                    "name": "search_interview_qa",
                    # 注意：arguments 是 JSON 字符串，不是 dict
                    "arguments": json.dumps({"query": last_user, "top_k": 2},
                                            ensure_ascii=False),
                },
            }],
            "finish_reason": "tool_calls",
        }
    # 已经拿到工具结果 -> 基于结果生成最终回答
    hits = [json.loads(m["content"]) for m in messages if m["role"] == "tool"]
    lines = [f"- {h['id']} {h['q']}：{h['a']}" for batch in hits for h in batch]
    return {"role": "assistant",
            "content": "根据面经库检索结果：\n" + "\n".join(lines),
            "finish_reason": "stop"}


# 4. Agent Loop 本体：for + max_steps 兜底，比裸 while True 更安全
def run_agent_loop(question, model_fn=fake_model, max_steps=8):
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        print(f"--- 第 {step} 轮：向模型发送 {len(messages)} 条消息（全量历史）")
        msg = model_fn(messages, TOOLS)
        messages.append(msg)  # assistant 消息（含 tool_calls）原样入列
        if msg.get("finish_reason") != "tool_calls":
            return msg["content"] or ""
        for call in msg["tool_calls"]:
            name = call["function"]["name"]
            raw_args = call["function"]["arguments"]
            fn = TOOL_IMPL[name]
            try:
                result = fn(**json.loads(raw_args))
                content = json.dumps(result, ensure_ascii=False)
            except Exception as exc:  # 工具失败不该炸掉整个 loop
                content = f"工具调用失败：{type(exc).__name__}: {exc}"
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": content})
    return "（已达到 max_steps，强制退出）"


print(run_agent_loop("面经里关于 Python GIL 和装饰器说了什么？"))
```

预期输出：

```text
--- 第 1 轮：向模型发送 1 条消息（全量历史）
--- 第 2 轮：向模型发送 3 条消息（全量历史）
根据面经库检索结果：
- Q1 Python 的 GIL 是什么？：GIL 是全局解释器锁，同一时刻只允许一个线程执行 Python 字节码；因此多线程适合 IO 密集，CPU 密集要用多进程。
- Q2 装饰器是怎么实现的？：装饰器是接收函数并返回新函数的高阶函数，@decorator 语法只是语法糖，常用于日志、鉴权、缓存等横切逻辑。
```

三个要点：

1. **协议就是消息列表的增删**：`user` 起头，`assistant`（带 `tool_calls`）追加，`tool` 结果回填，再回到模型。第 2 轮发送 3 条消息，说明历史是全量重发的。
2. **`tool_calls` 是数组**：模型一次可以请求多个工具，示例 3 处理这种情况。
3. **`max_steps` 是底线**：模型可能反复请求同一个工具，没有上限的 `while True` 会持续消耗调用额度。

### 示例 2：把模型输出当作不可信输入

DeepSeek 文档指出，`function.arguments` 是模型生成的 JSON 字符串，模型并不总是生成合法 JSON，也可能生成函数 schema 中没有的参数，调用函数前需要在代码里校验。下面的 `parse_tool_arguments` 依次设置四道检查：

```python
import inspect
import json
from typing import get_type_hints

MAX_ARGS_BYTES = 4096  # 长度闸门：限制待解析数据的大小


class ToolArgumentError(ValueError):
    """工具参数不合法。消息会作为 tool 消息内容喂回模型，而不是炸掉 loop。"""


def search_interview_qa(query: str, top_k: int = 3) -> list:
    return [{"id": "Q1", "q": "示例命中", "a": "……"}]


def parse_tool_arguments(fn, raw):
    """把模型生成的 arguments 字符串安全地变成 fn 的 kwargs。"""
    # 1) 长度闸门
    if len(raw.encode("utf-8")) > MAX_ARGS_BYTES:
        raise ToolArgumentError("arguments 超过长度上限")
    # 2) 只信 json.loads，并接住 JSONDecodeError
    try:
        args = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ToolArgumentError(f"不是合法 JSON：{exc}") from exc
    # 3) 顶层必须是 object
    if not isinstance(args, dict):
        raise ToolArgumentError("arguments 顶层必须是 JSON object")
    # 4) 签名绑定：校验参数名与形态，多出来的字段在这里现形
    try:
        inspect.signature(fn).bind(**args)
    except TypeError as exc:
        raise ToolArgumentError(f"参数与函数签名不匹配：{exc}") from exc
    # 5) bind 只管「绑得上」，不校验类型；按注解补一次轻量检查
    hints = get_type_hints(fn)
    for key, value in args.items():
        if hints.get(key) is int and not isinstance(value, int):
            raise ToolArgumentError(f"参数 {key} 需要 int，实际是 {type(value).__name__}")
    return args


CASES = [
    ("合法参数", '{"query": "GIL", "top_k": 2}'),
    ("模型输出坏 JSON", '{"query": "GIL", "top_k": 2'),   # 缺右括号
    ("幻觉出的参数名", '{"query": "GIL", "limit": 10}'),  # schema 里没有 limit
    ("参数类型不对", '{"query": "GIL", "top_k": "很多"}'),  # str 传给 int 形参
    ("顶层不是 object", '["GIL"]'),
    ("超长输入", '{"query": "' + "GIL" * 2000 + '"}'),
]

for title, raw in CASES:
    try:
        print(f"{title} -> OK: {parse_tool_arguments(search_interview_qa, raw)}")
    except ToolArgumentError as exc:
        # 关键：把错误原因作为 tool 消息发回模型，让它自我修正
        print(f"{title} -> 喂回模型的错误信息: {exc}")
```

预期输出：

```text
合法参数 -> OK: {'query': 'GIL', 'top_k': 2}
模型输出坏 JSON -> 喂回模型的错误信息: 不是合法 JSON：Expecting ',' delimiter: line 1 column 28 (char 27)
幻觉出的参数名 -> 喂回模型的错误信息: 参数与函数签名不匹配：got an unexpected keyword argument 'limit'
参数类型不对 -> 喂回模型的错误信息: 参数 top_k 需要 int，实际是 str
顶层不是 object -> 喂回模型的错误信息: arguments 顶层必须是 JSON object
超长输入 -> 喂回模型的错误信息: arguments 超过长度上限
```

设计要点：

- **失败即反馈**：错误文本作为 `tool` 消息发回模型，模型下一轮通常能据此修正参数，比直接抛异常终止 loop 更稳健。练习中有完整演示。
- **`bind` 不校验类型**：它只检查参数名和个数能否匹配，所以补了基于注解的轻量类型检查；生产环境建议改用 JSON Schema 校验库。
- **不要用 `eval` 解析参数**：官方文档说明 `eval` 会执行任意代码，对用户输入使用可能带来安全漏洞，而模型输出应按用户输入对待。解析 JSON 请使用 `json.loads`。

依据：[json 模块文档](https://docs.python.org/3.12/library/json.html)（含对不可信 JSON 的资源消耗提示）、[`eval` 内置函数文档](https://docs.python.org/3.12/library/functions.html#eval)、[`inspect.Signature.bind`](https://docs.python.org/3.12/library/inspect.html#inspect.Signature.bind)。

### 示例 3：一次返回多个 tool_call——并发、超时与阻塞工具

协议不规定多个 `tool_call` 的执行顺序。彼此无依赖的工具应当并发执行，否则延迟线性叠加。Python 3.11 起提供 `asyncio.TaskGroup` 与 `asyncio.timeout`，对应 JS 里的 `Promise.all` 与超时控制。该示例用到事件循环、线程和子进程，浏览器内的运行器不支持，请在本机运行（`python3 example3.py`）：

```text
import asyncio
import subprocess
import sys
import time


class ToolArgumentError(ValueError):
    pass


async def tool_search_qa(query, delay=0.1):
    await asyncio.sleep(delay)  # 模拟等模型 / 等数据库
    return {"tool": "search_qa", "query": query, "hits": 2}


async def tool_fetch_url(url, delay=0.1):
    await asyncio.sleep(delay)
    return {"tool": "fetch_url", "url": url, "bytes": 1234}


def tool_grep_corpus(pattern, timeout=2.0):
    """同步阻塞工具：subprocess 超时后会杀死子进程并等待其结束，再抛 TimeoutExpired。"""
    proc = subprocess.run(
        [sys.executable, "-c", "import time; time.sleep(30)"],  # 故意卡住
        capture_output=True, text=True, timeout=timeout,
    )
    return {"tool": "grep_corpus", "pattern": pattern, "returncode": proc.returncode}


ASYNC_TOOLS = {"search_qa": tool_search_qa, "fetch_url": tool_fetch_url}


async def run_one(call):
    name, args = call["name"], call["args"]
    if name in ASYNC_TOOLS:
        return await ASYNC_TOOLS[name](**args)
    if name == "grep_corpus":
        return await asyncio.to_thread(tool_grep_corpus, **args)  # 阻塞函数进线程
    raise ToolArgumentError(f"未知工具：{name}")


async def run_tool_calls(calls, budget=1.0):
    """并发执行一批 tool_call；budget 是总预算（秒）。"""
    try:
        async with asyncio.timeout(budget):
            failure = None
            try:
                async with asyncio.TaskGroup() as tg:
                    tasks = [tg.create_task(run_one(c)) for c in calls]
            except* ToolArgumentError as eg:  # ExceptionGroup 用 except* 接
                failure = {"tool": "*", "error": f"{len(eg.exceptions)} 个工具失败：{eg.exceptions}"}
            if failure is not None:  # return 不能写在 except* 块里
                return failure
        return [t.result() for t in tasks]
    except TimeoutError:  # 只能在 timeout 上下文外部捕获
        return [{"tool": "*", "error": f"总预算 {budget}s 用尽，未完成的任务已被取消"}]


def demo_calls():
    return [
        {"name": "search_qa", "args": {"query": "GIL"}},
        {"name": "fetch_url", "args": {"url": "https://example.com"}},
    ]


async def main():
    print("== 场景 A：两个异步工具并发，总预算 1s ==")
    started = time.perf_counter()
    print(await run_tool_calls(demo_calls(), budget=1.0))
    print(f"耗时 {time.perf_counter() - started:.2f}s（串行约 0.2s）")

    print("== 场景 B：预算只有 0.05s，超时取消 ==")
    print(await run_tool_calls(demo_calls(), budget=0.05))

    print("== 场景 C：一个工具抛异常，TaskGroup 取消其余任务 ==")
    print(await run_tool_calls(demo_calls() + [{"name": "no_such_tool", "args": {}}]))

    print("== 场景 D：阻塞工具经 to_thread 执行，超时被杀 ==")
    try:
        await asyncio.to_thread(tool_grep_corpus, "GIL", 0.5)
    except subprocess.TimeoutExpired as exc:
        print(f"TimeoutExpired：{exc.timeout}s 后超时，子进程已被杀死")


asyncio.run(main())
```

预期输出：

```text
== 场景 A：两个异步工具并发，总预算 1s ==
[{'tool': 'search_qa', 'query': 'GIL', 'hits': 2}, {'tool': 'fetch_url', 'url': 'https://example.com', 'bytes': 1234}]
耗时 0.10s（串行约 0.2s）
== 场景 B：预算只有 0.05s，超时取消 ==
[{'tool': '*', 'error': '总预算 0.05s 用尽，未完成的任务已被取消'}]
== 场景 C：一个工具抛异常，TaskGroup 取消其余任务 ==
{'tool': '*', 'error': "1 个工具失败：(ToolArgumentError('未知工具：no_such_tool'),)"}
== 场景 D：阻塞工具经 to_thread 执行，超时被杀 ==
TimeoutExpired：0.5s 后超时，子进程已被杀死
```

四个语义，迁移时逐一对应：

1. **`TaskGroup` 不等于 `Promise.all`**：第一个非 `CancelledError` 异常会取消组内剩余任务，所有异常最终打包为 `ExceptionGroup`，要用 `except*` 捕获（场景 C）。`return`、`break` 不能出现在 `except*` 块内，所以先存变量再返回。
2. **`asyncio.timeout` 把取消转换为超时**：超时后取消当前任务，并把内部的 `CancelledError` 转成 `TimeoutError`，只能在上下文管理器外部捕获（场景 B）。
3. **阻塞函数进线程**：`asyncio.to_thread` 面向会阻塞事件循环的 IO 密集函数（场景 D）。
4. **同步工具也要有超时**：`subprocess` 超时后会终止子进程并等待其结束，再抛 `TimeoutExpired`。

依据：[asyncio 任务文档](https://docs.python.org/3.12/library/asyncio-task.html)（`TaskGroup`、`timeout`、`to_thread`）、[subprocess 文档](https://docs.python.org/3.12/library/subprocess.html)。

### 示例 4：把假模型换成真实 HTTP 客户端

示例 1 的 `run_agent_loop` 通过 `model_fn` 参数注入模型，换成真实接口时 loop 本身不用改。下面用标准库 `urllib.request` 构造 OpenAI 兼容端点的请求，需要你自己的 API Key 和网络，因此用 `text` 围栏展示，不在页面中运行：

```text
import json
import os
import urllib.request

BASE_URL = "https://api.deepseek.com"   # OpenAI 兼容端点
MODEL = "deepseek-chat"


def chat_completions(messages, tools, api_key, timeout=30.0):
    """POST {BASE_URL}/chat/completions，返回解析后的响应 dict。"""
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        # 不传 tool_choice：有 tools 时默认是 auto
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    # timeout 单位是秒，必须显式传
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def real_model(messages, tools):
    """适配成 fake_model 的签名，run_agent_loop 不用改。"""
    api_key = os.environ.get("API_KEY", "")
    if not api_key:
        raise RuntimeError("缺少 API_KEY 环境变量")
    data = chat_completions(messages, tools, api_key)
    choice = data["choices"][0]
    msg = choice["message"]
    msg["finish_reason"] = choice["finish_reason"]  # finish_reason 在 choice 上，并回消息里
    return msg


# 用法：print(run_agent_loop("面经里关于 GIL 说了什么？", model_fn=real_model))
```

三个工程细节：

- **`urlopen` 的 `timeout`**：以秒为单位限制连接等阻塞操作，需要显式传入；
- **`HTTPError` 同时是异常和 file-like 对象**：4xx、5xx 时可以用 `exc.read()` 读取服务端返回的错误 JSON；
- **`tool_choice` 可以不传**：没有 `tools` 时默认 `none`，有 `tools` 时默认 `auto`。

依据：[urllib.request 文档](https://docs.python.org/3.12/library/urllib.request.html)、[urllib.error 文档](https://docs.python.org/3.12/library/urllib.error.html)、[DeepSeek Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion)。

---

## 四、练习：面经检索问答 Agent

### 任务

用上面的积木搭一个「面经检索问答」小 Agent：

1. **检索工具**：内置 8 条以上面经语料（题目加要点答案），实现 `search_interview_qa(query, top_k=3)`。中文检索可用「字符二元组（bigram）加 IDF」打分，只需标准库。
2. **安全解析**：复用示例 2 的检查；任何失败都转成文本喂回模型，不让 loop 中断。
3. **Agent Loop**：复用示例 1 的结构；离线模型用规则模拟，并演示一次「多余参数、错误反馈、自我修正」的完整过程。
4. **带引用的回答**：最终回答列出命中的面经编号（如 `[Q1]`）；检索不到时明确说明库中没有。

验收：问「Python 的 GIL 是什么」时输出工具调用日志、自我修正过程和带编号的回答；问语料外的问题（如「今天天气怎么样」）时输出「没有检索到相关内容」；全程不发起网络请求。

### 参考答案

```python
import inspect
import json
import math
import re
from enum import StrEnum

# 0. 面经语料（教学数据）
CORPUS = [
    {"id": "Q1", "q": "Python 的 GIL 是什么？对多线程有什么影响？",
     "a": "GIL 是全局解释器锁，同一时刻只允许一个线程执行 Python 字节码。"
          "多线程适合 IO 密集场景；CPU 密集要用多进程或 C 扩展。"},
    {"id": "Q2", "q": "装饰器的实现原理是什么？",
     "a": "装饰器是接收函数、返回函数的高阶函数；@decorator 只是语法糖。"
          "常见用途：日志、鉴权、重试、缓存。"},
    {"id": "Q3", "q": "列表去重有哪些方法？",
     "a": "dict.fromkeys 可保序去重；set 去重更快但不保序。"
          "元素是 dict 时不可哈希，需要先转成元组。"},
    {"id": "Q4", "q": "with 语句和上下文管理器是干嘛的？",
     "a": "上下文管理器通过 __enter__/__exit__ 管理资源，with 保证退出时释放，"
          "等价于 try/finally 的语法糖。"},
    {"id": "Q5", "q": "生成器和迭代器有什么区别？",
     "a": "迭代器实现 __iter__/__next__；生成器是写起来像函数的迭代器，"
          "用 yield 暂停/恢复，惰性求值省内存。"},
    {"id": "Q6", "q": "浅拷贝和深拷贝的区别？",
     "a": "浅拷贝只复制顶层容器，内层对象共享；深拷贝递归复制整个对象图，"
          "用 copy.deepcopy。"},
    {"id": "Q7", "q": "*args 和 **kwargs 是什么？",
     "a": "*args 收集多余位置参数为元组，**kwargs 收集多余关键字参数为 dict；"
          "常用于透传参数和装饰器。"},
    {"id": "Q8", "q": "lambda 表达式有什么限制？",
     "a": "lambda 只能写单个表达式，不能包含语句；复杂逻辑应改用 def，"
          "可读性优先。"},
]

# 1. 检索：中文二元组（bigram）+ IDF 打分，纯标准库
_TOKEN = re.compile(r"\w+", re.UNICODE)


def bigrams(text):
    text = "".join(_TOKEN.findall(text))
    return [text[i:i + 2] for i in range(len(text) - 1)] or ([text] if text else [])


def build_index(corpus):
    """计算每个 bigram 的 IDF：出现在越少文档里的词越关键。"""
    df = {}
    for doc in corpus:
        for gram in set(bigrams(doc["q"] + doc["a"])):
            df[gram] = df.get(gram, 0) + 1
    n = len(corpus)
    return {g: math.log((n + 1) / (c + 1)) + 1.0 for g, c in df.items()}


IDF = build_index(CORPUS)


def search_interview_qa(query, top_k=3):
    q_grams = bigrams(query)
    scored = []
    for doc in CORPUS:
        text = doc["q"] + doc["a"]
        score = sum(IDF.get(g, 0.0) for g in q_grams if g in text)
        scored.append((score, doc))
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [{"id": d["id"], "q": d["q"], "a": d["a"], "score": round(s, 3)}
            for s, d in scored[:top_k] if s > 0]


# 2. 工具名用 StrEnum：成员本身就是 str，可直接当字符串查表
class ToolName(StrEnum):
    SEARCH_INTERVIEW_QA = "search_interview_qa"


TOOL_IMPL = {ToolName.SEARCH_INTERVIEW_QA: search_interview_qa}
MAX_ARGS_BYTES = 4096


class ToolArgumentError(ValueError):
    pass


def call_tool(call):
    """执行单个 tool_call；参数问题统一抛 ToolArgumentError。"""
    fn = TOOL_IMPL[call["function"]["name"]]
    raw = call["function"]["arguments"]
    if len(raw.encode("utf-8")) > MAX_ARGS_BYTES:
        raise ToolArgumentError("arguments 超过长度上限")
    try:
        args = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ToolArgumentError(f"不是合法 JSON：{exc}") from exc
    if not isinstance(args, dict):
        raise ToolArgumentError("arguments 顶层必须是 JSON object")
    try:
        inspect.signature(fn).bind(**args)
    except TypeError as exc:
        raise ToolArgumentError(f"参数与函数签名不匹配：{exc}") from exc
    return json.dumps(fn(**args), ensure_ascii=False)


def make_call(call_id, arguments):
    return {"role": "assistant", "content": None, "finish_reason": "tool_calls",
            "tool_calls": [{"id": call_id, "type": "function", "function": {
                "name": "search_interview_qa",
                "arguments": json.dumps(arguments, ensure_ascii=False)}}]}


# 3. 离线模型：第一轮故意给出多余参数 k，收到报错后自我修正
def fake_model(messages):
    last_user = next(m["content"] for m in reversed(messages) if m["role"] == "user")
    tool_msgs = [m for m in messages if m["role"] == "tool"]
    if not tool_msgs:
        return make_call("call_1", {"query": last_user, "k": 3})
    if "参数与函数签名不匹配" in tool_msgs[-1]["content"]:  # 只看最后一条
        return make_call("call_2", {"query": last_user, "top_k": 3})
    hits = [h for m in tool_msgs if not m["content"].startswith("工具调用失败")
            for h in json.loads(m["content"])]
    if not hits:
        return {"role": "assistant", "finish_reason": "stop",
                "content": "面经库里没有检索到相关内容，换个关键词试试。"}
    lines = [f"[{h['id']}] {h['q']}\n    {h['a']}" for h in hits]
    return {"role": "assistant", "finish_reason": "stop",
            "content": "参考面经回答：\n" + "\n".join(lines)}


# 4. Loop 本体
def run_agent_loop(question, max_steps=8):
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        print(f"[loop] 第 {step} 轮，累计 {len(messages)} 条消息")
        msg = fake_model(messages)
        messages.append(msg)
        if msg["finish_reason"] != "tool_calls":
            return msg["content"]
        for call in msg["tool_calls"]:
            try:
                content = call_tool(call)
            except ToolArgumentError as exc:
                content = f"工具调用失败：{exc}"
            print(f"[tool] {call['function']['arguments']}")
            print(f"[tool] -> {content[:60]}{'…' if len(content) > 60 else ''}")
            messages.append({"role": "tool", "tool_call_id": call["id"],
                             "content": content})
    return "（达到 max_steps，强制退出）"


print(run_agent_loop("面经：Python 的 GIL 是什么？对多线程有什么影响？"))
print("=" * 20)
print(run_agent_loop("今天天气怎么样"))
```

预期输出：

```text
[loop] 第 1 轮，累计 1 条消息
[tool] {"query": "面经：Python 的 GIL 是什么？对多线程有什么影响？", "k": 3}
[tool] -> 工具调用失败：参数与函数签名不匹配：got an unexpected keyword argument 'k'
[loop] 第 2 轮，累计 3 条消息
[tool] {"query": "面经：Python 的 GIL 是什么？对多线程有什么影响？", "top_k": 3}
[tool] -> [{"id": "Q1", "q": "Python 的 GIL 是什么？对多线程有什么影响？", "a": "GIL …
[loop] 第 3 轮，累计 5 条消息
参考面经回答：
[Q1] Python 的 GIL 是什么？对多线程有什么影响？
    GIL 是全局解释器锁，同一时刻只允许一个线程执行 Python 字节码。多线程适合 IO 密集场景；CPU 密集要用多进程或 C 扩展。
[Q2] 装饰器的实现原理是什么？
    装饰器是接收函数、返回函数的高阶函数；@decorator 只是语法糖。常见用途：日志、鉴权、重试、缓存。
[Q5] 生成器和迭代器有什么区别？
    迭代器实现 __iter__/__next__；生成器是写起来像函数的迭代器，用 yield 暂停/恢复，惰性求值省内存。
====================
[loop] 第 1 轮，累计 1 条消息
[tool] {"query": "今天天气怎么样", "k": 3}
[tool] -> 工具调用失败：参数与函数签名不匹配：got an unexpected keyword argument 'k'
[loop] 第 2 轮，累计 3 条消息
[tool] {"query": "今天天气怎么样", "top_k": 3}
[tool] -> []
[loop] 第 3 轮，累计 5 条消息
面经库里没有检索到相关内容，换个关键词试试。
```

关于自我修正的判断条件：`fake_model` 只检查**最后一条** `tool` 消息。若写成「历史中出现过错误就重试」，错误信息会一直留在 `messages` 中，模型将反复重试同一个工具；真实模型搭配脆弱规则时也会出现这种情况，`max_steps` 是最后的保险。

---

## 五、面试常问的三个追问

### 追问 1：为什么 Agent Loop 用循环而不是递归？

循环的状态就是 `messages` 列表本身，「直到模型不再请求工具」天然是循环的终止条件。每一轮做三件事：发送全量历史，有 `tool_calls` 就执行并回填，否则结束。递归写法要把消息列表逐层传递，而 Python 解释器栈有最大深度上限（`sys.getrecursionlimit()` 返回该上限），对话变深时会触达限制。工程上再加两层保护：`max_steps` 兜底，以及检测「同一工具加同一参数」的重复调用。

### 追问 2：模型返回的 arguments 是字符串，直接 json.loads 就够了吗？

不够。官方文档说明 `arguments` 可能不是合法 JSON，也可能包含 schema 中没有的参数，需要调用前自行校验。生产做法是依次执行：限制长度、`json.loads` 并处理 `JSONDecodeError`、校验顶层是 object、用 `inspect.Signature.bind` 校验参数名与形态，必要时再补类型检查。校验失败时不要把异常抛出 loop，而是把原因作为 `tool` 消息喂回模型。另外，schema 中的 `required` 只是给模型的提示，不是运行时保证。

### 追问 3：一次返回多个 tool_call，并发还是串行？

协议不规定顺序，选择权在调用方。无依赖的工具并发执行：`asyncio.TaskGroup` 加 `asyncio.timeout` 提供结构化并发和总预算；阻塞的同步工具用 `asyncio.to_thread` 放入线程。并发之前先确认两点：**依赖**（后一个工具的入参来自前一个的结果时只能串行）和**副作用**（并发会放大对下游的写入压力，非幂等操作应串行或加锁）。迁移时不要把 `TaskGroup` 当 `Promise.all`：前者在首个异常时取消其余任务。

---

## 六、参考资料

| 来源 | 覆盖内容 |
|------|----------|
| [Python 3.12 官方文档](https://docs.python.org/3.12/) | json、asyncio、subprocess、inspect、urllib、真值检测等标准库与语言行为 |
| [DeepSeek API 文档](https://api-docs.deepseek.com/) | `messages`、`tools`、`tool_calls`、`tool` 消息、`finish_reason`、`tool_choice`、`arguments` 校验要求（OpenAI 兼容协议） |
| [MDN Web Docs](https://developer.mozilla.org/) | JS 侧 Falsy、`JSON.parse`、`JSON.stringify` 等行为 |
| [Node.js child_process](https://nodejs.org/docs/latest/api/child_process.html) | `exec` 与 `execFile` 的 shell 语义 |

**未覆盖**：OpenAI 与 Anthropic 官方文档在原交付物写作环境中未能抓取，本页不对其 tool-use 协议细节下结论；若需对照，请另行补充。
