# 2026-10-19 证明加强与大小 84 的部分进展

状态为 **PASS_PROGRESS_ONLY**。全局范围仍是 **71≤N≤84**，没有完成上界 83 的证明。

- [六页报告 PDF](../../../reports/upper83_progress_20261019.pdf) 与 [LaTeX](../../../reports/upper83_progress_20261019.tex)
- [标准库验证器](../../../verification/upper83_progress.py) 与 [10 文件源清单](../../../data/upper83_progress_sources.json)
- [结果摘要](summary.json)、[完整进展检查](progress.json)、[普通与优化模式对比](comparison.json)
- [证明对应与假设](proof_review.json)、[剩余证明义务与松弛见证](remaining_obligations.json)、[六项负面控制](controls.json)
- [原上界 84 的完整回归](baseline_replay.json) 与 [140 项覆盖记录](baseline_coverage.json)
- [报告审阅](report_review.json)、[运行日志压缩包](execution_logs.zip) 与 [逐文件哈希](execution_manifest.json)

新增通用界为 Theta≤2d+8，以及 Theta+B_s+B_t≤2d+18（具体适用条件见报告）；两者都有实际整数源等号族。实际秩截断给 4tau−2xi_s+2|Q|+11F≥13|E|−25，结合后把已闭合大小 85 的 alpha 余量从 16 提高到 57。

大小 84 的零目标洞部分，在报告说明的共同整数源表示下已排除 j=0,1,6 及 j≥7；j=2..5、完整结构和其他洞数情形仍需处理。数值松弛见证均未被声称为原问题的可行集合。固定容量 84 的尖锐例子只认证外侧顺序模型。

在仓库根目录运行：

```sh
python -I -S -B verification/upper83_progress.py --output .work/upper83_progress.json
python -I -S -B -O verification/upper83_progress.py --output .work/upper83_progress_O.json
python -I -S -B verification/upper84_adoption.py --output .work/upper84_baseline.json
```

需要 Python 3.10+，不需要第三方 Python 包或优化器。普通与 `-O` 输出逐字节相同。Windows 启动器做了五项静态检查，本轮没有在 Windows 上执行。有限采样与回归不替代正文中的无界证明；没有使用证明助手宣称全定理形式化认证。
