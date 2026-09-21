"""
============================================================================
MODULO 3 (DL & CV) — CAPITOLO 10 (ULTIMO DEL MODULO)
"Dal .pt alla demo live": Gradio, HuggingFace Spaces
e — soprattutto — come si impacchetta un modello perché sia RIUSABILE
============================================================================

Nel cap.09 hai fatto la parte difficile: transfer learning su ResNet18,
due fasi di training su Colab, metriche e soglia su un test set.
Il risultato è un file di pesi.

Qui c'è il pezzo che nei corsi viene sempre liquidato in dieci righe e che
nella realtà è quello che decide se il tuo modello è un lavoro finito o un
esperimento che nessuno riesce a riusare (te compreso, fra tre mesi).

Il filo del capitolo è questo:

    un file .pt NON è un modello.
    È un sacco di numeri. Diventa un modello quando lo accompagni
    con il CONTRATTO che dice come si usa.

E da lì scendono due assi, che sono le due metà del capitolo:

  ASSE 1 — riuso del MODELLO (Sez. 1-2)
      il contratto di inferenza, il checkpoint che porta con sé i propri
      metadati, la model card. "Chiunque, con questo file, ottiene
      gli stessi numeri che ottengo io."

  ASSE 2 — riuso del CODICE (Sez. 3, 9)
      funzioni generiche invece di script usa-e-getta, una classe
      `ClassificatoreVisivo` che espone `predict_proba` e che domani
      chiami identica da Gradio, da FastAPI o da un notebook.

Nel mezzo la parte visibile: Gradio (Sez. 4-6) e il deploy su
HuggingFace Spaces (Sez. 7-8), cioè il SECONDO URL del tuo portfolio
dopo lo Streamlit del M2.

----------------------------------------------------------------------------
LA CATENA COMPLETA DEL MODULO 3
----------------------------------------------------------------------------

    Cursor (studio)  →  Colab GPU (training)  →  checkpoint .pt
                                                      ↓
                              contratto di inferenza (classi, size, mean/std, soglia)
                                                      ↓
                        ClassificatoreVisivo.predict_proba(immagine)
                                          ↙                    ↘
                              Gradio (demo pubblica)     FastAPI (Validator, M10)

Nota bene la forma: il pezzo in mezzo è UNO. Le due uscite in fondo sono
due presentazioni diverse della stessa funzione. Questo è il senso di
"rete facile da riutilizzare".

----------------------------------------------------------------------------
VINCOLI DI QUESTO CAPITOLO
----------------------------------------------------------------------------

⚠️ HARDWARE: qui NON si allena niente. L'inferenza (= usare il modello
   per predire) di una ResNet18 su una immagine costa pochi millisecondi
   anche sulla tua Vega 10 senza CUDA, e gira benissimo sulla CPU gratuita
   di HuggingFace Spaces. Il capitolo è tutto eseguibile in locale.

⚠️ PRIVACY: la demo di questo capitolo è PUBBLICA su internet.
   - Track PROVA (quello che deployi ora): `ants_vs_bees.pt`, formiche e
     api. Immagini pubbliche, zero dati personali. Si può mostrare.
   - Track PRODOTTO (debito C1-C8 dal cap.09): `busta_vs_altro.pt`.
     Quando lo avrai: Space PRIVATO, oppure esempi finti/sintetici.
     Mai una busta paga reale negli esempi di una demo pubblica.

⚠️ REGOLA 42 (teoria prima degli esercizi): ogni domanda discorsiva di
   questo file ha la sua spiegazione sopra, nel file. Se trovi una
   consegna il cui concetto non è spiegato da nessuna parte, segnalalo:
   è un bug del capitolo, non una tua lacuna.

----------------------------------------------------------------------------
RESIDUI DAL CAP.09 CHE CHIUDIAMO QUI (blocchi 🔁)
----------------------------------------------------------------------------
  #48  eval() ≠ freeze ≠ no_grad()        → 🔁 + Sez. 3.4
  #52  decomporre l'errore matmul         → 🔁 + Sez. 3.1 (in_features)
  #53  obiezione "sui numeri"             → 🔁 + Sez. 8.2
  #6   rispettare il formato della consegna (numero di bullet)
  avgpool → vettore fisso 512             → 🔁

----------------------------------------------------------------------------
DEFINITION OF DONE (cap.10)
----------------------------------------------------------------------------
  1) Sai elencare le 6 voci del contratto di inferenza e dire cosa si
     rompe se ne manca una                                    → Sez. 1
  2) Salvi e ricarichi un checkpoint che porta con sé i metadati → Sez. 2
  3) Hai funzioni riusabili: costruisci_modello / transform_eval /
     ClassificatoreVisivo                                      → Sez. 3
  4) Sai costruire una UI Gradio Image→Label e spiegare cosa fa   → Sez. 4-5
  5) Hai un app.py in 4 blocchi separati, core testabile senza Gradio → Sez. 6
  6) La demo è LIVE su HuggingFace Spaces e ha superato lo smoke test → Sez. 7-8
  7) Sai riusare lo stesso core da FastAPI (senza riscrivere predict) → Sez. 9
  8) 🔄 CONFRONTO PRIMA/DOPO del modulo completato              → fine file
  9) URL registrato nella tabella Portfolio di CONTESTO_CORSO.md → 🏗️

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO
----------------------------------------------------------------------------
   *  QUIZ D'INGRESSO (cerniera cap.09)                        Q1 - Q8
   *  🔁 RINFORZI  #48 / #52 / #53 / #6 / avgpool              micro
   *  SEZIONE 1  Un .pt non è un modello: il contratto di inferenza
   *  SEZIONE 2  Il checkpoint ricco (riuso del MODELLO)
   *  SEZIONE 3  Codice riusabile: factory, transform, wrapper
   *  SEZIONE 4  Gradio: anatomia (Interface, componenti, Blocks)
   *  SEZIONE 5  predict() end-to-end: dal PIL alle probabilità
   *  SEZIONE 6  app.py in 4 blocchi (il file che deployi)
   *  SEZIONE 7  Deploy su HuggingFace Spaces
   *  SEZIONE 8  Smoke test, model card, latenza, privacy
   *  SEZIONE 9  Stesso core da FastAPI → ponte al prodotto
   *  QUIZ DI VERIFICA                                         V1 - V8
   *  ESERCIZI  COLLOQUIO / REFACTOR / DEBUG / RETRIEVAL /
               INTERLEAVING / REAL-WORLD / SYSTEM DESIGN / 📚 LIBRO
   *  🏗️ PROGETTO INCREMENTALE — demo live (portfolio #2)      G1 - G8
   *  🔄 CONFRONTO PRIMA/DOPO (obbligatorio, fine modulo)
   *  SOLUZIONI
============================================================================
"""

from __future__ import annotations

from pathlib import Path

# --------------------------------------------------------------------------
# Import protetti (stesso schema del cap.07/08/09)
# --------------------------------------------------------------------------
# Perché protetti: questo file deve restare LEGGIBILE e IMPORTABILE anche
# su una macchina dove torch non è installato. Se l'import fallisse
# secco, non potresti nemmeno aprire il capitolo per studiarlo.

try:
    import torch
    import torch.nn as nn
    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Puoi leggere tutto il capitolo; per eseguire le funzioni\n"
        "         installa: pip install torch torchvision\n"
    )

try:
    from torchvision import models, transforms
    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}\n"
        )

try:
    from PIL import Image
    PIL_OK = True
except Exception:
    PIL_OK = False


# --------------------------------------------------------------------------
# Costanti del contratto (le spieghiamo in Sez. 1; qui stanno in alto
# perché sono dati, non logica, e vanno trovate al primo sguardo)
# --------------------------------------------------------------------------

# Statistiche dei pixel di ImageNet: NON sono numeri magici, sono la media
# e la deviazione standard dei canali R, G, B calcolate sul dataset con cui
# la ResNet è stata pre-addestrata. Servono a presentare al modello
# immagini "nella scala a cui è abituato". Vedi Sez. 5.2.
MEAN_IMAGENET = [0.485, 0.456, 0.406]
STD_IMAGENET = [0.229, 0.224, 0.225]

# Versione del FORMATO di checkpoint (non del modello). Se un domani
# cambi le chiavi del dizionario, alzi questo numero e il codice di
# caricamento può gestire i vecchi file invece di esplodere.
VERSIONE_CONTRATTO = "1.0"

ROOT = Path(__file__).parent if "__file__" in globals() else Path.cwd()


# ==========================================================================
# QUIZ D'INGRESSO — cerniera con il cap.09
# ==========================================================================
#
# Rispondi A FREDDO, senza riaprire il cap.09. Soluzioni in fondo al file.
# Se una risposta non arriva, non è un dramma: serve a dire a entrambi
# quali concetti vanno ripescati prima di andare avanti.

# --------------------------------------------------------------------------
# Q1 — 🔁 lacuna #48 — le tre leve
# --------------------------------------------------------------------------
# In inferenza (demo che predice, nessun training) chiami sia
# `modello.eval()` sia `torch.no_grad()`.
# Consegna: DUE bullet. In ciascuno scrivi cosa FA quella leva e cosa
# NON fa. (Attenzione al formato: due bullet, non un paragrafo.)
# TUA RISPOSTA:
# - modello.eval() imposta il modello in fase valutazione, ed in pratica utilizza i buffer ("es. batchnorm") per andare a scalare con le running states i dati che utilizza per fare la sua predizione.
# - torch.no_grad() smette di tenere traccia dal grafo delle operazioni, risparmiando vram dato che non stiamo addestrando.

# --------------------------------------------------------------------------
# Q2 — 🔁 lacuna #52 — la testa della ResNet
# --------------------------------------------------------------------------
# Dopo `AdaptiveAvgPool2d((1,1))` e il flatten, ResNet18 consegna alla
# `fc` un vettore di quanti numeri?
# E perché `Linear(512, 2)` continua a funzionare anche se l'immagine in
# ingresso era 320×320 invece di 224×224?
# TUA RISPOSTA:
# presenta un vettore di shape (N_esempi, 512). Continua a funzionare grazie all'averagepool, che schiaccia qualunque H e W a 1. Ad esempio se se arriva all'avgpool (8, 512, 10, 10) o (8, 512, 7, 7), in uscita la shape sarà (8, 512, 1, 1) e, dopo il flatten, diventa (8, 512).

# --------------------------------------------------------------------------
# Q3 — ordine delle classi
# --------------------------------------------------------------------------
# Con `ImageFolder` su una cartella che contiene `ants/` e `bees/`,
# quanto vale `class_to_idx`? E da cosa dipende quell'ordine?
# TUA RISPOSTA:
# dato che ImageFolder ordina in ordine alfabetico, class_to_idx di ants vale 0 e class_to_idx di bees vale 1.

# --------------------------------------------------------------------------
# Q4 — 🔁 lacuna #53 — obiezione sui numeri
# --------------------------------------------------------------------------
# Sul test set: 45 immagini, accuracy 0.89.
# Consegna: UNA obiezione tecnica che cita ALMENO UN NUMERO (non
# "l'accuracy da sola non basta", che è vero ma generico).
# TUA RISPOSTA:
# su un set così limitato (45 esempi), l'accuracy non è sufficiente come metrica di appoggio, anche perchè non sappiamo la distribuzione delle classi. Ad esempio, se classe 1 è presente 40 volte su 45, se il nostro modello dicesse sempre 1, avrebbe ragione il 90% dell volte. Bisognerebbe vedere anche recall, per capire quanti target sfuggono al nostro vaglio. Se accuracy alta e recall bassa, avremmo la conferma che la prima è alta per via della distribuzione dei target, non perchè il modello predice correttamente.

# --------------------------------------------------------------------------
# Q5 — preprocessing
# --------------------------------------------------------------------------
# Elenca nell'ORDINE i 4 passaggi che trasformano un `PIL.Image` RGB in
# un tensore pronto per il forward di una ResNet ImageNet.
# TUA RISPOSTA:
# 1) Resize(256)
# 2) CenterCrop(224)
# 3) ToTensor()
# 4) Normalize(mean, std)

# --------------------------------------------------------------------------
# Q6 — map_location
# --------------------------------------------------------------------------
# Hai allenato su Colab (GPU CUDA) e ora carichi il `.pt` sul tuo PC
# senza CUDA. Cosa passi a `torch.load` e perché serve?
# TUA RISPOSTA:
# device = "cuda" if torch.cuda.is_available() else "cpu"
# modello.load_state_dict(torch.load(percorso_pesi, map_location=device))
# in questo modo, in base al device disponibile carico i pesi del modello nel posto giusto a prescindere.
# Questo serve perchè avendo usato un cuda nel runtime di colab, i pesi sono impostati per essere usati da una gpu nvidia. Se sul pc non l'abbiamo, dobbiamo reimpostare il modello e i pesi in modo da poter essere utilizzati su cpu.

# --------------------------------------------------------------------------
# Q7 — soglia
# --------------------------------------------------------------------------
# Nel cap.09 hai esplorato le soglie da 0.3 a 0.7. Se ABBASSI la soglia
# sulla classe positiva, cosa succede a recall e precision, e perché?
# TUA RISPOSTA:
# Tendenzialmente, abbassando la soglia rendiamo il modello più "severo" (nel caso di nostro dominio, ci da classe "busta" più spesso). In questo modo, ci sfuggono meno fn(falsi negativi), andando così ad alzare la recall. Ma di converso, aumenterebbero i fp (falsi positivi), andando ad abbassare la precision.

# --------------------------------------------------------------------------
# Q8 — 💬 Feynman
# --------------------------------------------------------------------------
# Spiega in 4-6 righe, come se parlassi a un collega sviluppatore che non
# ha mai fatto deep learning, cos'è il transfer learning e perché lo hai
# fatto in due fasi (prima solo la testa, poi anche `layer4`).
# Vincolo: ogni termine tecnico che usi lo spieghi in mezza riga.
# TUA RISPOSTA:
# Immagina questa situazione: hai bisogno di un assistente per aiutarti catalogare e smistare documenti reddituali. Hai due scelte: la prima, prendere un bambino e formarlo partendo dall'insegnargli a leggere e scrivere. Oppure prendere un segretario di uno studio medico, che ha molte competenze trasversali che puoi usare, anche se devi dargli un infarinata sui documenti reddituali. Il transfer learning è come scegliere la seconda opzione. Prendiamo una rete e ne conserviamo il backbone(strati profondi e intermedi) e ricreiamo e addestriamo solo l'head (l'ultimo layer, che si occupa della classificazione finale). Poi, se necessario, possiamo addestrare anche il layer4 (l'ultimo strato convoluzionale, ma con prudenza per non perdere la conoscenza che già ha).


# ==========================================================================
# 🔁 RINFORZO MIRATO — le lacune ancora aperte dal cap.09
# ==========================================================================
#
# Questi blocchi sono corti di proposito. Servono a chiudere quattro cose
# che nel cap.09 erano "quasi giuste": il concetto c'era, la formulazione
# no. E la formulazione conta, perché è quello che ti chiedono a voce in
# un colloquio.


# --------------------------------------------------------------------------
# 🔁 #48 — eval() ≠ freeze ≠ no_grad(): tre leve, tre effetti
# --------------------------------------------------------------------------
#
# Nel cap.09 (Mini 5.3) le hai fuse insieme. Sono TRE interruttori
# indipendenti: puoi accenderne uno e lasciare spenti gli altri due.
#
# Analogia dell'auto in officina:
#
#   requires_grad = False  (FREEZE)
#       "togli le chiavi": il pezzo resta montato e l'auto cammina,
#       ma quel pezzo non verrà più modificato.
#       Tocca: l'AGGIORNAMENTO dei pesi (via .grad che resta None).
#       NON tocca: il forward, che passa comunque per quel layer.
#
#   modello.eval()
#       "spegni la modalità collaudo": due layer si comportano in modo
#       diverso fra training e uso reale —
#         Dropout: in train spegne neuroni a caso, in eval non spegne niente
#         BatchNorm: in train usa media/varianza DEL BATCH, in eval usa le
#                    medie accumulate durante il training (running stats)
#       Tocca: il comportamento di Dropout e BatchNorm.
#       NON tocca: requires_grad, né il grafo di autograd.
#
#   with torch.no_grad():
#       "non registrare il video del viaggio": PyTorch normalmente, mentre
#       fa il forward, costruisce il grafo delle operazioni per poter poi
#       tornare indietro col backward. In inferenza quel grafo è peso
#       morto: memoria occupata per niente.
#       Tocca: la costruzione del grafo (quindi RAM e un po' di velocità).
#       NON tocca: Dropout e BatchNorm, che restano come li hai messi.
#
# La conseguenza pratica, ed è il motivo per cui questo blocco sta in
# questo capitolo: in una demo ti servono eval() E no_grad(), e sono
# entrambi necessari perché fanno cose diverse.
# - Se scordi eval(): la BatchNorm usa le statistiche del "batch" che in
#   demo è UNA immagine sola → predizioni instabili e spesso sbagliate.
#   Questo è il classico bug che NON dà errore, dà solo risultati peggiori.
# - Se scordi no_grad(): funziona, ma sprechi memoria a ogni richiesta.
#   Su uno Space gratuito con RAM contata, si sente.

# 🧩 Mini 48.A — Vero/Falso con motivazione di mezza riga ciascuno.
#   1. `modello.eval()` imposta `requires_grad = False` sui parametri.
#   2. `torch.no_grad()` cambia il comportamento della BatchNorm.
#   3. Con il backbone congelato, il forward salta i layer congelati.
# TUA RISPOSTA:
# 1) Falso. Blocca il Dropout(spegnimento di neuroni casuali ad ogni ciclo) e il Batchnorm (smette di usare la mean e std del batch e usa quella acculata in tutto il training)
# 2) Falso. Smette di tracciare il grafo delle operazioni eseguite nel forward e che occorrono per la backprop.
# 3) Falso. Il backbone congelato significa che non si tiene traccia del gradiente del backbone, e di conseguenza non viene considerato nella retropropagazione.

# 🧩 Mini 48.B — UNA riga di codice (formato: una riga).
# Hai già chiamato `modello.eval()`. Scrivi la riga che apre il contesto
# in cui PyTorch non costruisce il grafo.
# TUA RIGA:

# with torch.no_grad():


