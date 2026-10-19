# 87 元端点：本轮成功回执

结论依赖配套报告的一般证明与此前独立上界87。独立范围推进为 **71≤N≤86**，没有宣称优于归档84。

- `summary.json`：结论范围、计数、运行时长和负面控制。
- `replay.json`：8个普通范围、22个补充组件、全部辅助/AP-free依赖和最终并集的成功回执。
- `geometry.json`、`controls.json`：独立重建的 c≥32 组合、直接集合验证及入口保护。
- `auxiliary_replay.json`、`apfree_extensions.json`、`archive_guard_controls.json`：结构、规范域、所选分支及AP-free延伸检查。
- `execution_logs.zip`、`execution_manifest.json`：全部本轮日志、每个实际进程回执、规范域及整数左逆证据，附字节数与SHA-256。诊断目录记录首次被源清单拒绝的尝试，不计入成功证明。
- `report_review.json`：最终PDF逐页检查及来源哈希。

复现（在仓库根目录，Python 3.10+，仅标准库）：

```bash
python -I -S -B verification/upper86.py --jobs 8 --output results/local-upper86.json
python -I -S -B experiments/check_upper86_controls.py --output results/local-upper86-controls.json
```

默认使用全新的系统临时目录。不得用 `-O` 运行完整入口。证书复用冻结归档，数学归约的人工核对与有限精确重放分别记录；不是证明助手形式化认证。
