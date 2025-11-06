"""
Vegetation-aware Penman-Monteith (EP_Veg) formula
植被感知的Penman-Monteith (EP_Veg) 公式

This module implements the EP_Veg model from Liu et al. (2023), which incorporates
optimal stomatal conductance theory (Medlyn et al. 2011) and explicit LAI scaling
to provide physically-based PET estimates that account for vegetation responses.
本模块实现了 Liu et al. (2023) 的 EP_Veg 模型，该模型结合了
最优气孔导度理论 (Medlyn et al. 2011) 和显式LAI缩放，
提供了考虑植被响应的基于物理的PET估算。

Scientific References / 科学参考文献:
----------------------------------------
1. Liu, B., et al. (2023). A physically-based potential evapotranspiration model for
   global water availability projections. Journal of Hydrology, 616, 128781.

2. Medlyn, B. E., et al. (2011). Reconciling the optimal and empirical approaches to
   modelling stomatal conductance. Global Change Biology, 17(6), 2134-2144.

Integrated from / 从以下项目整合:
---------------------------------
Liu_2023_PET/src/ep_veg/pm.py
Liu_2023_PET/src/ep_veg/gs.py
Liu_2023_PET/src/ep_veg/parameters.py
"""

import numpy as np
import math
from typing import Optional, Literal
from ..utils.constants import slope_saturation_vapor_pressure, get_psychrometric_constant


# ===== Physical Constants / 物理常数 =====
R_GAS = 8.314        # Universal gas constant (J mol⁻¹ K⁻¹) / 通用气体常数
P_AIR_PA = 101325.0  # Standard atmospheric pressure (Pa) / 标准大气压


# ===== Parameter Estimation Functions / 参数估算函数 =====

def estimate_g1(temperature_mean, moisture_index, log_base="ln"):
    """
    Estimate the g1 parameter for optimal stomatal conductance model.
    估算最优气孔导度模型的 g1 参数。

    Based on Liu et al. (2023) Equation 8, which relates g1 to climate conditions.
    基于 Liu et al. (2023) 方程8，将 g1 与气候条件关联。

    Formulation / 公式:
    ------------------
    log(g1) = a·T + b·MI + c·(T·MI) + d

    where / 其中:
        a = 0.027, b = -0.119, c = 0.024, d = 0.592
        T: mean temperature above 0°C / 0°C以上的平均温度 (°C)
        MI: moisture index / 湿润指数

    Parameters:
    -----------
    temperature_mean : float
        Mean temperature above 0°C (°C) / 0°C以上的平均温度 (°C)
    moisture_index : float
        Moisture index (P/PET or similar) / 湿润指数 (P/PET 或类似指标)
    log_base : str, default="ln"
        Logarithm base: "ln" (natural log) or "log10" (base 10)
        对数底：\"ln\"（自然对数）或 \"log10\"（以10为底）

    Returns:
    --------
    g1 : float
        Optimal stomatal conductance parameter (kPa⁰·⁵) / 最优气孔导度参数 (kPa⁰·⁵)
    """
    a, b, c, d = 0.027, -0.119, 0.024, 0.592
    X = a * temperature_mean + b * moisture_index + c * (temperature_mean * moisture_index) + d

    if log_base == "log10":
        return 10.0 ** X
    else:
        return math.exp(X)


def estimate_Aww(co2_ppm, species=None):
    """
    Estimate well-watered photosynthesis potential Aww as a function of CO2.
    估算充分供水条件下的光合潜力 Aww 与 CO2 的关系。

    Based on Liu et al. (2023) Equation 10, accounting for CO2 fertilization effects.
    基于 Liu et al. (2023) 方程10，考虑 CO2 施肥效应。

    Formulation / 公式:
    ------------------
    Aww = 10 · [1 + ((Ca - 400) / 100) · S]

    where / 其中:
        Ca: atmospheric CO2 concentration / 大气CO2浓度 (ppm)
        S: species-specific slope / 物种特异性斜率 (%)
           - Default: 7.5% (mixed vegetation) / 默认：7.5%（混合植被）
           - Tree: 12% / 乔木：12%
           - Grass: 4% / 草本：4%
           - Shrub: 7% / 灌木：7%

    Parameters:
    -----------
    co2_ppm : float
        Atmospheric CO2 concentration (ppm) / 大气CO2浓度 (ppm)
    species : str, optional
        Vegetation type: "tree", "grass", or "shrub" / 植被类型
        If None, uses default mixed vegetation (7.5%) / 如果为None，使用默认混合植被(7.5%)

    Returns:
    --------
    Aww : float
        Well-watered photosynthesis potential (μmol m⁻² s⁻¹) / 充分供水光合潜力 (μmol m⁻² s⁻¹)
    """
    if species is None:
        S = 0.075  # 7.5% for mixed vegetation / 混合植被为7.5%
    else:
        species_slopes = {
            "tree": 0.12,   # 12% / 乔木12%
            "grass": 0.04,  # 4%  / 草本4%
            "shrub": 0.07   # 7%  / 灌木7%
        }
        S = species_slopes.get(species.lower(), 0.075)

    Aww = 10.0 * (1.0 + ((co2_ppm - 400.0) / 100.0) * S)
    return Aww


