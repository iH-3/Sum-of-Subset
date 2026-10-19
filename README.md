# Sum-of-Subset：子集和包含于四重和集

研究有限实数集 `A` 满足

\[
\operatorname{FS}(A)=\left\{\sum_{a\in X}a:X\subseteq A\right\}
\subseteq A+A+A+A
\]

时，`|A|` 的最大值。空集和为 0，右侧允许重复使用同一个元素。

**精确最大值尚未确定。目前已独立核查闭合的范围为 71 ≤ N ≤ 84。** 2026-10-16 的多轮续研先排除 103、102、101，再排除 100、99、98、97、96、95、94、93，接续 2026-10-14 已完成的 115→103 论证；2026-10-17 再排除92元端点；2026-10-18 先后排除91、90、89元端点，2026-10-19 先后接入并完整核验88、87、86、85元端点。大小85的结构、13类实际情形与有限依赖现已完成独立接入，独立链达到归档上界84。新的尖锐源参数界为162；精确最大值仍待进一步研究。

**证明基础：** 已确认构造、新报告和旧基础上界 `N ≤ 115`；旧剥离证明的一处剩余类表述已修正，修正不改变引理结论。新的 115→103 报告沿用该修正，逐项证明所需的后续结构引理。先前审查记录见 [审查报告与勘误](reports/proof_review_20261014.md)。

## 先读什么

- **[85→84 接入报告 PDF](reports/upper84_adoption_20261019.pdf) · [LaTeX 源码](reports/upper84_adoption_20261019.tex)**：扣除重复计入中央区间的重新插入配对标签，将源参数界 **165→162**，并给出实际源的等号例子；全非空覆盖加强为 `w≥2|D|+8`，单空终端加强为 `112−w`。用三点截断和两条一元不等式替代最后7315状态枚举，矛盾余量至少16。大小85的13类实际情形全部接入，独立范围为 **`71≤N≤84`**。[完整标准库入口](verification/upper84_adoption.py)、[新增解析检查](verification/upper84_geometry.py)、[源文件清单](data/upper84_adoption_sources.json)、[审阅与运行记录](results/2026-10-19/upper84/)。

- **[86→85 接入报告 PDF](reports/upper85_adoption_20261019.pdf) · [LaTeX 源码](reports/upper85_adoption_20261019.tex)**：证明全非空覆盖必须有 `w≥2|D|−36`，以一条解析引理替代152个结构例外系统并消去两个本原性等号例外；适应性截断把单空单元终端从 `131−w` 加强到 `136−w`。完成13类实际情形的接入，新增2,097,152个组件指派的条件分类检查，完整140项有限义务在标准和优化模式下均通过。独立范围推进到 **`71≤N≤85`**。[标准库入口](verification/upper85.py)、[新解析与分类检查](verification/upper85_geometry.py)、[完整源码清单](data/upper85_adoption_sources.json)、[审查对应与运行回执](results/2026-10-19/upper85/)。

- **[87→86 接入报告 PDF](reports/upper86_adoption_20261019.pdf) · [LaTeX 源码](reports/upper86_adoption_20261019.tex)**：将零洞小松弛解析界加强为 **`c≥32`**，以可取到的最大密度公式统一前缀扩张和极值删除；核对87元格化、本原性及全部必要模型。复用归档证书并重新检查全部 **1,615,300 个原始根、1,625,639 个叶反证**，包含22类补充组件和完整AP-free有限依赖。独立闭合范围为 **`71≤N≤86`**。[标准库入口](verification/upper86.py)、[独立解析与集合检查](verification/upper86_geometry.py)、[源码对应](data/upper86_adoption_sources.json)、[运行回执](results/2026-10-19/upper86/)。

- **[88→87 接入报告 PDF](reports/upper87_adoption_20261019.pdf) · [LaTeX 源码](reports/upper87_adoption_20261019.tex)**：统一实际缺额与星形重叠，用同一个稠密子核心同时加强多个叶；核对 88 元格化、五空单元和全部行族，将归档端点接到新的独立链。复用归档整数证书并重新核验全部 **1,128,280 个原始根、1,132,744 个叶反证**，独立闭合上界推进到 **87**。没有重新发现这些归档证书。[标准库验证入口](verification/upper87.py)、[直接集合检查](verification/upper87_geometry.py)、[源码接入清单](data/upper87_adoption_sources.json)和[本次运行回执](results/2026-10-19/upper87/)。

- **[89→88 续研报告 PDF](reports/upper88_leading_overlap_20261018.pdf) · [LaTeX 源码](reports/upper88_leading_overlap_20261018.tex)**：重新提炼首项双和集与自身平移的核心重叠，旧松弛见证被四条新行各以 72 的违差排除。2,773 组整数权重覆盖全部 61,884 个结构组、641,619 个最终系统；仅 55 个整数根使用 95 个二分节点。该轮将独立闭合上界推进到 **88**。程序与回执见 [upper88_endpoint.py](verification/upper88_endpoint.py) 和 [验证结果](results/2026-10-18/upper88/)。

- **[2026-10-18 先前系统审查](reports/proof_audit_20261018.md) · [PDF](reports/proof_audit_20261018.pdf)**：未发现新的致命证明错误；当时独立闭合范围为 `71≤N≤89`。重新核对原始定理、格化与资源预算，34 次标准/优化运行、89 上界全部整数系统、84/85 完整有限套件以及 86 归档的 19 阶段组合重放均已完成。报告明确列出 84 的完整独立数学认证仍缺少的逐项对应工作；[回执与日志](results/2026-10-18/proof_audit/)另附。

- **[89元端点进展报告 PDF](reports/upper88_progress_20261018.pdf) · [LaTeX 源码](reports/upper88_progress_20261018.tex)**：R段局部预算由`329−I`收紧到`313−I`，排除整个R4家族；3,651个结构组已有精确部分证书。当时剩余平衡模式有满足全部1,619行及682个二分的有理松弛见证；这是本次补入核心重叠行之前的历史状态。原见证及部分证书保留供对照。

