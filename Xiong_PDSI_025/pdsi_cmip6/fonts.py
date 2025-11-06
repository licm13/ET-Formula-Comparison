
"""
字体与图形风格 / Fonts & plot style helpers.
- 自动尝试中文字体，保证中英文混排不乱码。
"""
from __future__ import annotations
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
    try:
        available = set(matplotlib.font_manager.findSystemFonts(fontpaths=None))
    except Exception:
        available = set()

    # We can't reliably check names from file paths; try names directly
    for name in _CANDIDATES:
        try:
            matplotlib.rcParams["font.family"] = [name, "DejaVu Sans", "Arial", "sans-serif"]
            break
        except Exception:
            continue
    # Minus sign fix
    matplotlib.rcParams["axes.unicode_minus"] = False

    # A few layout defaults
    matplotlib.rcParams["figure.dpi"] = 120
    matplotlib.rcParams["savefig.dpi"] = 150
    matplotlib.rcParams["figure.autolayout"] = True

def savefig(path: str, **kwargs):
    """统一保存图片，保证中文字体与高分辨率 / Save figures with consistent settings."""
    plt.savefig(path, dpi=kwargs.pop("dpi", 300), bbox_inches=kwargs.pop("bbox_inches", "tight"), **kwargs)
