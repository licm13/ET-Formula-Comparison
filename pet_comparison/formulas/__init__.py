"""
PET Formula implementations / PET 公式实现

This module provides access to all implemented PET formulas, including:
本模块提供对所有实现的 PET 公式的访问，包括：

- Classic methods (Penman-Monteith, Priestley-Taylor) / 经典方法
- Temperature-based methods (Jensen-Haise, Hargreaves, Oudin) / 基于温度的方法
- Radiation-based methods (Yang-Roderick) / 基于辐射的方法
- CO2-aware methods (PM-CO2, PML) / CO2感知方法
- Vegetation-aware methods (EP_Veg, PM-Jarvis) / 植被感知方法
- Complementary relationship methods / 互补关系方法
"""

from .penman_monteith import penman_monteith, penman_monteith_general
from .priestley_taylor import priestley_taylor, priestley_taylor_with_advection
from .priestley_taylor_jpl import priestley_taylor_jpl, priestley_taylor_jpl_partition
from .penman_monteith_leuning import penman_monteith_leuning, pml_v2
from .co2_aware import pm_co2_aware, pm_co2_lai_aware, co2_response_factor
from .complementary_relationship import (
    bouchet_complementary,
    advection_aridity_model,
    cr_nonlinear,
    granger_gray_model,
)

# New formulas from paper integrations / 从论文整合的新公式
from .temperature_based import jensen_haise, hargreaves, oudin
from .radiation_based import yang_roderick
from .penman_monteith_veg import (
    penman_monteith_veg,
    estimate_g1,
    estimate_Aww,
    stomatal_conductance_medlyn2011,
)
from .penman_monteith_jarvis import (
    penman_monteith_jarvis,
    jarvis_solar_radiation_response,
    jarvis_temperature_response,
    jarvis_vpd_response,
    jarvis_co2_response,
)

__all__ = [
    # Classic Penman-Monteith / 经典 Penman-Monteith
    'penman_monteith',
    'penman_monteith_general',
    # Priestley-Taylor
    'priestley_taylor',
    'priestley_taylor_with_advection',
    # PT-JPL
    'priestley_taylor_jpl',
    'priestley_taylor_jpl_partition',
    # PML (Penman-Monteith-Leuning)
    'penman_monteith_leuning',
    'pml_v2',
    # CO2-aware / CO2感知
    'pm_co2_aware',
    'pm_co2_lai_aware',
    'co2_response_factor',
    # Complementary relationship / 互补关系
    'bouchet_complementary',
    'advection_aridity_model',
    'cr_nonlinear',
    'granger_gray_model',
    # Temperature-based / 基于温度
    'jensen_haise',
    'hargreaves',
    'oudin',
    # Radiation-based / 基于辐射
    'yang_roderick',
    # Vegetation-aware (Liu 2023) / 植被感知 (Liu 2023)
    'penman_monteith_veg',
    'estimate_g1',
    'estimate_Aww',
    'stomatal_conductance_medlyn2011',
    # Jarvis-type (Wang 2025) / Jarvis型 (Wang 2025)
    'penman_monteith_jarvis',
    'jarvis_solar_radiation_response',
    'jarvis_temperature_response',
    'jarvis_vpd_response',
    'jarvis_co2_response',
]
