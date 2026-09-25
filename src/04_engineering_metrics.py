"""Experiment 3 - what the surrogate is actually worth to an antenna designer.

RMSE in dB over all frequency points is a weak figure of merit: most of an S11
sweep is flat near 0 dB, so a model can score well while completely missing the
resonance. An antenna designer cares about three numbers:

  f_res      resonant frequency (argmin of S11)
  S11_min    depth of the resonance
  BW-10dB    bandwidth below -10 dB

This experiment predicts the FULL S11(f) curve of every geometry that was never
seen during training (GroupKFold over geometry id) and reports the error in
those three quantities, which is the form in which the surrogate would replace a
CST parameter sweep.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import FIGURES, RESULTS, TARGET, load_data, model_zoo, plot_style

N_SPLITS = 5
MODELS = ["KNN (k=5)", "Random Forest (150)", "XGBoost"]


def curve_features(freq, s11):
    """Extract (f_res, S11_min, BW-10dB) from one sweep."""
    i = int(np.argmin(s11))
    f_res = float(freq[i])
    s_min = float(s11[i])

    below = s11 < -10.0
    if not below.any():
        bw = 0.0
    else:
        # width of the contiguous band that contains the minimum
        lo = i
        while lo > 0 and below[lo - 1]:
            lo -= 1
        hi = i
        while hi < len(below) - 1 and below[hi + 1]:
            hi += 1
        bw = float(freq[hi] - freq[lo]) if below[i] else 0.0
    return f_res, s_min, bw * 1000.0  # BW in MHz


def main():
    df, X, y, groups = load_data()
    const_cols = [c for c in X.columns if X[c].nunique() == 1]
    X = X.drop(columns=const_cols)

    gkf = GroupKFold(n_splits=N_SPLITS)
    records = []
    curves = {}  # (model, geometry) -> (freq, true, pred)

    for name in MODELS:
        model = model_zoo()[name]
        for tr, te in gkf.split(X, y, groups):
            pipe = make_pipeline(StandardScaler(), model)
            pipe.fit(X.iloc[tr], y.iloc[tr])
            pred = pipe.predict(X.iloc[te])

            fold = pd.DataFrame({
                "g": groups[te],
                "f": X.iloc[te]["frequency_GHz"].to_numpy(),
                "true": y.iloc[te].to_numpy(),
                "pred": pred,
            })
            # some geometries were simulated twice -> average duplicate points
            fold = fold.groupby(["g", "f"], as_index=False).mean()

            for g, sub in fold.groupby("g"):
                sub = sub.sort_values("f")
                f = sub["f"].to_numpy()
                t_res, t_min, t_bw = curve_features(f, sub["true"].to_numpy())
                p_res, p_min, p_bw = curve_features(f, sub["pred"].to_numpy())
                records.append({
                    "Model": name, "geometry": int(g),
                    "f_res_true": t_res, "f_res_pred": p_res,
                    "f_res_err_MHz": abs(p_res - t_res) * 1000.0,
                    "S11min_true": t_min, "S11min_pred": p_min,
                    "S11min_err_dB": abs(p_min - t_min),
                    "BW_true_MHz": t_bw, "BW_pred_MHz": p_bw,
                    "BW_err_MHz": abs(p_bw - t_bw),
                })
                curves[(name, int(g))] = (f, sub["true"].to_numpy(),
                                          sub["pred"].to_numpy())

    det = pd.DataFrame(records)
    det.to_csv(RESULTS / "exp3_per_geometry.csv", index=False)

    summary = det.groupby("Model").agg(
        f_res_MAE_MHz=("f_res_err_MHz", "mean"),
        f_res_median_MHz=("f_res_err_MHz", "median"),
        f_res_within_10MHz=("f_res_err_MHz", lambda s: (s <= 10).mean() * 100),
        S11min_MAE_dB=("S11min_err_dB", "mean"),
        BW_MAE_MHz=("BW_err_MHz", "mean"),
    ).round(2)
    summary.to_csv(RESULTS / "exp3_summary.csv")
    print("Unseen-geometry prediction of engineering quantities "
          f"({det.geometry.nunique()} geometries):\n")
    print(summary.to_string())

    # ---- figure: best / median / worst curve for the strongest model ----
    best_model = summary["f_res_MAE_MHz"].idxmin()
    sub = det[det.Model == best_model].sort_values("f_res_err_MHz")
    picks = [
        ("best", sub.iloc[0]),
        ("median", sub.iloc[len(sub) // 2]),
        ("worst", sub.iloc[-1]),
    ]

    plt = plot_style()
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2), sharey=True)
    for ax, (label, row) in zip(axes, picks):
        f, t, p = curves[(best_model, int(row.geometry))]
        ax.plot(f, t, "b-", lw=1.4, label="CST (true)")
        ax.plot(f, p, "r--", lw=1.4, label="surrogate")
        ax.axhline(-10, color="gray", ls=":", lw=0.8)
        ax.set_title(f"{label}: geom #{int(row.geometry)}, "
                     f"$\\Delta f_{{res}}$={row.f_res_err_MHz:.0f} MHz")
        ax.set_xlabel("Frequency (GHz)")
    axes[0].set_ylabel("$S_{11}$ (dB)")
    axes[0].legend(loc="lower left", fontsize=8)
    fig.suptitle(f"S11 prediction for unseen geometries - {best_model}", y=1.03)
    fig.savefig(FIGURES / "fig3_curves_unseen.png")
    print(f"\nsaved -> {FIGURES / 'fig3_curves_unseen.png'}")

    # ---- figure: error distribution ----
    fig, ax = plt.subplots(figsize=(6, 3.2))
    data = [det[det.Model == m]["f_res_err_MHz"].to_numpy() for m in MODELS]
    ax.boxplot(data, tick_labels=[m.split(" (")[0] for m in MODELS])
    ax.set_ylabel("$|\\Delta f_{res}|$ (MHz)")
    ax.set_title("Resonant-frequency error on unseen geometries")
    fig.savefig(FIGURES / "fig4_fres_error.png")
    print(f"saved -> {FIGURES / 'fig4_fres_error.png'}")


if __name__ == "__main__":
    main()
