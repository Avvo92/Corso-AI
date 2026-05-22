# Diario sessione — Capitolo 02 — Reti neurali da zero

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `02_reti_neurali.py` |
| **File diario** | `M03_C02_reti_neurali_sessione.md` |
| **Stato** | ✅ completato (21/05/2026) |
| **Voto difficoltà** | **8**/10 (confermato studente in chiusura) |

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

### [2026-05-19] — `02_reti_neurali.py` — TODO 3.1 (accuracy rete random vs `h` su CSV)

- **Esercizio / blocco:** Sezione 3, TODO 3.1 (~righe 759–797).
- **Valutazione (primo tentativo — "voto esame"):** **8/10**.
- **Punti di forza:** **`carica_pratiche`** + **`StandardScaler`** + **`rete_2_layer` su `X_scaled`** allineati all’`_esempio_rete_2_layer_su_csv`; **LR su `X_scaled`** (fit + soglia da `predict_proba`); loop su **`h ∈ {4,8,16,32,64,128}`**; **`init_pesi_he`** per **`W1,W2`**; **`accuracy_score`** sulla rete random con soglia **0.5**. Commento: osservazione che **`h`** non struttura l’accuracy (nessuna “cura” sul numero di neuroni senza training) è pertinente.
- **Errori / lacune:** **`acc_clf`** calcolato ma **mai usato/stampato** (rumore computazionale: **`fit`** LR ripetuto 6× identico sullo stesso dato — ok ma inutile se non parte del confronto). Stampa **`acc_rete` senza `h`** rende illeggibile il log a colpo d’occhio. Punto (**c**) chiedeva esplicitamente **vicinanza a ~0.5**: il commento non lo nominalizza (solo “randomico / correlazione con h”): aggiungere **«~0.5 come indovinare a caso su classificazione binaria bilanciata / rete senza allenamento»**.
- **Correzione / suggerimento:** `print(h, acc_rete)` o f-string unica; eventualmente **`seed` diversi per layer** come nell’esempio del capitolo (`42`,`43`) o parametro fisso **`random_state`**; una riga su **~0.5**.
- **Pattern errore / ID contesto** (se applicabile): —

### [2026-05-19] — POST-FEEDBACK — TODO 3.1 (`02_reti_neurali.py`)

- **Fix applicato:** rimosso/commentato blocco LR non richiesto per (b)(c); stampa con **`h`** esplicito; commento aggiornato con **vicinanza a ~0.5** e analogia **moneta / caso**.
- **Valutazione qualità attuale:** **~9.5–10/10**. Il **primo tentativo** storico resta **8/10**. Micro-opzionale: formattare **`acc_rete`** con **`:.4f`**; evitare `fit_transform`/`carica_pratiche` dentro la funzione a ogni `h` (spostare fuori dal loop una volta).

### [2026-05-21] — `02_reti_neurali.py` — TODO 3.2 (grafico ReLU, 5 neuroni)

- **Esercizio / blocco:** Sezione 3, TODO 3.2 (~righe 843–879).
- **Valutazione (primo tentativo — "voto esame"):** **7/10** (nucleo matematico **~9/10**, aderenza consegna/portfolio **~5/10**).
- **Punti di forza:** Pipeline corretta: `x_grid (200,1)`, `W1 (1,5)`, `b1 (5,)`, `z = x_grid @ W1 + b1` → `(200,5)`, `H = relu(z)`; `x_ax` con `ravel()`; grafico sovrapposto con 5 `plot`; **extra** subplot `1×5` con `fig.suptitle` / `supxlabel` / `supylabel` / `tight_layout(rect=...)` e titoli per peso `w` — dimostra padronanza Matplotlib oltre il minimo.
- **Errori / lacune:** **Path:** `os.path.join(dirname(__file__), "modulo_03_dl_cv", "figures")` crea cartella annidata `modulo_03_dl_cv/modulo_03_dl_cv/figures/` invece di `modulo_03_dl_cv/figures/`. **Nome file:** consegna chiede `02_relu_attivazioni.png`, salvato `02_attivazioni_relu.png`. Manca **legenda** (opzionale ma utile sul grafico sovrapposto). Manca **commento obbligatorio** (1 riga su rampe + intuizione UAT). `W1` ordinato con `np.sort` non è nella traccia (ok visivamente, ma non è il setup “pesi random” letterale). Subplot: `plt.savefig` / `plt.close()` senza `fig` esplicito (funziona spesso, meglio `fig.savefig` + `plt.close(fig)`).
- **Correzione / suggerimento:** `fig_dir = os.path.join(os.path.dirname(__file__), "figures")`; salvare overlay in `02_relu_attivazioni.png`; aggiungere `plt.legend()` nel primo grafico; una riga commento post-plot; opzionale tenere `03_...` come studio personale in path corretto.
- **Pattern errore / ID contesto:** monitoraggio **Pattern #6** (path/nome deliverable vs testo consegna).

