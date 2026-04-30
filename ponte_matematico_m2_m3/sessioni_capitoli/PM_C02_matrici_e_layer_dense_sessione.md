# Diario sessione — Capitolo 02 — Matrici e Layer Dense (Ponte Matematico)

| Campo | Valore |
|-------|--------|
| **Modulo** | Ponte Matematico (bridge M2 → M3) |
| **File capitolo** | `02_matrici_e_layer_dense.py` |
| **File diario** | `PM_C02_matrici_e_layer_dense_sessione.md` |
| **Stato** | in corso (avvio: 30/04/2026) |
| **Voto difficoltà** | — (assegnato in chiusura) |

---

## Obiettivi del capitolo (per il mentor)

- Costruire il ponte concettuale **vettore (cap.01) → matrice (cap.02)**: una matrice = un batch di pratiche.
- Far interiorizzare la regola del prodotto matrice-vettore (`X @ w + b`) come "N dot product in parallelo" → motivazione per GPU/batch in M3.
- Anticipare il **layer Dense** di una rete neurale come "trasformazione affine `X @ W + b` con W matrice" → preludio diretto a M3.
- **Rinforzare i 3 pattern emersi nel cap.01**:
  1. **Pattern #23** — virgole a fine chiamata creano tuple inutili
  2. **Pattern #24** — `iloc` (numerico) vs `loc` (etichetta)
  3. **Pattern #25** — `np.array` (factory) vs `np.ndarray` (tipo)
- Verificare la **retention dei 5 blocchi del cap.01** (richiesto esplicitamente dallo studente in auto-rating C4 cap.01) tramite la sezione "RIPASSO 5 BLOCCHI": vettori+shape, operazioni base, dot product, norma, coseno.
- Verificare al quiz d'ingresso che **Lacuna #12 (NumPy shape/reshape)** sia consolidata (era 🟢 già nel cap.01, ma il cap.02 e' un test naturale aggiuntivo).

---

## Domande durante lo studio