# --------------------------------------------------------------------------
# 🔁 #52 — decomporre l'errore di matmul (il metodo, non la risposta)
# --------------------------------------------------------------------------
#
# Nel cap.09 sapevi già mettere la pezza giusta (`fc.in_features`), ma la
# diagnosi a voce restava incompleta. Il metodo è sempre lo stesso e vale
# per QUALSIASI errore di shape: prendi i quattro numeri dell'errore e
# dai un nome a ciascuno. Non si tira a indovinare.
#
#   RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x512 and 256x2)
#                                                             ↑  ↑     ↑  ↑
#                                                             A  B     C  D
#
#   mat1 = quello che ARRIVA al layer.   mat2 = i PESI del layer.
#
#   A = 32   → righe di mat1 = il BATCH. Quante immagini stai passando.
#              Non c'entra nulla con l'architettura: se cambi batch_size
#              cambia questo numero. Va nominato per primo, così lo
#              escludi subito dai sospetti.
#   B = 512  → colonne di mat1 = le FEATURE che il backbone produce.
#              Per ResNet18 dopo avgpool sono 512. È il numero GIUSTO:
#              arriva dall'architettura, non da una tua scelta.
#   C = 256  → righe di mat2 = gli in_features che TU hai dichiarato
#              scrivendo `nn.Linear(256, 2)`. Questo è il bug.
#   D = 2    → colonne di mat2 = out_features = il numero di classi. Giusto.
#
#   Regola di compatibilità: perché il prodotto righe×colonne funzioni,
#   B deve essere uguale a C. 512 ≠ 256 → errore.
#
#   Fix sbagliato:  nn.Linear(512, 2)
#       funziona su resnet18 e si rompe su resnet50 (dove sono 2048).
#       Hai scritto una costante che vale solo per un caso.
#   Fix giusto:     nn.Linear(modello.fc.in_features, 2)
#       leggi il numero DAL modello, prima di sostituire la testa.
#       Vale per qualunque backbone. Questo è già riuso del codice.
#
# ⚠️ Trappola gemella, quella del cap.08: a volte B è sbagliato, non C.
#    Se ti aspettavi 1568 = 32·7·7 e ti arriva 3200 = 32·10·10, non devi
#    cambiare il Linear: ti manca un pooling. Decomponi SEMPRE anche il
#    numero che sembra giusto.

# 🧩 Mini 52.A — tre bullet, uno per numero (formato: tre bullet).
# Errore: (32x512) and (256x2).
# TUA RISPOSTA:
# - 32 = righe della matrice mat1, sono il numero di esempi del batch
# - 512 = colonne della matrice mat1, sono il numero di features per ogni esempio del batch
# - 256 = ... e il fix portabile è: Sono le righe del mat2, ossia le in_features che si aspetta il linear. Si può sistemare componendo il Linear in questo modo: 
# in_features = modello.fc.in_features
# modello.fc = nn.Linear(in_features, 2)


# --------------------------------------------------------------------------
# 🔁 #53 — l'obiezione "sui numeri": come si formula
# --------------------------------------------------------------------------
#
# Nel cap.09 (Mini 6.2) la direzione era giusta ma la frase era generica.
# La differenza fra un'osservazione da junior e una da senior non è il
# concetto: è che la seconda è ANCORATA a un numero verificabile.
#
#   Generica (vera ma inutile):
#       "L'accuracy da sola non basta, guardiamo anche la recall."
#       → chi ti ascolta non può fare nulla con questa frase.
#
#   Ancorata (utile):
#       "Accuracy 89% ma la recall sulla classe positiva è 25/30 = 83%:
#        stiamo perdendo 5 casi su 30. Se il costo di un caso perso è
#        una busta non intercettata, il numero da migliorare è quello,
#        e possiamo comprarlo abbassando la soglia e pagando in precision."
#       → contiene il numero, il costo, la leva e il prezzo della leva.
#
# Lo schema riusabile, in quattro pezzi:
#     [metrica citata + valore] + [quanti casi sono in gioco] +
#     [perché quel caso costa nel dominio] + [quale leva e cosa perdi]

# 🧩 Mini 53.A — UNA frase (formato: una frase sola).
# Scenario: 30 api (classe positiva) nel test, 25 trovate, 5 mancate,
# accuracy globale 0.89. Il project manager festeggia l'89%.
# Scrivi l'obiezione ancorata.
# TUA FRASE:

# Accuracy buona, ma recall sensibilmente più bassa ( 89 % acc e 83 % recall). Siamo sicuri che possiamo permetterci di perdere il 17 % delle api?


# --------------------------------------------------------------------------
# 🔁 avgpool — perché la testa non dipende dalla risoluzione
# --------------------------------------------------------------------------
#
# Residuo del TODO 7 del cap.09: avevi risposto "per il flatten". Il
# flatten c'entra, ma non è lui che salva la situazione.
#
# `nn.AdaptiveAvgPool2d((1,1))` significa: "qualunque sia la griglia che
# ti arriva, restituiscimela ridotta a 1×1". Fa la MEDIA di tutti i valori
# di ogni piano (canale) e produce un solo numero per canale.
#
#   input (8, 512, 7,  7)   → avgpool → (8, 512, 1, 1) → flatten → (8, 512)
#   input (8, 512, 10, 10)  → avgpool → (8, 512, 1, 1) → flatten → (8, 512)
#   input (8, 512, 3,  3)   → avgpool → (8, 512, 1, 1) → flatten → (8, 512)
#
# Il vettore in uscita è sempre lungo 512, cioè quanti sono i CANALI.
# Quindi `in_features` della `fc` dipende dal numero di canali del
# backbone, non da H×W dell'immagine di partenza. È esattamente il motivo
# per cui nel cap.09 una ResNet allenata su 224 accettava 320 senza
# lamentarsi. (Con un limite di buon senso: se scendi troppo, la griglia
# prima di avgpool diventa 1×1 già a metà rete e butti via informazione.)
#
# Analogia: un imbuto. Non gli importa quanta acqua versi sopra, sotto
# esce sempre dello stesso diametro.

# 🧩 Mini AVG — completa.
# `AdaptiveAvgPool2d((1,1))` su `(4, 2048, 12, 12)` → shape __________
# dopo `flatten(1)` → shape __________
# quindi `in_features` della testa è __________ (che architettura è?)
# TUA RISPOSTA:

# `AdaptiveAvgPool2d((1,1))` su `(4, 2048, 12, 12)` → shape (4, 2048, 1, 1)
# dopo `flatten(1)` → shape (4, 2048)
# quindi `in_features` della testa è 2048 (che architettura è? -> resnet50)


# ==========================================================================
# SEZIONE 1 — UN FILE .pt NON È UN MODELLO
#             (il contratto di inferenza)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 1.1 L'esperimento mentale che spiega tutto
# --------------------------------------------------------------------------
#
# Immagina di mandare a un collega, per email, solo questo:
#
#     ants_vs_bees.pt        (45 MB)
#
# Lui lo riceve. È in grado di usarlo? No. E non perché gli manchi la
# competenza: gli mancano delle INFORMAZIONI che non stanno nel file.
#
# Domande a cui il file non risponde:
#
#   1. Che architettura è? Un `state_dict` è un dizionario
#      "nome del parametro → tensore di numeri". Se non sai che era una
#      resnet18, non sai quale scheletro costruire per appenderci i pesi.
#   2. Quante classi e IN CHE ORDINE? Il modello sputa due numeri.
#      Il primo è "ants" o "bees"? Non c'è scritto da nessuna parte.
#   3. Che dimensione di immagine si aspetta? 224? 256? 320?
#   4. Con che normalizzazione? Se in training hai sottratto la media di
#      ImageNet e lui non la sottrae, gli stai dando in pasto immagini in
#      una scala che il modello non ha mai visto.
#   5. Qual è la soglia di decisione? Tu nel cap.09 hai esplorato 0.3-0.7
#      e ne hai scelta una. Quella scelta è parte del modello, non un
#      dettaglio dell'interfaccia.
#   6. Che versione è? Se fra un mese rialleni, come distingue il vecchio
#      dal nuovo, e come sa quali metriche corrispondono a quali pesi?
#
# Queste sei risposte sono il CONTRATTO DI INFERENZA.
#
# Definizione, in una riga: il contratto di inferenza è l'insieme minimo
# di informazioni che servono per riprodurre, su una macchina diversa, le
# stesse predizioni che ottieni tu.
#
# Analogia web: è la differenza fra spedire un file `.sql` e spedire un
# `.sql` più lo schema, la versione del DB e l'encoding. Con il solo dump
# il collega "apre" qualcosa, ma non è detto che ottenga i tuoi dati.
#
# Analogia ancora più terra-terra: il `.pt` è la chiave USB con la
# ricetta scritta in numeri. Il contratto è l'etichetta sulla chiavetta:
# "torta, forno 180°, 40 minuti, teglia da 24". Senza etichetta la
# ricetta è ancora lì, ma nessuno rifà la torta.
#
# --------------------------------------------------------------------------
# 1.2 Le sei voci, una per una, con il danno che fa ognuna se manca
# --------------------------------------------------------------------------
#
# Questa tabella è la parte del capitolo che vale la pena rileggere prima
# di un colloquio. La colonna importante è la terza: COME si manifesta
# l'errore. Perché quasi nessuno di questi bug dà un'eccezione.
#
#  VOCE                 COSA È                        SE SBAGLI / MANCA
#  ─────────────────────────────────────────────────────────────────────
#  architettura         "resnet18"                    Errore ESPLICITO al
#                                                     load: chiavi del
#                                                     state_dict che non
#                                                     combaciano. È il caso
#                                                     fortunato: crasha.
#
#  classi (ordinate)    ["ants", "bees"]              NESSUN errore.
#                                                     Le probabilità sono
#                                                     giuste ma le etichette
#                                                     invertite: la demo dice
#                                                     "ants 93%" quando il
#                                                     modello pensa "bees".
#                                                     Il bug peggiore del
#                                                     capitolo.
#
#  dimensione input     224                           Nessun errore (grazie
#                                                     ad avgpool!). Solo
#                                                     accuratezza che cala,
#                                                     perché il soggetto
#                                                     nell'immagine ha una
#                                                     scala diversa da quella
#                                                     vista in training.
#
#  mean / std           medie di ImageNet             Nessun errore.
#                                                     Probabilità plausibili
#                                                     e sbagliate. Tipico:
#                                                     il modello diventa
#                                                     "sicuro" sempre della
#                                                     stessa classe.
#
#  soglia               0.5, o quella che hai scelto  Nessun errore. Cambia
#                                                     il compromesso
#                                                     recall/precision che
#                                                     avevi deciso a tavolino.
#
#  versione             "v1", data, metriche          Nessun errore. Ma non
#                                                     sai più quale file ha
#                                                     prodotto quali numeri
#                                                     nel tuo README.
#
# Il punto da portarsi via: cinque voci su sei, se sbagliate, NON
# producono un'eccezione. Producono un sistema che risponde con sicurezza
# la cosa sbagliata. In un applicativo di controllo documentale (il tuo
# Validator) questo è il tipo di guasto più costoso che esista, perché
# nessun log si accende.
#
# --------------------------------------------------------------------------
# 1.3 Il caso più insidioso: l'ordine delle classi
# --------------------------------------------------------------------------
#
# Vale la pena fermarsi qui, perché è un errore che farai almeno una volta.
#
# Nel cap.09 hai usato `ImageFolder`, che assegna gli indici alle classi
# in ORDINE ALFABETICO delle cartelle:
#
#     dati/train/ants/   → indice 0
#     dati/train/bees/   → indice 1
#     (class_to_idx == {"ants": 0, "bees": 1})
#
# Il modello quindi produce `logits[0]` = punteggio ants,
# `logits[1]` = punteggio bees.
#
# Ora immagina che nella demo, tre mesi dopo, tu scriva:
#
#     return {"bees": float(prob[0]), "ants": float(prob[1])}      # ⚠️ BUG
#
# Non succede niente di visibile. L'app parte, le barre si disegnano, la
# somma fa 1. Solo che è tutto rovesciato. E se hai messo negli esempi
# una foto di ape, la demo dice "ants 94%" e tu pensi che il modello sia
# venuto male, e magari torni a riallenare. Hai perso una giornata per un
# ordine di dizionario.
#
# Il riparo strutturale (che applichiamo in Sez. 2) è: NON riscrivere mai
# a mano i nomi delle classi nel codice della demo. Salvarli DENTRO il
# checkpoint, nell'ordine giusto, e leggerli da lì. Se il nome delle
# classi vive in un solo posto, non può essere incoerente.
#
# Questo è un principio generale, non un trucco di PyTorch: una singola
# fonte di verità. Lo hai già visto in questo corso — `CONTESTO_CORSO.md`
# è la fonte di verità del corso, e i file capitolo non la duplicano.
#
# --------------------------------------------------------------------------
# 1.4 Perché questo capitolo parla di riuso e non solo di Gradio
# --------------------------------------------------------------------------
#
# Perché "deployare" è solo il primo consumatore del contratto. Gli altri
# arrivano dopo, e sono quelli che contano per il tuo prodotto:
#
#   - il cap.10 di oggi: Gradio, demo pubblica, portfolio
#   - il M4-M7: prototipi Streamlit che potrebbero incorporare lo score
#     visivo insieme a quello testuale
#   - il M10: FastAPI dentro il Validator, dove `prob_busta_paga_visivo`
#     diventa una feature del modello tabellare del M2
#   - te stesso fra sei mesi, che vuoi confrontare un modello nuovo col
#     vecchio e ha bisogno che i due parlino la stessa lingua
#
# Se il contratto è scritto, tutti questi consumatori riusano lo stesso
# modello. Se non lo è, ognuno se lo re-indovina, e prima o poi due
# consumatori lo indovinano in modo diverso.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.1 — elencare il contratto (formato: 6 voci)
# --------------------------------------------------------------------------
# Senza guardare la tabella sopra, scrivi le 6 voci del contratto di
# inferenza. Accanto a ognuna, una parola per dire dove la prendi
# (es. "dal codice del modello", "dal cap.09", "da ImageFolder"...).
# TUA RISPOSTA:
# 1) Architettura del modello (es. resnet18) -> La scelgo io in base al modello utilizzato, scrivendola come stringa.
# 2) Quali classi e in che ordine. -> da ImageFolder
# 3) Quale dimensione di immagine si aspetta -> Scelta in base al training del modello (Imagenet di solito 224 x 224)
# 4) Tipo di normalizzazione -> In base alla media e la std di Imagenet (per modelli tipo resnet 18)
# 5) Soglia -> La decido io
# 6) Versione -> La imposto io in base alla versione del modello, e riassume anche la data e le metriche del modello impostato con quei pesi.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.2 — il bug che non crasha (formato: 2 bullet)
# --------------------------------------------------------------------------
# Fra le sei voci, scegli DUE che, se sbagliate, non generano nessuna
# eccezione. Per ciascuna scrivi in una riga come te ne accorgeresti
# guardando il comportamento della demo (non il codice).
# TUA RISPOSTA:
# - Ordine delle classi -> Se non ho il contratto che mi dice l'indicizzazione delle classi, potrei invertirle, e il modello a quel punto potrebbe dire bees e pensare ants.
# - Tipo di normalizzazione -> potrei usare una normalizzazione sbagliata nelle trasformazioni e a quel punto il modello potrebbe predire con molta sicurezza sempre solo una delle classi.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 1.3
# --------------------------------------------------------------------------
# Un collega ti scrive: "mi passi il modello?" e tu gli mandi solo il .pt.
# Scrivi in 2 righe cosa gli servirebbe ancora, usando le parole del
# contratto, come se stessi rispondendo all'email.
# TUA RISPOSTA:

#Ti ho mandato il .pt con i pesi del modello addestrato: cmq, per il corretto utilizzo e la successiva analisi, ti invierò quanto segue:
# Architettura del modello.
# classi e indicizzazione corretta.
# dimensione delle immagini attese in input.
# normalizzazione per la trasformazione delle immagini.
# soglia selezionata su validation.
# versione e metriche di riferimento.


# ==========================================================================
# SEZIONE 2 — IL CHECKPOINT RICCO
#             (asse 1: rendere riusabile il MODELLO)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 2.1 Ripasso: cosa c'è dentro un state_dict
# --------------------------------------------------------------------------
#
# Dal cap.07: `modello.state_dict()` restituisce un dizionario ordinato
#
#     {
#       "conv1.weight":      tensore (64, 3, 7, 7),
#       "bn1.weight":        tensore (64,),
#       "bn1.bias":          tensore (64,),
#       "bn1.running_mean":  tensore (64,),      ← statistiche BatchNorm!
#       ...
#       "fc.weight":         tensore (2, 512),
#       "fc.bias":           tensore (2,),
#     }
#
# Due cose da notare, perché tornano utili:
#
# a) ci sono dentro anche le `running_mean` / `running_var` della
#    BatchNorm. Non sono "pesi appresi per gradiente", sono statistiche
#    accumulate. Ecco perché `eval()` è indispensabile: quei numeri
#    esistono solo per essere usati in modalità valutazione.
#
# b) le chiavi sono i NOMI dei moduli come li hai definiti. Se domani
#    rinomini un attributo nella tua classe, il vecchio checkpoint non si
#    carica più. Il `state_dict` è accoppiato alla struttura del codice.
#
# --------------------------------------------------------------------------
# 2.2 Le tre strade per salvare, e perché scegliamo la terza
# --------------------------------------------------------------------------
#
#   STRADA A — salvare l'oggetto intero
#       torch.save(modello, "m.pt")
#       torch.load("m.pt")
#
#     Sembra la più comoda: non devi ricostruire l'architettura.
#     È la peggiore per il riuso. Motivo: usa `pickle`, che non salva la
#     CLASSE, salva un RIFERIMENTO alla classe. Al load, Python va a
#     cercare quel modulo e quella classe nel codice. Se hai spostato il
#     file, rinominato la classe, o cambiato versione di torchvision,
#     ottieni un ImportError o un AttributeError.
#     In pratica: funziona sul tuo PC, oggi. Non è un formato di scambio.
#     (Aggiungi che `torch.load` su file pickle di terzi esegue codice:
#      non caricare mai un .pt di provenienza ignota.)
#
#   STRADA B — salvare solo il state_dict (quella del cap.07-09)
#       torch.save(modello.state_dict(), "m.pt")
#
#     Robusta: sono solo tensori. Ma è incompleta: è esattamente il caso
#     della Sez. 1, il file senza etichetta. Il contratto resta nella tua
#     testa o nel messaggio Telegram dove ti sei annotato "224, soglia 0.45".
#
#   STRADA C — salvare un DIZIONARIO: state_dict + metadati
#       torch.save({"model_state": ..., "classi": [...], ...}, "m.pt")
#
#     La scegliamo per un motivo semplice: `torch.save` non salva solo
#     tensori, serializza qualunque struttura Python di base. Quindi puoi
#     mettere nello stesso file i pesi E la sua etichetta.
#     Il file diventa AUTO-DESCRITTIVO: chi lo riceve non ha bisogno di
#     chiederti niente.
#
# Analogia: è la differenza fra un CSV nudo e un CSV dentro uno zip con
# un README accanto che dice separatore, encoding e significato delle
# colonne. Il secondo lo apri fra due anni senza telefonare a nessuno.
#
# --------------------------------------------------------------------------
# 2.3 Che cosa mettere dentro (e cosa no)
# --------------------------------------------------------------------------
#
# DENTRO — tutto ciò che serve per PREDIRE:
#     model_state          i pesi
#     nome_arch            per ricostruire lo scheletro
#     classi               nomi, NELL'ORDINE degli indici
#     dimensione_input     224
#     mean / std           la normalizzazione usata in training
#     soglia               la decisione scelta sul validation set
#     versione_contratto   versione del FORMATO del file
#
# DENTRO, utile ma non indispensabile — la carta d'identità:
#     metriche             accuracy/recall/precision sul test
#     data / commit        quando e da quale codice
#     note                 "proxy ants/bees, NON buste paga"
#
# FUORI — quello che serve per RIPRENDERE IL TRAINING, non per predire:
#     optimizer_state      stato di Adam (momenti). Pesa quanto i pesi e
#                          in una demo non lo usi. Se ti serve per
#                          riprendere un training interrotto, fai un
#                          file separato `..._training.pt`.
#     dataloader, dataset, immagini. Mai.
#
# ⚠️ E soprattutto FUORI: dati personali. Non mettere nel checkpoint
#    percorsi tipo `C:/Users/visaf/buste/rossi_mario_marzo.pdf`, che
#    finirebbero pubblicati insieme al file su HuggingFace. Sembra
#    un'esagerazione: è uno dei modi più comuni in cui i dataset privati
#    si fanno riconoscere.
#
# --------------------------------------------------------------------------
# 2.4 Le due funzioni (codice vero, riusabile)
# --------------------------------------------------------------------------
#
# Nota sullo stile: i parametri dopo `*` sono keyword-only, cioè vanno
# passati per nome. È volontario: `salva_checkpoint(m, p, "resnet18",
# ["a","b"], 224, ...)` sarebbe illeggibile e facilissimo da scambiare
# d'ordine. Con keyword-only il chiamante è obbligato a scrivere
# `classi=[...]`, e il codice si documenta da sé.


