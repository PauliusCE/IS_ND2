"""Experiment 5 - how many EM simulations does the surrogate actually need?

This is the question that matters when the method is transferred to a new
design (e.g. a Ku-band array element): each training geometry costs one full-wave
simulation. The curve below shows test error on a fixed set of held-out
geometries as the number of training geometries grows from 5 to 42.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import FIGURES, RESULTS, SEED, load_data, metrics, model_zoo, plot_style

MODELS = ["KNN (k=5)", "Random Forest (150)", "XGBoost"]
SIZES = [5, 10, 15, 20, 25, 30, 35, 42]
REPEATS = 5


def main():
    _, X, y, groups = load_data()
    const_cols = [c for c in X.columns if X[c].nunique() == 1]
    X = X.drop(columns=const_cols)

    rng = np.random.default_rng(SEED)
    all_groups = np.unique(groups)
    rows = []

    for rep in range(REPEATS):
        # fixed held-out geometries for this repetition
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED + rep)
        tr_idx, te_idx = next(gss.split(X, y, groups))
        pool = np.unique(groups[tr_idx])
        te_mask = np.isin(groups, np.unique(groups[te_idx]))

        for n in SIZES:
            if n > len(pool):
                continue
            chosen = rng.choice(pool, size=n, replace=False)
            tr_mask = np.isin(groups, chosen)

            for name in MODELS:
                pipe = make_pipeline(StandardScaler(), model_zoo()[name])
                pipe.fit(X[tr_mask], y[tr_mask])
                m = metrics(y[te_mask], pipe.predict(X[te_mask]))
                rows.append({"rep": rep, "n_geometries": n, "Model": name, **m})

    det = pd.DataFrame(rows)
    det.to_csv(RESULTS / "exp5_learning_curve_raw.csv", index=False)

    piv = det.groupby(["Model", "n_geometries"])["RMSE"].mean().unstack().round(3)
    piv.to_csv(RESULTS / "exp5_learning_curve.csv")
    print("Test RMSE (dB) on unseen geometries vs. number of training geometries:\n")
    print(piv.to_string())

    plt = plot_style()
    fig, ax = plt.subplots(figsize=(6, 3.6))
    for name in MODELS:
        sub = det[det.Model == name].groupby("n_geometries")["RMSE"]
        mean, std = sub.mean(), sub.std()
        ax.plot(mean.index, mean.values, "o-", lw=1.4, ms=4, label=name)
        ax.fill_between(mean.index, mean - std, mean + std, alpha=0.15)
    ax.set_xlabel("Number of simulated training geometries")
    ax.set_ylabel("Test RMSE (dB), unseen geometries")
    ax.set_title("Cost of the surrogate in full-wave simulations")
    ax.legend(fontsize=8)
    fig.savefig(FIGURES / "fig5_learning_curve.png")
    print(f"\nsaved -> {FIGURES / 'fig5_learning_curve.png'}")


if __name__ == "__main__":
    main()
