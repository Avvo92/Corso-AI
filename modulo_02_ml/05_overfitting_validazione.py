"""
============================================================================
MODULO 2 — CAPITOLO 05: Overfitting, validazione e generalizzazione
============================================================================

Prodotto (M10 — Controllo Documentale AI):
- Un modello con recall alto sulle pratiche **già viste** in training non basta:
  serve comportamento stabile su pratiche **nuove** (stesso spirito di
  `score_genuinita` e `semaforo` calibrati su dati reali, non "memorizzati").

Analogia:
- Immagina di studiare le domande dell'esame a memoria sul libro: rispondi bene
  sulle stesse pagine (training), ma in classe arrivano domande leggermente
  diverse (mondo reale). L'overfitting è un po' quello: il modello impara
  il rumore e le peculiarità del train invece del pattern utile.

Confronto web / Laravel:
- Validare un form solo in locale con dati finti ≠ provarlo con utenti reali.
- In ML: metriche sul **test** (mai usato per scegliere iperparametri) sono
  l'analogo del "staging" prima della produzione.

Dataset (dove indicato negli esercizi):
- `dati/pratiche_genuinita_mock.csv` — target `y_alterato` (0=genuino, 1=alterato).
- **Attenzione dimensione / qualità**: il mock ha **~640 pratiche** (generabile con
  `dati/genera_pratiche_genuinita_mock.py`), con casi limite e **poche etichette rumorose**
  volutamente — più realistico, ma più duro per il modello. In produzione servono volumi
  maggiori e tracciamento delle label. I numeri (accuracy, recall
  per fold) possono **saltare** tra un run e l’altro se cambi `random_state` o il seed;
  non sono “legge fisica”, ma **illustrano** gap train-test e utilità della **CV**
  (media ± std) rispetto a un singolo split. Su dataset reali più grandi le curve si
  stabilizzano.

Struttura didattica:
- Sezioni **📖 TEORIA** (commenti narrativi): quadro train/validation/test, varianza
  delle stime, CV vs test, metrica di scoring, nested CV (accenno), policy vs modello,
  lettura della validation curve. Da leggere insieme alle PARTI 1–5.
"""

import os
from joblib.memory import re
import pandas as pd
import numpy as np
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold,
    validation_curve,
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ==========================================================================
# 🔁 RINFORZO MIRATO — da cap.04 mini-esercizio 4 (zona "indecisa")
# ==========================================================================
#
# Al mini-es.4 avevi collegato l’indecisione allo score di genuinità in %.
# Per la regressione logistica, la zona più incerta è quando prob_alterato
# è vicina a 0.5 (cioè lo score (1 - prob_alterato)*100 è vicino a 50),
# non quando è "60%" da solo: 60% di score corrisponde a prob_alterato ≈ 0.40.
#
# Prova subito (rispondi in commento):
# 1) Se prob_alterato = 0.45, qual è score_genuinita? => 0.55
# 2) Se score_genuinita = 60, qual è prob_alterato? => 0.40
#
# Nel cap.05 userai la stessa logica: valutare il modello su dati tenuti da parte
# mostra se le probabilità sono calibrate o solo "memorizzate" dal train.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Data leakage (cap.04 es.5)
# ==========================================================================
#
# Prima di ottimizzare max_depth o fare cross-validation, ripeti il controllo:
# X non deve contenere y_alterato né colonne derivate dal target.
#
# Micro-check: scrivi la riga Pandas corretta per droppare pratica_id e target.
# X = df.drop(columns=['id', 'target']) => concetto astratto
# pratiche = pd.read_csv(path_file_mock) => dove "path_file_mock" è il percorso del file mock
# X = pratiche.drop(columns=['pratica_id', 'y_alterato'])



# ==========================================================================
# 🔁 RINFORZO MIRATO — Fit scaler solo sul train (sempre)
# ==========================================================================
#
# StandardScaler: fit su X_train, transform su X_train e X_test.
# Se fitti su tutto il dataset prima dello split, le statistiche "vedono"
# il test e la valutazione è ottimisticamente sbagliata (leakage di preprocessing).


# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da cap.04 (classificazione e metriche)
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Recall alto sul training set garantisce un buon modello in produzione."
# Rispondi V o F e spiega in 2 righe.
# Falso. Il recall alto sul training non ci dice molto sulla validità del modello. Per avere un giudizio affidabile dobbiamo confrontarlo con il recall prodotto dal test. A quel punto avremo sia un indicatore della recall del modello su dati che non ha mai visto, e dalla forbice tra i due indicatori avremo anche un indicazione se il modello soffre ad esempio di overfitting (qualora recall alto su train e basso su test)
#
# DOMANDA 2 — Definizione:
# Cosa misura il recall sulla classe 'alterato' (1)? Perché è spesso prioritaria
# nel controllo documentale?
# la recall ci indica quanti falsi negativi il nostro modello produce, quindi quanti 'alterato' (1) il modello si lascia sfuggire sul totale dei 'alterato' (1). Per fare un esempio, su 10 ladri che hanno cercato di rubare, l'antifurto quante volte ha suonato? Nel controllo documentale è fondamentale, perchè un falso negativo (ossia una pratica falsa che sfugge alla maglia del nostro controllo) ci espone a rischio potenzialmente molto gravi, come frodi.

#
# DOMANDA 3 — Completa:
# predict_proba per il binario restituisce due colonne: la colonna 1 è
# P(y = ___) e da lì ricavi prob_alterato e poi score_genuinita = (1 - prob_alterato) * ___.
# 'y_alterato', 100

