"""
============================================================================
 MODULO 1 — ESERCIZIO 09: Introduzione a Pandas
 DataFrame — Il Tuo Database SQL, Ma in RAM
============================================================================

 TEORIA: Pandas = SQL + Excel + JavaScript Objects, Tutto in Uno

 Ricordi l'esercizio 06 dove abbiamo letto un CSV "a mano" e abbiamo
 scritto 15-20 righe di codice per fare una semplice analisi?
 Con Pandas, quelle stesse operazioni richiedono 1-2 righe.

 Cos'è un DataFrame?
 Un DataFrame è una TABELLA in memoria RAM. Ha righe e colonne,
 come una tabella SQL o un foglio Excel.

 ANALOGIA CON SQL (che conosci da Laravel):
 ┌────────────────────────────────────────────┐
 │  SQL                → Pandas               │
 │  ──────────────────────────────────────── │
 │  SELECT *           → df                   │
 │  SELECT col1, col2  → df[["col1","col2"]]  │
 │  WHERE condizione   → df[df["col"] > 5]    │
 │  ORDER BY col       → df.sort_values("col")│
 │  GROUP BY + COUNT   → df.groupby().count() │
 │  LIMIT 5            → df.head(5)           │
 │  COUNT(*)           → len(df)              │
 │  AVG(col)           → df["col"].mean()     │
 │  JOIN               → pd.merge(df1, df2)   │
 └────────────────────────────────────────────┘

 ANALOGIA CON LARAVEL ELOQUENT (che conosci bene!):
 ┌──────────────────────────────────────────────────┐
 │  Eloquent                → Pandas                │
 │  ────────────────────────────────────────────── │
 │  Order::all()            → df                    │
 │  Order::find(1)          → df.loc[0]             │
 │  Order::where(...)       → df[df["col"]==valore] │
 │  ->orderBy('prezzo')     → df.sort_values(...)   │
 │  ->groupBy('citta')      → df.groupby('citta')   │
 │  ->pluck('nome')         → df["nome"]            │
 │  ->count()               → len(df)               │
 │  ->avg('prezzo')         → df["prezzo"].mean()   │
 │  ->toArray()             → df.to_dict()          │
 │  ->first()               → df.iloc[0]            │
 │  ->get()                 → df (è già caricato!)  │
 └──────────────────────────────────────────────────┘

 SPIEGAZIONE DEI METODI ELOQUENT (ripasso):
   Order::all()       → prende TUTTE le righe dalla tabella "orders"
   Order::find(1)     → trova la riga con id=1
   ->where('col','=',val)  → filtra le righe dove 'col' è uguale a val
   ->orderBy('col')   → ordina per la colonna specificata
   ->groupBy('col')   → raggruppa le righe per valore della colonna
   ->pluck('nome')    → estrae solo i valori di una colonna (come un array)
   ->count()          → conta il numero di righe
   ->avg('col')       → calcola la media di una colonna numerica
   ->first()          → prende solo la prima riga del risultato
   ->toArray()        → converte il risultato in un array PHP

 In Pandas fai le stesse operazioni, ma tutto avviene in RAM (memoria)
 invece che con query al database. I dati sono già "qui", non devi
 aspettare una risposta dal server MySQL.

============================================================================
"""

import pandas as pd  # 'pd' è la convenzione universale
import numpy as np
import os

# ==========================================================================
# QUIZ D'INGRESSO — Ripasso dal Capitolo 08 (Tensori)
# ==========================================================================
#
# DOMANDA 1 — Prevedi l'output:
#   x = np.zeros((12, 16, 16, 3))
#   print(x.shape[0], x.ndim)
# 12 4
#
# DOMANDA 2 — Vero o Falso?
# "mean(axis=3) su un batch immagini (n,h,w,c) produce shape (n,h,w)." V
#
# DOMANDA 3 — Trova l'errore:
#   img = np.random.randint(0, 256, (8, 8, 3))
#   flat = img.reshape(64,)
# Cosa non torna e perche?
# Il problema principale e il reshape: 8*8*3 = 192 elementi, non 64.
#
# DOMANDA 4 — Definizione:
# Spiega in una riga la differenza tra "traslare" e "ruotare" i dati.
#traslare come termine si usa per dire "spostare", ad esempio in avanti o indietro, ruotare invece indica un movimento circolare come un loop
#
# DOMANDA 5 — Completa il codice:
#   arr = np.arange(24).reshape(6, 4)
#   v = arr.reshape(-1)
# Per ottenere un vettore 1D senza calcolare a mano la lunghezza.
#
# DOMANDA 6 — Prevedi l'output:
#   a = np.array([[1, 2, 3], [4, 5, 6]])
#   b = np.array([10, 20, 30])
#   print((a + b).shape)
#(2, 3)
# DOMANDA 7 — 💬 Spiega con parole tue:
# Perche conviene usare shape attese ad ogni passaggio quando fai preprocessing?
# per avere la certezza di processare la giusta dimensione, utilizzare shape ci aiuta a campire meglio le dimensioni del tensore