- **[90→89 续研报告 PDF](reports/upper89_from90_20261018.pdf) · [LaTeX 源码](reports/upper89_from90_20261018.tex)**：缺陷相容性简化格化，前两层前缀保留加强跨度与质量行，评分顺序及46条符号约束补强固定损失；1,534组整数证书覆盖441,243个最终叶系统。
- **[91→90 续研报告 PDF](reports/upper90_from91_20261018.pdf) · [LaTeX 源码](reports/upper90_from91_20261018.tex)**：变阈值前缀递推、分阶段格化、完整平移的共同损失和固定项指标；995组整数证书覆盖372,137个最终叶系统，全部逐点核验通过。
- **[92→91 续研报告 PDF](reports/upper91_from92_20261017.pdf) · [LaTeX 源码](reports/upper91_from92_20261017.tex)**：9页；加强持续空洞递推、等差／非等差分支、整数中心基与删去极值后的双和集截断。4,130组整数证书覆盖274,476个最终叶系统，全部逐点核验通过。
- **[93→92 续研报告 PDF](reports/upper92_from93_20261016.pdf) · [LaTeX 源码](reports/upper92_from93_20261016.tex)**：9页；分段质量平移、外侧格性传播与更深的核心截断。2,450组整数证书覆盖128,106个最终叶系统，全部逐点核验通过。
- **[94→93 续研报告 PDF](reports/upper93_from94_20261016.pdf) · [LaTeX 源码](reports/upper93_from94_20261016.tex)**：7 页；精确前缀逆估计、两类小空洞见证，以及保留空洞变量的耦合预算。提前削减 20,264 个低空洞模型；1,539 组整数证书覆盖 76,891 个最终叶系统，全部逐点核验通过。
- **[95→94 续研报告 PDF](reports/upper94_from95_20261016.pdf) · [LaTeX 源码](reports/upper94_from95_20261016.tex)**：7 页；证明尖锐非等差缺陷下界 `ρ(X)≥|X|−5` 对 `|X|≥17` 成立，扩展有限基例并优化不等式的适用条件。先削减 10,280 个低空洞根模型；897 组新整数证书覆盖 61,915 个最终叶系统。6,806 个结构组中仅 48 组需要嵌套模型；完整逐点交叉核验通过。
- **[96→95 续研报告 PDF](reports/upper95_from96_20261016.pdf) · [LaTeX 源码](reports/upper95_from96_20261016.tex)**：8 页；尖锐四极值估计、统一重叠损失预算、三个空单元和无需限定大损失中心数量的二分。651 组整数证书覆盖 37,835 个最终叶系统；5,324 个结构组中仅 23 组需要嵌套模型，树深度最多 5。全部逐点交叉核验通过。

- **[97→96 续研报告 PDF](reports/upper96_from97_20261016.pdf) · [LaTeX 源码](reports/upper96_from97_20261016.tex)**：9 页；质量平移合并高空洞参数，保留贡献者决定的反射方向，并证明三类有效二分。156 组整数证书覆盖 23,303 个最终叶系统；只有 12 个结构组需要嵌套包络，17 个整数情形使用 35 个二分节点。全部逐点交叉核验通过。
- **[证明方法优化报告 PDF](reports/proof_method_20261016.pdf) · [LaTeX 源码](reports/proof_method_20261016.tex)**：6 页；通过质量平移把正低空洞统一到 `z=14`，先用粗双和集界反证，仅 5 个叶节点需要嵌套包络。1,455 次区间检查、94 组整数证书覆盖 18,280 个模型；上界保持 `N≤97`。
- **[98→97 续研报告 PDF](reports/upper97_from98_20261016.pdf) · [LaTeX 源码](reports/upper97_from98_20261016.tex)**：9 页；统一含空洞的跨度预算，以大损失中心组织分支，并补强 98 元端点的格化比较。3,750 次区间证书检查覆盖 45,928 个模型，全部逐个整数交叉核验通过。
- **[99→98 续研报告 PDF](reports/upper98_from99_20261016.pdf) · [LaTeX 源码](reports/upper98_from99_20261016.tex)**：9 页；小缺陷跨度、保留损失预算的两个空单元、嵌套区间包络，以及符号二次区间证书。5,443 次区间检查覆盖 82,257 个模型，并已逐个整数交叉核验。
- **[100→99 续研报告 PDF](reports/upper99_from100_20261016.pdf) · [LaTeX 源码](reports/upper99_from100_20261016.tex)**：8 页；零缺陷核心的分类、一个空单元与两个区间外中心、两个空单元的零损失覆盖，以及全部 59,206 个线性模型的精确反证。
- **[103→100 续研报告 PDF](reports/upper100_from103_20261016.pdf) · [LaTeX 源码](reports/upper100_from103_20261016.tex)**：8 页；统一有效空洞检验、恰有一个空覆盖单元的完整分支、最多一个区间外中心，以及 2,580 个线性模型的精确整数反证。
- **[115→103 续研报告 PDF](reports/upper103_from115_20261014.pdf) · [LaTeX 源码](reports/upper103_from115_20261014.tex)**：12 页；统一格化、四极值缺陷、24 个有效空洞参数、保留核心质量的覆盖证书，以及完整有限参数排除。
- [本次研究报告 PDF](reports/research_report.pdf) · [可编辑 LaTeX](reports/research_report.tex)：约定、完整构造证明、构造族的精确边界、显式整数化界、核验范围和下一步任务。
- [既有证明审查](reports/proof_review_20261014.md)：具体反例、剥离证明修正、基础上界 115 的核对、原始文献和审查范围。
- [原上界 86 完整报告](reports/upper86_complete_20261005.pdf) · [LaTeX](reports/upper86_complete_20261005.tex)。
- [原上界 85 汇总报告](reports/upper85_consolidated_20261005.pdf) · [LaTeX](verification/upper84/audit/verification_program/proof/report.tex)。
- [原上界 84 补充报告](reports/upper84_supplement_20261005.pdf) · [LaTeX](verification/upper84/proof/report.tex)。
- [研究状态与待办](RESEARCH_STATUS.md)。

## 目前能明确说明什么

