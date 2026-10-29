# learn-python

面向 Python Agent、后端和知识库 Agent 岗位的能力型学习仓库。课程从 JavaScript/TypeScript 工程经验出发，以可运行作品、故障调试、评测门禁和延迟复测作为掌握证据。

## 课程终局

从空目录独立交付一个可测试、可观测、可恢复的 Python Agent 服务：

- 处理结构化输入并执行运行时校验；
- 调用 LLM、白名单工具和知识库；
- 返回带版本和权限边界的引用；
- 处理超时、重试、重复调用和人工确认；
- 用 golden set、recall@k、MRR、引用覆盖率和任务成功率做回归；
- 通过 Docker/CI 交付并能在面试中解释关键取舍。

课程完整能力合同见 [curriculum.json](./curriculum.json)，执行环境见 [execution-modes.json](./execution-modes.json)。

## 学习路径

1. [Python 核心与 JS 对照](./docs/tutorial/begin.md)
2. [Python 后端工程底座](./docs/tutorial/backend-foundation.md)
3. 异步、HTTP、数据契约与 API
4. [手写 Agent Loop 与工具调用](./docs/tutorial/agent-loop.md)
5. [检索链路与评测回归](./docs/tutorial/retrieval-pipeline.md)
6. [知识库 Agent 端到端案例](./docs/tutorial/knowledge-base-agent.md)
7. 状态恢复、权限、可观测性和部署
8. [LLM 原理桥接](https://github.com/zenHeart/learn-llm)

## 执行环境

- browser：Pyodide，只用于纯 Python 和确定性教学练习；
- sandbox：隔离 Python 环境，用于网络、API、检索、Agent 和故障注入；
- local：学习者本机，用于 Docker、CI、本地模型和真实项目。

浏览器代码可以帮助理解语法，但不能替代后端服务和 Agent 交付证据。课程 fixture 使用合成资料，不接入生产数据和真实凭据。

## 可运行案例

[examples/knowledge_base_agent](./examples/knowledge_base_agent) 是一个标准库即可运行的知识库 Agent fixture：

~~~bash
python examples/knowledge_base_agent/app.py query "测试执行能不能使用生产数据"
python examples/knowledge_base_agent/app.py eval
~~~

## 相关资产

- Workflow 学习技能：[learn](https://github.com/zenHeart/workflow/tree/master/ai-assets/presets/content/skills/learn)
- LLM 原理课程：[learn-llm](https://github.com/zenHeart/learn-llm)
- 课程门户：[learn.zenheart.site](https://learn.zenheart.site)
