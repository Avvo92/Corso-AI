# Diario sessione — Capitolo 08 — CNN e Computer Vision

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `08_cnn_computer_vision.py` |
| **File diario** | `M03_C08_cnn_computer_vision_sessione.md` |
| **Stato** | aperto (13/08/2026) — file capitolo **scritto**; studio da iniziare dopo bridge R07 |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

- Fashion-MNIST, `(N,C,H,W)`, Conv/Pool, `PiccolaCNN`, feature maps, Colab
- Chiudere residui cap.07 nei 🔁 / quiz ingresso / TODO 5–6 / 🏗️
- Niente buste paga (privacy) — dataset pubblico only
- Libri: scheda `M03_C08_cnn.md` ([PYTORCH] cap.7–8 1ª ed., [GERON] 14)

---

## Domande durante lo studio

- **2026-08-23** — Su Colab `Path(__file__).parent / "dati"...` non funziona: in cella notebook `__file__` non esiste (`NameError`). Fix capitolo: fallback `Path.cwd()`.
- **2026-08-23** — Perché C è prima in `(1,28,28)` / PyTorch vs Matplotlib: convenzione `(C,H,W)` vs `(H,W)` o `(H,W,C)`.
- **2026-08-23** — Modello mentale CNN: filtri → pattern; corretto soft che non è “1 filtro = 1 logit softmax”.
- **2026-08-23** — Difficoltà a tenere il passo con i cambi di shape (Conv/Pool/Flatten) — normale; antidoto: tabella N,C,H,W a ogni layer.
- **2026-08-23** — Blocco mentale passaggio dense → CNN: rinforzare ponte “stesso training, cambia solo come leggi l’immagine”.
- **2026-08-23** — Click: feature map ≠ pixel; ogni cella = prodotto-somma del kernel in una posizione (es. 26×26 con pad=0).
- **2026-08-23** — Formulazione Conv ok: formula size → appoggia kernel → prodotto-somma → scrive in mappa (× out_channels).
- **2026-08-23** — Chiarito: canali dopo il 1° Conv ≠ colori RGB; sono feature map.
- **2026-08-23** — Kernel RGB 3×3: patch 3×3×3 → 27 prodotti, somma (+ bias) = 1 cella della feature map.
- **2026-08-23** — Confermato: uscita Conv = `(N, out_channels, H_out, W_out)`.
- **2026-08-23** — ReLU: stessa shape, elemento per elemento max(0,x).
- **2026-08-23** — MaxPool2: H e W dimezzati ciascuno (area ÷4), C uguale. “Semplificazione” ok (thumbnail / max locale).
- **2026-08-23** — Etimologia/senso di “convoluzione”.
- **2026-08-25** — “Convoluzionare” ≠ solo scorrere: scorrere + prodotto-somma; pool scorre ma non è Conv.
- **2026-08-25** — `classifier` Linear → logits `(N, 10)`, non probabilità (softmax nella CrossEntropy).
- **2026-08-25** — `optim.Adam(model.parameters(), lr=...)` spiegato.
- **2026-08-25** — SGD = Stochastic Gradient Descent.
- **2026-08-25** — Perché mini-batch vs tutto il dataset (memoria, velocità, rumore utile).
- **2026-08-25** — Confermato: full-batch 60k → grafo/attivazioni/grad troppo grandi in RAM.
- **2026-08-25** — `model.to(device)` = sposta pesi su CPU o GPU.
- **2026-08-25** — Commenti didattici su ogni step di `PiccolaCNN` (shape + ruolo layer).
- **2026-08-25** — Commenti su `accuracy_logits`, `train_cnn_epochs`, `feature_maps_primo_conv` + demo Sez.4.
- **2026-08-25** — Modello mentale: lungo la CNN, H×W ↓ e C ↑ (tipico).
- **2026-08-25** — CNN grandi = stessi mattoni, più profondità; ImageNet ~1000 classi (non “migliaia” sempre).
- **2026-08-25** — CNN vs face ID vs generativi (diffusion/U-Net/transformer): parentela, non stessa cosa.
- **2026-08-25** — Roadmap: M3 transfer/YOLO; M5 vision LLM; no modulo dedicato diffusion/DALL·E.
- **2026-08-25** — `flatten(x, 1)` = tieni N, schiaccia da C in poi.
- **2026-08-25** — Confermato: `start_dim` = indice (incluso) da cui inizia il flatten.
- **2026-08-25** — Chiesta analisi difficoltà attesa M4 vs M3.
- **2026-08-25** — Richiesta mini-corso React/Node in vista UI M10 (React+FastAPI); ora focus M3.
- **2026-08-25** — **Canonizzato** ripasso React/Node: `CONTESTO_CORSO` Impegno, `roadmap` Fase 0b, `docs/ripasso_frontend_react/`, prodotto README/REPLICATOR/ARCHITETTURA, AGENTS, APPUNTI stub.
- **2026-08-25** — Aggiunto blocco teoria CrossEntropy target Long vs one-hot prima Mini 4.2 (gap didattico segnalato dallo studente).
- **2026-08-25** — Espansa teoria FC vs Conv (Sez.2) + consegna 📚; **Regola 42** canonizzata (teoria prima di esercizi discorsivi).
- **2026-08-25** — `argmax(dim=1)` vs dim=0: dim=0 non crasha argmax, ma semantica sbagliata.

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### 2026-08-22 — Bridge M03_R08 Q1 shape HWC (`M03_R08_...md` ~9–11)

