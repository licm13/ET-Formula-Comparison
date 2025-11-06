\
# -*- coding: utf-8 -*-
"""
01_synthetic_timeseries.py
Create synthetic 1861–2100 monthly series to demonstrate:
- rs increases with [CO2] (Eq. 1)
- PM_CO2 vs PM_RC vs PM_OW
- ΔE attribution bars
"""
import numpy as np
import matplotlib.pyplot as plt
from _font_helper import setup_cn_en_font
from hydro_co2.penman import PM_RC, PM_CO2, PM_OW, aerodynamic_resistance
from hydro_co2.rs_co2 import rs_from_co2
from hydro_co2.attribution import attribute_deltaE

chosen = setup_cn_en_font()

# Synthetic timeline
years = np.arange(1861, 2101)
months = np.arange(12)
t = np.arange(len(years)*12)
rng = np.random.default_rng(42)

# Synthetic CO2 path (ppm): ~300 to ~800
co2 = 300 + (t / t.max()) * 507 + rng.normal(0, 2, size=t.size)

# Synthetic meteorology (monthly)
T = rng.normal(loc=18.0, scale=6.0, size=t.size)          # °C
Rn_star = rng.normal(loc=120.0, scale=20.0, size=t.size)  # W/m^2
D = np.clip(rng.normal(loc=1500.0, scale=400.0, size=t.size), 200, 4000)  # Pa
u2 = np.clip(rng.normal(loc=2.0, scale=0.5, size=t.size), 0.1, None)      # m/s

# EP estimates
ep_rc  = PM_RC(Rn_star, T, D, u2)
ep_co2 = PM_CO2(Rn_star, T, D, u2, co2)
ep_ow  = PM_OW(Rn_star, T, D, u2)

# rs–CO2 relationship (Eq. 1)
rs = rs_from_co2(co2)

# Plot rs vs CO2
plt.figure(figsize=(7,4))
plt.scatter(co2[::20], rs[::20], s=8, alpha=0.6)
plt.xlabel("CO$_2$ (ppm) / 二氧化碳浓度")
plt.ylabel("Surface resistance r$_s$ (s m$^{-1}$) / 表面阻力")
plt.title("rs–CO$_2$ synthetic relationship / 合成的 rs–CO$_2$ 关系")
plt.tight_layout()
plt.savefig("examples_out_01_rs_co2.png", dpi=180)
plt.close()

# Attribution demo at two states (baseline vs future mean)
# Baseline: first 30 years; Future: last 30 years
def monthly_mean(arr, start_yr, end_yr):
    idx0 = (years >= start_yr) & (years <= end_yr)
    idx = np.repeat(idx0, 12)
    return np.mean(arr[idx])

state_base = dict(
    Rn_star = monthly_mean(Rn_star, 1861, 1890),
    T       = monthly_mean(T,       1861, 1890),
    D       = monthly_mean(D,       1861, 1890),
    u2      = monthly_mean(u2,      1861, 1890),
    co2     = monthly_mean(co2,     1861, 1890),
)
state_fut = dict(
    Rn_star = monthly_mean(Rn_star, 2071, 2100),
    T       = monthly_mean(T,       2071, 2100),
    D       = monthly_mean(D,       2071, 2100),
    u2      = monthly_mean(u2,      2071, 2100),
    co2     = monthly_mean(co2,     2071, 2100),
)

# Build rs via Eq.1, ra via simple function
ra_base = aerodynamic_resistance(state_base["u2"])
ra_fut  = aerodynamic_resistance(state_fut["u2"])
rs_base = rs_from_co2(state_base["co2"])
rs_fut  = rs_from_co2(state_fut["co2"])

# Δ terms
dRn = state_fut["Rn_star"] - state_base["Rn_star"]
dD  = state_fut["D"]       - state_base["D"]
dra = ra_fut - ra_base
drs = rs_fut - rs_base

# Attribute ΔE (mm/day) using first-order approximation at baseline state
parts = attribute_deltaE(
    Rn_star=state_base["Rn_star"], T=state_base["T"], D=state_base["D"],
    ra=ra_base, rs=rs_base,
    dRn=dRn, dD=dD, dra=dra, drs=drs, ds=0.0
)

labels = ["ΔE from ΔRn*", "ΔE from ΔD", "ΔE from Δrs", "ΔE from Δra"]
values = [parts["dE_from_Rn"], parts["dE_from_D"], parts["dE_from_rs"], parts["dE_from_ra"]]

plt.figure(figsize=(7,4))
plt.axhline(0, lw=1)
plt.bar(np.arange(len(values)), values)
plt.xticks(np.arange(len(values)), labels, rotation=20)
plt.ylabel("ΔE (mm/day) / 蒸散变化")
plt.title("First-order attribution of ΔE / 一阶近似 ΔE 归因（合成示例）")
plt.tight_layout()
plt.savefig("examples_out_01_attribution.png", dpi=180)
plt.close()

# Compare EP methods over time
plt.figure(figsize=(8,4))
plt.plot(ep_rc,  label="PM_RC")
plt.plot(ep_co2, label="PM_CO2")
plt.plot(ep_ow,  label="PM_OW")
plt.legend()
plt.xlabel("Month index / 月序号")
plt.ylabel("EP (mm/day) / 潜在蒸散")
plt.title("PM variants comparison (synthetic) / PM 多版本对比（合成）")
plt.tight_layout()
plt.savefig("examples_out_01_pm_compare.png", dpi=180)
plt.close()

print("Saved: examples_out_01_rs_co2.png, examples_out_01_attribution.png, examples_out_01_pm_compare.png")
