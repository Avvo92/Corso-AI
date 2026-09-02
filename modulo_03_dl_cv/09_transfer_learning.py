"""
============================================================================
MODULO 3 (DL & CV) - CAPITOLO 09
"Transfer learning": riusare una rete già addestrata (e il primo dataset reale)
============================================================================

Nel cap.08 hai costruito `PiccolaCNN` da zero e l'hai allenata su
Fashion-MNIST: 60.000 immagini pubbliche, 28x28, in bianco e nero.

Qui cambiano DUE cose insieme:

  1) NON parti più da pesi casuali. Prendi una rete (ResNet18) già
     addestrata da altri su ImageNet (1,2 milioni di foto, 1000 classi),
     le tagli la testa e le insegni SOLO il tuo compito.
  2) NON usi più un dataset giocattolo. Entrano le tue buste paga reali,
     ANONIMIZZATE. Da qui in poi il progetto è un progetto vero, con
     vincoli veri.

Analogia (lavoro):
  - Training da zero = assumere un ragazzo appena diplomato e insegnargli
    tutto: cos'è un foglio, cos'è una tabella, cos'è un documento.
  - Transfer learning = assumere un perito che ha già lavorato 10 anni
    guardando immagini di ogni tipo. Non gli spieghi cos'è un bordo o una
    tabella: gli spieghi solo "queste sono buste paga, quelle no".
  - Fine-tuning = dopo qualche settimana, gli fai anche ritoccare un po'
    le abitudini vecchie che nel tuo settore non funzionano.

⚠️ HARDWARE: AMD Vega 10 → niente CUDA in locale.
   ResNet18 su 400 immagini a 224x224 in CPU = ore. Training su Colab.
   Workflow: Cursor (studio) → Colab GPU (training) → .pt scaricato →
   locale con map_location="cpu".

🔒 PRIVACY — LEGGI PRIMA DI TOCCARE QUALSIASI FILE:
   Questo è il capitolo in cui entrano documenti reali di persone reali.
   La SEZIONE 0 non è un preambolo burocratico: è la prima sezione tecnica
   del capitolo, e va eseguita prima di tutto il resto.
   Regola non negoziabile: su Colab salgono SOLO immagini anonimizzate.

----------------------------------------------------------------------------
COME LEGGERE QUESTO FILE
----------------------------------------------------------------------------
Stesso schema del cap.08:

    [1] ANALOGIA → [2] idea → [3] codice PyTorch → [4] tranelli → [5] mini
    [6] 📚 LETTURA PARALLELA (opzionale, dopo il mini)

I blocchi 🔁 RINFORZO sono le lacune rimaste aperte dal cap.08: non sono
ripetizioni, sono gli stessi concetti visti in un contesto nuovo.

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.09)
----------------------------------------------------------------------------
  1) Hai una cartella di buste paga ANONIMIZZATE e sai spiegare
     cosa hai mascherato e cosa no, e perché                       → Sez. 0
  2) Sai spiegare cos'è il transfer learning e quando NON funziona → Sez. 1
  3) Sai leggere l'anatomia di ResNet18: backbone + head,
     e sai dire la shape dopo ogni stage                           → Sez. 2
  4) Carichi ResNet18 pre-addestrata, sostituisci la `fc`,
     gestisci il problema 1 canale vs 3 canali                     → Sez. 3
  5) Costruisci le trasformazioni giuste per DOCUMENTI
     (e sai dire quali augmentation sarebbero un errore)           → Sez. 4
  6) Alleni in due fasi (head-only → unfreeze layer4) su Colab
     e salvi lo state_dict                                         → Sez. 5
  7) Valuti con metriche PER CLASSE + macro-F1 + confusion matrix  → Sez. 6
  8) Spieghi (Feynman) perché ImageNet (gatti e cani) aiuta
     su un dataset di documenti                                    → Quiz V

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  QUIZ D'INGRESSO (cerniera cap.08 + lacune aperte)         Q1 - Q8
   *  SEZIONE 0  🔒 Privacy e anonimizzazione (BLOCCANTE)
   *  SEZIONE 1  Cos'è il transfer learning (e quando fallisce)
   *  SEZIONE 2  Anatomia ResNet18 + freezing        🔁 #48 #51 Pattern #28
   *  SEZIONE 3  torchvision.models, testa nuova, canali    🔁 #49
   *  SEZIONE 4  Data augmentation per documenti
   *  SEZIONE 5  Fine-tuning in due fasi (Colab)
   *  SEZIONE 6  Valutazione per classe               🔁 #53
   *  QUIZ DI VERIFICA                                         V1 - V8
   *  ESERCIZI: COLLOQUIO, REFACTOR, DEBUG, RETRIEVAL,
                INTERLEAVING, REAL-WORLD, SHAPE, 📚 [LIBRO]
   *  🏗️ PROGETTO: primo modello visivo del prodotto
   *  Soluzioni quiz
============================================================================
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Studia le sezioni qui; il training va su Google Colab (GPU).\n"
    )

try:
    from torchvision import datasets, models, transforms
    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}\n"
            "         Su Colab è già installato.\n"
        )

try:
    import matplotlib.pyplot as plt
    PLOT_OK = True
except Exception:
    PLOT_OK = False

# OpenCV serve SOLO per lo script di anonimizzazione (Sez. 0), in LOCALE.
# Su Colab non serve: là arrivano già le immagini pulite.
try:
    import cv2
    CV2_OK = True
except Exception:
    CV2_OK = False

# sklearn: riuso delle metriche del M2 cap.04 (Sez. 6)
try:
    from sklearn.metrics import classification_report, confusion_matrix
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False


SEME = 42
random.seed(SEME)
np.random.seed(SEME)
if TORCH_OK:
    torch.manual_seed(SEME)


# ==========================================================================
# PRE-FLIGHT — da spuntare PRIMA di iniziare (non è burocrazia)
# ==========================================================================
#
#   [ ] `.gitignore` contiene `data/buste_*/`         (verificato 01/09/2026 ✅)
#   [ ] cartelle locali create:
#           data/buste_originali/        ← i PDF/JPG come li hai tu
#           data/buste_anonimizzate/     ← output dello script Sez. 0
#           data/altro/                  ← ~200 immagini "non busta paga"
#   [ ] dataset "altro" raccolto: fatture, contratti, lettere, moduli,
#       più qualche foto generica. Fonti pubbliche suggerite:
#       Tobacco-3482, RVL-CDIP (subset), documenti fac-simile pubblici.
#   [ ] hai guardato con i tuoi occhi 5 immagini "altro" a caso:
#       se sono tutte scansioni storte e le buste sono tutte PDF puliti,
#       il modello imparerà "storto vs pulito", non "busta vs altro".
#
# ==========================================================================
# WORKFLOW COLAB
# ==========================================================================
#
# 1) https://colab.research.google.com → Runtime → Cambia tipo runtime → GPU
# 2) Verifica:
#       import torch, torchvision
#       print(torch.__version__, torchvision.__version__, torch.cuda.is_available())
# 3) Comprimi in locale SOLO la cartella anonimizzata:
#       dataset_visivo.zip  ←  data/buste_anonimizzate/ + data/altro/
#    Carica lo zip su Colab (o su Drive) e scompatta in /content/dataset_visivo
# 4) Alleni (Sez. 5), poi:
#       torch.save({"model_state": modello.state_dict(),
#                   "classi": dataset.classes,
#                   "arch": "resnet18",
#                   "img_size": 224}, "busta_vs_altro.pt")
# 5) Scarichi il .pt e in locale:
#       ckpt = torch.load("busta_vs_altro.pt", map_location="cpu")
#
# ⚠️ Alla fine della sessione Colab: Runtime → Termina sessione.
#    Il disco della VM viene distrutto. Non lasciare dataset su Drive
#    condiviso senza motivo.
# ==========================================================================


# ==========================================================================
# QUIZ D'INGRESSO (Q1 - Q8) — cerniera cap.08 + lacune aperte
# ==========================================================================
#
# Rispondi SENZA aprire 08_cnn_computer_vision.py. Soluzioni in fondo al file.
#
# Q1) 🔁 #47 — In un training step, questa riga:
#         somma_loss += loss.item() * xb.size(0)
#     va scritta PRIMA o DOPO `loss.backward()`? E soprattutto: perché
#     usare `.item()` e non `loss`?
# TUA RISPOSTA:
# va scritta dopo -> si usa item() per avere solo il valore scalare della loss.

# Q2) 🔁 #50 — Il primo layer di ResNet18 è:
#         nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
#     Input (1, 3, 224, 224). Calcola H_out mostrando i passaggi della
#     formula (non solo il risultato).
# TUA RISPOSTA:
# input[2] = H_in -> 224
# H_out = (floor((224 + 2*3 - 7) / 2) + 1) -> 112

# Q3) 🔁 #49 — Hai un tensore `x` di shape (1, 28, 28).
#     Cosa rappresenta ciascuno dei tre numeri? E se volessi disegnarlo con
#     `plt.imshow`, cosa devi fare prima?
# TUA RISPOSTA:
# La shape del tensore in questione può essere vista come (C, H, W), ossia "canali", "altezza", "larghezza". 
# tuttavia, dato che plt.imshow() si aspetta un tensore 2D, usiamo x.squeeze() per trasformarlo in shape (28, 28)


# Q4) V/F — `nn.MaxPool2d(2)` ha parametri che vengono aggiornati
#     dall'optimizer durante il training. Motiva in una riga.
# TUA RISPOSTA:
# Falso: Il MaxPool2D(2) fa semplicemente un thumbnail della feature map che passiamo in input. Spostandosi lungo la mappa, in una finestra di dim 2*2 prende solo il valore più alto. In pratiche abbassa la risoluzione della feature map di input. Dunque non ha parametri (pesi) da aggiornare.


# Q5) Trova l'errore:
#         criterio = nn.CrossEntropyLoss()
#         y = torch.tensor([[0., 1.], [1., 0.]])   # one-hot, float
#         loss = criterio(logits, y)
#     Cosa vuole davvero `CrossEntropyLoss` come target (dtype e shape)?
# TUA RISPOSTA:
# nn.CrossEntropyLoss() si aspetta come y un Long(N, ), e non un one-hot di float


# Q6) Definizione — Cosa contiene esattamente uno `state_dict`? Cita due
#     cose che NON contiene.
# TUA RISPOSTA:
# contiene i pesi, i bias e i buffer di un modello. Non contiene lo state dell'optimizer, i gradienti (.grad), lr epoche di training e metriche

# Q7) Prevedi l'output:
#         x = torch.randn(8, 3, 32, 32)
#         conv = nn.Conv2d(3, 16, kernel_size=3, padding=1)
#         pool = nn.MaxPool2d(2)
#         print(pool(conv(x)).shape)
# TUA RISPOSTA:


# Q8) 💬 Con parole tue, in 2-3 righe: perché una CNN ha molti meno
#     parametri di una rete fully-connected che guarda gli stessi pixel?
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 0 — 🔒 PRIVACY E ANONIMIZZAZIONE (bloccante)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 0.1 Perché l'anonimizzazione viene PRIMA, non dopo
# --------------------------------------------------------------------------
#
# Analogia: è come il backup. Tutti sanno che va fatto "prima", ma lo si
# capisce davvero solo dopo il primo disco morto. Qui il disco morto è:
# hai caricato 200 buste paga con nome, codice fiscale e IBAN su una VM
# di Google per allenare un modello, e non hai più modo di dimostrare
# dove sono finiti quei byte.
#
# Cosa succede concretamente se salti il passaggio:
#
#   - I dati escono dal tuo perimetro. Colab è un servizio terzo: nel
#     momento in cui carichi il file, hai fatto un TRASFERIMENTO di dati
#     personali (e i dati di una busta paga sono dati personali:
#     nome, CF, retribuzione, a volte dati sindacali o sanitari, che sono
#     "categorie particolari", cioè la classe di dati più protetta).
#   - Non puoi più cancellarli davvero. Non controlli le copie, i backup,
#     le cache del servizio.
#   - Il modello può memorizzare. Una rete addestrata su pochi esempi può
#     riprodurre dettagli degli esempi. Se un domani pubblichi i pesi su
#     HuggingFace (ed è esattamente il piano del cap.10), stai pubblicando
#     qualcosa che è stato costruito su quei dati.
#   - Un repository Git non dimentica: se committi una busta paga e poi
#     la cancelli in un commit successivo, il file resta nella storia.
#
# Le tre regole operative del corso (già in CONTESTO_CORSO.md):
#   R1. Gli originali NON escono mai dal disco locale.
#   R2. Su Colab salgono SOLO immagini anonimizzate.
#   R3. Nessuna busta paga in Git, nemmeno anonimizzata → `.gitignore`.
#
# --------------------------------------------------------------------------
# 0.2 Cosa mascherare e cosa NON mascherare
# --------------------------------------------------------------------------
#
# Qui c'è la parte interessante dal punto di vista tecnico, non legale.
#
# Il compito del modello è: "questa immagine è una busta paga oppure no?".
# Per rispondere, il modello NON legge il testo. Guarda la GEOMETRIA:
#
#     - la griglia di una tabella con molte righe strette
#     - i blocchi di intestazione in alto
#     - le colonne di numeri allineate a destra
#     - la densità del testo e il rapporto bianco/nero
#     - la presenza di un riquadro riepilogativo in fondo
#
# Quindi:
#
#   DA MASCHERARE (dati personali, inutili al modello):
#     nome e cognome, codice fiscale, matricola, indirizzo,
#     IBAN, numero di conto, importi netti se ti sembrano identificanti,
#     eventuali dati su assenze per malattia o iscrizione sindacale.
#
#   DA NON MASCHERARE (struttura, utile al modello):
#     il layout della tabella, le righe e le colonne vuote,
#     le intestazioni generiche ("periodo di paga", "totale competenze"),
#     i bordi, il carattere generale, la disposizione dei blocchi.
#
# Il punto chiave da capire, e che vale in tutti i progetti reali:
# l'anonimizzazione ben fatta toglie l'informazione IDENTIFICANTE e
# conserva l'informazione UTILE AL COMPITO. Se maschera anche la seconda,
# hai buttato via il dataset; se conserva la prima, non hai anonimizzato.
#
# ⚠️ Attenzione al falso senso di sicurezza: un rettangolo nero disegnato
#    SOPRA un PDF con un editor non cancella il testo sottostante, lo copre
#    soltanto. Per questo lo script lavora su IMMAGINI RASTERIZZATE:
#    converti il PDF in pixel, poi anneri i pixel. Il testo non esiste più.
#
# --------------------------------------------------------------------------
# 0.3 Lo script di anonimizzazione (locale, fuori dal training)
# --------------------------------------------------------------------------
#
# Idea: le buste paga di uno stesso datore/software hanno layout costante.
# Le zone da coprire sono quasi sempre nelle stesse posizioni RELATIVE.
# Quindi definisci le zone in percentuale (0.0 - 1.0) e le riusi su tutte
# le immagini, indipendentemente dalla risoluzione.
#
#   (x0, y0, x1, y1) = angolo alto-sinistra e basso-destra, in frazione
#                      di larghezza e altezza. (0,0) = alto-sinistra.

# Esempio di configurazione: DA TARARE sulle tue buste, non copiarla e basta.
ZONE_DA_MASCHERARE = [
    (0.05, 0.08, 0.55, 0.18),   # blocco anagrafica in alto a sinistra
    (0.60, 0.08, 0.98, 0.14),   # matricola / codice fiscale in alto a destra
    (0.05, 0.86, 0.60, 0.94),   # riga IBAN / modalità di pagamento in fondo
]


def anonimizza_immagine(percorso_in, percorso_out, zone=ZONE_DA_MASCHERARE):
    """Copre con rettangoli neri le zone indicate e salva una NUOVA immagine.

    Lavora su pixel: dopo il salvataggio il testo coperto non è recuperabile.
    Non modifica mai il file originale.

    zone: lista di (x0, y0, x1, y1) in frazioni [0, 1] della dimensione.
    """
    if not CV2_OK:
        raise RuntimeError("Serve OpenCV: pip install opencv-python")

    immagine = cv2.imread(str(percorso_in))
    if immagine is None:
        raise ValueError(f"Immagine illeggibile o corrotta: {percorso_in}")

    altezza, larghezza = immagine.shape[:2]
    for (x0, y0, x1, y1) in zone:
        punto_1 = (int(x0 * larghezza), int(y0 * altezza))
        punto_2 = (int(x1 * larghezza), int(y1 * altezza))
        cv2.rectangle(immagine, punto_1, punto_2, color=(0, 0, 0), thickness=-1)

    Path(percorso_out).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(percorso_out), immagine)
    return percorso_out


# Conversione PDF → immagine (le buste paga spesso sono PDF).
# Richiede: pip install pymupdf
#
#     import fitz                                  # pymupdf
#     documento = fitz.open("busta.pdf")
#     pagina = documento[0]                        # solo la prima pagina
#     pixmap = pagina.get_pixmap(dpi=150)          # 150 dpi basta e avanza
#     pixmap.save("busta_p1.png")
#
# ⚠️ dpi alto = file enormi e nessun guadagno: tanto poi ridimensioni a 224.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 0.1 — verifica a campione
# --------------------------------------------------------------------------
# Dopo aver anonimizzato, NON fidarti dello script. Scrivi 3-4 righe che
# aprono 5 immagini a caso dalla cartella anonimizzata e le mostrano.
# Suggerimento: random.sample(lista, 5) + plt.imshow.
# TUO CODICE:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 0.2 — il ragionamento, non il codice
# --------------------------------------------------------------------------
# Scrivi ESATTAMENTE 2 bullet:
#   - uno con una cosa che hai mascherato e il motivo
#   - uno con una cosa che hai deciso di NON mascherare e il motivo
#     (deve essere un motivo TECNICO: "serve al modello perché...")
# TUA RISPOSTA:
# -
# -


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 0.3
# --------------------------------------------------------------------------
# Il tuo script salva in `data/buste_anonimizzate/`. Scrivi la riga di
# comando (o il codice) che ti dimostra che quella cartella NON verrà
# committata. Suggerimento: `git check-ignore -v <percorso>`.
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 1 — COS'È IL TRANSFER LEARNING (e quando NON funziona)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 1.1 Il problema che risolve
# --------------------------------------------------------------------------
#
# Nel cap.08 avevi 60.000 immagini. Qui ne hai 400. Con 400 immagini una
# CNN allenata da zero fa una cosa sola bene: imparare a memoria le 400
# immagini (overfitting) e sbagliare sulla 401esima.
#
# Perché servono tanti dati per partire da zero? Perché i primi layer
# devono re-imparare cose banali e universali: "esiste il concetto di
# bordo", "esiste il concetto di angolo", "esiste il concetto di zona
# scura accanto a zona chiara". Sono cose che NON dipendono dal tuo
# problema: valgono per i gatti, per le automobili e per le buste paga.
#
# Analogia web: non riscrivi la validazione delle email a mano ogni volta.
# Importi una libreria che qualcuno ha già scritto e testato su milioni di
# casi, e sopra ci metti la TUA logica di business.
#
# --------------------------------------------------------------------------
# 1.2 La teoria che serve davvero: feature generiche vs feature specifiche
# --------------------------------------------------------------------------
#
# Questa è la parte da capire bene, perché ci torna sopra la domanda
# Feynman del quiz di verifica.
#
# Una CNN profonda impara a livelli, e i livelli non sono tutti uguali:
#
#   LAYER BASSI (primi conv)
#     Imparano filtri elementari: bordi orizzontali, bordi verticali,
#     macchie di colore, gradienti, texture ripetute.
#     Se stampi i filtri del primo layer di una qualsiasi rete allenata su
#     ImageNet, vedi sempre le stesse cose: strisce e macchie. Sempre.
#     Sono UNIVERSALI: qualunque immagine del mondo è fatta di bordi.
#
#   LAYER MEDI
#     Combinano i bordi in forme: angoli, curve, griglie, motivi ripetuti,
#     "zona di testo fitto", "linea lunga orizzontale".
#     Ancora abbastanza generiche. Una tabella e una recinzione, per un
#     layer medio, si somigliano parecchio: righe che si incrociano.
#
#   LAYER ALTI (ultimi conv)
#     Combinano le forme in concetti del dominio su cui sono stati
#     allenati: "orecchio di gatto", "ruota di automobile", "muso di cane".
#     Qui la rete è SPECIALIZZATA su ImageNet.
#
#   TESTA (fc finale)
#     Traduce quei concetti nelle 1000 classi di ImageNet.
#     Per te è completamente inutile: tu non devi distinguere 1000 razze
#     di animali, devi rispondere sì/no su un documento.
#
# Da qui la strategia, che è tutto il capitolo in tre righe:
#
#     1. tieni i layer bassi e medi         (feature generiche → riusabili)
#     2. butta la testa e mettine una nuova (2 classi, non 1000)
#     3. eventualmente ritocca i layer alti (feature troppo "da ImageNet")
#
# Perché funziona su documenti anche se ImageNet è pieno di gatti?
# Perché una busta paga, agli occhi dei primi due terzi della rete, è:
# un rettangolo bianco con righe orizzontali lunghe, blocchi di texture
# fitta (il testo), zone vuote e una griglia. Tutte cose che la rete ha già
# visto migliaia di volte — nelle recinzioni, nelle finestre, nei tessuti,
# nei codici a barre, nei giornali fotografati.
#
# --------------------------------------------------------------------------
# 1.3 Transfer learning e fine-tuning: due parole per due gradi
# --------------------------------------------------------------------------
#
#   TRANSFER LEARNING (senso ampio)
#       Partire dai pesi di una rete allenata su un altro compito invece
#       che da numeri casuali.
#
#   FEATURE EXTRACTION (il caso più conservativo)
#       Congeli tutto il backbone, alleni SOLO la testa nuova.
#       Il backbone diventa una funzione fissa: immagine → 512 numeri.
#       È quasi come fare una regressione logistica su feature pre-calcolate.
#
#   FINE-TUNING
#       Alleni la testa E qualche layer alto del backbone, con un learning
#       rate piccolo per non distruggere quello che sanno già.
#
# In pratica il confine è sfumato e nel parlato si usa "fine-tuning" per
# tutto. In colloquio conviene essere precisi: "ho fatto feature extraction
# per 3 epoche e poi fine-tuning dell'ultimo blocco a lr 1e-4".
#
# --------------------------------------------------------------------------
# 1.4 Quando il transfer learning NON funziona (il caso più istruttivo)
# --------------------------------------------------------------------------
#
# Le reti su ImageNet vengono allenate con il flip orizzontale come
# augmentation: un cane girato a destra è sempre un cane. Conseguenza: la
# rete impara feature quasi identiche per un'immagine e la sua speculare.
#
# Ora prendi un compito dove destra e sinistra CONTANO: riconoscere i
# cartelli stradali "svolta a destra" e "svolta a sinistra". Il backbone
# pre-addestrato produce quasi lo stesso vettore per le due classi, e la
# testa non ha modo di distinguerle. Il transfer learning qui fa danno.
#
# Per te la lezione è doppia:
#   (a) verifica sempre se il tuo dominio ha simmetrie che ImageNet ha
#       "appiattito";
#   (b) NON usare il flip orizzontale sulle buste paga: un documento
#       specchiato non esiste in natura, e insegneresti alla rete che il
#       testo al contrario è normale. → ci torniamo in Sezione 4.
#
# Altri casi in cui rende poco: immagini mediche a 16 bit, spettrogrammi,
# immagini satellitari multibanda. Non perché "non è una foto", ma perché
# la statistica dei pixel è troppo diversa da quella di ImageNet.

# --------------------------------------------------------------------------
# 📚 LETTURA PARALLELA (Sez. 1)
# --------------------------------------------------------------------------
# [PYTORCH] §14.5.3 "Reusing preexisting weights: Fine-tuning".
#   La definizione del libro: partire da una rete allenata su dati affini
#   invece che da inizializzazione casuale è transfer learning; quando si
#   allenano solo gli ultimi layer si parla di fine-tuning. Il libro
#   descrive esattamente il caso dei cartelli stradali come esempio di
#   fallimento dovuto al flip.
# [GERON] cap. 14 "Pretrained Models for Transfer Learning".
#   Stessa strategia in due fasi che useremo in Sez. 5.
# Cosa ho scartato: nel libro PyTorch il fine-tuning è dentro il progetto
#   LUNA (TAC polmonari, dati 3D). L'idea è identica, l'ambientazione no.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.1
# --------------------------------------------------------------------------
# Completa la frase con UNA parola per spazio:
#   "Nel transfer learning i layer ________ imparano feature generiche e
#    sono quelli che riusiamo; i layer ________ sono specializzati sul
#    dataset originale e sono i primi che conviene ritoccare."
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.2
# --------------------------------------------------------------------------
# Un collega ti dice: "prendo ResNet18 pre-addestrata e la uso così com'è
# per dire se un documento è una busta paga". Cosa c'è che non va, in una
# riga? (pensa a cosa produce l'ultimo layer)
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.3
# --------------------------------------------------------------------------
# Inventa TU un caso, nel tuo settore (documenti, pratiche mutuo), in cui
# il transfer learning da ImageNet secondo te renderebbe poco. Una riga di
# scenario + una riga di motivo.
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 2 — ANATOMIA DI ResNet18 E FREEZING
# ==========================================================================
#
# --------------------------------------------------------------------------
# 2.1 Backbone + head: la separazione mentale del capitolo
# --------------------------------------------------------------------------
#
# Ogni CNN da classificazione si legge in due pezzi:
#
#     BACKBONE (o feature extractor)
#         tutta la parte convoluzionale: immagine → vettore di feature.
#         Per ResNet18: immagine 224x224x3 → vettore di 512 numeri.
#
#     HEAD (o classifier)
#         un Linear che traduce quei numeri in punteggi per classe.
#         Per ResNet18 originale: Linear(512, 1000).
#
# Analogia: il backbone è la libreria in `node_modules` che nessuno
# riscrive; la head è il tuo controller, tre righe, tue.
#
# --------------------------------------------------------------------------
# 2.2 Perché "Res"Net: la skip connection in due righe
# --------------------------------------------------------------------------
#
# Prima del 2015 le reti molto profonde si allenavano male: più layer
# aggiungevi, PEGGIO andava anche in training (non solo in test — quindi
# non era overfitting, era proprio un problema di ottimizzazione).
#
# La trovata: invece di far calcolare al blocco l'uscita completa, gli fai
# calcolare solo la CORREZIONE da sommare all'ingresso.
#
#     uscita = blocco(x) + x         ← "skip connection" / "shortcut"
#
# Conseguenza pratica: se i pesi partono vicini a zero, `blocco(x) ≈ 0` e
# il blocco produce `x`. Cioè: all'inizio la rete profonda si comporta come
# l'identità, non come rumore. Il segnale (e il gradiente, all'indietro)
# attraversa tutta la rete anche se metà dei layer non ha ancora imparato
# niente.
#
# Traduzione in codice web:
#     return input if non_ho_niente_da_aggiungere else input + correzione
#
# Per il nostro capitolo basta questo. Non ti serve implementarla: ti serve
# sapere perché puoi permetterti una rete da 18 (o 50, o 152) layer.

# --------------------------------------------------------------------------
# 2.3 🔁 RINFORZO #51 + Pattern #28 — la catena delle shape, UNA RIGA PER LAYER
# --------------------------------------------------------------------------
#
# Nel cap.08 hai perso punti due volte sullo stesso meccanismo: contare i
# dimezzamenti. Una volta hai applicato un pool quando erano due, una volta
# due quando era uno. L'antidoto non è "stare più attento": è scrivere una
# riga per layer, sempre, senza saltare passaggi mentali.
#
# ResNet18, input (N, 3, 224, 224). Ogni riga è UN modulo:
#
#   modulo                                    output              cosa cambia
#   ----------------------------------------------------------------------
#   conv1  Conv2d(3,64,k=7,s=2,p=3)           (N,  64, 112, 112)  H/2 (stride 2)
#   bn1    BatchNorm2d(64)                    (N,  64, 112, 112)  niente
#   relu   ReLU()                             (N,  64, 112, 112)  niente
#   maxpool MaxPool2d(k=3,s=2,p=1)            (N,  64,  56,  56)  H/2 (stride 2)
#   layer1  2 blocchi residui, stride 1       (N,  64,  56,  56)  niente
#   layer2  2 blocchi residui, stride 2       (N, 128,  28,  28)  H/2, canali x2
#   layer3  2 blocchi residui, stride 2       (N, 256,  14,  14)  H/2, canali x2
#   layer4  2 blocchi residui, stride 2       (N, 512,   7,   7)  H/2, canali x2
#   avgpool AdaptiveAvgPool2d((1,1))          (N, 512,   1,   1)  media su 7x7
#   flatten torch.flatten(x, 1)               (N, 512)            appiattisce
#   fc      Linear(512, 1000)                 (N, 1000)           logits
#
# Conta i dimezzamenti: sono CINQUE (conv1, maxpool, layer2, layer3,
# layer4). 224 → 112 → 56 → 28 → 14 → 7. E infatti 224 / 2^5 = 7.
#
# Due cose che vale la pena notare:
#
#   (a) La regola ricorrente delle CNN moderne: quando dimezzo H e W,
#       raddoppio i canali. La quantità di informazione per layer resta
#       nello stesso ordine di grandezza, ma diventa più "astratta".
#
#   (b) `AdaptiveAvgPool2d((1,1))` è il pezzo furbo. Non è un pool con
#       kernel fisso: gli dici la dimensione di USCITA che vuoi (1x1) e lui
#       calcola da solo la finestra. Qualunque cosa arrivi — 7x7, 10x10,
#       4x4 — esce (N, 512, 1, 1). Ecco perché la head `Linear(512, ...)`
#       non dipende dalla dimensione dell'immagine di partenza.
#       Nel cap.08 la tua `PiccolaCNN` invece si rompeva se cambiavi la
#       dimensione dell'immagine: quello era esattamente il problema che
#       `AdaptiveAvgPool2d` risolve.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.1 (🔁 #51)
# --------------------------------------------------------------------------
# Input (8, 3, 224, 224). Scrivi la shape dopo OGNI stage, UNA RIGA PER
# STAGE, per: maxpool, layer1, layer2, layer3, layer4, avgpool, flatten.
# Sono SETTE righe. Non saltarne nessuna.
# TUA RISPOSTA:
# maxpool  ->
# layer1   ->
# layer2   ->
# layer3   ->
# layer4   ->
# avgpool  ->
# flatten  ->


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.2 (🔁 #51, variante cattiva)
# --------------------------------------------------------------------------
# Stessa rete, ma input (8, 3, 96, 96). Quanto vale H dopo `layer4`?
# Scrivi il calcolo, non solo il numero. (Attenzione: 96 non è divisibile
# per 2 cinque volte in modo pulito — usa la divisione intera per difetto.)
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 2.4 🔁 RINFORZO #48 — freezing: chi calcola i gradienti, e cosa spegni
# --------------------------------------------------------------------------
#
# Nel cap.08 avevi risposto che i gradienti li calcola "il criterio" o
# "l'optimizer". Ripassiamo la catena, perché qui la usiamo davvero:
#
#   1. `requires_grad = True` su un tensore  → PyTorch TRACCIA ogni
#      operazione che lo coinvolge, costruendo il grafo di calcolo.
#      È un interruttore di registrazione, non un calcolatore.
#
#   2. `loss.backward()`                     → AUTOGRAD percorre il grafo
#      all'indietro e CALCOLA i gradienti, scrivendoli in `.grad` di ogni
#      foglia che aveva `requires_grad=True`.
#      Autograd è il motore. Il criterio (la loss) è solo il punto di
#      partenza del percorso.
#
#   3. `optimizer.step()`                    → LEGGE i `.grad` già scritti
#      e aggiorna i pesi. Non calcola niente di nuovo.
#
#   4. `optimizer.zero_grad()`               → azzera i `.grad`, perché
#      `backward()` ACCUMULA (somma) invece di sovrascrivere.
#
# Ora il freezing. Congelare un layer significa mettere `requires_grad`
# a False sui suoi parametri:
#
#       for parametro in modello.parameters():
#           parametro.requires_grad = False
#
# Cosa succede davvero, in ordine:
#   - PyTorch smette di registrare nel grafo le operazioni fatte per
#     calcolare i gradienti RISPETTO A QUEI PESI;
#   - non deve più conservare i tensori intermedi che servivano solo a
#     quel calcolo → risparmi MEMORIA (spesso è il guadagno maggiore);
#   - `backward()` fa meno lavoro → risparmi TEMPO;
#   - dopo `backward()`, il `.grad` di quei parametri resta `None`;
#   - di conseguenza l'optimizer non ha niente da aggiornare su di loro.
#
# Cioè: il freezing non è "l'optimizer li ignora". È una potatura del
# grafo, e il fatto che i pesi non cambino è la CONSEGUENZA.
#
# ⚠️ Il forward continua a passare per quei layer! Congelato ≠ disattivato.
#    I 512 numeri in uscita dal backbone li calcola comunque.
#
# ⚠️ Un layer nuovo creato adesso (es. `nn.Linear(512, 2)`) nasce con
#    `requires_grad=True` sui suoi parametri: se prima congeli tutto e POI
#    sostituisci la testa, la testa è già allenabile. L'ordine conta.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.3 (🔁 #48 — micro 48.A)
# --------------------------------------------------------------------------
# Un parametro ha `requires_grad = False`. Dopo `loss.backward()`, cosa
# trovi dentro il suo `.grad`? Scegli e motiva in una riga:
#   (a) un tensore di zeri   (b) None   (c) il gradiente calcolato ma non usato
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.4 (🔁 #48 — micro 48.B)
# --------------------------------------------------------------------------
# Perché il freezing fa risparmiare MEMORIA e non solo "blocca i pesi"?
# Due righe. (Indizio: cosa deve tenere in RAM il grafo di calcolo per
# poter fare il backward?)
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.5
# --------------------------------------------------------------------------
# Scrivi la riga che conta quanti parametri ALLENABILI ha un modello.
# Suggerimento: `p.numel()` e un filtro su `p.requires_grad`.
# TUO CODICE:
# n_allenabili =


# --------------------------------------------------------------------------
# 📚 LETTURA PARALLELA (Sez. 2)
# --------------------------------------------------------------------------
# [GERON] cap. 14, sezione ResNet: la skip connection porta la rete a
#   modellare f(x) = h(x) - x invece di h(x); siccome i pesi partono vicini
#   a zero, la rete parte dall'identità, e se la funzione obiettivo è
#   vicina all'identità (spesso lo è) il training accelera parecchio.
# [PYTORCH] §8.5.3 "Going deeper": stesso problema visto dal lato PyTorch,
#   con l'esperimento della rete profonda che non converge senza shortcut.
# Cosa ho scartato: l'implementazione a mano del blocco residuo (Géron la
#   fa in Keras). A noi serve saperla leggere, non riscriverla.


# ==========================================================================
# SEZIONE 3 — CARICARE ResNet18 E CAMBIARLE LA TESTA
# ==========================================================================
#
# --------------------------------------------------------------------------
# 3.1 torchvision.models: i pesi non sono nel codice
# --------------------------------------------------------------------------
#
# `torchvision.models` contiene le ARCHITETTURE. I PESI pre-addestrati si
# scaricano al primo utilizzo (~45 MB per ResNet18) e finiscono in cache
# (`~/.cache/torch/hub/checkpoints/`).
#
#     API attuale (da torchvision 0.13):
#         pesi = models.ResNet18_Weights.DEFAULT
#         modello = models.resnet18(weights=pesi)
#
#     API vecchia (deprecata, la trovi in tutti i tutorial vecchi):
#         modello = models.resnet18(pretrained=True)
#
#     Senza pesi (architettura vuota, inizializzazione casuale):
#         modello = models.resnet18(weights=None)
#
# L'oggetto `pesi` non porta solo i numeri: porta anche il preprocessing
# ufficiale con cui quei pesi sono stati allenati.
#
#         preprocess = pesi.transforms()     # pipeline pronta all'uso
#         print(pesi.meta["categories"][:5]) # le 1000 classi ImageNet
#
# --------------------------------------------------------------------------
# 3.2 Il preprocessing ImageNet non è un dettaglio
# --------------------------------------------------------------------------
#
# I pesi sono stati ottenuti dando in pasto alla rete immagini normalizzate
# in un modo preciso. Se tu gliene dai di normalizzate diversamente, è come
# chiamare un'API che si aspetta euro passandole centesimi: nessun errore,
# risultati senza senso.
#
#     transforms.Resize(256)          ridimensiona il lato corto a 256
#     transforms.CenterCrop(224)      ritaglia 224x224 al centro
#     transforms.ToTensor()           PIL (H,W,C) 0-255 → tensor (C,H,W) 0-1
#     transforms.Normalize(mean, std) (x - mean) / std, canale per canale
#
# I valori sono le medie e deviazioni standard dei canali RGB su ImageNet:

MEDIA_IMAGENET = [0.485, 0.456, 0.406]
STD_IMAGENET = [0.229, 0.224, 0.225]

# ⚠️ Nota sull'ordine: `ToTensor()` fa DUE cose insieme — sposta i canali
#    da (H,W,C) a (C,H,W) e scala da 0-255 a 0-1. `Normalize` va SEMPRE
#    dopo `ToTensor()`, perché lavora su tensori, non su immagini PIL.
#
# --------------------------------------------------------------------------
# 3.3 🔁 RINFORZO #49 — il problema dei canali: 1 vs 3
# --------------------------------------------------------------------------
#
# Ripasso della convenzione, perché nel cap.08 avevi letto il canale come
# batch:
#
#     PyTorch, singola immagine:   (C, H, W)      es. (1, 28, 28)
#     PyTorch, batch:              (N, C, H, W)   es. (32, 1, 28, 28)
#     Matplotlib / PIL:            (H, W)  oppure  (H, W, C)
#
# In `(1, 28, 28)` quell'1 è il numero di CANALI (grayscale = 1 canale),
# non "una immagine". La dimensione batch, se c'è, sta ancora più a
# sinistra.
#
# Da qui i due strumenti che confondi facilmente:
#
#     squeeze()   toglie le dimensioni di taglia 1
#                 (1, 28, 28) → (28, 28)          ✅ per imshow di un grigio
#     permute()   riordina gli assi, non ne toglie nessuno
#                 (3, 64, 64) → (64, 64, 3)       ✅ per imshow di un RGB
#
# Se provi `squeeze()` su (3, 64, 64) non succede niente: nessun asse vale
# 1. Se provi `permute` su un grigio ottieni (64, 64, 1), che Matplotlib
# spesso digerisce ma non è la strada pulita.
#
# ORA IL PROBLEMA VERO DI QUESTO CAPITOLO:
# ResNet18 ha come primo layer `Conv2d(3, 64, ...)`. Vuole 3 canali in
# ingresso, perché è stata allenata su foto a colori. Le tue scansioni sono
# spesso in scala di grigi: 1 canale. Se gliele passi così:
#
#     RuntimeError: Given groups=1, weight of size [64, 3, 7, 7],
#     expected input[8, 1, 224, 224] to have 3 channels, but got 1 channel
#
# Tre soluzioni, in ordine di preferenza:
#
#   (1) Nel transform, lato PIL — la più pulita:
#           transforms.Grayscale(num_output_channels=3)
#       Converte in grigio e replica il canale tre volte. Se l'immagine è
#       già a colori la porta a grigio: uniforma tutto il dataset, che è
#       esattamente quello che vuoi con documenti scansionati.
#
#   (2) Sul tensore già in batch:
#           x = x.repeat(1, 3, 1, 1)      # (N,1,H,W) → (N,3,H,W)
#       `repeat` copia i dati lungo l'asse indicato. Il "1" nelle altre
#       posizioni significa "lascia com'è".
#
#   (3) Modificare il primo conv della rete perché accetti 1 canale:
#           modello.conv1 = nn.Conv2d(1, 64, 7, stride=2, padding=3, bias=False)
#       Funziona, ma butti via i pesi pre-addestrati del primo layer, che
#       sono proprio quelli più riusabili. Da evitare, qui.
#
# ⚠️ Se usi la soluzione (1) o (2), i tre canali sono IDENTICI. Non è uno
#    spreco grave (il costo è solo nel primo conv) ed è la prassi.

# --------------------------------------------------------------------------
# 3.4 Sostituire la testa
# --------------------------------------------------------------------------
#
# La testa di ResNet18 si chiama `fc` ed è un `nn.Linear(512, 1000)`.
# Sostituirla vuol dire assegnare un nuovo modulo a quell'attributo:
#
#       modello.fc = nn.Linear(512, 2)
#
# Ma NON scrivere 512 a mano: chiedilo al modello.
#
#       n_feature = modello.fc.in_features      # 512 per resnet18
#       modello.fc = nn.Linear(n_feature, 2)
#
# Così se domani passi a resnet50 (dove sono 2048) il codice regge.
# Questo è anche l'antidoto all'errore del 🔍 [DEBUG] più avanti.


def costruisci_resnet18(num_classi=2, congela_backbone=True):
    """ResNet18 pre-addestrata su ImageNet, con testa nuova a `num_classi`.

    Ordine importante:
      1) carico i pesi
      2) congelo TUTTO
      3) sostituisco la testa  ← nasce con requires_grad=True, quindi
                                 resta l'unica parte allenabile
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    pesi = models.ResNet18_Weights.DEFAULT
    modello = models.resnet18(weights=pesi)

    if congela_backbone:
        for parametro in modello.parameters():
            parametro.requires_grad = False

    n_feature = modello.fc.in_features
    modello.fc = nn.Linear(n_feature, num_classi)
    return modello