### [2026-05-21] — POST-FEEDBACK — TODO 3.2 (`02_reti_neurali.py`, righe 843–881)

- **Fix applicato:** path non più annidato `modulo_03_dl_cv/modulo_03_dl_cv/`; cartella `reti_neurali_plot/` sotto il file capitolo; nome overlay **`02_relu_attivazioni.png`** corretto; commento riga 881 aggiunto; subplot bonus mantenuto (`03_relu_attivazioni_grafici_singoli.png`).
- **Valutazione qualità attuale:** **8/10**. Il **primo tentativo** storico resta **7/10**.
- **Ancora da allineare (micro):** consegna chiede cartella **`figures/`** (non `reti_neurali_plot/`); legenda opzionale assente sul grafico sovrapposto; commento UAT presente ma incompleto (manca rampe a zero + combinazione neuroni / UAT in parole della traccia); `W1` ancora `np.sort` (ok didattico, non letterale); subplot: preferire `fig.savefig` + `plt.close(fig)`.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V1 (shape catena matmul)

- **Domanda:** shape di `Z = (((X @ W1) @ W2) @ W3)` con `X (N,d)`, pesi come in traccia.
- **Risposta studente:** `(N, k)`.
- **Valutazione (primo tentativo):** **8/10** — risultato **corretto**; manca la **spiegazione** richiesta (“Spiega”).
- **Correzione:** aggiungere catena: `(N,d)@(d,h1)→(N,h1)` → `@(h1,h2)→(N,h2)` → `@(h2,k)→(N,k)`; N resta sulle righe (pratiche), k colonne in uscita.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V2 (pesi zero → P.mean)

- **Domanda:** rete 2-layer, ReLU hidden, tutti i pesi a 0 → `P.mean()` ≈ ? + perché.
- **Risposta studente:** **(b) 0.5** — dot product 0 per riga → sigmoid finale → 0.5 per riga.
- **Valutazione (primo tentativo):** **9/10** — scelta e filo logico **corretti** (allineato a `_demo_init_zero` con bias zero).
- **Manca per 10/10:** passaggio esplicito **ReLU(0)=0** sullo hidden; chiarire che si assume anche **bias=0** (solo “pesi” nella domanda, nel capitolo la demo usa `b1=b2=0`); secondo layer `H@W2=0` → logit `z=0` → `sigmoid(0)=0.5`; opzionale richiamo **R5** (neuroni hidden identici).

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V3 (UAT + limite pratico)

- **Risposta studente:** abbastanza neuroni → in teoria si approssima qualsiasi funzione complessa; limite = “capacità di elaborazione dei dati”.
- **Valutazione (primo tentativo):** **6.5/10** — **prima metà ~8/10** (intuizione giusta); **limite pratico ~4/10** (vago, non allineato al capitolo).
- **Correzione:** UAT = rete **2-layer**, neuroni hidden sufficienti, approssima funzioni **continue** (esistenza, non costruzione). Limiti pratici del file: (1) dice che **esiste** una rete, non **come trovarla** (serve training/backprop cap.03); (2) “abbastanza neuroni” può voler dire **molti** → compute/dati; (3) teoria ≠ generalizzazione su dati nuovi.