# DOMANDA 4 — Trova l'errore concettuale:
#   scaler.fit(X)  # X = intero DataFrame prima dello split
#   X_train, X_test, y_train, y_test = train_test_split(X, y, ...)
#   X_train_s = scaler.transform(X_train)
# Spiega cosa c'è che non va.
# Invece di fare il fit dello Scaler sulla X, bisognava fare prima lo split in train e test, e poi fare il fit dello scaler sulla X_train. in questo modo si stanno scalando le feature ad un unità di misura basandoci su una deviazione std la quale è stata prodotta anche sulla base dei dati che useremo per il test. Il termine corretto dell' errore è processing leakage.
#
# DOMANDA 5 — Vero/Falso:
# "È corretto provare 20 valori di max_depth guardando ogni volta il recall sul
# test set e tenere il migliore." V o F?
# Falso, lo si deve fare sul validation Set. In questo modo il test rimane solo come esame finale, poichè non deve avere nessuna correlazione con le scelte che abbiamo fatto per scegliere il modello migliore, ma deve essere "arbitro imparziale" a tutti gli effetti.
#
# DOMANDA 6 — Prevedi l'output (ordine di grandezza):
# Un DecisionTreeClassifier(max_depth=None) su un dataset **piccolo** rispetto alla
# complessità dell'albero: l'accuracy sul training sarà tipicamente vicina a ___ %
# e sul test potrebbe essere più ___ (più bassa / più alta / uguale)?
#100, bassa
#
# DOMANDA 7 — 💬 Spiega con parole tue:
# Perché l'accuracy da sola può essere ingannevole su un dataset con molte
# pratiche genuine e poche alterate?
#
# Scrivi le risposte qui sotto:
# Immaginiamo un dataset di 100 pratiche, di cui 90 genuine e 10 alterate. Qualora il modello si limitasse a darle tutte per genuine, si avrebbe un accuracy del 90%: ((TN + TP) / (TN + TP + FP + FN)) * 100 = (90 / 100) * 100 = 90 %. In generale, un valore del 90% potrebbe farci pensare che il modello sia molto efficace, ma se andassimo a vedere la recall dello stesso modello (TP / (TP + FP) => 0 / 0 => 0% (non possibile matematicamente, ma corretto per convenzione)) ci renderemmo conto che il modello in realtà è sostanzialmente inutile, in quando è come un allarme rotto che non scatta mai. L'accuracy è in realtà solo un specchietto delle addole, dovuto al fatto che in generale le pratiche alterate sono poche rispetto al totale.


# ==========================================================================
# 📖 TEORIA — Tre porzioni, tre domande diverse (quadro prima della Parte 1)
# ==========================================================================
#
# In laboratorio ti abitui a tre "mondi" di dati, anche se a volte usi solo due
# nomi (train e test). La confusione nasce quando mescoli **il compito** che fai
# su ciascuno.
#
# Sul **training** rispondi a: "Il modello riesce ad adattarsi a questi esempi?"
# È la fase di **fit**: stai minimizzando l'errore su un insieme fisso. Un modello
# troppo potente può abbassare l'errore sul train quasi a zero senza imparare ciò
# che ti serve sulle pratiche nuove: è lì che entra il discorso di overfitting.
#
# Sulla **validation** (un hold-out separato dal train, oppure le parti tenute da
# parte dentro la cross-validation sul solo train) rispondi a: "Tra modelli o
# impostazioni diverse, quale **scelta** sembra migliore?" Qui confronti
# `max_depth`, `C`, a volte anche soglie operative, senza ancora toccare il test
# finale. Stai facendo **selezione di modello** o di iperparametri: è un processo
# di prova e confronto, non la misura definitiva del rischio in produzione.
#
# Sul **test** (tenuto fuori da fit e da tuning) rispondi a: "Dopo aver congelato
# le scelte, quanto è alto l'errore su dati che non ho usato per decidere nulla?"
# Quella stima è quella più vicina all'idea di **generalizzazione** onesta, purché
# tu non ci torni sopra centinaia di volte per "aggiustare" il modello. Se ogni
# volta che non ti piace un numero cambi iperparametri guardando il test, il test
# smette di essere indipendente: è il cosiddetto **data snooping** (sbirciare i
# dati che dovevano restare imprevedibili).
#
# In sintesi: train = imparare; validation/CV sul train = **scegliere**; test =
# **stimare** una volta, con regole chiare. I prossimi blocchi rendono operative
# queste frasi con numeri e API.


# ==========================================================================
# PARTE 1 — Errore su train vs errore su test (generalizzazione)
# ==========================================================================
#
# Il modello impara dai dati di training. Se misuri l'accuracy (o F1) **solo**
# sul train, stai chiedendo: "quanto è bravo a ripetere ciò che ha già visto?"
# La domanda giusta per il prodotto è: "quanto è bravo su pratiche **nuove**?"
#
# **Overfitting**: il modello si adatta troppo ai dettagli del train (anche al
# rumore) e peggiora sul test. Sintomo tipico: accuracy train alta, test bassa.
#
# **Underfitting**: modello troppo semplice (non cattura i pattern). Sintomo:
# accuracy train e test entrambe basse.
#
# Nel documentale: un albero molto profondo può "memorizzare" le pratiche del
# train; su nuove pratiche i falsi negativi sugli alterati possono aumentare.

