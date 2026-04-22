"""
============================================================================
MODULO 2 — CAPITOLO 06: Streamlit da zero (primo deploy)
============================================================================

Questo è il capitolo dove trasformi il lavoro “da script” (`modello_base.py`)
in una vera mini web-app — e la porti online (primo deploy del corso).

È un capitolo lungo di proposito: parti da zero con Streamlit, quindi ogni
concetto nuovo viene introdotto con teoria discorsiva + mini-esercizio.

Obiettivo (portfolio + prodotto):
- mini web-app che seleziona una `pratica_id` e mostra `prob_alterato`,
  `score_genuinita`, `semaforo`, `motivi_top3`, metrica e stabilità CV
- deploy su Streamlit Cloud → una URL live nel portfolio (primo URL del corso!)

Analogia web (Laravel/React):
- in Laravel/React: route → controller → view
- in Streamlit: cambi un widget → il file viene rieseguito → UI si aggiorna

Vincoli imparati nei capitoli precedenti (da rispettare qui):
- cap.04: `prob_alterato` = P(y=1); `score_genuinita = (1 - prob_alterato) * 100`; semaforo 85/60
- cap.05: test solo UNA volta; CV sul train; `Pipeline` per evitare leakage preprocessing
"""


# ==========================================================================
# 📦 PREREQUISITI AMBIENTE (OBBLIGATORIO — ogni step sarà eseguibile)
# ==========================================================================
#
# 1) Ambiente virtuale attivo (Windows / Git Bash o cmd):
#
#       python -m venv venv
#       venv\Scripts\activate     (cmd)
#       source venv/Scripts/activate  (Git Bash)
#
# 2) `requirements.txt` (root repo) per il Modulo 2: scommenta
#    - scikit-learn
#    - streamlit
#
# 3) Installa:
#
#       pip install -r requirements.txt
#
# 4) Verifica:
#
#       streamlit --version
#
# Se la verifica fallisce, NON proseguire: è un prerequisito tecnico.
#
# --- MINI-ESERCIZIO — Verifica setup ---
# In chat, incolla l'output di `streamlit --version` (deve stampare una versione, non un errore).
#


# ==========================================================================
# QUIZ D'INGRESSO — Ripasso Cap.05 (validazione, leakage, metriche)
# ==========================================================================
#
# DOMANDA 1 — V/F:
# "Se ottengo recall=0.82 sul test UNA VOLTA, posso essere certo che in produzione sarà simile."
# Motiva in 2 righe.
# No, può darci un idea di massima ma in produzione potrebbero esserci valori diversi per la metrica di riferimento, sia per via del drift (i valori di riferimento cambiano nel tempo) sia per la diversa composizione degli split del set su cui abbiamo effettuato il test. Proprio per questo si usa la CV, per poter avere la media e la dev. std, le quali ci aiutano a stabilizzare le metriche

# DOMANDA 2 — Completa:
# Recall (classe 'alterato' = 1) = TP / (TP + fn).  (NON è precision.)
#
# DOMANDA 3 — Scala:
# Se `prob_alterato = 0.35`, qual è `score_genuinita`? => 65
# Se `score_genuinita = 70`, qual è `prob_alterato`?  => 0.30
#
# DOMANDA 4 — Trova l'errore (leakage intra-CV):
# In una CV con scaler, perché NON devo fare `scaler.fit(X_train)` PRIMA di `cross_val_score(...)`?
#Perchè, quando cross_val_score eseguira lo split per ogni fold, scaler i set di validazione sulla base di una deviazione std calcolata anche sul set di validazione. E' una forma di leakage sottile, per evitarla invece di passare un modello nudo all cv, passiamo una pipeline, che per ogni fold riesegue il fit dello scaler solo sul train. 