def salva_checkpoint(
    modello,
    percorso,
    *,
    nome_arch,
    classi,
    dimensione_input=224,
    mean=None,
    std=None,
    soglia=0.5,
    metriche=None,
    note="",
):
    """Salva pesi + contratto di inferenza in un unico file .pt.

    Il file risultante è auto-descrittivo: chi lo carica non ha bisogno
    di sapere nulla in più per ottenere le stesse predizioni.

    classi: lista di nomi NELL'ORDINE degli indici (class_to_idx).
    soglia: soglia di decisione scelta sul validation set (cap.09).
    """
    if not TORCH_OK:
        raise RuntimeError("Serve torch: pip install torch")

    pacchetto = {
        "versione_contratto": VERSIONE_CONTRATTO,
        "model_state": modello.state_dict(),
        "nome_arch": nome_arch,
        "classi": list(classi),
        "dimensione_input": int(dimensione_input),
        "mean": list(mean) if mean is not None else list(MEAN_IMAGENET),
        "std": list(std) if std is not None else list(STD_IMAGENET),
        "soglia": float(soglia),
        "metriche": dict(metriche) if metriche else {},
        "note": note,
        # str() non è decorativo: torch.__version__ è un oggetto TorchVersion,
        # e un oggetto non-base farebbe fallire il caricamento sicuro
        # (weights_only=True). Vedi 2.6. Nel checkpoint vanno SOLO tipi base.
        "torch_version": str(torch.__version__),
    }

    percorso = Path(percorso)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    torch.save(pacchetto, percorso)
    return percorso


def carica_checkpoint(percorso, device="cpu"):
    """Ricostruisce il modello dal checkpoint ricco e lo mette in eval().

    Ritorna (modello, contratto). Il modello è già pronto per predire:
    sul device richiesto e in modalità valutazione.
    """
    if not TORCH_OK:
        raise RuntimeError("Serve torch: pip install torch")

    # map_location: i tensori salvati da Colab hanno l'etichetta "cuda:0".
    # Senza questo argomento, torch prova ad allocarli su una GPU che qui
    # non esiste → RuntimeError. Con map_location li rimappa su CPU.
    #
    # weights_only=True: caricamento SICURO, spiegato in 2.6. Funziona
    # perché il nostro checkpoint contiene solo tensori e tipi base.
    pacchetto = torch.load(percorso, map_location=device, weights_only=True)

    # Diagnosi gentile invece di un KeyError incomprensibile: se qualcuno
    # passa un checkpoint "vecchio stile" (solo state_dict), diciamo cosa fare.
    if not isinstance(pacchetto, dict) or "model_state" not in pacchetto:
        raise ValueError(
            f"{percorso} non è un checkpoint ricco: sembra un semplice "
            "state_dict. Ricostruisci il contratto a mano (arch, classi, "
            "size, mean/std, soglia) e risalvalo con salva_checkpoint()."
        )

    modello = costruisci_modello(
        nome_arch=pacchetto["nome_arch"],
        num_classi=len(pacchetto["classi"]),
        pesi_pretrained=None,          # i pesi arrivano dal checkpoint
    )
    modello.load_state_dict(pacchetto["model_state"])
    modello.to(device)
    modello.eval()                     # 🔁 #48: BatchNorm in modalità inferenza
    return modello, pacchetto


# --------------------------------------------------------------------------
# 2.5 `strict` e le chiavi che non combaciano
# --------------------------------------------------------------------------
#
# `load_state_dict(..., strict=True)` è il default e vuole corrispondenza
# esatta fra le chiavi del file e quelle del modello. Se non combaciano:
#
#     RuntimeError: Error(s) in loading state_dict for ResNet:
#       Missing key(s) in state_dict: "fc.weight", "fc.bias"
#       Unexpected key(s) in state_dict: "classificatore.0.weight"
#
# Come si legge questo errore (e vale la pena imparare a leggerlo, perché
# è frequentissimo):
#
#   Missing    = il MODELLO ha quel parametro, il FILE non ce l'ha.
#                Tipico: hai cambiato il nome del layer finale.
#   Unexpected = il FILE ha quel parametro, il MODELLO non ce l'ha.
#                Tipico: il file viene da un'architettura diversa.
#
# Se le vedi ENTRAMBE con nomi simmetrici (come sopra: manca `fc`, arriva
# `classificatore`), la diagnosi è quasi sempre "stesso modello, nomi
# diversi": qualcuno ha ribattezzato la testa.
#
# `strict=False` fa passare il load ignorando le differenze, e ti
# restituisce la lista di ciò che non ha caricato:
#
#     esito = modello.load_state_dict(stato, strict=False)
#     print(esito.missing_keys, esito.unexpected_keys)
#
# Serve nel transfer learning (carichi un backbone e ignori la vecchia
# testa a 1000 classi). NON va usato a caso in produzione: con
# `strict=False` un modello a cui non sono stati caricati i pesi della
# testa parte comunque, con la testa inizializzata a caso, e predice
# rumore. Ancora una volta: nessun errore, risultati assurdi.

# --------------------------------------------------------------------------
# 2.6 `weights_only`: il caricamento sicuro (e perché ti riguarda)
# --------------------------------------------------------------------------
#
# Questo pezzo nasce da un errore vero, incontrato mentre scrivevo il
# capitolo. Lo lascio perché è istruttivo.
#
# In Sez. 2.2 dicevamo che `torch.load` usa `pickle`, e che il pickle può
# ESEGUIRE CODICE durante la deserializzazione. Non è teoria: un file
# `.pt` malevolo scaricato da internet può eseguire comandi sulla tua
# macchina nel momento in cui lo carichi. Per questo, da PyTorch 2.6,
# il comportamento di default è cambiato:
#
#     weights_only=True    ← ora è il DEFAULT
#
# Significa: "carica solo tensori e tipi base (dict, list, str, int,
# float, bool), e rifiuta qualunque altro oggetto Python". Il vantaggio
# è che il caricamento non può più eseguire codice arbitrario.
#
# La conseguenza pratica sul nostro checkpoint ricco, ed è il vincolo da
# ricordare:
#
#     dentro il checkpoint devi metterci SOLO tipi base e tensori.
#
# L'errore che ho preso, in forma abbreviata:
#
#     _pickle.UnpicklingError: Weights only load failed.
#     WeightsUnpickler error: Unsupported global:
#         GLOBAL torch.torch_version.TorchVersion was not an allowed global
#
# Causa: avevo salvato `torch.__version__`, che sembra una stringa ma è un
# oggetto `TorchVersion`. Un oggetto → rifiutato. Fix: `str(...)`.
# Stessa cosa succederebbe con un `np.float32`, un `Path`, un `datetime`
# o un `Enum`. Regola: `str()`, `int()`, `float()`, `list()`, `dict()`
# prima di infilare qualcosa nel checkpoint.
#
# E la STRADA A di Sez. 2.2 (salvare l'oggetto modello intero) oggi
# richiederebbe esplicitamente `weights_only=False`, cioè disattivare la
# protezione. Il fatto che PyTorch ti obblighi a scrivere "sì, lo so" per
# usarla dice abbastanza su quanto sia una buona idea.
#
# ⚠️ Retrocompatibilità: `weights_only` esiste come argomento dalla
#    versione 1.13. Se lavori su un ambiente più vecchio, `torch.load`
#    non lo accetta e devi togliere quel parametro.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.1 — dentro o fuori (formato: 2 liste)
# --------------------------------------------------------------------------
# Smista queste voci in DENTRO il checkpoint / FUORI dal checkpoint:
#   optimizer_state · classi · percorsi dei file di training · soglia ·
#   mean/std · immagini del validation · nome_arch · learning rate usato
# TUA RISPOSTA:
# DENTRO:classe, soglia, mean/std, nome_arch, 
# FUORI: optimizer_state, percorsi dei file di training, immagini del validation, lr usato 


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.2 — chiamata reale
# --------------------------------------------------------------------------
# Scrivi la chiamata a `salva_checkpoint(...)` per il tuo modello del
# cap.09: arch resnet18, classi ants/bees nell'ordine di ImageFolder,
# input 224, soglia 0.45, metriche con accuracy 0.889 sul test,
# nota che chiarisce che è un proxy e non buste paga.
# TUO CODICE:

# ckpt = salva_checkpoint(
#     modello = modello_di_prova,
#     percorso = "percorso_di_prova.pt",
#     nome_arch = "resnet18",
#     classi = ["ants", "bees"],
#     dimensione_input=224,
#     mean = [0.485, 0.456, 0.406],
#     std = [0.229, 0.224, 0.225],
#     soglia = 0.45,
#     metriche= {"accuracy": 0.889},
#     note="il modello è stato allenato per la proxy ants vs bees e non su buste paga",
# )

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.3 — leggere l'errore (formato: 2 bullet)
# --------------------------------------------------------------------------
# Ottieni:
#   Missing key(s): "fc.weight", "fc.bias"
#   Unexpected key(s): "head.weight", "head.bias"
# In due bullet: (a) cosa è successo, (b) perché `strict=False` qui
# sarebbe una pessima idea.
# TUA RISPOSTA:
# - il modello ha .fc. Il .pt chiama .head. Segno che probabilmente il linear finale è stato rinominato in .head.
# - sarebbe una pessima idea perchè con strict=False parti con .fc random. La demo funziona ma da risposte casuali.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 2.4 — weights_only (formato: 2 righe)
# --------------------------------------------------------------------------
# Vuoi mettere nel checkpoint anche la data di addestramento.
# Scrivi la riga del dizionario in modo che sopravviva al caricamento
# sicuro, e in una riga di' perché la versione "ovvia"
# (`"data": datetime.now()`) non funzionerebbe.
# TUA RISPOSTA:

# "data": str(datetime.now())

# Non possimo usare oggetti all'interno del contratto, perchè per ragioni di sicurezza il weights_only bloccherebbe la serializzazione.


# ==========================================================================
# SEZIONE 3 — CODICE RIUSABILE
#             (asse 2: funzioni e wrapper invece di script usa-e-getta)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 3.0 Il problema, visto sul tuo codice
# --------------------------------------------------------------------------
#
# Nel cap.09 il tuo `colab_track_prova_ants_bees.py` funziona, ma è uno
# script: costanti dentro le funzioni, percorsi assoluti, chiamate a
# livello di modulo. Va benissimo per una cella Colab. Non è riusabile,
# e si vede da tre sintomi che vale la pena riconoscere:
#
#   1. per cambiare una cosa devi MODIFICARE il codice (non passare un
#      argomento): es. per provare resnet50 devi editare la funzione;
#   2. importare il file ESEGUE il training (side effect all'import);
#   3. la logica di predizione è intrecciata con quella di stampa, quindi
#      non puoi riusarla senza portarti dietro i `print`.
#
# In questa sezione costruiamo i tre pezzi che risolvono i tre sintomi:
# una factory parametrica, una funzione di preprocessing derivata dal
# contratto, e una classe che tiene insieme modello + contratto e non
# stampa niente.
#
# --------------------------------------------------------------------------
# 3.1 La factory del modello (e il TODO 2 del cap.09 finito bene)
# --------------------------------------------------------------------------
#
# Nel cap.09 (TODO 2) eri arrivato vicino: `getattr(models, nome_arch)` e
# `in_features`. Rimaneva un difetto: il default dei pesi era legato a
# ResNet18, quindi `nome_arch="resnet50"` si rompeva.
#
# Due osservazioni che chiudono il problema:
#
# a) `getattr(models, "resnet18")` prende la FUNZIONE costruttrice dal
#    modulo, per nome. È lo stesso meccanismo di `$obj->$metodo()` in PHP
#    o `obj[nome]()` in JS: accesso dinamico a un attributo tramite
#    stringa. Utile qui perché il nome arriva dal checkpoint, cioè da un
#    dato, non da codice scritto a mano.
#
# b) per i pesi pre-addestrati, invece di importare l'enum specifico
#    (`ResNet18_Weights.DEFAULT`, che è legato a una sola architettura),
#    torchvision accetta la stringa `"DEFAULT"`. Vale per tutte le
#    architetture supportate: il problema del default sbagliato sparisce.
#
# E attenzione al terzo caso, che è quello che useremo di più qui:
# `pesi_pretrained=None` significa "costruisci lo scheletro con pesi
# casuali". In questo capitolo è esattamente ciò che vogliamo: i pesi
# buoni arrivano subito dopo dal checkpoint, e scaricare quelli di
# ImageNet sarebbe 45 MB di rete buttati (su uno Space, secondi di boot
# in più a ogni riavvio).


def costruisci_modello(nome_arch="resnet18", num_classi=2, pesi_pretrained=None):
    """Costruisce un modello torchvision con la testa adattata a num_classi.

    nome_arch: "resnet18", "resnet34", "resnet50", ...
    pesi_pretrained:
        None        → scheletro con pesi casuali (caso INFERENZA: i pesi
                      arrivano poi dal checkpoint)
        "DEFAULT"   → pesi pre-addestrati su ImageNet (caso TRAINING,
                      cioè quello che hai fatto nel cap.09)
    """
    if not VISION_OK:
        raise RuntimeError("Serve torchvision: pip install torchvision")

    costruttore = getattr(models, nome_arch, None)
    if costruttore is None:
        raise ValueError(
            f"Architettura '{nome_arch}' non trovata in torchvision.models. "
            "Esempi validi: resnet18, resnet34, resnet50."
        )

    modello = costruttore(weights=pesi_pretrained)

    # 🔁 #52: si LEGGE il numero dal modello, non si scrive a mano.
    # Su resnet18 vale 512, su resnet50 vale 2048: il codice non cambia.
    n_ingressi = modello.fc.in_features
    modello.fc = nn.Linear(n_ingressi, num_classi)
    return modello


# ⚠️ Limite dichiarato di questa funzione: assume che la testa si chiami
#    `fc`, cosa vera per le ResNet ma non per tutte le reti (in `vgg16` e
#    `efficientnet` si chiama `classifier`, in alcuni `head`). Dichiarare
#    i limiti di una funzione riusabile fa parte del lavoro: chi la riusa
#    deve sapere dove smette di valere. Estenderla è il TODO 4.

# --------------------------------------------------------------------------
# 3.2 Il preprocessing DERIVATO dal contratto
# --------------------------------------------------------------------------
#
# Qui c'è il punto più importante di tutta la sezione, e conviene dirlo
# in modo netto:
#
#     il preprocessing non è un dettaglio dell'interfaccia.
#     È parte del modello.
#
# Un modello addestrato su immagini normalizzate con le medie di ImageNet
# è una funzione che accetta quel tipo di input. Cambiargli il
# preprocessing è come cambiare unità di misura a un'equazione fisica:
# i numeri escono, ma non significano più niente.
#
# Perciò `transform_eval` NON ha valori scritti dentro: prende
# `dimensione`, `mean` e `std` come argomenti, e chi la chiama li legge
# dal checkpoint. Così è impossibile che il preprocessing della demo
# divergano da quello del training: vengono dalla stessa fonte.
#
# Sul perché `Resize(256)` seguito da `CenterCrop(224)` invece di un
# `Resize((224,224))` diretto:
#   - `Resize(256)` su un intero ridimensiona il LATO CORTO a 256 e
#     mantiene le proporzioni. Nessuna deformazione.
#   - `CenterCrop(224)` taglia il quadrato centrale.
#   - `Resize((224,224))` con una tupla invece SCHIACCIA l'immagine sui
#     due lati, cambiando le proporzioni del soggetto.
# Il rapporto 256/224 non è casuale: è la convenzione usata in training
# su ImageNet, e la usi in eval per coerenza (questo è il ragionamento
# del cap.09 su CenterCrop deterministico in valutazione).


def transform_eval(dimensione=224, mean=None, std=None):
    """Pipeline di preprocessing per l'INFERENZA (deterministica).

    Nessuna casualità: stessa immagine → sempre stesso tensore.
    Tutti i parametri arrivano dal contratto, non sono hardcoded.
    """
    if not VISION_OK:
        raise RuntimeError("Serve torchvision: pip install torchvision")

    mean = list(mean) if mean is not None else list(MEAN_IMAGENET)
    std = list(std) if std is not None else list(STD_IMAGENET)

    # Mantiene la proporzione 256/224 della convenzione ImageNet anche se
    # la dimensione target cambia (es. 160 → resize 183 → crop 160).
    lato_resize = int(round(dimensione * 256 / 224))

    return transforms.Compose([
        transforms.Resize(lato_resize),      # lato corto, proporzioni salve
        transforms.CenterCrop(dimensione),   # quadrato centrale, deterministico
        transforms.ToTensor(),               # PIL → tensore (C,H,W) in [0,1]
        transforms.Normalize(mean=mean, std=std),
    ])


