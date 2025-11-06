"""
Penman-Monteith with Jarvis-type stomatal response (PM-RC-Jarvis)
带 Jarvis 型气孔响应的 Penman-Monteith (PM-RC-Jarvis)

This module implements the PM-RC-Jarvis model from Wang et al. (2025), which integrates
the classic Jarvis (1976) multiplicative stomatal conductance model with the Penman-Monteith
framework to account for multiple environmental controls on stomatal behavior.
本模块实现了 Wang et al. (2025) 的 PM-RC-Jarvis 模型，
该模型将经典的 Jarvis (1976) 乘法气孔导度模型与 Penman-Monteith 框架相结合，
以考虑多种环境因素对气孔行为的控制。

Scientific References / 科学参考文献:
----------------------------------------
1. Wang, K., et al. (2025). Three Paradoxes Related to Potential Evapotranspiration in
   a Warming Climate. Current Climate Change Reports (in press).

2. Jarvis, P. G. (1976). The interpretation of the variations in leaf water potential
   and stomatal conductance found in canopies in the field. Philosophical Transactions
   of the Royal Society of London. B, Biological Sciences, 273(927), 593-610.

Integrated from / 从以下项目整合:
---------------------------------
Wang_2025_PET_Paradox/src/paradoxes_pet/pet.py
"""

import numpy as np
from ..utils.constants import slope_saturation_vapor_pressure, get_psychrometric_constant


# ===== Jarvis Stomatal Response Functions / Jarvis 气孔响应函数 =====

def jarvis_solar_radiation_response(solar_radiation, lai, rl_min=100.0, rl_max=5000.0, Sgl=100.0):
    """
    Calculate Jarvis-type solar radiation response factor.
    计算 Jarvis 型太阳辐射响应因子。

    Based on the classical Jarvis (1976) stomatal response to light.
    基于经典的 Jarvis (1976) 气孔对光的响应。

    Formulation / 公式:
    ------------------
    f(Sg) = (rl_min / rl_max) + 0.55 · (2·Sg / (Sgl·LAI)) / (1 + 0.55 · (2·Sg / (Sgl·LAI)))

    Bounded to [rl_min/rl_max, 1.0] / 限制在 [rl_min/rl_max, 1.0]

    where / 其中:
        Sg: solar radiation / 太阳辐射 (W m⁻²)
        LAI: leaf area index / 叶面积指数 (m² m⁻²)
        Sgl: light saturation point / 光饱和点 (W m⁻², default 100)
        rl_min, rl_max: minimum and maximum leaf resistances / 最小和最大叶片阻力 (s m⁻¹)

    Parameters:
    -----------
    solar_radiation : float or np.ndarray
        Solar radiation (W m⁻²) / 太阳辐射 (W m⁻²)
    lai : float or np.ndarray
        Leaf area index (m² m⁻²) / 叶面积指数 (m² m⁻²)
    rl_min : float, default=100.0
        Minimum leaf resistance (s m⁻¹) / 最小叶片阻力 (s m⁻¹)
    rl_max : float, default=5000.0
        Maximum leaf resistance (s m⁻¹) / 最大叶片阻力 (s m⁻¹)
    Sgl : float, default=100.0
        Light saturation point (W m⁻²) / 光饱和点 (W m⁻²)

    Returns:
    --------
    f_sg : float or np.ndarray
        Solar radiation response factor (0-1) / 太阳辐射响应因子 (0-1)
    """
    solar_radiation = np.asarray(solar_radiation, dtype=float)
    lai = np.asarray(lai, dtype=float)

    # Prevent division by zero / 防止除零
    lai_safe = np.maximum(lai, 1e-6)

    # Jarvis light response / Jarvis 光响应
    term = 0.55 * (2.0 * solar_radiation / (Sgl * lai_safe))
    f_sg = (rl_min / rl_max) + term / (1.0 + term)

    # Bound to valid range / 限制到有效范围
    f_sg = np.clip(f_sg, rl_min / rl_max, 1.0)

    return f_sg


