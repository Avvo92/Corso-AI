# Diario sessione — Capitolo 04 — Classificazione e metriche

| Campo | Valore |
|-------|--------|
| **Modulo** | M02 — Machine Learning Fundamentals |
| **File capitolo** | `04_classificazione_metriche.py` |
| **File diario** | `M02_C04_classificazione_metriche_sessione.md` |
| **Stato** | completato (chiusura 13/04/2026) |

---

## Domande durante lo studio

- _(da compilare durante la sessione)_

---

## Valutazioni esercizi / quiz / mini-esercizi

### 2026-04-09 — MINI-ESERCIZIO 4 (soglia, prob_alterato, score_genuinita, semaforo)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 519-535
- **Punti di forza**:
  - Ha colto bene l’idea di **threshold**: abbassando la soglia aumentano le predizioni “alterato” (classe 1) e tende a salire il **recall**.
  - Ha capito il rischio operativo di soglia troppo bassa: aumento dei falsi positivi → carico di revisione manuale → modello percepito “inutile”.
- **Correzioni / miglioramenti**:
  - Q1: “indeciso” va espresso in termini di **prob_alterato ~ 0.5** (non “60% score genuinità”). `score_genuinita = (1 - prob_alterato) * 100`, quindi score ~60% corrisponde a prob_alterato ~0.40 (zona medio-indecisa, ma non “vicino a 0.5”).
  - Q4: soglie semaforo non vanno fissate solo “a intuito”: in produzione si scelgono guardando trade-off precision/recall e costo degli errori (FN vs FP). Proposta iniziale ok come placeholder, ma motivarla con metriche a soglia variabile.
- **Note per rinforzo**:
  - Ponte mentale: soglia = compromesso **FN vs FP**; nel documentale FN è spesso più costoso → soglia più prudente (più recall) ma con gestione del carico (giallo/HITL).

### 2026-04-09 — QUIZ Verifica (Domanda 1: accuracy ≠ affidabilità)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 543-547
- **Esito**: corretto (V/F + esempio centrato)
- **Punti di forza**:
  - Ha identificato lo scenario classico: **dataset sbilanciato** (molti genuini, pochi alterati) → accuracy alta ma modello inutile sugli alterati.
  - Ha collegato la criticità al prodotto: recall sugli alterati può diventare 0.
- **Rifinitura “da colloquio”**:
  - Specificare che “accuracy 95%” può corrispondere al modello che **predice sempre ‘genuino’**.
  - Dire esplicitamente: in quel caso **recall(alterato)=0**, mentre accuracy resta alta perché la classe maggioritaria domina.

### 2026-04-09 — QUIZ Verifica (Domanda 2: metriche da confusion matrix)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 549-558
- **Esito**: calcoli corretti; solo piccola rifinitura di notazione
- **Punti di forza**:
  - Accuracy, recall e precision calcolate correttamente a partire da TN/FP/FN/TP.
  - Lettura implicita corretta: precision bassa = molti falsi allarmi; recall 0.5 = perdi metà degli alterati.
- **Rifinitura**:
  - Nella formula scritta: mettere parentesi per evitare ambiguità: `precision = 5 / (5 + 10)`.
  - Se vuoi “super preciso”: usa più decimali (precision = 0.333..., F1 ≈ 0.40).

### 2026-04-09 — QUIZ Verifica (Domanda 3: ordine argomenti metriche)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 560-564
- **Esito**: individuato correttamente il bug principale; conseguenza da correggere
- **Punti di forza**:
  - Ha notato che `precision_score` si chiama come `precision_score(y_true, y_pred)` e che nell’esempio sono invertiti.
- **Correzione**:
  - Invertendo i parametri non ottieni uno score “>100%”: di norma la metrica resta tra 0 e 1, ma diventa **semanticamente sbagliata** (stai misurando una cosa diversa / con possibili risultati fuorvianti).
  - Rischio: in un report potresti prendere decisioni su soglie/modello basandoti su numeri che sembrano ok ma non misurano la metrica corretta.

