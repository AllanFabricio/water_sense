# 💧 Water Sense

**Water Sense** é um projeto de análise e modelagem preditiva voltado para o monitoramento da **qualidade da água das praias de Aracaju (SE)**, a partir da correlação entre **índices de precipitação horária** e **dados de balneabilidade**.

---

## 🧩 Objetivo

O projeto busca integrar e analisar dados ambientais provenientes de fontes públicas, com o propósito de **avaliar como a chuva influencia a balneabilidade das praias**.  
A meta é estabelecer uma base estruturada que permita desenvolver **modelos preditivos** capazes de antecipar condições impróprias para banho com base em dados meteorológicos.

---

## 📊 Fontes de Dados

| Origem | Descrição | Frequência | Formato |
|--------|------------|-------------|----------|
| **INMET** (Instituto Nacional de Meteorologia) | Dados horários de precipitação, temperatura, umidade, vento e radiação solar da estação A409 (Aracaju/SE) | Horária | `.CSV` |
| **ADEMA** (Administração Estadual do Meio Ambiente - SE) | Relatórios semanais de balneabilidade das praias de Aracaju | Semanal | `.PDF` |

---

## 🧰 Tecnologias Utilizadas

- **Python 3.11+**
- **Pandas** – Manipulação e análise de dados
- **pdfplumber** – Extração de texto de relatórios PDF da ADEMA  
- **PyArrow** – Leitura e gravação de arquivos Parquet  
- **Matplotlib** – Visualização de séries temporais  
- **JupyterLab** – Ambiente interativo de análise

---

## 🚀 Fluxo de Trabalho

1. **Coleta dos dados brutos**
   - INMET: Precipitação horária (arquivo `.CSV`)
   - ADEMA: Relatório semanal de balneabilidade (arquivo `.PDF`)
2. **Processamento**
   - Conversão, limpeza e padronização com os scripts em `src/`
3. **Exploração e integração**
   - Consolidação semanal e análise no notebook `01_exploracao_eda.ipynb`
4. **Modelagem preditiva** *(em desenvolvimento)*
   - Criação de modelos que relacionam chuva e qualidade da água

---

## 👨‍💻 Autor

**Allan Fabrício**  
Projeto desenvolvido como parte de um estudo de análise e modelagem de dados ambientais, integrando meteorologia e qualidade da água em Sergipe.

---

## 📝 Licença

Este projeto é distribuído sob a licença **MIT**, permitindo uso e modificação livre, desde que preservadas as devidas referências.

---

> _“Analisar o ambiente é o primeiro passo para preservá-lo.”_ 🌱