# ===== Stomatal Conductance Functions / 气孔导度函数 =====

def stomatal_conductance_medlyn2011(vpd_kpa, photosynthesis_rate, co2_ppm, g1, g0=0.0):
    """
    Calculate leaf stomatal conductance using the Medlyn et al. (2011) optimal model.
    使用 Medlyn et al. (2011) 最优模型计算叶片气孔导度。

    This model represents optimal stomatal behavior that balances carbon gain and water loss.
    该模型代表了平衡碳获取和水分损失的最优气孔行为。

    Formulation / 公式:
    ------------------
    gₗₛ = g₀ + 1.6 · (1 + g₁ / √VPD) · A / Cₐ

    where / 其中:
        gₗₛ: leaf stomatal conductance / 叶片气孔导度 (mol m⁻² s⁻¹)
        g₀: residual conductance (usually ≈0) / 残余导度（通常≈0）
        g₁: optimal conductance parameter / 最优导度参数 (kPa⁰·⁵)
        VPD: vapor pressure deficit / 水汽压差 (kPa)
        A: net photosynthesis rate / 净光合速率 (μmol m⁻² s⁻¹)
        Cₐ: atmospheric CO2 concentration / 大气CO2浓度 (ppm)

    Parameters:
    -----------
    vpd_kpa : float or np.ndarray
        Vapor pressure deficit (kPa) / 水汽压差 (kPa)
    photosynthesis_rate : float or np.ndarray
        Net photosynthesis rate (μmol m⁻² s⁻¹) / 净光合速率 (μmol m⁻² s⁻¹)
    co2_ppm : float or np.ndarray
        Atmospheric CO2 concentration (ppm) / 大气CO2浓度 (ppm)
    g1 : float
        Optimal stomatal conductance parameter (kPa⁰·⁵) / 最优气孔导度参数 (kPa⁰·⁵)
    g0 : float, default=0.0
        Residual conductance (mol m⁻² s⁻¹) / 残余导度 (mol m⁻² s⁻¹)

    Returns:
    --------
    gls : float or np.ndarray
        Leaf stomatal conductance (mol m⁻² s⁻¹) / 叶片气孔导度 (mol m⁻² s⁻¹)

    References:
    -----------
    Medlyn et al. (2011), Global Change Biology, 17(6), 2134-2144
    """
    vpd_kpa = np.asarray(vpd_kpa)
    photosynthesis_rate = np.asarray(photosynthesis_rate)
    co2_ppm = np.asarray(co2_ppm)

    # Prevent division by zero / 防止除零
    vpd_safe = np.maximum(vpd_kpa, 1e-6)
    co2_safe = np.maximum(co2_ppm, 1e-6)

    # Medlyn et al. (2011) equation / Medlyn et al. (2011) 方程
    gls = g0 + 1.6 * (1.0 + g1 / np.sqrt(vpd_safe)) * (photosynthesis_rate / co2_safe)

    return gls


def ecosystem_conductance(leaf_conductance, lai):
    """
    Scale leaf conductance to ecosystem level using LAI.
    使用LAI将叶片导度缩放到生态系统水平。

    Linear upscaling approach from Liu et al. (2023) Equation 2.
    来自 Liu et al. (2023) 方程2 的线性上推方法。

    Formulation / 公式:
    ------------------
    gₑₛ = gₗₛ · LAI

    where / 其中:
        gₑₛ: ecosystem conductance / 生态系统导度 (mol m⁻² s⁻¹)
        gₗₛ: leaf stomatal conductance / 叶片气孔导度 (mol m⁻² s⁻¹)
        LAI: leaf area index / 叶面积指数 (m² m⁻²)

    Parameters:
    -----------
    leaf_conductance : float or np.ndarray
        Leaf stomatal conductance (mol m⁻² s⁻¹) / 叶片气孔导度 (mol m⁻² s⁻¹)
    lai : float or np.ndarray
        Leaf area index (m² m⁻²) / 叶面积指数 (m² m⁻²)

    Returns:
    --------
    ges : float or np.ndarray
        Ecosystem conductance (mol m⁻² s⁻¹) / 生态系统导度 (mol m⁻² s⁻¹)
    """
    lai = np.asarray(lai)
    leaf_conductance = np.asarray(leaf_conductance)

    # Ensure minimum LAI to prevent zero conductance / 确保最小LAI以防止导度为零
    lai_effective = np.maximum(lai, 1e-6)

    ges = leaf_conductance * lai_effective
    return ges