def jarvis_temperature_response(temperature):
    """
    Calculate Jarvis-type temperature response factor.
    计算 Jarvis 型温度响应因子。

    Based on Jarvis (1976) parabolic temperature response with optimum at ~25°C.
    基于 Jarvis (1976) 抛物线温度响应，最优值约为 25°C。

    Formulation / 公式:
    ------------------
    f(Ta) = 1 - 0.0016 · (T_opt - Ta)²

    where / 其中:
        T_opt = 24.85°C (298 K - 273.15)
        Ta: air temperature / 气温 (°C)

    Parameters:
    -----------
    temperature : float or np.ndarray
        Air temperature (°C) / 气温 (°C)

    Returns:
    --------
    f_ta : float or np.ndarray
        Temperature response factor (0-1) / 温度响应因子 (0-1)
    """
    temperature = np.asarray(temperature, dtype=float)

    # Optimal temperature / 最优温度
    T_opt = 24.85  # °C (298 K - 273.15)

    # Parabolic response / 抛物线响应
    f_ta = 1.0 - 0.0016 * (T_opt - temperature) ** 2

    # Bound to valid range / 限制到有效范围
    f_ta = np.clip(f_ta, 0.0, 1.1)

    return f_ta


def jarvis_vpd_response(vpd):
    """
    Calculate Jarvis-type vapor pressure deficit response factor.
    计算 Jarvis 型水汽压差响应因子。

    Based on Jarvis (1976) linear VPD response, where stomata close under high VPD.
    基于 Jarvis (1976) 线性 VPD 响应，高 VPD 时气孔关闭。

    Formulation / 公式:
    ------------------
    f(VPD) = 1 - 0.025 · VPD

    where / 其中:
        VPD: vapor pressure deficit / 水汽压差 (kPa)

    Parameters:
    -----------
    vpd : float or np.ndarray
        Vapor pressure deficit (kPa) / 水汽压差 (kPa)

    Returns:
    --------
    f_vpd : float or np.ndarray
        VPD response factor (0-1) / VPD 响应因子 (0-1)
    """
    vpd = np.asarray(vpd, dtype=float)

    # Linear VPD response / 线性 VPD 响应
    f_vpd = 1.0 - 0.025 * vpd

    # Bound to valid range / 限制到有效范围
    f_vpd = np.clip(f_vpd, 0.0, 1.1)

    return f_vpd


def jarvis_co2_response(co2_ppm, x=0.9):
    """
    Calculate Jarvis-type CO2 response factor.
    计算 Jarvis 型 CO2 响应因子。

    Based on Jarvis (1976) piecewise CO2 response, adapted for modern CO2 concentrations.
    基于 Jarvis (1976) 分段 CO2 响应，适配现代 CO2 浓度。

    Formulation / 公式:
    ------------------
    f(CO2) = 1.0,                                  if CO2 ≤ 100 ppm
           = 1.0 - (1 - x) · (CO2 - 100) / 900,   if 100 < CO2 < 1000 ppm
           = x,                                    if CO2 ≥ 1000 ppm

    where / 其中:
        x: minimum response factor at high CO2 / 高 CO2 时的最小响应因子 (default 0.9)

    Parameters:
    -----------
    co2_ppm : float or np.ndarray
        Atmospheric CO2 concentration (ppm) / 大气 CO2 浓度 (ppm)
    x : float, default=0.9
        Minimum response factor at high CO2 (0-1) / 高 CO2 时的最小响应因子 (0-1)
        Represents stomatal closure effect under elevated CO2
        代表高 CO2 下的气孔关闭效应

    Returns:
    --------
    f_co2 : float or np.ndarray
        CO2 response factor (0-1) / CO2 响应因子 (0-1)
    """
    co2_ppm = np.asarray(co2_ppm, dtype=float)

    # Initialize with ones / 用1初始化
    f_co2 = np.ones_like(co2_ppm, dtype=float)

    # Piecewise response / 分段响应
    mask1 = co2_ppm <= 100.0
    mask2 = (co2_ppm > 100.0) & (co2_ppm < 1000.0)
    mask3 = co2_ppm >= 1000.0

    f_co2[mask1] = 1.0
    f_co2[mask2] = 1.0 - (1.0 - x) / 900.0 * (co2_ppm[mask2] - 100.0)
    f_co2[mask3] = x

    # Bound to valid range / 限制到有效范围
    f_co2 = np.clip(f_co2, 0.1, 1.0)

    return f_co2


