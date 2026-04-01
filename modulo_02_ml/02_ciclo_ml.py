"""
============================================================================
MODULO 2 — CAPITOLO 02: Il Ciclo Completo del Machine Learning
Dal dato grezzo alla previsione: preprocessing → split → train → evaluate
============================================================================

Analogia pratica:
- Capitolo 01: hai capito COSA fa il ML e perché serve.
- Capitolo 02: costruisci il tuo PRIMO modello, passo dopo passo,
  e impari a misurare se funziona davvero.

Confronto web:
- PHP/JS: testi un endpoint con 2-3 chiamate manuali e dici "funziona".
- Machine Learning: testi su dati MAI visti dal modello e misuri errore reale.
"""

import pandas as pd
import numpy as np
import os

# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da cap.01 M2
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Le feature (X) sono un DataFrame, il target (y) è una Series." Vero
#
# DOMANDA 2 — Prevedi l'output:
#   X = case[["metri_quadri", "anno_costruzione"]]
#   print(X.shape)
# Se case ha 50 righe, cosa stampa? (50, 2)
#
# DOMANDA 3 — Trova l'errore:
#   y = case[["prezzo_euro"]]
#   # Ora y è pronto come target per un modello.
# Cosa c'è di sbagliato? Il targer di un modello deve essere definito come Series, la sintassi scritta sopra genererebbe un DataFrame con shape (n, 1)
#
# DOMANDA 4 — Completa:
#   Per selezionare righe con etichetta uso .loc ;
#   per selezionare righe con posizione numerica uso .iloc
#
# DOMANDA 5 — Definizione:
# Cos'è il data leakage? Fai un esempio concreto dal dominio documentale.
# il leakege avviene quando il target in maniera diretta o indiretta, finisce all'interno delle feature che il machine learnig utilizza per addestrarsi. Un esempio può
# essere quando all'interno della label di un documento reddituale, lo scoring di genuinità finisce tra le feature che il modello usa per trovare proprio quello scoring 
# in altri documenti. In questo caso avviene che nei test il modello risponde in maniera praticamente perfetta su dati test, ma quando invece si presentano documenti reali
# (che non hanno associato ancora uno scoring genuinità perchè sono documenti su cui non esiste alcuna prova a riguardo) le prestazioni del modello crollano. In sintesi,
# il modello deve fare affidamento solo su dati e feature che può trovare all'interno di ogni documento che analizza, e non su assunzioni postume fatte da chi lo sta addestrando

# DOMANDA 6 — 💬 Spiega con parole tue:
# Qual è la differenza tra valutare il modello sui dati di training
# e valutarlo su un test set separato? Perché la prima è un anti-pattern?
# E' un anti patter perchè sarebbe come chiedere a un modello di prevedere qualcosa che ha già visto. Per fare un esempio concreto, non è corretto fare scommesse 
# su una partità che si è già vista (come Beef di ritorno al futuro). In questo caso, il modello conosce già l'esito. I test vanno eseguiti su dati che il modello non ha 
# mai visto, solo in questo modo si può capire quanto effettivamente sia diventato bravo nella sua capacità di predizione.

# ==========================================================================
# 🔁 RINFORZO MIRATO — Anti-pattern di valutazione del modello
# ==========================================================================
#
# Al quiz del cap.01 ti è stato chiesto di citare un anti-pattern di
# VALUTAZIONE del modello. Hai risposto con un errore di feature selection
# ("feature non coerenti"), che è un problema reale ma riguarda la
# PREPARAZIONE dei dati, non la valutazione.
#
# Rivediamolo con chiarezza:
#
# Anti-pattern di PREPARAZIONE dati:
# - Mettere il target nelle feature (leakage)
# - Scegliere feature irrilevanti o ridondanti
# - Non pulire i dati (outlier, missing, encoding)
#
# Anti-pattern di VALUTAZIONE del modello:
# - Valutare sul training set → il modello ha "memorizzato" quei dati,
#   il risultato è gonfiato (come farsi le domande dell'esame che hai già visto)
# - Fare tuning degli iperparametri guardando il test set → il test
#   non è più "sconosciuto", perde il suo ruolo di giudice imparziale
# - Usare la metrica sbagliata → es. accuracy con classi sbilanciate
#   (99% genuini, 1% alterati → accuracy 99% anche senza modello!)
# - Split non corretto → es. mescolare documenti della stessa pratica
#   tra train e test (leakage temporale/pratica)
#
# Esempio dal tuo prodotto:
# Immagina di allenare il classificatore genuino/alterato su 100 pratiche,
# e di testarlo sulle STESSE 100 pratiche. Score: 98%. Sembra perfetto.
# Ma su 20 pratiche nuove mai viste: score 62%. Il modello ha memorizzato,
# non ha imparato.
#
# Prova subito:
# 1) Scrivi qui sotto 2 anti-pattern di valutazione (NON di preparazione dati).
# 2) Spiega in 1 riga perché valutare sul training set è ingannevole.
# fare validation usando il test set, che invece deve rimanere solo come "esame finale". Bisogna invece essere categorici e utilizzare i dati del test sono dopo la fase di validation
# sceglere la metrica sbagliata per il tipo di target che mi sono prefissato. Con i documenti reddituali è importante avere un accuracy alta, ma senza una recall alta diventa inutile.
# Valutare sul training test è ingannevole perchè è come valutare quanto si è bravi a predire il tempo meteorologico, allenandoci a fare solo previsioni solo sul meteo del giorno prima. In questo caso, sapendo già a monte la risposta, non avremmo idea di quanto siamo effettivamente efficaci con previsioni di cui non sappiamo l'esito finale.


