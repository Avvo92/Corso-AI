# Archivio Modulo 02 — Machine Learning Fundamentals

> Dettaglio storico del Modulo 2 (7 capitoli, ~marzo–aprile 2026).
> Migrato da `CONTESTO_CORSO.md` il **20/05/2026** (Passo 13).
>
> **Regola**: per rinforzi su ML classico, Streamlit deploy, `modello_base.py`, consultare questo file.
> **Codice**: `modulo_02_ml/` · **Diari**: `modulo_02_ml/sessioni_capitoli/`

---

## Riepilogo

| Campo | Valore |
|-------|--------|
| Capitoli | 7/7 completati |
| Periodo | ~25/03/2026 – 27/04/2026 |
| Media difficoltà | **~6.4** (voti: 6, 5, 6, 7, 8, 7, 6) |
| Demo portfolio | [Streamlit Cloud LIVE](https://appappdazeropy-g5tde3wvxdewl5arzmeq2j.streamlit.app/) |
| Deliverable progressivo | `modulo_02_ml/modello_base.py` (ownership studente) |
| App demo | `modulo_02_ml/app_streamlit_da_zero.py` |

---

## Progresso per capitolo

| File | Voto (1–10) | Note sintetiche |
|------|-------------|-----------------|
| `01_cos_e_il_ml.py` | 6 | Framework ML, X/y, leakage, pipeline prodotto; media esercizi ~9.1/10 |
| `02_ciclo_ml.py` | 5 | Ciclo train/test, DecisionTree, metriche regressione; `modello_base` anti-baseline |
| `03_regressione.py` | 6 | LinearRegression, StandardScaler, `motivi_top_n` |
| `04_classificazione_metriche.py` | 7 | Classificazione, recall, semaforo, sezione classificazione in `modello_base` |
| `05_overfitting_validazione.py` | 8 | CV StratifiedKFold, Pipeline anti-leakage in CV |
| `06_progetto_streamlit.py` | 7 | Streamlit, cache, predict_proba 2D, motivi_top3 con segno |
| `07_deploy_streamlit_cloud.py` | 6 | requirements, deploy cloud, primo URL portfolio |

---

## Componente pipeline prodotto (M2)

- Classificatore supervisionato vero/alterato + anomaly detection
- Output: `score_genuinita`, `prob_alterato`, `anomaly_score`, `semaforo`, `motivi_top3`
- Regola 38: primo deploy anticipato (Streamlit Cloud) — **completato**

---

## Domande per capitolo (storico)

Vedi sezioni complete migrate da contesto — capitoli: 01 (12 domande), 02 (2), 03 (2), 04 (2), 06 (8), 07 (4).

**Temi ricorrenti**: `value_counts`, train/validation/test, recall nel documentale, `cross_val_score`, `predict` vs `predict_proba`, deploy locale vs cloud, FN = alterato classificato genuino.

---

## Competenze acquisite (sintesi)

- **ML workflow**: supervised/unsupervised, feature/target, leakage, baseline, metriche P/R/F1, CV su train only
- **Modelli**: `DecisionTree*`, `LogisticRegression`, `Pipeline(StandardScaler + …)`
- **Streamlit**: widget, cache_data/cache_resource, policy semaforo sopra al modello
- **Deploy**: path deploy-safe, `requirements.txt`, smoke test cloud
- **Prodotto**: terminologia pipeline consolidata; demo end-to-end su pratiche mock

Dettaglio esteso per capitolo era in `CONTESTO_CORSO.md` sezioni Cap.01–07 M2 (migrato 20/05/2026).

---

## Pattern di errore — storico M2

| # | Pattern | Esito in chiusura M2 |
|---|---------|----------------------|
| 6 | Lettura incompleta consegne | 🟡 portato a M3 |
| 18 | Series vs DataFrame | 🟡 rinforzato, quiz ok |
| 19 | `if var:` vs `is not None` | 🟡 |
| 20 | Anti-pattern valutazione vs feature prep | 🟡 |
| 21 | Tupla `(x, n)` vs `round(x, n)` | 🟡 |
| 22 | Riutilizzo variabili tra esercizi nello stesso file | 🟡 nuovo in M2 |

---

## Lacune quiz — chiuse in M2 (🟢)

#12 shape (assorbita anche dal Ponte), #13–#18 varie su Pandas/ML — vedi tabella lacune storica in changelog CONTESTO 13/04–27/04.

---

## Diari sessione

| Capitolo | File diario |
|----------|-------------|
| 04 | `M02_C04_classificazione_metriche_sessione.md` |
| 05 | `M02_C05_overfitting_validazione_sessione.md` |
| 06 | `M02_C06_progetto_streamlit_sessione.md` |
| 07 | `M02_C07_deploy_streamlit_cloud_sessione.md` |

---

## Decision log archivio

| Data | Nota |
|------|------|
| 20/05/2026 | Creato archivio; Passo 13 eseguito in ritardo (studente già in M3). |
