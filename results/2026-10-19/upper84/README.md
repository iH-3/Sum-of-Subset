# 上界 84：独立接入与新证明

本轮接续 `0a06472` 的独立上界85，完成大小85的结构、13类实际情形与有限依赖的核查，得到 **71≤N≤84**，与原归档上界一致。精确最大值仍未知。

新的通用源参数界由165降到**162**，并给出实际77点源的等号例子。全非空覆盖的洞代价加强为 `w≥2|D|+8`；单空终端由 `107−w` 加强为 `112−w`。最后的alpha分支用三点截断和两条无界一元不等式取代7315状态枚举，矛盾余量至少16。源的等号例子不代表存在可行的85点集合。

- [报告 PDF](../../../reports/upper84_adoption_20261019.pdf) · [LaTeX](../../../reports/upper84_adoption_20261019.tex)
- [完整入口](../../../verification/upper84_adoption.py) · [新增几何检查](../../../verification/upper84_geometry.py) · [负面控制](../../../experiments/check_upper84_controls.py)
- [固定106文件清单](../../../data/upper84_adoption_sources.json)
- [总览](summary.json) · [数学审阅对应](proof_review.json) · [PDF审阅](report_review.json)
- [普通运行](full_replay.json) · [优化模式运行](optimized_replay.json) · [一致性](comparison.json)
- [11个套件](legacy_suites.json) · [140条完整记录](coverage.json) · [新几何结果](geometry.json) · [7项控制](controls.json)
- [完整日志 ZIP](execution_logs.zip) · [逐文件哈希](execution_manifest.json)

在仓库根目录复现：

```sh
python -I -S -B verification/upper84_adoption.py --output .work/upper84.json
python -I -S -B -O verification/upper84_adoption.py --output .work/upper84_O.json
python -I -S -B experiments/check_upper84_controls.py --output .work/controls84.json
```

仅需Python 3.10+标准库。两次完整回放均通过11/11顶层套件和140/140继承检查，无失败或跳过；新几何结果逐字节相同，旧结果去除环境与计时字段后一致。`-O` 仅用于新入口与显式判定的新几何检查，旧套件始终启用断言。第二次完整运行使用带中文和空格的目录。

Windows启动器仅作静态检查，未在Windows上实跑。日志包只保留此次新运行生成的文件。旧7315状态仍重放作为额外交叉检查。程序验证声明的有限命题，实际集合蕴涵和无限证明见报告及固定原证明；这些记录不是证明助手的形式化认证。
