"""
compute.py

Grid computations for DI, including area-weighted histograms.
包含：
- 依据格点 P, PET 计算 DI
- 基于纬度的面积权重（~ cos(lat)）
- 计算经验分布（密度/直方图），并与理论分布比较
"""
from __future__ import annotations
import numpy as np
from typing import Tuple

def dryness_index(P: np.ndarray, PET: np.ndarray) -> np.ndarray:
    """
    DI = PET / P. Return array with same shape as inputs.

    Notes:
    - P must be positive to avoid division by zero; small epsilon is applied.
    - 简单处理：对 P<eps 的格点，用 eps 代替，避免无穷大。
    """
    eps = 1e-8
    P_safe = np.where(P <= eps, eps, P)
    return PET / P_safe

def area_weights_from_lat(lat_deg: np.ndarray) -> np.ndarray:
    """
    Compute area weights proportional to cos(latitude).

    输入纬度（度）。输出与纬度长度一致的权重（未归一化）。
    """
    lat_rad = np.deg2rad(lat_deg)
    w = np.cos(lat_rad)
    # clamp negative rounds near poles
    w = np.clip(w, 0.0, None)
    return w

def weighted_histogram(values: np.ndarray, weights: np.ndarray, bins: np.ndarray, density: bool=True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Weighted histogram similar to numpy.histogram with weights.

    Parameters
    ----------
    values : array-like
    weights: array-like (same shape as values)
    bins   : bin edges
    density: if True, returns pdf estimate that integrates to 1

    Returns
    -------
    hist : array of shape len(bins)-1
    bin_centers : array of same shape as hist
    """
    hist, edges = np.histogram(values, bins=bins, weights=weights, density=False)
    bin_widths = np.diff(edges)
    if density:
        total = np.sum(hist)
        # 把权重总和换成“概率密度”意义：除以总面积并再除以 bin 宽度
        if total > 0:
            hist = hist / total / bin_widths
    centers = 0.5 * (edges[:-1] + edges[1:])
    return hist.astype(float), centers