# ==========================================================================
# 🔁 RINFORZO MIRATO — loc vs iloc
# ==========================================================================
#
# Al cap.01 hai usato .loc correttamente con mask booleane e nomi colonne.
# Ma .iloc (selezione per posizione numerica) non è ancora stato praticato.
#
# Rivediamoli fianco a fianco:
#
# .loc → usi NOMI (etichette) di righe e colonne
#   case.loc[mask, "prezzo_euro"]          → tutte le righe dove mask è True, colonna prezzo
#   case.loc[0:3, "metri_quadri"]          → righe con indice 0, 1, 2, 3 (incluso!)
#
# .iloc → usi NUMERI (posizioni), come gli indici di un array
#   case.iloc[0:3, 0]                      → prime 3 righe (0,1,2 — 3 escluso!), prima colonna
#   case.iloc[-1]                           → ultima riga
#
# Attenzione al tranello:
# .loc[0:3] include la riga 3 (è un'etichetta)
# .iloc[0:3] esclude la posizione 3 (è un indice, come range() e slicing)
#
# Prova subito:

path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)
print(case.iloc[5:10, case.columns.get_indexer(['citta', 'prezzo_euro'])])
print(case.loc[5:9, ["citta", "prezzo_euro"]])

# 1) Stampa le prime 3 righe usando .iloc (NON .head())
# 2) Stampa le colonne "citta" e "prezzo_euro" delle righe 5-9 usando .iloc
# 3) Stampa le stesse righe 5-9 usando .loc con gli stessi nomi colonna
# 4) Confronta: il risultato è lo stesso? Perché?
# Il risultato è identico perchè andiamo a stampare gli stessi valori nelle stesse posizioni del dataframe, la differenza sta nel modo in cui
# vi accediamo: il primo tramite indici numerici, il secondo tramite etichette


# ==========================================================================
# 🔁 RINFORZO MIRATO — is not None vs if var: (terminologia Python)
# ==========================================================================
#
# Nel cap.01 hai spiegato bene il concetto di valori falsy, ma nella risposta
# hai scritto "null" invece di "None". In Python il valore nullo si chiama
# None (con la N maiuscola). null è JavaScript, NULL è PHP.
#
# Riepilogo rapido:
# JavaScript: null, undefined     → falsy
# PHP:        NULL, false, 0, ""  → falsy
# Python:     None, False, 0, "" → falsy
#
# La regola d'oro per parametri opzionali:
#   if parametro is not None:   # ✅ controlla solo se è stato passato
#   if parametro:               # ⚠️ rischio: esclude anche 0, False, ""
#


# ==========================================================================
# PARTE 1: Il Ciclo ML — Panoramica
# ==========================================================================
#
# Ogni progetto ML serio segue un ciclo. Non si parte dal modello:
# si parte dal problema e dai dati. Il modello arriva dopo.
#
# Ecco il ciclo nella sua forma più semplice:
#
# 1) DOMANDA DI BUSINESS — Cosa voglio prevedere? Per chi? Perché?
#    Nel tuo caso: "Questo documento è genuino o alterato?"
#
# 2) RACCOLTA DATI — Dove sono i dati? Sono puliti? Sono sufficienti?
#    Nel tuo caso: pratiche storiche con documenti già verificati.
#
# 3) ESPLORAZIONE (EDA) — Come sono fatti i dati? Distribuzioni, anomalie,
#    valori mancanti, correlazioni. Questo lo hai già fatto al cap.01 con
#    report .agg, groupby, pd.cut.
#
# 4) PREPROCESSING — Pulizia e trasformazione: gestire valori mancanti,
#    scalare le feature, codificare le categoriche (one-hot encoding),
#    creare nuove feature (feature engineering).
#
# 5) SPLIT — Dividere i dati in train, validation e test.
#    Ricordi l'analogia? Train = studiare, validation = simulazione,
#    test = esame finale.
#    ⚠️ Nel tuo prodotto: lo split va fatto per PRATICA (tutti i documenti
#    di una pratica stanno insieme) e possibilmente per TEMPO (pratiche
#    recenti nel test). Mescolare documenti della stessa pratica tra
#    train e test sarebbe leakage.
#
# 6) TRAINING — Allenare il modello sui dati di training.
#    Il modello cerca una "regola numerica" che minimizza l'errore.
#
# 7) VALUTAZIONE — Misurare le performance sul test set (MAI sul training!).
#    Metriche: per classificazione → precision, recall, F1.
#    Per regressione → MAE, RMSE, R².
#
# 8) ITERAZIONE — Se non va bene: cambiare feature, modello, iperparametri.
#    Poi tornare al punto 4 o 5. Non al punto 7 (mai "aggiustare" il test).
#
# Questo ciclo è lo stesso per qualsiasi progetto ML, dal più semplice
# al più complesso. È il tuo "pilota automatico" professionale.

print("\nPARTE 1 — Il Ciclo ML")
print("Domanda → Dati → EDA → Preprocessing → Split → Train → Evaluate → Iterare")

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# Riscrivi il ciclo ML in 8 punti applicato al tuo prodotto documentale.
# Per ogni punto scrivi UNA frase concreta (non generica).
# Esempio punto 1: "La domanda è: dato un set di documenti reddituali di
# un cliente, qual è la probabilità che siano genuini?"


# 1) Voglio creare un applicativo che sia in grado di prendere in input un documento o più documenti reddituali di una persona, e in out put
# restituire un semaforo, uno scoring per coerenza fiscale, numerica, grafica e di metadati (ognuno di quali accompagnato da una motivazione testuale) che possa aiutare un gestore fidi o un consulente finanziario a capire il rischio di manomissione documentale di una pratica di finanziamento o di mutuo.

#2) il Dataset sarà formato da documenti alterati (già verificati come tali, per diverse ragioni) e da documenti invece all 100% genuini. In particolare per le buste paghe, i modelli unici, e le certificazioni uniche verranno forniti molti esempi per ogni tipo di software di elaborazione paghe, così per ogni formato sarà possibile essere accurati (dato che molte volte le buste paghe differiscono anche in modalità di calcolo e voci riportate). Inoltre verranno forniti sia documenti pdf nativi sia scansioni, per poter avere un dataset trasversale in grado di analizzare le incogruenze eliminando il rumore di fondo causato dai campiamento di tipo di immagine fornita.

