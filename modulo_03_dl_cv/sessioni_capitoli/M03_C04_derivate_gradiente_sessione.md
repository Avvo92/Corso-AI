# Diario sessione — Capitolo 04 — Derivate e Gradiente

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `04_derivate_gradiente.py` (segnaposto al 27/05/2026) |
| **File diario** | `M03_C04_derivate_gradiente_sessione.md` |
| **Stato** | **in corso** — bridge `M03_R03` completato 29/05/2026; prossimo quiz ingresso Q1–Q6 |
| **Voto difficoltà** | — / X/10 (atteso 6-7/10 dopo split) |

---

## ⚠️ Note sullo split (27/05/2026)

Le valutazioni di alcuni esercizi qui sotto sono state migrate dal vecchio diario `M03_C03_backpropagation_sessione.md` (capitolo monolitico, poi splittato in 4). Sono i TODO che riguardavano la sezione DERIVATA del vecchio file (Sez.2 originale).

---

## Obiettivi del capitolo (per il mentor — da affinare a chiusura cap.03)

- Far interiorizzare **derivata = pendenza** in codice, grafico, parole (NIENTE limiti formali).
- Introdurre il **gradiente come "lista di derivate parziali"** (= vettore).
- Mostrare la **derivata della sigmoid** `s(z) * (1 - s(z))` e farne capire il massimo (0.25) come anticipazione del vanishing gradient.
- Inserire rinforzi cap.01-02 (vettori come liste di coordinate, ReLU come step function).

---

## Strategia didattica (da affinare)

- Sequenza per OGNI concetto matematico: **analogia concreta -> codice Python -> grafico -> formula in parole**.
- Niente LaTeX.
- Se il cap.03 LOSS ha lasciato lacune aperte (segno BCE, clip, soglia), inserire blocchi `🔁 RINFORZO MIRATO` qui.

---

## Domande durante lo studio