- **Esercizio / blocco:** Shape immagine RGB 64×64 in formato height, width, channels
- **Valutazione (primo tentativo — "voto esame"):** **3/10**
- **Punti di forza:** Ha messo H=64, W=64 e C=3 (RGB) nell’ordine giusto all’inizio.
- **Errori / lacune:** Aggiunto un 4° asse `256` → shape corretta è **`(64, 64, 3)`**. Il `256` non è una dimensione: tipicamente confonde con i livelli di intensità pixel (0–255) o con altro contesto.
- **Correzione / suggerimento:** HWC = tre numeri. NCHW PyTorch = `(N, C, H, W)` — lì il batch `N` è un’altra storia.
- **Nota mentor:** file bridge è **R08** (dopo C08→prima C09); se C08 non è ancora studiato, il bridge da fare ora è **R07**.

### 2026-08-22 — Quiz ingresso Q1 training step (`08_cnn_computer_vision.py` ~130–133)

- **Esercizio / blocco:** completa ordine `____ → forward+loss → ____ → optimizer.step()`
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `optimizer.zero_grad()` → forward+loss → `loss.backward()` → `optimizer.step()` — ordine e naming corretti a freddo.
- **Errori / lacune:** Nessuno.
- **Pattern errore / ID contesto:** #45 fill-in `backward` → verifica a freddo **ok** → 🟢

### 2026-08-22 — Quiz ingresso Q2 retrieval 5-step (#45) (`08_cnn_computer_vision.py` ~135–147)

- **Esercizio / blocco:** 5 bullet `dZ2→…→grad_W1` + fill-in PyTorch
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** Catena completa e nell’ordine giusto (dZ2≈p−y → W2/b2 → dH → dZ1 via ReLU′ → W1/b1); fill-in **`loss.backward()`** presente.
- **Errori / lacune:** Soft: spesso `(p−y)/N` se loss = mean sul batch.
- **Pattern errore / ID contesto:** #45 confermata 🟢 (anche retrieval catena, non solo naming)

### 2026-08-22 — Quiz ingresso Q3 Pattern #27 (`08_cnn_computer_vision.py` ~150–154)

- **Esercizio / blocco:** `p*(1-?)` — `?` = p o y?
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** `? = p` corretto; effetto numerico di `y` (`p` o `0`) descritto.
- **Errori / lacune:** Ancora manca il perché #27: derivata sigmoid dipende da **`p`**, non dall’etichetta **`y`** (simbolo sbagliato in formula→codice). Soft: “p * 1 0 p * 0” poco leggibile → meglio `y=0→p`, `y=1→0`.
- **Correzione / suggerimento:** “`y` è label; `σ′=p(1−p)` usa solo la probabilità.”
- **Pattern errore / ID contesto:** #27 resta 🔴 (riconosce la forma, perché concettuale incompleto)
- **Rivalutazione (post-fix, richiesta esplicita):** **9.5/10** — aggiunto: simbolo sbagliato + σ′ dipende da **p** non da **y**. Soft: typo “probibilità”; “p * 1 0 p * 0” ancora poco chiaro → `y=0→p`, `y=1→0`. **#27** → 🟡 in miglioramento (forma + perché ok post-fix; tenere vivo nei micro).