#3/ 4) In seguito , i dati vengono analizzati per capire quali sono gli elementi mancanti o di potenziale disturbo, prima di procedere con la pulizia e poi con la creazione delle feature adatte per il machine learning: ad esempio sezioni della busta paga mancanti, o voci di retribuzioni poco usate e quindi che possono generare dei falsi positivi nell'analisi di contraffazione.

#5) Dopo di che il dataset verrà organizzato in trainig, validation e test. Questo split deve tenere in considerazione anche che i  redditi, anche se divisi in tipologia, ognuno di loro appartiene a una pratica distinta per persona e per data, quindi importante che le pratiche non vengano divise a "metà", di cui una parte inserita in training e l'altra in test. Devono essere trattare come organismi unici, e al loro interno ogni organo distinto deve essere analizzato sia in quanto documento appartente a una categoria (quindi una busta paga deve rispettare i pattern appartenenti a quel tipo di busta paga di quello specifico software di elaborazione paghe) sia in relazione alla pratica nel suo complesso (es. se in busta per ottobre viene riportato un netto di 1000 euro e sul conto invece compare per quel mese un accredito di 1500 euro, questa incongruenza deve essere segnalata come anomalia indice di una possibile manomissione). 

#6) Si allena il modello con la fase di training, facendo tuning degli iperparametri e aggiustando le feature per ottimizzare il risultato desiderato, . 

#7) alla fine si fa un test per vedere se le metriche raggiungono livelli soddisfacenti rispetto il nostro benchmark. Ossia si forniscono in fase di test sia documenti genuini che alterati( in ognuno dei 4 macrosettori stabiliti, o solo su uno o alcuni di essi), e si verificano le metriche per capire il livello di accuracy, precision e f1 che il modello (o i modelli creati) raggiunge. Nel nostro caso una recall quasi perfetta è necessaria, poichè meglio un falso positivo che un positivo mancato.

#8) si ripercorrono i passi precedenti fino a raggiungere il benchmark stabilito.


# ==========================================================================
# PARTE 2: Preprocessing — Preparare i Dati per il Modello
# ==========================================================================
#
# Un modello ML non capisce "Milano" o "Roma". Capisce solo numeri.
# Il preprocessing trasforma i dati grezzi in una tabella numerica
# che il modello può usare.
#
# I 4 passi fondamentali:
#
# 1) GESTIRE I VALORI MANCANTI (NaN)
#    Opzioni: riempire con la media/mediana, eliminare la riga, o usare
#    un valore di default. La scelta dipende dal contesto.
#    In Pandas: df.isnull().sum() per contare, df.fillna(valore) per riempire.
#
# 2) SCALARE LE FEATURE NUMERICHE
#    Se "metri_quadri" va da 30 a 200 e "anno_costruzione" da 1950 a 2024,
#    il modello potrebbe dare più peso ai valori grandi per via della scala.
#    Soluzione: portare tutto su una scala comune (es. 0-1 o media=0, std=1).
#    In Scikit-Learn: MinMaxScaler (0-1) o StandardScaler (media=0, std=1).
#
# 3) CODIFICARE LE FEATURE CATEGORICHE
#    "citta" = "Milano" → come lo trasformi in numero?
#    One-hot encoding: crei una colonna per ogni valore unico.
#    citta_Milano = 1, citta_Roma = 0, citta_Napoli = 0 (per una riga di Milano).
#    In Pandas: pd.get_dummies(df, columns=["citta"]).
#
# 4) CREARE NUOVE FEATURE (Feature Engineering)
#    A volte le feature grezze non bastano. Puoi crearne di nuove:
#    - prezzo_al_mq = prezzo / metri_quadri
#    - eta_casa = 2026 - anno_costruzione
#    - is_centro = distanza_centro_km < 3
#    Nel tuo prodotto: delta_netto_lordo, ratio_trattenute, match_cf_cross_doc.
#
# Attenzione: il preprocessing si "impara" sul training set e si "applica"
# al test set. Non calcolare media/std sul dataset intero prima dello split!
# Sarebbe un leakage sottile ma reale.
#
# Confronto web:
# È come validare un form: prima pulisci l'input (trim, sanitize),
# poi lo trasformi nel formato che il backend si aspetta (tipo, range).

print("\nPARTE 2 — Preprocessing")

# Esempio pratico: preprocessing su case.csv
print("\nValori mancanti per colonna:")
print(case.isnull().sum())

# Feature engineering: creiamo nuove colonne utili
case["eta_casa"] = 2026 - case["anno_costruzione"]
case["prezzo_al_mq"] = (case["prezzo_euro"] / case["metri_quadri"]).round(2)

print(f"\nNuove colonne create: eta_casa, prezzo_al_mq")
print(case[["citta", "eta_casa", "prezzo_al_mq"]].head())

# One-hot encoding: trasformiamo "citta" in colonne numeriche
case_encoded = pd.get_dummies(case, columns=["citta"], dtype=int)
print(f"\nDopo one-hot encoding: {case_encoded.shape[1]} colonne (prima: {case.shape[1]})")
print("Nuove colonne:", [c for c in case_encoded.columns if c.startswith("citta_")])

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Crea una feature "is_grande" che vale True se metri_quadri >= 100
# 2) Conta quante case grandi ci sono con value_counts()
# 3) Spiega in 1 riga: perché NON puoi mettere "prezzo_euro" come feature
#    se il target è "prezzo_euro"? (leakage!)
# perchè addestrimo il modello sulla base di un info che nell'utilizzo reale non avrebbe, in quanto lo stiamo addestrando proprio
# a prevedere il prezzo in un contesto dove non lo abbiamo e stiamo cercando di ricavarlo
print('\nMini-esercizio 2\n')
case['is_grande'] = case['metri_quadri'] >= 100
conta_case_grandi = (case['is_grande'].value_counts(normalize=True))*100
print(f"{case[['metri_quadri', 'is_grande']].head(10)}\n")
print(conta_case_grandi)

