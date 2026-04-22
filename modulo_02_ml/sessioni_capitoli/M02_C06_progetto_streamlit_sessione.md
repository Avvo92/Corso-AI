# Diario sessione — Capitolo 06 — Progetto Streamlit (primo deploy)

| Campo | Valore |
|-------|--------|
| **Modulo** | M02 — Machine Learning Fundamentals |
| **File capitolo** | `06_progetto_streamlit.py` |
| **File diario** | `M02_C06_progetto_streamlit_sessione.md` |
| **Stato** | in corso |

---

## Domande durante lo studio

- **Q:** Come organizzo il codice tra `modello_base.py` e `app_streamlit.py` senza duplicare logica?  
  **Nota / risposta sintetica:** La UI deve chiamare funzioni/oggetti “di servizio” e mostrare output; la logica ML resta in `modello_base.py` (o in piccole funzioni esportabili) per evitare copy-paste e incoerenze.

- **Q:** In demo, cosa mostro oltre a score/semaforo?  
  **Nota / risposta sintetica:** Almeno una metrica (recall sugli alterati) e una nozione di stabilità (CV media ± std) per non vendere un numero “da split fortunato”.

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-04-22 — Avvio cap.06: setup diario e deliverable

- **Esercizio / blocco:** creazione diario `M02_C06_progetto_streamlit_sessione.md` + definizione deliverable `app_streamlit.py`.
- **Punti di forza:** obiettivo chiaro: passare da script ML a demo usabile e deployabile.
- **Errori / lacune:** da monitorare in questo capitolo: scala `prob_alterato` (0–1) vs `score_genuinita` (0–100), recall vs precision, drop colonne reali (`pratica_id`, `y_alterato`).
- **Correzione / suggerimento:** in UI mostra sempre scale/unità e label esplicite; riusa `Pipeline` per CV (no leakage).
- **Pattern errore / ID contesto** (se applicabile): Lacune #16/#17/#18 (CONTESTO_CORSO.md), monitor Pattern #6 (consegne/DoD demo) e #22 (coerenza nomi/variabili).

### 2026-04-22 — Quiz d’ingresso (prime 2 domande)

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 1 (test una volta → produzione).
- **Valutazione finale:** **10/10** (dopo iterazioni).
- **Punti di forza:** hai distinto correttamente **drift** (dati che cambiano nel tempo) e **variabilità da split** (metrica che oscilla per composizione campione).
- **Micro-correzione linguistica:** “si usa la CV per stimare stabilità/variabilità” (la CV non “stabilizza” la metrica, la **stima**).

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 2 (formula recall).
- **Valutazione:** **10/10** (Recall = TP / (TP + FN), non precision).

### 2026-04-22 — Quiz d’ingresso, Domanda 3 (scale prob↔score)

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 3.
- **Valutazione:** **10/10**.
- **Note:** conversioni corrette: \(score=(1-prob)\cdot 100\). `prob_alterato=0.35 → score=65`; `score=70 → prob=0.30`.

### 2026-04-22 — Quiz d’ingresso, Domanda 4 (leakage intra-CV con scaler)

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 4.
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** hai spiegato che facendo `scaler.fit(X_train)` prima della CV, poi ogni fold vede dati già scalati con statistiche calcolate anche sui futuri validation fold → leakage; con `Pipeline` lo scaler fa `fit` solo sul train del fold.
- **Micro-miglioria:** dire “statistiche (media/dev std) calcolate su tutto `X_train`” (non solo dev std) per essere super-preciso.

### 2026-04-22 — Quiz d’ingresso, Domanda 5 (UI: media ± std CV)

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 5.
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** media = stima più robusta di un singolo split; std = misura della variabilità tra split (quanto “oscilla” la metrica).
- **Micro-miglioria:** esplicitare che “un singolo numero può essere fortunato/sfortunato” e che media±std comunica **stabilità/affidabilità** del modello.

### 2026-04-22 — Quiz d’ingresso, Domanda 6 (Feynman: train vs test)

- **Blocco:** `06_progetto_streamlit.py` — Quiz d’ingresso, Domanda 6.
- **Valutazione:** **8.5/10**.
- **Punti chiave corretti:** train = dati su cui il modello impara; test = dati mai visti per stimare la generalizzazione.
- **Micro-miglioria:** esplicitare la regola “il test si usa una volta” e che il confronto corretto è tra performance su train e su test (non “previsione sui dati train” in senso generico).

### 2026-04-22 — Rinforzo mirato Lacuna #16 (mini-esercizio scale)

- **Blocco:** `06_progetto_streamlit.py` — Rinforzo mirato Lacuna #16, mini-esercizio 1–3.
- **Valutazione:** **10/10**.
- **Note:** conversioni corrette (`prob=0.58 → score=42`; `score=55 → prob=0.45`) e hai identificato correttamente l’errore “score = 0.7” (scala sbagliata: lo score è 0–100).

### 2026-04-22 — Rinforzo mirato Lacuna #17 (drop colonne reali)

- **Blocco:** `06_progetto_streamlit.py` — Rinforzo mirato Lacuna #17, mini-esercizio.
- **Valutazione:** **10/10**.
- **Note:** corretta separazione feature/target usando colonne reali del dataset: `X = drop(["pratica_id","y_alterato"])`, `y = pratiche["y_alterato"]`.

### 2026-04-22 — Rinforzo mirato Lacuna #18 (precision vs recall + FP/FN)

- **Blocco:** `06_progetto_streamlit.py` — Rinforzo mirato Lacuna #18, mini-esercizio 1–2.
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** alzando la soglia aumenta tipicamente la precision e diminuisce il recall; in controllo documentale è più grave un **FN** (frode non intercettata) di un FP (falso allarme).
- **Micro-miglioria:** precisare “tipicamente” perché dipende da distribuzione e modello, ma la direzione è corretta nella maggior parte dei casi.

---

## Lacune e dubbi ancora aperti

- Scelte deploy: Streamlit Cloud (repo pubblico) e struttura file minima per renderlo ripetibile.

---

## Note per il capitolo successivo (mentor)

- Dopo il deploy, registrare l’URL nella tabella “Portfolio — Demo deployate per modulo” (CONTESTO_CORSO.md) quando M2 sarà chiuso.
