
import numpy as np
from pdsi_cmip6 import pdsi, ep

def test_pdsi_runs():
    t, y, x = 120, 2, 2
    rng = np.random.default_rng(0)
    P  = rng.gamma(shape=2.0, scale=40.0, size=(t,y,x))
    tas = rng.normal(15.0, 8.0, size=(t,y,x))
    rh  = np.clip(rng.normal(60.0, 15.0, size=(t,y,x)), 5, 100)
    ps  = np.full((t,y,x), 101.3)
    u2  = np.clip(rng.normal(2.0, 0.8, size=(t,y,x)), 0.1, None)
    Rn  = rng.normal(9.0, 2.0, size=(t,y,x))
    G   = np.zeros_like(Rn)
    EPd = ep.pm_rc(tas, rh, ps, u2, Rn, G)
    EP  = EPd*30.0

    E   = np.minimum(EP, P*0.7)
    RO  = np.maximum(P - E - 10, 0.0)
    R   = np.maximum(P - E - RO, 0.0)
    L   = rng.uniform(0, 2, size=(t,y,x))

    sc = pdsi.SelfCalibratedPDSI()
    Z, PDSI = sc.compute(P, EP, E=E, R=R, RO=RO, L=L)
    assert Z.shape == PDSI.shape == (t,y,x)
    assert np.isfinite(PDSI).any()