# ==========================================================================
# PARTE 3: Train/Test Split — Separare Studio da Esame
# ==========================================================================
#
# Il principio è semplice ma fondamentale: il modello studia su una parte
# dei dati (training set) e viene giudicato su dati che non ha MAI visto
# (test set).
#
# Se valuti sugli stessi dati con cui hai allenato, il modello può aver
# "memorizzato" le risposte — e il tuo score è un'illusione.
# Questo è proprio l'anti-pattern di valutazione di cui abbiamo parlato.
#
# In pratica, con Scikit-Learn:
#
#   from sklearn.model_selection import train_test_split
#   X_train, X_test, y_train, y_test = train_test_split(
#       X, y, test_size=0.2, random_state=42
#   )
#
# - test_size=0.2 → 20% dei dati va nel test, 80% nel training
# - random_state=42 → fissiamo il "seme" casuale per risultati riproducibili
#
# ⚠️ Nel tuo prodotto documentale: lo split va fatto per PRATICA, non per
# singolo documento. Se la pratica P001 ha 5 documenti e ne metti 3 nel
# train e 2 nel test, il modello "vede" parzialmente la pratica → leakage.
# Tutti i documenti della stessa pratica devono stare insieme (tutti nel
# train O tutti nel test).
#
# Un errore subdolo: il train/test split va fatto PRIMA del preprocessing
# che calcola statistiche (media, std per lo scaling). Calcolare la media
# sull'intero dataset e poi splitare significa che il test set ha
# "influenzato" la trasformazione → mini-leakage.
#
# L'ordine corretto:
# 1) Split grezzo (train / test)
# 2) Calcolare media/std SOLO sul train
# 3) Applicare la stessa trasformazione al test
#
# Scikit-Learn lo gestisce con le Pipeline, che vedremo più avanti.
# Per ora, l'importante è capire il PERCHÉ.

from sklearn.model_selection import train_test_split

# 1) Definiamo X e y
# - X (feature): tutte le colonne che useremo come input del modello.
# - y (target): la colonna che vogliamo prevedere.
#
# Regola anti-leakage (fondamentale):
# - Non mettere MAI in X il target (qui: "prezzo_euro"), altrimenti il modello
#   sembra bravissimo ma sta solo copiando la risposta.
# - Escludiamo anche eventuali colonne "fascia_*" / "fascia_prezzo" perché sono
#   derivate dal prezzo: sarebbero leakage indiretto.
#
# Nota: errors="ignore" evita crash se una colonna non esiste (capita spesso
# quando stai sperimentando e cambi il dataset / le feature).
cols_to_drop = (
    ["id", "prezzo_euro", "fascia_prezzo"]
    + [c for c in case_encoded.columns if "fascia" in c]
)
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded["prezzo_euro"]

# 2) Split train/test
# - test_size=0.2: 20% dei dati va nel test (esame finale), 80% nel training (studio).
# - random_state=42: fissa la casualità per ottenere SEMPRE lo stesso split,
#   così se cambi max_depth/feature sai che le metriche cambiano per le tue scelte,
#   non perché è cambiato il campione.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3) Stampiamo un riassunto utile per debug
# - Quante righe e quante feature stiamo usando
# - Quante righe finiscono in training e quante in test (con percentuali)
print("\nPARTE 3 — Train/Test Split")
print(f"Dataset totale: {X.shape[0]} righe, {X.shape[1]} feature")
print(f"Training set:   {X_train.shape[0]} righe ({X_train.shape[0]/X.shape[0]*100:.0f}%)")
print(f"Test set:        {X_test.shape[0]} righe ({X_test.shape[0]/X.shape[0]*100:.0f}%)")
print(f"y_train shape:  {y_train.shape}  (target per il training)")
print(f"y_test shape:   {y_test.shape}   (target per il test)")

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Cambia test_size a 0.3 (30% test). Stampa le nuove dimensioni.
# 2) Prova con random_state=0 invece di 42. Il numero di righe cambia?
#    Le RIGHE specifiche cambiano? (suggerimento: stampa y_test.head())
# 3) Scrivi in 1 riga: perché nel prodotto documentale lo split va fatto
#    per PRATICA e non per singolo documento.
# Lo split va fatto per pratiche e non per singoli documenti, perchè una pratica di finanziamento richiede una serie di documenti interconnessi tra loro (es. buste paga e conti correnti dove avvengono gli accrediti delle suddette buste paga). se si splittasse in maniere non omogenea rispetto le pratiche, sarebbe impossibile effettuare controlli incrociati coerenti tra i diversi documenti che costituiscono le pratiche
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(
    X, y, test_size=0.3, random_state=0
)
print("\nMini-esercizio 3\n")
print(f"Training set => {X_train_2.shape[0]} righe, {X_train_2.shape[1]} colonne ({((X_train_2.shape[0] / X.shape[0])*100):.2f} % del dataset totale)")
print(f"Testing set => {X_test_2.shape[0]} righe, {X_test_2.shape[1]} colonne ({((X_test_2.shape[0] / X.shape[0])*100):.2f} % del dataset totale)\n")
print(y_test.head())
print(y_test_2.head())
print(y_test.index[:5])
print(y_test_2.index[:5])

print(f"Confronto tra le prime righe dei dataset:\n{X_train.iloc[0:3, 0:3]}\n{X_train_2.iloc[0:3, 0:3]}")

# ==========================================================================
# PARTE 4: Il Primo Modello — Decision Tree (Albero Decisionale)
# ==========================================================================
#
# Partiamo dal modello più intuitivo: l'albero decisionale.
# Funziona esattamente come una serie di domande sì/no:
#
# "I metri quadri sono > 80?"
#   → Sì: "L'anno di costruzione è > 2000?"
#       → Sì: prezzo stimato = 280.000
#       → No: prezzo stimato = 210.000
#   → No: "Ha garage?"
#       → Sì: prezzo stimato = 180.000
#       → No: prezzo stimato = 130.000
#
# Il modello costruisce queste domande automaticamente, scegliendo le
# feature e le soglie che dividono meglio i dati.
#
# È il modello con cui iniziamo perché:
# 1) È facile da capire e visualizzare
# 2) Non richiede scaling delle feature
# 3) Funziona sia per regressione che per classificazione
# 4) È la base del Random Forest (che vedremo dopo)
#
# In Scikit-Learn:
#   from sklearn.tree import DecisionTreeRegressor    (per numeri)
#   from sklearn.tree import DecisionTreeClassifier   (per categorie)
#
# Parametri importanti:
# - max_depth: profondità massima dell'albero (limita la complessità)
#   → troppo basso: underfitting (non impara abbastanza)
#   → troppo alto: overfitting (memorizza i dati)
# - random_state: per risultati riproducibili
#
# Confronto web:
# Un Decision Tree è come una catena di if/else generata automaticamente
# dai dati. Se scrivessi tu quelle regole a mano, avresti bisogno di ore
# e non copriresti tutti i casi.

