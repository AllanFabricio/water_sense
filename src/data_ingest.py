# src/data_ingest.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Resolve RAW directory robustly. The project currently contains an extra nested
# `data/data/raw` directory in the workspace, so try common candidates first and
# fall back to a recursive search for a `raw` directory under ROOT.
def _find_raw_dir(root: Path) -> Path:
    candidates = [
        root / "data" / "raw",
        root / "data" / "data" / "raw",
    ]
    for p in candidates:
        if p.exists() and p.is_dir():
            return p
    # fallback: look for any folder named 'raw' under root (first match)
    for p in root.rglob("raw"):
        if p.is_dir():
            return p
    # final fallback: default location (may not exist)
    return root / "data" / "raw"

RAW = _find_raw_dir(ROOT)
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

print(f"[data_ingest] ROOT={ROOT}")
print(f"[data_ingest] RAW={RAW}")
print(f"[data_ingest] PROC={PROC}")

def load_inmet(csv_path: Path):
    # Tenta ler o arquivo com diferentes configurações
    print(f"\nTentando ler arquivo: {csv_path}")
    
    # Primeiro, vamos ver as primeiras linhas do arquivo para debug
    with open(csv_path, 'rb') as f:
        print("\nPrimeiras linhas do arquivo (raw):")
        for i, line in enumerate(f):
            if i < 5:  # mostrar primeiras 5 linhas
                print(line)
    
    # Tenta diferentes configurações de leitura
    try:
        # Tenta ler pulando linhas de cabeçalho se necessário
        df = pd.read_csv(csv_path, sep=';', encoding='latin1', skiprows=8)
        print("\nSucesso ao ler o arquivo!")
        print(f"Formato do DataFrame: {df.shape}")
    except Exception as e:
        print(f"\nErro ao ler o arquivo: {str(e)}")
        raise
    
    print("\nColunas encontradas no arquivo:")
    print(df.columns.tolist())
    
    # Colunas específicas do INMET
    date_col = 'DATA (YYYY-MM-DD)'
    hora_col = 'HORA (UTC)'
    precip_col = 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'
    
    # Verificar se as colunas existem
    required_cols = [date_col, hora_col, precip_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colunas obrigatórias não encontradas: {missing_cols}")
        
    # Combinar data e hora (formato esperado: YYYY-MM-DD HH:00)
    df['datetime'] = pd.to_datetime(df[date_col] + ' ' + df[hora_col], format='%Y-%m-%d %H:%M')
    # Selecionar e renomear colunas
    df = df[['datetime', precip_col]].rename(columns={precip_col: 'precip_mm'})
    
    # Converter precipitação para número e tratar missing values
    df['precip_mm'] = pd.to_numeric(df['precip_mm'], errors='coerce')
    df = df.dropna()
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