# DOMANDA 5 — Prodotto:
# Perché in una UI ha senso mostrare “media ± std” della CV invece di un singolo numero?
#Perchè vogliamo sia vedere la media, che è un valore più stabilte rispetto alla metrica ottenuta solo da un test, ma la deviazione std ci aiuta a capire la volatilità dei risultati prodotti rispetto n prove.
#
# DOMANDA 6 — 💬 Feynman:
# Con parole tue: differenza tra "train set" e "test set" in 3 righe.
#train set: set di allenamento, con il quale il modello viene addestrato.
#test set: set che il modello non ha mai visto, con cui effettuiamo l'esame per evincerne l'efficacia sui dati che non sono noti. Confrontandolo con i risultati prodotti da una previsione fatta su i dati train inoltre, possiamo capite se il modello ha generalizzato correttamente le regole che si celano dietro la predizione del target di riferimento. 


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #16 (scala 0–1 vs 0–100)
# ==========================================================================
#
# `prob_alterato` ∈ [0, 1]  |  `score_genuinita` ∈ [0, 100]
# Formula: score_genuinita = (1 - prob_alterato) * 100
#
# --- MINI-ESERCIZIO ---
# 1) prob_alterato = 0.58 → score_genuinita = 42
# 2) score_genuinita = 55  → prob_alterato = 0.45
# 3) Se UI dice "score = 0.7", cosa c'è di sbagliato?
# che lo score genuinità si esprire in un valore da 0 a 100, e non da 0 a 1


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #17 (drop colonne reali, non "id/target" astratti)
# ==========================================================================
#
# --- MINI-ESERCIZIO ---
# Completa (il dataset è `dati/pratiche_genuinita_mock.csv`):
# X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
# y = pratiche['y_alterato']
#


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #18 (recall vs precision)
# ==========================================================================
#
# Recall (classe 1) = TP / (TP + FN)
# Precision (classe 1) = TP / (TP + FP)
#
# --- MINI-ESERCIZIO ---
# 1) Se alzo la soglia da 0.5 a 0.8, tipicamente precision aumenta e recall diminuisce.
# 2) In controllo documentale, è più grave FP (falso allarme) o FN (frode non intercettata)?
# la seconda
#


# ==========================================================================
# ==========================================================================
# PARTE 1 — Cos'è Streamlit (modello mentale)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 1.1 — Streamlit in 3 righe
# ==========================================================================
#
# Streamlit è una libreria Python che:
# - prende un file `.py`
# - lo esegue come un web server locale (porta 8501 di default)
# - ti mostra nel browser un'interfaccia fatta dai "widget" che invochi nel codice
#
# Tu non scrivi HTML, CSS o JavaScript: scrivi Python, e i widget (come
# `st.selectbox`, `st.metric`) vengono renderizzati come elementi UI.
#
# Paragoni utili:
# - Laravel: il file `.py` è un po' come una `resources/views/*.blade.php` + controller
#   messi insieme, ma senza template engine: componi la pagina con funzioni Python
# - React: il file è un po' come un componente che RI-renderizza quando cambia lo stato;
#   lo "stato" qui sono i valori dei widget
#
# --- MINI-ESERCIZIO 1.1 ---
# Senza scrivere codice: in una riga, descrivi cosa vuoi vedere in pagina alla fine
# del capitolo. (Es: "titolo + select pratica + tre numeri + CV media±std")
# Titolo: Valutazione Pratica
# Select: una select con id delle pratiche
# Info generiche: stabilità/volatilità del modello (CV media e std)
# Info sulla pratica selezionata: semaforo (verde, giallo, rosso), score genuinità, motivi top3 della valutazione
# Sidebar: diverse select o input per cambiare soglie e iperparametri al modello.


# ==========================================================================
# 📖 TEORIA 1.2 — Il "rerun from top" (la regola più importante)
# ==========================================================================
#
# ⚠️ Questo è lo scoglio #1 per chi viene dal web classico:
#
# OGNI volta che l'utente cambia un input (clicca un bottone, sposta uno slider,
# cambia un select), Streamlit RIESEGUE il file `.py` DALL'ALTO.
#
# Non c'è un "onClick" o un "controller": il modello è
# "re-run everything e ricrea la pagina con i nuovi valori".
#
# Conseguenze pratiche:
# 1) I widget NON sono variabili permanenti: sono funzioni che ritornano il valore
#    corrente. Esempio: `pratica_id = st.selectbox(...)` → ogni rerun, `pratica_id`
#    vale il valore selezionato in quel momento.
# 2) Non usare `print()` per l'utente: usa `st.write`, `st.metric`, `st.dataframe`.
# 3) Operazioni costose (caricare CSV, addestrare modello) verrebbero rifatte OGNI rerun.
#    Per evitarlo esiste il caching (vedi PARTE 3).
#
# Mini-esempio (concetto):
#
# import streamlit as st
# st.title("Hello")                 # rieseguita ad ogni rerun
# nome = st.text_input("Nome")      # ad ogni rerun, `nome` ha il valore corrente
# st.write(f"Ciao {nome}")          # viene ri-renderizzata
#
# --- MINI-ESERCIZIO 1.2 ---
# In 2 righe: cosa succede se dentro il file scrivi `lista = []` e poi fai
# `lista.append(x)` pensando di accumulare dati tra un click e l'altro?
# (Suggerimento: ricorda il "rerun".)
# Ripartirebbe da 0, quindi avrei un array con solo l'ultimo elemento inserito