def surface_resistance_from_conductance(ecosystem_conductance_val, temperature):
    """
    Convert ecosystem conductance to surface resistance.
    将生态系统导度转换为表面阻力。

    Based on Liu et al. (2023) Equation 3 with unit conversion.
    基于 Liu et al. (2023) 方程3 及单位换算。

    Formulation / 公式:
    ------------------
    gₑₛ [m s⁻¹] = gₑₛ [mol m⁻² s⁻¹] · (R·T) / P
    rₛ = 1 / gₑₛ [m s⁻¹]

    where / 其中:
        R: universal gas constant / 通用气体常数 (J mol⁻¹ K⁻¹)
        T: absolute temperature / 绝对温度 (K)
        P: atmospheric pressure / 大气压力 (Pa)

    Parameters:
    -----------
    ecosystem_conductance_val : float or np.ndarray
        Ecosystem conductance (mol m⁻² s⁻¹) / 生态系统导度 (mol m⁻² s⁻¹)
    temperature : float or np.ndarray
        Air temperature (°C) / 气温 (°C)

    Returns:
    --------
    rs : float or np.ndarray
        Surface resistance (s m⁻¹) / 表面阻力 (s m⁻¹)
    """
    temperature = np.asarray(temperature)
    ecosystem_conductance_val = np.asarray(ecosystem_conductance_val)

    # Convert to Kelvin / 转换为开尔文
    T_kelvin = temperature + 273.15

    # Convert conductance from mol m⁻² s⁻¹ to m s⁻¹ / 将导度从 mol m⁻² s⁻¹ 转换为 m s⁻¹
    g_m_per_s = ecosystem_conductance_val * (R_GAS * T_kelvin) / P_AIR_PA

    # Ensure minimum conductance to prevent infinite resistance / 确保最小导度以防止无限阻力
    g_m_per_s = np.maximum(g_m_per_s, 1e-12)

    # Surface resistance / 表面阻力
    rs = 1.0 / g_m_per_s

    return rs


# ===== Main EP_Veg Formula / 主EP_Veg公式 =====

