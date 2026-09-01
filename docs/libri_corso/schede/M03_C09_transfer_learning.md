# Scheda — M03 C09 · Transfer learning e fine-tuning

| Campo | Valore |
|-------|--------|
| Capitolo corso | `modulo_03_dl_cv/09_transfer_learning.py` |
| Sezioni corso target | Sez. 1–6 (transfer learning, anatomia ResNet, freezing, augmentation, fine-tuning, metriche) |
| Libri usati | `[PYTORCH]` 1ª ed. (Stevens et al. 2020); `[GERON]` 2ª ed. |
| Data scheda | 2026-09-01 |
| Stato | **usata in capitolo** |

> ⚠️ **Correzione alla mappatura.** `MAPPATURA_LIBRI_MODULI.md` indicava per questo capitolo
> “PYTORCH cap. 12–13”. Verificato sul sommario del PDF locale (1ª ed., 522 pagine):
> il cap. 13 è *Using segmentation to find suspected nodules* (U-Net), fuori scope.
> Le sezioni giuste sono **cap. 2**, **§8.5.3**, **§12.6** e **§14.5.3**.
> Il PDF Géron in `books/` è la **2ª edizione** (Keras/TF2), non la 3ª: cap. 14 confermato.

---

## Fonti lette

| Codice | Capitolo / sezione (pag. PDF) | Cosa serve al corso |
|--------|-------------------------------|---------------------|
| PYTORCH | **Cap. 2 §2.1.3–2.1.5** *Pretrained networks / ResNet* (pp. 51–56) | `models.resnet101(pretrained=True)`, ImageNet = 1.2M immagini / 1000 classi, struttura stampata (`conv1`, `bn1`, `maxpool`, `layer1…`, `avgpool`, `fc`), pipeline `Resize(256) → CenterCrop(224) → ToTensor → Normalize(mean, std)`, `model.eval()` obbligatorio in inferenza |
| PYTORCH | **§8.5.3** *Going deeper to learn more complex structures: Depth* (p. 252) | Perché reti profonde si allenano male senza trucchi → skip connection; ponte verso ResNet |
| PYTORCH | **§12.6** *Preventing overfitting with data augmentation* (pp. 375–381) | Non tutte le augmentation sono utili; mirror/shift/scale/rotate/noise; “augmentare **dopo** la cache”; rotazione ammessa solo sugli assi intercambiabili |
| PYTORCH | **§12.3** *False positives / negatives, recall, precision, F1* (pp. 349–358) | Metriche per classe su dataset sbilanciato: l’accuracy globale mente |
| PYTORCH | **§14.5.3** *Reusing preexisting weights: Fine-tuning* (pp. 451–456) | Definizione, `requires_grad_(False)` sui blocchi non allenati, `strict=False` nel `load_state_dict`, depth-1 vs depth-2, unfreezing graduale, learning rate diversi per gruppo di parametri |
| GERON | **Cap. 14** *ResNet* (pp. 500–501) | Skip connection: la rete modella `f(x) = h(x) − x`; all’inizio ≈ identità → training più rapido; stack di residual unit |
| GERON | **Cap. 14** *Using Pretrained Models / Pretrained Models for Transfer Learning* (pp. 508–512) | Riusare i layer bassi quando i dati sono pochi; congelare, allenare la testa per poche epoche, poi scongelare con **learning rate molto più basso** |

---

## Citazioni chiave (parafrasi, niente copia di pagine)

1. **Definizione** — [PYTORCH §14.5.3]: partire da una rete allenata su un compito con dati affini invece che da inizializzazione casuale è *transfer learning*; quando si allenano solo gli ultimi layer si chiama *fine-tuning*.
2. **Meccanismo** — [PYTORCH §14.5.3]: si tratta una parte (spesso grande) della rete come **estrattore di feature fisso** e si allena solo una porzione piccola sopra.
3. **Quando NON funziona** — [PYTORCH §14.5.3]: su ImageNet si allena col flip orizzontale, quindi le feature di un’immagine e della sua speculare sono quasi identiche. Per un compito dove destra/sinistra conta (cartelli “svolta a destra/sinistra”) il modello pre-addestrato sbaglia sistematicamente. → **Ponte diretto sui documenti**: una busta paga specchiata non è una busta paga; niente `RandomHorizontalFlip`.
4. **Augmentation** — [PYTORCH §12.6]: randomizzare i 4 pixel d’angolo moltiplica il dataset per miliardi e non serve a nulla; il flip di un volto lo raddoppia soltanto ma ogni immagine è utile. Criterio: la trasformazione deve restare **rappresentativa** e non banalmente memorizzabile.
5. **Procedura in due fasi** — [GERON cap. 14]: congela la base, allena la testa poche epoche (arriva ~75–80% e si ferma), poi scongela e continua con learning rate molto più basso “per non danneggiare i pesi pre-addestrati” (~95% finale).
6. **Se la testa non basta** — [PYTORCH §14.5.3]: tre cause possibili (feature non utili al nuovo compito / testa troppo piccola / rete troppo piccola). Rimedio provato nel libro: includere anche l’ultimo blocco convoluzionale (`--finetune-depth 2`) → migliora, ma **va in overfitting prima** → serve regolarizzazione.
7. **Preprocessing** — [PYTORCH cap. 2]: la normalizzazione deve corrispondere a quella usata in training, altrimenti le risposte non hanno senso. Valori ImageNet: `mean=[0.485,0.456,0.406]`, `std=[0.229,0.224,0.225]`.
8. **Skip connection** — [GERON cap. 14]: aggiungendo l’input all’uscita, la rete parte dall’identità; il segnale attraversa tutta la rete anche se alcuni layer non hanno ancora imparato.

