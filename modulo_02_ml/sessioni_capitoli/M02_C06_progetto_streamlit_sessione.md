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

### 2026-04-22 — Mini-esercizio 1.1 (requisiti UI finali)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 1.1 (descrivi cosa vuoi vedere in pagina).
- **Valutazione:** **8.5/10**.
- **Punti di forza:** obiettivo UI chiaro (titolo, select pratica, semaforo, score, motivi_top3) e coerente col prodotto.
- **Micro-miglioria:** aggiungere esplicitamente `prob_alterato (0–1)` e una sezione “stabilità” (CV media ± std) perché fanno parte del deliverable e ti aiutano a non confondere le scale.

### 2026-04-22 — Mini-esercizio 1.1 (revisione: requisiti UI finali + modalità esperimento)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 1.1 (revisione).
- **Valutazione:** **9.5/10**.
- **Punti di forza:** hai incluso stabilità (CV media±std), output per pratica (semaforo/score/motivi) e controlli sidebar per soglie/iperparametri.
- **Micro-miglioria:** aggiungere esplicitamente `prob_alterato (0–1)` tra le info della pratica selezionata (per chiarezza di scala).

### 2026-04-22 — Mini-esercizio 1.2 (rerun: variabili non persistono)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 1.2 (lista + append tra click).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** ad ogni interazione Streamlit riesegue il file dall’alto → `lista = []` viene ricreata e quindi non accumuli storico tra rerun.
- **Micro-miglioria:** aggiungere che per “memoria” tra rerun si usano `st.session_state` (stato) o cache (per risultati/dati), non variabili Python globali.

### 2026-04-22 — Mini-esercizio 1.3 (comando avvio Streamlit)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 1.3 (comando da lanciare).
- **Valutazione:** **10/10**.
- **Note:** comando corretto: `streamlit run modulo_02_ml/app_streamlit.py` (da root del repo con venv attivo).

### 2026-04-22 — Mini-esercizio 1.4 (troubleshooting: streamlit command not found)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 1.4.
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** attivare il venv e verificare install (`streamlit --version`) prima di “reinstallare tutto”.
- **Micro-miglioria:** prima di reinstallare Streamlit, provare `python -m streamlit --version` e/o `pip install -r requirements.txt` (così riallinei tutte le dipendenze del progetto nel venv).

### 2026-04-22 — Mini-esercizio 2.1 (title + header + dict)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 2.1.
- **Valutazione:** **8.5/10**.
- **Punti chiave corretti:** hai mostrato titolo, header e hai stampato un dict (derivato dal DataFrame).
- **Micro-miglioria:** la consegna chiedeva “3 righe”: qui hai aggiunto import + lettura CSV (ok come extra), ma in app reale la lettura andrebbe messa in funzione cached (`@st.cache_data`). Inoltre `to_dict()` di un DataFrame produce una struttura annidata; per un dict più “leggibile” meglio `pratiche.head(1).to_dict(orient="records")[0]`.

### 2026-04-22 — Mini-esercizio 2.1 (revisione: cache + orient=\"records\")

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 2.1 (revisione).
- **Valutazione:** **10/10**.
- **Punti di forza:** lettura CSV spostata in funzione `@st.cache_data` (no reload ad ogni rerun) e `to_dict(orient="records")[0]` produce un dict riga→valori molto più leggibile.

### 2026-04-22 — Mini-esercizio 2.2 (sidebar + select binario + colonne)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 2.2 (righe ~312–318).
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** `with st.sidebar:` con header + select a 2 opzioni; fuori dalla sidebar `st.columns(2)` con due `st.write` distinti nelle colonne.
- **Micro-miglioria:** assegnare il valore del selectbox a una variabile (es. `scelta = st.selectbox(...)`) e poi usarlo in `st.write` per vedere subito l’effetto del rerun; opzionale: `st.set_page_config(layout="wide")` per rendere più evidente l’affiancamento su schermi stretti.

### 2026-04-23 — Mini-esercizio 2.3 (input + mostra valori correnti)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 2.3 (righe ~337–345).
- **Valutazione:** **8/10**.
- **Punti chiave corretti:** selectbox + checkbox + slider impostati bene; stai mostrando i valori correnti in pagina (quindi capisci il “rerun-aware”).
- **Micro-miglioria (aderenza consegna):** la consegna chiedeva 1 riga con `st.write(...)` per stampare i valori; tu hai usato `st.metric` (ok, ma diverso). Inoltre `a, b, c = st.metric(...)` è inutile: `st.metric` serve solo per renderizzare, non per assegnare valori.

