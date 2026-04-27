# =============================================================================
# APP STREAMLIT — DA ZERO (percorso didattico di ripasso M2)
# =============================================================================
# Obiettivo:
#   Ricostruire la demo Streamlit del cap.06 SCRIVENDO TUTTO TU, step-by-step.
#   Ogni STEP qui sotto spiega COSA fare e PERCHÉ, ma NON ti dà la soluzione.
#
# Come usarlo:
#   - Leggi lo step, prova a scrivere il codice nella riga indicata.
#   - Salva il file: Streamlit farà rerun.
#   - Quando uno step è rotto, l'errore ti guida: leggi stack trace + commenti.
#   - Se sei bloccato su uno step, guarda il commento "SUGGERIMENTI" (solo hint).
#
# Regola d'oro di questo percorso:
#   NON copiare da `app_streamlit.py` o dal cap.06. Se guardi lì, stai "barando":
#   il valore didattico è nel rifarlo a memoria (retrieval practice).
#
# Concetti che questo percorso ti fa ripassare (cap.06 + M2):
#   - scale: prob_alterato (0–1) vs score_genuinita (0–100)   (Lacuna #16)
#   - drop colonne reali: "pratica_id", "y_alterato"           (Lacuna #17)
#   - recall vs precision                                      (Lacuna #18)
#   - Pipeline (StandardScaler + LogisticRegression) → no leakage
#   - CV sul TRAIN (media ± std), il test è arbitro finale
#   - predict_proba su UNA pratica: shape 2D + indice [0, 1]
#   - spiegabilità "onesta": contributi per pratica + disclaimer
#   - UI Streamlit: rerun, widget, cache_data vs cache_resource, path deploy-safe
#
# Percorso consigliato (fai gli STEP in questo ordine, uno per volta):
#   STEP 0  → 1 → 2 → 3a → 3b → 4a → 4b → 5a → 5b → 6 → 7.1 → 7.2 → ... → 7.8
#   Dopo ogni STEP salva il file e controlla che non ci siano errori Python.
# =============================================================================


# =============================================================================
# PRONTUARIO TRANELLI PERSONALIZZATI (leggere PRIMA di iniziare)
# =============================================================================
# Non sono "consigli generici": sono errori che HAI GIÀ FATTO in questo capitolo
# (fonte: diario M02_C06). Tenerli davanti riduce lo stesso errore al 50%.
#
# [T1] Scale: prob (0–1) vs score (0–100)                   (Lacuna #16 🔴)
#   - se vedi un numero 0.x in un posto chiamato "score", c'è un bug di scala.
#   - label UI: mostra sempre "(0–1)" o "(0–100)" accanto al valore.
#
# [T2] drop: COLONNE, non righe                              (Lacuna #17 🔴)
#   - su DataFrame scrivi SEMPRE `drop(columns=[...])` (non `drop([...])`).
#   - attenzione al typo: `columns`, non `colums`.
#
# [T3] Nomi colonne reali del dataset                        (Lacuna #17 🔴)
#   - feature drop: "pratica_id" e "y_alterato" (NON "id" / "target").
#
# [T4] Recall = TP / (TP + FN), NON (TP + FP)                (Lacuna #18 🔴)
#   - in controllo documentale, il FN è più grave del FP
#     (frode non intercettata).
#
# [T5] Classe vs istanza
#   - NON scrivere `("scaler", StandardScaler)` → passi la CLASSE.
#   - serve ISTANZIARE: `StandardScaler()`.
#
# [T6] Attributo vs chiamata
#   - `X.columns` è un attributo (non lo chiami), `X.columns.tolist()` ok.
#   - `X.columns()` è SBAGLIATO (TypeError).
#
# [T7] `to_frame()` è della Series, non del DataFrame
#   - se hai già un DataFrame 2D (1×N), NON chiamare `to_frame().T`: crasha.
#   - `to_frame()` ti serve solo se parti da una Series 1D.
#
# [T8] predict_proba su UNA pratica
#   - input 2D (DataFrame 1×N), NON 1D (Series).
#   - output 2D: matrice 1×2. La probabilità di "alterato" è in [0, 1].
#     `[0]` da solo ti dà l'intera riga [p0, p1]: ti serve `[0, 1]`.
#
# [T9] Cross-validation: pipeline NON fit
#   - a `cross_val_score` passa una pipeline "fresca" (non fit-tata fuori).
#   - è la CV che deve fare `fit` dentro ogni fold: SOLO così eviti leakage.
#   - NON riusare `allena_pipe_cached` qui dentro (quella fa già fit).
#
# [T10] Parametro scoring
#   - `cross_val_score(..., scoring="recall")`, non `score="recall"`.
#
# [T11] Motivi top3: mantieni il SEGNO
#   - NON fare `contrib.abs().sort_values(...)`: perdi il segno.
#   - idioma Pandas: `contrib.sort_values(key=lambda s: s.abs(), ascending=False).head(3)`
#   - segno POSITIVO = spinge verso alterato; NEGATIVO = verso genuino.
#
# [T12] Test set = arbitro finale (una volta)
#   - la CV si calcola sul TRAIN.
#   - la recall sul test si calcola UNA volta alla fine, non per tuning.
#
# [T13] Cache giusta
#   - `@st.cache_data`  → output dati (DataFrame, array, numeri).
#   - `@st.cache_resource` → oggetti "vivi" e pesanti (modello addestrato, connessioni).
#   - passa gli iperparametri come ARGOMENTI, non come variabili globali,
#     altrimenti la cache non capisce che va invalidata.
#
# [T14] Path deploy-safe
#   - NO path assoluti (`C:/Users/...`): in cloud non esistono.
#   - costruisci i path da `__file__` con `os.path.join`.
# =============================================================================