# ==========================================================================
# 📖 TEORIA 1.3 — Avviare l'app ("streamlit run", non "python ...")
# ==========================================================================
#
# Streamlit NON si avvia con `python app_streamlit.py`: si avvia con un comando
# dedicato che lancia il server:
#
#     streamlit run modulo_02_ml/app_streamlit.py
#
# Streamlit stampa un URL locale (tipo http://localhost:8501). Aprilo in browser.
# Quando cambi il file e salvi, in alto a destra hai "Rerun" / "Always rerun".
#
# Per fermare il server: Ctrl+C nel terminale.
#
# --- MINI-ESERCIZIO 1.3 ---
# Scrivi qui sotto l'esatto comando che tu lancerai, con il path del file:
# ...
# streamlit run modulo_02_ml/app_streamlit.py


# ==========================================================================
# 📖 TEORIA 1.4 — Troubleshooting Windows/venv (errori tipici)
# ==========================================================================
#
# Errori frequenti e soluzioni:
#
# - "streamlit: command not found" / "'streamlit' non è riconosciuto"
#     → il venv non è attivo o Streamlit non è installato in quel venv.
#       Esegui `venv\Scripts\activate` (cmd) o `source venv/Scripts/activate` (Git Bash),
#       poi `pip install -r requirements.txt`.
#
# - "Port 8501 is already in use"
#     → un'altra app Streamlit è rimasta attiva.
#       `streamlit run ... --server.port 8502` oppure Ctrl+C del vecchio processo.
#
# - "FileNotFoundError: pratiche_genuinita_mock.csv"
#     → stai usando un path relativo "cattivo" (dipende dalla cwd). Usa SEMPRE
#       `os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")`.
#
# - Modifiche al file non si vedono
#     → in alto a destra c'è "Always rerun": cliccalo, oppure premi R sulla pagina.
#
# - `ModuleNotFoundError: sklearn` / `pandas` / ecc.
#     → venv non attivo o dipendenze non installate. Ripeti pip install -r requirements.txt.
#
# --- MINI-ESERCIZIO 1.4 ---
# Immagina di vedere "streamlit: command not found": scrivi i 2 passi che faresti PRIMA
# di "reinstallare tutto da zero".
# proverei ad attivare il venv
# controllerei che streamlit sia installato (streamlit --version)
# proverei a reinstallare streamlit


# ==========================================================================
# ==========================================================================
# PARTE 2 — Widget di base (con mini-esempio per ciascuno)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 2.1 — Testi e struttura della pagina
# ==========================================================================
#
# - st.title("...")      → titolo grande (1 per pagina)
# - st.header("...")     → sezione
# - st.subheader("...")  → sotto-sezione
# - st.write(...)        → "stampa" generica (testo, DataFrame, dict, numeri)
# - st.caption("...")    → testo piccolo grigio (note)
# - st.divider()         → linea orizzontale
#
# Mini-esempio:
#
# import streamlit as st
# st.title("Demo genuinità")
# st.header("Dati")
# st.write({"righe": 640, "feature": 7})
#
# --- MINI-ESERCIZIO 2.1 ---
# Scrivi 3 righe che producono: titolo, header "Dati", scrittura di un dict a tua scelta.
#
# import streamlit as st
# import os
# import pandas as pd

# @st.cache_data
# def carica_pratiche() -> pd.DataFrame:
#     path = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
#     return pd.read_csv(path)

# st.title("Mini-esercizio 2.1")
# st.header("Dati")
# pratiche = carica_pratiche()
# st.write(pratiche.head(1).to_dict(orient="records")[0])

# ==========================================================================
# 📖 TEORIA 2.2 — Sidebar e layout a colonne
# ==========================================================================
#
# - `with st.sidebar:` → tutto ciò che scrivi dentro il blocco finisce nel pannello laterale.
# - `col1, col2, col3 = st.columns(3)` → 3 colonne affiancate, poi `col1.metric(...)`, ecc.
#
# Mini-esempio sidebar:
#
import streamlit as st
with st.sidebar:
    st.header("Filtri")
    scelta = st.selectbox("Semaforo", ["tutti", "verde", "giallo", "rosso"])
#
# Mini-esempio colonne:
#
c1, c2 = st.columns(2)
c1.metric("Score", 80)
c2.metric("Semaforo", "verde")
#
# --- MINI-ESERCIZIO 2.2 ---
# Scrivi in 4 righe: sidebar con un header + un selectbox binario; fuori dalla sidebar
# due colonne affiancate con due st.write qualsiasi.
#


