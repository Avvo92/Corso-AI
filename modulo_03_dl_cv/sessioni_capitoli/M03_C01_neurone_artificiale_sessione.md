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