# ==========================================================================
# PARTE 1: Creare un DataFrame
# ==========================================================================

# Modo 1: Da un dizionario (come creare un oggetto JSON con array nei valori)
dati = {
    "nome": ["Marco", "Laura", "Giulia", "Luca", "Anna"],
    "eta": [28, 34, 22, 45, 31],
    "citta": ["Milano", "Roma", "Napoli", "Milano", "Firenze"],
    "stipendio": [35000, 42000, 28000, 55000, 38000]
}

df = pd.DataFrame(dati)
print("=== DataFrame creato da dizionario ===")
print(df)
print(f"\nTipo: {type(df)}")
print(f"Shape: {df.shape}")  # (5, 4) → 5 righe, 4 colonne
print(f"Colonne: {list(df.columns)}")

# Modo 2: Da un file CSV (il modo più comune)
percorso_csv = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(percorso_csv)

print("\n=== DataFrame da CSV ===")
print(vendite)

# ==========================================================================
# PARTE 2: Esplorare i Dati (I Primi Comandi da Memorizzare)
# ==========================================================================

print("\n" + "=" * 60)
print("  ESPLORARE IL DATASET")
print("=" * 60)

# .head(n) = LIMIT n → mostra le prime n righe (default 5)
print("\n--- head(3) = SELECT * LIMIT 3 ---")
print(vendite.head(3))

# .tail(n) → le ultime n righe
print("\n--- tail(3) = ultime 3 righe ---")
print(vendite.tail(3))

# .info() → struttura del DataFrame (colonne, tipi, valori nulli)
# Come DESCRIBE tabella in SQL
print("\n--- info() = DESCRIBE tabella ---")
print(vendite.info())

# .describe() → statistiche numeriche (count, mean, std, min, max...)
# Come SELECT COUNT(*), AVG(*), MIN(*), MAX(*) per ogni colonna numerica
print("\n--- describe() = statistiche ---")
print(vendite.describe())

# .shape → (righe, colonne) come COUNT(*) + num. colonne
print(f"\nRighe: {vendite.shape[0]}, Colonne: {vendite.shape[1]}")

# .dtypes → tipi di ogni colonna
print(f"\nTipi colonne:\n{vendite.dtypes}")

# 🔁 RINFORZO MIRATO — Shape/Axis: ponte NumPy -> Pandas
# Nel cap.08 hai consolidato shape/assi sui tensori. Qui il ponte e diretto:
# - np.array 2D: shape (righe, colonne)
# - pd.DataFrame: stesso concetto, ma con etichette di colonna.
# axis=0 = "verticale" (lavori per colonna), axis=1 = "orizzontale" (lavori per riga).
print("\n--- RINFORZO: asse e shape in Pandas ---")
print(f"Shape vendite: {vendite.shape}")
print(f"Media asse 0 (colonne numeriche):\n{vendite.select_dtypes(include='number').mean(axis=0)}")

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Stampa numero righe e colonne di vendite in due variabili separate.
# 2) Stampa solo i tipi delle colonne numeriche.
# 3) In una riga, spiega: perche axis=0 in Pandas e simile a axis=0 in NumPy?
#perchè entrambi funzionano basandosi su una logica di griglia multidimensionale, che quindi è fatta sostanzialmente di assi
print("\nMini-esercizio 1\n")
file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
data = pd.read_csv(file)
num_colonne = data.shape[1]
num_righe = data.shape[0]
print(f"{num_colonne}")
print(f"{num_righe}")
print(f"\nTipi colonne:\n{data.select_dtypes(include='number').dtypes}")

# ==========================================================================
# PARTE 3: Selezionare Dati (SELECT in SQL)
# ==========================================================================

print("\n" + "=" * 60)
print("  SELEZIONARE DATI")
print("=" * 60)

# Selezionare UNA colonna → restituisce una Series (come un array)
# SQL: SELECT prodotto FROM vendite
print("\n--- Una colonna (Series) ---")
print(vendite["prodotto"])

# Selezionare PIÙ colonne → restituisce un DataFrame
# SQL: SELECT prodotto, prezzo FROM vendite
print("\n--- Più colonne ---")
print(vendite[["prodotto", "prezzo"]])

# Selezionare RIGHE per posizione (come LIMIT + OFFSET)
# SQL: SELECT * FROM vendite LIMIT 3 OFFSET 5
print("\n--- Righe 5-7 (iloc) ---")
print(vendite.iloc[5:8])  # iloc = index location (per posizione numerica)

