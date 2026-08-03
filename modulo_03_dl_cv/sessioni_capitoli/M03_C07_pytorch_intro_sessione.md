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

---

## Lacune e dubbi ancora aperti (ereditati)

- 🟡 **#44** sanity check = analitico vs numerico (Q4 ingresso)
- 🔴 #42 clip BCE su `p` non su `z`
- 🔴 #43 scaler `(X-mean)/std`
- 🔴 Pattern #27 formula→codice
- 🟡 soft: backprop vs GD (da verificare in Q8 / TODO 1)

---

## Note per il capitolo successivo (mentor)

- Dopo cap.07 → bridge R07 + `08_cnn_computer_vision.py`
- Privacy/GDPR buste paga resta bloccante dal cap.08/09 in poi
