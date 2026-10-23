# Diario sessione — Capitolo 01 — Vettori da zero (Ponte Matematico)

| Campo | Valore |
|-------|--------|
| **Modulo** | Ponte Matematico (bridge M2 → M3) |
| **File capitolo** | `01_vettori_da_zero.py` |
| **File diario** | `PM_C01_vettori_da_zero_sessione.md` |
| **Stato** | **completato (30/04/2026)** |
| **Voto difficoltà** | **9/10** (confermato dallo studente in chiusura) |
| **Lacuna #12** | 🟢 Superata (uso intensivo `.shape`, `dtype`, dot product con shape coerenti) |
| **Pattern emersi** | #23 virgole→tuple, #24 iloc/loc, #25 type hint `np.array` vs `np.ndarray` (rinforzi nel cap.02 Ponte) |

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

### [2026-04-29] — Sezione 4.2 (grafico 2D con frecce + norme nel titolo)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~623–650) — Sezione 4.2.
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** `plt.subplots()` corretto; due `quiver` dall’origine con colori distinti; `set_aspect("equal")` ok; norme calcolate con `np.linalg.norm` e mostrate nel titolo; niente `plt.show()` (rispetta regola script/CI).
- **Cosa migliorare:** il blocco viola la regola “8–12 righe massimo” (è più lungo del necessario); `plt.savefig(...)` funziona ma è più robusto `fig.savefig(...)` + `plt.close(fig)`; opzionale: `os.makedirs("figures", exist_ok=True)` se la cartella non è garantita.
- **Fix applicato (post-feedback):** compresso a 6 righe e aggiunto `plt.close(fig)`; attenzione però: usare la virgola per “mettere più istruzioni su una riga” crea tuple ed è poco idiomatico (meglio 1 istruzione per riga o `;` se vuoi comprimere).

### [YYYY-MM-DD] — Sezione 5.1 (`coseno(a, b)` con controllo robusto)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 5.1.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Punti da controllare:** controllo `norma == 0` → `ValueError`; check `len(a) == len(b)`.

### [2026-04-30] — Sezione 5.1 (`coseno(a, b)` + visualizzazione con vettori normalizzati)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~736–813) — Sezione 5.1.
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** formula del coseno corretta; risultati dei 4 test richiesti corretti (1.0, 0.0, -1.0, 0.96); cast a `float(...)` presente.
- **Cosa manca rispetto alla consegna:** non hai implementato i 2 controlli robusti richiesti (norma zero → `raise ValueError`, shape diverso → `raise ValueError`).
- **Extra Matplotlib (buono come allenamento):** l’idea di normalizzare e disegnare le direzioni è coerente col concetto.
- **Nota stile/bug latenti:** attenzione alle virgole a fine riga tipo `ax.quiver(...),` e `ax.set_xlim(...), ax.set_ylim(...)`: creano tuple “inutili” e rendono il codice meno chiaro; inoltre `ax.set_xlim(-1, 1), ax.set_ylim(-1, 1)` non è equivalente a chiamarle su righe separate (anche se l’effetto collaterale spesso avviene).
- **Fix applicato (post-feedback):** aggiunti check `a.shape != b.shape` (ok) e check “vettore nullo” MA implementato come `a.sum() == 0` (bug): un vettore può avere somma 0 senza essere nullo (es. `[1, -1]`). Il check corretto è `np.linalg.norm(a) == 0` (o `== 0.0` con tolleranza).
- **Fix applicato (post-feedback 2):** corretto il check “vettore nullo” usando `np.linalg.norm(a) == 0` / `np.linalg.norm(b) == 0` (ora coerente con la consegna).

### [2026-04-30] — Sezione 5.1 (nuovo tentativo post-fix — voto finale richiesto)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~738–745) — funzione `coseno`.
- **Valutazione (post-fix / nuovo tentativo su richiesta):** **9/10**
- **Punti di forza:** controlli robusti corretti (norma zero + shape), formula corretta, cast a `float` presente; test base restano coerenti.
- **Cosa migliorare:** micro-ottimizzazione/leggibilità: controllare `a.shape` prima di calcolare le norme; e stile: messaggi `ValueError` coerenti con il testo della consegna (ma ok).
- **Fix applicato (post-feedback 3):** check `shape` spostato prima del calcolo delle norme (ora in ordine ideale); rimane ok.

### [YYYY-MM-DD] — Sezione 5.2 (mini-task prodotto: coseno tra pratiche)

- **Blocco:** `01_vettori_da_zero.py` — Sezione 5.2.
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Ponte M4–M6:** verificare che lo studente colleghi il coseno tra pratiche al concetto di similarità tra embeddings nei sistemi RAG.

### [2026-04-30] — Sezione 5.2 (mini-task prodotto: coseno(A,B) vs coseno(A,C) + ponte RAG)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~851–858) — Sezione 5.2.
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** `feature_C = feature_A * 1.05` è una scelta perfetta per “molto simile” (stessa direzione ⇒ coseno = 1.0); calcoli corretti (cos(A,B) ~ 0.84, cos(A,C) = 1.0); ponte RAG espresso correttamente (documenti/query come vettori e coseno come similarità).
- **Cosa migliorare:** le label stampate dicono “valori molto simili” ma il coseno misura soprattutto la **direzione/pattern** (non i valori assoluti); la soglia `> 0.84` è un po’ “magica” (ok come demo, ma meglio spiegare che è un esempio).