def conta_parametri(modello):
    """Ritorna (totali, allenabili). Utile per vedere l'effetto del freeze."""
    totali = sum(p.numel() for p in modello.parameters())
    allenabili = sum(p.numel() for p in modello.parameters() if p.requires_grad)
    return totali, allenabili


# Numeri attesi con congela_backbone=True e num_classi=2:
#     totali     ≈ 11.177.538
#     allenabili =      1.026     ( = 512*2 pesi + 2 bias )
# Cioè stai allenando lo 0,009% dei parametri. Ed è per questo che
# funziona con 400 immagini.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.1 (🔁 #49 — micro 49.A)
# --------------------------------------------------------------------------
# Hai `x` di shape (4, 1, 224, 224). Scrivi UNA riga che lo porta a
# (4, 3, 224, 224).
# TUO CODICE:
# x =


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.2 (🔁 #49 — micro 49.B)
# --------------------------------------------------------------------------
# Perché per fare `plt.imshow` su un tensore (3, 64, 64) serve `permute` e
# non `squeeze`? Una riga.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.3
# --------------------------------------------------------------------------
# Costruisci il modello con `costruisci_resnet18(num_classi=2)` e stampa
# quanti parametri sono allenabili. Poi rifallo con
# `congela_backbone=False` e confronta i due numeri.
# TUO CODICE:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.4
# --------------------------------------------------------------------------
# V/F, con motivazione in una riga:
# "Congelare il backbone significa che durante il forward le immagini non
#  passano più per quei layer."
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 4 — DATA AUGMENTATION PER DOCUMENTI
# ==========================================================================
#
# --------------------------------------------------------------------------
# 4.1 Il problema: 400 immagini sono poche
# --------------------------------------------------------------------------
#
# Con 400 immagini e una rete con 11 milioni di parametri, la rete può
# semplicemente memorizzare. Il sintomo classico: loss di training che
# scende verso zero mentre la loss di validation risale. Hai già visto
# questa forma di grafico nel M2.
#
# La data augmentation attacca il problema dal lato dei dati: a ogni epoca
# la stessa immagine arriva alla rete leggermente diversa. Il modello non
# può più memorizzare "quella immagine lì", deve trovare qualcosa di più
# stabile.
#
# ⚠️ Punto fondamentale, che quasi tutti sbagliano la prima volta:
#    l'augmentation vive nel `transform` del dataset di TRAINING e viene
#    riapplicata a ogni `__getitem__`, cioè a ogni epoca in modo diverso.
#    Non stai creando file nuovi su disco: stai modificando al volo.
#
# --------------------------------------------------------------------------
# 4.2 Quali trasformazioni hanno senso su un DOCUMENTO
# --------------------------------------------------------------------------
#
# Il criterio è uno solo: dopo la trasformazione, l'immagine deve essere
# ancora un esempio PLAUSIBILE della sua classe. Se una busta paga
# trasformata non potrebbe mai arrivare così dal cliente, stai insegnando
# alla rete un mondo che non esiste.
#
#   trasformazione                       ha senso?   perché
#   ------------------------------------------------------------------------
#   rotazione piccola (±3-5°)            ✅ sì       scansioni storte: capita
#   rotazione grande (±90°)              ⚠️ forse    solo se ricevi PDF girati
#   crop casuale leggero (85-100%)       ✅ sì       bordi tagliati: capita
#   luminosità / contrasto               ✅ sì       scanner e fotocopie diversi
#   rumore leggero                       ✅ sì       scansioni sporche
#   sfocatura leggera                    ✅ sì       foto da cellulare
#   flip ORIZZONTALE                     ❌ no       testo specchiato: mai visto
#   flip VERTICALE                       ❌ no       documento capovolto: mai
#   distorsione prospettica forte        ⚠️ forse    solo se accetti foto
#   cambio di colore aggressivo          ❌ no       un documento fucsia non esiste
#
# Il flip orizzontale è la trappola: è l'augmentation più usata al mondo
# (sulle foto naturali è quasi sempre giusta) e su documenti è sbagliata.
# È lo stesso identico problema dei cartelli "svolta a destra / sinistra"
# di cui abbiamo parlato in Sez. 1.4.
#
# Secondo criterio, meno ovvio: la trasformazione deve essere UTILE, non
# solo innocua. Randomizzare 4 pixel in un angolo genera infinite immagini
# diverse e non insegna niente, perché la rete impara subito a ignorarli.

# --------------------------------------------------------------------------
# 4.3 Le due pipeline: train e valutazione
# --------------------------------------------------------------------------
#
# Regola: augmentation SOLO in training. Validation e test devono essere
# deterministici, altrimenti confronti metriche calcolate su dati diversi
# a ogni giro e non capisci più se stai migliorando.

DIM_IMMAGINE = 224


def costruisci_trasformazioni(dim=DIM_IMMAGINE):
    """Ritorna (transform_train, transform_eval) tarate su documenti."""
    if not VISION_OK:
        raise RuntimeError("Serve torchvision (usa Colab).")

    transform_train = transforms.Compose([
        # 3 canali: ResNet vuole RGB anche se il contenuto è grigio (🔁 #49)
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((dim + 32, dim + 32)),
        # fill=255 = bianco: ruotando resta "carta", non bordo nero
        transforms.RandomRotation(degrees=4, fill=255),
        transforms.RandomResizedCrop(dim, scale=(0.85, 1.0), ratio=(0.9, 1.1)),
        transforms.ColorJitter(brightness=0.25, contrast=0.25),
        transforms.ToTensor(),
        transforms.Normalize(MEDIA_IMAGENET, STD_IMAGENET),
        # NIENTE RandomHorizontalFlip: vedi 4.2
    ])

    transform_eval = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((dim + 32, dim + 32)),
        transforms.CenterCrop(dim),
        transforms.ToTensor(),
        transforms.Normalize(MEDIA_IMAGENET, STD_IMAGENET),
    ])
    return transform_train, transform_eval


