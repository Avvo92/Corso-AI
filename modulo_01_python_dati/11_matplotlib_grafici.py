"""
============================================================================
 MODULO 1 — ESERCIZIO 11: Grafici con Matplotlib
 Visualizzare i Dati — Perché "Vedere" è Capire
============================================================================

 TEORIA: Perché i Grafici Sono Fondamentali nell'AI?

 Pensa a quando fai il debug di un sito web: apri il DevTools del browser
 e GUARDI il layout, i margini, i colori. Non leggi solo il codice CSS —
 lo VEDI applicato.

 Con i dati è uguale. Puoi leggere numeri per ore, ma un grafico ti fa
 capire in 2 secondi cosa succede:
   - I dati crescono o calano? → Grafico a linea
   - Come sono distribuiti? → Istogramma
   - Ci sono correlazioni? → Scatter plot
   - Come si dividono le categorie? → Grafico a barre / torta

 Matplotlib è la libreria standard per i grafici in Python.
 Non è la più bella (ce ne sono di più moderne come Plotly), ma è
 la più usata e tutti gli esempi di AI la usano.

 ANALOGIA WEB:
   - Matplotlib = il CSS dei grafici. Controlli ogni dettaglio.
   - È come scrivere CSS puro: potente ma verboso.
   - Pandas ha metodi .plot() che usano Matplotlib sotto il cofano,
     come usare un framework CSS al posto del CSS puro.

============================================================================
"""

import matplotlib
matplotlib.use("Agg")  # Backend non interattivo (funziona senza finestra grafica)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Creiamo la cartella output per salvare i grafici
output_dir = os.path.join(os.path.dirname(__file__), "grafici")
os.makedirs(output_dir, exist_ok=True)

# ==========================================================================
# 🔁 RINFORZO MIRATO — Report "puliti" prima dei grafici
# ==========================================================================
#
# Errore tipico quando si passa da analisi a grafici:
# - confondere `size()` / `count()` / `nunique()` e quindi disegnare un grafico "sbagliato"
#
# Regola pratica (business):
# - **ordini totali**: quante righe ho nel gruppo -> `size()` (conta anche eventuali NaN)
# - **valori presenti in una colonna**: `count()` (NON conta i NaN in quella colonna)
# - **ordini unici / clienti unici**: `nunique()` (conteggia solo i distinti)
#
# Mini-check veloce su vendite:
# - `id_ordine` spesso si ripete (più righe per lo stesso ordine), quindi per gli "ordini"
#   quasi sempre vuoi `nunique()`, non `size()`.
#

# ==========================================================================
# PARTE 1: Il Primo Grafico — Grafico a Linea
# ==========================================================================

print("=== Creazione grafici ===")
print("I grafici vengono salvati nella cartella 'grafici/'")

# Dati di esempio: temperature giornaliere
giorni = list(range(1, 15))
temperature = [12, 14, 13, 16, 18, 20, 22, 21, 19, 17, 15, 16, 18, 20]

# Creare il grafico:
plt.figure(figsize=(10, 5))       # Dimensione: 10 pollici x 5 pollici
plt.plot(giorni, temperature,      # I dati
         color="blue",             # Colore della linea
         marker="o",               # Pallini sui punti
         linewidth=2,              # Spessore linea
         label="Temperatura")      # Etichetta per la legenda

plt.title("Temperature Giornaliere", fontsize=16)    # Titolo
plt.xlabel("Giorno del mese", fontsize=12)           # Etichetta asse X
plt.ylabel("Temperatura (°C)", fontsize=12)          # Etichetta asse Y
plt.grid(True, alpha=0.3)                            # Griglia (semi-trasparente)
plt.legend()                                          # Mostra la legenda

