---
title: 学习走查
description: 以初级前端工程师视角真实走查 learn-python 教程的过程记录，含章节状态、概念理解证明、练习证据、困惑与修复、careers 对齐
---

# 学习走查 / 学习笔记

> 这份笔记由一次**真实的用户视角走查**产生，不是课程大纲的复述。
> 走查者设定：高中数学基础 + 基础前端经验，会 JS 的 `console.log`，
> 没写过生产 Python。只把**实际运行过**的内容当作已掌握。

## 怎么读这份笔记

| 页面 | 内容 |
|------|------|
| [覆盖总账](/walkthrough/coverage) | 课程真实存在多少内容、走了多少、卡在哪 |
| [L1 走查笔记](/walkthrough/l1) | 逐个概念的理解证明：预测 → 运行 → 新例子 + 反例 |
| [拆包断言核对](/walkthrough/unpack) | 把 `unpack.md` 的 22 条结论写成可执行断言 |
| [练习证据](/walkthrough/evidence) | 每个练习的真实命令与输出，含复现方式 |
| [发现的问题](/walkthrough/defects) | 走查中发现的缺陷、修复状态与证据 |
| [careers 对齐](/walkthrough/careers) | 岗位要求 → 课程章节 → 我的薄弱项 |
| [未解决与恢复点](/walkthrough/open) | 当前 blocked 在哪、下一步从哪继续 |

## 走查方法（可复现）

1. **先盘家底**：只认磁盘上真实存在的章节，不把 README / progress.md 的
   计划当作已写好的内容。
2. **每个概念过四问**：
   - 我当前已知的前置知识是什么？
   - 逐个符号、类型、公式、代码每一部分怎么解释？
   - 先预测再运行，预测错了就记下来。
   - 用一个**新例子**和一个**反例**证明理解，然后回答「怎样证明我理解了」。
3. **每个练习真跑**：命令行练习存命令 + 输出；浏览器/Pyodide 练习真实
   点击「▶ 运行」按钮读输出区，不用静态检查冒充完成。
4. **教程的每条结论都要核对**：把教程声称的结果写成断言，让 Python 自己
   判 TRUE/FALSE。
5. **遇到问题停住**：逻辑跳跃、术语未定义、数学前置不足、顺序错误、
   代码/文档不一致、缺练习——记录下来，做最小修复，然后回到原困惑点
   重新学。不越过未解决点。

## 证据存放

原始证据在仓库 `.walkthrough/evidence/`，可用一条命令复现：

```bash
bash .walkthrough/run-all.sh          # 命令行证据 + 断言门禁
node .walkthrough/check-links.js      # 链接门禁（需先 docs:build）
```

浏览器/Pyodide 证据的复跑步骤记录在
`.walkthrough/evidence/browser-podide-runs.md`。

## 当前状态

**active** —— 已存在的 4 个教程页 + 1 个首页全部走完并有证据，
但课程计划 15 课只写出了 1 课，剩余 14 课不存在，无法走查。
详见 [覆盖总账](/walkthrough/coverage) 与 [未解决与恢复点](/walkthrough/open)。