# ==========================================================================
# 📖 TEORIA 2.3 — Input: selectbox, checkbox, slider, number_input
# ==========================================================================
#
# - st.selectbox(label, opzioni, index=0)
# - st.checkbox(label, value=False)
# - st.slider(label, min_value, max_value, value)
# - st.number_input(label, min_value, max_value, value)
#
# Ritornano sempre il valore CORRENTE del widget (rerun-aware).
#
# Mini-esempio:
#
#     pid = st.selectbox("pratica_id", [1, 2, 3])
#     attiva = st.checkbox("mostra dettaglio", value=True)
#     soglia = st.slider("soglia prob_alterato", 0.0, 1.0, 0.5, step=0.05)
#
# --- MINI-ESERCIZIO 2.3 ---
# Scrivi 3 righe: un selectbox su ["alfa", "beta"], un checkbox, e uno slider 0–100 a step 5.
# Poi 1 riga che stampa con `st.write` i valori correnti.
#


# ==========================================================================
# 📖 TEORIA 2.4 — Output dati: dataframe, table, metric, messaggi
# ==========================================================================
#
# - st.dataframe(df) → tabella scrollabile (meglio per df grandi)
# - st.table(df)     → tabella statica
# - st.metric("label", value, delta=None)
# - st.success("...") / st.warning("...") / st.error("...") / st.info("...")
#
# `st.metric` è perfetto per score/semaforo: "card" con numero grande e label.
#
# --- MINI-ESERCIZIO 2.4 ---
# Scrivi 2 righe: una `st.metric` che mostra "score_genuinita" a 82.5,
# e una `st.warning` che dice "soglia in revisione".
#


# ==========================================================================
# ==========================================================================
# PARTE 3 — Caching: non ripetere inutilmente il lavoro costoso
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 3.1 — Perché serve il caching
# ==========================================================================
#
# Dato che Streamlit riesegue il file AD OGNI rerun, senza caching ogni click
# rifà: lettura CSV, addestramento modello, CV… anche se non serve.
#
# Streamlit offre due decoratori:
#
# - @st.cache_data     → per DATI (DataFrame, liste, dict, numpy). Immutabili o "trattati come tali".
# - @st.cache_resource → per RISORSE (oggetti pesanti come modelli addestrati, connessioni DB).
#
# La cache è basata sugli argomenti della funzione: se gli argomenti cambiano, ricalcola.
#
# Regola pratica per il nostro capitolo:
# - carichi CSV → @st.cache_data
# - addestri il modello una volta e lo riusi → @st.cache_resource
#
# Mini-esempio:
#
#     @st.cache_data
#     def carica_pratiche(path: str) -> pd.DataFrame:
#         return pd.read_csv(path)
#
#     @st.cache_resource
#     def addestra_modello(X_train, y_train):
#         pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])
#         return pipe.fit(X_train, y_train)
#
# --- MINI-ESERCIZIO 3.1 ---
# Dato il compito "calcola array CV recall per 5 fold", quale cache useresti e perché?
# (Suggerimento: è un array di numeri risultato di un calcolo deterministico.)
#


# ==========================================================================
# 📖 TEORIA 3.2 — Trappole classiche del caching
# ==========================================================================
#
# 1) Se passi argomenti che cambiano ogni rerun (es. un `datetime.now()`), la cache
#    "salta" sempre e non serve a nulla.
#
# 2) Se NON passi un argomento ma la funzione dipende da una variabile esterna,
#    la cache potrebbe non invalidarsi quando dovrebbe → passa tutto come argomento.
#
# 3) Se modifichi il DataFrame tornato da `@st.cache_data` dentro altre funzioni,
#    rischi effetti collaterali (Streamlit protegge, ma meglio clonare con `.copy()`).
#
# --- MINI-ESERCIZIO 3.2 ---
# Se nel tuo codice `addestra_modello()` non accetta `X_train, y_train` come argomenti
# ma li prende da variabili globali, cosa può andare storto con @st.cache_resource?
#


# ==========================================================================
# ==========================================================================
# PARTE 4 — Path "deploy-safe" (quando il file si sposta su cloud)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 4.1 — Perché i path assoluti sono un problema
# ==========================================================================
#
# In locale: "C:/Users/visaf/Desktop/Corso IA/..." funziona. Su Streamlit Cloud:
# il file vive in un altro filesystem, quel path NON esiste, l'app crasha.
#
# Soluzione: costruisci path RELATIVI al file `.py` in esecuzione.
#
# Due strumenti Python già visti (o quasi):
# - `__file__` → stringa con il path del file che lo contiene
# - `os.path.dirname(__file__)` → la cartella di quel file
# - `os.path.join(a, b, c)` → costruisce un path portabile (Windows/Linux)
#
# Ricetta:
#
#     path_csv = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
#     pratiche = pd.read_csv(path_csv)
#
# Così funziona sia in locale sia su Streamlit Cloud, perché il CSV è nel repo
# a fianco del file `.py` (cartella `dati/` relativa).
#
# --- MINI-ESERCIZIO 4.1 ---
# Se sposti il file `app_streamlit.py` in `modulo_02_ml/ui/app_streamlit.py`, come cambia il path al CSV?
# Scrivi la riga corretta.
#


