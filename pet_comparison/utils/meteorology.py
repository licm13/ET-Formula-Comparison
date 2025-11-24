"""
Meteorological utility functions
"""

import numpy as np
from .constants import GRAVITY, T_ZERO


def net_radiation(shortwave_in, albedo, longwave_in=None, temperature=None, emissivity=0.98):
    """
    Calculate net radiation
    
    Parameters:
    -----------
    shortwave_in : float or array-like
        Incoming shortwave radiation (W m-2)
    albedo : float or array-like
        Surface albedo (0-1)
    longwave_in : float or array-like, optional
        Incoming longwave radiation (W m-2)
    temperature : float or array-like, optional
        Surface temperature (°C), used if longwave_in not provided
    emissivity : float, optional
        Surface emissivity (default: 0.98)
    
    Returns:
    --------
    Rn : float or array-like
        Net radiation (W m-2)
    """
    # Net shortwave
    Rns = (1 - albedo) * shortwave_in
    
    # Net longwave
    if longwave_in is not None:
        from .constants import STEFAN_BOLTZMANN
        if temperature is not None:
            T_k = temperature + T_ZERO
        else:
            # Default to 20°C (293.15 K) if temperature not provided
            T_k = 293.15
        Rnl = longwave_in - emissivity * STEFAN_BOLTZMANN * (T_k ** 4)
    else:
        # Simplified approach if longwave not available
        Rnl = 0
    
    return Rns + Rnl


def extraterrestrial_radiation(doy, latitude):
    """
    Calculate extraterrestrial radiation
    
    Parameters:
    -----------
    doy : int or array-like
        Day of year (1-365)
    latitude : float or array-like
        Latitude (degrees)
    
    Returns:
    --------
    Ra : float or array-like
        Extraterrestrial radiation (MJ m-2 day-1)
    """
    # Solar constant
    Gsc = 0.0820  # MJ m-2 min-1
    
    # Convert latitude to radians
    lat_rad = np.deg2rad(latitude)
    
    # Inverse relative distance Earth-Sun
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy / 365)
    
    # Solar declination
    delta = 0.409 * np.sin(2 * np.pi * doy / 365 - 1.39)
    
    # Sunset hour angle
    ws = np.arccos(-np.tan(lat_rad) * np.tan(delta))
    
    # Extraterrestrial radiation
    Ra = (24 * 60 / np.pi) * Gsc * dr * (
        ws * np.sin(lat_rad) * np.sin(delta) + 
        np.cos(lat_rad) * np.cos(delta) * np.sin(ws)
    )
    
    return Ra


def clear_sky_radiation(elevation, Ra):
    """
    Calculate clear sky radiation
    
    Parameters:
    -----------
    elevation : float or array-like
        Elevation above sea level (m)
    Ra : float or array-like
        Extraterrestrial radiation (MJ m-2 day-1)
    
    Returns:
    --------
    Rso : float or array-like
        Clear sky radiation (MJ m-2 day-1)
    """
    return (0.75 + 2e-5 * elevation) * Ra


def atmospheric_pressure(elevation):
    """
    Calculate atmospheric pressure as function of elevation
    
    Parameters:
    -----------
    elevation : float or array-like
        Elevation above sea level (m)
    
    Returns:
    --------
    P : float or array-like
        Atmospheric pressure (kPa)
    """
    return 101.3 * ((293 - 0.0065 * elevation) / 293) ** 5.26


def wind_speed_adjustment(u_z, z=2.0):
    """
    Adjust wind speed to 2m height
    
    Parameters:
    -----------
    u_z : float or array-like
        Wind speed at height z (m s-1)
    z : float, optional
        Height of wind measurement (m), default: 2.0
    
    Returns:
    --------
    u_2 : float or array-like
        Wind speed at 2m height (m s-1)
    """
    if z == 2.0:
        return u_z
    else:
        # Logarithmic wind profile
        return u_z * (4.87 / np.log(67.8 * z - 5.42))


def aerodynamic_resistance(wind_speed, height=2.0, roughness_length=0.03):
    """
    Calculate aerodynamic resistance
    
    Parameters:
    -----------
    wind_speed : float or array-like
        Wind speed at reference height (m s-1)
    height : float, optional
        Reference height (m), default: 2.0
    roughness_length : float, optional
        Surface roughness length (m), default: 0.03
    
    Returns:
    --------
    ra : float or array-like
        Aerodynamic resistance (s m-1)
    """
    from .constants import VON_KARMAN
    
    # Zero plane displacement
    d = 2.0 / 3.0 * roughness_length * 10
    
    # Roughness length for heat
    z0h = 0.1 * roughness_length
    
    # Calculate resistance
    ra = (np.log((height - d) / roughness_length) *
          np.log((height - d) / z0h)) / (VON_KARMAN ** 2 * wind_speed)

    return ra


