
"""Plot helpers / 绘图辅助"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from . import fonts

def plot_timeseries(ts, title_cn="时间序列", title_en="Time Series", save=None):
    fonts.configure()
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(ts, lw=1.2)
    ax.set_xlabel("时间 / Time (months)")
    ax.set_ylabel("值 / Value")
    ax.set_title(f"{title_cn} · {title_en}")
    ax.grid(True, alpha=0.3)
    if save:
        fonts.savefig(save)
    return fig, ax

def plot_map(field, title_cn="空间分布", title_en="Spatial Map", save=None):
    fonts.configure()
    v = np.nanmax(np.abs(field))
    fig, ax = plt.subplots(figsize=(5,3))
    im = ax.imshow(field, origin="lower", cmap="RdBu_r", vmin=-v, vmax=v)
    ax.set_title(f"{title_cn} · {title_en}")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if save:
        fonts.savefig(save)
    return fig, ax
