"""
utils_fonts.py

Matplotlib font setup for bilingual (Chinese+English) plotting.

注意：不显式指定颜色；仅设置字体与负号显示。
"""
import matplotlib
from matplotlib import pyplot as plt

def setup_fonts():
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["font.sans-serif"] = ["DejaVu Sans", "Noto Sans CJK SC", "SimHei", "Microsoft YaHei", "Arial Unicode MS"]
    matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    matplotlib.rcParams["figure.dpi"] = 150

def new_figure(figsize=(6,4)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    return fig, ax