### 2026-08-22 — Quiz ingresso Q4 zero_grad V/F (`08_cnn_computer_vision.py` ~156–159)

- **Esercizio / blocco:** basta `zero_grad` una volta prima del `for epoch`?
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** **Falso** + motivo accumulo gradienti / `step()` sballato — corretto.
- **Errori / lacune:** Frequenza: non “ogni **epoch**”, ma **ogni batch/step** (prima di ogni `backward`). Stesso soft di R07 Q13.
- **Correzione / suggerimento:** `zero_grad` → forward → loss → `backward` → `step` **per ogni batch**.

### 2026-08-22 — Quiz ingresso Q5 map_location (#46) (`08_cnn_computer_vision.py` ~161–164)

- **Esercizio / blocco:** `torch.load(..., map_location=?)` Colab GPU → PC AMD
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** `map_location="cpu"` corretto; legame AMD ≠ CUDA chiaro.
- **Errori / lacune:** Soft: non solo “CUDA non disponibile”, ma i pesi sono **salvati su device CUDA** e vanno **rimappati** sulla CPU (altrimenti load cerca una GPU CUDA assente).
- **Correzione / suggerimento:** “`\"cpu\"` rimappa i tensori del checkpoint da CUDA a CPU.”
- **Pattern errore / ID contesto:** #46 map_location — confermato in miglioramento

### 2026-08-22 — Quiz ingresso Q6 Feynman Dataset vs DataLoader (#46) (`08_cnn_computer_vision.py` ~166–169)

- **Esercizio / blocco:** Feynman max 4 frasi Dataset vs DataLoader
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Analogia chiara: Dataset = collezione sullo scaffale; DataLoader = chi serve i pezzi “come glielo chiedi” (batch size / shuffle). Molto meglio del “Dataset = intero batch” di R07 Q9.
- **Errori / lacune:** Soft: esplicitare **batch** (pacchetti di N esempi) e che alimenta il **training loop**; “magazziniere” ok, ponte corso = **carrello**.
- **Correzione / suggerimento:** Dataset espone campioni; DataLoader costruisce batch (+shuffle) per il loop.
- **Pattern errore / ID contesto:** #46 lato DataLoader → in miglioramento forte

### 2026-08-22 — Quiz ingresso Q7 `.item()` vs `backward` (`08_cnn_computer_vision.py` ~172–174)

- **Esercizio / blocco:** `.item()` sulla loss: prima o dopo `backward` se serve il grafo?
- **Valutazione (primo tentativo — "voto esame"):** **2/10**
- **Punti di forza:** —
- **Errori / lacune:** Risposto **Prima** — atteso **Dopo**. Se ti serve il grafo per `backward`, la `loss` deve restare **tensore**; `.item()` (float Python) è per il **log**, tipicamente dopo (o senza riassegnare `loss = loss.item()` prima del backward — quello spezza il grafo).
- **Correzione / suggerimento:** `loss.backward()` poi `print(loss.item())` / accumula `.item()` per media epoch.
- **Pattern errore / ID contesto:** soft ripresa errore TODO 2 cap.07 (`.item()` troppo presto)

### 2026-08-23 — Quiz ingresso Q8 `requires_grad` (`08_cnn_computer_vision.py` ~176–179)

- **Esercizio / blocco:** a cosa serve `requires_grad=True` (1-2 frasi)
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**
- **Punti di forza:** Collega il flag al **backward** e al fatto che quel tensore può ricevere un gradiente.
- **Errori / lacune:** Non è il **criterio**/loss che calcola i gradienti: è **autograd**. Manca il pezzo chiave: chiede di **tracciare le operazioni** su quel tensore per **costruire il grafo**, così a `backward` si riempie `.grad`.
- **Correzione / suggerimento:** “`requires_grad=True` = attiva il diario (grafo) delle ops su quel tensore; al `backward` autograd scrive `.grad`.”
- **Pattern errore / ID contesto:** soft autograd vs “criterio” (vicino a confusione R07 Q1 requires_grad≠GPU)

### 2026-08-23 — Rinforzo Micro 27.A/B (`08_cnn_computer_vision.py` ~182–198)