### 2026-04-09 — QUIZ Verifica (Domanda 4: metrica critica e tipo errore)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 566-571
- **Esito**: corretto
- **Nota “da produzione”**:
  - “Recall sulla classe alterato” è la scelta giusta quando l’errore più grave è un **falso negativo** (alterato classificato come genuino).
  - In pratica poi si controlla anche la precision (carico revisione) e spesso si sceglie una soglia che massimizza recall rispettando un limite minimo di precision.

### 2026-04-09 — QUIZ Verifica (Domanda 5: `predict` vs `predict_proba`)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 574-577
- **Esito**: corretto
- **Rifinitura**:
  - Dire esplicitamente che `predict_proba` ritorna una matrice `n_righe x n_classi` e che per il binario di solito usi la colonna della classe “alterato” (es. `[:, 1]` se `classes_ = [0, 1]`) per derivare `prob_alterato` e quindi `score_genuinita`.

### 2026-04-09 — QUIZ Verifica (Domanda 6: precision/recall con analogia)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 579-585
- **Esito**: corretto e spiegato bene
- **Punti di forza**:
  - Analogia dell’allarme molto chiara: precision = “quando suona, quante volte era vero”; recall = “quanti ladri ha intercettato”.
  - Motivazione corretta sul dominio documentale: FN più pericolosi → recall spesso prioritaria.
- **Rifinitura**:
  - Chiudere la frase finale (qui è tronca) e nominare esplicitamente gli errori: “FN (alterato→genuino) vs FP (genuino→alterato)”.
- **Voto ponderato (1–10)**: 9/10 (corretto, completo, buona comunicazione; solo rifinitura forma/chiusura frase)

### 2026-04-09 — VALUTAZIONE (Esercizio 1: albero + metriche + confusion matrix + assert baseline)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 597-660
- **Punti di forza**:
  - Ha seguito la pipeline completa: load CSV → `X/y` → split → train → metriche → confusion matrix → assert baseline.
  - Feature/target preparati correttamente (`drop` di `y_alterato` e `pratica_id`).
  - Report comparativo TRAIN vs TEST: ottimo per vedere overfitting già da qui.
  - Assert `accuracy_test > 0.5` coerente con regola testing trasversale.
- **Correzioni / miglioramenti**:
  - Split: in classificazione è preferibile `stratify=y` per mantenere proporzioni classi (dataset piccolo + sbilanciamento).
  - Metriche: aggiungere `zero_division=0` a `precision_score/recall_score/f1_score` per evitare warning se una classe non viene predetta.
  - Confusion matrix: ok stampare `confusion_matrix(...)`, ma assicurarsi di avere l’import corretto da `sklearn.metrics`.
  - Naming: ok, ma potresti usare chiavi più corte (`accuracy`, `precision`, …) e stampare anche in percentuale per leggibilità.
- **Voto ponderato (1–10)**: 8.5/10 (corretto e completo; da alzare con `stratify` + robustezza metriche `zero_division`)

### 2026-04-09 — VALUTAZIONE (Esercizio 2: confronto modelli + scaling per logistica)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 663-729
- **Punti di forza**:
  - Split corretto e robusto: `random_state=42` + `stratify=y`.
  - Scaling corretto per la logistica: `fit` su train e `transform` su train/test.
  - Modelli allenati nel modo giusto (alberi su `X_train`, logistica su `X_train_scaled`).
  - Metriche su test calcolate correttamente e rese robuste con `zero_division=0`.
- **Cosa manca rispetto alla consegna**:
  - Manca: **“stampalo ordinato per recall”** → ti serve un `.sort_values("recall", ascending=False)` prima della stampa.
  - Manca: **commento di scelta modello** per il prodotto pensando ai **falsi negativi**.
- **Rifiniture**:
  - Naming stringhe: `Albero max_depth=3` (non `max:depth`), per chiarezza.
