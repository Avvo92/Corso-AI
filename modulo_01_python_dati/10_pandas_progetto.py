"""
============================================================================
 MODULO 1 — ESERCIZIO 10: Mini-Progetto Pandas
 Analisi Completa di un Dataset Reale
============================================================================

 TEORIA: Il Workflow di un Data Scientist

 Quando un data scientist riceve un nuovo dataset, segue sempre
 questi passaggi (chiamati EDA = Exploratory Data Analysis):

 1. CARICARE i dati
 2. ESPLORARE: shape, tipi, valori nulli, prime righe
 3. PULIRE: gestire valori mancanti, correggere tipi
 4. ANALIZZARE: statistiche, raggruppamenti, correlazioni
 5. VISUALIZZARE: grafici (lo faremo nel file 11)
 6. CONCLUDERE: insight e decisioni

 È come il workflow di un web developer:
 1. Leggere le specifiche (capire i dati)
 2. Setup del progetto (caricare e pulire)
 3. Sviluppo (analisi)
 4. Testing (verifica risultati)
 5. Deploy (presentare i risultati)

 In questo esercizio guideremo l'intero processo sul dataset
 vendite_ecommerce.csv.

============================================================================
"""

import pandas as pd
import numpy as np
import os

# ==========================================================================
# STEP 1: CARICARE I DATI
# ==========================================================================

percorso = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
df = pd.read_csv(percorso)

print("=" * 60)
print("  STEP 1: CARICAMENTO")
print("=" * 60)
print(f"Dataset caricato: {df.shape[0]} righe, {df.shape[1]} colonne")

# ==========================================================================
# STEP 2: ESPLORAZIONE
# ==========================================================================

print("\n" + "=" * 60)
print("  STEP 2: ESPLORAZIONE")
print("=" * 60)

print("\n--- Prime 5 righe ---")
print(df.head())

print("\n--- Informazioni ---")
print(df.info())

print("\n--- Statistiche ---")
print(df.describe())

print("\n--- Valori nulli per colonna ---")
print(df.isnull().sum())
# Se ci sono valori nulli, bisogna decidere cosa fare:
# - Eliminarli: df.dropna()
# - Riempirli: df.fillna(valore)
# In questo caso non ne abbiamo, ma è sempre bene controllare!

print("\n--- Valori unici per colonna ---")
for col in df.columns:
    print(f"  {col}: {df[col].nunique()} valori unici")

# ==========================================================================
# STEP 3: PULIZIA E PREPARAZIONE
# ==========================================================================

print("\n" + "=" * 60)
print("  STEP 3: PULIZIA")
print("=" * 60)

# Convertiamo i tipi corretti (il CSV legge tutto come stringa/oggetto)
df["prezzo"] = df["prezzo"].astype(float)
df["quantita"] = df["quantita"].astype(int)
df["data"] = pd.to_datetime(df["data"])  # Convertiamo la data in tipo datetime!

# Creiamo colonne calcolate utili:
df["fatturato"] = df["prezzo"] * df["quantita"]
df["giorno_settimana"] = df["data"].dt.day_name()  # Lunedì, Martedì...

print("Tipi dopo la pulizia:")
print(df.dtypes)
print(f"\nColonne aggiunte: 'fatturato', 'giorno_settimana'")

# ==========================================================================
# STEP 4: ANALISI
# ==========================================================================

print("\n" + "=" * 60)
print("  STEP 4: ANALISI")
print("=" * 60)

# --- ANALISI 1: Overview Generale ---
print("\n📊 OVERVIEW")
print(f"  Periodo: dal {df['data'].min().date()} al {df['data'].max().date()}")
print(f"  Ordini totali: {len(df)}")
print(f"  Fatturato totale: {df['fatturato'].sum():,.2f}€")
print(f"  Ordine medio: {df['fatturato'].mean():,.2f}€")
print(f"  Prodotti unici: {df['prodotto'].nunique()}")
print(f"  Città servite: {df['citta'].nunique()}")

# --- ANALISI 2: Top Prodotti ---
print("\n📦 TOP PRODOTTI (per fatturato)")
top_prodotti = df.groupby("prodotto").agg(
    fatturato=("fatturato", "sum"),
    quantita=("quantita", "sum"),
    ordini=("id_ordine", "count")
).sort_values("fatturato", ascending=False)
print(top_prodotti.round(2))

# --- ANALISI 3: Performance per Città ---
print("\n🏙️  PERFORMANCE PER CITTÀ")
per_citta = df.groupby("citta").agg(
    ordini=("id_ordine", "count"),
    fatturato=("fatturato", "sum"),
    ordine_medio=("fatturato", "mean")
).sort_values("fatturato", ascending=False)
print(per_citta.round(2))

