"""
============================================================================
MODULO 3 — CAPITOLO 10 (SEGNAPOSTO): Progetto Gradio + deploy HuggingFace Spaces
============================================================================

⚠️ FILE SEGNAPOSTO — DA CREARE alla chiusura del cap.09 M3.
Qui sotto solo TODO MENTOR. Nessun codice operativo.

⚠️ CAPITOLO FINALE DEL MODULO 3 — produce il SECONDO URL portfolio del corso
   (dopo Streamlit Cloud del M2 cap.07).
"""

# ============================================================================
# TODO MENTOR — quando si crea questo capitolo:
# ----------------------------------------------------------------------------
# 1) GATE: leggere CONTESTO + diario cap.09 M3 (transfer_learning) + tabella "Portfolio — Demo
#    deployate per modulo".
#
# 2) STRUTTURA SIMILE A M2 cap.06+07 ("Streamlit da zero" + "Deploy"):
#    cap.07 M3 unisce i due livelli (build app + deploy) in un solo capitolo
#    perche' Gradio e' piu' compatto di Streamlit.
#
# 3) AZIONI PROPEDEUTICHE:
#    [ ] modello fine-tuned dal cap.09 M3 disponibile in locale (state_dict)
#    [ ] account HuggingFace creato (Spaces e' free)
#    [ ] requirements.txt aggiornato con gradio, torch, torchvision, pillow
#
# 4) STRUTTURA del file:
#    - Header + DoD (4 domande)
#    - Mappa
#    - Quiz d'ingresso (cerniera cap.09 M3: transfer learning, fine-tuning)
#    - SEZIONE 1: Gradio in 30 secondi (gr.Interface(fn, inputs, outputs))
#    - SEZIONE 2: input gr.Image, output gr.Label (con probabilita' per classe)
#      + esempi pre-caricati (gr.Examples)
#    - SEZIONE 3: caricare il modello PyTorch in CPU per inferenza (in
#      produzione su Spaces gratuito non c'e' GPU - serve quantization?
#      no, ResNet18 quantized non serve, gira bene)
#    - SEZIONE 4: funzione predict(image) -> {"busta paga": p1, "altro": p2}
#      con preprocessing (resize, normalize ImageNet, ToTensor)
#    - SEZIONE 5: deploy su HuggingFace Spaces (creazione space, push git,
#      file richiesti: app.py, requirements.txt, README.md)
#    - SEZIONE 6 (CRITICA): test live + smoke test:
#      - cambiare immagine di input -> output cambia
#      - mostrare confidence (probabilita') in modo onesto
#      - disclaimer "questa e' una demo, non uno strumento di produzione"
#    - Quiz di verifica (1 Feynman: "perche' la prima inferenza su Spaces
#      e' lenta e poi diventa veloce?")
#    - Esercizi: COLLOQUIO ("come deployeresti un modello PyTorch in
#      produzione?"), REFACTORING (codice app.py inizialmente messo male),
#      DEBUG (Spaces che fallisce: file non trovato, dimensione modello, ecc.)
#    - 🏗️ PROGETTO INCREMENTALE: la demo live e' parte del prodotto. Aggiungere
#      l'URL al portfolio (CONTESTO_CORSO.md → tabella Portfolio).
#    - 🔄 CONFRONTO PRIMA/DOPO (OBBLIGATORIO ultimo capitolo modulo, regola 16):
#      lo studente riscrive il neurone del cap.01 M3 con la consapevolezza
#      acquisita - cosa farebbe di diverso ora?
#    - Soluzioni quiz
#
# 5) FOLLOW-UP A FINE CAPITOLO (FINE MODULO 3):
#    - completare protocollo FINE CAPITOLO (5 passi)
#    - completare protocollo FINE MODULO (regola del corso):
#      [ ] verificare CONFRONTO PRIMA/DOPO completato
#      [ ] aggiornare tabella Portfolio con URL HuggingFace Spaces
#      [ ] scommentare dipendenze del modulo successivo (M4 NLP) in
#          requirements.txt
#      [ ] creare archivi/ARCHIVIO_MODULO_03.md con storico e migrare il dettaglio
#      [ ] decidere se il dataset "alterato vs genuino" entra come capitolo
#          bonus M3 o si rimanda a M8 (fine-tuning specializzato)
#
# 6) DIARIO: M03_C10_progetto_gradio_sessione.md
# ============================================================================