---

## Concetti da portare nel corso

1. Backbone (estrattore di feature) + head (classificatore) = la separazione mentale di tutto il capitolo.
2. Feature **generiche** nei primi layer (bordi, gradienti, texture) → **specifiche** negli ultimi (parti di gatto). Un documento ha bordi, righe e texture di testo: i primi layer trasferiscono, gli ultimi vanno riallenati. *(Questa è la teoria che la Regola 42 richiede PRIMA della Feynman.)*
3. `requires_grad = False` = non tracciare le operazioni nel grafo → autograd non calcola quei gradienti → meno memoria e meno tempo, oltre a “pesi bloccati”.
4. Percorso shape ResNet18 su `(N,3,224,224)`: 224 → 112 (conv1 stride 2) → 56 (maxpool) → 56 → 28 → 14 → 7 → `avgpool` 1×1 → `fc(512, n_classi)`.
5. `AdaptiveAvgPool2d((1,1))` rende la testa indipendente dalla dimensione dell’immagine in ingresso.
6. Grayscale → 3 canali: `transforms.Grayscale(num_output_channels=3)` oppure `x.repeat(1,3,1,1)`.
7. Due fasi: head-only (LR normale) → unfreeze `layer4` (LR ~10× più basso).
8. Metriche **per classe** + macro-F1 + confusion matrix; l’accuracy globale non basta.

---

## Analogie / ponti mentali

- Transfer learning = assumere un perito già formato altrove e insegnargli solo le tue pratiche, invece di formarne uno da zero.
- Backbone congelato = libreria di terze parti in `node_modules`: la usi, non la riscrivi.
- Head nuova = il tuo `controller` sopra una libreria che non tocchi.
- Fine-tuning del `layer4` = mettere mano anche all’ultimo strato della libreria perché il tuo dominio è diverso da quello di chi l’ha scritta.
- Skip connection = `return input if nulla_da_aggiungere else input + correzione`.
- Normalizzazione sbagliata = mandare a un’API i valori in centesimi quando si aspetta euro.

---

## Esercizi del libro da ADATTARE

| Idea libro | Adattamento corso |
|------------|-------------------|
| PYTORCH cap. 2: inferenza ResNet101 su una foto di cane | Inferenza ResNet18 pre-addestrata su una busta paga anonimizzata: guardare le classi ImageNet assurde che escono → motivare la sostituzione della `fc` |
| PYTORCH §14.5.3 depth-1 vs depth-2 | 📚 **[LIBRO]** (l’unico del capitolo): confronto head-only vs head+`layer4`, con previsione scritta prima di lanciare il training |
| PYTORCH §12.6 cinque augmentation | Tabella “quale ha senso su un documento e quale no”, con il flip come trappola |
| GERON transfer learning sui fiori | Stessa procedura in due fasi su busta-paga-vs-altro |
| PYTORCH §12.3 recall/precision | Riuso del codice metriche M2 cap.04 → per classe + macro-F1 (lacuna #53) |

---

## Tranelli da inserire

- `ImageFolder` assegna gli indici in ordine **alfabetico**: `altro=0`, `busta_paga=1`. Chi assume il contrario legge la confusion matrix al contrario.
- Augmentation applicata anche a validation/test → metriche non confrontabili.
- Dimenticare `model.eval()` → BatchNorm e Dropout si comportano da training.
- Sostituire `fc` con `Linear(256, 2)` invece di `Linear(512, 2)` → `RuntimeError` matmul (lacuna #52).
- Passare al `Normalize` valori diversi da quelli ImageNet dopo aver caricato pesi ImageNet.
- Split casuale con più scansioni dello stesso cliente → leakage (regola prodotto: split **per cliente**).
- Ottimizzatore costruito su `model.parameters()` dopo il freeze: funziona ma è fuorviante; meglio filtrare `requires_grad`.

---

## Cosa saltare

- Segmentazione / U-Net (PYTORCH cap. 13), object detection, YOLO (GERON cap. 14 finale).
- Architetture Inception/Xception/SENet in dettaglio: solo citate.
- Scheduler di learning rate avanzati, mixed precision, `torch.compile`.
- Gradio e deploy → cap.10.

---

## Blocchi da iniettare

- `# 📚 LETTURA PARALLELA` dopo Sez. 1 (definizione transfer/fine-tuning), Sez. 2 (skip connection), Sez. 4 (augmentation utile vs inutile).
- `# 📚 [LIBRO]` (**max 1**, in fondo agli esercizi): depth-1 vs depth-2 ispirato a §14.5.3.

---

## Note mentor

- Le pagine indicate sono **pagine del PDF** (0-based come restituite da `pypdf`), non i numeri stampati: il libro stampa un offset di ~-29.
- Il capitolo è anche il primo con dati reali: la sezione privacy sta **prima** della teoria, non in appendice.
- `.gitignore` verificato il 01/09/2026: `data/buste_*/` e `dati/buste_*/` già presenti.
