\
# -*- coding: utf-8 -*-
"""
03_budyko_runoff_demo.py
Budyko partition with EP from three methods to illustrate ΔQ differences.
基于三种 EP 估算，演示 Budyko 的 ΔQ 差异（合成数据）。
"""
import numpy as np
import matplotlib.pyplot as plt
from _font_helper import setup_cn_en_font
from hydro_co2.penman import PM_RC, PM_CO2, PM_OW
from hydro_co2.budyko import budyko_choudhury

setup_cn_en_font()

rng = np.random.default_rng(7)

# Build two periods: baseline (B) & future (F)
N = 600
T_B = rng.normal(18, 5, size=N)
Rn_B = rng.normal(120, 20, size=N)
D_B = np.clip(rng.normal(1500, 400, size=N), 200, 4000)
u_B = np.clip(rng.normal(2.0, 0.5, size=N), 0.1, None)
co2_B = np.full(N, 300.0)

T_F = T_B + rng.normal(1.2, 0.3, size=N)     # slight warming
Rn_F = Rn_B + rng.normal(5.0, 5.0, size=N)   # small Rn* increase
D_F = D_B + rng.normal(200.0, 120.0, size=N) # higher VPD
u_F = u_B + rng.normal(0.0, 0.1, size=N)
co2_F = np.full(N, 800.0)

# Precip series (mm/day) -> convert to mm/yr by scaling at the end
P_B = np.clip(rng.normal(3.0, 1.0, size=N), 0.1, None)  # mm/day
P_F = P_B + rng.normal(0.0, 0.2, size=N)

EP_B_rc  = PM_RC(Rn_B, T_B, D_B, u_B)
EP_B_co2 = PM_CO2(Rn_B, T_B, D_B, u_B, co2_B)
EP_B_ow  = PM_OW(Rn_B, T_B, D_B, u_B)

EP_F_rc  = PM_RC(Rn_F, T_F, D_F, u_F)
EP_F_co2 = PM_CO2(Rn_F, T_F, D_F, u_F, co2_F)
EP_F_ow  = PM_OW(Rn_F, T_F, D_F, u_F)

# Budyko partition (mm/day) then scale to mm/yr (×365)
def annualize(arr): return np.mean(arr) * 365.0

def eval_pair(PB, EPB, PF, EPF):
    EB, QB = budyko_choudhury(PB, EPB, n=1.9)
    EF, QF = budyko_choudhury(PF, EPF, n=1.9)
    return annualize(QF) - annualize(QB)

dQ_rc  = eval_pair(P_B, EP_B_rc,  P_F, EP_F_rc)
dQ_co2 = eval_pair(P_B, EP_B_co2, P_F, EP_F_co2)
dQ_ow  = eval_pair(P_B, EP_B_ow,  P_F, EP_F_ow)

labels = ["Budyko–PM_RC", "Budyko–PM_[CO2]", "Budyko–PM_OW"]
vals = [dQ_rc, dQ_co2, dQ_ow]

plt.figure(figsize=(7,4))
plt.bar(np.arange(3), vals)
plt.xticks(np.arange(3), labels, rotation=15)
plt.ylabel("ΔQ (mm/yr) / 径流变化")
plt.title("ΔQ comparison across EP methods / 不同 EP 方法的 ΔQ 对比（合成）")
plt.tight_layout()
plt.savefig("examples_out_03_dQ.png", dpi=180)
plt.close()

print("Saved: examples_out_03_dQ.png")
