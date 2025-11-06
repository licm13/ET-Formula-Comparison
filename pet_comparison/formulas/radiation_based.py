"""
Radiation-based PET formula: Yang & Roderick
基于辐射的潜在蒸散发公式：Yang & Roderick

This module implements the Yang & Roderick (2019) radiation-based PET formulation,
which provides an alternative bulk parameterization of evapotranspiration.
本模块实现了 Yang & Roderick (2019) 基于辐射的PET公式，
提供了蒸散发的替代整体参数化方法。

Scientific References / 科学参考文献:
----------------------------------------
Yang, Y., & Roderick, M. L. (2019). Radiation, surface temperature and evaporation
over wet surfaces. Quarterly Journal of the Royal Meteorological Society, 145(720), 1118-1129.

Integrated from / 从以下项目整合:
---------------------------------
Xiong_PDSI_025/pdsi_cmip6/ep.py
"""

import numpy as np
from ..utils.constants import get_psychrometric_constant, slope_saturation_vapor_pressure


def yang_roderick(temperature, net_radiation, soil_heat_flux=0.0, pressure=101.3, beta=0.24):
    """
    Calculate PET using the Yang & Roderick (2019) radiation-based method.
    使用 Yang & Roderick (2019) 基于辐射的方法计算 PET。

    This formulation provides an alternative to the Priestley-Taylor equation by using
    a different partitioning of available energy. It modifies the denominator term
    to account for radiative feedback effects.
    该公式通过使用不同的可用能量分配方式，提供了 Priestley-Taylor 方程的替代方案。
    它修改了分母项以考虑辐射反馈效应。

    Formulation / 公式:
    ------------------
    PET = [Δ / (Δ + β·γ)] * (Rn - G) / λ

    where / 其中:
        Δ: slope of saturation vapor pressure curve / 饱和水汽压曲线斜率 (kPa °C⁻¹)
        γ: psychrometric constant / 干湿表常数 (kPa °C⁻¹)
        β: empirical coefficient (default 0.24) / 经验系数（默认 0.24）
        Rn: net radiation / 净辐射 (MJ m⁻² day⁻¹)
        G: soil heat flux / 土壤热通量 (MJ m⁻² day⁻¹)
        λ: latent heat of vaporization / 汽化潜热 (MJ kg⁻¹)

    Comparison with Priestley-Taylor / 与 Priestley-Taylor 的比较:
    --------------------------------------------------------------
    - Priestley-Taylor: PET = α * [Δ / (Δ + γ)] * (Rn - G) / λ
      where α ≈ 1.26 is an empirical multiplier
      其中 α ≈ 1.26 是经验乘数

    - Yang-Roderick: PET = [Δ / (Δ + β·γ)] * (Rn - G) / λ
      where β ≈ 0.24 modifies the denominator instead
      其中 β ≈ 0.24 改为修改分母

    The Yang-Roderick formulation accounts for radiative feedback by adjusting the
    psychrometric constant term, rather than multiplying the entire expression.
    Yang-Roderick 公式通过调整干湿表常数项来考虑辐射反馈，
    而不是乘以整个表达式。

    Parameters:
    -----------
    temperature : float or np.ndarray
        Air temperature (°C) / 气温 (°C)
    net_radiation : float or np.ndarray
        Net radiation (MJ m⁻² day⁻¹) / 净辐射 (MJ m⁻² day⁻¹)
    soil_heat_flux : float or np.ndarray, default=0.0
        Soil heat flux (MJ m⁻² day⁻¹) / 土壤热通量 (MJ m⁻² day⁻¹)
        Usually assumed zero for daily timescales
        对于日时间尺度通常假设为零
    pressure : float or np.ndarray, default=101.3
        Atmospheric pressure (kPa) / 大气压力 (kPa)
    beta : float, default=0.24
        Empirical coefficient β / 经验系数 β
        Yang & Roderick (2019) suggest β ≈ 0.24
        Yang & Roderick (2019) 建议 β ≈ 0.24

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Yang & Roderick (2019), Quarterly Journal of the Royal Meteorological Society
    - Xiong & Yang (2025), Scientific Data

    Notes:
    ------
    This formula is particularly useful for analyzing the role of radiative feedback
    in evapotranspiration and provides theoretical insights into the energy balance
    of wet surfaces.
    该公式对于分析辐射反馈在蒸散发中的作用特别有用，
    并提供了对湿表面能量平衡的理论见解。

    Example / 示例:
    ---------------
    >>> pet = yang_roderick(
    ...     temperature=20.0,
    ...     net_radiation=15.0,
    ...     soil_heat_flux=0.0,
    ...     pressure=101.3,
    ...     beta=0.24
    ... )
    """
    temperature = np.asarray(temperature)
    net_radiation = np.asarray(net_radiation)
    soil_heat_flux = np.asarray(soil_heat_flux)
    pressure = np.asarray(pressure)

    # Calculate slope of saturation vapor pressure curve / 计算饱和水汽压曲线斜率
    delta = slope_saturation_vapor_pressure(temperature)

    # Calculate psychrometric constant / 计算干湿表常数
    gamma = get_psychrometric_constant(pressure, temperature)

    # Latent heat of vaporization (approximate) / 汽化潜热（近似值）
    lambda_v = 2.45  # MJ kg⁻¹

    # Yang & Roderick formula / Yang & Roderick 公式
    # PET = [Δ / (Δ + β·γ)] * (Rn - G) / λ
    pet = (delta / (delta + beta * gamma)) * (net_radiation - soil_heat_flux) / lambda_v

    # Ensure non-negative values / 确保非负值
    pet = np.maximum(pet, 0.0)

    return pet


# Summary of implemented formulas / 实现公式概要
__all__ = ['yang_roderick']
