# src/parse_adema_pdf.py
import pdfplumber
import re
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "data" / "raw"  # ajustado para o caminho correto
PROC = ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

PDF = RAW / "nov18praias-14-11-18.pdf"  # corrigido nome do arquivo

def parse_pdf(pdf_path: Path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        # Extrair todo o texto primeiro
        full_text = ""
        for page in pdf.pages:
            if page.extract_text():
                full_text += page.extract_text() + "\n"
        
        # Pré-processar o texto para juntar linhas quebradas
        lines = []
        current_line = ""
        for line in full_text.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # Se a linha começa com um código conhecido e tem 5 números no final, é uma linha completa
            if re.match(r'^(?:AVS|S)\d+[MR]', line) and re.search(r'\d+(?:\s+\d+){4}$', line):
                if current_line:
                    lines.append(current_line)
                lines.append(line)
                current_line = ""
            # Se a linha começa com um código conhecido, é uma nova linha
            elif re.match(r'^(?:AVS|S)\d+[MR]', line):
                if current_line:
                    lines.append(current_line)
                current_line = line
            # Se a linha tem exatamente 5 números e temos uma linha atual, é o fim de uma entrada
            elif current_line and re.match(r'^\s*\d+(?:\s+\d+){4}\s*$', line):
                current_line += " " + line
                lines.append(current_line)
                current_line = ""
            # Se temos uma linha atual e a linha não tem números, é continuação
            elif current_line and not re.search(r'\d+', line):
                current_line += " " + line
        
        # Processar as linhas normalizadas
        print("\nLinhas normalizadas para debug:")
        for line in lines:
            print(f"Linha: {line}")
            # Regex melhorada para capturar o código e garantir 5 números no final
            m = re.search(r'((?:AVS|S)\d+[MR])\s+(.+?)\s+(\d+(?:\s+\d+){4})$', line)
            if m:
                code = m.group(1)
                name = m.group(2).strip()
                nums = m.group(3).strip().split()
                rows.append((code, name, nums))
                print(f"  Extraído: código={code}, valores={nums}")
            else:
                print("  Não extraído - não corresponde ao padrão esperado")
    # Transformar em DataFrame
    data = []
    for code, name, nums in rows:
        data.append({
            "code": code,
            "site": name,
            "values": ",".join(nums)
        })
    df = pd.DataFrame(data)
    out = PROC / "adema_aracaju_raw.csv"
    df.to_csv(out, index=False, encoding='utf-8')
    print(f"Saved {out}")
    return df

if __name__ == "__main__":
    df = parse_pdf(PDF)
    print(f"\nProcessamento concluído:")
    print(f"- Total de praias processadas: {len(df)}")
    print(f"- Colunas disponíveis: {', '.join(df.columns)}")
    print("\nPara análise detalhada dos dados, use o Jupyter Notebook/Lab")