# Selezionare una CELLA specifica
print(f"\nCella [2, 'prodotto']: {vendite.loc[2, 'prodotto']}")

# 🔁 RINFORZO MIRATO — Lettura consegne (checklist operativa)
# Pattern visto piu volte: si implementa solo una parte dei requisiti.
# Applica questa mini-checklist prima di dire "ho finito":
# - Quanti punti ci sono? (a,b,c,d...)
# - Ho stampato/verificato ogni output richiesto?
# - Ho usato esattamente il metodo richiesto (es. groupby, non ciclo for)?
# - Ho controllato shape/tipi finali?

# ==========================================================================
# PARTE 4: Filtrare i Dati (WHERE in SQL)
# ==========================================================================

print("\n" + "=" * 60)
print("  FILTRARE DATI (WHERE)")
print("=" * 60)

# SQL: SELECT * FROM vendite WHERE citta = 'Milano'
milano = vendite[vendite["citta"] == "Milano"]
print("--- WHERE citta = 'Milano' ---")
print(milano)

# SQL: SELECT * FROM vendite WHERE prezzo > 50
costosi = vendite[vendite["prezzo"] > 50]
print("\n--- WHERE prezzo > 50 ---")
print(costosi)

# SQL: SELECT * FROM vendite WHERE categoria = 'Elettronica' AND citta = 'Milano'
elett_milano = vendite[(vendite["categoria"] == "Elettronica") & (vendite["citta"] == "Milano")]
print("\n--- WHERE categoria='Elettronica' AND citta='Milano' ---")
print(elett_milano)

# SQL: SELECT * FROM vendite WHERE citta IN ('Milano', 'Roma')
due_citta = vendite[vendite["citta"].isin(["Milano", "Roma"])]
print(f"\n--- WHERE citta IN ('Milano','Roma'): {len(due_citta)} righe ---")

# SQL: SELECT * FROM vendite WHERE prodotto LIKE '%Cuffie%'
cuffie = vendite[vendite["prodotto"].str.contains("Cuffie")]
print(f"\n--- WHERE prodotto LIKE '%Cuffie%': {len(cuffie)} righe ---")
print(cuffie)

# 🔁 RINFORZO MIRATO — filter/lambda ordine parametri
# In Python il filter vuole prima la funzione, poi l'iterabile:
# filter(lambda x: condizione, lista)
# (NON: filter(lista, lambda ...))
prezzi_demo = [15, 49, 120, 75, 8]
solo_alti = list(filter(lambda p: p >= 50, prezzi_demo))
print(f"\nRINFORZO filter/lambda -> prezzi >= 50: {solo_alti}")

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Crea una lista con 6 prezzi.
# 2) Usa filter + lambda per tenere solo prezzi > 100.
# 3) Stampa il risultato e la lunghezza.
print("\nMini-esercizio 2\n")
import random
mia_lista = [random.randint(1, 200) for _ in range(6)]
solo_alti = list(filter(lambda x: x > 100, mia_lista))
print(f"Prezzi alti: {solo_alti}\nLunghezza lista: {len(solo_alti)}")
# ==========================================================================
# PARTE 5: Ordinare i Dati (ORDER BY in SQL)
# ==========================================================================

print("\n" + "=" * 60)
print("  ORDINARE DATI (ORDER BY)")
print("=" * 60)

# SQL: SELECT * FROM vendite ORDER BY prezzo DESC
per_prezzo = vendite.sort_values("prezzo", ascending=False)
print("--- ORDER BY prezzo DESC ---")
print(per_prezzo.head(5))

# Ordinare per più colonne:
# SQL: ORDER BY categoria ASC, prezzo DESC
per_cat_prezzo = vendite.sort_values(["categoria", "prezzo"], ascending=[True, False])
print("\n--- ORDER BY categoria ASC, prezzo DESC ---")
print(per_cat_prezzo.head(8))

# ==========================================================================
# PARTE 6: Aggregare i Dati (GROUP BY in SQL)
# ==========================================================================

print("\n" + "=" * 60)
print("  AGGREGARE DATI (GROUP BY)")
print("=" * 60)

# Prima convertiamo i tipi (il CSV legge tutto come stringhe)
vendite["prezzo"] = vendite["prezzo"].astype(float)
vendite["quantita"] = vendite["quantita"].astype(int)

# SQL: SELECT citta, COUNT(*) FROM vendite GROUP BY citta
per_citta = vendite.groupby("citta").size()
print("--- GROUP BY citta, COUNT(*) ---")
print(per_citta)