- **Esercizio / blocco:** `(1-p)` vs `(1-y)` con y=1, p=0.9
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** 27.B: `(1-1) != (1-0.9)` coglie il cuore numerico; con y=1 `(1-y)=0` azzera, `(1-p)=0.1` no.
- **Errori / lacune:** Soft: esplicitare la conseguenza (“con `(1-y)` il fattore diventa 0 e spegni il segnale; con `(1-p)` resta 0.1 informativo”). 27.A (completare `1-p`) non scritto a parte ma già nel template.
- **Correzione / suggerimento:** y=1 → bug azzera; p=0.9 → ok lascia 0.1.
- **Pattern errore / ID contesto:** #27 — micro ok, resta 🟡

### 2026-08-23 — Rinforzo Micro 45.A (`08_cnn_computer_vision.py` ~204–225)

- **Esercizio / blocco:** 5 bullet backward + fill-in `loss.backward()`
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** Ordine globale ok (dZ2 → … → W1); dH, dZ1, W1/b1 corretti; `loss.backward()` presente nel fill-in.
- **Errori / lacune:** Bullet (2): formula di **W2** (`H.T @ dZ2`, `db2`) ma etichettata **`grad_w1`** (e nella stessa riga `grad_b2`) — slip naming layer. Soft fill-in: la consegna chiedeva soprattutto “li fa **`loss.backward()`**”; lo step intero (`zero_grad`→…) è ok ma è il training loop, non solo i 5 step del backward.
- **Correzione / suggerimento:** (2) = **`dW2` / `db2`** da `dZ2` e `H`; (5) = **`dW1` / `db1`** da `dZ1` e `X`.
- **Pattern errore / ID contesto:** #45 🟢 naming `backward` ok; soft attenzione etichette W1 vs W2
- **Rivalutazione (post-fix, richiesta esplicita):** **9/10** — bullet (2) ora **`grad_W2`** corretto; catena completa. Soft: **manca il fill-in** esplicito “In PyTorch → `loss.backward()`” (c’era prima, ora assente sotto i bullet). Soft opzionale: `(p−y)/N`.
- **Nota (chat):** fill-in già in consegna = soft non conteggiato → catena **9.5/10**.

### 2026-08-23 — Rinforzo Micro 46.A/B (`08_cnn_computer_vision.py` ~234–239)

- **Esercizio / blocco:** `map_location="cpu"` + Dataset vs DataLoader operativo
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** 46.B operativo e chiaro: collezione vs carrello che prende/mescola/serve al training. 46.A `"cpu"` (in template) allineato.
- **Errori / lacune:** Soft: dire esplicitamente **batch** (pacchetti di N) — “rende disponibili” è un filo generico.
- **Correzione / suggerimento:** DataLoader → batch (+ shuffle) verso il loop.
- **Pattern errore / ID contesto:** #46 → candidata 🟢
- **Fix applicato (chat):** aggiunto “batch di N esempi” → formulazione **10/10**; #46 🟢 confermata.

### 2026-08-23 — Quiz ingresso Q1 (riconferma) (`08_cnn_computer_vision.py` ~128–131)

- **Esercizio / blocco:** ordine training step PyTorch
- **Valutazione:** **10/10** (allineata al primo tentativo 22/08)
- **Punti di forza:** `zero_grad` → forward+loss → `backward` → `step` corretto.
- **Errori / lacune:** Nessuno.

### 2026-08-23 — Mini 1.1 sample #10 + plot (`08_cnn_computer_vision.py` ~304–319)

- **Esercizio / blocco:** immagine 10, shape, label, `imshow` grayscale
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** Indice coerente se “10ª” = `[9]`; shape/label stampati; `squeeze()` + `cmap="gray"` giusti per Fashion-MNIST 1 canale.
- **Errori / lacune:** **`plt.show` senza `()`** → non esegue lo show, solo riferisce la funzione. Soft: `img, y = ds_demo[9]` una sola volta; se “indice 10” era `ds_demo[10]`. Soft: guard `if ds_demo is not None and PLOT_OK`.
- **Correzione / suggerimento:** `plt.show()`; opzionale unpacking.
- **Rivalutazione (post-fix, richiesta esplicita):** **9.5/10** — `ds_demo[10]` + `plt.show()` corretti. Soft residuo: unpacking `img, y = ds_demo[10]` e/o guard `PLOT_OK`.