# --------------------------------------------------------------------------
# 3.3 Il wrapper: una classe che tiene insieme le due metà
# --------------------------------------------------------------------------
#
# Abbiamo un modello e un contratto. Se li lasciamo come due variabili
# sciolte, prima o poi qualcuno userà il modello A con il contratto B.
# Tenerli insieme in un oggetto non è formalismo: è il modo di rendere
# impossibile quella combinazione sbagliata.
#
# Tre scelte di progetto, che vale la pena capire perché sono
# trasferibili a qualunque altro servizio che scriverai:
#
# 1) CARICAMENTO PIGRO (lazy). Il modello si carica alla prima
#    predizione, non nel costruttore. Motivo pratico: su Spaces l'app
#    deve rispondere all'health check in fretta; se il costruttore
#    impiega 8 secondi a leggere 45 MB, il container sembra bloccato.
#    Motivo di test: puoi istanziare la classe nei test senza avere il
#    file dei pesi a disposizione.
#
# 2) CARICAMENTO UNA VOLTA SOLA. `if self._modello is None` fa sì che
#    dalla seconda richiesta in poi si riusi quello in memoria. Sembra
#    ovvio, ed è l'errore di performance numero uno nelle demo ML:
#    ricaricare i pesi a ogni click. Passi da ~20 ms a ~2 s per
#    predizione, e non capisci perché la demo è lenta.
#
# 3) NIENTE print, NIENTE Gradio, NIENTE FastAPI dentro. La classe
#    restituisce dati (dizionari). Chi la usa decide se stamparli,
#    disegnarli come barre o serializzarli in JSON. È questa separazione
#    che ti permette, in Sez. 9, di riusarla da FastAPI senza toccare
#    una riga.


class ClassificatoreVisivo:
    """Modello + contratto insieme, pronto per essere riusato.

    Uso:
        clf = ClassificatoreVisivo("dati/pesi/ants_vs_bees.pt")
        clf.predict_proba(immagine_pil)     # {"ants": 0.07, "bees": 0.93}
        clf.predict_etichetta(immagine_pil) # + etichetta e soglia applicata
    """

    def __init__(self, percorso_checkpoint, device="cpu"):
        self.percorso = Path(percorso_checkpoint)
        self.device = device
        self._modello = None
        self._contratto = None
        self._trasformazione = None

    # -- caricamento -------------------------------------------------------

    def carica(self):
        """Carica pesi e contratto la PRIMA volta; poi non fa nulla."""
        if self._modello is None:
            if not self.percorso.exists():
                raise FileNotFoundError(
                    f"Checkpoint non trovato: {self.percorso}\n"
                    "Su HuggingFace Spaces ricordati che la working dir è "
                    "la radice dello Space: usa percorsi relativi al file app.py."
                )
            self._modello, self._contratto = carica_checkpoint(
                self.percorso, device=self.device
            )
            self._trasformazione = transform_eval(
                dimensione=self._contratto["dimensione_input"],
                mean=self._contratto["mean"],
                std=self._contratto["std"],
            )
        return self

    # -- lettura del contratto --------------------------------------------

    @property
    def classi(self):
        """Nomi delle classi nell'ordine degli indici (dal checkpoint)."""
        return list(self.carica()._contratto["classi"])

    @property
    def soglia(self):
        return float(self.carica()._contratto["soglia"])

    @property
    def classe_positiva(self):
        """Convenzione del corso: l'ultima classe è la positiva.

        Con ImageFolder alfabetico: altro=0 / busta_paga=1, ants=0 / bees=1.
        La convenzione è dichiarata qui, in un solo posto.
        """
        return self.classi[-1]

    def scheda(self):
        """Contratto senza i pesi: utile da mostrare in UI o in un /info."""
        contratto = dict(self.carica()._contratto)
        contratto.pop("model_state", None)
        return contratto

    # -- predizione --------------------------------------------------------

    def predict_proba(self, immagine_pil):
        """Probabilità per classe. Ritorna {nome_classe: probabilità}."""
        self.carica()

        # convert("RGB") non è decorativo: vedi Sez. 5.1. Gestisce PNG con
        # canale alfa (4 canali) e scansioni in scala di grigi (1 canale),
        # che altrimenti fanno esplodere il primo Conv2d che vuole 3 canali.
        immagine_rgb = immagine_pil.convert("RGB")

        tensore = self._trasformazione(immagine_rgb)      # (3, H, W)
        batch = tensore.unsqueeze(0).to(self.device)      # (1, 3, H, W)

        with torch.no_grad():                             # 🔁 #48
            logits = self._modello(batch)                 # (1, num_classi)
            probabilita = torch.softmax(logits, dim=1)[0]  # (num_classi,)

        return {
            nome: float(valore)
            for nome, valore in zip(self.classi, probabilita)
        }

    def predict_etichetta(self, immagine_pil, soglia=None):
        """Applica la soglia del contratto e restituisce la decisione."""
        probabilita = self.predict_proba(immagine_pil)
        soglia_usata = self.soglia if soglia is None else float(soglia)

        nome_positiva = self.classe_positiva
        p_positiva = probabilita[nome_positiva]
        etichetta = nome_positiva if p_positiva >= soglia_usata else self.classi[0]

        return {
            "etichetta": etichetta,
            "probabilita": probabilita,
            "classe_positiva": nome_positiva,
            "p_positiva": p_positiva,
            "soglia": soglia_usata,
        }


# --------------------------------------------------------------------------
# 3.4 Dove sono finite le tre leve (🔁 #48 in pratica)
# --------------------------------------------------------------------------
#
# Nel codice sopra le leve ci sono tutte e tre, in tre posti diversi.
# Vale la pena vederle "in situ", perché è la forma in cui le troverai
# in qualunque servizio di inferenza:
#
#   freeze (requires_grad=False)
#       NON c'è. Ed è corretto: il freeze serviva durante il TRAINING
#       (cap.09, fase 1) per non aggiornare il backbone. Qui non si
#       aggiorna niente per definizione, quindi non serve.
#
#   eval()
#       in `carica_checkpoint`, subito dopo il load. Messo LÌ e non nel
#       predict per un motivo: è una proprietà dello stato del modello,
#       non dell'operazione. Lo imposti una volta e resta.
#
#   no_grad()
#       in `predict_proba`, intorno al forward. Messo LÌ e non altrove
#       perché è un CONTESTO: vale solo per il blocco che racchiude.
#
# Riassunto operativo da tenere a mente: eval() è uno stato, no_grad() è
# un contesto. Per questo uno si chiama sull'oggetto e l'altro con `with`.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.1 — perché None (formato: 2 righe)
# --------------------------------------------------------------------------
# In `carica_checkpoint` chiamiamo `costruisci_modello(..., pesi_pretrained=None)`.
# Spiega in due righe perché scaricare i pesi ImageNet qui sarebbe uno
# spreco, e cosa succederebbe comunque ai pesi ImageNet un attimo dopo.
# TUA RISPOSTA:
# sarebbe uno spreco perchè poco dopo nella funzione facciamo il load dello state_dict con i pesi aggiornati (compresi quelli del backbone). In pratica scaricheremmo inutilmente qualcosa che già abbiamo e inseriamo cmq subito dopo.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.2 — caricamento pigro
# --------------------------------------------------------------------------
# Cosa cambia, in termini di tempo di risposta, fra caricare il modello
# nel `__init__` e caricarlo alla prima `predict`? Rispondi distinguendo
# la PRIMA richiesta dalle SUCCESSIVE (2 righe).
# TUA RISPOSTA: cambia per lo space, perchè caricandolo nell'__init__ l'healt cheack impiega troppi secondi. Caricandolo alla prima predict bypassiamo questo inconveniente, fermo restando che dobbiamo evitare che il modello venga ricaricato ad ogni predizione inserendo nel metodo carica una condizione che veda prima se il modello è ancora inizializzato su none oppure già abbiamo fatto la prima predizione e lo abbiamo effettivamente caricato.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.3 — trova il difetto di riuso
# --------------------------------------------------------------------------
# Questa funzione "funziona". Elenca TRE motivi per cui non è riusabile,
# riferendoti ai tre sintomi di 3.0:
#
#     def predici(percorso_immagine):
#         m = models.resnet18(weights="DEFAULT")
#         m.fc = nn.Linear(512, 2)
#         m.load_state_dict(torch.load("C:/Users/visaf/pesi/ants.pt"))
#         img = Image.open(percorso_immagine)
#         t = transforms.Compose([transforms.Resize((224, 224)),
#                                 transforms.ToTensor()])(img)
#         print(m(t.unsqueeze(0)).argmax().item())
#
# TUA RISPOSTA:

def crea_predittore(percorso_ckpt, device="cpu"):
    modello, contratto = carica_checkpoint(percorso_ckpt, device)
    transform = transform_eval(
        dimensione = contratto['dimensione_input'],
        mean = contratto['mean'],
        std = contratto['std']
    )
    classi = contratto["classi"]

    def predici(immagine_pil):
        img = immagine_pil.convert("RGB")
        tensore = transform(img)
        tensore = tensore.unsqueeze(0).to(device)
        with torch.no_grad():
            logits = modello(tensore)
            probabilita = torch.softmax(logits, dim=1)[0]
            return {nome: float(p) for nome, p in zip(classi, probabilita)}
    return predici

# predici = crea_predittore("dati/pesi/ants_vs_bees.pt")

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 3.4 — eval è stato, no_grad è contesto (1 riga)
# --------------------------------------------------------------------------
# Spiega in una riga perché `eval()` si chiama una volta sola sul modello
# mentre `no_grad()` va aperto ogni volta che predici.
# TUA RISPOSTA:
# eval() si chiama solo una volta sola sul modello per metterlo in modalita' valutazione .Il modello in pratica smette di usare il Batchnorm cominciando a utilizzare running_mean e running_var per normalizzare gli input.
# with torch.no_grad() wrappa il forward, e fa smettere autograd di tracciare il grafo delle operazioni, risparmiando vram in fase di valutazione (non dobbiamo in questo caso aggiornare i pesi). Si attiva ogni volta che viene lanciato un forward per fare una previsione.


# ==========================================================================
# SEZIONE 4 — GRADIO: ANATOMIA
# ==========================================================================
#
# --------------------------------------------------------------------------
# 4.1 Che problema risolve Gradio
# --------------------------------------------------------------------------
#
# Tu sai fare frontend. Quindi la domanda giusta non è "come funziona
# Gradio", è "perché non mi scrivo una pagina e basta?".
#
# Se dovessi mostrare il tuo modello a qualcuno senza Gradio, ti
# servirebbe: un backend con un endpoint che accetta multipart/form-data,
# la gestione del file temporaneo, una pagina HTML con un input file, un
# po' di JS per la fetch e per disegnare le probabilità, il CORS, e un
# server da mettere online. Mezza giornata, e non hai imparato niente di
# nuovo sul modello.
#
# Gradio genera tutto quel pezzo da una funzione Python:
#
#     gr.Interface(fn=predici, inputs="image", outputs="label")
#
# Legge la firma, costruisce il widget di upload, chiama la tua funzione,
# prende il valore di ritorno e lo disegna nel componente giusto.
#
# Analogia con quello che conosci: è un'impalcatura tipo `php artisan
# make:resource` o un Laravel Nova, ma per una funzione di inferenza.
# Non "fa il sito": fa la vetrina di UNA funzione.
#
# Confronto con Streamlit (che hai usato nel M2 cap.06-07):
#
#   Streamlit  = app a pagina intera, si riesegue lo script da cima a
#                fondo a ogni interazione, pensata per dashboard con
#                grafici, filtri, tabelle, più pagine.
#   Gradio     = vetrina di una funzione: input → fn → output. Ha già i
#                componenti tipici del ML (immagine, audio, etichette con
#                barre di probabilità, esempi cliccabili) e nasce
#                integrato con HuggingFace Spaces.
#
# Nessuno dei due è "meglio": per il tuo Validator, che è una app con
# più schermate, Streamlit (e poi React nel M10) è più adatto. Per
# mostrare un classificatore di immagini in un portfolio, Gradio ti fa
# arrivare all'URL in dieci minuti.
#
# --------------------------------------------------------------------------
# 4.2 I tre argomenti di Interface
# --------------------------------------------------------------------------
#
#     gr.Interface(fn=..., inputs=..., outputs=...)
#
#   fn       la tua funzione Python. Gradio la chiama passandole i valori
#            dei componenti di input, nell'ordine.
#   inputs   uno o più componenti in ingresso.
#   outputs  uno o più componenti in uscita.
#
# La regola da tenere a mente, che spiega il 90% degli errori da
# principiante: il NUMERO e l'ORDINE dei componenti devono combaciare con
# i parametri della funzione e con i suoi valori di ritorno.
#
#     def predici(immagine, soglia):            # due parametri
#         ...
#         return etichette, testo               # due ritorni
#
#     gr.Interface(fn=predici,
#                  inputs=[gr.Image(type="pil"), gr.Slider(0, 1)],   # due
#                  outputs=[gr.Label(), gr.Textbox()])               # due
#
# Se ne metti tre in `inputs` e la funzione accetta due parametri, ottieni
# un TypeError al primo click, non all'avvio: l'errore non compare nel
# log di build, compare quando qualcuno usa la demo.
#
# --------------------------------------------------------------------------
# 4.3 I componenti sono TIPIZZATI (la parte che si sbaglia)
# --------------------------------------------------------------------------
#
# `gr.Image` non consegna sempre la stessa cosa. Dipende da `type`:
#
#     gr.Image(type="pil")      → la fn riceve un PIL.Image
#     gr.Image(type="numpy")    → la fn riceve un np.ndarray (H, W, C) uint8
#     gr.Image(type="filepath") → la fn riceve una stringa: percorso del
#                                 file temporaneo su disco
#
# Noi usiamo `type="pil"` per un motivo preciso: le `transforms` di
# torchvision sono nate per lavorare su immagini PIL, e `convert("RGB")`
# è un metodo di PIL. Se prendessi `numpy`, dovresti convertire a mano e
# ti troveresti a gestire il caso (H,W,C) uint8 → (C,H,W) float, che è
# esattamente il lavoro che `ToTensor()` fa già per te.
#
# ⚠️ Trappola dei canali, ed è la stessa lacuna #49 del cap.08-09 vista
#    da un'altra porta: `numpy` ti dà (H, W, C), PyTorch vuole (C, H, W).
#    Con `type="pil"` + `ToTensor()` la conversione è inclusa e non devi
#    ricordarti l'ordine degli assi.
#
# `gr.Label` in uscita accetta:
#     - una stringa      → mostra solo quell'etichetta
#     - un dizionario {nome: probabilità} → mostra le barre ordinate
# Il secondo caso è quello che vogliamo, ed è il motivo per cui
# `predict_proba` restituisce un dizionario e non un `argmax`: un indice
# non dice niente all'utente, una barra all'87% sì.
# `num_top_classes=2` limita quante barre disegnare (utile con 1000 classi).
#
# --------------------------------------------------------------------------
# 4.4 Interface o Blocks
# --------------------------------------------------------------------------
#
# `Interface` è la scorciatoia: layout deciso da Gradio (input a
# sinistra, output a destra). Va benissimo per "una funzione, un
# risultato", che è il nostro caso.
#
# `Blocks` serve quando vuoi decidere il layout o collegare più eventi:
#
#     with gr.Blocks() as demo:
#         gr.Markdown("## Titolo e disclaimer")
#         with gr.Row():
#             immagine = gr.Image(type="pil")
#             esito = gr.Label(num_top_classes=2)
#         bottone = gr.Button("Analizza")
#         bottone.click(fn=predici, inputs=immagine, outputs=esito)
#
# La differenza concettuale, in termini web: `Interface` è uno scaffold
# generato, `Blocks` è scrivere il template a mano. Il `bottone.click(...)`
# è l'equivalente di un `addEventListener`: colleghi un evento a una
# funzione dichiarando cosa entra e cosa esce.
#
# Per questo capitolo `Interface` basta e avanza. `Blocks` te lo segno
# perché quando nel M10 vorrai una UI con più controlli, è quella la
# strada (o React, che è il piano vero per il prodotto).
#
# --------------------------------------------------------------------------
# 4.5 Examples: la cosa che fa la differenza in un portfolio
# --------------------------------------------------------------------------
#
#     gr.Interface(..., examples=["esempi/ape1.jpg", "esempi/formica1.jpg"])
#
# Perché conta più di quanto sembri: un recruiter apre il tuo Space, vede
# una casella di upload vuota, non ha una foto di formica sul desktop,
# chiude. Con gli esempi clicca e vede il modello funzionare in due
# secondi.
#
# `cache_examples=True` esegue le predizioni sugli esempi al momento del
# build e memorizza i risultati: i primi click diventano istantanei.
# Costo: il build dura qualche secondo in più.
#
# ⚠️ PRIVACY, e qui è un vincolo del corso, non un consiglio: gli esempi
#    sono file COMMITTATI nel repository dello Space, quindi pubblici e
#    scaricabili. Nel track prova sono formiche e api, nessun problema.
#    Nel track prodotto (buste paga) gli esempi devono essere documenti
#    finti o sintetici. Una busta reale, anche anonimizzata, non va in un
#    repository pubblico: è la regola R3 del cap.09.
#
# --------------------------------------------------------------------------
# 4.6 launch(): i parametri che servono davvero
# --------------------------------------------------------------------------
#
#     demo.launch()                      # locale, http://127.0.0.1:7860
#     demo.launch(share=True)            # tunnel pubblico temporaneo (~72h)
#     demo.launch(server_name="0.0.0.0") # ascolta su tutte le interfacce
#     demo.launch(server_port=7861)      # se la 7860 è occupata
#
# Tre note operative:
#
# a) `share=True` crea un URL pubblico temporaneo passando da un tunnel
#    di Gradio. Comodissimo per far provare qualcosa a un collega in
#    cinque minuti. Non è un deploy: scade, e il traffico passa dal tuo PC.
#
# b) su HuggingFace Spaces NON serve nessun parametro: la piattaforma si
#    aspetta un oggetto `demo` e lo serve lei. Anzi, `share=True` là
#    dentro è inutile e va lasciato via.
#
# c) `demo.launch()` NON va eseguito a livello di modulo in un file che
#    qualcuno potrebbe importare: si avvierebbe un server per il solo
#    fatto di aver fatto `import`. Si mette sotto
#    `if __name__ == "__main__":`. È lo stesso errore strutturale che
#    aveva il tuo `colab_track_prova_ants_bees.py` con il training.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.1 — Interface minima
# --------------------------------------------------------------------------
# Scrivi 4-5 righe: una `Interface` che prende un numero e restituisce il
# suo quadrato. (Componenti: `gr.Number`.)
# TUO CODICE:
# interfaccia = gr.Interface(fn=lambda x: x**2, inputs= gr.Number(), outputs=gr.Number())
# if __name__ == "__main__"
#   interfaccia.launch()


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.2 — V/F + motivo (formato: una riga di motivo)
# --------------------------------------------------------------------------
# "`gr.Label` vuole l'etichetta secca vincente; per mostrare le
#  probabilità serve un componente diverso."
# TUA RISPOSTA:
# Falso: dipende se in uscita dalla funzione c'è una stringa o un dizionario. Se c'è il dizionario con tutte le classi, mostra le barre di tutte le classi in ordine.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.3 — type dell'immagine (formato: 2 bullet)
# --------------------------------------------------------------------------
# Perché scegliamo `gr.Image(type="pil")` e non `type="numpy"`?
# Un bullet sul preprocessing, uno sull'ordine degli assi.
# TUA RISPOSTA:
# - Il preprocessing di torch si aspetta un immagile di tipo PIL, non direttamente un tensore numpy.
#  - Scegliendo numpy dovremmo occuparci di invertire l'ordine in cui si trovano i canali nel tensore ( (H, W, C) -> (C, H, W).


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 4.4
# --------------------------------------------------------------------------
# Il tuo Space mostra la demo ma al primo click ottieni
# `TypeError: predici() takes 1 positional argument but 2 were given`.
# In una riga: dove guardi e perché.
# TUA RISPOSTA:
# Guarderei gli input passati tramite gr.Interface() se coincidono con quelli richiesti dalla funzione predici(). E' il classico errore in cui si rischia di incappare, ossia gli argomenti passati devono essere lo stesso numero che la funzione si aspetta e nello stesso ordine.

