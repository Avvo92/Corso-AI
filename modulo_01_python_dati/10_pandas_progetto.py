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
# QUIZ D'INGRESSO — Ripasso dal Capitolo 09
# ==========================================================================
#
# DOMANDA 1 — Prevedi l'output:
#   df[["prodotto", "prezzo"]].shape
# Se il dataset ha 30 righe, che shape ottieni? (30, 2)
#
# DOMANDA 2 — Vero/Falso:
# "df['categoria'] restituisce un DataFrame." Falso restituisce una Series
#
# DOMANDA 3 — Trova l'errore:
#   img = np.random.randint(0, 256, (8, 8, 3))
#   flat = img.reshape(64,)
# Qual e il vero problema? il problema è il volore che si è impostato per la reshape, in quanto 8*8*3 da 192, non 64
#
# DOMANDA 4 — Completa:
# `idxmax()` restituisce l'elemento con il valore massimo ; `max()` restituisce il valore massimo
#
# DOMANDA 5 — Prevedi:
# Se `q = pd.Series([True, False, True])`, quanto vale `q.mean() * 100`? 66.6666666 periodico
#
# DOMANDA 6 — Scelta multipla:
# Per contare ordini unici per citta, useresti:
# a) count()
# b) nunique() x
# c) sum()
#
# DOMANDA 7 — 💬 Spiega con parole tue:
# Qual e la differenza pratica tra Series e DataFrame quando costruisci un report?
#il dataframe è tutto il set di dati, nella sua interezza, la Series invece è un qualsiasi sottoinsieme del dataframe

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

# 🔁 RINFORZO MIRATO — `.shape` su selezione colonne
# Al quiz del cap.09 c'era stata confusione su shape quando selezioni due colonne.
# Regola pratica:
# - df["col"] -> Series -> shape a 1 dimensione: (n_righe,)
# - df[["col1", "col2"]] -> DataFrame -> shape a 2 dimensioni: (n_righe, 2)
print("\nRINFORZO shape/Series/DataFrame:")
print(f"df['prodotto'] shape -> {df['prodotto'].shape}")
print(f"df[['prodotto','prezzo']] shape -> {df[['prodotto', 'prezzo']].shape}")

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

# 🔁 RINFORZO MIRATO — leggere il risultato, non solo il codice
# Per non confondere valore massimo e "chi lo ha prodotto":
fatturato_per_data = df.groupby("data")["fatturato"].sum()
print(f"Giorno top (idxmax): {fatturato_per_data.idxmax().date()}")
print(f"Valore top (max): {fatturato_per_data.max():.2f}€")

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


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "count() e nunique() sono equivalenti in tutti i report."
#
# DOMANDA 2 — Prevedi l'output:
#   report = df.groupby("citta").agg(ordini=("id_ordine", "nunique"))
#   print(report.shape)
# Quante colonne ha il report?
#
# DOMANDA 3 — Trova l'errore:
#   report = df.groupby("citta").agg(
#       fatturato=("fatturato", "sum"),
#       ticket_medio=("fatturato", "sum") / ("id_ordine", "nunique")
#   )
# Perche non funziona?
#
# DOMANDA 4 — Completa:
# Per aggiungere una colonna derivata dopo `.agg`, uso:
# `report["nuova_col"] = ______________________________`
#
# DOMANDA 5 — 💬 Spiega con parole tue:
# Perche `.agg` e utile per creare report "da business" e non solo output tecnici?
#

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
print("\nEsercizio 1\n")

"""Caricamento dei dati"""

path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
data = pd.read_csv(path_file)

"""Esplorazione preliminare"""

print("---- Esplorazione ----")
print(f"Shape:\nRighe =>{data.shape[0]}\nColonne =>{data.shape[1]}\n")
print("Info generali:\n")
print(data.info())
print("\nDescrizione:\n")
print(f"{data.describe()}\n")
print("Numero valori nulli:")
print(f"{data.isnull().sum()}\n")

"""Pulizia e aggiunta di colonne utili"""