# --- ANALISI 4: Metodi di Pagamento ---
print("\n💳 METODI DI PAGAMENTO")
per_pagamento = df.groupby("metodo_pagamento").agg(
    ordini=("id_ordine", "count"),
    fatturato=("fatturato", "sum")
)
per_pagamento["percentuale"] = (per_pagamento["ordini"] / len(df) * 100).round(1)
print(per_pagamento.sort_values("ordini", ascending=False))

# --- ANALISI 5: Trend Temporale ---
print("\n📅 FATTURATO PER GIORNO")
per_giorno = df.groupby("data")["fatturato"].sum().sort_index()
for data, fatt in per_giorno.items():
    barra = "█" * int(fatt / 20)
    print(f"  {data.date()}: {fatt:>8.2f}€  {barra}")

# --- ANALISI 6: Categorie ---
print("\n📁 CATEGORIE")
per_cat = df.groupby("categoria").agg(
    prodotti_unici=("prodotto", "nunique"),
    ordini=("id_ordine", "count"),
    fatturato=("fatturato", "sum"),
    prezzo_medio=("prezzo", "mean")
).sort_values("fatturato", ascending=False)
print(per_cat.round(2))

# ==========================================================================
# STEP 5: INSIGHT (Conclusioni)
# ==========================================================================

print("\n" + "=" * 60)
print("  STEP 5: INSIGHT")
print("=" * 60)

# Troviamo automaticamente gli insight principali:
cat_top = per_cat["fatturato"].idxmax()
citta_top = per_citta["fatturato"].idxmax()
prodotto_top = top_prodotti["fatturato"].idxmax()
metodo_top = per_pagamento["ordini"].idxmax()

print(f"""
RISULTATI DELL'ANALISI:

1. La categoria più redditizia è "{cat_top}"
   con {per_cat.loc[cat_top, 'fatturato']:.2f}€ di fatturato

2. La città con più fatturato è "{citta_top}"
   con {per_citta.loc[citta_top, 'ordini']} ordini

3. Il prodotto best-seller è "{prodotto_top}"
   con {top_prodotti.loc[prodotto_top, 'fatturato']:.2f}€ di fatturato

4. Il metodo di pagamento preferito è "{metodo_top}"
   usato nel {per_pagamento.loc[metodo_top, 'percentuale']}% degli ordini
""")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Progetto Completo — Case):
# Ripeti l'intero workflow EDA sul file case.csv:
# 1. Carica il dataset
# 2. Esplora (shape, info, describe, valori nulli)
# 3. Pulisci (converti tipi, crea colonne: prezzo_al_mq, eta_immobile)
# 4. Analizza:
#    a) Overview generale
#    b) Prezzo medio per città
#    c) Prezzo medio per decade di costruzione
#    d) Impatto del garage sul prezzo
#    e) Impatto del balcone sul prezzo
#    f) Correlazione tra distanza dal centro e prezzo
# 5. Scrivi 3 "insight" conclusivi
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Sfida — Crea il Tuo Dataset):
# Crea da zero un DataFrame con dati inventati di un'app di streaming:
# - 50 righe (utenti)
# - Colonne: nome, eta, piano (free/premium), ore_ascolto_mese,
#            genere_preferito, citta
# Poi fai un'analisi completa come quella sopra.
# Suggerimento per generare dati:
#   nomi = [f"Utente_{i}" for i in range(50)]
#   eta = np.random.randint(16, 65, 50)
#   piani = np.random.choice(["free", "premium"], 50, p=[0.7, 0.3])
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 (estratto) ---
# percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
# case = pd.read_csv(percorso_case)
#
# # Pulizia
# case["prezzo_al_mq"] = (case["prezzo_euro"] / case["metri_quadri"]).round(0)
# case["eta_immobile"] = 2024 - case["anno_costruzione"]
# case["decade"] = (case["anno_costruzione"] // 10) * 10
#
# # Analisi
# print("OVERVIEW:")
# print(f"  Case: {len(case)}, Città: {case['citta'].nunique()}")
# print(f"  Prezzo medio: {case['prezzo_euro'].mean():,.0f}€")
# print(f"  Mq medi: {case['metri_quadri'].mean():.0f}")
#
# print("\nPREZZO PER CITTA:")
# print(case.groupby("citta")["prezzo_euro"].mean().sort_values(ascending=False).round(0))
#
# print("\nPREZZO PER DECADE:")
# print(case.groupby("decade")["prezzo_euro"].mean().sort_values().round(0))
#
# print("\nIMPATTO GARAGE:")
# print(case.groupby("ha_garage")["prezzo_euro"].mean().round(0))
#
# print("\nIMPATTO BALCONE:")
# print(case.groupby("ha_balcone")["prezzo_euro"].mean().round(0))
#
# print("\nCORRELAZIONE distanza-prezzo:")
# print(case[["distanza_centro_km", "prezzo_euro"]].corr())
