# 学习进度

> 边学边练，逐步掌握 Python 与 Agent 开发能力。

---

## 📊 站点建设

| 任务 | 状态 |
|------|------|
| VitePress + Pyodide 交互引擎 | ✅ 完成 |
| 浏览器端运行 Python | ✅ 完成 |
| Hello World 可运行页面 | ✅ 完成（L1 有 9 个可运行交互块，全部实测通过） |
| 教程结论回归门禁 | ✅ 完成（3 个 Python 断言脚本 + 1 个链接门禁，接进 `npm run check`） |
| 练习自动判定 | ⏳ 待开始（门禁校验的是**教程结论**，不是**学习者作答**） |
| 部署到 GitHub Pages | ✅ 已配置（`.github/workflows/main.yml` + `deploy.yml`；两个 workflow 并存，哪一个权威待确认） |

---

## 📚 学习路径

### 阶段 1：Python 基础

| 课 | 内容 | 状态 |
|----|------|------|
| L1 | Hello Python — print / 变量 / 注释 / 拆包 | ✅ 已完成（走查证据见 [/walkthrough/l1](/walkthrough/l1)） |
| L2 | 数据类型 — int / str / bool / list | ⏳ 页面未写；素材已在 `examples/`（走查见 [/walkthrough/l2-types](/walkthrough/l2-types)） |
| L3 | 控制流 — if / for / while | ⏳ 页面未写；素材已在 `examples/statement/`（走查见 [/walkthrough/l3-flow](/walkthrough/l3-flow)） |
| L4 | 函数 — def / 参数 / 返回值 | ⏳ 页面未写；素材已在 `examples/function/`（走查见 [/walkthrough/l4-function](/walkthrough/l4-function)） |
| L5 | 类 — class / 方法 / 继承 | ⏳ 页面未写；素材已在 `examples/class/`（走查见 [/walkthrough/l5-class](/walkthrough/l5-class)） |

### 阶段 2：Python 进阶

| 课 | 内容 | 状态 |
|----|------|------|
| L6 | 异步编程 asyncio | ⏳ 待开始 |
| L7 | HTTP 与 API 调用（httpx） | ⏳ 待开始 |
| L8 | 数据处理（Pydantic） | ⏳ 待开始 |

### 阶段 3：Agent 专项

| 课 | 内容 | 状态 |
|----|------|------|
| L9 | Tool Use / Function Calling | ⏳ 待开始 |
| L10 | Prompt 工程 | ⏳ 待开始 |
| L11 | Chain 编排 | ⏳ 待开始 |
| L12 | Memory 与上下文管理 | ⏳ 待开始 |

### 阶段 4：实战

| 课 | 内容 | 状态 |
|----|------|------|
| L13 | 单文件 Agent 示例 | ⏳ 待开始 |
| L14 | 多工具编排 | ⏳ 待开始 |
| L15 | 自主决策树 | ⏳ 待开始 |

---

## 👨‍🏫 学习记录

_每次学完一课，在此记录学习心得。_

### L1 — Hello Python

```python
# 第一个 Python 程序
name = "Python"
print(f"Hello, {name}!")
print("Welcome to learn-python!")
```

> 状态：✅ 已完成
> 掌握程度：print / 变量 / f-string / 注释与 docstring / 模块导入 5 种形式 /
> 4 种内置容器 / 单层与嵌套拆包 / 星号收集 —— 逐概念有「预测 → 运行 →
> 新例子 + 反例」证据，见 [L1 走查笔记](/walkthrough/l1)。

### L2–L5 — 素材已走查，页面未写

`examples/` 下 66 个示例已逐条核对（256 条断言），但课程页面还不存在，
所以不计入「已完成」。走查笔记：

| 课 | 走查笔记 |
|----|---------|
| L2 数据类型 | [/walkthrough/l2-types](/walkthrough/l2-types) |
| L3 控制流 | [/walkthrough/l3-flow](/walkthrough/l3-flow) |
| L4 函数 | [/walkthrough/l4-function](/walkthrough/l4-function) |
| L5 类 | [/walkthrough/l5-class](/walkthrough/l5-class) |

---

## 🎯 学习目标

完成本课程后，你将能够：

1. **熟练编写 Python 脚本** — 处理文件、数据、自动化任务
2. **理解异步编程** — 用 asyncio 构建高性能应用
3. **掌握 Agent 开发** — 调用 LLM API、编排工具、管理上下文
4. **独立开发 Agent 应用** — 从需求到实现，全程自主

---

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| 站点框架 | VitePress |
| 交互引擎 | Pyodide（浏览器端 Python 3.11）|
| 部署 | GitHub Pages |
| 仓库 | github.com/zenHeart/learn-python |

---

## 开始学习 →

[进入第 1 课：Hello Python](/tutorial/begin)