- _(da popolare quando il capitolo verra' aperto)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Voto = "primo tentativo".

### 2026-05-29 — Quiz ingresso Q1 (`04_derivate_gradiente.py` — BCE + loss vs accuracy)

- **Domanda:** Cos'è la BCE in 1 riga? Perché minimizziamo la loss e non l'accuracy?
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** BCE = loss per **classificazione binaria**; intuizione **log/esponenziale** — errori gravi (p lontano da y) costano molto più di errori lievi; contrasto utile con accuracy “solo conta sbagliato/sì”.
- **Cosa manca (2ª metà domanda):** il motivo **operativo per il training** — l'accuracy è **discreta** (soglia 0.5: piccoli spostamenti di p non cambiano nulla) e **non differenziabile** → niente gradiente/retropropagazione; la loss è **continua** e guida i pesi.
- **Modello 1 riga aggiuntiva:** “Addestriamo sulla loss perché è continua e differenziabile; l'accuracy è solo una metrica di valutazione.”

### 2026-05-29 — Quiz ingresso Q2 (`04_derivate_gradiente.py` — clip bilaterale BCE)

- **Domanda:** Perché `(eps, 1-eps)`? Cosa succede senza il lato destro?
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** Risposta mirata alla domanda: senza `1-eps` può restare **`p=1`** → **`log(1-p)`** → NaN/inf; idea “proteggere gli estremi” ok.
- **Affinamento opzionale:** precisare termine `(1-y)*log(1-p)`; con solo `(eps, 1)` il lato **basso** è già ok, il guaio tipico è l’**alto** (`p→1`).

### 2026-05-29 — Quiz ingresso Q3 (`04_derivate_gradiente.py` — dense + forward 2-layer)

- **Domanda:** Cos'è un layer dense? Forward rete 2-layer in NumPy (1 riga ciascuno).
- **Valutazione (primo tentativo):** **6/10**.
- **Punti di forza:** Hidden + ReLU, output + sigmoid/probabilità — architettura concettuale ok (allineato bridge es.8).
- **Errori / lacune:** (1) **Dense** = trasformazione lineare **`Z = X @ W + b`** con **tutti** gli input collegati a **tutti** gli output (fully connected), non “un peso per elemento”; (2) forward senza operazioni NumPy richieste (`@`, bias, sequenza `Z1→H→Z2→P`); (3) “ogni elemento connesso a un peso specifico” è impreciso.
- **Modello compatto:** Dense: `X @ W + b`. Forward: `Z1=X@W1+b1; H=relu(Z1); Z2=H@W2+b2; P=sigmoid(Z2).ravel()`.

**Rivalutazione post-fix (2026-05-29):** dense = fully connected (tutti input → tutti neuroni); forward con `@`, bias, ReLU, sigmoid; riga operativa `Z1→H→Z2→P` corretta. **Post-fix: 9/10** (opzionale: `.ravel()` se output scalare per batch).

### 2026-05-29 — Quiz ingresso Q4 (`04_derivate_gradiente.py` — pendenza x² in x=2)

- **Domanda:** `f(x)=x²`, da x=2 a x=2.001: sale/scende? Di quanto circa?
- **Valutazione (primo tentativo):** **10/10**.
- **Punti di forza:** **Sale** (pendenza positiva a x=2); Δf ≈ **0.004** (`2.001² - 4 = 0.004001`); coincide con stima `f'(2)=4` × Δx=0.001 → 0.004 (anticipa sez.1 derivata).

### 2026-05-29 — Quiz ingresso Q5 (`04_derivate_gradiente.py` — Feynman pendenza)

- **Domanda:** 3 righe, senza derivata/limiti; analogia web dev suggerita.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** Nucleo corretto (Δaltezza / piccolo spostamento orizzontale); vincolo lessicale rispettato; coerente con bridge es.10.
- **Lacune:** (1) **1 riga** invece di 3; (2) nessuna analogia **web** (CPU, load time, metriche nel tempo); (3) “valore di partenza” ambiguo → meglio “asse x / tempo / passo a destra sul grafico”.
- **Modello:** “Sul grafico load time vs utenti: ogni +1 utente fa salire il tempo di X ms — quella X è la pendenza in quel punto.”

**Rivalutazione post-fix (2026-05-29):** esplicitati **asse y** (altezza) e **asse x** (spostamento); seconda frase chiarisce “quanto sali/scendi” per piccolo passo. **Post-fix: 8.5/10** (opzionale: analogia web dev CPU/load time per 9.5; typo “sull’asse y”).

### 2026-05-29 — Quiz ingresso Q6 (`04_derivate_gradiente.py` — prevedi output derivata numerica)

- **Domanda:** Output di `(f(2+h)-f(2-h))/(2h)` con `f(x)=x³`, `h=1e-6`, `round(..., 1)`.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** Risposta finale **`12.0`** corretta; formula **differenza centrale** ok; collegamento analitico `3x²` in x=2 → 12.
- **Errore numerico nel calcolo mostrato:** valori `8.012…` / `7.988…` e denominatore `0.002` corrispondono a **`h=0.001`**, non a `h=1e-6` (con `1e-6` il numeratore è ~`2.4e-5`, non `0.024`). Il risultato resta 12 per coincidenza con la derivata esatta.
- **Modello:** `print(round(deriv_approx, 1))` → **`12.0`**.

### 2026-05-29 — Mini-esercizio 1.1.A (`04_derivate_gradiente.py` — derivata_numerica su x²)

- **Esercizio:** `derivata_numerica(f, x)` con `f(x)=x²` in x=3, -3, 0 (attesi ~6, ~-6, ~0).
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** `f` corretta; tre punti richiesti; usa `derivata_numerica` come da consegna; output numerico ~6, ~-6, 0 (verificato); notazione `f'(x)` nei print ok.
- **Affinamento opzionale:** `round(..., 1)` o confronto con analitica `2*x` per sanity check esplicito.

### 2026-05-29 — Mini-esercizio 1.1.B (`04_derivate_gradiente.py` — pendenza retta y=3x+1)

- **Esercizio:** `derivata_numerica` in x=0, 5, -10; tutti attesi 3.0.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** `f_y = 3x+1` ok; tre punti richiesti; `assert np.all(np.isclose(arr, 3.0))` — verifica esplicita “tutti uguali al target” (pattern appena visto); concetto pendenza costante chiaro.
- **Affinamento opzionale:** evita doppia chiamata `derivata_numerica` (salvi in `der_*` ma nel `print` ricalcoli); loop su `[0,5,-10]` più DRY; label nel print (`x=…`).

### 2026-05-29 — Mini-esercizio 1.2.A (`04_derivate_gradiente.py` — numerica vs analitica ×3 funzioni)

- **Esercizio:** x³→3x², sin→cos, exp→exp in 3 punti; `np.isclose(..., atol=1e-4)`.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** Tre funzioni con formule analitiche corrette; `np.sin(x)` in **radianti** (no deg2rad); `np.isclose` + `ValueError` se fallisce; loop su `[-3,0,3]` → 9 confronti; esecuzione verificata (tutti passano).
- **Affinamento opzionale:** etichette print (`cubo/seno/exp`); a x=0 su x³ numerico ~1e-12 vs 0 (ok con atol); stile print uniforme (`print(f_cubo(a))` come gli altri).

### 2026-05-29 — Mini-esercizio 1.3.A (`04_derivate_gradiente.py` — grafico tangenti + exists)

- **Esercizio:** `_grafico_funzione_e_tangenti(out_path="figures/04_01_tangenti.png")` + verifica file creato.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** Chiamata con `out_path` corretto; `assert os.path.exists(...)` con path ancorato a `__file__` (più robusto del solo path relativo); messaggio errore chiaro; PNG presente in `modulo_03_dl_cv/figures/`.
- **Affinamento opzionale:** se esegui lo script dalla root repo, allinea `out_path` allo stesso base di `__file__` (es. `Path(__file__).parent / "figures" / ...`) per evitare salvataggi in cartelle diverse.

### 2026-05-29 — Mini-esercizio 1.3.B (`04_derivate_gradiente.py` — interpreta grafico tangenti)

- **Domanda:** (1) pendenza nulla? (2) trick: da lì come far **scendere** f?
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** (1) **x=0** corretto (fondo, m=0, tangente orizzontale); (2) capisce il trick — **non si può** abbassare ulteriormente f (x² ≥ 0); spostarsi da 0 fa **risalire** f.
- **Affinamento:** la trick è simmetrica: sia **sinistra** sia **destra** di 0 f **sale** (non solo “valori negativi di x”); nessuna direzione sul grafico abbassa f — sei al **minimo globale**.

### 2026-05-29 — Rinforzo sez.2 (`04_derivate_gradiente.py` — vanishing gradient, commento)

- **Domande:** (1) stima `0.25³` dopo 3 layer sigmoid; (2) perché ReLU non ha tetto 0.25.
- **Valutazione (primo tentativo):** **6.5/10** (solo Q2 risposta; Q1 assente).
- **Q1:** manca — atteso **0.25³ ≈ 0.0156** (~1.6% del segnale di gradiente vs layer ideale).
- **Q2 (7.5/10 sul pezzo):** ReLU non satura come sigmoid; valori >0 passano; sigmoid agli estremi “schiaccia” attivazioni — intuizione ok.
- **Cosa aggiungere:** ReLU in z>0 ha derivata **1** (non max 0.25); il gradiente non viene moltiplicato ripetutamente per ≤0.25 a ogni layer; saturazione sigmoid → derivata piccola → **vanishing gradient**.

### 2026-05-29 — Mini-esercizio 2.1.A (`04_derivate_gradiente.py` — sigmoid vs derivata)

- **Esercizio:** numerica vs analitica su z∈{-3,-1,0,1,3}; quale z dà derivata max?
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** Loop su 5 z; `derivata_numerica(sigmoid, z, h=1e-6)` + `derivata_sigmoid(z)`; `assert isclose` atol=1e-6; stampa num/ana; max corretto **z=0 → 0.25** via `max(report.items(), key=...)`.
- **Affinamento opzionale:** `max_z` è stringa (`"0"`) — ok per print; alternativa `max(logits, key=derivata_sigmoid)` senza dict intermedio.

### 2026-05-29 — Mini-esercizio 2.1.B (`04_derivate_gradiente.py` — max s'(z) con argmax)

- **Esercizio:** `linspace`, `der.max()` ~0.25, `zz[argmax(der)]` ~0; grafico opzionale.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** `zz` 1000 punti; `derivata_sigmoid(zz)`; stampa max + z con `np.argmax` (verificato ~0.25 @ ~0); bonus grafico der+sig.
- **Affinamento:** su stesso assi y, sigmoid (0–1) e derivata (0–0.25) scale diverse — etichetta seconda curva o `twinx`; `der.max()`/`der.argmax()` equivalenti a `np.max/np.argmax`; `plt.close()` senza save opzionale se non serve file.

### 2026-05-29 — Mini-esercizio 2.2.A (`04_derivate_gradiente.py` — 0.25⁵ vanishing)

- **Esercizio:** stima `0.25 ** 5`; cosa noti; perché ReLU interno.
- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** Calcolo **`0.25**5` corretto (~**0.00098**, 1/1024); stampa chiara.
- **Commento debole:** “> 1e-4” è vero ma non è il messaggio — il gradiente è **~1000× più piccolo** (~0.1% del segnale); training lentissimo → ReLU in hidden; typo *vaniscing* → *vanishing*.

### 2026-05-29 — Mini-esercizio 3.2.A (`04_derivate_gradiente.py` — dying ReLU)

- **Esercizio:** Z con b molto negativo; quanti Z>0? quanti derivata_relu==1?
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** X,W ok; `b=-np.max(X@W)-1` garantisce tutti Z<0 (Z=[-1.6,-1]); H=0; `derivata_relu` tutti 0; commento conclusione corretto.
- **Affinamento:** rispondere esplicitamente con `(Z>0).sum()` e `(der_relu==1).sum()`; stampare H; `np.array` su `X@W` ridondante.

### 2026-06-05 — Mini-esercizio 4.1.A (`04_derivate_gradiente.py` — gradiente numerico vs analitico)

- **Esercizio:** 3 funzioni, gradiente numerico + analitico, stampa confronto.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** `f_1/f_2/f_3` corrette; `dtype=float` (fix int→float); analitici `[2x,2y]`, `[y,x]`, `[2x,4y,6z]`; punti e attesi ok; esecuzione verificata (allclose num/ana e attesi).
- **Affinamento:** aggiungere `assert np.allclose(..., atol=1e-4)` per ogni coppia; etichette print (`num`/`ana`); opz. messaggio OK per funzione.

### 2026-06-05 — Mini-esercizio 4.2.A (`04_derivate_gradiente.py` — campo gradienti PNG)

- **Esercizio:** `_grafico_campo_gradiente(out_path=...)` + verifica file.
- **Valutazione (primo tentativo):** **9.5/10**.
- **Punti di forza:** Chiamata con path corretto; `assert exists` ancorato a `__file__` (robusto); messaggio errore chiaro; pattern allineato a 1.3.A.

### 2026-06-05 — Mini-esercizio 4.3.A (`04_derivate_gradiente.py` — parziali a mano + gradiente)

- **Esercizio:** `f=x²y+3y+2`; df/dx, df/dy a mano; verifica in (1,2) atteso [4,4].
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** Calcolo manuale differenza centrata → 4 e 4; `f(v)` corretta; `dtype=float`; `gradiente_numerico` + `allclose` con [4,4]; esecuzione verificata.
- **Affinamento:** aggiungere in commento formule simboliche `df/dx=2xy`, `df/dy=x²+3`; confrontare con `grad_ana` calcolato da `v` invece di letterale fisso; evitare nome generico `f` se possibile.

### 2026-06-05 — Mini-esercizio 4.3.B (`04_derivate_gradiente.py` — gradiente in R³)

- **Domanda:** 2 righe — perché gradiente di f(x,y,z) è vettore di 3 numeri (vive in R³).
- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** Gradiente = lista di **derivate parziali** (una per variabile); ogni componente = effetto di muovere **solo** quella coordinata; idea pendenza/incidenza ok.
- **Affinamento:** esplicitare **3 variabili → 3 componenti → R³**; più conciso (2 righe); typo *variabili*; “parametro” → *variabile/input*.

### 2026-06-05 — Rinforzo sez.5 intro (`04_derivate_gradiente.py` — clip BCE + ordine)

- **Esercizio:** (1) clip `(eps,1)` → inf? (2) clip bilaterale finito? (3) `bce_loss(p,y)==bce_loss(y,p)` → False.
- **Valutazione (primo tentativo):** **8.5/10**.
- **Punti di forza:** `p=[0,1]`, `y=[1,0]`; confronto `p_no_safe` vs `p_safe`; `bce_no_safe` con **inf** su p=1,y=0; `bce_safe` finito; commento limite destro ok; assert False sull’ordine.
- **Affinamento:** Q1–Q2 rispondere esplicitamente (inf vs finito); test ordine come da consegna `bce_loss(p,y) vs bce_loss(y,p)` (non `p_safe`); `bce_loss` ritorna **media** — confronto per-elemento vs funzione capitolo; lacuna #35 ancora da consolidare in parole.

### 2026-06-05 — Mini-esercizio 5.1.A (`04_derivate_gradiente.py` — derivata BCE rispetto a p)

- **Esercizio:** (p=0.8, y=1); num con `derivata_numerica` su log-BCE; ana `(p-y)/(p(1-p))`; `isclose` atol=1e-4.
- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** `der_ana = (p-y)/(p*(1-p))` corretta → **-1.25**; confronto num/ana ok (verificato); assert `isclose` passa.
- **Affinamento:** consegna chiede **`derivata_numerica(lambda p_var: -y*log(p_var)-...)`** — hai usato differenza manuale su **`bce_loss`** (funziona qui grazie al clip interno, ma non è il metodo richiesto); `eps=1e-4` come passo **e** come `atol` in `isclose` — ok ma confonde con `h` tipico `1e-6`.

### 2026-06-05 — TODO 1 (`04_derivate_gradiente.py` — derivata num vs ana ×4 funzioni)

- **Esercizio:** 4 funzioni, 3 punti, tabella, isclose 1e-4.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** 4 coppie f/f'_ana; loop 3 punti; `derivata_numerica`; DataFrame report; f1, f2, f4 ok su [-2,1,2].
- **Errori / lacune:** `np.isclose` chiamato ma **risultato ignorato** (no assert/colonna ok); variabile **`dict`** shadow builtin; **f3=log(x)** a x=-2: `return 0` fuori dominio → confronto **falso positivo** (ana=0, num≈0); f3 serve **x>0** (es. [0.5,1,2]); colonna `z` ok ma label `x` più chiara.

**Rivalutazione post-fix (2026-06-05):** `arr=[0.5,1,2]` (dominio log ok); **`assert isclose`** su tutte e 4 le funzioni; `row` al posto di `dict`. Esecuzione verificata 12/12 check. **Post-fix: 9/10** (opz.: `f_3` senza ramo `return 0`; punti diversi per f2 se x=0; colonna `x` invece di `z`).

### 2026-06-05 — TODO 2 (`04_derivate_gradiente.py` — grafico sigmoid + derivata)

- **Esercizio:** funzione `_grafico_sigmoid_e_derivata`; plot sigmoid + `derivata_sigmoid`; salva `04_03_sigmoid_derivata.png`; assert exists.
- **Valutazione (primo tentativo):** **7/10**.
- **Punti di forza:** `linspace(-6,6)`; sigmoid plottata; seconda curva rossa; griglia; path con `__file__`; `assert exists`; PNG creato.
- **Errori / lacune:** **manca funzione** `_grafico_sigmoid_e_derivata` (codice inline); usa **`derivata_numerica(sigmoid, arr)`** invece di **`derivata_sigmoid(arr)`** (consegna); `ax.legend()` **senza label** sulle curve; `print(shape)` debug; ylabel solo "Sigmoidi".

**Rivalutazione post-fix (2026-06-05):** funzione `_grafico_sigmoid_derivata` con `derivata_sigmoid(arr)` ✓; griglia/titolo/save/assert interni. **Manca chiamata** alla funzione con path (consegna: "Chiamala"); legend senza `label=`; nome leggermente diverso da `_grafico_sigmoid_e_derivata`. **Post-fix: 8/10**.

### 2026-06-05 — TODO 4 (`04_derivate_gradiente.py` — gradiente su W1_flat rete random)

- **Esercizio:** `f(W1_flat)` reshape+forward+BCE; `gradiente_numerico`; stampa shape e primi 4.
- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** Setup rng/X/y/W2/b ok; `f` con reshape (3,4), forward 2-layer, `bce_loss`; `my_grad_num` corretta (+=/-=); `result.shape==(12,)`, primi 4 stampati; coincide con `gradiente_numerico` del file.
- **Affinamento:** rinomina `W1_flat` → `f` (confonde funzione/vettore); usa `gradiente_numerico` già definita (non reinventare); `W1` come `(3,4)` poi `.ravel()`; `P=sigmoid(Z2).ravel()`; `W1.astype(float)` per sicurezza.

### 2026-06-05 — TODO 5 (`04_derivate_gradiente.py` — derivata BCE su batch)

- **Esercizio:** `dl_dp` analitico + verifica con `gradiente_numerico` su `p`; stampa entrambi i vettori.
- **Valutazione (post-fix):** **9.5/10**.
- **Punti di forza:** Formula `(p-y)/(p(1-p))` corretta; fattore `1/n` per allineamento a `bce_loss` (mean); `f(p_vec)` senza shadowing; `gradiente_numerico(f, p)`; `assert np.allclose(..., atol=1e-8)` con messaggio chiaro; vettori `[-0.37, 0.37, -0.48]` coincidono.
- **Affinamento minore:** opzionale stampare `dl_dp` grezzo (senza `/n`) per confronto didattico per-campione vs media.

### 2026-06-05 — TODO 6 (`04_derivate_gradiente.py` — derivata BCE rispetto a z)

- **Esercizio:** `p=sigmoid(z)`; `dL/dz = p-y` (+ `/n`); verifica con `gradiente_numerico` su `z`.
- **Valutazione:** **9/10**.
- **Punti di forza:** Formula miracolosa `(p-y)/len(p)` corretta (errore TODO 5 formula superato); `f(z_vec)` con `bce_loss(sigmoid(z_vec), y)`; `gradiente_numerico(f, z)`; vettori coincidono `[-0.294, 0.167, -0.040]`.
- **Affinamento:** `z.astype(float)` esplicito; `assert np.allclose(dl_dz, grad)` come TODO 5; stampare `p` opzionale per leggere i gradienti.

### 2026-06-05 — TODO PIPE.1 (`04_derivate_gradiente.py` — derivate_check_completo)

- **Esercizio:** sanity check analitico vs numerico su sigmoid, ReLU, BCE (y=1/y=0); dict max errori; tabella + soglie.
- **Valutazione:** **8.5/10**.
- **Punti di forza:** Loop su `z_val`; max err sigmoid/ReLU/BCE y1/y0; BCE con `derivata_numerica` per campione e y fissi; `np.abs(num - ana)` corretto; dict con 4 chiavi e `float()`; errori ~1e-10, soglie rispettate.
- **Affinamento:** chiamata `derivate_check_completo(n_punti=20)`; step 4 tabella leggibile; step 5 assert soglie (`<1e-3` sigmoid/BCE, `<0.5` ReLU); rinominare `z` → `z_punti`; indentazione lambda.

### 2026-06-05 — TODO 7 (`04_derivate_gradiente.py` — dp/dw chain rule)

- **Esercizio:** `gradiente_numerico` su `w` per `sigmoid(w·x+b)`; ana `derivata_sigmoid(z)*x`; assert.
- **Valutazione:** **9/10**.
- **Punti di forza:** Lambda corretta; `np.array(w, dtype=float)` (0-d, evita array-in-array); formula analitica ok; `assert np.isclose`; valori ~0.375 per z=1.1.
- **Affinamento:** `z = w*x+b` esplicito in ana; `float(grad_num)` in stampa; rimosso codice eps duplicato (se presente).

### 2026-06-05 — TODO 8 (`04_derivate_gradiente.py` — sigmoid/ReLU vettorizzate + derivate)

- **Esercizio:** riscrivere `my_sigmoid`/`my_relu`; applicare a Z; stampare forward e derivate.
- **Valutazione:** **9/10**.
- **Punti di forza:** Sigmoid con clip; ReLU `np.maximum`; forward corretti su Z; derivata sigmoid `p*(1-p)`; derivata ReLU; output allineati al riferimento.
- **Affinamento:** ReLU derivata idiomatica `(Z > 0)` invece di `(h > 0)` (equivalente ma più chiaro); opzionale funzioni `my_derivata_*` dedicate.

### 2026-06-05 — TODO 9 (`04_derivate_gradiente.py` — my_bce_loss da zero)

- **Esercizio:** riscrivere BCE vettorizzata; confronto con `bce_loss` del file.
- **Valutazione:** **9.5/10**.
- **Punti di forza:** Formula `-y*log(p)-(1-y)*log(1-p)`; clip `eps`/`1-eps`; `mean()`; ordine `(p, y)` corretto; `dtype=float`; `assert np.allclose`; coincide con riferimento.
- **Affinamento:** nome `my_bce` come in consegna (cosmetico); `np.asarray(p/y, dtype=float)` dentro la funzione per robustezza.

### 2026-06-05 — TODO 10 (`04_derivate_gradiente.py` — gradiente loss rispetto a b2)

- **Esercizio:** forward 2-layer; `gradiente_numerico` su `b2`; bonus linearità `Δloss ≈ grad×eps`.
- **Valutazione:** **9/10**.
- **Punti di forza:** Setup TODO 4; forward+`bce_loss` in wrapper; `grad_b2≈0.100`; bonus corretto (`delta≈0.00101` vs `grad×0.01≈0.00100`); `float(grad[0])`; `np.array(b2)` per evitare bug shape.
- **Affinamento:** `assert np.isclose(delta, prova_del_nove, atol=1e-4)`; rinominare `W1_flat`→`loss_rispetto_b2`; stampare `bce_loss_1` come loss step 3.

### 2026-06-05 — TODO 11 (`04_derivate_gradiente.py` — colloquio)

- **Esercizio:** 5 risposte brevi su derivata, gradiente, sigmoid', vanishing, p-y.
- **Valutazione:** **7/10**.
- **Per punto:** (1) ~5 — confonde derivata con "cambio della pendenza" (serve f(x), non pendenza della pendenza); (2) ~8.5 — gradiente/manopole ok; (3) ~9 — 0.25 e massimo corretti; (4) ~6 — idea saturazione ok, manca mitigazione (ReLU, init, ecc.); (5) ~5 — solo nome "semplificazione", serve chain rule in una riga.
- **Pattern:** rafforzare definizione derivata (pendenza / Δf per Δx); V7 meccanismo cancellazione p(1-p).

### 2026-06-05 — TODO 12 (`04_derivate_gradiente.py` — refactor derivata_numerica)

- **Esercizio:** `derivata_bella` (centrata, hint, h default); confronto con `derivata_brutta` su x³ in x=2.
- **Valutazione (post-fix `x`):** **7.5/10**.
- **Punti di forza:** `derivata_bella` corretta; `x=2` fixato; run ok; bella ≈12 vs analitica 12.
- **Errori residui:** `derivata_brutta(..., h=1e-16)` → `(0.0,)` (instabilità); confronto non esplicito (manca analitica/assert); brutta stampata come tuple; usare `h=1e-6` per confronto fair.

### 2026-06-05 — TODO 13 (`04_derivate_gradiente.py` — debug derivata sigmoid)

- **Esercizio:** trovare bug `s*(1+s)`; spiegazione; confronto num vs buggata vs corretta.
- **Valutazione (post-fix delta):** **8.5/10**.
- **Punti di forza:** Bug `1+s`→`1-s` identificato; loop+tabella; `delta=|ana_cor-ana_bug|`; run ok; num≈ana_cor; z=0 mostra errore 0.5 (0.75 vs 0.25).
- **Affinamento:** fix esplicito nel corpo funzione (non solo commento); colonna `|ana_cor-num|`; nota su z=0.

### 2026-06-05 — TODO 14 (`04_derivate_gradiente.py` — retrieval rete_2_layer)

- **Esercizio:** riscrivere forward 2-layer; verify `P.shape == (5,)`.
- **Valutazione:** **9/10**.
- **Punti di forza:** Forward Z1→ReLU→Z2→sigmoid→ravel corretto; setup shape ok; He init coerente; `b1`/`b2` ok; `assert P.shape == (X.shape[0],)`; esecuzione ok.
- **Affinamento:** nome `rete_2_layer` come consegna; type hint `b2: NDArray` non `float`; docstring; He opzionale (consegna bastava `*0.1`).

### 2026-06-05 — TODO 15 (`04_derivate_gradiente.py` — gradiente neurone w,x,b)

- **Esercizio:** neurone scalare; `gradiente_numerico` su dy/dw, dy/db, dy/dx; osservazioni chain rule.
- **Valutazione:** **8.5/10**.
- **Punti di forza:** Formule analitiche s'*w, s'*x, s' corrette; 3 wrapper gradiente_numerico; stampa ana/num; commento su b; valori coincidono.
- **Affinamento:** `b=0.1` consegna; ordine `(w,x,b)`; `assert np.isclose`; commento esplicito dy/dw dipende da x (formula ×x), dy/db no; `float(x_arr)` nelle lambda.

### 2026-05-25 — TODO 2.1 derivata sigmoid numerica vs analitica (`04_derivate_gradiente.py` ~TODO sigmoid)

> ⚠️ MIGRATA dal vecchio `03_backpropagation.py` (Sez.2 monolitico).

- **Esercizio / blocco:** TODO 2.1 — confronto derivata sigmoid (funzioni proprie). Riferimento storico: vecchio `03_backpropagation.py` righe ~608-639.
- **Valutazione (primo tentativo post-fix — "voto esame"):** **9/10**.
- **Punti di forza:** Formula numerica corretta (`/ 2h`); analitica `s*(1-s)` corretta; tutti i 5 punti z coincidono (es. z=0 → 0.25); `assert np.isclose` ottimo; `h=1e-6` passato esplicitamente.
- **Errori / lacune:** (1) type hint `Callable[[float, float]]` → dovrebbe essere `Callable[[float], float]`; (2) default `h=1e-12` in firma ma usa 1e-6 in chiamata — allineare; (3) `sigmoid` chiamata 2 volte nell'analitica (minore).
- **Correzione / suggerimento:** `s = sigmoid(z_safe); return s * (1 - s)` — una sola chiamata.
- **Pattern errore / ID contesto:** — (primo TODO derivate OK dopo fix divisione/precedenza).

---

### 2026-05-27 — TODO 2.3 grafico funzione+derivata (`04_derivate_gradiente.py` ~TODO grafico)

> ⚠️ MIGRATA dal vecchio `03_backpropagation.py` (Sez.2 monolitico).

- **Esercizio / blocco:** Generare PNG `figures/03_02_derivata.png` e (richiesto) verificare esistenza file. Riferimento storico: vecchio `03_backpropagation.py` righe ~651-672.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** `os.makedirs(...)` presente; plot creato con `fig, ax`; `plt.savefig(out_path, ...)` salva correttamente (file effettivamente presente).
- **Errori / lacune:** non implementa la parte richiesta di "verifica esistenza file" (`os.path.exists` + print/flag); inoltre salva con `plt.savefig` invece di `fig.savefig` (minore, ma più pulito).
- **Correzione / suggerimento:** dopo `savefig`, fai `exists = os.path.exists(out_path)` e stampa/`assert exists`.
- **Pattern errore / ID contesto:** ⚠️ "consegna salva ma manca exists check". Rinforzato in TODO 1.3 del nuovo `03_loss.py` (ora corretto con `assert file_created`).

---

### 2026-06-05 — Quiz verifica V8 (`04_derivate_gradiente.py` — Feynman vanishing gradient)

- **Esercizio:** 4 righe a un web dev; vietati: derivata, gradiente, layer, vanishing, chain.
- **Valutazione (primo tentativo):** **5.5/10**.
- **Punti di forza:** Analogia amplificatore + molte manopole = buona direzione (tanti stadi in serie); capisce che gli aggiustamenti diventano “irrilevanti”.
- **Errori / lacune:** (1) **Vincolo violato** — scrive “vaniscing gradient” (parole proibite + typo già segnalato in 2.2.A); (2) **2 righe**, non 4; (3) manca il **perché** (ogni stadio passa solo una frazione piccola del segnale, tipo manopola al minimo/massimo); (4) manca la **conseguenza** (le prime manopole quasi non si muovono → la rete impara lentissimo); (5) niente accenno alla **mitigazione** (manopole che non saturano, es. ReLU in mezzo).
- **Pattern:** lacuna #27 Feynman — vincoli lessicali; ripetizione typo *vaniscing*.
- **Per 8/10:** riscrivi 4 righe senza parole vietate; aggiungi “in fila” + “frazione piccola a ogni stadio” + “prima manopola non risponde”.

---

### 2026-06-16 — Mini-progetto `analizza_funzione_attivazione` (`04_derivate_gradiente.py`)

- **Esercizio:** scorecard sigmoid/relu/tanh + tabella + 3 righe commento.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** `linspace`+`der`; `f'_max`/`f'_max_z` con `argmax` corretto; `f'_mean`; `sat_sx`/`sat_dx`; 3 chiamate + lambda tanh; `pd.DataFrame(report)` ok; run exit 0; commenti finali sensati (ReLU migliore, sigmoid/tanh saturano, ReLU in hidden).
- **Errori / lacune:** (1) manca chiave **`sanity_check_ok`** nel dict (PASSO 3); (2) sanity fatto con `derivata_numerica(f, zz[100:105])` — API è per **uno** `z` float, non slice (funziona per broadcasting ma non è il pattern richiesto); (3) `assert` interno al posto di loop su 5 z fissi `[-2,-1,0,1,2]`; (4) nomi chiavi rinominate (`f(0)` vs `f_in_z=0`) — ok per tabella ma non allineate alla consegna; (5) `f'_max_z` ≈ ±0.03 non 0 — griglia 200 punti non passa esattamente da z=0 (non errore concettuale); (6) typo *vaniscing* nel commento.
- **Per 9/10:** aggiungi `sanity_check_ok` con loop scalare; opzionale colonna `ok` in tabella; `z_range` default `(-6,6)` in firma.

### 2026-06-16 — Mini-progetto `analizza_funzione_attivazione` — post-fix sanity_check

- **Fix:** aggiunta chiave `sanity_check` nel dict + colonna in tabella; tutte True su sigmoid/relu/tanh; run exit 0.
- **Valutazione post-feedback:** **8/10** (voto esame resta **7.5/10** primo tentativo).
- **Migliorato:** scorecard completo con verifica esposta in output.
- **Residui:** ancora `derivata_numerica(f, zz[100:105])` invece di loop su 5 z scalari `[-2,-1,0,1,2]`; chiave `sanity_check` vs `sanity_check_ok`; typo *vaniscing* nel commento PASSO 6.

### 2026-06-16 — Checkpoint C1 (`04_derivate_gradiente.py` — derivata vs gradiente)

- **Esercizio:** 1 frase su derivata 1D e gradiente nD.
- **Valutazione (primo tentativo):** **9/10**.
- **Punti di forza:** Derivata = pendenza in x corretta; gradiente = vettore di derivate parziali; intuizione “sposti un parametro, gli altri fermi” operativa e chiara. Miglioramento netto vs TODO 11 colloquio (dove confondeva derivata con “pendenza della pendenza”).
- **Affinamento opzionale:** aggiungere che il gradiente indica la direzione di salita più ripida della loss (bussola sulla collina).

### 2026-06-16 — Checkpoint C2 (`04_derivate_gradiente.py` — sigmoid 0.25 e layer impilati)

- **Esercizio:** 2 righe — perché 0.25 in z=0 è problema con tanti layer sigmoid.
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** Formula sigmoid' citata; calcolo 0.5×0.5=0.25 corretto; intuizione vanishing (gradiente diventa insignificante); collegamento “schiaccia tra 0 e 1”.
- **Errori / lacune:** (1) formula senza parentesi `s*(1-s)` scritta come `s*1-s` (priorità operatori sbagliata); (2) manca il meccanismo chiave del capitolo: **a ogni layer** il segnale viene moltiplicato per ≤0.25 → dopo n layer ~0.25^n (es. 5 layer ≈ 0.001); (3) typo *inifluente*; (4) “schiaccia valori” è vero ma secondario rispetto alla moltiplicazione ripetuta delle derivate.
- **Per 9/10:** una riga con 0.25^n + ReLU in hidden come mitigazione.

### 2026-06-16 — Checkpoint C3 (`04_derivate_gradiente.py` — BCE+sigmoid z=0, y=1)

- **Esercizio:** prevedi `dL/dz` e `dL/dp` per (z=0, y=1).
- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** `dL/dz = p - y = -0.5` corretto; chain rule scritta con cancellazione `p(1-p)`; calcolo numerico `-0.5/0.25 * 0.25 = -0.5` coerente.
- **Errori / lacune:** (1) **`dL/dp` non chiuso** — `-0.5/0.25 = -2` (manca il valore finale esplicito); (2) risposta mescola le due derivate in un unico calcolo invece di due righe separate come chiede C3; (3) risposta parzialmente nella riga consegna (1882–1883) oltre che in TUA RISPOSTA.
- **Per 9/10:** `dL/dz = -0.5` (semplificazione) e `dL/dp = -2` (formula su p) in due righe distinte.

---

## Lacune e dubbi ancora aperti

- _(da popolare quando il capitolo verra' aperto)_

---

## Note per il capitolo successivo (cap.05 chain rule + gd)

- _(da popolare a chiusura del cap.04)_
