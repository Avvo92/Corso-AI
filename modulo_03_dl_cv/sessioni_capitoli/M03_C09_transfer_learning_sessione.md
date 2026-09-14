# Diario sessione — Capitolo 09 — Transfer learning e primo dataset reale

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `09_transfer_learning.py` |
| **File diario** | `M03_C09_transfer_learning_sessione.md` |
| **Stato** | **chiuso** (14/09/2026) |
| **Voto difficoltà** | **8**/10 (studente: lunghezza della pipeline) |

---

## Obiettivi del capitolo (per il mentor)

- Far arrivare lo studente a un modello `busta_vs_altro.pt` allenato su Colab con transfer learning da ResNet18.
- Chiudere le lacune aperte dal cap.08: #47 `.item()`, #48 autograd/`requires_grad`, #49 canali, #50 formula `H_out`, #51 + Pattern #28 catena delle shape, #52 debug matmul, #53 metriche per classe.
- Far interiorizzare il vincolo privacy come **passo tecnico**, non come formalità: la Sez. 0 va eseguita prima di tutto.
- Verificare Pattern #6 (lettura consegne): il capitolo contiene 7 consegne con numero/formato esplicito in MAIUSCOLO. Se anche stavolta ne salta 3+, il pattern resta 🔴.

---

## Prerequisiti da verificare PRIMA di iniziare

- [ ] Bridge `M03_R08_after_C08_before_C09_cnn_to_transfer.md` completato e corretto
- [x] `.gitignore` con `data/buste_*/` (verificato 01/09/2026) + **14/09** `dati/proxy_ants_bees/` e `dati/_cache/`
- [x] **TRACK PROVA:** script `prepara_dataset_proxy_ants_bees.py` eseguito (14/09) → train 245 / val 108 / test 45
- [ ] Cartelle `data/buste_originali/` … (**debito prodotto**, non bloccanti ora)
- [ ] Dataset "altro" (~200) — **debito prodotto**
- [ ] Colab con GPU verificata (serve per P4 training)

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

### [2026-09-04] — Mini 2.1 (🔁 #51 + Pattern #28) shape ResNet18

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 2.1 (righe ~708–719) — catena shape input `(8,3,224,224)`.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** tutte le shape corrette (stem + layer1–4 + avgpool + flatten + fc); ragionamento esplicito su layer1 (nessun dimezzamento) e su layer2–4 (stride=2 sul 1° BasicBlock + canali ×2); bn1 corretto a 64 dopo il tipico typo 62 in chat; ha allargato utilemente lo stem e `fc` oltre le 7 righe minime.
- **Errori / lacune:** notazione `MaxPool(2)` imprecisa — in ResNet è `MaxPool2d(k=3,s=2,p=1)`; la shape `(8,64,56,56)` è comunque giusta.
- **Correzione / suggerimento:** scrivere `MaxPool2d(k=3,s=2,p=1)` (o almeno “maxpool stride 2”) così non si confonde con un pool 2×2 “classico” da notebook generici.
- **Pattern errore / ID contesto:** **#51** / Pattern **#28** 🟡 in miglioramento su caso 224 “pulito”; verifica successiva Mini 2.2 (input 96, floor).

### [2026-09-04] — Mini 2.2 (🔁 #51) shape ResNet18 input 96

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 2.2 (righe ~736–747) — H dopo `layer4` con input `(8,3,96,96)`.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** catena completa corretta: 96→48→24→12→6→3; H dopo layer4 = **3**; canali 64→128→256→512 giusti; ha superato da solo l’avviso errato sul file (96/32=3 è pulito) e ha comunque tracciato stem+layer.
- **Errori / lacune:** ancora `MaxPool(2)` al posto di `MaxPool2d(k=3,s=2,p=1)` — shape ok.
- **Correzione / suggerimento:** opzionale esplicitare una riga formula stem `floor((96+6-7)/2)+1=48` (ha il risultato, non la sostituzione numerica).
- **Pattern errore / ID contesto:** **#51** / **#28** 🟡→ quasi chiuso su casi “dimezza pulito”; resta TODO 7 / input non multiplo se previsto.

### [2026-09-04] — Mini 2.3 (🔁 #48 micro 48.A) requires_grad → .grad

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 2.3 (righe ~797–805).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** scelta **(b) None** corretta; gradiente **non calcolato** (non “calcolato e ignorato”); contrasto chiaro con (a) zeri e perché `step` non deve moltiplicare lr×0; risparmio VRAM/grafo citato correttamente.
- **Errori / lacune:** nessuno.
- **Pattern errore / ID contesto:** lacuna **#48** 🟡 in chiusura su questo micro; resta mini 2.4.

