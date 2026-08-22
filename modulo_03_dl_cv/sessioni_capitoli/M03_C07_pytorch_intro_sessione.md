# Diario sessione — Capitolo 07 — PyTorch intro

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `07_pytorch_intro.py` |
| **File diario** | `M03_C07_pytorch_intro_sessione.md` |
| **Stato** | chiuso anticipata (13/08/2026) — residui → cap.08 / bridge R07 |
| **Voto difficoltà** | **7**/10 |

---

## Obiettivi del capitolo (per il mentor)

- Tensori, autograd, `nn.Module`/`Linear`, Dataset/DataLoader, training loop, `state_dict`
- Workflow Colab (GPU) ↔ Cursor (CPU)
- Chiudere lacune **#42/#43** e Pattern **#27** con i 🔁 in testa al file
- Recuperare CONFRONTO / scaler / drift migrati dal cap.06

---

## Domande durante lo studio

- _(vuoto — capitolo appena aperto)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### 2026-08-03 — Quiz ingresso Q1 (`07_pytorch_intro.py` ~105–108)

- **Esercizio / blocco:** Q1 Training loop in 1 riga
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Ordine completo e corretto: `forward + loss + backward + update` (allineato a soluzione e al ciclo NumPy del cap.06).
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** in PyTorch lo stesso ciclo diventa `zero_grad → forward → loss → backward → optimizer.step()` (lo vedrai in sez.5)
- **Pattern errore / ID contesto:** — (rinforza glossario Training loop 2/3)

### 2026-08-03 — Quiz ingresso Q2 (`07_pytorch_intro.py` ~109–112)

- **Esercizio / blocco:** Q2 Cache del forward nel backward manuale
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Ruolo chiaro (valori intermedi per le derivate) + elenco corretto `Z1, H, Z2, P`.
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** in PyTorch la cache “manuale” la fa **autograd** (nastro/scontrino); tu non la costruisci a mano.
- **Pattern errore / ID contesto:** — (glossario Cache 2/3)

### 2026-08-03 — Quiz ingresso Q3 (`07_pytorch_intro.py` ~113–119)

