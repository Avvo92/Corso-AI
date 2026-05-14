# Diario sessione — Capitolo 01 — Neurone artificiale da zero

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `01_neurone_artificiale.py` |
| **File diario** | `M03_C01_neurone_artificiale_sessione.md` |
| **Stato** | in corso (avvio: 07/05/2026) |
| **Voto difficoltà** | — (assegnato in chiusura) |

---

## Obiettivi del capitolo (per il mentor)

- Costruire il ponte concettuale **layer Dense (Ponte cap.02) → neurone (M3 cap.01)**: un neurone è un layer Dense con `h = 1` + attivazione.
- Far interiorizzare la sequenza **forward = `X @ w + b` → attivazione (sigmoid/ReLU)** come "due passi separati": prima i punteggi (logits), poi la decisione/probabilità.
- Chiudere definitivamente la **Lacuna #28** (logits vs probabilità): il neurone produce un punteggio, è la **sigmoid** che lo trasforma in probabilità tra 0 e 1.
- **Re-check delle lacune quiz aperte** dal cap.02 Ponte:
  - **#23** shape `(N,)` vs `(N, 1)` → quiz d'ingresso Q1 + esercizio E5.
  - **#24** tupla accidentale `(0.1,)` vs `0.1` → quiz d'ingresso Q3 (trova l'errore).
  - **#26** 2 motivi performance BLAS vs loop → quiz d'ingresso Q4.
  - **#27** Feynman "niente termini tecnici" → quiz d'ingresso Q6 + V8.
  - **#29** slicing `X[i]` vs `X[i:i+1]` → quiz d'ingresso Q5.
- Verificare il **recall cross-modulo** (Regola 26): il neurone ricostruisce `X @ W + b` di Ponte cap.02 con `W` collassato a un vettore.
- Preparare il terreno per il cap.02 M3 (rete neurale = neuroni in parallelo + attivazioni concatenate).

---

## Domande durante lo studio