# =============================================================================
# CHECKPOINT PRIMA DI INIZIARE — auto-verifica concettuale (non scrivere codice)
# =============================================================================
# Rispondi mentalmente (anche solo a te stesso, velocemente):
#   Q1) Se prob_alterato = 0.62, qual è score_genuinita?
#   Q2) Perché serve `Pipeline` e non `scaler.fit_transform(X)` prima della CV?
#   Q3) Quali colonne TOGLI per ottenere X? (nomi esatti del nostro dataset)
#   Q4) `cross_val_score` ritorna un numero o un array? quanti valori se cv=5?
#   Q5) Perché mostrare media ± std è più "onesto" di un singolo recall sul test?
#   Q6) Quando vuoi `@st.cache_data` e quando `@st.cache_resource`?
#
# Se una di queste ti suona "hmm" → rivedila nel cap.06 PRIMA di partire.
# =============================================================================


# =============================================================================
# STEP 0 — IMPORT
# =============================================================================
# COSA FARE:
#   Importa qui tutto quello che ti serve. Tocca a te capire cosa serve.

import os
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Nota: questo file è un percorso "da zero".
# Non importiamo funzioni dalla demo già pronta (`app_streamlit.py`), altrimenti salti l'esercizio
# e in più rischi errori di import se `modulo_02_ml` non è un package.



# =============================================================================
# STEP 0.1 — CONFIG PAGINA
# =============================================================================

st.set_page_config(page_title='App Streamlit da Zero', layout='wide')

# =============================================================================
# STEP 0.2 — PATH DEPLOY-SAFE
# =============================================================================
# DOMANDA DI RIPASSO:
#   - cosa succederebbe in deploy con un path assoluto del tuo PC?
# in deploy, se qualcuno prova a utilizzare l'app dove sono stati definiti dei path assoluti, il programma, aperto su una macchina in cui i percorsi sono diversi, non riuscirebbe a trovare correttamente i path delle risorse

FILE_PATH = os.path.dirname(__file__)
CSV_PATH = os.path.join(FILE_PATH, "dati", "pratiche_genuinita_mock.csv")

# =============================================================================
# STEP 1 — carica_pratiche(csv_path) → DataFrame
# =============================================================================
# DOMANDA DI RIPASSO:
#   - `@st.cache_data` vs `@st.cache_resource`: quando usi uno e quando l'altro?
# Utilizziamo cache_data nel caso in cui si tratti di dati (es. DataFrame, Series ecc.) mentre usiamo cache_resources nel caso di oggetti pesanti (es. Modelli addestrati, Scaler ecc.)

