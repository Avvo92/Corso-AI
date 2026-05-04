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

### [2026-04-30] — Quiz d'ingresso Q1 (norma euclidea)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~133–136) — Quiz d'ingresso Q1.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** valore numerico corretto (5); formula corretta in parole (`sqrt` della somma dei quadrati); collegamento corretto norma ↔ "grandezza" del vettore `[3, 4]`.
- **Cosa migliorare (micro):** specificare che è la **norma euclidea (L2)** (nome ufficiale) e che misura la **lunghezza** del vettore come spostamento dall'origine (Pitagora in 2D); opzionale: tipo di ritorno `float` di `np.linalg.norm` su input lista.
- **Pattern errore / ID contesto:** nessuno; retention cap.01 su norma OK.

### [2026-04-30] — Quiz d'ingresso Q1 — rivalutazione post-feedback (testo aggiornato nelle righe ~132–136)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~132–136) — Quiz d'ingresso Q1 (versione aggiornata con "norma euclidea").
- **Valutazione (post-feedback — NON sostituisce il voto esame):** **10/10**
- **Punti di forza:** ora esplicita correttamente **norma euclidea**; mantiene calcolo `sqrt(9+16)=5` e il collegamento norma ↔ grandezza/lunghezza del vettore.
- **Next step:** proseguire con Q2–Q8 del quiz d'ingresso.

### [2026-05-04] — Quiz d'ingresso Q2 (coseno tra vettori paralleli e positivi)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~138–141) — Quiz d'ingresso Q2.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** identifica correttamente `b = 2 * a` (stessa direzione, stesso "pattern" delle componenti); intuisce **coseno = 1** senza conti; lega correttamente le norme con **||b|| = 2 * ||a||** (omogeneità della norma euclidea rispetto al fattore di scala positivo).
- **Micro-precisazione (opzionale):** aggiungere in una riga "stessa direzione / vettori paralleli con stesso verso" per chiarezza colloquio; non necessario per il voto.
- **Pattern errore / ID contesto:** nessuno; ponte cap.01 (coseno vs scala) consolidato.

### [2026-05-04] — Quiz d'ingresso Q3 (dot product: scalare vs vettore + valore)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~142–146) — Quiz d'ingresso Q3.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** risposta corretta **scalare**; definizione corretta del dot product come somma dei prodotti componente-per-componente; calcolo corretto **1*4 + 2*5 + 3*6 = 32**.
- **Micro-nota (non matematica):** ortografia italiana `poiché` (non `poichè`); irrilevante per il concetto.
- **Pattern errore / ID contesto:** nessuno.

### [2026-05-04] — Quiz d'ingresso Q4 (V/F: coseno=1 ⇒ vettori uguali)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~147–151) — Quiz d'ingresso Q4.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** **Falso** corretto; distingue bene **direzione** (coseno=1 ⇒ paralleli/stesso pattern) da **uguaglianza** delle componenti; aggiunge correttamente il caso **coseno=1 + norme uguali ⇒ vettori uguali** (salvo floating point).
- **Micro-nota (italiano):** "La risposta corrett**a** è ..." (concordanza di genere); non impatta la matematica.
- **Pattern errore / ID contesto:** nessuno; concetto chiave cap.01 (coseno vs norma) consolidato.

### [2026-05-04] — Quiz d'ingresso Q5 (shape `(3,)` vs `(1, 3)`)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~153–155) — Quiz d'ingresso Q5.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** risposta corretta **`(3,)`**; distinzione chiara **1D vs 2D**; collegamento corretto a `np.array([[1,2,3]])` → **`(1, 3)`** come "riga" di una matrice.
- **Cosa aggiungere (micro, per arrivare a 10/10):** 1 riga su **perché importa in pratica** oltre al nome: `a @ w`, broadcasting, `predict_proba` che vuole input **2D `(1, d)`**, slicing `a[0]` vs `A[0:1]` — cioè le shape guidano cosa puoi moltiplicare con cosa senza `ValueError`.
- **Micro-nota (italiano):** `perché` (non `perchè`); "nella fattispecie" / "in particolare" al posto di "nella fatti-specie".
- **Pattern errore / ID contesto:** nessuno; Lacuna #12 / shape retention OK.

### [2026-05-04] — Quiz d'ingresso Q6 (type hint: `np.array` vs `np.ndarray`)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~157–160) — Quiz d'ingresso Q6.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** messaggio chiave corretto: **`np.array` non è un tipo** (è la factory/callable che costruisce array); **`np.ndarray` è il tipo** da usare nei type hint; collegamento concettuale "quello che restituisce `np.array(...)` è un `ndarray`".
- **Cosa precisare (per 10/10):** `np.array` è tipicamente una **funzione** NumPy (built-in ufunc-level no, ma callable), non un "metodo" nel senso OOP stretto; opzionale: menzione `numpy.typing.NDArray` per hint più stretti.
- **Micro-nota (italiano):** "Il secondo" (non "La secondo"); `perché` (non `perchè`); "fattispecie" (non "fatti-specie").
- **Pattern errore / ID contesto:** Pattern #25 — chiusura in corso (cap.02 rinforzo + quiz Q6).

