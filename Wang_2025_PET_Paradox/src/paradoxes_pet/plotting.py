
"""
Plotting helpers with CN/EN font support.
中英文绘图工具，自动寻找常见中文字体 + 负号兼容。
"""
from __future__ import annotations
import matplotlib
import matplotlib.font_manager
import matplotlib.pyplot as plt

def set_cn_en_fonts():
    """
    Try several common CJK fonts; fall back gracefully.
    尝试设置常见中文字体，失败则回退到默认字体。
    """
    matplotlib.rcParams["axes.unicode_minus"] = False
    
    # Get available font names
    available_fonts = set(f.name for f in matplotlib.font_manager.fontManager.ttflist)
    
    candidates = [
        "Microsoft YaHei",
        "SimHei", 
        "Noto Sans CJK SC",
        "Noto Sans SC",
        "Source Han Sans SC",
        "Arial Unicode MS",
    ]
    
    # Find the first available Chinese font
    chosen_font = None
    for name in candidates:
        if name in available_fonts:
            chosen_font = name
            break
    
    if chosen_font:
        plt.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
        print(f"Font used: {chosen_font}")
        return chosen_font
    else:
        # Fallback to any available Chinese font
        chinese_fonts = [f for f in available_fonts if any(x in f.lower() for x in ['yahei', 'simhei', 'kai', 'hei'])]
        if chinese_fonts:
            chosen_font = chinese_fonts[0]
            plt.rcParams["font.sans-serif"] = [chosen_font, "DejaVu Sans", "Arial"]
            print(f"Font used: {chosen_font}")
            return chosen_font
        else:
            print("No Chinese fonts found. Chinese characters may not display correctly.")
            return None