print("\n" + "=" * 60)
print("PARTE 1 — Idea di generalizzazione")
print("=" * 60)

# Stessi nomi del cap.04 (`pratiche`, X, y, X_train, …) + prefisso `_demo_` = solo codice dimostrativo.
_path_file_demo = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
_demo_pratiche = pd.read_csv(_path_file_demo)
_demo_X = _demo_pratiche.drop(columns=["pratica_id", "y_alterato"])
_demo_y = _demo_pratiche["y_alterato"]
_demo_X_train, _demo_X_test, _demo_y_train, _demo_y_test = train_test_split(
    _demo_X, _demo_y, test_size=0.2, random_state=42, stratify=_demo_y
)
_demo_clf_albero_profondo = DecisionTreeClassifier(max_depth=None, random_state=42)
_demo_clf_albero_profondo.fit(_demo_X_train, _demo_y_train)
_demo_accuracy_train = accuracy_score(
    _demo_y_train, _demo_clf_albero_profondo.predict(_demo_X_train)
)
_demo_accuracy_test = accuracy_score(
    _demo_y_test, _demo_clf_albero_profondo.predict(_demo_X_test)
)
_demo_numero_righe_train = len(_demo_y_train)
_demo_numero_righe_test = len(_demo_y_test)
print(
    f"Esempio (righe train={_demo_numero_righe_train}, righe test={_demo_numero_righe_test}): "
    "albero max_depth=None"
)
print(
    f"  accuracy train ≈ {_demo_accuracy_train:.2%} | test ≈ {_demo_accuracy_test:.2%}"
)
print(
    "(Con pochi campioni il train spesso è altissimo: gap train-test = segnale di "
    "complessità eccessiva o rumore; ripeti il check con CV sotto.)"
)


# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Guarda i due numeri stampati sopra: il gap train-test è grande?
# 2) In una frase: cosa significa "generalizzare" in questo contesto?
# Scrivi qui sotto:
# c'è una differenza di quasi il 7% tra train e test.
# Generalizzare significa ottenere buoni risultati sul test set, che il modello non ha mai visto


# ==========================================================================
# 📖 TEORIA — Dopo la demo Parte 1: stima rumorosa e costo degli errori
# ==========================================================================
#
# **Un solo split** train/test è comodo ma è anche una **singola estrazione**:
# con poche righe, il test può contenere per caso molti alterati o pochissimi, e
# il recall che misuri salta. Non è che la metrica sia "sbagliata": è **instabile**.
# Per questo più avanti userai la cross-validation: non ti dà la verità assoluta,
# ma una media e una dispersione tra fold, cioè un'idea di quanto il punteggio
# dipenda dalla particolare suddivisione.
#
# Sul **controllo documentale**, il recall sulla classe "alterato" misura quante
# frodi vere intercetti tra tutte quelle presenti. Un **falso negativo** (alterato
# classificato come genuino) è spesso il rischio più temuto in revisione: una
# pratica sospetta che passa inosservata. Per questo, quando valuti modelli, è
# sensato allineare la **metrica in validazione** a ciò che il prodotto deve
# proteggere: non usare l'accuracy "per abitudine" se il dominio è sbilanciato o
# se il costo degli errori non è simmetrico.


# ==========================================================================
# PARTE 2 — Train / Validation / Test (e perché non si "tuna" sul test)
# ==========================================================================
#
# - **Train**: dove il modello impara i pesi.
# - **Validation** (o dev): dove confronti iperparametri (max_depth, C della
#   logistica, soglie di business derivate da metriche) senza toccare il test.
# - **Test**: valutazione finale, una tantum (o raramente), per stimare
#   l'errore di generalizzazione in modo onesto.
#
# Se scegli max_depth guardando ripetutamente il test, il test "perde la
# verginità": finisce per essere indirettamente nel training della tua scelta
# (data leakage da decisione umana). Per questo si usa un validation set o
# la cross-validation sul **solo** train.

print("\n" + "=" * 60)
print("PARTE 2 — Dove ottimizzare gli iperparametri")
print("=" * 60)
print(
    "Regola pratica: tuning su train (CV) o validation → report finale su test."
)


# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Riordina: "scelta max_depth" vs "valutazione finale sul test" — quale viene prima?
# 2) Nel prodotto: perché fissare soglie semaforo guardando solo il test è rischioso?
# Scrivi qui sotto:
# Viene prima la scelta della max_depth, e poi la valutazione finale tramite test.
# Perchè si stanno ottimizzando le soglie guardando i dati del test, cosa che invece andrebbe fatta nella validation o nella CV


# ==========================================================================
# 📖 TEORIA — Dopo la Parte 2: perché il test non è "una validation più grande"
# ==========================================================================
#
# La validation (o la CV che lavora **dentro** il train) serve a **ottimizzare**
# una scelta tra alternative già definite: modelli, profondità dell'albero,
# regolarizzazione, a volte soglie se le tratti come iperparametri su un set di
# sviluppo. Il **test** serve a **quantificare** l'errore quando quella scelta è
# stata fissata. Se usi il test per decidere quale alternativa tenere, la tua
# decisione si adatta anche al rumore presente in quel sottoinsieme: la stima
# finale diventa ottimistica, perché hai già "imparato" dal test cosa funzionava.
#
# Nel prodotto succede lo stesso se calibri il **semaforo** o le soglie guardando
# solo l'ultima valutazione sul test: stai adattando la policy ai dati che
# avrebbero dovuto simulare il mondo nuovo. La pratica sana è tenere un **blocco
# validation** (o CV) per le decisioni ripetute e un **test** per la fotografia
# finale, oppure rinnovare il test solo quando collezioni **nuovi** dati etichettati.