plt.savefig(os.path.join(output_dir, "01_grafico_linea.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 01_grafico_linea.png")

# ==========================================================================
# PARTE 2: Grafico a Barre
# ==========================================================================

# Dati: fatturato per categoria (dal nostro e-commerce)
categorie = ["Elettronica", "Abbigliamento", "Libri", "Accessori"]
fatturato = [1520.85, 359.82, 326.00, 260.00]
colori = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0"]

plt.figure(figsize=(8, 5))
barre = plt.bar(categorie, fatturato, color=colori, edgecolor="white", linewidth=2)

# Aggiungere i valori sopra ogni barra:
for barra, valore in zip(barre, fatturato):
    plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 20,
             f"{valore:.0f}€", ha="center", fontweight="bold")

plt.title("Fatturato per Categoria", fontsize=16)
plt.ylabel("Fatturato (€)", fontsize=12)
plt.ylim(0, max(fatturato) * 1.15)

plt.savefig(os.path.join(output_dir, "02_grafico_barre.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 02_grafico_barre.png")

# ==========================================================================
# PARTE 3: Istogramma — Distribuzione dei Dati
# ==========================================================================

# Un istogramma mostra COME i dati sono distribuiti.
# "Quante case costano tra 100k e 200k? Quante tra 200k e 300k?"

# Carichiamo il dataset case
percorso_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(percorso_case)

plt.figure(figsize=(10, 5))
plt.hist(case["prezzo_euro"], bins=10, color="#2196F3", edgecolor="white",
         alpha=0.8, label="Frequenza")
plt.axvline(case["prezzo_euro"].mean(), color="red", linestyle="--",
            linewidth=2, label=f"Media: {case['prezzo_euro'].mean():,.0f}€")

plt.title("Distribuzione Prezzi delle Case", fontsize=16)
plt.xlabel("Prezzo (€)", fontsize=12)
plt.ylabel("Numero di case", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3, axis="y")

plt.savefig(os.path.join(output_dir, "03_istogramma.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 03_istogramma.png")

# ==========================================================================
# PARTE 4: Scatter Plot — Correlazioni
# ==========================================================================

# Lo scatter plot è IL grafico per capire le correlazioni.
# "Se una casa ha più mq, costa di più?"

plt.figure(figsize=(10, 6))

# Coloriamo i punti per città:
citta_colori = {"Milano": "#2196F3", "Roma": "#F44336", "Napoli": "#FF9800",
                "Torino": "#4CAF50", "Firenze": "#9C27B0", "Bologna": "#795548"}

for citta in case["citta"].unique():
    dati_citta = case[case["citta"] == citta]
    plt.scatter(dati_citta["metri_quadri"], dati_citta["prezzo_euro"],
                color=citta_colori.get(citta, "gray"),
                label=citta, s=80, alpha=0.7, edgecolors="white")

# Linea di tendenza (regressione lineare semplice con NumPy):
coefficienti = np.polyfit(case["metri_quadri"], case["prezzo_euro"], 1)
x_linea = np.linspace(case["metri_quadri"].min(), case["metri_quadri"].max(), 100)
y_linea = np.polyval(coefficienti, x_linea)
plt.plot(x_linea, y_linea, color="red", linewidth=2, linestyle="--",
         label="Tendenza", alpha=0.7)

plt.title("Prezzo vs Metri Quadri (per Città)", fontsize=16)
plt.xlabel("Metri Quadri", fontsize=12)
plt.ylabel("Prezzo (€)", fontsize=12)
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)

plt.savefig(os.path.join(output_dir, "04_scatter_plot.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 04_scatter_plot.png")

# ==========================================================================
# PARTE 5: Grafici Multipli (Subplot)
# ==========================================================================

# Spesso vuoi mostrare più grafici insieme, come un "dashboard".
# Usi i subplot, che sono come un CSS Grid per i grafici.

fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # Griglia 2x2
fig.suptitle("Dashboard Immobiliare", fontsize=18, fontweight="bold")

# Grafico 1 (in alto a sinistra): Prezzo medio per città
prezzo_citta = case.groupby("citta")["prezzo_euro"].mean().sort_values(ascending=False)
axes[0, 0].barh(prezzo_citta.index, prezzo_citta.values, color="#2196F3")
axes[0, 0].set_title("Prezzo Medio per Città")
axes[0, 0].set_xlabel("Prezzo (€)")

# Grafico 2 (in alto a destra): Distribuzione mq
axes[0, 1].hist(case["metri_quadri"], bins=8, color="#4CAF50", edgecolor="white")
axes[0, 1].set_title("Distribuzione Metri Quadri")
axes[0, 1].set_xlabel("Metri Quadri")
axes[0, 1].set_ylabel("Frequenza")

# Grafico 3 (in basso a sinistra): Case per decade
case["decade"] = (case["anno_costruzione"] // 10) * 10
per_decade = case.groupby("decade").size()
axes[1, 0].bar(per_decade.index.astype(str), per_decade.values, color="#FF9800")
axes[1, 0].set_title("Case per Decade")
axes[1, 0].set_xlabel("Decade")
axes[1, 0].set_ylabel("Numero Case")
axes[1, 0].tick_params(axis="x", rotation=45)

# Grafico 4 (in basso a destra): Con/senza garage
garage_counts = case["ha_garage"].value_counts()
labels = ["Senza Garage", "Con Garage"]
axes[1, 1].pie(garage_counts.values, labels=labels, autopct="%1.0f%%",
               colors=["#F44336", "#4CAF50"], startangle=90)
axes[1, 1].set_title("Garage")

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "05_dashboard.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 05_dashboard.png")

# ==========================================================================
# PARTE 6: Grafici Direttamente da Pandas
# ==========================================================================

# Pandas ha metodi .plot() integrati che semplificano tutto.
# Usano Matplotlib sotto il cofano, ma con meno codice.

# Vendite per categoria (grafico a barre):
percorso_vendite = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(percorso_vendite)
vendite["fatturato"] = vendite["prezzo"].astype(float) * vendite["quantita"].astype(int)

# 🔁 RINFORZO MIRATO — "preparo il DataFrame GIUSTO" per il grafico
#
# Quando fai un grafico, l'errore più comune non è Matplotlib: è l'aggregazione.
# Qui sotto costruiamo 2 serie corrette, pronte da plottare:
# - fatturato per giorno (line chart)
# - ordini UNICI per città (bar chart)
#
vendite["data"] = pd.to_datetime(vendite["data"])
fatturato_per_giorno = vendite.groupby("data")["fatturato"].sum().sort_index()
ordini_unici_per_citta = vendite.groupby("citta")["id_ordine"].nunique().sort_values(ascending=False)
print("\nRINFORZO report per grafici:")
print("Fatturato per giorno (prime 3 righe):")
print(fatturato_per_giorno.head(3))
print("\nOrdini UNICI per città:")
print(ordini_unici_per_citta)

fig, ax = plt.subplots(figsize=(10, 5))
vendite.groupby("categoria")["fatturato"].sum().sort_values().plot(
    kind="barh", ax=ax, color="#673AB7"
)
ax.set_title("Fatturato per Categoria (con Pandas .plot())", fontsize=14)
ax.set_xlabel("Fatturato (€)")

plt.savefig(os.path.join(output_dir, "06_pandas_plot.png"), dpi=100, bbox_inches="tight")
plt.close()
print("Salvato: 06_pandas_plot.png")

print(f"\nTutti i grafici salvati nella cartella: {output_dir}")
print("Aprili con un qualsiasi visualizzatore di immagini per vederli!")


# ==========================================================================
# 🔁 RINFORZO MIRATO — `idxmax()` vs `max()` (utile anche nei grafici)
# ==========================================================================
#
# - `.max()` ti dà IL VALORE massimo
# - `.idxmax()` ti dà L'INDICE (es. la data o la città) dove quel massimo avviene
#
giorno_top = fatturato_per_giorno.idxmax()
valore_top = fatturato_per_giorno.max()
print("\nRINFORZO idxmax/max:")
print(f"Giorno col fatturato top: {giorno_top.date()}")
print(f"Valore fatturato top: {valore_top:,.2f}€\n")


# ==========================================================================
# --- MINI-ESERCIZIO EXTRA (prima degli esercizi ufficiali) — Prova subito! ---
# ==========================================================================
#
# 1) Crea `report_citta` con `.groupby('citta').agg(...)` che contenga:
#    - ordini_unici: nunique su id_ordine
#    - fatturato_totale: sum su fatturato
# 2) Aggiungi `ticket_medio = fatturato_totale / ordini_unici`
# 3) Ordina per fatturato_totale desc
# 4) Stampa le prime 3 righe del report
#
# Scrivi qui sotto:
path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
ordini = pd.read_csv(path_file)
ordini['fatturato_totale'] = ordini['prezzo'] * ordini['quantita']
print(ordini)
report_citta = ordini.groupby('citta').agg(
  ordini_unici = ('id_ordine', 'nunique'),
  fatturato = ('fatturato_totale', 'sum')
)
report_citta['ticket_medio'] = (report_citta['fatturato'] / report_citta['ordini_unici']).round(2)
report_citta = report_citta.sort_values(by='fatturato', ascending=False)
print(f"{report_citta.head(3)}\n")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Crea un grafico a linea che mostra il fatturato per giorno del dataset
# vendite. Aggiungi titolo, etichette assi e griglia.
# Salva come "es1_fatturato_giorno.png" nella cartella grafici.
#
# Scrivi il tuo codice qui sotto:
fatturato_per_giorno = ordini.groupby('data').agg(
  fatturato = ("fatturato_totale", "sum")
)
print(fatturato_per_giorno)
fig, ax = plt.subplots(figsize=(10, 5))
fatturato_per_giorno["fatturato"].plot(
    kind="line", ax=ax, color="#673AB7"
)
ax.set_title("Fatturato per Giorno", fontsize=14)
ax.set_xlabel("Gionro")
ax.set_ylabel("Fatturato")
ax.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, "es1_fatturato_giorno.png"), dpi=100, bbox_inches="tight")
plt.close()

