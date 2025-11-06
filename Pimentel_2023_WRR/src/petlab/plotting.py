
"""
Matplotlib style helpers with Chinese+English font compatibility.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt

CJK_CANDIDATES = ["Noto Sans CJK SC", "SimHei", "Microsoft YaHei", "PingFang SC", "WenQuanYi Zen Hei", "Source Han Sans SC", "DejaVu Sans"]

def setup_fonts():
    # Try to set a font that supports CJK; fall back to DejaVu Sans.
    available = set(mpl.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
    # Can't easily test family names from files here; use a family list.
    mpl.rcParams["font.family"] = CJK_CANDIDATES
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["figure.dpi"] = 120
    mpl.rcParams["savefig.dpi"] = 150

def savefig(path, bbox_inches="tight"):
    plt.savefig(path, bbox_inches=bbox_inches)
