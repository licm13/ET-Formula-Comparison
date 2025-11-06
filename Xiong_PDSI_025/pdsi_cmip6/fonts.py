
"""
字体与图形风格 / Fonts & plot style helpers.
- 自动尝试中文字体，保证中英文混排不乱码。
"""
from __future__ import annotations
import os
import matplotlib
import matplotlib.pyplot as plt

_CANDIDATES = [
    "Noto Sans CJK SC",
    "SimHei",
    "Microsoft YaHei",
    "PingFang SC",
    "WenQuanYi Zen Hei",
    "STHeiti",
]

def configure():
    """
    Configure Matplotlib fonts for bilingual (Chinese/English) plotting.
    自动配置 Matplotlib 字体以支持中英文混排。
    """
    # Get available font names
    available_fonts = set(f.name for f in matplotlib.font_manager.fontManager.ttflist)
    
    chosen_font = None
    for name in _CANDIDATES:
        if name in available_fonts:
            chosen_font = name
            break
    
    if chosen_font:
        matplotlib.rcParams["font.family"] = [chosen_font, "DejaVu Sans", "Arial", "sans-serif"]
        print(f"[Font] Using Chinese font: {chosen_font}")
    else:
        # Try to find any available Chinese font
        chinese_fonts = [f for f in available_fonts if any(x in f.lower() for x in ['yahei', 'simhei', 'kai', 'hei'])]
        if chinese_fonts:
            chosen_font = chinese_fonts[0]
            matplotlib.rcParams["font.family"] = [chosen_font, "DejaVu Sans", "Arial", "sans-serif"]
            print(f"[Font] Using fallback Chinese font: {chosen_font}")
        else:
            print("[Font] No Chinese fonts found. Chinese characters may not display correctly.")
    
    # Minus sign fix
    matplotlib.rcParams["axes.unicode_minus"] = False

    # A few layout defaults
    matplotlib.rcParams["figure.dpi"] = 120
    matplotlib.rcParams["savefig.dpi"] = 150
    matplotlib.rcParams["figure.autolayout"] = True

def savefig(path: str, **kwargs):
    """统一保存图片，保证中文字体与高分辨率 / Save figures with consistent settings."""
    # Create directory if it doesn't exist
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    plt.savefig(path, dpi=kwargs.pop("dpi", 300), bbox_inches=kwargs.pop("bbox_inches", "tight"), **kwargs)
