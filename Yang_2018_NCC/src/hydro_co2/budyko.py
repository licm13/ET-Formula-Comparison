\
# -*- coding: utf-8 -*-
"""
Budyko partition using Choudhury (1999) formulation (Eq. 13).
Budyko 分配公式（Choudhury 解析解）。
"""
from __future__ import annotations
import numpy as np

def budyko_choudhury(P, EP, n=1.9):
    """
    Return (E, Q) where Q = P - E, following Eq. (13):
    E/P = 1 + (EP/P) - [1 + (EP/P)^n]^(1/n)
    """
    P = np.asarray(P, dtype=float)
    EP = np.asarray(EP, dtype=float)
    x = np.maximum(EP / np.maximum(P, 1e-9), 0.0)
    E_over_P = 1.0 + x - np.power(1.0 + np.power(x, n), 1.0/n)
    E = E_over_P * P
    Q = P - E
    return E, Q