# ==========================================================================
# SEZIONE 5 — predict() END-TO-END
# ==========================================================================
#
# --------------------------------------------------------------------------
# 5.1 Il primo passo che tutti saltano: convert("RGB")
# --------------------------------------------------------------------------
#
# L'utente carica quello che vuole. In pratica arriva:
#
#     - JPEG a 3 canali          → RGB, il caso normale
#     - PNG con trasparenza      → RGBA, QUATTRO canali
#     - scansione in grigio      → modalità "L", UN canale
#     - immagine con profilo CMYK → quattro canali di altro tipo
#
# Il primo `Conv2d` della ResNet ha pesi di shape (64, 3, 7, 7): il `3`
# è il numero di canali che si aspetta. Se gliene arrivano 4 o 1, il
# prodotto non si può fare e ottieni un errore di shape.
#
# `immagine.convert("RGB")` normalizza tutti quei casi a tre canali:
# butta il canale alfa e replica il grigio sui tre canali.
#
# Nota il collegamento con la lacuna #49 del cap.09 (Mini 3.1): là la
# domanda era "come porto un TENSORE (N,1,H,W) a 3 canali?" e la risposta
# era `x.repeat(1, 3, 1, 1)`. Qui la domanda è "come porto un'IMMAGINE
# PIL a 3 canali?" e la risposta è `convert("RGB")`. Due strumenti
# diversi perché operano su due oggetti diversi: uno sul tensore, uno
# sull'immagine prima che diventi tensore. È esattamente il discrimine
# che nel cap.09 era rimasto fragile.
#
# Nota pratica sui documenti (track prodotto): una busta paga scansionata
# è spesso in grigio. `convert("RGB")` la triplica, e va bene: il modello
# pre-addestrato su ImageNet vuole 3 canali e non si offende se sono
# identici.
#
# --------------------------------------------------------------------------
# 5.2 Perché Normalize, e perché con QUEI numeri
# --------------------------------------------------------------------------
#
# `ToTensor()` porta i pixel da 0-255 a 0-1. Poi `Normalize(mean, std)`
# fa, per ogni canale:
#
#     valore_normalizzato = (valore - mean_canale) / std_canale
#
# È lo stesso `(X - media) / deviazione` dello StandardScaler del M2:
# centri intorno a zero e porti la dispersione a circa 1. Lo hai già
# incontrato, e c'era anche un pattern di errore tuo sulle parentesi
# (#43): `X - mean / std` è sbagliato, `(X - mean) / std` è giusto.
#
# I numeri `[0.485, 0.456, 0.406]` e `[0.229, 0.224, 0.225]` non sono
# magici: sono la media e la deviazione standard dei canali R, G, B
# calcolate su ImageNet, il dataset su cui la ResNet è stata
# pre-addestrata. Il modello ha imparato tutti i suoi pesi vedendo
# immagini in quella scala. Presentargliene altre è come dare a una
# funzione tarata sui metri dei valori in pollici: risponde, e risponde
# male.
#
# Cosa vedi concretamente se sbagli la normalizzazione (caso reale,
# tipico): il modello resta "sicuro" ma quasi sempre della stessa classe,
# tipo 0.98 su tutto. Nessuna eccezione, nessun log. È il motivo per cui
# in Sez. 3.2 `mean` e `std` arrivano dal checkpoint: così non possono
# divergere da quelli del training.
#
# --------------------------------------------------------------------------
# 5.3 unsqueeze(0): il batch da una sola immagine
# --------------------------------------------------------------------------
#
# Il modello vuole sempre `(N, C, H, W)` — questo lo hai consolidato nel
# cap.08. Anche per una sola immagine: N = 1.
#
#     tensore = trasformazione(img)      # (3, 224, 224)     ← tre assi
#     batch   = tensore.unsqueeze(0)     # (1, 3, 224, 224)  ← quattro assi
#
# `unsqueeze(0)` inserisce un asse di dimensione 1 in posizione 0.
# L'inverso è `squeeze()`, che togli gli assi di dimensione 1 (quello che
# usavi per `plt.imshow`).
#
# Se lo dimentichi, l'errore è esplicito e si legge bene:
#     Expected 4-dimensional input for 4-dimensional weight [64,3,7,7],
#     but got 3-dimensional input of size [3, 224, 224] instead
# "Expected 4-dimensional, got 3-dimensional" → manca il batch.
#
# --------------------------------------------------------------------------
# 5.4 Da logits a probabilità: softmax, e perché non argmax
# --------------------------------------------------------------------------
#
# Il modello restituisce LOGITS: punteggi grezzi, tipo `[-1.2, 2.8]`.
# Non sono probabilità: possono essere negativi e non sommano a 1.
#
# Ricorda dal cap.08 perché: la `CrossEntropyLoss` applica `log_softmax`
# al suo interno, quindi durante il training il modello non ha mai avuto
# bisogno di produrre probabilità. In inferenza la conversione la devi
# fare tu:
#
#     probabilita = torch.softmax(logits, dim=1)
#
# `dim=1` perché vuoi che la somma faccia 1 lungo l'asse delle CLASSI,
# per ogni riga del batch. Con `dim=0` normalizzeresti fra immagini
# diverse dello stesso batch, che non ha alcun senso.
#
# Tre alternative e quando usarle:
#     argmax                → solo l'indice del vincitore. Perde la
#                             confidenza: 51% e 99% diventano identici.
#     softmax (2+ classi)   → distribuzione sulle classi. È il nostro caso.
#     sigmoid (1 logit)     → se avessi fatto un'uscita singola con
#                             BCEWithLogitsLoss, come nel M2/cap.07.
#
# Per una demo honesta la confidenza va MOSTRATA. "Ape 51%" e "Ape 99%"
# sono due situazioni molto diverse per chi guarda, e nascondere la
# differenza è esattamente il modo in cui le demo ML ingannano.
#
# --------------------------------------------------------------------------
# 5.5 E la soglia?
# --------------------------------------------------------------------------
#
# Nel cap.09 hai esplorato le soglie da 0.3 a 0.7 guardando come si
# muovevano precision e recall. Quella scelta va portata fin qui,
# altrimenti l'hai fatta per niente.
#
# Attenzione a non confondere due cose:
#
#   - le PROBABILITÀ mostrate all'utente: sempre quelle vere del softmax,
#     senza ritocchi;
#   - la DECISIONE binaria ("è un'ape / non lo è"): dipende dalla soglia.
#
# Con due classi, `argmax` equivale a una soglia di 0.5. Se nel cap.09
# avevi scelto 0.45 perché ti serviva più recall, allora `argmax` NON è
# la tua regola di decisione, e usarlo in demo significa applicare
# silenziosamente una soglia diversa da quella dichiarata.
#
# Per questo `predict_etichetta` (Sez. 3.3) prende la soglia dal
# contratto, e nel README della demo la scrivi. Un utente che vede
# "soglia 0.45, scelta per privilegiare la recall" capisce che cosa sta
# guardando; uno che vede solo un'etichetta, no.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.1 — prevedi le shape
# --------------------------------------------------------------------------
# Immagine PIL RGB 400×300, contratto con dimensione_input=224.
# Scrivi la shape dopo OGNI passaggio (una riga per passaggio):
#   convert("RGB") → Resize → CenterCrop → ToTensor → unsqueeze(0)
# TUA RISPOSTA:
# dopo convert("RGB") -> 400×300          (ancora PIL, W×H; non è un tensore)
# dopo Resize         -> 341×256          (PIL, W×H; lato corto 300→256)
# dopo CenterCrop     -> 224×224          (PIL)
# dopo ToTensor       -> (3, 224, 224)    (C, H, W)
# dopo unsqueeze      -> (1, 3, 224, 224) (N, C, H, W)

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.2 — dim del softmax (formato: 1 riga)
# --------------------------------------------------------------------------
# Su logits di shape (4, 2), cosa cambia fra `softmax(dim=1)` e
# `softmax(dim=0)`? Quale è quello giusto e perché.
# TUA RISPOSTA:
# Se i logits arrivano in questa shape, significa che sono 4 righe, per ognuna 2 classi. 
# Dunque l'asse 0 è l'asse delle righe degli esempi, mentre l'asse 1 riguarda le classi.
# softmax(dim=0) confronterebbe portando a somma 1 le righe per ogni classe, e non avrebbe senso. Mentre facendolo su dim=1 per ogni riga riporterebbe a somma 1 le classi per ogni riga, che è esattamente quello che vogliamo.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.3 — il bug silenzioso (formato: 2 bullet)
# --------------------------------------------------------------------------
# Un collega toglie `Normalize` dalla pipeline di inferenza "perché
# tanto ToTensor già porta tutto fra 0 e 1".
# Un bullet: perché il codice non dà errore.
# Un bullet: cosa vedresti nelle probabilità.
# TUA RISPOSTA:
# - Non da errore perchè effettivamente to tensor trasforma i canali in numeri tra 0 e 1, quindi il modello riesce ad eleborare l'input
# - Dato che la scala però è sbagliata, probabilmente vedremo come output sempre risposte ultra confindenti (es circa 0.98) ma sempre sulla stessa classe, perchè gli input non scalati spingeranno inevitabilmente verso una sola delle classi.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 5.4 — soglia vs argmax (formato: 2 righe)
# --------------------------------------------------------------------------
# Il contratto dice soglia 0.45. In demo usi `argmax`. Spiega in due
# righe perché stai applicando una regola diversa da quella dichiarata,
# e con che probabilità di ape la differenza si vede.
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 6 — app.py IN QUATTRO BLOCCHI
# ==========================================================================
#
# --------------------------------------------------------------------------
# 6.1 Perché quattro blocchi e non un file e via
# --------------------------------------------------------------------------
#
# Il file che deployi è `app.py`. Potresti scriverlo di fila: import,
# carica pesi, definisci funzione, lancia. Trenta righe, funziona.
#
# Lo dividiamo in quattro blocchi con un criterio preciso: separare ciò
# che è LOGICA da ciò che è PRESENTAZIONE. Il test è questo:
#
#     se domani togli Gradio, quante righe devi riscrivere?
#
# Con i blocchi separati: solo il blocco 4. La logica (caricamento,
# preprocess, predizione) resta identica e la riusi da FastAPI, da un
# notebook, da uno script batch. È la stessa domanda che ti fai quando
# separi un controller Laravel da un service: il controller parla HTTP,
# il service fa il lavoro.
#
#   BLOCCO 1 — CONFIGURAZIONE
#       percorsi, costanti, niente logica. Tutto ciò che un domani
#       potresti voler cambiare senza leggere il resto del file.
#   BLOCCO 2 — MODELLO
#       una sola istanza di ClassificatoreVisivo, caricamento pigro.
#   BLOCCO 3 — FUNZIONE DI PREDIZIONE (il core)
#       prende un'immagine, restituisce dati. Nessun riferimento a
#       Gradio. Testabile con una immagine e un assert.
#   BLOCCO 4 — INTERFACCIA
#       l'unica parte che sa che esiste Gradio.
#
# --------------------------------------------------------------------------
# 6.2 Il file completo
# --------------------------------------------------------------------------
#
# Lo lascio come commento perché questo capitolo non deve avviare un
# server quando lo apri. Tu lo copi in un file `app.py` a parte (nella
# cartella dello Space) e lo esegui da lì.
#
# ------------------------------ app.py ------------------------------------
#
# """Demo Gradio — classificatore visivo (track prova ants/bees)."""
#
# from pathlib import Path
#
# import gradio as gr
#
# # In questo capitolo le funzioni stanno nel file del corso; nello Space
# # copiale in un modulo `modello.py` accanto a app.py e importalo così:
# from modello import ClassificatoreVisivo
#
#
# # --- BLOCCO 1: CONFIGURAZIONE --------------------------------------------
#
# QUI = Path(__file__).parent          # ⚠️ mai percorsi assoluti: lo Space
#                                      #    non ha le tue cartelle
# PERCORSO_PESI = QUI / "pesi" / "ants_vs_bees.pt"
# CARTELLA_ESEMPI = QUI / "esempi"
#
# TITOLO = "Classificatore visivo — formiche vs api"
# DESCRIZIONE = (
#     "Demo didattica di transfer learning (ResNet18 fine-tuned). "
#     "Carica una foto: il modello restituisce la probabilità per classe."
# )
# DISCLAIMER = (
#     "⚠️ Demo didattica, non uno strumento di produzione. "
#     "Il modello è addestrato su un dataset piccolo (circa 250 immagini) "
#     "e può sbagliare su foto molto diverse da quelle di addestramento. "
#     "Le immagini caricate non vengono conservate."
# )
#
#
# # --- BLOCCO 2: MODELLO ---------------------------------------------------
#
# # UNA istanza a livello di modulo: il caricamento pigro dentro la classe
# # fa sì che i pesi si leggano alla prima predizione e restino in memoria.
# classificatore = ClassificatoreVisivo(PERCORSO_PESI, device="cpu")
#
#
# # --- BLOCCO 3: IL CORE (nessuna dipendenza da Gradio) --------------------
#
# def analizza(immagine):
#     """immagine: PIL.Image → (dict per gr.Label, stringa di riepilogo)."""
#     if immagine is None:
#         return {}, "Carica un'immagine per iniziare."
#
#     esito = classificatore.predict_etichetta(immagine)
#
#     riepilogo = (
#         f"Decisione: {esito['etichetta']}  "
#         f"(p({esito['classe_positiva']}) = {esito['p_positiva']:.3f}, "
#         f"soglia = {esito['soglia']:.2f})"
#     )
#     return esito["probabilita"], riepilogo
#
#
# # --- BLOCCO 4: INTERFACCIA (l'unico pezzo che conosce Gradio) ------------
#
# esempi = sorted(str(p) for p in CARTELLA_ESEMPI.glob("*.jpg"))
#
# demo = gr.Interface(
#     fn=analizza,
#     inputs=gr.Image(type="pil", label="Immagine"),
#     outputs=[
#         gr.Label(num_top_classes=2, label="Probabilità per classe"),
#         gr.Textbox(label="Decisione e soglia applicata"),
#     ],
#     title=TITOLO,
#     description=DESCRIZIONE,
#     article=DISCLAIMER,          # testo sotto la demo
#     examples=esempi or None,
#     cache_examples=False,        # True = predizioni calcolate al build
#     allow_flagging="never",      # niente raccolta immagini utenti
# )
#
# if __name__ == "__main__":
#     demo.launch()                # su Spaces non serve: ci pensa la piattaforma
#
# --------------------------------------------------------------------------
#
# Tre dettagli del file che non sono estetici:
#
#   `Path(__file__).parent`
#       rende i percorsi relativi al file, non alla directory da cui lanci
#       il comando. Su Spaces la working directory è `/home/user/app` e
#       un percorso tipo `C:/Users/visaf/...` non esiste. Questo è il
#       motivo numero uno di `FileNotFoundError` nei deploy (vedi TODO 3).
#
#   `if immagine is None`
#       Gradio chiama la funzione anche quando l'utente clicca senza aver
#       caricato niente. Senza questa guardia, `None.convert("RGB")` →
#       AttributeError nel log e un errore rosso in faccia all'utente.
#
#   `allow_flagging="never"`
#       il "flagging" è una funzione di Gradio che salva l'input
#       dell'utente in una cartella per revisionarlo dopo. Su una demo
#       pubblica significa raccogliere immagini di terzi: disattivato,
#       sia per privacy sia perché non ti serve.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.1 — a cosa serve ogni blocco (formato: 4 bullet)
# --------------------------------------------------------------------------
# Una riga per blocco: cosa contiene e cosa NON deve contenere.
# TUA RISPOSTA:
# - Blocco 1: contiente le costanti e i percorsi, NON deve contenere nessuna logica di funzionamento dell'app.
# - Blocco 2:contiene SOLO l'istanza con cui si inizializza il classificatore visivo,
# - Blocco 3: contiene solo la funzione che prende un immagini e restituisce dati. Può essere testata anche solo tramite assert, non contiene le logiche di Gradio.
# - Blocco 4: contiene solo la logica di Gradio, quindi tutte quelle funzione relative alla visualizzazione nel browser.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.2 — il test del "togli Gradio" (formato: 1 riga)
# --------------------------------------------------------------------------
# Se domani sostituisci Gradio con FastAPI, quali blocchi riscrivi e
# quali resti a guardare?
# TUA RISPOSTA:
# Il blocca 4, perchè è l'unico che contiene le logiche di visualizzazione.


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 6.3 — testare il core senza UI
# --------------------------------------------------------------------------
# Scrivi 3-4 righe che verificano `analizza()` senza avviare Gradio:
# apri un'immagine con PIL, chiama la funzione, controlla con un `assert`
# che le probabilità sommino a circa 1 (tolleranza 1e-5).
# TUO CODICE:
from PIL import Image
from app import analizza
from pathlib import Path
import numpy as np

p = (
    Path("dati")
    / "proxy_ants_bees"
    / "test"
    / "ants"
    / "35558229_1fa4608a7a.jpg"
)
immagine_pil = Image.open(p)
esito, riepilogo = analizza(immagine_pil)
assert np.isclose(sum(esito.values()), 1.0, atol=1e-5), "Le probabilità non sommano a 1!"
print(esito)

