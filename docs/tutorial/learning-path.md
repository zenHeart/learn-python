# 能力路径：从 Python 到 Agent 岗位

本页解释课程如何按岗位终局组织，不把学习者锁在固定章节顺序中。完整能力、来源、角色和案例以仓库根目录 curriculum.json 为准。

## 三条路线

| 路线 | 适合目标 | 主要产物 |
| --- | --- | --- |
| Python Agent 应用 | 使用 LLM、工具、知识库和 API 交付业务 Agent | 知识库 Agent、工具协议、评测报告 |
| Python 后端 | 交付 API、异步任务、数据契约、持久化和部署 | 可测试的后端服务、Docker/CI |
| LLM 原理桥接 | 理解并手写自动微分、Attention、Transformer | clean-room 实现，转入 learn-llm |

三条路线共享 Python 核心、工程底座和数据契约。通过诊断后，已掌握节点从当前路线中裁剪，脆弱节点进入短修复任务。

## 主线顺序

~~~text
Python 核心
  → 工程环境与测试
  → 数据契约与运行时校验
  → 异步 / HTTP / SSE
  → FastAPI 后端
  → LLM API 与结构化输出
  → Tool Calling 与 Agent Loop
  → 知识库摄取、检索、引用和拒答
  → 权限、状态、恢复与 HITL
  → 评测、可观测性、成本和回归
  → Docker、CI、作品和面试表达
~~~

## 前端经验迁移

| 已有心智模型 | Python Agent 中的对应物 | 迁移时必须补的内容 |
| --- | --- | --- |
| TypeScript 类型 | 类型标注、dataclass、Pydantic | 类型标注本身不做运行时校验 |
| Promise / async | coroutine、TaskGroup、取消和超时 | 阻塞调用、异常聚合、资源释放 |
| Express 中间件 | FastAPI dependency | 生命周期、输入输出契约和测试 |
| Jest / Vitest | pytest fixtures、参数化和退出码 | 测试夹具、隔离和回归门禁 |
| 状态管理 | Agent checkpoint 和恢复 | 外部副作用、幂等键和未知结果 |
| API 调用 | Tool schema 与 MCP | 模型只提议，执行层负责安全 |

## 每个节点的最小交付

- 一次冷启动预测或检索；
- 一个最小可运行实现；
- 一个故障注入和调试任务；
- 一个条件变化后的迁移任务；
- 一份能说明机制、边界和取舍的短解释；
- 一次延迟复测。

完成课程页面不代表节点 mastered。状态由 learner events 中的 Explain、Perform、Debug、Transfer 和 Retain 证据共同决定。

## 建议的第一条纵向切片

先完成 examples/knowledge_base_agent：

1. 用标准库读取合成知识库；
2. 实现确定性检索；
3. 返回带引用的回答或拒答；
4. 加入只读工具和权限校验；
5. 跑 golden set 指标；
6. 注入一次工具错配和一次回归；
7. 写出故障复盘和迁移方案。

完成这个切片后，再替换检索器、LLM 适配器、FastAPI 接口和持久化层。这样每次增加框架都能保持同一份业务验收合同。

## LLM 原理桥接

`llm-clean-room-bridge` 从本仓库的 Python 工程能力出发，按以下顺序准备迁移证据：

1. 用 NumPy 表达批次、序列和特征维度，给矩阵乘法与广播写 shape 断言，并修复一个维度错误；
2. 手写最小标量自动微分，对加法、乘法和组合运算做有限差分对拍，保留失败与修复记录；
3. 实现最小 Attention 的打分、mask、归一化和输出，验证 shape 与被遮挡位置不会影响结果。

每个练习需要源码、可重复测试和无提示解释，不能以调用现成模型代替实现证据。完成后进入 [learn-llm 原理课程](https://github.com/zenHeart/learn-llm)，一周后从空接口重建关键函数。本页是迁移入口与验收合同，尚不提供这些练习的完成回执。