# ===== Main PM-RC-Jarvis Formula / 主 PM-RC-Jarvis 公式 =====

def penman_monteith_jarvis(temperature, net_radiation, wind_speed, vpd,
                           solar_radiation, co2_ppm, lai=None, crop_height=0.12,
                           rl_min=100.0, rl_max=5000.0, Sgl=100.0,
                           pressure=101.3, co2_response_x=0.9):
    """
    Calculate PET using Penman-Monteith with Jarvis-type stomatal response (PM-RC-Jarvis).
    使用带 Jarvis 型气孔响应的 Penman-Monteith (PM-RC-Jarvis) 计算 PET。

    This method integrates the multiplicative Jarvis (1976) stomatal conductance model
    into the Penman-Monteith framework, accounting for responses to solar radiation,
    temperature, VPD, and CO2. It represents an empirical approach to stomatal modeling
    that contrasts with optimization-based methods.
    该方法将乘法 Jarvis (1976) 气孔导度模型整合到 Penman-Monteith 框架中，
    考虑对太阳辐射、温度、VPD 和 CO2 的响应。它代表了气孔建模的经验方法，
    与基于优化的方法形成对比。

    Formulation / 公式:
    ------------------
    The method modifies the FAO-56 Penman-Monteith equation by replacing the standard
    resistance term (1 + 0.34·u₂) with a Jarvis-weighted term:
    该方法通过用 Jarvis 加权项替换标准阻力项 (1 + 0.34·u₂) 来修改 FAO-56 Penman-Monteith 方程：

    PET = [0.408·Δ·Rn + γ·(900/(T+273))·u₂·VPD] / [Δ + γ·(1 + 0.116·u₂·F⁻¹)]

    where / 其中:
        F = f(Sg) · f(Ta) · f(VPD) · f(CO2)  (multiplicative Jarvis factors)
        F⁻¹ = inverse of combined stomatal response / 组合气孔响应的倒数

    The Jarvis factors represent: / Jarvis 因子代表：
    - f(Sg): Solar radiation response (light limitation) / 太阳辐射响应（光限制）
    - f(Ta): Temperature response (temperature stress) / 温度响应（温度胁迫）
    - f(VPD): VPD response (atmospheric dryness) / VPD 响应（大气干燥）
    - f(CO2): CO2 response (CO2 fertilization effect) / CO2 响应（CO2 施肥效应）

    Parameters:
    -----------
    temperature : float or np.ndarray
        Air temperature (°C) / 气温 (°C)
    net_radiation : float or np.ndarray
        Net radiation (MJ m⁻² day⁻¹) / 净辐射 (MJ m⁻² day⁻¹)
    wind_speed : float or np.ndarray
        Wind speed at 2m height (m s⁻¹) / 2米高处风速 (m s⁻¹)
    vpd : float or np.ndarray
        Vapor pressure deficit (kPa) / 水汽压差 (kPa)
    solar_radiation : float or np.ndarray
        Solar radiation (W m⁻²) / 太阳辐射 (W m⁻²)
        Required for f(Sg) calculation / f(Sg) 计算所需
    co2_ppm : float or np.ndarray
        Atmospheric CO2 concentration (ppm) / 大气 CO2 浓度 (ppm)
    lai : float or np.ndarray, optional
        Leaf area index (m² m⁻²) / 叶面积指数 (m² m⁻²)
        If not provided, will be estimated from crop_height
        如果未提供，将从 crop_height 估算
    crop_height : float, default=0.12
        Crop height (m) / 作物高度 (m)
        Used to estimate LAI = 24 · crop_height (for reference crop)
        用于估算 LAI = 24 · crop_height（参考作物）
    rl_min : float, default=100.0
        Minimum leaf resistance (s m⁻¹) / 最小叶片阻力 (s m⁻¹)
    rl_max : float, default=5000.0
        Maximum leaf resistance (s m⁻¹) / 最大叶片阻力 (s m⁻¹)
    Sgl : float, default=100.0
        Light saturation point (W m⁻²) / 光饱和点 (W m⁻²)
    pressure : float or np.ndarray, default=101.3
        Atmospheric pressure (kPa) / 大气压力 (kPa)
    co2_response_x : float, default=0.9
        Minimum CO2 response factor at high CO2 / 高 CO2 时的最小 CO2 响应因子

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Wang et al. (2025), Current Climate Change Reports
    - Jarvis (1976), Philosophical Transactions of the Royal Society B

    Notes:
    ------
    This method demonstrates the "paradox" where different stomatal models can lead to
    opposite trends in PET under climate change, particularly regarding CO2 effects.
    该方法展示了"悖论"：在气候变化下，不同的气孔模型可导致 PET 的相反趋势，
    特别是关于 CO2 效应。

    Example / 示例:
    ---------------
    >>> pet = penman_monteith_jarvis(
    ...     temperature=20.0,
    ...     net_radiation=15.0,
    ...     wind_speed=2.5,
    ...     vpd=1.5,
    ...     solar_radiation=200.0,
    ...     co2_ppm=400.0,
    ...     lai=3.0
    ... )
    """
    temperature = np.asarray(temperature, dtype=float)
    net_radiation = np.asarray(net_radiation, dtype=float)
    wind_speed = np.asarray(wind_speed, dtype=float)
    vpd = np.asarray(vpd, dtype=float)
    solar_radiation = np.asarray(solar_radiation, dtype=float)
    co2_ppm = np.asarray(co2_ppm, dtype=float)
    pressure = np.asarray(pressure)

    # Estimate LAI if not provided / 如果未提供则估算 LAI
    if lai is None:
        # For reference crop: LAI ≈ 24 · crop_height (Wang et al. 2025)
        # 参考作物：LAI ≈ 24 · crop_height
        lai = 24.0 * crop_height
    else:
        lai = np.asarray(lai, dtype=float)

    # Calculate Jarvis response factors / 计算 Jarvis 响应因子
    f_sg = jarvis_solar_radiation_response(solar_radiation, lai, rl_min, rl_max, Sgl)
    f_ta = jarvis_temperature_response(temperature)
    f_vpd = jarvis_vpd_response(vpd)
    f_co2 = jarvis_co2_response(co2_ppm, x=co2_response_x)

    # Combined multiplicative factor / 组合乘法因子
    # F = f(Sg) · f(Ta) · f(VPD) · f(CO2)
    F_combined = f_sg * f_ta * f_vpd * f_co2

    # Inverse factor for resistance term / 阻力项的倒数因子
    # Prevent division by zero / 防止除零
    F_inverse = 1.0 / np.maximum(F_combined, 1e-6)

    # Calculate psychrometric parameters / 计算干湿表参数
    delta = slope_saturation_vapor_pressure(temperature)
    gamma = get_psychrometric_constant(pressure, temperature)

    # Penman-Monteith equation with Jarvis modification / 带 Jarvis 修改的 Penman-Monteith 方程
    # Numerator: radiation term + aerodynamic term / 分子：辐射项 + 空气动力学项
    T_kelvin = temperature + 273.15
    numerator = (
        0.408 * delta * net_radiation +
        gamma * (900.0 / T_kelvin) * wind_speed * vpd
    )

    # Denominator with Jarvis-weighted resistance / 带 Jarvis 加权阻力的分母
    # Standard FAO-56: den = delta + gamma * (1 + 0.34 * u2)
    # Jarvis-modified: den = delta + gamma * (1 + 0.116 * u2 * F^-1)
    adjustment = 1.0 + 0.116 * wind_speed * F_inverse
    denominator = delta + gamma * np.maximum(adjustment, 1e-6)

    # PET in mm/day / PET (mm/day)
    pet = numerator / np.maximum(denominator, 1e-6)

    # Ensure non-negative values / 确保非负值
    pet = np.maximum(pet, 0.0)

    return pet


# Summary of implemented formulas / 实现公式概要
__all__ = [
    'penman_monteith_jarvis',
    'jarvis_solar_radiation_response',
    'jarvis_temperature_response',
    'jarvis_vpd_response',
    'jarvis_co2_response'
]