### [2026-09-04] — Mini 2.4 (🔁 #48) freezing → risparmio memoria

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 2.4 (righe ~811–816).
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** direzione giusta — con `requires_grad=False` autograd **non traccia** quei parametri / non estende il grafo su di loro; collega freezing a meno lavoro di backward.
- **Errori / lacune:** (1) consegna chiedeva **due righe** — risposta una sola; (2) manca il pezzo dell’indizio: per il backward il grafo deve tenere in RAM le **attivazioni intermedie** del forward (feature maps); freezing evita di conservare quelle necessarie solo per i grad dei pesi congelati → meno VRAM. “Non iscrive il grafo di parametri freezzati” è un po’ impreciso (il forward sul backbone c’è comunque; non si costruisce il ramo di *derivazione* rispetto a quei pesi).
- **Correzione / suggerimento:** riga 1 = niente tracciamento / niente `.grad` su quei pesi; riga 2 = niente (o meno) salvataggio delle attivazioni intermedie per quel ramo → risparmio memoria.
- **Pattern errore / ID contesto:** **#48** ancora 🟡 (concetto sì, completezza consegna + meccanismo attivazioni no); Pattern **#6** (due righe).

### [2026-09-04] — Mini 2.5 — conteggio parametri allenabili

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 2.5 (righe ~819–824).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** generator expression corretta — `sum` + `p.numel()` + `model.parameters()` + filtro `if p.requires_grad`. Concetto transfer/freezing applicato bene (conta solo i pesi “vivi”).
- **Errori / lacune:** parentesi in più in coda: `requires_grad))` → `SyntaxError`. Versione giusta: `... if p.requires_grad)`.
- **Fix suggerito:** togliere una `)` prima di fine riga.
- **Pattern errore / ID contesto:** nessuno concettuale; solo attenzione alle parentesi (vicino allo spirito di Pattern #23, senza alzare priorità).

### [2026-09-04] — Mini 3.1 (🔁 #49) batch 1→3 canali

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 3.1 (righe ~1002–1007).
- **Valutazione (primo tentativo — "voto esame"):** **4/10**.
- **Punti di forza:** ha collegato il problema ai 3 canali / `Grayscale` della teoria (soluzione 1).
- **Errori / lacune:** (1) `x` è già un **tensore batch** `(4,1,224,224)` → serve soluzione (2) `x.repeat(1,3,1,1)`, non `Grayscale` (lato PIL / transform); (2) API sbagliata: `Grayscale(x, num_output_channels=3)` — il costruttore non prende l’immagine; (3) anche corretto, `t(x)` su batch NCHW non è il pattern del mini.
- **Fix suggerito:** `x = x.repeat(1, 3, 1, 1)`.
- **Pattern errore / ID contesto:** lacuna **#49** ancora aperta (sa che servono 3 canali, confonde dove applicare PIL vs tensore).

### [2026-09-04] — Mini 3.1 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso Mini 3.1; risposta aggiornata a `x = x.repeat(1, 3, 1, 1)`.
- **Valutazione fix:** corretto (voto esame del primo tentativo resta **4/10**).
- **Punti di forza:** shape `(4,1,224,224)→(4,3,224,224)`; fattori `1,3,1,1` giusti sull’asse canali.
- **Lacuna #49:** in miglioramento su questo micro (tensore batch); resta da consolidare il discrimine PIL/`Grayscale` vs `repeat` in Sez. 3 / mini successivi.

### [2026-09-04] — Mini 3.2 (🔁 #49) permute vs squeeze per imshow

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 3.2 (righe ~1009–1017).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** `squeeze` solo su assi di taglia 1 → su `(3,64,64)` non fa nulla; `imshow` vuole `(H,W,C)`; `permute` riordina gli assi. Collegamento chiaro al problema canali/#49.
- **Errori / lacune:** consegna chiedeva **una riga** (risposta lunga — Pattern #6 soft); “shape invertite” un po’ vago — meglio dire `permute(1,2,0)`: C,H,W → H,W,C (non un invert generico).
- **Pattern errore / ID contesto:** lacuna **#49** 🟡 in chiusura su questo micro; Pattern **#6** soft (formato “una riga”).

### [2026-09-04] — Mini 3.3 — parametri allenabili freeze vs non-freeze

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 3.3 (righe ~1021–1032).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** due modelli con `congela_backbone=True/False`; `conta_parametri` su entrambi; confronto diretto. Ordine invertito rispetto al testo (False prima) ma equivalente e chiaro.
- **Errori / lacune:** nessuno. Attesi: allenabili freeze ≈ **1026**; non-freeze ≈ **totali** (~11.2M).
- **Pattern errore / ID contesto:** nessun nuovo; conferma pratico del freezing (collegato a #48).

### [2026-09-07] — Mini 3.4 — freeze ≠ skip forward

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 3.4 (righe ~1035–1042).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** **Falso** corretto; distinzione chiara forward (tutti i layer) vs niente gradienti sul backbone / solo head allenabile. Chiude il malinteso “congelato = disattivato”.
- **Errori / lacune:** micro: `auto_grad` → **autograd**; consegna “una riga” un filo lunga (ok nel merito).
- **Pattern errore / ID contesto:** lacuna **#48** 🟡→ quasi chiusa su freeze/forward (resta completezza Mini 2.4 sulle attivazioni intermedie).

### [2026-09-08] — Mini 4.1 — fill=255 e CenterCrop in eval

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 4.1 (righe ~1251–1259).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** (1) angoli vuoti dopo rotazione → fill bianco 255; (2) val = stabilità, non ritagli fortuiti. Concetti giusti.
- **Errori / lacune:** formato: chiesti **2 bullet** (`- ...`) — due righe senza `-` (Pattern #6 soft). Opzionale: perché bianco e non nero (documento/carta, evitare artefatto scuro).
- **Pattern errore / ID contesto:** Pattern **#6** soft (formato bullet).

### [2026-09-08] — Mini 4.2 — no RandomHorizontalFlip su documenti

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 4.2 (righe ~1262–1269).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** flip ok su foto naturali, sbagliato su documenti (testo specchiato); collegamento esplicito ai cartelli (direzione/significato). Due idee chiare.
- **Errori / lacune:** nessuno sostanziale; micro: “due righe” un filo fuse in un paragrafo (ok nel merito).
- **Pattern errore / ID contesto:** nessuno.

### [2026-09-08] — Mini 4.3 — split 12 aziende con int()

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 4.3 (righe ~1272–1281).
- **Valutazione (primo tentativo — "voto esame"):** **5/10**.
- **Punti di forza:** train corretto: `int(12*0.7)=int(8.4)=8`. Ha usato `int` nel ragionamento.
- **Errori / lacune:** (1) val: `int(12*0.15)=int(1.8)=1`, non 2 (ha arrotondato invece di troncare); (2) test **non** è `int(12*0.15)` — è il **resto**: `12-8-1=3`. Risposta corretta: **8, 1, 3**.
- **Pattern errore / ID contesto:** attenzione a `int()` = truncazione; slice finale = remainder (non terza frazione indipendente).

### [2026-09-08] — Mini 5.1 — optimizer con/senza filtro requires_grad

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 5.1 (righe ~1492–1500).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** sì funziona (backbone senza `.grad` → non si aggiorna); costo memoria/stato optimizer sui ~11M; codice confuso; rischi futuri. Copre merito + pratico.
- **Errori / lacune:** nessuno (micro ortografia “Si,” / “freezzati”).
- **Pattern errore / ID contesto:** conferma #48 / freezing operativo.

### [2026-09-08] — Mini 5.2 — LR layer4 ≪ LR testa

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 5.2 (righe ~1503–1509).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** testa nuova ≈ pesi casuali → LR alto; `layer4` già utile da ImageNet → LR basso / ritocchi cauti. Idea del fine-tuning a due velocità.
- **Errori / lacune:** “dati importanti” un po’ vago — meglio “feature/pesi pre-addestrati” (catastrophic forgetting soft). Nel merito ok.
- **Pattern errore / ID contesto:** nessuno.

### [2026-09-08] — Mini 5.3 — eval() vs no_grad()

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 5.3 (righe ~1511–1520).
- **Valutazione (primo tentativo — "voto esame"):** **4/10**.
- **Punti di forza:** formato 2 bullet rispettato; ha intuìto che non sono la stessa cosa.
- **Errori / lacune:** (1) `eval()` **non** congela i parametri — mette Dropout/BatchNorm in modalità inferenza (BN = running stats); NON tocca `requires_grad`. (2) `no_grad()` non “non aggiorna i gradienti”: **non costruisce il grafo** / non calcola `.grad` in quel blocco; l’update pesi è `optimizer.step()`. Né l’uno né l’altro sostituisce il freeze.
- **Correzione attesa:**
  - `eval()`: FA cambiare Dropout/BN; NON FA freeze / NON disabilita autograd.
  - `no_grad()`: FA spegnere il tracking autograd; NON FA cambiare Dropout/BN.
- **Pattern errore / ID contesto:** nuova confusione **eval ≠ freeze ≠ no_grad** (vicina a #48).

### [2026-09-08] — Mini 5.3 — secondo tentativo (post-feedback)

- **Esercizio / blocco:** stesso Mini 5.3, risposta riscritta dopo correzione.
- **Valutazione (nuovo tentativo richiesto):** **8/10** (primo tentativo resta **4/10** come voto esame).
- **Punti di forza:** `eval` → Dropout/BN in modalità valutazione; `no_grad` → niente tracking del grafo / non serve backward. Distinzione centrale recuperata.
- **Errori / lacune:** la consegna chiedeva anche cosa **NON** fa ciascuno. Manca esplicito: `eval` non congela e non spegne autograd; `no_grad` non cambia Dropout/BN. “Smette di aggiornarli” è ok soprattutto per BN (running stats); su Dropout è più “disattiva il dropout”.
- **Pattern errore / ID contesto:** #48 in miglioramento su questa distinzione.

### [2026-09-11] — Mini 6.1 (🔁 #53) accuracy / recall / precision

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 6.1 (righe ~1627–1644).
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**.
- **Punti di forza:** (1) accuracy `(28+25)/60 ≈ 0.883` corretta subito; (3) precision `25/(25+2)` nella versione finale; formule con i conti.
- **Errori / lacune:** al primo tiro sulla (2) `25/(25+2)` chiamato recall (= precision). Fix in chat: `25/(25+5)≈0.833`. File finale: tutte e tre corrette.
- **Pattern errore / ID contesto:** lacuna **#53** 🟡 — discrimine recall/precision fragile a freddo.

### [2026-09-11] — Mini 6.2 — obiezione accuracy 88% in produzione

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 6.2 (righe ~1646–1653).
- **Valutazione (primo tentativo — "voto esame"):** **5/10**.
- **Punti di forza:** intuizione corretta — accuracy da sola non basta; richiama la recall.
- **Errori / lacune:** consegna: **UNA obiezione tecnica basata sui numeri**, non generica. Manca il dato: **5/30 buste perse** (FN), recall ≈ **0.83**; nel prodotto il costo è non intercettare buste. Pattern **#6** (vincolo “sui numeri”).
- **Esempio atteso:** “Accuracy 88% ma recall busta = 25/30 ≈ 83%: 5 buste su 30 non vengono viste — in produzione è inaccettabile se l’obiettivo è non perdere buste.”
- **Pattern errore / ID contesto:** #53 + Pattern #6.

### [2026-09-11] — Mini 6.3 — soglia vs recall busta

- **Esercizio / blocco:** `09_transfer_learning.py` Mini 6.3 (righe ~1656–1662).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** **abbassare** la soglia per più recall; in cambio più FP → **precision** giù. Meccanismo corretto.
- **Errori / lacune:** accuracy “potrebbe” scendere è plausibile ma secondaria; il trade-off da citare per primo è precision (come nel testo Sez. 6). Due righe ok.
- **Pattern errore / ID contesto:** #53 in chiusura su soglia/recall.

### [2026-09-11] — Quiz verifica V1 — shape output ResNet testa nuova

- **Esercizio / blocco:** `09_transfer_learning.py` V1 (righe ~1671–1676).
- **Valutazione (primo tentativo — "voto esame"):** **10/10**.
- **Punti di forza:** batch 8 → 8; `num_classi=2` → logits `(8, 2)`. Niente confusione con 1000 ImageNet o con (N,C,H,W) in uscita.
- **Errori / lacune:** nessuno.
- **Pattern errore / ID contesto:** nessuno.

### [2026-09-11] — Quiz verifica V2 — Linear(1000,2) vs 512

- **Esercizio / blocco:** `09_transfer_learning.py` V2 (righe ~1678–1684).
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** fix corretto `nn.Linear(512, 2)`; ha capito che 1000 è sbagliato come `in_features`.
- **Errori / lacune:** motivazione imprecisa. Non è “i canali raddoppiano da 16 a 512”. ResNet18: dopo `layer4` hai **512** canali → AdaptiveAvgPool → vettore **512** → la vecchia `fc` era `Linear(512, 1000)`. Il **1000** è `out_features` ImageNet (classi), non l’ingresso della testa. Numero giusto = `modello.fc.in_features` **prima** di sostituire (o 512 per ResNet18). “Da 16” confonde con CNN tiny del cap.08.
- **Pattern errore / ID contesto:** lacuna **#52** 🟡 — zona giusta, decomposizione del 512 ancora fumosa.

### [2026-09-11] — Quiz verifica V3 — augmentation solo in train

- **Esercizio / blocco:** `09_transfer_learning.py` V3 (righe ~1687–1692).
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**.
- **Punti di forza:** **Falso** corretto; train = crop random, val/test = centratura. Allineato a Mini 4.1 / Sez. 4.3.
- **Errori / lacune:** micro: CenterCrop in eval è **preprocessing deterministico**, non “augmentation centrata”. Il punto della frase falsa è: augmentation **casuale** solo in train; val/test stabili per metriche confrontabili (non “omogeneità” via stessa aug random).
- **Pattern errore / ID contesto:** nessuno grave.

### [2026-09-11] — Quiz verifica V4 — class_to_idx busta_paga

- **Esercizio / blocco:** `09_transfer_learning.py` V4 (righe ~1693–1698).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** valore **1** corretto; mapping `altro=0`, `busta_paga=1`.
- **Errori / lacune:** il “perché” è un filo vago (“secondo indice”). Motivo preciso: `ImageFolder` ordina le classi in **ordine alfabetico** delle cartelle → `altro` prima di `busta_paga`.
- **Pattern errore / ID contesto:** nessuno.

### [2026-09-11] — Quiz verifica V4 — Fix applicato (post-feedback)

- **Esercizio / blocco:** stesso V4; motivazione aggiornata con ordine alfabetico.
- **Valutazione fix:** **10/10** sul merito (voto esame primo tentativo resta **9/10**).
- **Punti di forza:** valore 1 + perché = ordinamento alfabetico ImageFolder; mapping 0/1 esplicito.
- **Nit:** nel testo “buste_paghe” → nome cartella reale `busta_paga`.

### [2026-09-11] — Quiz verifica V5 — parametri allenabili Linear(512,2)

- **Esercizio / blocco:** `09_transfer_learning.py` V5 (righe ~1700–1704).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** solo la testa allenabile; pesi `512×2 = 1024` corretti.
- **Errori / lacune:** manca il **bias** (`+ 2`) → totale **1026**, non 1024. (`nn.Linear` ha bias=True di default.)
- **Pattern errore / ID contesto:** nit ricorrente su Linear: weight + bias.

### [2026-09-11] — Quiz verifica V5 — secondo tentativo (post-feedback)

- **Esercizio / blocco:** stesso V5; aggiunta bias nel testo.
- **Valutazione (nuovo tentativo):** **9/10** (primo resta **8/10**).
- **Punti di forza:** ora include `+ bias` / `+ 2` nella formula.
- **Errori / lacune:** aritmetica finale sbagliata: scrive `512*2+2 -> 1024` ma **512×2+2 = 1026**. Concetto ok, risultato ancora 1024 per refuso.
- **Pattern errore / ID contesto:** Pattern soft — risultato ≠ conto scritto.

### [2026-09-11] — Quiz verifica V5 — Fix applicato (totale 1026)

- **Esercizio / blocco:** stesso V5; conto corretto `512*2+2 -> 1026`.
- **Valutazione fix:** **10/10** sul merito (voto esame primo tentativo resta **8/10**).
- **Punti di forza:** pesi + bias; solo testa; numero allineato a Mini 3.3 / commenti capitolo.

### [2026-09-11] — Quiz verifica V6 — freeze + nuova fc

- **Esercizio / blocco:** `09_transfer_learning.py` V6 (righe ~1706–1716).
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**.
- **Punti di forza:** `nn.Linear` nuovo nasce con `requires_grad=True` — corretto.
- **Errori / lacune:** manca il pezzo sull’**ordine**: la `fc` è un modulo **creato dopo** il ciclo `requires_grad=False`, quindi non viene congelata. Se la sostituissi **prima** del freeze, la testa nuova finirebbe congelata e non imparerebbe. Default True + timing.
- **Pattern errore / ID contesto:** #48 soft — default ok, ordine freeze/replace da fissare.

### [2026-09-11] — Quiz verifica V7 — H dopo layer4 su 320×320

- **Esercizio / blocco:** `09_transfer_learning.py` V7 (righe ~1719–1736).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**.
- **Punti di forza:** H dopo layer4 = **10**; `avgpool` → `(4, 512, 1, 1)`; catena 320→160→80→80→40→20→10 corretta; AdaptiveAvgPool indipendente da H. Canali 64/128/256/512 ok.
- **Errori / lacune:** nit notazione `MaxPool(2)` (è `MaxPool2d(k=3,s=2,p=1)`) — risultato 80 comunque giusto. Pattern #28/#51 in buona forma su input non-224.
- **Pattern errore / ID contesto:** nessuno sostanziale.

### [2026-09-11] — Quiz verifica V8 — Feynman ImageNet → buste

- **Esercizio / blocco:** `09_transfer_learning.py` V8 (righe ~1739–1745).
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza:** riusi feature generiche (bordi/linee/texture); butti la testa 1000 classi; nuova `Linear` a 2 classi. Idea del transfer corretta.
- **Errori / lacune:** (1) “layer **profondi**” per bordi/texture: in gergo sono i layer **bassi/primi**; i profondi sono più specifici (oggetti ImageNet). Stesso fraintendimento già visto in Sez.1. (2) “solo l’ultimo layer” = Fase 1; in Fase 2 si ritocca anche `layer4`. (3) un filo corto rispetto a 4–6 righe; manca il ponte “documenti condividono pattern geometrici con le foto”.
- **Pattern errore / ID contesto:** terminologia early vs deep layers.

### [2026-09-11] — TODO 1 — colloquio transfer vs scratch

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 1 (righe ~1749–1764).
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**.
- **Punti di forza:** 3 bullet rispettati; scelta pretrained con pochi dati; freeze + head poi fine-tune `layer4`; condizione di cambio (dominio troppo specifico / feature piccole).
- **Errori / lacune:** bullet 1 non cita esplicitamente **400** immagini (consegna “in termini di dati”); bullet 3 ok ma un filo vago — alternativa da colloquio: dataset enorme (milioni) → scratch possibile, oppure modality diversa (non RGB naturale).
- **Pattern errore / ID contesto:** Pattern #6 rispettato (3 bullet).

### [2026-09-11] — TODO 1 — secondo tentativo (post-feedback)

- **Esercizio / blocco:** stesso TODO 1; bullet 1 con **400**; bullet 3 dominio + dataset grande → scratch/aggressive FT.
- **Valutazione (nuovo tentativo):** **9.5/10** (primo resta **8.5/10**).
- **Punti di forza:** struttura colloquio completa; freeze→head→layer4; due condizioni di cambio idea sensate.
- **Nit:** “migliaia e migliaia” ok; da colloquio ancora meglio “centinaia di migliaia / milioni”; “aggessivo” → aggressivo.
- **Pattern errore / ID contesto:** nessuno.

### [2026-09-11] — TODO 2 — refactoring costruisci_modello_bello

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 2 (righe ~1766–1797).
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**.
- **Punti di forza:** firma con `nome_arch` / `num_classi` / freeze opzionale; `getattr(models, nome_arch)`; `in_features` al posto di 512; eliminato il ramo ridondante `if n==2`; API pesi al posto di `pretrained=True` (idea).
- **Errori / lacune:**
  1. `m.fc = (n_features, num_classi)` → manca **`nn.Linear(...)`** (assegna una tupla, non un layer).
  2. Typo: `weigths` → **`weights`**.
  3. Default `pesi=models.ResNet18_Weights.DEFAULT` rompe se `nome_arch="resnet50"`: i pesi devono combaciare con l’architettura (o map/enum per nome).
  4. (minore) spacing `num_classi = 2`.
- **Quattro problemi della brutta (check):** API deprecata ✅; freeze sempre → parametro ✅; 512 hardcoded → `in_features` ✅; `if n==2` ridondante ✅.
- **Pattern errore / ID contesto:** attenzione al risultato dell’assegnazione (`nn.Linear` vs tupla).

### [2026-09-11] — TODO 2 — secondo tentativo (post-feedback)

- **Esercizio / blocco:** stesso TODO 2; fix `weights=` + `nn.Linear(...)`.
- **Valutazione (nuovo tentativo):** **9/10** (primo resta **6.5/10**).
- **Punti di forza:** funzione coerente; getattr; freeze opzionale; `in_features`; testa corretta.
- **Residuo:** default `pesi=ResNet18_Weights.DEFAULT` ancora legato a ResNet18 se cambi `nome_arch`. Accettabile per il TODO; da colloquio meglio mappa nome→weights o `weights="DEFAULT"` dove supportato.
- **Pattern errore / ID contesto:** nessuno bloccante.

### [2026-09-11] — TODO 3 — DEBUG matmul 32x512 vs 256x2 (🔁 #52)

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 3 (righe ~1799–1829).
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**.
- **Punti di forza:** 3 bullet; individua **256** come sbagliato; collega 512 ad avgpool/flatten ResNet18; 2 = num classi.
- **Errori / lacune:**
  1. Bullet 1: manca **32 = batch** (`x` ha N=32); dice solo il 512.
  2. Bullet 3: “è il 256” ok, ma poco sul **perché** (backbone emette 512, non 256).
  3. **FIX**: `Linear(512, 2)` hardcodato — la consegna chiede che non si rompa su **resnet50** (lì sono **2048**). Serve `nn.Linear(modello.fc.in_features, 2)` **prima** di sovrascrivere (o salvare `in_features` subito dopo il load).
- **Pattern errore / ID contesto:** lacuna **#52** 🟡 — decomposizione parziale; fix non generale. Pattern **#6** soft (vincolo resnet50).

### [2026-09-11] — TODO 3 — secondo tentativo (FIX in_features)

- **Esercizio / blocco:** stesso TODO 3; FIX con `n_features = modello.fc.in_features` prima del replace.
- **Valutazione (nuovo tentativo):** **8.5/10** (primo resta **6.5/10**).
- **Punti di forza:** fix portabile ResNet18/50; ordine load → leggi `in_features` → sostituisci. Chiude il vincolo della consegna sul FIX.
- **Errori / lacune residui:** bullet 1 ancora senza esplicitare **32 = batch size**; bullet 3 ancora corto sul perché (512 dal backbone vs 256 inventato). Decomposizione numeri non ancora al 100% della consegna.
- **Pattern errore / ID contesto:** #52 in miglioramento sul fix; decomposizione verbale da rinforzare.

### [2026-09-14] — TODO 4 — retrieval metriche_binarie

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 4 (righe ~1832–1864).
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**.
- **Punti di forza:** maschere allineate + `&` + `.sum()` per tp/tn/fp/fn; formule precision/recall/F1 corrette; dict completo con tutte le chiavi; F1 protetto su `somma==0`; usa `classe_positiva`.
- **Errori / lacune:** consegna chiede gestione denominatore zero — **manca** su `recall = tp/(tp+fn)` e `precision = tp/(tp+fp)` (ZeroDivisionError / nan se nessun positivo vero o nessuna pred positiva). Pattern #6 soft sul vincolo esplicito della consegna.
- **Fix atteso:** stesso schema dell’F1, es. `recall = tp/(tp+fn) if (tp+fn) else 0.0` (e analogo per precision).
- **Pattern errore / ID contesto:** #53 in miglioramento sul codice; edge case denominatore ancora fragile.

### [2026-09-14] — TODO 4 — Fix tentato (denom ancora sbagliato)

- **Esercizio / blocco:** stesso TODO 4; riga tipo `tp/(tp+fn) if tp/(tp+fn) != 0 else 0.0`.
- **Nota:** non è ancora corretto — la divisione si valuta comunque (crash se denom=0); e `!= 0` controlla il risultato, non il denominatore. Atteso: `if (tp + fn) else 0.0`.
- **Voto esame:** resta **7.5/10**.

### [2026-09-14] — TODO 4 — Fix applicato (guardie denom)

- **Esercizio / blocco:** stesso TODO 4; `if (tp+fn) != 0` / `if (tp+fp) != 0` + F1 su `somma`.
- **Valutazione fix:** **10/10** sul merito (voto esame primo tentativo resta **7.5/10**).
- **Punti di forza:** conteggi, formule e edge case denominatore tutti a posto.

### [2026-09-14] — TODO 5 — interleaving feature visiva + leakage

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 5 (righe ~1865–1897).
- **Valutazione (primo tentativo — "voto esame"):** **7/10**.
- **Punti di forza (codice):** check `len`, `copy()`, colonna `prob_busta_paga_visivo`, `return`, `ValueError` chiaro. Concetto: riconosce **leakage**.
- **Errori / lacune (prosa):** (1) “probabilità di alterazione” — qui è prob. **busta paga**, non alterazione M2; (2) rimedio troppo radicale (“non usare questo dato”): si può usare la feature, ma le probabilità sul train tabellare devono venire da CNN **non allenata su quelle stesse righe** (es. CNN fit solo su train, pred su val/test; o out-of-fold). Senza quello il tabellare “vede” un segnale già calibrato sulle etichette → metriche gonfiate.
- **Pattern errore / ID contesto:** Data leakage 🟡 — diagnosi ok, riparo incompleto.

### [2026-09-14] — TODO 5 — secondo tentativo (prosa leakage)

- **Esercizio / blocco:** stesso TODO 5; risposta concettuale riscritta.
- **Valutazione (nuovo tentativo):** **9.5/10** (primo resta **7/10**).
- **Punti di forza:** leakage + CNN e tabellare non sulle stesse righe; cita **out-of-fold**. Codice invariato e già ok.
- **Nit:** “set diversi” va inteso come split/OOF sullo stesso progetto, non due dataset sconnessi; in produzione la CNN può predire su documenti nuovi senza problema.
- **Pattern errore / ID contesto:** Data leakage in chiusura su questo TODO.

### [2026-09-14] — TODO 6 — REAL-WORLD piano dataset sporco

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 6 (righe ~1898–1922).
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**.
- **Punti di forza:** idea multipagina → pagina utile; scartare illeggibili; punto 4 sul gruppo azienda (rischio **non** solo qualità); punto 5 ribilanciare `altro` vs buste (bias “pulito vs sporco”).
- **Errori / lacune:**
  1. Formato: chiesti **5 punti + una riga di motivo ciascuno** — motivi assenti/fusi (Pattern #6).
  2. Punto 1: 173≠200 non implica “etichette senza immagine”; sono semplicemente **meno file** del target.
  3. Punto 4: “solo nel train” impreciso — regola = **non spezzare** il gruppo (tutti train **o** tutti val/test); 60/173 in un solo split crea anche **sbilanciamento**.
  4. Non affrontati: **duplicati** (stesso contenuto, nome diverso), gestione foto cellulare (augmentation vs esclusione), ordine operativo (inventario/dedup prima dello split).
- **Pattern errore / ID contesto:** Pattern **#6**; leakage per gruppo / imbalance.

### [2026-09-14] — TODO 6 — secondo tentativo

- **Esercizio / blocco:** stesso TODO 6; piano riscritto.
- **Valutazione (nuovo tentativo):** **7.5/10** (primo resta **5.5/10**).
- **Punti di forza:** (1) inventario prima dello split per azienda; (2–3) multipagina + drop illeggibili; (5) ribilanciare `altro` vs bias qualità; (4) rischio non-qualità = concentrazione aziendale.
- **Errori / lacune:** ancora **duplicati** assenti; punto 4 confuso (“% aziende non avrebbe senso” — lo split **è** per azienda/gruppo; il problema è il gruppo da 60 file che resta intero e sbilancia); formato motivo ancora fuso nella stessa frase; foto cellulare non esplicitate (augmentation vs policy).
- **Pattern errore / ID contesto:** Pattern #6 soft; group split.

### [2026-09-14] — TODO 7 — shape gymnastics ResNet 320×320

- **Esercizio / blocco:** `09_transfer_learning.py` TODO 7 (righe ~1924–1941).
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**.
- **Punti di forza:** tutte e 7 le shape corrette (come V7): 160→80→80→40→20→10→1×1; canali ok.
- **Errori / lacune (perché Linear):** il punto chiave è **`AdaptiveAvgPool2d((1,1))`** → sempre vettore **512**, indipendente da H/W (320 vs 224). Citare il flatten è ok ma secondario. Sbagliato: `Linear(512, 1000)` — la domanda parla di `Linear(512, 2)`; e 1000 non spiega perché 320 funziona.
- **Pattern errore / ID contesto:** #51/#28 ok sulle shape; residuo sul ruolo di avgpool vs testa.

### [2026-09-14] — Reimpostazione 🏗️ TRACK PROVA (Ants vs Bees)

- **Decisione:** niente dataset buste ~400 per chiudere ora il pipeline transfer.
- **Fatto:** script `prepara_dataset_proxy_ants_bees.py`; sezione progetto cap.09 riscritta (P1–P6 prova + C1–C8 debito prodotto); `.gitignore` su `dati/proxy_ants_bees/` e `_cache/`; `INDICE_BUSTA=1` vale anche per `bees`.
- **Next studente:** lanciare lo script → Colab training → `ants_vs_bees.pt`.

### [2026-09-14] — TRACK PROVA Ants vs Bees (valutazione pipeline)

- **Valutazione complessiva track:** **7.5/10**.
- **Punti di forza (Colab):** training due fasi ok; F2 finale train **0.967** / val **0.907**; test ~**0.889**; `class_to_idx` ants=0 bees=1; load `state_dict` + `valuta` su test funzionanti. P1–P4 sostanzialmente chiusi.
- **Mancanze checkpoint:** P5 incompleto (niente report per classe / CM / tabella soglie); P6 README 5 righe **non** ancora nel diario; `.pt` non trovato in repo (scaricato? solo su Colab?).
- **Codice appiccicato in `09_transfer_learning.py` (righe ~2033–2268):** problemi strutturali:
  1. secondo `from __future__ import annotations` a metà file → rischio SyntaxError se si esegue il capitolo intero;
  2. ridichiarazione funzioni già presenti sopra (duplicati);
  3. `percorso_pesi = ROOT/"dati"/"pesi"` passato a `pipeline_addestramento` come **cartella**, poi `torch.load(percorso_pesi/"bees_vs_ants.pt")` — incoerente (serve un path **file** `.pt` nello `save`);
  4. nel blocco manca `def valuta` (usa quella sopra solo se non isoli il pezzo);
  5. dopo load: meglio `modello.to(device)` prima di `valuta`;
  6. eseguire `pipeline_addestramento(...)` a livello modulo nel file capitolo = side effect se qualcuno fa Run sul `.py`.
- **Raccomandazione:** spostare il notebook Colab in `modulo_03_dl_cv/colab_track_prova_ants_bees.py` (o `.ipynb`) e nel capitolo lasciare solo commenti + checklist spuntata; completare P5–P6.

### [2026-09-14] — TRACK PROVA — rivalutazione `colab_track_prova_ants_bees.py`

- **Valutazione file + track:** **8/10** (prima track 7.5).
- **Punti di forza:** loop soglie 0.3–0.7 con tp/fp/fn, precision/recall/accuracy e print → **P5 soglie** chiuso sul merito; `valuta` che restituisce `prob_bees`; checklist P1–P4 ancora ok; numeri Colab già noti (val ~90.7%, test ~88.9%).
- **Bug / lacune nel file:**
  1. `percorso_pesi = ROOT/"dati"/"pesi"` (cartella) passato a `pipeline_addestramento` come `percorso_salvataggio` — serve un **file** `.pt`; il load usa `percorso_pesi/"bees_vs_ants.pt"` (incoerente).
  2. **Ordine:** `pipeline_addestramento` chiama `valuta`, ma `def valuta` è **dopo** la chiamata a riga ~296 → a run sequenziale `NameError` (su Colab ok solo se `valuta` era già in una cella sopra).
  3. Dopo `load_state_dict` manca `modello.to(device)`.
  4. P5: ancora niente CM / `valuta_per_classe` (opzionale ma nella checklist).
  5. **P6** README 5 righe nel diario ancora `[ ]`.
  6. Esecuzione a livello modulo (train al import) — meglio `if __name__ == "__main__":`.
- **Next:** fix path `.pt`, spostare `valuta` sopra, P6 nel diario, scaricare pesi in `dati/pesi/`.

---

### [2026-09-14] — Chiusura formale capitolo (voto difficoltà)

- **Voto difficoltà studente:** **8**/10 — motivazione: lunghezza di tutta la pipeline (dati → transfer → metriche → Colab).
- **Esito chiusura:** Fase A–D completate; file capitolo **non** modificato (protocollo H); cap.10 creato con rinforzi #48/#52/#53/#6.
- **Debiti espliciti:** TODO 8 vuoto; P6 README 5 righe; C1–C8 buste; bug minori path `.pt` in `colab_track_prova_ants_bees.py`.

---

## Lacune e dubbi ancora aperti

Ereditate / aggiornate in chiusura (passano a C10):

- 🟡 **#48** — freeze/forward OK; Mini 5.3 secondo tentativo 8/10 (`eval`/`no_grad` ok sul FA; manca ancora il NON FA esplicito); residuo Mini 2.4
- 🟢 **#49** — Mini 3.2 OK; Mini 3.1 fix `repeat` — chiusa in CONTESTO
- 🟡 **#51** + **Pattern #28** — Mini 2.1/2.2 OK; V7 **9.5**/10 — quasi chiuso
- 🟡 **#52** — TODO 3 fix `in_features` OK (2° tent. 8.5); bullet ancora deboli su 32=batch
- 🟡 **#47** — Q1 ordine OK; spiegazione grafo/RAM soft
- 🟢 **#50** — Q2 con floor — chiusa
- 🟡 **#53** — TODO 4 denom OK; residuo Mini 6.2 obiezione numerica
- 🔴 **Pattern #6** — TODO 6 / Mini 6.2
- 📌 Debito prodotto C1–C8; TODO 8; P6 README

---

## Note per il capitolo successivo (mentor)

- Il deliverable di questo capitolo (`ants_vs_bees.pt` track prova; `busta_vs_altro.pt` = debito) è l'input del cap.10 (Gradio + deploy HuggingFace, portfolio piece #2).
- **Chiusura 14/09/2026**: voto **8**/10; creato `10_progetto_gradio.py` + micro R09 09.A–E; residui P6/TODO 8 non bloccanti.
- Se il modello prodotto (quando ci sarà) avesse recall busta < 0.85, valutare dataset "altro" troppo omogeneo prima di cambiare architettura.
