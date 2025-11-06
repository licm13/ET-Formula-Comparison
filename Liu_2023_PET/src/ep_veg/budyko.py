from typing import Tuple
import math

def budyko_evaporation(P_mm_d: float, EP_mm_d: float, n: float = 1.9) -> float:
    """
    Budyko 蒸散 (Eq.11).  E/P = [ (P/EP)^n + 1 ]^(-1/n)
    """
    P = max(P_mm_d, 0.0)
    EP = max(EP_mm_d, 1e-9)
    ratio = (P/EP) ** n
    return P * ((1.0 + ratio) ** (-1.0/n))

def budyko_runoff(P_mm_d: float, EP_mm_d: float, n: float = 1.9) -> float:
    """
    Budyko 径流 Q = P - E (Eq.12).
    """
    E = budyko_evaporation(P_mm_d, EP_mm_d, n=n)
    return P_mm_d - E
