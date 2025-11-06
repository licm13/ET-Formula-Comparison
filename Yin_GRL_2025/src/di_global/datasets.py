"""
datasets.py

Synthetic (random) global grid generators and simple I/O placeholders.

- 生成全球经纬网格 (1° x 1° 可调)，随机生成降水 P（指数分布）与 PET（近似常数+少量随机）
- 面向真实数据的占位 API（用户可替换为实际读取函数）
"""
from __future__ import annotations
import numpy as np
from typing import Tuple

def global_latlon_grid(dlon: float=1.0, dlat: float=1.0) -> Tuple[np.ndarray, np.ndarray]:
    lons = np.arange(-180, 180, dlon)
    lats = np.arange(-90, 90, dlat)
    lon2d, lat2d = np.meshgrid(lons, lats)
    return lon2d, lat2d

def synthetic_P_PET(lon2d: np.ndarray, lat2d: np.ndarray, mean_P: float=1000.0, mean_PET: float=1200.0,
                    seed: int=42) -> Tuple[np.ndarray, np.ndarray]:
    """
    合成数据：
    - P ~ Exponential(mean=mean_P) with mild latitudinal modulation
    - PET ~ mean_PET + small gaussian noise + subtropical bump
    """
    rng = np.random.default_rng(seed)
    # Precipitation: exponential with latitudinal factor (wetter near equator on avg)
    lat_abs = np.abs(lat2d)
    lat_factor = 1.0 + 0.5 * np.exp(-(lat_abs/20.0))  # ~equator wetter
    mu = mean_P * (lat_factor / lat_factor.mean())
    # Exponential with mean = mu -> scale = mu
    P = rng.exponential(scale=mu)
    P = np.clip(P, 1e-3, None)

    # PET: base with subtropical peak around ±25°
    subtrop_bump = 1.0 + 0.4 * np.exp(-((lat_abs-25.0)**2) / (2*10.0**2))
    PET = mean_PET * (subtrop_bump / subtrop_bump.mean()) + rng.normal(0, mean_PET*0.08, size=lon2d.shape)
    PET = np.clip(PET, 1e-3, None)
    return P, PET

# ---- Placeholders for real data I/O ----
def read_real_world_data(*args, **kwargs):
    """
    占位函数：请在此处接入真实数据读取流程（例如 CRU/GPCC/GPCP/Global AI PET/CMIP6）。
    返回 P, PET, lon2d, lat2d。
    """
    raise NotImplementedError("请实现真实数据读取函数 read_real_world_data()")