| 结论 | 依据与本次状态 |
| --- | --- |
| `N ≥ 71` | 明确构造；重新证明；独立核验全部 3349 个子集和值的四项表示 |
| `N ≤ 122` | 新报告中给出完整初等证明，作为不依赖旧逆定理的独立基线；不是对 84 的改进 |
| **最新独立上界 `N ≤ 84`** | 大小85的结构和13类实际情形完成接入；源参数界165→162，最后alpha分支由无界解析不等式排除；全部有限义务重放通过 |
| **此前独立上界 `N ≤ 85`** | 接入86元端点的13个实际情形；新解析引理替代结构矩阵例外，全部140项有限义务和新增分类检查通过 |
| **此前独立上界 `N ≤ 86`** | 接入87元端点；全部普通范围、22类补充树、结构与AP-free有限依赖重新核验 |
| 已审查的旧基础上界 `N ≤ 115` | 原始定理条件和基础推导已核对；采用审查报告中的剥离表述修正 |
| **续研上界 `N ≤ 103`** | 从已审查的 115 基础闭合；262 个格化方向、416 个低空洞状态、24 个高空洞参数见证全部精确通过；不依赖旧端点证书 |
| **续研上界 `N ≤ 100`** | 接续 103；108 个格化方向、894 个低空洞状态和 431 个高空洞终端状态通过；2,580 个空单元分支由新生成的 189 组整数证书全部排除 |
| **续研上界 `N ≤ 99`** | 排除 100 元端点；38 个格化方向、364 个低空洞状态及 966 个高空洞终端状态通过；59,206 个线性模型由重新生成的 204 组整数证书全部排除 |
| **续研上界 `N ≤ 98`** | 排除 99 元端点；39 个格化方向、391 个低空洞状态、1,217 个高空洞终端状态通过；90 组新整数证书，5,443 个符号区间覆盖 82,257 个线性模型，全部逐点交叉核验通过 |
| **续研上界 `N ≤ 97`** | 排除 98 元端点；结构参数检查不变。新简化证明使用 94 组整数证书、1,455 次区间检查，覆盖 18,280 个模型，全部逐点核验通过；原 209 组证书版本保留 |
| **续研上界 `N ≤ 96`** | 排除 97 元端点；41 个格化方向、437 个低空洞状态、2,200 个高空洞状态通过；412 个待处理高空洞状态合并为 17 组。156 组证书、2,085 次区间检查和 52 个二分树叶检查覆盖 23,303 个最终叶系统，全部逐点核验通过 |
| **续研上界 `N ≤ 95`** | 排除 96 元端点；42 个格化方向、456 个低空洞状态和 2,840 个高空洞状态通过。1,241 个待处理高空洞状态合并为 26 组；651 组整数证书、5,350 次区间检查及 416 个树叶检查覆盖全部 37,835 个最终叶系统 |
| **续研上界 `N ≤ 94`** | 排除 95 元端点；2,723 个删除区间基例支持新的缺陷引理。43 个格化方向、461 个低空洞状态和 3,500 个高空洞状态通过；2,330 个待处理高空洞状态合并为 50 组。897 组证书、6,809 次区间检查及 675 个树叶检查覆盖全部 61,915 个最终叶系统 |
| **续研上界 `N ≤ 93`** | 排除 94 元端点；44 个格化方向、420 个低空洞状态和 3,896 个高空洞状态通过。低空洞见证将预算收紧至 242；高空洞分组合并后保留同一个空洞变量。1,539 组证书覆盖全部 76,891 个最终叶系统 |
| **续研上界 `N ≤ 92`** | 排除93元端点；45个格化方向、443个低空洞状态、3,602个高空洞状态通过。格性传播保留5个例外，新增第二大核心元素截断；2,450组整数证书覆盖128,106个最终叶系统 |
| **续研上界 `N ≤ 91`** | 排除92元端点；44个格化方向通过，条件逆定理修复14个原余量不足的方向。全部三空单元恢复整性，四空单元保留30种部分整性例外；4,130组整数证书覆盖274,476个最终叶系统 |
| **续研上界 `N ≤ 90`** | 排除91元端点；45个格化方向通过。变阈值空洞界将同一端点的高空洞预算176降至140，995组整数证书覆盖372,137个最终叶系统；完整逐点核验通过 |
| **续研上界 `N ≤ 89`** | 排除90元端点；46个格化方向通过，前两层前缀保留加强跨度与质量，固定评分顺序及46条符号约束闭合困难分支；1,534组整数证书覆盖441,243个最终叶系统，完整逐点核验通过 |
| **此前独立上界 `N ≤ 87`** | 88元格化及模型行族完成接入；冻结整数证书重新验证全部1,128,280个原始根和1,132,744个叶反证，九类补充与普通根精确互补 |
| **此前续研上界 `N ≤ 88`** | 排除89元端点；首项—自身平移核心重叠与整侧亏损补强覆盖。2,773组整数证书覆盖61,884个结构组、641,524个整数根及641,619个最终系统；最小规范化余量 `11/1069` |
| 归档证明链 `N ≤ 84` | 完整原报告与程序按原字节保留；现已补足先行上界，并完成全部后续端点的独立接入；新报告明确加强及替换的步骤 |
| 固定构造族 `A_m` | 当且仅当 `1 ≤ m ≤ 31` 可行，证明覆盖所有整数参数 |
| 显式整数化 | 若有 n 元实数解，则有坐标绝对值至多 `floor(sqrt((n+16)^(n+1)))` 的 n 元整数解 |
| 最大值 | 仍待确定；失败的有限搜索不构成全局不存在证明 |

71 元例子为

\[
A=[-31,31]\cap\mathbb Z\ \cup\ \{\pm93,\pm155,\pm217,\pm713\}.
\]

其子集和集恰为 `[-1674,1674] ∩ Z`，整个区间都包含在 `4A` 中。完整逐值证书见 [construction71.json](data/construction71.json)。

## 最短验证入口

需要 Python 3.10+，不需要第三方 Python 包、求解器或网络。以下命令均在仓库根目录运行。

```bash
# 最新85→84完整有限回放；Windows可双击 verify_upper84_windows.bat
python -I -S -B verification/upper84_adoption.py --output .work/upper84.json
python -I -S -B verification/upper84_geometry.py --output .work/geometry84.json
# 前序86→85有限回放
python -I -S -B verification/upper85.py --output .work/upper85.json
python -I -S -B verification/upper85_geometry.py --output .work/geometry85.json
python verification/verify.py --output .work/independent.json
python verification/check_set.py --certificate data/construction71.json
python verification/check_set.py --elements -1 0 1
python verification/upper103.py --output .work/upper103.json
python -I -S -B verification/upper100.py --output .work/upper100.json
python -I -S -B verification/upper99.py --output .work/upper99.json
python -I -S -B verification/upper98.py --output .work/upper98.json
python -I -S -B verification/upper97.py --output .work/upper97.json
# 简化后的同一上界证明
python -I -S -B verification/upper97_simplified.py --output .work/upper97_simplified.json
# 97→96 续研
python -I -S -B verification/upper96.py --output .work/upper96.json
# 96→95 续研
python -I -S -B verification/upper95.py --output .work/upper95.json
# 95→94 续研（包含新的非等差缺陷有限基例）
python -I -S -B verification/upper94.py --output .work/upper94.json
# 94→93 续研
python -I -S -B verification/upper93.py --output .work/upper93.json
# 93→92 续研
python -I -S -B verification/upper92.py --output .work/upper92.json
# 92→91 续研
python -I -S -B verification/upper91.py --output .work/upper91.json
# 91→90 续研
python -I -S -B verification/upper90.py --output .work/upper90.json
# 90→89 续研
python -I -S -B verification/upper89.py --output .work/upper89.json
# 最新 87→86：完整端点、全部辅助与 AP-free 有限依赖（不要加 -O）
python -I -S -B verification/upper86.py --jobs 8 --output results/local-upper86.json
# 前序 88→87
python -I -S -B verification/upper87.py --jobs 4 --output .work/upper87.json
python -I -S -B verification/upper87_geometry.py --output .work/upper87_geometry.json

# 此前 89→88 续研
python -I -S -B verification/upper88_endpoint.py --output .work/upper88_endpoint.json
# 可单独检查完整前缀空洞引理的参数见证与边界实例
python -I -S -B verification/nonap_hole_rho_full.py
# 可单独检查新的整数逆估计
python -I -S -B verification/nonap_inverse.py
# 可单独检查尖锐缺陷引理的 2,723 个有限基例
python -I -S -B verification/nonap_sharp.py
# 可选：逐个整数复核最新模型与区间极值
python -I -S -B verification/upper88_endpoint.py --exhaustive --output .work/upper88_exhaustive.json
```

