# Diario sessione — Capitolo 06 — Progetto Streamlit (primo deploy)

| Campo | Valore |
|-------|--------|
| **Modulo** | M02 — Machine Learning Fundamentals |
| **File capitolo** | `06_progetto_streamlit.py` |
| **File diario** | `M02_C06_progetto_streamlit_sessione.md` |
| **Stato** | completato |

---

## Domande durante lo studio

- **Q:** Come organizzo il codice tra `modello_base.py` e `app_streamlit.py` senza duplicare logica?  
  **Nota / risposta sintetica:** La UI deve chiamare funzioni/oggetti “di servizio” e mostrare output; la logica ML resta in `modello_base.py` (o in piccole funzioni esportabili) per evitare copy-paste e incoerenze.

- **Q:** In demo, cosa mostro oltre a score/semaforo?  
  **Nota / risposta sintetica:** Almeno una metrica (recall sugli alterati) e una nozione di stabilità (CV media ± std) per non vendere un numero “da split fortunato”.

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-04-27 — Capitolo 07 (deploy) — Quiz d’ingresso Q1 (V/F locale vs cloud)

- **Blocco:** `modulo_02_ml/07_deploy_streamlit_cloud.py` — Quiz d’ingresso Q1.
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti chiave corretti:** hai detto “Falso” e hai elencato i principali motivi reali: path deploy-safe (no assoluti), dipendenze/requirements allineati, evitare dipendenze inutili.
- **Micro-miglioria:** aggiungi anche “differenze di ambiente” (versioni Python, file presenti, working directory e permessi): in cloud non hai il tuo filesystem locale.

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

### 2026-04-24 — Ripasso (shape: predict_proba su 1 pratica)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda “perché predict_proba si rompe con input 1D?” (righe ~241–243).
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** `predict_proba` si aspetta una matrice 2D (n_samples × n_features); anche per 1 sola pratica serve quindi shape `(1, n_feature)` (DataFrame 1 riga o array 2D).

### 2026-04-24 — App “da zero” STEP 4a (X_una_pratica_da_id) — implementazione robusta (parziale)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 4a `X_una_pratica_da_id` (righe ~245–251).
- **Valutazione (primo tentativo — “voto esame”):** **7.5/10**.
- **Punti ok:** filtro con `.loc[...]` e controlli robusti su numero righe (0 → errore, >1 → errore).
- **Cosa manca rispetto alle regole dello step:** devi ancora droppare le colonne non-feature (`"pratica_id"`, `"y_alterato"`) prima di ritornare, altrimenti `predict_proba` fallisce o usa feature sbagliate.

### 2026-04-24 — App “da zero” STEP 4a (X_una_pratica_da_id) — fix drop non-feature

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 4a `X_una_pratica_da_id` (fix: `drop(columns=["pratica_id","y_alterato"])`).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** controlli 0/>1 righe + ritorno DataFrame 2D 1×N con sole feature (compatibile con `predict_proba`).

### 2026-04-24 — App “da zero” STEP 4b (prob_alterato_da_pipe) — domanda + implementazione

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 4b (righe ~240–264).
- **Valutazione (primo tentativo — “voto esame”):** **9.5/10**.
- **Risposta domanda (predict vs predict_proba):** corretta: con `predict` perdi la probabilità (quindi perdi anche la possibilità di mostrare prob e di derivare score/semaforo in modo trasparente; e perdi la calibrazione/uncertainty percepita).
- **Codice:** `pipe.predict_proba(X_una)[0, 1]` corretto (classe 1 = alterato). Micro-miglioria: fare `return float(...)` per restituire un float Python pulito in UI.

### 2026-04-24 — Ripasso (scala prob↔score)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — ripasso conversioni prob↔score (righe ~261–263).
- **Valutazione (primo tentativo — “voto esame”):** **10/10**.
- **Punti chiave corretti:** `prob=0.3 → score=(1-0.3)*100=70`; `score=55 → prob=1-(55/100)=0.45` (nota: hai scritto 0.35, quindi qui va corretto a 0.45).

### 2026-04-24 — Ripasso (scala prob↔score) — correzione nota mentor

- **Nota:** nella entry precedente ho sbagliato a segnare il voto: con una risposta corretta e una errata il voto “primo tentativo” era **7/10** (non 10/10). Mantengo l’entry per storicità e registro qui la correzione.

### 2026-04-24 — App “da zero” STEP 5a (score_genuinita_da_prob) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 5a funzione conversione prob→score (righe ~266–267).
- **Valutazione (primo tentativo — “voto esame”):** **7.5/10**.
- **Punti ok:** formula corretta: `score = (1 - prob_alterato) * 100`, ritorni un `float`.
- **Da correggere:** nome funzione non coerente con la consegna (`score_genuinita_da_prob`): hai scritto `score_genuinita_sa_prov` → questo rompe le chiamate UI future. Aggiungi anche type hints sul parametro (`prob_alterato: float`).

