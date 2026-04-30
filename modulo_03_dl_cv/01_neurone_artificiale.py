"""
============================================================================
MODULO 3 — CAPITOLO 01 (SEGNAPOSTO): Neurone artificiale da zero
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.02 Ponte Matematico.
Qui sotto solo TODO MENTOR. Nessun codice operativo.
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO_CORSO.md (sezione "Stato Attuale", "Priorità Attive",
#    "Prossimo Capitolo") + diario chiusura cap.02 Ponte.
#
# 2) STRUTTURA OBBLIGATORIA del file (regole del corso):
#    - Header docstring con DoD (3-5 domande a cui sai rispondere a fine cap.)
#    - Mappa del capitolo (indice TOC come nei capitoli precedenti)
#    - Quiz d'ingresso (5-8 domande, 1 Feynman) — cerniera dal Ponte cap.01-02
#    - Eventuali blocchi # 🔁 RINFORZO MIRATO per lacune attive in CONTESTO
#    - SEZIONE 1: il neurone come "if con pesi" + analogia + codice NumPy
#    - SEZIONE 2: funzioni di attivazione (sigmoid, ReLU, tanh) + grafici
#    - SEZIONE 3: forward pass di UN neurone su una pratica del CSV M2
#    - Quiz di verifica (5-8 domande, 1 Feynman)
#    - Esercizi finali con i tag obbligatori:
#        🎯 [COLLOQUIO]   → "spiega cos'è un neurone come se fossi a colloquio"
#        🔧 [REFACTORING] → riscrivere un neurone "brutto" in stile pulito
#        🔍 [DEBUG]       → bug shape o dtype (autonomo, no scala progressiva)
#        🧠 [RETRIEVAL]   → riscrivere `coseno` o `norma` dal Ponte senza guardare
#        🔀 [INTERLEAVING] → mescola dot product (Ponte) + classificazione (M2)
#        🔄 [RECALL CROSS-MODULO] (OBBLIGATORIO per il cap.01 di un nuovo modulo,
#                                  regola 26): ricostruisci `X @ w + b` di Ponte
#                                  cap.02 e mostra che il neurone ne è un caso particolare
#    - Sezione 🏗️ PROGETTO INCREMENTALE: niente buste paga ancora; il task qui
#      è "trasformare la LogisticRegression del M2 cap.04 in un neurone scritto
#      a mano e verificare che dia risultati simili sulle stesse feature".
#    - Soluzioni quiz in fondo
#
# 3) PONTI MENTALI da riusare/registrare:
#    - "Neurone = dot product + bias + soglia" (web-dev: come una funzione che
#      somma input pesati e poi decide con un if morbido)
#    - "Sigmoid = soglia 0/1 ammorbidita" (rampa continua tra 0 e 1)
#    - "ReLU = max(0, x)" (un filtro che lascia passare solo i positivi)
#
# 4) HARDWARE: tutto su CPU locale, NumPy + Matplotlib. Niente PyTorch ancora.
#
# 5) DIARIO sessione: creare M03_C01_neurone_artificiale_sessione.md dal template.
#
# 6) TYPE HINT: usare np.ndarray (NON np.array), come da Pattern #25 chiuso nel
#    cap.02 Ponte.
#
# 7) STILE: niente virgole spurie a fine riga (Pattern #23), niente iloc con
#    etichette stringa (Pattern #24).
# ============================================================================
