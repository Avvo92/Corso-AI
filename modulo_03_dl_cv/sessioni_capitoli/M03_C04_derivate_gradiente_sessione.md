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

## Lacune e dubbi ancora aperti

- _(da popolare quando il capitolo verra' aperto)_

---

## Note per il capitolo successivo (cap.05 chain rule + gd)

- _(da popolare a chiusura del cap.04)_