from sklearn.tree import DecisionTreeRegressor

print("\nPARTE 4 — Il Primo Modello (Decision Tree)")

modello = DecisionTreeRegressor(max_depth=4, random_state=42)

# Il metodo .fit() è il cuore del training: il modello "studia" i dati
modello.fit(X_train, y_train)

# Il metodo .predict() usa ciò che ha imparato per fare previsioni
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

print(f"Previsioni sul training set (prime 5): {y_pred_train[:5].round(0)}")
print(f"Valori reali corrispondenti:           {y_train.values[:5]}")

# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Cambia max_depth a 2. Il modello fa previsioni diverse? Stampa le
#    prime 5 previsioni e confronta con quelle di max_depth=4.
# 2) Cambia max_depth a 20. Le previsioni sul TRAINING cambiano?
#    (Suggerimento: con albero molto profondo, memorizza i dati)
# 3) Scrivi in 1 riga: cos'è l'overfitting, usando l'analogia
#    dell'albero troppo profondo.
# l'overfitting è quando il modello ad albero raggiunge una profondità eccessiva, e non si limita più a trovare la regola generale, ma impara a memoria i risultati.
from sklearn.tree import DecisionTreeRegressor
print("\nMini-esercizio 4\n")

case_encoded = pd.get_dummies(case, columns=["citta"], dtype=int)

cols_to_drop = (['id', 'prezzo_euro'] + [c for c in case_encoded.columns if "fascia" in c ])
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded['prezzo_euro']

X_train, X_test, y_train, y_test = train_test_split(
    X, y , test_size=0.2, random_state=42
)

modello = DecisionTreeRegressor(max_depth=2, random_state=42)
modello.fit(X_train, y_train)
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

print("\nProfondita 2\n")

print(f"Predizione Train: {y_pred_train[:5].round(0)}")
print(f"Valori reali Train: {y_train[:5].values.round(0)}\n\n")

print(f"Predizione Test: {y_pred_test[:5].round(0)}")
print(f"Valori reali Test: {y_test[:5].values.round(0)}\n\n")

modello = DecisionTreeRegressor(max_depth=20, random_state=42)
modello.fit(X_train, y_train)
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

print("\nProfondita 20\n")

print(f"Predizione Train: {y_pred_train[:5].round(0)}")
print(f"Valori reali Train: {y_train[:5].values.round(0)}\n\n")

print(f"Predizione Test: {y_pred_test[:5].round(0)}")
print(f"Valori reali Test: {y_test[:5].values.round(0)}\n\n")



modello = DecisionTreeRegressor(max_depth=4, random_state=42)
modello.fit(X_train, y_train)
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

print("\nProfondita 4\n")

print(f"Predizione Train: {y_pred_train[:5].round(0)}")
print(f"Valori reali Train: {y_train[:5].values.round(0)}\n\n")

print(f"Predizione Test: {y_pred_test[:5].round(0)}")
print(f"Valori reali Test: {y_test[:5].values.round(0)}\n\n")



# ==========================================================================
# PARTE 5: Metriche di Valutazione — Misurare se Funziona
# ==========================================================================
#
# Hai il modello, hai le previsioni. Ma come sai se sono buone?
# Servono METRICHE: numeri che misurano quanto il modello sbaglia.
#
# Per la REGRESSIONE (previsione di numeri, come il prezzo):
#
# 1) MAE (Mean Absolute Error) — Errore medio in valore assoluto
#    "In media, il modello sbaglia di X euro"
#    Facile da capire, espresso nella stessa unità del target.
#    Formula: media di |vero - previsto|
#
# 2) RMSE (Root Mean Squared Error) — Radice dell'errore quadratico medio
#    Come il MAE ma penalizza di più gli errori grandi.
#    Formula: radice quadrata della media di (vero - previsto)²
#
# 3) R² (R-squared) — Quanto il modello spiega la variabilità dei dati
#    Valore tra 0 e 1 (può essere negativo se il modello è pessimo).
#    R² = 1.0 → modello perfetto
#    R² = 0.0 → il modello prevede come se facesse la media di tutto
#    R² < 0.0 → il modello è peggio della media (qualcosa è molto sbagliato)
#
# La regola d'oro: confronta SEMPRE le metriche sul training vs sul test.
# Se il training ha R²=0.99 e il test ha R²=0.45 → overfitting chiaro.
#
# Per la CLASSIFICAZIONE (previsione di categorie, come genuino/alterato):
# precision, recall, F1, accuracy — le vedremo in dettaglio quando
# costruiremo il classificatore vero nel cap.03.
# Per ora ricorda: nel tuo prodotto il recall è prioritario (meglio
# segnalare un documento genuino come sospetto che lasciar passare
# un documento alterato).

from sklearn.metrics import mean_absolute_error, r2_score

print("\nPARTE 5 — Metriche di Valutazione")

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print(f"MAE  training: {mae_train:,.0f} €")
print(f"MAE  test:     {mae_test:,.0f} €")
print(f"R²   training: {r2_train:.3f}")
print(f"R²   test:     {r2_test:.3f}")

if r2_train - r2_test > 0.2:
    print("⚠️ Possibile overfitting: R² training molto più alto del test!")