# ESERCIZIO 2 (Medio):
# Crea un grafico a barre che confronta il prezzo medio delle case
# CON e SENZA garage, per ogni città (barre affiancate).

path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)

# prezzo al metro quadro
case["prezzo_mq"] = case["prezzo_euro"] / case["metri_quadri"]

# media €/mq per città e presenza garage
# -> trasformo in tabella "wide": righe=città, colonne=[False, True]
tab = (
    case.groupby(["citta", "ha_garage"])["prezzo_mq"]
    .mean()
    .round(2)
    .unstack("ha_garage")
)

# assicuro l'ordine colonne: senza garage (False) poi con garage (True)
tab = tab.reindex(columns=[False, True])

print(tab)

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Prezzo medio €/mq per città (con/senza garage)", fontsize=14)
ax.set_xlabel("Città")
ax.set_ylabel("Prezzo medio €/mq")
ax.grid(True, alpha=0.3)

# posizioni delle barre (una posizione per città)
x = np.arange(len(tab.index))
width = 0.4

# due barre affiancate: sinistra=senza garage, destra=con garage
ax.bar(x - width / 2, tab[False].values, width=width, label="Senza garage", color="#03A9F4")
ax.bar(x + width / 2, tab[True].values,  width=width, label="Con garage",  color="#FF9800")

