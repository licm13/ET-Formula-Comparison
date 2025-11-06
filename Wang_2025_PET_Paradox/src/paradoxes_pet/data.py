
"""
Synthetic climate data generator for 1950-2100 monthly.
1950-2100 月尺度合成气候数据生成器（教学演示用）。
"""
from __future__ import annotations
import numpy as np
import pandas as pd

def generate_synthetic_monthly(seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # monthly timeline
    t = pd.date_range("1950-01-01", "2100-12-31", freq="MS")
    n = len(t)

    # Temperature (°C): upward trend + seasonality + noise
    Ta = 10 + 0.02 * np.arange(n)/12 + 10*np.sin(2*np.pi*(np.arange(n)%12)/12) + rng.normal(0, 1.2, n)

    # Global solar radiation Sg (W/m2): slight brightening after 1995, seasonal
    base_Sg = 180 + 60*np.sin(2*np.pi*(np.arange(n)%12)/12)
    trend_Sg = np.piecewise(np.arange(n), [np.arange(n) < (1995-1950)*12, np.arange(n) >= (1995-1950)*12],
                            [lambda k: -5 + 0*k, lambda k: -5 + 0.03*(k - (1995-1950)*12)])
    Sg = base_Sg + trend_Sg + rng.normal(0, 6, n)

    # Net available radiation Rn* (MJ/m2/day): scaled from Sg + temperature effect
    Rn_star = (Sg * 0.0864) * 0.6 + 0.03 * (Ta - 10)  # crude mapping for demo

    # Wind speed (m/s): stilling then slight reversal
    base_WS = 2.5 + rng.normal(0, 0.2, n)
    WS2 = base_WS + np.piecewise(np.arange(n), [np.arange(n) < (1990-1950)*12, np.arange(n) >= (1990-1950)*12],
                                 [lambda k: -0.5*(k/((1990-1950)*12)),
                                  lambda k: -0.5 + 0.3*((k - (1990-1950)*12)/((2100-1990)*12))])

    # VPD (kPa): increases with temperature + noise
    VPD = 0.5 + 0.02*(Ta-10) + rng.normal(0, 0.05, n)
    VPD = np.clip(VPD, 0.05, None)

    # Precipitation P (mm/month): seasonal + mild trend
    P = 60 + 30*np.sin(2*np.pi*(np.arange(n)%12)/12 + 0.5) + 0.02*np.arange(n)/12 + rng.normal(0, 10, n)
    P = np.clip(P, 0, None)

    # CO2 (ppm): increasing scenario
    years = np.array([ts.year for ts in t])
    CO2 = 310 + (years - 1950) * 1.5 + rng.normal(0, 2, n)  # ~1950:310ppm -> 2100:~ 535ppm

    df = pd.DataFrame({
        "time": t,
        "Ta_C": Ta,
        "Sg_W_m2": Sg,
        "Rn_star_MJ_m2_day": Rn_star,
        "WS2_m_s": WS2,
        "VPD_kPa": VPD,
        "P_mm": P,
        "CO2_ppm": CO2,
    }).set_index("time")
    return df
