# Diario sessione — Capitolo 05 — Chain Rule + Gradient Descent

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `05_chain_rule_gd.py` (segnaposto al 27/05/2026) |
| **File diario** | `M03_C05_chain_rule_gd_sessione.md` |
| **Stato** | da aprire — bridge **M03_R04** poi cap.05 |
| **Voto difficoltà** | — / X/10 (atteso 7–8/10) |

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

---

## Lacune e dubbi ancora aperti

- _(da popolare)_

---

## Note per il capitolo successivo (cap.06 backprop_training)

- _(da popolare a chiusura del cap.05 — questo bridge e' il piu' delicato perche' il cap.06 e' il pezzo piu' tosto)_
