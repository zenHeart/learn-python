# Knowledge Base Agent Fixture

这是一个无外部依赖的可重复教学 fixture，对应 curriculum.json 中的 knowledge-base-agent-delivery。

当前实现词元重叠检索、ACL、文档 ID/版本引用、拒答和离线门禁。回答只列候选证据；尚未实现 LLM、MCP、完整工具循环或业务服务，不能据此判定整个 capstone 已完成。

## 运行

~~~bash
cd examples/knowledge_base_agent
python app.py query "测试执行为什么不能使用生产数据？"
python app.py eval
python -m unittest -v test_app.py
~~~

## 证据边界

- 语料只使用合成内容；
- 每个文档包含 tenant 和 allowed_roles；
- rank 在排序前执行 ACL 过滤，get_doc 再次校验权限；
- 找不到证据或无权访问证据时返回拒答；
- eval 检查实际 answer 的引用，输出 hit_rate、recall_at_3、MRR、permission_pass_rate、citation_coverage 和 status_pass_rate；
- citation_coverage 是正向问题中返回非空、唯一、授权且版本匹配引用的比例，不衡量自然语言答案的事实支持性；
- unittest 覆盖召回前 ACL、直接读取与嵌套对象隔离、非法 top_k、引用版本、审批示例和真实 CLI 退化退出码；
- 检索器是教学实现，不代表生产向量数据库；
- 评测命令返回非零退出码表示回归门禁失败。

固定门禁要求至少 8 条 query，包含正常回答与角色/租户越权拒答；MRR 至少 0.9，其余指标均为 1.0。指标按未舍入值判定，报告保留三位小数。退出码 0 表示通过、1 表示指标或覆盖范围不达标、2 表示评测输入无效。当前 8 条固定题只是教学基线，不能代表生产质量。

下一步练习：注入错误的 tool_call_id、重复工具调用和指标下降，记录每个故障的信号、根因、修复和回归证据。
