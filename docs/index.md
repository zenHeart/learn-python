---
layout: home

hero:
  name: "learn-python"
  text: "交互式 Python 学习站"
  tagline: "边学边练，真正掌握 Python 与 Agent 开发能力"
  actions:
    - theme: brand
      text: 开始学习 →
      link: /tutorial/begin
    - theme: alt
      text: 查看学习路径
      link: /progress

features:
  - icon: 🐍
    title: 浏览器端运行 Python
    details: 无需安装任何环境，点击即可运行真实 Python 代码

  - icon: 📚
    title: 循序渐进
    details: 路线从基础语法到 Agent 开发共 15 课，按 L1–L15 计划逐步上线（当前已上线 L1）

  - icon: 💻
    title: 边学边练
    details: 每课配套可运行代码，当场验证掌握程度
---

## 为什么做这个站？

学习 Python 最常见的问题是：**看懂了，但不会写**。

这个站的设计目标是让你**学完就能用**——每个概念配套可运行的代码，敲一遍比看十遍印象更深。

## 学习路径

> 下面是**课程计划**，不是已完成清单。当前只上线了第 1 课，
> 每上一课会同步更新这张表和 [学习进度](/progress)。

1. **基础** — Python 语法、数据类型、控制流、函数、类（L1–L5）
2. **进阶** — 异步编程、HTTP 调用、数据处理（L6–L8）
3. **Agent 专项** — Tool Use、Prompt 工程、Chain 编排、Memory 管理（L9–L12）
4. **实战** — 单文件 Agent、多工具编排、自主决策（L13–L15）

## 如何找到已有素材？

`examples/` 目录下有 **66** 个可运行的 Python 示例（数字、字符串、列表、字典、
推导式、控制流、函数、类），目前大部分还没有被课程页面引用。
走查记录见 [学习走查](/walkthrough/) 的
[examples 全量走查清单](/walkthrough/examples-audit)。

## 如何使用？

1. 点击「开始学习」进入第一章
2. 阅读概念和示例代码
3. 点击代码块右上角的「▶ 运行」按钮，查看代码执行结果
4. 修改代码，尝试不同的写法

```python
# 试试修改下面的代码，然后点击运行
name = "Python"
print(f"Hello, {name}! Welcome to learn-python.")
```
