
import math
from petlab.formulas import compute_daily_pet

def test_compute_daily_pet_runs():
    # Guangzhou approx lat 23.1N, DOY 100
    val = compute_daily_pet("hargreaves", 23.1, 100, Tmean=20.0, Tmax=28.0, Tmin=12.0)
    assert math.isfinite(val) and val >= 0.0