Windows 可将 `python` 换成 `py -3`。双击 `verify_upper86_windows.bat` 检查新的87元端点及全部有限依赖，以已独立核查的上界87为数学前提；`verify_upper87_windows.bat` 保留此前88元端点检查。双击 `verify_upper88_windows.bat` 检查115→103→100→99→98→97→96→95→94→93→92→91→90→89→88十四段有限续研。双击 `verify_windows.bat` 检查构造与基础有限证书。此前各段的 Windows 入口仍保留。

校验自己的集合时，可以传入整数或有理数字符串，例如 `--elements -1/3 0 1/3`。也可使用 `--input candidate.json`，文件格式为 `{"A":[-1,0,1]}`。重复元素和浮点输入会被拒绝；触发资源上限时会报“无法得出结论”，不会误报不可行。

`upper103.py` 只用整数与有理数，检查报告中全部有限参数不等式；无限论证与适用条件由正文证明。普通模式与 `python -O` 的输出逐字节一致，两个故意失效的空洞参数均被拒绝。[本次完整结果](results/2026-10-14/upper103/result.json) 也记录了下一端点的障碍：`n=103, a=b=43, z=0` 时只能得到覆盖余量 `c≤116`，大于单元容量 `d=95`，因此尚不能继续套用“全部单元非空”的证书。这不是一个 103 元可行构造。

**2026-10-16 已解决上述障碍。** `upper100.py` 重建完整分支集合，读取 [整数证书](data/upper100_certificates.json)，逐项检查非负行组合给出严格矛盾；运行不需要 SciPy、求解器或第三方包。[完整结果](results/2026-10-16/upper100/result.json) 与 [运行记录](results/2026-10-16/upper100/run_receipt.json) 保存此次核验。普通模式与 `-O` 结果一致，7 项负面控制全部拒绝错误输入。可选的 [证书生成器](experiments/generate_upper100_certificates.py) 使用 SciPy 搜索候选权重，但只有经过精确整数验证的权重才会保存。新验证器不读取旧端点证书。

**随后完成的 100→99 续研已处理两个空单元。** [upper99.py](verification/upper99.py) 重建六类模型和每个整数参数，验证 [204 组整数证书](data/upper99_certificates.json)。证明数据按参数区间压缩，但每个整数仍单独检查，不允许区间缺口或遗漏分支。完整运行、基础 100 上界回归、普通模式与 `-O` 一致性及重新生成证书的记录见 [results/2026-10-16/upper99](results/2026-10-16/upper99)。新证明还给出零缺陷核心的完整分类；程序的 4,776 个小型检验仅作为佐证，不能替代正文的一般证明。

**99→98 续研解决了两个空单元后的 24 点残余预算。** [upper98.py](verification/upper98.py) 使用小缺陷跨度约束和嵌套区间包络保留损失信息；特别处理一个整数间隙分支和一个可能分裂的配对单元。验证路径也已优化：矩阵系数固定、右端为符号二次多项式，按整数区间的端点及凹二次函数顶点附近参数检查，5,443 次行组合检查覆盖 82,257 个模型，减少约 93.4% 的重复矩阵组合。它不从三个采样点猜测多项式。

[90 组整数证书](data/upper98_certificates.json) 已在标准库隔离模式下通过，最小规范化严格余量为 `12/271`；`--exhaustive` 对每个整数重新生成数值模型、逐行核对符号表达式并验证全部行组合，结果与区间模式一致。10 项负面控制包括“端点通过但内部顶点失败”、遗漏离散分支和误报下一个基数；全部被拒绝。当前机器上标准模式约 6.9 秒，完整逐点交叉核验约 50.7 秒。普通模式与 `-O` 输出一致，证书重新生成逐字节一致，99 基础回归结果未变。[完整记录](results/2026-10-16/upper98/) 与 [可选生成器](experiments/generate_upper98_certificates.py) 已保存。

**此前的 98→97 续研已处理上述更大的损失预算。** [upper97.py](verification/upper97.py) 在所有低空洞分支中统一使用含空洞的跨度预算，正空洞模型保留同一个 `z∈[1,14]` 变量，使质量、跨度、损失与和集基数约束互相配合。一个空单元时最多一个中心损失达到 86，因而可按“大损失中心”分类，无需枚举其区间外端点。五层区间包络、有效损失计数上限和粗略双和集界都被显式保留。

格化步骤也有实质补强：直接复用旧比较，在平衡参数处只能得到 7，不能推出所需的严格负值；保留缺陷项后，零空洞和正空洞两种比较分别至多为 `-388` 和 `-121`。[209 组新整数证书](data/upper97_certificates.json) 覆盖全部 45,928 个模型；3,750 次二次区间检查减少约 91.8% 的重复矩阵组合，最小规范化严格余量为 `12/349`。标准模式约 6.5 秒，完整逐点交叉核验约 67.4 秒，二者结果一致；此时间比较包含逐点模式额外的逐行公式核对。10 项负面控制、5,409 项整数逆公式边界检查、`-O` 一致性、证书再生成一致性和 98 基础回归均通过。[完整记录](results/2026-10-16/upper97/) 与 [可选生成器](experiments/generate_upper97_certificates.py) 已保存。

**证明方法优化（上界仍为 97）。** [新报告](reports/proof_method_20261016.pdf) 证明：对 `1≤z≤14`，令两侧质量坐标各增加 `14−z`，所有必要约束在 `z=14` 仍成立，因而可消去空洞变量。再把粗双和集界代入基数行，直接消去 `K`，形成只含外侧元素、核心跨度、两侧质量和损失的证明主干。

[upper97_simplified.py](verification/upper97_simplified.py) 重建全部 1,374 个结构根组；其中 1,313 组直接由计数约束和粗界排除。仅 4 组需要枚举大损失中心；最终 1,442 个叶节点中，1,437 个使用粗模型，只有报告明确列出的 5 个例外需要三个层级的嵌套包络。完整证明从 45,928 缩减至 18,280 个整数模型（减少约 60.2%），从 3,750 缩减至 1,455 次区间检查；[整数证书](data/upper97_simplified_certificates.json) 从 209 组减至 94 组，最小规范化余量为 `4/85`。这是证明规模的比较，不是运行速度的声明。

