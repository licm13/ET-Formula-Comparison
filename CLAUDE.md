# CLAUDE.md - AI Assistant Guide for ET-Formula-Comparison

**Version:** 1.0.0
**Last Updated:** 2025-11-17
**Repository:** ET-Formula-Comparison (PET & AET Formula Comparison Framework)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Code Architecture](#code-architecture)
4. [Development Workflows](#development-workflows)
5. [Key Conventions](#key-conventions)
6. [Testing Practices](#testing-practices)
7. [Common Tasks](#common-tasks)
8. [Important Gotchas](#important-gotchas)
9. [Git Workflow](#git-workflow)
10. [Resources](#resources)

---

## 🎯 Project Overview

### Purpose
This is a **production-ready scientific computing framework** for comparing:
- **AET** (Actual Evapotranspiration) models - 6 major implementations
- **PET** (Potential Evapotranspiration) formulas - 20+ formulas

### Scientific Context
The framework integrates methods from landmark papers in hydrology and climate science:
- Liu et al. (2023) - EP_Veg vegetation-aware PET
- Yang et al. (2019) - PM-CO2 climate change impacts
- Pimentel et al. (2023) - Temperature-based PET methods
- Wang et al. (2025) - PM-Jarvis stomatal models
- Xiong & Yang (2025) - PDSI drought indices

### Target Users
- Hydrologists studying water availability
- Climate scientists analyzing CO2 impacts
- Remote sensing researchers using satellite data
- Drought monitoring systems

### Publication Goals
Target journals: Nature Water, Nature Climate Change, Water Resources Research

---

## 📁 Repository Structure

### Top-Level Architecture

```
ET-Formula-Comparison/
├── py_et_lib/              # NEW: Modern AET models (xarray-based, OOP)
├── pet_comparison/         # ORIGINAL: PET formulas (numpy-based, functional)
├── Liu_2023_PET/           # Paper replica: EP_Veg
├── Pimentel_2023_WRR/      # Paper replica: Temperature methods
├── Yang_2018_NCC/          # Paper replica: PM-CO2
├── Xiong_PDSI_025/         # Paper replica: PDSI
├── Wang_2025_PET_Paradox/  # Paper replica: PM-Jarvis
├── Yin_GRL_2025/           # Paper replica: Aridity
├── examples/               # Unified examples
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

### Library Distinction (CRITICAL)

#### py_et_lib/ - Modern AET Framework
- **Paradigm:** Object-oriented
- **Data format:** xarray.Dataset (labeled multi-dimensional arrays)
- **Models:** MOD16, PMLv2, PTJPL, GLEAM, SEBAL, SSEBop
- **Organization:** By algorithm family (P-M, P-T, SEB)
- **Output:** xarray.Dataset with 'AET' variable (mm/day)
- **Use case:** Actual ET from remote sensing, complex models

#### pet_comparison/ - Legacy PET Library
- **Paradigm:** Functional programming
- **Data format:** NumPy arrays, pandas DataFrames
- **Formulas:** 20+ PET methods
- **Organization:** By method type (temperature, radiation, CO2-aware)
- **Output:** NumPy arrays (mm/day)
- **Use case:** Potential ET, climate projections, simple formulas

### Paper Replica Structure

Each paper replica follows this pattern:
```
Paper_Name/
├── src/
│   └── package_name/       # Installable package
│       ├── __init__.py
│       ├── formulas.py     # Core implementations
│       └── utils.py        # Helper functions
├── examples/               # Working demonstrations
├── tests/                  # Unit tests
├── pyproject.toml          # Modern packaging
└── README.md               # Paper-specific docs
```

**Key principle:** After refactoring (Nov 2025), paper replicas **import** core functions from main libraries instead of duplicating code.

---

## 🏗️ Code Architecture

### Design Patterns

#### 1. Single Source of Truth (SSOT)
**Critical:** All physical constant calculations centralized in:
- `/home/user/ET-Formula-Comparison/pet_comparison/utils/constants.py`

**Functions (DO NOT duplicate):**
- `saturation_vapor_pressure(temperature)` - Tetens formula (kPa)
- `slope_saturation_vapor_pressure(temperature)` - es curve slope (kPa/°C)
- `get_psychrometric_constant(pressure, temperature)` - gamma (kPa/°C)
- `get_latent_heat(temperature)` - lambda (MJ/kg)

**Why this matters:** Numerical consistency across all formulas. Any duplication will be flagged during code review.

#### 2. Inheritance Hierarchy (py_et_lib)

```python
EvapotranspirationModel (Abstract Base Class)
├── _validate_inputs()      # Abstract
├── compute_et()             # Abstract - MUST return xr.Dataset with 'AET'
└── partition_components()   # Optional - returns component breakdown

Algorithm Family Base Classes:
├── PenmanMonteithBase       # Resistance-based models
├── PriestleyTaylorBase      # Energy-limited + stress factors
└── EnergyBalanceBase        # Thermal residual methods

Concrete Implementations:
MOD16 < PenmanMonteithBase
PMLv2 < PenmanMonteithBase
PTJPL < PriestleyTaylorBase
GLEAM < PriestleyTaylorBase
SEBAL < EnergyBalanceBase
SSEBop < EnergyBalanceBase
```

**Template method pattern:** Base class defines workflow, subclasses implement specifics.

#### 3. Functional PET Formulas

Located in `pet_comparison/formulas/`:
- Each formula is a **standalone function**
- Pure functions: same input → same output
- No global state dependencies
- Accept numpy arrays or scalars
- Return numpy arrays or scalars

### Module Organization

#### pet_comparison/
```
formulas/
├── penman_monteith.py          # Classic PM, FAO-56
├── priestley_taylor.py         # PT variants
├── priestley_taylor_jpl.py     # PT-JPL with partitioning
├── penman_monteith_leuning.py  # PML models
├── co2_aware.py                # PM-CO2 variants
├── temperature_based.py        # Jensen-Haise, Hargreaves, Oudin
├── radiation_based.py          # Yang-Roderick
├── penman_monteith_veg.py      # EP_Veg (Medlyn stomatal)
├── penman_monteith_jarvis.py   # PM-Jarvis (multiplicative)
└── complementary_relationship.py # CR models

utils/
├── constants.py                # Physical constants (SSOT)
└── meteorology.py              # Radiation, pressure calculations

analysis/
├── comparison.py               # PETComparison class
└── visualization.py            # Plotting functions
```

#### py_et_lib/
```
core/
├── base_models.py              # Abstract base classes
├── constants.py                # Physical constants
└── __init__.py

models/
├── aet.py                      # MOD16, PMLv2, PTJPL, GLEAM
├── seb.py                      # SEBAL, SSEBop
└── __init__.py

utils/
├── validators.py               # Input validation
└── meteorology.py              # Helper calculations
```

---

## 🔄 Development Workflows

### Adding a New PET Formula

**Location:** `pet_comparison/formulas/`

**Template:**
```python
"""
Formula Name: Author et al. (Year)

Reference:
    Author, A. et al. (Year). Title. Journal, vol(issue), pages.
"""

import numpy as np
from ..utils.constants import (
    saturation_vapor_pressure,
    slope_saturation_vapor_pressure,
    get_psychrometric_constant
)

def new_formula_name(
    temperature,           # °C
    relative_humidity,     # % (0-100)
    net_radiation,         # MJ m^-2 day^-1
    pressure=101.3,        # kPa (default: sea level)
    **kwargs
):
    """
    Calculate PET using New Formula / 使用新公式计算PET

    Parameters
    ----------
    temperature : float or array-like
        Air temperature (°C)
    relative_humidity : float or array-like
        Relative humidity (%)
    net_radiation : float or array-like
        Net radiation (MJ m^-2 day^-1)
    pressure : float or array-like, optional
        Atmospheric pressure (kPa), default 101.3

    Returns
    -------
    PET : float or array-like
        Potential evapotranspiration (mm/day)

    References
    ----------
    Author et al. (Year). Title. Journal.

    Notes
    -----
    - Ensure units match documentation
    - Add validation for edge cases
    """
    # Convert inputs to numpy arrays
    T = np.asarray(temperature)
    RH = np.asarray(relative_humidity)
    Rn = np.asarray(net_radiation)
    P = np.asarray(pressure)

    # Calculate physical constants
    es = saturation_vapor_pressure(T)
    delta = slope_saturation_vapor_pressure(T)
    gamma = get_psychrometric_constant(P, T)

    # Your formula implementation
    # ...

    # Ensure non-negative output
    PET = np.maximum(PET, 0.0)

    return PET
```

**Testing checklist:**
1. Test scalar input
2. Test array input
3. Test physical behavior (e.g., higher T → higher PET)
4. Test edge cases (T=0, RH=100, Rn=0)
5. Add to `tests/test_formulas.py`

### Adding a New AET Model

**Location:** `py_et_lib/models/aet.py`

**Template:**
```python
from ..core.base_models import PenmanMonteithBase  # or appropriate base
from ..core.constants import CONSTANTS
from ..utils.validators import ensure_params, ensure_variables

class NewAETModel(PenmanMonteithBase):
    """
    New AET Model (Author et al., Year)

    Algorithm family: Penman-Monteith resistance-based

    Required variables:
        - T_mean: Air temperature (°C)
        - Rn: Net radiation (W/m²)
        - VPD: Vapor pressure deficit (kPa)
        - u2: Wind speed at 2m (m/s)
        - LAI: Leaf area index (m²/m²)

    Parameters
    ----------
    param1 : type
        Description

    References
    ----------
    Author et al. (Year). Title. Journal.
    """

    def __init__(self, param1=default1, **kwargs):
        self.param1 = param1
        super().__init__(**kwargs)

    def _validate_inputs(self):
        """Validate model parameters."""
        required = ['param1']
        ensure_params(self.params, required)

    def compute_et(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Compute AET using New Model.

        Parameters
        ----------
        ds : xr.Dataset
            Input dataset with required variables

        Returns
        -------
        result : xr.Dataset
            Dataset with 'AET' variable (mm/day)
        """
        # Validate required variables
        required_vars = ['T_mean', 'Rn', 'VPD', 'u2', 'LAI']
        ensure_variables(ds, required_vars)

        # Extract variables
        T = ds['T_mean']
        Rn = ds['Rn']
        # ...

        # Compute AET
        aet = ...  # Your implementation

        # Return as Dataset
        return xr.Dataset({'AET': aet})

    def partition_components(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Optional: Partition ET into components.

        Returns
        -------
        components : xr.Dataset
            Dataset with 'transpiration', 'soil_evaporation', etc.
        """
        # Implementation if model supports partitioning
        raise NotImplementedError()
```

**Integration steps:**
1. Add to `py_et_lib/models/__init__.py`
2. Add example to `examples/aet_comparison.py`
3. Add tests to `tests/test_aet_models.py`
4. Update `README.md` model table

### Integrating a New Paper Replica

**When:** You're implementing methods from a new scientific paper

**Structure:**
```bash
# 1. Create directory
mkdir Paper_Author_Year
cd Paper_Author_Year

# 2. Create package structure
mkdir -p src/package_name examples tests

# 3. Create pyproject.toml
cat > pyproject.toml <<EOF
[project]
name = "package_name"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["numpy", "pandas", "matplotlib"]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
EOF

# 4. Create src/package_name/__init__.py
# 5. Implement formulas in src/package_name/formulas.py
# 6. IMPORT from main library (DO NOT duplicate):
```

**Critical import pattern:**
```python
# In Paper_Replica/src/package/formulas.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from pet_comparison.utils.constants import (
    saturation_vapor_pressure,
    slope_saturation_vapor_pressure,
    get_psychrometric_constant,
    get_latent_heat
)

# Wrapper function for backward compatibility if needed
def _svp(T_C):
    """Wrapper maintaining original API."""
    return saturation_vapor_pressure(T_C)
```

---

## 📝 Key Conventions

### Naming Conventions

#### Functions
- **PET formulas:** `lowercase_with_underscores`
  - Good: `penman_monteith()`, `priestley_taylor()`
  - Bad: `PM()`, `PenmanMonteith()`, `pm()`
- **Helper functions:** `verb_noun` or `get_property`
  - Good: `calculate_resistance()`, `get_latent_heat()`
- **Private functions:** `_leading_underscore()`
  - Good: `_validate_inputs()`, `_calc_alpha_term()`

#### Classes
- **CamelCase:** `MOD16`, `PMLv2`, `PTJPL`
- **Base classes:** `EvapotranspirationModel`, `PenmanMonteithBase`
- **Analysis classes:** `PETComparison`, `SpatialAnalyzer`

#### Variables
- **Scientific notation:** Match variable names to equations
  - `T_mean`, `T_max`, `T_min` (temperature)
  - `Rn` (net radiation)
  - `VPD` (vapor pressure deficit)
  - `LAI` (leaf area index)
  - `fAPAR` (fraction of absorbed PAR)
  - `u2` (wind speed at 2m)

### Unit Conventions (CRITICAL)

**Standard units across entire codebase:**

| Variable | Unit | Symbol | Notes |
|----------|------|--------|-------|
| Temperature | °C | T | Celsius (NOT Kelvin for input) |
| Radiation | MJ m⁻² day⁻¹ | Rn, Rs, Ra | OR W m⁻² (check docstring) |
| Pressure | kPa | P, VPD | NOT Pa (divide by 1000) |
| Wind speed | m s⁻¹ | u2, WS | At 2m height |
| Humidity | % | RH | 0-100 scale (NOT 0-1) |
| ET/PET | mm day⁻¹ | ET, PET, AET | Output standard |
| LAI | m² m⁻² | LAI | Dimensionless ratio |
| CO2 | ppm | CO2, Ca | Parts per million |

**Always check docstrings for actual units used!**

### Code Style

#### Documentation
**Bilingual support (English/Chinese):**
```python
def calculate_something(...):
    """
    Calculate something important / 计算重要的东西

    Parameters
    ----------
    temperature : float
        Air temperature (°C) / 气温

    Returns
    -------
    result : float
        The result (mm/day) / 结果
    """
```

#### Defensive Programming
```python
# Prevent division by zero
wind_speed_safe = np.maximum(wind_speed, 0.5)

# Clip to valid ranges
RH = np.clip(relative_humidity, 0.0, 100.0)

# Ensure non-negative ET
ET = np.maximum(ET, 0.0)

# Handle missing data
if np.any(np.isnan(temperature)):
    raise ValueError("Temperature contains NaN values")
```

#### Performance
**After Nov 2025 refactoring:**
- **Prefer vectorization** over loops
- Use `np.vectorize()` for backward compatibility
- Avoid list comprehensions with large arrays

**Example:**
```python
# GOOD (vectorized)
EP = np.vectorize(ep_pm_rc)(T, Rn, U2, VPD)

# BAD (loop)
EP = np.array([ep_pm_rc(t, r, u, v) for t, r, u, v in zip(T, Rn, U2, VPD)])
```

---

## 🧪 Testing Practices

### Framework
- **pytest** - standard testing framework
- Run: `pytest tests/ -v`

### Test Organization
```
tests/
├── test_formulas.py          # PET formula tests
├── test_aet_models.py        # AET model tests
├── test_utils.py             # Utility function tests
└── test_comparison.py        # Analysis framework tests
```

### Test Patterns

#### 1. Sanity Checks
```python
def test_penman_monteith_positive():
    """ET should always be non-negative."""
    pet = penman_monteith(T=20, RH=60, wind=2.5, Rn=15)
    assert pet >= 0
```

#### 2. Physical Behavior
```python
def test_co2_reduces_pet():
    """Higher CO2 should reduce PET (stomatal closure)."""
    pet_380 = pm_co2_aware(T=20, RH=60, wind=2.5, Rn=15, co2=380)
    pet_550 = pm_co2_aware(T=20, RH=60, wind=2.5, Rn=15, co2=550)
    assert pet_550 < pet_380
```

#### 3. Array Handling
```python
def test_handles_arrays():
    """Formula should work with numpy arrays."""
    T = np.array([10, 15, 20, 25])
    pet = penman_monteith(T=T, RH=60, wind=2.5, Rn=15)
    assert pet.shape == T.shape
```

#### 4. Component Consistency
```python
def test_component_partitioning():
    """Components should sum to total."""
    pmlv2 = PMLv2()
    components = pmlv2.partition_components(ds)
    total = components['transpiration'] + components['soil_evaporation']
    aet = pmlv2.compute_et(ds)['AET']
    np.testing.assert_allclose(total, aet, rtol=1e-5)
```

#### 5. Edge Cases
```python
def test_zero_radiation():
    """ET should be zero when radiation is zero."""
    pet = priestley_taylor(T=20, Rn=0, pressure=101.3)
    assert pet == 0
```

### Running Tests
```bash
# All tests
pytest tests/

# Specific file
pytest tests/test_formulas.py -v

# Specific test
pytest tests/test_formulas.py::test_penman_monteith_positive -v

# With coverage
pytest tests/ --cov=pet_comparison --cov-report=html
```

---

## 🔧 Common Tasks

### Task 1: Compare Multiple PET Formulas

```python
import pandas as pd
import numpy as np
from pet_comparison.analysis import PETComparison

# Prepare forcing data
dates = pd.date_range('2020-01-01', periods=365, freq='D')
forcing = pd.DataFrame({
    'temperature': 20 + 10 * np.sin(2 * np.pi * np.arange(365) / 365),
    'relative_humidity': 60.0,
    'wind_speed': 2.5,
    'net_radiation': 15.0,
    'lai': 3.0,
    'co2': 400.0,
    'doy': np.arange(1, 366),
    'latitude': 45.0,
}, index=dates)

# Run comparison
comparison = PETComparison(forcing)
results = comparison.run_all()

# Get statistics
stats = comparison.compute_statistics()
print(stats)

# Get correlations
corr = comparison.compute_correlations()
print(corr)
```

### Task 2: Run AET Models

```python
import xarray as xr
import numpy as np
import pandas as pd
from py_et_lib.models import MOD16, PMLv2, PTJPL

# Create xarray Dataset
dates = pd.date_range('2020-01-01', periods=365, freq='D')
day_of_year = np.arange(365)

ds = xr.Dataset({
    'T_mean': (['time'], 15 + 12 * np.sin(2 * np.pi * day_of_year / 365)),
    'Rn': (['time'], 150 + 100 * np.sin(2 * np.pi * day_of_year / 365)),
    'RH': (['time'], np.ones(365) * 65),
    'VPD': (['time'], 1.0 + 0.5 * np.sin(2 * np.pi * day_of_year / 365)),
    'u2': (['time'], np.ones(365) * 2.5),
    'LAI': (['time'], 3.0 + 1.5 * np.sin(2 * np.pi * day_of_year / 365)),
}, coords={'time': dates})

# Run models
mod16 = MOD16(bplut_params={})
aet_mod16 = mod16.compute_et(ds)['AET']

pmlv2 = PMLv2()
aet_pmlv2 = pmlv2.compute_et(ds)['AET']

# Component partitioning
components = pmlv2.partition_components(ds)
transp = components['transpiration']
evap = components['soil_evaporation']
```

### Task 3: Analyze CO2 Sensitivity

```python
from pet_comparison.formulas import pm_co2_aware, penman_monteith

# Test CO2 levels
co2_levels = [280, 380, 550, 900]  # ppm

for co2 in co2_levels:
    pet_co2 = pm_co2_aware(
        temperature=20.0,
        relative_humidity=60.0,
        wind_speed=2.5,
        net_radiation=15.0,
        co2=co2
    )

    # Compare with CO2-agnostic PM
    pet_pm = penman_monteith(
        temperature=20.0,
        relative_humidity=60.0,
        wind_speed=2.5,
        net_radiation=15.0
    )

    diff = ((pet_co2 - pet_pm) / pet_pm) * 100
    print(f"CO2={co2:4d} ppm: PET_CO2={pet_co2:.2f} mm/d ({diff:+.1f}%)")
```

### Task 4: Spatial Analysis

```python
import xarray as xr
import numpy as np

# Create spatial dataset (lat, lon, time)
nlat, nlon, ntime = 72, 144, 365
lat = np.linspace(-90, 90, nlat)
lon = np.linspace(-180, 180, nlon)
time = pd.date_range('2020-01-01', periods=ntime, freq='D')

# Create 3D forcing data
T_spatial = xr.DataArray(
    np.random.randn(ntime, nlat, nlon) * 10 + 15,
    dims=['time', 'lat', 'lon'],
    coords={'time': time, 'lat': lat, 'lon': lon}
)

ds_spatial = xr.Dataset({
    'T_mean': T_spatial,
    'Rn': T_spatial * 0 + 150,  # Example constant
    # ... other variables
})

# Run model
mod16 = MOD16()
aet_spatial = mod16.compute_et(ds_spatial)['AET']

# Calculate global mean time series
aet_global = aet_spatial.mean(dim=['lat', 'lon'])

# Calculate spatial mean
aet_timemean = aet_spatial.mean(dim='time')
```

### Task 5: PDSI Calculation

```python
import sys
sys.path.insert(0, 'Xiong_PDSI_025')
from pdsi_cmip6.pdsi import SelfCalibratedPDSI

# Prepare monthly data
P_monthly = ...   # Precipitation (mm/month)
PET_monthly = ... # PET (mm/month)

# Initialize PDSI calculator
pdsi_calc = SelfCalibratedPDSI()

# Compute PDSI time series
pdsi = pdsi_calc.compute(P=P_monthly, PET=PET_monthly)

# Analyze drought trends
drought_years = pdsi < -2.0  # Moderate to severe drought
print(f"Drought frequency: {drought_years.sum() / len(pdsi):.1%}")
```

---

## ⚠️ Important Gotchas

### 1. **DO NOT Duplicate Physical Constants**

❌ **BAD:**
```python
def saturation_vapor_pressure(T):
    return 0.6108 * np.exp((17.27 * T) / (T + 237.3))
```

✅ **GOOD:**
```python
from pet_comparison.utils.constants import saturation_vapor_pressure

es = saturation_vapor_pressure(T)
```

**Why:** Single source of truth. Any formula changes must be universal.

### 2. **Unit Confusion**

❌ **BAD:**
```python
# Mixing units
T_kelvin = 293.15  # Kelvin
pet = some_formula(temperature=T_kelvin)  # Expects Celsius!
```

✅ **GOOD:**
```python
# Convert to standard units
T_celsius = T_kelvin - 273.15
pet = some_formula(temperature=T_celsius)
```

**Check docstrings for expected units!**

### 3. **xarray vs NumPy Confusion**

❌ **BAD:**
```python
# Passing numpy array to xarray-expecting model
T_array = np.array([10, 15, 20])
mod16 = MOD16()
aet = mod16.compute_et(T_array)  # ERROR!
```

✅ **GOOD:**
```python
# Create xarray Dataset
ds = xr.Dataset({'T_mean': (['time'], T_array)})
aet = mod16.compute_et(ds)['AET']
```

### 4. **Component Partitioning Availability**

❌ **BAD:**
```python
# Not all models support partitioning
mod16 = MOD16()
components = mod16.partition_components(ds)  # May raise NotImplementedError!
```

✅ **GOOD:**
```python
# Check availability first
if hasattr(model, 'partition_components'):
    try:
        components = model.partition_components(ds)
    except NotImplementedError:
        print(f"{model.__class__.__name__} doesn't support partitioning")
```

### 5. **Radiation Unit Confusion**

**Some formulas expect MJ m⁻² day⁻¹, others W m⁻²**

Check docstring! Convert if needed:
```python
# Convert W m^-2 to MJ m^-2 day^-1
Rn_MJ = Rn_W * 0.0864

# Convert MJ m^-2 day^-1 to W m^-2
Rn_W = Rn_MJ / 0.0864
```

### 6. **Paper Replica Independence**

Each paper replica can be installed independently:
```bash
cd Liu_2023_PET
pip install -e .
```

But they **import** from main library. Don't move them without updating imports.

### 7. **Algorithm Family Matters**

Don't mix concepts:
- **P-M models** need resistance parameters
- **P-T models** need stress factors
- **SEB models** need LST and spatial dimensions

Use appropriate base class when creating new models.

---

## 🔀 Git Workflow

### Branch Naming
- Feature: `claude/feature-name-{session_id}`
- Bugfix: `claude/fix-issue-{session_id}`
- Paper replica: `claude/add-paper-author-year-{session_id}`

**CRITICAL:** Session ID must match for push to succeed (403 error otherwise)

### Commit Messages

**Format:**
```
[Type] Brief description

- Detailed point 1
- Detailed point 2

Refs: #issue_number (if applicable)
```

**Types:**
- `[Add]` - New features/files
- `[Update]` - Modifications to existing code
- `[Fix]` - Bug fixes
- `[Refactor]` - Code restructuring without functionality change
- `[Docs]` - Documentation updates
- `[Test]` - Test additions/updates

**Example:**
```
[Add] Implement Shuttleworth-Wallace dual-source model

- Add new formula to pet_comparison/formulas/dual_source.py
- Implement canopy and soil resistance calculations
- Add unit tests for edge cases
- Update README model table

Refs: #42
```

### Push Workflow

```bash
# Always specify branch with -u flag
git push -u origin claude/feature-name-01CxwP4j8eJWWwCV4g5viFH9

# If network error, retry with exponential backoff (automatic in Claude Code)
# Manual: wait 2s, 4s, 8s, 16s between retries (max 4 retries)
```

### Creating Pull Requests

Use `gh` CLI (GitHub CLI):
```bash
# Ensure branch is pushed
git push -u origin $(git branch --show-current)

# Create PR with heredoc body
gh pr create --title "Add Shuttleworth-Wallace model" --body "$(cat <<'EOF'
## Summary
- Implemented dual-source Shuttleworth-Wallace PET model
- Added comprehensive unit tests
- Updated documentation

## Test plan
- [x] Unit tests pass
- [x] Physical behavior validated
- [x] Compared with literature values
- [ ] Reviewer testing needed
EOF
)"
```

---

## 📚 Resources

### Documentation Files
- `README.md` - Project overview, quick start
- `PROJECT_SUMMARY.md` - Framework summary
- `REFACTORING_SUMMARY.md` - Recent refactoring details (Nov 2025)
- `CHANGELOG.md` - Version history
- `docs/SCIENTIFIC_BACKGROUND.md` - Theory and equations
- `docs/USER_GUIDE.md` - Usage instructions
- `docs/API_REFERENCE.md` - Function reference

### Key Examples
- `examples/aet_comparison.py` - AET model comparison (start here!)
- `examples/basic_comparison.py` - PET formula comparison
- `examples/advanced_spatial_analysis.py` - Production-grade spatial analysis
- `examples/co2_sensitivity.py` - CO2 response analysis

### Scientific References

**Integrated papers:**
1. Liu et al. (2023) - *J. Hydrology* - EP_Veg
2. Yang et al. (2019) - *Nature Climate Change* - PM-CO2
3. Pimentel et al. (2023) - *Water Resources Research* - Temperature methods
4. Xiong & Yang (2025) - *Scientific Data* - PDSI
5. Wang et al. (2025) - *Current Climate Change Reports* - PM-Jarvis
6. Yin & Porporato (2023) - *GRL* - Aridity distributions

**Foundational:**
- Allen et al. (1998) - FAO-56 PM
- Priestley & Taylor (1972) - PT coefficient
- Medlyn et al. (2011) - Optimal stomatal conductance
- Jarvis (1976) - Empirical stomatal response

### External Tools
- `pytest` - Testing
- `xarray` - Multi-dimensional data
- `numpy` - Numerical computations
- `pandas` - Time series
- `matplotlib` / `seaborn` - Visualization

---

## 🎓 Best Practices for AI Assistants

### 1. Always Check Existing Code First
Before implementing new functionality, search for similar implementations:
```bash
# Search for similar formulas
grep -r "priestley_taylor" pet_comparison/formulas/

# Find usage examples
grep -r "MOD16" examples/
```

### 2. Maintain Consistency
- Follow existing naming conventions
- Use same docstring format
- Match code style (spacing, imports)
- Preserve bilingual comments where present

### 3. Test Thoroughly
- Add tests for new formulas/models
- Test physical behavior, not just numerical output
- Include edge cases
- Verify array and scalar inputs

### 4. Update Documentation
When adding features:
- Update `README.md` model/formula tables
- Add example to `examples/`
- Update `CHANGELOG.md`
- Add docstrings with references

### 5. Respect Single Source of Truth
**Never duplicate:**
- Physical constant calculations
- Meteorological functions
- Unit conversions

**Always import** from `pet_comparison/utils/constants.py`

### 6. Understand Algorithm Families
- P-M (Penman-Monteith): Resistance-based, needs stomatal/aerodynamic resistance
- P-T (Priestley-Taylor): Energy-limited, needs stress factors
- SEB (Surface Energy Balance): Thermal-based, needs LST

Choose appropriate base class and required variables.

### 7. Validate Physically
ET/PET should:
- Be non-negative
- Increase with temperature (usually)
- Increase with radiation
- Decrease with CO2 (for stomatal models)
- Increase with LAI (for vegetation models)

If behavior seems wrong, investigate!

---

## 📞 Getting Help

### Common Issues

**"Import error from pet_comparison"**
→ Install in development mode: `pip install -e .`

**"Unit test failures after refactoring"**
→ Check if physical constants changed
→ Verify units in docstrings

**"xarray error with numpy array"**
→ Wrap in `xr.Dataset({'var': (['time'], array)})`

**"Model doesn't support partitioning"**
→ Check `hasattr(model, 'partition_components')`
→ Only PMLv2, PTJPL support it currently

### Debug Checklist
1. Check units (°C vs K, kPa vs Pa, MJ vs W)
2. Verify array shapes match
3. Check for NaN values
4. Confirm imports from correct module
5. Review docstring for expected inputs

---

## 🔄 Recent Changes (Nov 2025)

**Major refactoring completed:**
1. ✅ Eliminated ~200 lines duplicate code (DRY principle)
2. ✅ Centralized physical functions in `constants.py`
3. ✅ Vectorized loops → 10-50x performance improvement
4. ✅ Created production-grade spatial analysis example
5. ✅ Paper replicas now import from main library

**Before editing older code:** Check `REFACTORING_SUMMARY.md` for changes.

---

**End of CLAUDE.md**

*This document is maintained for AI assistant guidance. Human developers should primarily refer to README.md and docs/*.md files.*
