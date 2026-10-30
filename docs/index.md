---
layout: home

hero:
  name: "learn-python"
  text: "从 Python 基础到可交付 Agent"
  tagline: "以岗位能力、真实知识库场景、故障调试和评测证据组织学习"
  actions:
    - theme: brand
      text: 开始诊断 →
      link: /tutorial/diagnostic
    - theme: alt
      text: 查看能力路径
      link: /tutorial/learning-path

features:
  - icon: 🧭
    title: 能力图谱驱动
    details: 先定义岗位终局和真实作品，再按表现裁剪路线

  - icon: 🧪
    title: 练习与故障注入
    details: 每个节点都有独立实现、调试、迁移和延迟复测

  - icon: 🤖
    title: 真实 Agent 场景
    details: 从工具调用、知识库检索到权限、恢复和评测门禁

  - icon: 🧰
    title: 三种执行环境
    details: 浏览器、隔离沙箱和本地项目分别承担不同验收责任
---

## 学习目标

完成课程后，你应能从空目录交付一个 Python Agent 服务：

- 用数据模型和运行时校验约束外部输入；
- 用异步、HTTP、FastAPI 和测试构建后端；
- 实现 Tool Calling、知识库检索、引用和拒答；
- 处理超时、重试、幂等、权限和人工确认；
- 用评测集、trace、成本和延迟判断版本是否回归。

## 统一课程入口

需要同时学习 Python、Java、Go 和 LLM 原理时，先打开[统一课程入口](./tutorial/course-portal.md)。它按岗位目标组织主线和迁移顺序，并保留每门课程自己的能力合同、练习和验收。

## 推荐入口

1. [先做诊断](./tutorial/diagnostic.md)，不要用自评跳过能力节点；
2. [阅读能力路径](./tutorial/learning-path.md)，理解主线和可选分支；
3. [从 Python 后端底座开始](./tutorial/backend-foundation.md)；
4. [完成知识库 Agent 案例](./tutorial/knowledge-base-agent.md)；
5. 再根据目标进入 Agent 应用、后端交付或 [LLM 原理课程](https://github.com/zenHeart/learn-llm)；需要 Java/Go 平台能力时进入[跨语言课程入口](./tutorial/course-portal.md)。

~~~python
# 浏览器练习只用于理解纯 Python 机制
def answer_or_refuse(evidence):
    if not evidence:
        return {"status": "refused", "reason": "no evidence"}
    return {"status": "answered", "citations": evidence}
~~~
