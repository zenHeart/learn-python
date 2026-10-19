# 未解决与恢复点

## 总体状态

**active**（不是 achieved）

理由：**已存在的章节和练习全部有证据**，但课程计划 15 课只写出 1 课，
剩余 14 课在磁盘上不存在，无法走查。按验收标准「只有所有实际存在的章节
和练习都有证据才报告 achieved」——已存在的 6 个页面 + 67 个示例 +
20 个交互块确实都有证据；但课程作为学习路径是断裂的，
所以报 active 并明确恢复点。

## 覆盖数

| 项 | 已覆盖 / 实际存在 |
|----|-----------------|
| 文档页 | 6 / 6 |
| 教程课 | 1 / 15（L2–L15 不存在） |
| examples 文件 | 67 / 67（61 直接通过，5 需交互 stdin，1 需 `-m` 调用） |
| 浏览器交互块 | 33 / 33（0 个非预期报错） |
| 教程断言 | 44 / 44 PASS（拆包 22 + 概念 22） |
| careers 要求映射 | 已映射，缺口已列 |

## 走查轮次

- **第一轮**：覆盖 4 个教程页的正文段落。漏掉 `begin.md` 的两张表格和
  `unpack.md` 第八节的三行——因为我是按「段落」而不是按「文档里每一张表、
  每一个标题」盘点的。
- **第二轮**：按 section header 逐条核对后补齐，又抓出 D-16 / D-17 / D-18。
  教训：盘点覆盖面要用结构（标题、表格、代码块计数），不能用阅读印象。

## 恢复点（下次从哪继续）

**从 L2 数据类型开始**，但 L2 页面不存在，所以真正的恢复点是：

1. **等 L2 写出来**，或
2. **先按现有材料自学 L2**：`examples/number/`（6 个文件）、
   `examples/string/`（7 个）、`examples/list/`（7 个）、`examples/map/`（5 个）、
   `examples/comprehension/`（2 个）已经在磁盘上，只是没被教程引用。
   这些足以覆盖 progress.md 里 L2 的「int / str / bool / list」范围。

第 2 条是可行的下一步，且不依赖别人写课。走查时已确认这 27 个文件全部
能直接运行通过（见 [练习证据](/walkthrough/evidence)）。

## 未核验 / 未修项

| # | 项 | 为什么没做 |
|---|----|-----------|
| O-01 | D-15：首页宣称「15 节课」与事实不符 | 要么删表述要么把课写出来。写课超出走查范围，需人决策 |
| O-02 | `docs/.vitepress/cache/` 已被 git 跟踪，dev server 反复弄脏工作区 | 取消跟踪 12 个缓存文件是一次仓库级变更，且 `.gitignore` 已声明该路径——属于历史遗留，需确认后单独处理 |
| O-03 | Pyodide 二进制重复两份（38M）+ dist 里再各一份 | 涉及部署路径（dev 用 `/pyodide/`，prod 用 `/learn-python/pyodide/`），改动会影响线上，需确认 |
| O-04 | Pyodide 被加载两次（CDN + 本地） | 同 O-03，涉及 dev/prod 两条路径的行为，需确认后统一 |
| O-05 | `docs/public/learn-python/pyodide-init.js` 是失联的老版本运行时 | 无引用，可删；但它是「修复 stdout 捕获之前」的唯一物证，留着有考古价值，交由维护者决定 |
| O-06 | 两个部署 workflow（`main.yml` + `deploy.yml`）同时部署 GitHub Pages | 需确认哪一个才是权威，删另一个。属于发布配置，超出走查范围 |
| O-07 | `unpack.html` 两个「错误演示」块把完整 traceback 铺开 | 对初学者是噪音。可只显示最后一行 `ValueError: ...`。属体验优化，不影响学习能否继续 |
| O-08 | 站点没有 pytest / 单元测试，`package.json` 只有 3 个 docs 脚本 | 本次新增了两个门禁（`check-links.js`、`unpack-claims-audit.py`）但没接进 `package.json` scripts，也没接 CI。接入需确认是否允许改 CI |
| O-09 | `examples/` 下 66 个文件与课程零关联 | 要么补教程引用，要么明确它们是素材库。属内容规划决策 |
| O-10 | careers 三份文件对 Python 自评不一致（未学/了解/弱） | careers 是只读的外部目录，本次不得修改，只记录观察 |
| O-11 | README 的 13 条外部学习路径在 `docs/` 里零引用 | 走查者从站内页面无法知道它们存在，也没有「学 L1 前要不要先看官方 tutorial」的说明。README 的自报进度与 `progress.md` 的课表是两套独立口径。属于内容规划决策，未改 |
| O-12 | `progress.md` 课表与 README 学习路径口径不一致 | 同上，需维护者统一 |

## 门禁状态

| 门禁 | 命令 | 结果 |
|------|------|------|
| 文档构建 | `npm run docs:build` | ✅ 通过 |
| 链接（含 frontmatter） | `node .walkthrough/check-links.js` | ✅ 通过（含反向验证） |
| 拆包断言 | `python .walkthrough/evidence/unpack-claims-audit.py` | ✅ 22 PASS |
| examples 运行 | `bash .walkthrough/run-all.sh` | ✅ 61 通过 / 6 需交互或特定调用 |
| 浏览器交互块 | Playwright 逐块点击 | ✅ 20/20，0 非预期报错 |

## 明确不做的事

- 不 push、不 merge、不 deploy、不删除外部资源。
- 不修改 `careers`、`workflow`、`zen`。
- 不写原始思维链或凭据到任何提交里。
