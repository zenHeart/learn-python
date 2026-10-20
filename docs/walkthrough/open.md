# 未解决与恢复点

## 总体状态

**active**（不是 achieved）

理由：**已存在的章节和练习全部有证据**——6 个文档页 + 66 个示例 +
走查笔记新增的 5 页都有逐概念理解证明，256 条断言全 PASS；
但课程计划 15 课只写出了 **1** 个页面，L2–L15 的**页面**不存在，
学习路径仍然断裂。按验收标准「只有所有实际存在的章节和练习都有证据
才报告 achieved」——实际存在的确实都有证据了；但课程作为学习路径没通，
所以报 active 并明确恢复点。

## 覆盖数

| 项 | 已覆盖 / 实际存在 |
|----|-----------------|
| 文档页 | 6 / 6（另有走查笔记 13 页，本轮新增 5 页） |
| 教程课页面 | 1 / 15（L2–L15 页面不存在） |
| examples 文件 | 66 / 66（58 直接通过，7 需交互 stdin，1 需 `-m` 调用） |
| 教程断言 | 300 / 300 PASS（拆包 22 + 概念 22 + examples 256） |
| 缺陷 | 36 项记录，35 项已修（D-33 待决） |
| 浏览器交互块 | 33 / 33（上轮实测 0 非预期报错；**本轮未复跑**，MCP 连接失败） |
| careers 要求映射 | 已映射，缺口已列 |

## 走查轮次

- **第一轮**：覆盖 4 个教程页的正文段落。漏掉 `begin.md` 的两张表格和
  `unpack.md` 第八节的三行——因为我是按「段落」而不是按「文档里每一张表、
  每一个标题」盘点的。
- **第二轮**：按 section header 逐条核对后补齐，又抓出 D-16 / D-17 / D-18。
- **第三轮（本轮）**：把 `examples/` 66 个文件逐条核对，抓出 D-19 至 D-34。
  教训有两条：
  1. 盘点覆盖面要用结构（标题、表格、代码块计数），不能用阅读印象；
  2. **笔记自己声称的数字也要用 `find` / `wc -l` 实测**——
     本轮发现上一版笔记把 `number/` 写成 6 个（实际 3）、
     `list/` 和 `function/` 各写成 7（实际 6）、L2 范围合计声称 27（实际 24）。
     估算数字直接导致差点漏掉一整个目录（D-34）。

## 恢复点（下次从哪继续）

**L2–L5 的素材已经走查完毕并有证据，缺的是把它们写成课程页面。**
所以真正的恢复点是：

1. **写 `docs/tutorial/types.md`（L2）**——素材和走查结论都是现成的：
   [L2 走查笔记](/walkthrough/l2-types) 已经把 24 个示例的概念、
   符号表、预测/运行差异、反例都整理好了，按它誊写成教程页即可，
   不需要再从零设计。誊写时把 `python` 块限定为「自包含可运行」的片段
   （`input()` 相关的用 `text`，浏览器没有 stdin）。
2. **同样处理 L3 / L4 / L5**：对应
   [l3-flow](/walkthrough/l3-flow)、[l4-function](/walkthrough/l4-function)、
   [l5-class](/walkthrough/l5-class)。
3. **L6 起没有素材**，需要先写示例再写课（见 careers 对齐的优先级）。

第 1、2 步不依赖任何人，走查产物可以直接当输入。

## 未核验 / 未修项