def stability_correction_stable(zeta, a=6.1, b=2.5):
    """
    Stability correction for stable atmospheric conditions.

    Implements the Cheng & Brutsaert (2005) formulation used with the
    Monin-Obukhov Similarity Theory (MOST).

    Parameters
    ----------
    zeta : float or array-like
        Dimensionless stability parameter (z - d0) / L.
    a : float, optional
        Coefficient controlling the magnitude of the correction.
    b : float, optional
        Coefficient controlling the shape of the correction.

    Returns
    -------
    array-like
        Stability correction term :math:`\psi`.
    """
    zeta = np.maximum(zeta, 1e-6)
    return -a * np.log(zeta + (1.0 + zeta ** b) ** (1.0 / b))


def stability_correction_unstable_momentum(zeta):
    """
    Momentum stability correction for unstable conditions (Businger-Dyer form).

    Parameters
    ----------
    zeta : float or array-like
        Dimensionless stability parameter (z - d0) / L, negative for unstable.

    Returns
    -------
    array-like
        Momentum stability correction term.
    """
    x = (1.0 - 16.0 * zeta) ** 0.25
    return (
        2.0 * np.log((1.0 + x) / 2.0)
        + np.log((1.0 + x ** 2) / 2.0)
        - 2.0 * np.arctan(x)
        + np.pi / 2.0
    )


def stability_correction_unstable_scalar(zeta):
    """
    Scalar (e.g., water vapor or heat) stability correction for unstable air.

    Parameters
    ----------
    zeta : float or array-like
        Dimensionless stability parameter (z - d0) / L, negative for unstable.

    Returns
    -------
    array-like
        Scalar stability correction term.
    """
    x = (1.0 - 16.0 * zeta) ** 0.25
    return 2.0 * np.log((1.0 + x ** 2) / 2.0)


def friction_velocity(u_z, measurement_height, displacement_height, roughness_length_momentum, psi_m):
    """
    Estimate friction velocity (u*) with stability corrections.

    Parameters
    ----------
    u_z : float or array-like
        Wind speed at measurement height (m s-1).
    measurement_height : float
        Measurement height z (m).
    displacement_height : float
        Zero-plane displacement height (m).
    roughness_length_momentum : float
        Roughness length for momentum (m).
    psi_m : float or array-like
        Momentum stability correction term.

    Returns
    -------
    array-like
        Friction velocity (m s-1).
    """
    denom = np.log((measurement_height - displacement_height) / roughness_length_momentum) - psi_m
    denom = np.where(np.abs(denom) < 1e-6, 1e-6, denom)
    return VON_KARMAN * u_z / denom


def monin_obukhov_length(u_star, net_available_energy, latent_heat_flux, air_temperature_c, air_density=1.225):
    """
    Compute Monin-Obukhov length using net available energy and latent heat flux.

    Parameters
    ----------
    u_star : float or array-like
        Friction velocity (m s-1).
    net_available_energy : float or array-like
        Net available energy (W m-2), often Rn - G.
    latent_heat_flux : float or array-like
        Latent heat flux (W m-2).
    air_temperature_c : float or array-like
        Air temperature (°C).
    air_density : float, optional
        Air density (kg m-3). Default is near sea level.

    Returns
    -------
    array-like
        Monin-Obukhov length (m). Positive for stable, negative for unstable.
    """
    from .constants import SPECIFIC_HEAT_AIR

    ta_k = air_temperature_c + T_ZERO
    sensible_heat = net_available_energy - latent_heat_flux
    denom = (sensible_heat / (ta_k * SPECIFIC_HEAT_AIR) + 0.61 * latent_heat_flux / (air_density * SPECIFIC_HEAT_AIR))
    denom = np.where(np.abs(denom) < 1e-9, 1e-9, denom)

    return -(air_density * SPECIFIC_HEAT_AIR * ta_k * u_star ** 3) / (VON_KARMAN * GRAVITY * denom)


def wind_function_with_stability(u_z, air_temperature_c, measurement_height, displacement_height, z0m, z0v, psi_m, psi_v):
    """
    Wind function with stability corrections for evaporation calculations.

    Parameters
    ----------
    u_z : float or array-like
        Wind speed at measurement height (m s-1).
    air_temperature_c : float or array-like
        Air temperature (°C).
    measurement_height : float
        Measurement height z (m).
    displacement_height : float
        Zero-plane displacement height (m).
    z0m : float
        Roughness length for momentum (m).
    z0v : float
        Roughness length for scalars (e.g., water vapor) (m).
    psi_m : float or array-like
        Momentum stability correction term.
    psi_v : float or array-like
        Scalar stability correction term.

    Returns
    -------
    array-like
        Wind function :math:`f_e` (m s-1 kPa-1) for Penman-type equations.
    """
    from .constants import SPECIFIC_GAS_CONSTANT_DRY_AIR

    ta_k = air_temperature_c + T_ZERO
    num = 0.622 * VON_KARMAN ** 2 * u_z
    denom = (
        SPECIFIC_GAS_CONSTANT_DRY_AIR * ta_k
        * (np.log((measurement_height - displacement_height) / z0v) - psi_v)
        * (np.log((measurement_height - displacement_height) / z0m) - psi_m)
    )
    denom = np.where(np.abs(denom) < 1e-9, 1e-9, denom)
    return num / denom
