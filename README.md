# Sum-of-Subset：子集和包含于四重和集

研究有限实数集 `A` 满足

\[
\operatorname{FS}(A)=\left\{\sum_{a\in X}a:X\subseteq A\right\}
\subseteq A+A+A+A
\]

时，`|A|` 的最大值。空集和为 0，右侧允许重复使用同一个元素。

**精确最大值尚未确定。** 本项目既有证明链给出 **71 ≤ N ≤ 84**。2026-10-14 的整理保留原始材料，并重跑了下列明确列出的有限检查；不声称已经独立重审整条上界证明。

## 先读什么

- [本次研究报告 PDF](reports/research_report.pdf) · [可编辑 LaTeX](reports/research_report.tex)：约定、完整构造证明、构造族的精确边界、显式整数化界、核验范围和下一步任务。
- [原上界 86 完整报告](reports/upper86_complete_20261005.pdf) · [LaTeX](reports/upper86_complete_20261005.tex)。
- [原上界 85 汇总报告](reports/upper85_consolidated_20261005.pdf) · [LaTeX](verification/upper84/audit/verification_program/proof/report.tex)。
- [原上界 84 补充报告](reports/upper84_supplement_20261005.pdf) · [LaTeX](verification/upper84/proof/report.tex)。
- [研究状态与待办](RESEARCH_STATUS.md)。

## 目前能明确说明什么

| 结论 | 依据与本次状态 |
| --- | --- |
| `N ≥ 71` | 明确构造；重新证明；独立核验全部 3349 个子集和值的四项表示 |
| `N ≤ 122` | 新报告中给出完整初等证明，作为不依赖旧逆定理的独立基线；不是对 84 的改进 |
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
```

Windows 可将 `python` 换成 `py -3`，或双击 `verify_windows.bat`。

校验自己的集合时，可以传入整数或有理数字符串，例如 `--elements -1/3 0 1/3`。也可使用 `--input candidate.json`，文件格式为 `{"A":[-1,0,1]}`。重复元素和浮点输入会被拒绝；触发资源上限时会报“无法得出结论”，不会误报不可行。

运行继承的 84/85 检查：

```bash
python verification/upper84/verify84.py --full
```

本次结果：**11/11 套件通过**，其中含原 upper-85 full suite。原程序中的 `--full` 指该包包含的有限组件，**不包含**另行保存的完整 upper-86 历史端点链。

## 上界 86 的完整程序

原始 ZIP 大小 116,323,869 字节，保存在 `archive/upper86/` 的三个分片中，每片小于 50 MiB。分片只是文件存储方式，内容未删改。恢复时检查每片以及完整 ZIP 的 SHA-256：

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
| `verification/bounded_search.py` | 指定整数盒内的完整穷举 |
| `verification/upper84/` | 原 upper-84 源码、数据、证明，以及其继承的 upper-85 包 |
| `archive/upper86/` | 原 upper-86 全部验证输入，无删节 |
| `data/` | 71 元构造与固定标签的精确证书 |
| `results/2026-10-14/` | 本次真实运行结果，区分完整套件与局部模式 |
| `experiments/` | 探索性搜索；不作为不存在证明 |

编译新报告：

```bash
pdflatex -output-directory reports reports/research_report.tex
pdflatex -output-directory reports reports/research_report.tex
```

也可使用 XeLaTeX 编译同一份英文数学源文件。验证程序不需要 LaTeX。
