# MODULO 2 — Machine Learning Fundamentals

## Obiettivo del Modulo

In questo modulo passi da "analisi dati" a "modello che impara dai dati".
In pratica: non ti limiti a leggere pattern, ma costruisci un sistema che
fa previsioni su dati nuovi.

Ponte mentale:
- Modulo 1 = prepari e organizzi i dati
- Modulo 2 = insegni al modello a usare quei dati

---

## Cosa Imparerai

| # | File | Argomento | Output pratico |
|---|------|-----------|----------------|
| 01 | `01_cos_e_il_ml.py` | Cos'e il Machine Learning, tipi e casi d'uso | Framework mentale solido |
| 02 | `02_ciclo_ml.py` | Pipeline completa: dati -> train -> evaluate | Workflow riusabile |
| 03 | `03_regressione.py` | Regressione lineare e alberi decisionali | Primo modello predittivo |
| 04 | `04_classificazione_metriche.py` | Classificazione, accuracy/precision/recall/F1 | Valutazione corretta modelli |
| 05 | `05_overfitting_validazione.py` | Overfitting, train/val/test, CV, bias-varianza, **validation curve** (tabella + grafico opzionale), caveat dataset piccolo | Modelli piu robusti; progetto incrementale = CV su `modello_base.py` (lo scrivi tu) |
| 06 | `06_progetto_streamlit.py` | Mini-progetto deployabile | Demo portfolio #1 |

Librerie principali del modulo:
- `scikit-learn`
- `streamlit`

Dataset mock (pratiche di genuinità):
- `dati/pratiche_genuinita_mock.csv` — circa **640 righe**; include **casi limite** (genuini ambigui, alterati lievi) e un **piccolo rumore sulle etichette** (~3%) per avvicinarsi a dati reali (errori di revisione). Distribuzione classi variabile dopo il rumore.
- Rigenerazione (solo libreria standard, seed 42): `python dati/genera_pratiche_genuinita_mock.py` dalla cartella `modulo_02_ml` o da `dati/`.

---

## Diario sessione per capitolo

File Markdown opzionali in `sessioni_capitoli/` — una traccia persistente di domande e correzioni durante ogni capitolo; usata in chiusura con `CONTESTO_CORSO.md`. Dettagli in `sessioni_capitoli/README.md` e **Regola 39** / sezione **J** in `CONTESTO_CORSO.md`.

---

## Setup Quando Inizi Davvero il Modulo

Nel file `requirements.txt` della root, scommenta:
- `scikit-learn`
- `streamlit`

Poi installa:

```bash
pip install -r requirements.txt
```

---

## Come Studiare il Modulo

Per ogni file:
1. Fai il quiz d'ingresso
2. Leggi teoria + completa mini-esercizi
3. Fai il quiz di verifica
4. Completa esercizi pratici (inclusi tag colloquio/debug/refactoring)
5. Esegui il progetto incrementale
6. Correzione finale + voto difficolta (1-10)

---

## Deliverable del Modulo

Alla fine del Modulo 2 avrai:
- un modello di predizione prezzi case
- una demo Streamlit deployabile (portfolio)
- basi solide per affrontare Deep Learning nel Modulo 3