### 2026-04-23 — Mini-esercizio 2.4 (metric + warning)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 2.4 (righe ~418–425).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** hai usato `st.metric("score_genuinita", 82.5)` e `st.warning("Soglia in revisione")` esattamente come richiesto; output in pagina coerente (card + riquadro giallo).

### 2026-04-23 — Mini-esercizio 3.1 (quale cache per CV array)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 3.1 (righe ~463–467).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** scelta corretta `@st.cache_data` perché l’output è un dato (array di score) e non una risorsa “viva” come un modello/connessione.
- **Micro-miglioria:** specificare che è deterministico *a parità di input* (dati + seed/parametri) — se cambiano, la cache deve invalidarsi.

### 2026-04-23 — Mini-esercizio 3.2 (cache_resource + variabili globali)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 3.2 (righe ~482–486).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** hai capito che la cache decide se ricalcolare guardando gli argomenti; se i dati/parametri stanno in globali, Streamlit può non accorgersi del cambiamento e restituire un modello “vecchio”.
- **Micro-miglioria:** oltre a `X_train,y_train`, stesso discorso per iperparametri (`C`, seed, ecc.): vanno passati come argomenti per invalidare correttamente la cache.

### 2026-04-23 — Mini-esercizio 4.1 (path deploy-safe dopo spostamento file)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 4.1 (righe ~517–522).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** spostando `app_streamlit.py` in `ui/`, per raggiungere `modulo_02_ml/dati/...` devi risalire di 1 livello (`dirname(dirname(__file__))`) e poi fare `os.path.join(..., "dati", "pratiche_genuinita_mock.csv")`.

### 2026-04-23 — Mini-esercizio 5.1 (confine UI vs ML)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 5.1 (righe ~548–554).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** (2) UI, (3) ML, (4) UI, (5) ML.
- **Nota di fino:** (1) “score_genuinita da prob_alterato” è più correttamente **logica di prodotto/policy** (può stare in ML/servizi condivisi), mentre la UI dovrebbe solo mostrarlo. La tua risposta “ML” è accettabile se intendi “logica non-UI”.

### 2026-04-23 — Mini-esercizio 6.1 (predict_proba su UNA pratica)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 6.1 (righe ~586–591).
- **Valutazione:** **4/10**.
- **Errori principali:** 1) usi `df` ma non è definito nel frammento (nel capitolo si chiama spesso `pratiche`); 2) calcoli `X_one` ma poi chiami `predict_proba(X)` (variabile sbagliata); 3) `predict_proba(...)[0]` restituisce un array di 2 probabilità (classe 0 e 1), non un singolo numero — per `prob_alterato` serve `[0, 1]`; 4) `X_one` dovrebbe contenere solo le feature (droppare `pratica_id` e `y_alterato`) per essere compatibile col `pipe`.\n+- **Schema corretto (concetto):** filtra la riga → droppa colonne non-feature → `prob_alterato = pipe.predict_proba(X_una)[0, 1]`.\n 
### 2026-04-23 — Mini-esercizio 6.1 (nuovo tentativo: struttura 2 righe)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 6.1 (nuovo tentativo).
- **Valutazione:** **7/10**.
- **Punti chiave corretti:** filtri per `pratica_id` e prendi `predict_proba(...)[0, 1]` (estrai la proba della classe 1).
- **Errore strutturale rimasto:** `df.loc[...].drop(['pratica_id','target'])` senza `columns=` (o `axis=1`) tenta di droppare RIGHE/etichette, non colonne. Va scritto `drop(columns=[...])`. Inoltre nel nostro dataset il target è `y_alterato` (non `target`).

### 2026-04-23 — Mini-esercizio 6.1 (nuovo tentativo: drop columns + proba[0,1])

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 6.1 (nuovo tentativo).
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** `drop(columns=[...])` ora è corretto (stai passando solo feature) e `predict_proba(...)[0, 1]` estrae la probabilità della classe 1.
- **Micro-miglioria:** nel dataset del corso il target è `y_alterato` (non `target`), quindi la drop corretta è `drop(columns=["pratica_id","y_alterato"])`.

---

## Lacune e dubbi ancora aperti

- Scelte deploy: Streamlit Cloud (repo pubblico) e struttura file minima per renderlo ripetibile.

---

## Note per il capitolo successivo (mentor)

- Dopo il deploy, registrare l’URL nella tabella “Portfolio — Demo deployate per modulo” (CONTESTO_CORSO.md) quando M2 sarà chiuso.
