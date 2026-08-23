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
- **2026-08-23** — Kernel su patch ≈ dot product (poi + bias); ripetuto su tutte le posizioni.

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

---

## Lacune e dubbi ancora aperti

- Ereditati da cap.07: #27 🟡, #45 🟢, #46 🟢 (Micro 46.B); **#47** 🟡 `.item()` vs backward; progetto 🏗️ ⚠️

---

## Note per il capitolo successivo (mentor)

- Dopo cap.08 → bridge R08 + `09_transfer_learning.py` (qui inizia il path buste paga anonimizzate)