### [2026-05-21] — POST-FEEDBACK — Quiz verifica V3 (UAT rivalutazione)

- **Risposta aggiornata:** hidden con abbastanza neuroni → approssima funzioni **continue**; 3 limiti: esiste strada ma non GPS; neuroni possono essere tantissimi; training ≠ mondo reale.
- **Valutazione qualità attuale:** **9/10**. Il **primo tentativo** storico resta **6.5/10**.
- **Micro:** typo `hydden`; opzionale citare esplicitamente **2 layer** e **backprop** (cap.03) come “GPS”; terzo limite formulabile come **generalizzazione** oltre al training set.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V4 (pesi ×100, sigmoid, He init)

- **Risposta studente:** pesi grandi → logit/dot enormi → sigmoid a rischio overflow (clip ±500); He scala con `sqrt(2/d)` per tenere i prodotti sotto controllo.
- **Valutazione (primo tentativo):** **8/10** — filo logico **corretto**; formula He ok.
- **Manca per 9–10:** esplicitare che **`H` satura ~0 o ~1** (non solo “blocco calcolo”); conseguenza **R6**: gradiente sigmoid ≈ 0 → si impara poco (anticipa cap.03); `d` = **fan_in** (colonne input / prima dim di `W`), non “righe” in senso ambiguo; He serve soprattutto **all’inizio del training**, non solo “in fase di test”.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V5 (equivalenza LogisticRegression)

- **Risposta studente:** **(a)** corretta; **(b)** “è una rete neurale” (non LR); **(c)** collassa senza attivazioni interne → equivalente al primo.
- **Valutazione (primo tentativo):** **8/10** — scelta **(a)** ok; intuizione **(c)** sul collasso lineare **corretta** (richiamo TODO 2.2).
- **Manca:** perché **(a)** = LR (`z=X@w+b` + sigmoid = `predict_proba`); **(b)** perché **ReLU** rompe la linearità (vera rete 2-layer, non collassa); **(c)** precisare: equivalente “come funzione” con **`W_eff = W1 @ W2`** (stessa classe del modello, parametrizzazione diversa) — la risposta ufficiale privilegia **(a)** come forma canonica.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V6 (conteggio parametri)

- **Risposta studente:** `((7*32)+1)+((32*2)+1)=290`; testo: 7 pesi×32 neuroni + bias + 32×2 output + bias.
- **Valutazione (primo tentativo):** **5.5/10** — schema **W1,b1,W2,b2** ok; **numero sbagliato** (corretto **289**).
- **Errori:** **b1** = **32** bias (non 1); output **binario** → **W2 (32,1)** e **b2 (1,)** (non `32*2`); formula: `7*32 + 32 + 32*1 + 1 = 289`. **N=100** non entra nel conteggio (solo batch).

### [2026-05-21] — POST-FEEDBACK — Quiz verifica V6 (parametri rivalutazione)

- **Risposta aggiornata:** `((7*32)+32)+((32*1)+1)=289`; testo: bias per neurone hidden, 32 pesi verso **1** neurone output + bias.
- **Valutazione qualità attuale:** **9.5/10**. Il **primo tentativo** storico resta **5.5/10**.
- **Micro:** opzionale esplicitare shape `W1(7,32), b1(32), W2(32,1), b2(1)`.

### [2026-05-21] — `02_reti_neurali.py` — Quiz verifica V7 (Feynman rete neurale)

- **Risposta studente:** analogia macchina che sforna biscotti: ingredienti → più passaggi → biscotti; trasformazione input→output.
- **Valutazione (primo tentativo):** **7/10** — rispetta **vincoli** (no math/codice/IA/computer); analogia **concreta**; manca il “cuore” rete: **più stazioni** che mescolano in modi diversi, **filtro** che scarta (tipo ReLU), **giudizio finale** (tipo probabilità).
- **Correzione:** aggiungere 1 riga su passaggi interni diversi + esito finale (“quanto è buono il biscotto” / sì-no) senza jargon.