data[["metri_quadri", "num_stanze", "piano", "ha_balcone", "ha_garage", "anno_costruzione"]] = data[["metri_quadri", "num_stanze", "piano", "ha_balcone", "ha_garage", "anno_costruzione"]].astype(int)
data[["distanza_centro_km", "prezzo_euro"]] = data[["distanza_centro_km", "prezzo_euro"]].astype(float)
data["prezzo_al_metro"] = round(data["prezzo_euro"] / data["metri_quadri"], 2)
data["eta_immobile"] = 2026 - data["anno_costruzione"]

"""Analisi dei dati"""

print("\nOverview generale\n")
print(f"Anni di costruzione: dal {data['anno_costruzione'].min()} al {data['anno_costruzione'].max()}")
print(f"Totale numero di immobili: {data.shape[0]}")
print(f"Totale valore degli immobili analizzati: {round(data['prezzo_euro'].sum(), 2):.2f} €")

"""Aggregazione dei dati"""

prezzo_medio_citta = data.groupby("citta")["prezzo_al_metro"].mean().round(2)
data["decade"] = data["anno_costruzione"] // 10 * 10
prezzo_medio_decade = data.groupby("decade")["prezzo_al_metro"].mean().round(2)
print(f"\nPresso medio per città")
print(f"{prezzo_medio_citta}")
print(f"\nPresso medio per decade:")
print(f"{prezzo_medio_decade}")

print("\nImpatto del garage sul prezzo\n")
impatto_garage = data.groupby("ha_garage").agg(
    prezzo_medio_mq = ("prezzo_al_metro", "mean"),
    prezzo_mediano_mq = ("prezzo_al_metro", "median"),
    prezzo_medio = ("prezzo_euro", "mean"),
    prezzo_mediano = ("prezzo_euro", "median")
)
print(f"Prezzo medio al mq immobili senza garage:\n{impatto_garage.loc[0, 'prezzo_medio_mq'].round(2):.2f} €\n")
print(f"Prezzo medio al mq immobili con garage:\n{impatto_garage.loc[1, 'prezzo_medio_mq'].round(2):.2f} €\n")
delta = impatto_garage.loc[1, "prezzo_medio_mq"] - impatto_garage.loc[0, "prezzo_medio_mq"]
percentuale_delta = ((impatto_garage.loc[1, "prezzo_medio_mq"] / impatto_garage.loc[0, "prezzo_medio_mq"]) - 1) * 100
print(f"Delta => {delta.round(2)}")
print(f"Percentuale Delta => {percentuale_delta.round(2)} %")


print("\nImpatto del balcone sul prezzo\n")
impatto_balcone = data.groupby("ha_balcone").agg(
    prezzo_medio_mq = ("prezzo_al_metro", "mean"),
    prezzo_mediano_mq = ("prezzo_al_metro", "median"),
    prezzo_medio = ("prezzo_euro", "mean"),
    prezzo_mediano = ("prezzo_euro", "median")    
)
print(f"Prezzo medio al mq immobili senza balcone:\n{impatto_balcone.loc[0, 'prezzo_medio_mq'].round(2):.2f} €\n")
print(f"Prezzo medio al mq immobili con balcone:\n{impatto_balcone.loc[1, 'prezzo_medio_mq'].round(2):.2f} €\n")
delta_2 = impatto_balcone.loc[1, "prezzo_medio_mq"] - impatto_balcone.loc[0, "prezzo_medio_mq"]
percentuale_delta_2 = ((impatto_balcone.loc[1, "prezzo_medio_mq"] / impatto_balcone.loc[0, "prezzo_medio_mq"]) - 1) * 100
print(f"Delta => {delta_2.round(2)}")
print(f"Percentuale Delta => {percentuale_delta_2.round(2)} %")

print("\nCorrelazione tra distanza dal centro e prezzo")
correlazione_prezzo_distanza = data["prezzo_euro"].corr(data["distanza_centro_km"])
print(f"{correlazione_prezzo_distanza}")

print("\nInsights generici")
print(f"La casa più costosa in vendita:\n\n{data.loc[data['prezzo_al_metro'].idxmax()]}\n")
print(f"La casa più economica in vendita:\n{data.loc[data['prezzo_al_metro'].idxmin()]}\n")
print(f"Città più costosa:\n{data.groupby('citta')['prezzo_al_metro'].mean().idxmax()}")


