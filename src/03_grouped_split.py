"""Experiment 2 - honest evaluation with a geometry-wise split.

Experiment 1 reproduces the paper, but the dataset contains only 53 distinct
antenna geometries, each swept over 1001 frequency points. A random row split
therefore places neighbouring points of the SAME S11 curve in both train and
test, so the models are interpolating along curves they have already seen. That
is not the task a design surrogate has to solve: in practice the model must
predict S11 for a geometry that was never simulated.

This experiment repeats the comparison with GroupKFold over the geometry id, so
every test geometry is unseen during training. Constant columns are dropped
because they carry no information.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import RESULTS, load_data, metrics, model_zoo

N_SPLITS = 5


def main():
    _, X, y, groups = load_data()

    const_cols = [c for c in X.columns if X[c].nunique() == 1]
    X = X.drop(columns=const_cols)
    print(f"dropped constant columns: {const_cols}")
    print(f"features used           : {list(X.columns)}")
    print(f"geometries              : {len(np.unique(groups))}, folds: {N_SPLITS}\n")

    gkf = GroupKFold(n_splits=N_SPLITS)
    rows = []

    for name, model in model_zoo().items():
        fold_scores = []
        for tr, te in gkf.split(X, y, groups):
            pipe = make_pipeline(StandardScaler(), model)
            pipe.fit(X.iloc[tr], y.iloc[tr])
            fold_scores.append(metrics(y.iloc[te], pipe.predict(X.iloc[te])))

        agg = {
            "Model": name,
            "RMSE": np.mean([s["RMSE"] for s in fold_scores]),
            "RMSE_std": np.std([s["RMSE"] for s in fold_scores]),
            "MAE": np.mean([s["MAE"] for s in fold_scores]),
            "R2": np.mean([s["R2"] for s in fold_scores]),
            "R2_std": np.std([s["R2"] for s in fold_scores]),
        }
        rows.append(agg)
        print(f"{name:<22} RMSE={agg['RMSE']:.3f}+-{agg['RMSE_std']:.3f}  "
              f"MAE={agg['MAE']:.3f}  R2={agg['R2']:.3f}+-{agg['R2_std']:.3f}")

    res = pd.DataFrame(rows)
    out = RESULTS / "exp2_grouped_split.csv"
    res.to_csv(out, index=False)
    print(f"\nsaved -> {out}")

    # Direct contrast with experiment 1.
    exp1 = pd.read_csv(RESULTS / "exp1_random_split.csv")
    cmp = exp1[["Model", "RMSE", "R2"]].merge(
        res[["Model", "RMSE", "R2"]], on="Model", suffixes=(" random", " grouped")
    )
    cmp.to_csv(RESULTS / "exp2_comparison.csv", index=False)
    print("\nrandom row split vs unseen-geometry split:")
    print(cmp.to_string(index=False))


if __name__ == "__main__":
    main()