### [2026-05-21] — POST-FEEDBACK — Quiz verifica V7 (Feynman rivalutazione)

- **Risposta aggiornata:** macchina biscotti; passaggi sequenziali; scarta ingredienti marci; decide vaniglia vs cioccolato (2 uscite).
- **Valutazione qualità attuale:** **8.5/10**. Il **primo tentativo** storico resta **7/10**.
- **Punti di forza:** filtro (scarto) ≈ ReLU; decisione binaria finale ≈ sigmoid/classificazione; più passaggi ≈ layer.
- **Micro:** typo `un una`, `out`; ultima frase un po’ ridondante; opzionale “più postazioni che mescolano in modi diversi” per hidden.

### [2026-05-21] — `02_reti_neurali.py` — E1 [COLLOQUIO] (architettura rete 2-layer su CSV M2)

- **Valutazione (primo tentativo):** **5.5/10**.
- **Punti di forza:** flusso layer1 → ReLU (perché taglia negativi) → layer2 → sigmoid (probabilità 0–1); idea batch N pratiche; distinzione logit vs probabilità sul finale.
- **Errori / lacune:** **W2** scritto come vettore `(h,)` invece di **`W2 (h, 1)`** (binario = 1 uscita); **mancano numeri concreti** del CSV (**d=7**, es. **h=32**, **289** parametri); **mancano** tutti i nomi richiesti in forma compatta (`X,W1,b1,H,W2,b2,Z,P`); **nessun confronto** con LogisticRegression; testo **>> 12 righe** (consegna colloquio).

### [2026-05-21] — `02_reti_neurali.py` — E2 [REFACTORING] `forward_bello`

