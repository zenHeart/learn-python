# 学习进度

> 本页面记录课程建设状态。学习者掌握状态由 learner events 和验收证据推导，不由本页勾选决定。

## 课程资产

| 资产 | 状态 |
| --- | --- |
| 能力型 curriculum.json | ✅ 已建立 |
| 前端工程师 / Python 零基础画像 | ✅ 已建立 |
| Python Agent / 后端岗位路线 | ✅ 已建立 |
| 知识库 Agent 案例合同 | ✅ 已建立 |
| 诊断探针与五维掌握规则 | ✅ 已建立 |
| 浏览器 / 沙箱 / 本地执行模式 | ✅ 已建立 |
| 标准库知识库 Agent fixture | ✅ 已建立 |
| 统一 learning-pack 渲染器 | ⏳ 接入 learn 门户 |
| PDF / EPUB 个性化导出 | ⏳ 接入 book skill |
| learner-events 持久化与复习队列 | ⏳ 接入 learn runtime |

## 能力主线

| 阶段 | 关键能力 | 当前入口 |
| --- | --- | --- |
| A | Python 核心、数据模型、异常、模块 | [L1](./tutorial/begin.md) |
| B | 环境、测试、类型、日志、命令行 | [后端底座](./tutorial/backend-foundation.md) |
| C | async、HTTP、SSE、FastAPI、Pydantic | curriculum.json |
| D | LLM API、结构化输出、Tool Calling | [Agent Loop](./tutorial/agent-loop.md) |
| E | 摄取、切块、召回、引用、拒答 | [检索链路](./tutorial/retrieval-pipeline.md) |
| F | 权限、恢复、HITL、评测、可观测性 | [知识库 Agent](./tutorial/knowledge-base-agent.md) |
| G | Docker、CI、岗位表达和作品 | curriculum.json |
| H | 自动微分、Attention、Transformer | [learn-llm](https://github.com/zenHeart/learn-llm) |

## 课程验收

每个能力节点都需要分别记录：

- Explain：因果、不变量、边界和反例；
- Perform：新起点独立完成；
- Debug：故障注入后的定位和修复；
- Transfer：改变场景、工具或约束后的迁移；
- Retain：延迟复测。

完成页面阅读或浏览器运行只能作为学习活动证据，不能直接改为 mastered。
