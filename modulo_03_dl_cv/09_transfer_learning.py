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


# ============================================================================
# RINFORZI OBBLIGATORI DA CHIUSURA CAP.08 (01/09/2026)
# ----------------------------------------------------------------------------
# Questi blocchi NON sono opzionali: vanno inseriti nel capitolo 09 quando
# viene scritto, ognuno nel punto della teoria indicato. Fonte: chiusura
# cap.08 + tabella "Lacune dai Quiz" e "Pattern di Errore" di CONTESTO_CORSO.md.
#
# Voto difficolta' cap.08: 7/10. Media primi tentativi ~8.2 su 36 valutazioni.
# ----------------------------------------------------------------------------
#
# 🔁 #49 — "il 1 di (1,28,28) e' il CANALE" → in SEZIONE 3 (caricare ResNet)
#     Ponte perfetto: ResNet18 pre-addestrata su ImageNet vuole 3 canali,
#     le scansioni/buste in grayscale ne hanno 1. Spiegare:
#       - convenzione (C,H,W) vs (H,W,C) di Matplotlib/PIL
#       - squeeze() toglie le dimensioni di size 1, permute riordina gli assi
#       - due soluzioni: transforms.Grayscale(num_output_channels=3)
#         oppure x.repeat(1, 3, 1, 1) sul batch
#     Micro 49.A: dato x di shape (4,1,224,224), scrivi la riga che lo porta
#                 a (4,3,224,224). Micro 49.B: perche' imshow su (3,64,64)
#                 richiede permute e non squeeze?
#
# 🔁 #48 — "chi calcola i gradienti: autograd" → in SEZIONE 2 (freezing)
#     Il freezing e' il contesto naturale: for p in backbone.parameters():
#     p.requires_grad = False. Spiegare che il flag governa il TRACCIAMENTO
#     delle operazioni (grafo), che autograd e' il motore che calcola, e che
#     l'optimizer si limita a usare i .grad gia' scritti.
#     Micro 48.A: con requires_grad=False, dopo loss.backward() cosa trovi
#                 in .grad? Micro 48.B: perche' il freezing fa risparmiare
#                 tempo e memoria, non solo "blocca i pesi"?
#
# 🔁 #51 + Pattern #28 — "catena dei dimezzamenti" → in SEZIONE 2 (anatomia)
#     Errori cap.08: V4 3/10 (un pool invece di due) e TODO 7 4/10 (due
#     dimezzamenti per un solo pool). Antidoto in capitolo: TABELLA shape con
#     UNA RIGA PER LAYER sul percorso ResNet18: 224 → 112 → 56 → 28 → 14 → 7,
#     con indicato cosa dimezza (conv stride 2 / maxpool / stage).
#     Micro 51.A: input (8,3,224,224), scrivi la shape dopo ogni stage.
#     Micro 51.B: perche' avgpool finale + Linear(512, n_classi) non dipende
#                 dalla dimensione originale dell'immagine?
#
# 🔁 #52 — "debug numerico dell'errore matmul" → esercizio 🔍 [DEBUG]
#     Consegna in formato NUMERATO (vedi Pattern #6): esattamente 3 bullet +
#     fix. Scenario: si sostituisce model.fc con Linear(256, 2) invece di
#     Linear(512, 2) → RuntimeError con numeri espliciti. Lo studente deve
#     decomporre i numeri prima di toccare il codice.
#
# 🔁 #47 — ".item() vs backward" → verifica a freddo nel QUIZ D'INGRESSO
#     Una domanda secca. In cap.08 l'ha sbagliata a freddo (2/10) ma poi usata
#     correttamente due volte nel codice: se risponde bene → lacuna 🟢.
#
# 🔁 #50 — "il + 1 nella formula H_out" → una domanda di calcolo nel quiz
#     d'ingresso, questa volta CON stride diverso da 1 (es. k=7, stride=2,
#     pad=3 del primo conv di ResNet18).
#
# 🔁 #53 — "metriche per classe / macro-F1" → in SEZIONE 6 (valutazione)
#     Riusare precision/recall/F1/confusion_matrix del M2 cap.04, ma con
#     esplicito: metriche PER CLASSE + macro-F1, non solo accuracy globale.
#     Collegare al prodotto: recall su "busta paga" e' la metrica critica.
#
# ⚠️ Pattern #6 (consegne) — 🔴 riattivato con 4 occorrenze nel cap.08.
#     Regola per la scrittura del capitolo 09: quando una consegna contiene un
#     NUMERO o un FORMATO ("3 bullet", "5 controlli", "una riga", "dopo due
#     pool"), metterlo in MAIUSCOLO o come lista numerata vuota da riempire,
#     cosi' il vincolo non evapora nella lettura.
#
# 📌 Regola 42 — teoria prima degli esercizi discorsivi: la domanda Feynman
#     prevista ("perche' funziona il transfer learning su documenti se
#     ImageNet ha gatti e cani?") richiede che nel capitolo ci sia PRIMA la
#     teoria su feature generiche nei primi layer vs feature specifiche negli
#     ultimi. Non darlo per scontato.
#
# 🏗️ PROGETTO — stato al 01/09/2026: il debito tabellare M3-07 e' CHIUSO
#     (cap.08 TODO 5). Il cap.09 apre il ramo visivo reale del prodotto:
#     deliverable = state_dict del modello busta-paga-vs-altro, destinato a
#     diventare la feature `prob_busta_paga_visivo` nel modello M2.
# ============================================================================