# ==========================================================================
# SEZIONE 7 — DEPLOY SU HUGGINGFACE SPACES
# ==========================================================================
#
# --------------------------------------------------------------------------
# 7.1 Che cosa è, tecnicamente, uno Space
# --------------------------------------------------------------------------
#
# Uno Space è un REPOSITORY GIT più un runtime che lo esegue. Non è
# concettualmente diverso da Streamlit Cloud del M2 cap.07: fai push,
# la piattaforma installa le dipendenze e avvia l'app.
#
# La sequenza che avviene a ogni push:
#
#     git push
#        → HF legge il README per sapere che SDK usare
#        → crea un container, installa requirements.txt
#        → avvia app.py e cerca l'oggetto `demo`
#        → espone l'URL pubblico
#
# Il piano gratuito dà: 2 vCPU, 16 GB di RAM, nessuna GPU, e lo Space
# va in "sleep" dopo un periodo di inattività (si risveglia alla prima
# visita, con qualche secondo di attesa). Per una ResNet18 in inferenza
# è più che sufficiente: parliamo di decine di millisecondi per immagine.
#
# --------------------------------------------------------------------------
# 7.2 Il README con il front-matter: la parte che spiazza
# --------------------------------------------------------------------------
#
# Su Spaces il `README.md` non è solo documentazione: le prime righe sono
# CONFIGURAZIONE. È un blocco YAML fra due righe di tre trattini, che HF
# legge per sapere come eseguire il tuo codice.
#
#     ---
#     title: Classificatore Formiche vs Api
#     emoji: 🐝
#     colorFrom: yellow
#     colorTo: gray
#     sdk: gradio
#     sdk_version: 4.44.0
#     app_file: app.py
#     pinned: false
#     ---
#
#     # Classificatore visivo formiche vs api
#     ... qui il testo normale, che diventa la model card ...
#
# Le tre righe che rompono tutto se sbagliate:
#     sdk           `gradio` o `streamlit` o `docker`. Se metti quello
#                   sbagliato, HF prova a lanciare l'app nel modo sbagliato.
#     sdk_version   se è incompatibile con la versione in requirements,
#                   il build fallisce con un messaggio poco chiaro.
#     app_file      il nome del file da eseguire. Se il tuo si chiama
#                   `demo.py` e qui c'è `app.py`, ottieni "app file not found".
#
# Analogia: è un `composer.json` / `package.json` travestito da README.
# Se vieni dal web ti sembra strano; a HF serve perché così la pagina
# dello Space e la sua configurazione stanno nello stesso posto.
#
# --------------------------------------------------------------------------
# 7.3 requirements.txt: pinnare le versioni
# --------------------------------------------------------------------------
#
#     gradio==4.44.0
#     torch==2.4.1
#     torchvision==0.19.1
#     pillow==10.4.0
#
# Perché con `==` e non a mano libera: senza pin, HF installa l'ultima
# versione disponibile IL GIORNO DEL BUILD. Il tuo Space funziona oggi e
# fra tre mesi, a un riavvio, non parte più perché una libreria ha
# cambiato una firma. È lo stesso ragionamento del `package-lock.json`:
# build ripetibili.
#
# Due note che ti risparmiano tempo:
#
# a) `torch` di default tira dentro le librerie CUDA: sono centinaia di
#    MB inutili su una macchina senza GPU. Se il build è lentissimo o
#    supera lo spazio, usa la variante CPU:
#
#        --extra-index-url https://download.pytorch.org/whl/cpu
#        torch==2.4.1
#        torchvision==0.19.1
#
# b) NON metti `numpy` o `pillow` se già arrivano come dipendenze di
#    torchvision, a meno che ti serva una versione specifica. Meno righe,
#    meno conflitti.
#
# --------------------------------------------------------------------------
# 7.4 Dove mettere i pesi: due strade
# --------------------------------------------------------------------------
#
#   STRADA 1 — i pesi nel repository dello Space
#       Semplice: `pesi/ants_vs_bees.pt` committato accanto a app.py.
#       Per file oltre ~10 MB serve git-lfs (Large File Storage), che
#       salva il file su uno storage separato e nel repo mette un
#       puntatore:
#
#           git lfs install
#           git lfs track "*.pt"
#           git add .gitattributes pesi/ants_vs_bees.pt
#           git commit -m "pesi modello"
#           git push
#
#       ⚠️ Se dimentichi lfs e committi un file grosso, il push viene
#          rifiutato. E se hai già committato, il file resta nella storia
#          del repo: va ripulita, non basta un `git rm`.
#
#   STRADA 2 — i pesi in un Model Repository, scaricati al boot
#       Carichi il `.pt` in un repo HF di tipo "model" (separato dallo
#       Space) e nell'app lo scarichi:
#
#           from huggingface_hub import hf_hub_download
#           percorso = hf_hub_download(
#               repo_id="tuo-utente/ants-vs-bees",
#               filename="ants_vs_bees.pt",
#           )
#
#       Vantaggi: separi il codice dai pesi (che è la separazione giusta
#       concettualmente), versioni i modelli indipendentemente, e più
#       Space possono usare gli stessi pesi. `hf_hub_download` mette in
#       cache: scarica una volta, non a ogni riavvio.
#
#       È anche la strada da preferire se un domani vuoi tenere i pesi
#       privati e la demo pubblica.
#
# Per oggi va benissimo la Strada 1 (un modello, una demo). La Strada 2
# è quella che userai nel M10, quando il Validator e il Replicator
# dovranno puntare allo stesso modello versionato.
#
# --------------------------------------------------------------------------
# 7.5 Cold start: perché la prima predizione è lenta
# --------------------------------------------------------------------------
#
# Questa è la domanda Feynman del quiz (V7), quindi la spieghiamo bene.
#
# Quando apri uno Space fermo da un po', succede una catena di cose che
# la SECONDA visita non rifà:
#
#   1. risveglio del container (lo Space era in sleep)
#   2. avvio del processo Python e import di torch — che non è un import
#      leggero: carica librerie native di centinaia di MB
#   3. lettura dei 45 MB di pesi dal disco e costruzione del modello
#   4. prima `forward`: allocazione dei buffer, eventuale
#      inizializzazione delle librerie di calcolo, cache della CPU fredda
#
# Dalla seconda richiesta in poi il processo è già vivo, i pesi sono in
# RAM e i buffer allocati: resta solo il calcolo, che per una ResNet18
# su CPU sono decine di millisecondi.
#
# La confusione tipica, che vale la pena smontare: non è che "il modello
# si scalda" o "impara". Il modello è identico. Quello che cambia è che
# la prima volta paghi il SETUP (processo, librerie, pesi) e le volte
# dopo no. Esattamente come la prima query di un'app dopo il deploy paga
# la connessione al database e il warm-up del pool.
#
# Cosa puoi fare per non far aspettare un recruiter:
#     - `cache_examples=True`: gli esempi hanno il risultato già pronto
#     - tenere il modello a livello di modulo (caricato una volta, non
#       per richiesta)
#     - non ricreare le `transforms` a ogni chiamata
#
# --------------------------------------------------------------------------
# 7.6 Il build log e i quattro errori che farai
# --------------------------------------------------------------------------
#
# Su Spaces, tab "Logs": ci sono due flussi, BUILD (installazione) e
# RUNTIME (app in esecuzione). Sapere quale guardare è metà del lavoro:
# se l'app non parte affatto → build; se parte e crasha al click → runtime.
#
#   1. `FileNotFoundError: ants_vs_bees.pt`
#      Percorso assoluto, o file mai committato, o lfs dimenticato.
#      Diagnosi rapida: stampa `Path.cwd()` e la lista dei file all'avvio.
#
#   2. `RuntimeError: Attempting to deserialize object on a CUDA device`
#      Hai salvato da Colab e caricato senza `map_location="cpu"`.
#      È letteralmente la lacuna #46 del cap.07, in produzione.
#
#   3. `ModuleNotFoundError: No module named 'torchvision'`
#      Manca da requirements.txt. In locale funzionava perché nel tuo
#      ambiente era già installato.
#
#   4. Build che fallisce per spazio/tempo
#      Stai installando torch con CUDA. Usa l'index CPU di 7.3.b.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 7.1 — i file minimi (formato: 3 bullet)
# --------------------------------------------------------------------------
# Elenca i tre file indispensabili di uno Space Gradio e, per ognuno, in
# mezza riga, a cosa serve.
# TUA RISPOSTA:
# -
# -
# -


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 7.2 — front-matter
# --------------------------------------------------------------------------
# Scrivi il blocco YAML del README per il tuo Space (sdk gradio, file
# app.py, titolo a scelta).
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 7.3 — pin (formato: 1 riga)
# --------------------------------------------------------------------------
# Perché `gradio==4.44.0` e non `gradio`? Rispondi con il caso concreto
# che si evita.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 7.4 — build o runtime (formato: 4 risposte)
# --------------------------------------------------------------------------
# Per ognuno dei quattro errori di 7.6, scrivi se lo troveresti nel log
# di BUILD o in quello di RUNTIME.
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)


# ==========================================================================
# SEZIONE 8 — SMOKE TEST, MODEL CARD, LATENZA, PRIVACY
# ==========================================================================
#
# --------------------------------------------------------------------------
# 8.1 Smoke test: cinque minuti che ti salvano la figura
# --------------------------------------------------------------------------
#
# "Smoke test" viene dall'elettronica: accendi e guardi se esce fumo. Non
# verifica che il sistema sia corretto, verifica che non sia
# palesemente rotto. Si fa DOPO ogni deploy, anche quando "non hai
# cambiato niente".
#
# La checklist, con accanto il motivo di ciascun punto:
#
#   [ ] carichi l'immagine A, poi la B: l'output CAMBIA
#       → se non cambia, stai mostrando un risultato in cache o la
#         funzione ignora l'input (succede più spesso di quanto pensi)
#
#   [ ] le probabilità sommano a ~1
#       → se no, hai sbagliato il `dim` del softmax
#
#   [ ] una foto ovvia di ape dà "bees" alto
#       → controllo di sanità sull'ORDINE DELLE CLASSI (Sez. 1.3):
#         se è invertito, te ne accorgi qui e solo qui
#
#   [ ] carichi un PNG con trasparenza e una scansione in grigio
#       → verifica di `convert("RGB")` (Sez. 5.1)
#
#   [ ] clicchi "invia" senza immagine
#       → verifica la guardia `if immagine is None`
#
#   [ ] carichi qualcosa di completamente fuori dominio (un gatto)
#       → il modello RISPONDERÀ comunque, con sicurezza. Va capito e
#         dichiarato: ha due sole classi, non sa dire "nessuna delle due"
#
#   [ ] il disclaimer è visibile senza scrollare
#   [ ] negli esempi non c'è nessun documento reale
#
# Il sesto punto è quello che distingue una demo onesta: un
# classificatore a due classi su una foto di gatto dirà "ape 87%". Non è
# un bug, è come funziona il softmax: distribuisce su ciò che conosce.
# Se lo dichiari, dimostri di aver capito il modello.
#
# --------------------------------------------------------------------------
# 8.2 La model card: la parte "riuso" che si legge in italiano
# --------------------------------------------------------------------------
#
# Nella Sez. 2 abbiamo messo il contratto DENTRO il file, in forma
# macchina. La model card è lo stesso contratto in forma umana, nel
# README dello Space. Serve a chi guarda la demo (e a te fra sei mesi).
#
# Le sei voci, con lo standard minimo da rispettare:
#
#   1. A COSA SERVE, in una frase, e a cosa NON serve
#      "Distingue foto di formiche da foto di api. Non riconosce altri
#       insetti e non è un identificatore di specie."
#
#   2. SU COSA È STATO ADDESTRATO
#      Dataset, numeri, provenienza. "hymenoptera (tutorial PyTorch),
#      245 train / 108 val / 45 test."
#
#   3. COME È STATO ADDESTRATO
#      "ResNet18 pre-addestrata su ImageNet, fine-tuning in due fasi:
#       prima la sola testa, poi anche layer4 con learning rate ridotto."
#
#   4. QUANTO VA, CON I NUMERI GIUSTI (🔁 #53)
#      Non solo l'accuracy. Accuracy 0.889 sul test, e accanto la recall
#      sulla classe positiva con il conteggio dei casi. Questo è lo
#      stesso schema dell'obiezione ancorata: metrica + valore + quanti
#      casi. Se scrivi solo "89% di accuratezza" stai comunicando come
#      il project manager del Mini 53.A.
#
#   5. LA SOGLIA, CON LA MOTIVAZIONE
#      "Soglia 0.45 sulla classe positiva, scelta per privilegiare la
#       recall: preferiamo un falso positivo a un caso mancato."
#
#   6. I LIMITI, ESPLICITI
#      Poche immagini, dominio ristretto, risposta comunque prodotta su
#      input fuori dominio, nessuna garanzia su foto molto diverse.
#
# Perché questo è riuso e non burocrazia: le voci 2-5 sono esattamente
# ciò che serve a un altro sviluppatore per decidere se il tuo modello è
# adatto al suo problema, senza rileggere il tuo codice. Ed è la stessa
# informazione che nel tuo prodotto servirà per dire all'operatore quanto
# fidarsi di `prob_busta_paga_visivo`.
#
# --------------------------------------------------------------------------
# 8.3 Misurare la latenza (senza strumenti complicati)
# --------------------------------------------------------------------------
#
# "Quanto è veloce?" è una domanda da colloquio a cui bisogna saper
# rispondere con un numero misurato, non stimato.
#
#     import time
#
#     tempi = []
#     for _ in range(20):
#         inizio = time.perf_counter()
#         classificatore.predict_proba(immagine)
#         tempi.append((time.perf_counter() - inizio) * 1000)   # in ms
#
#     tempi_ordinati = sorted(tempi)
#     p50 = tempi_ordinati[len(tempi_ordinati) // 2]
#     p95 = tempi_ordinati[int(len(tempi_ordinati) * 0.95) - 1]
#     print(f"p50 {p50:.0f} ms   p95 {p95:.0f} ms")
#
# Due cose da capire, che valgono per qualsiasi misura di performance:
#
# a) `time.perf_counter()` e non `time.time()`: il primo è un contatore
#    monotono ad alta risoluzione fatto per misurare intervalli; il
#    secondo è l'ora di sistema e può fare salti.
#
# b) si guardano i PERCENTILI, non la media. Il p50 (mediana) dice
#    "l'esperienza tipica"; il p95 dice "l'esperienza del 5% più
#    sfortunato". La media nasconde i picchi: una richiesta da 2 secondi
#    su venti da 30 ms fa una media di 128 ms, che non descrive nessuna
#    delle due situazioni.
#
# c) SCARTA la prima misurazione o fai qualche giro a vuoto prima: la
#    prima include il cold start di Sez. 7.5 e sporca tutto.
#
# --------------------------------------------------------------------------
# 8.4 Privacy della demo pubblica
# --------------------------------------------------------------------------
#
# Il cap.09 aveva la Sez. 0 sulla privacy dei dati di TRAINING. Qui il
# rischio è diverso e va guardato da tre lati:
#
#   1. Cosa pubblichi tu
#      Il repository dello Space è pubblico: codice, esempi e pesi sono
#      scaricabili da chiunque. Quindi: esempi mai reali nel track
#      prodotto, e nessun percorso o nome di file nei metadati del
#      checkpoint (Sez. 2.3).
#
#   2. Cosa raccogli dagli utenti
#      `allow_flagging="never"`. Se lasci attivo il flagging, gli input
#      degli utenti finiscono in una cartella del repo. Stai
#      raccogliendo dati di terzi senza averlo dichiarato.
#
#   3. Cosa dichiari
#      Una riga nel disclaimer: "le immagini caricate non vengono
#      conservate". Detta solo se è vera — ed è vera se non logghi e non
#      flagghi.
#
# Per il track prodotto (buste paga), quando ci arriverai: Space PRIVATO
# oppure esempi sintetici. Una demo pubblica di un classificatore di
# buste paga con esempi veri non è un rischio teorico: è pubblicare
# documenti reddituali su un CDN.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 8.1 — smoke test (formato: 3 punti numerati)
# --------------------------------------------------------------------------
# Scegli i TRE controlli che faresti per primi dopo il deploy e, per
# ognuno, una riga sul bug che scoprirebbe.
# TUA RISPOSTA:
# 1)
# 2)
# 3)


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 8.2 — 🔁 #53 nella model card (formato: 2 frasi)
# --------------------------------------------------------------------------
# Scrivi la voce "quanto va" della tua model card usando i numeri veri
# del cap.09 (test accuracy ~0.889, 45 immagini). Devono comparire
# almeno due numeri e la classe positiva.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 8.3 — percentili (formato: 1 riga)
# --------------------------------------------------------------------------
# Perché riportiamo p50 e p95 invece della media? Rispondi con l'esempio
# numerico di 8.3.b.
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 8.4 — il gatto (formato: 2 righe)
# --------------------------------------------------------------------------
# Un utente carica la foto di un gatto e la demo risponde "bees 0.87".
# Spiega in due righe perché è il comportamento atteso e come lo
# dichiareresti nella model card.
# TUA RISPOSTA:


# ==========================================================================
# SEZIONE 9 — LO STESSO CORE DA FASTAPI
#             (dove il riuso smette di essere teoria)
# ==========================================================================
#
# --------------------------------------------------------------------------
# 9.1 Il punto dell'intero capitolo
# --------------------------------------------------------------------------
#
# Tutto quello che abbiamo costruito serve a poter scrivere questa frase:
# per esporre il modello via API non riscrivo niente della logica.
#
# Riguarda la catena dell'intestazione: `ClassificatoreVisivo` non sa se
# chi la chiama è Gradio, FastAPI o un test. Restituisce dizionari.
# Quindi le due uscite sono due adattatori sottili sopra lo stesso core.
#
#   Gradio  (demo, umano)          FastAPI (servizio, macchina)
#        ↓                                ↓
#     immagine PIL dal widget        UploadFile multipart
#        ↓                                ↓
#        └────────→ ClassificatoreVisivo.predict_etichetta ←────────┘
#        ↓                                ↓
#     dict → barre                    dict → JSON
#
# --------------------------------------------------------------------------
# 9.2 L'endpoint, commentato
# --------------------------------------------------------------------------
#
# Lo hai già visto FastAPI nel M1 cap.12 (`12_web_bridge.py`), quindi qui
# guardiamo solo le differenze di questo caso.
#
#     from fastapi import FastAPI, UploadFile, File, HTTPException
#     from PIL import Image
#     import io
#
#     app = FastAPI(title="Classificatore visivo documenti")
#
#     # Stessa istanza, stessa classe, stesso checkpoint. Zero logica nuova.
#     classificatore = ClassificatoreVisivo("pesi/ants_vs_bees.pt")
#
#     @app.get("/info")
#     def info():
#         """Espone il CONTRATTO. Un client può interrogarlo."""
#         return classificatore.scheda()
#
#     @app.post("/classifica")
#     async def classifica(file: UploadFile = File(...)):
#         contenuto = await file.read()
#         try:
#             immagine = Image.open(io.BytesIO(contenuto))
#         except Exception:
#             raise HTTPException(status_code=400, detail="File non è un'immagine")
#
#         esito = classificatore.predict_etichetta(immagine)
#         return {
#             "etichetta": esito["etichetta"],
#             "probabilita": esito["probabilita"],
#             "soglia": esito["soglia"],
#             "versione_modello": classificatore.scheda()["versione_contratto"],
#         }
#
# Quattro dettagli che nella versione Gradio non c'erano e qui sì:
#
#   `io.BytesIO(contenuto)`
#       il file arriva come byte in memoria, non come percorso. `BytesIO`
#       lo fa sembrare un file a `Image.open`. È lo stesso trucco di
#       `php://memory` o di uno stream in Node.
#
#   `HTTPException(400)`
#       un'API deve rispondere con uno status code, non con un traceback.
#       Gradio poteva permettersi di mostrare l'errore a schermo; un
#       client che riceve un 500 su un PDF caricato per sbaglio non sa
#       distinguere "colpa tua" da "colpa mia".
#
#   `versione_modello` nella risposta
#       serve a chi consuma l'API per sapere quale modello ha risposto.
#       Quando ne avrai due in parallelo (il vecchio e il nuovo), questo
#       campo è l'unico modo di interpretare i risultati a posteriori.
#
#   `/info`
#       il contratto diventa interrogabile via HTTP. Un client può
#       chiedere "quali classi hai? che soglia usi?" senza leggere
#       documentazione. È la versione API della model card.
#
# --------------------------------------------------------------------------
# 9.3 Il ponte con il prodotto: prob_busta_paga_visivo
# --------------------------------------------------------------------------
#
# Ricorda l'obiettivo dichiarato dal cap.05 M3: il ramo visivo non è un
# progetto a sé, produce una FEATURE per il modello tabellare del M2.
#
# Nel Validator, quando ci arriverai:
#
#     per ogni documento della pratica:
#         prob = classificatore.predict_proba(immagine_pagina)
#         riga["prob_busta_paga_visivo"] = prob["busta_paga"]
#
#     poi il modello tabellare del M2 usa quella colonna insieme alle
#     feature testuali/strutturali già esistenti
#
# E qui riemerge il data leakage del cap.09 (TODO 5), che vale la pena
# ripetere perché è il tipo di errore che si ripresenta identico:
# le probabilità che finiscono nel TRAIN tabellare non devono venire da
# una CNN allenata su quelle stesse righe. Servono predizioni
# out-of-fold, o una CNN allenata solo sul train e usata per predire su
# val/test. Altrimenti il modello tabellare "vede" un segnale già
# calibrato sulle etichette e le metriche risultano gonfiate.
#
# In produzione il problema non esiste: i documenti nuovi non erano nel
# training di nessuno. Esiste solo quando costruisci il dataset.
#
# --------------------------------------------------------------------------
# 9.4 Demo o API: quando l'una, quando l'altra
# --------------------------------------------------------------------------
#
#   Gradio / Streamlit         FastAPI
#   ─────────────────────────  ──────────────────────────────────
#   utente umano               software che chiama software
#   portfolio, verifica a mano  integrazione in una pipeline
#   un'immagine alla volta     batch, concorrenza, timeout
#   output visivo              output JSON contrattuale
#   niente auth                auth, rate limit, versioning
#
# Nel tuo percorso: Gradio ora (portfolio #2), FastAPI nel M10 dentro il
# Validator. Ed è precisamente per questo che valeva la pena scrivere la
# Sez. 3 come l'abbiamo scritta: quando arriverà il M10, il lavoro di
# oggi sarà riusabile invece che da rifare.

# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 9.1 — cosa cambia (formato: 2 bullet)
# --------------------------------------------------------------------------
# Passando da Gradio a FastAPI: un bullet su cosa cambia nel modo in cui
# arriva l'immagine, un bullet su cosa cambia nella gestione degli errori.
# TUA RISPOSTA:
# -
# -


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 9.2 — /info (formato: 1 riga + elenco)
# --------------------------------------------------------------------------
# Perché esporre un endpoint `/info` con il contratto, e quali campi ci
# metteresti (elenca quelli che NON sono pesi)?
# TUA RISPOSTA:


# --------------------------------------------------------------------------
# 🧩 Mini-esercizio 9.3 — leakage, di nuovo (formato: 2 righe)
# --------------------------------------------------------------------------
# Devi aggiungere `prob_busta_paga_visivo` al dataset tabellare del M2.
# In due righe: qual è la regola da rispettare e perché in produzione il
# problema non si presenta.
# TUA RISPOSTA:


# ==========================================================================
# QUIZ DI VERIFICA
# ==========================================================================
#
# Su QUESTO capitolo. Soluzioni in fondo.

# --------------------------------------------------------------------------
# V1 — Prevedi l'output
# --------------------------------------------------------------------------
# Immagine PIL RGBA 500×400, contratto dimensione_input=224.
# Che shape ha il tensore passato al modello? E quanti canali, dopo il
# `convert("RGB")`?
# TUA RISPOSTA:

# --------------------------------------------------------------------------
# V2 — Trova l'errore
# --------------------------------------------------------------------------
#     stato = torch.load("pesi_da_colab.pt")
#     modello.load_state_dict(stato)
#
# In locale (senza CUDA) ottieni:
#     RuntimeError: Attempting to deserialize object on a CUDA device
#     but torch.cuda.is_available() is False
# Cosa manca, e in quale delle due righe?
# TUA RISPOSTA:

# --------------------------------------------------------------------------
# V3 — Vero / Falso con motivazione
# --------------------------------------------------------------------------
# "Su Spaces gratuito devo quantizzare o alleggerire ResNet18, altrimenti
#  la demo non parte."
# TUA RISPOSTA:

# --------------------------------------------------------------------------
# V4 — Completa il codice
# --------------------------------------------------------------------------
#     logits = modello(batch)              # shape (1, 2)
#     probabilita = torch.________(logits, dim=___)[0]
#     return {nome: float(p) for nome, p in zip(________, probabilita)}
#
# Riempi i tre spazi e spiega in mezza riga la scelta del `dim`.
# TUA RISPOSTA:

# --------------------------------------------------------------------------
# V5 — Il bug silenzioso (formato: 2 bullet)
# --------------------------------------------------------------------------
# La demo funziona, le probabilità sommano a 1, ma su ogni foto di ape
# risponde "ants" con alta confidenza. I pesi sono quelli giusti e le
# metriche sul test in Colab erano buone.
# Un bullet con la causa più probabile, un bullet con il controllo che la
# confermerebbe in trenta secondi.
# TUA RISPOSTA:
# -
# -

# --------------------------------------------------------------------------
# V6 — Le tre leve (formato: 3 righe)
# --------------------------------------------------------------------------
# Per ciascuna, dove va messa in un servizio di inferenza e perché
# proprio lì: `requires_grad=False`, `eval()`, `no_grad()`.
# TUA RISPOSTA:
# 1)
# 2)
# 3)

# --------------------------------------------------------------------------
# V7 — 💬 Feynman
# --------------------------------------------------------------------------
# Perché la prima predizione su uno Space appena aperto è lenta e quelle
# dopo sono veloci? Spiegalo in 4-6 righe a un collega sviluppatore,
# senza dire che "il modello si scalda".
# TUA RISPOSTA:

# --------------------------------------------------------------------------
# V8 — 💬 Feynman sul riuso
# --------------------------------------------------------------------------
# Un collega ti dice: "il modello è il file .pt, il resto sono dettagli".
# Rispondi in 4-6 righe spiegando cos'è il contratto di inferenza e
# portando UN esempio concreto di guasto che non produce errori.
# TUA RISPOSTA:


# ==========================================================================
# ESERCIZI
# ==========================================================================

# --------------------------------------------------------------------------
# TODO 1 — 🎯 [COLLOQUIO]
# --------------------------------------------------------------------------
# Domanda reale: "Hai un modello PyTorch addestrato. Come lo porti in
# produzione?"
#
# Rispondi in ESATTAMENTE 5 bullet, uno per tema:
#   1. cosa spedisci insieme ai pesi (e perché non basta il .pt)
#   2. demo vs API: quando l'una, quando l'altra
#   3. CPU o GPU, e come giustifichi la scelta con un numero
#   4. cosa versioni e come lo esponi a chi consuma
#   5. come ti accorgi che qualcosa è andato storto dopo il deploy
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)
# 5)


# --------------------------------------------------------------------------
# TODO 2 — 🔧 [REFACTORING]
# --------------------------------------------------------------------------
# Questo codice "funziona" su una demo. Ha SEI problemi.
#
#     modello = None
#
#     def pred(percorso):
#         global modello
#         modello = models.resnet18(weights="DEFAULT")
#         modello.fc = nn.Linear(512, 2)
#         modello.load_state_dict(
#             torch.load("C:/Users/visaf/Desktop/pesi/ants.pt")
#         )
#         modello.train()
#         img = Image.open(percorso)
#         t = transforms.Compose([
#             transforms.Resize((224, 224)),
#             transforms.ToTensor(),
#         ])(img)
#         out = modello(t.unsqueeze(0))
#         print("classe:", out.argmax().item())
#         return out.argmax().item()
#
# Parte (a): elenca i SEI problemi, uno per bullet, con mezza riga di
#            conseguenza pratica ciascuno.
# Parte (b): riscrivi la funzione usando `ClassificatoreVisivo`, con
#            firma `pred_bella(immagine_pil) -> dict`.
#
# Suggerimento per trovarli tutti: passa in rassegna le tre leve, il
# contratto (sei voci), e i tre sintomi di non-riusabilità di Sez. 3.0.
# TUA RISPOSTA (a):
# -
# -
# -
# -
# -
# -
# TUO CODICE (b):


# --------------------------------------------------------------------------
# TODO 3 — 🔍 [DEBUG] — nessun aiuto, come da protocollo
# --------------------------------------------------------------------------
# Il build dello Space va a buon fine. Al primo click, nel log RUNTIME:
#
#     Traceback (most recent call last):
#       File "/home/user/app/app.py", line 34, in analizza
#         esito = classificatore.predict_etichetta(immagine)
#       File "/home/user/app/modello.py", line 88, in carica
#         raise FileNotFoundError(
#     FileNotFoundError: Checkpoint non trovato:
#         /home/user/app/pesi/ants_vs_bees.pt
#
# In locale funziona. Il file è nel repository (lo vedi nella pagina
# "Files" dello Space, 133 byte).
#
# Scrivi: (a) la diagnosi in 2 bullet, (b) il fix in 1 bullet.
# Indizio da usare, non da ignorare: 133 byte.
# TUA RISPOSTA:
# (a) -
#     -
# (b) -


# --------------------------------------------------------------------------
# TODO 4 — 🧠 [RETRIEVAL] — a memoria, file chiuso
# --------------------------------------------------------------------------
# Senza guardare la Sez. 3, riscrivi da zero `costruisci_modello`:
#   - firma con nome architettura, numero classi, pesi opzionali
#   - accesso dinamico al costruttore di torchvision
#   - errore chiaro se l'architettura non esiste
#   - testa sostituita leggendo `in_features` dal modello
#
# Poi, come estensione: rendila compatibile anche con reti la cui testa
# si chiama `classifier` invece di `fc` (es. `efficientnet_b0`).
# Suggerimento: `hasattr`.
# TUO CODICE:


# --------------------------------------------------------------------------
# TODO 5 — 🔀 [INTERLEAVING] — M2 Streamlit + M3 Gradio
# --------------------------------------------------------------------------
# Nel M2 cap.06-07 hai deployato la demo di genuinità su Streamlit
# Cloud, con semaforo, `motivi_top3` e recall in UI.
#
# In 4 bullet:
#   1. quale elemento di quella UI riuseresti identico qui e perché
#   2. quale NON ha senso con un input immagine e perché
#   3. che cosa diventa `motivi_top3` in un classificatore visivo (pensa
#      a cosa il cap.08 ti ha fatto visualizzare)
#   4. come combineresti in un'unica schermata lo score tabellare del M2
#      e quello visivo del M3 per la stessa pratica
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)


# --------------------------------------------------------------------------
# TODO 6 — 🌊 [REAL-WORLD] — consegna vaga, come nella realtà
# --------------------------------------------------------------------------
# Un collega della rete vede la tua demo e ti scrive:
#
#     "Bello! Mettiamoci le buste paga vere così i colleghi provano con i
#      loro documenti. Ho già una cartella con 40 buste di clienti, te la
#      giro. Tanto è solo una demo interna."
#
# Rispondi con 5 punti numerati. Ogni punto: cosa fai o non fai, e UNA
# riga di motivo (tecnico, di privacy o di prodotto — non "non si fa").
# Almeno uno dei punti deve proporre un'ALTERNATIVA praticabile, non solo
# un divieto: il collega ha un bisogno reale e va indirizzato.
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)
# 5)


# --------------------------------------------------------------------------
# TODO 7 — 📐 [SYSTEM DESIGN]
# --------------------------------------------------------------------------
# Scenario: il Validator (FastAPI) deve classificare le pagine dei
# fascicoli. Volumi: ~200 pratiche al giorno, ~8 pagine ciascuna, picchi
# a fine mese. Gira su un server senza GPU.
#
# Progetta in 6 bullet:
#   1. endpoint: uno per pagina o uno per fascicolo? Trade-off.
#   2. dove vive il modello: nello stesso processo dell'API o in un
#      servizio separato? Trade-off.
#   3. cosa contiene la risposta JSON (pensa al contratto e a chi la
#      consuma a valle)
#   4. timeout e cosa fa il chiamante se scade
#   5. fallback se il checkpoint non si carica: errore o degradazione?
#   6. come rilasci un modello nuovo senza rompere i client esistenti
#
# Non c'è una risposta giusta: si valuta il ragionamento sui compromessi.
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)
# 5)
# 6)