# --- MINI-ESERCIZIO 5 — Prova subito! ---
# 1) Allena un Decision Tree con max_depth=2 e uno con max_depth=20.
# 2) Calcola MAE e R² per entrambi, sia su train che su test.
# 3) Quale dei due ha overfitting? Come lo riconosci?
# lo si riconosce guardando quale dei 2 ha una forbice maggiore tra r2 del train e r2 del test.
# 4) Scrivi in 2 righe: qual è il valore ideale di max_depth e come
#    lo troveresti nella pratica?
# Non esiste un valore ideale in assoluto, dipende da tanti fattori (come feature e tipo di dataset).Lo si può trovare in ogni situazione a seguito di diverse prove e dopo aver valutato diversi valori. 
print("\nMini-esercizio 5\n")

print("\nProfondità 2")
modello = DecisionTreeRegressor(max_depth=2, random_state=42)
modello.fit(X_train, y_train)

y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print(f"MAE Train => {mae_train:.2f}")
print(f"MAE Test  => {mae_test:.2f}")
print(f"R²  Train => {r2_train:.2f}")
print(f"R²  Test  => {r2_test:.2f}")
if (r2_train - r2_test) > 0.1:
    print(f"!!! Possibile Overfitting !!!")

print("\nProfondità 20")
modello = DecisionTreeRegressor(max_depth=20, random_state=42)
modello.fit(X_train, y_train)

y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

print(f"MAE Train => {mae_train:.2f}")
print(f"MAE Test  => {mae_test:.2f}")
print(f"R²  Train => {r2_train:.2f}")
print(f"R²  Test  => {r2_test:.2f}")
if (r2_train - r2_test) > 0.1:
    print(f"!!! Possibile Overfitting !!!")


# ==========================================================================
# PARTE 6: Baseline — Il Punto di Partenza
# ==========================================================================
#
# Prima di entusiasmarti per il modello, chiediti: è meglio di una
# previsione stupida? La baseline è il "modello idiota" di confronto.
#
# Per la regressione, la baseline più comune è: prevedere SEMPRE la media.
# "Quanto costa questa casa?" → "Boh, la media di tutte: 250.000 €"
#
# Se il tuo Decision Tree non batte questa baseline, il modello non serve.
#
# Per la classificazione, la baseline è: prevedere SEMPRE la classe
# più frequente. "Questo documento è genuino?" → "Sì, perché il 95%
# lo sono". Se il modello non batte il 95%, non sta imparando nulla.

print("\nPARTE 6 — Baseline")

y_baseline = np.full_like(y_test, y_train.mean())
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)

print(f"Baseline (media): MAE = {mae_baseline:,.0f} €, R² = {r2_baseline:.3f}")
print(f"Decision Tree:    MAE = {mae_test:,.0f} €, R² = {r2_test:.3f}")

if mae_test < mae_baseline:
    print("✅ Il modello batte la baseline!")
else:
    print("❌ Il modello NON batte la baseline — qualcosa non va.")

# Primo assert — testing AI come skill trasversale (regola 37)
assert mae_test < mae_baseline, "Il modello deve battere la baseline"

# --- MINI-ESERCIZIO 6 — Prova subito! ---
# 1) Per il tuo prodotto documentale (classificazione genuino/alterato):
#    se il 90% dei documenti è genuino, qual è l'accuracy della baseline? 90% classificandoli come tutti genuini.
# 2) Se il modello ha accuracy 91%, è buono? Spiega in 2 righe
#    perché l'accuracy da sola non basta (suggerimento: recall).
# E' sicuramente meglio rispetto la baseline, ma potenzialmente su 10 documenti alternati potrebbero sfuggirne addirittura 9. Non basta che il modello abbia un accuracy elevata (90% sembra molto), ma in realtà nel caso di documenti alterati vogliamo che il recall (ossia in numero di alterati trovati rispetto al totale degli alterati) sia il più alto possibile, perchè siamo molto più interessati a trovare tutti gli alterati piuttosto che a classificare come non alterati i genuini.


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Il preprocessing (scaling, encoding) si calcola sull'intero dataset
# prima dello split." Rispondi e spiega perché. Falso. Acnhe se il formato dei dati deve essere uguale (encoding), per fare scaling, come ad esempio la deviazione standard e le media, devono essere calcolate solo sul training, altrimenti si rischierebbe di fare leakage 
#
# DOMANDA 2 — Completa:
# train_test_split(X, y, test_size=___, random_state=___)
# Per avere 80% train e 20% test, con risultati riproducibili.
# train_test_split(X, y, test_size=0.2, random_state=42)
#
# DOMANDA 3 — Trova l'errore:
#   modello.fit(X_test, y_test)
#   y_pred = modello.predict(X_test)
#   print("MAE:", mean_absolute_error(y_test, y_pred))
# Dove sta l'anti-pattern? Spiega.
# si sta facendo fitting sul testing, invece che sul training. In pratica si allena il modello sugli stessi dati su cui poi verrà esaminato.

# DOMANDA 4 — Prevedi:
# Se un Decision Tree ha R²=0.95 sul training e R²=0.40 sul test,
# cosa sta succedendo? Come lo risolvi?
# Evidentemente un caso di overfitting, si dovrebbe procedere a ridurre la max_depth.

