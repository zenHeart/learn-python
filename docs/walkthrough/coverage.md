# 覆盖总账

> 声明数量必须等于实测数量。下面是走查开始时对磁盘的实测，不是计划。

## 外部前置（README 声明但站内不提供）

`README.md` 列了一串外部学习路径，全部是站外链接，**本仓库不提供内容**。
它们既是「外部前置」，也是进度标记（百分比是 README 里的自报，未核验）：

| 分类 | 条目 | README 自报进度 |
|------|------|----------------|
| 基础 | python tutorial（官方入门） | 60% |
| 基础 | python reference（语言手册） | 40% |
| 基础 | MIT python 视频 + MIT 教案 | 0% |
| 基础 | python hardway | — |
| 基础 | PEP 规范 | — |
| 基础 | pip 用户手册 / pip 帮助中心 | 0% |
| 基础 | python 标准库学习 | 0% |
| 计划阅读 | dive in python | — |
| 计划阅读 | think python | — |
| 计划阅读 | python/C API | — |
| 工具 | flask doc / awesome（中 / 英） | — |
| 工具 | pytest doc / awesome | — |
| 工具 | airtest | — |

**与站内教程的关系**：这些链接**没有一条在 `docs/` 里被引用**。
走查者从站内页面无法知道它们存在，站内也没有说明「学 L1 之前要不要先看
官方 tutorial」。README 的自报进度与 `docs/progress.md` 的课表也是两套
独立口径，互不一致。

## 课程真实存在的内容

`docs/` 下 Markdown 文件共 **19** 个（不含 `.vitepress/` 产物）：

| 文件 | 路由 | 类型 | 走查状态 |
|------|------|------|---------|
| `docs/index.md` | `/` | 首页 hero | ✅ 已走查 |
| `docs/progress.md` | `/progress` | 学习进度页 | ✅ 已走查 |
| `docs/tutorial/begin.md` | `/tutorial/begin` | L1 教程 | ✅ 已走查 |
| `docs/tutorial/annotation.md` | `/tutorial/annotation` | 标注规范 | ✅ 已走查 |
| `docs/tutorial/gaps.md` | `/tutorial/gaps` | 知识盲点清单 | ✅ 已走查 |
| `docs/tutorial/unpack.md` | `/tutorial/unpack` | 拆包完全指南 | ✅ 已走查 |
| `docs/walkthrough/*` | `/walkthrough/*` | 走查笔记 13 页 | ✅ 本轮新增 5 页 |

`examples/` 下 Python 文件共 **66** 个（`find examples -name '*.py' | wc -l`），
但**只有 `examples/mnist/` 被教程引用过一次**，其余 65 个与课程零关联。
（原为 67：`_draft/11-define-variable.py` 是 0 字节空文件，已删除，D-29。）

## 计划 vs 现实

`docs/progress.md` 规划了 15 课。实际写出：

| 课 | 计划内容 | 实际 |
|----|---------|------|
| L1 | Hello Python — print / 变量 / 注释 | ✅ 存在（走查前 9 个交互块中 5 个报错，已修） |
| L2 | 数据类型 — int / str / bool / list | ❌ 不存在，`begin.md` 末尾写「敬请期待」 |
| L3 | 控制流 — if / for / while | ❌ 不存在 |
| L4 | 函数 — def / 参数 / 返回值 | ❌ 不存在 |
| L5 | 类 — class / 方法 / 继承 | ❌ 不存在 |
| L6 | 异步编程 asyncio | ❌ 不存在 |
| L7 | HTTP 与 API 调用（httpx） | ❌ 不存在 |
| L8 | 数据处理（Pydantic） | ❌ 不存在 |
| L9 | Tool Use / Function Calling | ❌ 不存在 |
| L10 | Prompt 工程 | ❌ 不存在 |
| L11 | Chain 编排 | ❌ 不存在 |
| L12 | Memory 与上下文管理 | ❌ 不存在 |
| L13 | 单文件 Agent 示例 | ❌ 不存在 |
| L14 | 多工具编排 | ❌ 不存在 |
| L15 | 自主决策树 | ❌ 不存在 |

**结论：1 / 15 课存在。** 首页 `docs/index.md` 的 feature 卡片写
「从基础语法到 Agent 开发，15 节课逐步深入」，与事实不符——走查时只有
1 课。这句话属于把计划当现状宣传。

## 已覆盖的概念（有运行证据）