@st.cache_data
def carica_pratiche(csv_path) -> pd.DataFrame:
    return pd.read_csv(csv_path)

# =============================================================================
# STEP 2 — split_X_y(pratiche) → (X, y)
# =============================================================================
# DOMANDA DI RIPASSO:
#   - cosa cambia tra drop(["a","b"]) e drop(columns=["a","b"])?
# il primo si usato su una series droppa le etichette selezionate, mentre su un dataframe droppa provando le etichette di riga, il secondo in un dataframe selezione invece le colonne

def split_X_y(pratiche) -> tuple[pd.DataFrame, pd.Series]:
    X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
    y = pratiche['y_alterato']
    return (X, y)

# =============================================================================
# STEP 3a — allena_pipe_cached(X_train, y_train, C, max_iter, random_state)
# =============================================================================
# DOMANDE DI RIPASSO:
#   - se cambi `C` e la cache non cambia, perché? (hint: argomenti → chiave)
# non sto passando la c tramite argomento
#   - perché usare Pipeline invece di scalare a mano `X_train`?
# così abbiamo sempre la certezza che il modello si addestra solo sul train, e non rischiamo di fare leakage

@st.cache_resource
def allena_pipe_cached(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    C: float,
    max_iter: int,
    random_state: int
    ) -> Pipeline:
    
    pipe = Pipeline(
        steps=[
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=max_iter, C=C, random_state=random_state))
            ]
        )
    return pipe.fit(X_train, y_train)

# =============================================================================
# STEP 3b — cv_recall_cached(X_train, y_train, C, random_state) → np.ndarray
# =============================================================================
# DOMANDA DI RIPASSO:
#   - cosa restituisce `cross_val_score`? (hint: un numero o tanti numeri?)
# cross_val_score restituisce un np.array
@st.cache_data
def cv_recall_cached(X_train, y_train, C, random_state) -> np.ndarray:
    pipe = Pipeline(
        steps=[
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=1000, C=C, random_state=random_state))
            ]
        )
    kfold = StratifiedKFold(n_splits=5, random_state=random_state, shuffle=True)
    score = cross_val_score(
        pipe,
        X_train,
        y_train,
        cv=kfold,
        scoring="recall"
    )
    return score


# =============================================================================
# STEP 4a — X_una_pratica_da_id(pratiche, pratica_id) → DataFrame (1, n_feature)
# =============================================================================
# DOMANDA DI RIPASSO:
#   - perché `predict_proba` si rompe con input 1D? (hint: "shape")
# perchè l'imput deve essere una matrice 2D, anche se si tratta di una sola riga di una dataframe.

def X_una_pratica_da_id(pratiche, pratica_id) -> pd.DataFrame:
    X_una = pratiche.loc[pratiche['pratica_id'] == pratica_id]
    
    if X_una.shape[0] == 0:
        raise ValueError("ID non trovato")
    if X_una.shape[0] > 1:
        raise ValueError("ID duplicato: più righe trovate")
    return X_una.drop(columns=['pratica_id', 'y_alterato'])

# =============================================================================
# STEP 4b — prob_alterato_da_pipe(pipe, X_una) → float in [0, 1]
# =============================================================================
# DOMANDA DI RIPASSO:
#   - se usassi `predict(...)` invece di `predict_proba(...)` cosa perdi?
# vedrei solo la classe di appartenenza definita a seconda della soglia impostata, non vedrei le probabilita alterato e lo scoring genuinita.

def prob_alterato_da_pipe(pipe, X_una) -> float:
    return float(pipe.predict_proba(X_una)[0, 1])

# =============================================================================
# STEP 5a — score_genuinita_da_prob(prob_alterato) → float in [0, 100]
# =============================================================================
# DOMANDA DI RIPASSO:
#   - se prob_alterato = 0.3, quanto vale score_genuinita? => 70
#   - se score_genuinita = 55, quanto vale prob_alterato? => 0.45
def score_genuinita_da_prob(prob_alterato) -> float:
    return float((1-prob_alterato)*100)

