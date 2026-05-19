# Diario sessione — Capitolo 02 — Reti neurali da zero

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `02_reti_neurali.py` |
| **File diario** | `M03_C02_reti_neurali_sessione.md` |
| **Stato** | in corso |
| **Voto difficoltà** | — / X/10 (atteso 7/10) |

---

## Obiettivi del capitolo (per il mentor)

- Generalizzare il neurone (cap.01 M3) a un **layer Dense con h neuroni** (`X @ W + b` con `W (d, h)`).
- Costruire e fare il **forward** di una **rete 2-layer** (input -> hidden ReLU -> output sigmoid) in **NumPy puro**, senza framework.
- Far vivere allo studente la differenza fra **rete random** (accuracy ~ 0.5) e **rete addestrata** (anticipato — il training arriva nel cap.03 M3).
- Far emergere intuitivamente l'**Universal Approximation Theorem** senza formule (frasi semplici + grafico delle attivazioni ReLU).
- Fissare 3 tranelli chiave: **R2 collasso lineare** senza attivazione, **R5 init zero** che rompe la simmetria, **R7 shape dei pesi** sempre verificate.

---

## Domande durante lo studio

- _(da popolare durante il capitolo)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `02_reti_neurali.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [2026-05-11] — `02_reti_neurali.py` — TODO 1.1 (Dense + ReLU, conteggio zeri)

- **Esercizio / blocco:** Sezione 1, TODO 1.1 (~righe 334–348 dopo traccia commentata).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Pipeline corretta: `X (5,3)`, `init_pesi_he` con `d` coerente alle colonne di `X`, `W (3,4)`, `b (4,)`, `layer_dense(..., relu)` valido (4° argomento = `att`). Conteggio `(H == 0).sum()` corretto. Commento finale: concetto giusto — ReLU annulla i **logit** negativi (`z = X@W+b`), non “i valori di X” in generale.
- **Errori / lacune:** Traccia richiedeva `default_rng(1)` — usato `42` (ok per seed ma non allineato al testo). `X` uniforme in `[0,10]` rende l’esperimento meno “transparente” sul motivo dei negativi rispetto a input anche negativi (es. gaussiani): non è sbagliato, ma indebolisce un po’ l’intuizione richiesta. `len(X[1])` per `d`: funziona qui; più idiomatico `X.shape[1]`.
- **Correzione / suggerimento:** Opzionale: `layer_dense(X, W, b, att=relu)` per leggibilità; stampare solo una riga di `H` se serve debug compatto.
- **Pattern errore / ID contesto** (se applicabile): monitoraggio **Pattern #6** (lettura consegna dettagli tipo seed rng) — singolo caso, non ancora ricorrente.

### [2026-05-11] — POST-FEEDBACK — stesso TODO 1.1 (`02_reti_neurali.py`)

- **Fix applicato:** `default_rng(1)` come da traccia; `X` uniforme su intervallo bilanciato (`[-5, 5]`) così i logit negativi sono più facili da “vedere”; `X.shape[1]` per `d`; `att=relu` esplicito.
- **Nota:** il voto **primo tentativo** della entry precedente resta **8/10** (regola diario). La versione corrente è **allineata al 100% alla consegna** e mostra cura su seed + API leggibile.

### [2026-05-19] — `02_reti_neurali.py` — TODO 1.2 (lineare vs sigmoid, scala output)

- **Esercizio / blocco:** Sezione 1, TODO 1.2 (~righe 349–420: setup `X,W,b`, doppio forward, print matrici + min/max, commento).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** Stesso triplo `(X, W, b)` per entrambi i passaggi; `H_lineare` senza attivazione vs `H_sigmoid` con `att=sigmoid`; shape coerenti `(10,2)×(2,3)→(10,3)`; `min`/`max` stampati su entrambe le uscite; `default_rng(1)` allineato allo stile delle tracce; uso He su `W` coerente col capitolo (anche se la traccia diceva solo “random”).
- **Errori / lacune:** Ridefinizioni di `layer_dense` / `relu` / `sigmoid` **dentro il blocco TODO**: rischio **shadowing** delle funzioni già definite sopra nel file e confusione all’`import`/run dell’intero modulo — meglio usare le definizioni globali del capitolo e tenere nel TODO solo dati + forward + print. Commento: il **clip** in sigmoid serve alla **stabilità numerica** dell’`exp`, non è ciò che “mette i valori tra 0 e 1” (quello è la formula sigmoid); formulazione da affinare. `layer_dense(X,W,b)` è ok (`att=None` default); esplicitare `att=None` aiuta la lettura vs R6.
- **Correzione / suggerimento:** Spostare/eliminare le `def` duplicate; nel commento finale contrastare **uscita lineare non limitata** vs **uscita sigmoid in (0,1)** e **saturazione** per \(|z|\) grande (R6).
- **Pattern errore / ID contesto** (se applicabile): nessun pattern ricorrente nuovo; solo attenzione struttura file (manutenibilità).

### [2026-05-19] — `02_reti_neurali.py` — TODO 1.3 (He init: media e std di W)

- **Esercizio / blocco:** Sezione 1, TODO 1.3 (~righe 423–445: `init_pesi_he`, assert shape, `mean`/`std` su `W.ravel()`, commento righe 433–434).
- **Valutazione (primo tentativo — "voto esame"):** **codice 9/10**, **commento / domanda 4 ~6.5–7/10** → **complessivo ~8/10**.
- **Punti di forza:** `init_pesi_he(10, 20, seed=42)` coerente con traccia; **assert** su `W.shape` e `b.shape`; uso di **`W.ravel()`** per statistiche globali; **`np.mean` / `np.std`** su tutti i pesi (std con default `ddof=0` confrontabile con σ teorica **√(2/d)**). Spiegazione nel commento: collegamento **standard_normal × √(2/d)** → σ finale **≈ 0.447** è nel segno giusto.
- **Errori / lacune:** `print("\nTODO 1.2\n")` è **etichetta sbagliata** (dovrebbe essere TODO **1.3**). Nel commento mescoli bene il **pipeline** N(0,1)×scala, ma la **domanda 4** chiedeva perché la **media campionaria non è esattamente 0**: va detto esplicitamente che su un **numero finito** di campioni la media è una **variabile casuale** che **fluttua** intorno a 0 (solo con infiniti campioni andrebbe a 0); non basta ripetere “circa 0”. Precisione: i pesi **finali** non sono “N(0,1)”, sono **N(0, σ²)** dopo la moltiplicazione — la frase va leggibile come “prima gaussiana standard, poi scala”.
- **Correzione / suggerimento:** Una riga tipo: *con N pesi finiti, la media dei campioni non coincide quasi mai esattamente con la media teorica (0)*; opzionale `float(...)` sulle stampe come da traccia.
- **Pattern errore / ID contesto** (se applicabile): —

### [2026-05-19] — `02_reti_neurali.py` — TODO 2.1 (rete 2-layer random: shape + statistiche P + commento)

- **Esercizio / blocco:** Sezione 2, TODO 2.1 (~righe 588–613).
- **Valutazione (primo tentativo — "voto esame"):** **codice ~8/10**, **commento domanda finale ~4/10** → **complessivo ~7/10**.
- **Punti di forza:** `N, d, h` corretti; `default_rng(7)` per `X`; `init_pesi_he(..., seed=10)` e `(..., seed=11)` per i due layer; `rete_2_layer` usata correttamente → `(H, P)` con stampa di shape di `H`, statistiche su `P`. Idea che **ReLU** taglia i **logit** negativi del primo layer e che questo cambia cosa arriva al secondo layer è nella direzione giusta.
- **Errori / lacune:** Nel commento: **`X` è uniforme su [-5, 5], non gaussiana** — errore concettuale grave su **Uniform vs Normal** (serve rinforzo per quiz/stat ML). Catena successiva (“campana gaussiana”, “metà campana”) non è più attendibile dopo quel punto. **Codice:** `my_esempio_rete_2_layer_random()` viene richiamata **più volte** invece di `H, P = ...` una volta sola (ridondante; anche se seed fissi ripetono gli stessi numeri). **`P.mean()` vicino a 0.5:** va legato a **rete non allenata**, **sigmoid** che mappa logit ~0 verso ~0.5, e al bilanciamento grossolano dei **logit** secondo layer più che a “uniforme = gaussiana”.
- **Correzione / suggerimento:** Un solo forward; stampare esplicitamente `H.shape` e `P.shape`; riscrivere il commento dopo aver corretto **Uniform**; collegare **0.5** a **sigmoid(0)** e ordine di grandezza dei **logit** casuali.
- **Pattern errore / ID contesto** (se applicabile): monitoraggio confusione **distribuzioni** (Uniform vs Gaussian) — registrare se ricorre.

### [2026-05-19] — POST-FEEDBACK — TODO 2.1 (`02_reti_neurali.py`)

- **Fix applicato:** una sola assegnazione `H, P = ...` richiesta nel senso giusto (ma vedi nota); commento riscritto: **rete non allenata**, **logit** vicini a **0** → **sigmoid ~ 0.5** — linea corretta rispetto alla versione precedente (niente più Uniform=Gaussiana).
- **Nota tecnica:** ancora **`my_esempio_rete_2_layer_random()` chiamata due volte** (`[0]` e `[1]` su due invocazioni): meglio **`H, P = my_esempio_rete_2_layer_random()`** (una forward). La traccia chiedeva **`P.shape`**: ora stampi tutto **`P`** invece della sola shape — ok per debug, ma non è la consegna letterale.
- **Valutazione post-feedback (solo qualità attuale):** **codice ~8.5/10**, **commento ~8/10** → **~8–8.5/10**. Il voto **primo tentativo** della entry TODO 2.1 precedente resta **~7/10** (regola diario).

### [2026-05-19] — POST-FEEDBACK 2 — TODO 2.1 (`02_reti_neurali.py`)

- **Fix applicato:** `H, P = my_esempio_rete_2_layer_random()` (una sola forward); stampa **`P.shape`** come da traccia; commento riga ~614 confermato (logit ~0 → sigmoid ~0.5, rete non allenata).
- **Valutazione qualità attuale:** **~9.5/10** (implementazione + consegna + commento). Micro-miglioramento opzionale: etichette nelle `print` tipo `print("P.mean()", ...)`.

### [2026-05-19] — `02_reti_neurali.py` — TODO 2.2 (crollo lineare 3 layer vs layer equivalente)

- **Esercizio / blocco:** Sezione 2, TODO 2.2 (~righe 615–648).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**.
- **Punti di forza:** Shape coerenti `(30,4)×(4,8)×(8,6)×(6,1)`; tre `layer_dense` con **`att=None`** (solo lineare); **`W_eq = W1 @ W2 @ W3`**; **`b_eq = (b1 @ W2 + b2) @ W3 + b3`** con **`b`** tutti zero ma formula generale corretta; confronto **`K`** vs **`K_eq`**; **`np.allclose(..., atol=1e-10)`** come richiesto; stampa differenza massima.
- **Errori / lacune:** **`diff_max = np.max(K - K_eq)`** senza **valore assoluto**: se ci fossero errori numerici misti segno, **`max`** può essere fuorviante — meglio **`np.max(np.abs(K - K_eq))`** (anche se con **`b=0`** e stesso calcolo spesso è ok). Opzionale: He solo su **`W1`** mentre **`W2,W3`** sono `standard_normal` puro — non rompe l’esercizio, solo incoerenza estetica di init.
- **Correzione / suggerimento:** Usare **`np.abs`** sul residuo; opzionale **`float(diff_max)`** in print.
- **Pattern errore / ID contesto** (se applicabile): —

### [2026-05-19] — POST-FEEDBACK — TODO 2.2 (`02_reti_neurali.py`)

- **Fix applicato:** **`diff_max = np.max(np.abs(K - K_eq))`**; init **He coerente** su **`W1`/`W2`/`W3`** (`sqrt(2/d)`, `sqrt(2/h)`, `sqrt(2/k)` con fan-in corretto per layer).
- **Valutazione qualità attuale:** **~10/10** (consegna + correttezza + robustezza stampa residuo). Il voto **primo tentativo** storico resta **9/10** (regola diario).

### [2026-05-19] — `02_reti_neurali.py` — TODO 2.3 (`my_demo_init_zero` vs init He)

- **Esercizio / blocco:** Sezione 2, TODO 2.3 (~righe 650–668).
- **Valutazione (primo tentativo — "voto esame"):** **~7.5/10**.
- **Punti di forza:** Stesso schema della **`_demo_init_zero`** ( **`rete_2_layer`**, **`X`** `(20,4)`**, **`h=8`** ); **`init_pesi_he`** per **`W1,b1`** e **`W2,b2`** → bias ancora zero, pesi diversi tra loro → **`z`** dell’output non è più ovunque zero → **`P`** non è più **costante 0.5**; stampa **`mean`/`min`/`max`** con formato leggibile.
- **Errori / lacune:** La consegna chiedeva cosa **cambia** rispetto alla demo: manca un confronto esplicito (es. una **`print`** della **`_demo_init_zero`** o una riga “prima tutti 0.5, ora …”). **`rng` seed 42** vs demo **`0`**: ok per ripetibilità, ma va nominato se vuoi confronto fedele. Commento sopra il codice: italiano poco chiaro (“dot product = 0”); l’idea “neuroni diversi → **`H`** diversa → **`P`** varia tra righe” c’è ma va sintetizzata come **`symmetry breaking` rotto / neuroni non identici** (hint nel docstring della demo).
- **Correzione / suggerimento:** Aggiungere **due righe** di stampa: output demo init-zero vs output He; commento **una riga** tipo *«non più tutti 0.5 perché `z` dipende da `X` e da pesi distinti per neurone»*. Opzionale: rimuovere la virgola finale dopo **`8`** in **`N, d, h = 20, 4, 8,`** (solo stile).
- **Pattern errore / ID contesto** (se applicabile): monitoraggio **consegna “cosa cambia”** (prima/dopo) — Pattern lettura traccia legato a #6 se ricorrente.

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se il TODO 1.1 evidenzia ancora confusione sulle shape `(N, d) @ (d, h) -> (N, h)`, **bloccare** prima di passare alla Sez. 2.
- Se l'`init_pesi_he` non viene compreso (perche' `sqrt(2/d)` e non `0.01`?), recuperare prima del cap.03 M3 (li' si parla di vanishing/exploding gradient).
- Verificare che TODO 2.2 (collasso lineare a 3 layer) sia eseguito DA SOLO: e' il check che la regola R2 e' stata davvero capita.
- Per il cap.03 M3 (backpropagation): partire dalla rete 2-layer di questo capitolo e introdurre il **training** (loss + gradient descent + backward). NON saltare il capitolo se questo non e' chiuso 8+/10.

---

## Note tecniche di stesura (mentor)

- _(da popolare quando il capitolo verra' aperto e lavorato)_
