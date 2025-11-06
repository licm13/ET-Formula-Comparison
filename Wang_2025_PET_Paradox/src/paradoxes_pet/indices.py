
"""
Indices used in the paradox analysis (teaching version).
用于悖论分析的指标（教学版）。
"""
from __future__ import annotations
import numpy as np
import pandas as pd

def annual_aridity_index(precip_mm_month: pd.Series, pet_mm_month: pd.Series, freq="A") -> pd.Series:
    """
    Aridity Index (AI) = P / PET, aggregated annually. 旱湿指数 AI=年总降水/年总PET。
    Inputs are monthly series with DatetimeIndex.
    """
    P_annual = precip_mm_month.resample(freq).sum(min_count=1)
    PET_annual = pet_mm_month.resample(freq).sum(min_count=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        AI = P_annual / np.where(PET_annual==0, np.nan, PET_annual)
    return AI

def toy_pdsi_like(precip_mm_month: pd.Series, pet_mm_month: pd.Series, window=12) -> pd.Series:
    """
    A toy, PDSI-like anomaly index for demonstration only (not real PDSI).
    教学演示用“类 PDSI”指标——基于 (P - PET) 的平滑与标准化，非真实 PDSI。

    Steps:
    1) M = P - PET (monthly moisture anomaly proxy)
    2) rolling mean (window)
    3) standardize to zero-mean / unit-variance
    """
    M = (precip_mm_month - pet_mm_month).astype(float)
    M_roll = M.rolling(window=window, min_periods=max(3, window//3)).mean()
    mu = M_roll.rolling(window=120, min_periods=24).mean()  # decadal baseline (10y)
    sigma = M_roll.rolling(window=120, min_periods=24).std(ddof=1)
    Z = (M_roll - mu) / sigma
    return Z

def drought_extent_and_frequency(pdsi_like: pd.Series, thresh=-3.0, freq="A") -> tuple[pd.Series, pd.Series]:
    """
    Estimate "extent" and "frequency" based on % of months below threshold.
    以阈值统计“频次”与“范围”（单点示意：用百分比近似）。
    For a single series, we treat extent as the share of months below threshold in a year,
    and frequency as the count of such months.
    """
    below = pdsi_like < thresh
    freq_year = below.resample(freq).sum(min_count=1)  # count months
    tot_year = below.resample(freq).count()
    extent_year = (freq_year / tot_year).replace([np.inf, -np.inf], np.nan)
    return extent_year, freq_year
