"""
example_validate_power_law_tail.py

验证 -2 幂律尾部特征（log-log 上近似直线斜率 ~ -2）。
我们：
1) 从理论分布采样 DI（逆变换法）
2) 构建经验 pdf
3) 同时绘制理论 pdf 与在右侧尾部的参考线（-2 斜率）
"""
import numpy as np
from di_global.theory import p_DI, sample_DI
from di_global.compute import weighted_histogram
from di_global.plots import plot_empirical_vs_theory

def main():
    rng = np.random.default_rng(123)
    D0 = 1.2  # 任意取值（合成示例）
    samples = sample_DI(n=500_000, D0=D0, rng=rng)
    weights = np.ones_like(samples)  # 无权

    bins = np.logspace(-2, 3, 120)
    pdf_emp, centers = weighted_histogram(samples, weights, bins=bins, density=True)
    pdf_theo = p_DI(centers, D0)

    plot_empirical_vs_theory(
        centers, pdf_emp, pdf_theo,
        title="Power-law tail ~ DI^{-2} / 幂律尾部 ~ DI^{-2}",
        xlabel="DI",
        ylabel="PDF",
        savepath="figures/di_powerlaw_tail.png"
    )
    print("Saved: figures/di_powerlaw_tail.png")

if __name__ == "__main__":
    main()
