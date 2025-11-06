"""
Temperature-based PET formulas: Jensen-Haise, Hargreaves, Oudin
温度法潜在蒸散发公式：Jensen-Haise、Hargreaves、Oudin

This module implements three classic temperature-based PET formulas that require minimal
meteorological data. These methods are particularly useful when data availability is limited.
本模块实现了三种经典的基于温度的PET公式，只需最少的气象数据。
这些方法在数据有限时特别有用。

Scientific References / 科学参考文献:
----------------------------------------
1. Jensen, M. E., & Haise, H. R. (1963). Estimating evapotranspiration from solar radiation.
   Journal of the Irrigation and Drainage Division, 89(4), 15-41.

2. Hargreaves, G. H., & Samani, Z. A. (1985). Reference crop evapotranspiration from temperature.
   Applied Engineering in Agriculture, 1(2), 96-99.

3. Oudin, L., et al. (2005). Which potential evapotranspiration input for a lumped rainfall-runoff model?
   Journal of Hydrology, 303(1-4), 290-306.

Integrated from sub-projects / 从子项目整合:
-------------------------------------------
- Jensen-Haise & Hargreaves: Pimentel_2023_WRR/src/petlab/formulas.py
- Oudin: Xiong_PDSI_025/pdsi_cmip6/ep.py
"""

import numpy as np
from ..utils.constants import get_latent_heat
from ..utils.meteorology import extraterrestrial_radiation


def jensen_haise(temperature, radiation=None, doy=None, latitude=None,
                 temperature_offset=5.0, temperature_scale=100.0, crop_coefficient=1.0):
    """
    Calculate PET using the Jensen-Haise (Oudin-style) temperature-based method.
    使用 Jensen-Haise (Oudin 风格) 温度法计算 PET。

    This simplified formula estimates PET based on temperature and extraterrestrial radiation.
    It's particularly useful for hydrological modeling when data is limited.
    这个简化公式基于温度和天文辐射估算PET。在数据有限时特别适用于水文建模。

    Formulation / 公式:
    ------------------
    PET = kc * (Ra / λ) * (T + T_add) / T_scale, if (T + T_add) > 0, else 0

    where / 其中:
        kc: crop coefficient / 作物系数
        Ra: extraterrestrial radiation / 天文辐射 (MJ m⁻² day⁻¹)
        λ: latent heat of vaporization / 汽化潜热 (MJ kg⁻¹)
        T: mean temperature / 平均温度 (°C)
        T_add: temperature offset (default 5°C) / 温度偏移 (默认 5°C)
        T_scale: temperature scaling factor (default 100°C) / 温度缩放因子 (默认 100°C)

    Parameters:
    -----------
    temperature : float or np.ndarray
        Mean air temperature (°C) / 平均气温 (°C)
    radiation : float or np.ndarray, optional
        Extraterrestrial radiation (MJ m⁻² day⁻¹) / 天文辐射 (MJ m⁻² day⁻¹)
        If not provided, will be calculated from doy and latitude
        如果未提供，将从日序和纬度计算
    doy : int or np.ndarray, optional
        Day of year (1-365) / 日序 (1-365)
        Required if radiation not provided / 如果未提供辐射则必需
    latitude : float or np.ndarray, optional
        Latitude in degrees / 纬度（度）
        Required if radiation not provided / 如果未提供辐射则必需
    temperature_offset : float, default=5.0
        Temperature offset T_add (°C) / 温度偏移 T_add (°C)
    temperature_scale : float, default=100.0
        Temperature scaling factor T_scale (°C) / 温度缩放因子 T_scale (°C)
    crop_coefficient : float, default=1.0
        Crop coefficient kc / 作物系数 kc

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Oudin et al. (2005), Journal of Hydrology
    - Pimentel et al. (2023), Water Resources Research
    - Xiong & Yang (2025), Scientific Data

    Example / 示例:
    ---------------
    >>> # Using pre-calculated radiation / 使用预计算的辐射
    >>> pet = jensen_haise(temperature=20.0, radiation=30.0)
    >>>
    >>> # Auto-calculate radiation / 自动计算辐射
    >>> pet = jensen_haise(temperature=20.0, doy=180, latitude=45.0)
    """
    temperature = np.asarray(temperature)

    # Calculate or use provided radiation / 计算或使用提供的辐射
    if radiation is None:
        if doy is None or latitude is None:
            raise ValueError("If radiation is not provided, both doy and latitude must be specified.\n"
                           "如果未提供辐射，则必须指定日序和纬度。")
        Ra = extraterrestrial_radiation(doy, latitude)
    else:
        Ra = np.asarray(radiation)

    # Latent heat of vaporization (approximate) / 汽化潜热（近似值）
    lambda_v = 2.45  # MJ kg⁻¹, typical value for ~20°C / 约20°C的典型值

    # Apply formula / 应用公式
    temp_term = temperature + temperature_offset
    pet = np.where(
        temp_term > 0,
        crop_coefficient * (Ra / lambda_v) * (temp_term / temperature_scale),
        0.0
    )

    return pet