# ESERCIZIO 2 (Sfida — Crea il Tuo Dataset):
# Crea da zero un DataFrame con dati inventati di un'app di streaming:
# - 50 righe (utenti)
# - Colonne: nome, eta, piano (free/premium), ore_ascolto_mese,
#            genere_preferito, citta
#
# Poi esegui QUESTE analisi (una per una):
#
# 1) Esplorazione base
#    a) shape (righe, colonne)
#    b) info()
#    c) describe() per colonne numeriche
#    d) valori nulli per colonna
#
# 2) Pulizia/trasformazioni
#    a) verifica e conversione tipi (eta int, ore_ascolto_mese numerico)
#    b) crea fascia_eta (es. 16-24, 25-34, 35-44, 45-54, 55+)
#    c) crea ore_giornaliere_medie = ore_ascolto_mese / 30
#
# 3) Analisi descrittive principali
#    a) utenti totali, età media, ore medie mensili
#    b) conteggio utenti per piano (free/premium)
#    c) ore medie mensili per piano
#    d) ore medie mensili per città
#    e) ore medie mensili per genere_preferito
#    f) piano più usato in assoluto
#    g) città con più utenti
#
# 4) Analisi avanzate (stile mini-report)
#    a) confronto free vs premium: differenza assoluta e percentuale delle ore medie
#    b) top 5 utenti per ore_ascolto_mese
#    c) distribuzione utenti per fascia_eta
#    d) correlazione tra eta e ore_ascolto_mese (.corr())
#
# 5) Insight finali (obbligatori)
#    Scrivi 3 insight in linguaggio business, ad esempio:
#    - quale piano ascolta di più e quanto
#    - quale città è più attiva
#    - se l'età sembra influenzare (o no) le ore di ascolto


print("\nEsercizio 2\n")
n = 50
nomi = [f"Utente_{i}" for i in range(1, 51)]
eta = np.random.randint(16, 65, n)
piano =  np.random.choice(["free", "premium"], n, p=[0.7, 0.3])
genere_preferito = np.random.choice(["pop", "rock", "jazz", "classica"], n)
citta = np.random.choice(["roma", "milano", "bologna", "firenze", "torino"], n)
ore_ascolto_mese = np.random.randint(10, 45, n)

df_streaming = pd.DataFrame({
    "nome": nomi,
    "eta": eta,
    "piano": piano,
    "genere": genere_preferito,
    "citta": citta,
    "ore_ascolto_mese": ore_ascolto_mese 
})

print(f"\nAnalisi preliminare")
print(f"Shape:\n{df_streaming.shape}")
print("\nInfo Generali\n")
df_streaming.info()
print(f"\nStatistica;\n{df_streaming.describe()}")
print(f"Valori null:\n{df_streaming.isnull().sum()}")

print(f"\nPulizia e trasformazioni")
df_streaming["eta"] = df_streaming["eta"].astype(int)
df_streaming["ore_ascolto_mese"] = df_streaming["ore_ascolto_mese"].astype(int)
df_streaming["ore_ascolto_giornaliere"] = df_streaming["ore_ascolto_mese"] / 30
bins = [16, 24, 34, 44, 54, 120]
labels = ["16-24", "25-34", "35-44", "45-54", "55+"]
df_streaming["fascia_eta"] = pd.cut(
    df_streaming["eta"],
    bins = bins,
    labels = labels,
    include_lowest = True
)
print("\nAnalisi descrittive principali\n")
print(f"Numero Utenti:\n{df_streaming.shape[0]}")
print(f"Età media:\n{df_streaming['eta'].mean().round(0):.0f}")
print(f"Media ore mensili:\n{df_streaming['ore_ascolto_mese'].mean().round(2):.2f}\n")
print(f"Numero utenti per piano:\n{df_streaming.groupby('piano').size()}\n")
print(f"Ore medie mensili per piano:\n{df_streaming.groupby('piano')['ore_ascolto_mese'].mean().round(2)}\n")
print(f"Ore medie mensili per genere:\n{df_streaming.groupby('genere')['ore_ascolto_mese'].mean().round(2)}\n")
print(f"Piano più utilizzato:\n{df_streaming.groupby('piano')['ore_ascolto_mese'].sum().idxmax()}\n")
print(f"Citta con più utenti:\n{df_streaming.groupby('citta').size().sort_values(ascending=False)}")