def penman_monteith_veg(temperature, net_radiation, wind_speed, vpd,
                        lai, co2_ppm, g1=None, Aww=None,
                        temperature_mean=None, moisture_index=None,
                        species=None, pressure=101.3):
    """
    Calculate PET using the vegetation-aware Penman-Monteith (EP_Veg) method.
    使用植被感知的Penman-Monteith (EP_Veg) 方法计算 PET。

    This advanced method integrates optimal stomatal conductance theory with LAI-based
    canopy scaling to provide physically-based PET estimates that account for vegetation
    responses to environmental conditions and elevated CO2.
    这种先进方法将最优气孔导度理论与基于LAI的冠层缩放相结合，
    提供考虑植被对环境条件和CO2升高响应的基于物理的PET估算。

    Formulation / 公式:
    ------------------
    The method follows Liu et al. (2023) Equations 1-7:

    1. Estimate photosynthesis potential: A ≈ 0.9 · Aww(Ca)
       估算光合潜力：A ≈ 0.9 · Aww(Ca)

    2. Calculate leaf stomatal conductance (Medlyn et al. 2011):
       计算叶片气孔导度 (Medlyn et al. 2011):
       gₗₛ = 1.6 · (1 + g₁/√VPD) · A / Cₐ

    3. Scale to ecosystem conductance:
       缩放到生态系统导度:
       gₑₛ = gₗₛ · LAI

    4. Convert to surface resistance:
       转换为表面阻力:
       rₛ = 1 / [gₑₛ · (R·T)/P]

    5. Apply Penman-Monteith equation:
       应用Penman-Monteith方程:
       ET = [Δ·Rn + ρ·cₚ·VPD/rₐ] / [λ·(Δ + γ·(1 + rₛ/rₐ))]

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
    lai : float or np.ndarray
        Leaf area index (m² m⁻²) / 叶面积指数 (m² m⁻²)
    co2_ppm : float or np.ndarray
        Atmospheric CO2 concentration (ppm) / 大气CO2浓度 (ppm)
    g1 : float, optional
        Optimal stomatal conductance parameter (kPa⁰·⁵) / 最优气孔导度参数 (kPa⁰·⁵)
        If not provided, will estimate from temperature_mean and moisture_index
        如果未提供，将从temperature_mean和moisture_index估算
    Aww : float, optional
        Well-watered photosynthesis potential (μmol m⁻² s⁻¹) / 充分供水光合潜力 (μmol m⁻² s⁻¹)
        If not provided, will estimate from co2_ppm and species
        如果未提供，将从co2_ppm和species估算
    temperature_mean : float, optional
        Mean temperature above 0°C for g1 estimation / 用于g1估算的0°C以上平均温度
        Required if g1 not provided / 如果未提供g1则必需
    moisture_index : float, optional
        Moisture index for g1 estimation / 用于g1估算的湿润指数
        Required if g1 not provided / 如果未提供g1则必需
    species : str, optional
        Vegetation type: "tree", "grass", or "shrub" / 植被类型
        Used for Aww estimation if Aww not provided / 如果未提供Aww则用于Aww估算
    pressure : float or np.ndarray, default=101.3
        Atmospheric pressure (kPa) / 大气压力 (kPa)

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Liu et al. (2023), Journal of Hydrology, 616, 128781
    - Medlyn et al. (2011), Global Change Biology, 17(6), 2134-2144

    Example / 示例:
    ---------------
    >>> # With provided parameters / 使用提供的参数
    >>> pet = penman_monteith_veg(
    ...     temperature=20.0,
    ...     net_radiation=15.0,
    ...     wind_speed=2.5,
    ...     vpd=1.5,
    ...     lai=3.0,
    ...     co2_ppm=400.0,
    ...     g1=5.0,
    ...     Aww=10.0
    ... )
    >>>
    >>> # With automatic parameter estimation / 使用自动参数估算
    >>> pet = penman_monteith_veg(
    ...     temperature=20.0,
    ...     net_radiation=15.0,
    ...     wind_speed=2.5,
    ...     vpd=1.5,
    ...     lai=3.0,
    ...     co2_ppm=400.0,
    ...     temperature_mean=15.0,
    ...     moisture_index=1.2,
    ...     species="tree"
    ... )
    """
    temperature = np.asarray(temperature)
    net_radiation = np.asarray(net_radiation)
    wind_speed = np.asarray(wind_speed)
    vpd = np.asarray(vpd)
    lai = np.asarray(lai)
    co2_ppm = np.asarray(co2_ppm)
    pressure = np.asarray(pressure)

    # Estimate g1 if not provided / 如果未提供则估算g1
    if g1 is None:
        if temperature_mean is None or moisture_index is None:
            raise ValueError(
                "Either g1 must be provided, or both temperature_mean and moisture_index "
                "must be specified for automatic g1 estimation.\n"
                "必须提供g1，或者必须指定temperature_mean和moisture_index以自动估算g1。"
            )
        g1 = estimate_g1(temperature_mean, moisture_index)

    # Estimate Aww if not provided / 如果未提供则估算Aww
    if Aww is None:
        Aww = estimate_Aww(co2_ppm, species=species)

    # Assume well-watered conditions: A ≈ 0.9 * Aww / 假设充分供水条件：A ≈ 0.9 * Aww
    net_photosynthesis = 0.9 * Aww

    # Calculate leaf stomatal conductance / 计算叶片气孔导度
    gls = stomatal_conductance_medlyn2011(vpd, net_photosynthesis, co2_ppm, g1)

    # Scale to ecosystem conductance / 缩放到生态系统导度
    ges = ecosystem_conductance(gls, lai)

    # Convert to surface resistance / 转换为表面阻力
    rs = surface_resistance_from_conductance(ges, temperature)

    # Calculate aerodynamic resistance / 计算空气动力学阻力
    # FAO-56 approximation: ra = 208 / u2 (Equation 6 in Liu et al. 2023)
    # FAO-56 近似：ra = 208 / u2（Liu et al. 2023 方程6）
    wind_speed_safe = np.maximum(wind_speed, 1e-6)
    ra = 208.0 / wind_speed_safe

    # Calculate psychrometric parameters / 计算干湿表参数
    delta = slope_saturation_vapor_pressure(temperature)
    gamma = get_psychrometric_constant(pressure, temperature)

    # Latent heat of vaporization / 汽化潜热
    lambda_v = 2.45  # MJ kg⁻¹

    # Penman-Monteith equation (Liu et al. 2023 Equation 4) / Penman-Monteith 方程
    # Numerator: radiation term + aerodynamic term / 分子：辐射项 + 空气动力学项
    T_kelvin = temperature + 273.15
    numerator = (
        0.408 * delta * net_radiation +
        gamma * (900.0 / T_kelvin) * wind_speed * vpd
    )

    # Denominator / 分母
    denominator = delta + gamma * (1.0 + rs / ra)

    # PET in mm/day / PET (mm/day)
    pet = numerator / denominator

    # Ensure non-negative values / 确保非负值
    pet = np.maximum(pet, 0.0)

    return pet


# Summary of implemented formulas / 实现公式概要
__all__ = [
    'penman_monteith_veg',
    'estimate_g1',
    'estimate_Aww',
    'stomatal_conductance_medlyn2011',
    'ecosystem_conductance',
    'surface_resistance_from_conductance'
]
