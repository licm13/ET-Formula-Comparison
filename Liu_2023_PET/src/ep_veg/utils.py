import math
from typing import Optional, Sequence

def saturation_vapor_pressure_kpa(T_C: float) -> float:
    """
    饱和水汽压 (Tetens, kPa). Units per FAO-56.
    es = 0.6108 * exp(17.27 * T / (T + 237.3))
    """
    return 0.6108 * math.exp(17.27 * T_C / (T_C + 237.3))

def slope_svp_kpa_per_C(T_C: float) -> float:
    """
    Δ: 饱和水汽压-温度曲线斜率 (kPa/°C). FAO-56
    Δ = 4098 * es / (T + 237.3)^2
    """
    es = saturation_vapor_pressure_kpa(T_C)
    return 4098.0 * es / ((T_C + 237.3) ** 2)

def vpd_from_T_RH(T_C: float, RH: float) -> float:
    """
    基于温度与相对湿度估算 VPD (kPa). RH ∈ [0,100].
    VPD = es(T) * (1 - RH/100)
    """
    es = saturation_vapor_pressure_kpa(T_C)
    return es * (1.0 - RH / 100.0)

def auto_configure_chinese_fonts(candidate_families: Optional[Sequence[str]] = None) -> str:
    """
    自动配置 Matplotlib 中文字体（若可用）。返回使用的字体名。
    - 默认候选：Noto Sans CJK SC / Microsoft YaHei / SimHei / Source Han Sans SC / PingFang SC / Heiti TC
    - 若均不可用，则保持默认字体（英文正常，中文可能为方块）。
    """
    try:
        import matplotlib
        from matplotlib import font_manager
        matplotlib.rcParams["axes.unicode_minus"] = False  # 修复负号显示
        if candidate_families is None:
            candidate_families = [
                "Noto Sans CJK SC", "Microsoft YaHei", "SimHei",
                "Source Han Sans SC", "PingFang SC", "Heiti TC"
            ]
        installed = [f.name for f in font_manager.fontManager.ttflist]
        for fam in candidate_families:
            if fam in installed:
                matplotlib.rcParams["font.family"] = fam
                return fam
        return matplotlib.rcParams.get("font.family", ["DejaVu Sans"])[0]
    except Exception:
        return "default"
