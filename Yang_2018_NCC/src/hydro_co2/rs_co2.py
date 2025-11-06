\
# -*- coding: utf-8 -*-
"""
Surface resistance rs and its [CO2] dependence (Eq. 1), plus a toy inverter.
叶面积指数不变条件下，rs 随 [CO2] 增大而增大（式1）。此处以教学为主。
"""
from __future__ import annotations
import numpy as np
from .penman import penman_monteith, aerodynamic_resistance, latent_heat, slope_svp, psychrometric_constant, air_density, CP, P0

def rs_from_co2(co2_ppm, rs_300=55.0, sensitivity_pct_per_ppm=0.0009):
    """
    Eq. (1): rs = rs_300 * [1 + S*(CO2 - 300)]
    其中 S 约为 0.09% ppm^-1 => 0.0009 per ppm
    """
    return rs_300 * (1.0 + sensitivity_pct_per_ppm * (co2_ppm - 300.0))

def invert_rs_from_E(Rn_star, T, D, u2, E_mm_day, P=P0):
    """
    Educational inversion: given measured E (mm/day), solve for rs in PM equation (approx).
    仅用于教学演示，未考虑稳定度等复杂因素。
    """
    # We solve penman_monteith for rs with a simple 1D search (bisection) to match E.
    ra = aerodynamic_resistance(u2)
    target = E_mm_day
    lo, hi = 0.0, 500.0  # plausible rs range in s/m
    for _ in range(60):
        mid = 0.5*(lo+hi)
        Emid = penman_monteith(Rn_star, T, D, ra, mid, P=P)
        if Emid > target:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)
