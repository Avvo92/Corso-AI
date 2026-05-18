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