# ==========================================================================
# PARTE 3 — Cross-validation (k-fold) sul train
# ==========================================================================
#
# Con pochi dati, un singolo split train/val può essere fortunato o sfortunato.
# La **k-fold cross-validation** divide il train in k parti: a turno ogni parte
# fa da mini-test e il resto fa da mini-train. Ottieni k punteggi e ne fai la media.
#
# In sklearn: `cross_val_score(modello, X_train, y_train, cv=..., scoring=...)`.
# StratifiedKFold mantiene la proporzione delle classi in ogni fold (utile se
# gli alterati sono pochi).

print("\n" + "=" * 60)
print("PARTE 3 — Cross-validation")
print("=" * 60)

_demo_clf_albero_profondita_4 = DecisionTreeClassifier(max_depth=4, random_state=42)
_demo_stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
_demo_scores_recall_cv = cross_val_score(
    _demo_clf_albero_profondita_4,
    _demo_X_train,
    _demo_y_train,
    cv=_demo_stratified_kfold,
    scoring="recall",
)
print(
    "Recall (classe positiva default) su 5 fold (solo porzione train della demo): "
    f"{_demo_scores_recall_cv}"
)
print(
    f"Media recall CV: {_demo_scores_recall_cv.mean():.3f} "
    f"(+/- {_demo_scores_recall_cv.std():.3f})"
)


# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Perché cross_val_score qui usa _demo_X_train/_demo_y_train e non tutto il dataset incluso il test?
# 2) Cosa indica una deviazione standard alta tra i fold?
# Scrivi qui sotto:
# si una _demo_X_train e _demo_y_train per la cv è non su tutto il dataset per mantenere il test diviso dalla fase di addestramento e validation, lasciandolo così come arbitro imparziale. una deviazione std alta può significare ad esempio che il dataset, essendo molto contenuto in termini di dimensioni, in tra le varie configurazioni produce risultati sensibilmente diversi. 


# ==========================================================================
# 📖 TEORIA — Dopo la Parte 3: CV, test, metrica e (accenno) nested CV
# ==========================================================================
#
# La **cross-validation sul train** risponde a: "Se riparto il training su
# porzioni diverse dello stesso materiale, quanto oscillano le mie metriche?"
# Utile per confrontare modelli e capire **stabilità**. Non risponde invece a:
# "Su **esemplari mai entrati** in nessun fit, com'è l'errore?" — per quello
# serve un **test hold-out** (o dati nuovi in produzione, che sono il vero banco
# finale). Quindi CV e test **si completano**: la prima riduce l'illusione di un
# singolo split fortunato; il secondo stima l'errore con un insieme che non hai
# usato per scegliere nulla.
#
# Quando chiami `cross_val_score(..., scoring="recall")`, stai dicendo a sklearn
# quale aspetto del classificatore vuoi massimizzare **nei fold**. Scegli la
# metrica coerente con il rischio di business (qui recall sugli alterati), non
# necessariamente l'accuracy.
#
# Se un giorno farai **grid search** molto ampia su molti iperparametri, la
# selezione stessa assorbe informazione dai dati. In contesti rigidi si usa la
# **cross-validation annidata** (CV esterna per stimare l'errore, CV interna per
# scegliere i parametri): non la implementiamo in questo capitolo, ma è il
# ponte naturale verso MLOps e valutazioni più formali.


# ==========================================================================
# PARTE 4 — Bias, varianza e complessità (messaggio operativo)
# ==========================================================================
#
# - Modello **troppo semplice** → bias alto: sottoperforma ovunque.
# - Modello **troppo complesso** → varianza alta: va bene sul train, instabile sul test.
# - Obiettivo: zona intermedia dove il test (o CV) è ancora buono senza gap enorme dal train.
#
# Per gli alberi: `max_depth` basso → più semplice; `max_depth` alto o None → più
# complesso. Per la logistica: `C` più basso → più regolarizzazione (in sklearn),
# comportamento meno "nervoso" su piccoli dataset.
#
# **Stesso concetto, due leve**: limitare la complessità dell'albero e
# regolarizzare la logistica sono modi diversi di dire "non adattarti al rumore
# più di quanto i dati possano giustificare". In altri moduli incontrerai penalità
# esplicite (L1/L2): l'intuizione resta quella di **bias–variance**: troppo poco
# flex → bias; troppa flex → varianza e overfitting.

print("\n" + "=" * 60)
print("PARTE 4 — Bias-varianza (visione operativa)")
print("=" * 60)
print("Controlla gap train-test e stabilità dei fold CV prima di fidarti del deploy.")
print(
    "Collegamento pratico: albero troppo profondo → spesso alta varianza "
    "(punteggi diversi tra fold); albero troppo basso → bias alto ovunque."
)


# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Due frasi: cosa cambi prima, max_depth dell'albero o soglie del semaforo sul prodotto?
#    (Suggerimento: iperparametri modello vs policy business.)
# 2) Collega: recall alto sul train e basso sul test → che parola usa il mentor?
# 3) Guarda la tabella nella PARTE 5: a occhio, dove si vede il trade-off bias-varianza?
# Scrivi qui sotto:
# 1) Prima cambio la max_depth, facendo una cross_validation per 3/4 diversi tuning del modello. Poi, una volta identificato il modello che sembra il più efficace, aggiusto le soglie per adeguarle ai risultitati prodotti dal modello. Infine eseguo un test.
# 2) problema di over-fitting, flex-varianza
# 3) si vede a max_depth=3 un apex per quanto riguarda il recall in fase di test, dopo di che diminuisce i modo quasi lineare  


