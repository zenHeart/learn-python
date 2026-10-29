# Python 后端基础：从函数到可交付服务

本章只保留 Agent 岗位和后端交付会用到的 Python 能力。

## 能力链

```
数据模型
→ 输入校验
→ 业务函数
→ 异步边界
→ HTTP API
→ 持久化适配器
→ 测试与可观测性
→ Docker/CI
```

每一层都必须能独立测试。先用标准库 fixture 理解机制，再接入 FastAPI、Pydantic、数据库和真实模型服务。

## JS/TS 到 Python 的迁移重点

| 已有经验 | Python 目标能力 | 关键差异 |
| --- | --- | --- |
| TypeScript interface | dataclass / Pydantic model | 注解不会自动做运行时校验 |
| Promise | coroutine / TaskGroup | 取消、超时和阻塞调用必须明确 |
| Express middleware | FastAPI dependency | 依赖解析和请求生命周期可测试 |
| Jest/Vitest | pytest | fixture、参数化和退出码进入交付门禁 |
| JSON API | typed request/response | 错误 code、trace id 和版本必须稳定 |
| state machine | checkpoint / recovery | 重试前先读取外部状态 |

## 通过标准

- 能从新起点写出一个带输入校验的 API；
- 能覆盖成功、非法输入、超时、重复请求和依赖失败；
- 能解释哪些调用可重试，哪些副作用必须人工确认；
- 能写出一份运行命令、依赖版本、故障处理和选型说明；
- 能把同一接口迁移到新的存储适配器而不改变调用方契约。

浏览器中的 Pyodide 只能证明纯 Python 练习。涉及网络、数据库、进程、FastAPI 或 Docker 的任务必须在隔离沙箱或本机运行。
