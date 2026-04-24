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
- **Errori principali:** 1) usi `df` ma non è definito nel frammento (nel capitolo si chiama spesso `pratiche`); 2) calcoli `X_one` ma poi chiami `predict_proba(X)` (variabile sbagliata); 3) `predict_proba(...)[0]` restituisce un array di 2 probabilità (classe 0 e 1), non un singolo numero — per `prob_alterato` serve `[0, 1]`; 4) `X_one` dovrebbe contenere solo le feature (droppare `pratica_id` e `y_alterato`) per essere compatibile col `pipe`.
- **Schema corretto (concetto):** filtra la riga → droppa colonne non-feature → `prob_alterato = pipe.predict_proba(X_una)[0, 1]`.

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

### 2026-04-24 — Mini-esercizio 6.2 (prob → score → semaforo)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 6.2 (righe ~609–611).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** `prob_alterato=0.42` → `score_genuinita=(1-0.42)*100=58` → sotto soglia giallo (60) → semaforo **rosso** (ramo `else`).

### 2026-04-24 — Mini-esercizio 7.1 (coef_: top3 per |peso| + segno)

- **Blocco:** `06_progetto_streamlit.py` — Mini-esercizio 7.1 (righe ~636–639).
- **Valutazione (primo tentativo — “voto esame”):** **4/10**.
- **Errori principali:**
  - (1) top3 per \(|peso|\): includevi `0.3` ma \(|-0.6|=0.6\) è più grande → i top3 corretti sono \(0.8, -0.6, 0.3\) (feature `a`, `d`, `c`).
  - (2) segno invertito: secondo la teoria del capitolo, `coef < 0` spinge verso **classe 0 (genuino)**, non verso alterato.

### 2026-04-24 — Mini-esercizio 7.1 (correzione applicata)

- **Esito correzione:** ora corretto.
- **Fix chiave:** (1) top3 per \(|peso|\) = `[0.8, 0.6, 0.3]`; (2) “spinge verso alterato” = `0.8` (coefficiente positivo).

### 2026-04-24 — App “da zero” STEP 1 (carica_pratiche)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 1 `carica_pratiche`.
- **Valutazione (primo tentativo — “voto esame”):** **7/10**.
- **Punti ok:** usi `pd.read_csv(...)` e ritorni un `DataFrame`.
- **Da correggere:** 1) la funzione deve usare l’argomento `csv_path` (non `CSV_PATH` globale); 2) rimuovere il `raise NotImplementedError` rimasto sotto al `return` (è codice morto ma confonde).
- **Fix applicato:** ora usi `pd.read_csv(csv_path)` e la funzione termina con `return` (nessun `NotImplementedError` residuo).

### 2026-04-24 — App “da zero” STEP 2 (split_X_y)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 2 `split_X_y`.
- **Valutazione (primo tentativo — “voto esame”):** **6/10**.
- **Punti ok:** concetto giusto: `y = pratiche["y_alterato"]` e `X` senza `pratica_id`/target.
- **Errore bloccante:** hai scritto `drop(colums=...)` (typo). Deve essere `drop(columns=...)` altrimenti l’app va in errore.

### 2026-04-24 — App “da zero” STEP 2 (split_X_y) — rivalutazione su nuovo tentativo

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 2 `split_X_y` (nuovo tentativo).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** `X = drop(columns=["pratica_id","y_alterato"])` e `y = pratiche["y_alterato"]` (shape e colonne coerenti per training).

### 2026-04-24 — App “da zero” STEP 3a (allena_pipe_cached)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3a `allena_pipe_cached`.
- **Valutazione (primo tentativo — “voto esame”):** **8.5/10**.
- **Punti ok:** pipeline corretta (`StandardScaler` → `LogisticRegression`), usi `C`, `max_iter`, `random_state`, fai `fit` e ritorni il `pipe`.
- **Nota integrazione:** assicurati che la chiamata passi anche `max_iter` (era facile dimenticarlo). Ora in UI c’è lo slider e la chiamata è coerente.

### 2026-04-24 — App “da zero” STEP 3b (cv_recall_cached)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3b `cv_recall_cached`.
- **Valutazione (primo tentativo — “voto esame”):** **6.5/10**.
- **Punti ok:** usi `StratifiedKFold(n_splits=5, shuffle=True, random_state=...)` e `cross_val_score` restituisce un array di score (uno per fold).
- **Da correggere (2 cose):**
  - parametro sbagliato: `cross_val_score(..., scoring="recall")` (non `score="recall"`).
  - per CV non dovresti passare una pipeline *già fit* (la tua `allena_pipe_cached` fa fit). In CV è meglio creare una pipeline “vuota” (non fit) e lasciare che `cross_val_score` faccia il fit in ogni fold.