- _(template — il mentor le aggiungerà man mano)_
- **Q:** …
  **Nota / risposta sintetica:** …

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `02_matrici_e_layer_dense.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [YYYY-MM-DD] — Quiz d'ingresso Q1-Q8 (cerniera cap.01 Ponte)

- **Blocco:** `02_matrici_e_layer_dense.py` — Quiz d'ingresso (Q1: norma; Q2: coseno parallelo; Q3: dot product; Q4: V/F coseno=1 ⇒ vettori uguali; Q5: shape `(3,)` vs `(1,3)`; Q6: type hint `np.ndarray`; Q7: trova errore `iloc` con stringa; Q8: Feynman norma vs coseno).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** verifica retention cap.01 + cerniera Pattern #24 (Q7) e #25 (Q6).

### [YYYY-MM-DD] — Rinforzo Pattern #23 (virgole → tuple)

- **Blocco:** `02_matrici_e_layer_dense.py` — sezione RINFORZO Pattern #23.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Pattern #23 (chiusura mirata).

### [YYYY-MM-DD] — Rinforzo Pattern #24 (iloc vs loc)

- **Blocco:** `02_matrici_e_layer_dense.py` — sezione RINFORZO Pattern #24.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Pattern #24 (chiusura mirata).

### [YYYY-MM-DD] — Rinforzo Pattern #25 (np.array vs np.ndarray)

- **Blocco:** `02_matrici_e_layer_dense.py` — sezione RINFORZO Pattern #25.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** Pattern #25 (chiusura mirata).

### [YYYY-MM-DD] — Ripasso 5 blocchi cap.01 (R1-R5)

- **Blocco:** `02_matrici_e_layer_dense.py` — sezione RIPASSO 5 BLOCCHI.
- **Valutazione (primo tentativo — "voto esame"):** —/10 per blocco.
  - R1 (vettori+shape): —/10
  - R2 (operazioni base): —/10
  - R3 (dot senza np.dot): —/10
  - R4 (norma senza np.linalg.norm): —/10
  - R5 (coseno mentale): —/10
- **Note retention:** se uno dei 5 blocchi è <7/10, registrarlo come lacuna nel contesto e programmare ripasso aggiuntivo.

### [YYYY-MM-DD] — Sezione 1.1 (matrice batch da CSV)

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 1.1 (carica CSV M2, costruisci X delle prime 5 pratiche).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 1.2 (vettore-riga vs vettore-colonna)

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 1.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 2.1 (`punteggio_batch(X, w, b)`)

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 2.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note ponte M2:** verificare che lo studente colleghi `X @ w + b` a "tutti i `z` del cap.06 calcolati in un colpo solo".

### [YYYY-MM-DD] — Sezione 2.2 (lento vs veloce + benchmark)

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 2.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Sezione 3.1 (`layer_dense(X, W, b)`)

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 3.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note ponte M3:** verificare che lo studente colleghi `X @ W + b` al "primo layer di una rete neurale".

### [YYYY-MM-DD] — Sezione 3.2 (interpretazione W come "h regressioni in parallelo")

- **Blocco:** `02_matrici_e_layer_dense.py` — Sez. 3.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Quiz di verifica V1-V8

- **Blocco:** `02_matrici_e_layer_dense.py` — Quiz di verifica (V1: shape `X@w`; V2: shape + n. moltiplicazioni; V3-V4: trova errore; V5: V/F Dense=regressione; V6: perche' batch e' veloce; V7: trasposta; V8: Feynman rete=sequenza prodotti).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Esercizio E1 [COLLOQUIO] - softmax

- **Blocco:** `02_matrici_e_layer_dense.py` — E1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [YYYY-MM-DD] — Esercizio E2 [REFACTORING] - calcola_punteggi

- **Blocco:** `02_matrici_e_layer_dense.py` — E2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** verifica chiusura Pattern #23 e #25.

### [YYYY-MM-DD] — Esercizio E3 [DEBUG] - shapes not aligned

- **Blocco:** `02_matrici_e_layer_dense.py` — E3.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note:** scala progressiva NON applicabile (regola corso esercizio DEBUG); intervento solo dopo 2+ tentativi falliti.

### [YYYY-MM-DD] — Esercizio E4 [RETRIEVAL] - coseno from scratch

- **Blocco:** `02_matrici_e_layer_dense.py` — E4.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note retention:** se ricorda la funzione `coseno` del cap.01 senza guardare → incrementare contatore Glossario; altrimenti programmare nuovo retrieval nel cap.03.

### [YYYY-MM-DD] — Esercizio E5 [INTERLEAVING] - cap.06 M2 + matrici

- **Blocco:** `02_matrici_e_layer_dense.py` — E5.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note:** verificare comprensione del broadcasting NumPy (riusato nel layer Dense).

### [YYYY-MM-DD] — Mini-progetto guidato (`classifica_batch`)

- **Blocco:** `02_matrici_e_layer_dense.py` — sezione MINI-PROGETTO.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Note ponte:** preludio diretto al "batch inference" che vedremo in M3 (PyTorch DataLoader) e M5 (LLM batch API).

### [YYYY-MM-DD] — Checkpoint finale C1-C4

- **Blocco:** `02_matrici_e_layer_dense.py` — Checkpoint C1-C4.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **C4 auto-rating:** registrare i 5 voti su matrici/dot batch/Dense/ripasso/rinforzi per programmare il cap.03.

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se Pattern #23/#24/#25 sono confermati 🟢 al primo tentativo dei rinforzi, marcarli `🟢 Superato` in CONTESTO_CORSO.md.
- Se la retention dei 5 blocchi cap.01 è ≥8/10 media, NON serve un altro ripasso "5 blocchi" nel cap.03; altrimenti riproporre i blocchi deboli.
- Il cap.03 del Ponte Matematico (eventuale, da decidere se serve dopo il cap.02 o se si entra direttamente in M3) potrebbe trattare: gradiente come vettore di derivate, intuizione minimi/massimi su superfici 2D, preludio backpropagation. Decidere a fine cap.02 in base al voto difficoltà.
- Domini concreti già usati: feature `[importo, giorni, tasse, irpef, contributi]` (CSV M2). Riutilizzabili per M3 (training rete neurale binaria sulle stesse feature → comparare con LogisticRegression cap.06 M2).
