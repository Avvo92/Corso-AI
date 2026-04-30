"""
============================================================================
MODULO 3 — CAPITOLO 02 (SEGNAPOSTO): Reti neurali da zero
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.01 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario chiusura cap.01 M3.
#
# 2) FILO CONDUTTORE: una rete neurale = layer impilati, dove ogni layer e'
#    "X @ W + b + attivazione". Letteralmente la generalizzazione del cap.02
#    Ponte (layer Dense) ripetuta piu' volte.
#
# 3) STRUTTURA del file:
#    - Header + DoD (3-5 domande)
#    - Mappa
#    - Quiz d'ingresso (cerniera cap.01 M3: neurone, attivazioni)
#    - SEZIONE 1: dal neurone al layer (h neuroni in parallelo = matrice W)
#    - SEZIONE 2: rete a 2 layer (input -> hidden -> output) in NumPy puro
#    - SEZIONE 3: forward pass su batch di pratiche del CSV M2 (X (N, d) -> y_hat (N,))
#    - Quiz di verifica (1 Feynman: "spiega perche' due layer Dense con
#      attivazione fra di mezzo possono approssimare funzioni complesse")
#    - Esercizi: COLLOQUIO, REFACTORING, DEBUG, RETRIEVAL, INTERLEAVING
#    - 🏗️ PROGETTO INCREMENTALE: rete 2-layer NumPy che predice prob_alterato
#      sulle stesse feature M2 e si confronta con LogisticRegression cap.04 M2
#    - Soluzioni quiz
#
# 4) RINFORZI da inserire (in base allo stato di CONTESTO al momento):
#    - Pattern shape (n,), (1, n), (n, 1) - sempre chirurgico
#    - Eventuali lacune residue dal cap.02 Ponte (es. interpretazione W come
#      "h neuroni in parallelo")
#
# 5) TEORIA DA NON SALTARE:
#    - perche' serve l'attivazione fra layer (senza, e' ancora una sola
#      trasformazione lineare = regressione lineare con piu' output)
#    - inizializzazione pesi (random piccolo vs zero - perche' zero non funziona)
#    - intuizione "universal approximation theorem" senza formule
#
# 6) HARDWARE: ancora CPU + NumPy. PyTorch arriva al cap.04.
#
# 7) DIARIO: M03_C02_reti_neurali_sessione.md
# ============================================================================
