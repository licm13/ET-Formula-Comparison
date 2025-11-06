
"""Quickstart with synthetic data / 快速上手（合成数据）"""
import numpy as np
from pdsi_cmip6 import ep, pdsi, metrics, plotting, fonts

def main():
    fonts.configure()
    nt, ny, nx = 360, 4, 5
    rng = np.random.default_rng(2025)

    P  = rng.gamma(shape=2.0, scale=40.0, size=(nt,ny,nx))
    tas = rng.normal(15.0, 8.0, size=(nt,ny,nx))
    rh  = np.clip(rng.normal(60.0, 15.0, size=(nt,ny,nx)), 5, 100)
    ps  = np.full((nt,ny,nx), 101.3)
    u2  = np.clip(rng.normal(2.0, 0.8, size=(nt,ny,nx)), 0.1, None)
    Rn  = rng.normal(9.0, 2.0, size=(nt,ny,nx))
    G   = np.zeros_like(Rn)
    co2 = np.linspace(300, 520, nt).reshape(-1,1,1)

    EPd = ep.pm_rc_co2(tas=tas, rh=rh, ps=ps, u2=u2, Rn=Rn, G=G, co2=co2)  # mm/day
    EP  = EPd * 30.0  # ≈ monthly

    E   = np.minimum(EP, P*0.7)
    RO  = np.maximum(P - E - 10, 0.0)
    R   = np.maximum(P - E - RO, 0.0)
    L   = rng.uniform(0, 2, size=(nt,ny,nx))

    sc = pdsi.SelfCalibratedPDSI()
    Z, PDSI = sc.compute(P, EP, E=E, R=R, RO=RO, L=L, self_calibrate=True)

    # save a few demo plots
    plotting.plot_timeseries(PDSI[:,0,0], "PDSI时间序列", "PDSI Time Series", save="./figures/example_timeseries.png")
    plotting.plot_map(PDSI.mean(axis=0), "平均PDSI", "Mean PDSI", save="./figures/example_map_mean.png")

    trend = metrics.linear_trend(PDSI)
    plotting.plot_map(trend, "PDSI趋势（每年）", "PDSI Trend (per yr)", save="./figures/example_trend.png")

if __name__ == "__main__":
    main()