- **Voto ponderato (1–10)**: 8/10 (corretto e pulito; perdi punti solo per due requisiti non completati: ordinamento + commento scelta)

### 2026-04-09 — VALUTAZIONE (Esercizio 3 🎯 COLLOQUIO: spiegazione metriche)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 732-747
- **Punti di forza**:
  - Precision e recall spiegati con esempi concreti e coerenti col dominio documentale.
  - Scelta della metrica critica nel prodotto: recall sugli alterati (per ridurre FN) motivata bene.
  - F1: ha colto l’idea chiave “se una delle due è bassa, F1 scende”.
- **Correzioni / rifiniture**:
  - Precision/recall: ottimo l’esempio “su 10…”, ma il collegamento tra metrica ed errore va espresso così:
    - precision bassa ⇢ **molti FP**,
    - recall bassa ⇢ **molti FN**.
    (nelle parentesi hai indicato “falsi positivi/falsi negativi” in modo un po’ ambiguo).
  - F1: una riga in più “da colloquio”: è la media armonica che penalizza gli sbilanciamenti e rappresenta un compromesso tra precision e recall.
  - Confusion matrix: non è “una matrice 2”, ma una **matrice 2×2** (nel binario). Lettura `[[TN, FP], [FN, TP]]` corretta.
- **Voto ponderato (1–10)**: 8.5/10 (solida risposta da colloquio; da rendere perfetta chiarendo FP vs FN nelle definizioni e rifinendo F1)

### 2026-04-09 — VALUTAZIONE (Esercizio 5 🔍 DEBUG: recall sospetto)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 772-787
- **Punti di forza**:
  - Ha individuato correttamente il **data leakage**: `y_alterato` resta nelle feature perché si fa solo `drop(pratica_id)` — il modello “vede la risposta”.
  - Collegamento al risultato ingannevole: recall 1.0 spiegabile perché la predizione è quasi banale.
- **Rifinitura**:
  - L’overfitting / `max_depth` è un argomento secondario qui: il bug principale è proprio il target nelle X; senza leakage l’albero potrebbe comunque avere recall alta ma non “magica”.
  - Correzione: `X_dbg = pratiche_dbg.drop(columns=["pratica_id", "y_alterato"], errors="ignore")`.
- **Voto ponderato (1–10)**: 9/10 (leakage centrato; -0.5 per mescolare un po’ troppo con overfitting senza chiarire la priorità)

### 2026-04-09 — VALUTAZIONE (Esercizio 4 🔧 REFACTORING: split + nomi + ordine metriche)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 750-788
- **Punti di forza**:
  - Risolve i 3 problemi indicati: **train/test split** (`stratify=y`), **nomi descrittivi** (`clf_tree_model`, `y_pred`), **ordine corretto** `metriche(y_true, y_pred)`.
  - Valuta su **test** (`X_test`), non sul train intero → metriche più significative.
  - Formattazione stampa con `%` leggibile.
- **Rifiniture**:
  - `pratiche` è definito negli esercizi precedenti: ok se lo script gira dall’inizio; per esercizio “autonomo” meglio ricaricare il CSV qui.
  - Import ridondanti (già in cima al file): opzionale toglierli.
  - `recall_score(..., zero_division=0)` per coerenza con il resto del capitolo.
  - Per **due cifre decimali** nella percentuale: `:.2%` invece di `:.1%`.
  - Opzionale: `max_depth` sull’albero per limitare overfitting (non era tra i 3 bug obbligatori).
- **Voto ponderato (1–10)**: 9/10 (refactoring corretto e completo; piccole rifiniture di robustezza e formattazione)

