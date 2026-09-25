"""Shared helpers: data loading, model zoo, metrics, plotting style.

Paper under reproduction:
  A. Mersani et al., "AI-Powered S11 Prediction for a Compact 2.4 GHz Patch
  Antenna", Indian Journal of Science and Technology, 2025.
Dataset:
  "Parametric simulation dataset of a 2.4 GHz patch antenna with slot for
  AI-based S11 prediction", Data in Brief, 2025.
  Zenodo DOI 10.5281/zenodo.15866821 (CC BY 4.0).
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "Cleaned_DataSet.csv"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

SEED = 42
TARGET = "S11_dB"

# All 10 geometric columns present in the CSV. Three of them are constant in the
# published data (width_imp_line_mm, substrate_height_mm, patch_height_mm); they
# are kept here so the replication matches the authors' protocol exactly, and are
# dropped separately in the grouped-split experiment.
GEOM_COLS = [
    "width_substrate_mm", "width_imp_line_mm", "length_imp_line_mm",
    "substrate_height_mm", "patch_height_mm", "width_slot_mm",
    "length_slot_mm", "patch_width_mm", "substrate_length_mm",
    "patch_length_mm",
]

# Table 2 of the paper, "Performance Comparison of Regression Models for S11
# Prediction". All seven models are reported there; keys match model_zoo().
PAPER_RESULTS = {
    "KNN (k=5)":           {"MAE": 0.0495, "RMSE": 0.4216, "R2": 0.9866},
    "MLP (128-64)":        {"MAE": 0.1795, "RMSE": 0.5110, "R2": 0.9803},
    "Random Forest (150)": {"MAE": 0.0600, "RMSE": 0.5380, "R2": 0.9782},
    "XGBoost":             {"MAE": 0.1329, "RMSE": 0.5855, "R2": 0.9742},
    "SVR (RBF)":           {"MAE": 1.2276, "RMSE": 3.3202, "R2": 0.1690},
    "Linear Regression":   {"MAE": 1.9968, "RMSE": 3.5244, "R2": 0.0637},
    "Ridge Regression":    {"MAE": 1.9968, "RMSE": 3.5244, "R2": 0.0637},
}


def load_data():
    """Return (df, X, y, groups) where groups identifies the antenna geometry."""
    df = pd.read_csv(CSV)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    groups = df.groupby(GEOM_COLS, sort=False).ngroup().to_numpy()
    return df, X, y, groups


def model_zoo():
    """The seven models benchmarked in Table 2 of the paper.

    The paper states the protocol (normalisation, 80/20 split, MAE/RMSE/R2) but
    gives no hyperparameters. KNN (k=5) and Random Forest (150 trees) are taken
    from the authors' own notebook on Zenodo; the rest are scikit-learn defaults
    except XGBoost and MLP, which are tuned here (see report, section 3).
    """
    return {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(random_state=SEED),
        "SVR (RBF)": SVR(cache_size=1000),
        "KNN (k=5)": KNeighborsRegressor(n_neighbors=5),
        "Random Forest (150)": RandomForestRegressor(
            n_estimators=150, random_state=SEED, n_jobs=-1
        ),
        "XGBoost": XGBRegressor(
            n_estimators=600, max_depth=8, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9,
            random_state=SEED, n_jobs=-1, tree_method="hist",
        ),
        "MLP (128-64)": MLPRegressor(
            hidden_layer_sizes=(128, 64), activation="relu", solver="adam",
            learning_rate_init=1e-3, max_iter=400, early_stopping=True,
            n_iter_no_change=15, random_state=SEED,
        ),
    }


def metrics(y_true, y_pred):
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
    }


def plot_style():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 130,
        "font.size": 9,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "savefig.bbox": "tight",
    })
    return plt