# --------------------------------------------------------------------------
# 4.4 ImageFolder: il dataset che legge le cartelle
# --------------------------------------------------------------------------
#
# Nel cap.08 hai scritto una `Dataset` a mano (e nel TODO 5 una tabellare).
# Per le immagini su disco esiste già la classe pronta: `ImageFolder`.
# Vuole questa struttura, dove il NOME DELLA CARTELLA è l'etichetta:
#
#     dataset_visivo/
#         train/
#             altro/          img_001.png ...
#             busta_paga/     img_101.png ...
#         val/
#             altro/  busta_paga/
#         test/
#             altro/  busta_paga/
#
#     ds = datasets.ImageFolder("dataset_visivo/train", transform=transform_train)
#     print(ds.classes)        # ['altro', 'busta_paga']
#     print(ds.class_to_idx)   # {'altro': 0, 'busta_paga': 1}
#
# ⚠️ TRANELLO da ricordare: `ImageFolder` ordina le classi in ordine
#    ALFABETICO. Quindi 'altro' = 0 e 'busta_paga' = 1. Se assumi il
#    contrario, leggi la confusion matrix al rovescio e ti convinci di
#    avere un modello pessimo (o ottimo) senza motivo.
#    Non indovinare mai: stampa `ds.class_to_idx`.