全部 18,280 个数值模型已逐行与符号模型核对；12 项负面控制、普通模式与 `-O` 的逐字节一致性、证书重新生成及旧 upper97 回归均通过。[完整结果与运行记录](results/2026-10-16/proof_method/) 和 [可选生成器](experiments/generate_upper97_simplified_certificates.py) 已保存。验证器只依赖标准库，不读取上一版端点证书；报告保留实际集合到模型的推导依据，并给出一组可直接手算的整数行反证。上一版报告、源码和数据均保留供对照。

**97→96 续研解决了这个端点的新例外。** [upper96.py](verification/upper96.py) 对两个空单元统一使用核心计数约束，避免把正低空洞余量 46 错当作小于普通计数阈值 45。质量平移进一步把 117 个高空洞全非空状态与 295 个一空单元状态合并为 17 组端点模型：原本需要 21,118 个高空洞模型，合并后只需 662 个，且全部由粗界排除。

覆盖估计必须先按第一对的实际贡献者固定反射方向，再计算该方向的两个分支下界；不能任取反射后较大的下界。报告给出 `(a,b,z)=(47,33,112)` 的明确检查：有效方向余量为 `−1`，错误换向会得到 `377`。这一错误捷径已纳入负面控制。

完整根集合共 1,966 组，其中 1,900 组直接使用粗模型；仅 6 组需要指定大损失中心。细化后共 2,068 个结构组，其中只有 12 组使用三个层级的嵌套包络。剩余 17 个具体整数情形用三类已证明的二分处理，共 35 个内部节点、52 个树叶；每次二分至少一侧立即矛盾，最长链为 10。最终 23,303 个叶系统由 [156 组新整数证书](data/upper96_certificates.json) 全部排除，最小规范化严格余量为 `2/299`。

标准库隔离模式、完整逐点交叉核验、15 项负面控制、`-O` 输出一致性、证书重新生成以及前一版简化 upper97 回归均通过。[完整结果和运行回执](results/2026-10-16/upper96/) 与 [可选生成器](experiments/generate_upper96_certificates.py) 已保存。新程序不读取归档端点证书；正文分别证明必要模型和各二分的穷尽性，包括质量平移后上端点的处理。

**96→95 续研完成了上述下一端点。** [upper95.py](verification/upper95.py) 重建包括三个空单元在内的完整根集合。尖锐四极值不等式将耦合预算中的 `G` 从 164 提升到 166；普通平移和主要双和集平移按实际并集亏损分组，共用一个覆盖损失预算。局部“核心计数或大损失”二分可以处理多个大损失中心，无需错误套用“至多一个”的旧规则。两个空单元时的外层格化也已单独证明；三个空单元仍只使用弱序关系。

96 元格化门槛的最小余量为 99，内层两类严格比较至多为 `−649` 和 `−17`，外层余量至少 827。高空洞筛选保留 477 个全非空状态和 764 个一空单元状态，质量平移合并为 26 组，将对应模型数从 55,388 减至 1,028（约 98.1%）。所有 1,241 个状态的 369,244 行平移支配关系均已检查。

完整证明含 5,324 个结构组，5,301 个直接使用粗模型，只有 23 个需要嵌套几何。141 个整数情形使用 275 个二分节点、416 个树叶，最大深度为 5。[651 组新整数证书](data/upper95_certificates.json) 经 5,350 次符号区间检查及全部树叶检查，覆盖 37,835 个最终叶系统，最小规范化严格余量为 `1/73`。

标准库隔离模式、全部整数的逐行交叉核验、15 项负面控制、`-O` 逐字节一致性、证书重新生成及 upper96 基础回归全部通过。[完整结果与运行回执](results/2026-10-16/upper95/) 和 [可选生成器](experiments/generate_upper95_certificates.py) 已保存。新程序不读取归档端点证书；报告包含新增无限论证，程序 PASS 不能替代这些数学论证。

**95→94 续研先改进结构引理，再求解端点。** [新报告](reports/upper94_from95_20261016.pdf) 将非等差子集和支持的缺陷下界从续研所用的 `ρ(X)≥|X|−14` 提升到尖锐的 `ρ(X)≥|X|−5`。归档证明已有大小至少 21 的版本；本轮补充大小 8、9 的 383 个删除区间基例，使一般证明的适用门槛降到 17。全部 2,723 个基例由集合和位集两种方式独立计算，并检查缺陷位置与深度恒等式；向任意大小和实数集的推广在正文中证明。

在 95 元端点，正低空洞总预算从 264 收紧到 `246<3×87`，因此整个正空洞三空单元家族消失；低空洞根模型从 69,192 减至 58,912，减少 10,280 个。各组按自身损失上限选择普通、核心或全局计数行，只有严格满足门槛时才使用较强的主要平移行。特别地，高空洞一空单元的剩余预算可达 84，不能统一使用门槛 83 的核心计数。

95 元格化检查的逆定理最小余量为 68，两类内层比较至多为 `−597`、`−33`，外层余量至少 773。2,330 个待处理高空洞状态合并成 50 组，对应模型由 99,806 减至 2,510，逐行检查 702,836 次质量平移关系。完整证明有 6,806 个结构组，6,758 个使用粗模型，仅 [48 个例外组](results/2026-10-16/upper94/nested_groups.json) 使用嵌套模型。182 棵二分树共 493 个内部节点、675 个树叶，最大深度 10。

[upper94.py](verification/upper94.py) 用 [897 组整数证书](data/upper94_certificates.json) 检查全部 61,915 个最终叶系统，最小规范化严格余量为 `1/91`。标准库隔离模式、完整逐点交叉核验、19 项负面控制、`-O` 输出一致性、证书重新生成及 upper95 基础回归全部通过。[结果与回执](results/2026-10-16/upper94/) 包含输入哈希、有限基例摘要和生成日志；[可选生成器](experiments/generate_upper94_certificates.py) 只用浮点求解器寻找候选，每个保存的证书都须通过精确运算。

**94→93 续研保留空洞与预算的关联。** [新报告](reports/upper93_from94_20261016.pdf) 从大小 17 的尖锐缺陷引理出发，按“总超额较大”或“后续前缀均非等差”两种情况推导加强逆估计，并精确求解含取整的整数不等式。例如 `r=38, μ≥165` 时，缺陷下界从 105 提升到 111；5,409 项整数逆边界与最小性检查通过。

