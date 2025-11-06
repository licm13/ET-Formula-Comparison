"""
utils_fonts.py

Matplotlib font setup for bilingual (Chinese+English) plotting.

注意：不显式指定颜色；仅设置字体与负号显示。
"""
import matplotlib
import matplotlib.font_manager
from matplotlib import pyplot as plt

def setup_fonts():
    # Get available font names
    available_fonts = set(f.name for f in matplotlib.font_manager.fontManager.ttflist)
    
    # List of preferred Chinese fonts
    chinese_candidates = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Noto Sans SC", "Arial Unicode MS"]
    
    # Find the first available Chinese font
    chosen_font = None
    for font in chinese_candidates:
        if font in available_fonts:
            chosen_font = font
            break
    
    # Set font family with Chinese font support
    if chosen_font:
        matplotlib.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
        print(f"[Font] Using Chinese font: {chosen_font}")
    else:
        # Fallback to any available Chinese font
        chinese_fonts = [f for f in available_fonts if any(x in f.lower() for x in ['yahei', 'simhei', 'kai', 'hei'])]
        if chinese_fonts:
            chosen_font = chinese_fonts[0]
            matplotlib.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
            print(f"[Font] Using fallback Chinese font: {chosen_font}")
        else:
            matplotlib.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
            print("[Font] No Chinese fonts found. Chinese characters may not display correctly.")
    
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    matplotlib.rcParams["figure.dpi"] = 150

def new_figure(figsize=(6,4)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    return fig, ax
