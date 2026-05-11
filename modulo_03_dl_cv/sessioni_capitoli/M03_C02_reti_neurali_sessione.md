# Diario sessione — Capitolo 02 — Reti neurali da zero

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `02_reti_neurali.py` |
| **File diario** | `M03_C02_reti_neurali_sessione.md` |
| **Stato** | in corso |
| **Voto difficoltà** | — / X/10 (atteso 7/10) |

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

### [YYYY-MM-DD] — Riferimento (placeholder)

- **Esercizio / blocco:** …
- **Valutazione (primo tentativo — "voto esame"):** **X/10**.
- **Punti di forza:** …
- **Errori / lacune:** …
- **Correzione / suggerimento:** …
- **Pattern errore / ID contesto** (se applicabile): …

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se il TODO 1.1 evidenzia ancora confusione sulle shape `(N, d) @ (d, h) -> (N, h)`, **bloccare** prima di passare alla Sez. 2.
- Se l'`init_pesi_he` non viene compreso (perche' `sqrt(2/d)` e non `0.01`?), recuperare prima del cap.03 M3 (li' si parla di vanishing/exploding gradient).
- Verificare che TODO 2.2 (collasso lineare a 3 layer) sia eseguito DA SOLO: e' il check che la regola R2 e' stata davvero capita.
- Per il cap.03 M3 (backpropagation): partire dalla rete 2-layer di questo capitolo e introdurre il **training** (loss + gradient descent + backward). NON saltare il capitolo se questo non e' chiuso 8+/10.

---

## Note tecniche di stesura (mentor)

- _(da popolare quando il capitolo verra' aperto e lavorato)_
