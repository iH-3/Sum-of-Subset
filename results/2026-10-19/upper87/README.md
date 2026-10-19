# 88 元端点：本次完整运行证据

在此前独立 `N≤88` 基础及本次一般数学接入后，得到 **71≤N≤87**。

这是对归档大小88端点的重新接入与完整精确重放，复用其冻结整数证书，没有声称重新发现证书，也没有声称87数值上优于归档84。数学依据见 [中文报告](../../../reports/upper87_adoption_20261019.pdf) 和 [来源清单](../../../data/upper87_adoption_sources.json)。

- 原始根：1,128,280。
- 普通精确反证：1,127,649；普通池有10,689个整数向量。
- 补充父根：631，与普通分配流的631个空位精确互补。
- 补充子模型743个，二分4,352个，叶5,095个；最终叶共1,132,744个。
- 本次8个普通范围及完整补充阶段全部实际退出0；前后源码完整性通过；总用时556.933秒。
- 新直接集合检查通过，标准与 `-O` JSON逐字节相同。端点完整入口明确拒绝 `-O`，因为冻结内部保留断言。
- 11项算术/启动负面控制及2项范围拼合负面控制通过。

`replay.json` 保存逐范围命令、退出码、身份、计数、严格矛盾余量和日志哈希；`execution_logs.zip` 保存本次原始日志，`execution_manifest.json` 列出每个成员哈希。`geometry.json`、`controls.json` 是新增直接检查结果；`summary.json` 给出汇总。每个单独范围和补充阶段的“partial”标记保留，只有它们的完整拼合才通过总入口。

复现（从仓库根目录，仅Python标准库）：

```bash
python -I -S -B verification/upper87.py --jobs 4 --output .work/replay87.json
python -I -S -B verification/upper87_geometry.py --output .work/geometry87.json
```

显式指定 `--work-dir .work/fresh87` 可保留解压副本和全部本地日志；该目录必须尚不存在。默认使用临时工作目录，最终JSON仍保存。Windows使用 `verify_upper87_windows.bat`，本次未在原生Windows上运行。

只提取和验证已存归档中的 `proofs/exact87/`，不重新运行其它归档端点。程序的有限PASS以报告中的一般数学归约和此前独立上界为前提，不是形式化证明助手认证。
