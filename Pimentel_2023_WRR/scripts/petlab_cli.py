
#!/usr/bin/env python
"""
Simple CLI to run the pipeline and save outputs.
"""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from petlab.analysis import run_pipeline
from petlab.plotting import setup_fonts, savefig

def main():
    parser = argparse.ArgumentParser(description="Run PET-Lab synthetic analysis.")
    parser.add_argument("--outdir", type=str, default="outputs", help="Output directory")
    parser.add_argument("--N", type=int, default=20, help="Number of catchments")
    parser.add_argument("--T", type=int, default=730, help="Number of daily timesteps")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = run_pipeline(Ncatch=args.N, T=args.T)
    df.to_csv(outdir / "scores.csv", index=False, encoding="utf-8-sig")

    # Map: best consensus
    setup_fonts()
    fig, ax = plt.subplots(figsize=(6,4))
    colors = {"jensen_haise":"tab:blue","hargreaves":"tab:orange","priestley_taylor":"tab:green","no_match":"gray"}
    d2 = df.drop_duplicates("catchment")[["catchment","lat","lon","best_consensus"]]
    for name, grp in d2.groupby("best_consensus"):
        ax.scatter(grp["lon"], grp["lat"], s=50, label=name, alpha=0.8, c=colors.get(name,"gray"))
    ax.set_xlabel("Longitude / 经度")
    ax.set_ylabel("Latitude / 纬度")
    ax.set_title("Best PET Formula (Consensus over PET/AET/Q) / 最优公式（多过程一致）")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Formula / 公式", fontsize=8)
    savefig(outdir / "map_best_formula.png")
    plt.close(fig)

    # Budyko: density by best formula
    fig, ax = plt.subplots(figsize=(6,4))
    for name, grp in df[df["formula"]==df["best_consensus"]].groupby("best_consensus"):
        ax.scatter(grp["PET_over_P_mean"], grp["AET_over_P_mean"], s=50, alpha=0.7, label=name)
    import numpy as np
    x = np.linspace(0.01, 4.0, 400)
    from petlab.budyko import budyko_phi
    ax.plot(x, budyko_phi(x), lw=2, label="Budyko φ")
    ax.set_xlabel("Mean PET/P")
    ax.set_ylabel("Mean AET/P")
    ax.set_title("Budyko Space by Best Formula / Budyko 空间（按最优公式）")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    savefig(outdir / "budyko_density.png")
    plt.close(fig)

    print(f"Done. Results written to: {outdir}")

if __name__ == "__main__":
    main()