INDICE_BUSTA = 1   # coerente con ImageFolder: 'altro'=0, 'busta_paga'=1

# --------------------------------------------------------------------------
# 4.5 Lo split: perché "casuale" qui è sbagliato
# --------------------------------------------------------------------------
#
# Le tue 200 buste paga non sono 200 documenti indipendenti: sono, molto
# probabilmente, poche decine di aziende con più mensilità a testa.
# Le buste di gennaio e febbraio della stessa azienda sono quasi identiche.
#
# Se fai uno split casuale, gennaio finisce in train e febbraio in
# validation. Il modello riconosce il layout di quell'azienda, non
# "la busta paga". Risultato: 98% in validation e disastro sul primo
# cliente nuovo. È lo stesso data leakage che hai visto nel M2, in versione
# visiva.
#
# Regola del prodotto: LO SPLIT SI FA PER CLIENTE (per gruppo), mai per
# file. Tutte le buste dello stesso datore stanno tutte di qua o tutte
# di là.


def dividi_per_gruppo(elementi, gruppo_di, frazioni=(0.7, 0.15, 0.15), seme=SEME):
    """Divide in train/val/test tenendo insieme gli elementi dello stesso gruppo.

    elementi : lista di percorsi (o oggetti qualsiasi)
    gruppo_di: funzione elemento -> chiave di gruppo (es. il cliente)
    Ritorna: (train, val, test) come liste di elementi.
    """
    per_gruppo = {}
    for elemento in elementi:
        per_gruppo.setdefault(gruppo_di(elemento), []).append(elemento)

    chiavi = sorted(per_gruppo)
    rng = random.Random(seme)
    rng.shuffle(chiavi)

    n_train = int(len(chiavi) * frazioni[0])
    n_val = int(len(chiavi) * frazioni[1])
    blocchi = {
        "train": chiavi[:n_train],
        "val": chiavi[n_train:n_train + n_val],
        "test": chiavi[n_train + n_val:],
    }
    return tuple(
        [e for chiave in blocchi[nome] for e in per_gruppo[chiave]]
        for nome in ("train", "val", "test")
    )


