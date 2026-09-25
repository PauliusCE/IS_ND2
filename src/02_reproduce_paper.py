"""Experiment 1 - literal replication of the paper's protocol.

Protocol taken from the paper and from the authors' own notebook shipped with
the Zenodo record (ML_PatchAntenna_.ipynb):
  - all 11 columns (10 geometry + frequency) used as features
  - StandardScaler fitted on the full feature matrix
  - train_test_split(test_size=0.2, random_state=42), i.e. a RANDOM ROW SPLIT
  - metrics: RMSE, MAE, R2

Reference values are Table 2 of the paper, which reports MAE, RMSE and R2 for all
seven benchmarked models.
"""

import time

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import PAPER_RESULTS, RESULTS, SEED, load_data, metrics, model_zoo


def main():
    _, X, y, _ = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )
    print(f"train rows: {len(X_train)}   test rows: {len(X_test)}\n")

    rows = []
    for name, model in model_zoo().items():
        pipe = make_pipeline(StandardScaler(), model)
        t0 = time.perf_counter()
        pipe.fit(X_train, y_train)
        fit_s = time.perf_counter() - t0
        m = metrics(y_test, pipe.predict(X_test))
        m["Model"] = name
        m["fit_s"] = round(fit_s, 1)
        rows.append(m)
        print(f"{name:<22} RMSE={m['RMSE']:.4f}  MAE={m['MAE']:.4f}  "
              f"R2={m['R2']:.4f}  ({fit_s:.1f}s)")

    res = pd.DataFrame(rows)[["Model", "MAE", "RMSE", "R2", "fit_s"]]

    # Side-by-side comparison with Table 2 of the paper.
    for metric in ("MAE", "RMSE", "R2"):
        res[f"paper_{metric}"] = res["Model"].map(
            lambda n: PAPER_RESULTS.get(n, {}).get(metric)
        )
    res["d_RMSE"] = (res["RMSE"] - res["paper_RMSE"]).round(4)
    res["d_R2"] = (res["R2"] - res["paper_R2"]).round(4)

    res = res.sort_values("RMSE").reset_index(drop=True)
    out = RESULTS / "exp1_random_split.csv"
    res.to_csv(out, index=False)
    print(f"\nsaved -> {out}")

    show = res[["Model", "MAE", "paper_MAE", "RMSE", "paper_RMSE",
                "R2", "paper_R2", "d_RMSE"]]
    print("\nthis reproduction vs. Table 2 of the paper:")
    print(show.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
