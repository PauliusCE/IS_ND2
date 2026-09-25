"""Step 1 - dataset audit.

Checks the structural properties of the Zenodo dataset (DOI 10.5281/zenodo.15866821)
before any model is trained. The key question is how the 55,053 rows are organised:
if they are a frequency sweep of a small number of geometries, a plain row-wise
random split leaks information between train and test.
"""

import pandas as pd

from common import CSV

GEOM = [
    "width_substrate_mm", "width_imp_line_mm", "length_imp_line_mm",
    "substrate_height_mm", "patch_height_mm", "width_slot_mm",
    "length_slot_mm", "patch_width_mm", "substrate_length_mm",
    "patch_length_mm",
]


def main():
    df = pd.read_csv(CSV)
    print(f"shape                : {df.shape}")
    print(f"missing values       : {int(df.isna().sum().sum())}")
    print(f"duplicated rows      : {int(df.duplicated().sum())}")

    groups = df.groupby(GEOM, sort=False).ngroup()
    sizes = groups.value_counts()
    print(f"\nunique geometries    : {groups.nunique()}")
    print(f"rows per geometry    : min={sizes.min()}, max={sizes.max()}, mean={sizes.mean():.1f}")

    print(f"\nfrequency range      : {df.frequency_GHz.min():.4f} - {df.frequency_GHz.max():.4f} GHz")
    print(f"frequency points     : {df.frequency_GHz.nunique()}")
    print(f"S11 range            : {df.S11_dB.min():.2f} .. {df.S11_dB.max():.2f} dB")

    print("\nunique values per column:")
    for c in df.columns:
        print(f"  {c:<22} {df[c].nunique()}")

    print("\nColumns that never vary (useless as ML features):")
    const = [c for c in df.columns if df[c].nunique() == 1]
    print("  " + (", ".join(const) if const else "none"))


if __name__ == "__main__":
    main()