# SQL: SELECT categoria, AVG(prezzo) FROM vendite GROUP BY categoria
media_cat = vendite.groupby("categoria")["prezzo"].mean()
print("\n--- GROUP BY categoria, AVG(prezzo) ---")
print(media_cat.round(2))

# SQL: SELECT citta, SUM(prezzo * quantita) as fatturato GROUP BY citta
vendite["fatturato"] = vendite["prezzo"] * vendite["quantita"]
fatturato_citta = vendite.groupby("citta")["fatturato"].sum()
print("\n--- Fatturato per città ---")
print(fatturato_citta.sort_values(ascending=False).round(2))

# Aggregazioni multiple:
# SQL: SELECT categoria, COUNT(*), AVG(prezzo), SUM(quantita) GROUP BY categoria
report = vendite.groupby("categoria").agg(
    ordini=("id_ordine", "count"),
    prezzo_medio=("prezzo", "mean"),
    quantita_totale=("quantita", "sum"),
    fatturato=("fatturato", "sum")
).round(2)
print("\n--- Report per categoria ---")
print(report)

# ==========================================================================
# PARTE 7: Creare e Modificare Colonne
# ==========================================================================

print("\n" + "=" * 60)
print("  CREARE COLONNE")
print("=" * 60)

# Creare una nuova colonna calcolata (già fatto sopra con 'fatturato'):
vendite["prezzo_con_iva"] = vendite["prezzo"] * 1.22
print(vendite[["prodotto", "prezzo", "prezzo_con_iva"]].head(5))

# Creare una colonna con condizioni (come un CASE WHEN in SQL):
vendite["fascia_prezzo"] = "economico"
vendite.loc[vendite["prezzo"] > 50, "fascia_prezzo"] = "medio"
vendite.loc[vendite["prezzo"] > 100, "fascia_prezzo"] = "premium"

print("\n--- Fascia prezzo ---")
print(vendite[["prodotto", "prezzo", "fascia_prezzo"]].drop_duplicates("prodotto"))

# Applicare una funzione personalizzata (come .map() in JS):
vendite["prodotto_upper"] = vendite["prodotto"].apply(lambda x: x.upper())
print(f"\nProdotti in maiuscolo: {vendite['prodotto_upper'].unique()[:3]}")

# ==========================================================================
# PARTE 8: Valori Unici e Conteggi
# ==========================================================================

print("\n" + "=" * 60)
print("  VALORI UNICI")
print("=" * 60)

# SQL: SELECT DISTINCT categoria FROM vendite
print(f"Categorie: {vendite['categoria'].unique()}")
print(f"Num. categorie: {vendite['categoria'].nunique()}")

# SQL: SELECT categoria, COUNT(*) GROUP BY categoria ORDER BY COUNT(*) DESC
print(f"\nConteggio per categoria:")
print(vendite["categoria"].value_counts())

print(f"\nConteggio per metodo pagamento:")
print(vendite["metodo_pagamento"].value_counts())

# 🔁 RINFORZO MIRATO — Dict comprehension
# Nel cap.05 era un punto da automatizzare. Qui lo riusiamo su dati Pandas:
conteggio_categoria = vendite["categoria"].value_counts().to_dict()
etichette = {k: f"{k} ({v} ordini)" for k, v in conteggio_categoria.items()}
print(f"\nRINFORZO dict comprehension: {etichette}")
print(f"{conteggio_categoria}")

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Crea un dizionario "sconti" con 3 categorie e percentuali.
# 2) Con dict comprehension crea "sconti_testo" tipo "categoria: 15%".
# 3) Stampa il dizionario finale.

dizionario =  {
  "elettronica" : 10,
  "abbigliamento" : 15,
  "sport" : 25  
  }
