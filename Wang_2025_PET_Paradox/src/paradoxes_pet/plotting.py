
"""
Plotting helpers with CN/EN font support.
中英文绘图工具，自动寻找常见中文字体 + 负号兼容。
"""
from __future__ import annotations
import matplotlib
import matplotlib.pyplot as plt

def set_cn_en_fonts():
    """
    Try several common CJK fonts; fall back gracefully.
    尝试设置常见中文字体，失败则回退到默认字体。
    """
    matplotlib.rcParams["axes.unicode_minus"] = False
    candidates = [
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
    ]
    for name in candidates:
        try:
            plt.rcParams["font.sans-serif"] = [name] + plt.rcParams.get("font.sans-serif", [])
            # quick test draw (not shown)
            return name
        except Exception:
            continue
    return None