# --------------------------------------------------------------------------
# TODO 8 — 📚 [LIBRO]
# --------------------------------------------------------------------------
# 📚 LETTURA PARALLELA
#   [PYTORCH] cap. 2 mostra l'inferenza con una rete pre-addestrata:
#   nota che anche lì, prima del forward, c'è SEMPRE il blocco
#   `transforms` con `Resize` + `CenterCrop` + `Normalize` sugli stessi
#   valori di ImageNet, e la chiamata a `eval()`. Quel preambolo, che
#   nel libro sembra una formalità, è esattamente il contratto di
#   inferenza di cui parla la Sez. 1 di questo capitolo.
#   [GERON] cap. 19 (2ª ed.) tratta il serving: model server, versioni
#   multiple in parallelo, deploy graduale. Concetti che nel nostro
#   piccolo ritrovi nella Sez. 9 (versione nella risposta, /info).
#
# Consegna, in 3 bullet:
#   1. il libro carica il modello, chiama `eval()` e predice. Cosa manca
#      al suo esempio perché un collega possa RIUSARE quel modello?
#   2. Géron mostra un server che tiene più versioni del modello attive
#      contemporaneamente. Perché è utile, in una riga?
#   3. una cosa che il libro fa e che NOI abbiamo deciso di fare in modo
#      diverso in questo capitolo, con il motivo
# TUA RISPOSTA:
# 1)
# 2)
# 3)


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — la demo live (portfolio #2)
# ==========================================================================
#
# Obiettivo: il SECONDO URL pubblico del tuo portfolio, dopo lo Streamlit
# del M2. Tempo stimato: una sessione.
#
# --------------------------------------------------------------------------
# TRACK PROVA — ants vs bees (da fare ORA, privacy-safe)
# --------------------------------------------------------------------------
#
#   [ ] G1 — Recupera i pesi da Colab e salvali in `dati/pesi/`.
#            Se hai solo il vecchio `state_dict`, ricostruisci il
#            contratto e risalva con `salva_checkpoint(...)`:
#            arch, classi nell'ordine di ImageFolder, 224, mean/std,
#            la soglia che hai scelto, le metriche del test.
#            DoD: `carica_checkpoint(percorso)` funziona e
#                 `scheda()` stampa tutte le voci del contratto.
#
#   [ ] G2 — Verifica il core in locale, senza UI: apri due immagini
#            (una formica, un'ape), stampa `predict_proba` su entrambe.
#            DoD: le due predizioni sono diverse e vanno nella direzione
#                 giusta. Se sono invertite, hai trovato il bug di
#                 Sez. 1.3 prima di pubblicarlo.
#
#   [ ] G3 — Crea la cartella dello Space con i quattro file:
#            `app.py` (i 4 blocchi), `modello.py` (le funzioni riusabili
#            copiate da qui), `requirements.txt` pinnato, `README.md` con
#            front-matter YAML.
#
#   [ ] G4 — Metti 4 immagini in `esempi/` (2 formiche, 2 api) e
#            collegale con `examples=`.
#            DoD: dalla home dello Space si prova senza caricare nulla.
#
#   [ ] G5 — Scrivi la model card nel README: le 6 voci di Sez. 8.2.
#            DoD: compaiono la soglia con la sua motivazione e la recall
#                 con il conteggio dei casi, non solo l'accuracy.
#
#   [ ] G6 — Deploy: `git push` allo Space. Se il build fallisce, leggi
#            il log e usa la lista di Sez. 7.6 prima di cambiare codice
#            a caso.
#
#   [ ] G7 — Smoke test completo (Sez. 8.1), inclusi il PNG trasparente,
#            il click a vuoto e l'immagine fuori dominio.
#            DoD: 8 caselle spuntate e nessun errore nel log runtime.
#
#   [ ] G8 — Misura p50/p95 su 20 chiamate locali (Sez. 8.3) e scrivi i
#            numeri nel diario del capitolo. Poi registra l'URL nella
#            tabella Portfolio di `CONTESTO_CORSO.md` (riga #2).
#
# Deliverable: URL HuggingFace Spaces funzionante + model card + numeri
# di latenza nel diario.
#
# --------------------------------------------------------------------------
# TRACK PRODOTTO — buste vs altro (debito dichiarato dal cap.09)
# --------------------------------------------------------------------------
#
# Resta aperto C1-C8 del cap.09: senza `busta_vs_altro.pt` non c'è nulla
# da deployare sul prodotto. Quando ci arriverai, il lavoro di oggi si
# riusa senza modifiche strutturali:
#
#   [ ] P1 — stesso `salva_checkpoint`, con classi `["altro","busta_paga"]`
#   [ ] P2 — stesso `app.py`: cambiano solo i nomi delle classi, che
#            comunque arrivano dal checkpoint e non dal codice
#   [ ] P3 — Space PRIVATO oppure esempi sintetici (mai buste reali)
#   [ ] P4 — endpoint FastAPI di Sez. 9 dentro il Validator
#   [ ] P5 — `prob_busta_paga_visivo` nel dataset tabellare, con la
#            regola anti-leakage di Sez. 9.3
#
# Il fatto che P2 sia "cambiano solo i nomi, e nemmeno nel codice" è la
# prova che il capitolo ha funzionato.


# ==========================================================================
# 🔄 CONFRONTO PRIMA/DOPO — obbligatorio, ultimo capitolo del Modulo 3
# ==========================================================================
#
# Torna al cap.01 di questo modulo, `01_neurone_artificiale.py`: un
# neurone in NumPy, `z = X @ w + b`, poi `sigmoid(z)`, e una soglia a 0.5
# per decidere la classe.
#
# Da allora hai attraversato: reti a due layer, loss, derivate, chain
# rule, gradient descent, backpropagation scritta a mano, PyTorch,
# autograd, CNN, transfer learning, metriche, soglie, deploy.
#
# --------------------------------------------------------------------------
# Parte A — il codice
# --------------------------------------------------------------------------
# Riscrivi il classificatore del cap.01 come lo faresti oggi. Non serve
# che giri: serve che si veda cosa hai imparato. Copri almeno:
#   - shape dichiarate e verificate
#   - la scelta della loss e perché quella
#   - training loop (chi azzera i gradienti, chi li calcola, chi aggiorna)
#   - come valuti (e perché non sull'insieme di addestramento)
#   - come salvi il risultato perché sia riusabile
# TUO CODICE:


# --------------------------------------------------------------------------
# Parte B — la riflessione (formato: 5 bullet)
# --------------------------------------------------------------------------
# Cinque cose che al cap.01 non vedevi e adesso vedi. Un bullet ciascuna.
# Vincolo: almeno uno deve riguardare la VALUTAZIONE (non l'architettura)
# e almeno uno il RIUSO / la messa in produzione. "Userei PyTorch" non
# vale come risposta: è uno strumento, non una cosa capita.
# TUA RISPOSTA:
# -
# -
# -
# -
# -


# ==========================================================================
# SOLUZIONI
# ==========================================================================
#
# Leggile DOPO aver scritto le tue. Dove c'è una rubrica, non esiste una
# formulazione unica giusta: conta che compaiano gli elementi elencati.
#
# --------------------------------------------------------------------------
# QUIZ D'INGRESSO
# --------------------------------------------------------------------------
# Q1  eval(): FA passare Dropout e BatchNorm in modalità inferenza (BN usa
#     le running stats accumulate); NON congela i pesi, NON spegne autograd.
#     no_grad(): FA smettere di costruire il grafo (risparmio RAM);
#     NON cambia Dropout/BatchNorm.
#
# Q2  512 numeri. Perché AdaptiveAvgPool2d((1,1)) collassa qualunque H×W
#     a 1×1 per canale: in uscita hai sempre un valore per canale, e i
#     canali dopo layer4 in ResNet18 sono 512. La dimensione dell'immagine
#     non entra in `in_features`.
#
# Q3  {"ants": 0, "bees": 1}. ImageFolder ordina i nomi delle cartelle in
#     ordine alfabetico e assegna gli indici in quell'ordine.
#
# Q4  Rubrica: deve comparire un numero. Esempio: "45 immagini di test
#     sono poche: un errore in più o in meno sposta l'accuracy di ~2,2
#     punti (1/45), quindi la differenza fra 0.889 e 0.91 non è
#     significativa". Oppure il conteggio dei falsi negativi sulla classe
#     positiva con la recall.
#
# Q5  1) Resize (lato corto) 2) CenterCrop 3) ToTensor 4) Normalize.
#     Mezzo punto in più se citi `convert("RGB")` prima di tutto.
#
# Q6  `map_location="cpu"` (o `torch.device("cpu")`). I tensori salvati
#     portano con sé il device di origine ("cuda:0"); senza il remap
#     torch prova ad allocarli su una GPU inesistente.
#
# Q7  Abbassando la soglia classifichi come positivi più casi: la recall
#     sale (peschi più positivi veri) e la precision scende (fra i
#     pescati ci sono più falsi positivi).
#
# Q8  Rubrica: (a) riuso di una rete già addestrata su molti dati;
#     (b) i primi layer imparano cose generiche (bordi, texture) che
#     valgono per qualsiasi immagine; (c) si sostituisce la testa perché
#     le classi sono altre; (d) fase 1 solo testa = pochi parametri, si
#     stabilizza in fretta senza rovinare il backbone; (e) fase 2 si
#     sblocca layer4 con learning rate basso per adattare le feature più
#     specifiche. Termini tecnici spiegati.
#
# --------------------------------------------------------------------------
# RINFORZI
# --------------------------------------------------------------------------
# 48.A  1) Falso — eval() non toglie i gradienti, cambia Dropout/BN.
#       2) Falso — no_grad() tocca il grafo, non i layer.
#       3) Falso — il forward passa da tutti i layer; il freeze impedisce
#          l'aggiornamento, non l'esecuzione.
# 48.B  `with torch.no_grad():`
# 52.A  32 = batch (quante immagini nel forward, non c'entra con
#       l'architettura). 512 = feature prodotte dal backbone ResNet18
#       dopo avgpool, ed è il numero corretto. 256 = `in_features`
#       dichiarati a mano nel Linear: è il bug, perché deve combaciare
#       con 512. Fix portabile: `nn.Linear(modello.fc.in_features, 2)`
#       letto PRIMA di sostituire la testa (su resnet50 diventa 2048 da sé).
# 53.A  Esempio: "Accuracy 89% ma la recall sulle api è 25/30 = 83%:
#       perdiamo 5 casi su 30; se il caso mancato è quello che costa,
#       la leva è abbassare la soglia, pagando in precision."
# AVG   (4, 2048, 1, 1) → flatten → (4, 2048) → in_features 2048 → è una
#       ResNet50 (o 101/152: tutte le ResNet "grandi" hanno 2048).
#
# --------------------------------------------------------------------------
# MINI-ESERCIZI (le risposte brevi; le altre sono rubriche)
# --------------------------------------------------------------------------
# 1.1  architettura · classi ordinate · dimensione input · mean/std ·
#      soglia · versione.
# 1.2  Le candidate migliori: classi (etichette invertite) e mean/std
#      (probabilità plausibili ma sbagliate). Accettabili anche
#      dimensione input e soglia.
# 2.1  DENTRO: classi, soglia, mean/std, nome_arch (e metriche, utili).
#      FUORI: optimizer_state, percorsi dei file, immagini, learning rate
#      (quest'ultimo è informazione di training: sta nelle note, non serve
#      per predire).
# 2.3  (a) Stesso modello, testa rinominata da `fc` a `head`: il file
#      viene da un codice diverso dal tuo.
#      (b) Con strict=False il load passerebbe MA la testa resterebbe
#      inizializzata a caso: la rete predirebbe rumore senza dare errori.
# 2.4  `"data_training": datetime.now().isoformat()` (o `str(...)`).
#      Un oggetto `datetime` non è un tipo base: con weights_only=True
#      il caricamento lo rifiuta con "Unsupported global".
# 3.1  Scaricherebbe ~45 MB di pesi ImageNet che verrebbero sovrascritti
#      un attimo dopo da `load_state_dict`. Su uno Space è tempo di boot
#      e banda buttati a ogni riavvio.
# 3.2  Nel `__init__`: la prima richiesta è veloce ma l'AVVIO è lento
#      (rischio health check). Pigro: l'avvio è immediato, la prima
#      richiesta paga il caricamento, le successive sono tutte veloci.
# 3.3  1) Tutto hardcoded: architettura, `512`, percorso assoluto — per
#      cambiare qualsiasi cosa devi editare la funzione.
#      2) Ricarica i pesi a OGNI chiamata (e con `weights="DEFAULT"`
#      scarica anche ImageNet); manca `map_location`.
#      3) Logica e presentazione intrecciate (`print`), restituisce un
#      indice invece delle probabilità, nessun `eval()`/`no_grad()`,
#      `Resize((224,224))` deforma l'immagine e manca `Normalize`.
# 3.4  eval() è uno STATO del modello (lo imposti e resta); no_grad() è un
#      CONTESTO che vale solo dentro il blocco `with`.
# 4.2  Falso: `gr.Label` accetta un dizionario {classe: probabilità} e
#      disegna le barre; è proprio il caso d'uso principale.
# 4.3  - con PIL le `transforms` di torchvision funzionano direttamente e
#        hai `convert("RGB")` per i canali;
#      - numpy dà (H,W,C) mentre PyTorch vuole (C,H,W): con PIL +
#        ToTensor la conversione è già inclusa.
# 4.4  Numero di componenti in `inputs` diverso dal numero di parametri
#      della funzione: si guarda la firma di `fn` contro la lista `inputs`.
# 5.1  convert("RGB") 400×300 RGB → Resize(256) lato corto: 341×256 →
#      CenterCrop(224): 224×224 → ToTensor: (3,224,224) →
#      unsqueeze(0): (1,3,224,224).
# 5.2  dim=1 normalizza lungo le classi, per ciascuna delle 4 immagini
#      (giusto). dim=0 normalizzerebbe la stessa classe attraverso le 4
#      immagini del batch: senza senso.
# 5.3  - Non dà errore perché le shape sono identiche: cambiano solo i
#        valori dei pixel, e il modello accetta qualunque numero.
#      - Vedresti probabilità sbilanciate e molto confidenti, spesso
#        sempre sulla stessa classe, con accuracy reale molto più bassa
#        di quella misurata in training.
# 5.4  argmax equivale alla soglia 0.5. Con soglia dichiarata 0.45, i
#      casi con p(ape) fra 0.45 e 0.50 verrebbero classificati "formica"
#      dalla demo e "ape" dalla regola dichiarata: stai applicando una
#      politica diversa da quella scritta nella model card.
# 6.2  Riscrivi solo il blocco 4 (interfaccia). Blocchi 1, 2 e 3 restano
#      identici: è il senso della separazione.
# 7.1  app.py (il codice della demo) · requirements.txt (dipendenze
#      riproducibili) · README.md (front-matter con sdk e app_file, più
#      la model card). I pesi sono un quarto elemento, nel repo o su Hub.
# 7.3  Senza pin, un riavvio fra tre mesi installa versioni nuove e il
#      build può rompersi per un cambio di API (stesso ruolo del lock file).
# 7.4  1) runtime · 2) runtime · 3) runtime (l'import fallisce all'avvio
#      dell'app; il build invece era riuscito perché il pacchetto non era
#      nemmeno richiesto) · 4) build.
# 8.3  La media nasconde i picchi: una richiesta da 2000 ms insieme a 19
#      da 30 ms fa una media di ~128 ms, che non descrive né il caso
#      tipico né il caso peggiore. p50 e p95 li separano.
# 8.4  Il softmax distribuisce la probabilità SOLO fra le classi che
#      conosce: con due classi non esiste l'uscita "nessuna delle due".
#      Nella model card si dichiara come limite ("risponde comunque su
#      input fuori dominio").
# 9.1  - L'immagine arriva come byte (UploadFile) e non come oggetto PIL:
#        serve `Image.open(io.BytesIO(...))`.
#      - Gli errori diventano status code HTTP (400 per input non valido)
#        invece di messaggi a schermo.
# 9.3  Le probabilità usate nel train tabellare devono venire da una CNN
#      che non ha visto quelle righe (out-of-fold, o fit su train e
#      predizione su val/test). In produzione non si pone: i documenti
#      nuovi non erano nel training di nessun modello.
#
# --------------------------------------------------------------------------
# QUIZ DI VERIFICA
# --------------------------------------------------------------------------
# V1  (1, 3, 224, 224). Dopo `convert("RGB")` i canali sono 3: il canale
#     alfa dell'RGBA viene scartato.
#
# V2  Manca `map_location="cpu"` nella PRIMA riga, quella di `torch.load`.
#     È lì che i tensori vengono materializzati su un device. Aggiungere
#     `.to("cpu")` dopo non basta: l'errore avviene prima.
#
# V3  Falso. ResNet18 sono ~11,7 milioni di parametri, ~45 MB in float32,
#     e l'inferenza su una immagine costa decine di millisecondi su CPU.
#     Lo Space gratuito (2 vCPU, 16 GB) è sovrabbondante. La
#     quantizzazione serve su dispositivi edge o con volumi molto alti,
#     non qui.
#
# V4  `torch.softmax(logits, dim=1)[0]` e `zip(self.classi, probabilita)`.
#     `dim=1` perché la somma deve fare 1 lungo l'asse delle classi, per
#     ogni riga del batch.
#
# V5  - Causa più probabile: ordine delle classi invertito fra training e
#       demo (Sez. 1.3) — i nomi sono stati riscritti a mano invece di
#       leggerli dal checkpoint. Seconda ipotesi: mean/std diversi da
#       quelli del training.
#     - Controllo: stampare `classificatore.classi` (o `class_to_idx` del
#       training) e confrontarlo con l'ordine usato nel dizionario di
#       output. Trenta secondi, e chiude il dubbio.
#
# V6  1) `requires_grad=False`: in inferenza NON serve: era la leva del
#        training per non aggiornare il backbone.
#     2) `eval()`: subito dopo il load dei pesi, perché è uno stato del
#        modello e deve valere per tutte le predizioni.
#     3) `no_grad()`: intorno al forward nella funzione di predizione,
#        perché è un contesto e vale solo per il blocco.
#
# V7  Rubrica, devono comparire almeno tre di questi: risveglio del
#     container in sleep; avvio del processo e import di torch (librerie
#     native pesanti); lettura dei 45 MB di pesi e costruzione del
#     modello; prima forward con allocazione dei buffer. Dalla seconda
#     richiesta il processo è vivo e i pesi sono in RAM, quindi resta
#     solo il calcolo. NON deve comparire l'idea che il modello "impari"
#     o "si scaldi": i pesi sono identici, cambia solo cosa è già pronto.
#
# V8  Rubrica: (a) il .pt è un dizionario nome→tensori, non contiene
#     architettura, ordine delle classi, dimensione di input,
#     normalizzazione, soglia, versione; (b) esempio di guasto silenzioso
#     — classi invertite: le probabilità sono corrette ma le etichette
#     scambiate, la demo risponde con sicurezza il contrario del vero e
#     nessun log si accende; (c) conclusione: il contratto va salvato
#     insieme ai pesi, e i nomi delle classi si leggono da lì, non si
#     riscrivono nel codice della demo.
#
# --------------------------------------------------------------------------
# ESERCIZI — tracce di correzione
# --------------------------------------------------------------------------
# TODO 1  Elementi attesi: (1) pesi + contratto/model card, non solo .pt;
#         (2) demo per umani, API per software, con un criterio;
#         (3) CPU con un numero a supporto (decine di ms per ResNet18);
#         (4) versione del modello esposta nella risposta o in /info;
#         (5) smoke test dopo ogni deploy + qualcosa da osservare
#         (latenza, distribuzione delle predizioni, errori nei log).
#
# TODO 2  I sei problemi: (1) `global` + ricarica del modello a ogni
#         chiamata; (2) percorso assoluto della macchina dell'autore;
#         (3) `weights="DEFAULT"` inutile (scarica ImageNet per poi
#         sovrascriverlo) e manca `map_location`; (4) `modello.train()`
#         al posto di `eval()`, quindi BatchNorm sbagliata, e manca
#         `no_grad()`; (5) `512` hardcoded → rompe su altre architetture,
#         e `Resize((224,224))` deforma invece di Resize+CenterCrop;
#         manca `Normalize` e manca `convert("RGB")`; (6) restituisce un
#         indice e stampa: perde le probabilità e mescola logica e
#         presentazione.
#
# TODO 3  Il 133 byte è il punto: un checkpoint ResNet18 pesa ~45 MB.
#         133 byte è la dimensione di un PUNTATORE git-lfs, cioè un file
#         di testo con l'hash. Diagnosi: `git lfs track` non era attivo
#         quando hai committato (o lo Space non ha risolto l'oggetto
#         lfs), quindi nel repository c'è il puntatore e non i pesi.
#         `torch.load` su quel file di testo fallisce o il file non è
#         quello atteso. Fix: `git lfs install`, `git lfs track "*.pt"`,
#         ricommittare il file (verificando che la dimensione remota sia
#         di decine di MB), oppure passare a `hf_hub_download` da un
#         model repository.
#
# TODO 4  Per l'estensione: verificare `hasattr(modello, "fc")` e in
#         alternativa gestire `classifier`, che a seconda della rete è un
#         `Linear` o un `Sequential` (in quel caso si sostituisce
#         l'ultimo elemento). Il punto dell'esercizio è capire che una
#         funzione riusabile deve dichiarare dove smette di valere.
#
# TODO 5  Riusabile: il disclaimer e la logica del semaforo (soglia →
#         decisione → azione consigliata). Non riusabile: `motivi_top3`
#         basati sui coefficienti, perché su un'immagine non hai feature
#         con un nome. L'equivalente visivo sono le feature maps del
#         cap.08, o una mappa di salienza (Grad-CAM): "dove ha guardato".
#         La combinazione: una riga per pratica con score tabellare e
#         score visivo affiancati, e il semaforo calcolato sulla loro
#         combinazione, dichiarando il peso di ciascuno.
#
# TODO 6  Deve emergere: (1) niente documenti reali in un repo pubblico,
#         nemmeno "solo per una demo"; (2) il repository conserva la
#         storia, cancellare dopo non basta; (3) i dati sono di clienti,
#         non tuoi — non è una decisione che puoi prendere da solo;
#         (4) alternativa praticabile: Space privato con accesso ai
#         colleghi, oppure documenti sintetici generati ad hoc, oppure
#         demo eseguita in locale sul PC di chi deve valutare;
#         (5) il modello attuale è addestrato su un proxy (formiche/api):
#         sulle buste non funzionerebbe comunque, quindi la richiesta è
#         prematura anche tecnicamente. Il quinto punto è quello che
#         distingue una risposta da collega senior: dici anche perché la
#         cosa non porterebbe il risultato sperato.
#
# TODO 7  Non c'è soluzione unica. Segnali di buon ragionamento:
#         endpoint per fascicolo per ridurre il numero di chiamate ma con
#         il rischio di risposte lente (e quindi streaming o job
#         asincrono per i picchi); modello nello stesso processo per
#         semplicità, servizio separato se vuoi scalare o aggiornare il
#         modello senza toccare l'API; JSON con probabilità, soglia
#         applicata, versione del modello e identificativo della pagina;
#         timeout con un comportamento definito lato chiamante (riprova o
#         marca la pagina come non classificata); fallback che degrada
#         dichiarando l'assenza dello score visivo invece di far
#         fallire tutta la pratica; rilascio con versioni affiancate e il
#         campo `versione_modello` nella risposta.
#
# TODO 8  Atteso: (1) all'esempio del libro manca tutto il contratto
#         salvato insieme ai pesi (classi, size, normalizzazione, soglia):
#         il codice funziona perché i valori sono scritti nella stessa
#         pagina, non perché il modello sia autodescrittivo; (2) tenere
#         più versioni attive permette di confrontarle su traffico reale
#         e di tornare indietro senza un nuovo deploy; (3) risposta
#         libera, ma un esempio valido: noi salviamo un checkpoint ricco
#         invece del solo `state_dict`, perché il nostro obiettivo è il
#         riuso da parte di altri consumatori (Gradio, FastAPI, dataset
#         tabellare) e non un singolo script dimostrativo.
#
# ==========================================================================
# Fine del capitolo 10 — e del Modulo 3.
# Nessun codice eseguito all'import: il file si può leggere, importare e
# riusare senza avviare server né training.
# ==========================================================================