# ==========================================================================
# ==========================================================================
# PARTE 5 — Architettura "pulita": UI vs ML (niente copy-paste)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 5.1 — Regola del confine
# ==========================================================================
#
# `modello_base.py` = logica ML (funzioni, Pipeline, scoring).
# `app_streamlit.py` = PRESENTAZIONE: carica dati, chiede input, mostra output.
#
# Domande per decidere "dove va una riga di codice":
# - riguarda come si calcola lo score? → modello_base (o una funzione)
# - riguarda come APPARE lo score nella pagina? → app_streamlit
#
# Questo ti salva dal Pattern #22 (incoerenze tra nomi/modelli tra i due file).
#
# Nota: in questo capitolo non ti obbliga a estrarre TUTTE le funzioni subito;
# l'ESERCIZIO 8 (refactoring) ti guiderà quando ne avrai almeno 1–2 da estrarre.
#
# --- MINI-ESERCIZIO 5.1 ---
# Categorizza ognuna in "UI" o "ML":
# 1) calcolare score_genuinita da prob_alterato
# 2) mostrare "score: 82" in colonna 1
# 3) addestrare la LogisticRegression
# 4) disegnare il semaforo colorato
# 5) calcolare CV media ± std
#


# ==========================================================================
# ==========================================================================
# PARTE 6 — Inference su UNA singola pratica (predict_proba 1-riga)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 6.1 — Come passare 1 riga al modello (shape e forma)
# ==========================================================================
#
# sklearn vuole sempre un input 2D (matrice). Una riga di DataFrame (Series) è 1D.
# Se passi una Series, esplode con "Expected 2D array, got 1D".
#
# Due modi corretti:
# 1) Passare un DataFrame filtrato con `loc` (mantiene 2D):
#
#       X_una = pratiche.loc[pratiche["pratica_id"] == pid].drop(columns=["pratica_id", "y_alterato"])
#       proba = pipe.predict_proba(X_una)   # shape: (1, 2)
#
# 2) Ri-wrappare la Series in un DataFrame:
#
#       riga = pratiche.loc[pratiche["pratica_id"] == pid].iloc[0]
#       X_una = riga.drop(["pratica_id", "y_alterato"]).to_frame().T
#       proba = pipe.predict_proba(X_una)
#
# Entrambi restituiscono `proba` con shape (1, 2). La probabilità di "alterato" è `proba[0, 1]`.
#
# --- MINI-ESERCIZIO 6.1 ---
# Completa: dato `pipe` e una `pratica_id = 42`, scrivi 2 righe che ottengono
# `prob_alterato` (un numero 0–1).
#


# ==========================================================================
# 📖 TEORIA 6.2 — Pattern completo 1-riga: prob → score → semaforo
# ==========================================================================
#
# Ricetta da riusare in UI:
#
#     prob_alterato = pipe.predict_proba(X_una)[0, 1]         # 0–1
#     score_genuinita = (1 - prob_alterato) * 100              # 0–100
#     if   score_genuinita >= 85: semaforo = "verde"
#     elif score_genuinita >= 60: semaforo = "giallo"
#     else:                        semaforo = "rosso"
#
# Nota UI: è buona prassi MOSTRARE ENTRAMBI (prob e score) con label chiare,
# così un utente non confonde le scale (Lacuna #16).
#
# --- MINI-ESERCIZIO 6.2 ---
# Se `prob_alterato = 0.42`, quale semaforo dovrebbe uscire? Perché?
#


# ==========================================================================
# ==========================================================================
# PARTE 7 — Spiegabilità "onesta" con coef_ (motivi_top3)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 7.1 — Cosa sono i coefficienti dopo scaling
# ==========================================================================
#
# Nella `Pipeline(StandardScaler + LogisticRegression)`, dopo il fit:
# - `pipe.named_steps["model"].coef_` → array 1D con un peso per feature
# - dato che le feature sono STANDARDIZZATE (media 0, std 1), i pesi sono
#   CONFRONTABILI tra feature: ha senso ordinarli per valore assoluto.
#
# Interpretazione del segno:
# - coefficiente > 0 → la feature spinge verso la classe 1 (alterato)
# - coefficiente < 0 → spinge verso la classe 0 (genuino)
#
# `motivi_top3` = le 3 feature con |coefficiente| più grande.
#
# --- MINI-ESERCIZIO 7.1 ---
# Se dopo il fit vedi `coef_ = [0.8, -0.1, 0.3, -0.6]` con feature ["a","b","c","d"]:
# 1) top 3 per |peso| = ?
# 2) quale "spinge" verso alterato?
#