# Esempio d'uso, se i file si chiamano "ACME_2024_01.png":
#     gruppo_di = lambda percorso: Path(percorso).stem.split("_")[0]
#     train, val, test = dividi_per_gruppo(lista_buste, gruppo_di)
#
# ⚠️ Con lo split per gruppo le proporzioni non vengono mai esatte
#    (70/15/15 sui GRUPPI, non sui file). È il prezzo giusto da pagare.

# --------------------------------------------------------------------------
# 📚 LETTURA PARALLELA (Sez. 4)
# --------------------------------------------------------------------------
# [PYTORCH] §12.6 "Preventing overfitting with data augmentation".
#   Il libro elenca cinque tecniche (specchio, traslazione, scala,
#   rotazione, rumore) e insiste su due criteri: la trasformazione deve
#   mantenere l'esempio RAPPRESENTATIVO e deve essere abbastanza diversa
#   da non essere memorizzabile insieme all'originale. L'esempio contrario
#   è bellissimo: randomizzare 4 pixel d'angolo moltiplica il dataset per
#   miliardi e non serve a niente.
#   C'è anche un avvertimento operativo che vale per te: se metti una cache
#   nella pipeline, la cache va PRIMA dell'augmentation. Altrimenti
#   memorizzi una sola versione aumentata e hai buttato via il meccanismo.
# Cosa ho scartato: il libro lavora con `affine_grid`/`grid_sample` su dati
#   3D (TAC). Con immagini 2D `torchvision.transforms` fa tutto.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.1
# --------------------------------------------------------------------------
# Guarda `costruisci_trasformazioni`. Scrivi ESATTAMENTE 2 bullet:
#   - perché `RandomRotation` usa `fill=255`
#   - perché in `transform_eval` c'è `CenterCrop` e non `RandomResizedCrop`
# TUA RISPOSTA:
# -
# -


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.2
# --------------------------------------------------------------------------
# Un collega aggiunge `transforms.RandomHorizontalFlip(p=0.5)` alla
# pipeline di training "perché aumenta i dati". Spiegagli in due righe
# perché su questo dataset è un errore, collegandoti al caso dei cartelli
# stradali di Sez. 1.4.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.3
# --------------------------------------------------------------------------
# Hai 200 buste provenienti da 12 aziende diverse. Usi `dividi_per_gruppo`
# con frazioni (0.7, 0.15, 0.15). Quante AZIENDE finiscono in train, val e
# test? Scrivi i tre numeri e il calcolo (attenzione a `int()`).
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 5 — FINE-TUNING IN DUE FASI (su Colab)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 5.1 La strategia standard
# --------------------------------------------------------------------------
#
#   FASE 1 — "feature extraction"
#       backbone congelato, alleni solo la testa, learning rate normale
#       (1e-3 con Adam). Poche epoche: 3-5 bastano, perché stai allenando
#       1026 parametri.
#       Serve a far arrivare la testa a valori sensati PRIMA di toccare il
#       backbone. Se scongelassi subito, i gradienti enormi di una testa
#       casuale si propagherebbero all'indietro e rovinerebbero pesi buoni.
#
#   FASE 2 — "fine-tuning"
#       scongeli l'ultimo blocco (`layer4`), learning rate molto più basso
#       (1e-4 o meno) su quel blocco. Altre 3-5 epoche.
#       Serve perché `layer4` è la parte più "ImageNet-specifica": è lì che
#       la rete pensa in termini di musi e zampe, e a te servono griglie e
#       blocchi di testo.
#
# Perché due learning rate diversi? Perché i due pezzi partono da
# situazioni opposte: la testa è casuale (deve muoversi tanto), il
# backbone sa già qualcosa di buono (deve muoversi poco). PyTorch lo
# permette con i "parameter group" dell'optimizer.
#
# Se dopo la fase 2 sei ancora sotto le aspettative, le cause possibili
# sono tre (e vale la pena sapere l'ordine in cui indagarle):
#   1) le feature del backbone non sono adatte al compito;
#   2) la testa è troppo semplice (un solo Linear);
#   3) tutta la rete è troppo piccola.
# Nel 90% dei casi reali con 400 immagini, però, il problema non è la
# capacità: è il dataset.