### [2026-04-30] — Mini-progetto guidato (top-k pratiche più simili con coseno)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~957–982) — mini-progetto.
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** struttura corretta (carica CSV → costruisci X → estrai query → loop → calcoli coseno → escludi query → ordini decrescente → `[:k]`); gestione errore `k` presente; output è nel formato richiesto `[(pratica_id, coseno), ...]`.
- **Cosa migliorare:** (1) la consegna chiedeva di usare la tua funzione `coseno` (5.1), qui hai riscritto la formula con `np.dot/np.linalg.norm`; (2) `k` andrebbe validato come `k > len(pratiche) - 1` (perché escludi la query); (3) `r_np = r.to_numpy(dtype=float)` per coerenza; (4) `y` è calcolata ma non usata.
- **Nota esecuzione (blocco esterno):** l’esecuzione completa del file può fermarsi prima del mini-progetto se `figures/` non esiste (savefig in 4.2) o se l’ambiente Python non ha `pandas` installato.
- **Fix applicato (post-feedback):** validazione `k > len(pratiche) - 1` corretta; `to_numpy(dtype=float)` coerente; uso della tua funzione `coseno(...)` come richiesto. Restano due finezze: (1) cast `pid = int(...)` per garantire `tuple[int, float]`; (2) coerenza `iloc` vs `loc` per la query (meglio usare `iloc` anche per `pratica_query` se `pratica_id_query` è posizione).

### [YYYY-MM-DD] — Checkpoint fine capitolo (C1–C5)

- **Blocco:** `01_vettori_da_zero.py` — Checkpoint C1–C5 (auto-verifica concettuale).
- **Valutazione (primo tentativo — "voto esame"):** —/10.

### [2026-04-30] — Checkpoint C1 (shape 1D vs 2D)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~866–868) — C1.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** risposta corretta: `(3,)` per array 1D, `(1, 3)` per array 2D con una riga.
- **Micro-precisazione:** `[[1,2,3]]` crea una matrice 1×3 (una “riga”), quindi molte operazioni (broadcast/dot) si comportano diversamente rispetto a `(3,)`.

### [2026-04-30] — Checkpoint C2 (dot product base)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~870–872) — C2.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** risultato numerico corretto (6) e spiegazione corretta: dot product = somma dei prodotti componente-per-componente (element-wise product + sum).

### [2026-04-30] — Checkpoint C3 (perché coseno non definito con norma 0)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~874–876) — C3.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** centrati entrambi i motivi: (1) divisione per zero nella formula \(dot / (||a||·||b||)\); (2) intuizione corretta: il vettore zero non ha direzione, quindi “angolo/coseno” non è definibile.

### [2026-04-30] — Checkpoint C5 (utilità del coseno in M4–M6 nel prodotto)

- **Blocco:** `ponte_matematico_m2_m3/01_vettori_da_zero.py` (righe ~883–887) — C5.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** concetto corretto: usare il coseno per confrontare pratiche/documenti “come vettori” e stimare somiglianza globale.
- **Cosa migliorare:** rendere l’esempio più concreto M4–M6: es. “dato un documento/pratica nuova, cerco i k documenti storici più simili (embedding + coseno) per recuperare casi analoghi e motivazioni/controlli già visti” (retrieval/RAG).

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- ✅ Lacuna #12 confermata 🟢 (uso autonomo di `.shape`, `dtype`, controlli early-exit, `to_numpy(dtype=float)`); anomalia cap.07 M1 chiusa per assorbimento.
- ⚠️ **Rinforzi obbligatori nel cap.02 Ponte** (richiesti dallo studente + emersi):
  1. **Pattern #23** — virgole a fine chiamata creano tuple inutili (`ax.quiver(...),`, `plt.savefig(...), plt.close(...)`). Mostrare cosa restituisce davvero (`type(...)` su una tupla `(None, None)`).
  2. **Pattern #24** — `iloc[i, "col_str"]` non funziona; `iloc` solo numerico, `loc` solo etichette. Tabella decisionale + esercizio.
  3. **Pattern #25** — `np.array` (factory) vs `np.ndarray` (tipo). Type hint corretti con `numpy.typing.NDArray`.
  4. **Sezione "RIPASSO 5 BLOCCHI"** richiesta esplicitamente (auto-rating in fondo al cap.01): 1 micro-esercizio (2-4 righe) per ognuno di vettori+shape, operazioni base, dot product, norma, coseno.
- Tema principale cap.02: matrici come "tante pratiche insieme" (batch); prodotto matrice-vettore come dot product generalizzato (`X @ w + b`); anteprima layer Dense (M3).
- Pattern di errore da monitorare nel cap.02: confusione tra shape `(n,)`, `(1, n)`, `(n, 1)` nelle moltiplicazioni — è il bug più tipico quando si passa a layer Dense in M3.
- Domini concreti riusabili: feature `[importo, giorni, tasse, irpef, contributi]` (coerente col mock CSV M2). Idea: caricare 5-10 pratiche reali dal CSV → costruire matrice X → calcolare `X @ w + b` per tutte in un colpo solo (efficienza batch).
- Voto difficoltà 9/10 → cap.02 deve essere **più guidato e meno aperto** (più TODO scaffolded, più mini-esercizi piccoli che assalti grandi).
