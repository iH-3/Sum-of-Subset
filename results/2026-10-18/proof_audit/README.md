# 2026-10-18 证明审查回执

审查基准：`702b78476185eb1554a1f679c1117f3b2eb8bf25`。

[审查报告](../../../reports/proof_audit_20261018.md)与 [PDF](../../../reports/proof_audit_20261018.pdf)说明一般数学论证、有限检查及尚未完成的独立对应。独立闭合范围保持 `71≤N≤89`；归档上界 84 没有因这些有限 PASS 被改标为完整独立认证，upper88 研究仍为部分进展。

`summary.json` 的状态为 `PASS_LISTED_FINITE_CHECKS_ONLY`。它不是证明助手认证，也不表示所有历史模型行与实际集合的对应已重新独立证明。

| 检查 | 本次结果 |
|---|---|
| 新链 17 个入口 | 标准/优化模式共 34 次成功运行，逐字节一致；其中 15 个入口亦与已发布结果逐字节一致 |
| 最新上界 89 | 440,904 个整数根、441,243 个最终系统全部重建；逐整数结果与符号区间结果完全一致 |
| 实际集合几何行 | 固定种子，120 个集合、66,615 项检查通过；有限测试不替代普遍性证明 |
| upper84 完整入口 | 11/11；其中 retained upper85 为 140 PASS、0 FAIL、0 SKIP |
| upper86 归档 | 原始 19 阶段及附加前提的全新组合重放；size-88 的 4 个范围与 size-87 的 8 个范围、22 个补充组件全部拼合；运行前后完整性检查通过 |
| 归档 `-O` 防护 | 两个正式完整入口均拒绝优化模式；内部 `assert __debug__` 防护会被优化删除，详见报告第 6.2 节 |

## 文件

- `summary.json`：状态、命令回执摘要、来源与审查驱动 SHA-256。
- `evidence_manifest.json`：`evidence.zip` 每个成员解压后内容的 SHA-256。
- `evidence.zip`：本次新日志、逐段回执、84/85 覆盖信息、89 的逐整数分片及其他补充检查。

大型新链输出与已发布结果逐字节相同的，只记录哈希及仓库参考位置，不再重复存放。没有引用旧 PASS 日志冒充本次运行。归档各范围的局部日志有意保留 `partial` 或 `full_ordinary_replay: false`；完整性由最后的覆盖拼合及组合驱动汇总判定。

`execution_history/` 保留最初的基础入口 `-I` 导入失败、改用兼容 `-E` 的成功回执、最初状态解析问题、归档目录完整性问题及主动中止的串行运行。初始失败回执没有改写为成功。冻结归档未修改；环境残留与原 ZIP 成员核对后移到冻结目录外。最终通过只使用新的完整组合运行。

## 复现

完整命令见报告第 7 节。新增驱动位于：

- [audit_upper_bound_chain.py](../../../experiments/audit_upper_bound_chain.py)：重跑新链并比较标准/优化输出。
- [audit_archived_upper86.py](../../../experiments/audit_archived_upper86.py)：用原归档接口组合全部阶段及范围。
- [audit_upper89_geometry.py](../../../experiments/audit_upper89_geometry.py)：直接从集合检查几何行及负面控制。
- [audit_archive_entrypoints.py](../../../experiments/audit_archive_entrypoints.py)：复现优化模式入口防护检查。
- [collect_proof_audit.py](../../../experiments/collect_proof_audit.py)：本次历史目录的回执打包器，不是数学验证器；新的干净重放不必制造历史失败目录。

结果包 SHA-256：`eee195088c23e8842482d45d78e7db34afbe39aa117e6a35ce711378972c6149`。

## 补齐独立数学认证的最短路径

可以从新链已证明的 `N≤89` 接入以下五个端点。已有报告给出了这些论证，本轮也阅读了关键路径；这里列的是后续应逐项记录的独立对应义务，不是在宣称这些地方已有反例或缺失证明。数百万次数值代入不必改成人工重复检查，应以通用行族、实际辅助变量的实现和完整分类为复核单元。

| 排除基数 → 上界 | 主要阅读入口 | 应逐项记录的对应 |
|---|---|---|
| 89 → 88 | 冻结包 `proofs/exact88/proof89.md` 及完整汇总证明 | 稠密核心、平移交叠、实际亏损变量；分支中的外层整数性与原始模型行 |
| 88 → 87 | `proofs/exact87/MATHEMATICAL_SCOPE.md`、`proofs/exact87/bundle/adoption/MODEL_ACCEPTANCE.md` 及结构证明 | 2,992 种保留中心的整数组合；原始容量门槛与后加改进行的先后；所有补充父根与行族 |
| 87 → 86 | `auxiliary_snapshot/endpoint87/model_hypotheses.md` 及完整汇总证明 | 最终门槛重建、实际基数恒等式、22 个补充组件的适用域及穷尽性 |
| 86 → 85 | 仓库 `verification/upper84/audit/verification_program/proof/report.tex` | Z/P/H 分类、唯一实际贡献者、森林资源和每条终端路径到程序清单的对应 |
| 85 → 84 | 仓库 `verification/upper84/proof/report.tex` 及其补充证明 | 新端点的活动性、Z5 端点正常性的推导顺序、C5 实际尾部分类及其资源计费 |

前三行的 `proofs/` 路径相对于冻结包的 `payload/subset_sum_verification/`；`auxiliary_snapshot/` 相对于冻结包根目录。还须核对每个端点引用的通用引理；不能因为旧端点曾有 PASS 就跳过其数学前提。
