# Sum-of-Subset：子集和包含于四重和集

研究有限实数集 `A` 满足

\[
\operatorname{FS}(A)=\left\{\sum_{a\in X}a:X\subseteq A\right\}
\subseteq A+A+A+A
\]

时，`|A|` 的最大值。空集和为 0，右侧允许重复使用同一个元素。

**精确最大值尚未确定。目前已独立核查闭合的范围为 71 ≤ N ≤ 100。** 2026-10-16 的续研排除了 103、102、101 三个基数，接续 2026-10-14 已完成的 115→103 论证。归档证明链记载更强的 **71 ≤ N ≤ 84**，但其完整独立复核尚未完成；本次 100 是独立审查与简化的进展，不是对归档 84 的数值改进。

**证明基础：** 已确认构造、新报告和旧基础上界 `N ≤ 115`；旧剥离证明的一处剩余类表述已修正，修正不改变引理结论。新的 115→103 报告沿用该修正，逐项证明所需的后续结构引理。先前审查记录见 [审查报告与勘误](reports/proof_review_20261014.md)。

## 先读什么

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
| 已审查的旧基础上界 `N ≤ 115` | 原始定理条件和基础推导已核对；采用审查报告中的剥离表述修正 |
| **续研上界 `N ≤ 103`** | 从已审查的 115 基础闭合；262 个格化方向、416 个低空洞状态、24 个高空洞参数见证全部精确通过；不依赖旧端点证书 |
| **最新续研上界 `N ≤ 100`** | 接续 103；108 个格化方向、894 个低空洞状态和 431 个高空洞终端状态通过；2,580 个空单元分支由新生成的 189 组整数证书全部排除 |
| 既有证明链 `N ≤ 84` | 完整原报告与程序已保留；84/85 有限套件本次通过；86 仅重跑附加检查，未重跑全部历史端点 |
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
python verification/verify.py --output .work/independent.json
python verification/check_set.py --certificate data/construction71.json
python verification/check_set.py --elements -1 0 1
python verification/upper103.py --output .work/upper103.json
python -I -S -B verification/upper100.py --output .work/upper100.json
```

Windows 可将 `python` 换成 `py -3`。双击 `verify_windows.bat` 检查构造与基础有限证书；双击 `verify_upper100_windows.bat` 检查 115→103→100 的两段续研有限验证。

校验自己的集合时，可以传入整数或有理数字符串，例如 `--elements -1/3 0 1/3`。也可使用 `--input candidate.json`，文件格式为 `{"A":[-1,0,1]}`。重复元素和浮点输入会被拒绝；触发资源上限时会报“无法得出结论”，不会误报不可行。

`upper103.py` 只用整数与有理数，检查报告中全部有限参数不等式；无限论证与适用条件由正文证明。普通模式与 `python -O` 的输出逐字节一致，两个故意失效的空洞参数均被拒绝。[本次完整结果](results/2026-10-14/upper103/result.json) 也记录了下一端点的障碍：`n=103, a=b=43, z=0` 时只能得到覆盖余量 `c≤116`，大于单元容量 `d=95`，因此尚不能继续套用“全部单元非空”的证书。这不是一个 103 元可行构造。

**2026-10-16 已解决上述障碍。** `upper100.py` 重建完整分支集合，读取 [整数证书](data/upper100_certificates.json)，逐项检查非负行组合给出严格矛盾；运行不需要 SciPy、求解器或第三方包。[完整结果](results/2026-10-16/upper100/result.json) 与 [运行记录](results/2026-10-16/upper100/run_receipt.json) 保存此次核验。普通模式与 `-O` 结果一致，7 项负面控制全部拒绝错误输入。可选的 [证书生成器](experiments/generate_upper100_certificates.py) 使用 SciPy 搜索候选权重，但只有经过精确整数验证的权重才会保存。新验证器不读取旧端点证书。

新的障碍位于 `n=100, a=41, b=42, z=0`：当前预算允许 `c≤184=2d`，因此下一步需要处理两个空覆盖单元。当前程序明确拒绝把这一端点误报为已排除。

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

完整解压约需 2 GB，全部检查可能需要数小时。**本次没有运行最后一条完整命令**，只运行了其 `--auxiliary-only` 模式并通过。完整历史运行记录仍在原包中；新记录位于 [results/2026-10-14](results/2026-10-14)。哈希检查、旧 PASS 记录和附加检查都不能替代完整数学重跑。

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
| `data/upper100_certificates.json` | 189 组整数行权重与全部 2,580 个分支的映射 |
| `verification/bounded_search.py` | 指定整数盒内的完整穷举 |
| `verification/upper84/` | 原 upper-84 源码、数据、证明，以及其继承的 upper-85 包 |
| `archive/upper86/` | 原 upper-86 全部验证输入，无删节 |
| `data/` | 71 元构造与固定标签的精确证书 |
| `results/2026-10-14/` | 本次真实运行结果，区分完整套件与局部模式 |
| `results/2026-10-16/upper100/` | 最新 103→100 完整运行结果与 103 基础回归结果 |
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
```

也可使用 XeLaTeX 编译同一份英文数学源文件。验证程序不需要 LaTeX。
