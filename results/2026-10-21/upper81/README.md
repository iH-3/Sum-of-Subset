# 上界 81：完整运行回执

普通与 `-O` 模式均返回 `PASS_COMPLETE_FINITE_REPLAY`，报告上界 81。
两次的有限结果、已有 82 基线摘要、源清单摘要、覆盖结果和错误输入检查一致。

| 核验 | 结果 |
| --- | --- |
| 固定依赖文件 | 198 |
| 统一参数根 / 实际参数根 | 4,654 / 121,403 |
| 主终端反证 | 4,853 |
| 互补分支 / 分支根 | 199 / 12 |
| 小松弛接口 | 22 个模式全部排除 |
| 错误输入控制 | 10 项全部拒绝 |
| 普通模式耗时 | 1234.430 秒 |
| 优化模式耗时 | 1256.433 秒 |

有限结果摘要：`8594ce625131c7fb931d4c1e20f72050054e8b71269ff640dec03b6a49fe4160`。

`normal.json` 和 `optimized.json` 是两次完整入口的回执。`normal_details/` 保存各模块的有限结果；两种模式的运行日志分别为 `normal.log` 和 `optimized.log`。旧基础的传递结果可按验证入口重新生成，仓库中保留其既有报告和回执。

在仓库根目录复现：

```sh
python -I -S -B verification/upper81/check.py --output results/local_upper81.json
python -I -S -B -O verification/upper81/check.py --output results/local_upper81_O.json
```

任意实际集合到有限必要系统的数学依据见修订报告；有限重放不等同于形式化证明助手认证。