### 2026-08-23 — Mini 1.2 squeeze/permute vs Matplotlib (`08_cnn_computer_vision.py` ~322–327)

- **Esercizio / blocco:** perché squeeze/permute su tensore `(1, 28, 28)`
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**
- **Punti di forza:** Matplotlib in grayscale vuole tipicamente **`(H, W)`** — pezzo giusto.
- **Errori / lacune:** Il `1` in `(1, 28, 28)` è il **canale C** (PyTorch `(C,H,W)`), **non** N (batch) né “numero di righe”. `squeeze()` toglie le dimensioni di **size 1** (qui C), non le righe. `permute` serve soprattutto per RGB: `(C,H,W)` → `(H,W,C)`.
- **Correzione / suggerimento:** “`(1,28,28)` = 1 canale × 28 × 28; squeeze → `(28,28)` per `imshow`.”

### 2026-08-23 — Mini 2.1 H_out a mano (`08_cnn_computer_vision.py` ~373–379)

- **Esercizio / blocco:** H=W=28, k=3, pad=0, stride=1 → H_out, W_out
- **Valutazione (primo tentativo — "voto esame"):** **6/10**
- **Punti di forza:** Parte `(28 + 2*0 - 3) / 1 = 25` ok.
- **Errori / lacune:** Manca il **`+ 1`** della formula → corretto **26** (non 25).
- **Correzione / suggerimento:** `H_out = (H + 2*pad - k) / stride + 1` → `25 + 1 = 26`.

### 2026-08-23 — Mini 2.2 Conv2d 1→16 k=5 pad=2 (`08_cnn_computer_vision.py` ~381–393)

- **Esercizio / blocco:** crea Conv, applica a `randn(2,1,28,28)`, stampa shape
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `Conv2d(1,16,5,padding=2)` corretto; forward su batch 2; `no_grad` ok. Shape attesa **`(2, 16, 28, 28)`**.
- **Errori / lacune:** Soft: consegna “UNA riga” — qui più righe, ma chiaro e corretto.
- **Correzione / suggerimento:** verifica print: `(2, 16, 28, 28)`.

### 2026-08-25 — Mini 3.1 shape dopo Pool→Conv32→Pool (`08_cnn_computer_vision.py` ~421–444)

- **Esercizio / blocco:** `(N,16,28,28)` → Pool → Conv32 (keep HW) → Pool → shape finale
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Risposta `(5, 32, 7, 7)` (N=5) = caso di `(N, 32, 7, 7)`. Codice allineato: Pool→Conv(16→32,k=3,pad=1)→Pool; print shape.
- **Errori / lacune:** Nessuno.
- **Correzione / suggerimento:** Percorso: `(5,16,28,28)`→`(5,16,14,14)`→`(5,32,14,14)`→`(5,32,7,7)`.

### 2026-08-25 — Mini 3.2 pooling impara pesi? (`08_cnn_computer_vision.py` ~447–450)

- **Esercizio / blocco:** V/F pooling impara pesi come Conv2d
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** **Falso** corretto; idea max nel timbro + thumbnail senza apprendimento — ok.
- **Errori / lacune:** Soft: “convoluzionando” può confondere — il pool **scorre** una finestra, ma **non** fa prodotto-somma con pesi; non c’è kernel appreso.
- **Correzione / suggerimento:** “Pool = regola fissa (max/avg); Conv = pesi imparati.”

### 2026-08-26 — 📚 [LIBRO] FC flatten vs Conv+Pool (`08_cnn_computer_vision.py` ~647–659)

- **Esercizio / blocco:** 5–8 frasi: perché solo Linear su flatten generalizza peggio di Conv+Pool (stesso training)
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Tre pilastri giusti: esplosione parametri; geometria/correlazione pixel ignorata; traslazione → nuovi pesi. Niente copia; parole proprie.
- **Errori / lacune:** Ultima frase debole: Conv+Pool non è solo “ridimensionare”; manca esplicito parameter sharing (stesso filtro ovunque) e che il Linear finale classifica *feature*, non pixel grezzi. “Decine di migliaia” sottostima (Linear 784→256 ≈ 200k).
- **Correzione / suggerimento:** Rinforzare: Conv = pattern locali + pesi condivisi; Pool = downsample + tolleranza spostamenti; poi Linear piccolo sulle mappe.
- **Lacune contesto:** nessuna nuova 🔴 (concetto solido).

