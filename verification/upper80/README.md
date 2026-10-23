# 向上界 80 的研究：全局仍为 71≤N≤81

本目录同时保存已完成的辅助定理验证和未完成的研究原型。**它不是上界 80 的完整验证包。**

## 已完成的辅助验证

```bash
python -I -S -B verification/upper80/check.py --output normal.json
python -O -I -S -B verification/upper80/check.py --output optimized.json
```

Python 3.10+，只需标准库。`density.py` 完整检查 β=0..24 的有限基例与归纳算术；`profiles.py` 独立重建410项同步更新；`source_bounds.py` 对解析引理执行整数集合回归，并检查严格直径及尖锐性反例。定理和通用证明见 [报告](../../reports/upper80_progress_20261023.tex)。固定种子实例只作回归，未用来代替证明。

入口只会报告 `PASS_AUXILIARY_IMPROVEMENTS_ONLY`，同时声明 `global_upper_bound_certified=false`。完整普通/优化回执在 [results](../../results/2026-10-23/upper80_progress/)。

## 明确未完成的有限研究

```bash
python -I -S -B verification/upper80/replay_partial.py --output partial.json
```

该入口重放 `data/upper80_partial_research.json.gz` 中的候选系统证书，并检查已闭合树的互补分支。全部目录包括显式列出的开放根；**开放根计入目录不代表已排除它。** 接口只能报告 `PASS_PARTIAL_RESEARCH_REPLAY`，且 `structural_applicability_certified=false`。

`model.py`、`parametric.py`、`exact.py` 是研究模型及其算术重放器。`discover.py`、`branch_discover.py`、`fast_lp.py`、`low_c_discover.py` 是可选发现工具，需要 NumPy/SciPy。求解器的不可行状态不作为数学证书；每次成功发现仍须重建整数权重并独立重放。新源和集行、截断交叠行的通用证明已写出，但完整结构接入仍缺等差边界等审阅，不能由这些原型推断全局结论。

未闭合的原始根：`(j,index,positive)` 为 `(4,142,0)`、`(4,142,1)`、`(5,219,0)`、`(5,256,0)`、`(5,266,0)`、`(5,268,0)`、`(5,270,0)`、`(5,413,0)`、`(6,436,0)`。索引来自 `list(patterns(j))+list(partial_patterns(j))`，实际状态完整保存于数据包。

已有完整上界仍使用 `verification/upper81/check.py`；其文件未被本次研究修改。
