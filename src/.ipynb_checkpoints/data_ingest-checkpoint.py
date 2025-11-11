# src/data_ingest.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

def load_inmet(csv_path: Path):
    # tenta detectar separador e colunas essenciais
    try:
        df = pd.read_csv(csv_path, sep=None, engine='python')
    except Exception:
        df = pd.read_csv(csv_path, sep=';', engine='python', encoding='latin1')
    # tente achar coluna de data/hora e precipitação
    # ajustar conforme o CSV real (verificar nomes: 'DATE', 'DATA', 'hora', 'PRECIP', etc)
    # Vamos procurar colunas com nome parecido:
    cols = [c.lower() for c in df.columns]
    # heurística:
    date_col = None
    precip_col = None
    for c in df.columns:
        if 'data' in c.lower() or 'date' in c.lower() or 'hora' in c.lower():
            date_col = c
        if 'prec' in c.lower() or 'chuv' in c.lower() or 'rain' in c.lower():
            precip_col = c
    if date_col is None:
        raise ValueError("Não consegui localizar coluna de data/hora no CSV.")
    # parse datetime
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')
    df = df.dropna(subset=[date_col])
    if precip_col is None:
        # se não encontrou precip, tenta colunas numéricas possíveis
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            precip_col = numeric_cols[0]
        else:
            raise ValueError("Não foi possível identificar coluna de precipitação.")
    df = df[[date_col, precip_col]].rename(columns={date_col: 'datetime', precip_col: 'precip_mm'})
    # garantir ordenação
    df = df.sort_values('datetime').reset_index(drop=True)
    print(df.head())
    # salvar
    out = PROC / "inmet_precip_hourly.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {out}")
    return df

if __name__ == "__main__":
    csv_path = RAW / "INMET_NE_SE_A409_ARACAJU_01-01-2018_A_31-12-2018.CSV"
    load_inmet(csv_path)