### 2026-04-09 — VALUTAZIONE (Esercizio 6 🔀 INTERLEAVING: report Pandas + filtro OCR + modello)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 808-856
- **Punti di forza**:
  - Report Pandas impostato bene: totali, % alterate, medie per classe su `delta_netto_lordo` e `confidence_ocr_media`.
  - Filtri e pipeline modello coerenti (anti-leakage: droppi `pratica_id` e `y_alterato`; poi train/predict).
  - Commento finale centrato: filtro OCR troppo alto può eliminare gli alterati ⇒ valutazione non significativa.
- **Correzioni / miglioramenti**:
  - Soglia: consegna dice `>= 0.75`, nel codice hai `> 0.75` (dettaglio, ma da allineare).
  - Se dopo il filtro resta **una sola classe** (succede nel mock), `classification_report`/`confusion_matrix` diventano fuorvianti e può comparire warning “single label”. Prima di split conviene controllare `y.value_counts()` sul filtrato.
  - `.abs()` su `confidence_ocr_media` è inutile (è già positiva) e su `delta_netto_lordo` cambia il significato della media: ok solo se lo fai consapevolmente.
  - Stampare anche `print(report)` (ora lo costruisci ma non lo mostri).
  - `classification_report(..., zero_division=0)` per coerenza/robustezza.
- **Voto ponderato (1–10)**: 8/10 (buona impostazione e ottima osservazione sul filtro; perdi punti per edge-case mono-classe + piccoli mismatch consegna/stampa)

### 2026-04-09 — VALUTAZIONE (Esercizio 7 🧠 RETRIEVAL: LogisticRegression + scaling + predict_proba)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 862-910
- **Punti di forza**:
  - Pipeline corretta: load → `X/y` senza leakage → `train_test_split` con `stratify` e `random_state` → `StandardScaler` fit su train → logistica su train scalato → `predict` / `predict_proba` su **test scalato**.
  - Loop di stampa allineato alla traccia: reale vs previsto + `score_genuinita` da `proba[1]` (equivalente a `(1 - prob_alterato)` come probabilità; `.2%` coerente).
  - Metriche su test + assert sul recall.
- **Rifiniture**:
  - Aggiungere `zero_division=0` a precision/recall/F1 per coerenza col capitolo.
  - Consegna: assert `recall >= 0.5`; nel codice c’è `> 0.5` (stretto: un recall esattamente 0.5 fallirebbe).
  - Ordine stampa metriche: la traccia elenca accuracy, recall, precision, F1 — ordine attuale diverso ma contenuto ok.
- **Voto ponderato (1–10)**: 9/10 (esercizio ben eseguito; piccole rifiniture assert/ordine/zero_division)

### 2026-04-13 — ESERCIZIO 8 (Analisi prodotto: coefficienti, score_genuinita, semaforo)

- **Riferimento**: `modulo_02_ml/04_classificazione_metriche.py` ~righe 911-968
- **Punti di forza**:
  - **Coefficienti**: DataFrame con `nome_feature`, peso, valore assoluto e `sort_values` — stesso spirito di `motivi_top_n` del cap.03, adattato al classificatore.
  - **score_genuinita**: con `y_alterato` (0=genuino, 1=alterato) e `classes_` ordinato `[0,1]`, usare `y_proba_test[:, 0] * 100` è **coerente** con il Blueprint: equivale a `(1 - prob_alterato) * 100` perché `prob_alterato = proba[:, 1]`.
  - **Semaforo**: `np.select` con soglie 85 / 60 allineate al Blueprint; ordine condizioni corretto (prima `>=85`, poi `>=60`, default rosso).
  - **Tabella richiesta**: colonne `pratica`, `score_genuinita`, `semaforo`, `classe_reale`, `classe_prevista` presenti; mapping reale/previsto con `np.select` leggibile.
  - **Commento di business**: interpretazione sensata — il giallo come allerta anche quando la classe prevista non coincide; collegamento a “non verde = non ok operativo”.