- _(template — il mentor le aggiungerà man mano)_
- **Q:** …
  **Nota / risposta sintetica:** …

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `01_neurone_artificiale.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [YYYY-MM-DD] — Quiz d'ingresso Q1-Q6 (cerniera cap.02 Ponte)

- **Blocco:** `01_neurone_artificiale.py` — Quiz d'ingresso (Q1: shape `X @ w` lacuna #23; Q2: layer Dense = h regressioni in parallelo, output = punteggi non probabilità lacuna #28; Q3: trova l'errore tupla `(0.1,)` lacuna #24; Q4: 2 motivi BLAS vs loop lacuna #26; Q5: `X[5]` vs `X[5:6]` lacuna #29 re-check; Q6: Feynman senza termini tecnici lacuna #27).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** verifica chiusura lacune #23/#24/#26/#27/#28 e re-check #29.

### [2026-05-07] — Quiz d'ingresso Q1 (lacuna #23 re-check)

- **Blocco:** `01_neurone_artificiale.py` righe ~150–154 (`X @ w` vs `X @ w.reshape(-1, 1)`).
- **Voto (primo tentativo):** **7/10** (solo parte numerica delle shape).
- **Corretto:** `(200,)` per `X @ w`; `(200, 1)` per `X @ w.reshape(-1, 1)` — allineato a `numpy.matmul` / `@`.
- **Manca (consegna esplicita):** una frase che dica **quale risultato è 1D vs 2D** e **perché** (regola NumPy: secondo operando 1D `(7,)` → output 1D `(200,)`; secondo operando 2D `(7,1)` → output 2D `(200,1)`).
- **Next step:** completare la spiegazione nel commento sotto Q1; poi rivalutare solo quel punto se vuoi un secondo tentativo formale.
- **Lacuna #23:** shape giuste → ok; **spiegazione “perché”** ancora da chiudere per considerare Q1 al 100%.

### [2026-05-07] — Quiz d'ingresso Q1 — rivalutazione (post-completamento spiegazione)

- **Blocco:** `01_neurone_artificiale.py` righe ~150–156.
- **Voto:** **10/10** (tentativo dopo integrazione spiegazione — registrato come completamento Q1, non nuovo “esame” separato se si vuole rigore solo sul primo tentativo).
- **Corretto:** shape `(200,)` vs `(200, 1)` + motivazione coerente: `(N,d) @ (d,)` → `(N,)`; `(N,d) @ (d,1)` → `(N,1)` dopo `reshape(-1, 1)`.
- **Micro-nota didattica:** in NumPy si dice anche **`matmul`** (`@`); “dot product” per riga×colonna va bene come intuizione. Ortografia: “perché”, “a quel punto”.
### [2026-05-07] — Quiz d'ingresso Q2 (lacuna #28 re-check)

- **Blocco:** `01_neurone_artificiale.py` righe ~157–165 (`z` vs `a = sigmoid(z)`).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** **`a`** è la **probabilità stimata** (valore tra 0 e 1 dopo **sigmoid**); **`z`** è il **logit** / punteggio grezzo prima dell’attivazione — ripristina il discrimine della lacuna #28.
- **Ambiguità:** la frase «**il secondo** è un logit grezzo» è fuorviante: nell’ordine del codice **`z` viene prima**, **`a` dopo** — “secondo” sembrerebbe **`a`**. Meglio scrivere esplicitamente: «**`z`** è il logit».
- **Nota terminologica:** «logit grezzo» è ridondante; va bene **logit** (o “punteggio lineare”).
- **Next step:** ripulire il commento nel file con `z` / `a` nominati; lacuna #28 considerabile **superata** su questo checkpoint.

### [2026-05-07] — Quiz d'ingresso Q3 (lacuna #24 re-check — tupla `(0.1,)`)

- **Blocco:** `01_neurone_artificiale.py` righe ~166–173.
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** versione `z = X @ w + 0.1`; distingue **anti-pattern di stile** (bias espresso come **tupla monoelemento** `(0.1,)` per virgola/ambiguità) dal caso corretto **scalare**; `type((0.1,))` → **`tuple`** (in runtime: `<class 'tuple'>`).
- **Nota:** osservazione sul **broadcasting** NumPy coerente col Ponte: spesso “gira” comunque, ma si perdono chiarezza e intento (**bias** deve essere numero/array esplicito).
- **Lacuna #24 (tupla bias):** **superata** su questo checkpoint.

### [2026-05-07] — Quiz d'ingresso Q4 (lacuna #26 re-check — velocità `X @ w` vs loop)

- **Blocco:** `01_neurone_artificiale.py` righe ~174–181.
- **Voto (primo tentativo):** **8/10**.
- **Corretto (motivo 1):** confronto **una chiamata vettorizzata** (codice **C/Fortran** dietro NumPy, **BLAS** / `matmul`) vs **molte iterazioni** Python — è il motivo “tecnico-NumPy” richiesto.
- **Debole (motivo 2):** «linguaggio interpretato / preprocessato» è **vago** e **non ben separato** dal primo (anche il loop è lento perché resta in Python). Meglio uno tra: **overhead per iterazione** (bytecode, `range`, indexing `X[i]` ripetuto); **tante piccole chiamate** (`np.dot` × N); **memoria contigua / cache** (un solo passaggio ottimizzato vs saltare riga per riga); dove applicabile **SIMD** nel kernel BLAS.
- **Nota:** il fattore **50–1000×** è **ordine di grandezza possibile**, dipende da N,d e macchina — ok come intuizione, non come legge fissa.
- **Lacuna #26:** da **🔴** a **🟡** — migliorata ma **non chiusa** al 100% finché il **secondo motivo** non è **distinto** e **operativo** (integrare nel commento Q4 una frase sul ciclo/indexing o sulla cache).

### [2026-05-07] — Quiz d'ingresso Q5 (lacuna #29 re-check — slicing righe)

- **Blocco:** `01_neurone_artificiale.py` righe ~183–188 (`X[5]` vs `X[5:6]`, `predict_proba`).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** `X[5]` → **`(7,)`** (1D); `X[5:6]` → **`(1, 7)`** (2D — una riga, tutte le feature); **`predict_proba`** vuole forma **`(n_campioni, n_feature)`** → **`X[5:6]`** è la forma giusta per **un** campione.
- **Micro-nota:** alcune versioni sklearn **accettano** anche `(n_features,)` per **un** solo vettore, ma è **fragile** e fuori convenzione; la risposta **corretta didattica** è **`(1, 7)`**.
- **Lacuna #29:** **🟢 Superato** su questo checkpoint.

### [2026-05-07] — Quiz d'ingresso Q6 (lacuna #27 re-check — Feynman senza jargon)

- **Blocco:** `01_neurone_artificiale.py` righe ~193–201.
- **Voto (primo tentativo):** **10/10**.
- **Vincoli:** nessuno tra feature / logit / regressione / matrice / sigmoid / vettore; analogia **cuoco / ingredienti → punteggio “primo piatto”** chiara e nel limite **≤ 5 righe**.
- **Micro-nota:** «un neurone **è** un cuoco» (accento), non «**e**».
- **Lacuna #27:** **🟢 Superato** su questo checkpoint.

### [2026-05-08] — Mini-esercizio RINFORZO #24 (lacuna #24 — tuple bias)

- **Blocco:** `01_neurone_artificiale.py` righe ~272–282 (`type((0.05,))`, `z_ok` senza tuple bias).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** (a) `tuple` / `<class 'tuple'>` — ok; (b) **`z_ok = X @ w + b`** con **`b` scalare** — niente `(0.1,)`, intento della lacuna rispettato.
- **Da migliorare sulla consegna:** il testo chiedeva esplicitamente **`+ 0.05`** (letterale); hai usato **`b = 0.5`** — va bene come stile **nome bias**, ma per “segui il foglio” conviene **`z_ok = X @ w + 0.05`** oppure **`b = 0.05`** se vuoi il nome.
- **Extra:** `print` decorativo ok; opzionale aggiungere **`print(type((0.05,)))`** per chiudere (a) nel runner.

### [2026-05-08] — Mini-esercizio RINFORZO #26 (lacuna #26 — BLAS vs loop)

- **Blocco:** `01_neurone_artificiale.py` righe ~305–310 (due bullet motivazioni).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** due motivi **non ridondanti**: (A) costo **interprete / ciclo** a ogni `i` vs un’unica chiamata ottimizzata; (B) **memoria contigua** / **località** vs oggetti **sparsi** nell’**heap** — coerente con la lacuna #26 (overhead Python + cache / memoria contigua).
- **Migliorabile:** etichetta «Motivo A … NumPy/C» — il testo parla soprattutto dell’**interprete**; aggiungere «**una sola** routine **BLAS** (GEMV/matmul) in C» renderebbe il bullet A completo. Ortografia: *chiamare*, *linguaggio*, *efficienza*, *effettuate*, *memoria*, *perché*.
- **Opzionale consegna:** annotare lo **speedup** stampato dopo `_benchmark_loop_vs_blas()` (una riga nel commento).
- **Lacuna #26:** da 🟡 a **🟢** in `CONTESTO_CORSO.md`.

### [2026-05-08] — Mini-esercizio RINFORZO #28 (lacuna #28 — logit vs probabilità)

- **Blocco:** `01_neurone_artificiale.py` righe ~374–384 (`z_test`, `clip`, `p_test`, commento).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** `np.clip` prima di `exp` → stabilità; `p_test = 1/(1+exp(-z_test))` **element-wise**; stampa arrotondata; commento **logit = z_test**, **probabilità = p_test** — coerente con lacuna #28.
- **Micro-nota:** per `-100/100` il clip non cambia i numeri (già dentro ±500); utile come **abitudine** quando gli \(z\) possono essere enormi.

### [2026-05-08] — Mini-esercizio RINFORZO #29 (lacuna #29 — slicing 1D vs 2D)

- **Blocco:** `01_neurone_artificiale.py` righe ~410–420 (`X[3]`, `X[3:4]`, `X[[3]]`, `riga_2d`).
- **Voto (primo tentativo):** **10/10** (post-correzione `X[3:4].shape` e rimozione `X.shape[3]`).
- **Corretto:** `X[3].shape` → **(5,)**; `X[3:4].shape` e `X[[3]].shape` → **(1, 5)**; **`riga_2d = X[[3]]`** (equivale anche **`X[3:4]`**) → forma richiesta per **sklearn** / batch una riga.
- **Opzionale:** `print(riga_2d.shape)` per chiudere esplicitamente la DoD sul `(1, 5)`.

### [2026-05-08] — RIPASSO cap.02 Ponte — mini R1 (matrice = batch)

- **Blocco:** `01_neurone_artificiale.py` righe ~428–440.
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** `X` **(3, 4)** interi (`randint`); **`shape`**, **`dtype`**; **`X[0]`** = prima riga/pratica; **`X[:, 0]`** = prima colonna/feature su tutte le righe — allineato al Ponte “batch = matrice”.
- **Extra:** `print(X)` utile per controllo visivo; non richiesto dalla consegna.

### [2026-05-08] — RIPASSO cap.02 Ponte — mini R2 (X @ w vs dot per riga)

- **Blocco:** `01_neurone_artificiale.py` righe ~443–452.
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** `X (3,4)`, `w (4,)`, `z = X @ w`; **`np.dot(X, w)`** con queste shape è **il prodotto matrice–vettore** le cui componenti sono proprio **`np.dot(X[i], w)`** — quindi **`np.allclose(z, np.dot(X, w))`** verifica l’equivalenza richiesta **senza** ciclo di assert.
- **Nota:** equivalente alla lista comprehension sulle righe, ma tutto **vettorizzato** in una chiamata.

### [2026-05-08] — RIPASSO cap.02 Ponte — mini R3 (broadcasting bias)

- **Blocco:** `01_neurone_artificiale.py` righe ~455–467.
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** `z (3,)`, `b` scalare, `z_pre = z + b`; commento sul **broadcast** dello scalare su forma **`(3,)`** e somma **element-wise**; **`z2_pre`** con bias **vettoriale** `(3,)` coerente; **`print` delle shape** (`z_pre` e `z2_pre` → **(3,)**).
- **Micro-nota:** ortografia *ogni* (non “agni”); opzionale stampare **`z_pre`** / **`z2_pre`** per vedere dtype/promo dopo la somma.

### [2026-05-08] — RIPASSO cap.02 Ponte — mini R4 (Dense = h regressioni in parallelo, lacuna #28 ricontrollo)

- **Blocco:** `01_neurone_artificiale.py` righe ~470–482 (`X @ W`, shape `Z`, commento righe/colonne).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** **`rng = np.random.default_rng(42)`**; **`X (3, 4)`**, **`W (4, 2)`**, **`Z = X @ W`**; **`print(Z.shape)`** → **`(3, 2)`** coerente con **`(N, d) @ (d, h) → (N, h)`**; commento secondario sulla moltiplicazione matriciale allineato al Ponte.
- **Affinare terminologia:** la **riga** = **un campione / una pratica** (vettore di **due uscite lineari**) è giusta; la **colonna** è più precisamente l’**uscita della j-esima regressione (neurone) su tutti i campioni**, non una “feature” nel senso delle colonne di **`X`** (feature di input). In linguaggio corso: **due neuroni in parallelo → due colonne di logits/punteggi**.
- **Ortografia:** *si otterrà*, *risultati* (non «di otterrà» / «risultadi»).

### [2026-05-08] — RIPASSO cap.02 Ponte — mini R5 (shape 1D vs 2D, lacuna #29 ricontrollo)

- **Blocco:** `01_neurone_artificiale.py` righe ~483–496 (`X[2]`, `X[2:3]`, `X[2, :]`, `predict_proba`).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** **`X`** `(10, 3)`; **`X[2].shape` → `(3,)`**; **`X[2:3].shape` → `(1, 3)`**; **`X[2, :].shape` → `(3,)`** (equivalente a **`X[2]`** per i valori e la forma); commento sullo slicing **`X[r:r+1]`** per avere **batch 1×N** — allineato alla lacuna #29 / sklearn `(n_campioni, n_feature)`.
- **Chiudere la consegna in una frase:** esplicitare che **`predict_proba` al sicuro didattico** riceve **`X[2:3]`**; **`X[2]`** e **`X[2, :]`** sono **`(3,)`** — alcune versioni sklearn **possono** accettare il vettore 1D per **un** campione, ma è **fragile** e fuori convenzione rispetto a **`(1, n_feature)`**.
- **Stile:** *richiede* / *ha bisogno di* una matrice **`(1, N)`** (non «necessita in una matrice»).

### [2026-05-11] — TODO 1.1 Sez.1 — `top3_contributi(x, w, feature_names)`

- **Blocco:** `01_neurone_artificiale.py` righe ~677–698 (setup CSV + funzione + print).
- **Voto (iterazione dopo correzioni in chat):** **8/10** *(come “chiusura esercizio”: funzione ok; DoD/setup ancora da rifinire)*.
- **Corretto nella funzione:** controllo **`x.ndim != 1 or w.ndim != 1`**; **`x.shape == w.shape`** e **`len(feature_names)`** allineati; **`np.argsort(np.abs(x * w))[::-1][:3]`** = **top-3 per modulo**, ordine **decrescente** di **|**contributo**|**; output **`list[tuple[str, float]]`** con contributo **con segno** tramite **`(x * w)[i]`**.
- **Da sistemare (consegna / stile):** (1) **`X`** alla riga setup è in realtà **una sola pratica** `(7,)` → usa **`x`** (minuscolo) e **`X_full`** `(N, 7)` per le **prime 2 righe** richieste dal testo; (2) **`feature_names`**: evita secondo `.drop`, usa **una** variabile `df_feat` + **`list(df_feat.columns)`** per matchare il type hint; (3) micro-DRY: salva **`contrib_values = x * w`** una volta; (4) path: **`"modulo_02_ml"`** senza **`/`** finale in `join`.

### [2026-05-11] — TODO 1.1 Sez.1 — `top3_contributi` (rivaluazione dopo print su 2 pratiche)

- **Blocco:** `01_neurone_artificiale.py` righe ~677–698.
- **Voto (secondo tentativo / revisione DoD):** **9/10**.
- **Corretto:** **`X`** come mini-batch **`(2, 7)`** (`[:2]`); **`w = rng.standard_normal(X[0].size)`**; **`print`** separati per **`X[0]`** e **`X[1]`** → DoD «prime 2 pratiche» soddisfatto; **`top3_contributi`** invariata e corretta su **`np.abs` + ordine decrescente**.
- **Micro-affinamenti:** **`contrib_values = x * w`** una volta (DRY); **`feature_names = list(df_feat.columns)`** + un solo **`drop`**; path **`modulo_02_ml`** senza slash nel **`join`**.

### [2026-05-11] — TODO 1.2 Sez.1 — mini-batch logit + sigmoid + suggerimento #29

- **Blocco:** `01_neurone_artificiale.py` righe ~703–726 (`X (3,4)`, `w (4,)`, logit, sigmoid, `X[0]` vs `X[0:1]`).
- **Voto (primo tentativo):** **7/10**.
- **Corretto:** **`rng.default_rng(42)`**; **`X.shape == (3, 4)`**, **`w.shape == (4,)`** coerenti con **`X @ w`**; tre **logit** riga per riga; **sigmoid** coerente su ogni logit; stampa **`X[0].shape`** vs **`X[0:1].shape`** — lacuna **#29** consolidata.
- **Manca sulla consegna:** il testo chiede esplicitamente **`X @ w + b`**: manca un **`b`** scalare (es. **`b = 0.3`**) usato nei logit (**`X @ w + b`** vettoriale o **`float(X[i] @ w + b)`**).
- **Stile / robustezza:** usa **`sigmoid(...)`** già definita nel file (clip ±500, zero warning); evita **`for`** dove **`z = X @ w + b`** poi **`sigmoid(z)`** in una mossa (allineato al neurone batch); **`range(0, X[0, :].size - 1)`** è contorto → **`range(X.shape[0])`** o **`range(3)`**.

### [2026-05-11] — TODO 1.3 Sez.1 — if morbido vs rigido

- **Blocco:** `01_neurone_artificiale.py` righe ~730–765 (`y_morbido`, `y_rigido`, `zip`, commento).
- **Voto (primo tentativo):** **6/10** (logica principale ok; **return ValueError** è un bug serio di API).
- **Corretto:** flusso **(a)(b)**; **`X (10,3)`**, **`w (3,)`**; **`y_rigido = (y_morbido >= 0.5).astype(int)`**; stampa coppie con **`zip`**; intuizione sulle **probabilità vicine a 0.5** (incertezza) come perdita di dettaglio.
- **Bug bloccante (se i check falliscono):** in **`my_sigmoid`** / **`my_neurone_batch`**, **`return ValueError(...)`** restituisce un **oggetto** `ValueError` come se fosse l’output del neurone, **non** interrompe l’esecuzione → va **`raise ValueError(...)`**. Con codice che passa i check oggi “sembra” funzionare, ma l’API è **rotta**.
- **Consegna / riuso:** il testo chiede **`neurone_batch(X, w, 0.0)`** già nel file — riusala per non duplicare; **`my_sigmoid`**: anche batch produce **`(N,)`** → ok solo per questo uso; per robustezza usare **`sigmoid`** del capitolo (clip); **`w`**: preferire **`dtype=float`** esplicito.
- **Commento:** chiudere la riflessione (oltre la soglia 0.5): **due `y_morbido` diversi** possono collassare nello **stesso** **`y_rigido`** → si perde il **grado di confidenza**.

### [2026-05-11] — TODO 1.3 Sez.1 — rivalutazione post-fix

- **Blocco:** `01_neurone_artificiale.py` righe ~729–765.
- **Voto (secondo tentativo):** **9/10**.
- **Corretto:** **`raise ValueError`** (non più **`return ValueError`**); **`w`** con **`dtype=float`**; pipeline **`X @ w + b`** → sigmoid; **`y_rigido`** con soglia **0.5**; **`zip`** per le coppie; commento che generalizza la perdita di informazione (**confidenza** collassata nel binario).
- **Micro-nota consegna:** il testo chiede esplicitamente **`neurone_batch(...)`** del file — va bene **`my_neurone_batch`** come esercizio mentale, ma per chiudere al **100%** usa la funzione già fornita (meno duplicazione); **`sigmoid`** del capitolo resta preferibile (**clip** anti-warning).

### [2026-05-11] — TODO 1.3 Sez.1 — rivalutazione (clip su sigmoid + print)

- **Blocco:** `01_neurone_artificiale.py` righe ~730–766.
- **Voto (terzo tentativo / stato attuale):** **9.5/10**.
- **Corretto:** **`np.clip(v, -500, +500)`** prima di **`exp`** → stesso spirito della **`sigmoid`** del capitolo; **`raise ValueError`**; **`dtype=float`** su **`w`**; pipeline morbido/rigido e **`zip`**; commento sulla **confidenza** / collasso binario.
- **Micro-stile print:** **`soft.astype(str)`** con **`:20s`** funziona ma è poco idiomatico per float — preferibile **`f"{float(soft):.4f}"`** o **`round(float(soft), 4)`**; così eviti conversioni strane su **`numpy.float64`**.
- **DoD letterale:** sostituisci **`my_neurone_batch`** con **`neurone_batch(X, w, 0.0)`** e **`sigmoid`** globale → **10/10** “da foglio”.

### [2026-05-11] — TODO 2.1 Sez.2 — attivazioni su `z` vettore + domande (a)(b)

- **Blocco:** `01_neurone_artificiale.py` righe ~922–940 (`sigmoid`/`relu`/`tanh`, commenti).
- **Voto (primo tentativo):** **6/10**.
- **Corretto:** **`z`** come **`np.array([-3, -1, 0, 1, 3])`**; stampa delle tre attivazioni su tutto il vettore con **`sigmoid`/`relu`/`tanh`** già nel file; **(b)** in commento: **ReLU** è l’unica che per **`z < 0`** dà **0 esatto** — OK.
- **Debole — (a):** la consegna chiede quale attivazione è **«MENO interessante»** proprio in **`z = -1`** (punto didattico: in quel punto **ReLU** ha già **«spento tutto il ramo negativo»** → valore **0** come per **qualsiasi** **`z < 0`**, derivata **0** → localmente **piatta / non discrime** tra negativi; **tanh** e **sigmoid** restano **non costanti** sui negativi). La risposta *«dipende dal contesto»* **elude** il confronto richiesto.
- **Stile codice:** **`z = -1`** **sovrascrive** l’array **`z`** → nome riutilizzato per tipo diverso (**scalare**); stampa ridondante (il **`-1`** era già nel vettore). Meglio **`z_scalar = -1.0`** o iterare **`for zi in z:`** / indicizzare **`z[z == -1]`** senza shadowing.

### [2026-05-11] — TODO 3.1 Mini-esercizio — Pipeline + forward manuale vs `predict_proba`

- **Blocco:** `01_neurone_artificiale.py` righe ~1033–1075 (`my_esempio_neurone_csv`).
- **Voto (primo tentativo):** **6/10**.
- **Corretto:** **`Pipeline`**, **`named_steps["model"]`**, **`coef_`/`intercept_`**, **`scaler.transform(X)`** → **`X_scaled`** coerente col forward manuale; **`sigmoid(X_scaled @ w + b)`**; **`predict_proba(X)[:, 1]`**; **(b)** conteggio **`prob >= 0.5`** sul vettore probabilità (anche su ordinato il conteggio coincide); stampa **top 5** arrotondate e **`to_string`** leggibile.
- **Errore concettuale su (c):** il testo chiede media delle probabilità dove **`y == 1`** e dove **`y == 0`** (etichette vere). Nel codice risultano **`manuale_sorted[manuale_sorted >= 0.6]`** e **`< 0.4`** → maschere sulla **probabilità**, non su **`y`** → si risponde a un’altra domanda (sottoinsiemi “molto sicuri”), non al sanity check richiesto (`p[y == 1].mean()` alta, `p[y == 0].mean()` bassa).
- **Micro:** **`print(my_esempio_neurone_csv())`** stampa **`None`** in fondo (meglio chiamare senza **`print`** se la funzione stampa già tutto); **`(a)`** — se il capitolato intendeva le prime pratiche **in ordine CSV**, servirebbe **`p[:5]`** non ordinato.
### [2026-05-11] — TODO 3.1 Mini-esercizio — rivalutazione post-fix (maschera su `y`)

- **Blocco:** `01_neurone_artificiale.py` righe ~1033–1077 (`my_esempio_neurone_csv`).
- **Voto (post-feedback / secondo stato):** **9/10**.
- **Corretto:** **`p_man = sigmoid(...)`**; **(c)** con **`np.mean(p_man[y == 1])`** e **`p_man[y == 0]`** — allineato al testo dell’esercizio e alla lacuna #30; **`raise ValueError`** se le medie non rispettano le soglie didattiche (>0.6 / <0.4) → rende esplicito il “sanity check”.
- **Micro:** etichette nel **`pd.Series`** ancora **`Media (manuale >= 0.6)`** / **`Media (manuale < 0.4)`** ma i valori sono **medie condizionate a `y`**, non a soglie su `p` → rinominare es. **`Media p | y==1`** / **`Media p | y==0`** per non confondere chi rilegge; **`prob_magg_50`** più leggibile come **`np.sum(p_man >= 0.5)`** (equivalente all’ordinato).
- **Micro:** **`print(my_esempio_neurone_csv())`** stampa ancora **`None`** → chiamata senza **`print`** attorno.
- **Lacuna #30:** comportamento corretto su questo checkpoint → 🟢 in `CONTESTO_CORSO.md`.

### [2026-05-11] — TODO 3.1 — rivalutazione (etichette riepilogo + niente `print(None)`)

- **Blocco:** `01_neurone_artificiale.py` righe ~1033–1077 (`my_esempio_neurone_csv`).
- **Voto (stato attuale / micro-fix):** **10/10**.
- **Corretto:** stessa logica solida (**`p_man`**, **`y == 1` / `y == 0`**, assert soglie); **`Media Sigmoide Alterati` / `Media Sigmoide Genuini`** leggibili e coerenti col dominio (sottoinsieme da **`y`**, non da soglie su **`p`**); invocazione **`my_esempio_neurone_csv()`** senza **`print`** → niente **`None`** in console.
- **Micro-opzionale:** **`prob_magg_50 = int(np.sum(p_man >= 0.5))`** rende esplicito che il conteggio è sulle pratiche nel **ordine naturale** del dataset (equivale all’ordinato); messaggio **`ValueError`** più descrittivo (`mean_alt`, `mean_gen`) aiuta in debug.

### [2026-05-11] — TODO 3.2 — forward su `X` grezzo con `w`,`b` del modello allenato su dati scalati

- **Blocco:** `01_neurone_artificiale.py` righe ~1088–1107 (`my_neurone_non_scalato`).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** **`Pipeline`** + **`StandardScaler`** + **`LogisticRegression`**; **`pipe.fit(X,y)`**; estrazione **`w`/`b`** da **`named_steps["model"]`**; **`manual_logits = X @ w + b`** su **`X` non trasformato** → dimostra incoerenza rispetto allo spazio in cui sono stati stimati i parametri; commento che collega **unità di misura / confrontabilità colonne** alla necessità dello scaling — coerente col M2 cap.04.
- **Micro-precisione terminologica:** **`StandardScaler`** non si limita a “dividere per la deviazione standard”: applica **\((x - \mu) / \sigma\)** per colonna (centrare e scalare). Vale la pena di dirlo in una frase nel commento per chiudere al 100% con il richiamo M2.
- **Micro-output:** stampare anche **`pipe.predict_proba(X)[:, 1][:30]`** (o **`np.max(np.abs(manual_pred_alt - p_sk))`**) rende **numerico** il contrasto “corretto vs sbagliato spazio”; riusare **`sigmoid`** globale del capitolo (**clip**) evita warning su logit estremi.

### [2026-05-11] — TODO 3.2 — rivalutazione (tabella + `transform` + formula scaler nel commento)

- **Blocco:** `01_neurone_artificiale.py` righe ~1088–1116 (`my_neurone_non_scalato`).
- **Voto (stato attuale):** **10/10**.
- **Corretto:** **`X_scaled = pipe.named_steps["scaler"].transform(X)`** dopo **`fit`** (no doppio **`fit_transform`** improprio); confronto esplicito **logit/probabilità** su **`X` grezzo vs `X_scaled`** con **`w`,`b` identici**; **`DataFrame`** senza **`str(...)`** sul vettore → **5 righe** leggibili; **`to_string(index=False)`**; commento aggiornato con **\((x-\mu)/\sigma\)** per colonna + messaggio su **coerenza dello spazio** parametri vs input.
- **Micro-opzionale:** una riga **`np.max(np.abs(scaled_manual_pred_alt - pipe.predict_proba(X)[:, 1]))`** mostra che la colonna “Scalato” coincide col **`predict_proba`** (~1e-10); **`sigmoid(...)`** del capitolo al posto di **`exp`** manuale.

### [2026-05-11] — Quiz di verifica V1 (lacuna #28) — logit vs probabilità vs F1

- **Blocco:** `01_neurone_artificiale.py` righe ~1123–1134 (domanda V1 + commento risposta).
- **Voto (primo tentativo):** **9/10**.
- **Corretto:** scelta **(b) logit**; **logit** = output lineare **`X @ w + b`** prima dell’attivazione; distinzione dalla **probabilità** ottenuta dopo **sigmoid**; **(c)** correttamente escluso perché **F1** è una **metrica** su predizioni/etichette (precision/recall), non un output di layer.
- **Micro-testo:** ortografia **“probabilità”**, **“ultimo”**; nella frase sulla probabilità, più preciso dirlo così: **la probabilità stimata è `sigmoid(logit)`**, non che la sigmoid sia “l’ultimo layer” in sé — il layer lineare produce il **logit**, la **sigmoid** è la **funzione di attivazione** che lo mappa in \([0,1]\).
- **Riga “in più”:** formula **`1/(1+e^-z)`** coerente col capitolo (accetta anche rimando alla **`sigmoid`** con clip del file).

### [2026-05-11] — Quiz di verifica V2 — `sigmoid(0)` e limiti

- **Blocco:** `01_neurone_artificiale.py` righe ~1135–1140 (domanda V2 + risposta).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** **`sigmoid(0) = 0.5`** → scelta **(b)**; limite **`z → +∞`** → **1**, **`z → -∞`** → **0**; intuizione del **punto centrale** sul grafico coerente (origine tra i due limiti asintotici).
- **Micro-stile:** nella domanda “**inf**” è bene specificare sempre **`+∞`** / **`-∞`** come hai fatto subito dopo — così non si confonde con “infinito” generico.

### [2026-05-11] — Quiz di verifica V3 — shape `(100, 1)` vs `(100,)`

- **Blocco:** `01_neurone_artificiale.py` righe ~1141–1150 (domanda V3 + risposta).
- **Voto (primo tentativo):** **9.5/10**.
- **Corretto:** con **`w`** di shape **`(4, 1)`**, **`X @ w`** ha shape **`(100, 1)`** → **`p = sigmoid(z)`** resta **`(100, 1)`**; **`reshape(100,)`** (o **`(-1,)`**) appiattisce correttamente per **`roc_auc_score(y_true, y_score)`** che vuole un vettore 1D allineato alle **`n_samples`**.
- **Micro:** **`p.ravel()`** / **`np.squeeze(p)`** sono alternative idiomatiche (stesso effetto se non ci sono ambiguità di dimensione); ortografia **“rappresentata”**.
- **Nota quiz:** nel frammento **`b`** non è definito → in esecuzione saltresti prima sul **`NameError`**; la parte “shape strana” resta comunque la colonna **`(100,1)`** vs **`(100,)`**.

### [2026-05-11] — Quiz di verifica V4 — attivazioni layer nascosti vs sigmoid

- **Blocco:** `01_neurone_artificiale.py` righe ~1151–1156 (domanda V4 + risposta).
- **Voto (primo tentativo):** **7/10**.
- **Corretto:** serve **non-linearità** nei layer nascosti (altrimenti composizione di lineari = ancora lineare); **tanh** centrato su zero conserva il **segno** (utile rispetto a sigmoid tutta positiva); **sigmoid in uscita** per interpretazione **probabilistica** `(0,1)` è coerente.
- **Manca il punto chiave del quiz (“cosa schiaccia troppo”):** la **sigmoid** nei layer profondi **satura** (`→0` o `→1`) → **gradiente quasi zero** (**vanishing gradients**, gradienti che “muoiono”) → reti profonde faticano ad aggiornare i primi layer; **ReLU** mitiga (derivata 1 per `z>0`) anche se ha altri trade-off (es. “dying ReLU”).
- **Micro:** **“si usa”** non “di usa”; **tanh** ortografia.

### [2026-05-11] — Quiz di verifica V5 — inizializzazione pesi a zero

- **Blocco:** `01_neurone_artificiale.py` righe ~1157–1166 (domanda V5 + risposta).
- **Voto (primo tentativo — rubrica “completa” incluso richiamo cap.03):** **6/10**.
- **Corretto:** con **`w = 0`** e **`b = 0`**, **`z = 0`** per ogni riga → **`sigmoid(0)=0.5`** → **`p.mean() == 0.5`**; intuizione “**incertezza massima**” (probabilità a metà) è sensata sul piano della predizione.
- **Preview cap.03 (non prerequisito del cap.01):** con **più neuroni** (layer nascosti), **pesi tutti uguali** → **simmetria**: neuroni identici ricevono **stessi gradienti** e restano **identici** → la rete non esprime **rappresentazioni diverse**; serve **rompere la simmetria** (inizializzazione casuale piccola, Xavier/He, ecc.). **Questa parte va rivalutata dopo il cap.03**, non come lacuna obbligatoria “ora”.
- **Micro:** **“perché”** con accento.

### [2026-05-11] — Quiz V5 — nota equità curricolare (richiesta studente)

- La domanda V5 mescola (a) output **sigmoid/neurone** già visto nel cap.01 e (b) motivazione **allenamento** che nel syllabus è **cap.03 (backprop / gradiente)**.
- **Voto atteso sul solo prerequisito cap.01** (media di **`p`**, significato di **0.5**, incertezza): **8.5/10** — la risposta di Gianluca copre bene questo livello.
- **Regola mentor:** nelle valutazioni del cap.01 non penalizzare per non citare **gradiente/simmetria**; eventualmente etichettare la seconda sotto-domanda come **“Da ripetere dopo cap.03”** nel file capitolo.

### [2026-05-11] — Quiz di verifica V6 — sigmoid su logit ±1.5

- **Blocco:** `01_neurone_artificiale.py` righe ~1167–1172 (domanda V6 + risposta).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** **`sigmoid(1.5) ≈ 0.8176`**, **`sigmoid(-1.5) ≈ 0.1824`** (coerenti con **`1/(1+e^-z)`**); interpretazione **probabilità alta (~82%)** per classe positiva quando **`z = +1.5`** (sopra soglia 0.5); simmetria **sigmoid(z) + sigmoid(-z) = 1** riflessa nei due numeri.
- **Micro-opzionale:** in quiz veloci può bastare **“≈ 0.82 / ≈ 0.18”** senza troppe cifre.

### [2026-05-11] — Quiz di verifica V7 — forward batch `(N,d) @ (d,)`

- **Blocco:** `01_neurone_artificiale.py` righe ~1174–1183 (domanda V7 + risposta).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** **(b) `X @ w + b`** è l’idioma più moderno/alineato a **`numpy.matmul`** e stack numpy/sklearn/PyTorch; **(a)** e **(c)** sono equivalenti numericamente; output shape **`(N,)`** (un logit per riga).
- **Micro-notazione:** convenzione chiara **`(N,)`** al posto di “righe di X” — stesso significato.

### [2026-05-11] — Quiz di verifica V8 — Feynman attivazione (vincolo #27)

- **Blocco:** `01_neurone_artificiale.py` righe ~1185–1189 (domanda V8 + risposta).
- **Voto (primo tentativo):** **10/10**.
- **Corretto:** analogia **estrusione pasta / stampo** rispetta i vincoli (**nessun** uso di “non lineare”, “logit”, “sigmoid”, “rete”); messaggio chiaro: **trasforma** l’output grezzo prima del passo successivo — adeguato per pubblico **web dev**.
- **Micro-opzionale:** una frase sul fatto che è una **regola di trasformazione applicata numero per numero** (come uno stampo che agisce su ogni filo) avvicina ancora di più al neurone senza introdurre jargon vietato.

### [2026-05-11] — E1 [COLLOQUIO] — “Cos’è un neurone artificiale?”

- **Blocco:** `01_neurone_artificiale.py` righe ~1195–1205 (testo risposta E1).
- **Voto (primo tentativo):** **7/10**.
- **Corretto:** definizione **operativa** (combinazione pesata degli input + **bias**) richiamata con **`X @ w + b`** in parole; distinzione **logit grezzo** vs **probabilità** dopo funzione di uscita tipo sigmoid; motivazione **non-linearità** (**ReLU** ecc.) vs solo composizioni lineari — tutto utile in colloquio.
- **Errore da correggere:** espressione **“dot product element-wise”** è **contraddittoria**: *dot product* (qui **`X @ w`**) non è moltiplicazione ** elemento per elemento** tra `X` e `w` (quella sarebbe **`X * w`** solo se broadcastabile, contesto diverso). Dire in colloquio: **combinazione lineare per riga** = **prodotto righe-per-colonna** tra la riga di `X` e il vettore `w`.
- **Struttura consegna:** i **4 punti** richiesti sono **un po’ mescolati** in un unico paragrafo — in interview conviene **enumerare (1)–(4)** in **8–10 righe** nette; ortografia **tanh** non “tahn”.
- **Micro:** “**cuore pulsante**” va bene come metafora; evita di dare esempi di shape troppo lunghi se il recruiter vuole sintesi — una frase su **`N` esempi × `d` feature** basta.

### [2026-05-11] — E2 [REFACTORING parte 1] — `neuro_v1` pattern #25 / #23 / #19

- **Blocco:** `01_neurone_artificiale.py` righe ~1208–1232 (`neuro_v1`).
- **Voto (primo tentativo):** **8/10**.
- **Corretto:** **`NDArray[np.float64]`** al posto di **`np.array`** nei hint; niente **tuple spurie** (`,` fine riga / `return z,`); **`if b is None`** poi **`0.0`** — pattern **#19** rispettato; **`return X @ w + b`** (scala/array, non tupla).
- **Bug API:** firma **`b: float | None`** senza **`= None`** rendeva **`b` obbligatorio** alla chiamata — diverso dall’originale **`b=None`**. **Fix applicato nel file:** **`b: float | None = None`**.

### [2026-05-11] — E2 [REFACTORING parte 1] — rivalutazione stato attuale

- **Blocco:** `01_neurone_artificiale.py` righe ~1225–1232 (`neuro_v1`).
- **Voto (dopo fix `= None`):** **10/10**.
- **Corretto:** **`b: float | None = None`** ripristina parametro opzionale; **pattern #25 / #23 / #19** soddisfati; corpo minimo con **`if b is None`** e **`return X @ w + b`** coerente col testo dell’esercizio.

### [2026-05-11] — E3 [REFACTORING parte 2] — `my_neuro_v2` vettoriale vs `neuro_v2` loop

- **Blocco:** `01_neurone_artificiale.py` righe ~1258–1280 (`my_neuro_v2`, verifica RNG).
- **Voto (primo tentativo):** **7/10**.
- **Corretto:** **`logits = X @ w + b`** (una **`@`**, niente loop); controllo **`X.shape[1] != w.shape[0]`** con **`ValueError`**; nomi **`logits`** / **`probs`** nel corpo; **`np.round(..., 4)`** senza virgola spuria; **`np.allclose`** vs **`neuro_v2`** originale — confronto sensato; check **`ndim`** utile (extra rispetto alla consegna).
- **Manca punto esplicito consegna (lacuna #28):** il testo chiede di **restituire entrambi** — es. **`tuple (logit, prob)`** (logit **non arrotondato**, prob come nell’originale con 4 decimali). Attualmente **`return`** è **solo** le probabilità → **`-> NDArray`** ok per quel return ma non per la tuple richiesta; verifica **`allclose`** andrebbe su **`my_neuro_v2(...)[1]`** (o unpack) dopo il fix.
- **Micro:** messaggio errore “**righe di w**” → più preciso “**lunghezza di `w`**” / **`w.shape[0]`** vs **`X.shape[1]`**; riuso **`sigmoid`** globale del capitolo possibile.

### [2026-05-11] — E3 [REFACTORING parte 2] — rivalutazione (tuple + assert su prob)

- **Blocco:** `01_neurone_artificiale.py` righe ~1258–1280 (`my_neuro_v2`).
- **Voto (stato attuale):** **8.5/10**.
- **Corretto:** **`return` tuple** con **logit** e **prob** separati; **`np.allclose(...)[0]`** confronta le **probabilità** con **`neuro_v2`** — coerente col testo “stessi numeri”; messaggio **`ValueError`** sulla lunghezza di **`w`** corretto; vettorizzazione **`@`** e controlli mantenuti.
- **Micro-consegna:** ordine suggerito nel capitolo è **`(logit, prob)`**; qui è **`(prob, logit)`** — va bene se documentato/unpack esplicito, altrimenti allineare per leggibilità (#28).
- **Micro:** di solito si **arrotonda solo `prob`** (come il loop originale); **`logits`** è utile **grezzo** per debug/metriche — **`np.round(logits, 4)`** opzionale ma meno fedele alla separazione logit vs prob.
- **Type hint:** **`-> NDArray[...]`** non riflette più una **tuple** — meglio **`tuple[NDArray[np.float64], NDArray[np.float64]]`** (o **`tuple`** generico).

### [2026-05-11] — E3 [REFACTORING parte 2] — rivalutazione finale (ordine + hint + assert)

- **Blocco:** `01_neurone_artificiale.py` righe ~1258–1280 (`my_neuro_v2`).
- **Voto (stato attuale):** **10/10**.
- **Corretto:** **`return (logits, np.round(probs, 4))`** — ordine **`(logit, prob)`** come nel testo; **logit grezzo**, prob arrotondata come **`neuro_v2`**; **`assert ... [1]`** allineato alla seconda componente; **`-> tuple[NDArray[np.float64], NDArray[np.float64]]`**; vettorizzazione **`@`**, **`ValueError`** su shape, controlli **`ndim`**.
- **Micro-opzionale:** **`probs = sigmoid(logits)`** usando la **`sigmoid`** del capitolo (**clip**).

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se le lacune #23/#24/#26/#27/#28 risultano 🟢 al primo tentativo del quiz d'ingresso → marcarle `🟢 Superato` in `CONTESTO_CORSO.md` (Lacune dai Quiz).
- Se la #28 (logits vs probabilità) è ancora confusa nel quiz di verifica → riproporre nel cap.02 M3 un blocco esplicito sigmoid/softmax PRIMA di parlare di rete a 2 layer.
- Se il `🔄 [RECALL CROSS-MODULO]` (E6) viene completato senza aiuto → marcare il "ponte cap.02 Ponte → cap.01 M3" come consolidato in CONTESTO; altrimenti riprendere il punto in cap.02 M3.
- Per il cap.02 M3 (reti neurali): partire dall'output del progetto incrementale di questo capitolo (neurone manuale vs LogisticRegression M2 cap.04) e generalizzare a `h` neuroni in parallelo (matrice `W` (d, h)).

---

## Note tecniche di stesura (mentor)

- **07/05/2026 — Lucidatura del capitolo (Fix 1-6)**: dopo aver creato la prima versione, applicati 6 fix di calibrazione:
  1. **`sigmoid` numericamente robusta**: `np.clip(z, -500, +500)` prima di `exp(-z)` → zero `RuntimeWarning` per `|z|` grandi (problema visto nel benchmark). La precisione float64 rende l'arrotondamento irrilevante (tanto sigmoid è già 0.0 o 1.0 oltre `|z| ≈ 36`).
  2. **E5 [RETRIEVAL]** spostato da `sigmoid_stabile` (presente nello scaffold) a **`coseno`** del cap.01 Ponte (Regola 15: retrieval su funzione di capitolo *precedente*).
  3. **Aggiunto blocco `RIPASSO 5 PUNTI cap.02 Ponte`** (R1-R5, mini-esercizi 2-4 righe) prima della Sezione 1 (Regola 8: mini-esercizi inline). R4 e R5 ricontrollano lacune #28 e #29.
  4. **E2 [REFACTORING] splittato in E2 (pattern stilistici) + E3 (logica vettoriale)** per ridurre il sovraccarico (4 pattern in 1 esercizio era troppo). Esercizi rinumerati: E1-E7.
  5. **TODO 1.1 sostituito** con `top3_contributi(x, w, feature_names)` (più creativo, usa le 7 feature reali del CSV M2, no copia-incolla del `neurone()`).
  6. **Aggiunta `_infografica_forward_neurone()`** (Matplotlib): pannello 1 = contribuzioni `x * w`, pannello 2 = somma+bias=z, pannello 3 = sigmoid che mappa z→p. Salva in `modulo_03_dl_cv/figures/01_forward_neurone.png` durante il `__main__`.
- **MAPPA aggiornata** per riflettere R1-R5 e E1-E7.
- **07/05/2026 — Mini-esercizi per blocchi RINFORZO #23–#29**: dopo la parte teorica / «Regola pratica» di ogni lacuna, aggiunti blocchi `Mini-esercizio [RINFORZO #…]` (2–4 righe, `TUO CODICE` o bullet parole per #26) allineati a Regola 8 — prima delle demo `_demo_lacuna_*` / `_benchmark_loop_vs_blas` dove pertinente.
- **DoD line 49** e **auto-rating C4** allineati al nuovo numero esercizio recall (E7).