### [2026-05-04] — Quiz d'ingresso Q7 (errore `iloc` con etichetta colonna)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~161–167) — Quiz d'ingresso Q7.
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** diagnosi corretta: **`iloc` accetta solo indici numerici** per righe e colonne; usare `"a"` come secondo indice di `iloc` è incoerente e spiega il `TypeError`; esempio `df.iloc[0, 1]` è coerente come idea (se la colonna `"a"` fosse in posizione 1).
- **Cosa manca (per 9.5–10/10):** citare almeno **una** fix idiomatica con etichetta: `df.loc[0, "a"]` **oppure** `df.iloc[0]["a"]` **oppure** `df["a"].iloc[0]`; nota: nel `DataFrame` d'esempio la colonna `"a"` è in posizione **0**, non 1 (l'esempio numerico va allineato al caso reale o va presentato chiaramente come ipotesi).
- **Micro-nota (italiano):** "stringa" (non "striga"); "trovare" (non "travare").
- **Pattern errore / ID contesto:** Pattern #24 — verifica acquisizione (quiz Q7).

### [2026-05-04] — Quiz d'ingresso Q8 (Feynman: norma vs coseno, senza formule)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~168–173) — Quiz d'ingresso Q8 (Feynman).
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** rispetta il vincolo **niente formule**; analogia **frecce** chiara; norma ↔ **lunghezza/grandezza**; coseno ↔ confronto di **direzioni** con estremi **1 (stessa direzione)** e **-1 (opposte)**; tono adatto a collega web dev.
- **Cosa aggiungere (per 10/10 Feynman):** una frase sul caso intermedio **perpendicolari → "non allineati" (valore 0)**; precisare che il coseno qui misura soprattutto **allineamento / "stessa forma proporzionale"** (non solo "differenza" come parola); nota: la norma non include il segno delle componenti perché "misura lunghezza" (concetto implicito, ok se espresso a voce).
- **Micro-nota (testo):** refuso finale `,.` → scegliere `.` oppure `;` (typo di battitura).
- **Pattern errore / ID contesto:** nessuno; Feynman OK (non segnalare come lacuna).

### [2026-05-04] — Rinforzo Pattern #23 (virgole → tuple) — TODO esercizio

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~202–214) — TODO Rinforzo #23 (codice rotto con virgole spurie → fix).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** virgole spurie rimosse correttamente; `fig, ax = plt.subplots()` senza tupla fantasma; `set_title` / `set_xlim` / `set_ylim` su righe separate (stile preferito); `plt.close(fig)` ok; commento che spiega l’idea (**tuple inutili** create dalle virgole) presente e centrato.
- **Cosa migliorare (micro):** commento riga 209: italiano più pulito (“**il** grafico”, “**le** istruzioni”) e possibilmente **una sola riga** come richiesto dalla consegna (“1 riga COMMENTATA”); opzionale coerenza stilistica `fig` ovunque (qui `plt.close(fig)` è ok perché `close` accetta la figura).
- **Pattern errore / ID contesto:** Pattern #23 — acquisizione OK al primo tentativo (monitorare che non ricompaia in Matplotlib/E2).

### [2026-05-04] — Rinforzo Pattern #24 (iloc vs loc) — TODO esercizio df_demo

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~249–256) — TODO Rinforzo #24 (a) riga posizione 1 come Series; (b) `voto` riga posizione 2.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** (b) **`df_demo['voto'].iloc[2]`** idiomatico e corretto (riga indice 2 → `9`); (a) logica corretta (riga posizione 1 = Bob) ma implementata con **`pd.Series(df_demo.iloc[1])`** (ridondante).
- **Cosa migliorare:** (a) **`pd.Series(...)` è ridondante** — `df_demo.iloc[1]` è già una `Series`; meglio `riga_series = df_demo.iloc[1]` oppure esplicito **`df_demo.iloc[1, :]`**.
- **Pattern errore / ID contesto:** Pattern #24 — acquisizione OK; togliere ridondanza `pd.Series(...)` per stile.

### [2026-05-04] — Rinforzo Pattern #24 — rivalutazione post-feedback (righe ~249–256)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~253–255) — TODO Rinforzo #24 (versione aggiornata).
- **Valutazione (post-feedback — NON sostituisce il voto esame):** **10/10**
- **Punti di forza:** (a) **`riga_series = df_demo.iloc[1, :]`** forma esplicita e pulita (riga posizione 1 → `Series`); (b) **`df_demo['voto'].iloc[2]`** invariato e corretto.
- **Pattern errore / ID contesto:** Pattern #24 — ridondanza `pd.Series(...)` eliminata.