### 2026-08-26 — Mini 4.1 parametri primo Conv2d (`08_cnn_computer_vision.py` ~661–667)

- **Esercizio / blocco:** Conta parametri Conv2d(1,16,k=3,pad=1)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `1×16×3×3=144` pesi + `16` bias = **160**; padding non contato (giusto: pad non aggiunge pesi).
- **Errori / lacune:** Nessuno. Naming informale (`base_kernel`/`altezza_kernel`) ok al posto di `k×k`.
- **Correzione / suggerimento:** Formula ufficiale: `out_ch * in_ch * k * k + out_ch`.

### 2026-08-26 — Mini 4.2 CrossEntropy target Long vs one-hot (`08_cnn_computer_vision.py` ~697–702)

- **Esercizio / blocco:** Perché CE vuole target Long (N,) e non float one-hot
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** Mutual exclusivity → basta un’etichetta per immagine: giusto (cuore del blocco [3]).
- **Errori / lacune:** Manca il “perché API/PyTorch”: CE fa softmax+NLL *sull’indice*; one-hot sarebbe ridondante e tipico di altre loss; **Long** = intero usato come indice del cassetto (non float 0/1).
- **Correzione / suggerimento:** Completare: esclusività + indice Long compatto + API pensata così (vs BCE soft-label / multi-label).
- **Lacune contesto:** soft — confronto CE vs BCE target shapes; non aprire 🔴 se completa in chat/fix.

### 2026-08-26 — Mini 4.2 (post-feedback) CrossEntropy Long vs one-hot

- **Esercizio / blocco:** `08_cnn_computer_vision.py` ~701–702 (riscrittura dopo 7/10)
- **Valutazione (post-feedback — non ricalcola il voto esame):** **9.5/10**
- **Punti di forza:** Esclusive + indice Long che seleziona la classe per la CE + one-hot ridondante: pacchetto completo.
- **Errori / lacune:** Soft: in pratica CE lavora sui logits (`log_softmax` interno), non su un vettore softmax già materializzato — ma l’idea “indice → classe giusta” è corretta.
- **Nota:** voto esame resta **7/10**; questa è la qualità dopo il fix.

### 2026-08-26 — Mini 5.1 feature maps primo Conv (`08_cnn_computer_vision.py` ~715–752)

- **Esercizio / blocco:** shape maps + griglia visualizzazione
- **Valutazione (primo tentativo valido — "voto esame"):** **9.5/10**
- **Nota mentor:** valutazione precedente (8/10 su paste incompleto/`cmqp`/formula `+k`) **annullata** su richiesta studente: codice Colab corretto non era ancora nel file.
- **Punti di forza:** Shape **(16, 28, 28)**; formula `(H+2p-k)/stride+1` con numeri 28→28; helper + `4×4` + loop + `detach().cpu().numpy()` + **`cmap="gray"`** + `show`.
- **Errori / lacune:** Nessuno bloccante. Soft opzionale: `ax.axis("off")` per leggibilità; `PiccolaCNN()` fresco = mappe random (atteso dalla consegna).
- **Correzione / suggerimento:** Nessuna obbligatoria.

### 2026-08-26 — Mini 5.2 feature maps ≠ probabilità classi (`08_cnn_computer_vision.py` ~753–757)

- **Esercizio / blocco:** V/F feature maps primo layer = probabilità 10 classi
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** **Falso** corretto; spiega attivazioni per filtro/kernel (mappa risposta locale), non softmax a 10 classi.
- **Errori / lacune:** Nessuno. Soft opzionale: le 10 probabilità arrivano solo dopo flatten+Linear(+CE/softmax), non dal primo Conv.
- **Correzione / suggerimento:** Nessuna obbligatoria.

### 2026-08-26 — Quiz verifica V1 shape batch (`08_cnn_computer_vision.py` ~763–765)

- **Esercizio / blocco:** Shape batch Fashion-MNIST batch_size=32
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `(32, 1, 28, 28)` = NCHW corretto (grayscale C=1).
- **Errori / lacune:** Nessuno.

### 2026-08-26 — Quiz verifica V2 Conv2d shape (`08_cnn_computer_vision.py` ~767–770)

