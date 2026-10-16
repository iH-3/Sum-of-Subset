# Sum-of-Subset：子集和包含于四重和集

研究有限实数集 `A` 满足

\[
\operatorname{FS}(A)=\left\{\sum_{a\in X}a:X\subseteq A\right\}
\subseteq A+A+A+A
\]

时，`|A|` 的最大值。空集和为 0，右侧允许重复使用同一个元素。

**精确最大值尚未确定。目前已独立核查闭合的范围为 71 ≤ N ≤ 96。** 2026-10-16 的多轮续研先排除 103、102、101，再排除 100、99、98、97，接续 2026-10-14 已完成的 115→103 论证。归档证明链记载更强的 **71 ≤ N ≤ 84**，但其完整独立复核尚未完成；本次 96 是独立审查与简化的进展，不是对归档 84 的数值改进。

**证明基础：** 已确认构造、新报告和旧基础上界 `N ≤ 115`；旧剥离证明的一处剩余类表述已修正，修正不改变引理结论。新的 115→103 报告沿用该修正，逐项证明所需的后续结构引理。先前审查记录见 [审查报告与勘误](reports/proof_review_20261014.md)。

## 先读什么

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
| 已审查的旧基础上界 `N ≤ 115` | 原始定理条件和基础推导已核对；采用审查报告中的剥离表述修正 |
| **续研上界 `N ≤ 103`** | 从已审查的 115 基础闭合；262 个格化方向、416 个低空洞状态、24 个高空洞参数见证全部精确通过；不依赖旧端点证书 |
| **续研上界 `N ≤ 100`** | 接续 103；108 个格化方向、894 个低空洞状态和 431 个高空洞终端状态通过；2,580 个空单元分支由新生成的 189 组整数证书全部排除 |
| **续研上界 `N ≤ 99`** | 排除 100 元端点；38 个格化方向、364 个低空洞状态及 966 个高空洞终端状态通过；59,206 个线性模型由重新生成的 204 组整数证书全部排除 |
| **续研上界 `N ≤ 98`** | 排除 99 元端点；39 个格化方向、391 个低空洞状态、1,217 个高空洞终端状态通过；90 组新整数证书，5,443 个符号区间覆盖 82,257 个线性模型，全部逐点交叉核验通过 |
| **续研上界 `N ≤ 97`** | 排除 98 元端点；结构参数检查不变。新简化证明使用 94 组整数证书、1,455 次区间检查，覆盖 18,280 个模型，全部逐点核验通过；原 209 组证书版本保留 |
| **最新续研上界 `N ≤ 96`** | 排除 97 元端点；41 个格化方向、437 个低空洞状态、2,200 个高空洞状态通过；412 个待处理高空洞状态合并为 17 组。156 组证书、2,085 次区间检查和 52 个二分树叶检查覆盖 23,303 个最终叶系统，全部逐点核验通过 |
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
python -I -S -B verification/upper99.py --output .work/upper99.json
python -I -S -B verification/upper98.py --output .work/upper98.json
python -I -S -B verification/upper97.py --output .work/upper97.json
# 简化后的同一上界证明
python -I -S -B verification/upper97_simplified.py --output .work/upper97_simplified.json
# 最新 97→96 续研
python -I -S -B verification/upper96.py --output .work/upper96.json
# 可选：逐个整数复核最新模型与区间极值
python -I -S -B verification/upper96.py --exhaustive
```

Windows 可将 `python` 换成 `py -3`。双击 `verify_upper96_windows.bat` 检查完整的 115→103→100→99→98→97→96 六段有限续研。双击 `verify_windows.bat` 检查构造与基础有限证书；双击 `verify_upper97_windows.bat` 依次检查 115→103→100→99→98→97 的五段续研有限验证。也可双击 `verify_upper97_simplified_windows.bat`，以本轮简化证明替代最后一段。旧入口仍保留。

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

**最新 97→96 续研解决了这个端点的新例外。** [upper96.py](verification/upper96.py) 对两个空单元统一使用核心计数约束，避免把正低空洞余量 46 错当作小于普通计数阈值 45。质量平移进一步把 117 个高空洞全非空状态与 295 个一空单元状态合并为 17 组端点模型：原本需要 21,118 个高空洞模型，合并后只需 662 个，且全部由粗界排除。

覆盖估计必须先按第一对的实际贡献者固定反射方向，再计算该方向的两个分支下界；不能任取反射后较大的下界。报告给出 `(a,b,z)=(47,33,112)` 的明确检查：有效方向余量为 `−1`，错误换向会得到 `377`。这一错误捷径已纳入负面控制。

完整根集合共 1,966 组，其中 1,900 组直接使用粗模型；仅 6 组需要指定大损失中心。细化后共 2,068 个结构组，其中只有 12 组使用三个层级的嵌套包络。剩余 17 个具体整数情形用三类已证明的二分处理，共 35 个内部节点、52 个树叶；每次二分至少一侧立即矛盾，最长链为 10。最终 23,303 个叶系统由 [156 组新整数证书](data/upper96_certificates.json) 全部排除，最小规范化严格余量为 `2/299`。

标准库隔离模式、完整逐点交叉核验、15 项负面控制、`-O` 输出一致性、证书重新生成以及前一版简化 upper97 回归均通过。[完整结果和运行回执](results/2026-10-16/upper96/) 与 [可选生成器](experiments/generate_upper96_certificates.py) 已保存。新程序不读取归档端点证书；正文分别证明必要模型和各二分的穷尽性，包括质量平移后上端点的处理。

下一端点是 `n=96`：零空洞的覆盖余量可达 268，超过三个空单元的成本 `3×88=264`；一个空单元后的余量 180 也允许两个损失至少 84 的中心。现有根集合及“至多一个大损失中心”规则不能直接沿用。这些是必要预算中的障碍，不是可行构造；当前新验证器明确拒绝认证上界 95。

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
| `verification/upper96.py` | 97→96 的固定方向筛选、高空洞平移合并、选择性细化和完整二分验证 |
| `verification/upper97_simplified.py` | 质量平移、粗界主干与仅五类嵌套例外的同一上界简化证明 |
| `verification/upper97.py` | 98→97 的统一空洞/跨度/损失模型、区间证书与逐点交叉核验 |
| `verification/upper98.py` | 99→98 的符号二次区间证书、完整分支与可选逐点交叉核验 |
| `verification/upper99.py` | 100→99 的六类模型、完整区间覆盖及整数证书验证 |
| `data/upper100_certificates.json` | 189 组整数行权重与全部 2,580 个分支的映射 |
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

编译证明方法与最新续研报告：

```bash
pdflatex -output-directory reports reports/proof_method_20261016.tex
pdflatex -output-directory reports reports/proof_method_20261016.tex
pdflatex -output-directory reports reports/upper96_from97_20261016.tex
pdflatex -output-directory reports reports/upper96_from97_20261016.tex
```