# DOMANDA 5 — 💬 Spiega con parole tue:
# Cos'è una baseline e perché è il primo passo OBBLIGATORIO prima di
# costruire modelli complessi?
# In pratica una baseline costituisce il valore di riferimento di una metrica per capire quanto il mio modello è migliore rispetto alla suddivisione più basica possibile. Nel caso di valori numerici, ad esempio, si valuta quanto le mie previsioni sono accurate rispetto alla semplice media di tutti i valori del training. Ovviamente un modello è efficace solo se riesce a battere la metrica valutata sulla baseline.
#
# DOMANDA 6 — Definizione:
# Differenza tra MAE e R². Quale è più facile da spiegare a un collega
# non tecnico e perché?
# il MAE, acronimo di mean absolute error, e semplicemente il calcolo dello scostamento medio rispetto ai valori di y (ossia i valori reali del  target). R² invece è un indicatore che va da 1 a 0 (o addirittua anche valori negativi) che ci aiuta a capire quanto è effettivamente preciso il nostro modello. 1 significa che il modello è perfetto, 0 che il modello risponde come se facesse semplicemente la media, valore negativo qualora il nostro modello stesse addirittura facendo peggio rispetto alla semplice media. Il più semplice da spiegare è il MAE, perchè il calcolo è di facile comprensione poichè è costituito dalla semplice media dello scostamento rispetto ai valori reali. Il secondo invece è un indice il cui calcolo è più complesso.
#


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================
#
# ESERCIZIO 1 (Facile):
# Carica `case.csv`, crea le feature (inclusa eta_casa e prezzo_al_mq),
# esegui one-hot encoding su "citta", fai il train/test split (80/20),
# e stampa le dimensioni di X_train, X_test, y_train, y_test.
# Attenzione: escludi "id" e "prezzo_euro" da X!


print("\nEsercizio 1\n")
#carico il file csv
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)

#creo le features richieste
case['eta_casa'] = 2026 - case['anno_costruzione']
case['prezzo_al_mq'] = case['prezzo_euro'] / case['metri_quadri']
# case['stanze_per_mq'] = case['metri_quadri'] / case['num_stanze']

#faccio one-hot encoding per case['citta']
case_encoded = pd.get_dummies(case, columns=['citta'], dtype=int)

#preparo il dataset per il train e per il test
cols_to_drop = (
    ['prezzo_euro', 'id'] + [c for c in case_encoded.columns if ("prezzo" in c) or ("fascia" in c)]
    )
X = case_encoded.drop(columns=cols_to_drop, errors="ignore")
y = case_encoded['prezzo_euro']

# faccio lo split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

print(f"Size di X_train =>{X_train.shape}")
print(f"Size di X_test  =>{X_test.shape}")
print(f"Size di y_train =>{y_train.shape}")
print(f"Size di y_test  =>{y_test.shape}")



# ESERCIZIO 2 (Medio):
# Allena un DecisionTreeRegressor con max_depth=3 sui dati del training.
# Calcola MAE e R² sia sul training che sul test.
# Calcola anche la baseline (media).
# Stampa un confronto formattato e scrivi un assert che verifica
# che il modello batte la baseline.

#imposto gli iper-parametri e alleno il modello
print("\nEsercizio 2\n")
modello = DecisionTreeRegressor(max_depth=3, random_state=42)
modello.fit(X_train, y_train)

# testo il modello sul dataset del train e poi sul test (per avere i riferimenti su cui fare analisi tramite le metriche)
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

# imposto le metriche di riferimento basate sulla baseline
y_baseline = np.full_like(y_test, y_train.mean())
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)

# creo le metriche su cui fare le valutazioni
mae_train = mean_absolute_error(y_train, y_pred_train)
mae_test = mean_absolute_error(y_test, y_pred_test)
r2_train = r2_score(y_train, y_pred_train)
r2_test = r2_score(y_test, y_pred_test)

# effettuo un confronto
print(f"Previsioni Train   =>{y_pred_train[:5].astype(int)}")
print(f"Valori Reali Train =>{y_train[:5].values.round(0)}")
print(f"MAE Train =>{mae_train:.2f}")
print(f"R² Train  =>{r2_train:.3f}\n")

print(f"Previsioni Test   =>{y_pred_test[:5].astype(int)}")
print(f"Valori Reali Test =>{y_test[:5].values.round(0)}")
print(f"MAE Test =>{mae_test:.2f}")
print(f"R² Test  =>{r2_test:.3f}\n")

print(f"Previsioni Baseline =>{y_baseline[:5]}")
print(f"Valori Reali Test   =>{y_test[:5].values.round(0)}")
print(f"MAE Baseline => {mae_baseline:.2f}")
print(f"R² Baseline  => {r2_baseline:.3f}")

assert mae_test < mae_baseline

# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Spiega in 8-10 righe:
# - Cos'è l'overfitting e come lo riconosci dalle metriche
# - 2 strategie concrete per ridurlo (nel contesto di un Decision Tree)
# - Come si collega al concetto di bias-variance tradeoff
#   (anche se non conosci la formula, spiega l'intuizione)
# over-fitting è quando il modello, divenuto troppo profondo e complesso, arriva non più a generalizzare ma a imparare a memoria le risposte, adattandosi anche al così detto "rumore" presente nei dati. Darà dunque previsioni perfette con i dati del train, ma sbaglierà nella fase di test (e si riscontrerà un' ampia differenza tra la metrica R² sui dati train e sui dati test). Lo si può trovare andando a regolare gli iperparametri (ad esempio min_samples_split, max_leaf_nodes o il più utilizzato max_depth), oppure lavorando sulla qualità delle freature, fino ad avere delle risposte dalle metriche che soddisfano in nostro benchmark. il punto è trovare il giusto bias-variance_tradeoff, ossia l'equilibrio tra underfitting e overfitting, il giusto compromesso tra generalizzazione e memoria.

# ESERCIZIO 4 (🔧 [REFACTORING]):
# Riscrivi questo codice "brutto" in modo pulito e professionale:
#
# import pandas as pd
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.metrics import mean_absolute_error
# d = pd.read_csv("case.csv")
# a = d[['metri_quadri','anno_costruzione']]
# b = d['prezzo_euro']
# from sklearn.model_selection import train_test_split
# c,e,f,g = train_test_split(a,b,test_size=0.2)
# m = DecisionTreeRegressor()
# m.fit(c,f)
# p = m.predict(e)
# print(mean_absolute_error(g,p))
#
# Problemi da risolvere: nomi variabili, import disordinati, nessun
# random_state, nessuna baseline, nessun confronto train/test.

print("\nEsercizio 4")
import pandas as pd
import numpy as np
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

path_case_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_case_file)
X = case[['metri_quadri','anno_costruzione']]
y = case['prezzo_euro']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modello = DecisionTreeRegressor(random_state=42, max_depth=5)

modello.fit(X_train, y_train)

