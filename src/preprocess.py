# src/preprocess.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"

def load_precip():
    df = pd.read_parquet(PROC / "inmet_precip_hourly.parquet")
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def aggregate_to_weekly(df):
    df = df.set_index('datetime')
    weekly = df['precip_mm'].resample('W-SUN').sum().reset_index()  # soma por semana
    weekly = weekly.rename(columns={'precip_mm': 'precip_mm_weekly', 'datetime': 'week_end_date'})
    return weekly

if __name__ == "__main__":
    df = load_precip()
    weekly = aggregate_to_weekly(df)
    out = PROC / "precip_weekly.parquet"
    weekly.to_parquet(out, index=False)
    print(f"Saved {out}")