sconti_testo = {k.capitalize(): f"{k.capitalize()} => {v}%" for k, v in dizionario.items()}
print(f"{sconti_testo}")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ DI VERIFICA — Prima degli esercizi                              ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# DOMANDA 1 — Prevedi l'output:
#   print(vendite[["prodotto", "prezzo"]].shape)
#(n_righe, 2)
#
# DOMANDA 2 — Vero o Falso?
# "vendite['categoria'] restituisce un DataFrame." F
#
# DOMANDA 3 — Trova l'errore:
#   milano = vendite[vendite["citta"] = "Milano"]
# Qual e l'errore sintattico? l'operatore logico è scritto male : corretto dovrebbe essere "=="
#
# DOMANDA 4 — Definizione:
# Spiega la differenza tra .loc e .iloc in parole semplici.
#loc va a trovare gli elementi in base alla label, iloc in base a un indice numerico
#
# DOMANDA 5 — Completa il codice:
#   top = vendite.sort_values("prezzo", ascending=False).head(5)
# Completa per avere i 5 prezzi piu alti.
#
# DOMANDA 6 — Prevedi l'output:
#   print(vendite["categoria"].nunique())
# Che tipo di informazione restituisce nunique? restituisce il numero di categorie presenti all'interno del dataset, ognuna presa una sola volta senza ripetizioni
#
# DOMANDA 7 — 💬 Spiega con parole tue:
# Perche un DataFrame e il ponte naturale tra CSV "grezzo" e Machine Learning? il cvs grezzo è come la materia prima, il data frame è il dato ripulito e per cosi dire
#raffinato che viene dato nel machine learning, così da essere estremamente ottimizzato per essere assimilato.
#


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Approccio didattico del capitolo:
# - Esercizi 1-2: doppia versione (dict-style + Pandas) per consolidare il ponte mentale.
# - Esercizi 3-5: solo Pandas nativo, come nel flusso reale di analisi dati.
#
# ESERCIZIO 1 (Facile — Ponte Dict -> Pandas):
# A) Versione "dict-style":
#    1) Carica `case.csv`.
#    2) Converti il DataFrame in lista di dizionari con `to_dict(orient="records")`.
#    3) Mostra: prime 5 righe, numero righe, numero colonne, città uniche.
# B) Versione Pandas nativa:
#    Rifai gli stessi 4 punti usando solo: `head`, `shape`, `unique`.
# C) Confronto finale (3 righe):
#    scrivi quale versione è più leggibile e quale è più veloce da implementare.
#
# Scrivi il tuo codice qui sotto:
print("\nEsercizio 1\n")
import os
path_file = os.path.join(os.path.dirname(__file__),"dati", "case.csv")

"""Metodi nativi dei Dictionary"""
dict_data = pd.read_csv(path_file).to_dict(orient="records")
print(f"Primi 5 record:\n")
for k, v in enumerate(dict_data):
  if k < 5:
    print(f"{v}")
print(f"Città uniche:\n")
citta_uniche = {}
for k, v in enumerate(dict_data):
  citta_uniche[v['citta']] = citta_uniche.get(v['citta'], 0)
for k, v in citta_uniche.items():
  print(f"{k}")
print(f"\nNumero di Dizionari presenti:\n-->{len(dict_data)}")
print(f"Numero di colonne per record:\n-->{len(dict_data[0])}\n\n")



"""Metodi nativi Pandas"""
pd_data = pd.read_csv(path_file)
print(f"Primi 5 record:\n{pd_data.head(5)}")
print(f"Numero righe nel DataFrame:\n-->{len(pd_data)}")
print(f"Numero di colonne per riga:\n-->{len(pd_data.columns)}")
print(f"{pd_data['citta'].unique()}")


"""Sicuramente la differenza maggiora la li evince nel momento in cui facciamo
la selezione dei primi 5 record, o per andare a fare la stampa delle citta' uniche:
mentre con il dictionary abbiamo eseguito un ciclo for, con pandas abbiamo potuto
utilizzare il metodo .head(). Per il resto invece sono stati abbastanza equivalenti
in termini di facilità di implementazione"""

# ESERCIZIO 2 (Medio — Ponte sui filtri):
# Sempre usando `case.csv`.
# A) Versione "dict-style" con list comprehension:
#    a) Case a Milano con più di 70 mq
#    b) Case costruite dopo il 2000 con garage
#    c) Case con prezzo tra 100000 e 300000
# B) Versione Pandas nativa:
#    rifai a), b), c) con filtri Pandas e:
#    d) ordina per prezzo decrescente e mostra top 5
# C) Check di coerenza:
#    stampa la lunghezza dei risultati dict-style vs Pandas (devono coincidere su a,b,c).
#
# Scrivi il tuo codice qui sotto:
print("\nEsercizio 2\n")

"""Dict Style"""
dict_data = pd.read_csv(path_file).to_dict(orient="records")
case_milano_70 = [v['id'] for v in list(filter(lambda c:  c['citta'] == "Milano" and int(c['metri_quadri']) > 70, dict_data))]
case_dopo_2000 = [v['id'] for v in list(filter(lambda c: int(c['anno_costruzione']) > 2_000 and c['ha_garage'] == 1, dict_data))]
case_prezzo_medio =  [v['id'] for v in list(filter(lambda c: int(c['prezzo_euro']) >= 100_000 and int(c['prezzo_euro']) <= 300_000, dict_data))]

print(f"Indici case Milano con più di 70 mq:\n{case_milano_70}")
print(f"Indici case costruite dopo il 2000 che hanno il garage:\n{case_dopo_2000}")
print(f"Case con prezzo tra i 100.000 e 200.000 €:\n{case_prezzo_medio}")

"""Pandas Nativa"""

