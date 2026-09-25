"""Experiment 6 - checking the paper's design claims against its own dataset.

Three claims are testable directly:

  Table 1  the final optimised dimensions
  Fig. 7   "deep resonance at 2.45 GHz and a return loss of less than -40 dB"
  Sec 2.1  the parametric sweeps of slot width, slot length and feed length

The point is not fault-finding but provenance: the dataset released with the
paper should contain the design the paper reports.
"""

import numpy as np
import pandas as pd

from common import GEOM_COLS, RESULTS, load_data

# Table 1 of the paper, mapped onto the dataset's column names.
TABLE1 = {
    "substrate_length_mm": 40,
    "width_substrate_mm": 42,
    "width_imp_line_mm": 3,
    "substrate_height_mm": 1.6,
    "patch_height_mm": 0.035,
    "patch_length_mm": 29.3,
    "width_slot_mm": 2,
    "length_slot_mm": 7,
    "patch_width_mm": 42,
    "length_imp_line_mm": 11,
}


def main():
    df, X, y, groups = load_data()

    # ---- which Table 1 values actually occur in the released data? ----
    print("Table 1 of the paper vs. the values present in the dataset:\n")
    rows = []
    for col, want in TABLE1.items():
        present = sorted(df[col].unique())
        rows.append({
            "parameter": col,
            "Table 1": want,
            "in dataset": "yes" if want in present else "NO",
            "dataset values": ", ".join(str(v) for v in present[:8]),
        })
    t1 = pd.DataFrame(rows)
    t1.to_csv(RESULTS / "exp6_table1_check.csv", index=False)
    print(t1.to_string(index=False))

    # ---- is the final design (Fig. 7) in the dataset? ----
    df = df.assign(g=groups)
    best = df.loc[df.groupby("g")["S11_dB"].idxmin(),
                  ["g", "frequency_GHz", "S11_dB"] + GEOM_COLS]
    best = best.rename(columns={"frequency_GHz": "f_res_GHz",
                                "S11_dB": "S11_min_dB"})

    print(f"\n\nDeepest resonance over all {len(best)} geometries: "
          f"{best.S11_min_dB.min():.2f} dB")

    claim = best[(best.S11_min_dB < -40)
                 & (best.f_res_GHz.between(2.44, 2.46))]
    print(f"Geometries matching Fig. 7 (S11 < -40 dB at 2.45 +- 0.01 GHz): {len(claim)}")
    if len(claim):
        print(claim[["g", "f_res_GHz", "S11_min_dB", "width_slot_mm",
                     "length_slot_mm", "length_imp_line_mm"]].to_string(index=False))

    near = best[best.S11_min_dB < -40]
    print(f"\nGeometries with S11 < -40 dB at any frequency: {len(near)}")
    if len(near):
        print(near[["g", "f_res_GHz", "S11_min_dB"]].to_string(index=False))

    best.sort_values("S11_min_dB").to_csv(RESULTS / "exp6_best_per_geometry.csv",
                                          index=False)

    # ---- the slot-width sweep of Fig. 2(a) ----
    print("\n\nFig. 2(a) slot-width sweep, as reconstructed from the dataset")
    print("(paper: best match at SW = 2 mm, S11 = -29.59 dB):\n")
    sw = best.groupby("width_slot_mm").agg(
        geometries=("g", "count"),
        best_S11_dB=("S11_min_dB", "min"),
        f_res_GHz=("f_res_GHz", "median"),
    ).round(2)
    print(sw.to_string())
    sw.to_csv(RESULTS / "exp6_slot_width_sweep.csv")


if __name__ == "__main__":
    main()
