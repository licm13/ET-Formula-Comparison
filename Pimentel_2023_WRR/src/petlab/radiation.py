
"""
Radiation and solar geometry helpers (FAO-56 style).

中文注释：本模块实现常见的太阳几何与辐射估算（外辐射、日地距离校正、太阳高度角、清空辐射等），
用于 Hargreaves/PT 等公式。参考 FAO-56（Allen et al., 1998）。
"""
import numpy as np

# FAO-56 constants
GSC = 0.0820  # MJ m-2 min-1, solar constant
SIGMA = 4.903e-9  # MJ K-4 m-2 day-1, Stefan-Boltzmann (daily)

def day_angle(doy: int) -> float:
    """Return day angle in radians for day-of-year."""
    return 2.0 * np.pi * (doy - 1) / 365.0

def dr(doy: int) -> float:
    """Inverse relative distance Earth-Sun (dimensionless)."""
    B = day_angle(doy)
    return 1 + 0.033 * np.cos(B)

def solar_declination(doy: int) -> float:
    """Solar declination (radians)."""
    B = day_angle(doy)
    return 0.409 * np.sin(B - 1.39)

def sunset_hour_angle(lat_rad: float, doy: int) -> float:
    """Sunset hour angle (radians)."""
    sd = solar_declination(doy)
    return np.arccos(-np.tan(lat_rad) * np.tan(sd))

def Ra_extraterrestrial(lat_deg: float, doy: int) -> float:
    """
    Daily extraterrestrial radiation Ra [MJ m-2 day-1].
    lat_deg: decimal degrees latitude (positive north).
    """
    phi = np.deg2rad(lat_deg)
    ws = sunset_hour_angle(phi, doy)
    ra = (24*60/np.pi) * GSC * dr(doy) * (
        ws*np.sin(phi)*np.sin(solar_declination(doy)) +
        np.cos(phi)*np.cos(solar_declination(doy))*np.sin(ws)
    )
    return float(ra)

def Rso_clear_sky(alt_km: float, Ra: float) -> float:
    """Clear-sky shortwave radiation Rso [MJ m-2 d-1]. alt_km: station elevation (km)."""
    return (0.75 + 2e-5 * alt_km*1000) * Ra

def ea_from_Tdew(Tdew: float) -> float:
    """Actual vapour pressure ea [kPa] via Tdew (°C)."""
    return 0.6108 * np.exp(17.27 * Tdew / (Tdew + 237.3))

def ea_from_RH(Tmax: float, Tmin: float, RHmax: float, RHmin: float) -> float:
    """Approximate ea from Tmax/Tmin and RH extremes."""
    esTmax = 0.6108 * np.exp(17.27*Tmax/(Tmax+237.3))
    esTmin = 0.6108 * np.exp(17.27*Tmin/(Tmin+237.3))
    es = (esTmax + esTmin) / 2.0
    ea = (esTmin*RHmax/100 + esTmax*RHmin/100)/2.0
    return ea

def slope_vapour_pressure_curve(Tmean: float) -> float:
    """Slope delta [kPa/°C]."""
    es = 0.6108 * np.exp(17.27*Tmean/(Tmean+237.3))
    return 4098 * es / (Tmean + 237.3)**2

def psychrometric_constant(P_kPa: float=101.3) -> float:
    """Psychrometric constant gamma [kPa/°C]. For sea level ~0.066."""
    # gamma = Cp * P / (epsilon * lambda)
    # Here we return typical sea-level value unless pressure provided.
    return 0.000665 * P_kPa

def shortwave_from_hargreaves(Ra: float, Tmax: float, Tmin: float, krs: float=0.16) -> float:
    """
    Estimate incoming shortwave Rs [MJ m-2 d-1] via Hargreaves: Rs = krs * sqrt(Tmax - Tmin) * Ra
    krs: ~0.16 inland, ~0.19 coastal.
    """
    dT = max(Tmax - Tmin, 0.0)
    return krs * np.sqrt(dT) * Ra

def net_radiation(Rs: float, Rso: float, albedo: float, Tmax: float, Tmin: float, ea: float) -> float:
    """
    Net radiation Rn = Rns - Rnl [MJ m-2 d-1].
    Rns = (1 - albedo) * Rs
    Rnl = sigma * ((TmaxK^4 + TminK^4)/2) * (0.34 - 0.14*sqrt(ea)) * (1.35*Rs/Rso - 0.35)
    """
    Rns = (1 - albedo) * Rs
    TmaxK, TminK = Tmax + 273.16, Tmin + 273.16
    Rnl = SIGMA * ((TmaxK**4 + TminK**4)/2.0) * (0.34 - 0.14*np.sqrt(max(ea, 1e-6))) * (1.35*min(Rs/Rso if Rso>0 else 0, 1.0) - 0.35)
    return Rns - Rnl
