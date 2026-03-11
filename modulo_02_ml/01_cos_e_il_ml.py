"""
============================================================================
MODULO 2 — CAPITOLO 01: Cos'e il Machine Learning
Da "analisi dati" a "previsione automatica"
============================================================================

Analogia pratica:
- Modulo 1: hai imparato a leggere report e tabelle.
- Modulo 2: costruisci un "assistente" che impara dai casi passati
  e propone una previsione su un caso nuovo.

Confronto web:
- JavaScript/PHP: regole scritte a mano con if/else
- Machine Learning: regole apprese dai dati
"""

import pandas as pd
import numpy as np
import os

# ==========================================================================
# QUIZ D'INGRESSO — Ripasso da Pandas (cap.09-10)
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "df['colonna'] restituisce un DataFrame."
#
# DOMANDA 2 — Prevedi l'output:
#   print(df[["a", "b"]].shape)
# Se df ha 30 righe, cosa stampa?
#
# DOMANDA 3 — Trova l'errore:
#   top = df[df["prezzo"] = 100]
#
# DOMANDA 4 — Definizione:
# Differenza tra `.loc` e `.iloc` in una frase.
#
# DOMANDA 5 — Completa:
#   righe = df.shape[___]
#   colonne = df.shape[___]
#

# ==========================================================================
# PARTE 1: Cos'e il Machine Learning (ML)
# ==========================================================================
#
# Machine Learning = il computer impara pattern dai dati storici
# e li usa per fare previsioni su dati nuovi.
#
# Esempio e-commerce:
# input: metri quadri, citta, anno casa
# output: prezzo stimato
#
# Non scrivi a mano tutte le regole:
# il modello le apprende dai dati.

print("\nPARTE 1 — Cos'e il ML\n")
print("ML = apprendere pattern dai dati per fare previsioni.")

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Scrivi un esempio reale (tuo dominio) di problema predittivo.
# 2) Scrivi input (feature) e output (target).
# 3) Spiega in 1 riga perche conviene ML invece di if/else fissi.


# ==========================================================================
# PARTE 2: Tipi principali di Machine Learning
# ==========================================================================
#
# 1) Supervisionato:
#    hai input + target noto (es. prezzo casa)
#
# 2) Non supervisionato:
#    non hai target, cerchi gruppi/pattern (es. segmenti clienti)
#
# 3) Reinforcement Learning:
#    agente che impara da ricompense/penalita.

print("\nPARTE 2 — Tipi di ML\n")
print("Supervisionato, non supervisionato, reinforcement.")

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# Classifica questi casi:
# a) Predire abbandono cliente (si/no)
# b) Raggruppare utenti per comportamento acquisto
# c) Agente che impara a giocare


# ==========================================================================
# PARTE 3: Dataset, Feature, Target (ponte con Pandas)
# ==========================================================================

percorso_case = os.path.join(os.path.dirname(__file__), "..", "modulo_01_python_dati", "dati", "case.csv")
case = pd.read_csv(percorso_case)

# Rinforzo mirato: Series vs DataFrame
print("\nRINFORZO — Series vs DataFrame")
print(type(case["prezzo_euro"]))             # Series
print(type(case[["prezzo_euro"]]))           # DataFrame

# Rinforzo mirato: shape su selezione colonne
print("\nRINFORZO — Shape selezione colonne")
print(case[["metri_quadri", "prezzo_euro"]].shape)

# Creiamo feature/target (concetto base ML)
X = case[["metri_quadri", "anno_costruzione", "distanza_centro_km"]]
y = case["prezzo_euro"]

print(f"\nFeature X shape: {X.shape}")
print(f"Target y shape: {y.shape}")

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# 1) Aggiungi `ha_garage` alle feature X.
# 2) Stampa shape nuova di X.
# 3) Scrivi in una riga: perche y e Series e non DataFrame?


# ==========================================================================
# PARTE 4: Rinforzo report con .agg (ponte M1 -> M2)
# ==========================================================================
#
# Nel lavoro reale di Machine Learning non fai solo modello:
# prima devi capire i dati con report sintetici.
# Il metodo .agg ti permette di costruire report leggibili e veloci.

print("\nPARTE 4 — Report con .agg\n")

case["is_centro"] = case["distanza_centro_km"] < 3
report_base = (
    case.groupby("citta", as_index=False).agg(
        pratiche_totali=("id", "count"),
        prezzo_medio=("prezzo_euro", "mean"),
        metri_quadri_medi=("metri_quadri", "mean"),
        quota_centro=("is_centro", "mean"),
    )
)
report_base["quota_centro"] = (report_base["quota_centro"] * 100).round(2)
print(report_base.sort_values("prezzo_medio", ascending=False).round(2))

