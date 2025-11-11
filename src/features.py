# src/features.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

def build_features():
    precip = pd.read_parquet(PROC / "precip_weekly.parquet")
    precip = precip.sort_values('week_end_date')
    precip['precip_1w_lag'] = precip['precip_mm_weekly'].shift(1)
    precip['precip_2w_lag'] = precip['precip_mm_weekly'].shift(2)
    precip['precip_3w_lag'] = precip['precip_mm_weekly'].shift(3)
    precip = precip.dropna().reset_index(drop=True)
    precip.to_parquet(PROC / "features_precip.parquet", index=False)
    print("Saved features_precip.parquet")
    return precip

if __name__ == "__main__":
    build_features()