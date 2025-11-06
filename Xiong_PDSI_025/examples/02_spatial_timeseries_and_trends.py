
"""Spatial–temporal demo & correlations / 空间-时间与相关性演示"""
import numpy as np
from pdsi_cmip6 import ep, pdsi, metrics, plotting, fonts

def main():
    fonts.configure()
    nt, ny, nx = 360, 3, 4
    rng = np.random.default_rng(7)
    P  = rng.gamma(shape=2.2, scale=35.0, size=(nt,ny,nx))
    tas = rng.normal(16.0, 9.0, size=(nt,ny,nx))
    rh  = np.clip(rng.normal(62.0, 18.0, size=(nt,ny,nx)), 5, 100)
    ps  = np.full((nt,ny,nx), 101.3)
    u2  = np.clip(rng.normal(2.0, 0.9, size=(nt,ny,nx)), 0.1, None)
    Rn  = rng.normal(8.0, 2.5, size=(nt,ny,nx))
    G   = np.zeros_like(Rn)

    EPd = ep.pm_rc(tas=tas, rh=rh, ps=ps, u2=u2, Rn=Rn, G=G)
    EP  = EPd*30.0

    E   = np.minimum(P*0.65 + rng.normal(0,2,size=(nt,ny,nx)), EP)
    RO  = np.maximum(P - E - 8, 0.0)
    R   = np.maximum(P - E - RO, 0.0)
    L   = rng.uniform(0, 1.5, size=(nt,ny,nx))

    sc = pdsi.SelfCalibratedPDSI()
    Z, PDSI = sc.compute(P, EP, E=E, R=R, RO=RO, L=L)

    soilm = rng.normal(size=(nt,ny,nx)) + np.cumsum(R - L - RO - 0.1*(E-EP/3), axis=0)*1e-3
    corr = metrics.temporal_corr(PDSI, soilm)
    plotting.plot_map(corr, "与土壤湿度相关系数", "Correlation vs. Soil Moisture", save="./figures/example_corr.png")

if __name__ == "__main__":
    main()
