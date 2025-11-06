\
# -*- coding: utf-8 -*-
import numpy as np
from hydro_co2.penman import PM_RC, PM_CO2, PM_OW

def test_smoke():
    T=20.0; Rn=120.0; D=1500.0; u2=2.0
    ep1 = PM_RC(Rn, T, D, u2)
    ep2 = PM_CO2(Rn, T, D, u2, 400.0)
    ep3 = PM_OW(Rn, T, D, u2)
    assert ep1>0 and ep2>0 and ep3>0
