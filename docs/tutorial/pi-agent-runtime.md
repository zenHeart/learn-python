# Pi Agent Runtime 定制化

本页定义把知识库 Agent 推进为可复用 Agent Runtime 的练习合同，让 Context、Skill、Tool、Hook/Policy 和 Eval 成为可版本化、可测试、可回滚的系统资产。下方只有策略函数示例；完整 Loop、checkpoint、Skill 加载和真实 Pi 集成尚待学习者实现，案例保持 `not-run`。

## 运行链

~~~text
用户目标
→ Context 选择与裁剪
→ Skill 路由
→ Tool schema 与权限检查
→ 执行前 Hook/Policy 与必要人工批准
→ Agent Loop 中的工具执行（每次调用重新检查）
→ 执行后结果验证与审计
→ 结果、引用、trace
→ Eval 与版本比较
→ 资产沉淀或回滚
~~~

## 五层合同

| 层 | 负责什么 | 最小验收 |
| --- | --- | --- |
| Context | 系统规则、项目规则、任务、画像、来源和上下文预算 | 替换一条约束后能解释保留和丢弃 |
| Skill | 触发条件、步骤、工具允许列表、输出和失败处理 | 新增 Skill 不改核心 Loop |
| Tool | 输入/输出 schema、权限、超时、重试、幂等、审计 | 非法参数和越权调用失败 |
| Hook/Policy | 隐私、权限、来源、成本、完成证据和人工确认 | 高影响动作未批准时停止 |
| Eval | Golden、BadCase、轨迹、指标、版本对比和回滚 | 改动后报告退化样本 |

## Python 教学实现

先用标准库实现可确定复现的 Runtime：

~~~python
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class ToolSpec:
    name: str
    handler: Callable
    read_only: bool
    requires_approval: bool

def can_run(tool: ToolSpec, approved: bool) -> bool:
    return approved or (tool.read_only and not tool.requires_approval)
~~~

`ToolSpec` 来自可信工具注册表，`approved` 来自绑定本次工具、参数和身份的审批记录，不能使用模型自行声明的字段。写工具默认需要批准；显式要求审批的只读工具也必须等待批准。此函数只回答审批是否满足，调用前仍须独立通过身份、范围与参数检查；批准不覆盖其他拒绝条件。

然后把它迁移到真实模型、MCP、FastAPI 或 Pi 运行时。迁移时保持工具 schema、trace id、错误分类和评测集不变。

## 练习顺序

1. 注册一个只读知识检索工具；
2. 注册一个评测运行器；
3. 为工具增加 schema 和结构化错误；
4. 加入隐私扫描和来源检查 Hook；
5. 注入工具结果错配、超时和重复调用；
6. 用 Golden/BadCase 比较两个 Skill 版本；
7. 让运行中断后从 checkpoint 恢复；
8. 将知识库 Skill 迁移为 Workflow 任务执行 Skill。

## 真实业务迁移

可以把测试知识库迁移为以下脱敏工作流：

- 输入测试需求或回归问题；
- 读取测试规则、接口说明和历史异常；
- 选择检索、分析、报告或只读查询工具；
- 生成带来源的建议；
- 高影响动作保留人工确认；
- 保存执行 trace、失败分类和报告链接。

生产数据、用户凭据和真实业务副作用不进入课程 fixture。要证明系统具备岗位能力，必须同时展示工具合同、权限边界、故障注入、Eval 报告和回滚路径。

## 面试验收

候选人应能说明：

- 为什么 Context、Skill、Tool、Hook 要分层；
- 如何新增 Skill 而不修改核心运行时；
- 如何保证不同语言工具的错误、超时和 trace 语义一致；
- 如何防止模型伪造工具结果或完成状态；
- 如何把一次真实排障沉淀为 Golden/BadCase；
- 如何在上下文不足时安全停止。

## 迁移题

把知识库 Skill 迁移成 Workflow 任务 Skill：

~~~text
需求 → 规格 → 资源绑定 → 执行 → 证据 → 独立核验 → 人工验收
~~~

要求保持：

- 输入和输出合同；
- trace 和幂等键；
- 权限和人工确认；
- 失败分类和恢复；
- Eval 与回滚证据。

这一步把 Python Agent 能力连接到 Workflow、Career 和后续 Java/Go 实现。
