from typing import Optional
from .utils import slope_svp_kpa_per_C
from .parameters import psychrometric_constant_kpa_per_C, latent_heat_MJ_per_kg
from .gs import stomatal_conductance_M2011, ecosystem_conductance, surface_resistance_from_conductance
from .parameters import estimate_Aww

def _pm_core(T_C: float, Rn_MJ_m2_d: float, U2_m_s: float, VPD_kPa: float, rs_s_m: float, ra_s_m: Optional[float] = None, P_kPa: float = 101.3) -> float:
    """
    Penman–Monteith (日尺度，G≈0) 的通用实现 (Eq.4)，返回 EP (mm d^-1).
    rs, ra: s m^-1
    ra 默认采用 FAO-56 近似 ra = 208 / U2 (Eq.6)
    """
    if ra_s_m is None:
        U2 = max(U2_m_s, 1e-6)
        ra_s_m = 208.0 / U2  # Eq.6

    Δ = slope_svp_kpa_per_C(T_C)
    γ = psychrometric_constant_kpa_per_C(P_kPa)
    λ = latent_heat_MJ_per_kg(T_C)

    num = 0.408 * Δ * Rn_MJ_m2_d + γ * (900.0 / (T_C + 273.0)) * U2_m_s * VPD_kPa
    den = Δ + γ * (1.0 + rs_s_m / ra_s_m)
    return num / den

def ep_pm_rc(T_C: float, Rn_MJ_m2_d: float, U2_m_s: float, VPD_kPa: float, P_kPa: float = 101.3) -> float:
    """
    EP_PM_RC (Eq.13): FAO-56 参考作物（rs = 70 s m^-1, ra = 208 / U2）
    """
    return _pm_core(T_C, Rn_MJ_m2_d, U2_m_s, VPD_kPa, rs_s_m=70.0, ra_s_m=None, P_kPa=P_kPa)

def ep_yang(T_C: float, Rn_MJ_m2_d: float, U2_m_s: float, VPD_kPa: float, Ca_ppm: float, P_kPa: float = 101.3) -> float:
    """
    EP_Yang (Eq.14–15): 将 1 + rs/ra 合并为 {1 + U2*[0.34 + 2.4e-4 (Ca-300)]}
    直接复现文章给出的结构，以便结果可比。
    """
    Δ = slope_svp_kpa_per_C(T_C)
    γ = psychrometric_constant_kpa_per_C(P_kPa)
    num = 0.408 * Δ * Rn_MJ_m2_d + γ * (900.0 / (T_C + 273.0)) * U2_m_s * VPD_kPa
    den = Δ + γ * (1.0 + U2_m_s * (0.34 + 2.4e-4 * (Ca_ppm - 300.0)))
    return num / den

def ep_veg(
    T_C: float,
    Rn_MJ_m2_d: float,
    U2_m_s: float,
    VPD_kPa: float,
    LAI: float,
    Ca_ppm: float,
    Aww_μmol_m2_s: float = None,
    g1_kPa05: float = None,
    g1_args: dict = None,
    P_kPa: float = 101.3,
) -> float:
    """
    EP_Veg (Eq.1–3, 7): 以 gls(M2011) + LAI 线性上推得到 rs，再代入 PM。
    若未提供 Aww/g1，可通过 g1_args 指定 (T_C_mean_above0, MI, log_base, species) 自动估计。
    """
    if g1_kPa05 is None:
        from .parameters import estimate_g1
        if g1_args is None:
            raise ValueError("Provide g1_kPa05 or g1_args={'T_C_mean_above0':..,'MI':..,'log_base': 'ln'/'log10', 'species': Optional}")
        g1_kPa05 = estimate_g1(**{k:v for k,v in g1_args.items() if k in ["T_C_mean_above0","MI","log_base"]})
    if Aww_μmol_m2_s is None:
        species = None if g1_args is None else g1_args.get("species")
        Aww_μmol_m2_s = estimate_Aww(Ca_ppm, species=species)

    # A ≈ 0.9 * Aww（非水分限制日）
    A_net = 0.9 * Aww_μmol_m2_s

    gls = stomatal_conductance_M2011(VPD_kPa=VPD_kPa, A_μmol_m2_s=A_net, Ca_ppm=Ca_ppm, g1_kPa05=g1_kPa05)
    ges = ecosystem_conductance(gls, LAI=LAI)
    rs = surface_resistance_from_conductance(ges, T_C=T_C)

    return _pm_core(T_C, Rn_MJ_m2_d, U2_m_s, VPD_kPa, rs_s_m=rs, ra_s_m=None, P_kPa=P_kPa)