ax.set_xticks(x)
ax.set_xticklabels(tab.index, rotation=30, ha="right")
ax.legend()
fig.tight_layout()

plt.savefig(os.path.join(output_dir, "es2_presenza_garage.png"), dpi=100, bbox_inches="tight")
plt.close()


# ESERCIZIO 3 (Medio):
# Crea uno scatter plot che mostra la relazione tra:
# - Asse X: distanza dal centro (km)
# - Asse Y: prezzo della casa
# Colora i punti in base al numero di stanze (usa un colormap).
# Aggiungi una colorbar.
# Suggerimento: plt.scatter(..., c=case["num_stanze"], cmap="viridis")
#
# Scrivi il tuo codice qui sotto:
plt.scatter(
  x = case["metri_quadri"],
  y = case["prezzo_euro"],
  c = case["num_stanze"],
  cmap = "viridis",
  s = 80,
  alpha = 0.8,
  edgecolors = "white"
  )
plt.xlabel("Metri quadri")
plt.ylabel("Prezzo euro")
plt.title("Scatter: metri quadri vs prezzo")
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, "es3_rapporto_prezzo_mq.png"), dpi=100, bbox_inches="tight")
plt.close()

# ==========================================================================
# ESERCIZI GUIDATI EXTRA (RINFORZO) — Difficoltà crescente
# ==========================================================================
#
# Nota: questi esercizi servono a fissare i concetti del capitolo 11.
# Strategia: prima costruisci il "report giusto" con Pandas (groupby/agg),
# poi lo plotti con Matplotlib (subplots/ax.*).
#
# Ponte mentale Web:
# - Pandas `groupby().agg()` = una query SQL `GROUP BY ... SELECT AVG/SUM/COUNT`
# - Matplotlib `fig, ax = plt.subplots()` = creare il "container" (come un <div>)
#   e poi disegnare dentro (come aggiungere elementi UI + stile).
#

