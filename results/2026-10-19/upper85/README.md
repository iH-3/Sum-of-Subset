# 86→85：本轮证明与复现记录

接续 `f111002` 的独立上界 86，本轮完成大小 86 的结构归约与全部 13 类实际情形接入，得到 **71 ≤ N ≤ 85**。归档 84 尚待大小 85 的独立接入；本轮没有确定精确最大值。

- [8 页报告 PDF](../../../reports/upper85_adoption_20261019.pdf) / [LaTeX](../../../reports/upper85_adoption_20261019.tex)
- [完整验证入口](../../../verification/upper85.py)、[新增解析与分类检查](../../../verification/upper85_geometry.py)、[故意篡改控制](../../../experiments/check_upper85_controls.py)
- [55 个固定源文件与 140 个检查编号](../../../data/upper85_adoption_sources.json)
- [数学结论与计数](summary.json)、[文字证明审阅索引](proof_review.json)、[PDF 审阅](report_review.json)
- [普通回放](full_replay.json)、[优化回放](optimized_replay.json)、[空格与中文路径回放](unicode_replay.json)、[数学结果一致性](comparison.json)
- [全部 140 项逐项记录](coverage.json)、[新增检查结果](geometry.json)、[6 项负面控制](controls.json)
- [三次完整日志与覆盖 ZIP](execution_logs.zip)、[ZIP 内容哈希与读回核对](execution_manifest.json)

新引理在原实际覆盖中证明 `j=0 ⇒ w≥2|D|−36`，因此 `|D|=78,w≤119 ⇒ c≥78`。它替换 152 个结构例外系统并消去两个本原性等号例外。两种截断深度共同把单空单元终端从 `131−w` 加强至 `136−w`，必要偶洞数从 50 提高到 54。

三次完整回放均为 **140 PASS、0 FAIL、0 SKIP**。移除环境和计时字段后，逐项数学记录相同；新增几何 JSON 逐字节相同。6 项故意篡改全部被拒绝。旧 152 个系统额外回放作为回归检查，但新的结构论证不再依赖其证书。

## 复现

Python 3.10+，仅标准库，不需要网络或求解器。在仓库根目录执行：

```bash
python -I -S -B verification/upper85.py --output .work/upper85.json
python -I -S -B -O verification/upper85.py --output .work/upper85_O.json
python -I -S -B experiments/check_upper85_controls.py --output .work/controls85.json
```

完整入口只复制清单内源文件到新临时目录，重算全部有限检查，并在结束时复查源文件和检查编号。回执保留运行时的临时绝对路径，仅作来源记录；复现程序不依赖那些路径。

Windows 可双击根目录 `verify_upper85_windows.bat`。本轮在 Linux 上完成启动器静态检查和中文路径完整回放，未声称实际运行过 Windows。报告用 XeLaTeX 编译，支持 Noto Sans CJK SC 或 Microsoft YaHei。

实际集合到活动条件的蕴涵、一般定理和无限归纳由报告及固定源中的文字证明承担。分类程序枚举的是给定解析前提后的布尔活动指派；标量程序检查的是必要松弛参数域。有限 PASS 不是证明助手形式化认证。各计数对应不同对象，不可相加称为实际集合总数。
