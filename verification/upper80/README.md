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

## 2026-10-24 的新增研究工具

```bash
python -I -S -B verification/upper80/check_new_lemmas.py --output lemmas_normal.json
python -O -I -S -B verification/upper80/check_new_lemmas.py --output lemmas_optimized.json
```

新入口检查源内部空隙、首项交叠、固定项覆盖与冲突、整数同余、目标探针、已知源子集的完整并集以及顶部尾部容量；同时核查条件性结构算术和适应性端点日程。独立集合对照和负面控制仍不代替一般证明，证明及适用前提记录于 [研究检查点](research_checkpoint.md)。入口明确返回 `PASS_NEW_RESEARCH_LEMMA_CONTROLS_ONLY`，不认证全局上界 80。

完整整数模式还可使用实际截断见证的整性：`F`、`FD`、`GB` 和 `phi` 来自整数极值，而非任意假定线性松弛解为整数。每次取整均须先给出严格的有理上界证书。

六空根的秩偏差 `k=2..7` 已取得局部终端反证，其中 `k=2` 用 3 次互补分支和 4 个叶闭合；`k=0,1` 仍需排除。这些 [局部证书](../../data/upper80_refinements_20261024.json.gz) 可用下面的标准库命令复核，合计 9 个终端。整个原始根尚未因此闭合。

```bash
python -I -S -B verification/upper80/verify_refinements.py --output refinements.json
```

`cover_capacity.py` 还把扩大的源区间与外点组成的并集转化为总容量上界，并对完整源和集 `2D` 同样计数。独立对照包含 1,200 项容量检查、400 项零超额精确等号以及 1,200 项缺失条目的拒绝控制。

条件性小松弛接口已保存为独立数据包；`j=1, delta≤110` 的 22 个模式及 `j=2, delta≤40` 的 66 个模式均闭合，要求共同整数源、`w≤32` 和 `F≥24`。它们不替代尚未完成的结构适用性证明。

```bash
python -I -S -B verification/upper80/low_slack.py --output low_slack.json
```

## 正洞根的新局部闭合

原始根 `(4,142,1)` 已排除 `W=w/2=2..7`，仍保留 `W=1` 为开放。联合核心前缀检查把 `w=4` 总质量下界加强到 126，双侧前驱下界加强到 122，并闭合这一切片。原始根总数仍是 4,645/4,654 已闭合。

```bash
python -I -S -B verification/upper80/verify_positive_refinements.py --output positive.json
python -O -I -S -B verification/upper80/verify_positive_refinements.py --output positive_optimized.json
```

证书包含全部前提与显式开放切片；验证只需标准库。单独继续 `W=1` 可先导出其已核验前提，再运行发现器：

```bash
python -I -S -B verification/upper80/verify_positive_refinements.py --export-open .work/upper80/positive_W1_parent.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verification/upper80/resume_search.py 4 142 --positive --hole-W 1 --parent .work/upper80/positive_W1_parent.json --cache .work/upper80/positive_W1_resume --output .work/upper80/positive_W1_result.json
```

## 恢复发现搜索

`data/upper80_search_frontier_20261024.json.gz` 保存 3,907 个缓存节点及共享前提；其中 1,603 个局部闭合节点不构成任何新增原始根的完整覆盖。以下命令适用于尚无相应缓存的工作副本；恢复器拒绝覆盖内容不同的现有节点。

```bash
python -I -S -B verification/upper80/search_frontier.py --restore data/upper80_search_frontier_20261024.json.gz
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verification/upper80/resume_search.py 6 436 --rank 1 --integer-first --cache .work/upper80/20261024/kernel_rank_branch6_1 --output .work/upper80/resumed_rank1.json
```

v2 存档保留模式键的顺序，因为证书按确定的行号引用不等式；恢复后的闭合节点会重新重放。旧 v1 存档不再接受，需要从原缓存重新导出。恢复只需标准库，继续发现需要 NumPy/SciPy。成功的终端仍须整数证书重放；完整返回的分支树还会核验互补域覆盖。
