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

 ANALOGIA CON LARAVEL ELOQUENT:
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
 └──────────────────────────────────────────────────┘

============================================================================
"""

import pandas as pd  # 'pd' è la convenzione universale
import numpy as np
import os

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


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Carica il file 'case.csv' con pd.read_csv() e:
# a) Mostra le prime 5 righe
# b) Mostra la shape del DataFrame
# c) Mostra le statistiche con .describe()
# d) Elenca le città uniche presenti nel dataset
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio — SELECT + WHERE):
# Sempre usando il dataset case.csv:
# a) Seleziona solo le case a Milano con più di 70 mq
# b) Seleziona le case costruite dopo il 2000 con garage
# c) Ordina tutte le case per prezzo decrescente e mostra le top 5
# d) Seleziona le case con prezzo tra 100,000€ e 300,000€
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio — GROUP BY):
# Sempre usando case.csv:
# a) Calcola il prezzo medio per città
# b) Calcola il numero di case per città
# c) Per ogni città: prezzo medio, mq medi, casa più cara, casa meno cara
# d) Calcola il prezzo medio al metro quadro per città
#    (crea prima la colonna prezzo_al_mq = prezzo_euro / metri_quadri)
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida):
# Usando vendite_ecommerce.csv:
# a) Trova il giorno con il fatturato più alto
# b) Calcola il "carrello medio" per ogni metodo di pagamento
#    (fatturato totale / numero ordini per metodo)
# c) Crea un report che per ogni città mostra:
#    - Ordini totali
#    - Fatturato totale
#    - Prodotto più acquistato (per quantità)
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Preview ML):
# Questo esercizio anticipa quello che farai nel Modulo 2 (Machine Learning).
# Usando case.csv, prepara i dati come farebbe un data scientist:
# a) Crea una colonna booleana 'is_centro' (True se distanza_centro_km < 3)
# b) Crea una colonna 'decade' con la decade di costruzione (es. 1970, 1980...)
#    Suggerimento: (anno // 10) * 10
# c) Calcola la correlazione tra metri_quadri e prezzo_euro:
#    df[["metri_quadri","prezzo_euro"]].corr()
#    (un valore vicino a 1 = forte correlazione positiva)
# d) Dividi il dataset: 80% training, 20% test (prime 24 righe e ultime 6)
#    Stampa la shape di entrambi
#
# Scrivi il tuo codice qui sotto:
# ...


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
