# EP_Veg Replication (Journal of Hydrology, 2023) | 植被响应的潜在蒸散模型复刻

> A physically-based potential evapotranspiration model for global water availability projections (Liu et al., 2023).  
> 本仓库复刻并开源实现文中提出的 **EP_Veg** 潜在蒸散模型，以及与 **Budyko** 框架耦合的长时段径流估算。**包含随机数据示例、中文/英文文档与注释、Matplotlib 中文字体适配**。

**Reference | 参考文献**  
Liu, Z., Wang, T., Li, C., Yang, W., Yang, H. (2023). *A physically-based potential evapotranspiration model for global water availability projections*. Journal of Hydrology, 622, 129767.

---

## What’s implemented | 实现内容

- EP models | 潜在蒸散模型
  - `EP_PM_RC` — FAO-56 参考作物 (Eq.13)
  - `EP_Yang` — CO₂ 响应的经验修正 (Eq.14–15)
  - `EP_Veg` — **本文核心模型**：由最优气孔导度 + 体尺度上推得到表面阻力，嵌入 Penman–Monteith (Eq.1–3, 7)
- Budyko 函数与径流估算 (Eq.11–12)
- 参数方案
  - `g1(T, MI)` （Lin et al., 2015，Eq.8，此处提供自然对数/常用对数可选）
  - `Aww(Ca)` 线性响应（默认斜率 `S=7.5%`，可选物种特异：树 12%、草 4%、灌丛 7%，Eq.10）
- 实用工具
  - VPD 计算、饱和水汽压与斜率 Δ、心理温度常数 γ、潜热 λ 等
  - Matplotlib 中文/英文字体自动适配，负号显示修正

> **单位体系**：遵循 FAO-56/文献习惯，`Rn` 用 MJ·m⁻²·d⁻¹，`T(°C)`，`U2(m·s⁻¹)`，`VPD(kPa)`；
> `EP` 输出为 `mm·d⁻¹`。

---

## Install | 安装

```bash
pip install -e .
```

> 需要 `numpy`, `pandas`, `matplotlib`。本仓库不依赖网络下载数据，示例使用**随机生成**的合成数据。

---

## Quick Start | 快速开始

```bash
python examples/run_quick_demo.py
```

该脚本将：
1) 生成 365 天的随机气象与植被数据；  
2) 计算 `EP_PM_RC / EP_Yang / EP_Veg` 与 Budyko 径流；  
3) 在 `figures/` 输出对比图（已自动适配中英文字体）。

---

## Repository Layout | 仓库结构

```
ep_veg_repro/
├─ src/ep_veg/
│  ├─ __init__.py
│  ├─ parameters.py   # g1 / Aww / 常数与单位换算
│  ├─ gs.py           # gls (M2011) → ges → rs
│  ├─ pm.py           # EP_PM_RC / EP_Yang / EP_Veg
│  ├─ budyko.py       # Budyko 函数与径流计算
│  └─ utils.py        # VPD/Δ/γ/λ/字体工具等
├─ examples/
│  └─ run_quick_demo.py
├─ figures/           # 示例图输出目录
├─ tests/
│  └─ test_basic.py
├─ README.md
├─ LICENSE
└─ pyproject.toml
```

---

## Notes & Assumptions | 说明与假设

- **EP_Veg 实现**：采用文中 M2011 气孔导度（Eq.1），以 LAI 线性上推（Eq.2–3）得到表面阻力 `rs`，再代入 PM（Eq.4）与 FAO-56 的 `ra≈208/U2`（Eq.6）形成 Eq.7 的数值实现。  
  文中排版将常数合并为 `0.14U2` 等项，我们则保留“先算 `rs/ra` 再代入”的**物理直观写法**（结果应保持一致量级）。
- **g1 的对数底**：原式未明确底数，代码同时支持 `log10` 与 `ln`（默认 `ln`），并暴露可切换开关。  
- **Aww–Ca**：默认 `S=7.5%`；如指定 `species` 将采用文表中的物种特异斜率（树/草/灌丛）。
- **等式与变量出处**：详见源码注释中的公式编号。

---

## Citation | 引用

If you use this repository, please cite the original paper:  
Liu et al. (2023) Journal of Hydrology 622:129767.

---

## License | 许可协议

MIT
