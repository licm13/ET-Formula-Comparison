
"""
Self-calibrated PDSI (scPDSI) – simplified, vectorized implementation.
自校准PDSI（简化实现），支持直接输入水文分量以贴近论文思路。

This module implements the key steps:
1) Compute CAFEC precipitation P_hat and moisture anomaly D.
2) Compute monthly Z-index (Ki * D) and recurse PDSI using duration (p,q).
3) Self-calibration: re-estimate (p,q) per grid via regression against Z to improve spatial comparability.

Notes:
- This is a pedagogical reimplementation for demonstration with synthetic data.
- For research use with CMIP6, carefully check units and masks.
"""
from __future__ import annotations
import numpy as np

class SelfCalibratedPDSI:
    def __init__(self, p0=0.897, q0=1/3, cap=10.0):
        self.p0 = p0
        self.q0 = q0
        self.cap = float(cap)

    def _monthly_coeff_K(self, D):
        """Compute Ki' per month using a simple variance-based scaling. 简化计算每月系数"""
        # D: (t,y,x); monthly group by month-of-year
        t, ny, nx = D.shape
        months = np.arange(t) % 12
        K = np.zeros_like(D)
        # Use robust scaling: Ki' = 1.5 * log10( sum |D| ) normalized by monthly mean magnitude
        for m in range(12):
            sel = months == m
            if not np.any(sel): 
                continue
            Dm = np.abs(D[sel])
            scale = np.nanmean(Dm, axis=0)
            scale = np.where(scale==0, np.nan, scale)
            Ki = 1.5 * np.log10(np.nansum(Dm, axis=0) + 1e-6)
            Ki = Ki / (scale / (np.nanmean(scale)))
            # broadcast back
            K[sel] = Ki
        # normalize to a moderate magnitude
        K /= np.nanmean(np.abs(K), axis=0)[None,...]
        return np.nan_to_num(K, nan=1.0, posinf=1.0, neginf=1.0)

    def _cafec_and_D(self, P, EP, E, R, RO, L):
        """
        Compute CAFEC precipitation P_hat and moisture departure D.
        If any hydrologic component is None, fallback to simple P-EP anomaly.
        """
        P = np.asarray(P, dtype=float)
        EP = np.asarray(EP, dtype=float)
        if E is None or R is None or RO is None or L is None:
            climP = np.nanmean(P, axis=0)
            climEP = np.nanmean(EP, axis=0)
            # CAFEC-like P_hat
            P_hat = climP + (EP - climEP) * 0.5
        else:
            E = np.asarray(E, dtype=float)
            R = np.asarray(R, dtype=float)
            RO= np.asarray(RO, dtype=float)
            L = np.asarray(L, dtype=float)
            # Potential components from monthly climatology (very simplified proxy)
            # Xp ≈ monthly max across years; α = X / Xp; CAFEC components α*Xp ≈ X (climatology)
            # We approximate CAFEC using anomalies of the hydrologic components from climatology.
            clim = lambda X: np.nanmean(X, axis=0)
            dE, dR, dRO, dL = E - clim(E), R - clim(R), RO - clim(RO), L - clim(L)
            P_hat = clim(P) + (clim(E) + dE) + (clim(R) + dR) + (clim(RO) + dRO) - (clim(L) + dL)
            # This reduces to P_hat ≈ clim(P) + (E+R+RO-L) anomaly added onto climatology
        D = P - P_hat
        return P_hat, D

    def _recurse_pdsi(self, Z, p, q):
        """Recursively compute PDSI from Z-index with parameters p,q (axis=0 is time)."""
        Z = np.asarray(Z, dtype=float)
        t, ny, nx = Z.shape
        PDSI = np.zeros_like(Z)
        for i in range(1, t):
            PDSI[i] = p * PDSI[i-1] + q * Z[i]
        # cap to avoid outliers (±10)
        PDSI = np.clip(PDSI, -self.cap, self.cap)
        return PDSI

    def _self_calibrate(self, Z, PDSI0):
        """
        Fit grid-wise (p,q) from linear regression PDSI ~ p*PDSI_{-1} + q*Z.
        Simple least squares per grid cell.
        """
        t, ny, nx = Z.shape
        p = np.full((ny, nx), self.p0, dtype=float)
        q = np.full((ny, nx), self.q0, dtype=float)

        X1 = PDSI0[:-1]         # (t-1, ny, nx)
        y  = PDSI0[1:]          # (t-1, ny, nx)
        Z1 = Z[1:]              # align with y

        # Solve for p and q via normal equations at each grid cell
        A11 = np.nansum(X1*X1, axis=0)
        A12 = np.nansum(X1*Z1, axis=0)
        A22 = np.nansum(Z1*Z1, axis=0)
        b1  = np.nansum(X1*y, axis=0)
        b2  = np.nansum(Z1*y, axis=0)

        det = A11*A22 - A12*A12
        valid = det != 0
        p_new = np.full_like(p, np.nan)
        q_new = np.full_like(q, np.nan)
        p_new[valid] = ( A22[valid]*b1[valid] - A12[valid]*b2[valid] ) / det[valid]
        q_new[valid] = ( A11[valid]*b2[valid] - A12[valid]*b1[valid] ) / det[valid]

        # Clean & constrain
        p = np.where(np.isfinite(p_new), p_new, p)
        q = np.where(np.isfinite(q_new), q_new, q)
        p = np.clip(p, 0.6, 0.99)
        q = np.clip(q, 0.05, 0.6)
        return p, q

    def compute(self, P, EP, E=None, R=None, RO=None, L=None, awc=150.0, self_calibrate=True):
        """
        Compute Z-index and scPDSI.
        Inputs:
          P  : precipitation (mm/month)
          EP : potential evaporation (mm/month)
          E, R, RO, L : hydrologic components (mm/month) – optional but recommended
          awc: available water capacity (mm) – placeholder for future constraints
        Returns:
          Z, PDSI
        """
        P_hat, D = self._cafec_and_D(P, EP, E, R, RO, L)
        K = self._monthly_coeff_K(D)
        Z = K * D

        # first pass with default p,q
        PDSI0 = self._recurse_pdsi(Z, self.p0, self.q0)

        if self_calibrate:
            p_grid, q_grid = self._self_calibrate(Z, PDSI0)
            # apply grid-wise recursion
            t = Z.shape[0]
            PDSI = np.zeros_like(Z)
            for i in range(1, t):
                PDSI[i] = p_grid * PDSI[i-1] + q_grid * Z[i]
            PDSI = np.clip(PDSI, -self.cap, self.cap)
            return Z, PDSI
        else:
            return Z, PDSI0
