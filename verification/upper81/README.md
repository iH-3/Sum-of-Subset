# 大小 82 的排除：精确验证

对应报告：`reports/upper81_complete_20261021.pdf`，可编辑源为同名 `.tex`。

在仓库根目录运行（Python 3.10+）：

```sh
python -I -S -B verification/upper81/check.py --output results/local_upper81.json
python -I -S -B -O verification/upper81/check.py --output results/local_upper81_O.json
```

Windows 可运行 `verification/upper81/run_windows.bat`。验证只依赖 Python 标准库，不需要求解器、第三方包或网络。

完整入口核验：

1. 已有上界 82 的完整有限依赖和本次采用的勘误。
2. 大小 82 的结构算术、共同单位与等差例外、全部高洞和低洞局部化。
3. 136 个通用固定空隙证书，以及不要求核心本原的 22 个小松弛接口。
4. 全部 4,654 个统一参数根，对应 121,403 个实际参数根；所有端点、计数、位移条件分支都检查互补覆盖。
5. 每条 LOW/HIGH、固定扣减、根森林、端点平面、尾部不相容及整数反证；对子域继承先验证父证书和域包含关系。
6. 缺失根、重复根、缺少补支、错误乘数、零反证余量、无依据扣减、错误端点平面和修改源文件等负面控制。

只有全部通过才返回 `PASS_COMPLETE_FINITE_REPLAY` 并报告上界 81。两种模式的 `finite_digest` 应一致。`--new-only` 只核对新增有限部分，返回 `PASS_NEW_FINITE_CHECKS_ONLY`，不会认证完整新上界。

程序重建每条必要行，用精确整数或有理数验证反证；不把浮点不可行状态当成证明。任意集合到这些有限系统的适用性由报告给出。这不是形式化证明助手认证。

`data/upper81_sources.json` 固定正文、程序、数据及旧基础传递依赖的 SHA-256。修改这些文件后验证器会拒绝通过，直到重新审查并重建清单。