# --- MINI-ESERCIZIO 4 — Rinforzo .agg ---
# 1) Aggiungi una colonna prezzo_al_mq = prezzo_euro / metri_quadri
# 2) Crea report per citta con .agg:
#    - pratiche_totali
#    - prezzo_massimo
#    - prezzo_minimo
#    - prezzo_medio_al_mq
# 3) Ordina per prezzo_massimo desc e stampa top 3


# ==========================================================================
# QUIZ DI VERIFICA — Prima degli esercizi
# ==========================================================================
#
# DOMANDA 1 — Vero/Falso:
# "Nel supervisionato il target e noto nel training."
#
# DOMANDA 2 — Completa:
# `X` contiene ______ ; `y` contiene ______
#
# DOMANDA 3 — Trova l'errore:
#   X = case["metri_quadri", "prezzo_euro"]
#
# DOMANDA 4 — Prevedi:
# Se X ha shape (30, 4), quante feature per campione ha?
#
# DOMANDA 5 — 💬 Spiega con parole tue:
# differenza pratica tra scrivere regole a mano e farle apprendere al modello.


# ==========================================================================
# ESERCIZI — Ora prova tu
# ==========================================================================
#
# ESERCIZIO 1 (Facile):
# Carica `case.csv` e identifica chiaramente:
# - feature candidate
# - target candidate
# Stampa shape e tipi (`type`) di entrambe.
#
# ESERCIZIO 2 (Medio):
# Crea 2 versioni di X:
# a) X_base con 3 feature
# b) X_plus con 5 feature
# Confronta shape e scrivi quale versione useresti e perche.
#
# ESERCIZIO 3 (🎯 [COLLOQUIO]):
# Spiega in 8-10 righe:
# - differenza regressione vs classificazione
# - un esempio reale per ciascuna
# - quale metrica useresti per valutarle
#
# ESERCIZIO 4 (🔧 [REFACTORING]):
# Riscrivi questo codice "brutto" in modo pulito:
# dati = pd.read_csv(...)
# a = dati[['metri_quadri','anno_costruzione','distanza_centro_km']]
# b = dati['prezzo_euro']
# print(a.shape); print(b.shape)
# (usa nomi espliciti + output leggibili)
#
# ESERCIZIO 5 (🔍 [DEBUG]):
# Correggi questo blocco e spiega l'errore:
# X = case["metri_quadri", "anno_costruzione"]
# y = case[["prezzo_euro"]]
# print(X.shape[1], y.shape[1])
#
# ESERCIZIO 6 (🔀 [INTERLEAVING] — Pandas + ML):
# Partendo da `case.csv`:
# 1) Crea `fascia_prezzo` con 3 classi: basso, medio, alto
# 2) Costruisci un report con `.agg` per `citta` e `fascia_prezzo`:
#    - pratiche_totali
#    - prezzo_medio
#    - metri_quadri_medi
# 3) Spiega in 3 righe come useresti questo report per scegliere feature utili.
#
# ESERCIZIO 7 (🧠 [RETRIEVAL] — riscrittura da memoria):
# Senza guardare il capitolo 09, riscrivi da zero:
# 1) creazione di una mask booleana
# 2) assegnazione condizionale con `.loc`
# 3) report con `.groupby(...).agg(...)`
# Usa sempre `case.csv` e salva il risultato in `dati/report_retrieval_agg.csv`.
#
# ESERCIZIO 8 (Rinforzo focus `.agg`):
# Crea un report "pronto recruiter" con colonne:
# - citta
# - pratiche_totali
# - prezzo_medio
# - metri_quadri_medi
# - quota_case_recenti (anno_costruzione >= 2000, in %)
# - varianza_prezzo
# Vincoli:
# - usare `.agg` in modo esplicito
# - ordinare per `quota_case_recenti` decrescente
# - stampare top 5 e salvare CSV in `dati/report_rinforzo_agg.csv`
#

# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — Predittore Prezzo Casa (fase 1)
# ==========================================================================
#
# Task:
# 1) Carica `case.csv`
# 2) Definisci X e y (scegli almeno 4 feature)
# 3) Stampa:
#    - numero campioni
#    - numero feature
#    - prime 3 righe di X
#    - primi 3 valori di y
# 4) Salva un mini report testuale in `dati/report_fase1_ml.txt`
#

# ==========================================================================
# SOLUZIONI — Solo dopo aver provato
# ==========================================================================
#
# --- RISPOSTE QUIZ D'INGRESSO ---
# 1) Falso (Series)
# 2) (30, 2)
# 3) Usa "=" invece di "=="
# 4) .loc = label, .iloc = posizione numerica
# 5) 0 e 1
#
# --- RISPOSTE QUIZ DI VERIFICA ---
# 1) Vero
# 2) feature, target
# 3) Serve doppia parentesi quadra: case[["metri_quadri", "prezzo_euro"]]
# 4) 4
# 5) Regole a mano = statiche; ML = pattern appresi e adattabili ai dati

