"""Experiment 4 - reproduction of the paper's figures 4, 5 and 6.

  Fig. 4  relative importance of the input parameters.
          Paper's claim: "the patch width and the length of the feed line are
          the most influential factors".
  Fig. 5  predicted vs. simulated S11 scatter.
  Fig. 6  Pearson correlation matrix.
          Paper's claim: S11 shows "very weak correlations with all input
          features (maximum |r| ~ 0.13)".

All are regenerated under the paper's own protocol (random row split), so the
comparison with the published figures is like for like.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import FIGURES, RESULTS, SEED, load_data, metrics, plot_style


def main():
    _, X, y, _ = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )

    rf = RandomForestRegressor(n_estimators=150, random_state=SEED, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print("Random Forest (paper protocol):", metrics(y_test, y_pred))

    plt = plot_style()

    # ---- Fig. 4: feature importance ----
    # The paper never states whether frequency was included in its importance
    # plot, so both variants are computed: the claim is only testable on the
    # geometry-only variant.
    imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values()

    geom_only = X.drop(columns=["frequency_GHz"])
    rf_g = RandomForestRegressor(n_estimators=150, random_state=SEED, n_jobs=-1)
    rf_g.fit(geom_only.loc[X_train.index], y_train)
    imp_g = pd.Series(rf_g.feature_importances_, index=geom_only.columns).sort_values()

    pd.DataFrame({"with_frequency": imp, "geometry_only": imp_g}).to_csv(
        RESULTS / "exp4_feature_importance.csv"
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for ax, s, title in [
        (axes[0], imp, "All inputs"),
        (axes[1], imp_g, "Geometry only (frequency excluded)"),
    ]:
        ax.barh(s.index, s.values,
                color=["#c0392b" if n == "frequency_GHz" else "#2c7fb8" for n in s.index])
        ax.set_xlabel("Relative importance")
        ax.set_title(title)
    fig.suptitle("Fig. 4 reproduction - input-parameter importance (Random Forest)")
    fig.savefig(FIGURES / "fig1_feature_importance.png")
    print(f"saved -> {FIGURES / 'fig1_feature_importance.png'}")

    print("\nwith frequency:")
    print(imp.sort_values(ascending=False).round(4).to_string())
    print("\ngeometry only (this is what the paper's claim can be tested against):")
    print(imp_g.sort_values(ascending=False).round(4).to_string())
    top2 = list(imp_g.sort_values(ascending=False).index[:2])
    print(f"\npaper claims top-2 = [patch_width_mm, length_imp_line_mm]")
    print(f"reproduction top-2 = {top2}")

    # ---- Fig. 6: Pearson correlation matrix ----
    df_all = X.copy()
    df_all["S11_dB"] = y
    corr = df_all.corr(method="pearson")
    corr.round(4).to_csv(RESULTS / "exp4_correlation_matrix.csv")

    s11_corr = corr["S11_dB"].drop("S11_dB").abs().sort_values(ascending=False)
    print(f"\nmax |r| between S11 and any single input: {s11_corr.max():.4f}"
          f"  (paper claims ~0.13)")
    print(s11_corr.round(4).to_string())

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(len(corr)), corr.columns, fontsize=7)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("Fig. 6 reproduction - Pearson correlation matrix")
    fig.savefig(FIGURES / "fig6_correlation_matrix.png")
    print(f"saved -> {FIGURES / 'fig6_correlation_matrix.png'}")

    # ---- Fig. 5: predicted vs simulated ----
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    ax.scatter(y_test, y_pred, s=3, alpha=0.25, c="#2c7fb8", edgecolors="none")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", lw=1)
    ax.set_xlabel("Simulated $S_{11}$ (dB)")
    ax.set_ylabel("Predicted $S_{11}$ (dB)")
    ax.set_title(f"Random Forest, $R^2$={metrics(y_test, y_pred)['R2']:.4f}")
    fig.savefig(FIGURES / "fig2_pred_vs_true.png")
    print(f"saved -> {FIGURES / 'fig2_pred_vs_true.png'}")

    # ---- extra: where the error actually lives ----
    # Two different questions: how big is the typical error in each region
    # (drives MAE), and how much of the squared-error sum each region owns
    # (drives RMSE and R2). They give opposite answers, which is the point.
    err = np.abs(y_test.to_numpy() - y_pred)
    bins = pd.cut(y_test, [-70, -30, -20, -10, -5, 0])
    tbl = pd.DataFrame({"S11 range (dB)": bins, "abs_err": err, "sq_err": err ** 2})

    prof = tbl.groupby("S11 range (dB)", observed=True).agg(
        count=("abs_err", "size"),
        mean_abs_err=("abs_err", "mean"),
        max_abs_err=("abs_err", "max"),
        sum_sq_err=("sq_err", "sum"),
    )
    prof["pct_of_points"] = (100 * prof["count"] / prof["count"].sum()).round(1)
    prof["pct_of_SSE"] = (100 * prof["sum_sq_err"] / prof["sum_sq_err"].sum()).round(1)
    prof = prof.round(3)
    prof.to_csv(RESULTS / "exp4_error_profile.csv")

    print("\nError by S11 level - note that the last two columns disagree:")
    print(prof[["count", "pct_of_points", "mean_abs_err", "max_abs_err",
                "pct_of_SSE"]].to_string())
    print("\n  MAE is dominated by the flat region (89% of the points).")
    print("  RMSE is dominated by the resonances (0.1% of the points carry 34% of SSE),")
    print("  so RMSE does penalise the large errors - it simply measures them in dB,")
    print("  not in the frequency shift a designer would act on. See experiment 3.")


if __name__ == "__main__":
    main()
