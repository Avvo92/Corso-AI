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

- _(vuoto — in attesa prima sessione di studio)_

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

---

## Lacune e dubbi ancora aperti

- Ereditati da cap.07: #27 🟡, #45 🟢, #46 🟡; **#47** 🟡 `.item()` vs backward (Q7); progetto 🏗️ ⚠️

---

## Note per il capitolo successivo (mentor)

- Dopo cap.08 → bridge R08 + `09_transfer_learning.py` (qui inizia il path buste paga anonimizzate)
