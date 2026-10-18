# 89元端点：局部上界改进、部分证书与精确障碍

**本轮全局上界仍为 `N≤89`，没有证明 `N≤88`。** 已证明的数值改进是R段预算从`329−I`收紧到`313−I`，排除整个R4家族。一般证明见[九页报告](../../../reports/upper88_progress_20261018.pdf)及[LaTeX源码](../../../reports/upper88_progress_20261018.tex)。归档上界84的完整独立复核仍未完成。

本轮补强本原格修复、前缀保留、核心重叠、剥离点吸收、双向分位约束及两重和集的区间并集计数。固定评分约束仍保留在两个特殊零空洞模式中。

| 核验对象 | 结果与范围 |
| --- | --- |
| 局部R段预算 | 390项同参数见证证明 `ρP+ρQ−2z≥81`，故 `c≤313−I<4d` |
| 部分排除证书 | 3,651组、95,443个整数根系统；387组整数权重；38个二分节点、95,481个最终叶系统；最小规范化严格余量`1/46` |
| 未覆盖部分 | 完整候选域61,884组、641,524个整数根系统；58,233组不在本次部分证书中 |
| 精确松弛障碍 | `a=b=36`的Z4 A模式；450个非负变量，1,619条根行及682个二分中选定的1,420条行全部成立 |
| 数值矩阵展开 | 8批逐个检查全部95,443个**已供给**整数根系统，与符号区间逐组、逐统计量一致 |
| 模式一致性 | 普通与`-O`输出逐字节一致；逐点结果仅验证模式字段不同 |
| 实际集合矩阵检查 | 150组实际集合、48,734项当前程序生成的几何行检查 |
| 基础回归 | upper89输出与此前归档逐字节一致 |

该有理点是必要条件松弛的可行点，不是原问题的可行集合或反例。它同时满足每个可用二分的某一子分支，因此用同一套约束继续分支不能排除该点；需要新的必要条件。

从仓库根目录运行，均只需Python标准库：

```bash
python -I -S -B verification/upper88_progress.py --output .work/upper88-progress.json
python -I -S -B -O verification/upper88_progress.py --output .work/upper88-progress-optimized.json
python -I -S -B experiments/verify_upper88_geometric_rows.py --output .work/upper88-geometric-rows.json
```

进展验证器输出`PASS_PROGRESS_ONLY`，不把部分覆盖解释为全局排除。Windows可运行`verify_upper88_progress_windows.bat`。

本次逐整数展开使用：

```bash
python -I -S -B experiments/verify_upper88_progress_sharded.py --reference .work/upper88-progress.json --output .work/upper88-progress-exhaustive.json --work-dir .work/upper88-progress-parts --receipt .work/upper88-progress-parts/receipt.json --jobs 8
```

也可使用进展验证器的`--exhaustive`参数。批次驱动的每批原始结果均压缩保存；合并要求每个供给根组恰好出现一次，不表示覆盖完整候选域。

| 文件 | 内容 |
| --- | --- |
| `summary.json`、`run_receipt.json` | 明确的进展范围、命令、耗时、输入哈希和结果比较 |
| `result.json.gz`、`result_archive.json` | 完整标准输出及压缩前后SHA-256；解压后逐字节一致 |
| `exhaustive_shards.json`、`exhaustive_parts/`、`exhaustive_summary.json` | 8批部分域逐整数展开的完整回执、输出和统计 |
| `lattice_gate.json`、`retained_prefix.json` | 本原格修复、提前保留、5,876项后续前缀预算及有限检查 |
| `low_envelope.json`、`high_groups.json` | R段390项耦合预算见证，以及高空洞分组的逐行蕴涵检查 |
| `core_overlap.json`、`crossing_envelopes.json` | 几何引理的实际集合辅助检查 |
| `geometric_rows.json` | 当前源代码生成矩阵的48,734项独立实际集合检查及哈希 |
| `obstruction_summary.json` | 精确有理松弛见证的核验摘要 |
| `negative_controls.json` | 11项负面控制，包括把部分证书误当完整覆盖、篡改见证、遗漏或错选二分 |
| `search_status.json` | 未闭合搜索的范围与失败状态，未计作证明成功 |
| `withdrawn_search.json` | 撤回早期宽度项符号错误的探索；未据此发布证书或上界 |
| `report_review.json` | 九页最终PDF的逐页视觉核对及PDF／TeX哈希 |

独立的证明数据为[data/upper88_partial_certificates.json](../../../data/upper88_partial_certificates.json)和[data/upper88_relaxation_witness.json](../../../data/upper88_relaxation_witness.json)。可选搜索程序`experiments/search_upper88_candidate.py`需要NumPy和SciPy；当前模型已存在上述精确障碍，不应把未闭合搜索称为成功证明。

有限实例检查补充一般论证的审查，不替代报告中的任意大小证明；本轮结果不是证明助手形式化认证。
