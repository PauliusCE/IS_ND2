# Reproduction: AI-Powered S11 Prediction for a Compact 2.4 GHz Patch Antenna

Reproduction of the experiments in

> A. Mersani, K. Mekki, O. Ncibi, *AI-Powered S11 Prediction for a Compact 2.4 GHz Patch
> Antenna*, Indian Journal of Science and Technology, 2025, 18(33): 2715–2728.
> DOI 10.17485/IJST/v18i33.1326

using the public dataset

> *Parametric simulation dataset of a 2.4 GHz patch antenna with slot for AI-based
> S11 prediction*, Data in Brief, 2025. Zenodo DOI **10.5281/zenodo.15866821** (CC BY 4.0).

Full write-up (in Lithuanian): **[ATASKAITA.md](ATASKAITA.md)**

## Setup

```bash
pip install -r requirements.txt
mkdir data
curl -L -o data/Cleaned_DataSet.csv "https://zenodo.org/records/15866865/files/Cleaned_DataSet.csv?download=1"
```

## Run

```bash
cd src
python 01_inspect_data.py        # dataset audit
python 02_reproduce_paper.py     # Exp 1: literal replication of the paper
python 03_grouped_split.py       # Exp 2: evaluation on unseen geometries
python 04_engineering_metrics.py # Exp 3: f_res / S11_min / bandwidth errors
python 05_figures.py             # Exp 4: Figs 4/5/6, error profile
python 06_learning_curve.py      # Exp 5: how many EM simulations are needed
```

Or run everything in the browser: `jupyter notebook`, then `ND2_reproduction.ipynb`.

Total runtime ~15 min on a laptop CPU. Results land in `results/` (CSV) and
`figures/` (PNG).

## Headline results

Table 2 of the paper, reproduced:

| Model | RMSE (here) | RMSE (paper) | R² (here) | R² (paper) |
|---|---|---|---|---|
| KNN (k=5) | 0.4213 | 0.4216 | 0.9866 | 0.9866 |
| XGBoost | 0.4570 | 0.5855 | 0.9843 | 0.9742 |
| MLP (128-64) | 0.5317 | 0.5110 | 0.9787 | 0.9803 |
| Random Forest | 0.5389 | 0.5380 | 0.9781 | 0.9782 |
| SVR (RBF) | 3.3202 | 3.3202 | 0.1690 | 0.1690 |
| Linear Regression | 3.5244 | 3.5244 | 0.0637 | 0.0637 |
| Ridge Regression | 3.5244 | 3.5244 | 0.0637 | 0.0637 |

Five of seven match to 3–4 decimal places. The two that don't are the two whose
hyperparameters the paper never states.

Three findings beyond the paper:

- The dataset contains only **53 distinct geometries** swept over 1001 frequency
  points. Under a geometry-wise split — the task a design surrogate actually has
  to solve — RMSE rises from 0.42 to 1.26 dB and R² drops from 0.987 to 0.872.
- A single tuning pass on XGBoost beats the published result by 22%, which is
  hard to square with the paper's claim of "systematic hyperparameter tuning".
- Global RMSE ranks Random Forest best (1.252 dB) while the resonant-frequency
  error ranks it worst (9.08 MHz) — optimising the published metric does not
  optimise what a designer acts on.

See [ATASKAITA.md](ATASKAITA.md) for the full analysis.

## Layout

```
data/       dataset (downloaded, not committed)
src/        experiment scripts
results/    CSV outputs
figures/    generated figures
ATASKAITA.md  report (LT)
```
