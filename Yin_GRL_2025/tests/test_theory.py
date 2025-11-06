import numpy as np
from di_global.theory import p_DI, p_HI, sample_DI

def test_pdf_nonnegative():
    x = np.logspace(-3, 3, 100)
    y = p_DI(x, D0=1.0)
    assert np.all(y >= 0.0)

def test_hi_pdf_nonnegative():
    x = np.logspace(-3, 3, 100)
    y = p_HI(x, H0=1.0)
    assert np.all(y >= 0.0)

def test_sampling_mean_hi():
    # HI 的期望应接近 H0
    D0 = 1.5
    H0 = 1.0 / D0
    di = sample_DI(200000, D0=D0)
    hi = 1.0 / di
    m = hi.mean()
    assert abs(m - H0) < 0.05