低空洞只需两类有效空洞见证：对全部 44 个方向，`z=3,4` 时两侧缺陷之和至少 80，`5≤z≤14` 时至少 103。于是统一预算从 266 降至 `242<3×86`，正空洞三空单元家族全部消失；低空洞根模型从 89,456 减至 69,192，减少 20,264 个。验证器保存全部 88 对见证及逆估计参数，证明不依赖浮点判定。

高空洞出现两个空单元的新情况，完整保留 1,350 个全非空、1,746 个一空和 82 个两空状态。按共同质量下界合成 69 组，对应模型从 175,016 减至 6,756；模型保留同一个空洞变量和三个耦合预算行。例子 `(a,b,u_p,u_q)=(36,41,148,193)` 虽分别有 `c≤177`、`z≤145`，还必须满足 `c+z≤231`，因此不能同时代入两个最大值。全部 3,178 个状态的 974,444 行分组关系均已检查。

[upper93.py](verification/upper93.py) 重建 11,052 个结构组，其中 10,958 个使用粗模型，仅 [94 个例外组](results/2026-10-16/upper93/nested_groups.json) 使用嵌套模型。284 棵二分树有 943 个内部节点和 1,227 个树叶，最大深度 12。[1,539 组整数证书](data/upper93_certificates.json) 覆盖 76,891 个最终叶系统，最小规范化严格余量为 `1/196`。

标准库隔离模式、完整逐点交叉核验、23 项负面控制、`-O` 逐字节一致性、证书再生成与 upper94 基础回归全部通过。[完整结果与回执](results/2026-10-16/upper93/) 包含输入哈希、低空洞见证、逆估计摘要和日志；[可选生成器](experiments/generate_upper93_certificates.py) 仅用 SciPy 搜索候选。

**93→92续研保留核心第二大元素。** [新报告](reports/upper92_from93_20261016.pdf) 将低空洞分成1–2、3–4、5–14三段，分别在2、4、14做质量平移，预算为262、254、250；完整保留第一段重新出现的三空单元家族。格化阶段提前使用已证明的前缀逆估计，45个方向的逆定理最小余量为8，内层两类比较至多为−497、−17，外层余量至少669。

从实际贡献中心进行单位系数消元，2,992种三空单元模式中有2,987种可以恢复全部外侧元素的格性；其余5种继续使用弱间隙。保留正负核心的第二大元素后，以质量约束控制它们，双和集独立截断从25种增加至36种，内侧损失二分扩展到6个位置。一个此前存活的松弛点的双和集上界由447压到420。784个小集合对的28,224项直接计数检查通过。

另由稠密区间定理导出`2R≥2r+min(z,r−3)`，保留同一空洞变量的弦下界；16,593个稠密删除区间及14,491个弦取值检查通过。

最后以空洞持续性直接估计缺陷量；在大小36和40、空洞至少19的情形，两侧缺陷下界从97、126提升为112、144。10,869组参数检查通过。一般证明在报告中给出。最终证书中1,354组实际使用新增核心截断，434组使用跨度弦下界；可选的质量上界和密度二分未被采用，[具体使用统计](results/2026-10-16/upper92/method_usage.json)另附。

[upper92.py](verification/upper92.py) 重建14,700个结构组，其中14,518个使用粗模型，仅[其余182组](results/2026-10-16/upper92/nested_groups.json)使用嵌套模型。443个低空洞状态及3,602个高空洞状态通过；2,889个待处理高空洞状态合并为67组，947,062行分组关系逐一检查。[2,450组整数证书](data/upper92_certificates.json)覆盖128,106个最终叶系统，最小规范化严格余量为`1/936`。

标准库隔离模式、完整逐点交叉核验、31项负面控制、`-O`逐字节一致性、证书重新生成及upper93基础回归全部通过。[完整结果与回执](results/2026-10-16/upper92/)保存格性传播记录、截断检查、小空洞见证、输入哈希与日志；[可选生成器](experiments/generate_upper92_certificates.py)只用SciPy发现候选，接受与否由精确运算决定。

**92→91续研以条件逆定理和整数中心基为主线。** [新报告](reports/upper91_from92_20261017.pdf) 处理92元端点：原统一逆定理余量最低为−21，14个方向必须区分等差与非等差支持。非等差侧同时改善支持大小和缺陷预算，两类严格余量至少为20、24；等差支持按步长精确计数，唯一剩余的双步长情形再由剥离预算排除，严格余量至少139。提前使用已证明的持续空洞缺陷界后，格化的内层两类比较至多为−449、−31，外层余量至少619。

持续空洞引理改为直接使用完整前缀的中央区间，并从前一非等差前缀的锐缺陷下界起步，门槛由L≥2β+5降到L≥2β+4；高空洞覆盖预算由199降到150，两空单元情形随之排除，相同其余条件下的结构组由35,372减至28,180。22,335组参数和88,392个边界实例检查通过。

在三个低空洞区间同时保留支持超额下界：r−3、r+6、2r−5，84组有效空洞参数见证全部通过，质量平移不会丢失这些下界。

以实际贡献中心的整数行组合替代逐个变量消元，全部2,992种三空单元模式无需假定主要平移贡献即可恢复外侧格性。新出现的四空单元共10,880种模式全部保留；普通中心与有计费依据的主要中心合计恢复10,850种，剩余30种只使用逐项证明的整数间隙。行变换记录整数系数并复乘检查，不把有理满秩当成整性。

另从核心第二大元素导出157/156的新主要平移分位界，只有残余损失严格低于157且相应损失确已计费时启用。对双和集先删去一侧或两侧极值，再按数对数量计费，得到85条新截断；66,640项直接计数全部通过。此前满足256行约束和210种二分的松弛点，其允许的双和集大小由373压至至多356，因而被排除。

[upper91.py](verification/upper91.py) 重建28,180个结构组和271,156个整数根系统，其中27,795组由粗模型处理，[其余385组](results/2026-10-17/upper91/nested_groups.json)使用嵌套模型。460个低空洞状态、2,968个高空洞状态及871,618行分组关系检查通过。[4,130组整数证书](data/upper91_certificates.json)覆盖274,476个最终叶系统；最小规范化严格余量为`3/2519`。

标准库隔离模式、完整逐点交叉核验、36项负面控制、`-O`逐字节一致性、证书重新生成和upper92基础回归全部通过。[完整结果与回执](results/2026-10-17/upper91/)将大型结果保存为`result.json.gz`，解压后与验证器输出逐字节一致；`result_archive.json`记录压缩前后哈希。该目录还包含整数中心基、8,428组等差和集公式核对、分支覆盖和运行哈希；[可选生成器](experiments/generate_upper91_certificates.py)只用于发现候选，全部证书由精确运算验收。

该阶段只排除92元端点；其后91、90元端点已由下述续研处理。

