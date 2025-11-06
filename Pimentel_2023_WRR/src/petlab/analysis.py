
"""
Multi-process evaluation pipeline.

中文：给定若干流域与气象序列，计算三种PET，合成“观测”PET/AET/Q，
按相对误差（RE）选择各变量最优公式，并输出“联合最优”与Budyko图所需量。
"""
import numpy as np
import pandas as pd
from .synthetic import random_catchments, random_meteo, make_pet_series, synthesize_observations
from .metrics import relative_error, summarize_scores

FORMULAS = ["jensen_haise", "hargreaves", "priestley_taylor"]

def run_pipeline(Ncatch=20, T=730, seed=2025):
    rng = np.random.default_rng(seed)
    cats = random_catchments(Ncatch, seed=seed)
    met = random_meteo(T=T, seed=seed+1)
    rows = []

    # Choose a hidden "true" formula per catchment to generate pseudo-observations
    true_formulas = rng.choice(FORMULAS, size=Ncatch, p=[0.33,0.34,0.33])

    for i, c in enumerate(cats):
        pet_true = make_pet_series(c, met, true_formulas[i])
        PET_obs, AET_obs, Q_obs = synthesize_observations(met["P"].values, pet_true, rng)

        # Evaluate each candidate formula
        for f in FORMULAS:
            pet_sim = make_pet_series(c, met, f)
            # Close the loop with Budyko for AET_sim and simple residual for Q_sim (toy model)
            P = met["P"].values + 1e-6
            # Use same Budyko function as in synthetic generator to mirror model behavior
            from .budyko import budyko_phi
            AET_sim = budyko_phi(pet_sim / P) * P
            Q_sim = (P - AET_sim).clip(min=0.0)

            rows.append({
                "catchment": c.id,
                "lat": c.lat,
                "lon": c.lon,
                "formula": f,
                "RE_PET": relative_error(pet_sim, PET_obs),
                "RE_AET": relative_error(AET_sim, AET_obs),
                "RE_Q": relative_error(Q_sim, Q_obs),
                "PET_over_P_mean": float(np.mean(pet_sim / P)),
                "AET_over_P_mean": float(np.mean(AET_sim / P)),
            })

    df = pd.DataFrame(rows)
    summary = summarize_scores(df, var_cols=["RE_PET","RE_AET","RE_Q"], id_col="catchment")
    df_merged = df.merge(summary, on="catchment", how="left")
    return df_merged
