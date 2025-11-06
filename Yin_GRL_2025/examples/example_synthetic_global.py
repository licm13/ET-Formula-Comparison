"""
example_synthetic_global.py

使用合成全球格点（1°）数据演示：
- 构造 P（指数分布，均值随纬度略变）与 PET（次峰出现在±25°附近）
- 计算 DI，并构建面积权重直方图
- 绘制经验 pdf 与理论 pdf（Yin & Porporato, 2023）对比
"""
import numpy as np
from matplotlib import pyplot as plt

from di_global.datasets import global_latlon_grid, synthetic_P_PET
from di_global.compute import dryness_index, area_weights_from_lat, weighted_histogram
from di_global.theory import p_DI
from di_global.plots import plot_empirical_vs_theory

def main():
    lon2d, lat2d = global_latlon_grid(1.0, 1.0)
    P, PET = synthetic_P_PET(lon2d, lat2d, mean_P=1000.0, mean_PET=1200.0, seed=2025)

    DI = dryness_index(P, PET)

    # 面积权重 ~ cos(lat)
    w_lat = area_weights_from_lat(lat2d[:,0])
    # broadcast to 2D
    W = np.repeat(w_lat[:,None], lon2d.shape[1], axis=1)

    di_vals = DI.ravel()
    weights = W.ravel()

    # 经验 pdf
    bins = np.logspace(-2, 2.3, 80)  # 约 0.01~200
    hist, centers = weighted_histogram(di_vals, weights, bins=bins, density=True)

    # 理论 pdf：D0 = mean(PET) / mean(P)
    D0 = float(PET.mean() / P.mean())
    y_theory = p_DI(centers, D0)

    plot_empirical_vs_theory(
        centers, hist, y_theory,
        title="Global DI empirical vs theory / 全球 DI 经验分布与理论分布",
        xlabel="DI (= PET / P)",
        ylabel="PDF",
        savepath="figures/di_empirical_vs_theory.png"
    )
    print("Saved: figures/di_empirical_vs_theory.png")
    print(f"Estimated D0 (PET_mean/P_mean) = {D0:.3f}")

if __name__ == "__main__":
    main()