| 概念 | 教程位置 | 我的理解证明 |
|------|---------|-------------|
| `print()` 输出、`end` 参数、返回 `None` | L1 §1 | [L1 走查笔记](/walkthrough/l1) |
| 变量赋值、f-string、`=` 是绑定不是相等 | L1 §2 | 同上 |
| `#` 注释与三引号字符串的区别 | L1 §3 | 同上 |
| 单层拆包、右侧任意可迭代对象 | unpack §一 | [拆包断言核对](/walkthrough/unpack) |
| 多层嵌套拆包 | unpack §二 | 同上 |
| 星号收集 `*rest` | unpack §六 | 同上 |
| int / float / complex、进制字面量、`//` 与 `%` 的符号规则 | `examples/number/` | [L2 走查笔记](/walkthrough/l2-types) |
| 字符串字面量、转义、r-string、索引与切片越界行为 | `examples/string/` | 同上 |
| 列表增删改查、原地方法返回 `None`、`[x]*n` 引用复制 | `examples/list/` | 同上 |
| 字典字面量、`in` 看键、`items()` 动态视图 | `examples/map/` | 同上 |
| 列表推导式（map / filter / else / 嵌套） | `examples/comprehension/` | 同上 |
| for / while / if-elif-else / break / continue | `examples/statement/` | [L3 走查笔记](/walkthrough/l3-flow) |
| `for/else` 与 `try/except/else/finally` 执行序 | `examples/statement/` | 同上 |
| def / return / 默认参数（含可变默认参数坑） | `examples/function/` | [L4 走查笔记](/walkthrough/l4-function) |
| 关键字实参、`*args`、`**kwargs` | `examples/function/` | 同上 |
| `class` / `__init__` / `self` / 属性遮蔽 | `examples/class/` | [L5 走查笔记](/walkthrough/l5-class) |
| 方法绑定（实例取 vs 类取）、继承与 `super()` | `examples/class/` | 同上 |
| `__doc__`、`__class__`、类体定义时执行 | `examples/class/` | 同上 |
| os.path / 字符串方法 / 闭包 / 函数属性 | `examples/api/`、`_draft/` | [examples 全量清单](/walkthrough/examples-audit) |

## 未覆盖（内容不存在，无法走查）

**L6–L15 的页面全部不存在**，磁盘上也没有对应素材：

| 课 | 计划内容 | 素材情况 |
|----|---------|---------|
| L6 | 异步编程 asyncio | `examples/` 下 0 个文件 |
| L7 | HTTP 与 API 调用（httpx） | 0 个（`api/os.py` 只是本地路径操作） |
| L8 | 数据处理（Pydantic） | 0 个 |
| L9–L15 | Tool Use / Prompt / Chain / Memory / 实战 | 0 个 |

按 careers 要求优先级最高的是 L6 asyncio、L7 HTTP/API——详见
[careers 对齐](/walkthrough/careers)。

## 走查中修掉的问题

**36 项**（D-01 至 D-36），其中 **35 项已修**，1 项记录待决（D-33：
两个 `_draft/` 文件名与内容不符，改名属内容规划决策）。

| 来源 | 条目 | 已修 |
|------|------|------|
| 第一轮（教程页正文） | D-01 – D-15 中的 13 项 | 13 |
| 第二轮（补齐漏掉的表格与三行） | D-16 – D-18 | 3 |
| 第三轮（`examples/` 66 个文件 + 门禁自身 + 仓库卫生） | D-19 – D-36 | 17（D-33 待决） |
| **合计** | **36** | **35** |

按性质分（一项只归一类）：

| 类别 | 数量 |
|------|------|
| 教程/示例内容与 Python 实际行为不符 | 8 |
| 交互块不可运行（伪代码/标注符号/缺依赖被当 Python 执行） | 11 |
| 死链 / 链接指错 | 2 |
| 界面文案与文档指引不一致 | 1 |
| 死代码 + 语法错误 | 3 |
| examples 代码语法错误 | 1 |
| 术语不精确 / 注释词不达意 | 6 |
| 反模式未覆盖（可变默认参数、内建遮蔽、裸 except 等） | 2 |
| 门禁自身失效 / gitignore 失效 | 2 |

明细见 [发现的问题](/walkthrough/defects)。

> 走查做了三轮：第一轮覆盖 4 个教程页的正文，漏掉了 `begin.md` 的
> 「Python 模块导入语法」「对比 Python 内置数据类型」两张表和
> `unpack.md` 第八节的三行；第二轮补齐时又抓出 D-16 / D-17 / D-18。
> 第三轮把 `examples/` 66 个文件逐条核对，抓出 D-19 至 D-36 共 18 项。
> 漏掉的原因是我按「段落」而不是按「文档里的每一张表、每一个标题」
> 盘点覆盖面——已改为按 section header 逐条核对。