# --- ESERCIZIO EXTRA 3A (Facile) — Linea + media mobile ---
# Obiettivo: sul dataset vendite, disegna:
# - linea del fatturato giornaliero
# - linea della media mobile a 7 giorni (rolling mean)
#
# Hint (Pandas): rolling è come fare una "finestra" di 7 giorni.
# In JS sarebbe come calcolare una media su una slice dell'array ad ogni i.
#
# Requisiti:
# - titolo, label assi, griglia, legenda
# - salva: "extra3a_linea_media_mobile.png"
#
# Scrivi qui sotto:
# vendite = pd.read_csv(...)
# vendite["data"] = pd.to_datetime(...)
# fatt = vendite.groupby("data")["fatturato"].sum().sort_index()
# fatt_mm7 = fatt.rolling(7).mean()
# fig, ax = plt.subplots(...)
# ax.plot(...)
# ax.plot(...)
# plt.savefig(...)


path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(path_file)
vendite['data'] = pd.to_datetime(vendite['data'])
vendite['fatturato'] = vendite['prezzo'] * vendite['quantita']
report_fatturato = vendite.groupby('data')['fatturato'].sum().sort_index()
report_fatturato_mm7 = report_fatturato.rolling(7).mean()

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_title("Media mobile 7 giorni fatturato", fontsize=14)
ax.set_xlabel("Giorno")
ax.set_ylabel("Media mobile fatturato")
ax.grid(True, alpha=0.3)

usable_fatturato_mm7 = report_fatturato_mm7.iloc[6:]

len_x = np.arange(len(usable_fatturato_mm7))
bar_width = 0.4

ax.bar(len_x, usable_fatturato_mm7.values, width=bar_width )
ax.set_xticks(len_x)
ax.set_xticklabels(usable_fatturato_mm7.index.strftime("%Y-%m-%d"), rotation=30, ha="right")
fig.tight_layout()

plt.savefig(os.path.join(output_dir, "es3a_report_media_mobile.png"), dpi=100, bbox_inches="tight")
plt.close()


