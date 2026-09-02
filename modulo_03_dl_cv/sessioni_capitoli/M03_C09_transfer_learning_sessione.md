# Diario sessione — Capitolo 09 — Transfer learning e primo dataset reale

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `09_transfer_learning.py` |
| **File diario** | `M03_C09_transfer_learning_sessione.md` |
| **Stato** | in corso (aperto 01/09/2026) |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

- Far arrivare lo studente a un modello `busta_vs_altro.pt` allenato su Colab con transfer learning da ResNet18.
- Chiudere le lacune aperte dal cap.08: #47 `.item()`, #48 autograd/`requires_grad`, #49 canali, #50 formula `H_out`, #51 + Pattern #28 catena delle shape, #52 debug matmul, #53 metriche per classe.
- Far interiorizzare il vincolo privacy come **passo tecnico**, non come formalità: la Sez. 0 va eseguita prima di tutto.
- Verificare Pattern #6 (lettura consegne): il capitolo contiene 7 consegne con numero/formato esplicito in MAIUSCOLO. Se anche stavolta ne salta 3+, il pattern resta 🔴.

---

## Prerequisiti da verificare PRIMA di iniziare

- [ ] Bridge `M03_R08_after_C08_before_C09_cnn_to_transfer.md` completato e corretto
- [x] `.gitignore` con `data/buste_*/` (verificato 01/09/2026)
- [ ] Cartelle `data/buste_originali/`, `data/buste_anonimizzate/`, `data/altro/`
- [ ] Dataset "altro" (~200 immagini) raccolto e vario (non solo scansioni pulite)
- [ ] Colab con GPU verificata

---

## Domande durante lo studio

