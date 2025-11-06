
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compute PET variants, AI, and toy PDSI-like metrics from synthetic data and plot demo figures.
基于合成数据计算 PET 变体、AI 与教学版干旱指标，并出图（定性复刻 Fig.2/3 趋势形态）。
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from paradoxes_pet.plotting import set_cn_en_fonts
from paradoxes_pet.data import generate_synthetic_monthly
from paradoxes_pet.pet import (
    pm_rc_pet_mm_day, pm_rc_pet_yang_mm_day, pm_rc_pet_jarvis_mm_day
)
from paradoxes_pet.indices import (
    annual_aridity_index, toy_pdsi_like, drought_extent_and_frequency
)

def main():
    font_used = set_cn_en_fonts()
    print("Font used:", font_used)

    df = generate_synthetic_monthly(seed=42)

    # PET calculations (monthly, mm/day -> convert to mm/month by multiplying by ~30 for demo)
    days = df.index.days_in_month.values
    PET_pm = pm_rc_pet_mm_day(df["Ta_C"], df["Rn_star_MJ_m2_day"], df["VPD_kPa"], df["WS2_m_s"])
    PET_yang = pm_rc_pet_yang_mm_day(df["Ta_C"], df["Rn_star_MJ_m2_day"], df["VPD_kPa"], df["WS2_m_s"], df["CO2_ppm"])
    PET_jarvis = pm_rc_pet_jarvis_mm_day(df["Ta_C"], df["Rn_star_MJ_m2_day"], df["VPD_kPa"], df["WS2_m_s"], df["Sg_W_m2"], df["CO2_ppm"])

    pet_month_pm = pd.Series(PET_pm * days, index=df.index)
    pet_month_yang = pd.Series(PET_yang * days, index=df.index)
    pet_month_jarvis = pd.Series(PET_jarvis * days, index=df.index)

    # AI (annual)
    AI_pm = annual_aridity_index(df["P_mm"], pet_month_pm)
    AI_yang = annual_aridity_index(df["P_mm"], pet_month_yang)
    AI_jarvis = annual_aridity_index(df["P_mm"], pet_month_jarvis)

    # Plot AI anomalies relative to 1950–2014 mean (demo)
    ref = (1950, 2014)
    AI_df = pd.DataFrame({
        "AI_PM": AI_pm,
        "AI_Yang": AI_yang,
        "AI_Jarvis": AI_jarvis
    }).dropna()
    ref_slice = AI_df[(AI_df.index.year >= ref[0]) & (AI_df.index.year <= ref[1])].mean()
    AI_anom = AI_df - ref_slice

    os.makedirs("figures", exist_ok=True)
    plt.figure(figsize=(10,5))
    AI_anom["AI_PM"].plot(label="AI (PM-RC) 传统", alpha=0.9)
    AI_anom["AI_Yang"].plot(label="AI (PM-RC+CO₂)", alpha=0.9)
    AI_anom["AI_Jarvis"].plot(label="AI (PM-RC+多因子气孔)", alpha=0.9)
    plt.axhline(0, lw=1, ls="--")
    plt.title("AI 年距平（教学演示，合成数据）\nAnnual Aridity Index anomalies (synthetic demo)")
    plt.xlabel("Year")
    plt.ylabel("AI anomaly (相对于1950–2014)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/fig2_AI_anomalies_demo.png", dpi=180)
    plt.close()

    # Toy PDSI-like series (monthly) + annual stats
    Z_pm = toy_pdsi_like(df["P_mm"], pet_month_pm)
    Z_yang = toy_pdsi_like(df["P_mm"], pet_month_yang)
    Z_jarvis = toy_pdsi_like(df["P_mm"], pet_month_jarvis)

    # Annual mean PDSI-like anomaly (demo for panel a)
    Z_annual = pd.DataFrame({
        "PM": Z_pm.resample("YE").mean(),
        "Yang": Z_yang.resample("YE").mean(),
        "Jarvis": Z_jarvis.resample("YE").mean()
    })
    Z_annual = Z_annual - Z_annual[(Z_annual.index.year>=1950)&(Z_annual.index.year<=2014)].mean()

    plt.figure(figsize=(10,5))
    Z_annual["PM"].plot(label="PDSI-like (PM-RC)", alpha=0.9)
    Z_annual["Yang"].plot(label="PDSI-like (PM-RC+CO₂)", alpha=0.9)
    Z_annual["Jarvis"].plot(label="PDSI-like (PM-RC+多因子气孔)", alpha=0.9)
    plt.axhline(0, lw=1, ls="--")
    plt.title("类PDSI 年距平（教学演示，合成数据）\nAnnual PDSI-like anomalies (synthetic demo)")
    plt.xlabel("Year")
    plt.ylabel("Anomaly")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/fig3a_pdsi_like_demo.png", dpi=180)
    plt.close()

    # Extent & frequency under severe threshold (e.g., -3)
    extent_pm, freq_pm = drought_extent_and_frequency(Z_pm, thresh=-3.0)
    extent_yang, freq_yang = drought_extent_and_frequency(Z_yang, thresh=-3.0)
    extent_jarvis, freq_jarvis = drought_extent_and_frequency(Z_jarvis, thresh=-3.0)

    # For single-point demo, "extent" = share of months below threshold per year
    EF = pd.DataFrame({
        "Extent_PM": extent_pm,
        "Extent_Yang": extent_yang,
        "Extent_Jarvis": extent_jarvis,
        "Freq_PM": freq_pm,
        "Freq_Yang": freq_yang,
        "Freq_Jarvis": freq_jarvis
    })

    # Plot extent (panel b analogue) and frequency (panel c analogue)
    plt.figure(figsize=(10,5))
    (100*EF["Extent_PM"]).plot(label="PM-RC", alpha=0.9)
    (100*EF["Extent_Yang"]).plot(label="PM-RC+CO₂", alpha=0.9)
    (100*EF["Extent_Jarvis"]).plot(label="PM-RC+多因子气孔", alpha=0.9)
    plt.title("严重干旱月占比（%）（教学演示，单点近似）\nSevere-drought months (%), synthetic single-point demo")
    plt.ylabel("% of months (per year)")
    plt.xlabel("Year")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/fig3b_extent_demo.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10,5))
    EF["Freq_PM"].plot(label="PM-RC", alpha=0.9)
    EF["Freq_Yang"].plot(label="PM-RC+CO₂", alpha=0.9)
    EF["Freq_Jarvis"].plot(label="PM-RC+多因子气孔", alpha=0.9)
    plt.title("严重干旱月频次（教学演示，单点近似）\nSevere-drought monthly count (per year)")
    plt.ylabel("Months/year")
    plt.xlabel("Year")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/fig3c_frequency_demo.png", dpi=180)
    plt.close()

    print("Saved figures -> figures/fig2_AI_anomalies_demo.png, fig3a_pdsi_like_demo.png, fig3b_extent_demo.png, fig3c_frequency_demo.png")

if __name__ == "__main__":
    main()