pd_data = pd.read_csv(path_file)
pd_case_milano_70 = pd_data[(pd_data['metri_quadri'] > 70) & (pd_data['citta'] == 'Milano')]
pd_case_dopo_2000 = pd_data[(pd_data['anno_costruzione'] > 2_000) & (pd_data['ha_garage'] == 1)]
pd_case_prezzo_medio = pd_data[(pd_data['prezzo_euro'] >= 100_000) & (pd_data['prezzo_euro'] <= 300_000)]

print(f"Case Milano con più di 70 mq con Pandas:\n{pd_case_milano_70.sort_values('prezzo_euro', ascending=False).head(5)}")
print(f"Case costruite dopo il 2000 che hanno il garage con Pandas:\n{pd_case_dopo_2000.sort_values('prezzo_euro', ascending=False).head(5)}")
print(f"Case con prezzo tra i 100.000 e 200.000 con Pandas €:\n{pd_case_prezzo_medio.sort_values('prezzo_euro', ascending=False).head(5)}")

"""Confronti"""

print(f"Confronti tra i due metodi:\n")
print(f"Case a Milano di più di 70 mq:\n {f'Confronto verificato con successo, per entrambi il risultato è: {len(case_milano_70)}' if len(case_milano_70) == pd_case_milano_70.shape[0] else 'Confronto errato'}")
print(f"Case costruite dopo il 2000 che hanno il garage:\n {f'Confronto verificato con successo, per entrambi il risultato è: {len(case_dopo_2000)}' if len(case_dopo_2000) == pd_case_dopo_2000.shape[0] else 'Confronto errato'}")
print(f"Case con prezzo tra i 100.000 e 200.000:\n {f'Confronto verificato con successo, per entrambi il risultato è: {len(case_prezzo_medio)}' if len(case_prezzo_medio) == pd_case_prezzo_medio.shape[0] else 'Confronto errato'}")


# ESERCIZIO 3 (Medio — GROUP BY, solo Pandas nativo):
# Sempre usando `case.csv`:
# a) Calcola il prezzo medio per città
# b) Calcola il numero di case per città
# c) Per ogni città: prezzo medio, mq medi, casa più cara, casa meno cara
# d) Calcola il prezzo medio al metro quadro per città
#    (crea prima la colonna prezzo_al_mq = prezzo_euro / metri_quadri)
# e) Ordina il report finale per prezzo medio decrescente
#
# Scrivi il tuo codice qui sotto:

print(f"\nEsercizio 3\n")
prezzo_medio_citta = pd_data.groupby('citta')['prezzo_euro'].mean()
case_per_citta = pd_data.groupby('citta').size()
pd_data['prezzo_x_mq'] = pd_data['prezzo_euro'] / pd_data['metri_quadri']
info_citta = pd_data.groupby('citta').agg(
  prezzo_medio = ("prezzo_euro", "mean"),
  mq_medi = ("metri_quadri", "mean"),
  prezzo_massimo = ("prezzo_euro", "max"),
  prezzo_minimo = ("prezzo_euro", "min"),
  media_x_mq = ("prezzo_x_mq", "mean")
).sort_values('media_x_mq', ascending=False)

print(f"{round(prezzo_medio_citta, 2)}\n")
print(f"{round(info_citta, 0)}")


# ESERCIZIO 4 (Sfida — solo Pandas nativo):
# Usando `vendite_ecommerce.csv`:
# a) Trova il giorno con il fatturato più alto
# b) Calcola il "carrello medio" per ogni metodo di pagamento
#    (fatturato totale / numero ordini per metodo)
# c) Crea un report che per ogni città mostra:
#    - Ordini totali
#    - Fatturato totale
#    - Prodotto più acquistato (per quantità)
# d) Aggiungi al report una colonna `ticket_medio`:
#    ticket_medio = fatturato_totale / ordini_totali
#
# Scrivi il tuo codice qui sotto:

print(f"\nEsercizio 4\n")
path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
pd_data = pd.read_csv(path_file)

pd_data['tot_fatturato'] = pd_data['prezzo'] * pd_data['quantita']
giorno_max_fatt = pd_data.groupby("data")['tot_fatturato'].sum().idxmax()
print(f"{giorno_max_fatt}\n")
ordini_per_metodo = pd_data.groupby('metodo_pagamento')['id_ordine'].nunique()
carrello_medio = pd_data.groupby('metodo_pagamento')['tot_fatturato'].sum() / ordini_per_metodo
print("Carrello Medio\n")
print(f"{round(carrello_medio, 2).sort_values()}\n")
print(f"Dati divisi per metodo di pagamento\n")
for k, v in pd_data.groupby('metodo_pagamento'):
  print(f"{k} => {v}\n")  