- **Miglioramenti (non bloccanti)**:
  - Un commento esplicito tipo `prob_alterato = y_proba_test[:, 1]` / `score_genuinita = (1 - prob_alterato) * 100` rende il legame alla pipeline leggibile a colpo d’occhio (anche se numericamente identico a `[:,0]*100`).
  - Per il punto 4 della consegna (conteggi verdi/gialli/rossi) si può aggiungere `report["semaforo"].value_counts()` (e eventualmente filtrare rossi con `y_test==1`) così i numeri restano nel codice, non solo nel commento.
  - Evitare accenti nel nome variabile (`genuinità_prev` → es. `genuinita_prev`) per convenzione e compatibilità tool.
- **Pattern**: nessuno nuovo; coerenza con #22 (variabili allineate al modello usato: qui `clf_log` + `y_pred_test`/`y_proba_test` dallo stesso blocco es.7).
- **Voto ponderato (1–10)**: **9/10** (corretto, completo, forte collegamento prodotto; piccoli extra per esplicitare `prob_alterato` e conteggi programmatici).

### 2026-04-13 — PROGETTO INCREMENTALE `modello_base.py` (sezione CLASSIFICAZIONE, ~145-253)

- **Riferimento**: `modulo_02_ml/modello_base.py` ~righe 145-253
- **Punti di forza**:
  - Pipeline completa: CSV → `X/y` → split stratificato → scaler fit su train → due classificatori → metriche → report test con `pratica_id`, score da `predict_proba`, semaforo.
  - **`score_genuinita`** da `y_proba_log[:, 0] * 100` coerente con `0=genuino` (equivale a `(1 - prob_alterato)*100`).
  - **Soglie semaforo** 85/60 allineate al Blueprint; `top3` coefficienti con `coef_.ravel()` e ordinamento per `abs`.
  - Extra utile: tabella ordinata per score, confronto reale/previsto in linguaggio dominio.
- **Gap rispetto al task / DoD**:
  - Assert richiesto: **recall di almeno un modello ≥ 0.5** — nel file c’è un assert **diverso** (logistica vs “baseline”); va sostituito o affiancato a quello della consegna.
  - **`y_baseline = np.full_like(y_test, y_train.mean())`**: per target interi, la media spesso viene **troncata a 0** → baseline “sempre genuino”, confronto recall poco significativo; per una baseline classica meglio **classe maggioritaria** o `DummyClassifier(strategy="most_frequent")`.
  - **`semaforo`**: la consegna suggerisce **`semaforo(score)`** (punteggio 0–100); qui accetti **`proba`** intera — ok funzionale, ma API e nome parametro da allineare; evitare **`proba=[]`** (default mutabile).
  - **`motivi_top_3`**: la funzione esistente non viene riusata per la logistica; hai replicato la logica con DataFrame — ok come output, ma il DoD chiede che **`motivi_top_3` “funzioni anche” sul classificatore** → estendere con `.ravel()` (o ramo dedicato) e una `print(motivi_top_3(clf_log, ...))`.
  - Colonna **`f1`** vs `f1_score` (solo naming).
- **Pattern**: nessuno nuovo critico; attenzione a **rinominare variabili** tra regressione e classificazione (`report_metriche` riusato per due contenuti diversi — funziona ma confonde in lettura).
- **Voto ponderato (1–10)**: **7.5/10** (ottimo lavoro su dati e prodotto; perde punti su assert/DoD, baseline, API `semaforo`, riuso `motivi_top_3`).

---

## Lacune e dubbi ancora aperti

- …

---

## Note per il capitolo successivo (mentor)

- Inseriti in `05_overfitting_validazione.py` (blocco iniziale) rinforzi su: prob_alterato vs score, leakage, scaler fit-on-train; quiz ingresso bozza.
- Ripasso trade-off validazione e collegamento a metriche prodotto (recall, generalizzazione).

### Rettifica voto difficoltà (13/04/2026)

- **Voto difficoltà capitolo 04 (studente)**: **7**/10 (conferma esplicita; aggiornato in `CONTESTO_CORSO.md`).
