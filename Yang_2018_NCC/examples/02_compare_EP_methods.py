\
# -*- coding: utf-8 -*-
"""
02_compare_EP_methods.py
Demonstrate the difference among PM_OW, PM_RC, and PM_CO2 on synthetic samples.
演示 PM 多版本输出差异。
"""
import numpy as np
import matplotlib.pyplot as plt
from _font_helper import setup_cn_en_font
from hydro_co2.penman import PM_RC, PM_CO2, PM_OW

setup_cn_en_font()

rng = np.random.default_rng(0)
N = 300
T = rng.normal(20, 5, size=N)
Rn_star = rng.normal(130, 25, size=N)
D = np.clip(rng.normal(1600, 450, size=N), 200, 4500)
u2 = np.clip(rng.normal(2.0, 0.6, size=N), 0.1, None)
co2 = rng.uniform(300, 800, size=N)

y1 = PM_OW(Rn_star, T, D, u2)
y2 = PM_RC(Rn_star, T, D, u2)
y3 = PM_CO2(Rn_star, T, D, u2, co2)

plt.figure(figsize=(7,4))
plt.scatter(y2, y3, s=12, alpha=0.6, label="PM_RC vs PM_CO2")
plt.scatter(y1, y2, s=12, alpha=0.5, label="PM_OW vs PM_RC")
plt.xlabel("X (mm/day) / 横轴蒸散")
plt.ylabel("Y (mm/day) / 纵轴蒸散")
plt.title("Comparison among PM variants / 不同 PM 版本的比较")
plt.legend()
plt.tight_layout()
plt.savefig("examples_out_02_scatter.png", dpi=180)
plt.close()
print("Saved: examples_out_02_scatter.png")