**91→90续研采用随前缀长度变化的阈值。** [新报告](reports/upper90_from91_20261018.pdf) 在每个前缀分别核对中央区间、等差逃逸和大跳跃条件，再累加缺陷量。37元、空洞至少33时，下界从144提高到193；同一91元端点的高空洞预算由176降为140，二空单元状态从56个降为0。先用单预算比较处理小空洞，再对剩余空洞使用新估计，平衡格化余量从+3降至−95，全部45个方向严格通过。等差支持以完整的间隙／剩余类论证单独处理，没有提前使用格上剥离常数。

覆盖阶段恢复空平移的位置条件，对最大的空同侧单元额外计入4个固定项损失；完整平移共同区间和截断区间共享同一个亏损变量。只有特定四空单元例外启用110个固定标签的精确指标二分，26个非正组与8个已计费高项分开核对，避免重复计费。这些一般论证在正文重新证明；未读取归档端点证书。

[upper90.py](verification/upper90.py) 重建27,802个结构组、371,986个整数根系统，其中27,250组用粗模型闭合，552组采用嵌套模型。25个树根包含151个二分节点；[995组整数证书](data/upper90_certificates.json)认证372,137个最终叶系统，最小规范化严格余量为`3/151`。3,311个阈值参数查询、2,432个实际整数集合、17,479项等差间隙检查及4,733项双剩余类检查另附。

标准库隔离模式、完整逐点核验、43项负面控制、`-O`逐字节一致性、独立证书再生成及upper91基础回归全部通过。[完整结果与回执](results/2026-10-18/upper90/)保留压缩的完整结果、来源哈希、方法使用统计及运行记录；[可选生成器](experiments/generate_upper90_certificates.py)支持有源码指纹保护的断点恢复。主验证器不依赖SciPy，也不将浮点求解状态视为证明。

**最新90→89续研把缺陷相容性、保留前缀和固定评分顺序结合起来。** [新报告](reports/upper89_from90_20261018.pdf) 在格化阶段保留 `μ≥ρ`，直接用已有变阈值空洞界将剩余大空洞的内层比较压至 `−75` 以下，无需对删去极值后的前缀提前使用空洞定理。46个格化方向与等差支持的双剩余类例外均重新核对。

新的预算判据排除最后两步中互不相交的子集和平移，因此前两个前缀仍是本原、非等差支持，并分别保留至少一半、四分之一的空洞。4,644个状态／侧别检查的第一、第二前缀严格余量至少为68、44。正空洞跨度行由 `R_p+R_q+δ−4z≤454−I−82j` 加强为 `R_p+R_q+δ−3z≤393−I−82j`，同一实际状态的改进为 `61+z`；同时增强三类质量行。2,916个实际集合检查及空洞损失因子2的锐例仅作一般证明的佐证。

110个固定评分之间有1,510个系数可证的顺序关系，由180条覆盖关系生成。利用这些关系约束高项与非正项指标，再把209个二元、7,736个三元符号蕴涵压缩为46条必要约束。验证器从原始评分重建全部系数、传递闭包与见证；压缩依据实际布尔指标，不把它误称为分数松弛之间的线性等价。搜索以残余损失为目标选择已证明的二分，每个分支仍须有精确整数反证。

[upper89.py](verification/upper89.py) 重建30,396个结构组、440,904个整数根系统，其中29,819组使用粗模型、577组使用嵌套模型。33个树根包含339个二分节点；[新增的1,534组整数证书](data/upper89_certificates.json)覆盖441,243个最终叶系统，最小规范化严格余量为`1/748`。高空洞来源到合并模型的粗／嵌套两类逐行检查共740,143项。

标准库隔离模式、完整逐点核验、50项负面控制、`-O`逐字节一致性、独立证书再生成及upper90基础回归全部通过。[完整结果与回执](results/2026-10-18/upper89/)包含压缩的完整结果、前缀见证、评分顺序与符号约束、方法使用统计、输入哈希和运行记录；[可选生成器](experiments/generate_upper89_certificates.py)仅用于发现证书。本轮完整逐点核验由[标准库分批驱动](experiments/verify_upper89_sharded.py)分8批完成，每个根组恰好出现一次，全部逐组结果与标准模式一致；先前中断的连续运行另行记为未完成。下一端点为`n=89`，当前程序拒绝据此认证上界88。归档84仍待完整独立复核。

运行继承的 84/85 检查：

```bash
python verification/upper84/verify84.py --full
```

本次结果：**11/11 套件通过**，其中含原 upper-85 full suite。原程序中的 `--full` 指该包包含的有限组件，**不包含**另行保存的完整 upper-86 历史端点链。

## 上界 86 的完整程序

原始 ZIP 大小 116,323,869 字节，保存在 `archive/upper86/` 的28 个分片中，每片不超过 4 MiB。分片只是文件存储方式，内容未删改。恢复时检查每片以及完整 ZIP 的 SHA-256：

```bash
python verification/unpack_upper86.py
cd .work/upper86/subset_sums_upper86_complete_verification_20261005
python -I -S -B verify_complete_upper86.py
```

完整解压约需 2 GB，全部检查可能需要数小时。2026-10-14 仅运行 `--auxiliary-only`，记录位于 [results/2026-10-14](results/2026-10-14)。**2026-10-18 已用原包的阶段和范围接口完成全新组合重放**，覆盖 19 阶段及附加前提，并核对最终范围并集与运行前后来源清单；这不是一次默认串行命令。组合驱动为 [audit_archived_upper86.py](experiments/audit_archived_upper86.py)，[完整回执](results/2026-10-18/proof_audit/)区分有限计算与一般数学归约。旧 PASS 记录仍原样保留，未冒充本次运行。

原 upper-84 README 中“未收到完整 upper-86 证明”的文字是原文件的历史说明。本仓库已另外补入后来的完整证明和程序，保留旧文件以便核对来源。

## 文件布局