# ==========================================================================
# 📖 TEORIA — Dopo la Parte 4: iperparametri modello vs policy prodotto
# ==========================================================================
#
# **Modello** e **policy** non sono la stessa cosa. `max_depth`, `C`, tipo di
# modello sono scelte sul **come** apprendere dai dati. Soglie del semaforo,
# regole operative ("se score sotto X vai in revisione manuale") sono scelte sul
# **come** usare l'output in azienda. Entrambe vanno validate senza barare sul
# test, ma è utile non mescolare i livelli: prima tendi a stabilizzare il
# modello, poi calibri la policy su metriche e costi accettati dal dominio.


# ==========================================================================
# PARTE 5 — Validation curve (complessità vs errore, solo sul train)
# ==========================================================================
#
# `validation_curve` prova **più valori** di un iperparametro (qui `max_depth`)
# usando cross-validation **solo** su `X_train`, `y_train`. Per ogni profondità
# ottieni punteggi sui fold di training e sui fold di validazione interni alla CV
# (non il tuo test set riservato: quello resta fuori da questo blocco).
#
# Pattern tipico (non sempre monotono su dati reali piccoli):
# - train score sale (o resta alto) quando il modello si complessifica;
# - lo score di validazione sale, poi può scendere → zona dove conviene fermarsi.
#
# Questo è il parente numerico della "curva di validazione" che vedi nei tutorial.

print("\n" + "=" * 60)
print("PARTE 5 — Validation curve (demo su X_train, y_train)")
print("=" * 60)

_demo_valori_max_depth = np.arange(1, 12)
_demo_matrice_recall_train_fold, _demo_matrice_recall_valid_fold = validation_curve(
    DecisionTreeClassifier(random_state=42),
    _demo_X_train,
    _demo_y_train,
    param_name="max_depth",
    param_range=_demo_valori_max_depth,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="recall",
)

_demo_recall_medio_su_train_fold = _demo_matrice_recall_train_fold.mean(axis=1)
_demo_recall_medio_su_valid_fold = _demo_matrice_recall_valid_fold.mean(axis=1)

print("max_depth | recall medio (train fold) | recall medio (valid fold)")
print("-" * 62)
for indice_profondita, profondita_max in enumerate(_demo_valori_max_depth):
    print(
        f"   {profondita_max:2d}     |      "
        f"{_demo_recall_medio_su_train_fold[indice_profondita]:.3f}            |      "
        f"{_demo_recall_medio_su_valid_fold[indice_profondita]:.3f}"
    )
_demo_indice_profondita_migliore = int(np.argmax(_demo_recall_medio_su_valid_fold))
print(
    f"\n(Demo) Profondità con recall validazione medio massimo in questa griglia: "
    f"max_depth={_demo_valori_max_depth[_demo_indice_profondita_migliore]} "
    "— da confermare su altri seed/dataset."
)

# --- Grafico opzionale (in locale, se usi matplotlib): decommenta e salva/esegui ---
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(figsize=(7, 4))
# ax.plot(_demo_valori_max_depth, _demo_recall_medio_su_train_fold, marker="o", label="Recall train (CV)")
# ax.plot(_demo_valori_max_depth, _demo_recall_medio_su_valid_fold, marker="s", label="Recall validazione (CV)")
# ax.set_xlabel("max_depth")
# ax.set_ylabel("Recall medio sui fold")
# ax.legend()
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()


# ==========================================================================
# 📖 TEORIA — Dopo la Parte 5: cosa aggiunge la validation curve
# ==========================================================================
#
# La tabella sopra esplora più valori di `max_depth` usando solo il train della
# demo: per ogni profondità vedi come si comporta il modello su fold di
# addestramento e su fold di **validazione interna** alla CV. Quando la curva di
# validazione smette di salire o scende mentre il train resta alto, è il segnale
# classico di **eccesso di complessità** rispetto a ciò che i dati sostengono.
#
# Resta il principio già detto: anche questa analisi **non sostituisce** il test
# riservato. La validation curve ti aiuta a **dove** regolare la complessità; il
# test hold-out (o il monitoraggio su dati nuovi) ti dice ancora "com'è andata
# fuori dal laboratorio" dopo che hai congelato le scelte.


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# La cross-validation sul train può sostituire completamente un test set tenuto
# separato per la valutazione finale.
# No, il test alla fine è sempre indispensabile. La cross-validation serve solo a stabilizzare i risultati di uno score, cercando di arginare la possibilità che lo score sia stato influenzato da una composizione fortunata del set usato per il train e la validazione. Alla fine, dopo che avremo scelto in base a uno score stabilizzato, il  test ci darà eventualmente la conferma finale del fatto se siamo o meno sulla strada giusta, facendo come da "arbitro finale"
#
# DOMANDA 2 — Definizione:
# Cos'è l'overfitting in due righe?
# Si parla di overfitting quando il modello che abbiamo addestrato è divenuto troppo complesso, e invece di generalizzare impara a memoria le risposte in base ai target specifici del train set
#
# DOMANDA 3 — Trova l'errore:
#   for d in [1, 2, 3, 4, 5]:
#       clf = DecisionTreeClassifier(max_depth=d)
#       clf.fit(X_train, y_train)
#       print(d, recall_score(y_test, clf.predict(X_test)))
#   # scelgo il d col recall migliore sul test
# Stiamo a tutti gli effetti facendo tuning guardano i recall prodotti dal test. 
# per avere dati coerenti dovremmo impostare un random_state fisso, altrimenti avremmo un variabilità legata anche alla configurazione del set, e non solo dovuta alle differenti impostazioni degli iperparametri