### 2026-04-24 — App “da zero” STEP 3b (cv_recall_cached) — nuovo tentativo

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3b `cv_recall_cached` (nuovo tentativo).
- **Valutazione:** **8.5/10**.
- **Punti chiave corretti:** ora usi `scoring="recall"` e passi a `cross_val_score` una pipeline NON fit (quindi ogni fold fa `fit` sul proprio train).
- **Micro-errore rimasto:** nello step `("scaler", StandardScaler)` manca `()` → deve essere `StandardScaler()` (altrimenti scikit-learn non riceve un transformer istanziato).

### 2026-04-24 — App “da zero” STEP 3b (cv_recall_cached) — rivalutazione finale

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3b `cv_recall_cached` (fix `StandardScaler()`).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** CV stratificata sul train, pipeline non fit dentro `cross_val_score`, `scoring="recall"`, output = array score per fold.

### 2026-04-24 — App “da zero” STEP 4a (X_una_pratica_da_id)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 4a `X_una_pratica_da_id`.
- **Valutazione (primo tentativo — “voto esame”):** **6/10**.
- **Punti ok:** filtro per `pratica_id` con `.loc[...]` e drop di `["pratica_id","y_alterato"]` (colonne giuste).
- **Errore tecnico:** dopo il `drop(...)` hai già un `DataFrame` 2D (1×N se la selezione è singola). `to_frame().T` qui è sbagliato perché `to_frame()` è un metodo della **Series**, non del DataFrame.

### 2026-04-24 — App “da zero” STEP 4b (prob_alterato_da_pipe)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 4b `prob_alterato_da_pipe`.
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** usi `predict_proba(X_una)[0, 1]` (classe 1 = alterato) e ritorni un `float` (valore 0–1).

### 2026-04-24 — App “da zero” STEP 5 (motivi_top3) — primo tentativo

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 5 `motivi_top3`.
- **Valutazione (primo tentativo — “voto esame”):** **6/10**.
- **Punti ok:** recuperi `scaler/model`, calcoli `x_scaled = scaler.transform(X_una)[0]`, prendi `coef = model.coef_[0]`, costruisci `contrib = x_scaled * coef` e lo metti in una `Series` con index = nomi feature.
- **Da correggere (2 cose):**
  - `X_una.columns()` non è corretto: è una proprietà → usare `X_una.columns.tolist()`.
  - `contrib_series.abs().sort_values(...)` ordina ma ti lascia i valori **assoluti** (perdi il segno). Meglio `sort_values(key=lambda s: s.abs(), ...)` così ordini per abs ma mantieni i contributi con segno.

### 2026-04-24 — App “da zero” STEP 0 (import)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 0 import (righe ~116–130).
- **Valutazione (primo tentativo — “voto esame”):** **8/10**.
- **Punti ok:** importi tutto il necessario per path (`os`), UI (`streamlit`), dati (`pandas`) e ML (Pipeline, scaler, LogReg, split, CV, metriche).
- **Micro-migliorie:** `numpy` di solito si importa come `import numpy as np` (più comodo per `np.mean/np.std`), e assicurati che nel codice sotto tu usi coerentemente `numpy` o `np` (uno solo).

### 2026-04-24 — App “da zero” STEP 0.1 (config pagina)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 0.1 `st.set_page_config(...)` (righe ~134–148).
- **Valutazione (primo tentativo — “voto esame”):** **9.5/10**.
- **Punti ok:** `page_title` + `layout="wide"` corretti; motivazione sensata (più spazio per colonne/elementi).
- **Micro-miglioria:** ricordati che deve stare *prima* di qualsiasi altro comando Streamlit che renderizza in pagina (title/write/metric). Qui è nel punto giusto del percorso.

### 2026-04-24 — App “da zero” STEP 0.2 (path deploy-safe) — check domanda

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 0.2 domanda “perché path assoluti sono un problema in deploy?” (righe ~141–156).
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** hai detto che i path assoluti dipendono dalla macchina (directory diverse) → in deploy la risorsa non viene trovata e l’app fallisce. È esattamente il motivo pratico.

### 2026-04-24 — App “da zero” STEP 0.2 (path deploy-safe) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 0.2 definizione `FILE_PATH` + `CSV_PATH` (righe ~160–161).
- **Valutazione (primo tentativo — “voto esame”):** **9.5/10**.
- **Punti ok:** path relativo a `__file__` + `os.path.join(...)` → deploy-safe e cross-OS; `CSV_PATH` punta correttamente a `dati/pratiche_genuinita_mock.csv`.
- **Micro-miglioria:** puoi rendere esplicito l’assoluto con `os.path.abspath(__file__)` (o `os.path.dirname(os.path.abspath(__file__))`) per evitare edge case se `__file__` non è già normalizzato; naming più leggibile tipo `HERE`/`DATA_DIR` aiuta, ma non è obbligatorio.

