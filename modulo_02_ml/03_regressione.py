"""
============================================================================
MODULO 2 — CAPITOLO 03: Regressione Lineare — Dal Decision Tree alla Retta
============================================================================

Analogia pratica:
- Cap.02: hai costruito il tuo primo modello (Decision Tree) e misurato
  se funziona con MAE, R² e baseline. Come un muratore che sa usare il
  martello.
- Cap.03: aggiungi un secondo strumento — la regressione lineare.
  È come passare dal martello al trapano: non è migliore in assoluto,
  è migliore PER CERTI lavori. E impari a scegliere quando usare quale.

Confronto web:
- PHP/JS: scegli tra MySQL e MongoDB in base al problema.
  Non ce n'è uno "migliore" — dipende dai dati e dal caso d'uso.
- Machine Learning: scegli tra modello lineare e albero in base alla
  struttura dei dati. Se la relazione è lineare, la retta vince.
  Se è complessa e non lineare, l'albero vince.
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.preprocessing import StandardScaler

# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da cap.02 M2
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Il preprocessing (scaling, encoding) va calcolato sull'intero dataset
# PRIMA dello split train/test."
# Rispondi V o F e spiega perché.
# Falso, solo l'encoding deve essere fatto su tutto il data set. Mentre ad esempio lo one-hot encoding deve essere fatto su dutto il dataset, in quanto in generale i modelli come il decision tree non accettano feature categoriche, Lo scaling deve essere fatto solo sul train. Questo perchè dobbiamo essere sicuri si non fare leakage quando ad esempio, facendo scaling, calcoliamo la media di alcune feature: in questo modo, i dati del test starebbero subdolamente entrando nel trai, alterando la genuinità poi della valutazione finale
#
# DOMANDA 2 — Prevedi l'output:
#   modello = DecisionTreeRegressor(max_depth=2)
#   modello.fit(X_train, y_train)
#   y_pred = modello.predict(X_train)
#   print(r2_score(y_train, y_pred))
# Il valore sarà vicino a 1.0 o a 0.5? Perché?
# vicino a 1 , perchè lo stiamo testando sullo stesso data set su cui lo abbiamo addestrato
#
# DOMANDA 3 — Trova l'errore:
#   mae = (mean_absolute_error(y_test, y_pred), 2)
#   print(f"MAE: {mae}")
# Cosa stampa? Perché non è un numero arrotondato?
# perchè manca il round davanti le parentesi
#
# DOMANDA 4 — Completa:
#   Per verificare che un modello sia utile, lo confronto con la ___ .
#   Se il modello non la batte, significa che ___ .
# baseline, fa peggio della semplice media
#
# DOMANDA 5 — Definizione:
# Qual è la differenza tra valutare un modello sul training set e
# valutarlo sul test set? Perché il primo è un anti-pattern?
# la differenza sta nel fatto che valutandolo sul train set, lo stiamo valutando nel trovare i valori sui cui lui si è addestrato, ed il rischio è che non abbia generalizzato alcuna regola, ma più probabilmente ha imparato a memoria dei pattern, oppure ovefittato aderendo troppo ai dati. In questo modo il nostro modello sarà estremamente preciso nei dati train, ma potenzialmente scadente quando fornirò previsioni su dati che non conosce. Valutarlo sul test, che è un dataset che il modello non ha mai visto, ci da un idea chiara di come se la cava con le regole generali del contesto su cui lui deve fornire le sue previsioni, senza il rischio che stia per così dire "barando".
#
# DOMANDA 6 — Completa:
#   gap_r2 = r2_train - r2_test. Se gap_r2 è molto alto (es. 0.5),
#   il modello soffre di ___ . Per ridurlo in un Decision Tree posso ___ .
# overfitting, fare tuning sugli iperparametri, come ad esempio ridurre la max_depth


# ==========================================================================
# 🔁 RINFORZO MIRATO — Lacuna #12 (reshape / numero di elementi)
# ==========================================================================
#
# Al quiz del cap.09 avevi guardato la sintassi di reshape prima di
# verificare che il numero totale di elementi combaci.
# Regola: PRIMA conta gli elementi (.size), POI scegli la forma.
#
# Esempio:
#   arr = np.arange(12)        # 12 elementi
#   arr.reshape(3, 4)          # 3×4 = 12 → OK
#   arr.reshape(5, 5)          # 5×5 = 25 ≠ 12 → ERRORE!
#
# Prova subito (rispondi nei commenti):
# 1) np.arange(24).reshape(4, 6) — funziona? Perché?
# Si funziona, perche 4*6 = 24
# 2) np.arange(24).reshape(5, 5) — funziona? Perché?
# No, non fuziona, perche 5*5 = 25 


# ==========================================================================
# 🔁 RINFORZO MIRATO — Pattern #21: virgola = tupla, non round
# ==========================================================================
#
# Nel cap.02 hai scritto (mae_test, 2) pensando di arrotondare.
# In realtà la virgola crea una TUPLA con due elementi: (28981.48, 2).
#
# Confronto rapido:
#   risultato_sbagliato = (mae_test, 2)         # → tupla!
#   risultato_corretto  = round(mae_test, 2)    # → numero arrotondato
#
# È lo stesso meccanismo per cui x = 3, crea una variabile, ma
# x = 3, 4 crea una tupla (3, 4). La virgola ha un significato
# speciale in Python — non è solo "separatore" come in JS o PHP.
#
# Prova subito:
# x = 3.14159
# a = (x, 2)
# b = round(x, 2)
# print(type(a), a)     # → tupla, (3.14159, 2)
# print(type(b), b)     # → float, 3.14


# ==========================================================================
# PARTE 1: Regressione Lineare — L'Idea
# ==========================================================================
#
# Il Decision Tree risponde con una serie di domande sì/no e arriva a
# un "contenitore" con un valore. È potente ma a volte "spigoloso":
# per dati molto diversi può dare lo stesso prezzo (stesso nodo foglia).
#
# La regressione lineare è un'altra filosofia: cerca una RETTA (o un
# piano, in più dimensioni) che minimizza la distanza dai punti reali.
#
# L'equazione è semplice:
#
#   prezzo = w1 × metri_quadri + w2 × anno + w3 × piano + ... + b
#
# Dove:
# - w1, w2, w3... sono i COEFFICIENTI (o "pesi") — quanto conta ogni
#   feature nella previsione. Se w1 = 2500, significa che ogni metro
#   quadro in più aggiunge circa 2500 € al prezzo stimato.
# - b è l'INTERCETTA — il valore base quando tutte le feature sono zero.
#   Non ha sempre un significato reale (una casa con 0 mq non esiste),
#   ma serve alla formula per "partire dal punto giusto".
#
# Confronto web:
# È come una funzione PHP/JS che calcola un punteggio pesato:
#
#   // JavaScript
#   function stimaPrezzo(mq, anno, piano) {
#       return 2500 * mq + 800 * anno + 1200 * piano - 1500000;
#   }
#
# La differenza? In JS quei numeri li scegli tu a mano.
# In ML, li CALCOLA il modello automaticamente dai dati (con .fit()).
#
# Quando preferire la regressione lineare al Decision Tree?
# - Se la relazione tra feature e target è circa LINEARE (più mq →
#   più prezzo, in modo proporzionale) → la retta funziona bene.
# - Se la relazione è complessa, con soglie e interazioni → l'albero
#   è migliore.
# - Nel dubbio? Prova entrambi e confronta le metriche sul TEST.
#
# Nel tuo prodotto documentale:
# Lo score_genuinita potrebbe dipendere linearmente da alcune feature
# (es. delta_netto_lordo, ratio_trattenute) — la regressione ti dice
# QUANTO pesa ogni feature nella previsione, cosa che un albero non fa
# in modo così diretto. Questo è prezioso per le "motivazioni" (motivi_top3):
# "Il documento è sospetto perché il delta netto-lordo pesa molto
# negativamente nello score."

print("\nPARTE 1 — Regressione Lineare: l'idea")

path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)

# Feature engineering (come nel cap.02)
case["eta_casa"] = 2026 - case["anno_costruzione"]
case["prezzo_al_mq"] = (case["prezzo_euro"] / case["metri_quadri"]).round(2)

# One-hot encoding
case_encoded = pd.get_dummies(case, columns=["citta"], dtype=int)

# X e y (anti-leakage: escludi tutto ciò che contiene il target)
cols_to_drop = (
    ["id", "prezzo_euro", "prezzo_al_mq"]
    + [c for c in case_encoded.columns if "fascia" in c]
)
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded["prezzo_euro"]

# Split (stesso random_state del cap.02 per confrontabilità)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Alleniamo una regressione lineare
modello_lin = LinearRegression()
modello_lin.fit(X_train, y_train)

# I coefficienti: quanto "pesa" ogni feature
print("\nCoefficienti del modello lineare:")
for nome, peso in zip(X.columns, modello_lin.coef_):
    print(f"  {nome:25s} -> {peso:>12,.1f} EUR")
print(f"  {'(intercetta)':25s} -> {modello_lin.intercept_:>12,.1f} EUR")

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Guarda i coefficienti stampati: quale feature ha il peso più alto
#    (in valore assoluto)? Ha senso che sia quella?
# 2) L'intercetta è negativa o positiva? Cosa significa intuitivamente?
# 3) In 1 riga: perché i coefficienti sono utili per spiegare le
#    previsioni a un collega non tecnico? (Pensa a motivi_top3
#    nel prodotto documentale.)
# 1) => Il coefficente con maggior peso in termini di valore assoluto è costituito dalla colonna "Roma": potrebbe aver senso che sia quello perchè Roma è la capitale d'Italia ed ha senso che il fatto che l'immobile si trovi li ha molta rilevanza nel determinare il valore dell'immobile.
# 2) => L'intercetta è negativa. intuitivamente se ne deduce che i coefficenti, moltiplicati per il valore relativo ad ognuno di loro, poi sommati tra loro, producono un numero positivo che è maggiore in termini di valore assoluto a quello dell'intercetta, visto che non esiste una casa nella realtà che abbia costo in euro negativo.
# 3) i coefficenti danno un idea abbastanza immediata dell'importanza relativa delle vare feature, in modo da capire quasi istantaneamente, come per una fotografia, la situazione generale di un mercato come quello immobiliare 


# ==========================================================================
# PARTE 2: LinearRegression vs DecisionTree — Confronto Pratico
# ==========================================================================
#
# Non basta sapere che esistono due modelli — devi sapere CONFRONTARLI
# sugli stessi dati, con le stesse metriche, per decidere quale usare.
#
# Qui alleniamo entrambi sullo stesso split e misuriamo:
# - MAE (errore medio)
# - RMSE (errore medio che penalizza gli sbagli grossi — novità!)
# - R² (quanto il modello spiega la variabilità)
#
# RMSE — Root Mean Squared Error (novità di questo capitolo)
# ─────────────────────────────────────────────────────────
# MAE tratta tutti gli errori allo stesso modo: se sbagli di 10€ o di
# 100.000€, il MAE li media senza differenze.
# RMSE invece PENALIZZA gli errori grandi: prima eleva al quadrato
# ogni errore (così quelli grossi pesano molto di più), poi fa la media,
# poi prende la radice per tornare alla stessa unità del target (€).
#
# Quando preferire RMSE al MAE?
# - Se nel tuo dominio un errore grosso è molto peggio di tanti piccoli
#   (es. sottovalutare di 200.000€ una casa è peggio di sbagliare
#   20 case di 10.000€ ciascuna) → RMSE ti avvisa prima.
# - Nel prodotto documentale: se classifichi come "genuino" un documento
#   con score_genuinita reale di 20 (rosso) → errore enorme, RMSE lo
#   penalizza pesantemente.
#
# Confronto rapido:
# - MAE ≈ RMSE → errori distribuiti uniformemente, pochi outlier
# - RMSE >> MAE → ci sono errori grandi (outlier), il modello sbaglia
#   molto su alcuni casi

print("\nPARTE 2 — Confronto LinearRegression vs DecisionTree")

# Decision Tree (stesso max_depth del cap.02)
modello_tree = DecisionTreeRegressor(max_depth=4, random_state=42)
modello_tree.fit(X_train, y_train)

# Previsioni
y_pred_lin_train = modello_lin.predict(X_train)
y_pred_lin_test = modello_lin.predict(X_test)
y_pred_tree_train = modello_tree.predict(X_train)
y_pred_tree_test = modello_tree.predict(X_test)

# Baseline (media del training — ricordi il cap.02?)
y_baseline = np.full_like(y_test, y_train.mean())

# Metriche
risultati = []
for nome, y_tr, y_te in [
    ("Baseline", y_baseline, y_baseline),
    ("LinearRegression", y_pred_lin_train, y_pred_lin_test),
    ("DecisionTree(d=4)", y_pred_tree_train, y_pred_tree_test),
]:
    if nome == "Baseline":
        mae_tr, r2_tr, rmse_tr = "-", "-", "-"
    else:
        mae_tr = round(mean_absolute_error(y_train, y_tr), 0)
        r2_tr = round(r2_score(y_train, y_tr), 3)
        rmse_tr = round(root_mean_squared_error(y_train, y_tr), 0)

    mae_te = round(mean_absolute_error(y_test, y_te), 0)
    r2_te = round(r2_score(y_test, y_te), 3)
    rmse_te = round(root_mean_squared_error(y_test, y_te), 0)

    risultati.append({
        "modello": nome,
        "mae_train": mae_tr, "mae_test": mae_te,
        "rmse_train": rmse_tr, "rmse_test": rmse_te,
        "r2_train": r2_tr, "r2_test": r2_te,
    })

confronto_df = pd.DataFrame(risultati)
print(confronto_df.to_string(index=False))

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Quale modello ha il MAE test più basso? E l'R² test più alto?
# il MAE test più basso appartiene al decision tree.
# 2) Confronta RMSE e MAE per il Decision Tree: sono simili o molto
#    diversi? Cosa ti dice questo sulla presenza di errori grandi?
# la differenza tra MAE e RMSE nel decision tree, che si attesta in circa 8000 €, ci indica che ci sono degli errori di grande entità, e che quando il modello sbaglia, sbaglia, in alcuni casi sbaglia di molto.
# 3) Entrambi i modelli battono la baseline? (Controlla MAE test)
# si entrambi si sono rivelati efficaci rispetto alla baseline
# 4) Se dovessi scegliere un modello per stimare il prezzo di una casa,
#    quale sceglieresti e perché? (Non c'è UNA risposta giusta —
#    ragiona su metriche + interpretabilità.)
# Sono entrambi efficaci, ma visti i confronti tra le metriche di entrambi, ma il linearRegression sembra essere più efficace nell'evitare errori di grande entità, quindi sceglierei quest'utlimo


# ==========================================================================
# PARTE 3: Feature Scaling — Perché Conta per la Regressione
# ==========================================================================
#
# Quando hai feature con scale molto diverse (es. metri_quadri va da
# 35 a 130, anno_costruzione va da 1968 a 2018), la regressione lineare
# può avere problemi: i coefficienti diventano difficili da interpretare
# e l'ottimizzazione può essere meno stabile.
#
# Il Decision Tree NON ha questo problema: lui fa solo confronti
# "feature > soglia?", e non gli importa se il numero è 35 o 35.000.
#
# Per la regressione lineare, è buona pratica SCALARE le feature, cioè
# portarle tutte su una scala comune.
#
# I due scaler più comuni:
#
# 1) StandardScaler — porta ogni feature a media=0, deviazione standard=1
#    Formula: x_scalato = (x - media) / deviazione_standard
#    Utile quando: i dati hanno distribuzione circa normale
#
# 2) MinMaxScaler — porta ogni feature tra 0 e 1
#    Formula: x_scalato = (x - min) / (max - min)
#    Utile quando: vuoi valori in un range fisso
#
# ⚠️ REGOLA ANTI-LEAKAGE FONDAMENTALE:
# Lo scaler si "impara" (fit) SOLO sul training set e si "applica"
# (transform) sia al training che al test.
#
# SBAGLIATO (leakage):
#   scaler.fit(X)           # fit su TUTTO il dataset
#   X_scaled = scaler.transform(X)
#   X_train, X_test = ...   # split DOPO
#
# CORRETTO:
#   X_train, X_test = ...   # split PRIMA
#   scaler.fit(X_train)     # fit SOLO sul train
#   X_train_s = scaler.transform(X_train)
#   X_test_s = scaler.transform(X_test)
#
# Perché? Se fai fit su tutto, la media e la std contengono informazioni
# dal test set — il modello "sa qualcosa" dei dati di test prima di
# vederli. È un mini-leakage: i risultati sul test sembreranno migliori
# di quanto siano davvero.
#
# Nel prodotto documentale: quando scalerai le feature dei documenti
# (delta_netto_lordo, confidence_ocr_media, ecc.), farai fit SOLO sui
# documenti di training (pratiche storiche verificate) e transform
# sui nuovi documenti da valutare.

print("\nPARTE 3 — Feature Scaling")

# Esempio pratico: StandardScaler su case
scaler = StandardScaler()

# FIT solo sul train (impara media e std dal training)
scaler.fit(X_train)

# TRANSFORM su entrambi (applica la stessa trasformazione)
X_train_scaled = pd.DataFrame(
    scaler.transform(X_train), columns=X_train.columns, index=X_train.index
)
X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X_test.columns, index=X_test.index
)

print("Prima dello scaling (X_train):")
print(f"  metri_quadri: media={X_train['metri_quadri'].mean():.1f}, "
      f"std={X_train['metri_quadri'].std():.1f}")
print(f"  anno_costr.:  media={X_train['anno_costruzione'].mean():.1f}, "
      f"std={X_train['anno_costruzione'].std():.1f}")
print("\nDopo lo scaling (X_train_scaled):")
print(f"  metri_quadri: media={X_train_scaled['metri_quadri'].mean():.4f}, "
      f"std={X_train_scaled['metri_quadri'].std():.4f}")
print(f"  anno_costr.:  media={X_train_scaled['anno_costruzione'].mean():.4f}, "
      f"std={X_train_scaled['anno_costruzione'].std():.4f}")

# Ri-alleniamo il modello lineare sui dati scalati
modello_lin_scaled = LinearRegression()
modello_lin_scaled.fit(X_train_scaled, y_train)

y_pred_scaled_test = modello_lin_scaled.predict(X_test_scaled)
mae_scaled = mean_absolute_error(y_test, y_pred_scaled_test)
r2_scaled = r2_score(y_test, y_pred_scaled_test)

print(f"\nLinearRegression SENZA scaling -> MAE test: "
      f"{mean_absolute_error(y_test, y_pred_lin_test):,.0f} EUR, "
      f"R2: {r2_score(y_test, y_pred_lin_test):.3f}")
print(f"LinearRegression CON scaling   -> MAE test: "
      f"{mae_scaled:,.0f} EUR, R2: {r2_scaled:.3f}")

# Con dataset piccoli e feature poche, la differenza può essere minima.
# Su dataset reali con 50+ feature a scale diverse, lo scaling
# fa spesso una differenza significativa.

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Dopo lo scaling, la media è ~0 e la std ~1. Perché?
# la media è zero perchè gli scarti sono espressi in valori che possono essere positivi o negativi in base alla loro relazione con la media, e la loro somma è sempre 0 nello stesso insieme. la deviazione std invece è l'unita di misura in cui vengono trasformate le grandezze, e dopo la trasformazione, tutto viene convertito nel "numero di passi tipici" di cui è composta una grandezza
# 2) Il Decision Tree ha bisogno dello scaling? Perché no?
# lo scaling non si usa nel DecisionTree perchè il modello funziona tramite domande riguardanti specifiche feature che non vengono confrontate tra di loro, e per ognuna la soglia è costruita per la specifica freature.
# 3) Cosa succede se fai scaler.fit(X) su TUTTO il dataset prima
#    dello split? Spiega il leakage in 1 riga.
# a quel punto le medie del test influiscono nel training, e quindi inquiniamo il modello.
# 4) Nel prodotto: su quale set faresti fit dello scaler —
#    pratiche storiche o pratiche nuove da verificare?
# Ovviamente pratiche storiche per il fit, poi farei il trasform su entrambe (con la sicurezza che lo farebbe sulle medie del solo train)


# ==========================================================================
# PARTE 4: Interpretare i Coefficienti — Il Valore Aggiunto della Retta
# ==========================================================================
#
# Il Decision Tree ti dà una previsione, ma non ti dice facilmente
# "questa feature è la più importante". Per capirlo serve analizzare
# feature_importances_ (che vedremo in dettaglio più avanti).
#
# La regressione lineare invece ti dà i COEFFICIENTI: numeri che
# dicono direttamente quanto "pesa" ogni feature.
#
# Attenzione: i coefficienti sono comparabili tra loro SOLO se le
# feature sono sulla stessa scala. Ecco un altro motivo per scalare!
#
# Dopo lo scaling:
# - Un coefficiente di +50.000 per "metri_quadri" e +5.000 per "piano"
#   significa che i metri quadri contano 10 volte di più del piano
#   nella previsione del prezzo.
#
# Questo è ORO per il tuo prodotto: se il modello ha un coefficiente
# alto su "delta_netto_lordo", puoi dire all'operatore:
# "Il documento è sospetto PERCHÉ il delta netto-lordo è anomalo."
# Questa è la base dei motivi_top3 — spiegabilità dal modello.

print("\nPARTE 4 — Coefficienti dopo scaling (comparabili)")

print("\nCoefficienti (modello scalato, valori assoluti ordinati):")
coef_df = pd.DataFrame({
    "feature": X.columns,
    "coef": modello_lin_scaled.coef_,
    "coef_abs": np.abs(modello_lin_scaled.coef_)
}).sort_values("coef_abs", ascending=False)

for _, row in coef_df.iterrows():
    segno = "+" if row["coef"] >= 0 else "-"
    print(f"  {segno} {row['feature']:25s}  peso: {row['coef']:>12,.1f} EUR")

print(f"\nLa feature più influente è: {coef_df.iloc[0]['feature']}")

# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Qual è la feature con il coefficiente più alto in valore assoluto?
# il valore più alto in assoluto lo hanno i metri quadri
# 2) Ha senso che sia quella? (Pensa al dominio immobiliare)
# in effetti la prima cosa che viene in mente per determinare il valore di una casa è il numero di metri quadri, quindi direi che ha molto senso
# 3) Ci sono feature con coefficiente NEGATIVO? Cosa significa?
#    (Es. se "distanza_centro_km" ha coefficiente negativo: più sei
#    lontano dal centro, più il prezzo SCENDE — ha senso?)
# si ha senso perchè alcune features rappresentano anche cose negative, quindi se il loro valore è alto per alcuni record, può determinare un prezzo più basso (come nell esempio fatto nella domanda, all'aumentare della distanza dal centro il prezzo segue un andamento più o meno opposto, e quindi scende)
# 4) Nel prodotto: se il coefficiente di "delta_netto_lordo" è molto
#    negativo, come lo spiegheresti all'operatore in linguaggio semplice?
#quando il delta tra netto/lordo è molto anomalo, il sistema abbassa pesantemente lo scoring della pratica, suggerendo un controllo più specifico sui documenti che hanno fatto scattare l'allarme.


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "La regressione lineare funziona bene quanto il Decision Tree su
# qualsiasi tipo di dati." Rispondi e spiega.
# Falso, la regressione lineare funziona bene solo per relazioni che sono quasi lineari. Possiamo aiutarlo tramite lo scaling, ma per relazioni non lineari il modello non va bene( meglio usare modelli a soglia come il DecisionTree)
#
# DOMANDA 2 — Prevedi:
# Se MAE = 15.000 e RMSE = 45.000, cosa ti dice sulla distribuzione
# degli errori del modello? (Suggerimento: RMSE >> MAE)
# Che ci sono errori molto grandi (outliner) e non solo tanti piccoli errori simili tra loro. Su alcune osservazioni il modello sbaglia di molto
#
# DOMANDA 3 — Trova l'errore:
#   scaler = StandardScaler()
#   scaler.fit(X)
#   X_scaled = scaler.transform(X)
#   X_train, X_test = train_test_split(X_scaled, test_size=0.2)
# Qual è il problema? Come lo correggi?
# Si è fatto lo scaling prima di splittare il dataset in train e test (problema di leakage);
# lo si risolve così:
# X_train, X_test = train_test_split(X, test_size=0.2)
# scaler = StandardScaler()
# scaler.fit(X_train)
# X_train_scaled = scaler.transform(X_train)
# X_test_scaled = scaler.transform(X_test)
#
# DOMANDA 4 — Completa:
#   I ___ della regressione lineare indicano quanto ogni feature
#   contribuisce alla previsione. Sono confrontabili tra feature
#   diverse SOLO se le feature sono ___ .
# coefficenti, scalate
#
# DOMANDA 5 — 💬 Spiega con parole tue:
# Perché nel tuo prodotto documentale i coefficienti della regressione
# lineare sono utili per costruire i "motivi_top3" dell'esito?
# Fai un esempio concreto con una feature a tua scelta.
# Sono utili perchè aiutano a capire il peso relativo delle feature per generare gli scoring di genuinità: ad esempio, il delta tra netto della busta paga e stipendio accreditato sul conto nel mese di riferimento nella busta è una feature molto importante, quindi deve avere un peso consistente in grado di far scattare un allarme alla minima incongruenza
#
# DOMANDA 6 — Definizione:
# Differenza tra MAE e RMSE. In quale situazione preferiresti RMSE?
# Il MAE è la media degli errori rispetto i valori reali. L'RMSE invece penalizza gli errori più grandi, aumentando il peso relativo all'interno della media. Comparando il delta tra MAE e RMSE si può avere un idea sulla composizione e distribuzione degli errori. Si usa l'RMSE nei casi in cui si vuole avere per tenere traccia in modo più chiaro degli errori di  grande entità


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================

# ESERCIZIO 1 (Facile):
# Carica case.csv, prepara X e y (con feature engineering: eta_casa),
# fai lo split 80/20 (random_state=42).
# Allena una LinearRegression e stampa:
# - I 3 coefficienti più alti (in valore assoluto) con il nome della feature
# - MAE e R² sul test
# - L'assert che il modello batte la baseline
print("\nEsercizio 1\n")

#carico il file case.csv
path_file_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file_case)

#aggiungo feature per eta casa
case['eta_casa'] = 2026 - case['anno_costruzione']

#preparo X e y (features e target)
case_encoded = pd.get_dummies(case, columns=["citta"], dtype="int")
cols_to_drop = ['prezzo_euro', 'id'] + [c for c in case_encoded.columns if ("prezzo" in c) or ("fascia" in c)]
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded['prezzo_euro']

#faccio lo split del dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

#creo il modello lienare, lo addestro e faccio la previsione sul test
modello_lineare = LinearRegression()
modello_lineare.fit(X_train, y_train)

y_pred_test = modello_lineare.predict(X_test)

#trovo la baseline 
y_baseline = np.full_like(y_test, y_train.mean())

#calcolo le metriche
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_test = r2_score(y_test, y_pred_test)

#creo un DataFrame per visualizzare i coefficenti
coef_df = pd.DataFrame({
    "feature": X_train.columns,
    "coef": modello_lineare.coef_.round(2)
})

coef_df['abs'] = coef_df['coef'].abs()


#stampo come da richiesta dell'esercizio
print(coef_df.sort_values(by="abs", ascending=False).drop(columns="abs").head(3).reset_index(drop=True))
print(f"\nMAE Test =>{round(mae_test, 2)}")
print(f"R² Score =>{round(r2_test, 3)}")

assert mae_test < mae_baseline, "il modello batte la baseline"

# ESERCIZIO 2 (Medio):
# Confronta 3 modelli sullo stesso split:
# 1) LinearRegression (senza scaling)
# 2) LinearRegression (con StandardScaler — fit solo su train!)
# 3) DecisionTreeRegressor(max_depth=4)
# Per ciascuno calcola MAE, RMSE e R² su train e test.
# Crea un DataFrame di confronto e stampalo ordinato per mae_test.
# Quale modello scegli? Motiva in 2 righe di commento.

#leggo il file csv
print("\nEsercizio 2\n")
path_file_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file_case)

#eseguo one-hot encoding delle colonne categoriche
case_encoded = pd.get_dummies(case, columns=["citta"], dtype='int')

#definisco le colonne da eliminare dalle features
cols_to_drop = ['prezzo_euro', 'id'] + [c for c in case_encoded.columns if ('fascia' in c) or ('prezzo' in c)]

#divido le features dal target
X = case_encoded.drop(columns=cols_to_drop, errors='ignore')
y = case_encoded['prezzo_euro']

#faccio lo split in train e test

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

#assegno i modelli a delle variabili
modello_albero= DecisionTreeRegressor(max_depth=4)
modello_lineare = LinearRegression()
modello_lineare_scalato = LinearRegression()

#creiamo uno StandardScaler
scaler = StandardScaler()

# FIT solo sul train (impara media e std dal training)
scaler.fit(X_train)

# TRANSFORM su entrambi (applica la stessa trasformazione)
X_train_scaled = pd.DataFrame(
    scaler.transform(X_train), columns=X_train.columns, index=X_train.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X_test.columns, index=X_test.index
)

#Alleno i tre modelli
modello_albero.fit(X_train, y_train)
modello_lineare.fit(X_train, y_train)
modello_lineare_scalato.fit(X_train_scaled, y_train)

#facciamo le previsioni sul test
y_pred_albero_test = modello_albero.predict(X_test)
y_pred_albero_train = modello_albero.predict(X_train)

y_pred_lin_test = modello_lineare.predict(X_test)
y_pred_lin_train = modello_lineare.predict(X_train)

y_pred_lin_scl_test = modello_lineare_scalato.predict(X_test_scaled)
y_pred_lin_scl_train = modello_lineare_scalato.predict(X_train_scaled)

#per ognuno creiamo le metriche per la valutazione, sia train che test
mae_test_albero = mean_absolute_error(y_test, y_pred_albero_test)
r2_test_albero = r2_score(y_test, y_pred_albero_test)
rmse_test_albero = root_mean_squared_error(y_test, y_pred_albero_test)

mae_train_albero = mean_absolute_error(y_train, y_pred_albero_train)
r2_train_albero = r2_score(y_train, y_pred_albero_train)
rmse_train_albero = root_mean_squared_error(y_train, y_pred_albero_train)

#-----------------------------------------------------------------------

mae_test_lin = mean_absolute_error(y_test, y_pred_lin_test)
r2_test_lin = r2_score(y_test, y_pred_lin_test)
rmse_test_lin = root_mean_squared_error(y_test, y_pred_lin_test)

mae_train_lin = mean_absolute_error(y_train, y_pred_lin_train)
r2_train_lin = r2_score(y_train, y_pred_lin_train)
rmse_train_lin = root_mean_squared_error(y_train, y_pred_lin_train)

#-----------------------------------------------------------------------

mae_test_lin_scl = mean_absolute_error(y_test, y_pred_lin_scl_test)
r2_test_lin_scl = r2_score(y_test, y_pred_lin_scl_test)
rmse_test_scl = root_mean_squared_error(y_test, y_pred_lin_scl_test)

mae_train_lin_scl = mean_absolute_error(y_train, y_pred_lin_scl_train)
r2_train_lin_scl = r2_score(y_train, y_pred_lin_scl_train)
rmse_train_scl = root_mean_squared_error(y_train, y_pred_lin_scl_train)

#creiamo una lista di dizionari di confronto delle metriche
confronto_metriche = [
    {
    "modello": "Albero Decisionale",
    "mae_train": round(mae_train_albero, 2),
    "r2_score_train": round(r2_train_albero, 3),
    "rmse_train": round(rmse_train_albero,3),
    "mae_test": round(mae_test_albero, 2),
    "r2_score_test": round(r2_test_albero, 3),
    "rmse_test": round(rmse_test_albero,3)
    },
    
    {
    "modello": "Regressione Lineare",
    "mae_train": round(mae_train_lin, 2),
    "r2_score_train": round(r2_train_lin, 3),
    "rmse_train": round(rmse_train_lin,3),
    "mae_test": round(mae_test_lin, 2),
    "r2_score_test": round(r2_test_lin, 3),
    "rmse_test": round(rmse_test_lin,3)
    },
    
    {
    "modello": "Regressione Lineare Scalata",
    "mae_train": round(mae_train_lin_scl, 2),
    "r2_score_train": round(r2_train_lin_scl, 3),
    "rmse_train": round(rmse_train_scl,3),
    "mae_test": round(mae_test_lin_scl, 2),
    "r2_score_test": round(r2_test_lin_scl, 3),
    "rmse_test": round(rmse_test_scl,3)
    }
]

#trasformiamola in DataFrame
df_confronto = pd.DataFrame(confronto_metriche)


print(f"Confronto Modello Albero:\n{y_pred_albero_test.astype('int')}\n{y_test.values.astype(int)}\n\n")
print(f"Confronto Modello Lineare:\n{y_pred_lin_test.astype('int')}\n{y_test.values.astype(int)}\n\n")
print(f"Confronto Modello Lineare Scalato:\n{y_pred_lin_scl_test.astype('int')}\n{y_test.values.astype(int)}\n\n")

print(df_confronto.sort_values(by="mae_test"))

#Scelgo il modello lineare perchè ha ottenuto punteggi migliori nel confronto di tutte le metriche, mostrando in particolare anche una forbice meno ampia tra train e test.



# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Spiega in 8-10 righe di commento:
# - Quando preferisci un modello lineare a un albero decisionale
# - Quando preferisci un albero a un modello lineare
# - Come i coefficienti della regressione possono aiutare la
#   spiegabilità delle previsioni (pensa al tuo prodotto)
# - Cos'è il trade-off bias-varianza in questo contesto
# E' preferibile usare un modello lineare quando tra features e target esiste una relazione di tipo lineare, ossia modellabile su una retta.
# Si preferisce invece un albero decisionale quando il rapporto tra target e feature esiste una relazione di tipo non lineare, che quindi segue un andamento che può essere curvilineo. In questo caso la logica delle soglie è quella più efficace.
#La spiegabilità a partire dai coefficienti, soprattutto nell'ambito della valutazione della genuinità di un documento, è determinante. Per fare un esempio,  un delta errato tra lordo e netto in una busta paga, dovendo influire molto sullo scoring della pratica, avrà sicuramente un coefficiente con peso relativo molto elevato, rispetto ad altre feature di minore importanza.
#Il trade-off bias varianza è il compromesso tra un modello troppo semplice (under-fitting) e uno troppo complesso (over-fitting). In pratica bias e varianza sono gli estremi opposti entro cui noi dobbiamo trovare il giusto equilibrio. Per trovarlo, possiamo modulare gli iperparametri (come ad esempio la max_depth di un albero decisionale per regolare la complessità del modello), oppure lavorare sulle feature per trovare quelle più adatte e più efficaci.
#


# ESERCIZIO 4 (🔧 [REFACTORING]):
# Riscrivi questo codice in modo corretto e pulito.
# Il codice ha 3 problemi: trovali tutti e correggili.
#
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import StandardScaler
# s = StandardScaler()
# s.fit(X)
# X2 = s.transform(X)
# a,b,c,d = train_test_split(X2, y, test_size=0.2)
# m = LinearRegression()
# m.fit(a, c)
# p = m.predict(b)
# print(mean_absolute_error(p, d))
#
# Problemi da trovare: ordine scaling/split, nomi variabili,
# ordine argomenti mean_absolute_error.
print("\nEsercizio 4\n")
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

modello_lineare_scalato = LinearRegression()
modello_lineare_scalato.fit(X_train_scaled, y_train)
y_pred_test = modello_lineare_scalato.predict(X_test_scaled)
print(mean_absolute_error(y_test, y_pred_test))


# ESERCIZIO 5 (🔍 [DEBUG]):
# Questo codice gira senza errori ma produce risultati SBAGLIATI.
# Il MAE sul test è suspiciously basso (quasi zero).
# Trova il bug e spiega perché il risultato è ingannevole.
#
# case_e = pd.get_dummies(case, columns=["citta"], dtype=int)
# case_e["prezzo_al_mq"] = case_e["prezzo_euro"] / case_e["metri_quadri"]
# X_bug = case_e.drop(columns=["id", "citta_Milano"], errors="ignore")
# y_bug = case_e["prezzo_euro"]
# X_tr, X_te, y_tr, y_te = train_test_split(X_bug, y_bug, test_size=0.2, random_state=42)
# m = LinearRegression()
# m.fit(X_tr, y_tr)
# print("MAE test:", round(mean_absolute_error(y_te, m.predict(X_te)), 2))
#
# Suggerimento: guarda le colonne di X_bug. C'è qualcosa che NON
# dovrebbe essere lì? (Pensa al data leakage.)
# il problema è che la colonna prezzo_euro non è stata eliminata dalle feature, ed è stata eliminata la colonna citta_Milano (scelta da valutare), quindi in pratica si sta allenando il modello dandogli tutte le risposte che invece dovrebbe trovare lui, e si è tolta una feature che poteva invece aiutare il modello.
# correzione veloce: X_no_bug = case_e.drop(columns=["id", "prezzo_euro", "prezzo_al_mq"], errors="ignore") 

# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + Regressione):
# 1) Usando case.csv, crea un report groupby("citta") con:
#    - prezzo_medio, metri_quadri_medi, num_case
# 2) Identifica la città con più case nel dataset
# 3) Allena due modelli SOLO su quella città:
#    - LinearRegression
#    - DecisionTreeRegressor(max_depth=3)
# 4) Stampa MAE e R² test di entrambi e della baseline
# 5) Commenta in 2 righe: con pochi dati (una sola città),
#    quale modello tende a soffrire di più di overfitting?
print("\nEsercizio 6\n")
path_file_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file_case)

report = case.groupby('citta').agg(
    prezzo_medio = ('prezzo_euro', 'mean'),
    metri_quadri_medi = ('metri_quadri', 'mean'),
    num_case = ('id', 'count')    
)
#trovo la citta con il maggior numero di case in vendita
top_citta = report.sort_values(by='num_case', ascending=False).head(1).index[0]

#filtro usando .loc
case_roma = case.loc[case['citta'] == top_citta]

#creo i due modelli
modello_albero = DecisionTreeRegressor(max_depth=3, random_state=42)
modello_lineare = LinearRegression()

#scelta delle colonne da eliminare dalle features
cols_to_drop = ['prezzo_euro', 'id', 'citta'] + [c for c in case_roma.columns if ('prezzo' in c) or ('fascia' in c)]

#divido features e target
X = case_roma.drop(columns=cols_to_drop, errors='ignore')
y = case_roma['prezzo_euro']

#splitto test e train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

#addestro i modelli sul dataset del train
modello_albero.fit(X_train, y_train)
modello_lineare.fit(X_train, y_train)

#facciamo le previsioni sul test con entrambi i modelli
y_pred_albero_test = modello_albero.predict(X_test)
y_pred_albero_train = modello_albero.predict(X_train)
y_pred_lineare_test = modello_lineare.predict(X_test)
y_pred_lineare_train = modello_lineare.predict(X_train)

#creaiamo la base line 
y_baseline = np.full_like(y_test, y_train.mean())

#creiamo le metriche a partire da quella della baseline
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)

#metriche modello albero per train e test
mae_train_albero = mean_absolute_error(y_train, y_pred_albero_train)
mae_test_albero = mean_absolute_error(y_test, y_pred_albero_test)
r2_train_albero = r2_score(y_train, y_pred_albero_train)
r2_test_albero = r2_score(y_test, y_pred_albero_test)

#metriche modello lineare per train e test
mae_train_lineare = mean_absolute_error(y_train, y_pred_lineare_train)
mae_test_lineare = mean_absolute_error(y_test, y_pred_lineare_test)
r2_train_lineare = r2_score(y_train, y_pred_lineare_train)
r2_test_lineare = r2_score(y_test, y_pred_lineare_test)

report_metriche = [
    {
        'modello': 'Baseline',
        'mae_train': '-',
        'mae_test': round(mae_baseline, 2),
        'r2_train': '-',
        'r2_test': round(r2_baseline, 3) 
    },
    {
        'modello': 'Decision Tree',
        'mae_train': round(mae_train_albero, 2),
        'mae_test': round(mae_test_albero, 2),
        'r2_train': round(r2_train_albero, 3),
        'r2_test': round(r2_test_albero, 3) 
    },
    {
        'modello': 'Linear Regression',
        'mae_train': round(mae_train_lineare, 2),
        'mae_test': round(mae_test_lineare, 2),
        'r2_train': round(r2_train_lineare, 3),
        'r2_test': round(r2_test_lineare, 3) 
    }
]

df_report_metriche = pd.DataFrame(report_metriche)
print(df_report_metriche)

#guardando le metriche a confronto, il Decision Tree sembra soffrire di più l'over-fitting. Lo si evince dalla forbice tra r2_score del train e r2_score del test

# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrivi da memoria):
# Senza guardare il codice sopra, riscrivi da zero:
# 1) Carica case.csv
# 2) Prepara X e y (con anti-leakage)
# 3) Split 80/20
# 4) Scala le feature con StandardScaler (fit solo su train!)
# 5) Allena una LinearRegression sui dati scalati
# 6) Calcola MAE, RMSE, R² su test
# 7) Stampa i 3 coefficienti più influenti
# 8) Assert: modello batte la baseline

print("\nEsercizio 7\n")
path_file_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file_case)

case_encoded = pd.get_dummies(case, columns=['citta'], dtype='int')
X = case_encoded.drop(columns=['id', 'prezzo_euro'])
y = case_encoded['prezzo_euro']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

modello_lineare = LinearRegression()
modello_lineare.fit(X_train_scaled, y_train)

y_pred_train = modello_lineare.predict(X_train_scaled)
y_pred_test = modello_lineare.predict(X_test_scaled)
y_baseline = np.full_like(y_test, y_train.mean())

mae_baseline = mean_absolute_error(y_test, y_baseline)

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)
rmse_train = root_mean_squared_error(y_train, y_pred_train)
rmse_test = root_mean_squared_error(y_test, y_pred_test)

df_coef = pd.DataFrame({
    'nome' : X.columns,
    'valore': modello_lineare.coef_,
})

df_coef['valore_abs'] = df_coef['valore'].abs()

print(df_coef.sort_values(by='valore_abs', ascending=False).round(2).head(3).to_string(index=False))    

assert mae_test < mae_baseline, 'il modello deve battere la baseline'



# ESERCIZIO 8 (Analisi — collegamento al prodotto):
# Usando i coefficienti del modello lineare scalato:
# 1) Crea una funzione `motivi_top_n(modello, feature_names, n=3)` che
#    restituisce una lista di stringhe tipo:
#    ["metri_quadri (+52340.2)", "eta_casa (-31200.5)", "piano (+8900.1)"]
#    (le n feature con coefficiente più alto in valore assoluto,
#    con segno + o - e valore)
# 2) Testa la funzione sul modello scalato e stampa i motivi_top3
# 3) In un commento: spiega come adatteresti questa funzione per il
#    prodotto documentale (dove le feature sarebbero delta_netto_lordo,
#    ratio_trattenute, match_cf_cross_doc, ecc.)

print("\nEsercizio 8\n")

def motivi_top_n(modello, feature_names, n=3):    
    df_coef = pd.DataFrame({
        'nome': feature_names,
        'valore': modello.coef_
    })
    df_coef['abs'] = df_coef['valore'].abs()
    df_coef_sorted = df_coef.sort_values(by='abs', ascending=False)
    report = []
    for _, row in df_coef_sorted.head(n).iterrows():
        report.append(f"{row['nome']} ({row['valore']:+.1f})")
    return report
        
print(motivi_top_n(modello_lineare_scalato, X_train.columns, 3))


#La funzione rimane sostanzialmente invariata nel suo utilizzo. inserendo come parametro il modello addestrato sullo score di genuinità, la funzione restituisce n coefficienti a partire dal più importante, il modo da avere un idea di cosa a maggiormente influito per raggiungere lo scoring.



# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Modulo 2, Cap.03
# ==========================================================================
#
# Componente pipeline: Cuore predittivo (confronto modelli)
# Deliverable: aggiorna modello_base.py aggiungendo il confronto
#              LinearRegression vs DecisionTree
#
# TASK:
# 1) Apri modello_base.py (creato nel cap.02)
# 2) Aggiungi un secondo modello: LinearRegression (con scaling)
# 3) Stampa un DataFrame di confronto con colonne:
#    modello | mae_train | mae_test | rmse_test | r2_test
# 4) Aggiungi una funzione motivi_top3() che usa i coefficienti
#    del modello lineare per spiegare le previsioni
# 5) Assert: almeno uno dei due modelli batte la baseline
#
# Definition of Done:
# - modello_base.py gira senza errori con `python modello_base.py`
# - Stampa confronto tra i modelli
# - La funzione motivi_top3() restituisce 3 stringhe sensate
# - Codice con nomi espliciti e commenti essenziali
#
# Impatto roadmap: R0 — primo confronto multi-modello + spiegabilità base


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) Falso. Il preprocessing si calcola SOLO sul training set e si applica
#    al test. Calcolare su tutto è un leakage sottile.
# 2) Vicino a 1.0 — perché sta predicendo sugli stessi dati su cui è stato
#    allenato (anti-pattern di valutazione: il modello ha "memorizzato").
# 3) Stampa una tupla (28981.48..., 2), non un numero arrotondato.
#    La virgola crea una tupla. Serve round(mean_absolute_error(...), 2).
# 4) baseline; il modello non sta imparando nulla di utile
# 5) Sul training il modello ha "visto" quei dati — il risultato è gonfiato.
#    Sul test, i dati sono nuovi → il risultato riflette la capacità reale.
#    Valutare sul training è un anti-pattern perché dà un'illusione di
#    performance che non si replica sui dati nuovi.
# 6) overfitting; ridurre max_depth (o min_samples_split, max_leaf_nodes)
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Falso. La regressione lineare funziona bene se la relazione
#    feature→target è circa lineare. Se è non lineare o con interazioni
#    complesse, l'albero è spesso migliore.
# 2) RMSE molto più alto del MAE → ci sono alcuni errori molto grandi
#    (outlier). Il modello sbaglia pesantemente su certi casi.
# 3) Leakage: lo scaler è fittato su TUTTO il dataset (incluso il test).
#    Correzione: prima split, poi scaler.fit(X_train), poi transform.
# 4) coefficienti; scalate (sulla stessa scala, es. con StandardScaler)
# 5) I coefficienti dicono QUANTO ogni feature contribuisce allo score.
#    Se delta_netto_lordo ha coefficiente -30.000, posso dire all'operatore:
#    "Lo score è basso PERCHÉ il delta netto-lordo è anomalo — questa
#    feature da sola abbassa la previsione di genuinità di ~30 punti."
#    I 3 coefficienti più grandi in valore assoluto diventano motivi_top3.
# 6) MAE = media degli errori assoluti (stessa unità del target, facile
#    da spiegare). RMSE = radice della media degli errori al quadrato
#    (penalizza errori grandi). Preferisci RMSE quando un errore grosso
#    è molto peggio di tanti piccoli (es. classificare come genuino un
#    documento rosso è catastrofico, non solo "un errore in più").
#
# --- RISPOSTE ESERCIZI ---
#
# ESERCIZIO 5 (DEBUG) — Soluzione:
# X_bug contiene "prezzo_euro" come feature! Non è stato droppato.
# Il modello usa il prezzo (il target stesso) per prevedere il prezzo
# → data leakage perfetto → MAE ≈ 0. In più "prezzo_al_mq" è
# derivato dal prezzo → doppio leakage.
# Correzione: X = case_e.drop(columns=["id", "prezzo_euro", "prezzo_al_mq"])
