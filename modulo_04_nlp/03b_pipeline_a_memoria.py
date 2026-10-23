# -----------------------------------------------------------------------------
# E6 · ⌨️ [PIPELINE A MEMORIA] — P1 → P2 → P3 senza guardare sopra
# -----------------------------------------------------------------------------
# Scrivi da zero, in fondo al file o su un foglio poi ricopiato, la pipeline
# completa su un mini-benchmark: 4 query con tipo atteso noto
#   ("busta paga con totale competenze e trattenute del mese" → busta_paga;
#    "redditi da lavoro dipendente e ritenute nella certificazione unica" → cu;
#    "estratto conto con elenco movimenti bonifici e saldo progressivo" → estratto_conto;
#    "atto notarile" → altro).
# Per ogni query: embedda → E @ q → top_k → decidi_con_soglia(0.70).
# Stampa una tabellina con, per ogni query: i 3 vicini (tipo + punteggio),
# precision@3 sul RANKING (la tua precision_su_k sui tipi dei 3 vicini, PRIMA
# della soglia), quanti vicini passano la soglia, esito ("risposta"/"non_lo_so").
# Poi rileggi la Sez. 2-4 e segna cosa avevi dimenticato (se qualcosa).
# Nota: le query 1-3 sono volutamente "piene di contesto" (quelle corte
# funzionano peggio, Sez. 5.3); la 4 è volutamente fuori corpus.

# =============================================================================
# SETUP — carica mappa e testi (riuso dal 02b)
# =============================================================================

import os
import joblib
import numpy as np
import pandas as pd

from numpy.typing import NDArray

from embed_utils import PERCORSO_VETTORI, carica_modello_frasi, embedda, carica_vettori

from testo_utils import coseno, tokenizza

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERCORSO_CSV = os.path.join(BASE_DIR, "dati", "note_documenti.csv")
PERCORSO_CONTRATTO = os.path.join(BASE_DIR, "dati", "contratti", "contratto.pkl")

note = pd.read_csv(PERCORSO_CSV)
testi = note["testo"].tolist()
E = carica_vettori()
modello = carica_modello_frasi()
