# Diario sessione — Capitolo 01 — Vettori da zero (Ponte Matematico)

| Campo | Valore |
|-------|--------|
| **Modulo** | Ponte Matematico (bridge M2 → M3) |
| **File capitolo** | `01_vettori_da_zero.py` |
| **File diario** | `PM_C01_vettori_da_zero_sessione.md` |
| **Stato** | in corso (avvio: 27/04/2026) |
| **Voto difficoltà** | — (assegnato in chiusura) |

---

## Obiettivi del capitolo (per il mentor)

- Chiudere la **Lacuna #12** (NumPy shape/reshape) verificando l'acquisizione dopo M1 cap.07.
- Verificare in chiave "cerniera" che le **Lacune #16, #17, #18** restino 🟢 (Q1–Q3 del quiz d'ingresso).
- Introdurre il vocabolario nuovo (vettore, dot product, norma, coseno) con sequenza:
  **analogia → codice Python → grafico Matplotlib → formula in parole** (Regola 21).
- Costruire il **ponte mentale M2→M4/M6**: la riga `contrib = x_scaled * coef` del cap.06 = dot product;
  il coseno tra vettori = stessa idea della similarità con embeddings nei sistemi RAG.

---

## Domande durante lo studio

- _(template — il mentor le aggiungerà man mano)_
- **Q:** …
  **Nota / risposta sintetica:** …

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto.
> - Riferimento puntuale al blocco/righe del file `01_vettori_da_zero.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [YYYY-MM-DD] — Quiz d'ingresso Q1 (cerniera Lacuna #16)

- **Blocco:** `01_vettori_da_zero.py` — Quiz d'ingresso, Q1 (prob → score).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Punti di forza:** —
- **Errori / lacune:** —
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** Lacuna #16 (verifica acquisizione).

### [YYYY-MM-DD] — Quiz d'ingresso Q2 (cerniera Lacuna #17)

- **Blocco:** `01_vettori_da_zero.py` — Quiz d'ingresso, Q2 (drop colonne, leakage).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Lacuna #17 (verifica acquisizione).

### [YYYY-MM-DD] — Quiz d'ingresso Q3 (cerniera Lacuna #18)

- **Blocco:** `01_vettori_da_zero.py` — Quiz d'ingresso, Q3 (recall vs precision nel documentale).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Lacuna #18 (verifica acquisizione).

### [YYYY-MM-DD] — Quiz d'ingresso Q4 (vocabolario: vettore)

- **Blocco:** `01_vettori_da_zero.py` — Quiz d'ingresso, Q4 (spiega "pratica = vettore 5D" a un collega).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Quiz d'ingresso Q5 (ponte mentale: shape per `*`)

- **Blocco:** `01_vettori_da_zero.py` — Quiz d'ingresso, Q5 (shape di `x_scaled` e `coef`).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Rinforzo Lacuna #12 (NumPy shape/reshape)

- **Blocco:** `01_vettori_da_zero.py` — Micro-check Lacuna #12 (3x4 da 12 numeri, errore con (2,5)).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Lacuna #12 (chiusura formale prevista qui).

### [YYYY-MM-DD] — Sezione 1.1 (creazione vettori NumPy + shape/dtype)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 1.1 (3 vettori sul dominio).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 1.2 (ripasso shape `(3,)` vs `(1,3)`)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 1.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 2.1 (somma/sottrazione/scalare × vettore)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 2.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 2.2 (interpretazione `A − B` nel dominio)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 2.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 3.1 (`punteggio_lineare(x, w, b)` con dot product)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 3.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Ponte M2:** verificare che lo studente colleghi `dot(x, w) + b` a `z = sum(x_scaled * coef) + intercept` del cap.06.

### [YYYY-MM-DD] — Sezione 3.2 (cosa rappresenta ciascun `contrib[i]`)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 3.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 4.1 (`norma(v)` con `np.linalg.norm`)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 4.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [2026-04-29] — Sezione 4.1 (`norma(v)` con `np.linalg.norm`)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~578–586) — Sezione 4.1.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** usa `np.linalg.norm` come richiesto, fa `float(...)` esplicito, stampa 3 norme con label leggibili (output coerente).
- **Cosa migliorare:** type hint: `v: np.array` non è corretto (meglio `np.ndarray` o `numpy.typing.NDArray[...]`); naming leggermente diverso dalla consegna (`feature_pratica_A/B`), ma sostanza ok; attenzione all’indentazione (usa 4 spazi per consistenza).

### [YYYY-MM-DD] — Sezione 4.2 (grafico 2D con frecce + Pitagora)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 4.2 (Matplotlib, `quiver`/`annotate`).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note grafico:** verificare `set_aspect("equal")` per fedeltà delle lunghezze.

### [YYYY-MM-DD] — Sezione 5.1 (`coseno(a, b)` con controllo robusto)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 5.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Punti da controllare:** controllo `norma == 0` → `ValueError`; check `len(a) == len(b)`.

### [YYYY-MM-DD] — Sezione 5.2 (mini-task prodotto: coseno tra pratiche)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 5.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Ponte M4–M6:** verificare che lo studente colleghi il coseno tra pratiche al concetto di similarità tra embeddings nei sistemi RAG.

### [YYYY-MM-DD] — Checkpoint fine capitolo (C1–C5)

- **Blocco:** `01_vettori_da_zero.py` — Checkpoint C1–C5 (auto-verifica concettuale).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se la Lacuna #12 viene confermata 🟢 al primo tentativo del micro-check, segnalarlo in chiusura per chiudere formalmente l'**anomalia aperta cap.07 M1** (CONTESTO_CORSO.md → "Anomalia aperta").
- Pattern di errore da monitorare nel cap.02 del Ponte (matrici/dot generalizzato): confusione tra shape `(n,)` e `(1, n)`/`(n, 1)` nelle moltiplicazioni — è il bug più tipico quando si passa a layer Dense in M3.
- Se il coseno tra pratiche è chiaro a fine capitolo, il prossimo capitolo del Ponte può introdurre **matrici come "tante pratiche insieme"** e prodotto matrice-vettore (= classificare un batch in un colpo solo).
- Domini concreti già usati che si possono riusare: feature `[importo, giorni, tasse, irpef, contributi]` (coerente col mock CSV M2).