| 路径 | 用途 |
| --- | --- |
| `reports/` | 新研究报告与旧上界报告 |
| `verification/exact.py` | 精确子集和、四重和、独立证书校验 |
| `verification/verify.py` | 新结果的有限检查和负面控制 |
| `verification/review_checks.py` | 本次审查的独立有限边界检查，不认证完整上界 84 |
| `verification/upper103.py` | 115→103 统一证明的精确参数验证与负面控制 |
| `verification/upper100.py` | 103→100 的完整参数、分支、整数证书验证与负面控制 |
| `verification/upper95.py` | 96→95 的尖锐预算、重叠分组、完整三空单元模式及局部二分验证 |
| `verification/upper96.py` | 97→96 的固定方向筛选、高空洞平移合并、选择性细化和完整二分验证 |
| `verification/upper97_simplified.py` | 质量平移、粗界主干与仅五类嵌套例外的同一上界简化证明 |
| `verification/upper97.py` | 98→97 的统一空洞/跨度/损失模型、区间证书与逐点交叉核验 |
| `verification/upper98.py` | 99→98 的符号二次区间证书、完整分支与可选逐点交叉核验 |
| `verification/upper99.py` | 100→99 的六类模型、完整区间覆盖及整数证书验证 |
| `data/upper100_certificates.json` | 189 组整数行权重与全部 2,580 个分支的映射 |
| `data/upper95_certificates.json` | 651 组整数权重、完整参数覆盖和 141 棵穷尽二分树 |
| `data/upper96_certificates.json` | 156 组整数权重、完整参数覆盖和 17 棵穷尽二分树 |
| `data/upper97_simplified_certificates.json` | 94 组整数证书与穷尽的选择性细化树；覆盖 18,280 个模型 |
| `data/upper97_certificates.json` | 209 组整数行权重；3,750 个区间覆盖 45,928 个模型 |
| `data/upper98_certificates.json` | 90 组整数行权重；5,443 个区间覆盖 82,257 个模型 |
| `data/upper99_certificates.json` | 204 组整数行权重；压缩区间覆盖全部 59,206 个模型 |
| `verification/bounded_search.py` | 指定整数盒内的完整穷举 |
| `verification/upper84/` | 原 upper-84 源码、数据、证明，以及其继承的 upper-85 包 |
| `archive/upper86/` | 原 upper-86 全部验证输入，无删节 |
| `data/` | 71 元构造与固定标签的精确证书 |
| `results/2026-10-14/` | 本次真实运行结果，区分完整套件与局部模式 |
| `results/2026-10-16/upper100/` | 最新 103→100 完整运行结果与 103 基础回归结果 |
| `results/2026-10-16/upper99/` | 100→99 完整运行、证书重新生成与 100 基础回归结果 |
| `results/2026-10-16/upper98/` | 99→98 区间验证、逐点交叉核验回执、证书再生成与 99 基础回归 |
| `results/2026-10-16/upper95/` | 96→95 完整核验、逐点摘要、再生成日志、基础回归和运行哈希 |
| `results/2026-10-16/upper96/` | 97→96 完整核验、逐点摘要、生成日志、基础回归和运行哈希 |
| `results/2026-10-16/proof_method/` | 简化证明的完整结果、逐点摘要、再生成日志与实际运行回执 |
| `results/2026-10-16/upper97/` | 98→97 完整核验、证书再生成和 98 基础回归记录 |
| `experiments/` | 探索性搜索；不作为不存在证明 |

编译新报告：

```bash
pdflatex -output-directory reports reports/research_report.tex
pdflatex -output-directory reports reports/research_report.tex
pdflatex -output-directory reports reports/upper103_from115_20261014.tex
pdflatex -output-directory reports reports/upper103_from115_20261014.tex
pdflatex -output-directory reports reports/upper103_from115_20261014.tex
pdflatex -output-directory reports reports/upper100_from103_20261016.tex
pdflatex -output-directory reports reports/upper100_from103_20261016.tex
pdflatex -output-directory reports reports/upper100_from103_20261016.tex
pdflatex -output-directory reports reports/upper99_from100_20261016.tex
pdflatex -output-directory reports reports/upper99_from100_20261016.tex
pdflatex -output-directory reports reports/upper99_from100_20261016.tex
pdflatex -output-directory reports reports/upper98_from99_20261016.tex
pdflatex -output-directory reports reports/upper98_from99_20261016.tex
pdflatex -output-directory reports reports/upper98_from99_20261016.tex
pdflatex -output-directory reports reports/upper97_from98_20261016.tex
pdflatex -output-directory reports reports/upper97_from98_20261016.tex
pdflatex -output-directory reports reports/upper97_from98_20261016.tex
```

也可使用 XeLaTeX 编译同一份英文数学源文件。验证程序不需要 LaTeX。

编译证明方法与97→96续研报告：

```bash
pdflatex -output-directory reports reports/proof_method_20261016.tex
pdflatex -output-directory reports reports/proof_method_20261016.tex
pdflatex -output-directory reports reports/upper96_from97_20261016.tex
pdflatex -output-directory reports reports/upper96_from97_20261016.tex
```

编译96→95报告：

```bash
pdflatex -output-directory reports reports/upper95_from96_20261016.tex
pdflatex -output-directory reports reports/upper95_from96_20261016.tex
```

编译最新90→89报告：

```bash
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=reports reports/upper89_from90_20261018.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=reports reports/upper89_from90_20261018.tex
```

## 2026-10-18：89元端点的局部改进与精确障碍

本轮优化了格化顺序：在较大侧自己的本原格上修复16个失败逆定理方向，先证明前缀平移相交，再使用格上剥离预算。保留同一个空洞参数的390项见证给出`ρP+ρQ−2z≥81`，将R段预算从`329−I`改进到`313−I<4d`，提前排除整个四空单元R4家族。

覆盖方法新增核心重叠、剥离点吸收、零空洞的双向分位约束、两重和集的区间外计数及区间并集去重。两个特殊零空洞模式仍保留原有固定评分约束。

[进展验证器](verification/upper88_progress.py)检查387组整数权重，排除3,651个结构组、95,443个整数根系统；38个二分节点产生95,481个最终叶系统。8批逐整数展开与符号区间结果一致，普通及`-O`输出逐字节一致。另有48,734项检查将生成的几何矩阵直接代入实际集合。

**这些是部分证书。** 完整候选域有61,884组、641,524个整数根系统，仍有58,233组不在该证书中。尤其，[精确松弛见证](data/upper88_relaxation_witness.json)在`a=b=36`满足450个变量的非负性、1,619条根行及682个二分中的一个子分支。因此，继续搜索同一套约束不能排除该模式，需要新的必要条件。这不是原问题的可行集合或反例；全局范围继续保持`71≤N≤89`。

```bash
python -I -S -B verification/upper88_progress.py --output .work/upper88-progress.json
python -I -S -B experiments/verify_upper88_geometric_rows.py --output .work/upper88-geometric-rows.json
```

Windows可运行`verify_upper88_progress_windows.bat`。结果标记为`PASS_PROGRESS_ONLY`，不会把部分覆盖记为全局证明。完整数据、负面控制、逐批输出和执行回执见[results/2026-10-18/upper88_progress](results/2026-10-18/upper88_progress/)。


编译 87→86 中文报告（需 Noto Sans CJK SC 或 Windows 的 Microsoft YaHei）：

```bash
cd reports
xelatex -interaction=nonstopmode -halt-on-error upper86_adoption_20261019.tex
xelatex -interaction=nonstopmode -halt-on-error upper86_adoption_20261019.tex
```