# =============================================================================
# STEP 5b — semaforo_da_score(score, soglia_verde, soglia_giallo) → "verde|giallo|rosso"
# =============================================================================
# DOMANDA DI RIPASSO:
#   - questa funzione è LOGICA DI UI o LOGICA DI PRODOTTO?
#   - se domani cambia la policy, dove la tocchi (UI o ML)?
# logica di prodotto
# se domani cambia la policy, la si andrà nella funzione di policy, richiamata dalla UI

def semaforo_da_score(score, soglia_verde, soglia_giallo) -> str:
    if score >= soglia_verde:
        return "Verde"
    if score >= soglia_giallo:
        return "Giallo"
    else:
        return "Rosso"

# =============================================================================
# STEP 6 — motivi_top3(pipe, X_una) → list[tuple[str, float]]
#            (ESERCIZIO 5b / 7b del cap.06: contributi PER PRATICA)
# =============================================================================
# DOMANDE DI RIPASSO:
#   - perché moltiplichi `x_scaled` (non `X_una` grezzo) per `coef`?
# perchè la x scalata fornisce il valure del peso di ogni freature in un unità di misura comune a tutte le feature (un unita di misursa riferita alla loro deviazione rispetto la deviazione standard), così che i pesi siano confrontabili tra loro. In caso contrario, confrontare le feature tra di loro sarebbe come confrontare tra loro mele e ananas
#   - se in UI scrivi "questi 3 sono la CAUSA", stai mentendo. Perché?
#     (scrivi il disclaimer nello step UI dei motivi)
# perchè non sono la causa in se per se, ma i primi tre motivi che hanno portato a generare la valutazione. Sicuramente sono determinanti, ma non rispecchiano la decisione in toto. In teoria, la somma delle altre freature escluse dalla top3 potrebbe aver avuto, sommate tra loro, un peso maggior della somma delle top 3 nel terminare la classe. Inoltre sono dei pesi di un modello generati sui dati ora disponibili. Cambiando il modello o i dati, i risultati variano.
def motivi_top3(pipe, X_una) -> list[tuple[str, float]]:
    scaler = pipe.named_steps['scaler']
    model = pipe.named_steps['model']
    X_una_scaled = scaler.transform(X_una)[0]
    model_coef = model.coef_[0]
    contrib = X_una_scaled * model_coef
    motivi = pd.Series(contrib, index=X_una.columns)
    top3_motivi = motivi.sort_values(key=lambda m: m.abs(), ascending=False).head(3)
    tuple_list = []
    for k, v in top3_motivi.items():
        tuple_list.append((k, float(v)))
    return tuple_list


