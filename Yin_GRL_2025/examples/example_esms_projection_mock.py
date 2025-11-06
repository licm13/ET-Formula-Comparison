"""
example_esms_projection_mock.py

构造“历史 vs 未来”两个时期的合成 P 与 PET，模拟
- ΔP/P、ΔPET/PET、ΔD0/D0，
- 以及“变干区域”（DI_future > DI_hist）的面积比例。

注意：这里只是“流程复刻”，非真实结论。
"""
import numpy as np
from di_global.datasets import global_latlon_grid, synthetic_P_PET
from di_global.compute import dryness_index, area_weights_from_lat

def main():
    lon2d, lat2d = global_latlon_grid(1.0, 1.0)
    # 历史期
    P_h, PET_h = synthetic_P_PET(lon2d, lat2d, mean_P=1000.0, mean_PET=1200.0, seed=1)
    # 未来期（假设变暖导致 PET 上升更快，P 略增）
    P_f = P_h * 1.08     # +8%
    PET_f = PET_h * 1.17 # +17%

    D0_h = float(PET_h.mean() / P_h.mean())
    D0_f = float(PET_f.mean() / P_f.mean())

    DI_h = dryness_index(P_h, PET_h)
    DI_f = dryness_index(P_f, PET_f)

    w = np.cos(np.deg2rad(lat2d))  # 面积权重 ~ cos(lat)
    w = np.clip(w, 0.0, None)

    drier_mask = (DI_f > DI_h)
    frac_drier = float((w[drier_mask].sum()) / (w.sum()))

    print(f"D0_h = {D0_h:.4f}, D0_f = {D0_f:.4f}, ΔD0/D0 = {(D0_f-D0_h)/D0_h:.3f}")
    print(f"Fraction area getting drier (DI_future > DI_hist): {frac_drier:.3f}")

if __name__ == "__main__":
    main()
