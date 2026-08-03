# Diario sessione — Capitolo 07 — PyTorch intro

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `07_pytorch_intro.py` |
| **File diario** | `M03_C07_pytorch_intro_sessione.md` |
| **Stato** | aperto (03/08/2026) — creato in chiusura anticipata cap.06 |
| **Voto difficoltà** | — |

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

### 2026-08-03 — Revisione capitolo (richiesta studente)

- **Motivo:** confusione sul passaggio NumPy → PyTorch.
- **Fatto:** file riscritto con schema fisso per sezione (analogia → codice NumPy cap.06 → codice PyTorch → cosa cambia → tranelli → mini-esercizio), **dizionario di traduzione NumPy↔torch**, blocco 🔁 **#44** eseguibile (analitico vs numerico con `assert`), spiegazioni su dtype float64/32, `from_numpy` vs `tensor`, `device`, accumulo `.grad`, `weight (out,in)`, batch/step/epoca, tabella loop cap.06↔cap.07, `state_dict`.
- **Nuovi mini:** 1.3, 1.4, 2.3, 3.2, 3.3, 4.2, 5.2, 6.2 + micro 44.A/44.B.
- **Infrastruttura:** `try/except Exception` (l'import torch in locale dà `OSError WinError 126`, non `ImportError`) + stop pulito con messaggio "usa Colab"; risposte studente conservate.
- **Verifica:** file eseguito in locale → rinforzi NumPy ok, sanity check `assert` passa, stop pulito (exit 0).

---

## Lacune e dubbi ancora aperti (ereditati)

- 🟢 **#44** sanity check = analitico vs numerico (chiusa Micro 44.A)
- 🟢 **#42** clip BCE su `p` (chiusa)
- 🟢 **#43** scaler parentesi (chiusa)
- 🔴 Pattern #27 formula→codice — **riemerso** Micro 27.A: `(1-y)` invece di `(1-p)`
- 🟢 soft backprop vs GD: chiuso a Q8 post-feedback (primo tentativo ancora 6.5)

---

## Note per il capitolo successivo (mentor)

- Dopo cap.07 → bridge R07 + `08_cnn_computer_vision.py`
- Privacy/GDPR buste paga resta bloccante dal cap.08/09 in poi