- **Valutazione (primo tentativo):** **8/10**.
- **Punti di forza:** `NDArray` ok (#25); `W` 2D; `X.shape[1]==W.shape[0]`; **`return X @ W + b`** vettorizzato (niente loop); niente virgola tuple (#23).
- **Errore:** check bias confronta `b.shape[0]` con **`W.shape[0]`** (fan-in **d**) — corretto è **`W.shape[1]`** (fan-out **h**, un bias per colonna di W). Con `W(7,32)` e `b(32,)` il tuo testo non segnala errore se `b` ha 7 elementi per sbaglio.
- **Fix:** `if b.shape[0] != W.shape[1]:` (o `len(b) != W.shape[1]`); opzionale messaggi con `f"{X.shape} {W.shape}"`.

### [2026-05-21] — POST-FEEDBACK — E2 `forward_bello` (fix bias check)

- **Fix:** condizione `b.shape[0] != W.shape[1]` corretta; messaggio errore ancora dice `W.shape[0]` (typo testo).
- **Valutazione qualità attuale:** **9/10**. Primo tentativo storico **8/10**.

### [2026-05-21] — `02_reti_neurali.py` — E3 [DEBUG] (P.mean sempre 0.5)

- **Valutazione (primo tentativo):** **8/10**.
- **Fix:** `att=relu` su primo `layer_dense` — **corretto** (richiamo R2 / TODO 2.2).
- **Diagnosi:** conclusione ok (logit ~0 → sigmoid ~0.5); spiegazione parziale (“gaussiana schiaccia a 0”) — meccanismo preciso: **senza ReLU** i due layer lineari **collassano**, `Z≈0` → `P≈0.5`.
- **Autonomia:** rispettata (bug trovato senza hint a cascata).

### [2026-05-21] — POST-FEEDBACK — E3 [DEBUG] (diagnosi aggiornata)

- **Diagnosi:** aggiunto **collasso lineare** + valori centrati → `Z≈0` → sigmoid ~0.5.
- **Valutazione qualità attuale:** **9/10**. Primo tentativo storico **8/10**.

### [2026-05-21] — `02_reti_neurali.py` — E4 [RETRIEVAL] `neurone_batch` da memoria

- **Valutazione (primo tentativo):** **6/10**.
- **Punti di forti:** firma `NDArray`, check `X` 2D / `w` 1D / colonne, `X @ w + b` vettorizzato, test con `X(3,4)`, `w(4,)`.
- **Errore principale:** `return X @ w + b` restituisce **logit** `(N,)`, non **probabilità** — manca **`sigmoid` dentro** la funzione (cap.01: `z` poi `sigmoid(z)`). Il `print(sigmoid(neurone_batch(...)))` maschera il bug.
- **Fix:** `z = X @ w + b`; `return np.asarray(sigmoid(z), dtype=float)` (o `return sigmoid(X @ w + b)`).

### [2026-05-21] — POST-FEEDBACK — E4 [RETRIEVAL] `neurone_batch` (fix sigmoid)

- **Fix:** `return sigmoid(X @ w + b)`; test diretto `print(neurone_batch(...))` senza sigmoid esterna.
- **Valutazione qualità attuale:** **9/10**. Primo tentativo storico **6/10**.

### [2026-05-21] — `02_reti_neurali.py` — E5 [INTERLEAVING] (pesi ×100, saturazione sigmoid)

- **Valutazione (primo tentativo):** **7.5/10**.
- **Punti di forza:** `X_scaled` + CSV M2; forward `relu`→`Z`→`P`; confronto pesi normali vs `W*100`; (a) Z molto grandi (commento ±500); (c) sigmoid stabile non esplode, satura ~0/~1 — **R6** ok.
- **Manca:** stampa esplicita **`P.min/max/mean`** per (b); tabella **prima/dopo** su Z **e** P insieme; etichette dicono “scalatura” ma è **pesi×100** (X già sempre scalato); opzionale `W.min/max` prima/dopo moltiplicazione.

### [2026-05-21] — `02_reti_neurali.py` — Mini-progetto `rete_2_layer_vs_logreg` (~righe 1167–1213)

- **Valutazione (primo tentativo):** **7/10**.
- **Punti di forza:** `carica_pratiche` + `StandardScaler`; `LogisticRegression` + `predict_proba[:, 1]`; `rete_2_layer` + `init_pesi_he`; **accuracy** su soglia 0.5 corretta; `n_param_rete` formula ok; dict con chiavi richieste; `pprint` finale.
- **Errore critico:** `roc_auc_score(y, y_clf)` e `roc_auc_score(y, y_rete)` — AUC va sulle **probabilità** (`P_clf`, `P_rete`), non su 0/1 già tagliati (concetto AUC appena visto in chat).
- **Dettagli:** parametro `seed` in firma ma non passato a `init_pesi_he`; opzionale `seed`/`seed+1` distinti per W1/W2 come in Sez. 3.2.

### [2026-05-21] — POST-FEEDBACK — Mini-progetto `rete_2_layer_vs_logreg` (fix AUC + seed)

- **Fix:** `roc_auc_score(y, P_clf)` / `roc_auc_score(y, P_rete)`; `init_pesi_he(..., seed=seed)` su W1 e W2.
- **Valutazione qualità attuale:** **9/10**. Primo tentativo storico **7/10**.
- **Residuo opzionale:** `random_state` della LR fissa a `42` (non usa `seed` della firma); stesso `seed` su entrambi i layer — in Sez. 3.2 si usava `seed+1` sul secondo.

### [2026-05-21] — `02_reti_neurali.py` — Checkpoint C1 (layer Dense, 1 frase)

- **Valutazione (primo tentativo):** **7/10**.
- **Ok:** strato della rete; collegamento a prodotto matriciale + idea attivazione.
- **Da affinare:** operazione core = **`X @ W + b`** (non solo “dot product”); attivazione **opzionale** (`att=None` → layer lineare); “due matrici” poco preciso (batch `N` righe, `W` shape `(d,h)`).

### [2026-05-21] — POST-FEEDBACK — Checkpoint C1 (layer Dense)

- **Fix:** fully-connected; `(N,d)@(d,h)+bias`; `funzione_di_att(...)`; bias esplicito.
- **Valutazione qualità attuale:** **8.5/10**. Primo tentativo storico **7/10**.
- **Residuo:** sostituire “dot product” con **moltiplicazione matriciale**; una parola su attivazione **opzionale** se `att=None`.

### [2026-05-21] — `02_reti_neurali.py` — Checkpoint C2 (shape output rete)

- **Valutazione (primo tentativo):** **9/10**.
- **Ok:** `(50, 3)` corretto; regola `(righe X, colonne ultimo W)` valida se la catena combacia (`5→8→3`).
- **Plus opzionale:** una riga intermedia `(50, 5)@(5,8)→(50,8)` poi `(50,8)@(8,3)→(50,3)` per fissare il ragionamento layer per layer.

### [2026-05-21] — `02_reti_neurali.py` — Checkpoint C3 (lineare vs ReLU, 2 righe)

- **Valutazione (primo tentativo):** **8.5/10**.
- **Ok:** **collasso** in un solo layer lineare (R2); ReLU introduce **non-linearità** e più capacità espressiva.
- **Plus opzionale:** legare al dominio — senza ReLU resti vicino a un confine **lineare** (come LR); ReLU “piega” lo spazio delle feature.

### [2026-05-21] — `02_reti_neurali.py` — Checkpoint C4 (auto-rating onesto)

- **Autovalutazione studente:** Dense 9, R2 9, He/R5 9, forward CSV 9, UAT 7.
- **Allineamento mentor:** coerente con valutazioni sessione (mini-progetto 9, C1–C3 8.5–9); **UAT 7** plausibile (intuizione senza formalizzazione).
- **Nota chiusura capitolo:** E1 ancora con `W2 (h,)` e senza conteggio parametri/confronto LR; **E6** vuoto — non dichiarare capitolo chiuso finché non completati o esplicitamente rinviati.

---

## Lacune e dubbi ancora aperti

- **E6 [REAL-WORLD]** rinviato volontariamente (21/05/2026): studente preferisce non “copiare” risposte senza visione d’insieme; ripianificare a fine M3 o in mock system design.
- **E1 [COLLOQUIO]** post-fix: `W2 (h,1)` ok; ancora senza conteggio parametri esplicito (es. 145 con h=16) né confronto LR in testo; oltre 12 righe.

---

## Chiusura capitolo (21/05/2026)

- **Voto difficoltà:** **8/10** (Gianluca).
- **Completati:** teoria R1–R6, quiz, E2–E5, mini-progetto `rete_2_layer_vs_logreg` (9/10), checkpoint C1–C4, E1 fix shape output.
- **Rinviato:** E6 (scelta consensuale).
- **Prossimo:** `03_backpropagation.py` — loss, gradienti, training rete 2-layer.

### [2026-05-21] — POST-FIX — E1 [COLLOQUIO] (`W2 (h,1)`)

- **Fix:** output layer `W2` shape `(h, 1)` (non `(h,)`).
- **Residuo:** mancano conteggio parametri (145 con h=16) e confronto LR esplicito; testo >12 righe.
- **Valutazione post-fix:** **7.5/10** (chiusura accettata).

---

## Note per il capitolo successivo (mentor)

- Se il TODO 1.1 evidenzia ancora confusione sulle shape `(N, d) @ (d, h) -> (N, h)`, **bloccare** prima di passare alla Sez. 2.
- Se l'`init_pesi_he` non viene compreso (perche' `sqrt(2/d)` e non `0.01`?), recuperare prima del cap.03 M3 (li' si parla di vanishing/exploding gradient).
- Verificare che TODO 2.2 (collasso lineare a 3 layer) sia eseguito DA SOLO: e' il check che la regola R2 e' stata davvero capita.
- Per il cap.03 M3 (backpropagation): partire dalla rete 2-layer di questo capitolo e introdurre il **training** (loss + gradient descent + backward). NON saltare il capitolo se questo non e' chiuso 8+/10.

---

## Note tecniche di stesura (mentor)

- _(da popolare quando il capitolo verra' aperto e lavorato)_