def hargreaves(temperature_mean, temperature_max, temperature_min,
               radiation=None, doy=None, latitude=None, crop_coefficient=1.0):
    """
    Calculate PET using the Hargreaves temperature-based method.
    使用 Hargreaves 温度法计算 PET。

    This widely-used formula estimates PET from temperature range and extraterrestrial radiation.
    It's particularly popular for its simplicity and reasonable accuracy with minimal data.
    这个广泛使用的公式从温度范围和天文辐射估算PET。
    因其简单性和数据需求少而准确度合理而特别受欢迎。

    Formulation / 公式:
    ------------------
    PET = 0.0023 * Ra * (T_mean + 17.8) * √(T_max - T_min)

    where / 其中:
        Ra: extraterrestrial radiation / 天文辐射 (MJ m⁻² day⁻¹)
        T_mean: mean temperature / 平均温度 (°C)
        T_max: maximum temperature / 最高温度 (°C)
        T_min: minimum temperature / 最低温度 (°C)

    Parameters:
    -----------
    temperature_mean : float or np.ndarray
        Mean air temperature (°C) / 平均气温 (°C)
    temperature_max : float or np.ndarray
        Maximum air temperature (°C) / 最高气温 (°C)
    temperature_min : float or np.ndarray
        Minimum air temperature (°C) / 最低气温 (°C)
    radiation : float or np.ndarray, optional
        Extraterrestrial radiation (MJ m⁻² day⁻¹) / 天文辐射 (MJ m⁻² day⁻¹)
        If not provided, will be calculated from doy and latitude
        如果未提供，将从日序和纬度计算
    doy : int or np.ndarray, optional
        Day of year (1-365) / 日序 (1-365)
        Required if radiation not provided / 如果未提供辐射则必需
    latitude : float or np.ndarray, optional
        Latitude in degrees / 纬度（度）
        Required if radiation not provided / 如果未提供辐射则必需
    crop_coefficient : float, default=1.0
        Crop coefficient kc / 作物系数 kc

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Hargreaves & Samani (1985), Applied Engineering in Agriculture
    - Pimentel et al. (2023), Water Resources Research

    Example / 示例:
    ---------------
    >>> pet = hargreaves(
    ...     temperature_mean=20.0,
    ...     temperature_max=28.0,
    ...     temperature_min=12.0,
    ...     doy=180,
    ...     latitude=45.0
    ... )
    """
    temperature_mean = np.asarray(temperature_mean)
    temperature_max = np.asarray(temperature_max)
    temperature_min = np.asarray(temperature_min)

    # Calculate or use provided radiation / 计算或使用提供的辐射
    if radiation is None:
        if doy is None or latitude is None:
            raise ValueError("If radiation is not provided, both doy and latitude must be specified.\n"
                           "如果未提供辐射，则必须指定日序和纬度。")
        Ra = extraterrestrial_radiation(doy, latitude)
    else:
        Ra = np.asarray(radiation)

    # Temperature range (ensure non-negative) / 温度范围（确保非负）
    temp_range = np.maximum(temperature_max - temperature_min, 0.0)

    # Temperature term (ensure non-negative) / 温度项（确保非负）
    temp_term = np.maximum(temperature_mean + 17.8, 0.0)

    # Hargreaves formula / Hargreaves 公式
    pet = 0.0023 * Ra * temp_term * np.sqrt(temp_range)

    # Apply crop coefficient / 应用作物系数
    pet = crop_coefficient * pet

    return pet