# =============================================================================
# STEP 7 — UI (costruzione a sotto-step)
# =============================================================================
# Idea guida:
#   - evita di scrivere tutto di fila in un blocco da 80 righe.
#   - spezza in sotto-funzioni UI come quelle ML: più ordinato, più leggibile.
#   - OGNI sotto-step qui è un pezzo della pagina.
#
# Scrivi in questo ordine (l'ordine conta: alcuni pezzi dipendono dai precedenti):
#
#   7.1) TITOLO + CAPTION
#        - st.title(...) con un nome chiaro
#        - st.caption(...) con 1 frase che spiega cosa fa la demo
#
#   7.2) SIDEBAR (iperparametri + soglie)
#        Cosa metterci (come widget):
#          - slider per C  (LogReg)          → range ragionevole, step piccolo
#          - slider per max_iter             → non è qualità, è convergenza
#          - number_input per random_state   → intero
#          - 2 slider per le soglie (0..100):
#              soglia_verde (default 85)
#              soglia_giallo (default 60)
#        Suggerimenti:
#          - tutta la sidebar va dentro un blocco `with st.sidebar:` (indentato).
#          - IMPORTANTE: la sidebar va costruita PRIMA di caricare/allenare,
#            perché i suoi valori servono a train_test_split e al training.
#          - raccogli i valori in un dict Python per passarli ai chiamanti
#            in modo ordinato (e così non riempi lo script di variabili globali).
#
#   7.3) CARICA DATI + SPLIT
#        - chiama carica_pratiche(CSV_PATH)
#        - chiama split_X_y(pratiche)
#        - fai train_test_split(..., test_size=0.2, stratify=y, random_state=...)
#        Domanda: perché stratify=y nel test split?
#
#   7.4) TRAINING + CV
#        - chiama allena_pipe_cached(...) con i parametri dalla sidebar
#        - chiama cv_recall_cached(...) e calcola media e std (numpy)
#        - renderizza la "stabilità" (es. 2 st.metric: CV Recall media, CV Recall std)
#        - aggiungi 1 FRASE TUA che spieghi cosa racconta la std della CV
#          (non copiarla da me).
#
#   7.5) SELEZIONE PRATICA
#        - selectbox con la lista di pratica_id
#        - salva la scelta in una variabile
#
#   7.6) OUTPUT PRATICA
#        - X_una = X_una_pratica_da_id(...)
#        - prob  = prob_alterato_da_pipe(...)
#        - score = score_genuinita_da_prob(prob)
#        - sem   = semaforo_da_score(score, soglia_verde, soglia_giallo)
#        - renderizzali (es. 3 colonne con st.metric per prob, score, sem)
#        - ATTENZIONE (Lacuna #16): mostra SEMPRE le unità/scale (0–1 vs 0–100),
#          così non confondi te (e il recruiter).
#
#   7.7) MOTIVI TOP3 + DISCLAIMER
#        - disclaimer (st.caption): 1 riga "onesta" che dice cosa NON sono i motivi
#          (non sono cause provate, dipendono da dati/modello, ecc.)
#        - chiama motivi_top3(pipe, X_una)
#        - renderizzali come elenco leggibile con feature + contributo CON SEGNO
#        - opzionale: colora/decora il segno (+ = verso alterato, − = verso genuino)
#
#   7.8) TEST FINALE (una volta)
#        - calcola y_pred sul TEST (pipe.predict su X_test)
#        - mostra recall_test (sklearn.metrics.recall_score)  → [T4]
#        - ricorda la formula: recall = TP / (TP + FN), non (TP + FP).
#        - aggiungi una NOTA (1 riga) sul perché il test si usa "una volta sola"  → [T12]
#
# REGOLA D'ORO UI:
#   - la UI deve solo ORCHESTRARE/MOSTRARE.
#   - se ti accorgi di scrivere logica ML dentro la UI, stoppati e sposta in funzione.




# --- 7.1 ------------------------------------------------------------------
# <<< TITOLO + CAPTION >>>
#   7.1) TITOLO + CAPTION
st.title("Demo App Score Pratica")
st.caption("questa demo simula il funzionamento di un applicazione per il controlla documentale")

# --- 7.2 ------------------------------------------------------------------
# <<< SIDEBAR: slider C / max_iter, number_input random_state, slider soglie >>>
#   7.2) SIDEBAR (iperparametri + soglie)

with st.sidebar:
    st.header("Selezione Iperparametri")
    ui = {
        "C": st.slider(
            "Iperparametro LogisticRegression: C",
            min_value=0.01,
            max_value=10.0,
            value=1.0,
            step=0.01
        ),
        "max_iter": st.slider(
            'Iperparametro LogisticRegression: max_iter',
            min_value=100,
            max_value=2000,
            value=1000,
            step=50
        ),
        "random_state": st.number_input(
            'Iperparametro LogisticRegression: random_state',
            min_value=0,
            max_value=100,
            value=42,
            step=1
            
        )
    }
    st.divider()
    st.header("Selezione Soglie")   
    ui["soglia_verde"] = st.slider(
            'Soglia Verde',
            min_value=1,
            max_value=100,
            value=85,
            step=1
        )
    
    ui["soglia_giallo"] =  st.slider(
            'Soglia Giallo',
            min_value=1,
            max_value=100,
            value=60,
            step=1
        )    

# --- 7.3 ------------------------------------------------------------------
# <<< carica pratiche, split X/y, train_test_split >>>
# Domanda: perché stratify=y nel test split?
# Perchè voglio che la classe alterato sia omogenuinamente distributita nel test così come nel train
pratiche = carica_pratiche(CSV_PATH)
X, y = split_X_y(pratiche)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=ui['random_state'], stratify=y
)

