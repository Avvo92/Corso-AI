# Diario sessione — Capitolo 06 — Backpropagation + Training

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `06_backprop_training.py` |
| **File diario** | `M03_C06_backprop_training_sessione.md` |
| **Stato** | 🟢 **Pronto ad aprire** (27/07/2026) — prima il bridge `M03_R05`; rinforzi 🔁 già inseriti nel file |
| **Voto difficoltà** | — / X/10 (atteso 8–9/10 dopo split, era 9/10 nel vecchio monolitico) |

---

## Obiettivi del capitolo (per il mentor — da affinare a chiusura cap.05)

- Mettere insieme tutto: forward (con cache) + loss (cap.03) + chain rule (cap.05) + gradient descent (cap.05) APPLICATI alla rete 2-layer del cap.02.
- Sanity check OBBLIGATORIO: gradiente analitico VS gradiente numerico (per dW1[0, 0]) — se differiscono > 1e-4 c'e' un bug.
- Far girare il **mini-progetto**: rete 2-layer addestrata sul CSV M2 che pareggia/batte LogisticRegression M2 cap.04.
- Inserire `🔄 CONFRONTO PRIMA/DOPO` (chiusura "primo blocco" full-NumPy cap.01-06, ANTICIPATO rispetto al fine modulo - cap.10).

---

## Strategia didattica (da affinare)