### [2026-05-04] — Rinforzo Pattern #25 (np.array vs np.ndarray) — TODO firma `somma_due_vettori`

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~280–288) — TODO Rinforzo #25 (type hint corretti).
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** sostituisce correttamente **`np.array` (anti-pattern)** con **`np.ndarray`** su `a`, `b` e sul **return**; corpo `return a + b` coerente.
- **Cosa migliorare:** il codice è **tutto commentato** (`# def ...`): per considerarlo “eseguito” decommentare le righe così la funzione esiste davvero nel modulo (e puoi provarla da REPL); opzionale avanzato: `from numpy.typing import NDArray` + `NDArray[np.float64]` per hint più stretti.
- **Pattern errore / ID contesto:** Pattern #25 — acquisizione OK.

### [2026-05-04] — Ripasso 5 blocchi — R1 (vettori + shape)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~298–305) — R1 vettori + shape.
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** vettore con **6 elementi**; **`dtype=float`** esplicito (ottimo); **`print(v.shape)`** → atteso **`(6,)`**; **`print(v.dtype)`** → `float64`.
- **Cosa migliorare:** la riga `print("Mini-esercizio R2")` è **etichetta sbagliata** (qui è **R1**); correggere per non confonderti in revisione/log.
- **Pattern errore / ID contesto:** nessuno; retention cap.01 OK.

### [2026-05-04] — Ripasso 5 blocchi — R2 (operazioni base)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~308–320) — R2 operazioni base.
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** `a`, `b` corretti; **`a+b`**, **`a-b`**, **`a*b`** stampati e coerenti con **broadcasting element-wise**; commento che lega le operazioni a **vettore di shape uguale** va nella direzione giusta.
- **Cosa manca:** la consegna chiedeva esplicitamente anche **`print(2 * a)`** (scala × vettore = broadcast element-wise) — **assente**; aggiunto **`a/b`** (utile ma non richiesto, non sostituisce `2*a`). Domanda «**quanti scalari**»: precisare che ognuna produce **un array 1D con 3 componenti** (tre numeri), non un singolo scalare; opzionale distinguere **`a*b`** come *prodotto elemento per elemento* vs prodotto interno (dot).
- **Pattern errore / ID contesto:** leggere checklist consegna prima di chiudere il blocco (output richiesti vs extra).

### [2026-05-04] — Ripasso 5 blocchi — R3 (dot product senza `np.dot` / `@`)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~322–331) — R3 dot product.
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `x`, `w` corretti; **`(x * w).sum()`** è esattamente il pattern **Hadamard + riduzione** richiesto; nessun **`np.dot`** né **`@`**; risultato atteso **140** (`10+40+90`).
- **Micro-nota (opzionale):** per colloquio, saper dire a voce che il dot è **una somma di prodotti** e che in layer densi è la stessa idea moltiplicata per molte righe (matmul).

### [2026-05-04] — Ripasso 5 blocchi — R4 (norma euclidea senza `np.linalg.norm`)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~333–340) — R4 norma euclidea.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** `v` corretto **`[3, 4]`**; **`np.sqrt((v**2).sum())`** implementa \(\sqrt{\sum_i v_i^2}\) con solo **`np.sqrt`** e **`.sum()`**; niente **`np.linalg.norm`**; output **`5.0`** (entro floating point).
- **Cosa aggiungere (micro, per 10/10 sulla parola «Verifica»):** una riga esplicita tipo **`assert np.isclose(norma, 5.0)`** (o confronto stampato atteso/ok) così la verifica è nel codice, non solo a occhio sull’output.

### [2026-05-04] — Ripasso 5 blocchi — R5 (coseno tra vettori)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~342–355) — R5 coseno.
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** idea corretta **dot / (norma a × norma b)**; uso di **`@`** e **`np.linalg.norm`** coerente con “implementazione”; secondo caso con **`b` riassegnato**; **`assert np.isclose(...)`** per 0.0 e 1.0 (ottima abitudine).
- **Errore critico — precedenza operatori:** scritto `(a @ b) / np.linalg.norm(a) * np.linalg.norm(b)` Python lo legge come **`((a @ b) / ||a||) * ||b||`**, NON come dot diviso **prodotto** delle norme. Con **`a=[1,0]`** e **`b=[0,1]`** o **`[1,0]`** le norme sono **1** quindi il bug **non si vede** e gli assert passano **per fortuna**.
- **Fix obbligatorio:** **`coseno = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))`** (parentesi sul denominatore). Prova mentale: **`a=[1,0]`**, **`b=[1,1]`** → coseno vero **`1/√2 ≈ 0.707`**, con la formula sbagliata ottieni **`√2 ≈ 1.414`**.
- **Pattern errore / ID contesto:** espressioni con **`/` e `*`** in fila: **sempre parentesi** sul denominatore (o variabile `den = na * nb`).
- **Fix applicato (post-feedback):** denominatore con parentesi **`(np.linalg.norm(a) * np.linalg.norm(b))`** su entrambe le assegnazioni a `coseno` — voto esame resta **6.5/10** (primo tentativo).