print("\nAnalisi avanzate\n")
medie = df_streaming.groupby('piano')['ore_ascolto_mese'].mean().sort_values(ascending=False)
print(f"Piano {medie.index[0]} - {medie.index[1]} => differenza di {round(medie.iloc[0] - medie.iloc[1], 2)} ore\n")
print(f"Top 5 utenti per ore di ascolto del mese:\n{df_streaming.sort_values(by='ore_ascolto_mese', ascending=False)[['nome', 'ore_ascolto_mese']].head(5)}\n")
print(f"Distribuzione utenti per fascia d'età:\n{df_streaming.groupby('fascia_eta').size().sort_values(ascending=False)}\n")
print(f"Correlazione tra età e ore di ascolto:\n{df_streaming['eta'].corr(df_streaming['ore_ascolto_mese']):.2f}")

print(f"\nInsight finali\n")
medie = df_streaming.groupby('piano')['ore_ascolto_mese'].mean().sort_values(ascending=False)
print(f"Il piano che ascolta di più:\n{medie.index[0]} => {medie.iloc[0]}\n")
print(f"La citta più attiva è:\n{df_streaming.groupby('citta')['ore_ascolto_mese'].sum().sort_values(ascending=False).idxmax()}")
corr = df_streaming['eta'].corr(df_streaming['ore_ascolto_mese'])
print(f"l'età sembra {'non' if  -0.5 < corr < 0.5 else ''} influenzare le ore di ascolto\n")




# ESERCIZIO 3 (Rinforzo mirato `.agg` — Report Operativo):
# Sempre su `vendite_ecommerce.csv`, crea un report per citta con:
# - ordini_totali (id_ordine unici)
# - fatturato_totale (somma fatturato)
# - prezzo_medio (media prezzo)
# - quantita_totale (somma quantita)
# - ticket_medio (fatturato_totale / ordini_totali)
# Vincoli:
# 1) usare `groupby(...).agg(...)` per costruire il report base
# 2) aggiungere `ticket_medio` come colonna derivata
# 3) ordinare per `fatturato_totale` desc
# 4) salvare in `dati/report_citta_agg.csv`
#
# Scrivi il tuo codice qui sotto:
print("\nEsercizio 4\n")
path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
data = pd.read_csv(path_file)
data['fatturato'] = data['prezzo'] * data['quantita']
report = data.groupby('citta').agg(
    ordini_totali = ("id_ordine", "size"),
    totale_fatturato = ("fatturato", "sum"),
    prezzo_medio = ("prezzo", "mean"),
    quantita_tot = ("quantita", "sum")
)
report["ticket_medio"] = report["totale_fatturato"] / report["ordini_totali"]

print(f"{report.sort_values(by='totale_fatturato', ascending=False)}\n\n")


# ESERCIZIO 4 (Rinforzo `.agg` + Debug logico):
# Sul file `case.csv` crea un report per citta:
# - pratiche_totali
# - prezzo_medio
# - metri_quadri_medi
# - quota_case_recenti (anno_costruzione >= 2000, in percentuale)
# Poi rispondi in 3 righe:
# a) Perche `count()` e diverso da `nunique()` in un report?
# risposta: count() conta gli elementi presenti in un dataframe, nunique() conta il numero di unici, ossia dati che non si ripetono
# b) Quando useresti `size()` invece di `count()`? in base e voglio o meno considerare nel totale i valori Nan
# c) Perche conviene tenere i nomi colonna del report espliciti in `.agg`? per una più facile lettura e cosultazione
#
# Scrivi il tuo codice qui sotto:

path_file = os.path.join(os.path.dirname(__file__),"dati", "case.csv")
case = pd.read_csv(path_file)
case['costr_dopo_2000'] = case['anno_costruzione'] >= 2_000
report_case = case.groupby('citta').agg(
    pratiche_totali = ("id", "size"),
    metri_quadri_medi = ("metri_quadri", lambda x: x.mean().round(2)),
    quota_case_recenti = ("costr_dopo_2000", lambda x : f"{100*x.mean().round(2):.2f} %")
)

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