| # | 项 | 为什么没做 |
|---|----|-----------|
| O-01 | D-15：首页宣称「15 节课」与事实不符 | **本轮已修**：feature 卡改成「路线共 15 课，按计划逐步上线（当前已上线 L1）」，正文补「这是课程计划，不是已完成清单」 |
| O-02 | `docs/.vitepress/cache/` 已被 git 跟踪，dev server 反复弄脏工作区 | **本轮已修 `.gitignore`**（D-36：`.vitepress/cache` 带斜杠锚定根目录，匹配不到 `docs/` 下的真实路径，所以从未生效）。但已跟踪的 12 个文件仍未 `git rm --cached`——那是仓库级变更，留给维护者确认 |
| O-03 | Pyodide 二进制重复两份（38M）+ dist 里再各一份 | 涉及部署路径（dev 用 `/pyodide/`，prod 用 `/learn-python/pyodide/`），改动会影响线上，需确认 |
| O-04 | Pyodide 在 dev 下被加载两次（CDN + 本地） | **本轮修正归因并删掉死代码**：`theme/client.js` 是从未进 bundle 的死代码（构建产物里只有 `index.js` 的中文文案，app 入口也不引用它），已删除（D-35）。真正的两次注入来自 `config.js` 的 `head`（dev 用 CDN）和 `theme/index.js`（dev 用本地 `/pyodide/`）。删掉 client.js **不减少**加载次数；要真正去掉重复得改这两个之一，但那会动 dev/prod 两条路径的运行时行为，需在浏览器里验证后才能做 |
| O-05 | `docs/public/learn-python/pyodide-init.js` 是失联的老版本运行时 | 无引用，可删；但它是「修复 stdout 捕获之前」的唯一物证，留着有考古价值，交由维护者决定 |
| O-06 | 两个部署 workflow（`main.yml` + `deploy.yml`）同时部署 GitHub Pages | 需确认哪一个才是权威，删另一个。属于发布配置，超出走查范围 |
| O-07 | `unpack.html` 两个「错误演示」块把完整 traceback 铺开 | 对初学者是噪音。可只显示最后一行 `ValueError: ...`。属体验优化，不影响学习能否继续 |
| O-08 | 站点没有 pytest / 单元测试 | 本轮已把三个断言门禁 + 链接门禁全部接进 `npm run check`；但**浏览器交互块仍未接 CI**（需要 dev server + Playwright），接入需确认是否允许改 CI |
| O-09 | `examples/` 下 65 个文件与课程零关联 | **本轮部分推进**：已在首页和 `progress.md` 指向走查清单，让学习者知道素材存在；但「补教程引用」仍是内容规划决策。`_draft/` 两个文件名与内容不符（D-33）也未改名 |
| O-10 | careers 三份文件对 Python 自评不一致（未学/了解/弱） | careers 是只读的外部目录，本次不得修改，只记录观察 |
| O-11 | README 的 13 条外部学习路径在 `docs/` 里零引用 | 走查者从站内页面无法知道它们存在，也没有「学 L1 前要不要先看官方 tutorial」的说明。README 的自报进度与 `progress.md` 的课表是两套独立口径。属于内容规划决策，未改 |
| O-12 | `progress.md` 课表与 README 学习路径口径不一致 | 同上，需维护者统一 |
| O-13 | `docs/tutorial/gaps.md` 宣称「点击标签筛选 / `?tag=` 分享」但没有任何筛选实现 | **本轮已修**：页首改成明说「计划中的交互，尚未实现，站点当前没有筛选脚本」，并把走查记到的 34 条困惑列成表指向各笔记页。真正的筛选实现属于功能开发，未做 |
| O-16 | `theme/client.js` 已删，但 `config.js` 与 `theme/index.js` 仍各注入一次 Pyodide | 见 O-04。改动会影响 dev/prod 运行时，需浏览器验证 |
| O-14 | 走查记到的 34 条困惑没有归档进 `gaps.md` 的 ❓ 清单 | 手工誊一份即可，但本页计数与各笔记条数要一致；属维护动作，未做 |
| O-15 | 12 条跨示例反模式里 8 条「无示例覆盖」 | 写 L2–L5 页面时应把这 8 条各配一个可运行反例（可变默认参数、`[x]*n` 引用复制、`round` 银行家舍入、`bool` 是 int 子类、`and/or` 返回操作数、`str+int` 报错、`nan` 自不等、负数取模）。清单见 [examples 全量清单](/walkthrough/examples-audit) |

## 门禁状态

| 门禁 | 命令 | 结果 |
|------|------|------|
| 文档构建 | `npm run docs:build` | ✅ 通过 |
| 链接（含 frontmatter） | `node .walkthrough/check-links.js` | ✅ 通过（含反向验证） |
| 拆包断言 | `python .walkthrough/evidence/unpack-claims-audit.py` | ✅ 22 PASS |
| 概念断言 | `python .walkthrough/evidence/concepts-round2-audit.py` | ✅ 22 PASS |
| examples 断言 | `python .walkthrough/evidence/examples-claims-audit.py` | ✅ 256 PASS（含反向验证） |
| examples 运行 | `bash .walkthrough/run-all.sh` | ✅ 58 通过 / 8 需交互或特定调用 |
| 浏览器交互块 | Playwright 逐块点击 | ⚠️ 上轮 33/33；**本轮未复跑** |

## 明确不做的事

- 不 push、不 merge、不 deploy、不删除外部资源。
- 不修改 `careers`、`workflow`、`zen`。
- 不写原始思维链或凭据到任何提交里。
