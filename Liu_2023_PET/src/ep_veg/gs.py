from typing import Optional
import math

R_gas = 8.314  # J mol^-1 K^-1
P_air_Pa = 101325.0  # Pa

def stomatal_conductance_M2011(VPD_kPa: float, A_μmol_m2_s: float, Ca_ppm: float, g1_kPa05: float, g0_mol_m2_s: float = 0.0) -> float:
    """
    最优气孔导度 gls (M2011, Eq.1). 单位：mol m^-2 s^-1 (水汽)。
    gls = g0 + 1.6 * (1 + g1 / sqrt(VPD)) * A / Ca
    近无水分限制可取 A ≈ 0.9*Aww.
    """
    if VPD_kPa <= 0:
        VPD_kPa = 1e-6
    return g0_mol_m2_s + 1.6 * (1.0 + g1_kPa05 / (VPD_kPa ** 0.5)) * (A_μmol_m2_s / max(Ca_ppm, 1e-6))

def ecosystem_conductance(gls_mol_m2_s: float, LAI: float) -> float:
    """
    体尺度导度 ges (Eq.2). mol m^-2 s^-1
    """
    LAI_eff = max(LAI, 1e-6)
    return gls_mol_m2_s * LAI_eff

def surface_resistance_from_conductance(ges_mol_m2_s: float, T_C: float = 20.0) -> float:
    """
    由体尺度导度求表面阻力 rs (s m^-1) (Eq.3 + 单位换算):
    g_es[m s^-1] = g_es[mol m^-2 s^-1] * (R*T)/P
    rs = 1 / g_es
    """
    T_K = T_C + 273.15
    g_mps = ges_mol_m2_s * (R_gas * T_K) / P_air_Pa  # m s^-1
    g_mps = max(g_mps, 1e-12)
    return 1.0 / g_mps  # s m^-1
