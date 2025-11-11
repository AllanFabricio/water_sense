# src/modeling.py
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
MODELS = ROOT / "models"
MODELS.mkdir(exist_ok=True)

def load_data(lim_threshold=1000):
    features = pd.read_parquet(PROC / "features_precip.parquet")
    adema = pd.read_csv(PROC / "adema_aracaju_raw.csv", encoding='utf-8')
    # adema tem 'values' como csv de números por semana; precisamos mapear semanas para datas
    # Estratégia simplificada (exemplo): pegar a última semana numérica como rótulo e juntar por ordem
    # WARNING: isso é apenas um exemplo; ideal é mapear as datas reais de coleta do PDF a datas da precipitação.
    adema['last_val'] = adema['values'].apply(lambda s: int(s.split(',')[-1]) if isinstance(s, str) and s.split(',')[-1].isdigit() else None)
    adema = adema.dropna(subset=['last_val']).reset_index(drop=True)
    # replicar features para cada site (cria um dataset por site com as mesmas features temporais)
    # Para exemplo, vamos juntar por posição (i-th row of features -> i-th site). Melhor mapear por data.
    minlen = min(len(features), len(adema))
    df = features.iloc[:minlen].reset_index(drop=True).copy()
    df['label'] = (adema['last_val'].iloc[:minlen].values > lim_threshold).astype(int)
    return df

def train():
    df = load_data(lim_threshold=1000)
    X = df[['precip_1w_lag','precip_2w_lag','precip_3w_lag']]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))
    joblib.dump(clf, MODELS / "rf_precip_adema.joblib")
    print("Modelo salvo em models/rf_precip_adema.joblib")

if __name__ == "__main__":
    train()