# --- 7.4 ------------------------------------------------------------------
# <<< training pipeline + CV (media, std) + render stabilità + 1 frase tua >>>
pipe = allena_pipe_cached(
    X_train,
    y_train,
    C=float(ui['C']),
    max_iter=int(ui['max_iter']),
    random_state=int(ui['random_state'])
)
cv = cv_recall_cached(
    X_train,
    y_train,
    C=float(ui['C']),
    random_state=int(ui['random_state'])
)
cv_mean = cv.mean()
cv_std = cv.std()
st.metric("CV Recall (media)", f"{cv_mean:.3f}")
st.metric("CV Recall (std)", f"{cv_std:.3f}")
st.write("La media e la deviazione della CV ci aiutano a comprendere meglio la stabilità del modello rispetto a diversi split / diverse composizioni dei dati")


# --- 7.5 ------------------------------------------------------------------
# <<< selectbox pratica_id >>>
pratica_id = st.selectbox('Pratiche', pratiche['pratica_id'].tolist())

# --- 7.6 ------------------------------------------------------------------
# <<< X_una → prob → score → semaforo → render (3 colonne) >>>
X_una = X_una_pratica_da_id(pratiche, pratica_id)
prob = prob_alterato_da_pipe(pipe, X_una)
score = score_genuinita_da_prob(prob)
sem = semaforo_da_score(
    score,
    soglia_verde=int(ui['soglia_verde']),
    soglia_giallo=int(ui['soglia_giallo'])
)

col_1, col_2, col_3, col_4 = st.columns(4)
with col_1:
    st.metric('Pratica', f"{pratica_id}")
with col_2:
    st.metric('Prob Alterato => 0 - 1', f"{prob:.3f}")
with col_3:
    st.metric('Score Genuinita => 0 - 100', f"{(score/100):.2f}")
with col_4:
    st.metric('Semaforo', f"{sem}")

# --- 7.7 ------------------------------------------------------------------
# <<< disclaimer + motivi_top3 + render lista con segno >>>
st.divider()
st.header('Top 3 Motivi')
st.caption("I pesi del modello sono generati sui dati ora disponibili. Cambiando il modello o i dati, i risultati variano.")
mot_top3 = motivi_top3(pipe, X_una)
for i, v in mot_top3:
    st.write(f"{str(i):<25}  => {v:+.3f} {'verso genuino' if v < 0 else 'verso alterato'}")
    
# --- 7.8 ------------------------------------------------------------------
# <<< y_pred su TEST + recall_test + nota sul "test si usa una volta" >>>

y_pred_test = pipe.predict(X_test)
recall_test = recall_score(y_test, y_pred_test)
st.divider()
st.subheader('Test Recall')
st.metric('Punteggio', round(recall_test, 3))
st.caption('Il test, in quanto è un arbitro imparziale, viene eseguito una sola volta')
# =============================================================================
# FINE PERCORSO
# =============================================================================
# Checklist finale (spunta quando l'hai fatto DAVVERO tu):
#   [x] STEP 0   — import + config + path deploy-safe
#   [x] STEP 1   — carica_pratiche
#   [x] STEP 2   — split_X_y
#   [x] STEP 3a  — allena_pipe_cached
#   [x] STEP 3b  — cv_recall_cached
#   [x] STEP 4a  — X_una_pratica_da_id
#   [x] STEP 4b  — prob_alterato_da_pipe
#   [x] STEP 5a  — score_genuinita_da_prob
#   [x] STEP 5b  — semaforo_da_score
#   [x] STEP 6   — motivi_top3 (con segno!)
#   [x] STEP 7   — UI completa (7.1 → 7.8)
#
# Quando sei arrivato in fondo, riesegui:
#   python -m streamlit run modulo_02_ml/app_streamlit_da_zero.py
#
# Poi confronta MENTALMENTE quello che hai scritto con `app_streamlit.py`
# (NON durante lo sviluppo): è il momento "retrieval + confronto".
