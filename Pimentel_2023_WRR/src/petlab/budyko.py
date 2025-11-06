
"""
Budyko curve utilities and plotting.
"""
import numpy as np
import matplotlib.pyplot as plt
from .plotting import setup_fonts

def budyko_phi(PET_over_P):
    """Schreiber/Ol'Dekop-like smooth function (pedagogical): AET/P = sqrt( PET/P * tanh(1/PET/P) * (1 - exp(-PET/P)) )."""
    x = np.maximum(PET_over_P, 1e-6)
    return np.sqrt( x * np.tanh(1.0/x) * (1.0 - np.exp(-x)) )

def plot_budyko_density(ax, PET_over_P, AET_over_P, label=None, cmap=None):
    setup_fonts()
    ax.scatter(PET_over_P, AET_over_P, s=18, alpha=0.6, label=label)
    x = np.linspace(0.01, 4.0, 500)
    ax.plot(x, budyko_phi(x), lw=2, label="Budyko φ(x)")
    ax.set_xlabel("PET / P")
    ax.set_ylabel("AET / P")
    ax.set_xlim(0, 3.5)
    ax.set_ylim(0, 1.2)
    if label:
        ax.legend()
    ax.grid(True, alpha=0.25)
    return ax