# ==========================================================================
# 📖 TEORIA 7.2 — Cosa NON sono (la parte "onesta")
# ==========================================================================
#
# I motivi_top3 NON sono una "causa provata": dicono solo quali feature hanno
# avuto più peso nel modello LOGISTIC REGRESSION su QUESTI dati.
#
# - cambia dataset → cambiano i coef
# - cambia modello (albero) → cambia il concetto stesso di "importanza"
# - correlazioni forti tra feature possono "spostare" i pesi senza significato causale
#
# In UI dobbiamo scriverlo, altrimenti un recruiter serio ti chiede "e se mentono?".
#
# --- MINI-ESERCIZIO 7.2 ---
# Scrivi in 1 riga il disclaimer che metteresti sotto la lista dei "motivi".
#


# ==========================================================================
# ==========================================================================
# PARTE 8 — CV media±std in UI (rinforzo cap.05 in ambiente Streamlit)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 8.1 — Perché mostriamo CV in UI
# ==========================================================================
#
# Nel cap.05 hai imparato che:
# - il test va usato una volta (arbitro finale)
# - la CV sul train stima la stabilità del modello
#
# In UI, mostrare "recall sul test = 0.82" da solo è fragile: un recruiter
# potrebbe chiederti "quanto oscilla?". La risposta è media±std dalla CV.
#
# Piccolo caveat: in una demo didattica calcolare CV ogni rerun è pesante.
# Ecco perché useremo `@st.cache_data` o cacheremo la fase di training.
#
# Pattern:
#
#     @st.cache_data
#     def cv_recall(X_train, y_train) -> tuple[list[float], float, float]:
#         pipe = Pipeline([("scaler", StandardScaler()),
#                          ("model", LogisticRegression(max_iter=1000, random_state=42))])
#         kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
#         scores = cross_val_score(pipe, X_train, y_train, cv=kf, scoring="recall")
#         return list(scores), float(scores.mean()), float(scores.std())
#
# --- MINI-ESERCIZIO 8.1 ---
# Perché NON passiamo `X_test, y_test` a `cv_recall`? (Basta 1 riga.)
#


# ==========================================================================
# ==========================================================================
# PARTE 9 — Deploy su Streamlit Cloud (portfolio live)
# ==========================================================================
# ==========================================================================


# ==========================================================================
# 📖 TEORIA 9.1 — Cosa succede quando fai deploy
# ==========================================================================
#
# Streamlit Cloud è un servizio gratuito che:
# - legge un repo GitHub
# - installa le dipendenze da `requirements.txt`
# - esegue il file `.py` che scegli (es. `modulo_02_ml/app_streamlit.py`)
# - ti dà una URL pubblica (es. https://tuonome-app.streamlit.app)
#
# Pre-requisiti:
# - repo GitHub pubblico (o collegato a Streamlit Cloud)
# - `requirements.txt` completo (streamlit, scikit-learn, pandas, numpy ≥ versioni sensate)
# - nessun path assoluto locale nell'app
# - CSV presenti nel repo (se servono all'app)
#
# --- MINI-ESERCIZIO 9.1 ---
# Guarda il tuo `requirements.txt` e conferma che `streamlit` e `scikit-learn` siano
# NON commentati. Se commentati → scommentali.
#


# ==========================================================================
# 📖 TEORIA 9.2 — Checklist deploy-ready (copia/incolla prima del deploy)
# ==========================================================================
#
# - [ ] `streamlit run modulo_02_ml/app_streamlit.py` parte in locale senza errori
# - [ ] Nessun path assoluto (solo `os.path.join(os.path.dirname(__file__), ...)`)
# - [ ] `requirements.txt` aggiornato (streamlit, sklearn, pandas, numpy)
# - [ ] Il CSV usato è nel repo (`modulo_02_ml/dati/...`)
# - [ ] Nessuna credenziale/segreto hard-coded
# - [ ] `README.md` (anche mini) con: cosa fa, cosa mostra, come lanciarla
# - [ ] Repo pushato su GitHub
#
# --- MINI-ESERCIZIO 9.2 ---
# Spunta mentalmente la checklist sul tuo progetto ora: cosa manca?
#


