"""
============================================================================
MODULO 3 — CAPITOLO 08 (SEGNAPOSTO): CNN e Computer Vision
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.07 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.

⚠️ ULTIMO CAPITOLO PRIMA DI PASSARE AL DATASET REALE BUSTE PAGA.
   In questo capitolo si lavora SOLO su dataset pubblico low-stakes
   (Fashion-MNIST o CIFAR-10). Niente buste paga ancora.
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario cap.07 M3 (pytorch_intro).
#
# 2) AZIONE PROPEDEUTICA OBBLIGATORIA:
#    - PRIMA DI INIZIARE: aggiungere a `.gitignore` la riga `data/buste_*/`
#      anche se la cartella non esiste ancora (cosi' il cap.06 puo' partire
#      sicuro)
#    - decidere e documentare quale dataset pubblico usiamo (Fashion-MNIST
#      consigliato: 28x28 grayscale, leggero, scaricabile da torchvision)
#
# 3) STRUTTURA del file:
#    - Header + DoD
#    - Mappa
#    - Quiz d'ingresso (cerniera cap.07 M3: tensori, DataLoader, training loop)
#    - SEZIONE 1: immagini come tensori (H, W, C) e (N, C, H, W) - convenzione
#      PyTorch vs convenzione "intuitiva". Visualizzare un'immagine col plot.
#    - SEZIONE 2: convoluzione 2D - analogia "selettore CSS che cerca pattern"
#      o "filtro Photoshop". Esempio con kernel manuale (edge detection).
#    - SEZIONE 3: pooling (max-pool come "compressione che tiene il piu'
#      saliente"), feature maps come "attivazioni a vari livelli di astrazione"
#    - SEZIONE 4: una CNN piccola (2 conv + 2 pool + 1 dense) addestrata su
#      Fashion-MNIST. Plot loss + metriche per epoca.
#    - SEZIONE 5: visualizzare le feature maps del primo layer su un'immagine
#      di test (per "vedere" cosa ha imparato la rete)
#    - Quiz di verifica (1 Feynman: "perche' una CNN ha senso per immagini ma
#      una rete fully-connected fa fatica?")
#    - Esercizi: COLLOQUIO ("spiega CNN a un dev"), REFACTORING (semplificare
#      una CNN con troppi layer), DEBUG (loss che non scende = learning rate?),
#      RETRIEVAL (riscrivere training loop), INTERLEAVING (calcolo della shape
#      output di una conv2D — collega alla regola del Ponte cap.02!)
#    - 🏗️ PROGETTO INCREMENTALE: il PRODOTTO non si tocca ancora — qui solo
#      teoria CV su dataset pubblico. Documentare nel diario che la pipeline
#      reale parte dal cap.09 (transfer_learning).
#    - Soluzioni quiz
#
# 4) HARDWARE: training SEMPRE su Colab (anche Fashion-MNIST e' fattibile in
#    CPU ma vogliamo abituare al workflow GPU per i capitoli successivi).
#
# 5) DIARIO: M03_C08_cnn_computer_vision_sessione.md
# ============================================================================