- **Esercizio / blocco:** Q3 Shape gradienti rete d=4, h=8, out=1
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Regola “grad ha la stessa shape del parametro”: `(d,h)`, `(h,)`, `(h,1)`, `(1,)` → con i numeri `(4,8)`, `(8,)`, `(8,1)`, `(1,)`. Coerente con convenzione colonna del corso (non la variante flatten W2 `(h,)`).
- **Errori / lacune:** nessuno (ex lacuna #41 shape non riemerge)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Quiz ingresso Q4 (`07_pytorch_intro.py` ~120–123)

- **Esercizio / blocco:** Q4 Sanity check del backward
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Idea “prova del nove prima di addestrare” / evitare lavoro inutile — direzione giusta.
- **Errori / lacune:** Manca la definizione operativa: confrontare **gradiente analitico** (backward a mano) vs **gradiente numerico** (`h≈1e-6`). “Funzioni modificate” è troppo generico. Typo: “abbiamo” → “abbiano”.
- **Correzione / suggerimento:** Sanity check = `assert np.allclose(grad_analitico, grad_numerico)` sui pesi **prima** del training loop.
- **Pattern errore / ID contesto:** lacuna soft **#44** (definizione sanity check)

### 2026-08-03 — Quiz ingresso Q5 (`07_pytorch_intro.py` ~124–128)

- **Esercizio / blocco:** Q5 Trova errore — manca `/N` su `dZ2`
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Individua `/N` (media batch BCE); collega a `p-y` = `dL/dz`; formula `((P-y)/N).reshape(-1,1)` corretta (equivalente a reshape poi `/N`).
- **Errori / lacune:** nessuno (typo soft “miracoloso” → “miracolosa”)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** — (ex residuo soft #36 sul `/N` chiuso a freddo)

### 2026-08-03 — Quiz ingresso Q6 (`07_pytorch_intro.py` ~129–134)

- **Esercizio / blocco:** Q6 Loss iniziale BCE rete random, dataset bilanciato
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `≈ 0.693` = `-log(0.5)` = `ln(2)`; cifra corretta.
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Quiz ingresso Q7 (`07_pytorch_intro.py` ~134–137)

- **Esercizio / blocco:** Q7 Loss 0.692 dopo 500 epoche
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Diagnosi corretta = opzione **(b)** “qualcosa non funziona”; collega a loss ancora ≈ random (`0.693`).
- **Errori / lacune:** nessuno (lettera non citata, contenuto sì)
- **Correzione / suggerimento:** cause tipiche: lr sbagliato, bug backward/update, no learning, label invertite, ecc.
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Quiz ingresso Q8 (parziale) (`07_pytorch_intro.py` ~138–142)

- **Esercizio / blocco:** Q8 Feynman backprop vs GD — solo bozza “Backpropagation: …”
- **Valutazione (primo tentativo — parziale):** **6.5/10** (non ancora risposta completa 4–6 frasi su entrambi)
- **Punti di forza:** Chain rule / derivate locali / “distribuisce l’errore” sui parametri = cuore della **backprop** ok.
- **Errori / lacune:** Nell’ultima frase entra `w = w - grad * lr` → quello è **gradient descent** (l’update), non la backprop. Stesso mix soft di TODO 14 cap.06. Manca ancora un blocco esplicito “GD fa…”.
- **Correzione / suggerimento:** Chiudi backprop a “calcola i gradienti”; poi 1–2 frasi solo su GD = usa quei gradienti per il passo. Typo: chian → chain.
- **Pattern errore / ID contesto:** soft backprop vs GD (priorità attiva)

### 2026-08-03 — Quiz ingresso Q8 (post-feedback) (`07_pytorch_intro.py` ~138–143)

- **Esercizio / blocco:** Q8 Feynman backprop vs GD — versione separata
- **Valutazione (post-feedback):** **9.5/10** (primo tentativo resta **6.5/10**)
- **Punti di forza:** Distacco netto: backprop = distribuisce errore / calcola gradienti; GD = update `w = w - grad * lr`. Mix TODO 14 risolto.
- **Errori / lacune:** soft lingua: chian→chain, Gradiente→Gradient, parziale→parziali
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** soft backprop vs GD → in miglioramento (verificato post-hint)

### 2026-08-03 — Rinforzo #42 clip BCE (`07_pytorch_intro.py` ~149–162)

- **Esercizio / blocco:** Micro 42.A + 42.B
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** 42.A `np.clip(p, eps, 1-eps)` + BCE su `p_safe`; 42.B **Falso** con motivo corretto (`-log(0)` / inf-nan sulla probabilità).
- **Errori / lacune:** nessuno (opzionale: z non vive in (0,1), quindi clippare z in [eps,1-eps] non ha nemmeno senso di dominio)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** lacuna **#42** → 🟢

### 2026-08-03 — Rinforzo #43 scaler (`07_pytorch_intro.py` ~167–186)

- **Esercizio / blocco:** Micro 43.A + 43.B
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** 43.A identifica precedenza `/` prima di `-`; codice `X_right` corretto. 43.B `std==0 → 1.0`.
- **Errori / lacune:** nessuno (lingua soft)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** lacuna **#43** → 🟢

### 2026-08-03 — Rinforzo Pattern #27 Micro 27.A (`07_pytorch_intro.py` ~192–206)

- **Esercizio / blocco:** `dL/dp = (p-y)/(p*(1-p))`
- **Valutazione (primo tentativo — "voto esame"):** **4/10**
- **Punti di forza:** Parentesi ok; niente moltiplicazione implicita `p(1-p)`; forma quoziente corretta.
- **Errori / lacune:** Denominatore `(p * (1 - y))` invece di `(p * (1 - p))` — variabile sbagliata (`y` al posto di `p`). Pattern **#27**.
- **Correzione / suggerimento:** Rileggere simbolo per simbolo la formula del commento; 27.B ancora da fare.
- **Pattern errore / ID contesto:** Pattern **#27** ancora 🔴

### 2026-08-03 — Rinforzo Pattern #27 Micro 27.B (`07_pytorch_intro.py` ~208–211)

- **Esercizio / blocco:** `H` @ pesi output — (a)/(b)/(c)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** **(b) `H @ W2`** — prodotto matriciale; non `*` element-wise né `W2 @ H` (shape invertite).
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** 27.A resta da correggere (`1-p`, non `1-y`) se non già fatto
- **Pattern errore / ID contesto:** Pattern #27 — pezzo `@` vs `*` ok; pezzo variabili in formula ancora aperto su 27.A

### 2026-08-03 — Sez.1 Mini 1.1 + 1.2 (`07_pytorch_intro.py` ~228–237)

- **Esercizio / blocco:** tensor zeri (4,3) float32 CPU; ndarray→tensor + shape
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10** (1.1 ≈8.5, 1.2 ≈6.5)
- **Punti di forza:** 1.1: zeri, shape `(4,3)`, `float32`, device default CPU ok. 1.2: conversione `torch.tensor(arr_numpy)` corretta, array `(5,)`.
- **Errori / lacune:** 1.2 chiede di stampare **`.shape`**, hai stampato `type(...)`. 1.1 funziona ma idiom idiomatico è `torch.zeros(4, 3, dtype=torch.float32)` (senza passare da NumPy).
- **Correzione / suggerimento:** `print(arr_torch.shape)` → `(5,)`; opzionale `torch.from_numpy` (condivide memoria) vs `torch.tensor` (copia).
- **Pattern errore / ID contesto:** soft Pattern #6 (consegne: shape vs type)

---

### 2026-08-03 — Rinforzo #44 Micro 44.A (`07_pytorch_intro.py` ~307–310)

- **Esercizio / blocco:** Micro 44.A — definizione operativa sanity check (analitico + numerico)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Meccanismo corretto: analitico rigoroso ma sbagliabile; numerico lento ma fidato; se coincidono → formula analitica ok → si può addestrare. Chiude il gap di Q4 (prima solo “prova del nove”).
- **Errori / lacune:** nessuno (nit soft: “sempre esatta” ≈ “fidata entro `h≈1e-6`”; non scala il voto)
- **Correzione / suggerimento:** prossimo Micro 44.B (perché in PyTorch il check manuale quasi sparisce)
- **Pattern errore / ID contesto:** lacuna **#44** → 🟢 Superato

### 2026-08-03 — Rinforzo #44 Micro 44.B (`07_pytorch_intro.py` ~311–315)

- **Esercizio / blocco:** Micro 44.B — perché in PyTorch il sanity check manuale quasi sparisce
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Direzione giusta: i gradienti li gestisce PyTorch → non c’è (quasi) più una formula tua da verificare.
- **Errori / lacune:** Formulazione soft: non è “improbabile sbagliarsi”, è che **non scrivi più** il backward analitico (lo fa **autograd**). Eccezione: layer custom → `torch.autograd.gradcheck`.
- **Correzione / suggerimento:** Frase da colloquio: “Autograd calcola i gradienti al posto tuo; il sanity check manuale serve soprattutto se implementi un’operazione custom.”
- **Pattern errore / ID contesto:** #44 resta 🟢 (44.A ha chiuso il meccanismo; 44.B ok con nit)

### 2026-08-03 — Sez.1 Mini 1.3 (`07_pytorch_intro.py` ~476–484)

- **Esercizio / blocco:** Mini 1.3 — X_demo float64 → tensor float32, stampa shape + dtype
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** `from_numpy` + print di `.shape` e `.dtype` ok; risultato pratico float32 shape `(2, 2)`.
- **Errori / lacune:** Hai **ricreato** `X_demo` già in `float32`, saltando il punto dell’esercizio: usare l’`X_demo` del rinforzo #43 (float64 di default) e **convertire**. Soft Pattern #6 (lettura consegna).
- **Correzione / suggerimento:** `torch.tensor(X_demo, dtype=torch.float32)` oppure `torch.from_numpy(X_demo.astype(np.float32))` sull’array già definito sopra.
- **Pattern errore / ID contesto:** soft #6 consegne; tranello dtype 64→32 da consolidare
- **Fix applicato (post-feedback):** `X_demo` senza dtype (→ float64) + `torch.tensor(..., dtype=torch.float32)` + print shape/dtype — **corretto**.

### 2026-08-03 — Sez.1 Mini 1.4 (`07_pytorch_intro.py` ~486–497)

- **Esercizio / blocco:** Mini 1.4 — tensori (2,3)@(3,2), shape attesa prima di stampare
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Shape attesa `(2, 2)` corretta (regola `(m,k)@(k,n)→(m,n)`); `@` usato bene; print di `.shape` ok.
- **Errori / lacune:** nessuno (`torch.rand` va benissimo al posto di `randn`/`zeros`)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Sez.2 verifica numerica esempio 2.1 (`07_pytorch_intro.py` ~541–552)

- **Esercizio / blocco:** Check numerico di `dy/dw` per `y=(w*x)^2` (dopo esempio autograd)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Dopo correzione: perturba `w` (non `x`); composizione `u=w*x`, `y=u^2`; differenza centrata `/ (2*eps)` corretta → ≈ 36, allineato a chain rule e `w.grad`.
- **Errori / lacune:** Soft: riscrive `w`/`x` torch con NumPy (meglio `w_np`/`x_np`); manca un `print`/`assert` esplicito del confronto nel snippet (la formula però è giusta).
- **Correzione / suggerimento:** `print(derivata_numerica)` e confronta con 36; non sovrascrivere i tensori dell’esempio 2.1.
- **Pattern errore / ID contesto:** — (primo tentativo aveva dy/dx; fix applicato prima della valutazione formale)

### 2026-08-03 — Sez.2 verifica numerica esempio 2.1 RIVALUTAZIONE (`07_pytorch_intro.py` ~534–555)

- **Esercizio / blocco:** Autograd `(w*x)^2` + check numerico + `assert` vs `w.grad`
- **Valutazione (richiesta esplicita post-fix):** **10/10**
- **Punti di forza:** Tensori torch intatti (`w`/`x`); NumPy in `w_1`/`x_1`; formula centrata su `w`; `assert np.isclose(w.grad.item(), derivata_numerica)` chiude il cerchio analitico/autograd/numerico.
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Sez.2 Mini 2.1 (`07_pytorch_intro.py` ~589–605)

- **Esercizio / blocco:** Mini 2.1 — dy/dw di `y=(w+1)^2` a `w=1`, a mano + autograd
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**
- **Punti di forza:** Parte PyTorch corretta: `requires_grad=True`, `y=(w_tch+1)**2`, `.backward()`, confronto con `.grad`.
- **Errori / lacune:** Formula analitica sbagliata: `2*w` invece di `2*(w+1)`. Usi il `w` torch dell’esempio sopra (=2), non `w_np` (=1) → `der_ana=4` e l’assert **passa per coincidenza** (a `w=1` il vero gradiente è comunque 4). `y_np` calcolato ma non usato.
- **Correzione / suggerimento:** A mano: `dy/dw = 2*(w+1)` → a `w=1` vale **4**. Codice: `der_ana = 2*(w_np+1)` e usa solo `w_np` / `w_tch`.
- **Pattern errore / ID contesto:** soft #6 variabili; attenzione assert “fortunati”
- **Fix applicato (post-feedback):** `der_ana = 2*(w_np+1)`, `y_np` su `w_np`, autograd invariato → **corretto** (rivalutazione informale **10/10**).

### 2026-08-03 — Sez.2 Mini 2.2 (`07_pytorch_intro.py` ~606–609)

- **Esercizio / blocco:** Mini 2.2 — cosa sostituisce autograd rispetto al cap.06 (2 frasi)
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** Nocciolo corretto: niente più derivate/backward scritti a mano con chain rule.
- **Errori / lacune:** Solo 1 frase (ne chiedeva 2). Manca il pezzo “cache/scontrino”: autograd sostituisce anche la contabilità manuale dei valori intermedi. Typo `chian` → chain. Non confondere: non sostituisce il GD/`optimizer.step()`.
- **Correzione / suggerimento:** Frase 2 es.: “Registra il grafo delle operazioni (come la cache) e con `.backward()` riempie `.grad`.”
- **Pattern errore / ID contesto:** —

### 2026-08-03 — Sez.2 Mini 2.3 (`07_pytorch_intro.py` ~609–613)

- **Esercizio / blocco:** Mini 2.3 — perché `q.grad` = 2, 4, 6 (parola accumulo)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Meccanismo corretto: `.grad` somma i contributi di ogni `backward` se non azzeri → 2+2+2. Usa la famiglia lessicale di “accumulo”.
- **Errori / lacune:** nessuno (nit: “accumula” vs sostantivo “accumulo”; non scala)
- **Correzione / suggerimento:** Ecco perché esiste `optimizer.zero_grad()` a ogni step.
- **Pattern errore / ID contesto:** —

### 2026-08-04 — Sez.3 Mini 3.1 (`07_pytorch_intro.py` ~709–728)

- **Esercizio / blocco:** Mini 3.1 — istanzia rete 2-layer + `named_parameters()` (nome + shape); studente ha ricreato la classe per pratica
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Architettura corretta (`fc1` d→h, `fc2` h→1, ReLU, sigmoid+squeeze); `super().__init__()` ok; loop su `named_parameters()` giusto. Ricreare `My_Rete_2_layer` invece di riusare `Rete2Layer` = ottima pratica.
- **Errori / lacune:** La consegna chiede **nome + shape**; stampi l’intero `parameter` (pesante). Hint: `"torch.tensor"` → meglio `"torch.Tensor"` (il tipo è `Tensor`).
- **Correzione / suggerimento:** `print(name, tuple(parameter.shape))`
- **Pattern errore / ID contesto:** soft lettura consegna (#6) su “shape”
- **Fix / rivalutazione (04/08/2026):** `parameter.shape` + hint `torch.Tensor` → **10/10**

### 2026-08-04 — Sez.3 Mini 3.2 (`07_pytorch_intro.py` ~733–741)

- **Esercizio / blocco:** Mini 3.2 — conta parametri `numel()` vs formula `d*h + h + h*1 + 1`
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `sum(p.numel() for p in ...)` corretto; formula manuale corretta (73 con d=7,h=8); `d`/`h` definiti; `assert` chiude il check.
- **Errori / lacune:** nessuno (nit: per interi basta `==`; `np.isclose` va comunque)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-04 — Sez.3 Mini 3.3 (`07_pytorch_intro.py` ~742–757)

- **Esercizio / blocco:** Mini 3.3 — batch (10,7) → shape output; perché non (10,1)
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `torch.randn(10, 7)`, forward del modello, shape `(10,)`; motiva correttamente `squeeze(-1)` sul logit `(10,1)`.
- **Errori / lacune:** Soft: `squeeze(-1)` ≠ `ravel()` in generale — toglie solo l’ultima dim se è 1; `ravel` appiattisce tutto. Qui l’effetto coincide. Typo `sqeeze`.
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-04 — Sez.4 Mini 4.1 (`07_pytorch_intro.py` ~845–866)

- **Esercizio / blocco:** Mini 4.1 — TensorDataset + DataLoader batch 32, shape primo batch
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** float32, `TensorDataset`, `DataLoader(..., shuffle=True)`, `next(iter(...))`; shape attese `(32, 7)` e `(32,)`.
- **Errori / lacune:** nessuno (`torch.tensor` ok al posto di `from_numpy`; `h` inutilizzato non scala)
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-04 — Sez.4 Mini 4.2 (`07_pytorch_intro.py` ~868–875)

- **Esercizio / blocco:** Mini 4.2 — step per epoca con N=200, batch_size=64
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Ragionamento corretto `ceil(200/64)=4` (3×64 + resto 8); verifica con `len(loader)`.
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

### 2026-08-04 — Sez.5 Rinforzo 5.4 training loop (`07_pytorch_intro.py` ~949–953)

- **Esercizio / blocco:** 5.4 — completa `zero_grad → forward → ? → backward → ?`
- **Valutazione (primo tentativo — "voto esame"):** **5/10**
- **Punti di forza:** Il primo `?` è corretto: **loss**.
- **Errori / lacune:** Manca il secondo pezzo: dopo `backward` → **`step`** / `optimizer.step()` (update dei pesi). Risposta incompleta rispetto alla consegna a due slot.
- **Correzione / suggerimento:** `zero_grad → forward → loss → backward → step`
- **Pattern errore / ID contesto:** soft #6 lettura consegna (due `?`)

### 2026-08-04 — Sez.5 Mini 5.1 (`07_pytorch_intro.py` ~955–990)

- **Esercizio / blocco:** Mini 5.1 — 5 epoche, TensorDataset finto, BCELoss + SGD, print loss
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Dataset/loader ok; ordine loop corretto (`zero_grad`→forward→loss→`backward`→`step`); 5 epoche; stampa loss per epoca.
- **Errori / lacune:** `somma_loss += loss_batch` senza `.item()` → tieni vivo il grafo (memory leak, avviso sez. 5.3). Usa `loss_batch.item()`. Soft: `{a[1]:4f}` → meglio `{a[1]:.4f}`; `list(media_epoche)` ridondante.
- **Correzione / suggerimento:** `somma_loss += loss_batch.item()`
- **Pattern errore / ID contesto:** —
- **Fix / rivalutazione (04/08/2026):** `.item()` applicato → **10/10** (nit residuo: `{a[1]:.4f}` al posto di `:4f`)

### 2026-08-04 — Sez.5 Mini 5.2 (`07_pytorch_intro.py` ~992–997)

- **Esercizio / blocco:** Mini 5.2 — senza `optimizer.step()`, cosa fa la loss e perché
- **Valutazione (primo tentativo — "voto esame"):** **5/10**
- **Punti di forza:** Sai cos’è lo `step` (GD: `w -= lr * grad`) e che i gradienti arrivano dalla loss/backward.
- **Errori / lacune:** Non rispondi all’esperimento: **senza `step` i pesi non si aggiornano → la loss resta quasi piatta** (non scende tra epoche). Forward+backward girano comunque; manca solo l’update.
- **Correzione / suggerimento:** Frase tipo: “La loss non migliora perché calcolo i gradienti ma non applico l’update.”
- **Pattern errore / ID contesto:** soft #6 (consegna: osserva il comportamento della loss)
- **Fix / rivalutazione (04/08/2026):** “loss non scende perché manca lo step/GD” → **10/10**

### 2026-08-07 — Sez.6 Mini 6.1 (`07_pytorch_intro.py` ~1091–1119)

- **Esercizio / blocco:** Mini 6.1 — salva/ricarica `nn.Linear(3,1)` + `allclose` sui weight
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Ciclo corretto `state_dict` → `torch.save` → nuovo `Linear` → `load_state_dict` + `map_location="cpu"`; seed sui pesi; assert end-to-end su `out` vs `out_2` (logica solida).
- **Errori / lacune:** Consegna chiede `allclose` sui **weight** (e idealmente `bias`), non solo sugli output; file fisso `.pt` invece di temporaneo; typo `path_weigths`.
- **Correzione / suggerimento:** Aggiungere `assert torch.allclose(modello.weight, modello_reloaded.weight)` (e sul `bias`); opz. `tempfile`.
- **Pattern errore / ID contesto:** soft #6 (verifica chiesta vs verifica fatta)
- **Rivalutazione post-fix (2026-08-07):** assert su `weight` (con `.T` ridondante ma corretto) → **9.5/10**. Residui opzionali: `bias`, file temporaneo, typo `path_weigths`.

### 2026-08-07 — Sez.6 Mini 6.2 (`07_pytorch_intro.py` ~1121–1132)

- **Esercizio / blocco:** Mini 6.2 — ricaricare `state_dict` in architettura diversa; leggere RuntimeError
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Esperimento fatto (non solo teorizzato); messaggio d’errore corretto e citato (`size mismatch for weight`); concetto chiaro — i pesi richiedono stessa shape dell’architettura.
- **Errori / lacune:** Consegna chiede `h` diverso (es. `h=16` su `Rete2Layer`); hai usato `Linear(4,1)` vs `Linear(3,1)` (mismatch su `in_features`). Stesso fenomeno, scenario non letterale.
- **Correzione / suggerimento:** Opz. ripetere con `Rete2Layer(d=..., h=8)` → load su `h=16` per allinearti all’esempio del capitolo.
- **Pattern errore / ID contesto:** soft #6 (lettera consegna vs spirito)

### 2026-08-07 — Sez.6 [LIBRO] checkpoint dict §13.6.6 (`07_pytorch_intro.py` ~1134–1180)

- **Esercizio / blocco:** Salvare dict con `model_state` + metadati; ricaricare via `["model_state"]`; allclose predizioni
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**
- **Punti di forza:** Costruisci correttamente `out_dict` (`model_state`, `nota`, `d`, `h`); `Rete2Layer` coerente; seed; assert allclose su output.
- **Errori / lacune:** Salvi ancora lo **state_dict nudo** (`torch.save(modello.state_dict(), ...)`) invece di `torch.save(out_dict, ...)`; al load non usi `torch.load(...)["model_state"]`. Il dict stampato non entra nel file — obiettivo esercizio non raggiunto.
- **Correzione / suggerimento:** `torch.save(out_dict, percorso)` → `ckpt = torch.load(..., map_location="cpu")` → `load_state_dict(ckpt["model_state"])` (opz. ricostruisci con `ckpt["d"]`, `ckpt["h"]`).
- **Pattern errore / ID contesto:** #6 consegne (dict costruito ma non salvato/usato)
- **Rivalutazione post-fix (2026-08-07):** `torch.save(out_dict, ...)` + `load(...,)['model_state']` + allclose → **9.5/10**. Opzionale residuo: ricostruire `Rete2Layer` da `ckpt["d"]`/`ckpt["h"]`.

### 2026-08-11 — CONFRONTO PRIMA/DOPO migrato da cap.06 (`07_pytorch_intro.py` ~1186–1204)

- **Esercizio / blocco:** Commento 8–10 righe: neurone → magia loss → derivate/backprop → cosa hai afferrato → aspettative PyTorch + bonus accuracy
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** Tutti i punti toccati; filo coerente (shape → BCE numerica → derivata/responsabilità → ciclo train completo → API PyTorch = cap.06 sotto il cofano); bonus accuracy random ~0.5 vs addestrata ~1 corretto a grandi linee.
- **Errori / lacune:** Troppo sintetico vs “8–10 righe” richieste; typo `paramentro`/`addestamento`; su PyTorch manca ½ frase sul fatto che `backward`/`optim.step` nascondono chain rule ma non la sostituiscono concettualmente; bonus: “~1” solo su casi facili/perfetti — meglio “molto sopra 0.5 / alta se il problema è lineare-separabile”.
- **Correzione / suggerimento:** Espandi ogni bullet a 1–2 frasi concrete (es. shape `(N,)` vs `(N,1)`; BCE vs accuracy; GD = update dopo i gradienti).
- **Pattern errore / ID contesto:** soft #6 (lunghezza/completezza consegna)

### 2026-08-11 — SCALER + TRAIN spirito TODO 18 (`07_pytorch_intro.py` ~1208–1314)

- **Esercizio / blocco:** Commento raw vs scaled + fit scaler solo train; 2 modelli uguali, 20 epoche, confronta loss finale
- **Valutazione (primo tentativo — "voto esame"):** **5/10**
- **Punti di forza:** Scaler corretto (mean/std solo su `X_train`, applicato al test); idea raw vs scaled; loop training strutturato; drop ID/target ok.
- **Errori / lacune:** (1) **Stesso** `modello`/`ottimizzatore` per entrambi i run — dopo 20 epoche raw continui sul modello già allenato, poi solo **5** epoche scaled → confronto non valido. Serve **due** reti (stesso seed/init). (2) Consegna: **20** epoche per entrambi. (3) Commento ~2 righe, non 5–8. (4) `somma_losses += loss` senza `.item()`. (5) “Loss iniziale” con indice `[1]` invece di `[0]`. (6) Type hint `d = int` → `d: int`.
- **Correzione / suggerimento:** `torch.manual_seed(0); modello_raw=...` poi `torch.manual_seed(0); modello_scaled=...` (due optimizer); entrambi `range(20)`; commento più lungo su loss iniziale/convergenza.
- **Pattern errore / ID contesto:** #6 consegne; soft leak confronto sperimentale (modello condiviso)
- **Rivalutazione post-fix (2026-08-11):** due modelli + seed×2 + 20 epoche + `.item()` + type hint → **8.5/10**. Residui: print “iniziale” usa `[1][0]` (indice epoca, non loss) → deve essere `[0][1]`; commento ancora ~2 righe (servono 5–8).

### 2026-08-13 — DRIFT REAL-WORLD spirito TODO 19 (`07_pytorch_intro.py` ~1325–1351)

- **Esercizio / blocco:** 3 ipotesi drift produzione + simula `X_test * 1.5` + confronta accuracy (+ spiegazione se resta alta)
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Tre ipotesi solide (scanner/qualità OCR, shift popolazione clienti, cambio abitudini); simula `* 1.5`; ricarica pesi scaled; misura un degrado.
- **Errori / lacune:** (1) Consegna chiede **accuracy**, hai usato solo **BCE/loss**. (2) Confronti loss su test driftato vs **ultima loss di train** → non è lo stesso set/regime. Serve acc (o loss) **prima** su `X_test_scaled` e **dopo** su `*1.5`. (3) Manca la spiegazione “se resta alta, perché `*1.5` può non bastare sul toy”. (4) Typo: puà/consueguenza/clieni.
- **Correzione / suggerimento:** `(pred >= 0.5) == y` mean su test pulito vs driftato; commento su scala relativa / linearità del toy.
- **Pattern errore / ID contesto:** soft #6 (metrica chiesta vs metrica usata)

### 2026-08-13 — TODO 1 [COLLOQUIO] (`07_pytorch_intro.py` ~1370–1381)

- **Esercizio / blocco:** (1) autograd 2 frasi (2) Dataset vs DataLoader (3) perché zero_grad
- **Valutazione (primo tentativo — "voto esame"):** **6/10**
- **Punti di forza:** Idea giusta su zero_grad (accumulo); Dataset≈dati, DataLoader≈come li servi a batch.
- **Errori / lacune:** (1) Autograd troppo corto/impreciso: non è “il gradiente”, è il motore che **costruisce il grafo** e calcola i gradienti con `backward` (chain rule automatica). Serve **2 frasi**. (2) DataLoader non è solo “organizzazione interna”: **batch**, shuffle, iterazione per step. (3) Accumulo è **per step/batch**, non “ogni epoca”; senza zero_grad sommi i `.grad` tra batch dello stesso (o di più) step → update sbagliato.
- **Correzione / suggerimento:** Autograd = traccia operazioni → `backward` riempie `.grad`; Dataset = `__getitem__`/campione; DataLoader = mini-batch + shuffle; zero_grad prima di ogni nuovo step.
- **Pattern errore / ID contesto:** soft colloquio (precisione lessicale)

### 2026-08-13 — TODO 2 [REFACTORING] rete 2-layer PyTorch (`07_pytorch_intro.py` ~1384–1402)

- **Esercizio / blocco:** `nn.Module` ReLU+sigmoid, BCE, SGD; confronto mentale NumPy; bonus BCEWithLogitsLoss + stabilità (#42)
- **Valutazione (primo tentativo — "voto esame"):** **4.5/10**
- **Punti di forza:** Scheletro architettura ok: `Linear(d,h)` → ReLU → `Linear(h,1)` → sigmoid + `squeeze(-1)` (coerente con BCE su probabilità).
- **Errori / lacune:** (1) Manca `super().__init__()` in `__init__` → `nn.Module` non registrato bene (bug tipico). (2) Consegna chiede anche **BCE + SGD** (training loop) — assente. (3) Nessun confronto mentale con `train_rete_2_layer` NumPy. (4) Bonus BCEWithLogitsLoss (logit in uscita, no sigmoid nel forward) + 1 riga stabilità/#42 — assente.
- **Correzione / suggerimento:** `super().__init__()`; poi mini-loop come sez.5; bonus: `return z.squeeze(-1)` + `BCEWithLogitsLoss` (sigmoid+BCE fusi, più stabili numericamente / clip).
- **Pattern errore / ID contesto:** #6 consegna incompleta; soft nn.Module init
- **Rivalutazione post-fix (2026-08-13):** `super().__init__()` + loop SGD + y binario + spiegazione stabilità ok → **7/10**. Bloccante: `nn.BCEwithlogits()` non esiste → `nn.BCEWithLogitsLoss()`. Residui: `append(..., loss)` senza `.item()`; percorso “BCE+sigmoid” della consegna base non mostrato (solo bonus logit); confronto mentale esplicito con NumPy cap.06 ancora debole.
- **Rivalutazione 2 (2026-08-13):** nome loss corretto → ma **regressione**: `loss = criterio(...).item()` **prima** di `backward` → `float` non ha `.backward()` (crash). Ordine: `loss = criterio(...); loss.backward(); append(..., loss.item())`. Voto aggiornato **6/10** (peggio del 7 per il bug sul grafo).
- **Rivalutazione 3 (2026-08-13):** ordine loop corretto (`loss` Tensor → `backward` → `.item()` → `step`) → **9/10**. Residui soft: niente percorso esplicito sigmoid+`BCELoss`; confronto mentale NumPy cap.06 solo implicito (manca 1 frase forward/cache vs autograd).

### 2026-08-13 — TODO 3 [DEBUG] (`07_pytorch_intro.py` ~1427–1438)

- **Esercizio / blocco:** Scegli 2 bug tipici A–D e spiega la fix
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Hai scelto A e B; su A l’idea `zero_grad` è corretta; su B capisci che tensore e modello devono stare sullo stesso device.
- **Errori / lacune:** (A) Non basta “prima del ciclo”: va **a ogni step/batch**, non solo all’inizio. (B) Fix tipica: `device = "cuda" if torch.cuda.is_available() else "cpu"` poi `modello.to(device)` e `xb = xb.to(device)` (stesso device); in test spesso tutto su CPU con `map_location="cpu"` — la frase “cuda in training e cpu o cuda su entrambi in test” è confusa. Soft typo “il fase”.
- **Correzione / suggerimento:** A: `optimizer.zero_grad()` ogni iterazione del batch. B: un solo `device` condiviso; errore tipico = `X.cuda()` ma modello ancora su CPU.
- **Pattern errore / ID contesto:** soft precisione colloquio/debug

### 2026-08-13 — TODO 4 [RETRIEVAL] backward 5 step (`07_pytorch_intro.py` ~1437–1445)

- **Esercizio / blocco:** 5 step backward 2-layer a parole (dZ2→…→grad_W1); completare “in PyTorch li fa ______”
- **Valutazione (primo tentativo — "voto esame"):** **5.5/10**
- **Punti di forza:** Idea chain rule verso `grad_W1` presente (`dL/dp … dZ1/dW1`).
- **Errori / lacune:** Non sono i **5 step** operativi del cap.06 (dZ2 → grad_W2/b2 → dH → dZ1 via ReLU → grad_W1/b1): è una sola formula compressa. Fill-in sbagliato: non `auto_grad()` → **`loss.backward()`** / motore **autograd**. Manca ReLU (maschera) e i gradienti del layer 2.
- **Correzione / suggerimento:** Elenca 5 bullet: (1) dZ2 (2) dW2/db2 (3) dH (4) dZ1=dH⊙ReLU' (5) dW1/db1; PyTorch: `loss.backward()`.
- **Pattern errore / ID contesto:** retrieval compresso; soft naming API

### 2026-08-13 — Quiz verifica V1–V3 (`07_pytorch_intro.py` ~1495–1507)

- **Esercizio / blocco:** V1 requires_grad; V2 Linear X@W.T+b; V3 ordine loop
- **Valutazione (primo tentativo — "voto esame"):** **8/10** (V1 6, V2 10, V3 10)
- **Punti di forza:** V2 corretto (convenzione weight); V3 ordine giusto `zero_grad → forward+loss → backward → step`.
- **Errori / lacune:** V1 troppo corto: non è solo “richiedere il gradiente”, è dire a PyTorch di **tracciare le operazioni** su quel tensore per poter fare `.backward()` / riempire `.grad`.
- **Correzione / suggerimento:** V1 modello: “`requires_grad=True` → tensore sorvegliato: autograd costruisce il grafo e calcola i gradienti al backward.”
- **Pattern errore / ID contesto:** —

### 2026-08-13 — Quiz verifica V4 (`07_pytorch_intro.py` ~1508–1511)

- **Esercizio / blocco:** Errore concettuale “Autograd sostituisce il gradient descent”
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Distingue calcolo gradienti (autograd/backward) vs update pesi (`optimizer.step()`).
- **Errori / lacune:** Soft: `step()` non “sostituisce” il GD — **è** l’implementazione del GD (o Adam, ecc.). Autograd non sostituisce nulla del GD: fornisce i `.grad` che il GD usa.
- **Correzione / suggerimento:** “Autograd calcola i gradienti; GD/Adam aggiornano i pesi.”
- **Pattern errore / ID contesto:** soft backprop vs GD (già visto)

### 2026-08-13 — Quiz verifica V5–V6 (`07_pytorch_intro.py` ~1512–1519)

- **Esercizio / blocco:** V5 `map_location="cpu"`; V6 Feynman DataLoader
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10** (V5 5.5, V6 7)
- **Punti di forza:** V5 idea “dove caricare”; V6 analogia magazziniere/efficienza nella direzione giusta.
- **Errori / lacune:** V5 troppo generica: il punto del corso è **pesi salvati su GPU (Colab) → caricati su CPU (il tuo PC senza CUDA)**. V6 manca il pezzo operativo da Feynman: **pacchetti/batch**, eventuale mescola, te li porta uno alla volta (carrello/paginatore).
- **Correzione / suggerimento:** V5: remap device al load. V6: “prende N esempi dallo scaffale, li mette sul carrello, te li porta a pacchetti.”
- **Pattern errore / ID contesto:** soft #6 completezza risposta

### 2026-08-03 — Revisione capitolo (richiesta studente)

- **Motivo:** confusione sul passaggio NumPy → PyTorch.
- **Fatto:** file riscritto con schema fisso per sezione (analogia → codice NumPy cap.06 → codice PyTorch → cosa cambia → tranelli → mini-esercizio), **dizionario di traduzione NumPy↔torch**, blocco 🔁 **#44** eseguibile (analitico vs numerico con `assert`), spiegazioni su dtype float64/32, `from_numpy` vs `tensor`, `device`, accumulo `.grad`, `weight (out,in)`, batch/step/epoca, tabella loop cap.06↔cap.07, `state_dict`.
- **Nuovi mini:** 1.3, 1.4, 2.3, 3.2, 3.3, 4.2, 5.2, 6.2 + micro 44.A/44.B.
- **Infrastruttura:** `try/except Exception` (l'import torch in locale dà `OSError WinError 126`, non `ImportError`) + stop pulito con messaggio "usa Colab"; risposte studente conservate.
- **Verifica:** file eseguito in locale → rinforzi NumPy ok, sanity check `assert` passa, stop pulito (exit 0).

### 2026-08-14 — TODO 5 INTERLEAVING Dataset+loop (`07_pytorch_intro.py` ~1482–1526)

- **Esercizio / blocco:** CSV → MioDataset → DataLoader → Sequential → 1 epoca BCEWithLogits
- **Valutazione (primo tentativo — "voto esame"):** **7/10** (Dataset ok dopo fix `Dataset`/`__getitem__`; loop inizialmente su `X,y` interi invece di `xb,yb`)
- **Fix applicato (post-feedback):** `z = min_model(xb).squeeze(-1)` + `crit(z, yb)` — pipeline coerente.
- **Stato attuale (rivalutazione post-fix):** **9/10** — filo end-to-end corretto; soft: accuracy opzionale non stampata; media loss per n. batch (ok smoke test).
- **Pattern errore / ID contesto:** confusione iniziale Dataset vs `nn.Module`; uso batch vs full tensor

### 2026-08-22 — Bridge M03_R07 Q2 completa `.grad` (hint richiesto)

- **Esercizio / blocco:** dopo `loss.backward()`, dove stanno i gradienti?
- **Nota:** studente non ricordava → hint/soluzione data in chat (non voto esame a freddo).
- **Risposta attesa:** attributo **`.grad`** su ogni parametro (es. `param.grad` / `model.weight.grad`).
- **Pattern:** retrieval API PyTorch (collegato soft a #45 naming backward)

### 2026-08-22 — Bridge M03_R07 Q3 pathlib vs `\`

- **Esercizio / blocco:** perché preferire `Path(...) / "dati"` a concatenare `\` a mano
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Idea corretta: separatori/path diversi tra OS; meglio qualcosa di portabile.
- **Errori / lacune:** Soft lessico: `pathlib` non è “un linguaggio”, è il modulo/classe Python che normalizza i path. Concetto operativo ok.
- **Correzione / suggerimento:** “`Path` gestisce i separatori al posto tuo (Windows/Linux/Mac).”

### 2026-08-22 — Bridge M03_R07 Q4 prevedi `a[0]` dopo `b=a*2; b[0]=99`

- **Esercizio / blocco:** output di `print(a[0])`
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Risposta **1.0** corretta: `b = a * 2` crea un **nuovo** array; modificare `b` non tocca `a`.
- **Errori / lacune:** nessuno
- **Correzione / suggerimento:** (nota per dopo) attenzione a viste/slice NumPy e `from_numpy`/`tensor` che possono condividere memoria — qui la moltiplicazione copia.

### 2026-08-22 — Bridge M03_R07 Q5 Pandas read_csv

- **Esercizio / blocco:** due righe import + `read_csv("train.csv")` → `df`
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `import pandas as pd` + `pd.read_csv(...)` + DataFrame in `df` — corretto.
- **Errori / lacune:** Soft: la consegna chiedeva **due** righe; hai usato tre (path intermedio). Equivalente e anzi più pulito.
- **Correzione / suggerimento:** forma minima: `df = pd.read_csv("train.csv")` subito dopo l’import.

### 2026-08-22 — Bridge M03_R07 Q6 target random ogni volta

- **Esercizio / blocco:** problema didattico del snippet con `y` random a ogni forward
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Capisce che il target non è stabile e che il confronto non misura un apprendimento reale.
- **Errori / lacune:** Soft: non è che il GD sia “impossibile” (i gradienti esistono e i pesi si muovono); è che **non c’è supervisione vera** — la loss non misura progresso verso un pattern fisso/utile.
- **Correzione / suggerimento:** “Target casuale ≠ etichette reali; stai inseguendo un bersaglio che cambia ogni volta.”
- **Fix applicato (chat):** raffinato — “il gradiente funziona, ma la loss non scende in modo sensato perché il target cambia.”

### 2026-08-22 — Bridge M03_R07 Q7 cuda False su Mac/AMD

- **Esercizio / blocco:** perché `cuda.is_available()` è False in locale Mac/AMD
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Idea giusta: in locale quella GPU non serve (per CUDA) all’addestramento PyTorch tipico.
- **Errori / lacune:** Manca il pezzo chiave: **CUDA = stack NVIDIA**. AMD/Mac non espongono CUDA a PyTorch come una GPU NVIDIA; il codice è ok, il hardware/runtime no → cade su `"cpu"` (o Colab NVIDIA).
- **Correzione / suggerimento:** “False non = bug nel codice; = niente CUDA disponibile su questa macchina.”
- **Pattern errore / ID contesto:** soft #46 device / Colab

### 2026-08-22 — Bridge M03_R07 Q8 dict hyperparameter

- **Esercizio / blocco:** `hp` + `epochs` con `int` sicuro
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** Dict corretto; `int(hp['epochs'])` è esattamente l’idioma atteso (cast esplicito → tipo int sicuro anche se il valore arrivasse come stringa/`float` da config).
- **Errori / lacune:** Nessuno sostanziale. Soft stile: spazio `"lr" :` e indentazione del blocco nel markdown.
- **Correzione / suggerimento:** Opzionale: `hp.get("epochs", 5)` se vuoi default; qui la consegna non lo chiedeva.

### 2026-08-22 — Bridge M03_R07 Q9 Dataset vs DataLoader (Feynman)

- **Esercizio / blocco:** differenza Dataset (cosa contiene) vs DataLoader (cosa fa nel loop)
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** DataLoader: idea giusta — organizza, batch size, shuffle, fornisce i pezzi al training.
- **Errori / lacune:** Dataset **non** è “l’intero batch”: è la collezione di **campioni** (es. riga `X[i], y[i]` / `__getitem__`). Il **batch** lo costruisce il DataLoader. Soft: “modo che non gli specifichiamo” → in realtà **glielo specifichi** (`batch_size`, `shuffle`, …).
- **Correzione / suggerimento:** Dataset = scaffale di esempi; DataLoader = carrello che prende N pezzi, eventualmente mescola, e li porta al loop.
- **Pattern errore / ID contesto:** residuo soft **#46** (DataLoader/batch Feynman)
- **Fix applicato / rivalutazione (post-feedback, richiesta esplicita):** **8.5/10** — Dataset ora correttamente “collezione” (non più “intero batch”). Resta soft: “modo che **non** gli specifichiamo” → glielo **specifichi** (`batch_size`, `shuffle`); e DataLoader **costruisce i batch** per il loop, non solo “organizza il set”.

### 2026-08-22 — Bridge M03_R07 Q10 slicing primo esempio batch

- **Esercizio / blocco:** `x.shape (32,3,28,28)` → primo esempio shape `(3,28,28)`
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `X[0]` toglie la dimensione batch N → `(3,28,28)` come richiesto (equivalente a `x[0]` / `x[0, ...]`).
- **Errori / lacune:** Soft naming: nella consegna il tensore si chiama `x` minuscolo; non cambia il concetto.
- **Correzione / suggerimento:** Evitare `X[0:1]` se vuoi shape `(3,28,28)` — quello lascia N=1 → `(1,3,28,28)`.

### 2026-08-22 — Bridge M03_R07 Q11 retrieval 5-step backward (#45)

- **Esercizio / blocco:** catena `dZ2 → … → grad_W1` + fill-in PyTorch
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Ordine corretto e completo: `dZ2≈p−y` → `dW2/db2` → `dH` → `dZ1` via ReLU′ → `dW1/db1`. Recupero forte rispetto a TODO 4 compresso.
- **Errori / lacune:** (1) **Manca il fill-in** “In PyTorch questi step li fa ______.” → atteso **`loss.backward()`** / **autograd** (era il bug tipico `auto_grad()`). (2) Soft: spesso `dZ2` è `(p−y)/N` se la loss è media sul batch.
- **Correzione / suggerimento:** Completare il blank prima di chiudere #45.
- **Pattern errore / ID contesto:** #45 — catena 🟢 in miglioramento; fill-in ancora da verificare
- **Fix fill-in (post-feedback):** scritto “`.autograd()`” → **non corretto**. Atteso: **`loss.backward()`** (oppure “**autograd**” come motore, non un metodo `.autograd()`). Stesso pattern di TODO 4 (`auto_grad`). Catena resta ok; #45 resta 🟡 finché non fissa `backward`.
- **Rivalutazione (post-fix, richiesta esplicita):** **9.5/10** — fill-in ora **`loss.backward()`** corretto. Soft residuo: `(p−y)/N` se loss = mean. **#45** → 🟡 in miglioramento (chiusura a freddo al quiz ingresso cap.08).

### 2026-08-22 — Bridge M03_R07 Q12 Pattern #27 Micro 27.A

- **Esercizio / blocco:** `p*(1-p)` vs `p*(1-y)` — quale corretta e perché
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Scelta **B** corretta; descrive bene il comportamento numerico di A (`y=1→0`, `y=0→p`).
- **Errori / lacune:** Manca il perché concettuale: la derivata della sigmoid dipende da **`p`**, non dall’etichetta **`y`**. A è il bug tipico #27 (simbolo sbagliato in formula→codice).
- **Correzione / suggerimento:** “A mescola probabilità e label; B è σ′(z)=p(1−p).”
- **Pattern errore / ID contesto:** #27 — micro ok sulla scelta; resta 🔴 sul perché “simbolo sbagliato”

### 2026-08-22 — Bridge M03_R07 Q13 zero_grad V/F

- **Esercizio / blocco:** `zero_grad` una volta prima del `for epoch`?
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** **Falso** corretto; motivo giusto = i `.grad` **si accumulano** e `step()` userebbe la somma.
- **Errori / lacune:** Soft frequenza: non solo “ogni epoch”, ma **ogni batch/step** (prima di ogni `backward`), altrimenti anche i batch nella stessa epoch si sommano.
- **Correzione / suggerimento:** Loop tipico: `zero_grad` → forward → loss → `backward` → `step` (ripeti per ogni batch).

### 2026-08-22 — Bridge M03_R07 Q14 map_location (#46)

- **Esercizio / blocco:** `torch.load(..., map_location=?)` Colab GPU → PC AMD
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Blank `"cpu"` (nel codice) + motivo hardware: AMD ≠ NVIDIA/CUDA — direzione corretta.
- **Errori / lacune:** Soft precisione: non solo “non c’è CUDA”, ma **i tensori del checkpoint sono stati salvati su device CUDA**; `map_location` li **rimappa** su CPU altrimenti il load prova a ricrearli su una GPU CUDA assente.
- **Correzione / suggerimento:** Una frase modello: “Metto `\"cpu\"` per rimappare i pesi da CUDA (Colab) alla CPU di casa.”
- **Pattern errore / ID contesto:** #46 — in miglioramento su map_location

---

## Lacune e dubbi ancora aperti (ereditati)

- 🟢 **#44** sanity check = analitico vs numerico (chiusa Micro 44.A)
- 🟢 **#42** clip BCE su `p` (chiusa)
- 🟢 **#43** scaler parentesi (chiusa)
- 🔴 Pattern #27 formula→codice — **riemerso** Micro 27.A: `(1-y)` invece di `(1-p)` → migrato cap.08/R07
- 🟡 **#45** retrieval 5-step + `loss.backward()` — R07 Q11 post-fix ok (9.5); primo fill-in era `.autograd()` → verificare a freddo quiz ingresso 08
- 🟡 **#46** map_location + DataLoader — R07 Q14 map_location ok (8.5); DataLoader soft da Q9 → quiz ingresso 08
- ✅ TODO 5 INTERLEAVING chiuso (14/08/2026, post-fix 9/10)
- ⚠️ TODO 6 REAL-WORLD / 🏗️ progetto M3-07 — ancora aperti
- 🟢 soft backprop vs GD: chiuso a Q8 post-feedback (primo tentativo ancora 6.5)

---

## Note per il capitolo successivo (mentor)

- Bridge **M03_R07** (es. 11–15) prima di scrivere/studiare cap.08
- Scrivere `08_cnn_computer_vision.py` da segnaposto (Fashion-MNIST, Colab); no buste paga
- Privacy/GDPR buste paga resta bloccante dal cap.09 in poi
