\
# -*- coding: utf-8 -*-
"""
Matplotlib CN/EN font helper.
自动设置一组常见中文字体的优先级，并关闭负号乱码。
"""
import matplotlib
from matplotlib import font_manager as fm

def setup_cn_en_font():
    candidates = [
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Microsoft YaHei",
        "SimHei",
        "PingFang SC",
        "WenQuanYi Zen Hei",
        "Arial Unicode MS",
    ]
    # Note: fm._rebuild() is deprecated in newer matplotlib versions
    # Font cache is now automatically managed
    existing = set(f.name for f in fm.fontManager.ttflist)
    chosen = None
    for name in candidates:
        if name in existing:
            chosen = name
            break
    if chosen is None:
        # fallback to default; warn
        print("[Font] No CJK font found. Falling back to default; Chinese may not render.")
    else:
        matplotlib.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans", "Arial"]
    matplotlib.rcParams["axes.unicode_minus"] = False
    return chosen