- **Esercizio / blocco:** Conv2d(1,8,3,pad=1) su (4,1,28,28)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `(4, 8, 28, 28)` + formula H/W corretta; N invariato, C=out_channels.
- **Errori / lacune:** Nessuno.

### 2026-08-26 — Quiz verifica V3 MaxPool no pesi (`08_cnn_computer_vision.py` ~771–775)

- **Esercizio / blocco:** Errore concettuale “MaxPool impara 4 pesi”
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** Errore individuato: niente pesi appresi; max su finestra 2×2; esempio shape `(4,8,28,28)→(4,8,14,14)` corretto (area ÷4).
- **Errori / lacune:** Soft: “4 volte la dimensione” meglio “ogni lato ÷2 (area ÷4)”; Pool non è legato solo al Conv (opera su qualsiasi tensore 4D).
- **Correzione / suggerimento:** Nessuna obbligatoria.

### 2026-08-26 — Quiz verifica V4 due MaxPool (`08_cnn_computer_vision.py` ~776–779)

- **Esercizio / blocco:** Dopo due MaxPool2d(2) su 28×28, H=W=?
- **Valutazione (primo tentativo — "voto esame"):** **3/10**
- **Punti di forza:** Sa che un pool 2×2 dimezza (28→14).
- **Errori / lacune:** La domanda chiede **due** pool: 28→14→**7**. Risposta data (14) = dopo un solo pool.
- **Correzione / suggerimento:** Contare i dimezzamenti in serie; in PiccolaCNN dopo 2 pool sei a 7×7 prima del Linear.
- **Lacune contesto:** soft shape tracking multi-layer — non 🔴 se fix immediato.

### 2026-08-26 — Quiz verifica V4 (post-feedback, lettura consegna)

- **Esercizio / blocco:** `08_cnn_computer_vision.py` ~776–779 — fix `14 → 7`
- **Valutazione (post-feedback — non ricalcola il voto esame):** corretto **7** (catena 28→14→7).
- **Nota:** voto esame resta **3/10** (primo shot solo 14); pattern #6 soft (lettura consegna “due”).

### 2026-08-26 — Quiz verifica V5 ordine loop (`08_cnn_computer_vision.py` ~780–783)

- **Esercizio / blocco:** Ordine (a) step (b) zero_grad (c) backward (d) loss
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `b, d, c, a` = zero_grad → loss → backward → step.
- **Errori / lacune:** Nessuno.

### 2026-08-26 — Quiz verifica V6 map_location (`08_cnn_computer_vision.py` ~784–787)

- **Esercizio / blocco:** map_location serve quando… (1 frase operativa)
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** Caso tipico corretto: load `state_dict` addestrato su CUDA (es. Colab) → esecuzione su CPU locale; rimappa i tensori sul device giusto.
- **Errori / lacune:** Soft: vale in generale per qualunque cambio device al load (non solo Colab→PC), ma l’esempio operativo è quello che serve.
- **Correzione / suggerimento:** Forma tipica: `torch.load(..., map_location="cpu")` (o `device`).
- **Allineamento:** coerente con #46 🟢.

### 2026-08-26 — Quiz verifica V7 Feynman CNN vs FC (`08_cnn_computer_vision.py` ~788–796)

- **Esercizio / blocco:** Perché CNN vs fully-connected su flatten (5–8 frasi)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Quattro pilastri chiari: parametri; geometria/correlazione locale; traslazione + parameter sharing; Conv trova / Pool sintetizza + Linear solo in coda sui logits. Migliore della 📚 precedente (8.5).
- **Errori / lacune:** Soft: analogia web/Photoshop non usata (opzionale in consegna); “prima di softmax” — in PyTorch spesso esci in **logits** e CE fa softmax dentro (hai già detto logits: ok). Typo “a poca” → “ha poca”.
- **Correzione / suggerimento:** Nessuna obbligatoria. Quiz V1–V7 chiuso.

### 2026-08-26 — TODO 1 colloquio Conv/Pool/FM vs MLP (`08_cnn_computer_vision.py` ~804–808)

