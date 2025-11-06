# hydro-co2 (Yang et al. 2018 Replica Utilities)

> 🇨🇳 **中文简介在下方**

This repository re-implements the key hydrologic pieces from **Yang et al. (2018, Nature Climate Change)** — the
[CO2]-aware Penman–Monteith potential evapotranspiration (PM-[CO2]) and a Budyko runoff comparison — with
fully runnable **synthetic examples** (no external data required). It is structured like a standard GitHub Python
package (`pyproject.toml`, `src/`, `examples/`, `tests/`) and includes **bilingual (EN/中文) code comments** as well as
**Chinese/English font handling** in Matplotlib figures.

> **Important:** This is a didactic replica that follows the paper’s equations and logic on synthetic data and
does *not* reproduce the full CMIP5 workflow. Please cite the original paper if these ideas help your work.

- Paper: Yang, Y., Roderick, M. L., Zhang, S., McVicar, T. R., & Donohue, R. J. (2019).
  *Hydrologic implications of vegetation response to elevated CO2 in climate projections.* Nature Climate Change, 9, 44–48. https://doi.org/10.1038/s41558-018-0361-0

## What’s included

- **Penman–Monteith variants**
  - `PM_OW` (open water; Eq. 4 in Methods)
  - `PM_RC` (FAO-56 reference crop; Eq. 5)
  - `PM_CO2` (reference crop modified to include [CO2]; Eq. 14)
  - General `penman_monteith(E)` helpers, psychrometric constants, saturation-slope, latent heat, etc.
- **rs–[CO2] function (Eq. 1)** and a simple inverter to estimate `rs` from given `E` (for teaching).
- **Attribution** of ΔE into components (ΔRn*, ΔD, Δrs, Δra, Δs) via first-order partials (Eqs. 6–12).
- **Budyko (Choudhury, 1999) partition** and a ΔQ comparison between PM-OW/PM-RC/PM-[CO2].
- **Examples** creating monthly synthetic climate series (1861–2100), plotting rs–CO2 relationships,
  attribution bars, and runoff changes consistent with the paper’s logic.
- **Robust CN/EN font setup** to avoid missing glyphs for Chinese labels.

## Install & Run

```bash
# (Optional) create a fresh environment
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# run examples
python examples/01_synthetic_timeseries.py
python examples/02_compare_EP_methods.py
python examples/03_budyko_runoff_demo.py
```

## Font notes (CN/EN)

Figures try to use one of the following sans-serif fonts in order:
`Noto Sans CJK SC`, `SimHei`, `Microsoft YaHei`, `PingFang SC`, `Source Han Sans SC`, falling back to Matplotlib defaults.
If you still see tofu boxes ▯▯▯, please install one of the listed fonts and re-run.

---

## 🇨🇳 中文说明

本仓库在**合成数据**上复刻了 Yang 等（2018, *Nature Climate Change*）的核心计算：
考虑大气二氧化碳浓度变化的 Penman–Monteith 潜在蒸散（PM-[CO2]），以及基于 Budyko 框架的径流
变化对比。我们提供了**可直接运行的示例**（无需外部数据），仓库结构遵循 GitHub/Python 惯例，
并在**代码注释与 README 中提供中英文双语说明**。绘图部分针对**中英文字体**进行了处理。

> 说明：此复刻用于教学演示，遵循论文给出的公式与思想，并未完整复现 CMIP5 全流程。若相关思路对您有帮助，
> 请引用原论文。

- 论文：Yang 等（2019）。*Hydrologic implications of vegetation response to elevated CO2 in climate projections.*
  Nature Climate Change, 9, 44–48. https://doi.org/10.1038/s41558-018-0361-0

### 已实现功能

- **Penman–Monteith 多版本**
  - `PM_OW`：开阔水面（方法部分公式 4）
  - `PM_RC`：FAO-56 参考作物（公式 5）
  - `PM_CO2`：加入 CO2 影响的参考作物（公式 14）
  - 通用常数与函数：心理常数、饱和水汽压斜率、潜热、等
- **rs–[CO2] 关系（公式 1）**，并提供一个简化的 `rs` 反演用于教学
- **ΔE 归因**（ΔRn*、ΔD、Δrs、Δra、Δs）的一阶近似分解（公式 6–12）
- **Budyko（Choudhury, 1999）分配**与 `ΔQ` 对比（PM-OW / PM-RC / PM-[CO2]）
- **可运行示例**：合成 1861–2100 的月尺度气候序列，绘制 rs–CO2 关系、归因柱状图与径流变化

### 字体建议

绘图将优先尝试：`Noto Sans CJK SC`、`SimHei`、`Microsoft YaHei`、`苹方`、`思源黑体`。
若中文仍显示为方框，请安装上述任一字体。

---

## References

- Yang et al. (2019) *Nature Climate Change* 9, 44–48. https://doi.org/10.1038/s41558-018-0361-0
- Allen et al. (1998) FAO-56; Choudhury (1999) Budyko form; Shuttleworth (1993).