#
# DOMANDA 4 — Completa:
# StratifiedKFold serve a mantenere la proporzione delle ___ in ogni fold.
# classi
#
# DOMANDA 5 — Prevedi:
# All'aumentare di max_depth (da 1 a molto alto), tipicamente l'accuracy sul train ___
# e sul test prima ___ poi può ___ .
# sale, sale, scendere
#
# DOMANDA 6 — 💬 Spiega con parole tue:
# Perché "guardare il test più volte per scegliere l'iperparametro" è come
# barare all'esame?
# perchè starei di fatto scegliendo le mie risposte sul voto che prenderei poi all'esame finale.In pratica si dice che sto facendo tuning su dei dati che non dovrebbero essere noti nel momento in cui sto ancora scegliendo la configurazione del modello.
#
# DOMANDA 7 — Vero/Falso:
# "Con un dataset piccolo, un singolo split train/test basta per stimare in modo
# affidabile il recall in produzione; la cross-validation non aggiunge nulla."
# V o F? Motiva in 2 righe.
# Falso. In un data-set piccolo, la probabilità di avere uno split che mal rappresenti le regole generali contenute nei dati aumenta. Dunque, la cross validation può in realtà rappresentare uno strumento prezioso per stabilizzare i valori delle metriche a cui poi ci affideremo per scegliere la giusta configurazione del nostro modello.


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================
#
# Dataset quando richiesto: `dati/pratiche_genuinita_mock.csv`
# Target: `y_alterato` (0=genuino, 1=alterato). Anti-leakage: droppa `pratica_id` e target da X.
#
# Ordine consigliato: 1 → 2 → 3 → 4 → 5 → 7 → 8; es.6 solo se vuoi il passaggio manuale
# sui fold (è lungo). La PARTE 5 del file ti mostra già l’idea della validation curve.
#

# ESERCIZIO 1 (Facile):
# 1) Carica il CSV delle pratiche, prepara X e y.
# 2) train_test_split 80/20, stratify, random_state=42.
# 3) Allena DecisionTreeClassifier(max_depth=2) e uno con max_depth=None.
# 4) Stampa accuracy train e test per entrambi (4 numeri). Commenta il gap.
#
# Scrivi qui sotto:

pratiche = pd.read_csv(os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv"))

X = pratiche.drop(columns=['y_alterato', 'pratica_id'])
y = pratiche['y_alterato']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42, stratify=y
)

clf_tree_md2 = DecisionTreeClassifier(max_depth=2, random_state=42)
clf_tree_md_none = DecisionTreeClassifier(random_state=42)

clf_tree_md2.fit(X_train, y_train)
clf_tree_md_none.fit(X_train, y_train)

print("\nEsercizio 1\n")
print("Decision Tree max_depth = 2")
print(f"Accuracy Train => {accuracy_score(y_train, clf_tree_md2.predict(X_train)):.2%}")
print(f"Accuracy Test  => {accuracy_score(y_test, clf_tree_md2.predict(X_test)):.2%}\n")

print("Decision Tree max_depth = None")
print(f"Accuracy Train => {accuracy_score(y_train, clf_tree_md_none.predict(X_train)):.2%}")
print(f"Accuracy Test  => {accuracy_score(y_test, clf_tree_md_none.predict(X_test)):.2%}\n")

# si può notare che il gap tra train e test del modello senza max_depth definita sia sostanzialmente più ampio, segno questo che il modello soffre di overfitting per via della eccessiva complessita'. Inoltre l'accuracy nel test è superiore nel modello con max_depth=2, segno che, anche un modello relativamente molto semplice è più efficace nel generalizzare rispetto al modello più complesso. 


# ESERCIZIO 2 (Medio):
# 1) Stesso split dell'es.1.
# 2) Usa cross_val_score con StratifiedKFold(5), scoring='recall', su X_train, y_train
#    per max_depth in [2, 4, 6, None] (DecisionTreeClassifier, random_state=42).
# 3) Stampa una tabella: max_depth | recall medio CV | std
# 4) Scegli il max_depth con recall medio migliore (in commento: perché NON usi il test per questa scelta?).
# Opzionale: confronta la tua tabella con l’idea della PARTE 5 (validation_curve su più profondità).
#
# Scrivi qui sotto:


print("\nEsercizio 2\n")
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
recall_medi = []
recall_std = []
depth_arr = [2, 4, 6, None]

for depth in depth_arr:
    scores = cross_val_score(
        DecisionTreeClassifier(max_depth=depth, random_state=42),
        X_train,
        y_train,
        cv=kfold,
        scoring="recall"
        )
    recall_medi.append(scores.mean())
    recall_std.append(scores.std())

table = pd.DataFrame({
    'max_depth': depth_arr,
    'recall_medio_cv': [round(x*100 ,2) for x in recall_medi],
    'std': [round(x ,3) for x in recall_std],
})

print(table)

# la profondità migliore è quella del modello con max depth 4. Abbiamo fatto questa prova solo sul train set, perchè altrimenti avremmo  in pratica scelto il modello sulla base del test, e quindi avrebbe perso il suo ruolo di arbitro finale.





# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# In 8-12 righe di commento spiega:
# - Differenza tra overfitting e underfitting (con un esempio su pratiche documentali).
# - Cosa guardi per capire se stai overfittando (due segnali).
# - Ruolo della cross-validation quando il dataset è piccolo.
# - (Bonus) Cosa aggiunge una validation curve rispetto a un solo max_depth provato a caso?
#
# Scrivi qui sotto:
#


# ESERCIZIO 4 (🔧 [REFACTORING]):
# Il codice sotto "funziona" ma viola la buona pratica di validazione.
# Riscrivilo: usa SOLO X_train, y_train per la grid su max_depth e valuta
# sul test UNA SOLA volta alla fine (o usa CV per scegliere d, poi fit sul train e metrica sul test).
#
# # CODICE DA CORREGGERE:
# # X_train, X_test, y_train, y_test = train_test_split(...)
# # best_d, best_rec = 1, 0
# # for d in range(1, 15):
# #     clf = DecisionTreeClassifier(max_depth=d, random_state=42)
# #     clf.fit(X_train, y_train)
# #     r = recall_score(y_test, clf.predict(X_test))
# #     if r > best_rec:
# #         best_rec, best_d = r, d
#
# Scrivi qui sotto:

print("\nEsercizio 4\n")
best_depth, best_recall = 1, 0

for depth in range(1, 15):
    recall_scores = cross_val_score(
    DecisionTreeClassifier(max_depth=depth, random_state=42),
        X_train,
        y_train,
        cv=StratifiedKFold(n_splits=5, random_state=42, shuffle=True),
        scoring="recall"
        )
    if recall_scores.mean() > best_recall:
        best_depth, best_recall = depth, recall_scores.mean()
best_clf_tree = DecisionTreeClassifier(max_depth=best_depth, random_state=42)
best_clf_tree.fit(X_train, y_train)       
test_recall = recall_score(y_test, best_clf_tree.predict(X_test))
print(f"Miglior Train Recall => {best_recall:.2%}")
print(f"Test Recall          => {test_recall:.2%}")

# ESERCIZIO 5 (🔍 [DEBUG]):
# Leggi il codice sotto (non eseguirlo se vedi l'errore): cosa produce di fuorviante?
# Spiega il bug in 3-4 righe e come correggere.
#
# scaler = StandardScaler()
# X_all = pd.read_csv(...).drop(columns=['pratica_id','y_alterato'])
# y_all = pd.read_csv(...)['y_alterato']
# scaler.fit(X_all)
# X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, stratify=y_all)
# X_train_s = scaler.transform(X_train)
# X_test_s = scaler.transform(X_test)
#
# Scrivi qui sotto:
# Lo scaler viene impostato su tutto il set, prima che questo venga diviso in train e test. In questo modo, la deviazione std su cui viene effettuate la trasformazione dei valori è calcolata anche sul dataset che poi verrà diviso per il  test, provocando di fatto un preprocessing leakage. di seguito il codice corretto

# scaler = StandardScaler()
# X_all = pd.read_csv(...).drop(columns=['pratica_id','y_alterato'])
# y_all = pd.read_csv(...)['y_alterato']
# X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, stratify=y_all)
# scaler.fit(X_train)
# X_train_s = scaler.transform(X_train)
# X_test_s = scaler.transform(X_test)



