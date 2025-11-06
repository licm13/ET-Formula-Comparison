
"""Simple diagnostics and metrics / 诊断指标与度量"""
from __future__ import annotations
import numpy as np

def linear_trend(arr, years_per_step=1/12.0):
    """
    Ordinary least squares linear trend along time axis=0.
    返回斜率（每年单位）; arr: (t, y, x)
    """
    arr = np.asarray(arr, dtype=float)
    t = np.arange(arr.shape[0], dtype=float) * years_per_step
    t = t[:, None, None]
    t_mean = np.nanmean(t, axis=0)
    y_mean = np.nanmean(arr, axis=0)
    num = np.nansum((t - t_mean) * (arr - y_mean), axis=0)
    den = np.nansum((t - t_mean)**2, axis=0)
    slope = np.divide(num, den, out=np.full_like(y_mean, np.nan), where=den!=0)
    return slope

def temporal_corr(a, b):
    """
    Pearson correlation along time axis (axis=0). a,b: (t, y, x)
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    am = np.nanmean(a, axis=0)
    bm = np.nanmean(b, axis=0)
    num = np.nansum((a-am)*(b-bm), axis=0)
    den = np.sqrt(np.nansum((a-am)**2, axis=0) * np.nansum((b-bm)**2, axis=0))
    return np.divide(num, den, out=np.full_like(am, np.nan), where=den!=0)