def prepara_dataloader(cartella_base, batch=16, num_workers=2):
    """Crea i tre DataLoader da una cartella con train/ val/ test/."""
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    transform_train, transform_eval = costruisci_trasformazioni()
    base = Path(cartella_base)

    ds_train = datasets.ImageFolder(str(base / "train"), transform=transform_train)
    ds_val = datasets.ImageFolder(str(base / "val"), transform=transform_eval)
    ds_test = datasets.ImageFolder(str(base / "test"), transform=transform_eval)

    print("classi:", ds_train.class_to_idx)
    print(f"train={len(ds_train)}  val={len(ds_val)}  test={len(ds_test)}")

    dl_train = DataLoader(ds_train, batch_size=batch, shuffle=True,
                          num_workers=num_workers)
    dl_val = DataLoader(ds_val, batch_size=batch, shuffle=False,
                        num_workers=num_workers)
    dl_test = DataLoader(ds_test, batch_size=batch, shuffle=False,
                         num_workers=num_workers)
    return dl_train, dl_val, dl_test, ds_train.classes


def allena_una_epoca(modello, dataloader, criterio, optimizer, device):
    """Un passaggio completo sul training set. Ritorna (loss_media, accuracy)."""
    modello.train()                      # BatchNorm/Dropout in modalità training
    somma_loss = 0.0
    corretti = 0
    visti = 0

    for xb, yb in dataloader:
        xb, yb = xb.to(device), yb.to(device)

        optimizer.zero_grad()
        logits = modello(xb)
        loss = criterio(logits, yb)
        loss.backward()
        optimizer.step()

        # .item() stacca il numero dal grafo: se accumulassi `loss`
        # terresti in memoria il grafo di TUTTI i batch dell'epoca
        somma_loss += loss.item() * xb.size(0)
        corretti += (logits.argmax(1) == yb).sum().item()
        visti += xb.size(0)

    return somma_loss / visti, corretti / visti


def valuta(modello, dataloader, criterio, device):
    """Valutazione senza gradienti. Ritorna (loss, accuracy, y_veri, y_pred, prob_busta)."""
    modello.eval()                       # BatchNorm usa le statistiche salvate
    somma_loss = 0.0
    visti = 0
    tutti_veri, tutti_pred, tutte_prob = [], [], []

    with torch.no_grad():                # niente grafo: meno memoria, più veloce
        for xb, yb in dataloader:
            xb, yb = xb.to(device), yb.to(device)
            logits = modello(xb)
            loss = criterio(logits, yb)

            somma_loss += loss.item() * xb.size(0)
            visti += xb.size(0)

            probabilita = torch.softmax(logits, dim=1)[:, INDICE_BUSTA]
            tutti_veri.append(yb.cpu())
            tutti_pred.append(logits.argmax(1).cpu())
            tutte_prob.append(probabilita.cpu())

    y_veri = torch.cat(tutti_veri).numpy()
    y_pred = torch.cat(tutti_pred).numpy()
    prob_busta = torch.cat(tutte_prob).numpy()
    accuratezza = float((y_veri == y_pred).mean())
    return somma_loss / visti, accuratezza, y_veri, y_pred, prob_busta


def scongela_layer4(modello):
    """Fase 2: riapre i gradienti sull'ultimo blocco convoluzionale."""
    for parametro in modello.layer4.parameters():
        parametro.requires_grad = True
    return modello


def ottimizzatore_due_velocita(modello, lr_testa=1e-3, lr_backbone=1e-4):
    """Parameter group: la testa si muove 10 volte più del layer4."""
    return torch.optim.Adam([
        {"params": modello.layer4.parameters(), "lr": lr_backbone},
        {"params": modello.fc.parameters(), "lr": lr_testa},
    ])