### 2026-04-24 — App “da zero” STEP 1 (carica_pratiche)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 1 `carica_pratiche` (righe ~170–172).
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** usi `@st.cache_data`, la funzione legge con `pd.read_csv(csv_path)` e ritorna un `DataFrame` usando l’argomento (riusabile/testabile).
- **Micro-miglioria (stile):** aggiungere l’annotazione del tipo anche al parametro (`csv_path: str`) rende la firma più chiara, ma non è necessario.

### 2026-04-24 — Ripasso (drop vs drop(columns=...))

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda ripasso su `drop(["a","b"])` vs `drop(columns=["a","b"])`.
- **Valutazione (primo tentativo — “voto esame”):** **6.5/10**.
- **Punto giusto:** hai intuito che cambia l’oggetto e l’asse (Series vs DataFrame/colonne).
- **Correzione precisa:** su DataFrame, `drop(["a","b"])` prova a droppare ETICHETTE di riga (axis=0) per default; per droppare colonne serve `drop(columns=["a","b"])` (o `drop(["a","b"], axis=1)`). Su Series, `drop([...])` rimuove etichette dell’indice (non “colonne”, perché non esistono).
- **Fix applicato:** nuova formulazione corretta: su Series `drop([...])` elimina etichette dell’indice; su DataFrame `drop([...])` tenta di eliminare etichette di riga (default axis=0), mentre `drop(columns=[...])` elimina colonne.

### 2026-04-24 — Ripasso (cache argomenti + Pipeline vs leakage)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domande ripasso su cache e Pipeline (righe ~203–208).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti ok:** (1) hai centrato il motivo tipico: se `C` non è un argomento della funzione cached (o non entra nella chiave), Streamlit può riusare la cache “vecchia”; (2) hai collegato Pipeline al rischio leakage (fit dello scaler solo su train / dentro fold in CV).
- **Micro-miglioria:** nella (2) esplicita “in CV ogni fold deve fittare scaler+modello sul proprio train” (è il punto più “da colloquio”). 

### 2026-04-24 — App “da zero” STEP 3a (allena_pipe_cached) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3a `allena_pipe_cached` (righe ~212–226).
- **Valutazione (primo tentativo — “voto esame”):** **9.5/10**.
- **Punti chiave corretti:** `@st.cache_resource` appropriato per il modello; Pipeline con `StandardScaler()` prima e `LogisticRegression(C, max_iter, random_state)`; fai `fit` su `(X_train, y_train)` e ritorni l’oggetto addestrato.
- **Micro-migliorie:** 1) aggiungere type hints (`X_train: pd.DataFrame`, `y_train: pd.Series`, `C: float`, `max_iter: int`, `random_state: int`) aumenta chiarezza; 2) stile firma: metti ogni parametro su una riga per leggibilità.

### 2026-04-24 — App “da zero” STEP 3a (allena_pipe_cached) — fix type hints

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3a `allena_pipe_cached` (aggiunti type hints).
- **Esito fix:** applicato (firma più chiara, nessun impatto negativo su runtime).

### 2026-04-24 — App “da zero” STEP 2 (split_X_y) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 2 `split_X_y` (righe ~182–186).
- **Valutazione (primo tentativo — “voto esame”):** **8.5/10**.
- **Punti chiave corretti:** `X = drop(columns=["pratica_id","y_alterato"])`, `y = pratiche["y_alterato"]`, ritorni `(X, y)` con oggetti giusti (DataFrame + Series).
- **Micro-errori (type hints):** `pd.Dataframe` è scritto male → `pd.DataFrame`; meglio tipizzare il return come `tuple[pd.DataFrame, pd.Series]` (o `tuple[...]` in Python 3.9+). Il decorator `@st.cache_data` qui è ok ma non indispensabile.
- **Fix applicato:** return type aggiornato a `tuple[pd.DataFrame, pd.Series]` (corretto).

### 2026-04-24 — Ripasso (cross_val_score output)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda “cosa restituisce cross_val_score?” (righe ~220–222).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punto giusto:** corretto che restituisce un array NumPy di score.
- **Micro-miglioria:** specifica “uno score per fold” (es. con 5 fold → array di 5 numeri). 

### 2026-04-24 — App “da zero” STEP 3b (cv_recall_cached) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 3b `cv_recall_cached` (righe ~223–239).
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** pipeline “fresca” non fit passata a `cross_val_score`; `StratifiedKFold(5, shuffle=True, random_state=...)`; `scoring="recall"`; output = array score per fold; `@st.cache_data` coerente (stai cachando un dato).
- **Micro-miglioria (opzionale):** puoi parametrizzare `max_iter` (coerenza con slider) e aggiungere type hints ai parametri per leggibilità.

---

## Lacune e dubbi ancora aperti

- Scelte deploy: Streamlit Cloud (repo pubblico) e struttura file minima per renderlo ripetibile.

---

## Note per il capitolo successivo (mentor)

- Dopo il deploy, registrare l’URL nella tabella “Portfolio — Demo deployate per modulo” (CONTESTO_CORSO.md) quando M2 sarà chiuso.