- Sequenza per OGNI concetto: **analogia concreta -> codice -> grafico -> formula in parole**.
- Le SHAPE di `dW1, db1, dW2, db2, dZ1, dZ2` devono essere VISIBILI in ogni passaggio (meta' dei bug di backprop sono shape mismatch).
- Se a meta' capitolo lo studente e' bloccato -> STOP, mini-recap dedicato.
- ⚠️ Capitolo difficile - andare lenti. Pianificare **2-3 sessioni**: (1) sez.1-2, (2) sez.3-4, (3) mini-progetto + confronto prima/dopo.

### Rinforzi 🔁 inseriti alla chiusura del cap.05 (27/07/2026)

| Lacuna | Blocco | Posizione nel file |
|--------|--------|--------------------|
| #38 `dL/dp` vs `dL/dz` | Analogia del **termostato** + verifica con `gradiente_numerico` su `p` e su `z` | dopo RINFORZO SHAPE, prima di SEZIONE 1 |
| #39 catena verso `W1` | Analogia dei **due affluenti** (W1/W2 rami, non tappe) + catena per `db1` | dopo RINFORZO SHAPE, prima di SEZIONE 1 |
| #37 `derivata_relu` in z=0 | Analogia **valvola di non ritorno**; convenzione corso/PyTorch = **0**; `>` non `>=` | sez. 2.4, prima del mini 2.4.A |
| Pattern #27 formula → codice | 3 regole di lettura (`*` vs `@`, shape attesa, `=` vs `==`) + quiz sulle shape | sez. 3, prima di `sanity_check_grad` |
| #40 Feynman come ciclo | "senti → passo → ripeti" + ruolo della dimensione del passo | sez. 4, prima di `train_rete_2_layer` |

**Da verificare durante il capitolo:** quiz ingresso Q2 (catena W1 → #39), Q3 (`p-y` → #36/#38), Q4 (ReLU spenta → #37), Q7 (Feynman → #40).

---

## Domande durante lo studio

- _(da popolare)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Voto = "primo tentativo".

### 2026-07-27 — Cap.06 Quiz ingresso Q1 (chain rule + update GD)

- **Risposta:** chain rule = prodotto delle derivate locali della composizione; update `w = w - grad * lr` con i tre termini nominati. Entrambe corrette a freddo.
- **Manca (1):** le derivate locali vanno **valutate nel punto giusto** — `h'(x) = f'(g(x))·g'(x)`, non `f'(x)·g'(x)`. È la ragione d'essere della cache del forward (`derivata_relu` valutata in `Z1`).
- **Manca (2):** il **perché del segno meno** (il gradiente punta in salita, si va contro per minimizzare) — concetto che aveva invece esplicitato bene al V5 del cap.05.
- **Forma:** typo "uguale la prodotto" → "al prodotto".
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-27 — Cap.06 Quiz ingresso Q2 (quante derivate per dL/dW1) — ✅ chiude lacuna #39

- **Risposta:** 5 derivate, `dL/dp · dp/dZ2 · dZ2/dH · dH/dZ1 · dZ1/dW1` — ordine corretto, **W2 non inserito** come anello.
- **Confronto:** al V7 del cap.05 aveva scritto `dz/dW2 · dW2/dh · dH/dW1` (5/10). Il rinforzo 🔁 "due affluenti" ha funzionato → **lacuna #39 → 🟢**.
- **Neo:** ultimo fattore scritto `dZ1*dW1` invece di `dZ1/dW1` (Pattern #27, scivolata di operatore in trascrizione).
- **Notazione:** con batch conviene `dL/dP` e `dP/dZ2` maiuscoli (matrice), la minuscola è il singolo campione.
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-27 — Cap.06 Quiz ingresso Q3 (semplificazione miracolosa) — ✅ chiude #36 e #38

- **Risposta:** `dL/dp * dp/dZ2 → (p-y)/p(1-p) * p(1-p) → p-y`, con cancellazione mostrata passo per passo.
- **Chiude #38:** `dL/dp` scritta **con il denominatore**, distinta da `p-y`. Chiude anche **#36** (`p-y` sotto stress, senza aprire il cap.04).
- **Manca la seconda metà della domanda:** valore di `dL/dZ2` sul **batch** → `(P - y).reshape(-1,1) / N`, shape `(N,1)`. Mancano sia il **`/N`** (loss come media) sia il **reshape** (rischio broadcasting silenzioso `(N,N)`).
- **Da verificare:** mini 2.1.A (calcolo di `dL/dZ2`) e mini 3.1.B (esperimento senza `/N`).
- **Forma:** "tra tra" ripetuto; `p(1-p)` → `p*(1-p)` se trasferito in codice.
- **Valutazione (primo tentativo):** **8/10**.
- **Fix applicato (post-feedback):** aggiunta `dL_dZ2 = (P - y).reshape(-1, 1) / N` con motivazione corretta di entrambi i pezzi (shape allineata a `Z2`; `/N` perché la loss è una media sul batch, applicata a ogni elemento). **Post-feedback 10/10** — il voto d'esame resta 8/10. Unica precisazione lessicale: `N` = numero di **campioni** (qui coincide con le righe).

### 2026-07-27 — Cap.06 Quiz ingresso Q4 (ReLU spenta e gradiente di W1)

- **Risposta:** "la derivata parziale dei neuroni disattivati varrà 0" — nucleo corretto ma molto compresso.
- **Manca (1):** la conseguenza operativa — `W1 -= lr * 0` lascia il peso **invariato**, il neurone spento non impara.
- **Manca (2) — imprecisione concettuale:** la maschera ReLU agisce **elemento per elemento** su `Z1` `(N, h)`. Con "metà dei valori negativi" il gradiente di `W1` **non è zero**: `grad_W1 = X.T @ dZ1` somma su tutto il batch, quindi perde metà dei contributi ma continua ad aggiornarsi. Zero esatto solo se il neurone è spento per **tutti** i campioni → **dying ReLU**.
- **Da colloquio:** distinguere "spento per questo campione" da "spento per sempre".
- **Lacuna #37 NON ancora chiusa:** la domanda non testa il caso `z = 0` (la convenzione è già scritta nel testo della domanda). Verifica rimandata al blocco 🔁 di sez. 2.4 (previsione output su `[-2, -0.0, 0.0, 1e-9, 3.0]`).
- **Valutazione (primo tentativo):** **7.5/10**.
- **Fix applicato (post-feedback):** aggiunta la conseguenza `w = w - 0 * lr` → peso invariato (punto 1 chiuso). **Punto 2 ancora aperto:** continua ad affermare che i neuroni "non impareranno nulla", mentre con metà valori negativi `grad_W1 = X.T @ dZ1` riceve comunque i contributi degli altri campioni. Nullo solo se spento su **tutto** il batch (dying ReLU). **Post-feedback 8.5/10** — voto d'esame resta 7.5/10. Da riverificare al mini 2.4.A e al blocco 🔁 sez.2.4.
- **Secondo re-check (stessa sessione):** modifica solo lessicale ("i" → "quei" neuroni), punto 2 invariato. Nodo concettuale: "disattivato" è uno stato della coppia **(neurone, campione)**, non del neurone. Deciso di **non insistere a parole** e riprendere la risposta dopo il mini 2.4.A, dove le celle azzerate di `dL_dZ1` rendono la cosa visiva.

### 2026-07-27 — Cap.06 Quiz ingresso Q5 (shape N=10, d=5, h=8)

- **Corrette 7/9:** `X (10,5)`, `W1 (5,8)`, `Z1 (10,8)`, `H (10,8)`, `W2 (8,1)`, `b2 (1,)`, `Z2 (10,1)` — inclusi i prodotti matriciali.
- **Errore 1:** `b1` scritto `(8,1)` invece di **`(8,)`**. Incoerente con `b2 (1,)` scritto giusto. Conseguenza concreta: `X@W1 + b1` con `(10,8)+(8,1)` → **ValueError** (10 vs 8 dopo l'allineamento da destra).
- **Errore 2:** `P` scritto `(10,1)` invece di **`(10,)`**. Ignorato il `.ravel()` in `forward_2layer`. Conseguenza: `P - y` → `(10,10)` per broadcasting **silenzioso**, loss calcolata su 100 numeri senza senso.
- **Famiglia dell'errore:** vettore 1D vs colonna 2D — imparentata con la vecchia lacuna #23 (chiusa a maggio). Riemersa → **nuova lacuna #41**.
- **Regola data:** "uno per neurone / uno per campione" = 1D (`b1`, `b2`, `y`, `P`); "tabella campioni × qualcosa" = 2D.
- **Valutazione (primo tentativo):** **7/10**.
- **Fix applicato (post-feedback):** corretti i **valori concreti** → `(8,)` e `(10,)`. Resta sbagliata la **forma simbolica**: `b1.shape == (h, 1) == (8, )` e `P.shape == (N, 1) == (10, )` sono uguaglianze false; vanno `(h,)` e `(N,)`. Segnalato che la forma simbolica è quella che si generalizza (rischio di rifare l'errore con `h` diverso). **Post-feedback 8.5/10** — voto d'esame resta 7/10. Lacuna #41 resta 🔴.
- **Secondo fix:** corrette anche le forme simboliche → `b1 (h,)`, `P (N,)`. **Tutte le 9 shape corrette e coerenti, post-feedback 10/10** (voto d'esame resta 7/10). Lacuna #41 resta 🔴 fino alla verifica pratica al mini 1.1.A/1.1.B.

### 2026-07-27 — Cap.06 Quiz ingresso Q6 (sanity check)

- **Risposta:** "prova del nove tramite gradiente numerico" — tecnica giusta, immagine efficace, ma **8 parole**: nomina lo strumento senza procedura né criterio.
- **Manca (1) procedura:** perturbare ogni parametro di `±h` (`1e-6`), forward completo, differenza centrata; confronto su **tutti e 4** i parametri (un bug nel passo 3 lascia `grad_W2` sano e rompe solo `grad_W1`).
- **Manca (2) criterio:** `max|num - ana| < 1e-4` (idealmente `< 1e-6`), come in `sanity_check_grad`.
- **Manca (3) diagnosi:** le 4 cause tipiche — trasposta, `axis` in `sum`, segno, `/N` mancante.
- **Manca (4) perché non in training:** 2 forward per parametro (98 forward per 49 parametri) → solo controllo una tantum.
- **Pattern:** tendenza a risposte troppo compresse nelle domande "a parole" (già vista in Q4). Da monitorare in ottica colloquio.
- **Valutazione (primo tentativo):** **7/10**.

### 2026-07-27 — Cap.06 Quiz ingresso Q8 (loss e accuracy iniziali)

- **Risposta:** `~0.69` e `~0.5` — entrambe corrette (opzioni b, b).
- **Manca (non richiesto, ma prezioso):** `0.69 = -ln(0.5)`; pesi random → logit ~0 → `sigmoid ≈ 0.5` per tutti → su dataset bilanciato BCE = 0.693 e accuracy = 0.5.
- **Conseguenza operativa data:** 0.69 è il **pavimento di riferimento** — se dopo il training la loss è ancora lì, la rete non impara (lr, scaling, init, dataset degenere). Collegato al **TODO 17 REAL-WORLD del cap.05 rimasto in sospeso** (collega con loss 0.69 dopo 1000 epoche).
- **Valutazione (primo tentativo):** **9/10**.
- **Nota:** **Q7 (Feynman backprop) ancora vuota** — è la verifica della lacuna #40.

### 2026-07-27 — Cap.06 Micro-esercizio RINFORZO SHAPE (carry-over)

- **Tutte le 10 shape corrette** (incluse `y (10,)` non richiesta in Q5): `b1 (8,)` e `P (10,)` al posto giusto, notazione e valori coerenti.
- **Caveat:** svolto pochi minuti dopo la correzione di Q5 → memoria fresca, non recupero autonomo. **Lacuna #41 → 🟡**; conferma definitiva al **mini 1.1.A** (shape stampate dal codice, non scritte a mano).
- **Forma:** `(10,  )` con doppio spazio — abituarsi a `(10,)` compatto per coerenza con `reshape`.
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-27 — Cap.06 Q7 (Feynman backprop): saltata per scelta

- Lo studente ha deciso di **non svolgere** la Q7 del quiz d'ingresso (unica delle 8 rimasta aperta), rifiutando anche la variante orale in chat.
- **Lacuna #40 (Feynman senza ciclo iterativo) resta 🔴**: verifica spostata a **fine capitolo**, dopo aver visto la backprop in codice — dove la spiegazione a parole sarà comunque richiesta.
- Nota per il mentor: non insistere; riproporre il Feynman a fine cap.06 quando il concetto sarà supportato dal codice scritto.

### 2026-07-27 — Cap.06 🔁 RINFORZO #38 punto 1 (`dL/dp` vs `dL/dz`, p=0.8 y=1)

- **Valori tutti corretti**: `dL/dp = -1.25`, `dp/dz = 0.16`, prodotto `-0.2 = p - y`. La distinzione `dL/dp` ≠ `dL/dz` è ora esplicita con due numeri diversi → **#38 confermata chiusa**.
- **Pattern #27 riemerso nella scrittura** (non nel calcolo): `(0.8-1) / 0.8*(1-0.8)` senza parentesi al denominatore → in Python vale `-0.05`, non `-1.25`; inoltre `p(1-p)` implicito → `TypeError: not callable`. **Pattern #27 resta 🔴.**
- Minore: virgole decimali (`-1,25`) miste a punti; in Python è una tupla.
- **Punto 2 non svolto** (verifica con `gradiente_numerico`, riga 361) — da recuperare.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-27 — Cap.06 🔁 RINFORZO #38 punto 2 (verifica con `gradiente_numerico`)

- **Codice corretto ed eseguito**: `grad_p = -1.25000000004`, `grad_z = -0.20000000003` → coincidono con i valori calcolati a mano al punto 1.
- **Bene:** lambda con parametri `p_var`/`z_var` (niente shadowing); `bce_loss(sigmoid(z_var), y)` e non `bce_loss(z_var, y)`; indicizzazione `[0]`.
- **Manca:** verifica solo **visiva** (due `print` nudi). Indicato il pattern `assert np.allclose(...)` + print con valore atteso — è l'antidoto formale al **Pattern #27**.
- Minore: `y = np.array([1])` int invece di `1.0`.
- **Domanda posta:** perché `z = np.log(p/(1-p))` → spiegato logit/log-odds come inversa della sigmoid (buon segnale: ha chiesto invece di copiare).
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-27 — Cap.06 🔁 RINFORZO #39 punto 1 (catena `dL/db1`)

- Catena corretta e **senza W2 come anello** (terza conferma di fila) → **#39 chiusa senza riserve**.
- **Manca il conteggio degli anelli** (5), esplicitamente richiesto nella stessa riga → **Pattern #6** (lettura incompleta delle consegne) ancora attivo.
- Aggiunto in feedback: `dZ1/db1 = 1` (il bias entra sommato) e la conseguenza `grad_b1 = dL_dZ1.sum(axis=0)` da `(N,h)` a `(h,)` — aggancio diretto alla lacuna #41.
- **Valutazione (primo tentativo):** **9/10**.
- *Fix applicato:* aggiunto `== 5 anelli` (10/10 post-feedback; voto di riferimento resta 9/10 — Pattern #6 riguarda la lettura, non il conteggio).

### 2026-07-27 — Cap.06 🔁 RINFORZO #39 punto 2 (V/F: `dL/dW2` prima di `dL/dW1`)

- **Verdetto corretto (Falso)**, ma motivazione imprecisa: «si procede a ritroso *da* `dL/dW2` *per arrivare a* `dL/dW1`» implica una dipendenza fra i due gradienti che non esiste. Eco attenuata della #39.
- Chiarito: i due sono **rami indipendenti**; il pezzo riusato è **`dL/dZ2`** (variabile intermedia), non `dL/dW2`. È questo il risparmio della backprop sul gradiente numerico.
- Corollario pratico dato in feedback: `dZ2/dH = W2` → **non aggiornare W2 prima di aver calcolato tutti i gradienti** (bug silenzioso: la loss scende comunque, storta).
- **Valutazione (primo tentativo):** **8/10**.

### 2026-07-28 — Cap.06 Mini 1.1.A (forward + shape stampate)

- Eseguito: `P (10,)`, `Z1 (10,8)`, `H (10,8)`, `Z2 (10,1)` — tutte e quattro come atteso. **Lacuna #41 → 🟢** (conferma dal codice, non a memoria fresca).
- Setup corretto: `b1`/`b2` come array (`np.zeros(h)`, `np.zeros(1)`); He a mano ok.
- Stile migliorabile: `P, cache = forward_2layer(...)` invece di `result[0]` / `result[1]` (tuple unpacking più leggibile).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-28 — Cap.06 Mini 1.1.B (perché `.ravel()`)

- Direzione corretta: BCE e accuracy vogliono `P` come vettore 1D `(N,)`.
- **Manca il perché pericoloso**: con `P (N,1)` e `y (N,)`, `P - y` (e le operazioni in BCE) fanno **broadcasting silenzioso** → shape `(N,N)`, loss/metriche sbagliate senza crash. Eco della #41.
- **Valutazione (primo tentativo):** **8/10**.

### 2026-07-28 — Cap.06 Mini 1.2.A (backward alla cieca / cache)

- **Concetto centrale corretto**: da `P` → `Z2` via logit; da `Z2` **non** si ricostruisce `H` in modo univoco (matmul non invertibile univocamente). Quindi serve la cache del forward.
- Completo: ha citato sia l'inversione sigmoid sia il prodotto matriciale non reversibile.
- Minore: anche `Z1`→`H` (ReLU) non è invertibile in modo unico (i negativi diventano 0).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-28 — Cap.06 Mini 2.1.A (`dL/dZ2` a mano)

- Shape `(3,1)` e valori `[-0.0333, 0.1333, -0.1]` corretti: `(P-y)/N` + `reshape(-1,1)`.
- **Naming:** variabile chiamata `Z2` ma è il **gradiente** `dL/dZ2`, non il logit del forward. Confusione pericolosa nel backward (due oggetti diversi con lo stesso nome).
- **Valutazione (primo tentativo):** **9/10**.
- *Fix applicato:* rinominato in `dL_dZ2` → **10/10** post-feedback (voto di riferimento resta 9/10).

### 2026-07-28 — Cap.06 Mini 2.2.A (`dL/dW2`, `dL/db2`)

- Shape e valori corretti: `dL_dW2 (2,1) ≈ [[0.233], [-0.167]]`; `dL_db2 (1,) ≈ 0` (somma batch: -0.033+0.133-0.1).
- Formule giuste: `H.T @ dL_dZ2` e `sum(axis=0)`; naming coerente.
- Nota: `~1e-17` è rumore float ≈ zero, non un errore.
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-28 — Cap.06 Mini 2.3.A (`dL/dH`)

- Shape `(3,2)` e valori corretti: ogni riga = `dL_dZ2[i] * W2.T` (es. riga0 ≈ `[-0.0167, -0.0333]`).
- Formula `dL_dZ2 @ W2.T` giusta — qui **W2 è un valore moltiplicatore**, non una tappa della catena (eco #39 chiusa).
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-28 — Cap.06 🔁 RINFORZO #37 (`derivata_relu` @0 + dying ReLU)

- **Punto 1 ok**: previsione **2** uni su `[-2, -0, 0, 1e-9, 3]` — `z=0` e `-0` → 0 (convenzione corso). `my_derivata_relu` con `z > 0`. **#37 → 🟢**.
- **Punto 2**: intuizione corretta (niente update se spento su tutto il batch) ma naming sbagliato: non è `Z1 = Z1 - 0*lr`, sono i **pesi/bias** di quel neurone (`W1[:,j]`, `b1[j]`) a restare fermi. Dying ReLU: se resta sempre ≤0, resta bloccato.
- **Valutazione (primo tentativo):** **8.5/10**.
- *Fix applicato (commento):* ora parla di segnale all’indietro e pesi non aggiornati. Da precisare: parametri = `W1`/`b1` di quel neurone; condizione “tutto il batch”.

### 2026-07-28 — Cap.06 Mini 2.4.A + 2.5.A (`dL/dZ1`, `dL/dW1`, `dL/db1`)

- **2.4.A**: shape `(3,2)`; elementi con `Z1<0` azzerati (colonna1 riga0, colonna0 riga2) — ReLU gate ok.
- **2.5.A**: `dL_dW1 (3,2)` e `dL_db1 (2,)` corretti (`X.T @ dL_dZ1`, `sum(axis=0)`). Catena backward mini completa fino a W1/b1.
- **Valutazione 2.5.A (primo tentativo):** **10/10**.

### 2026-07-28 — Cap.06 Mini 2.6.A (`forward` + `backward_2layer`, shape grads)

- Setup e chiamate corrette; 4 assert sulle shape `(5,8)`, `(8,)`, `(8,1)`, `(1,)` — passano.
- Minore: per le shape meglio `grads["grad_W1"].shape == (5, 8)` invece di `np.allclose(...)` (allclose è per float; sulle tuple funziona per caso).
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-28 — Cap.06 🧠 [RETRIEVAL] `my_forward` / `my_backward` / `my_sanity_check` (righe ~799–930)

- **Verifica finale:** assert vs `forward_2layer`/`backward_2layer` OK; `ok=True` con max_diff ~`1e-10` / `1e-11`.
- **Forward (1° tentativo):** catena e cache ok; mancava `.ravel()` su `P` (eco #41 / mini 1.1.B) → fix immediato.
- **Backward (1° tentativo):** formula a 5 step presente, ma (1) `P` non dalla cache; (2) `/N` sbagliato due volte (`X[0]` / `len(X[0])` = `d` invece di `shape[0]`); (3) `X.T` invece di `cache["X"].T`. Dopo fix: allineato al ref.
- **Sanity (1° tentativo, guidato):** confusione `[0]`/`[1]` sulla tupla forward; `W1v` al posto di `W1` per grads ana; `W1.flat()` invece di flatten/reshape — poi versione pulita senza flatten (corretta per questa `gradiente_numerico`).
- **Valutazione (primo tentativo — aggregato):** **7.5/10**. *Fix applicato: verifica passa (post-feedback OK).*
- **Pattern / note:** shape `N` vs `d`; accesso cache; indice tupla `(P, cache)`. Pattern #27 non riaperto (nessun `*` vs `@` qui). Domanda laterale dying ReLU / init → intuizione buona (già trattata in #37).

### 2026-07-28 — Cap.06 Mini 3.0.A (sanity su un solo peso `W1[0,0]`)

- Setup, `loss_solo_w00`, analitico vs numerico: **assert passa** (`|diff|` reale ~1e-12).
- Commento diagnostica (`|diff|~0.5` → **segno**): direzione corretta come prima ipotesi; `@` vs `*` di solito crasha o dà errori grossi; shape spesso esplode/NaN.
- Nota run terminale: stampa `Differenza: 0.044...` = `abs(ana) - num` (con entrambi negativi ≈ 2·|g|), non `abs(ana-num)`. Il check `assert` era comunque ok. Eco Pattern #27 (parentesi / ordine operazioni).
- **Valutazione (primo tentativo):** **9/10**.

### 2026-07-29 — Cap.06 Mini 3.1.A (`sanity_check_grad` ufficiale)

- Setup corretto (`he_init` seed 0/1, N=10,d=5,h=8); call ufficiale + assert `ok` + loop sui max_diff `< 1e-4` — passano (~1e-10).
- Extra (opzionale consegna): confronto `my_sanity_check_grad` con `np.allclose` sui valori — ok sullo stesso seed (stesso ordine di grandezza / stessi numeri).
- Minori: (1) consegna chiedeva stampa del **dict** intero (nel run si vede solo l’array dei diff); (2) confrontare `list(values)` è fragile se l’ordine chiavi diverge — meglio `assert abs(result[k]-my_result[k]) < …` per chiave; (3) `== True` funziona, `assert result["ok"]` è più idiomatico.
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-29 — Cap.06 Mini 3.1.B (sanity fallito: perché numerico ok / analitico no)

- **Idea centrale corretta:** il numerico passa da `forward + bce_loss` (perturbazione black-box), non da `backward_2layer` → resta allineato alla loss vera; l’analitico usa la formula buggata → max_diff grandi / `ok=False`.
- **Errori:** (1) chiama `dL/dp` il pezzo `(P-y)/N` — è **`dL/dZ2`** (eco #38, già 🟢 ma naming); (2) `/ X[0].shape` — di nuovo **`d` (feature)** al posto di **`N = X.shape[0]`** (stesso bug del RETRIEVAL backward); (3) “numerico non usa chain rule” è ok come intuizione, più preciso: non scompone la rete, stima ∂loss/∂param sulla loss implementata.
- **Valutazione (primo tentativo):** **7/10**.
- *Rivalutazione post-feedback (2026-07-29):* corretto `dL/dZ2`, `N = X.shape[0]`, e “numerico non scompone i layer / stima d_loss/d_param”. Rimasto un doppio “perché invece perché” (solo stile). **Post-fix: 9.5/10**.

### 2026-07-29 — Cap.06 🔁 RINFORZO #40 (training come ciclo — Feynman)

- **Punto 1 (prosa):** ha “ripeti/ciclo” e “quanto sono grandi i passi”; niente parole vietate. Analogia collina al buio chiara. **Ordine invertito** rispetto al GD classico: nel testo fa *prima il passo e poi sente*; nel GD vero *prima senti la pendenza (dove scende), poi fai il passo*. La versione “provo e se salgo cambio” è più trial-and-error.
- **Punto 2 (codice):** `(c) for epoch` ok; ma ha messo `(b) passo` sul **forward** e `(a) senti` solo su `bce_loss`. Il **passo** sono gli update `W -= lr * grad` (le sue righe “decidi”); il **senti** è forward + loss + **backward** (capire dove scende).
- **Lacuna #40 → 🟡** (ciclo+dimensione passo presenti in prosa; mapping codice da rifissare).
- **Valutazione (primo tentativo):** **6.5/10**.
- *Fix applicato (etichette codice):* `(a)` su forward, `(b)` sugli update, `(c)` sul `for`. **#40 → 🟢**. Idealmente `(a)` = blocco fino a `backward`, `(b)` = tutte e 4 le righe `-=`. Prosa ancora “passo poi senti” (residuo soft).

### 2026-07-29 — Cap.06 Mini 4.1.A (train su dataset lineare facile)

- Setup corretto (N=200, d=5, y da `X[:,0]+X[:,1]>0`); `train_rete_2_layer(..., h=16, n_epochs=300)` (lr default 0.1 ok).
- Risultati: loss finale **0.0885** (<0.3 e <0.1), acc **0.975** (>0.9). Assert passano. Curva monotona discendente.
- **Valutazione (primo tentativo):** **10/10**.

### 2026-07-29 — Cap.06 Mini 4.3.A (confronto lr)

- Loop su `[0.001, 0.01, 0.1, 1.0]`, stesso dataset 4.1.A, `verbose=False`; `n_epochs=200` via default ok.
- Risultati: 0.001→loss~0.80 acc 0.56; 0.01→0.44/0.80; 0.1→0.12/0.98; **1.0→0.024/1.0**. Commento “converge meglio 1.0” corretto *su questo* problema facile a 200 epoch.
- Nota didattica: lr alto non è sempre meglio (su XOR / loss rumore può oscillare); qui il dataset lineare lo regge. Preferibile passare `n_epochs=200` esplicito.
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-29 — Cap.06 TODO 1 (forward + ispezione cache)

- Setup `(20,4)` / h=6, forward, stampa shape cache, assert `H>=0` e `P in (0,1)` — corretti e passano.
- Scostamento minore: consegna `W2 = he_init(..., seed=1)`, tu hai `seed=0` (stesso di W1). Non invalida i check; per riproduibilità allineata alla consegna usa seed 1 su W2.
- **Valutazione (primo tentativo):** **9.5/10**.

### 2026-07-29 — Cap.06 TODO 2 (backward + shape)

- `backward_2layer` + assert shape `(4,6)/(6,)/(6,1)/(1,)` + stampa somma assoluta: ok (passano).
- Scostamenti: (1) consegna `y = rng.integers(0,2,size=20)` — tu hai label lineari da `X[:,0]+X[:,1]`; per le shape va bene, ma non è la consegna; (2) `list = [...]` **ombra** il builtin `list` — rinomina in `shapes_attese`; (3) zip su `.items()` funziona per ordine di inserimento, ma assert per chiave (`result["grad_W1"].shape == (4,6)`) è più robusto.
- **Valutazione (primo tentativo):** **8.5/10**.
- *Rivalutazione post-fix:* `y = rng.integers(...)` e `shape_attese` (niente shadow di `list`). Assert per chiave resta opzionale. **Post-fix: 9.5/10**.

### 2026-07-29 — Cap.06 TODO 3 (sanity_check + bonus bug `/N`)

- Parte base: `sanity_check_grad` ufficiale + assert tutti i max_diff `< 1e-4` — ok.
- Bonus: copia `my_backward_*_bug` senza `/N` + sanity dedicata — **meglio** che sporcare `backward_2layer` ufficiale.
- Manca la verifica positiva del protesto: l’assert sul bug è **commentato**. Serve qualcosa tipo `assert sanity_check_bug["ok"] is False` (o `assert all(v > 1e-4 for ...)`), più stampa dei max_diff buggati. Altrimenti non dimostri che “protesta”.
- **Valutazione (primo tentativo):** **8.5/10**.

### 2026-07-29 — Cap.06 TODO 4 (train lineare + loss curve PNG)

- Training con default h=16/lr=0.1/n_epochs=200; loss finale **0.11** (<0.2), acc **0.987** (>0.95); PNG `figures/06_03_loss_lineare.png` salvato — ok.
- Errori/scostamenti: (1) label **`X[:,0] + X[:,1]`** invece di **`X[:,0] - X[:,1]`** come da consegna; (2) manca check loss iniziale ~0.69 (nel run: **0.85** — non ~0.69); (3) `np.array((...))` superfluo su `y`.
- **Valutazione (primo tentativo):** **8/10**.

### 2026-07-29 — Cap.06 TODO 5 (cerchio + decision boundary)

- Acc finale **0.958** (>0.95), PNG boundary salvato, `n_epochs=500` / `lr=0.1` ok.
- Scostamenti: (1) `X` con **`standard_normal`** invece di **`uniform(-3, 3)`** — distribuzione diversa (più punti vicino all’origine); (2) **`h=16`** (default) invece di **`h=32`**; (3) riscrittura `my_train_*` + lista `parametri` inutile: `train_rete_2_layer` già ritorna `W1`… nel dict; (4) messaggio assert “accuracy non è scesa” — l’accuracy deve **salire**.
- **Valutazione (primo tentativo):** **7.5/10**.
- *Rivalutazione post-fix:* `uniform(-3,3)`, `h=32`, `train_rete_2_layer` ufficiale + pesi dal dict, messaggio assert corretto. **Post-fix: 10/10**.

---

## Lacune e dubbi ancora aperti

- 🟢 #40 Feynman (chiusa; residuo soft ordine analogia)
- 🔴 Pattern #27 formula→codice
- (corollario Q4: spento per campione ≠ spento sempre — ancora da tenere a mente nel mini 2.4/2.5)

---

## Note per il capitolo successivo (cap.07 PyTorch)

- Verificare che il sanity check numerico delle derivate (TODO 6.1 vecchio) sia stato fatto e funzioni. E' il check piu' importante prima di passare a PyTorch.
- Verificare che il mini-progetto su CSV M2 abbia raggiunto i target (loss < 0.3, accuracy paragonabile a LogReg).
- Preparare un notebook Colab con setup `torch + torchvision`, `device = "cuda" if available else "cpu"`, e mostrare che il training loop "vero" (PyTorch) e' lo STESSO concettuale di questo capitolo (forward -> loss -> backward -> update), solo che il backward lo fa autograd automaticamente.
- Mostrare anche il **confronto tempi**: training loop manuale (NumPy) vs `torch.optim.SGD` -> 10-50x piu' veloce in PyTorch su GPU, "ma con piu' magia nascosta".
