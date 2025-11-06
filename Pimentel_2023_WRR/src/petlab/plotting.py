
"""
Matplotlib style helpers with Chinese+English font compatibility.
"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

CJK_CANDIDATES = ["Noto Sans CJK SC", "SimHei", "Microsoft YaHei", "PingFang SC", "WenQuanYi Zen Hei", "Source Han Sans SC", "DejaVu Sans"]

def setup_fonts():
    # Get available font names
    available_fonts = set(f.name for f in mpl.font_manager.fontManager.ttflist)
    
    # Find the first available Chinese font
    chosen_font = None
    for font in CJK_CANDIDATES:
        if font in available_fonts:
            chosen_font = font
            break
    
    # Set font family with Chinese font support
    if chosen_font:
        mpl.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
        print(f"[Font] Using Chinese font: {chosen_font}")
    else:
        # Fallback to any available Chinese font
        chinese_fonts = [f for f in available_fonts if any(x in f.lower() for x in ['yahei', 'simhei', 'kai', 'hei'])]
        if chinese_fonts:
            chosen_font = chinese_fonts[0]
            mpl.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
            print(f"[Font] Using fallback Chinese font: {chosen_font}")
        else:
            mpl.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
            print("[Font] No Chinese fonts found. Chinese characters may not display correctly.")
    
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["axes.unicode_minus"] = False
    mpl.rcParams["figure.dpi"] = 120
    mpl.rcParams["savefig.dpi"] = 150

def savefig(path, bbox_inches="tight"):
    # Create directory if it doesn't exist
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    plt.savefig(path, bbox_inches=bbox_inches)
