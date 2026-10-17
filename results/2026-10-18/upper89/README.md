# 90→89：完整核验记录

本轮排除90元端点，接续已审查的 `N≤90` 基础，得到 `71≤N≤89`。归档上界84的完整独立复核仍未完成。一般数学引理及从实际集合到必要不等式的归约见[报告](../../../reports/upper89_from90_20261018.pdf)和[LaTeX源码](../../../reports/upper89_from90_20261018.tex)。

从仓库根目录运行：

```bash
python -I -S -B verification/upper89.py --output .work/upper89.json
python -I -S -B verification/upper89.py --exhaustive --output .work/upper89-exhaustive.json
```

验证器仅依赖Python标准库。它独立重建全部30,396个结构组和440,904个整数根系统；1,534组整数证书覆盖441,243个最终叶系统，最小规范化严格余量为 `1/748`。每个二分的两个子分支均检查；浮点求解状态不作为证明。

| 文件 | 内容 |
| --- | --- |
| `summary.json` | 标准模式的完整统计与有限审计摘要 |
| `result.json.gz`、`result_archive.json` | 完整输出及压缩前后字节数、SHA-256；解压后与标准模式输出完全一致 |
| `run_receipt.json`、`exhaustive_summary.json` | 命令、时间、输入哈希，以及标准／逐点／`-O`／再生成／upper90回归的比较 |
| `exhaustive_shards.json`、`exhaustive_parts/`、`interrupted_exhaustive.json` | 完整逐点核验的8批回执和压缩输出，以及未计为PASS的中断运行记录 |
| `lattice_gate.json`、`progression_checks.json` | 格化参数、等差支持与双剩余类检查 |
| `retained_prefix_checks.json` | 全部4,644个状态／侧别的前缀预算见证，以及有限实例与小基数边界检查 |
| `fixed_score_order.json`、`sign_clauses.json` | 评分顺序的180条覆盖关系与46条带原始见证的符号约束 |
| `compatibility_comparison.json` | 同一90元标量模型中加入 `μ≥ρ` 前后的逐状态比较 |
| `low_envelope.json`、`high_groups.json`、`grouping_checks.json`、`hole_schedule.json` | 空洞预算、合并参数及740,143项来源到模型的逐行蕴涵检查 |
| `covering_checks.json`、`negative_controls.json` | 覆盖辅助检查与50项负面控制 |
| `nested_groups.json`、`method_usage.json` | 577个嵌套组及证书中正权重所用的行族统计 |
| `generation.log`、`regeneration.log` | 两次从空白状态进行的证书发现与最终精确验收 |
| `report_review.json` | 六页最终PDF的逐页检查记录及PDF／TeX哈希 |

可选再生成命令需要NumPy和SciPy：

```bash
python experiments/generate_upper89_certificates.py --output .work/upper89-regenerated.json
```

有限实例检查支持一般论证的审查，不替代报告中的任意大小证明；本项目没有把本轮结果称为证明助手形式化认证。

本轮将完整逐点核验分成8个批次。各批逐一检查数值矩阵、整数证书和完整二分树；合并时检查所有重建根组恰好出现一次，并要求每组结果和全部统计量与标准模式一致。批次输出带输入哈希，可用`--resume`恢复。此前中断的连续运行没有记为PASS。

```bash
python -I -S -B experiments/verify_upper89_sharded.py --reference .work/upper89.json --output .work/upper89-exhaustive.json --work-dir .work/upper89-parts --receipt .work/upper89-parts/receipt.json --jobs 8
```
