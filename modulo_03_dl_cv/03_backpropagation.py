"""
============================================================================
MODULO 3 — CAPITOLO 03 (SEGNAPOSTO): Backpropagation e training
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.02 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.

⚠️⚠️ CAPITOLO PIU' TOSTO DEL MODULO (atteso 9/10 di difficolta').
    Andare LENTI, tanti grafici, ogni concetto tradotto in codice prima della formula.
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario cap.02 M3.
#
# 2) APPROCCIO DIDATTICO (Regola 21 — obbligatoria qui):
#    sequenza analogia -> codice -> grafico -> formula in parole.
#    NIENTE LaTeX, niente notazione compressa.
#
# 3) ANALOGIE CHIAVE (registrare quelle che funzionano nei Ponti Mentali):
#    - "Loss = quanto la previsione e' lontana dalla verita'" (errore in metri,
#      non in concetti astratti)
#    - "Gradiente = vettore che dice 'in che direzione aumenta la loss'"
#    - "Discesa del gradiente = scendere una collina al buio sentendo la pendenza
#      sotto i piedi"
#    - "Learning rate = quanto e' grande il passo che fai in quella direzione"
#    - "Backprop = GPS che, dopo aver fatto la strada sbagliata (forward), ti
#      dice di quanto sterzare a ogni incrocio (layer)"
#
# 4) STRUTTURA del file:
#    - Header + DoD esteso (5 domande, perche' qui si gioca il modulo)
#    - Mappa
#    - Quiz d'ingresso (cerniera: rete da cap.02 M3)
#    - SEZIONE 1: derivata come pendenza (1 variabile, plot Matplotlib)
#    - SEZIONE 2: gradiente come "vettore di derivate" (multivariato)
#    - SEZIONE 3: chain rule "a parole" + esempio numerico minimale
#    - SEZIONE 4: discesa del gradiente su una funzione semplice (paraboloide)
#      - implementare gradient descent a mano + plot loss vs iterazioni
#      - effetto del learning rate (troppo basso, troppo alto, giusto)
#    - SEZIONE 5: backprop su una rete 2-layer del cap.02 M3 (NumPy puro,
#      derivate a mano fatte passo passo)
#    - SEZIONE 6: training loop completo (loop forward -> loss -> backward ->
#      update pesi) + plot della loss che cala
#    - Quiz di verifica (1 Feynman: "spiega backpropagation a un dev senza
#      usare le parole 'gradiente', 'derivata', 'chain rule'")
#    - Esercizi: COLLOQUIO ("spiega backprop in 2 minuti"), REFACTORING,
#      DEBUG (gradient explosion / vanishing), RETRIEVAL, INTERLEAVING
#    - 🏗️ PROGETTO INCREMENTALE: la rete 2-layer del cap.02 M3 ora si addestra
#      sul CSV M2 e batte la baseline LogisticRegression del cap.04 M2
#    - Soluzioni quiz
#
# 5) DIFFICOLTA' GESTIONE:
#    - se lo studente arriva a meta' capitolo gia' bloccato: fare un mini-recap
#      in 1 sessione dedicata, NON proseguire.
#    - tenere visibili a margine le SHAPE di ogni quantita' (X, W1, W2, dW1,
#      dW2, dz1, dz2): meta' dei bug del backprop sono shape mismatch.
#
# 6) HARDWARE: ancora CPU + NumPy. Niente PyTorch (lo studente DEVE vedere
#    cosa c'e' sotto, prima che PyTorch lo nasconda).
#
# 7) DIARIO: M03_C03_backpropagation_sessione.md (sara' lungo, prevedere
#    multiple sessioni di lavoro nel diario)
# ============================================================================