# ==========================================================================
# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
# ==========================================================================
#
# DOMANDA 1 — V/F:
# "Streamlit mantiene lo stato delle variabili Python tra un click e l'altro."
# V/F? Motiva.
#
# DOMANDA 2 — Completa:
# Per dati (DataFrame) si usa il decoratore ___; per oggetti pesanti (modello
# addestrato) si usa ___.
#
# DOMANDA 3 — Trova l'errore:
#     pratiche = pd.read_csv("C:/Users/visaf/Desktop/Corso IA/modulo_02_ml/dati/pratiche_genuinita_mock.csv")
# Perché è un problema in deploy? Come correggi?
#
# DOMANDA 4 — Prevedi l'output:
#     import streamlit as st
#     x = st.slider("x", 0, 10, 5)
#     st.write(x * 2)
# Se l'utente sposta lo slider a 7, cosa apparirà sotto?
#
# DOMANDA 5 — Shape:
# Per calcolare `predict_proba` di UNA pratica, quale shape deve avere l'input?
# Quale comando lo garantisce?
#
# DOMANDA 6 — 💬 Feynman:
# Spiega con parole tue perché mostrare "media ± std" della CV è più onesto di
# mostrare solo `recall_score(y_test, y_pred)` in una demo di portfolio.
#
# DOMANDA 7 — Architettura:
# Tra queste righe, quale NON dovrebbe stare in `app_streamlit.py`?
# a) calcolo score_genuinita da prob_alterato
# b) `pipe.fit(X_train, y_train)` chiamato dentro una funzione cached
# c) definizione dettagliata del dataset di training (riga per riga)
# d) `st.metric("Score", 82)`
#