def oudin(temperature, radiation=None, doy=None, latitude=None):
    """
    Calculate PET using the Oudin temperature-based method.
    使用 Oudin 温度法计算 PET。

    This formula provides a simple temperature-based PET estimate that is particularly
    suitable for hydrological modeling at the catchment scale.
    这个公式提供了一个简单的基于温度的PET估算，特别适用于流域尺度的水文建模。

    Formulation / 公式:
    ------------------
    PET = (Ra * (T + 5)) / (100 * λ * ρ_w), if T > -5°C, else 0

    where / 其中:
        Ra: extraterrestrial radiation / 天文辐射 (MJ m⁻² day⁻¹)
        T: air temperature / 气温 (°C)
        λ: latent heat of vaporization / 汽化潜热 (MJ kg⁻¹)
        ρ_w: water density / 水密度 (kg m⁻³)

    Parameters:
    -----------
    temperature : float or np.ndarray
        Air temperature (°C) / 气温 (°C)
    radiation : float or np.ndarray, optional
        Extraterrestrial radiation (MJ m⁻² day⁻¹) / 天文辐射 (MJ m⁻² day⁻¹)
        If not provided, will be calculated from doy and latitude
        如果未提供，将从日序和纬度计算
    doy : int or np.ndarray, optional
        Day of year (1-365) / 日序 (1-365)
        Required if radiation not provided / 如果未提供辐射则必需
    latitude : float or np.ndarray, optional
        Latitude in degrees / 纬度（度）
        Required if radiation not provided / 如果未提供辐射则必需

    Returns:
    --------
    pet : float or np.ndarray
        Potential evapotranspiration (mm day⁻¹) / 潜在蒸散发 (mm day⁻¹)

    References:
    -----------
    - Oudin et al. (2005), Journal of Hydrology
    - Xiong & Yang (2025), Scientific Data

    Notes:
    ------
    The formula uses a temperature threshold of -5°C (here coded as +5°C offset).
    Below this threshold, PET is set to zero.
    公式使用-5°C的温度阈值（此处编码为+5°C偏移）。
    低于此阈值时，PET设为零。

    Example / 示例:
    ---------------
    >>> pet = oudin(temperature=20.0, doy=180, latitude=45.0)
    """
    temperature = np.asarray(temperature)

    # Calculate or use provided radiation / 计算或使用提供的辐射
    if radiation is None:
        if doy is None or latitude is None:
            raise ValueError("If radiation is not provided, both doy and latitude must be specified.\n"
                           "如果未提供辐射，则必须指定日序和纬度。")
        Ra = extraterrestrial_radiation(doy, latitude)
    else:
        Ra = np.asarray(radiation)

    # Constants / 常数
    lambda_v = 2.45  # Latent heat (MJ kg⁻¹) / 汽化潜热 (MJ kg⁻¹)
    rho_w = 1000.0   # Water density (kg m⁻³) / 水密度 (kg m⁻³)

    # Oudin formula with temperature threshold / Oudin公式带温度阈值
    # Original: EP = Ra * (T + 5) / (100 * λ * ρ_w/1000), if T > -5
    # Simplified: EP = Ra * (T + 5) / (100 * λ), if T > -5
    pet = np.where(
        temperature > -5.0,
        (Ra * (temperature + 5.0)) / (100.0 * lambda_v),
        0.0
    )

    return pet


# Summary of implemented formulas / 实现公式概要
__all__ = ['jensen_haise', 'hargreaves', 'oudin']
