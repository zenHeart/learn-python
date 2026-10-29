# Knowledge Base Agent Fixture

这是一个无外部依赖的可重复教学 fixture，对应 `curriculum.json` 中的 `knowledge-base-agent-delivery`。

## 运行

```bash
python app.py query "测试环境为什么不能使用生产数据？"
python app.py eval
```

## 证据边界

- 语料只使用合成内容；
- 检索器是教学实现，不代表生产向量数据库；
- `get_doc` 是只读白名单工具；
- 找不到证据时返回拒答；
- 评测命令返回非零退出码表示回归门禁失败。

下一步练习：注入错误的 `tool_call_id`、越权角色、重复工具调用和指标下降，记录每个故障的信号、根因、修复和回归证据。
