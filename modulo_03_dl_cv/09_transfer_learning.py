"""
============================================================================
MODULO 3 — CAPITOLO 09 (SEGNAPOSTO): Transfer learning + dataset reale buste paga
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.08 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.

⚠️ INGRESSO DEL DATASET REALE: questo e' il capitolo dove si introducono le
   buste paga ANONIMIZZATE. Vincoli privacy/GDPR strettamente rispettati.
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario cap.08 M3 (cnn) + sezione "Computer Vision nel
#    Prodotto" di CONTESTO_CORSO.md (decisione 30/04/2026 — vincoli privacy)
#    + sezione 10 di APPUNTI_APPLICATIVO.md.
#
# 2) AZIONI PROPEDEUTICHE OBBLIGATORIE (verificare PRIMA di iniziare):
#    [ ] `.gitignore` ha gia' `data/buste_*/` (regola di sicurezza)
#    [ ] cartelle locali create: `data/buste_originali/`, `data/buste_anonimizzate/`,
#        `data/altro/` (ognuna ignorata da git)
#    [ ] dataset "altro" raccolto (~200 immagini da dataset pubblici: fatture,
#        contratti, foto generiche). Suggerimenti: Document Image Dataset,
#        Tobacco-3482, IIT-CDIP subset, immagini ImageNet random per il "non documento"
#    [ ] script di anonimizzazione `anonimizza_buste.py` (stand-alone, fuori
#        dal capitolo) testato su 2-3 buste paga prima di processare tutte
#
# 3) STRUTTURA del file:
#    - Header + DoD
#    - Mappa
#    - Quiz d'ingresso (cerniera cap.08 M3: CNN, feature maps)
#    - SEZIONE PRIVACY (dedicata): perche' anonimizzazione PRIMA del training,
#      cosa succede se la salti (incidente), cosa NON va anonimizzato (layout
#      grafico, font generale = informazioni che SERVONO al modello)
#    - SEZIONE 1: cosa significa "transfer learning" (analogia: usare
#      manodopera specializzata di un altro cantiere invece di assumere da zero)
#    - SEZIONE 2: anatomia di ResNet18/50 - backbone (feature extractor) +
#      classifier head. Perche' "freezing" del backbone funziona.
#    - SEZIONE 3: torchvision.models, caricare pesi pre-addestrati ImageNet,
#      sostituire l'ultimo layer con un classificatore binario
#    - SEZIONE 4: data augmentation (rotazioni, crop, flip) per piccoli dataset
#      come il nostro
#    - SEZIONE 5: addestrare ResNet18 fine-tuned su busta-paga-vs-altro
#      (200+200 immagini); split train/val/test (es. 70/15/15) STRATIFICATO
#    - SEZIONE 6: valutazione con metriche dal cap.04 M2 (precision, recall,
#      F1, confusion matrix) — riusare codice gia' scritto
#    - Quiz di verifica (1 Feynman: "perche' funziona il transfer learning su
#      un dataset di documenti se ImageNet contiene foto di gatti e cani?")
#    - Esercizi: COLLOQUIO ("transfer learning vs training from scratch"),
#      REFACTORING, DEBUG (overfitting con 200 immagini = molto probabile),
#      RETRIEVAL (recall metrica giusta dal M2 cap.04),
#      INTERLEAVING (calcolare manualmente la dimensione output di ResNet
#      backbone per scegliere dim del classifier head)
#    - 🏗️ PROGETTO INCREMENTALE: la pipeline visiva del prodotto comincia qui.
#      Output: modello fine-tuned salvato (state_dict), pronto per Gradio.
#    - Soluzioni quiz
#
# 4) HARDWARE: training su Colab (obbligatorio - 200+200 immagini con ResNet18
#    su CPU sarebbe lentissimo).
#
# 5) DIARIO: M03_C09_transfer_learning_sessione.md
#
# 6) NOTE PER MENTOR — RISCHI SPECIFICI:
#    - overfitting: con 200 immagini per classe, e' quasi inevitabile senza
#      data augmentation aggressiva e early stopping
#    - data leakage: se le 200 buste paga vengono dallo stesso cliente, fare
#      split per cliente, non per file (regola del prodotto)
#    - compatibilita' MIME: le buste paga potrebbero essere PDF -> conversione
#      PDF->JPG nel preprocessing (pdf2image / pymupdf)
# ============================================================================
