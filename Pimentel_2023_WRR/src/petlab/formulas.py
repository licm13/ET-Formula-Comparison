
"""
PET formulas: Jensen–Haise (Oudin-style), Hargreaves, Priestley–Taylor.

英文注释：This module implements three classic PET formulas with minimal, FAO-56-consistent
radiation helpers. Equations follow the pedagogical forms in literature; constants consolidated
to produce mm/day given input radiation in MJ m-2 day-1.

参考文献：Allen & Breshears/FAO-56；Oudin (2005) scaling；Priestley & Taylor (1972).
"""
from dataclasses import dataclass
import numpy as np
from .radiation import (
    Ra_extraterrestrial, shortwave_from_hargreaves, slope_vapour_pressure_curve,
    psychrometric_constant, net_radiation, Rso_clear_sky, ea_from_RH
)

LAMBDA = 2.45  # MJ kg-1, latent heat at ~20C

@dataclass
class JensenHaiseParams:
    Tadd: float = 5.0      # °C, Oudin temperature offset
    Tscale: float = 100.0  # °C, Oudin scaling
    kc: float = 1.0

def jensen_haise(Tmean: float, Ra: float, params: JensenHaiseParams=JensenHaiseParams()) -> float:
    """
    Oudin-style Jensen–Haise:
        PET = kc * (Ra / lambda) * (Tmean + Tadd) / Tscale, if Tmean + Tadd > 0 else 0
    返回单位：mm/day
    """
    x = Tmean + params.Tadd
    if x <= 0:
        return 0.0
    return params.kc * (Ra / LAMBDA) * (x / params.Tscale)

@dataclass
class HargreavesParams:
    kc: float = 1.0
    krs: float = 0.16  # inland ~0.16; coastal ~0.19

def hargreaves(Tmean: float, Tmax: float, Tmin: float, Ra: float, params: HargreavesParams=HargreavesParams()) -> float:
    """
    Classic Hargreaves (1985):
        PET = 0.0023 * Ra * (Tmean + 17.8) * sqrt(Tmax - Tmin)
    其中 Ra 单位 MJ m-2 d-1；返回 mm/day。
    """
    dT = max(Tmax - Tmin, 0.0)
    pet = 0.0023 * Ra * max(Tmean + 17.8, 0.0) * np.sqrt(dT)
    return params.kc * pet

@dataclass
class PriestleyTaylorParams:
    kc: float = 1.0
    alpha_pt: float = 1.26
    albedo: float = 0.23    # typical reference
    krs: float = 0.16       # Rs from Hargreaves if no radiation obs.
    P_kPa: float = 101.3

def priestley_taylor(Tmean: float, Tmax: float, Tmin: float, Ra: float,
                     RHmax: float=80.0, RHmin: float=40.0,
                     elev_km: float=0.1,
                     params: PriestleyTaylorParams=PriestleyTaylorParams()) -> float:
    """
    Priestley–Taylor (1972):
        PET = kc * alpha * [Δ / (Δ + γ)] * (Rn / λ)
    Rn 通过简化净辐射估计；Rs 采用 Hargreaves 近似。
    """
    # Radiation terms
    Rs = shortwave_from_hargreaves(Ra, Tmax, Tmin, params.krs)
    Rso = Rso_clear_sky(elev_km, Ra)
    ea = ea_from_RH(Tmax, Tmin, RHmax, RHmin)
    Rn = net_radiation(Rs, Rso, params.albedo, Tmax, Tmin, ea)

    # Psychrometric terms
    delta = slope_vapour_pressure_curve(Tmean)
    gamma = psychrometric_constant(params.P_kPa)

    pet = params.alpha_pt * (delta / (delta + gamma)) * (Rn / LAMBDA)
    return params.kc * max(pet, 0.0)

def compute_daily_pet(formula: str, lat_deg: float, doy: int, Tmean: float, Tmax: float, Tmin: float, **kwargs) -> float:
    """
    Convenience wrapper to compute PET by name.
    formula in {"jensen_haise","hargreaves","priestley_taylor"}.
    """
    Ra = Ra_extraterrestrial(lat_deg, doy)
    if formula == "jensen_haise":
        return jensen_haise(Tmean, Ra, **kwargs)
    elif formula == "hargreaves":
        return hargreaves(Tmean, Tmax, Tmin, Ra, **kwargs)
    elif formula == "priestley_taylor":
        return priestley_taylor(Tmean, Tmax, Tmin, Ra, **kwargs)
    else:
        raise ValueError(f"Unknown formula: {formula}")
