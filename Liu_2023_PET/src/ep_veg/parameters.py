import math
from typing import Literal, Optional

def psychrometric_constant_kpa_per_C(P_kPa: float = 101.3) -> float:
    """
    心理温度常数 γ (kPa/°C). FAO-56 近似：γ ≈ 0.000665 * P(kPa).
    """
    return 0.000665 * P_kPa

def latent_heat_MJ_per_kg(T_C: float = 20.0) -> float:
    """
    水的汽化潜热 λ (MJ/kg). FAO-56 常用 λ≈2.45 MJ/kg（随温度轻微变化）。
    """
    return 2.45

def estimate_g1(T_C_mean_above0: float, MI: float, log_base: Literal["ln","log10"]="ln") -> float:
    """
    估算最优气孔模型的 g1 参数 (Eq.8).
    log(g1) = a*T + b*MI + c*(T*MI) + d
    a=0.027, b=-0.119, c=0.024, d=0.592
    NOTE: 原式未明确对数底，此处默认 'ln'，可切换 'log10'。
    返回 g1 (kPa^0.5)
    """
    a, b, c, d = 0.027, -0.119, 0.024, 0.592
    X = a*T_C_mean_above0 + b*MI + c*(T_C_mean_above0*MI) + d
    if log_base == "log10":
        return 10.0 ** X
    else:
        return math.exp(X)

def estimate_Aww(Ca_ppm: float, species: Optional[Literal["tree","grass","shrub"]] = None) -> float:
    """
    估算 Aww (μmol m^-2 s^-1) 与 CO2 的关系 (Eq.10).
    Aww = 10 * (1 + ((Ca-400)/100) * S)
    默认 S=7.5% (0.075)；可选物种特异斜率：树 12%、草 4%、灌丛 7%.
    """
    if species is None:
        S = 0.075
    else:
        S = {"tree": 0.12, "grass": 0.04, "shrub": 0.07}[species]
    return 10.0 * (1.0 + ((Ca_ppm - 400.0)/100.0) * S)