# --- ESERCIZIO EXTRA 3B (Facile/Medio) — Barre ordinate + etichette valori ---
# Obiettivo: barre orizzontali (barh) dei TOP 8 prodotti per fatturato.
#
# Focus concetto: scegliere l'aggregazione GIUSTA.
# - "fatturato per prodotto" = sum del fatturato
#
# Requisiti:
# - ordina decrescente, prendi top 8
# - usa `ax.barh(...)`
# - scrivi il valore su ogni barra (con un for sulle barre)
# - salva: "extra3b_top_prodotti_barh.png"
#
# Scrivi qui sotto:
path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(path_file)
vendite['fatturato'] = vendite['prezzo'] * vendite['quantita']
top_vendite = vendite.groupby('prodotto')['fatturato'].sum().sort_values(ascending=False).head(8).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(18, 10))
bars = ax.barh(top_vendite.index, top_vendite.values)
ax.set_title("Fatturato top 8 prodotti", fontsize=14)
ax.set_xlabel("fatturato totale")
ax.set_ylabel("prodotti")
ax.grid(True, alpha=0.3)

for bar in bars:
  w = bar.get_width()
  ax.text(w + 5, bar.get_y() + bar.get_height() / 2, f"{w:.0f}€", va="center")

fig.tight_layout()

plt.savefig(os.path.join(output_dir, "es3b_top_8_prodotti.png"), dpi=100, bbox_inches="tight")
plt.close()


# --- ESERCIZIO EXTRA 3C (Medio) — Scatter + soglia (outlier) ---
# Obiettivo: scatter "metri_quadri" vs "prezzo_euro" (case.csv) e evidenzia
# le case sopra una soglia di prezzo (es. > 400000) con un colore diverso.
#
# Ponte JS/PHP: è come fare un if dentro un loop e pushare su 2 array diversi.
# In Pandas lo fai con una mask booleana.
#
# Requisiti:
# - 2 scatter: uno per "normali", uno per "sopra soglia"
# - legenda, griglia
# - salva: "extra3c_scatter_soglia.png"
#
# Scrivi qui sotto:
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)

soglia = 400000
mask_outlier = case["prezzo_euro"] > soglia

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_title("Scatter: metri quadri vs prezzo (soglia outlier)", fontsize=14)
ax.set_xlabel("Metri quadri")
ax.set_ylabel("Prezzo euro")
ax.grid(True, alpha=0.3)

# Case normali
ax.scatter(
    x=case.loc[~mask_outlier, "metri_quadri"],
    y=case.loc[~mask_outlier, "prezzo_euro"],
    s=80,
    alpha=0.8,
    color="#4CAF50",
    edgecolors="white",
    label=f"Normali (<= {soglia:,}€)"
)

# Case sopra soglia
ax.scatter(
    x=case.loc[mask_outlier, "metri_quadri"],
    y=case.loc[mask_outlier, "prezzo_euro"],
    s=110,
    alpha=0.9,
    color="#F44336",
    edgecolors="black",
    label=f"Sopra soglia (> {soglia:,}€)"
)

ax.legend()
fig.tight_layout()

plt.savefig(os.path.join(output_dir, "extra3c_scatter_soglia.png"), dpi=100, bbox_inches="tight")
plt.close()


# 🎯 [COLLOQUIO] ESERCIZIO EXTRA 3D (Medio/Difficile) — Groupby doppio + barre affiancate (MultiIndex) ---
# Domanda tipica: "Mi fai un grafico che confronta due categorie per ogni gruppo?"
#
# Obiettivo: per ogni città, confronta:
# - prezzo medio €/mq per (ha_garage == False)
# - prezzo medio €/mq per (ha_garage == True)
#
# Vincolo: DEVI passare da una struttura "lunga" (MultiIndex) a una "wide".
# - `unstack()` (oppure `pivot_table`) ti porta `ha_garage` nelle colonne.
#
# Requisiti:
# - 2 chiamate `ax.bar(...)` con posizioni sfalsate
# - tick X = città, rotazione etichette
# - salva: "extra3d_barre_affiancate_garage.png"
#
# Scrivi qui sotto:

