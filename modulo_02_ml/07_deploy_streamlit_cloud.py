"""
============================================================================
MODULO 2 — CAPITOLO 07: Deploy Streamlit Cloud (prima URL portfolio)
============================================================================

Obiettivo:
  Portare ONLINE la demo Streamlit del Modulo 2 e ottenere una URL live.

Input (già costruito nel cap.06):
  - `modulo_02_ml/app_streamlit_da_zero.py` (la demo completa)
  - `modulo_02_ml/dati/pratiche_genuinita_mock.csv`
  - `requirements.txt` nella root

Output (portfolio-ready):
  - una URL Streamlit Cloud funzionante
  - README breve (o note) con: cosa fa la demo, come eseguirla in locale, limiti noti

Vincoli importanti (ripasso “da recruiter”):
  - path deploy-safe (NO `C:/Users/...`) → usa `__file__` + `os.path.join`
  - niente import strani o dipendenze inutili
  - mostrare chiaramente le scale: prob (0–1) vs score (0–100)
  - disclaimer motivi_top3: spiegazione del modello, non causalità
"""


# ==========================================================================
# QUIZ D'INGRESSO — Deploy & packaging (5 domande secche)
# ==========================================================================
#
# 1) V/F: “Se funziona in locale, funzionerà uguale in cloud.” Motiva.
# Falso, ci devono essere alcuni accorgimenti per renderla fruibile in cloud: path deploy safe senza path assoluti, nessuna dipendenza inutile, file requirementes.txt per installare tutte le librerie utilizzate nell'esecuzione del file.

# 2) Trova l’errore: path assoluto nel read_csv.
# il path assoluto non permette all'applicazione di essere fruibile in macchine diverse. Bisogna prevedere che ogni macchina a un suo filesystem, sia per composizione che per tipologia di sintassi untilizzata nell'esprimere i path, e dunque dobbiamo utilizzare la libreria os per generare path fruibili in tutti gli ambienti.

# 3) Completa: file obbligatori minimi per Streamlit Cloud: requirements.txt, app_streamlit_da_zero.py, file che l'app utilizza per girare (es. file mock).

# 4) Feynman: cos’è `requirements.txt` e perché serve in deploy?
# il requirements.txt è quel file dove sono inserite tutte le librerie che la nostra app utilizza per funzionare. In questo modo, installandolo, chiunque scarichi la nosta app avrà tutte le dipendenze necessarie per farla girare senza problemi.

# 5) Trova il rischio: import non usati / dipendenze extra → che problema crea?
# Si rischia di generare confusione, e lanciare errori nel momento in cui magari si ha una dipendenza dichiarata a una libreria non installata. Inoltre aumentano il tempo necessasario per la build, e si ci espone a più attacchi e alla necessasita' di maggiore manutenzione, oltre che a possibili conflitti tra diverse versioni.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #16 (scala prob 0–1 vs score 0–100)
# ==========================================================================
#
# Micro-check prima del deploy:
# - In UI si vede chiaramente quale valore è 0–1 e quale è 0–100?
# - Hai almeno una label esplicita con "(0–1)" e "(0–100)"?
#
# Scrivi qui: 1 riga di testo UI che evita confusione di scala.
# la prob alterata è espressa in una scala da 0 a 1. Lo score genuinita è invece espresso in scala a 0 a 100.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #17 (drop colonne reali)
# ==========================================================================
#
# Micro-check prima del deploy:
# - In `X_una_pratica_da_id`: stai droppando ESATTAMENTE `pratica_id` e `y_alterato`?
# - Se cambi dataset, dove lo aggiorni (una funzione sola, non 10 punti)?
# il drop avviene all'interno della funzione split_X_y. Se cambio dataset e target, basta modificarlo li.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #18 (recall vs precision)
# ==========================================================================
#
# Micro-check prima del deploy:
# - In UI mostri recall test. Sai dire in 1 riga cos’è il FN nel tuo dominio?
# Il FN nel mio dominio sono tutte quelle pratiche alterate che invece passano come genuine


# ==========================================================================
# STEP 7.1 — “Pulizia deploy”: dipendenze e import
# ==========================================================================
# COSA FARE (tu):
# - apri `modulo_02_ml/app_streamlit_da_zero.py`
# - rimuovi import non usati o sospetti (es. roba di scipy che non serve)
# - assicurati che il file giri in locale dopo la pulizia
#
# Checklist:
# [x] nessun import inutilizzato
# [x] nessun import “strano” che non serve alla demo
# [x] `python -m streamlit run modulo_02_ml/app_streamlit_da_zero.py` ok
#


# ==========================================================================
# STEP 7.2 — `requirements.txt` allineato
# ==========================================================================
# COSA FARE (tu):
# - apri `requirements.txt` nella root
# - verifica che contenga (almeno): streamlit, pandas, numpy, scikit-learn
# - se hai aggiunto dipendenze “accidentali”, toglile
#
# Nota: in cloud, Streamlit installa SOLO ciò che c’è in requirements.
#


# ==========================================================================
# STEP 7.3 — Push su GitHub (repo pubblico o accessibile a Streamlit Cloud)
# ==========================================================================
# COSA FARE (tu):
# - fai commit delle modifiche (se non l’hai già fatto)
# - push su GitHub
#
# Domanda: perché serve push? (risponditi in 1 riga)
#


# ==========================================================================
# STEP 7.4 — Creazione app su Streamlit Cloud
# ==========================================================================
# COSA FARE (tu):
# - vai su Streamlit Community Cloud
# - collega GitHub
# - seleziona repo + branch
# - imposta come “Main file path”:
#       modulo_02_ml/app_streamlit_da_zero.py
#
# Se fallisce:
# - leggi i log: spesso sono FileNotFound (path) o requirements mancanti
#


# ==========================================================================
# STEP 7.5 — Smoke test post-deploy (5 minuti)
# ==========================================================================
# COSA FARE (tu):
# - apri l’URL e prova:
#   [x] cambia pratica_id → output cambia (prob/score/semaforo)
#   [x] motivi_top3 visibili e con segno
#   [x] CV media±std visibile
#   [x] recall test visibile
#   [x] nessun errore nei log
#
# Scrivi qui l’URL finale della demo:
# URL: https://appappdazeropy-g5tde3wvxdewl5arzmeq2j.streamlit.app/

