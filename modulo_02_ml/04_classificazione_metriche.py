"""
============================================================================
MODULO 2 — CAPITOLO 04: Classificazione e Metriche
============================================================================

Prodotto (M10 — Controllo Documentale AI, vedi APPUNTI_APPLICATIVO.md):
- Termini di pipeline: `prob_alterato`, `score_genuinita`, `semaforo`, `motivi_top3`.
- Da questo capitolo gli esercizi usano sempre il dominio documentale (mock),
  allineato all'app che costruirai nel modulo finale.

Analogia pratica:
- Nei cap.02-03 hai fatto REGRESSIONE: predicevi un numero continuo (es. su
  `case.csv`) e misuravi l'errore con MAE, RMSE, R².
- Qui passi alla CLASSIFICAZIONE sul dominio pratiche: il modello risponde
  SÌ o NO — "questa pratica presenta segnali di alterazione?" (target
  `y_alterato`: genuino vs alterato).
  Non ti interessa più di QUANTO sbaglia in euro, ma SE sbaglia l'etichetta —
  e soprattutto su quali casi (FN vs FP).

Dataset:
- `dati/pratiche_genuinita_mock.csv`: feature di genuinità simulate
  (delta_netto_lordo, ratio_trattenute, match_cf_cross_doc,
  coerenza_date, accrediti_stipendio_presenti, confidence_ocr_media,
  num_incoerenze_cross_doc). Target: `y_alterato` (0=genuino, 1=alterato).

Confronto web:
- In PHP/JS/Laravel:
    if ($status === "approved") { ... } else { ... }
  Il risultato è binario: approvato o rifiutato.
- In ML la classificazione fa lo stesso: dato un insieme di feature,
  il modello sceglie una CLASSE (0 o 1, genuino o alterato).
  La differenza? Il modello sceglie in base ai DATI, non a un if scritto
  da te — e può sbagliare. L'arte sta nel MISURARE come sbaglia.
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.preprocessing import StandardScaler


# ==========================================================================
# 🔁 RINFORZO MIRATO — Pattern #21 / #22 (cap.03 → cap.04)
# ==========================================================================
#
# Pattern #21: `(x, 2)` è una tupla, non un arrotondamento. Usa `round(x, 2)`.
#
# Pattern #22: in uno script lungo con più esercizi, riusi nomi come
# `modello_lineare` o `clf_albero`. Verifica sempre che il modello
# passato a `.predict` o ai coefficienti sia quello addestrato nell'esercizio
# corrente (stesso X_train/y_train).
#
# Micro-check (rispondi a mente):
# 1) Dopo split e scaling, la sequenza corretta è:
#    scaler.fit(X_train) → transform(X_train) → transform(X_test)
#    → modello.fit(X_train_scaled, y_train) → predict(X_test_scaled).
# 2) Se l'ultimo `.fit` l'hai fatto su `clf` ma stampi
#    `clf_scalato.coef_`, i coefficienti sono quelli VECCHI.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Preprocessing: encoding prima o dopo lo split?
# ==========================================================================
#
# Al quiz d'ingresso del cap.03 hai scritto che "l'encoding va su tutto
# il dataset". Per `pd.get_dummies` su dati di esercizio piccoli questo
# funziona perché le categorie sono note a priori. Ma in produzione, se
# nel test arrivano categorie MAI viste nel train, le colonne non coincidono.
#
# Per il prodotto documentale:
# - Usa `OneHotEncoder(handle_unknown='ignore')` di sklearn → fit solo
#   su train, transform su entrambi. Categorie nuove vengono azzerate.
# - Lo scaler (media/std) va SEMPRE stimato solo sul train.
#
# Regola: se i dati cambiano nel tempo (documenti nuovi, tipi nuovi),
# tratta OGNI trasformazione come fit-on-train → transform-on-both.


# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da cap.03 M2
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "I coefficienti di una regressione lineare sono confrontabili tra feature
# diverse anche SENZA scaling."
# Rispondi V o F e spiega in 2 righe.
# (Stesso concetto nel dominio app: senza scaling, pesi su colonne a scale
#  diverse — es. importi vs ratio 0-1 vs contatori — non sono confrontabili.)
#Falso. lo scaling serve proprio a trasformare le unità di misura di ogni colonna in un ordine di grandezza che sia comune a tutti. Lo si fa tramite lo StandardScaler, che per ogni valore effettua la trasformazione tramite il calcolo (x - media della colonna) / deviazione std della colonna. In questo modo, i valori vengono trasformati in rapporto alla deviazione standard, piuttosto che ad es. uno in euro, il secondo in metri ecc.
#
# DOMANDA 2 — Prevedi l'output:
#   scaler = StandardScaler()
#   scaler.fit(X_train)
#   X_test_scaled = scaler.transform(X_test)
#   modello = LinearRegression()
#   modello.fit(X_train, y_train)
#   y_pred = modello.predict(X_test_scaled)
# Il modello funzionerà bene? Perché sì o perché no?
# c'è un problema: non è stata fatta la trasformazione del train in scaled per addestrare il modello. Poi dopo si chiede di fare una previsione sui dati del test scalati, ma in questo modo il modello non è addestrato a ricevere dati impostati sulla scala standardizzata.
#
# DOMANDA 3 — Trova l'errore:
#   mae = round(mean_absolute_error(y_pred, y_test), 2)
# Questo codice funziona, ma c'è un errore concettuale
# nell'ordine degli argomenti. Qual è?
# y_test deve essere il primo parametro passato al mean_absolute_error, nell' esempio sono invertiti
#
# DOMANDA 4 — Completa:
#   RMSE penalizza gli errori ___ più del MAE. Se MAE = 10.000
#   e RMSE = 40.000, significa che il modello ha ___ .
# grandi, ha errori molto grandi, (quindi outlier/ pochi errori sbagliati di tanto)
#
# DOMANDA 5 — Definizione:
# Cos'è il trade-off bias-varianza? Fai un esempio con un Decision Tree.
# il trade-off bias-varianza e il compromesso tra un modello troppo semplice (under-fitting), quindi che poco si adatta alla  varietà dei dati forniti nelle features, e un modello troppo complesso (over-fitting), ossia un modello troppo complesso che non generalizza più i pattern ma praticamente memorizza le risposte da dare. in pratica sono i due estremi tra cui noi dobbiamo trovare il giusto equilibri. Ad esempio, un Decision Tree con max_depth=1 rischi di essere troppo semplice. Se max_depth=None, il modello invece si adatta anche al rumore di fondo (varianza troppo elevata)
#
# DOMANDA 6 — 💬 Spiega con parole tue:
# Perché, nel tuo prodotto documentale, i coefficienti di un modello
# lineare scalato sono utili per costruire i `motivi_top3` dell'esito?
#Perchè i coefficenti dammi un idea del peso relativo dello scoring di una pratica. Ad esempio, un delta tra lordo e netto errato, avrà un peso molto rilevante nel definire una pratica "non genuina", ed aiuta l'operatore a capire subito il perchè di questa classificazione.


# ==========================================================================
# PARTE 1: Da Regressione a Classificazione — Il Cambio di Prospettiva
# ==========================================================================
#
# Finora, nei cap.02-03, il target della regressione era un NUMERO continuo
# (es. prezzo stimato su `case.csv`) e misuravi quanto il modello si
# avvicinava al valore vero (MAE, RMSE, R²).
#
# La classificazione è un problema diverso: il target non è un numero
# continuo, è una CATEGORIA. Due classi, nel caso più semplice:
#
#   - 0 = classe negativa → "genuino"
#   - 1 = classe positiva → "alterato"
#
# Il modello non dice "questa pratica ha uno score di 73.5" ma
# "questa pratica è alterata: SÌ" oppure "questa pratica è genuina: NO".
#
# Nella pipeline del prodotto documentale, il classificatore riceve
# le feature di una pratica (delta_netto_lordo, ratio_trattenute,
# match_cf_cross_doc, coerenza_date...) e risponde:
#
#   genuino (0) oppure alterato (1)?
#
# Da quella risposta si derivano:
# - `prob_alterato` (0.0-1.0): la probabilità che sia alterato
# - `score_genuinita` = (1 - prob_alterato) * 100
# - `semaforo`: verde / giallo / rosso in base alle soglie
#
# Ma c'è un problema: quando il modello sbaglia, NON tutti gli errori
# sono uguali. Se dice "genuino" a un documento alterato, è MOLTO peggio
# che dire "alterato" a uno genuino. Questo capitolo ti dà gli strumenti
# per misurare COME sbaglia — non solo QUANTO.
#
# Confronto veloce regressione vs classificazione:
#
#   Regressione                    │ Classificazione
#   ──────────────────────────────────────────────────────
#   Target: numero continuo        │ Target: classe (0/1)
#   Errore: distanza dal valore    │ Errore: classe sbagliata
#   Metriche: MAE, RMSE, R²        │ Metriche: accuracy, precision,
#                                  │   recall, F1, confusion matrix
#   Modelli: LinearRegression,     │ Modelli: LogisticRegression,
#     DecisionTreeRegressor        │   DecisionTreeClassifier
#
# Il Decision Tree e la Regressione Lineare hanno le loro versioni
# per la classificazione: DecisionTreeClassifier e LogisticRegression.
# Stessi ingredienti (fit, predict, feature, target), piatto diverso.

print("\n" + "="*60)
print("PARTE 1 — Da regressione a classificazione")
print("="*60)

# Carichiamo il dataset documentale mock.
# Le feature simulano controlli di genuinità su pratiche bancarie:
# - delta_netto_lordo: differenza netto-lordo (valori negativi = sospetti)
# - ratio_trattenute: rapporto trattenute/lordo (alto = sospetto)
# - match_cf_cross_doc: codice fiscale coerente tra documenti (1=sì, 0=no)
# - coerenza_date: date coerenti tra documenti della pratica (1=sì, 0=no)
# - accrediti_stipendio_presenti: accrediti in conto coerenti con busta (1=sì)
# - confidence_ocr_media: qualità media estrazione OCR (0-1)
# - num_incoerenze_cross_doc: numero di incoerenze trovate tra documenti
# Target: y_alterato (0=genuino, 1=alterato)

path_file = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
pratiche = pd.read_csv(path_file)

print(f"Dataset pratiche: {len(pratiche)} righe")
print(f"\nDistribuzione classi (y_alterato):")
print(f"  genuino (0): {(pratiche['y_alterato'] == 0).sum()}")
print(f"  alterato (1): {(pratiche['y_alterato'] == 1).sum()}")

# X e y (anti-leakage: togli ID e target da X)
X = pratiche.drop(columns=["pratica_id", "y_alterato"])
y = pratiche["y_alterato"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nFeature usate: {list(X.columns)}")
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# Alleniamo un DecisionTreeClassifier
clf_albero = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_albero.fit(X_train, y_train)

y_pred = clf_albero.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy albero: {acc:.2%}")
print(f"Previsioni: {y_pred}")
print(f"Reali:      {y_test.values}")


# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Guarda le previsioni vs i valori reali stampati sopra.
#    Conta a occhio: quante previsioni sono giuste? Quante sbagliate?
# 2) Verifica che il calcolo dell'accuracy corrisponde:
#    accuracy = numero_giusti / totale
# 3) Rispondi in un commento: l'accuracy del 100% significherebbe che
#    il modello è perfetto. Ma un modello con accuracy 90% è sempre
#    "buono"? Pensa a un caso in cui 90% di accuracy è INUTILE.
#    (Suggerimento: se il 90% delle pratiche è genuino e il modello
#    dice SEMPRE "genuino"...)
# Scrivi qui sotto:
#


# ==========================================================================
# PARTE 2: Confusion Matrix — I 4 Quadranti dell'Errore
# ==========================================================================
#
# L'accuracy ti dice "quanti ne hai azzeccati sul totale". Ma non ti dice
# COME hai sbagliato — e nel controllo documentale, non tutti gli errori
# pesano uguale.
#
# Il modello ha due modi di sbagliare:
#
# 1) Dice "alterato" a un documento genuino → FALSO ALLARME
#    Il consulente controlla un documento che era a posto. Fastidioso,
#    fa perdere tempo, ma nessun danno grave.
#
# 2) Dice "genuino" a un documento alterato → MANCATA RILEVAZIONE
#    Il documento alterato passa il controllo. Potenziale danno economico,
#    rischio compliance, possibile frode non intercettata. MOLTO peggio.
#
# Per distinguere questi due tipi di errore, usiamo la CONFUSION MATRIX
# (matrice di confusione). È una tabella 2×2 che incrocia le previsioni
# del modello con la realtà:
#
#                          Realtà
#                     0 (genuino)    1 (alterato)
#   Previsto 0    │  TN (True Neg)  │  FN (False Neg)  │
#   Previsto 1    │  FP (False Pos) │  TP (True Pos)   │
#
# Nel dominio documentale (positivo = alterato):
#
# - TP (True Positive): dice "alterato" e il documento ERA alterato.
#   BENE — ha trovato il problema.
# - TN (True Negative): dice "genuino" e il documento ERA genuino.
#   BENE — nessun falso allarme.
# - FP (False Positive): dice "alterato" ma il documento era genuino.
#   FALSO ALLARME — spreco di tempo, ma niente danni gravi.
# - FN (False Negative): dice "genuino" ma il documento era alterato.
#   MANCATA RILEVAZIONE — il caso peggiore!
#
# Confronto web:
# È come il testing nel software:
# - TP = un test trova un bug reale (ottimo!)
# - TN = un test conferma che il codice funziona (bene)
# - FP = un test segna un errore ma il codice era giusto (flaky test)
# - FN = nessun test rileva il bug (il bug va in produzione — disastro)
#
# La confusion matrix di sklearn:
#
#   from sklearn.metrics import confusion_matrix
#   cm = confusion_matrix(y_test, y_pred)
#
# Restituisce un array 2×2:
#   [[TN, FP],
#    [FN, TP]]
#
# ATTENZIONE all'ordine: prima il REALE (y_test), poi il PREVISTO (y_pred).
# Come in `mean_absolute_error(y_test, y_pred)` — sempre reale prima.

print("\n" + "="*60)
print("PARTE 2 — Confusion matrix: i 4 quadranti dell'errore")
print("="*60)

cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:\n{cm}")
print(f"\n  TN={cm[0,0]}  FP={cm[0,1]}")
print(f"  FN={cm[1,0]}  TP={cm[1,1]}")

totale = cm.sum()
corretti = cm[0, 0] + cm[1, 1]
print(f"\nTotale: {totale} | Corretti: {corretti} | Accuracy: {corretti/totale:.2%}")


# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Dalla confusion matrix stampata sopra:
#    - Quanti documenti alterati il modello ha classificato correttamente? (TP)
#    - Quanti documenti genuini il modello ha sbagliato? (FP)
# 2) I FN (False Negative) sono pericolosi: perché?
#    I FP (False Positive) sono fastidiosi ma tollerabili: perché?
# 3) Scrivi la formula dell'accuracy usando TN, FP, FN, TP:
#    accuracy = ___
# Scrivi qui sotto:
#


# ==========================================================================
# PARTE 3: Precision, Recall, F1 — Le Metriche che Contano
# ==========================================================================
#
# L'accuracy è utile come punto di partenza, ma in molti casi è
# INSUFFICIENTE. Ecco perché:
#
# Immagina di avere 100 pratiche: 90 genuine e 10 alterate.
# Un modello "stupido" che dice SEMPRE "genuino" ha accuracy del 90%.
# Sembra fantastico! Ma non ha trovato NESSUNA delle pratiche alterate.
# È completamente inutile per lo scopo del prodotto.
#
# Servono metriche più precise. Tre in particolare:
#
# ---
# PRECISION (Precisione):
# "Delle pratiche che il modello ha CHIAMATO alterate, quante lo erano
# davvero?"
#
#   precision = TP / (TP + FP)
#
# Se il modello dice "alterato" 10 volte, e 8 di quelle erano davvero
# alterate → precision = 8/10 = 0.80 (80%).
# Precision alta = pochi falsi allarmi.
#
# Analogia: un allarme antifurto con precision alta suona SOLO quando
# c'è davvero un intruso. Non ti sveglia di notte per un gatto.
#
# ---
# RECALL (Richiamo / Sensibilità):
# "Delle pratiche che ERANO davvero alterate, quante ne ha trovate
# il modello?"
#
#   recall = TP / (TP + FN)
#
# Se ci sono 10 pratiche alterate e il modello ne trova 7
# → recall = 7/10 = 0.70 (70%). 3 gli sono sfuggite.
# Recall alto = il modello non si lascia sfuggire i positivi.
#
# Analogia: un allarme antifurto con recall alto suona SEMPRE quando
# c'è un intruso. Può anche suonare per un gatto (FP), ma non si perde
# MAI un ladro.
#
# ---
# NEL PRODOTTO DOCUMENTALE: la recall è LA METRICA CRITICA.
# Una pratica alterata che passa il controllo (FN) può causare danni
# economici reali. Un falso allarme (FP) costa solo tempo al revisore.
# Quindi vuoi recall alto sulla classe "alterato", anche a costo di
# qualche falso allarme in più (precision un po' più bassa).
#
# ---
# F1 SCORE:
# La media armonica di precision e recall. È un compromesso unico
# che tiene conto di entrambe:
#
#   F1 = 2 * (precision * recall) / (precision + recall)
#
# Perché "armonica" e non aritmetica? Perché la media armonica penalizza
# i valori bassi. Se precision = 1.0 e recall = 0.0, la media aritmetica
# sarebbe 0.5 — sembra ok. Ma la media armonica è 0.0 — correttamente
# riflette che il modello è inutile (non trova nessun positivo).
#
# In sklearn:

print("\n" + "="*60)
print("PARTE 3 — Precision, Recall, F1")
print("="*60)

prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print(f"\nPrecision: {prec:.2f}")
print(f"Recall:    {rec:.2f}")
print(f"F1 Score:  {f1:.2f}")

# classification_report: un riepilogo completo per ogni classe
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["genuino", "alterato"], zero_division=0))

# Il report mostra precision/recall/F1 PER OGNI CLASSE (genuino e alterato),
# più la media (macro e weighted). "support" è il numero di campioni
# reali per classe nel test set.

# Confronto web:
# Pensa ai risultati di un motore di ricerca:
# - Precision = dei risultati mostrati, quanti erano pertinenti?
# - Recall = dei documenti pertinenti esistenti, quanti sono stati trovati?
# Un motore che mostra 3 risultati tutti pertinenti ha precision perfetta,
# ma recall basso se ne esistevano 100 pertinenti.
# Un motore che mostra 1000 risultati trova tutto (recall alto) ma
# la maggior parte è spazzatura (precision bassa).


# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Dalla confusion matrix del modello sopra, calcola A MANO:
#    precision = TP / (TP + FP) = ?
#    recall    = TP / (TP + FN) = ?
#    f1        = 2 * (prec * rec) / (prec + rec) = ?
#    Confronta con i valori stampati da sklearn.
#
# 2) Immagina questo scenario documentale:
#    100 pratiche: 90 genuine, 10 alterate.
#    Il modello dice SEMPRE "genuino".
#    Calcola: accuracy = ?  precision = ?  recall = ?
#    Cosa noti?
#
# 3) Ora immagina il contrario: il modello dice SEMPRE "alterato".
#    Calcola: accuracy = ?  precision = ?  recall = ?
#    Quale dei due è più pericoloso per il prodotto?
# Scrivi qui sotto:
#


# ==========================================================================
# PARTE 4: LogisticRegression e predict_proba — Oltre il Sì/No
# ==========================================================================
#
# La regressione logistica (LogisticRegression) è il cugino classificatore
# della LinearRegression del cap.03. Nonostante il nome contenga
# "regressione", è un CLASSIFICATORE: produce una classe (0 o 1), non
# un numero continuo.
#
# Come funziona a grandi linee:
# 1) Calcola una somma pesata delle feature:
#    z = w1 * delta_netto_lordo + w2 * ratio_trattenute + ... + b
# 2) Passa il risultato attraverso una funzione "sigmoide" che lo
#    comprime tra 0 e 1 — interpretabile come PROBABILITÀ:
#    p = 1 / (1 + e^(-z))
# 3) Se p >= 0.5 → classe 1 (alterato)
#    Se p < 0.5  → classe 0 (genuino)
#
# La magia è che puoi accedere alla probabilità con `.predict_proba()`:
# non solo "sì/no", ma "sì con probabilità 87%".
#
# Nel prodotto documentale questo è ORO:
# - `predict_proba` restituisce `prob_alterato` (colonna 1)
# - `score_genuinita = (1 - prob_alterato) * 100`
# - Puoi poi scegliere TU la soglia: non devi per forza usare 0.5.
#   Se vuoi essere più prudente (non lasciarti sfuggire alterati),
#   abbassi la soglia a 0.3 → il modello dice "alterato" più spesso
#   → recall sale, precision scende → meno FN, più FP.
#   Questo è il TRADE-OFF PRECISION/RECALL, e lo controlli con la soglia.
#
# Come scaling: anche la LogisticRegression beneficia dello StandardScaler,
# come la LinearRegression del cap.03.

print("\n" + "="*60)
print("PARTE 4 — LogisticRegression e predict_proba")
print("="*60)

# Scaling (fit solo su train — ormai lo sai!)
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_log = LogisticRegression(random_state=42, max_iter=1000)
clf_log.fit(X_train_scaled, y_train)

y_pred_log = clf_log.predict(X_test_scaled)
y_proba = clf_log.predict_proba(X_test_scaled)

print("\nPrevisioni LogisticRegression:")
print(f"  Classi:       {y_pred_log}")
print(f"  Reali:        {y_test.values}")

# predict_proba restituisce una matrice con 2 colonne:
# colonna 0 = P(genuino), colonna 1 = P(alterato)
print(f"\n  Probabilità (prime 5 pratiche del test):")
for i in range(min(5, len(y_proba))):
    p0, p1 = y_proba[i]
    print(f"    Pratica {i+1}: P(genuino)={p0:.2f}  P(alterato)={p1:.2f}  → classe {y_pred_log[i]}")

# La colonna 1 è prob_alterato → da qui si ricava score_genuinita
prob_alterato_esempio = y_proba[:, 1]
score_genuinita_esempio = ((1 - prob_alterato_esempio) * 100).round(1)
print(f"\n  prob_alterato:    {np.round(prob_alterato_esempio, 2)}")
print(f"  score_genuinita:  {score_genuinita_esempio}")

# Metriche
print(f"\n  Accuracy:  {accuracy_score(y_test, y_pred_log):.2%}")
print(f"  Precision: {precision_score(y_test, y_pred_log, zero_division=0):.2f}")
print(f"  Recall:    {recall_score(y_test, y_pred_log, zero_division=0):.2f}")
print(f"  F1:        {f1_score(y_test, y_pred_log, zero_division=0):.2f}")

# Effetto della soglia (esempio: soglia 0.3 invece di 0.5)
soglia_prudente = 0.3
y_pred_prudente = (prob_alterato_esempio >= soglia_prudente).astype(int)
print(f"\n  Con soglia {soglia_prudente} (più prudente — meno FN):")
print(f"  Previsioni: {y_pred_prudente}")
print(f"  Recall:     {recall_score(y_test, y_pred_prudente, zero_division=0):.2f}")
print(f"  Precision:  {precision_score(y_test, y_pred_prudente, zero_division=0):.2f}")


# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Guarda le probabilità stampate sopra: ci sono pratiche in cui il
#    modello era "indeciso" (probabilità vicina a 0.5)?
# si, alcune erano intorno al 60% di score genuinità
# 2) Se abbassi la soglia da 0.5 a 0.3, cosa succede al numero di
#    previsioni "1" (alterato)? Aumenta o diminuisce?
#    Perché questo fa salire il recall?
#Aumenta, perchè in questo caso, appena la probabilità alterato sale oltre il 30 %, fa scattare l'alert e da classe 1
# 3) Nel prodotto: se la soglia è troppo bassa (es. 0.1), il modello
#    dice "alterato" quasi sempre. Cosa succede alla precision?
#    Qual è il rischio operativo per il consulente?
# Bisogna trovare il giusto equilibrio, perchè altrimenti il consulente si trova a controllare manualmente praticamente tutte le pratiche, ma a quel punto il modello diventa praticamente inutile. La precision deve cmq essere sufficientemente alta così da scongiurare questa evenienza. 
# 4) Il semaforo (verde/giallo/rosso) è derivato dallo score_genuinita
#    con soglie. Come sceglieresti le soglie in produzione?
# 0% - 50% rosso, 51% - 70% giallo, 71% - 100 % verde utilizzando una soglia di .3
#    (Suggerimento: non con l'intuizione, ma guardando precision/recall
#    a soglie diverse sul test set.)
# Scrivi qui sotto:
#


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Un modello con accuracy 95% è sempre affidabile."
# Rispondi V o F, fai un esempio concreto dove non lo è.
# Falso, in un data set di documenti , in cui 95 sono genuini e 5 alterati praticamente il modello, anche avendo accuracy 95 (sembra molto bravo) ha allo stesso tempo recall 0, quindi di fatto non ne prende neanche 1, ed è di fatto inutile
#
# DOMANDA 2 — Prevedi:
# Confusion matrix:
#   [[80, 10],
#    [ 5, 5]]
# Calcola: accuracy, precision, recall, F1.
# Il modello è buono per trovare le pratiche alterate?
# accuracy = (TN + TP) / (TN + TP + FN + FP) = 85 / 100 = 85.00%
# precision = TP / (TP + FP) = 5 / 5 + 10 = 5 / 15 = 33.33%
# recall = TP / (TP + FN) = 5 / 5 + 5 = 5 / 10 = 50.00%
# f1 = (2 * 0.50 * 0.33) / (0.5 + 0.33) = 0.33 / 0.83 = 0.4
#
# DOMANDA 3 — Trova l'errore:
#   y_pred = clf.predict(X_test)
#   print(precision_score(y_pred, y_test))
# Cosa c'è di sbagliato? Cosa può succedere?
# I parametri di precision_score sono invertiti, e di conseguenza la metrisca non avrebbe senso e sarebbe fuorviante
#
# DOMANDA 4 — Completa:
#   Nel prodotto documentale, la metrica CRITICA è la ___ sulla classe
#   "alterato" perché un ___ (pratica alterata classificata come
#   genuina) è molto più grave di un ___ (genuina classificata
#   come alterata).
#  recall, falso negativo, falso positivo
#
#
# DOMANDA 5 — Definizione:
# Qual è la differenza tra `predict` e `predict_proba` in sklearn?
# Quale dei due è necessario per calcolare `score_genuinita`?
# predict da un esito che è binario, nel nostro caso genuino o alterato rappresentati con 0 o 1. la predict_proba, invece restituisce le probabilità di appartenenza all'una o l'altra classe, e dunque fondamentale perchè da questa probabilità possiamo ricavare proprio lo score_genuinità.
#
# DOMANDA 6 — 💬 Spiega con parole tue:
# Spiega a un collega non tecnico cosa significano precision e recall,
# usando l'esempio dell'allarme antifurto (o un'analogia a tua scelta).
# Quale delle due è più importante nel controllo documentale? Perché?
# precision è : su 10 volte che è scattato l'allarme, quante volte era davvero entrato un ladro?
# recall : su 10 volte che sono arrivati i ladri, quante volte l'allarme se ne è accorto ed è scattato?
# Nel caso del controllo documentale, la recall ha sicuramente un importanza maggiore. Questo perchè se anche il modello segnala un falso positivo, li può intervenire l'operatore e verificare manualmente, ma ne caso di un positivo non segnalato, li non si puù intervenire per sistemare, e l'errore passa semplicemente e può causare rischi gravi (come frodi)


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================
#
# Tutti gli esercizi sotto usano il dataset del prodotto (mock):
#   dati/pratiche_genuinita_mock.csv — stesso dominio dell'app Controllo
#   Documentale (pratiche reddituali, genuino/alterato, semaforo in es.8).
#

# ESERCIZIO 1 (Facile):
# 1) Carica pratiche_genuinita_mock.csv
# 2) Prepara X (tutte le feature) e y (y_alterato)
# 3) Split 80/20, random_state=42
# 4) Allena un DecisionTreeClassifier(max_depth=3, random_state=42)
# 5) Stampa: accuracy, precision, recall, F1
# 6) Stampa la confusion matrix
# 7) Assert: accuracy > 0.5 (deve battere il lancio di una moneta)

print("\n" + "="*60)
print("ESERCIZIO 1")
print("="*60)

path_file_mock = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
pratiche = pd.read_csv(path_file_mock)

print(pratiche.columns)

X = pratiche.drop(columns=['y_alterato', 'pratica_id'])
y = pratiche['y_alterato']

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size = .2, random_state=42, stratify=y
)


clf_tree = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_tree.fit(X_train, y_train)

y_pred_train = clf_tree.predict(X_train)
y_pred_test = clf_tree.predict(X_test)

accuracy_train = accuracy_score(y_train, y_pred_train)
precision_train = precision_score(y_train, y_pred_train, zero_division=0)
recall_train = recall_score(y_train, y_pred_train, zero_division=0)
f1_train = f1_score(y_train, y_pred_train, zero_division=0)

accuracy_test = accuracy_score(y_test, y_pred_test)
precision_test = precision_score(y_test, y_pred_test, zero_division=0)
recall_test = recall_score(y_test, y_pred_test, zero_division=0)
f1_test = f1_score(y_test, y_pred_test, zero_division=0)

report= [
  {
    'set': 'TRAIN',
    'accuracy_score': accuracy_train,
    'precision_score': precision_train,
    'recall_score': recall_train,
    'f1_score': f1_train
  },
  {
    'set': 'TEST',
    'accuracy_score': accuracy_test,
    'precision_score': precision_test,
    'recall_score': recall_test,
    'f1_score': f1_test
  }
]

print(pd.DataFrame(report))
print(confusion_matrix(y_test, y_pred_test))


assert accuracy_test > .5, 'Il modello deve battere il lancio di una moneta'


# ESERCIZIO 2 (Medio):
# Confronta 3 classificatori sullo stesso split (dal dataset pratiche):
# 1) DecisionTreeClassifier(max_depth=3)
# 2) DecisionTreeClassifier(max_depth=6)
# 3) LogisticRegression (con StandardScaler — fit solo su train!)
# Per ciascuno calcola: accuracy, precision, recall, F1 su test.
# Crea un DataFrame di confronto e stampalo ordinato per recall.
# In un commento: quale sceglieresti per il prodotto documentale?
# Motiva la scelta pensando ai falsi negativi.
# Nel caso di questo test, i modelli sono risultati identici in termini di punteggi delle metriche, compreso il recall sui falsi negativi. Quindi la scelta, nel nostro caso specifico, ricadrebbe sul logistic regressor per via del predict proba, che ci sarebbe utile per generare poi il punteggio di scoring.

print("\n" + "="*60)
print("ESERCIZIO 2")
print("="*60)

path_file_mock = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
pratiche = pd.read_csv(path_file_mock)

X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
y = pratiche['y_alterato']

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=.2, random_state=42, stratify=y
)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_tree_md3 = DecisionTreeClassifier(max_depth = 3, random_state=42)
clf_tree_md6 = DecisionTreeClassifier(max_depth = 6, random_state=42)
clf_log = LogisticRegression(max_iter=1000, random_state=42)

clf_tree_md3.fit(X_train, y_train)
clf_tree_md6.fit(X_train, y_train)
clf_log.fit(X_train_scaled, y_train)

y_pred_tree_md3 = clf_tree_md3.predict(X_test)
y_pred_tree_md6 = clf_tree_md6.predict(X_test)
y_pred_log = clf_log.predict(X_test_scaled)

report=[
  {
    'modello': 'Albero max_depth=3',
    'accuracy': accuracy_score(y_test, y_pred_tree_md3),
    'precision': precision_score(y_test, y_pred_tree_md3, zero_division=0),
    'recall': recall_score(y_test, y_pred_tree_md3, zero_division=0),
    'f1_score': f1_score(y_test, y_pred_tree_md3, zero_division=0)
  },
  {
    'modello': 'Albero max_depth=6',
    'accuracy': accuracy_score(y_test, y_pred_tree_md6),
    'precision': precision_score(y_test, y_pred_tree_md6, zero_division=0),
    'recall': recall_score(y_test, y_pred_tree_md6, zero_division=0),
    'f1_score': f1_score(y_test, y_pred_tree_md6, zero_division=0)
  },
  {
    'modello': 'Logistic Regressor',
    'accuracy': accuracy_score(y_test, y_pred_log),
    'precision': precision_score(y_test, y_pred_log, zero_division=0),
    'recall': recall_score(y_test, y_pred_log, zero_division=0),
    'f1_score': f1_score(y_test, y_pred_log, zero_division=0)
  }
]

print(pd.DataFrame(report).sort_values(by='recall', ascending=False))

# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Rispondi in 10-12 righe di commento:
# - Cosa sono precision e recall? Fai un esempio per ciascuno nel
#   contesto del controllo documentale.
# precision: su 10 documenti segnalati, quanti erano realmente alterati ? (falsi positivi)
# recall: su 10 documenti alterati, quanti ne ha segnalati il modello ? (falsi negativi)
# - Quando è più importante la precision? Quando il recall?
# la precision è importante in quei contesti in cui è meglio avere meno falsi allarmi possibile. la recall è importante quando devono sfuggire meno target possibili.
# - Cos'è l'F1 e perché usa la media armonica (non aritmetica)?
# perchè se uno dei valori è molto basso (anche se l'altro è invece alto), l'f1 score lo segnala 
# - Nel prodotto: su quale classe vuoi recall alto e perché?
# voglio recall alto sulle pratiche alterate, perchè non trovarle significa esporsi a rischi gravi (come le frodi)
#   Cosa succede se il recall sulla classe "alterato" è basso?
# che molto pratiche alterate superano il controllo, e quindi il modello non è adeguato al compito che ci siamo prefissati, ossia evitare le frodi
# - Cos'è una confusion matrix? Come la leggi?
# la confusion matrix e una matrice 2, che va letta in questo modo = [[TN, FP][FN, TP]]. La si utilizza per il calcolo delle metriche.


# ESERCIZIO 4 (🔧 [REFACTORING]):
# Riscrivi questo codice in modo corretto e pulito.
# Ci sono 3 problemi: trovali tutti e correggili.
#
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score, recall_score
# d = DecisionTreeClassifier()
# d.fit(X, y)
# p = d.predict(X)
# print(accuracy_score(p, y))
# print(recall_score(p, y))
#
# Problemi da trovare:
# - Nessuno split train/test
# - Nomi variabili non descrittivi
# - Ordine argomenti metriche

print("\n" + "="*60)
print("ESERCIZIO 4 — REFACTORING")
print("="*60)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score

X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
y = pratiche['y_alterato']

clf_tree_model = DecisionTreeClassifier(random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=.2, random_state=42, stratify=y
)

clf_tree_model.fit(X_train, y_train)

y_pred = clf_tree_model.predict(X_test)

print(f"Accuracy Score => {accuracy_score(y_test, y_pred):.1%}")
print(f"Recall Score   => {recall_score(y_test, y_pred):.1%}")


# ESERCIZIO 5 (🔍 [DEBUG]):
# Questo codice gira senza errori ma il recall è SOSPETTOSAMENTE alto (1.0).
# Trova il bug e spiega perché il risultato è ingannevole.
#
# pratiche_dbg = pd.read_csv("dati/pratiche_genuinita_mock.csv")
# X_dbg = pratiche_dbg.drop(columns=["pratica_id"], errors="ignore")
# y_dbg = pratiche_dbg["y_alterato"]
# X_tr, X_te, y_tr, y_te = train_test_split(X_dbg, y_dbg, test_size=0.2, random_state=42)
# clf = DecisionTreeClassifier(random_state=42)
# clf.fit(X_tr, y_tr)
# print("Recall:", recall_score(y_te, clf.predict(X_te)))
#
# Suggerimento: guarda le colonne di X_dbg. Hai droppato davvero solo
# ciò che serve? Il target è ancora nelle feature?
# c'è un problema di leakage. in pratica non è stato tolto il target dalla X, e dunque il modello utilizza anche la feature che dovrebbe prevedere per addestrarsi. inoltre non è stata impostato nessun iperparametro (es. max_depth) per regolare un possibile prblema di over-fitting


# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + Classificazione):
# 1) Carica pratiche_genuinita_mock.csv
# 2) Crea un report con Pandas:
#    - pratiche_totali, pratiche_alterate, perc_alterate
#    - media di delta_netto_lordo per classe (genuino vs alterato)
#    - media di confidence_ocr_media per classe
# 3) Filtra SOLO le pratiche con confidence_ocr_media >= 0.75
# 4) Allena un DecisionTreeClassifier SOLO su quelle filtrate
# 5) Stampa la confusion matrix e il classification_report
# 6) Commenta: filtrare per confidence alta migliora o peggiora
#    le metriche? Ha senso nel prodotto reale?

# può avere senso nel ottica di offrire dati più leggibili, e quindi meglio interpretabili. Ma nel test svolto con il mock, l'aver imposto una soglia di ocr_confidence così alta, ha di fatto eliminato dal data set tutti gli alterati. Questo è un problema perchè non abbiamo un reale confronto con delle pratiche alterate

print("\n" + "="*60)
print("ESERCIZIO 6 — INTERLEAVING")
print("="*60)
from sklearn.metrics import classification_report

pratiche = pd.read_csv(os.path.join(os.path.dirname(__file__), 'dati', 'pratiche_genuinita_mock.csv'))

report = pd.DataFrame([
  {
  'pratiche_totali': len(pratiche),
  'pratiche_alterate': len(pratiche[pratiche['y_alterato'] == 1]),
  'perc_alterate': round(((len(pratiche[pratiche['y_alterato'] == 1]) / len(pratiche))*100), 2),
  'delta_lordo_netto_alterati':  pratiche.loc[pratiche['y_alterato'] == 1, 'delta_netto_lordo'].abs().mean().round(2),
  'delta_lordo_netto_genuini':  pratiche.loc[pratiche['y_alterato'] == 0, 'delta_netto_lordo'].abs().mean().round(2),
  'conf_ocr_media_alterati': pratiche.loc[pratiche['y_alterato'] == 1, 'confidence_ocr_media'].mean().round(2),
  'conf_ocr_media_genuini': pratiche.loc[pratiche['y_alterato'] == 0, 'confidence_ocr_media'].mean().round(2)
  }
])

print(report)

pratiche_ocr_alta = pratiche.loc[pratiche['confidence_ocr_media'] >= 0.75].sort_values(by='confidence_ocr_media')

X = pratiche_ocr_alta.drop(columns=['pratica_id', 'y_alterato'])
y = pratiche_ocr_alta['y_alterato']

print(y.value_counts())

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=.2, random_state=42, stratify=y
)


clf_tree = DecisionTreeClassifier(max_depth=6, random_state=42)
clf_tree.fit(X_train, y_train)

y_pred_test = clf_tree.predict(X_test)

print(confusion_matrix(y_test, y_pred_test))
print(classification_report(y_test, y_pred_test, zero_division=0))

# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrivi da memoria):
# Senza guardare il codice sopra, riscrivi da zero:
# 1) Carica pratiche_genuinita_mock.csv
# 2) Prepara X e y (anti-leakage!)
# 3) Split 80/20
# 4) Allena una LogisticRegression con scaling
# 5) Calcola predict_proba → prob_alterato (colonna 1)
#    → score_genuinita = (1 - prob_alterato) * 100
# 6) Stampa per ogni pratica del test: score_genuinita, classe prevista,
#    classe reale
# 7) Stampa accuracy, recall, precision, F1
# 8) Assert: recall >= 0.5

print("\n" + "="*60)
print("ESERCIZIO 7 — RETRIEVAL")
print("="*60)

path_file_mock = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
pratiche = pd.read_csv(path_file_mock)

X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
y = pratiche['y_alterato']

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=.2, random_state=42, stratify=y
)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_log = LogisticRegression(max_iter=1000, random_state=42)
clf_log.fit(X_train_scaled, y_train)

y_pred_test = clf_log.predict(X_test_scaled)
y_proba_test = clf_log.predict_proba(X_test_scaled)

for classe_reale, classe_prev, proba in zip(y_test, y_pred_test, y_proba_test):
  print(f"Classe Reale: {('Genuino' if classe_reale == 0 else 'Alterato'):15s}Classe Prevista: {('Genuino' if classe_prev == 0 else 'Alterato'):10s} =>  score genuinità: {(1 - proba[1]):.2%} {'!!!' if classe_reale != classe_prev else ''}")
  
print(f"Accuracy Score:    {accuracy_score(y_test, y_pred_test):.2f}")
print(f"\nPrecision Score:   {precision_score(y_test, y_pred_test, zero_division=0):.2f}")
print(f"Recall Score:      {recall_score(y_test, y_pred_test, zero_division=0):.2f}")
print(f"F1 Score:          {f1_score(y_test, y_pred_test, zero_division=0):.2f}")

assert recall_score(y_test, y_pred_test) >= .5, 'Il recall deve essere maggiore o uguale rispetto al caso'

# ESERCIZIO 8 (Analisi — collegamento al prodotto):
# 1) Usando il classificatore LogisticRegression scalato dell'es.7 (o
#    allenatone uno nuovo): stampa i coefficienti del modello con il
#    nome della feature, ordinati per valore assoluto (come `motivi_top_n`
#    del cap.03, ma questa volta per un CLASSIFICATORE su pratiche).
# 2) Simula il semaforo: usando le soglie del Blueprint
#    (score >= 85 → verde, 60-84 → giallo, < 60 → rosso),
#    assegna un semaforo a ogni pratica del test set.
# 3) Stampa un DataFrame con colonne:
#    pratica | score_genuinita | semaforo | classe_reale | classe_prevista
# 4) In un commento: conta quanti verdi/gialli/rossi ci sono.
#    Quanti rossi sono effettivamente alterati (classe 1)?
#    Questo corrisponde alla logica "rosso = pratica sospetta da bloccare"?
# i verdi sono 6, 1 giallo e 3 rossi. Tutti i rossi segnalati sono effettivamente da bloccare, mentre, anche se il giallo è stato alla fine etichettato come genuino (mentre in realtà era alterato), il semaforo ci ha permesso comunque di avere un allert perchè in ogni caso non era stato etichettato come verde. Quindi si, la logica funziona

print("\n" + "="*60)
print("ESERCIZIO 8 — Prodotto")
print("="*60)

coefficienti = pd.DataFrame({
  'nome_feature': X.columns,
  'peso': clf_log.coef_.ravel()
})
coefficienti['abs'] = coefficienti['peso'].abs()
print(coefficienti.sort_values(by='abs', ascending=False))

report = pd.DataFrame({
  'pratica': pratiche.loc[y_test.index, 'pratica_id'],
  'score_genuinita': (((y_proba_test[:, 0]).round(4))*100), 
})

score = report["score_genuinita"].to_numpy()
semaforo = np.select(
    [score >= 85, score >= 60],
    ["verde", "giallo"],
    default="rosso",
)

# lo trasformiamo in np.array perchè in forma originale è una Series
a = y_test.to_numpy()
genuinita_reale = np.select(
  [a == 1, a == 0],
  ["Alterato", "Genuino"],
  default='?'
)

#si presenta in forma originale come np.array
genuinità_prev = np.select(
  [y_pred_test == 1, y_pred_test == 0],
  ["Alterato", "Genuino"],
  default='?'
)

report["semaforo"] = semaforo
report['classe_reale'] = genuinita_reale
report['classe_prevista'] = genuinità_prev
print(report)


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Modulo 2, Cap.04
# ==========================================================================
#
# Componente pipeline: Cuore predittivo (classificazione)
# Deliverable: aggiorna modello_base.py aggiungendo un classificatore
#
# TASK:
# 1) Apri modello_base.py (usato nei cap.02-03 per la regressione)
# 2) Aggiungi una sezione CLASSIFICAZIONE che:
#    a) Carica pratiche_genuinita_mock.csv
#    b) Allena un DecisionTreeClassifier e una LogisticRegression
#    c) Stampa un DataFrame di confronto con colonne:
#       modello | accuracy | precision | recall | f1
#    d) Aggiungi una funzione semaforo(score) che restituisce
#       "verde" / "giallo" / "rosso" in base alle soglie del Blueprint
#    e) Stampa i motivi_top3 usando i coefficienti della LogisticRegression
# 3) Assert: recall di almeno un modello >= 0.5
#
# Definition of Done:
# - modello_base.py gira senza errori con `python modello_base.py`
# - Stampa confronto REGRESSIONE (dal cap.03) + CLASSIFICAZIONE (nuovo)
# - La funzione semaforo() restituisce valori coerenti
# - La funzione motivi_top3 funziona anche sul classificatore
#
# Impatto roadmap: R0 — primo classificatore binario + semaforo + scoring


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) Falso. Senza scaling, i coefficienti riflettono la scala della feature,
#    non la sua importanza. Se "delta_netto_lordo" va da -350 a 240 e
#    "match_cf_cross_doc" è 0 o 1, i pesi non sono confrontabili.
#    Lo StandardScaler li porta sulla stessa scala → confrontabili.
# 2) No, funzionerà male. Il modello è addestrato su X_train (non scalato)
#    ma predice su X_test_scaled (scalato). Le feature sono su scale
#    diverse tra training e inferenza → previsioni incoerenti. Bisogna
#    fare transform su ENTRAMBI, e usare i dati scalati per fit e predict.
# 3) L'ordine corretto è mean_absolute_error(y_test, y_pred), non
#    (y_pred, y_test). Convenzione sklearn: REALE prima, PREVISTO dopo.
#    Con MAE il valore numerico non cambia, ma con precision_score sì.
# 4) grandi; alcuni errori molto grandi (outlier nelle previsioni)
# 5) Il bias-varianza è il compromesso tra modello troppo semplice
#    (alto bias, underfitting) e troppo complesso (alta varianza,
#    overfitting). Es: DecisionTree con max_depth=1 è troppo semplice;
#    con max_depth=None si adatta al rumore. Ottimo: max_depth=3-6.
# 6) Dopo lo scaling, i coefficienti indicano l'importanza relativa di
#    ogni feature. I 3 più alti in valore assoluto diventano motivi_top3
#    per spiegare all'operatore PERCHÉ la pratica ha ricevuto quel score.
#    Es. "delta_netto_lordo pesa molto → è la feature più sospetta."
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Falso. Se il dataset è sbilanciato (es. 95% genuino, 5% alterato),
#    un modello che dice SEMPRE "genuino" ha accuracy 95% ma recall 0%
#    sulla classe alterato — non trova nessuna pratica sospetta.
# 2) TN=80, FP=10, FN=5, TP=5. Totale=100.
#    Accuracy = (80+5)/100 = 85%
#    Precision = 5/(5+10) = 0.333
#    Recall = 5/(5+5) = 0.50
#    F1 = 2*(0.333*0.50)/(0.333+0.50) = 0.40
#    Il modello trova solo metà delle pratiche alterate (recall=0.50)
#    e molte che chiama alterate sono falsi allarmi (precision=0.33).
#    Per il prodotto: insufficiente.
# 3) L'ordine è invertito. Deve essere precision_score(y_test, y_pred),
#    non (y_pred, y_test). Con precision_score l'inversione cambia
#    il valore (scambia TP con TN, FP con FN).
# 4) recall; FN (False Negative); FP (False Positive)
# 5) `predict` restituisce la classe (0 o 1). `predict_proba` restituisce
#    la probabilità per ogni classe (array 2 colonne: P(genuino), P(alterato)).
#    Per score_genuinita serve predict_proba: colonna 1 = prob_alterato,
#    score_genuinita = (1 - prob_alterato) * 100.
# 6) [Risposta Feynman — esempio valido:
#    "Precision: se il sistema segna 10 pratiche come sospette, quante
#    lo erano davvero? Se 8 su 10 → precision 80%.
#    Recall: su 10 pratiche davvero alterate, quante ne ha trovate?
#    Se ne trova 7 → recall 70%, 3 alterate sono passate inosservate.
#    Nel controllo documentale il recall è più importante: meglio qualche
#    falso allarme che lasciar passare una pratica alterata."]
#
# --- RISPOSTE ESERCIZI ---
#
# ESERCIZIO 4 (REFACTORING) — Problemi:
# 1) Nessuno split train/test: il modello si valuta sugli stessi dati
#    su cui è stato allenato → anti-pattern valutazione.
# 2) Nomi variabili: d, p → poco leggibili. Usare clf, y_pred.
# 3) Ordine argomenti: accuracy_score(y, p) non accuracy_score(p, y).
#    (per accuracy il risultato non cambia, ma per recall sì!)
# Codice corretto:
# clf = DecisionTreeClassifier(random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print(accuracy_score(y_test, y_pred))
# print(recall_score(y_test, y_pred))
#
# ESERCIZIO 5 (DEBUG) — Bug:
# X_dbg contiene ANCORA la colonna "y_alterato"! Non è stata droppata
# (si droppa solo "pratica_id"). Il target è nelle feature →
# data leakage perfetto: il modello impara che y_alterato == 1
# → recall 1.0 garantito.
# Correzione: X_dbg = pratiche_dbg.drop(columns=["pratica_id", "y_alterato"])