def pipeline_addestramento(cartella_base, epoche_fase1=4, epoche_fase2=4,
                           percorso_salvataggio="busta_vs_altro.pt"):
    """Le due fasi, con salvataggio del modello migliore in validation.

    Da lanciare su Colab con GPU. In locale (CPU) è lentissimo.
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device)

    dl_train, dl_val, dl_test, classi = prepara_dataloader(cartella_base)
    modello = costruisci_resnet18(num_classi=len(classi), congela_backbone=True)
    modello = modello.to(device)
    criterio = nn.CrossEntropyLoss()

    totali, allenabili = conta_parametri(modello)
    print(f"parametri: {totali:,} totali / {allenabili:,} allenabili")

    # --- FASE 1: solo la testa -------------------------------------------
    optimizer = torch.optim.Adam(
        [p for p in modello.parameters() if p.requires_grad], lr=1e-3
    )
    migliore_val = 0.0

    for epoca in range(epoche_fase1):
        loss_tr, acc_tr = allena_una_epoca(modello, dl_train, criterio, optimizer, device)
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(f"[F1 {epoca+1}/{epoche_fase1}] train {loss_tr:.4f}/{acc_tr:.3f} "
              f"| val {loss_va:.4f}/{acc_va:.3f}")
        if acc_va > migliore_val:
            migliore_val = acc_va
            torch.save({"model_state": modello.state_dict(), "classi": classi,
                        "arch": "resnet18", "img_size": DIM_IMMAGINE,
                        "fase": 1, "acc_val": acc_va}, percorso_salvataggio)

    # --- FASE 2: testa + layer4 ------------------------------------------
    modello = scongela_layer4(modello)
    optimizer = ottimizzatore_due_velocita(modello)
    totali, allenabili = conta_parametri(modello)
    print(f"dopo unfreeze: {allenabili:,} parametri allenabili")

    for epoca in range(epoche_fase2):
        loss_tr, acc_tr = allena_una_epoca(modello, dl_train, criterio, optimizer, device)
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(f"[F2 {epoca+1}/{epoche_fase2}] train {loss_tr:.4f}/{acc_tr:.3f} "
              f"| val {loss_va:.4f}/{acc_va:.3f}")
        if acc_va > migliore_val:
            migliore_val = acc_va
            torch.save({"model_state": modello.state_dict(), "classi": classi,
                        "arch": "resnet18", "img_size": DIM_IMMAGINE,
                        "fase": 2, "acc_val": acc_va}, percorso_salvataggio)

    print(f"migliore accuracy validation: {migliore_val:.3f} → {percorso_salvataggio}")
    return modello, dl_test, classi


# --------------------------------------------------------------------------
# 5.2 Riconoscere l'overfitting mentre succede
# --------------------------------------------------------------------------
#
# Guarda le due colonne stampate a ogni epoca:
#
#   train 0.62/0.71 | val 0.60/0.74     → stanno scendendo insieme: bene
#   train 0.11/0.98 | val 0.55/0.79     → train scende, val ferma: overfitting
#   train 0.05/0.99 | val 0.83/0.72     → val RISALE: overfitting conclamato
#
# Cosa fare, in ordine di costo crescente:
#   1) tenere il modello dell'epoca migliore (lo fa già il codice sopra);
#   2) fermarsi prima (early stopping);
#   3) aumentare l'augmentation;
#   4) congelare di più (tornare a head-only);
#   5) raccogliere più dati — quasi sempre la risposta vera.
#
# ⚠️ Con 400 immagini divise per cliente, il validation set ha forse 60
#    immagini. Una differenza di accuracy del 2% sono UN'IMMAGINE E MEZZA.
#    Non fare scelte architetturali su quel rumore.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.1
# --------------------------------------------------------------------------
# In `pipeline_addestramento`, l'optimizer della fase 1 è costruito con
# `[p for p in modello.parameters() if p.requires_grad]`.
# Cosa cambierebbe passando semplicemente `modello.parameters()`?
# Il training funzionerebbe lo stesso? Due righe.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.2
# --------------------------------------------------------------------------
# Perché nella fase 2 il learning rate del `layer4` è 10 volte più piccolo
# di quello della testa? Una riga.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.3
# --------------------------------------------------------------------------
# `valuta()` chiama sia `modello.eval()` sia `torch.no_grad()`.
# Sono la stessa cosa? Scrivi ESATTAMENTE 2 bullet, uno per ciascuno,
# dicendo cosa fa e cosa NON fa.
# TUA RISPOSTA:
# - modello.eval():
# - torch.no_grad():


# ==========================================================================
# SEZIONE 6 — VALUTAZIONE: 🔁 RINFORZO #53 (metriche PER CLASSE)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 6.1 L'accuracy globale mente
# --------------------------------------------------------------------------
#
# Il tuo dataset è bilanciato (200 vs 200), quindi l'accuracy è meno
# ingannevole del solito. Ma il dato reale del prodotto non è bilanciato:
# un operatore carica per lo più buste paga, oppure per lo più altro,
# a seconda della pratica. E soprattutto: i due errori NON costano uguale.
#
# Ripasso del vocabolario (M2 cap.04), fissando la classe "busta paga"
# come positiva:
#
#   VERO POSITIVO   (TP)  era busta paga, ho detto busta paga
#   FALSO POSITIVO  (FP)  NON era busta paga, ho detto busta paga
#   FALSO NEGATIVO  (FN)  era busta paga, ho detto altro
#   VERO NEGATIVO   (TN)  non era, ho detto non era
#
#   precision = TP / (TP + FP)   quanto mi fido quando dice "busta paga"
#   recall    = TP / (TP + FN)   quante buste paga riesco a trovare
#   F1        = media armonica delle due
#
# La media armonica (2·p·r / (p+r)) invece di quella semplice serve perché
# punisce lo sbilanciamento: precision 1.0 e recall 0.0 dà F1 = 0, non 0.5.
#
# --------------------------------------------------------------------------
# 6.2 Per classe, macro-F1, e perché non basta un numero
# --------------------------------------------------------------------------
#
# Precision e recall si calcolano PER OGNI CLASSE: la recall di "altro" è
# una cosa diversa dalla recall di "busta paga". Due modi di riassumerle:
#
#   macro-F1     media semplice degli F1 di ogni classe.
#                Ogni classe pesa uguale, anche quella rara. È la scelta
#                giusta quando le classi rare ti interessano.
#   weighted-F1  media pesata sul numero di esempi.
#                Somiglia all'accuracy: la classe grossa domina.
#
# In colloquio, la risposta buona a "che metrica usi?" non è mai un nome
# secco: è "dipende da quale errore costa di più nel mio prodotto".
#
# --------------------------------------------------------------------------
# 6.3 Nel NOSTRO prodotto quale errore costa di più?
# --------------------------------------------------------------------------
#
# Il classificatore visivo serve a smistare i documenti caricati
# dall'operatore, e il suo output (`prob_busta_paga_visivo`) diventerà una
# feature del modello tabellare M2. Quindi:
#
#   FALSO NEGATIVO (busta paga scambiata per altro)
#       la busta finisce nel percorso sbagliato, i controlli sul reddito
#       non partono, la pratica prosegue senza il documento chiave.
#       Costo: alto. È l'errore che il prodotto deve evitare.
#
#   FALSO POSITIVO (fattura scambiata per busta paga)
#       parte un controllo su un documento sbagliato: l'estrazione campi
#       fallisce o produce valori assurdi, e qualcuno se ne accorge.
#       Costo: fastidio, non danno.
#
# Conclusione: la metrica critica è la RECALL sulla classe "busta paga".
# E siccome la soglia di decisione è una tua scelta (non è scolpita a
# 0.5), puoi comprare recall pagando in precision abbassandola.

def valuta_per_classe(y_veri, y_pred, classi):
    """Report per classe + confusion matrix. Riuso diretto del M2 cap.04."""
    if not SKLEARN_OK:
        raise RuntimeError("Serve scikit-learn.")

    print("\n--- report per classe ---")
    print(classification_report(y_veri, y_pred, target_names=classi, digits=3))

    matrice = confusion_matrix(y_veri, y_pred)
    print("--- confusion matrix (righe = vero, colonne = predetto) ---")
    print("            " + "  ".join(f"{c:>12}" for c in classi))
    for nome, riga in zip(classi, matrice):
        print(f"{nome:>12}" + "  ".join(f"{v:>12}" for v in riga))
    return matrice


def predizioni_con_soglia(prob_busta, soglia=0.5):
    """Trasforma le probabilità in etichette usando una soglia scelta da te.

    Vale perché 'busta_paga' = 1 e 'altro' = 0 (ordine alfabetico di ImageFolder):
    il booleano diventa direttamente l'indice di classe.
    """
    return (prob_busta >= soglia).astype(int)


def esplora_soglie(y_veri, prob_busta, soglie=(0.3, 0.4, 0.5, 0.6, 0.7)):
    """Mostra come recall e precision della classe busta cambiano con la soglia."""
    print("\nsoglia  precision  recall   trovate/totali")
    positivi_veri = (y_veri == INDICE_BUSTA).sum()
    for soglia in soglie:
        y_pred = predizioni_con_soglia(prob_busta, soglia)
        tp = int(((y_pred == INDICE_BUSTA) & (y_veri == INDICE_BUSTA)).sum())
        fp = int(((y_pred == INDICE_BUSTA) & (y_veri != INDICE_BUSTA)).sum())
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / positivi_veri if positivi_veri else 0.0
        print(f"{soglia:>6.2f}  {precision:>9.3f}  {recall:>6.3f}   {tp}/{positivi_veri}")


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.1 (🔁 #53)
# --------------------------------------------------------------------------
# Confusion matrix su 60 immagini di test (righe = vero, colonne = predetto,
# ordine classi: ['altro', 'busta_paga']):
#
#                  altro   busta_paga
#     altro          28        2
#     busta_paga      5       25
#
# Calcola, mostrando i conti:
#   1) accuracy globale
#   2) recall della classe busta_paga
#   3) precision della classe busta_paga
# TUA RISPOSTA:
# 1)
# 2)
# 3)


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.2
# --------------------------------------------------------------------------
# Con quella matrice, il modello ha accuracy ~88%. Il tuo capo dice
# "ottimo, mettiamolo in produzione". Scrivi UNA obiezione tecnica basata
# sui numeri (non generica).
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.3
# --------------------------------------------------------------------------
# Vuoi più recall sulla classe busta_paga. Devi ALZARE o ABBASSARE la
# soglia rispetto a 0.5? E cosa peggiora in cambio? Due righe.
# TUA RISPOSTA:


# ==========================================================================
# QUIZ DI VERIFICA (V1 - V8)
# ==========================================================================
#
# Soluzioni in fondo. Rispondi senza scorrere.
#
# V1) Prevedi l'output:
#         modello = costruisci_resnet18(num_classi=2)
#         x = torch.randn(8, 3, 224, 224)
#         print(modello(x).shape)
# TUA RISPOSTA:


# V2) Trova l'errore:
#         modello = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
#         modello.fc = nn.Linear(1000, 2)
#     Cosa c'è di sbagliato e qual è il numero giusto? Perché proprio quello?
# TUA RISPOSTA:


# V3) V/F con motivazione: "Le trasformazioni di data augmentation vanno
#     applicate a training, validation e test, altrimenti i dati non sono
#     omogenei."
# TUA RISPOSTA:


# V4) Hai `ds = datasets.ImageFolder("dataset_visivo/train")` con le
#     sottocartelle `busta_paga/` e `altro/`. Quanto vale
#     `ds.class_to_idx["busta_paga"]`? Perché?
# TUA RISPOSTA:


# V5) Calcolo: ResNet18 congelata con testa `Linear(512, 2)`.
#     Quanti parametri sono ALLENABILI? Mostra il conto.
# TUA RISPOSTA:


# V6) Completa il codice — congela tutto tranne l'ultimo blocco e la testa:
#         for p in modello.parameters():
#             p.requires_grad = ______
#         for p in modello.layer4.parameters():
#             p.requires_grad = ______
#         modello.fc = nn.Linear(modello.fc.in_features, 2)
#     E poi: perché la riga della `fc` va bene anche senza toccare
#     `requires_grad`?
# TUA RISPOSTA:


# V7) Prevedi l'output (attenzione: input NON quadrato standard):
#         x = torch.randn(4, 3, 320, 320)
#         # dentro resnet18, dopo layer4
#     Quanto vale H dopo `layer4`? E cosa esce da `avgpool`?
# TUA RISPOSTA:


# V8) 💬 Spiega con parole tue (niente codice, 4-6 righe):
#     perché una rete addestrata su ImageNet — che è piena di gatti, cani e
#     automobili — aiuta a classificare buste paga? Cosa riusi davvero e
#     cosa butti via?
# TUA RISPOSTA:


# ==========================================================================
# ESERCIZI
# ==========================================================================

# --------------------------------------------------------------------------
# TODO 1 — 🎯 [COLLOQUIO] transfer learning vs training from scratch
# --------------------------------------------------------------------------
# Domanda da colloquio: "Hai 400 immagini etichettate e devi classificarle
# in 2 categorie. Parti da zero o usi una rete pre-addestrata? Motiva."
#
# Rispondi in ESATTAMENTE 3 BULLET (il numero fa parte della consegna):
#   - bullet 1: la scelta e il motivo principale, in termini di dati
#   - bullet 2: cosa congeli e cosa alleni, concretamente
#   - bullet 3: una condizione in cui cambieresti idea
# TUA RISPOSTA:
# -
# -
# -


# --------------------------------------------------------------------------
# TODO 2 — 🔧 [REFACTORING]
# --------------------------------------------------------------------------
# Questa funzione funziona ma è scritta male. Riscrivila come
# `costruisci_modello_bello(nome_arch, num_classi, congela)`.
#
# Problemi da correggere (ce ne sono almeno QUATTRO, trovali tutti):

def costruisci_modello_brutto(n):
    m = models.resnet18(pretrained=True)
    for p in m.parameters():
        p.requires_grad = False
    m.fc = nn.Linear(512, n)
    if n == 2:
        m.fc = nn.Linear(512, 2)
    return m

# TUO CODICE:
# def costruisci_modello_bello(...):


# --------------------------------------------------------------------------
# TODO 3 — 🔍 [DEBUG] (🔁 #52)
# --------------------------------------------------------------------------
# Codice eseguito su Colab:
#
#     modello = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
#     modello.fc = nn.Linear(256, 2)
#     x = torch.randn(32, 3, 224, 224)
#     out = modello(x)
#
# Errore:
#
#     RuntimeError: mat1 and mat2 shapes cannot be multiplied
#     (32x512 and 256x2)
#
# Consegna in formato FISSO — ESATTAMENTE 3 BULLET, poi il fix.
# Nei bullet devi DECOMPORRE I NUMERI dell'errore prima di toccare il
# codice: da dove viene ogni numero che compare nel messaggio.
#   - bullet 1: cosa sono 32 e 512 in `mat1`, e da quale layer arrivano
#   - bullet 2: cosa sono 256 e 2 in `mat2`, e chi li ha decisi
#   - bullet 3: quale dei quattro numeri è quello sbagliato, e perché
# Poi: la riga di fix, scritta in modo che non si rompa passando a resnet50.
# TUA RISPOSTA:
# -
# -
# -
# FIX:


# --------------------------------------------------------------------------
# TODO 4 — 🧠 [RETRIEVAL] (dal M2 cap.04, senza guardare)
# --------------------------------------------------------------------------
# Riscrivi DA ZERO, senza sklearn e senza aprire il modulo 2, la funzione:
#
#     def metriche_binarie(y_veri, y_pred, classe_positiva=1) -> dict
#
# Deve ritornare un dizionario con: tp, fp, fn, tn, precision, recall, f1.
# Gestisci il caso denominatore zero (non deve esplodere).
# `y_veri` e `y_pred` sono array NumPy di interi.
# TUO CODICE:


# --------------------------------------------------------------------------
# TODO 5 — 🔀 [INTERLEAVING] visivo + tabellare (M3 + M2)
# --------------------------------------------------------------------------
# Il modello di questo capitolo produce, per ogni documento, un numero:
# `prob_busta_paga_visivo`. Nel M2 avevi un classificatore tabellare che
# lavorava su feature come numero di pagine, dimensione file, esito OCR.
#
# Scrivi una funzione:
#
#     def aggiungi_feature_visiva(df, probabilita) -> DataFrame
#
# che aggiunge la colonna `prob_busta_paga_visivo` al DataFrame,
# verificando PRIMA che lunghezza e ordine coincidano (se non coincidono,
# solleva un errore chiaro invece di allineare a caso).
#
# Poi rispondi in 2 righe a questa domanda, che è la parte difficile:
# se calcoli quelle probabilità con il modello CNN allenato sulle stesse
# righe che poi usi per allenare il modello tabellare, che problema hai?
# Come lo eviteresti?
# TUO CODICE + RISPOSTA:


# --------------------------------------------------------------------------
# TODO 6 — 🌊 [REAL-WORLD] il dataset che ti arriva davvero
# --------------------------------------------------------------------------
# Apri la cartella con le tue buste e trovi questa situazione:
#
#   - 173 file, non 200
#   - 40 sono PDF multipagina (busta paga + cedolino + comunicazione)
#   - 12 sono foto da cellulare, storte e con l'ombra della mano
#   - 8 sono scansioni a 72 dpi, illeggibili anche per un umano
#   - alcuni file hanno lo stesso contenuto con nome diverso
#   - 60 file su 173 vengono dalla stessa azienda
#   - la cartella "altro" che hai scaricato è fatta al 90% di scansioni
#     pulite in bianco e nero
#
# Non c'è una soluzione unica. Scrivi il tuo piano in ESATTAMENTE 5 PUNTI
# NUMERATI, in ordine di esecuzione, e per ognuno una riga di motivo.
# Almeno uno dei cinque punti deve riguardare un rischio che NON è la
# qualità delle immagini.
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)
# 5)


# --------------------------------------------------------------------------
# TODO 7 — shape gymnastics su ResNet18
# --------------------------------------------------------------------------
# Input `(4, 3, 320, 320)`. Scrivi la shape dopo OGNI riga, SETTE righe:
# conv1, maxpool, layer1, layer2, layer3, layer4, avgpool.
# Poi rispondi: il `Linear(512, 2)` finale funziona lo stesso con immagini
# 320x320 invece di 224x224? Perché?
# TUA RISPOSTA:
# conv1   ->
# maxpool ->
# layer1  ->
# layer2  ->
# layer3  ->
# layer4  ->
# avgpool ->
# Il Linear funziona? perché:


# --------------------------------------------------------------------------
# TODO 8 — 📚 [LIBRO] depth-1 vs depth-2
# --------------------------------------------------------------------------
# In [PYTORCH] §14.5.3 gli autori provano prima a riallenare solo la testa
# ("depth 1"), ottenendo un risultato mediocre; poi includono anche
# l'ultimo blocco convoluzionale ("depth 2") e il modello migliora
# nettamente — ma inizia ad andare in overfitting molto prima.
#
# Prima di lanciare il training, scrivi la tua PREVISIONE in 2 bullet:
#   - cosa ti aspetti che succeda alla accuracy di validation passando
#     dalla fase 1 alla fase 2 sul TUO dataset
#   - cosa ti aspetti che succeda alla distanza fra loss di training e
#     loss di validation
# Poi lancia `pipeline_addestramento(...)` e confronta la previsione con i
# numeri veri. Se hai sbagliato la previsione, scrivi perché.
# TUA PREVISIONE:
# -
# -
# NUMERI VERI (dopo il training):
# COMMENTO:


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — il ramo visivo del prodotto parte qui
# ==========================================================================
#
# Nel M2 hai costruito il ramo tabellare (regole + classificatore su
# feature dei file). Nel cap.08 hai imparato le CNN su dati giocattolo.
# Da qui esce il primo pezzo VISIVO del prodotto vero.
#
# Deliverable del capitolo: `busta_vs_altro.pt`, uno state_dict che,
# data un'immagine di documento, dice quanto è probabile che sia una busta
# paga. Nel cap.10 questo file diventa una demo Gradio deployata
# (portfolio piece #2); più avanti, `prob_busta_paga_visivo` diventa una
# colonna in più per il modello M2.
#
# CHECKPOINT (spunta man mano):
#
#   [ ] C1 — cartelle create, `.gitignore` verificato con `git check-ignore`
#   [ ] C2 — PDF convertiti in immagini (prima pagina), file corrotti scartati
#            e ANNOTATI (quanti e perché: serve nel README del progetto)
#   [ ] C3 — `anonimizza_buste.py` eseguito su tutte le buste; verifica
#            visiva a campione su 10 immagini fatta con i tuoi occhi
#   [ ] C4 — dataset "altro" raccolto e reso confrontabile (non tutte
#            scansioni pulite: mescola qualità e formati)
#   [ ] C5 — split PER CLIENTE con `dividi_per_gruppo`, e conteggio
#            scritto: quante immagini e quanti clienti per ogni split
#   [ ] C6 — training su Colab, due fasi, `busta_vs_altro.pt` scaricato
#   [ ] C7 — valutazione sul TEST (mai guardato prima) con report per
#            classe, confusion matrix, e tabella soglie
#   [ ] C8 — 5 righe di README nel diario: accuracy, recall busta paga,
#            soglia scelta e perché, e il limite principale del modello
#
# ⚠️ C7 è quello che si salta più facilmente: il test set si guarda UNA
#    volta sola, alla fine. Se lo usi per scegliere la soglia o l'epoca,
#    hai trasformato il test in un secondo validation e non hai più una
#    stima onesta.


# ==========================================================================
# SOLUZIONI — QUIZ D'INGRESSO
# ==========================================================================
#
# Q1) Nella pratica si scrive DOPO `loss.backward()` (spesso dopo
#     `optimizer.step()`), ma il punto non è l'ordine: `.item()` non
#     romperebbe niente nemmeno prima, perché legge il valore senza
#     modificare il grafo.
#     Il vero motivo di `.item()` è un altro: restituisce un float Python
#     STACCATO dal grafo di calcolo. Se accumulassi il tensore `loss`
#     (`somma += loss`), terresti vivo in memoria il grafo di ogni batch
#     dell'epoca: la RAM cresce fino a esplodere. `* xb.size(0)` serve a
#     pesare la media, perché l'ultimo batch può essere più piccolo.
#
# Q2) H_out = floor((H_in + 2*padding - kernel) / stride) + 1
#            = floor((224 + 6 - 7) / 2) + 1
#            = floor(223 / 2) + 1
#            = 111 + 1
#            = 112
#     Il "+1" finale conta la posizione iniziale del filtro: le divisioni
#     contano gli SPOSTAMENTI, non le posizioni.
#
# Q3) (1, 28, 28) = (C, H, W): 1 CANALE (grayscale), 28 righe, 28 colonne.
#     Non c'è la dimensione batch. Per `imshow` serve (H, W): `x.squeeze()`
#     toglie l'asse di taglia 1 → (28, 28).
#
# Q4) FALSO. `MaxPool2d` non ha parametri: prende il massimo di ogni
#     finestra, è un'operazione fissa. Ha iperparametri (kernel, stride),
#     che sono scelte tue, non pesi appresi.
#
# Q5) `CrossEntropyLoss` vuole i target come indici di classe:
#     dtype `torch.long`, shape `(N,)`. Quindi `torch.tensor([1, 0])`,
#     non la matrice one-hot float. E gli input devono essere LOGITS
#     grezzi `(N, num_classi)`: la softmax la applica internamente.
#
# Q6) Uno `state_dict` è un dizionario ordinato nome → tensore, con i
#     parametri appresi (pesi e bias) e i buffer (es. `running_mean` e
#     `running_var` di BatchNorm).
#     NON contiene: l'architettura (serve la classe/funzione per
#     ricostruirla), lo stato dell'optimizer, gli iperparametri, i
#     gradienti, il codice.
#
# Q7) `torch.Size([8, 16, 16, 16])`
#     conv con padding=1 e kernel=3 mantiene 32x32 → (8, 16, 32, 32);
#     il pool dimezza → (8, 16, 16, 16).
#
# Q8) Due motivi: (a) connessioni LOCALI — ogni neurone guarda una
#     finestrella, non tutti i pixel; (b) PESI CONDIVISI — lo stesso
#     filtro scorre su tutta l'immagine, quindi paghi i suoi parametri una
#     volta sola invece che per ogni posizione. Un dense su 224x224x3
#     avrebbe ~150.000 pesi per singolo neurone; un conv 3x3 a 64 filtri
#     ne ha 1.792 in tutto.
#
# ==========================================================================
# SOLUZIONI — QUIZ DI VERIFICA
# ==========================================================================
#
# V1) `torch.Size([8, 2])`. Il backbone riduce ogni immagine a 512 numeri,
#     la testa nuova li mappa su 2 logit. La dimensione batch (8) non si
#     tocca mai.
#
# V2) Sbagliato `nn.Linear(1000, 2)`. Il 1000 sono le CLASSI di uscita
#     della testa originale, non le feature in ingresso. Le feature in
#     ingresso sono 512, cioè quello che esce da `avgpool` + `flatten`.
#     Scrittura robusta:
#         modello.fc = nn.Linear(modello.fc.in_features, 2)
#     Con `Linear(1000, 2)` otterresti l'errore matmul del TODO 3.
#
# V3) FALSO. L'augmentation va SOLO sul training. Su validation e test le
#     trasformazioni devono essere deterministiche (resize + center crop +
#     normalize), altrimenti le metriche cambiano a ogni esecuzione e non
#     sono confrontabili fra epoche o fra modelli. Quello che DEVE essere
#     omogeneo è il preprocessing di base (dimensione e normalizzazione),
#     non la parte casuale.
#
# V4) 1. `ImageFolder` ordina le classi in ordine alfabetico:
#     'altro' → 0, 'busta_paga' → 1. Non è una scelta semantica, è
#     `sorted()`. Da verificare sempre stampando `class_to_idx`.
#
# V5) 512 * 2 + 2 = 1.026 parametri allenabili (pesi + bias della testa)
#     su ~11,18 milioni totali: circa lo 0,009%.
#
# V6) `False`, poi `True`. La `fc` va bene senza toccare niente perché è un
#     modulo NUOVO, creato dopo il congelamento: i parametri di un modulo
#     appena istanziato hanno `requires_grad=True` per default. Se avessi
#     sostituito la testa PRIMA del ciclo di congelamento, l'avresti
#     congelata anche lei e il modello non avrebbe imparato niente.
#
# V7) conv1: floor((320 + 6 - 7)/2) + 1 = floor(319/2) + 1 = 160
#     maxpool: floor((160 + 2 - 3)/2) + 1 = 80
#     layer1 → 80, layer2 → 40, layer3 → 20, layer4 → 10.
#     Da `avgpool` esce comunque (4, 512, 1, 1), perché
#     `AdaptiveAvgPool2d((1,1))` media QUALSIASI griglia in un solo valore
#     per canale. Per questo la testa `Linear(512, 2)` continua a
#     funzionare: non vede mai H e W.
#
# V8) Risposta attesa (concetti, non parole esatte):
#     Una CNN impara a strati. I primi strati imparano cose universali —
#     bordi, angoli, gradienti, texture — che non dipendono dal soggetto:
#     valgono per un gatto come per un foglio. Gli strati intermedi
#     combinano quei bordi in forme: griglie, righe lunghe, zone di
#     texture fitta. Una busta paga, per quegli strati, è una griglia con
#     righe e blocchi di testo, e la rete ha già visto migliaia di
#     griglie e texture nelle foto di ImageNet.
#     Quello che NON si trasferisce sono gli ultimi strati e la testa:
#     lì la rete ragiona in termini di "orecchio di gatto" e produce 1000
#     punteggi che non ti servono. Quindi riusi il backbone (soprattutto
#     la parte bassa e media), butti la testa e ne metti una a 2 classi,
#     e se serve ritocchi l'ultimo blocco convoluzionale con un learning
#     rate piccolo.
#     Menzione bonus (non obbligatoria): funziona bene perché hai pochi
#     dati; con 500.000 buste paga il vantaggio si assottiglierebbe.


# ==========================================================================
# TRACCIA RINFORZI (per il mentor — verifica in chiusura capitolo)
# ==========================================================================
#
#   lacuna / pattern      dove è stato inserito
#   ------------------------------------------------------------------
#   #47 .item()           Q1 quiz d'ingresso + commento in allena_una_epoca
#   #48 autograd          Sez. 2.4 + mini 2.3 (48.A) + mini 2.4 (48.B)
#   #49 canale            Sez. 3.3 + mini 3.1 (49.A) + mini 3.2 (49.B) + Q3
#   #50 formula H_out     Q2 (stride 2) + V7 (320x320) + mini 2.2
#   #51 / Pattern #28     Sez. 2.3 tabella una-riga-per-layer + mini 2.1 + TODO 7
#   #52 debug matmul      TODO 3 (formato 3 bullet obbligatorio) + V2
#   #53 metriche classe   Sez. 6 + mini 6.1/6.2/6.3 + esplora_soglie
#   Pattern #6 consegne   numeri in MAIUSCOLO in: mini 0.2, 4.1, 5.3,
#                         TODO 1, TODO 3, TODO 6, TODO 7
#   Regola 42             Sez. 1.2 (feature generiche/specifiche) precede
#                         la Feynman V8
# ==========================================================================

