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

`docs/` 下 Markdown 文件共 **6** 个：

| 文件 | 路由 | 类型 | 走查状态 |
|------|------|------|---------|
| `docs/index.md` | `/` | 首页 hero | ✅ 已走查 |
| `docs/progress.md` | `/progress` | 学习进度页 | ✅ 已走查 |
| `docs/tutorial/begin.md` | `/tutorial/begin` | L1 教程 | ✅ 已走查 |
| `docs/tutorial/annotation.md` | `/tutorial/annotation` | 标注规范 | ✅ 已走查 |
| `docs/tutorial/gaps.md` | `/tutorial/gaps` | 知识盲点清单 | ✅ 已走查 |
| `docs/tutorial/unpack.md` | `/tutorial/unpack` | 拆包完全指南 | ✅ 已走查 |

`examples/` 下 Python 文件共 **67** 个（`find examples -name '*.py' | wc -l`），
但**只有 `examples/mnist/` 被教程引用过一次**，其余 66 个与课程零关联。

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
| `for/else`、`try/except/else/finally` | examples/statement/ | [练习证据](/walkthrough/evidence) |

## 未覆盖（内容不存在，无法走查）

L2–L15 全部。按 careers 要求，其中优先级最高的是：
L2 数据类型、L4 函数、L6 asyncio、L7 HTTP/API——详见
[careers 对齐](/walkthrough/careers)。

## 走查中修掉的问题

18 项，全部有证据。分类统计：

| 类别 | 数量 |
|------|------|
| 教程内容错误（结论与 Python 实际行为不符） | 2 |
| 交互块不可运行（伪代码/标注符号/缺依赖被当 Python 执行） | 11 |
| 死链 / 链接指错 | 2 |
| 界面文案与文档指引不一致 | 1 |
| 死代码 + 语法错误 | 1 |
| examples 代码语法错误 | 1 |
| 术语不精确（「多行注释」「完整 BNF」） | 2 |
| 示例跑不通 / 类型规则未说 / 结论无验证手段 | 3 |

明细见 [发现的问题](/walkthrough/defects)。

> 走查做了两轮：第一轮覆盖 4 个教程页的正文，漏掉了 `begin.md` 的
> 「Python 模块导入语法」「对比 Python 内置数据类型」两张表和
> `unpack.md` 第八节的三行；第二轮补齐时又抓出 D-16 / D-17 / D-18。
> 漏掉的原因是我按「段落」而不是按「文档里的每一张表、每一个标题」
> 盘点覆盖面——已改为按 section header 逐条核对。