report_citta = pd_data.groupby("citta", as_index=False).agg(
  ordini_totali=("id_ordine", "nunique"),
  fatturato_totale=("tot_fatturato", "sum")
)
top_prodotto_citta = (
  pd_data.groupby(["citta", "prodotto"], as_index=False)["quantita"]
  .sum()
  .sort_values(["citta", "quantita"], ascending=[True, False])
  .drop_duplicates("citta")
  .rename(columns={"prodotto": "prodotto_top"})
  [["citta", "prodotto_top"]]
)
report_citta = report_citta.merge(top_prodotto_citta, on="citta", how="left")
report_citta["ticket_medio"] = report_citta["fatturato_totale"] / report_citta["ordini_totali"]
print("Report finale per citta:\n")
print(
  report_citta.sort_values("fatturato_totale", ascending=False).round(
    {"fatturato_totale": 2, "ticket_medio": 2}
  )
)
  


# ESERCIZIO 5 (Sfida — Preview ML, solo Pandas):
# Questo esercizio anticipa quello che farai nel Modulo 2 (Machine Learning).
# Usando `case.csv`, prepara i dati come farebbe un data scientist:
# a) Crea una colonna booleana 'is_centro' (True se distanza_centro_km < 3)
# b) Crea una colonna 'decade' con la decade di costruzione (es. 1970, 1980...)
#    Suggerimento: (anno // 10) * 10
# c) Calcola la correlazione tra metri_quadri e prezzo_euro:
#    df[["metri_quadri","prezzo_euro"]].corr()
#    (un valore vicino a 1 = forte correlazione positiva)
# d) Dividi il dataset: 80% training, 20% test (prime 24 righe e ultime 6)
#    Stampa la shape di entrambi
# e) Check qualità dati:
#    stampa eventuali valori nulli per colonna e i dtype finali principali
#
# Scrivi il tuo codice qui sotto:

