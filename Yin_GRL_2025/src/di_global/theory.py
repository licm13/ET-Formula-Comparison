"""
theory.py

Theoretical distributions for dryness index (DI) and humidity index (HI).

中英双语注释：
- 公式来源于 Yin & Porporato (2023, GRL) 的推导：
  p_DI(di; D0) = D0 / di^2 * exp(-D0/di)
  p_HI(hi; H0) = (1/H0) * exp(-hi/H0), 其中 H0 = 1/D0

注意：本仓库默认使用合成数据进行演示；若使用真实数据，请结合论文与数据源。
"""
from __future__ import annotations
import numpy as np

def p_DI(di: np.ndarray, D0: float) -> np.ndarray:
    """
    Probability density function (pdf) of the dryness index DI = PET / P.
    DI > 0, D0 = mean(PET) / mean(P).
    公式: p_DI(di) = D0 / di^2 * exp(-D0/di).
    """
    di = np.asarray(di, dtype=float)
    out = np.zeros_like(di)
    mask = di > 0
    out[mask] = (D0 / (di[mask]**2)) * np.exp(-D0 / di[mask])
    return out

def p_HI(hi: np.ndarray, H0: float) -> np.ndarray:
    """
    pdf of humidity index HI = P / PET, HI > 0.
    公式: p_HI(hi) = (1/H0) * exp(-hi/H0), H0 = 1 / D0.
    """
    hi = np.asarray(hi, dtype=float)
    out = np.zeros_like(hi)
    mask = hi > 0
    out[mask] = (1.0 / H0) * np.exp(-hi[mask] / H0)
    return out

def sample_DI(n: int, D0: float, rng: np.random.Generator | None = None) -> np.ndarray:
    """
    Draw random samples from the DI distribution using the inverse-CDF method.

    累积分布函数 F_DI(di) = exp(-D0/di)，对 di>0.
    令 U ~ Uniform(0,1), 则 di = D0 / (-ln U).
    """
    rng = np.random.default_rng() if rng is None else rng
    u = rng.uniform(low=0.0, high=1.0, size=n)
    # Avoid U=0 to prevent inf
    u = np.clip(u, 1e-12, 1.0-1e-12)
    return D0 / (-np.log(u))
