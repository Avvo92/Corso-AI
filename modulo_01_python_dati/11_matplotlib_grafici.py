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
# Suggerimento: usa due chiamate plt.bar() con posizioni leggermente diverse.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio):
# Crea uno scatter plot che mostra la relazione tra:
# - Asse X: distanza dal centro (km)
# - Asse Y: prezzo della casa
# Colora i punti in base al numero di stanze (usa un colormap).
# Aggiungi una colorbar.
# Suggerimento: plt.scatter(..., c=case["num_stanze"], cmap="viridis")
#
# Scrivi il tuo codice qui sotto:
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
