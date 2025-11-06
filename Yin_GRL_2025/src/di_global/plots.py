"""
plots.py

Plotting helpers: empirical PDFs, theoretical curves, and simple annotations.
遵循要求：
- 使用 matplotlib，且不指定颜色。
- 每张图仅一个坐标轴，无子图。
"""
from __future__ import annotations
import os
import numpy as np
from matplotlib import pyplot as plt
from .utils_fonts import setup_fonts, new_figure

def plot_empirical_vs_theory(x: np.ndarray, y_emp: np.ndarray, y_theory: np.ndarray, title: str, xlabel: str, ylabel: str, savepath: str):
    setup_fonts()
    fig, ax = new_figure(figsize=(7,5))
    ax.plot(x, y_emp, label="Empirical PDF / 经验分布", linewidth=2)
    ax.plot(x, y_theory, label="Theory / 理论", linestyle="--", linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    fig.tight_layout()
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(savepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    fig.savefig(savepath, bbox_inches="tight")

def plot_histogram(x: np.ndarray, y: np.ndarray, title: str, xlabel: str, ylabel: str, savepath: str):
    setup_fonts()
    fig, ax = new_figure(figsize=(7,5))
    ax.plot(x, y, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xscale("log")
    ax.set_yscale("log")
    fig.tight_layout()
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(savepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    fig.savefig(savepath, bbox_inches="tight")