### Ripasso 5 blocchi cap.01 — stato valutazioni

- **R1:** vedi entry **[2026-05-04] — Ripasso 5 blocchi — R1** sopra (**9/10**).
- **R2:** vedi entry **[2026-05-04] — Ripasso 5 blocchi — R2** sopra (**7/10**).
- **R3:** vedi entry **[2026-05-04] — Ripasso 5 blocchi — R3** sopra (**10/10**).
- **R4:** vedi entry **[2026-05-04] — Ripasso 5 blocchi — R4** sopra (**9.5/10**).
- **R5:** vedi entry **[2026-05-04] — Ripasso 5 blocchi — R5** sopra (**6.5/10**).

### [2026-05-04] — Sezione 1.1 (matrice batch da CSV)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~413–445) — TODO 1.1.
- **Valutazione (primo tentativo — "voto esame"):** **4.5/10**
- **Punti di forza:** path con **`os.path.join`** + **`__file__`** coerente con la traccia; **`read_csv`**; **`drop(..., 'pratica_id', 'y_alterato')`** + **`to_numpy(dtype=float)`** su **`X_full`** corretto come preprocessing.
- **Errore critico:** **`X = pratiche[:5]`** prende le prime 5 righe del **DataFrame originale** (colonne ancora con `pratica_id`, `y_alterato`), **non** le prime 5 righe della **matrice numerica**. Doveva essere **`X = X_full[:5]`**. Così l’obiettivo “matrice **X** delle feature” non è raggiunto.
- **Disallineamento consegna:** richiesto **`X.shape`**, **`X.dtype`**, **`X[0]`**, **`X[:, 0]`** (API **NumPy**); ottenuto **`X.dtypes`**, **`iloc`** → resti in **pandas** e **`dtypes`** è per colonna, non l’dtype unico dell’array.
- **Next step:** `X = X_full[:5]` poi `print(X.shape, X.dtype, X[0], X[:, 0])` (eventuale `print(..., sep="\n")` per leggibilità).

### [2026-05-04] — Sezione 1.1 — rivalutazione post-fix (stesse righe ~413–445)

- **Blocco:** `02_matrici_e_layer_dense.py` — TODO 1.1 dopo correzione refuso.
- **Valutazione (post-fix — secondo stato del codice):** **6/10**
- **Cosa è a posto:** **`X = X_full[:5]`** — ora **`X`** è davvero la sottomatrice numerica delle prime 5 pratiche (feature-only); refuso **`pratiche[:5]`** risolto.
- **Cosa resta errato:** **`X`** è **`ndarray`**: non ha **`.dtypes`** né **`.iloc`** → in esecuzione andresti in **`AttributeError`**. La consegna chiedeva **`X.dtype`**, **`X[0]`**, **`X[:, 0]`** (indicizzazione NumPy).
- **Nota:** il voto **primo tentativo** della entry precedente resta **4.5/10** (regola diario).

### [2026-05-04] — Sezione 1.1 — rivalutazione (stato finale righe ~428–445)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` — TODO 1.1.
- **Valutazione (stato codice corrente dopo fix stampe):** **10/10**
- **Punti di forza:** path robusto; **`drop` + `to_numpy(dtype=float)`**; **`X = X_full[:5]`**; stampe **`shape`**, **`dtype`**, **`X[0]`**, **`X[:, 0]`** allineate alla consegna e coerenti con **`ndarray`**.
- **Nota diario:** non sostituisce il voto **primo tentativo** (**4.5/10**); traccia il **raggiungimento learning outcome** dell’esercizio.

### [2026-05-04] — Sezione 1.2 (vettore-riga vs vettore-colonna)

- **Blocco:** `ponte_matematico_m2_m3/02_matrici_e_layer_dense.py` (righe ~448–460) — TODO 1.2.
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** **`v`** corretto; **`vr = v.reshape(1, 5)`** → **`(1, 5)`**; **`vc = v.reshape(5, 1)`** → **`(5, 1)`** (alternativa alla list comprehension, esplicitamente ammessa); stampa delle **tre shape** **`v`**, **`vr`**, **`vc`** come richiesto.
- **Refuso:** `print("\nEsercizio 1.1\n")` dovrebbe essere **1.2** (stesso tipo di errore già visto su R1/R2).

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
