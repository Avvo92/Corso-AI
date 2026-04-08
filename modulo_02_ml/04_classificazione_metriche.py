"""
============================================================================
MODULO 2 — CAPITOLO 04: Classificazione e Metriche
============================================================================

Analogia pratica:
- Nei cap.02-03 hai previsto un NUMERO (il prezzo di una casa). Il modello
  diceva "questa casa vale circa 280.000 €" e tu misuravi di quanto
  sbagliava (MAE, RMSE, R²).
- Ora cambi gioco: il modello deve rispondere SÌ o NO.
  "Questo documento è alterato?" → sì / no.
  "Questa casa è costosa?" → sì / no.
  Non ti interessa più di QUANTO sbaglia, ma SE sbaglia — e soprattutto
  su QUALI casi sbaglia.

Confronto web:
- In PHP/JS/Laravel:
    if ($status === "approved") { ... } else { ... }
  Il risultato è binario: approvato o rifiutato.
- In ML la classificazione fa lo stesso: dato un insieme di feature,
  il modello sceglie una CLASSE (0 o 1, vero o falso, genuino o alterato).
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
# `modello_lineare` o `modello_albero`. Verifica sempre che il modello
# passato a `.predict` o ai coefficienti sia quello addestrato nell'esercizio
# corrente (stesso X_train/y_train).
#
# Micro-check (rispondi a mente):
# 1) Dopo split e scaling, la sequenza corretta è:
#    scaler.fit(X_train) → transform(X_train) → transform(X_test)
#    → modello.fit(X_train_scaled, y_train) → predict(X_test_scaled).
# 2) Se l'ultimo `.fit` l'hai fatto su `modello` ma stampi
#    `modello_scalato.coef_`, i coefficienti sono quelli VECCHI.


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
# Regola: se i dati cambiano nel tempo (documenti nuovi, città nuove),
# tratta OGNI trasformazione come fit-on-train → transform-on-both.


# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da cap.03 M2
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "I coefficienti di una regressione lineare sono confrontabili tra feature
# diverse anche SENZA scaling."
# Rispondi V o F e spiega in 2 righe.
#
#
# DOMANDA 2 — Prevedi l'output:
#   scaler = StandardScaler()
#   scaler.fit(X_train)
#   X_test_scaled = scaler.transform(X_test)
#   modello = LinearRegression()
#   modello.fit(X_train, y_train)
#   y_pred = modello.predict(X_test_scaled)
# Il modello funzionerà bene? Perché sì o perché no?
#
#
# DOMANDA 3 — Trova l'errore:
#   mae = round(mean_absolute_error(y_pred, y_test), 2)
# Questo codice funziona, ma c'è un errore concettuale
# nell'ordine degli argomenti. Qual è?
#
#
# DOMANDA 4 — Completa:
#   RMSE penalizza gli errori ___ più del MAE. Se MAE = 10.000
#   e RMSE = 40.000, significa che il modello ha ___ .
#
#
# DOMANDA 5 — Definizione:
# Cos'è il trade-off bias-varianza? Fai un esempio con un Decision Tree.
#
#
# DOMANDA 6 — 💬 Spiega con parole tue:
# Perché, nel tuo prodotto documentale, i coefficienti di un modello
# lineare scalato sono utili per costruire i `motivi_top3` dell'esito?
#


# ==========================================================================
# PARTE 1: Da Regressione a Classificazione — Il Cambio di Prospettiva
# ==========================================================================
#
# Finora il tuo modello prediceva un NUMERO continuo: il prezzo di una casa.
# Il target (y) era un valore come 280.000, 150.000, 420.000 — e misuravi
# quanto il modello si avvicinava al valore vero con MAE, RMSE e R².
#
# La classificazione è un problema diverso: il target non è un numero
# continuo, è una CATEGORIA. Due classi, nel caso più semplice:
#
#   - 0 = classe negativa (es. "genuino", "non costosa", "non spam")
#   - 1 = classe positiva (es. "alterato", "costosa", "spam")
#
# Il modello non dice "questa casa vale 280.000 €" ma "questa casa
# è costosa: SÌ" oppure "questa casa è costosa: NO".
#
# Perché serve nel tuo prodotto?
# La pipeline del prodotto documentale ha bisogno di un classificatore
# che, data una pratica con le sue feature (delta_netto_lordo,
# ratio_trattenute, match_cf_cross_doc...), risponda:
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

# Prepariamo il dataset per la classificazione.
# Usiamo sempre case.csv, ma creiamo un TARGET BINARIO:
# la casa è "costosa" (1) o "non costosa" (0)?
# Soglia: prezzo >= mediana → costosa.

path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)

mediana_prezzo = case["prezzo_euro"].median()
case["costosa"] = (case["prezzo_euro"] >= mediana_prezzo).astype(int)

print(f"Mediana prezzo: {mediana_prezzo:,.0f} EUR")
print(f"Distribuzione classi:\n{case['costosa'].value_counts()}")

# Feature engineering (stesse del cap.03 per continuità)
case["eta_casa"] = 2026 - case["anno_costruzione"]
case_encoded = pd.get_dummies(case, columns=["citta"], dtype=int)

# Anti-leakage: togliamo TUTTO ciò che contiene il prezzo.
# "costosa" è derivata dal prezzo, ma è il NOSTRO TARGET — non una feature.
# Il prezzo stesso e i derivati (prezzo_al_mq, fascia) vanno eliminati da X.
cols_to_drop = (
    ["id", "prezzo_euro", "costosa"]
    + [c for c in case_encoded.columns if "prezzo" in c or "fascia" in c]
)
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded["costosa"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nFeature usate: {list(X.columns)}")
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# Alleniamo un DecisionTreeClassifier (la versione classificazione
# dell'albero che già conosci dal cap.02)
clf_albero = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_albero.fit(X_train, y_train)

y_pred = clf_albero.predict(X_test)

# La metrica più semplice: accuracy (percentuale di risposte giuste)
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
#    (Suggerimento: se il 90% dei documenti è genuino e il modello
#    dice SEMPRE "genuino"...)
# Scrivi qui sotto:
#


# ==========================================================================
# PARTE 2: Confusion Matrix — I 4 Quadranti dell'Errore
# ==========================================================================
#
# L'accuracy ti dice "quanti ne hai azzeccati sul totale". Ma non ti dice
# COME hai sbagliato — e nel mondo reale, non tutti gli errori pesano
# uguale.
#
# Prendiamo il prodotto documentale. Il modello ha due modi di sbagliare:
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
#                     0 (negativo)   1 (positivo)
#   Previsto 0    │  TN (True Neg)  │  FN (False Neg)  │
#   Previsto 1    │  FP (False Pos) │  TP (True Pos)   │
#
# Traduciamo nel dominio documentale (dove positivo = alterato):
#
# - TP (True Positive): il modello dice "alterato" e il documento ERA
#   davvero alterato. BENE — ha trovato il problema.
# - TN (True Negative): il modello dice "genuino" e il documento ERA
#   davvero genuino. BENE — nessun falso allarme.
# - FP (False Positive): il modello dice "alterato" ma il documento
#   era genuino. FALSO ALLARME — spreco di tempo, ma niente danni gravi.
# - FN (False Negative): il modello dice "genuino" ma il documento
#   era alterato. MANCATA RILEVAZIONE — il caso peggiore!
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

# Verifica: TN + FP + FN + TP = totale campioni nel test
totale = cm.sum()
corretti = cm[0, 0] + cm[1, 1]  # TN + TP
print(f"\nTotale: {totale} | Corretti: {corretti} | Accuracy: {corretti/totale:.2%}")


# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Dalla confusion matrix stampata sopra:
#    - Quanti documenti "costosi" il modello ha classificato correttamente? (TP)
#    - Quanti documenti "non costosi" il modello ha sbagliato? (FP)
# 2) Se questo fosse il prodotto documentale (1 = alterato):
#    - I FN (False Negative) sono pericolosi: perché?
#    - I FP (False Positive) sono fastidiosi ma tollerabili: perché?
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
# Immagina di avere 100 documenti: 95 genuini e 5 alterati.
# Un modello "stupido" che dice SEMPRE "genuino" ha accuracy del 95%.
# Sembra fantastico! Ma non ha trovato NESSUNO dei documenti alterati.
# È completamente inutile per lo scopo del prodotto.
#
# Servono metriche più precise. Tre in particolare:
#
# ---
# PRECISION (Precisione):
# "Dei documenti che il modello ha CHIAMATO alterati, quanti lo erano
# davvero?"
#
#   precision = TP / (TP + FP)
#
# Se il modello dice "alterato" 10 volte, e 8 di quelle erano davvero
# alterati → precision = 8/10 = 0.80 (80%).
# Precision alta = pochi falsi allarmi.
#
# Analogia: un allarme antifurto con precision alta suona SOLO quando
# c'è davvero un intruso. Non ti sveglia di notte per un gatto.
#
# ---
# RECALL (Richiamo / Sensibilità):
# "Dei documenti che ERANO davvero alterati, quanti ne ha trovati
# il modello?"
#
#   recall = TP / (TP + FN)
#
# Se ci sono 10 documenti alterati e il modello ne trova 7
# → recall = 7/10 = 0.70 (70%). 3 gli sono sfuggiti.
# Recall alto = il modello non si lascia sfuggire i positivi.
#
# Analogia: un allarme antifurto con recall alto suona SEMPRE quando
# c'è un intruso. Può anche suonare per un gatto (FP), ma non si perde
# MAI un ladro.
#
# ---
# NEL PRODOTTO DOCUMENTALE: la recall è LA METRICA CRITICA.
# Un documento alterato che passa il controllo (FN) può causare danni
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

prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\nPrecision: {prec:.2f}")
print(f"Recall:    {rec:.2f}")
print(f"F1 Score:  {f1:.2f}")

# classification_report: un riepilogo completo per ogni classe
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

# Il report mostra precision/recall/F1 PER OGNI CLASSE (0 e 1),
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
# 1) Calcola una somma pesata delle feature (come la regressione lineare):
#    z = w1 * mq + w2 * eta + w3 * piano + ... + b
# 2) Passa il risultato attraverso una funzione "sigmoide" che lo
#    comprime tra 0 e 1 — interpretabile come PROBABILITÀ:
#    p = 1 / (1 + e^(-z))
# 3) Se p >= 0.5 → classe 1 (costosa / alterato)
#    Se p < 0.5  → classe 0 (non costosa / genuino)
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
# colonna 0 = P(classe 0), colonna 1 = P(classe 1)
print(f"\n  Probabilità (prime 5 righe):")
for i in range(min(5, len(y_proba))):
    p0, p1 = y_proba[i]
    print(f"    Casa {i+1}: P(non costosa)={p0:.2f}  P(costosa)={p1:.2f}  → classe {y_pred_log[i]}")

# Nel prodotto: la colonna 1 è prob_alterato
prob_alterato_esempio = y_proba[:, 1]
score_genuinita_esempio = ((1 - prob_alterato_esempio) * 100).round(1)
print(f"\n  Se fosse il prodotto (colonna 1 = prob_alterato):")
print(f"  score_genuinita: {score_genuinita_esempio}")

# Metriche
print(f"\n  Accuracy:  {accuracy_score(y_test, y_pred_log):.2%}")
print(f"  Precision: {precision_score(y_test, y_pred_log, zero_division=0):.2f}")
print(f"  Recall:    {recall_score(y_test, y_pred_log, zero_division=0):.2f}")
print(f"  F1:        {f1_score(y_test, y_pred_log, zero_division=0):.2f}")

# Effetto della soglia (esempio: soglia 0.3 invece di 0.5)
soglia_prudente = 0.3
y_pred_prudente = (prob_alterato_esempio >= soglia_prudente).astype(int)
print(f"\n  Con soglia {soglia_prudente} (più prudente):")
print(f"  Previsioni: {y_pred_prudente}")
print(f"  Recall:     {recall_score(y_test, y_pred_prudente, zero_division=0):.2f}")
print(f"  Precision:  {precision_score(y_test, y_pred_prudente, zero_division=0):.2f}")


# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Guarda le probabilità stampate sopra: ci sono casi in cui il modello
#    era "indeciso" (probabilità vicina a 0.5)?
# 2) Se abbassi la soglia da 0.5 a 0.3, cosa succede al numero di
#    previsioni "1" (costosa/alterato)? Aumenta o diminuisce?
#    Perché questo fa salire il recall?
# 3) Nel prodotto: se la soglia è troppo bassa (es. 0.1), il modello
#    dice "alterato" quasi sempre. Cosa succede alla precision?
#    Qual è il rischio operativo per il consulente?
# 4) Collegamento al prodotto: il semaforo (verde/giallo/rosso) è
#    derivato dallo score_genuinita con soglie. Come sceglieresti
#    le soglie in produzione? (Suggerimento: non con l'intuizione,
#    ma guardando precision/recall a soglie diverse sul test set.)
# Scrivi qui sotto:
#


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Un modello con accuracy 95% è sempre affidabile."
# Rispondi V o F, fai un esempio concreto dove non lo è.
#
#
# DOMANDA 2 — Prevedi:
# Confusion matrix:
#   [[80, 10],
#    [ 5, 5]]
# Calcola: accuracy, precision, recall, F1.
# Il modello è buono per trovare i positivi?
#
#
# DOMANDA 3 — Trova l'errore:
#   y_pred = modello.predict(X_test)
#   print(precision_score(y_pred, y_test))
# Cosa c'è di sbagliato? Cosa può succedere?
#
#
# DOMANDA 4 — Completa:
#   Nel prodotto documentale, la metrica CRITICA è la ___ sulla classe
#   "alterato" perché un ___ (documento alterato classificato come
#   genuino) è molto più grave di un ___ (genuino classificato
#   come alterato).
#
#
# DOMANDA 5 — Definizione:
# Qual è la differenza tra `predict` e `predict_proba` in sklearn?
# Quale dei due è necessario per calcolare `score_genuinita`?
#
#
# DOMANDA 6 — 💬 Spiega con parole tue:
# Spiega a un collega non tecnico cosa significano precision e recall,
# usando l'esempio dell'allarme antifurto (o un'analogia a tua scelta).
# Quale delle due è più importante nel controllo documentale? Perché?
#


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================

# ESERCIZIO 1 (Facile):
# 1) Carica case.csv e crea il target binario "costosa"
#    (prezzo >= mediana → 1, altrimenti → 0)
# 2) Prepara X e y (anti-leakage: elimina prezzo e derivati da X)
# 3) Split 80/20, random_state=42
# 4) Allena un DecisionTreeClassifier(max_depth=3, random_state=42)
# 5) Stampa: accuracy, precision, recall, F1
# 6) Stampa la confusion matrix
# 7) Assert: accuracy > 0.5 (deve battere il lancio di una moneta)

print("\n" + "="*60)
print("ESERCIZIO 1")
print("="*60)


# ESERCIZIO 2 (Medio):
# Confronta 3 classificatori sullo stesso split:
# 1) DecisionTreeClassifier(max_depth=3)
# 2) DecisionTreeClassifier(max_depth=6)
# 3) LogisticRegression (con StandardScaler — fit solo su train!)
# Per ciascuno calcola: accuracy, precision, recall, F1 su test.
# Crea un DataFrame di confronto e stampalo ordinato per recall.
# In un commento: quale sceglieresti per il prodotto documentale?
# Motiva la scelta pensando ai falsi negativi.

print("\n" + "="*60)
print("ESERCIZIO 2")
print("="*60)


# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Rispondi in 10-12 righe di commento:
# - Cosa sono precision e recall? Fai un esempio per ciascuno.
# - Quando è più importante la precision? Quando il recall?
# - Cos'è l'F1 e perché usa la media armonica (non aritmetica)?
# - Nel tuo prodotto documentale: su quale classe vuoi recall alto
#   e perché? Cosa succede se il recall sulla classe "alterato" è basso?
# - Cos'è una confusion matrix? Come la leggi?

print("\n" + "="*60)
print("ESERCIZIO 3 — COLLOQUIO")
print("="*60)


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


# ESERCIZIO 5 (🔍 [DEBUG]):
# Questo codice gira senza errori ma il recall è SOSPETTOSAMENTE alto (1.0).
# Trova il bug e spiega perché il risultato è ingannevole.
#
# case_e = pd.get_dummies(case, columns=["citta"], dtype=int)
# mediana = case_e["prezzo_euro"].median()
# case_e["costosa"] = (case_e["prezzo_euro"] >= mediana).astype(int)
# X_dbg = case_e.drop(columns=["id", "costosa"], errors="ignore")
# y_dbg = case_e["costosa"]
# X_tr, X_te, y_tr, y_te = train_test_split(X_dbg, y_dbg, test_size=0.2, random_state=42)
# clf = DecisionTreeClassifier(random_state=42)
# clf.fit(X_tr, y_tr)
# print("Recall:", recall_score(y_te, clf.predict(X_te)))
#
# Suggerimento: guarda le colonne di X_dbg. Il prezzo è ancora lì?
# E ricorda: "costosa" è DERIVATA dal prezzo...

print("\n" + "="*60)
print("ESERCIZIO 5 — DEBUG")
print("="*60)


# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + Classificazione):
# 1) Carica case.csv e crea il target "costosa"
# 2) Crea un report con groupby("citta"):
#    - num_case, perc_costose (percentuale di case costose per città)
# 3) Identifica la città con la percentuale più alta di case costose
# 4) Allena un DecisionTreeClassifier SOLO sulle case di quella città
# 5) Stampa la confusion matrix e il classification_report
# 6) Commenta: con pochi dati (una sola città), le metriche sono
#    affidabili? Perché sì o perché no?

print("\n" + "="*60)
print("ESERCIZIO 6 — INTERLEAVING")
print("="*60)


# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrivi da memoria):
# Senza guardare il codice sopra, riscrivi da zero:
# 1) Carica case.csv, crea target "costosa" (>= mediana)
# 2) Prepara X e y (anti-leakage!)
# 3) Split 80/20
# 4) Allena una LogisticRegression con scaling
# 5) Calcola predict_proba → prob_alterato (colonna 1)
#    → score_genuinita = (1 - prob_alterato) * 100
# 6) Stampa per ogni casa del test: score_genuinita, classe prevista,
#    classe reale
# 7) Stampa accuracy, recall, precision, F1
# 8) Assert: recall >= 0.5

print("\n" + "="*60)
print("ESERCIZIO 7 — RETRIEVAL")
print("="*60)


# ESERCIZIO 8 (Analisi — collegamento al prodotto):
# 1) Usando il classificatore LogisticRegression scalato dell'es.7 (o
#    allenatone uno nuovo): stampa i coefficienti del modello con il
#    nome della feature, ordinati per valore assoluto (come `motivi_top_n`
#    del cap.03, ma questa volta per un CLASSIFICATORE).
# 2) Simula il semaforo: usando le soglie del Blueprint
#    (score >= 85 → verde, 60-84 → giallo, < 60 → rosso),
#    assegna un semaforo a ogni casa del test set.
# 3) Stampa un DataFrame con colonne:
#    indice | score_genuinita | semaforo | classe_reale | classe_prevista
# 4) In un commento: conta quanti verdi/gialli/rossi ci sono.
#    Quanti rossi sono effettivamente "costosi" (classe 1)?
#    Questo corrisponde alla logica "rosso = pratica sospetta da bloccare"?

print("\n" + "="*60)
print("ESERCIZIO 8 — Prodotto")
print("="*60)


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
#    a) Crea il target binario "costosa" (>= mediana del prezzo)
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
#    non la sua importanza. Se "metri_quadri" va da 30 a 200 e "piano" da
#    1 a 10, i pesi non sono confrontabili. Lo StandardScaler li porta
#    sulla stessa scala → i coefficienti diventano confrontabili.
# 2) No, funzionerà male. Il modello è stato addestrato su X_train (non
#    scalato) ma sta predicendo su X_test_scaled (scalato). Le feature
#    sono su scale diverse tra training e inferenza → le previsioni
#    saranno incoerenti. Bisogna fare fit su X_train, poi transform
#    sia su X_train sia su X_test, e usare i dati scalati per ENTRAMBI
#    fit e predict.
# 3) L'ordine corretto è mean_absolute_error(y_test, y_pred), non
#    (y_pred, y_test). La convenzione sklearn è sempre:
#    REALE prima, PREVISTO dopo. Con MAE il risultato numerico è lo
#    stesso, ma con altre metriche (es. precision_score) l'inversione
#    cambia il valore.
# 4) grandi; alcuni errori molto grandi (outlier nelle previsioni)
# 5) Il bias-varianza è il compromesso tra un modello troppo semplice
#    (alto bias, underfitting) e uno troppo complesso (alta varianza,
#    overfitting). Es: un DecisionTree con max_depth=1 è troppo semplice
#    (bias alto); con max_depth=None si adatta a ogni rumore nel train
#    (varianza alta). Il punto ottimale è nel mezzo (es. max_depth=3-6).
# 6) Dopo lo scaling, i coefficienti indicano l'importanza relativa di
#    ogni feature: quanto contribuisce alla previsione, confrontabile
#    con le altre. I 3 coefficienti più alti in valore assoluto diventano
#    i motivi_top3 per spiegare all'operatore PERCHÉ il modello ha dato
#    quel risultato. Es. "delta_netto_lordo ha il peso più alto →
#    questa feature è la principale responsabile dello score."
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Falso. Se il dataset è sbilanciato (es. 95% genuino, 5% alterato),
#    un modello che dice SEMPRE "genuino" ha accuracy 95% ma recall 0%
#    sulla classe alterato — non trova nessun problema.
# 2) TN=80, FP=10, FN=5, TP=5. Totale=100.
#    Accuracy = (80+5)/100 = 85%
#    Precision = 5/(5+10) = 0.333
#    Recall = 5/(5+5) = 0.50
#    F1 = 2*(0.333*0.50)/(0.333+0.50) = 0.40
#    Il modello trova solo metà dei positivi (recall=0.50) e molti
#    di quelli che chiama positivi sono falsi allarmi (precision=0.33).
#    Per il prodotto: insufficiente.
# 3) L'ordine è invertito. Deve essere precision_score(y_test, y_pred),
#    non (y_pred, y_test). Con precision_score l'inversione cambia il
#    valore calcolato (scambia TP con TN, FP con FN).
# 4) recall; FN (False Negative); FP (False Positive)
# 5) `predict` restituisce la classe (0 o 1). `predict_proba` restituisce
#    la probabilità per ogni classe (array con 2 colonne: P(classe 0) e
#    P(classe 1)). Per score_genuinita serve predict_proba, perché
#    score_genuinita = (1 - prob_alterato) * 100, e prob_alterato è la
#    colonna 1 di predict_proba.
# 6) [Risposta Feynman — esempio valido:
#    "Precision: se l'allarme suona 10 volte, quante volte c'è davvero
#    un ladro? Se 8 su 10 → precision 80%.
#    Recall: su 10 furti reali, quante volte ha suonato l'allarme?
#    Se ha suonato per 7 → recall 70%, 3 ladri passati inosservati.
#    Nel controllo documentale il recall è più importante: meglio qualche
#    falso allarme (il consulente controlla un doc buono) che lasciar
#    passare un documento alterato."]
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
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score, recall_score
# clf = DecisionTreeClassifier(random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print(accuracy_score(y_test, y_pred))
# print(recall_score(y_test, y_pred))
#
# ESERCIZIO 5 (DEBUG) — Bug:
# X_dbg contiene ANCORA la colonna "prezzo_euro"! Non è stata droppata.
# Dato che "costosa" è derivata dalla mediana del prezzo, il prezzo
# è un predittore perfetto del target → data leakage. Il modello
# impara la soglia del prezzo, non le feature reali.
# Correzione: aggiungere "prezzo_euro" (e derivati) alla lista drop:
# X_dbg = case_e.drop(columns=["id", "costosa", "prezzo_euro"] +
#   [c for c in case_e.columns if "prezzo" in c or "fascia" in c])
