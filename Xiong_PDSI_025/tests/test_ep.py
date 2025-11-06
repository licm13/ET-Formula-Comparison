
import numpy as np
from pdsi_cmip6 import ep

def test_pm_shapes():
    t, y, x = 24, 2, 3
    rng = np.random.default_rng(0)
    tas = rng.normal(15, 5, size=(t,y,x))
    rh  = np.clip(rng.normal(60, 10, size=(t,y,x)), 10, 100)
    ps  = np.full((t,y,x), 101.3)
    u2  = np.clip(rng.normal(2.0, 0.5, size=(t,y,x)), 0.1, None)
    Rn  = rng.normal(8.0, 1.0, size=(t,y,x))
    G   = np.zeros_like(Rn)
    out = ep.pm_rc(tas, rh, ps, u2, Rn, G)
    assert out.shape == (t,y,x)
    assert np.all(np.isfinite(out))