case['prezzo_mq'] = case['prezzo_euro'] / case['metri_quadri']
report_citta = case.groupby(['citta', 'ha_garage'])['prezzo_mq'].mean().round(2).unstack('ha_garage')
report_citta['media_reale'] = report_citta.mean(axis=1).round(2)
report_citta = report_citta.sort_values(by="media_reale", ascending=False)
report_citta = report_citta.reindex(columns=[False, True])
print(f"\n\n{report_citta}")

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Prezzo medio €/mq per città (con/senza garage)", fontsize=14)
ax.set_xlabel("Città")
ax.set_ylabel("Prezzo medio €/mq")
ax.grid(True, alpha=0.3)
report_len = np.arange(len(report_citta.index))
width = 0.3
ax.bar(report_len - width / 2, report_citta[False].values, width=width, label="senza garage", color="#03A9F4") 
ax.bar(report_len + width / 2, report_citta[True].values, width=width, label="con garage", color="#FF9800")

ax.set_xticks(report_len)
ax.set_xticklabels(report_citta.index, rotation=30, ha="right")
ax.legend()
fig.tight_layout()

plt.savefig(os.path.join(output_dir, "extra3d_barre_affiancate_garage.png"), dpi=100, bbox_inches="tight")
plt.close()

# 🔧 [REFACTORING] ESERCIZIO EXTRA 3E (Difficile) — Da pyplot a OO (fig, ax) ---
# Ti lascio qui sotto un codice "pyplot style" funzionante ma poco scalabile.
# Refactor: riscrivilo in stile object-oriented usando `fig, ax = plt.subplots()`
# e SOLO metodi `ax.*` (niente plt.title/plt.grid/plt.xlabel...).
#
# Codice da refactorare (NON modificarlo: riscrivilo sotto):
# plt.figure(figsize=(10, 4))
# plt.plot(fatturato_per_giorno.index, fatturato_per_giorno.values, color="blue")
# plt.title("Fatturato per giorno")
# plt.xlabel("Data")
# plt.ylabel("€")
# plt.grid(True, alpha=0.3)
# plt.savefig(os.path.join(output_dir, "extra3e_refactor_oo.png"), dpi=100, bbox_inches="tight")
# plt.close()
#
# Scrivi qui sotto la versione refactor:
path_file = os.path.join(os.path.dirname(__file__), "dati", "vendite_ecommerce.csv")
vendite = pd.read_csv(path_file)
vendite['data'] = pd.to_datetime(vendite['data'])
vendite['fatturato'] = vendite['prezzo'] * vendite['quantita']
fatturato_giorno = vendite.groupby('data')['fatturato'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title("Fatturato in base al giorno", fontsize=14)
ax.set_xlabel("Data")
ax.set_ylabel("Fatturato €")
ax.grid(True, alpha=0.3)
fatturato_giorno.plot(kind="line", ax=ax, color="#673AB7")
plt.savefig(os.path.join(output_dir, "extra3e_refactor_oo.png"), dpi=100, bbox_inches="tight")
plt.close()



# 🔀 [INTERLEAVING] ESERCIZIO EXTRA 3F (Difficile) — 2 grafici, 1 figura (subplots) ---
# Obiettivo: in una figura 1x2 (una riga, due colonne), metti:
# - sinistra: istogramma di `prezzo_euro` (case.csv) + linea della media
# - destra: pie chart con percentuali case con/senza garage
#
# Requisiti:
# - `fig, axes = plt.subplots(1, 2, ...)`
# - titolo generale `fig.suptitle(...)`
# - salva: "extra3f_istogramma_pie.png"
#
# Passi consigliati (senza soluzione):
# 1) Carica `case.csv` e identifica le 2 serie che ti servono:
#    - prezzi: `prezzo_euro`
#    - composizione garage: conteggi di `ha_garage`
# 2) Crea la figura 1x2:
#    - `axes[0]` = pannello sinistro
#    - `axes[1]` = pannello destro
# 3) Pannello sinistro:
#    - disegna l'istogramma dei prezzi
#    - calcola la media dei prezzi e aggiungi una linea verticale
#    - aggiungi titolo subplot + label assi + griglia
# 4) Pannello destro:
#    - calcola i conteggi di case con/senza garage
#    - disegna la pie chart con etichette e percentuali
#    - aggiungi titolo subplot
# 5) Rifinitura:
#    - `fig.suptitle(...)`
#    - `fig.tight_layout(...)` (lascia spazio al titolo generale)
#    - salva e chiudi figura
#
# Checklist veloce:
# - [ ] 2 subplot nella stessa figura
# - [ ] istogramma + linea media a sinistra
# - [ ] pie con percentuali a destra
# - [ ] titolo generale presente
# - [ ] nome file corretto
#
# Errori tipici da evitare:
# - usare `plt.*` senza specificare il subplot giusto (`axes[0]` / `axes[1]`)
# - passare la colonna raw `ha_garage` alla pie senza prima fare i conteggi
# - dimenticare spazio per `suptitle` (titolo tagliato nel PNG)
#
# Scrivi qui sotto:
path_file = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file)
media = case['prezzo_euro'].mean()
width = 0.4
fig, axes = plt.subplots(1, 2, figsize=(25, 8))
bars_axes_0 = axes[0].hist(case['prezzo_euro'].values, bins=7, density=True, color="#03A9F4")
axes[0].set_title("Prezzo case", fontsize=12)
axes[0].set_xlabel("Prezzo")
axes[0].set_ylabel("Numero case")
axes[0].axvline(media, color="red", linestyle="--", linewidth=2, label="Media")
axes[0].legend()
  
  
plt.savefig(os.path.join(output_dir, "extra3f_istogramma_pie.png"), dpi=100, bbox_inches="tight")
plt.close()


