# 83 → 82：完整证明和精确有限核验

本目录对应 `reports/upper82_complete_20261019.tex` / `.pdf`。数学正文是 `proof.md`。
报告负责任意集合的结构归约与每条资源不等式的适用性；程序重建全部有限状态，并用整数、有理数检验证书。
这不是 Lean、Coq 等形式化证明助手的认证。

## 运行

需要 Python 3.10 或更新版本，仅用标准库，不需要 NumPy、SciPy、求解器或网络。在仓库根目录运行：

```text
python -I -S -B verification/upper82_global/check.py --output results/local_upper82.json
```

Windows 可双击 `run_windows.bat`，或将上面的 `python` 换为 `py -3`。优化模式也必须得到同一个 `finite_digest`：

```text
python -I -S -B -O verification/upper82_global/check.py --output results/local_upper82_optimized.json
```

只有完整入口返回 `PASS_COMPLETE_FINITE_REPLAY`。`--new-only` 跳过旧 83 上界与 alpha 分支的重新运行，明确返回 `PASS_NEW_FINITE_CHECKS_ONLY`，不能作为完整验证回执。

## 检查内容

- `structure.py`：大小 83 的新结构预算、22 个逆定理修复行、等差例外、小侧边界、高洞与低洞局部化。
- `geometry.py`：136 条固定空隙排除证书、分母 42 的剩余类目录、全整数及部分整数活动分类、全非空接口。
- `coverage.py`：独立生成所有主状态，逐个比较集合，检查端点二叉树的互补性，以及无所有者和小松弛接口的完整性。
- `model.py`：从原始状态重建必要不等式；逐个整数截失秩、逐个质量域顶点验证端点平面。
- `replay.py`：检查实际森林、固定标签的 LOW/HIGH 推论、每次信用更新和最终整数反证。只重建证书用到的预定义森林行；每条仍需通过许可检查。
- `compression.py`：附加的剩余类压缩交叠引理的实际集合交叉检查；本轮终端证书不依赖该加强。
- `check.py`：统一以上项目，重放旧依赖，核对传递源文件 SHA-256，并运行遗漏分支、错误信用、负权重、错误端点和洞数覆盖等负面控制。

数据位于 `data/upper82_global/`，采用可直接读取的 JSON + gzip。不存在求解器输出的可信性假设：发现证书可用浮点工具，接受证书只用精确运算。结果目录保留每类状态数、整数行组合数、运行日志及标准/优化模式一致性。

## 与旧文件的关系

旧 alpha 报告仍是一个条件性定理，其 `global_upper82_proved=false` 是历史文件的正确范围说明；本轮证明提供了剩余结构和分类接入。旧 83 上界验证器只有一项平台修复：清单中的相对路径统一使用 `/`，以便 Windows 与 Linux 一致。其数学检查和数据未改动；源清单随之更新，完整依赖重新运行。

正式模型的首项上端点右端为 `+1`。目标洞数始终使用当前状态的 `w`，不会被秩核循环变量覆盖。这两点均有专门回归检查；实验稿与受影响证书不作为正式结果发布。