- _(2026-09-01)_ **Q:** Cos'è ImageNet?
  **Nota / risposta sintetica:** Archivio di ~14M immagini etichettate via WordNet (progetto 2009, Fei-Fei Li); nel DL si intende il sottoinsieme della gara ILSVRC = 1,2M immagini / 1000 classi. Classi sbilanciate verso animali (~120 razze di cani) → spiega perché la testa `Linear(512,1000)` è inutile per noi. Storia: AlexNet 2012, ResNet 2015 (errore top-5 < 3,6%, sotto l'umano ~5%). Tre punti di contatto col capitolo: i pesi scaricati da `ResNet18_Weights.DEFAULT`, il 1000 della testa da sostituire, i valori `mean/std` del `Normalize` = statistiche dei pixel di ImageNet. Limite: foto naturali ≠ scansioni → si trasferiscono i layer bassi/medi, si ritocca `layer4`.
  **Segnale positivo:** domanda spontanea su un termine dato per noto nell'intestazione del capitolo — buona abitudine di non passare sopra le parole non chiare.

- _(2026-09-01)_ **Q:** Come facciamo a dire che una rete impara bordi e texture nei primi layer?
  **Nota / risposta sintetica:** Tre evidenze, spiegate poi con l'analogia della catena di montaggio: (1) i pesi di `conv1` sono disegnabili (64 quadratini 7×7×3 → strisce orientate; convergono uguali su reti/dataset diversi); (2) si osserva quando un filtro si accende (feature maps già fatte in cap.08 mini 5.1; versione sistematica = patch che massimizzano il neurone, Zeiler & Fergus 2014; oppure activation maximization/DeepDream); (3) prova sperimentale del congelamento (Yosinski 2014): congelando i primi k layer il transfer regge, crolla al crescere di k → il TODO 8 del cap.09 è la versione in miniatura di quell'esperimento. Segnalati i limiti: neuroni polisemantici, texture bias (Geirhos 2019), confine generico/specifico graduale.
  **Nota mentor:** lo studente ha scritto "layer profondi" intendendo "primi layer" — corretto in chat senza insistere. Proposto (non ancora inserito) un mini in Sez. 1.2 che disegna i filtri di `conv1` di ResNet18, per rendere la teoria verificabile (spirito Regola 42). **Da decidere con lo studente.**

- _(2026-09-01)_ **Q:** Allora la prima conv di ResNet non è 2d? / "Mi ero confuso perché fino ad ora abbiamo lavorato solo in scala di grigi e avevo una shape in meno."
  **Nota / risposta sintetica:** Il "2d" conta le **direzioni di scorrimento** (H e W), non gli assi del tensore. `weight` di `Conv2d(3,64,7)` = `(64, 3, 7, 7)`; il filtro legge tutti i canali in blocco (non scorre sui canali) e li fa collassare in un solo numero per posizione → 64 canali in uscita, non 192. Conti: 3·7·7 = 147 per filtro, ×64 = 9.408 (`bias=False`). Conferma: nella formula `H_out` i canali non appaiono. Famiglia `Conv1d`/`Conv2d`/`Conv3d` (audio, immagini, video-TAC).
  **Punto chiave del fraintendimento (collegato a lacuna #49):** in grayscale non c'era "un asse in meno": `(1,28,28)` ha gli stessi 3 assi di `(3,224,224)`, con il canale a 1. L'asse era invisibile perché di taglia 1 e perché veniva rimosso con `squeeze()` per il plot. Data l'abitudine correttiva: non dire "immagine 28×28" ma "1 canale, 28 per 28".
  **Stato lacuna #49:** in miglioramento — l'errore è stato riconosciuto e spiegato **dallo studente**, non dal mentor. Verifica formale ancora da fare su Q3 / mini 3.1–3.2 del cap.09.
  **Check lasciato aperto (non ancora risposto):** shape e conteggio parametri di `nn.Conv2d(1, 16, kernel_size=3)` (attesa: `(16,1,3,3)`, 144 + 16 bias = 160).

- _(2026-09-01)_ **Q:** Rilettura TODO 7 del cap.08 (righe 976–991): "le shape che ho scritto sono sbagliate?"
  **Nota / risposta sintetica:** No: tutte le sei shape e le 8192 feature finali sono corrette (versione post-feedback). Sbagliata invece la **traccia del calcolo** in due righe: ha sostituito il numero di CANALI al posto di `H_in` dentro la formula — riga 987 `((16 + 2·1 − 3)/1) + 1` con `H_in = 32` (16 = `in_channels`), riga 989 `16 / 2` con `H_in = 32` (16 = risultato). Le righe si contraddicono da sole ma il risultato accanto è giusto → shape portate a mente, non derivate dalla formula.
  **Diagnosi più fine di Pattern #28 / lacuna #51:** il meccanismo dell'errore non è (solo) "contare i dimezzamenti", è **infilare nella formula un numero che non le appartiene**. Regola data: in `H_out` entrano solo `H_in`, `padding`, `kernel`, `stride`; se compare un numero di canali è sbagliato per definizione.
  **Implicazione per la verifica in cap.09:** nei mini 2.1/2.2 e nel TODO 7 non basta controllare le shape finali — va controllato **da dove viene ogni numero** della traccia. Con `kernel=7, stride=2, padding=3` di ResNet il calcolo a mente non copre più l'errore.
  **Nota minore data:** `8.192` nei commenti → in Python è un float; usare `8192` o `8_192`.

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" senza ricalcolo, salvo richiesta esplicita di nuovo tentativo.
> - Riferimento puntuale al blocco/righe del file.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [2026-09-01] — Creazione capitolo (nessuna valutazione)

- **Blocco:** file `09_transfer_learning.py` scritto integralmente (1955 righe) su richiesta dello studente subito dopo la chiusura del cap.08.
- **Contenuto:** Sez. 0 privacy → Sez. 6 metriche; Q1–Q8, V1–V8, TODO 1–8, 🏗️ C1–C8, soluzioni.
- **Nota mentor:** in fondo al file c'è il blocco **TRACCIA RINFORZI** con la mappa lacuna → posizione. Usarlo in chiusura per verificare che ogni rinforzo sia stato effettivamente esercitato e non solo scritto.

### [2026-09-02] — Quiz d'ingresso Q1 (🔁 lacuna #47)

- **Esercizio / blocco:** `09_transfer_learning.py` Q1 — `.item()` prima o dopo `backward`? Perché `.item()` e non `loss`?
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**.
- **Punti di forza:** ordine corretto — "dopo" `backward` (a freddo, dopo il 2/10 del cap.08 Q7). Sa che `.item()` estrae uno scalare.
- **Errori / lacune:** risposta incompleta sulla seconda metà ("soprattutto: perché"). Manca: `.item()` **stacca** il numero dal grafo di autograd; accumulare `loss` (tensore) terrebbe in RAM il grafo di ogni batch. Non menziona `* xb.size(0)`.
- **Correzione / suggerimento:** "`.item()` per loggare senza tenere vivo il grafo; dopo `backward` per convenzione — `.item()` da solo non rompe il backward, rompe `loss = loss.item()` **prima** del backward".
- **Pattern errore / ID contesto:** lacuna **#47** 🟡 — ordine ✅ a freddo; spiegazione grafo/RAM ancora assente.

### [2026-09-02] — Quiz d'ingresso Q2 (🔁 lacuna #50)

- **Esercizio / blocco:** `09_transfer_learning.py` Q2 — `H_out` di `Conv2d(3,64,k=7,s=2,p=3)` su input `(1,3,224,224)`.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** formula completa con `+1` finale (lacuna #50 chiusa su questo esercizio); `H_in = 224` da `input[2]` corretto in NCHW; risultato **112** giusto; stride 2 e padding 3 applicati bene.
- **Errori / lacune:** non scrive il passaggio intermedio `224+6-7 = 223`; non esplicita `floor` / divisione intera (`223 // 2 = 111` → `111+1=112`). Con H pari non cambia il risultato, ma su input dispari la divisione float darebbe errore.
- **Correzione / suggerimento:** template: `H_out = floor((H_in + 2·pad − k) / stride) + 1` con una riga di sostituzione numerica prima del risultato.
- **Pattern errore / ID contesto:** lacuna **#50** 🟡 → quasi chiusa (formula ok; manca solo esplicitare floor).

### [2026-09-02] — Quiz d'ingresso Q2 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso Q2, risposta aggiornata con `floor(...)`.
- **Valutazione fix:** **9/10** (non ricalcola il voto esame del primo tentativo: resta **8/10**).
- **Punti di forza:** `floor` esplicito; formula e risultato 112 invariati e corretti.
- **Micro-miglioramento opzionale:** una riga `224+6-7 = 223 → 223//2 = 111 → +1 = 112` renderebbe la traccia a prova di errore su input dispari.
- **Lacuna #50:** 🟢 superata su questo esercizio (formula completa a freddo con stride ≠ 1).

### [2026-09-02] — Quiz d'ingresso Q3 (🔁 lacuna #49)

- **Esercizio / blocco:** `09_transfer_learning.py` Q3 — shape `(1, 28, 28)`: significato assi + `plt.imshow`.
- **Valutazione (primo tentativo — "voto esame"):** **5/10**.
- **Punti di forza:** `(C, H, W)` corretto; il `1` è il **canale** grayscale — progresso reale rispetto al cap.08 (lo leggeva come batch).
- **Errori / lacune:** seconda metà invertita: `imshow` **non** vuole 4D; vuole `(H, W)` per grayscale o `(H, W, C)` per RGB. `unsqueeze` **aggiunge** un asse → `(1,1,28,28)` peggiora. Serve `x.squeeze()` → `(28, 28)` (o `.squeeze(0)`). Confusione batch `(N,C,H,W)` del modello vs formato Matplotlib.
- **Correzione / suggerimento:** regola: PyTorch singola immagine `(C,H,W)`; batch `(N,C,H,W)`; Matplotlib grigio `(H,W)` → `squeeze`; RGB `(H,W,C)` → `permute(1,2,0)`.
- **Pattern errore / ID contesto:** lacuna **#49** 🔴 — metà chiusa (canale ✅); ponte Matplotlib ancora sbagliato.

### [2026-09-02] — Quiz d'ingresso Q3 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso Q3, risposta aggiornata con `squeeze()` → `(28, 28)`.
- **Valutazione fix:** **9/10** (voto esame primo tentativo resta **5/10**).
- **Punti di forza:** `(C,H,W)` + `squeeze` per `imshow` corretti; direzione giusta (togliere asse, non aggiungere).
- **Micro-miglioramento:** esplicitare i tre numeri uno per uno (`1`=canale, `28`=H, `28`=W) invece che solo la convenzione generale.
- **Lacuna #49:** 🟢 superata su Q3 (canale + Matplotlib). Mini 3.1–3.2 del capitolo restano verifica formale.

### [2026-09-02] — Quiz d'ingresso Q4

- **Esercizio / blocco:** `09_transfer_learning.py` Q4 — V/F: `MaxPool2d` ha parametri aggiornati dall'optimizer?
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**.
- **Punti di forza:** **Falso** corretto; meccanismo chiaro (finestra 2×2, max, dimezza risoluzione); analogia thumbnail efficace.
- **Errori / lacune:** la consegna chiedeva motivazione sul **perché l'optimizer non lo aggiorna** — manca la frase esplicita: non ha pesi (`weight`/`bias`), solo regole fisse; l'optimizer modifica solo `requires_grad=True`.
- **Correzione / suggerimento:** una riga bastava: "Falso: nessun parametro apprendibile — prende il max in una finestra fissa, non ha pesi da aggiornare."

### [2026-09-02] — Quiz d'ingresso Q4 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso Q4, aggiunta frase "non ha parametri (pesi) da aggiornare".
- **Valutazione fix:** **9/10** (voto esame primo tentativo resta **7.5/10**).
- **Punti di forza:** V/F + meccanismo + legame esplicito optimizer/parametri; risposta completa rispetto alla consegna.
- **Micro-miglioramento:** opzionale citare che ha solo iperparametri fissi (`kernel_size`, `stride`), non `weight`/`bias`.

### [2026-09-02] — Quiz d'ingresso Q5

- **Esercizio / blocco:** `09_transfer_learning.py` Q5 — target di `CrossEntropyLoss` (dtype e shape).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** `torch.long` e shape `(N,)` corretti; capisce che non vuole one-hot float; collegamento diretto all'errore del codice.
- **Errori / lacune:** manca l'esempio concreto sul caso dato: `[[0.,1.],[1.,0.]]` → `torch.tensor([1, 0], dtype=torch.long)`.
- **Correzione / suggerimento:** ricordare che la loss applica softmax internamente sui logits `(N, num_classi)` — non serve one-hot.

### [2026-09-02] — Quiz d'ingresso Q7

- **Esercizio / blocco:** `09_transfer_learning.py` Q7 — shape dopo `Conv2d(3,16,k=3,p=1)` + `MaxPool2d(2)` su `(8,3,32,32)`.
- **Valutazione (primo tentativo — "voto esame"):** **4/10**.
- **Punti di forza:** calcolo H/W del conv corretto (32→32 con padding=1); capisce che il pool dimezza (32→16).
- **Errori / lacune:** shape scritte senza batch e con canali invertiti: `(16, 3, 32, 32)` invece di `(8, 16, 32, 32)`. Il `3` è `in_channels` in ingresso, non in uscita; il `16` è `out_channels` ma va in posizione **C** (asse 1), non N. Dopo pool: atteso `(8, 16, 16, 16)`, non `(16, 3, 16, 16)`.
- **Correzione / suggerimento:** template fisso `(N, C, H, W)` — N non cambia mai con conv/pool; C diventa `out_channels` del conv; H/W seguono formula/pool.
- **Pattern errore / ID contesto:** richiama lacuna **#49** (ordine assi) — qui confonde N/C e dimentica il batch.

### [2026-09-02] — Quiz d'ingresso Q7 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso Q7, shape corrette `(8,16,32,32)` → `(8,16,16,16)`.
- **Valutazione fix:** **9.5/10** (voto esame primo tentativo resta **4/10**).
- **Punti di forza:** `(N,C,H,W)` completo; N invariato; C=16 out_channels; pool dimezza H/W; collegamento post-chiarimento "ogni filtro legge tutti i canali insieme".
- **Micro-miglioramento:** nella formula H_out usare `//` o `floor` esplicito (come Q2).

### [2026-09-02] — Quiz d'ingresso Q8

- **Esercizio / blocco:** `09_transfer_learning.py` Q8 — Feynman: perché CNN ≪ FC sugli stessi pixel?
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** concetto chiave **parameter sharing** / filtri riusati su tutta l'immagine; contrasto corretto con FC (un peso per pixel/connessione).
- **Errori / lacune:** manca il secondo motivo: **connessioni locali** (ogni neurone guarda solo una finestrella, non tutti i pixel). "Matrici di parametri" un po' generico — sono kernel 3×3 (o 7×7) con pochi numeri ciascuno.
- **Correzione / suggerimento:** due righe: (1) stesso filtro scorre ovunque → pochi pesi riusati; (2) ogni connessione è locale, non verso ogni pixel.

---

## Lacune e dubbi ancora aperti

Ereditate dal cap.08 (da chiudere qui):

- 🔴 **#48** — chi calcola i gradienti: autograd, non il criterio/optimizer → Sez. 2.4, mini 2.3/2.4
- 🔴 **#49** — il `1` di `(1,28,28)` è il canale → Sez. 3.3, mini 3.1/3.2, Q3
- 🔴 **#51** + **Pattern #28** — catena dei dimezzamenti → Sez. 2.3, mini 2.1/2.2, TODO 7
- 🔴 **#52** — debug numerico dell'errore matmul → TODO 3, V2
- 🟡 **#47** — `.item()` vs `backward` → Q1 (verifica a freddo)
- 🟡 **#50** — il `+1` nella formula `H_out` → Q2 (con stride 2), V7
- 🟡 **#53** — metriche per classe / macro-F1 → Sez. 6, mini 6.1–6.3
- 🔴 **Pattern #6** — lettura incompleta delle consegne → 7 consegne con vincolo numerico esplicito

---

## Note per il capitolo successivo (mentor)

- Il deliverable di questo capitolo (`busta_vs_altro.pt` + soglia scelta + metriche sul test) è l'input diretto del cap.10 (Gradio + deploy HuggingFace, portfolio piece #2).
- Se il modello risultasse debole (recall busta paga < 0.85), valutare se il problema è il dataset "altro" troppo omogeneo prima di cambiare architettura.
