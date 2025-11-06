# PDSI_CMIP6 (Python Replicate) · Python 复刻与重构

**English | 中文双语**

This repository is a **clean-room Python reimplementation** of the core workflow described in *“PDSI_CMIP6: an ensemble CMIP6-projected self-calibrated Palmer drought severity index dataset” (Scientific Data, 2025)* (Xiong & Yang). It provides:
- Modular **potential evapotranspiration (EP)** algorithms (PM-RC, PM-RC-CO2, Penman-OW, Priestley–Taylor, Yang–Roderick, Oudin).
- A lightweight, vectorized **(self-calibrated) PDSI** implementation compatible with direct hydrologic inputs (for demonstration).
- **Synthetic demo data** and end-to-end examples (no CMIP6 data required) showing time series, maps, trends, and correlation with soil moisture.
- **Plot utilities** that set up Chinese/English fonts automatically on Matplotlib.
- Thorough **docstrings and bilingual comments**.
- GitHub-ready structure: `pyproject.toml`, `tests/`, `examples/`, `docs/`.

> ⚠️ This code is written from scratch for demonstration/education and **does not reuse** any original MATLAB code. For the research article and the official dataset/code, please refer to the original sources.

---

## 1. Install / 安装

```bash
pip install -e .
```

Python ≥3.9 is recommended. Dependencies are minimal (`numpy`, `scipy`, `xarray`, `matplotlib`, `pandas`).

---

## 2. Quick start / 快速上手

```python
from pdsi_cmip6 import fonts, ep, pdsi, metrics
import numpy as np

# 1) Configure bilingual plot fonts / 配置中英文字体
fonts.configure()

# 2) Generate a tiny synthetic dataset for 30 years monthly on a 2×3 grid
#    生成 30 年（逐月）的 2×3 网格演示数据
nt = 30*12
ny, nx = 2, 3
rng = np.random.default_rng(42)
P  = rng.gamma(shape=2.0, scale=50.0, size=(nt, ny, nx))           # precipitation (mm/month)
tas = rng.normal(loc=15.0, scale=10.0, size=(nt, ny, nx))          # 2m air temperature (°C)
rh  = np.clip(rng.normal(loc=60.0, scale=20.0, size=(nt,ny,nx)), 1, 100)  # relative humidity (%)
ps  = np.full((nt,ny,nx), 101.3)                                   # air pressure (kPa)
u2  = np.clip(rng.normal(loc=2.0, scale=1.0, size=(nt,ny,nx)), 0.1, None) # wind speed (m/s)
Rn  = rng.normal(loc=8.0, scale=2.0, size=(nt,ny,nx))              # net radiation (MJ m-2 d-1)
G   = np.zeros_like(Rn)                                            # soil heat flux ~0 for monthly
CO2 = np.linspace(300, 520, nt).reshape(-1,1,1)                    # CO2 ppm rising

# EP via PM-RC-CO2
EP = ep.pm_rc_co2(tas=tas, rh=rh, ps=ps, u2=u2, Rn=Rn, G=G, co2=CO2)  # mm/day-equivalent

# Hydrologic components (synthetic) / 水文分量（演示）
E   = np.minimum(EP*30, P*0.6)                                     # evaporation ~受限于P
RO  = np.maximum(P - E - 5, 0.0)                                   # runoff 简化估计
R   = np.maximum(P - E - RO, 0.0)                                  # soil recharge
L   = rng.uniform(0, 2, size=(nt,ny,nx))                           # losses to lower layer

# 3) Compute scPDSI
pdsi_obj = pdsi.SelfCalibratedPDSI()
Z, PDSI = pdsi_obj.compute(P=P, EP=EP*30, E=E, R=R, RO=RO, L=L, awc=150.0)

# 4) Simple metrics: linear trend and correlation with soil moisture proxy
soilmoist = rng.normal(size=(nt,ny,nx)) + np.cumsum(R - L - RO - (E-EP*0.1), axis=0)*1e-3
trend = metrics.linear_trend(PDSI)  # slope per year (units of PDSI/yr)
corr  = metrics.temporal_corr(PDSI, soilmoist)
print("trend shape:", trend.shape, "corr range:", np.nanmin(corr), np.nanmax(corr))
```

More runnable scripts are under `examples/`. Run:

```bash
python examples/01_quickstart_synthetic.py
python examples/02_spatial_timeseries_and_trends.py
```

Figures are saved to `./figures/` by default.

---

## 3. Notes on methodology / 方法说明要点

- We expose 6 EP algorithms aligned with the paper (equations & symbols in code docstrings).  
- PDSI implementation follows the classic precipitation–potential (CAFEC) and Z-index recursion, with **grid-wise self-calibration** that re-estimates duration parameters `(p, q)` to improve spatial comparability.  
- The workflow supports both (a) traditional offline use (P, EP → two-layer water balance) and (b) **direct hydrologic inputs** (E, R, RO, L) consistent with the paper’s recommendation of using climate model outputs.  
- Trend, correlation, and masking utilities mirror the paper’s validation and usage examples.

> **Disclaimer / 免责声明**: This repo uses **synthetic/random** data for examples. When replacing with actual CMIP6 fields, care must be taken for units, calendars, masks, conservative remapping, and SSP scenarios.

---

## 4. Fonts for bilingual plots / 中英文字体设置

`pdsi_cmip6.fonts.configure()` tries, in order: `Noto Sans CJK SC` → `SimHei` → `Microsoft YaHei` → default Matplotlib `DejaVu Sans`. It also sets `axes.unicode_minus=False` to avoid minus-sign boxes.  
If you see tofu (□), install a CJK font (e.g., Noto Sans CJK).

---

## 5. Testing / 测试

```bash
pytest -q
```

Light tests validate EP outputs’ shapes/ranges and that PDSI recursion runs without NaNs on synthetic data.

---

## 6. Citation / 引用

If you use this replicate to prototype ideas, please cite the original work by Xiong & Yang (2025, Scientific Data). See `CITATION.cff`.

---

## 7. License / 许可协议

This replication scaffolding is under MIT License. The original article, dataset, and MATLAB code are governed by their respective licenses.

---

*Happy hydrology!* 祝研究顺利！
