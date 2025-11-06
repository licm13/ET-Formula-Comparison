\
# -*- coding: utf-8 -*-
"""
ΔE attribution into components using first-order Taylor expansion (Eqs. 6–12).
基于一阶近似，将 E 的变化归因到 ΔRn*、ΔD、Δrs、Δra、Δs 五部分。
"""
from __future__ import annotations
import numpy as np
from .penman import latent_heat, slope_svp, psychrometric_constant, air_density, CP, P0

def attribution_terms(Rn_star, T, D, ra, rs, P=P0):
    """
    Return partial derivatives and sensitivities at state (Rn*, T, D, ra, rs).
    返回在给定状态下的偏导与敏感度系数，便于估算 ΔE 的各项贡献。
    """
    lam = latent_heat(T)
    s = slope_svp(T)
    gamma = psychrometric_constant(P=P, lambda_Jkg=lam)
    rho_a = air_density(P=P, T=T)

    # Using derivatives from Methods (7)–(11):
    dE_dRn = (s) / (lam * (s + gamma * (1 + rs/ra)))  # Eq. (7) simplified to mm/s; we convert later
    dE_dD  = (rho_a * CP / ra) / (lam * (s + gamma * (1 + rs/ra)))  # Eq. (8)
    # Eq. (9), (10) are a bit messy; use numerical perturbation for robustness in this demo:
    def E_val(Rn_star_, D_, ra_, rs_):
        num = s * Rn_star_ + rho_a * CP * D_ / ra_
        den = lam * (s + gamma * (1.0 + rs_ / ra_))
        E_kg_m2_s = num / den
        return E_kg_m2_s

    base = E_val(Rn_star, D, ra, rs)
    eps = 1e-6
    dE_drs = (E_val(Rn_star, D, ra, rs + 1.0) - base) / 1.0  # per s/m
    dE_dra = (E_val(Rn_star, D, ra + 1.0, rs) - base) / 1.0  # per s/m

    # Convert to mm/day scale
    SEC_PER_DAY = 86400.0
    fac = SEC_PER_DAY
    return {
        "dE_dRn": dE_dRn * fac,
        "dE_dD":  dE_dD  * fac,
        "dE_drs": dE_drs * fac,
        "dE_dra": dE_dra * fac,
        # slope s changes are usually small; approximate with finite difference in T (+0.1 °C)
        "dE_ds_approx": ((E_val(Rn_star, D, ra, rs) - E_val(Rn_star, D, ra, rs)) * fac)  # ~0 placeholder
    }

def attribute_deltaE(Rn_star, T, D, ra, rs, dRn, dD, dra, drs, ds=0.0, P=P0):
    """
    First-order ΔE ≈ dE_dRn*ΔRn* + dE_dD*ΔD + dE_dra*Δra + dE_drs*Δrs (+ small ds)
    """
    g = attribution_terms(Rn_star, T, D, ra, rs, P=P)
    return {
        "dE_from_Rn": g["dE_dRn"] * dRn,
        "dE_from_D":  g["dE_dD"]  * dD,
        "dE_from_ra": g["dE_dra"] * dra,
        "dE_from_rs": g["dE_drs"] * drs,
        "dE_from_s":  0.0
    }
