---
title: 统一课程入口
description: 从 Python Agent 到 Java、Go、LLM 原理的岗位能力学习入口。
---

# 统一课程入口

这个站点是学习入口，不把四门课程拼成一条固定章节列表。先根据目标选择主线，再回到当前能力路径完成诊断、练习、调试、迁移和复测。

## 选择主线

| 目标 | 入口 | 终局作品 |
| --- | --- | --- |
| Python Agent / 后端 | [Python 能力路径](/learn-python/tutorial/learning-path) | 带 ACL、引用、工具、评测和恢复的 Python Agent |
| Java 后端 / 企业 Agent | [learn-java](https://github.com/zenHeart/learn-java#readme) | Java 知识库 Agent、工具审批、事务与治理 |
| Go Agent 平台 | [learn-engineering · Go 路径](https://github.com/zenHeart/learn-engineering/tree/main/docs/go) | Go 并发服务、检索、ToolRunner 与基础设施 |
| LLM 原理 | [learn-llm](https://github.com/zenHeart/learn-llm#readme) | 从 Python、数学、Transformer 到 RAG/Agent/Eval |
| 面试与作品验收 | [Career 能力矩阵](https://github.com/zenHeart/careers/tree/main/resume/2026/jobs/agents) | 可复核的项目、测试、失败样例和答辩证据 |

## 推荐顺序

以“前端工程师、Python 零基础、目标 Agent 应用岗位”为例：

1. [先做诊断](/learn-python/tutorial/diagnostic)，确认 Python、测试、后端和数据契约断点。
2. [Python 后端底座](/learn-python/tutorial/backend-foundation)，建立项目、类型、测试和 API 基础。
3. [Agent Loop](/learn-python/tutorial/agent-loop) 与 [检索链路](/learn-python/tutorial/retrieval-pipeline)。
4. [知识库 Agent](/learn-python/tutorial/knowledge-base-agent)，完成租户、角色、引用和拒答。
5. [Pi Agent Runtime](/learn-python/tutorial/pi-agent-runtime)，理解 Context、Skill、Tool、Hook、Policy 和 Eval。
6. 进入 [learn-llm](https://github.com/zenHeart/learn-llm)，补齐模型、Attention、Transformer、RAG 和评测原理。
7. 根据岗位需要迁移到 [Java](https://github.com/zenHeart/learn-java) 或 [Go](https://github.com/zenHeart/learn-engineering/tree/main/docs/go)。
8. 用 [evals](https://github.com/zenHeart/evals/tree/main/data/eval-specs) 和 [web-interview](https://github.com/zenHeart/web-interview) 验收作品与面试表达。

## 同一套验收标准

每条主线都要留下五类证据：

- **Explain**：能解释机制、不变量、边界和取舍；
- **Perform**：从空目录完成最小任务；
- **Debug**：修复故意注入的 ACL、引用、工具或恢复故障；
- **Transfer**：替换数据源、语言、工具或业务约束后仍能工作；
- **Retain**：延迟复测时无提示重建关键链路。

阅读章节、复制代码、浏览器示例通过都不能单独标记为 mastered。统一计划、诊断和路线合同由 [Workflow Learning Coach](https://github.com/zenHeart/workflow/tree/master/ai-assets/presets/content/agents) 维护。

## 课程边界

公开站点只使用合成或公开资料。真实模型、企业数据、凭据和生产副作用必须留在授权的 sandbox/local 环境；当前站点展示的是课程内容与计划快照，学习尝试、提示依赖、测试输出和作品引用应写入私有 learner events。

PDF/EPUB 导出应复用同一份 versioned learning pack，并携带来源 commit、未核验项、生成时间和答案隔离状态。统一评测证据格式见 [learning-agent-v1](https://github.com/zenHeart/evals/tree/main/data/eval-specs)。

## 继续学习

- [能力路径](/learn-python/tutorial/learning-path)
- [诊断与掌握](/learn-python/tutorial/diagnostic)
- [知识盲点](/learn-python/tutorial/gaps)
- [Python 进度](/learn-python/progress)
- [统一 Learning OS 门户](https://learn.zenheart.site/learning-os/)