### 2026-04-24 — App “da zero” STEP 5a (score_genuinita_da_prob) — fix parziale nome

- **Esito fix:** hai rinominato la funzione ma il nome è ancora non coerente con la consegna (`score_genuinita_a_prov` ≠ `score_genuinita_da_prob`). Formula ok, manca solo il naming finale.

### 2026-04-24 — App “da zero” STEP 5a (score_genuinita_da_prob) — fix naming finale

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 5a (nome funzione allineato alla consegna).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** nome coerente + formula corretta + ritorno float (scala 0–100).

### 2026-04-24 — Ripasso (policy semaforo: UI vs prodotto)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda “logica UI o prodotto?” (righe ~271–274).
- **Valutazione (primo tentativo — “voto esame”):** **8.5/10**.
- **Punto giusto:** sì, il semaforo è una **policy di prodotto** (regola decisionale sopra al modello), la UI idealmente la applica chiamando una funzione condivisa.
- **Micro-miglioria:** rispondi anche alla seconda domanda: se cambia la policy, la tocchi nella funzione/policy (non nel modello ML; e la UI dovrebbe solo riflettere la nuova regola).

### 2026-04-27 — App “da zero” STEP 5b (semaforo_da_score) — implementazione codice

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 5b `semaforo_da_score` (righe ~277–283).
- **Valutazione (primo tentativo — “voto esame”):** **7/10**.
- **Punti ok:** logica corretta e ordine giusto: prima verde, poi giallo, altrimenti rosso.
- **Errori da correggere:** 1) variabile: hai scritto `soglia_gialla` ma il parametro è `soglia_giallo` (NameError); 2) nella risposta “se cambia la policy la tocchi in UI” → meglio toccarla nella funzione di policy (logica prodotto) e farla solo usare dalla UI.

### 2026-04-27 — App “da zero” STEP 5b (semaforo_da_score) — fix NameError + concetto policy

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 5b `semaforo_da_score` (fix).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** nomi variabili coerenti (`soglia_giallo`), logica e ordine corretti, e concetto: policy si cambia nella funzione (logica prodotto) che la UI richiama.

### 2026-04-27 — Ripasso (perché contrib = x_scaled * coef)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda su perché usare `x_scaled` e non `X_una` grezzo per i contributi (righe ~311–312).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti chiave corretti:** hai centrato che con scaling le feature sono su scala comparabile (unità comuni), quindi moltiplicare per `coef` produce contributi confrontabili; senza scaling confronteresti grandezze con unità diverse (“mele e ananas”).
- **Micro-miglioria:** specifica che `coef_` è appreso sullo spazio standardizzato (quello che vede il modello nella Pipeline), quindi usare `x_scaled` rende il contributo coerente con ciò che il modello usa davvero.

### 2026-04-27 — Ripasso (perché “motivi top3” non sono CAUSA)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — domanda “se scrivi che sono la CAUSA, stai mentendo: perché?” (righe ~313–315).
- **Valutazione (primo tentativo — “voto esame”):** **7.5/10**.
- **Punti ok:** hai colto che top3 è una *semplificazione* (non spiega “tutta” la decisione) e che le altre feature sommate possono contare.
- **Cosa manca per essere “onesto” come nel cap.06:** il punto principale non è solo “mancano le altre feature”, ma che: 1) sono pesi di un modello su questi dati (cambiano se cambia dataset/modello), 2) non implicano causalità (correlazioni tra feature possono spostare i pesi), 3) sono spiegazione *del modello*, non “prova” nel mondo reale.

### 2026-04-27 — Ripasso (perché “motivi top3” non sono CAUSA) — nuovo tentativo

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — stesso ripasso (nuovo tentativo).
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** ora includi che top3 non spiega tutto, e che sono pesi del modello sui dati disponibili e possono cambiare cambiando dati/modello.
- **Micro-miglioria:** aggiungi esplicitamente “non è causalità” (feature correlate) per chiudere il disclaimer “da recruiter”.

### 2026-04-27 — App “da zero” STEP 6 (motivi_top3) — nuovo tentativo (contrib per pratica)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 6 `motivi_top3` (righe ~318–327).
- **Valutazione (primo tentativo — “voto esame”):** **7/10**.
- **Punti ok:** hai finalmente introdotto il passaggio giusto per “contributi per pratica”: `x_scaled = scaler.transform(X_una)[0]`, `coef = model.coef_[0]`, `contrib = x_scaled * coef`; costruisci una `Series` indicizzata con `X_una.columns` e ordini per valore assoluto mantenendo il segno.
- **Errori da correggere (bloccanti):**
  - `pipe.named_steps` è un dict, non una funzione: va indicizzato (`[...]`), non chiamato con `(...)`.
  - il return type richiesto è `list[tuple[str, float]]`, ma `to_list()` restituisce solo i VALORI (perdi i nomi feature). Serve restituire anche i nomi (tuples feature→contrib).