y_pred_test = modello.predict(X_test)
y_pred_train = modello.predict(X_train)

y_baseline = np.full_like(y_test, y_train.mean())
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)

mae_test = mean_absolute_error(y_test, y_pred_test)
r2_test = r2_score(y_test, y_pred_test)

mae_train = mean_absolute_error(y_train, y_pred_train)
r2_train = r2_score(y_train, y_pred_train)

print("\nBaseline")
print(f"MAE Baseline =>{mae_baseline:.2f}")
print(f"R² Baseline  =>{r2_baseline:.3f}")

print(f"\nTrain")
print(f"MAE Train =>{mae_train:.2f} €")
print(f"R² Train  =>{r2_train:.3f}")

print(f"\nTest")
print(f"MAE Test =>{mae_test:.2f} €")
print(f"R² Test  =>{r2_test:.3f}")

# ESERCIZIO 5 (🔍 [DEBUG]):
# Questo codice produce un errore. Trova il bug e spiega l'errore:
#
# X = case[["metri_quadri", "anno_costruzione", "citta"]]
# y = case["prezzo_euro"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# modello = DecisionTreeRegressor(max_depth=4)
# modello.fit(X_train, y_train)
#
# Suggerimento: il Decision Tree di Scikit-Learn accetta feature categoriche?
#

# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + ML):
# Partendo da case.csv:
# 1) Crea un report con groupby/agg per "citta":
#    - pratiche_totali, prezzo_medio, prezzo_al_mq_medio
# 2) Identifica la città con il prezzo_al_mq più alto
# 3) Filtra il dataset solo per quella città
# 4) Allena un DecisionTreeRegressor solo su quei dati (split 80/20)
# 5) Stampa MAE e R² e confronta con la baseline
# 6) Scrivi in 2 righe: allenarti su una sola città è una buona idea?
#    Perché sì o perché no?
#

# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrittura da memoria):
# Senza guardare il codice sopra, riscrivi da zero il ciclo completo:
# 1) Carica case.csv
# 2) Crea almeno 2 feature engineered
# 3) Esegui one-hot encoding
# 4) Fai train/test split
# 5) Allena un Decision Tree
# 6) Calcola baseline
# 7) Calcola e confronta metriche (MAE, R²) training vs test vs baseline
# 8) Scrivi un assert
#

# ESERCIZIO 8 (🔀 [INTERLEAVING] — Confronto modelli):
# Allena 3 Decision Tree con max_depth diversi: 2, 5, 10.
# Per ciascuno calcola MAE e R² su train e test.
# Crea un DataFrame di confronto con colonne:
#   max_depth | mae_train | mae_test | r2_train | r2_test | gap_r2
# dove gap_r2 = r2_train - r2_test (indicatore di overfitting).
# Stampa il DataFrame ordinato per gap_r2 crescente.
# Quale max_depth sceglieresti e perché?
#

# ESERCIZIO 9 (Teoria applicata):
# In massimo 10 righe:
# - Descrivi il ciclo ML applicato al tuo prodotto documentale
# - Per ogni fase cita un esempio concreto dal dominio documenti
# - Spiega quale fase è la più critica per il tuo caso e perché
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Modulo 2, Cap.02
# ==========================================================================
#
# Componente pipeline: Cuore predittivo (primo classificatore)
# Deliverable: script che allena un modello sui dati case.csv e produce
#              previsioni di prezzo con metriche verificabili.
#
# TASK:
# 1) Crea un file `modello_base.py` nella cartella modulo_02_ml/
# 2) Il file deve contenere un ciclo ML completo e autonomo:
#    - Carica case.csv
#    - Preprocessing (feature engineering + one-hot encoding)
#    - Train/test split (80/20, random_state=42)
#    - Allena un DecisionTreeRegressor
#    - Calcola baseline
#    - Stampa metriche comparate (MAE, R² per training/test/baseline)
#    - Assert: il modello batte la baseline
# 3) Il file deve essere eseguibile con `python modello_base.py`
#
# Definition of Done:
# - Lo script gira senza errori
# - L'assert passa
# - Le metriche sono stampate in modo leggibile
# - Il codice usa nomi espliciti e terminologia coerente
#
# Impatto roadmap: R0 — primo modello predittivo funzionante
#
# ⚠️ Nota: questo task recupera anche il progetto incrementale non svolto
# nel cap.01. Nel cap.01 avevi completato gli esercizi ma non il task
# prodotto — lo facciamo qui come primo passo concreto.
#


# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) Vero: X = DataFrame (2D), y = Series (1D)
# 2) (50, 2)
# 3) y deve essere una Series (singola parentesi), non un DataFrame
#    (doppia parentesi)
# 4) .loc ; .iloc
# 5) Data leakage = quando il target finisce nelle feature.
#    Esempio: mettere "esito_verifica" come feature per prevedere
#    genuino/alterato — è il target stesso mascherato.
# 6) Valutare sul training è come fare l'esame con le risposte davanti:
#    il modello ha "memorizzato" quei dati, non ha imparato a generalizzare.
#    Sul test set, i dati sono nuovi → il risultato riflette la capacità
#    reale del modello.
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Falso: il preprocessing si calcola SOLO sul training set e si applica
#    al test set. Calcolare su tutto il dataset è un leakage sottile.
# 2) test_size=0.2, random_state=42
# 3) Il modello è allenato sul TEST set e valutato sullo STESSO test set.
#    Doppio errore: (a) non ha training separato, (b) valuta su dati visti.
# 4) Overfitting: il modello ha memorizzato i dati di training.
#    Soluzione: ridurre max_depth o usare più dati.
# 5) La baseline è il modello più semplice possibile (es. prevedere la
#    media). Se il tuo modello non batte la baseline, non sta imparando
#    nulla di utile — è uno spreco di complessità.
# 6) MAE = errore medio in euro (o unità del target), R² = proporzione
#    di variabilità spiegata (0-1). MAE è più facile da spiegare perché
#    è nella stessa unità: "il modello sbaglia in media di 15.000 €".

