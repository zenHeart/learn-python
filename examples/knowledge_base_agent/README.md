# Knowledge Base Agent Fixture

这是一个无外部依赖的可重复教学 fixture，对应 curriculum.json 中的 knowledge-base-agent-delivery。它分成两个证据层：检索/ACL/引用门禁，以及可恢复的 typed tool Agent Loop。

当前实现词元重叠检索、ACL、文档 ID/版本引用、拒答、typed tool、tool_call_id 对齐、最大步数、审批门、幂等重放、超时停止和离线评测。它仍然不包含真实 LLM、MCP、数据库或网络服务，不能据此判定生产 capstone 已完成。

## 运行

~~~bash
cd examples/knowledge_base_agent
python app.py query "测试执行为什么不能使用生产数据？"
python app.py eval
python -m unittest -v test_app.py test_agent_runtime.py
~~~

## 运行时合同

agent_runtime.py 只接受结构化 ToolCall：

- id 必须存在，工具结果必须回填同一个 tool_call_id；
- 工具名称和参数必须通过 ToolRegistry，未知工具或非对象参数直接失败；
- max_steps 防止模型无限循环；
- 写工具必须同时声明 read_only=false 和 requires_approval=true；注册时拒绝绕过审批的副作用工具，未批准时不会执行 handler；
- 相同 idempotency_key 只执行一次，后续请求返回 replayed=true；
- 工具超过 deadline 会返回 timeout 并停止当前运行；
- failed、timeout、approval_required 都是停机状态，不能被模型自述覆盖；
- timeout 后线程池不会等待 handler；真实服务必须使用可取消的下游 context、幂等键和 durable state，线程取消不等于副作用已取消。

## 证据边界

- 语料只使用合成内容；
- 每个文档包含 tenant 和 allowed_roles；
- rank 在排序前执行 ACL 过滤，get_doc 再次校验权限；
- 找不到证据或无权访问证据时返回拒答；
- eval 检查实际 answer 的引用，输出 hit_rate、recall_at_3、MRR、permission_pass_rate、citation_coverage 和 status_pass_rate；
- citation_coverage 是正向问题中返回非空、唯一、授权且版本匹配引用的比例，不衡量自然语言答案的事实支持性；
- unittest 覆盖召回前 ACL、直接读取与嵌套对象隔离、非法 top_k、引用版本、审批示例、工具循环和真实 CLI 退化退出码；
- 检索器和 Agent runtime 是教学实现，不代表生产向量数据库或完整服务；
- 评测命令返回非零退出码表示回归门禁失败。

固定门禁要求至少 8 条 query，包含正常回答与角色/租户越权拒答；MRR 至少 0.9，其余指标均为 1.0。指标按未舍入值判定，报告保留三位小数。退出码 0 表示通过、1 表示指标或覆盖范围不达标、2 表示评测输入无效。当前固定题只是教学基线，不能代表生产质量。

下一步练习：把 ToolSpec 迁移为真实 MCP schema，增加持久化 checkpoint、下游状态查询和故障恢复，然后把同一组 golden/BadCase 迁移到 FastAPI 或银行测试环境 mock。