print(f"\nEsercizio 5\n")
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
dati_case = pd.read_csv(path_file)
dati_case['is_centro'] = dati_case['distanza_centro_km'] < 3
dati_case['decade'] = (dati_case['anno_costruzione'] // 10) * 10
correlazione = dati_case[['metri_quadri', 'prezzo_euro']].corr()
print(f"{dati_case.head(1)}")
print(f"{correlazione}")
training = dati_case[:(dati_case.shape[0]*80) // 100]
testing = dati_case[(dati_case.shape[0]*80) // 100:]
print(f"TRAINING:\n{training.shape}")
print(f"TESTING:\n{testing.shape}")
print("\nValori nulli per colonna:")
print(dati_case.isnull().sum())
print("\nDtype finali:")
print(dati_case.dtypes)



# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  🏗️ PROGETTO INCREMENTALE — Controllo Documentale (Pandas)            ║
# ╚═════════════════════════════════════════════════════════════════════════╝
#
# Task (20-30 minuti):
# 1) Carica `case.csv` in un DataFrame chiamato `pratiche`.
# 2) Crea una colonna `rischio_base`:
#    - "rosso"  se prezzo_euro > 350000 e distanza_centro_km < 2
#    - "giallo" se prezzo_euro tra 200000 e 350000
#    - "verde"  altrimenti
# 3) Crea un report per citta con:
#    - pratiche_totali
#    - prezzo_medio
#    - metri_quadri_medi
#    - quota_rosso (percentuale pratiche rosse)
# 4) Ordina il report per quota_rosso decrescente e stampa top 5.
# 5) Salva il report in `dati/report_rischio_citta.csv`.
#
# Obiettivo mentale:
# - Da NumPy (shape e assi) a Pandas (righe/colonne etichettate)
# - Da analisi tecnica a report operativo leggibile
#
# Scrivi il tuo codice qui sotto:

print(f"\nProgetto Incrementale\n")
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
pratiche = pd.read_csv(path_file)
pratiche['rischio_base'] ="verde"
mask_rosso = (pratiche['prezzo_euro'] > 350_000) & (pratiche['distanza_centro_km'] < 2)
mask_giallo = pratiche['prezzo_euro'].between(200_000, 350_000, inclusive="both") & (~mask_rosso)
pratiche.loc[mask_rosso, "rischio_base"] = "rosso"
pratiche.loc[mask_giallo, "rischio_base"] = "giallo"
print(f"{pratiche}\n")
report = (
  pratiche.groupby("citta", as_index=False).agg(
    pratiche_totali = ("id", "nunique"),
    prezzo_medio = ("prezzo_euro", lambda q: round(q.mean(), 2)),
    metri_quadri_medi = ("metri_quadri", lambda q: round(q.mean(), 2)),
    quota_rosso = ("rischio_base", lambda q: round((q == "rosso").mean() * 100, 2))
  )
).sort_values("quota_rosso", ascending=False)
print("Report città\n")
print(f"{report.head(5)}")
report.to_csv("dati/report_rischio_citta.csv", index=False)

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
# case = pd.read_csv(percorso_case)
# print(case.head())
# print(f"Shape: {case.shape}")
# print(case.describe())
# print(f"Città: {case['citta'].unique()}")

# --- SOLUZIONE ESERCIZIO 2 ---
# percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
# case = pd.read_csv(percorso_case)
# # a)
# milano_grandi = case[(case["citta"] == "Milano") & (case["metri_quadri"] > 70)]
# print(f"Milano >70mq:\n{milano_grandi}")
# # b)
# nuove_garage = case[(case["anno_costruzione"] > 2000) & (case["ha_garage"] == 1)]
# print(f"\nDopo 2000 con garage:\n{nuove_garage}")
# # c)
# top5 = case.sort_values("prezzo_euro", ascending=False).head(5)
# print(f"\nTop 5 costose:\n{top5[['citta','metri_quadri','prezzo_euro']]}")
# # d)
# fascia = case[(case["prezzo_euro"] >= 100000) & (case["prezzo_euro"] <= 300000)]
# print(f"\nFascia 100k-300k: {len(fascia)} case")

# --- SOLUZIONE ESERCIZIO 3 ---
# percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
# case = pd.read_csv(percorso_case)
# # a)
# print(case.groupby("citta")["prezzo_euro"].mean().round(0))
# # b)
# print(case.groupby("citta").size())
# # c)
# report = case.groupby("citta").agg(
#     prezzo_medio=("prezzo_euro", "mean"),
#     mq_medi=("metri_quadri", "mean"),
#     piu_cara=("prezzo_euro", "max"),
#     meno_cara=("prezzo_euro", "min")
# ).round(0)
# print(report)
# # d)
# case["prezzo_al_mq"] = case["prezzo_euro"] / case["metri_quadri"]
# print(case.groupby("citta")["prezzo_al_mq"].mean().round(0).sort_values(ascending=False))

# --- SOLUZIONE ESERCIZIO 4 ---
# vendite["fatturato"] = vendite["prezzo"].astype(float) * vendite["quantita"].astype(int)
# # a)
# fatt_giorno = vendite.groupby("data")["fatturato"].sum()
# giorno_top = fatt_giorno.idxmax()
# print(f"Giorno migliore: {giorno_top} ({fatt_giorno.max():.2f}€)")
# # b)
# per_metodo = vendite.groupby("metodo_pagamento").agg(
#     fatturato=("fatturato", "sum"),
#     ordini=("id_ordine", "count")
# )
# per_metodo["carrello_medio"] = (per_metodo["fatturato"] / per_metodo["ordini"]).round(2)
# print(per_metodo)
# # c) (semplificato)
# for citta in vendite["citta"].unique():
#     dati_citta = vendite[vendite["citta"] == citta]
#     top_prod = dati_citta.groupby("prodotto")["quantita"].sum().idxmax()
#     print(f"{citta}: {len(dati_citta)} ordini, {dati_citta['fatturato'].sum():.2f}€, top: {top_prod}")

# --- SOLUZIONE ESERCIZIO 5 ---
# percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
# case = pd.read_csv(percorso_case)
# # a)
# case["is_centro"] = case["distanza_centro_km"] < 3
# print(f"Case in centro: {case['is_centro'].sum()}")
# # b)
# case["decade"] = (case["anno_costruzione"] // 10) * 10
# print(f"Decadi:\n{case['decade'].value_counts().sort_index()}")
# # c)
# corr = case[["metri_quadri", "prezzo_euro"]].corr()
# print(f"\nCorrelazione mq-prezzo:\n{corr}")
# # d)
# training = case.iloc[:24]
# test = case.iloc[24:]
# print(f"\nTraining shape: {training.shape}")
# print(f"Test shape: {test.shape}")

# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) 12 4
# 2) Vero
# 3) Errore di shape: (8*8*3)=192, non 64
# 4) Traslare = spostare i valori; ruotare = cambiare orientamento/assi
# 5) -1
# 6) (2, 3)
# 7) Perche previene bug silenziosi e garantisce che ogni trasformazione sia coerente

# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) (n_righe, 2) -> nel file corrente (12, 2)
# 2) Falso (restituisce una Series)
# 3) Usa "=" invece di "=="
# 4) .loc usa etichette; .iloc usa posizioni numeriche
# 5) False
# 6) Restituisce quante categorie distinte esistono
# 7) Perche permette pulizia, filtro, aggregazioni e preparazione feature in modo tabellare