# ESERCIZIO 6 (Opzionale — 🔀 [INTERLEAVING] — Pandas + validazione):
# Obiettivo: capire *a mano* cosa fa k-fold (senza `cross_val_score`). Saltalo se
# preferisci: es.2 + PARTE 5 coprono lo stesso messaggio in modo più rapido.
# 1) Carica pratiche, aggiungi 'fold_id' = indice di riga modulo 5
#    (didattico — NON è StratifiedKFold e può sbilanciare le classi nei fold).
# 2) Per fold_id 0..4: train = righe con fold_id != k, test = fold_id == k;
#    allena DecisionTreeClassifier(max_depth=3, random_state=42), calcola recall sul test.
# 3) Stampa i 5 recall e la media (solo sklearn.metrics, niente CV sklearn).
# 4) Due righe: perché StratifiedKFold è preferibile a questo trucco?
# Il modo che abbiamo utilizzato non permette una stratificazione omogeneare delle classi di y_alterato. Dunque, i risultati saranno meno precisi rispetto ai valori ottenuti dallo stesso set splittato tramite StratifiedKFold
# Scrivi qui sotto:
#
print("\nEsercizio 6\n")
pratiche = pd.read_csv(os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv"))

pratiche["fold_id"] = np.arange(len(pratiche)) % 5

scores = []

for k in range(0, pratiche['fold_id'].max() + 1):
    X_train = pratiche.loc[pratiche['fold_id'] != k].drop(columns=['pratica_id', 'y_alterato'])
    y_train = pratiche.loc[pratiche['fold_id'] != k]['y_alterato']
    X_test = pratiche.loc[pratiche['fold_id'] == k].drop(columns=['pratica_id', 'y_alterato'])
    y_test = pratiche.loc[pratiche['fold_id'] == k]['y_alterato']
        
    clf_tree = DecisionTreeClassifier(max_depth=3, random_state=42)    
    clf_tree.fit(X_train, y_train)
    
    rec_score = recall_score(y_test, clf_tree.predict(X_test))
    scores.append(rec_score)
    
print(f"{[round(x*100, 2) for x in scores]}")
print(f"Media Recall => {round(np.array(scores).mean(), 4):.2%}")
    
    
    
    
    
    








# ESERCIZIO 7 (🧠 [RETRIEVAL]):
# Senza guardare la PARTE 3, riscrivi da zero:
# - import per cross_val_score e StratifiedKFold
# - 3 righe: split train/test, creazione modello DecisionTreeClassifier(max_depth=5),
#   cross_val_score con scoring='f1' su X_train, y_train, cv=StratifiedKFold(5, shuffle=True, random_state=42)
# - stampa della media
#
# Scrivi qui sotto:
#


# ESERCIZIO 8 (Prodotto — policy vs test):
# 1) Carica pratiche, split 60/20/20 train/val/test con stratify (due split o train_test_split due volte).
# 2) Allena LogisticRegression su train scalato (StandardScaler fit solo su train).
# 3) Prova 3 soglie su prob_alterato (colonna 1 di predict_proba): 0.3, 0.5, 0.7
#    e calcola recall sul **validation** set per ciascuna.
# 4) Scegli la soglia col recall migliore sul val (scrivi in commento).
# 5) Solo alla fine calcola recall e precision sul **test** con quella soglia.
# 6) Commento: perché questo schema è più onesto per il prodotto rispetto a
#    provare soglie sul test finché trovi quella che piace?
#
# Scrivi qui sotto:
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Modulo 2, Cap.05 (lo completi TU in modello_base.py)
# ==========================================================================
#
# > Il mentor **non** scrive il codice nel tuo `modello_base.py`: è il tuo
# > deliverable progressivo. Qui c’è solo la consegna e il criterio di “fatto”.
#
# Componente pipeline: stimare la stabilità del modello **prima** di fidarsi
# di un singolo numero sul test (prepara MLOps e decisioni su soglie).
#
# Deliverable: **tu** estendi `modello_base.py` dopo la sezione CLASSIFICAZIONE.
#
# TASK (ordine consigliato):
# 1) Importa ciò che serve (es. `cross_val_score`, `StratifiedKFold`, e per
#    evitare leakage nello scaler dentro ogni fold: `sklearn.pipeline.Pipeline`).
# 2) Costruisci una `Pipeline` con `StandardScaler` + `LogisticRegression`
#    (stessi iperparametri sensati che usi già: max_iter, random_state).
# 3) Esegui `cross_val_score` sulla porzione **train** della classificazione
#    (gli stessi `X_train`, `y_train` che già usi dopo lo split), con:
#    - `cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
#    - `scoring="recall"`
# 4) Stampa: array dei recall per fold, **media** e **deviazione standard**.
# 5) Aggiungi un commento (2–4 righe): cosa ti dice la CV che un solo
#    `recall_score(y_test, y_pred)` sul test **non** ti dice?
#
# Definition of Done:
# - `python modello_base.py` termina senza errori
# - In output compare almeno una riga con **media recall** dalla CV
# - Il commento al punto 5 è presente
#
# Non usare il **test set** per la cross-validation (solo `X_train`, `y_train`).
#
# Impatto roadmap: R0 — non fidarsi di un solo split; base per monitoring e retuning.
#
# Scrivi tutto il codice in `modello_base.py` (sotto l’assert della sezione classificazione).
#


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO (bozza guida) ---
# 1) F: sul train può essere alto per memorizzazione.
# 2) Recall alterati = TP/(TP+FN); FN = frode non vista.
# 3) 1 (alterato); 100
# 4) fit su tutto X prima dello split → leakage statistiche scaler.
# 5) F: va usato validation o CV sul train.
# 6) train ~100% o molto alta; test più bassa (tipico overfit).
# 7) Modello che predice sempre genuino → accuracy alta, recall alterati 0.
#
# --- RISPOSTE QUIZ DI VERIFICA (bozza guida) ---
# 1) F: il test finale separato resta utile; CV stima variabilità sul train.
# 2) Modello che si adatta troppo al rumore del train e generalizza male.
# 3) Stai usando il test per scegliere d → ottimizzazione sul test (scorretto).
# 4) classi / etichette
# 5) sale (o resta alta); sale poi può scendere (test)
# 6) Perché adatti le tue scelte ai dati che dovrebbero essere "imprevedibili".
# 7) F: con pochi campioni un singolo split è rumoroso; CV dà media±std su più
#    partizioni e riduce la fortuna del sorteggio (il test hold-out resta però utile).
#
# --- PARTE 5 / validation_curve — Nota ---
# Train vs valid fold: gap ampio → possibile overfitting; valid che cala dopo un max
# → troppa complessità. Su n piccolo la curva può essere irregolare: usa più dati reali
# appena possibile.
#
# --- ESERCIZIO 4 — Idea refactoring ---
# Usa cross_val_score nel loop sui d, oppure un validation set; valuta test una volta.
#
# --- ESERCIZIO 5 — Bug ---
# scaler.fit su tutto il dataset prima dello split: il test influenza media/varianza.
#
# --- ESERCIZIO 8 — Schema ---
# Due split sequenziali o train_test_split due volte; tuning soglie solo su val.
#
# --- PROGETTO INCREMENTALE (modello_base.py) — idea risolutiva (dopo i tuoi tentativi) ---
# Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(...))])
# + cross_val_score(pipe, X_train, y_train, cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring="recall")
# Così lo scaler è fit solo sul train di ogni fold, non sul test intero.
