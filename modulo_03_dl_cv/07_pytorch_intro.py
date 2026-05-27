"""
============================================================================
MODULO 3 — CAPITOLO 07 (SEGNAPOSTO): PyTorch — primo contatto + training su Colab
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.06 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.

⚠️ PRIMO CAMBIO DI PIATTAFORMA: da qui in poi training su Google Colab (GPU).
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario cap.06 M3 (backprop_training).
#
# 2) PRE-REQUISITI OPERATIVI (DA PREPARARE PRIMA DI INIZIARE IL CAPITOLO):
#    - notebook Google Colab template con torch + torchvision pre-installati
#    - test "torch.cuda.is_available()" funzionante
#    - documentare in CONTESTO_CORSO.md la procedura "salva su Drive ->
#      scarica pesi modello in locale"
#    - aggiornare requirements.txt con: torch, torchvision, gradio (commentati
#      finche' non si arriva al cap.07)
#
# 3) FILO CONDUTTORE: PyTorch e' "NumPy con autograd e GPU".
#    Ogni concetto si introduce facendo prima il parallelo NumPy.
#
# 4) STRUTTURA del file:
#    - Header + DoD
#    - Mappa
#    - Quiz d'ingresso (cerniera cap.06 M3: backprop_training a mano)
#    - SEZIONE 1: tensori PyTorch vs ndarray NumPy (creazione, shape, dtype,
#      device CPU/GPU)
#    - SEZIONE 2: autograd — il "tape" che traccia le operazioni e calcola
#      le derivate da solo (CONFRONTO: nel cap.04+05+06 le derivavi a mano)
#    - SEZIONE 3: nn.Module, nn.Linear (= il layer Dense del Ponte cap.02!),
#      attivazioni come moduli
#    - SEZIONE 4: Dataset e DataLoader (perche' batch + shuffle)
#    - SEZIONE 5: training loop standard PyTorch (zero_grad / forward / loss /
#      backward / step) + tensorboard o solo matplotlib per la loss
#    - SEZIONE 6: salvare/caricare pesi (state_dict)
#    - Quiz di verifica (1 Feynman: "perche' DataLoader e' un wrapper attorno
#      a un Dataset e non solo una lista?")
#    - Esercizi: COLLOQUIO, REFACTORING (riscrivere training loop manuale in
#      forma PyTorch), DEBUG (device mismatch, NaN nella loss), RETRIEVAL,
#      INTERLEAVING (caricare il CSV M2 in un Dataset PyTorch custom)
#    - 🏗️ PROGETTO INCREMENTALE: addestrare la stessa rete del cap.06 M3 con
#      PyTorch su Colab; confrontare tempi (CPU NumPy vs GPU PyTorch) e
#      verificare metrica di test simile o migliore
#    - Soluzioni quiz
#
# 5) WORKFLOW Colab da documentare nel capitolo:
#    - "Sviluppo codice in Cursor, lo copio in una cella Colab"
#    - "Eseguo il training su GPU"
#    - "Salvo i pesi su Drive, scarico in locale"
#    - "Riapro il modello in Cursor con torch.load() per inferenza CPU"
#
# 6) DIARIO: M03_C07_pytorch_intro_sessione.md
# ============================================================================