- **Micro-miglioria (scelta cache):** l’output qui è un dato (lista/serie), quindi `cache_data` è più coerente di `cache_resource`.

### 2026-04-27 — App “da zero” STEP 6 (motivi_top3) — fix named_steps + cache

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 6 `motivi_top3` (righe ~318–327).
- **Valutazione:** **9/10**.
- **Punti chiave corretti:** ora usi `@st.cache_data`; accesso corretto a `pipe.named_steps[...]`; contrib per pratica (`x_scaled * coef`) e top3 per valore assoluto mantenendo il segno.
- **Cosa manca per aderire alla firma:** stai ancora ritornando una `Series`, non una `list[tuple[str, float]]`. Devi convertire mantenendo nome-feature + valore (non solo valori).

### 2026-04-27 — App “da zero” STEP 6 (motivi_top3) — fix return list[tuple]

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — STEP 6 `motivi_top3` (fix conversione in `list[tuple[str,float]]`).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** usi `.items()` per iterare (feature, valore) e `append((k, float(v)))`; ritorni `tuple_list`.

### 2026-04-27 — UI 7.2 (sidebar → dict ui)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI sidebar con dict `ui` (righe ~397–439).
- **Valutazione (primo tentativo — “voto esame”):** **8/10**.
- **Punti ok:** `with st.sidebar:` corretto; hai separato elementi UI (header/divider) dai valori principali; raccogli parametri in `ui` (pulito per usarli dopo).
- **Da correggere:** 1) `st.divider(),` ha una virgola finale → crea una tupla inutile (meglio `st.divider()` senza virgola); 2) coerenza naming: chiave `ui["soglia_gialla"]` dovrebbe essere `ui["soglia_giallo"]` per allinearsi a funzioni/step (evita bug giallo/gialla).

### 2026-04-27 — UI 7.2 (sidebar → dict ui) — fix virgola + naming

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI sidebar (fix).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** `st.divider()` senza virgola; chiavi coerenti `soglia_verde`/`soglia_giallo`; `ui` contiene solo i parametri utili al resto dell’app.

### 2026-04-27 — UI 7.3 (carica dati + split + train_test_split)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.3 caricamento e split (righe ~438–442).
- **Valutazione (primo tentativo — “voto esame”):** **8.5/10**.
- **Punti ok:** chiami `carica_pratiche(CSV_PATH)`, poi `split_X_y(pratiche)`, poi `train_test_split(..., test_size=0.2, stratify=y)`; motivazione su `stratify` corretta (mantenere proporzioni classe in train/test).
- **Micro-miglioria:** usare `random_state=ui["random_state"]` (non un numero fisso 24) per coerenza con la sidebar e per rendere l’esperimento controllabile.

### 2026-04-27 — UI 7.3 (carica dati + split + train_test_split) — fix random_state da sidebar

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.3 (fix).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** ora usi `random_state=ui["random_state"]` coerente con la sidebar; split riproducibile e controllabile.

### 2026-04-27 — UI 7.4 (training + CV + stabilità in pagina)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.4 (righe ~449–466).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti ok:** alleni il `pipe` usando i parametri da sidebar; calcoli CV sul train e ottieni media+std; mostri in pagina due metriche + una frase di interpretazione (std = stabilità/oscillazione su split diversi).
- **Micro-migliorie:** 1) label più precisa (es. “CV Recall (media)” e “CV Recall (std)”, non “Media Std”); 2) cast esplicito dei tipi da UI (`float(ui["C"])`, `int(ui["max_iter"])`, `int(ui["random_state"])`) evita edge case; 3) la frase finale: “diverse formulazioni degli split/dati” (non “formulazione del dataset”).

### 2026-04-27 — UI 7.4 (training + CV + stabilità) — fix label + cast + frase

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.4 (fix).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** label chiare, cast espliciti dai widget, frase finale più precisa sugli split/composizione dati; output portfolio-ready (media ± std).

### 2026-04-27 — UI 7.5 (select pratica_id)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.5 selectbox pratica_id (righe ~465–468).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti ok:** `st.selectbox` su colonna `pratica_id` e salvi in variabile (ok).
- **Micro-miglioria:** passa una lista esplicita (`pratiche["pratica_id"].tolist()`) e/o ordina gli id per UX; se ti serve int garantito, fai cast `int(pratica_id)` (selectbox spesso restituisce numpy int).