# 🧠 [RETRIEVAL] ESERCIZIO EXTRA 3G (Sfida) — Riscrivi da memoria (Pandas report → plot) ---
# Senza guardare il codice sopra nel file, riscrivi DA ZERO:
# - un report `ordini_unici_per_citta` corretto (usa `nunique` su id_ordine)
# - e un grafico a barre (top 6 città) salvato come "extra3g_retrieval_top_citta.png"
#
# Se ti blocchi: prima stampa il report, poi plotti.
#
# Scrivi qui sotto:
# ...


# ESERCIZIO 4 (Sfida — Dashboard Completa):
# Crea una dashboard 2x3 (2 righe, 3 colonne) che riassuma
# TUTTO il dataset vendite_ecommerce.csv:
# 1. Fatturato per giorno (linea)
# 2. Ordini per città (barre)
# 3. Distribuzione prezzi (istogramma)
# 4. Metodi pagamento (torta)
# 5. Top 5 prodotti per fatturato (barre orizzontali)
# 6. Quantità vendute per categoria (barre)
# Salva come "es4_dashboard_completa.png"
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# vendite["data"] = pd.to_datetime(vendite["data"])
# fatt_giorno = vendite.groupby("data")["fatturato"].sum()
# plt.figure(figsize=(10, 5))
# plt.plot(fatt_giorno.index, fatt_giorno.values, marker="o", color="#2196F3")
# plt.title("Fatturato Giornaliero")
# plt.xlabel("Data")
# plt.ylabel("Fatturato (€)")
# plt.grid(True, alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig(os.path.join(output_dir, "es1_fatturato_giorno.png"), dpi=100)
# plt.close()

# --- SOLUZIONE ESERCIZIO 3 ---
# plt.figure(figsize=(10, 6))
# scatter = plt.scatter(case["distanza_centro_km"], case["prezzo_euro"],
#                       c=case["num_stanze"], cmap="viridis", s=80, edgecolors="white")
# plt.colorbar(scatter, label="Numero Stanze")
# plt.title("Distanza vs Prezzo (colorato per Num. Stanze)")
# plt.xlabel("Distanza dal Centro (km)")
# plt.ylabel("Prezzo (€)")
# plt.grid(True, alpha=0.3)
# plt.savefig(os.path.join(output_dir, "es3_scatter_stanze.png"), dpi=100, bbox_inches="tight")
# plt.close()
