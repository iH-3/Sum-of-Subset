# 89 元端点排除：独立上界 88

本目录记录首项双和集与自身平移的核心重叠补强，以及完整端点证书验证。结合此前独立闭合的上界 89，结论为 **71 ≤ N ≤ 88**。这不是对归档上界 84 的数值改进。

一般证明见 [报告](../../../reports/upper88_leading_overlap_20261018.pdf)。共同核心 E 给出的首项分量与自身平移交集下界为
\[
2|E|-R_p-R_q-p_i+M_p-1.
\]
原始并集亏损只叠加两个成员的区间外损失中的一个。整侧亏损按实际并集定义，与原有子组同时实现，避免重复计费。

| 项目 | 数量 |
| --- | ---: |
| 结构根组 | 61,884 |
| 整数根系统 | 641,524 |
| 粗模型 / 嵌套模型组 | 60,766 / 1,118 |
| 整数证书向量 | 2,773 |
| 区间检查 | 61,980 |
| 使用二分的整数根 | 55 |
| 二分节点 / 树叶 | 95 / 150 |
| 最终系统 | 641,619 |
| 最大树深 | 10 |
| 最小规范化严格余量 | 11/1069 |

## 复现

在仓库根目录运行，仅需 Python 3.10+ 标准库：

~~~bash
python -I -S -B verification/upper88_endpoint.py --output .work/upper88_endpoint.json
python -O -I -S -B verification/upper88_endpoint.py --output .work/upper88_endpoint_optimized.json
python -I -S -B experiments/verify_leading_core_geometry.py --output .work/upper88_geometry.json
~~~

完整逐点交叉核验：

~~~bash
python -I -S -B experiments/verify_upper88_endpoint_sharded.py \
  --reference .work/upper88_endpoint.json \
  --output .work/upper88_exhaustive.json \
  --work-dir .work/upper88_exhaustive_parts \
  --receipt .work/upper88_exhaustive_receipt.json \
  --jobs 8
~~~

也可用单进程：

~~~bash
python -I -S -B verification/upper88_endpoint.py --exhaustive --output .work/upper88_exhaustive.json
~~~

Windows 完整续研链入口为仓库根目录的 verify_upper88_windows.bat。前置数学证明来自新链和 upper88_progress_20261018.tex；本轮不读取归档端点证书。

## 文件含义

- summary.json：完整验证结果摘要。
- result.json.gz：逐组证明结果及源文件指纹，解压后为 JSON。
- result_archive.json：压缩包与原始 JSON 的大小、SHA-256。
- run_receipt.json：普通/优化模式的实际退出码及输出一致性。
- exhaustive_receipt.json、exhaustive_parts/：逐点矩阵重建、整数证书和完整分区检查。
- geometry.json：240 个实际集合、4,800 项新几何行检查及旧见证违差。
- regression.json：旧进展验证器除源文件指纹外的结果保持不变。
- discovery_receipt.json、discovery_evidence.zip：搜索来源和一次被精确检查拒绝的浮点权重重构。该失败不计入验证通过。
- report_review.json：编译及逐页视觉检查记录。

搜索程序 experiments/generate_upper88_endpoint.py 可用 SciPy 发现权重，支持分区和显式种子。最终验证不依赖 SciPy、求解器状态或搜索日志。候选权重只有在精确残余非负且右端严格为负时才被接受。

旧 upper88_relaxation_witness.json 保持原样：它仍满足旧模型，但四条新核心重叠行分别被违反 72。旧验证结果与新完整排除不存在矛盾。
