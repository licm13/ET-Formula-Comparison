
"""Metrics / 评估指标。"""
import numpy as np
import pandas as pd

def relative_error(sim: np.ndarray, obs: np.ndarray) -> float:
    """Relative Error (RE) in %, sum(sim-obs)/sum(obs)*100. 中文：相对误差%（总量偏差）。"""
    obs_sum = np.sum(obs)
    if abs(obs_sum) < 1e-9:
        return float('nan')
    return float(100.0 * (np.sum(sim - obs) / obs_sum))

def summarize_scores(df: pd.DataFrame, var_cols, id_col="catchment"):
    """Summarize RE per formula and choose consensus best (all vars agree)."""
    # df contains columns: id, formula, RE_PET, RE_AET, RE_Q
    best_by_var = {}
    for v in var_cols:
        best_by_var[v] = df.loc[df.groupby(id_col)[v].idxmin()][[id_col, "formula"]].rename(columns={"formula": f"best_{v}"})
    out = best_by_var[var_cols[0]]
    for v in var_cols[1:]:
        out = out.merge(best_by_var[v], on=id_col, how="outer")
    out["consensus"] = (out.filter(like="best_").nunique(axis=1) == 1)
    # consensus formula (if all equal) else "no_match"
    def pick(row):
        vals = [row[c] for c in out.filter(like="best_").columns]
        return vals[0] if len(set(vals))==1 else "no_match"
    out["best_consensus"] = out.apply(pick, axis=1)
    return out