### 2026-04-27 — UI 7.6 (output pratica: prob → score → semaforo + metriche)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.6 (righe ~481–494).
- **Valutazione (primo tentativo — “voto esame”):** **7.5/10**.
- **Punti ok:** pipeline logica corretta: `X_una` → `prob` → `score` → `semaforo`; cast soglie da sidebar; label mostrano chiaramente le scale (0–1 e 0–100).
- **Da correggere (layout colonne):** stai creando le colonne (`st.columns(4)`) ma poi usi `st.metric(...)` fuori dai container e sovrascrivi le variabili (`col_1 = st.metric(...)`). Risultato: le metriche non finiscono davvero nelle 4 colonne. Devi renderizzare *dentro* i container (con `with col_1: ...` oppure usando i metodi del container).
- **Micro-miglioria:** per lo score puoi mostrare anche il numero 0–100 “nudo” (es. `82.3`) oltre alla percentuale, per non confondere percentuale vs score.

### 2026-04-27 — UI 7.6 (output pratica) — fix layout colonne

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.6 (fix layout con `with col_x:`).
- **Valutazione:** **9.5/10**.
- **Punti chiave corretti:** ora le metriche finiscono davvero nelle 4 colonne e non sovrascrivi più i container.
- **Micro-miglioria:** la label “Score Genuinita => 0% - 100%” può confondere: lo score è 0–100 (numero), la percentuale è solo un formato; valuta mostrare `score` come 0–100.

### 2026-04-27 — UI 7.7 (motivi top3 + disclaimer + segno)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.7 rendering motivi top3 con segno (righe ~499–504).
- **Valutazione (primo tentativo — “voto esame”):** **9/10**.
- **Punti ok:** header + disclaimer presenti; stampi i top3 e mostri esplicitamente il segno (`{v:+.3f}`) e una direzione leggibile (“verso genuino/alterato”) coerente col segno.
- **Micro-miglioria:** il `:25s` può essere fragile (se `i` non è `str` puro). Più robusto: `f\"{str(i):<25}\"` o `f\"{str(i).upper():<25}\"`. Inoltre, se vuoi coerenza col capitolo 7.1, potresti chiarire che “verso alterato” significa “spinge verso classe 1” (non causa).

### 2026-04-27 — UI 7.8 (test finale: y_pred + recall_test)

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.8 calcolo recall su test (righe ~509–510).
- **Valutazione (primo tentativo — “voto esame”):** **8.5/10**.
- **Punti ok:** `y_pred_test = pipe.predict(X_test)` e `recall_score(y_test, y_pred_test)` corretti per calcolare recall sul test (classe alterata = 1).
- **Cosa manca per completare lo step UI:** devi ancora mostrare `recall_test` in pagina (es. `st.metric` o `st.write`) e aggiungere 1 riga sul perché il test si usa “una volta sola” (T12).

### 2026-04-27 — UI 7.8 (test finale) — completamento UI + nota

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — UI 7.8 (righe ~511–514).
- **Valutazione:** **10/10**.
- **Punti chiave corretti:** ora mostri `recall_test` in pagina (subheader + metric) e aggiungi una nota sul “test una volta” coerente con il capitolo.
- **Micro-miglioria (solo wording):** più che “imparziale”, la ragione è che il test è l’**arbitro finale** e non va “consumato” per scegliere/tarare decisioni; ma il senso è corretto.

### 2026-04-27 — Valutazione complessiva `app_streamlit_da_zero.py`

- **Blocco:** `modulo_02_ml/app_streamlit_da_zero.py` — demo completa + percorso didattico.
- **Valutazione complessiva:** **9/10**.
- **Punti forti:** flusso completo “portfolio-ready” (CV media±std, output pratica prob/score/semaforo, motivi_top3 con segno+disclaimer, recall su test); ottima coerenza con lacune (#16 scala, #17 drop colonne reali, #18 recall); funzioni ML separate dalla UI (buona architettura).
- **Criticità/micro-fix:** 1) rimuovere import inutile `from scipy.integrate._ivp.radau import C` (non serve e crea confusione con `C` di LogReg); 2) `semaforo_da_score` restituisce “Verde/Giallo/Rosso” (ma nelle istruzioni spesso era “verde/giallo/rosso”: uniforma per coerenza); 3) score in UI: stai mostrando `score/100` come 0–1, ma lo labelizzi 0–100 (meglio mostrare direttamente 0–100).

---

## Lacune e dubbi ancora aperti

- Scelte deploy: Streamlit Cloud (repo pubblico) e struttura file minima per renderlo ripetibile.

---

## Note per il capitolo successivo (mentor)

- Dopo il deploy, registrare l’URL nella tabella “Portfolio — Demo deployate per modulo” (CONTESTO_CORSO.md) quando M2 sarà chiuso.
