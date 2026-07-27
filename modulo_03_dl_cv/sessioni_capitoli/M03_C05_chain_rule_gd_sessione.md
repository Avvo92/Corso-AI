# Diario sessione — Capitolo 05 — Chain Rule + Gradient Descent

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `05_chain_rule_gd.py` |
| **File diario** | `M03_C05_chain_rule_gd_sessione.md` |
| **Stato** | ✅ **Chiuso il 27/07/2026** — bridge **M03_R05** popolato, rinforzi inseriti in cap.06 |
| **Voto difficoltà** | ⏳ da confermare (atteso 7–8/10) |

---

## Obiettivi del capitolo (aggiornato a chiusura cap.04 — 16/06/2026)

- Far interiorizzare la **chain rule** come "prodotto di derivate strato per strato" via esempio numerico semplice.
- Implementare **gradient descent generico** su funzione test (paraboloide).
- Mostrare l'**effetto del learning rate** con 3 lr a confronto (piccolo / "giusto" / grande).
- **Prima di tutto:** completare **🔁 RINFORZO MIRATO cap.04** (R1–R6) su `dL/dz = p-y` — lacuna #36.
- Usare **`h=1e-6`** in gradiente_numerico (Pattern #26 da cap.04).

---

## Strategia didattica (da affinare)

- Sequenza per OGNI concetto matematico: **analogia concreta -> codice Python -> grafico -> formula in parole**.
- Niente LaTeX.
- Se il cap.04 ha lasciato lacune (gradiente, derivata sigmoid), inserire blocchi `🔁 RINFORZO MIRATO`.

---

## Domande durante lo studio

- _(da popolare)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Voto = "primo tentativo".

_(Nessuna valutazione ancora — capitolo da aprire.)_

### 2026-06-16 — Bridge R04 Q1 (`M03_R04` — derivata in 1 riga)

- **Domanda:** cos'è una derivata (senza limiti/LaTeX).
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** Pendenza nel punto x — vocabolario corretto del cap.04; allineato a checkpoint C1 (9/10).
- **Affinamento opzionale:** aggiungere “quanto cambia f se muovi x di un filo” per collegare a training.

### 2026-06-16 — Bridge R04 Q2 (`M03_R04` — sigmoid derivata max)

- **Domanda:** massimo di `derivata_sigmoid(z)` e dove.
- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** **0.25** corretto; collegamento a **z=0** (via f'(0)).
- **Errori / lacune:** notazione ambigua — “si trova in f'(0)” confonde **punto** (z=0) e **valore** (0.25); meglio “massimo **0.25** quando **z=0**”; typo *sigimoide*.
- **Modello:** `derivata_sigmoid(0) = 0.25` (unico massimo).

### 2026-06-16 — Bridge R04 Q2 — post-fix notazione z=0

- **Fix:** “si trova in **0**” (z=0) invece di f'(0).
- **Valutazione post-feedback:** **9/10** (primo tentativo resta **8/10**).
- **Residuo:** esplicitare `z=0` per chiarezza colloquio.

### 2026-06-16 — Bridge R04 Q3 (`M03_R04` — vanishing `0.25**4`)

- **Domanda:** valore decimale di `0.25 ** 4` (4 layer sigmoid in fila).
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** **0,00390625** esatto (= 1/256); calcolo corretto; notazione decimale italiana ok.
- **Affinamento opzionale:** in colloquio aggiungere “~**0.004**” per l’intuizione vanishing — dopo 4 layer il gradiente è già quasi zero.

### 2026-06-16 — Bridge R04 Q4 (`M03_R04` — derivata ReLU)

- **Domanda:** output di `derivata_relu([-2, 0, 3])`.
- **Risposta studente:** `[0, 0.5, 1]`.
- **Valutazione (primo tentativo):** **6.5/10**.
- **Corretto:** `z=-2 → 0`, `z=3 → 1`.
- **Errore:** `z=0 → 0`, non `0.5`. Regola corso: `1 se z>0`, `0 se z<=0` (PyTorch idem).
- **Probabile confusione:** sigmoid(0)=0.5 oppure nota “alcune librerie usano 0.5” nel cap.04 — qui vale **0**.
- **Modello:** `[0, 0, 1]` (o `[0. 0. 1.]` NumPy).

### 2026-06-16 — Bridge R04 Q5 (`M03_R04` — semplificazione `p-y`)

- **Domanda:** con `p = sigmoid(z)` e BCE, `dL/dz` (un campione).
- **Risposta studente:** `p - y`.
- **Valutazione (primo tentativo):** **10/10**.
- **Punti di forza:** formula esatta; allineato a cap.04 C3 post-fix (9/10) e lacuna #36; pronto per chain rule cap.05.
- **Nota:** verificare sotto stress in cap.05 R1–R6 (non solo recall a freddo).

### 2026-06-16 — Bridge R04 Q6 (`M03_R04` — `dL/dp` vs `dL/dz`)

- **Domanda:** `dL/dp` è uguale a `p-y`? (Sì/No + perché).
- **Risposta studente:** Sì; `(p-y)/(p(1-p)) * p(1-p) = p-y`.
- **Valutazione (primo tentativo):** **5.5/10**.
- **Errore:** risposta **No** — `dL/dp = (p-y)/(p(1-p))`, non `p-y`.
- **Punti di forza:** algebra chain rule corretta (`dL/dp * dp/dz = dL/dz`); confonde **risultato finale** `dL/dz` con `dL/dp`.
- **Modello:** No — `p-y` è `dL/dz`; `dL/dp` ha il denominatore `p(1-p)`.

### 2026-06-16 — Bridge R04 Q6 — post-fix `dL/dp` ≠ `p-y`

- **Fix:** **No**; `(p-y)/(p(1-p)) != p-y`.
- **Valutazione post-feedback:** **9/10** (primo tentativo resta **5.5/10**).
- **Punti di forza:** risposta binaria corretta; formula `dL/dp` esplicita.
- **Affinamento opzionale:** aggiungere che `p-y` è **`dL/dz`** dopo chain rule × `p(1-p)`.

### 2026-06-16 — Bridge R04 Q7 (`M03_R04` — gradiente in (1, 2))

- **Domanda:** gradiente di `f(x,y)=x²+y²` in `(1, 2)`.
- **Risposta studente:** `[2, 4]`.
- **Valutazione (primo tentativo):** **10/10**.
- **Punti di forza:** `∂f/∂x=2x→2`, `∂f/∂y=2y→4`; ordine `[x, y]` corretto; allineato a cap.04 C4 (9/10).

### 2026-06-16 — Bridge R04 Q8 (`M03_R04` — `h` numerico)

- **Domanda:** default `h`/`eps` in `derivata_numerica`; perché non `1e-24`.
- **Risposta studente:** default `eps=1e-6`; troppo piccolo → impreciso, inconfrontabile con analitica.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** **1e-6** corretto; intuizione imprecisione ok (Pattern #26).
- **Manca:** **cancellazione numerica** in `f(x+h)-f(x)`; precisione float64 ~**1e-16** → `1e-24` è rumore.
- **Stile:** chiarire che “troppo piccolo” si riferisce a `1e-24`, non a `1e-6`.

### 2026-06-16 — Bridge R04 Q8 — post-fix chiarezza `1e-24`

- **Fix:** `1e-24 sarebbe troppo piccolo` esplicito; `1e-6` = default corretto.
- **Valutazione post-feedback:** **9/10** (primo tentativo resta **8.5/10**).
- **Residuo opzionale:** cancellazione in `f(x+h)-f(x)` + precisione float ~1e-16.

### 2026-06-16 — Bridge R04 Q9 (`M03_R04` — Feynman derivata vs gradiente)

- **Domanda:** differenza in 2 righe, senza jargon pesante.
- **Risposta studente:** derivata = pendenza; gradiente = vettore di derivate parziali (un parametro alla volta, altri fissi).
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** pendenza 1D; meccanismo parziali esplicito; allineato a soluzione bridge e cap.04 C1/C4.
- **Affinamento opzionale:** “un **numero** vs una **lista** di pendenze” per il contrasto 1D/nD.

### 2026-06-16 — Bridge R04 Q10 (`M03_R04` — ordine `bce_loss`)

- **Domanda:** chiamata corretta con probabilità `P` ed etichette `y`.
- **Risposta studente:** `bce_loss(p, y)`.
- **Valutazione (primo tentativo):** **10/10**.
- **Punti di forza:** ordine **probabilità → etichette** corretto; lacuna #35 recall ok al bridge.

### 2026-06-16 — Cap.05 Quiz ingresso Q1 (`05_chain_rule_gd.py` — sigmoid' e vanishing)

- **Domanda:** derivata sigmoid in z=0 e z=10; significato vanishing.
- **Risposta studente:** z=0 → **0.25**; z=10 → **~4.54e-05**; ~`0.25^n` con layer sigmoid in fila.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** valori numerici corretti; meccanismo moltiplicativo esplicito; lacuna #33 in miglioramento.
- **Affinamento:** z=10 → sigmoid satura (~1), derivata quasi zero; chain rule moltiplica questi fattori.

### 2026-06-16 — Cap.05 Quiz ingresso Q2 (`05_chain_rule_gd.py` — semplificazione `p-y`)

- **Domanda:** da dove arriva `dL/dz = p - y` con BCE + sigmoid.
- **Risposta studente:** chain rule `dL/dp * dp/dz`; solo BCE+sigmoid; `(p-y)/(p(1-p)) * p(1-p) = p-y`.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** algebra e cancellazione corrette; vincolo BCE+sigmoid esplicito; lacuna #36 in miglioramento vs bridge Q6.
- **Affinamento:** citare i 4 passi della guida (chain rule → formule → moltiplica → cancella).

### 2026-06-16 — Cap.05 Quiz ingresso Q3 (`05_chain_rule_gd.py` — BCE su probabilità)

- **Domanda:** perché BCE su probabilità continue, non su `P>=0.5` binario.
- **Risposta studente:** BCE giudica la “sicurezza”; serve percentuale continua; vs `accuracy_score`.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** intuizione confidenza vs etichetta dura; contrasto metrica di training vs accuracy.
- **Manca (critico per cap.05–06):** **derivabilità** per backprop; binarizzare → `log(0)` / gradiente nullo → training impossibile.

### 2026-06-16 — Cap.05 Quiz ingresso Q4 (`05_chain_rule_gd.py` — ops forward 2-layer)

- **Domanda:** operazioni elementari forward **per pratica** (X `(N,d)`, W1 `(d,h)`, W2 `(h,1)`).
- **Risposta studente:** `N*d*h + N*h*1`.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** due dot product corretti (`d*h` + `h`); struttura forward cap.02 ok.
- **Errore:** domanda chiede **per pratica** → `d*h + h` (= `h*(d+1)`); `N` è costo **batch intero**, non singolo campione.

### 2026-06-16 — Cap.05 Quiz ingresso Q4 — post-fix per pratica

- **Fix:** `d*h + h*1` (senza `N`).
- **Valutazione post-feedback:** **9.5/10** (primo tentativo resta **7.5/10**).
- **Punti di forza:** scope corretto; equivalente `h*(d+1)`.
- **Residuo:** notazione `*d*h` superflua — scrivere `d*h + h`.

### 2026-06-16 — Cap.05 Quiz ingresso Q5 (`05_chain_rule_gd.py` — direzione GD)

- **Domanda:** `f(x)=(x-3)²`, in `x=0` dove muoversi per far scendere `f`?
- **Risposta studente:** né +x né -x; crede minimo in 0 perché confonde con `x²`.
- **Valutazione (primo tentativo):** **2.5/10**.
- **Errore:** `f(0)=(0-3)²=9`, minimo in **x=3**; `f'(0)=-6` → muoversi in **+x** (contro il gradiente).
- **Pattern:** #6 consegna — parabola **traslata**, non centrata in 0.

### 2026-06-16 — Cap.05 Quiz ingresso Q5 — post-fix direzione +x

- **Fix:** **+x**; intuizione `(x-3) → 0` quindi `x → 3` (minimo).
- **Valutazione post-feedback:** **8.5/10** (primo tentativo resta **2.5/10**).
- **Punti di forza:** direzione corretta; lettura parabola traslata recuperata.
- **Affinamento:** esplicitare minimo in **x=3**; opzionale `f'(0)=-6` → contro gradiente = +x.

### 2026-06-16 — Cap.05 Quiz ingresso Q6 (`05_chain_rule_gd.py` — Feynman GD)

- **Domanda:** spiegare GD in 4 righe a collega web dev; vietati gradiente/derivata/funzione/pesi.
- **Risposta studente:** loop prova→misura punteggio→passo nella direzione che abbassa→ripeti.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** vincoli lessicali rispettati; ciclo iterativo chiaro; alto/basso errore ok.
- **Affinamento:** 6 righe vs 4 richieste; agganciare esempio web (tempo caricamento); in GD reale si va sempre “contro la pendenza”, non si provano due direzioni a caso.

---

### 2026-06-16 — Cap.05 Quiz ingresso Q7 (`05_chain_rule_gd.py` — prevedi output loop GD)

- **Domanda:** prevedere output di 3 step: `x = x - 0.1*(2*x)` partendo da `x=10`.
- **Risposta studente:** `8`, `6.4`, `5.12`.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** moltiplicatore `0.8` usato correttamente: `10→8→6.4→5.12`.
- **Affinamento:** in Python `round(...,4)` stampa `8.0`, `6.4`, `5.12` (stesso valore; solo formato float).

### 2026-06-18 — Cap.05 Mini 1.1.A (`05_chain_rule_gd.py` — chain rule 3 composizioni)

- **Esercizio:** `h'(x)` a mano + chain rule su 3 funzioni; verifica in `x=1`.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** tutti e 3 i punti con decomposizione, `g_prime`/`f_prime`, `h_prime` e `h_prime_chain` corretti; fix punto 3 (`* 2`, `2*x`).
- **Manca:** `derivata_numerica(h, 1)` esplicita (consegna); `h = f(g)` solo nel punto 1 — aggiungere in 2 e 3.
- **Valori attesi x=1:** 24 | ~1.08 | ~40.17.

### 2026-06-18 — Cap.05 Mini 1.1.A — post-fix verifica numerica

- **Fix:** `h = f(g)` in tutti e 3 i punti; `derivata_numerica(h, x)` aggiunta.
- **Valutazione post-feedback:** **9.5/10** (primo tentativo resta **8.5/10**).
- **Residuo cosmetico:** `h_prime_num` wrapper opzionale — `derivata_numerica(h, 1)` diretto basta.

### 2026-06-18 — Cap.05 Mini 1.3.A (`05_chain_rule_gd.py` — sigmoid composta)

- **Esercizio:** `h(x)=sigmoid(2x+1)`; chain rule; verifica in `x∈{0,1,-1}`.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** `g`/`g_prime`/`derivata_sigmoide`/`h` corretti; loop + `assert np.allclose` su 3 punti.
- **Affinamento:** stampa `x` nel loop per leggibilità; opzionale `f=sigmoid` per pattern uniforme con 1.1.A.

### 2026-06-18 — Cap.05 RINFORZO R1 (`05_chain_rule_gd.py` — schema p-y a parole)

- **Esercizio:** 4 righe su z, p, dL/dz, chain rule, semplificazione miracolosa.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** z=logit, p dopo sigmoid; dL/dz su z; chain rule dL/dp·dp/dz; cancellazione → p-y.
- **Affinamento:** esplicitare `p=sigmoid(z)`; L dipende da **p** non da z direttamente (motivo del passaggio intermedio).

### 2026-06-18 — Cap.05 RINFORZO R2 (`05_chain_rule_gd.py` — retrieval dL/dp, dp/dz)

- **Esercizio:** formule locali + moltiplicazione → `p-y` (senza aprire cap.04).
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** `dL/dp=(p-y)/(p(1-p))`, `dp/dz=p(1-p)`; cancellazione e `p-y` corretti; lacune #36/#38.
- **Affinamento:** notazione `p*(1-p)` al denominatore per chiarezza.

### 2026-06-18 — Cap.05 RINFORZO R3 (`05_chain_rule_gd.py` — numerico vs analitico su z)

- **Esercizio:** `ana=(p-y)/len(z)` vs `gradiente_numerico` su BCE media; `z=[-2,0,2]`, `y=[1,0,1]`.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** formula analitica corretta; lambda su `bce_loss(sigmoid(...))`; `assert np.allclose`; `/len(z)` compreso (media batch).
- **Affinamento:** `y` come `dtype=float` per coerenza; lacuna #36 consolidata se assert ok.

### 2026-06-18 — Cap.05 RINFORZO R4 (`05_chain_rule_gd.py` — dL/dp vs dL/dz)

- **Esercizio:** `ana=((p-y)/(p(1-p)))/len(p)` vs `gradiente_numerico` su `p`; commento perché non `p-y`.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** codice e assert corretti; `/len(p)` ok; distingue semplificazione su `z` vs formula su `p`.
- **Affinamento:** nel commento usare `(p-y)/(p*(1-p))` — la prosa `(p-y)/p*(1-p)` è ambigua; chiudere con «p-y è dL/dz, non dL/dp» (lacuna #38).

### 2026-06-18 — Cap.05 Mini 2.1.A (`05_chain_rule_gd.py` — chain rule 3 livelli)

- **Esercizio:** `y=sin((2x+1)²)`; h/g/f + verifica `x∈{0,1}`.
- **Valutazione (primo tentativo):** **9.5/10** (dopo fix `g_prime`).
- **Punti di forza:** `f_y` composizione ok; `f'·g'·h'` corretta; assert su 2 punti.
- **Valori attesi:** x=0 ~2.16; x=1 ~-10.9.

### 2026-06-18 — Cap.05 Mini 2.1.B (`05_chain_rule_gd.py` — chain rule 4 livelli)

- **Esercizio:** `y=exp(sin(cos(x²)))`; prodotto 4 derivate; verifica `x=0.5`.
- **Valutazione (primo tentativo):** **5.5/10** (h2' senza `-`, h3=-sin errato).
- **Valutazione post-fix:** **9.5/10**.
- **Punti di forza:** h2'=-sin, h3=sin, composizione e assert ok.

### 2026-06-18 — Cap.05 TODO 3 (`05_chain_rule_gd.py` — 5 derivate locali dL/dW1)

- **Esercizio:** mappatura mentale delle 5 derivate locali sulla catena verso W1.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** catena L→P→Z2→H→Z1→W1 corretta; semplificazione p-y citata; ramo parallelo dL/dW2 (fork da dL/dZ2) — ottimo insight.
- **Affinamento:** (1) esercizio chiede derivate *locali* (dL/dP, dP/dZ2, dZ2/dH, dH/dZ1, dZ1/dW1) — non solo il prodotto accumulato; (2) «rispetto a P» non «rispetto sigmoide»; (3) notazione dZ2/dW2 non dZ2/W2.

### 2026-06-18 — Cap.05 ESERCIZIO 3.A (`05_chain_rule_gd.py` — punti a, b, c)

- **(a) Catena L→W2:** corretta dopo fix (`L→P→Z2→W2`). **10/10**.
- **(b) Tre anelli:** corretta dopo fix direzione (P→L, Z2→P, W2→Z2). **9.5/10** (usa P maiuscolo).
- **(c) Altro fattore:** `dZ2/dW2=H`, `dZ2/dH=W2`. **10/10**.

### 2026-06-18 — Cap.05 ESERCIZIO 3.B (`05_chain_rule_gd.py` — dL/dW2 a mano)

- **(a) Formula/shape:** scritto `dL/dZ2 @ H^T` (ordine invertito); W2 citato `(2,2)` invece di `(h,1)=(2,1)`.
- **(b) Calcolo:** `H.T @ delta` → **[-0.20, -0.10]** numericamente corretto. Manca `.reshape(-1,1)` per shape `(2,1)`.
- **(c) Segno:** scritto «vuole abbassare» — **errato**: grad negativo → update `W - lr*grad` **aumenta** il peso (la loss scende).
- **Valutazione (primo tentativo):** **7/10**.

### 2026-06-18 — Cap.05 ESERCIZIO 3.C (`05_chain_rule_gd.py` — mezzo backward verso W1)

- **Codice:** `dL_dH = dL_dZ2 @ W2.T`, maschera ReLU, `X.T @ dL_dZ1` — formule corrette.
- **Numeri attesi:** dL/dH `[[0.125, 0.25], [-0.075, -0.15]]`; dopo ReLU azzera `[0,1]` e `[1,0]`; dL/dW1 = dL/dZ1 (X=I).
- **(b)** non nominato esplicitamente quali elementi (due azzerati: Z1[0,1]=-1, Z1[1,0]=0).
- **(c)** shape `(2,2)` ok ma motivazione `(d,N)` errata → corretto `(d,h)`.
- **(d) Feynman:** ok ma generico; manca «ReLU piatta → ∂H/∂Z1=0 → niente gradiente verso W1».
- **Valutazione (primo tentativo):** **8/10**.

### 2026-06-18 — Cap.05 Mini 4.1.A (`05_chain_rule_gd.py` — GD su 3 funzioni)

- **Esercizio:** `gradient_descent_1d` su 3 parabole/polinomi; x0=10, n_steps=50; stampa ultimo x.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** 3 funzioni lambda corrette; parametri lr/n_steps come consegna; uso corretto di `traj[-1]`.
- **Affinamento:** typo stampa «Funzione 2» due volte (f3 → «Funzione 3»); opzionale kwargs espliciti (`x0=10`).
- **Post-fix stampa:** **10/10** implementazione. Nota: con lr=0.05 su `(x-1)^4` da x0=10 GD **diverge** (ultimo x lontanissimo da 1) — lezione su lr, non bug del codice studente.

### 2026-06-18 — Cap.05 Mini 4.1.B (`05_chain_rule_gd.py` — GD lr troppo grande)

- **Codice:** corretto (`f=(x-3)^2`, lr=1.5, stampa traiettoria).
- **Osservazione:** scritto «oscilla» — più preciso: **diverge** (oscillazioni con ampiezza che cresce: 10→-11→31→…).
- **Spiegazione:** ok (step troppo ampi amplificano errore); manca overshoot oltre il minimo x=3.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-06-18 — Cap.05 Mini 4.2.A (`05_chain_rule_gd.py` — grafico GD + verifica file)

- **Codice:** `_grafico_gd_1d_traiettoria(out_path=...)` + `os.path.exists` con if/else — corretto.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Opzionale:** `getsize > 0` o `Path(__file__).parent / "figures" / ...` per path robusto se si esegue da root progetto.

### 2026-06-18 — Cap.05 Mini 4.3.A (`05_chain_rule_gd.py` — GD early stop)

- **Funzione:** `gradient_descent_1d_early_stop` con `|grad|<tol` o passo `<tol`, `break`, append finale, ritorno `(traiettoria, int)`.
- **Test:** `(x-3)^2`, x0=10, lr=0.2 → ~30 iter (stop su passo piccolo prima di `|grad|<1e-6` stretto — accettabile).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-06-18 — Cap.05 Mini 5.1.A (`05_chain_rule_gd.py` — replica `_demo_lr`)

- **Codice:** `my_demo_lr` con loop su lr, `gradient_descent_1d`, stampa x finale e distanza — corretto e buon allenamento.
- **Differenze da `_demo_lr`:** n_steps=50 (ok), manca riga header tabella; non chiamata `_demo_lr()` (scelta volontaria per pratica).
- **Commenti:** lr=0.01 ok concetto; formula con `+` invece di `W - lr*grad`; riga «divergenza» etichettata `lr=0.9` invece di `1.5`; manca commento esplicito su oscillazione 0.9.
- **Valutazione (primo tentativo):** **8/10** (codice 9+, commenti 6.5).

### 2026-06-18 — Cap.05 Mini 5.1.B (`05_chain_rule_gd.py` — grafico lr confronto)

- **Codice:** `_grafico_lr_a_confronto` + `assert os.path.exists` — corretto.
- **Risposta divergenza lr=1.5:** scritto «plateau» — **errato**: loss **esplode** (crescita rapida, oscillante); plateau = curva piatta (opposto).
- **Valutazione (primo tentativo):** **7/10**.

### 2026-06-18 — Cap.05 Mini 5.2.A (`05_chain_rule_gd.py` — lr ottimo)

- **Struttura:** loop lr, lista→DataFrame, sort — buona.
- **Bug metrica:** `4 - abs(x_finale)` invece di `abs(x_finale - 4)`; sort `ascending=False` (meglio True su distanza).
- **lr ottimo atteso:** ~0.3–0.5 (distanza ≈ 0 in 30 step); 1.0 e 1.5 pessimi.
- **Valutazione (primo tentativo):** **6.5/10**.

### 2026-06-18 — Cap.05 Mini 6.1.A (`05_chain_rule_gd.py` — GD multivariato)

- **Post-fix:** stampa `traj[::5]` ok; replica `my_gradient_descent_nd` corretta.
- **Spiegazione y più veloce:** migliorata (gradiente più ripido → passi più lunghi); opzionale citare esplicitamente `∂f/∂x=2x` vs `∂f/∂y=8y`.
- **Valutazione (primo tentativo):** **7.5/10** → **post-fix: 9/10**.

### 2026-06-18 — Cap.05 TODO 1 (`05_chain_rule_gd.py` — sigmoid composta)

- **Esercizio:** h(x)=sigmoid(a*x+b), chain rule + check numerico x∈{0,1,2}.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** g,f,h scomposte; `*a`; `derivata_numerica` su h composta; assert+print.
- **Opzionale:** `float(x)`; lambda `xv` per evitare shadowing del loop `x`.

### 2026-07-17 — Cap.05 TODO 3 (`05_chain_rule_gd.py` — GD 2D verso (3,-2))

- **Setup:** f=(w1-3)²+(w2+2)², x0=[0,0], lr=0.3, n_steps=30 — corretto; converge (assert ok).
- **Stampa:** x0 + step 1/5/15/30 ok.
- **Lacuna:** variabile `dist_euclidea` = punto minimo, non distanza; manca `np.linalg.norm(traj[i]-minimo)`.
- **Naming:** `grad` è la traiettoria, non il gradiente.
- **Valutazione (primo tentativo):** **8/10**.

### 2026-07-21 — Cap.05 TODO 5 (`05_chain_rule_gd.py` — GD su BCE 1 peso)

- **GD:** `gradient_descent_nd(loss_w, [-3], lr=1, 30)` converge: w≈2.39, p≈0.99, loss↓ — concetto ok.
- **loss_w:** funziona ma shape fragile (`w_vec*x` + `np.array([p])` → (1,1)); meglio `w_vec[0]*2.0`.
- **Stampa:** `sigmoid(traj[-1])` e `bce_loss(sigmoid(traj[0]), …)` **dimenticano ×x** → p/loss stampati sbagliati (modello è sigmoid(w*x)).
- **Valutazione (primo tentativo):** **7.5/10**.
- **Post-fix:** loss iniziale/finale con `sigmoid(w*x)` ok; sigmoid finale stampata ancora senza `×x`. **9/10**.

### 2026-07-21 — Cap.05 TODO 6 (`05_chain_rule_gd.py` — dL/dw analitico vs numerico)

- **Codice:** `(p-y)*x` + `gradiente_numerico` + `assert isclose` + `w=-3.0` (fix dtype) — corretto.
- **Commento segno:** ok (w più grande); manca legame esplicito update `w - lr*grad` e `p→1`.
- **Opzionale:** `w_var[0]` nella lambda; stampare ana vs num.
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-21 — Cap.05 TODO 7 (`05_chain_rule_gd.py` — retrieval dL/dz = p-y)

- **Commento:** semplificazione ok; manca esplicito `z→p→L` in 4 righe.
- **Codice:** verifica numerica ok in sostanza; usato `gradiente_numerico` invece di `derivata_numerico` (consegna); `assert` su array ok per broadcasting; `semp_mir` calcolato ma non usato nell'assert.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-21 — Cap.05 TODO 8 (`05_chain_rule_gd.py` — recall my_bce)

- **Clip bilaterale:** ok.
- **Bug formula:** scritto `-y - log(p)` invece di `-y * log(p)` (manca moltiplicazione).
- **Manca:** confronto/assert con `bce_loss` ufficiale.
- **Valutazione (primo tentativo):** **5.5/10**.
- **Post-fix:** formula `-y*log(p)-(1-y)*log(1-p)` + assert vs `bce_loss` — **10/10**.

### 2026-07-21 — Cap.05 TODO 9 (`05_chain_rule_gd.py` — recall derivata sigmoid/ReLU)

- **Formule:** sigmoid' e ReLU' corrette e vettorizzate; z=[-2,0,2] → ReLU' [0,0,1] ok.
- **Naming:** `derivata_*` invece di `my_derivata_*` (consegna) — accettabile.
- **Manca:** assert sui valori attesi (solo print).
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-22 — Cap.05 TODO 10 (`05_chain_rule_gd.py` — recall gradiente_numerico)

- **Funzione:** differenza centrata corretta (`xp += h`, `xm -= h`); verifica vs `gradiente_numerico` e atteso [2,-4] ok.
- **Opzionale:** `zeros_like(..., dtype=float)`; assert anche su `[2,-4]`.
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-22 — Cap.05 TODO 11 (`05_chain_rule_gd.py` — 1 step GD numerico su W2)

- **Pipeline:** setup, forward, f(W2)→loss, gradiente_numerico, W2-=lr*grad, loss finale + assert — corretto; loss scende.
- **Note:** flatten manuale opzionale (API supporta shape (4,1)); `y` da `np.random` invece di `rng` (riproducibilità minore).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-22 — Cap.05 PIPE.1 (`05_chain_rule_gd.py` — addestramento neurone via grad numerico)

- **Motore:** `[w,b]` + `loss_params` + GD numerico + accuracy soglia 0.5 — corretto; con lr=0.5 tipicamente acc=1, w>0, b<0.
- **Gap consegna:** `lr=0.3` (chiesto 0.5); history lunghezza `n_steps` non `n_steps+1` (manca stato post-ultimo update in lista); nome ≠ `addestramento_via_gradiente_numerico`; print verbose ok ma senza stato iniziale in history; bonus plot assente.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-22 — Cap.05 TODO 12 Q1 (`05_chain_rule_gd.py` — chain rule colloquio)

- **Risposta:** collega chain rule a backprop e moltiplicazione derivate — direzione ok.
- **Gap:** chain rule è più generale (derivata di funzioni *composte*); backprop la *usa*. Manca formula/esempio y=f(g(x)) → f'·g'. Typo chian/regole.
- **Valutazione (primo tentativo):** **6/10**.

### 2026-07-22 — Cap.05 TODO 12 Q1+Q2 (rivalutazione)

- **Q1 post-fix:** definizione composizione + derivate locali ok; ancora “alla base del backprop” come uguaglianza (meglio: backprop la usa); manca f(g(x)). **7.5/10**.
- **Q2:** idea minimizzare/scendere ok; formulazione confusa (“minimo di ogni elemento del gradiente”); manca update `θ = θ - lr·∇L`. Confonde chain rule (calcola grad) con GD (usa grad). **5.5/10**.
- **Q2 post-fix:** abbassa loss + usa grad backprop + aggiorna pesi — ok; manca esplicito `θ−lr∇L` e “direzione *opposta* al gradiente”. **8/10**.
- **Q2 post-fix 2:** opposta + `w = w - lr * grad` — **9.5/10**.

### 2026-07-22 — Cap.05 TODO 12 Q3 (derivate locali per W1)

- **Risposta:** 5 derivate, ordine BCE→sigmoid→W2→ReLU→W1 — conteggio e catena corretti.
- **Affinamento:** nomi `der_w2`/`der_w1` imprecisi (sono dZ2/dH e dZ1/dW1); meglio elencare i 5 simboli locali.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-22 — Cap.05 TODO 12 Q4 (lr troppo grande/piccolo)

- **Risposta:** lr alto → salta/diverge loss↑; lr basso → lento — corretto.
- **Affinamento:** “salta intorno” meglio “supera il minimo / diverge”; lento ≠ solo “curva piatta” (scende ma con passi minuscoli).
- **Valutazione (primo tentativo):** **8.5/10**.
- **Post-fix:** lr alto → supera/diverge ok; lr basso → passi minuscoli ok; ancora rischia di confondere “lento” con “stallo/plateau”. **8.5/10** (stabile).

### 2026-07-22 — Cap.05 TODO 12 Q5 bonus (semplificazione miracolosa)

- **Algebra:** cancellazione (p-y)/[p(1-p)] * p(1-p) = p-y — corretta.
- **Errore naming:** scritto `dp/dW2`; la semplificazione è su **logit z**: `dL/dz = dL/dp * dp/dz`. `dL/dW2` richiede ancora `dZ2/dW2 = H`.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Post-fix:** `dL/dp * dp/dz` → `p-y` corretto (= `dL/dz`). **9.5/10**.

### 2026-07-22 — Cap.05 TODO 13 (`05_chain_rule_gd.py` — refactor GD)

- **Core:** differenza centrata + update GD corretti; converge a ~3 su (x-3)^2.
- **Gap:** manca docstring 2 righe; return `np.array` invece di `list`; type hint `NDArray` vs lista; `eps=1e-12` (meglio ~1e-6 come corso); manca confronto/assert vs `gradient_descent_1d`.
- **Valutazione (primo tentativo):** **8/10**.
- **Post-fix:** `list[float]` + docstring + `eps=1e-6` + assert vs `gradient_descent_1d` OK (allclose). **10/10**.

### 2026-07-22 — Cap.05 TODO 14 (`05_chain_rule_gd.py` — DEBUG segno GD)

- **Diagnosi:** `w + lr * grad` → sale loss; corretto `w - lr * mean((p-y)*x)` — spiegazione chiara (stessa direzione del gradiente).
- **Gap:** formula nel commento OK; manca la funzione riscritta eseguibile (consegna: “versione corretta”).
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-22 — Cap.05 TODO 16 (`05_chain_rule_gd.py` — INTERLEAVING rete + GD numerico)

- **Core:** He ok, theta flat 21, unpack+loss BCE, GD con `-lr*grad`, print ogni 10; loss 0.66→0.16, acc 0.55→1.0.
- **Nota:** loop GD riscritto a mano (equivalente a `gradient_descent_nd`); print prima dell’update (label step corretti).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-23 — Cap.05 Quiz V1 (chain rule)

- **Risposta:** prodotto derivate locali; formula `dL/dw = dL/dp * dp/dz * dz/dw` — corretta e pertinente al neurone.
- **Affinamento:** “2 livelli” classico = `dh/dx = dh/du * du/dx` (2 fattori); la sua è catena a 3 anelli (ancora valida).
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-23 — Cap.05 Quiz V2 (h=sin(x²))

- **Risposta:** `cos(x²)*2x` via f1=x², f2=sin; controprova `derivata_numerica(h,x)` — impostazione corretta.
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-23 — Cap.05 Quiz V3 (gradient descent)

- **Update:** peso − lr·gradiente — corretto.
- **Imprecisione:** “portare la *derivata* al minimo” → si minimizza la **funzione** (loss); al minimo il gradiente tende a ~0.
- **Valutazione (primo tentativo):** **8/10**.
- **Post-fix:** minimizza la loss; al minimo derivata ~0; update −lr·grad — **9.5/10**.

### 2026-07-23 — Cap.05 Quiz V4 (lr grande/piccolo)

- **Risposta:** lr alto → salta minimo/diverge; lr basso → traiettoria “quasi piatta” / addestramento lungo — sostanzialmente ok.
- **Affinamento:** non è il gradiente che salta, è il **passo** `lr·grad`; “piatta” ≠ plateau (scende, ma a passi minuscoli).
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-23 — Cap.05 Quiz V5 (bug segno GD)

- **Risposta:** `+` → `-`; contro il gradiente per far scendere la loss — corretta e chiara.
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-23 — Cap.05 Quiz V6 (prevedi output GD)

- **Metodo:** `x - lr * f'(x)` con f=x² → f'=2x — schema corretto.
- **Errore:** a x=3.2, grad=2·3.2=**6.4** (non 6.2) → x=3.2-0.64=**2.56** (non 2.58).
- **Valutazione (primo tentativo):** **7/10**.
- **Post-fix:** grad=6.4, x=2.56 — **10/10**.

### 2026-07-23 — Cap.05 Quiz V7 (5 derivate locali → dL/dW1)

- **Inizio ok:** dL/dp · dp/dz… ma poi catena sbagliata: `dz/dW2`, `dW2/dh`, `dH/dW1` (W2 non è sul percorso verso W1; manca Z1).
- **Corretta:** dL/dP · dP/dZ2 · dZ2/dH · dH/dZ1 · dZ1/dW1.
- **Valutazione (primo tentativo):** **5/10**.

### 2026-07-23 — Cap.05 Quiz V8 (Feynman GD)

- **Ok:** collina di notte, passi per sentire su/giù; niente jargon vietato.
- **Manca:** dopo aver capito dove scende → **un passetto lì** e **ripeti**; passi troppo lunghi/corti (inciampi vs ci metti una vita).
- **Valutazione (primo tentativo):** **7/10**.

---

## Lacune e dubbi ancora aperti

- Catena verso **W1**: non inserire W2 come “anello”; dopo Z2 vai a **H → Z1 → W1**.

### 2026-07-27 — Cap.05 Mini-progetto `confronto_lr_su_addestramento`

- **Core:** 4 subplot + PNG ok; train da w=b=0; lr 0.5 stabile con acc=1; lr 2.0 oscilla (visibile).
- **Gap commenti:** “troppo cauto” indicato 0.1 invece di **0.01**; Q4 vaga (“plusibili”); report console non stampato (`verbose=False`); soglia loss&lt;0.1 → tutte barre a 100 (nessun lr sotto 0.1 in 100 step).
- **Valutazione (primo tentativo):** **8/10**.
- **Post-fix:** rinominata trainer; `verbose=True`; nota barre tutte a 100. Commenti 3–4 ancora errati/vaghi (cauto=0.01; plausibilità con `-b/w`). **8.5/10**.

---

### 2026-07-27 — Chiusura capitolo 05 (sintesi)

- **Media valutazioni capitolo:** ~**8.6/10** (primi tentativi). Punte: V2, V5 10/10; refactoring `gd_bello_1d` 10/10 post-fix; PIPE/TODO 16 9.5/10.
- **Punti bassi:** **V7 5/10** (catena `dL/dW1` passata da W2 → lacuna #39), **V8 7/10** (Feynman senza il ciclo iterativo → lacuna #40), mini-progetto 8/10 sui commenti.
- **Pattern nuovo #27** (traduzione formula → codice): `/` per `*`, `*` per `@`, `==` per `=`, parentesi mancanti. Concetto sempre corretto, trascrizione no.
- **Chiusi:** lacune #33 (vanishing, Q1), #34 (clip bilaterale, TODO 8), #35 (ordine `bce_loss`, TODO 8). #36 (`p-y`) rinforzato con R1–R6, verifica finale al quiz ingresso cap.06.
- **Non svolti (opzionali, non bloccanti):** mini 1.2.A, R6 punto B, TODO 17 REAL-WORLD, checkpoint C1–C5.
- **Artefatti:** `figures/05_01_gd_1d.png`, `05_02_lr_confronto.png`, `05_03_gd_2d.png`, `05_06_confronto_lr.png`.

---

## Note per il capitolo successivo (cap.06 backprop_training)

- **Bridge obbligatorio prima:** `quiz_ripasso_tra_capitoli/M03_R05_after_C05_before_C06_chain_to_backprop.md` — popolato il 27/07/2026 con **11 esercizi** (chain rule numerica, direzione GD, lr, ReLU@0, `dL/dp` vs `dL/dz`, catena W1, shape, regola shape gradiente, sanity check, NumPy, Feynman).
- **Rinforzi 🔁 inseriti in `06_backprop_training.py`:**
  - `dL/dp` vs `dL/dz` (#38) — blocco pre-SEZIONE 1, analogia del termostato + 2 micro-esercizi.
  - Catena verso W1 (#39) — blocco pre-SEZIONE 1, analogia dei due affluenti + 2 micro-esercizi.
  - `derivata_relu` in z=0 (#37) — sez. 2.4, analogia valvola di non ritorno + previsione output.
  - Pattern #27 formula → codice — sez. 3, tre regole di lettura + quiz sulle shape.
  - Feynman come ciclo (#40) — sez. 4, prima del training loop.
- **Attenzione al ritmo:** il cap.06 è il più lungo del modulo (~19 TODO + pipeline + mini-progetto reale + CONFRONTO PRIMA/DOPO). Pianificare **2–3 sessioni**: (1) sez.1–2 backward step-by-step, (2) sez.3–4 sanity check + training loop, (3) mini-progetto su CSV M2 + chiusura primo blocco M3.
- **Da chiedere all'apertura:** il **voto difficoltà del cap.05** se non ancora dato.
