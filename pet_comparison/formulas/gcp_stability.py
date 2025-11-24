"""Generalized Complementary Principle with stability corrections.

This module implements the sub-daily Generalized Complementary Principle (GCP)
model with Monin-Obukhov-based atmospheric stability corrections proposed by
Zhang et al. (2025). The formulation follows the replication scripts in
``paper_replication_GCP_Subdaily_Evap`` but is integrated with the shared
utilities and constants from :mod:`pet_comparison`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from scipy.optimize import minimize_scalar

from ..utils.constants import get_psychrometric_constant, slope_saturation_vapor_pressure
from ..utils.meteorology import (
    stability_correction_stable,
    stability_correction_unstable_momentum,
    stability_correction_unstable_scalar,
    friction_velocity,
    monin_obukhov_length,
    wind_function_with_stability,
)


def _compute_metrics(est: np.ndarray, obs: np.ndarray) -> Dict[str, float]:
    """Compute slope, R², RMSE, and percent bias between arrays."""

    mask = np.isfinite(est) & np.isfinite(obs)
    est_masked = est[mask]
    obs_masked = obs[mask]

    if est_masked.size == 0:
        return dict(slope=np.nan, r2=np.nan, rmse=np.nan, bias_pct=np.nan)

    slope_num = np.sum(obs_masked * est_masked)
    slope_den = np.sum(obs_masked**2)
    slope = slope_num / slope_den if slope_den != 0 else np.nan

    obs_mean = np.mean(obs_masked)
    ss_res = np.sum((obs_masked - est_masked) ** 2)
    ss_tot = np.sum((obs_masked - obs_mean) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot != 0 else np.nan

    rmse = np.sqrt(np.mean((obs_masked - est_masked) ** 2))
    bias_pct = 100.0 * (np.mean(est_masked) - np.mean(obs_masked)) / np.mean(obs_masked)

    return dict(slope=slope, r2=r2, rmse=rmse, bias_pct=bias_pct)


def _objective_m_r2(est: np.ndarray, obs: np.ndarray) -> float:
    """Objective function defined as :math:`m \times R^2` used in Zhang et al. (2025)."""

    metrics = _compute_metrics(est, obs)
    slope = metrics["slope"]
    r2 = metrics["r2"]
    if np.isnan(slope) or np.isnan(r2):
        return -np.inf
    m = min(1.0 / slope, slope) if slope > 0 else 0.0
    return m * r2


def compute_equilibrium_evaporation(net_available_energy: np.ndarray, air_temperature_c: np.ndarray) -> np.ndarray:
    """Estimate equilibrium evaporation (:math:`E_e`) from net available energy.

    Parameters
    ----------
    net_available_energy : array-like
        Net available energy (W m-2), typically net radiation minus soil heat flux.
    air_temperature_c : array-like
        Air temperature (°C).

    Returns
    -------
    numpy.ndarray
        Equilibrium evaporation in energy flux units (W m-2).
    """

    delta = slope_saturation_vapor_pressure(air_temperature_c)
    gamma = get_psychrometric_constant(pressure=101.3, temperature=air_temperature_c)
    coeff = delta / (delta + gamma)
    return coeff * net_available_energy


def gcp_evaporation(beta_c: float, ee: np.ndarray, epa: np.ndarray) -> np.ndarray:
    """Compute actual evaporation using the GCP relationship.

    The formulation follows Zhang et al. (2025) Eq. (6) where
    :math:`x = \beta_c E_e / E_{pa}` and :math:`E = x^2 (2E_{pa} - \beta_c E_e)`.

    Parameters
    ----------
    beta_c : float
        Complementary coefficient :math:`\beta_c`.
    ee : array-like
        Equilibrium evaporation term (:math:`E_e`).
    epa : array-like
        Potential evaporation accounting for atmospheric stability (:math:`E_{pa}`).

    Returns
    -------
    numpy.ndarray
        Actual evaporation (:math:`E`).
    """

    epa_safe = np.where(epa <= 1e-6, 1e-6, epa)
    x = beta_c * ee / epa_safe
    x = np.clip(x, 0.0, 1.0)
    actual_e = x ** 2 * (2.0 * epa_safe - beta_c * ee)
    return np.maximum(actual_e, 0.0)


@dataclass
class GCPWithStability:
    """Sub-daily GCP model with MOST stability corrections (Zhang et al., 2025).

    This implementation mirrors the study "A generalized complementary principle
    (GCP) model with atmospheric stability correction for estimating sub-daily
    evaporation" while reusing the shared meteorological utilities.

    Attributes
    ----------
    z : float
        Measurement height (m).
    d0 : float
        Zero-plane displacement height (m).
    z0m : float
        Roughness length for momentum (m).
    z0v : float
        Roughness length for scalars such as humidity (m).
    p_kpa : float, optional
        Air pressure (kPa). Defaults to standard sea-level pressure.
    """

    z: float
    d0: float
    z0m: float
    z0v: float
    p_kpa: float = 101.3

    def _compute_penman_epa(
        self,
        net_available_energy: np.ndarray,
        air_temperature_c: np.ndarray,
        vapor_pressure_deficit_kpa: np.ndarray,
        u2: np.ndarray,
        actual_evaporation: np.ndarray,
        with_stability: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate Penman-style potential evaporation with stability corrections."""

        delta = slope_saturation_vapor_pressure(air_temperature_c)
        gamma = get_psychrometric_constant(self.p_kpa, air_temperature_c)

        if with_stability:
            psi_m = np.zeros_like(net_available_energy)
            psi_v = np.zeros_like(net_available_energy)

            for _ in range(3):
                u_star = friction_velocity(
                    u_z=u2,
                    measurement_height=self.z,
                    displacement_height=self.d0,
                    roughness_length_momentum=self.z0m,
                    psi_m=psi_m,
                )
                obukhov_length = monin_obukhov_length(
                    u_star=u_star,
                    net_available_energy=net_available_energy,
                    latent_heat_flux=actual_evaporation,
                    air_temperature_c=air_temperature_c,
                )
                zeta = (self.z - self.d0) / obukhov_length

                psi_m = np.zeros_like(zeta)
                psi_v = np.zeros_like(zeta)

                neutral = np.abs(obukhov_length) >= 100.0
                stable = (obukhov_length > 0.0) & (np.abs(obukhov_length) < 100.0)
                unstable = (obukhov_length < 0.0) & (np.abs(obukhov_length) < 100.0)

                psi_m[neutral] = 0.0
                psi_v[neutral] = 0.0

                psi_m[stable] = stability_correction_stable(zeta[stable])
                psi_v[stable] = stability_correction_stable(zeta[stable])

                psi_m[unstable] = stability_correction_unstable_momentum(zeta[unstable])
                psi_v[unstable] = stability_correction_unstable_scalar(zeta[unstable])
        else:
            psi_m = np.zeros_like(net_available_energy)
            psi_v = np.zeros_like(net_available_energy)

        fe = wind_function_with_stability(
            u_z=u2,
            air_temperature_c=air_temperature_c,
            measurement_height=self.z,
            displacement_height=self.d0,
            z0m=self.z0m,
            z0v=self.z0v,
            psi_m=psi_m,
            psi_v=psi_v,
        )

        radiation_term = delta / (delta + gamma) * net_available_energy
        aerodynamic_term = gamma / (delta + gamma) * fe * vapor_pressure_deficit_kpa
        epa = radiation_term + aerodynamic_term

        return epa, psi_m, psi_v

    def estimate_time_series(
        self,
        net_available_energy: np.ndarray,
        air_temperature_c: np.ndarray,
        vapor_pressure_deficit_kpa: np.ndarray,
        u2: np.ndarray,
        beta_c: float,
        max_iter: int = 20,
        tol: float = 1e-3,
        with_stability: bool = True,
    ) -> Dict[str, np.ndarray]:
        """Iteratively estimate evaporation time series.

        Returns a dictionary with actual evaporation ``E``, potential evaporation
        ``Epa``, equilibrium evaporation ``Ee``, and stability corrections
        ``psi_m``/``psi_v``.
        """

        net_available_energy = np.asarray(net_available_energy)
        air_temperature_c = np.asarray(air_temperature_c)
        vapor_pressure_deficit_kpa = np.asarray(vapor_pressure_deficit_kpa)
        u2 = np.asarray(u2)

        n = len(net_available_energy)
        ee = compute_equilibrium_evaporation(net_available_energy, air_temperature_c)

        actual_evaporation = ee.copy()
        psi_m = np.zeros(n)
        psi_v = np.zeros(n)

        for _ in range(max_iter):
            previous_e = actual_evaporation.copy()
            epa, psi_m, psi_v = self._compute_penman_epa(
                net_available_energy=net_available_energy,
                air_temperature_c=air_temperature_c,
                vapor_pressure_deficit_kpa=vapor_pressure_deficit_kpa,
                u2=u2,
                actual_evaporation=actual_evaporation,
                with_stability=with_stability,
            )
            ee = compute_equilibrium_evaporation(net_available_energy, air_temperature_c)
            actual_evaporation = gcp_evaporation(beta_c=beta_c, ee=ee, epa=epa)

            diff = np.nanmax(np.abs(actual_evaporation - previous_e))
            if diff < tol:
                break

        return dict(E=actual_evaporation, Epa=epa, Ee=ee, psi_m=psi_m, psi_v=psi_v)

    def calibrate_beta_c(
        self,
        net_available_energy: np.ndarray,
        air_temperature_c: np.ndarray,
        vapor_pressure_deficit_kpa: np.ndarray,
        u2: np.ndarray,
        observed_evaporation: np.ndarray,
        beta_bounds: Tuple[float, float] = (0.7, 1.5),
        with_stability: bool = True,
    ) -> Dict[str, float]:
        """Calibrate :math:`\beta_c` using the Zhang et al. (2025) objective function."""

        def neg_obj(beta: float) -> float:
            res = self.estimate_time_series(
                net_available_energy=net_available_energy,
                air_temperature_c=air_temperature_c,
                vapor_pressure_deficit_kpa=vapor_pressure_deficit_kpa,
                u2=u2,
                beta_c=beta,
                with_stability=with_stability,
                max_iter=20,
            )
            est_e = res["E"]
            obj = _objective_m_r2(est_e, observed_evaporation)
            return -obj

        res_opt = minimize_scalar(
            neg_obj,
            bounds=beta_bounds,
            method="bounded",
            options=dict(xatol=1e-3),
        )
        best_beta = float(res_opt.x)

        best_result = self.estimate_time_series(
            net_available_energy=net_available_energy,
            air_temperature_c=air_temperature_c,
            vapor_pressure_deficit_kpa=vapor_pressure_deficit_kpa,
            u2=u2,
            beta_c=best_beta,
            with_stability=with_stability,
            max_iter=20,
        )
        metrics = _compute_metrics(best_result["E"], observed_evaporation)
        obj_best = -float(res_opt.fun)

        return dict(
            beta_c=best_beta,
            obj=obj_best,
            **metrics,
        )


__all__ = [
    "GCPWithStability",
    "compute_equilibrium_evaporation",
    "gcp_evaporation",
]