- **Esercizio / blocco:** Spiega a collega web: convoluzione, pooling, feature map, perché non flatten+MLP
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Conv (filtri, punteggio locale, riuso pesi); Pool come sintesi dei punteggi alti; critiche a flatten+MLP (pesi, geometria, traslazione) chiare e senza formule.
- **Errori / lacune:** **Feature map** non nominata esplicitamente (è nella consegna): andrebbe detto che l’insieme dei punteggi di un filtro = una mappa/evidenziatore. Pool un po’ generico (manca “finestra locale → griglia più piccola”).
- **Correzione / suggerimento:** 1 frase: “feature map = immagine dei punteggi di un filtro”; Pool = max (o media) in zone, riduce H×W.

### 2026-08-26 — TODO 1 (post-feedback) Conv/Pool/FM vs MLP

- **Esercizio / blocco:** `08_cnn_computer_vision.py` ~804–808
- **Valutazione (post-feedback — non ricalcola il voto esame):** **9.5/10**
- **Punti di forza:** Aggiunti **feature map** esplicita e pooling a **finestre** sulla mappa; resta solido Conv + critiche MLP/traslazione.
- **Errori / lacune:** Soft: pooling riduce anche la griglia (H×W ↓) — implicito ma non detto; typo “Inolte”.
- **Nota:** voto esame resta **8/10**.

### 2026-08-26 — TODO 2 refactoring CnnBella (`08_cnn_computer_vision.py` ~832–847)

- **Esercizio / blocco:** Rifattorizzare CnnBrutta (Sequential / metodi chiari, stessa shape PiccolaCNN)
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `features` in `Sequential` (Conv/ReLU/Pool ×2); `forward` pulito flatten `start_dim=1` + Linear; architettura allineata a PiccolaCNN; `32*7*7` leggibile (meglio del magico `1568` della brutta).
- **Errori / lacune:** Nessuno rispetto alla consegna. Soft/extra non richiesto: `img_size` + `.numel()` per Linear adattivo (ne avete parlato in chat).
- **Correzione / suggerimento:** Nessuna obbligatoria.

### 2026-08-26 — TODO 3 DEBUG matmul 64×3200 vs 1568×10 (`08_cnn_computer_vision.py` ~853–862)

- **Esercizio / blocco:** Diagnosi RuntimeError Linear + 3 bullet + fix
- **Valutazione (primo tentativo — "voto esame"):** **6/10**
- **Punti di forza:** Zona giusta: disallineamento flatten vs `in_features` del Linear / MaxPool.
- **Errori / lacune:** Manca diagnosi numerica a 3 bullet. `3200 = 32×10×10`, `1568 = 32×7×7`: le mappe sono 10×10 ma il Linear aspetta 7×7 (PiccolaCNN dopo 2 pool su 28). Consegna chiedeva 3 bullet + fix esplicito; risposta troppo generica. Fix solo “cambio Linear” può mascherare un MaxPool mancante: meglio ripristinare i 2 pool (28→14→7) *oppure* riallineare Linear solo se la geometria voluta è davvero 10×10.
- **Correzione / suggerimento:** Bullet: (1) leggi mat1/mat2 (2) 3200 vs 1568 (3) causa pool/shape (4) fix preferito = 2× MaxPool2d(2).

### 2026-08-27 — TODO 4 retrieval training epoch (`08_cnn_computer_vision.py` ~863–889)

- **Esercizio / blocco:** Un epoch: zero_grad → … → step + loss media con `.item()`
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Ordine corretto; **`loss.item()` dopo `backward`** (allineato a #47); media pesata `* xb.size(0)` / `n_seen` corretta.
- **Errori / lacune:** `loss_for_epoch = list(tuple[int, float])` non crea una lista — andrebbe `loss_for_epoch: list[tuple[int, float]] = []` (o `= []`). Soft: `model.train()` opzionale; codice tutto in commento `#` (ok se solo bozza nel file capitolo).
- **Correzione / suggerimento:** Fix init lista; resto del loop è retrieval riuscito.
- **Lacune:** #47 🟡 → soft miglioramento (uso corretto `.item()` qui).

---

## Lacune e dubbi ancora aperti

- Ereditati da cap.07: #27 🟡, #45 🟢, #46 🟢 (Micro 46.B); **#47** 🟡 `.item()` vs backward; progetto 🏗️ ⚠️

---

## Note per il capitolo successivo (mentor)

- Dopo cap.08 → bridge R08 + `09_transfer_learning.py` (qui inizia il path buste paga anonimizzate)