# ==========================================================================
# ==========================================================================
# ESERCIZI PRATICI — Percorso guidato (step-by-step con DoD)
# ==========================================================================
# ==========================================================================
#
# NOTA: il file `modulo_02_ml/app_streamlit.py` è già presente come base.
# Ogni esercizio sotto lo completa un passo alla volta.
#
# ESERCIZIO 0 (Setup progetto):
# Apri `modulo_02_ml/app_streamlit.py` e leggilo dall'alto: è fatto apposta per
# essere eseguibile subito con un placeholder.
# DoD: file esiste, nessun import rotto, sai indicare i TODO.
#
# ESERCIZIO 1 (Hello Streamlit):
# Avvia:
#     streamlit run modulo_02_ml/app_streamlit.py
# DoD: si apre il browser, vedi titolo, sidebar e almeno 3 card (anche con valori placeholder).
#
# ESERCIZIO 2 (Select pratica + riga):
# Verifica che cambiando `pratica_id` nella sidebar cambi anche la riga mostrata.
# Se non funziona: leggi `iloc[0]` e verifica che il filtro con `.loc[...]` sia corretto.
# DoD: cambiando id, cambia la tabella.
#
# ESERCIZIO 3 (Modello vero al posto del placeholder):
# Rimuovi `prob_alterato = 0.5` e sostituiscilo con un'inferenza reale:
# - definisci X, y droppando `pratica_id`, `y_alterato`
# - split 80/20, stratify, random_state=42
# - `Pipeline(StandardScaler + LogisticRegression(max_iter=1000, random_state=42))`
# - `pipe.fit(X_train, y_train)` (caching consigliato: @st.cache_resource)
# - per la pratica selezionata: `prob_alterato = pipe.predict_proba(X_una)[0, 1]`
# DoD: `prob_alterato` cambia cambiando pratica_id; score e semaforo sono coerenti.
#
# ESERCIZIO 4 (🔍 [DEBUG] — scala invertita):
# Inserisci volutamente il bug "tratto prob come 0–100" (ad es. score = prob*100).
# Osserva in UI cosa diventa incomprensibile; poi correggi. Scrivi 2 righe sul rischio in prodotto.
#
# ESERCIZIO 5 (Spiegabilità — motivi_top3):
# Dopo `fit`, costruisci una tabella con nomi colonne + `coef_` (e |coef|).
# Mostra le TOP 3 in UI con una label che distingue "spinge verso alterato" (coef>0)
# da "spinge verso genuino" (coef<0).
# DoD: in UI compaiono 3 feature con peso e segno; sotto, un disclaimer onesto.
#
# ESERCIZIO 6 (🔀 [INTERLEAVING]):
# Aggiungi in sidebar un filtro `st.selectbox("Semaforo", ["tutti","verde","giallo","rosso"])`
# e mostra in una tabella TUTTE le pratiche con i loro score/semaforo (NON solo la selezionata).
# Se il filtro non è "tutti", applica una maschera Pandas.
# DoD: tabella cambia correttamente in base al filtro.
#
# ESERCIZIO 7 (🧠 [RETRIEVAL] — CV con Pipeline):
# Senza guardare cap.05, riscrivi in `app_streamlit.py` una funzione cached che
# ritorna (array_fold, media, std) di recall in 5-fold StratifiedKFold SOLO su X_train,y_train.
# Stampa i 3 risultati in UI (tabella + st.metric).
# DoD: media e std appaiono in UI; cambiando soglia UI NON si ricalcola la CV (cache funziona).
#
# ESERCIZIO 8 (🔧 [REFACTORING]):
# Estrai 2 funzioni pure in cima al file (o in un modulo a parte):
#   carica_pratiche(path) -> DataFrame
#   calcola_score_e_semaforo(pipe, riga_X) -> (prob, score, semaforo)
# DoD: `app_streamlit.py` è più corto e leggibile; UI invariata.
#
# ESERCIZIO 9 (Modalità esperimento — iperparametri & soglie in UI):
# Obiettivo: capire la differenza tra:
# - iperparametri del modello (es. `C` della LogisticRegression) → richiedono retrain
# - soglia di decisione su `prob_alterato` (es. 0.5→0.8) → NON richiede retrain
# - soglie semaforo su `score_genuinita` (es. 85/60) → sono policy/UX, NON ML
#
# Implementazione (in `app_streamlit.py`):
# 1) Sidebar:
#   - slider `C` (es. 0.01–10.0, log scale facoltativa)
#   - slider `soglia_prob` (0.0–1.0, default 0.5)
#   - slider `soglia_verde` e `soglia_giallo` (0–100, default 85/60)
# 2) Caching:
#   - l’addestramento deve stare in una funzione `@st.cache_resource` che dipende da `C`
#     (così non rifai fit a ogni click su `pratica_id`).
# 3) Output:
#   - mostra `prob_alterato`, `score_genuinita`, `semaforo` (con soglie personalizzabili)
#   - mostra anche `classe_predetta = 1 se prob_alterato >= soglia_prob altrimenti 0`
#
# Regola cap.05 (importante):
# - NON “scegliere” `C` o `soglia_prob` guardando il test: se vuoi ottimizzare, fallo su validation/CV.
#
# DoD: cambiando `soglia_prob` cambia la classe predetta senza retrain; cambiando `C` il modello si riallena
# (solo una volta per valore di C) e `prob_alterato` cambia in modo coerente.
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Modulo 2, Cap.06 (DEPLOY finale)
# ==========================================================================
#
# Deliverable:
# - `modulo_02_ml/app_streamlit.py` completo (esercizi 1→8)
# - breve README (in `modulo_02_ml/README.md` o in cima al file) con:
#   cosa fa, cosa mostra, come si lancia in locale, URL deploy
# - deploy su Streamlit Cloud attivo
#
# Definition of Done:
# - In UI: prob + score + semaforo per la pratica selezionata
# - In UI: motivi_top3 (con segno + disclaimer)
# - In UI: CV media±std (fatta con Pipeline, solo su X_train,y_train)
# - Nessun path assoluto; CSV nel repo
# - URL live raggiungibile
#
# Impatto roadmap: R0 ("primo deploy" nel portfolio del corso).
#


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# Quiz d'ingresso (bozza):
# 1) F — un singolo numero è una fotografia; serve stabilità (CV) + test usato 1 volta.
# 2) FN.
# 3) 65 ; 0.30.
# 4) Perché le statistiche dello scaler userebbero anche i validation fold → leakage.
# 5) Perché riduce il "rumore da sorteggio" di un singolo split.
# 6) Train = impara; Test = stima generalizzazione (una volta).
#
# Quiz di verifica (bozza):
# 1) F — ogni rerun riparte dall'alto; lo "stato" vero sta nei widget o in cache.
# 2) @st.cache_data ; @st.cache_resource.
# 3) path assoluto: in deploy il file non esiste. Usa os.path.join(os.path.dirname(__file__), ...).
# 4) "14".
# 5) (1, n_feature) — garantita passando un DataFrame filtrato con `.loc[...]` o `.to_frame().T`.
# 6) Libera — accetta che la CV cattura la variabilità tra split.
# 7) c) — dettagli di training non vanno nella UI.
#
# Esercizio 5 (motivi_top3) — idea risolutiva:
#     pesi = pd.DataFrame({
#         "feature": X_train.columns,
#         "coef":     pipe.named_steps["model"].coef_.ravel(),
#     })
#     pesi["abs"] = pesi["coef"].abs()
#     top3 = pesi.sort_values("abs", ascending=False).head(3)
#     # poi in UI: st.dataframe(top3) + disclaimer
#
# Esercizio 7 (CV) — idea risolutiva:
#     @st.cache_data
#     def cv_recall(X_train, y_train):
#         pipe = Pipeline([("scaler", StandardScaler()),
#                          ("model", LogisticRegression(max_iter=1000, random_state=42))])
#         kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
#         scores = cross_val_score(pipe, X_train, y_train, cv=kf, scoring="recall")
#         return list(scores), float(scores.mean()), float(scores.std())
#
# Deploy:
# - Streamlit Cloud → New app → seleziona repo/branch/file
# - Aspetta build (installa requirements) → ottieni URL
# - Metti l'URL nel README.
