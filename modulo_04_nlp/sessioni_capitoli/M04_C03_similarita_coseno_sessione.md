# Diario sessione — Capitolo 03 — Similarità coseno

| Campo | Valore |
|-------|--------|
| **Modulo** | M04 — NLP, Embeddings & Transformers |
| **File capitolo** | `03_similarita_coseno.py` |
| **File diario** | `M04_C03_similarita_coseno_sessione.md` |
| **Stato** | in corso (bridge R02 in avvio) |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

- Coseno / euclidea / dot su vettori normalizzati; top-k, soglia, precision@k scritti dallo studente (Regola 45)
- Falsi amici (negazione, cifre, match esatto); progetto `match_utils.py`
- Verificare a freddo le lacune #66–#69 (rinforzi già nel file; chiusura formale al quiz ingresso cap.04)

---

## Domande durante lo studio

_(nessuna ancora)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Append-only. Il voto esame è il primo tentativo.

### 2026-10-19 — Bridge R02 es. 1 (`M04_R02` · Prevedi output argsort) — **5/10**

- **Corretto:** il secondo `print` → `0.9` (ha capito che `ordine[0]` punta al massimo).
- **Manca:** il primo `print(ordine)` → atteso `[1 2 0]`. Due `print`, una sola risposta.
- **Next:** rileggere i due `print` e dire cosa stampa ciascuno; ripasso: `argsort(-p)` = indici dal più alto al più basso.
- Soft Pattern **#6** (output incompleto: un pezzo su due).

### 2026-10-19 — Bridge R02 es. 1 post-feedback (`M04_R02`) — **10/10**

- Non sostituisce l’esame **5/10**. Ora: `[1,2,0]` + `0.9` — entrambi i `print` corretti.
- Nit cosmetico: NumPy stampa `[1 2 0]` (spazi, senza virgole); il contenuto e l’ordine sono giusti.

### 2026-10-19 — Bridge R02 es. 2 (`M04_R02` · list comprehension + soglia) — **10/10**

- Entrambi i `print`: `["nota_4", "nota_7"]` e `2`. Filtra correttamente `p >= 0.70`; 0.69 fuori.

### 2026-10-19 — Bridge R02 es. 3 (`M04_R02` · maschera Pandas) — **10/10**

- `note[note['tipo'] == "busta_paga"]` — maschera booleana corretta. Virgolette doppie ok (equivalente a `'busta_paga'`).

### 2026-10-19 — Bridge R02 es. 4 (`M04_R02` · V/F soglia) — **10/10**

- Vero + meccanismo: soglia ↑ → meno sensibile → precision ↑, recall ↓. Chiude col trade-off di costo FP vs FN (dominio). Pronto per Sez. 3 del cap.03.

### 2026-10-19 — Bridge R02 es. 5 (`M04_R02` · precision / recall) — **9.5/10**

- Denominatori giusti: precision = tra i positivi segnalati; recall = tra i veri positivi del dataset.
- Nit: la domanda “quanti veri / quanti falsi” (o “scovati / sfuggiti”) descrive entrambi i pezzi; la metrica in sé è la sola quota dei giusti (TP / predetti+ o TP / veri+). Concetto ok.

### 2026-10-19 — Bridge R02 es. 6 (`M04_R02` · predict_proba[0]) — **7/10**

- Giusto: `proba[0]` è la probabilità della prima classe in ordine alfabetico (`pipe.classes_[0]`), non della classe vincente.
- Impreciso: `print(classe, …)` stampa sì la classe predetta (`predict`); sbagliata è solo la probabilità accoppiata. Confonde “classe stampata” con “probabilità della classe predetta”.
- Fix: indice di `classe` in `pipe.classes_`, oppure `proba.max()` se basta il massimo.

### 2026-10-19 — Bridge R02 es. 6 post-feedback (`M04_R02`) — **9/10**

- Non sostituisce l’esame **7/10**. Fix operativo corretto: `list(pipe.classes_).index(classe)` → `proba[indice]`.
- Resta la frase iniziale imprecisa («non stampiamo la classe predetta»): si stampa `classe`; sbagliata era solo la probabilità. Operativo ok, formulazione ancora un filo storta.

### 2026-10-19 — Bridge R02 es. 7 (`M04_R02` · shape embedda) — **10/10**

- Falso → `(1, 384)`. Contratto matrice a posto. Segnale positivo su lacuna **#66** (resta 🟡 fino a verifica formale al quiz ingresso cap.04).

### 2026-10-19 — Bridge R02 es. 8 (`M04_R02` · E @ q) — **7/10**

- Giusto: con norme 1, `E @ q` dà i coseni (uno per nota).
- Sbagliato: shape `(30, 1)`. Con `q` 1D di shape `(384,)` il risultato è `(30,)`. `(30, 1)` richiederebbe `q` come colonna `(384, 1)`. Eco soft di Ponte #23 (vettore 1D vs colonna 2D).

### 2026-10-19 — Bridge R02 es. 8 post-feedback (`M04_R02`) — **9.5/10**

- Non sostituisce l’esame **7/10**. Shape `(30,)` corretta; coseno ok.
- Nit: `(30,)` è un vettore 1D, non una “matrice” (matrice = 2D). Contenuto a posto.

### 2026-10-19 — Bridge R02 es. 9 (`M04_R02` · id vs posizione) — **9/10**

- Diagnosi #68 ok: id 1–30 vs `i` 0–29 → sfasamento; ultima riga saltata; `id == i+1` funziona se vuoi la posizione `i`.
- Nit: la via diretta per “riga in posizione i” è `corpus.iloc[i]` (senza passare dalla colonna id). Con `id == 0` il DataFrame è vuoto (bug silenzioso). Segnale positivo su **#68**.

### 2026-10-19 — Bridge R02 es. 10 (`M04_R02` · parola/token/sottoparola + precision@k) — **7.5/10**

- **b) 10/10:** precision@3 = giusti/3, esempio 2/3 corretto. Segnale positivo su **#67** (nome e metrica).
- **a) ~6/10:** parola ok; token un po’ vago («base di informazione»); sottoparola ridotta alle «parole rare» — in realtà un token può essere parola intera *o* pezzo; le sottoparole spezzano anche parole comuni. Distinzione presente ma incompleta (#67 lato sottoparola).

### 2026-10-19 — Bridge R02 es. 10 post-feedback (`M04_R02`) — **9.5/10**

- Non sostituisce l’esame **7.5/10**. (a) ora: parola / token (legge e conta) / sottoparola (frammento) — tolta la restrizione «solo rare». (b) invariata e corretta.
- Nit opzionale: esplicitare che un token *può essere* parola intera oppure sottoparola. Typo: «sottoparole» → sottoparola.

### 2026-10-19 — Bridge R02 — bilancio complessivo

- **Media esame (primo tentativo):** **8.5/10** (5 · 10 · 10 · 10 · 9.5 · 7 · 10 · 7 · 9 · 7.5).
- **Solidi:** Pandas/maschera, soglia+precision/recall, shape `embedda` (#66), id vs posizione (#68), precision@k.
- **Da tenere d’occhio:** completezza output (es.1 / soft #6); `proba[0]` ≠ prob della classe predetta (es.6); `(N,)` vs `(N,1)` (es.8); triade parola/token/sottoparola ancora un filo scheletrica (es.10a / #67).
- **Verdetto:** bridge superato. Pronto per `03_similarita_coseno.py`.

### 2026-10-19 — Quiz ingresso C03 Q1 (`03_similarita_coseno.py`) — **10/10**

- `(1, 384)` corretto. `embedda` su stringa → sempre matrice. Conferma a freddo di **#66** (dopo bridge R02 es.7).

### 2026-10-19 — Quiz ingresso C03 Q2–Q8 (`03_similarita_coseno.py`) — media blocco **~9.0/10**

| Q | Voto | Nota |
|---|------|------|
| Q2 | **8/10** | Vero corretto; manca la riga di spiegazione richiesta (norme 1 → coseno = dot). Soft #6. |
| Q3 | **9/10** | #68 ok; fix `i+1` funziona; preferibile `.iloc[i]`. |
| Q4 | **6/10** | Token ≠ «unità semantica»; sottoparola *è* un tipo di token (frammento). Relazione ancora confusa (#67). |
| Q5 | **10/10** | `q / np.linalg.norm(q)`. |
| Q6 | **10/10** | 2/3 ≈ 0.66… — precision@k ok (#67 lato metrica). |
| Q7 | **10/10** | Forma ≠ spazio. |
| Q8 | **10/10** | q non normalizzata → dot ≠ coseno (può > 1). |

- **Media quiz ingresso intero (Q1–Q8):** **~9.1/10** (10+8+9+6+10+10+10+10)/8.
- **#66** e **#68** ok a freddo; **#67** ok su precision@k, debole su token/sottoparola.

### 2026-10-20 — Mini 1.1 (`03_similarita_coseno.py`) — **6.5/10**

- **Ok:** diagonale ≈ 1 (assert + spiegazione); simmetria `S[0,1]≈S[1,0]`; idea di normalizzare prima del matmul.
- **Problema serio:** `E = rng.uniform(...)` **sovrascrive** la mappa reale del setup. Da lì in poi il capitolo lavora su dati random, non su `note_minilm.pkl`. Usare l’`E` già caricato (norme già 1).
- **TODO 4 sbagliato/incompleto:** ha fatto `argsort(coseni)` senza il meno; va `argsort(-s0)` vs `argsort(d0)` → coincidono. Senza meno ottieni l’ordine inverso. Risposta a parole vuota.
- **Next:** togliere il random; `S = E @ E.T`; TODO 4 con il meno + frase «stessa classifica».

### 2026-10-20 — Mini 1.1 post-feedback (`03_similarita_coseno.py`) — **9.5/10**

- Non sostituisce l’esame **6.5/10**. Ora: `E` reale, `S = E @ E.T`, assert ok, `argsort(-(E@E[0]))` vs `argsort(distanze)`, risposta TODO 4: classifica identica.
- Nit: `(s0 == d0).all()` al posto del for; typo «eucliedee». `carica_vettori()` ridondante (E già in setup) ma innocuo.

### 2026-10-20 — Mini 1.2 rinforzo #66 (`03_similarita_coseno.py`) — **10/10**

- TODO 1: `(1, 384)`, `(1, 384)`, `(3, 384)` — contratto matrice ok.
- TODO 2: `q[0]` per passare a `(384,)`. **#66** consolidata nel capitolo.

### 2026-10-20 — Sez. 2.2 `top_k` Regola 45 (`03_similarita_coseno.py`) — **9.5/10**

- `argsort(-punteggi)[:k]` + list di `(idx, punteggio)`: ordine e firma ok. Verificato: `[0.5,0.9,0.7]` → `[(1,0.9),(2,0.7)]`.
- Guardia `k > len` con `ValueError`: scelta valida e documentata.
- Nit: `int(idx)` e `float(punteggi[idx])` per allineare al type hint (ora escono `np.int64`/`np.float64`); typo «lunghezze».

### 2026-10-20 — Sez. 2.2 `top_k` post-feedback — **10/10**

- Non ricalcola l’esame **9.5/10** (già altissimo). Ora: `int`/`float` + typo «lunghezza» sistemati. Firma e comportamento allineati.

### 2026-10-20 — Mini 2.1 verifica `top_k` (`03_similarita_coseno.py`) — **9.5/10**

- TODO 1–2: assert ok (verificati in esecuzione). TODO 3: `>=` corretto.
- Nit: TODO 3 testa solo `todo_1` (2 elementi = un confronto); più robusto sugli score di `top_k(punteggi_guida, 3)`.

### 2026-10-20 — Mini 2.2 query prospetto (`03_similarita_coseno.py`) — **9.5/10**

- Output allineato ai valori attesi: 1/busta 0.612 · 24/altro 0.582 · 5/busta 0.570. Pipeline embedda→matmul→top_k ok.
- Risposta: «vicino onesto» corretta (gap ~0.03, tema soldi).
- Nit: `True` posizionale → meglio `normalizza=True`; `E`/`note` già in setup; `S` qui è vettore punteggi, non la matrice (30,30).

### 2026-10-20 — Mini 2.3 rinforzo #68 (`03_similarita_coseno.py`) — **10/10**

- TODO 1: id prima riga = 1. TODO 2: DataFrame vuoto. TODO 3: posizioni → `.iloc`. **#68** consolidata nel capitolo.

### 2026-10-20 — Mini 2.4 contratto (`03_similarita_coseno.py`) — **10/10**

- TODO 1: `modello_minilm` (chi ha prodotto E). TODO 2: `mappa_dim_minilm` == 384 == `E.shape[1]` (via `E[0].shape[0]`). TODO 3: forma ≠ spazio, serve lo stesso modello. joblib ok dopo il fix. Segnale positivo su #64.

### 2026-10-21 — Mini 3.1 verifica `decidi_con_soglia` (`03_similarita_coseno.py`) — **8.5/10**

- TODO 1–2: assert ok. `decidi_con_soglia` con `v > soglia`.
- TODO 3: ha testato `<` vs `<=` sui *conteggi* corpus (stesso risultato) — utile ma non è la domanda. La domanda: «0.70 con soglia 0.70 passa?» → con il suo `>` **no**. Manca quella riga esplicita (opzionale: `decidi_con_soglia([(0, 0.70)], 0.70) == []`).
- Il blocco `f()`/errori bloccati è già Mini **3.2** (anticipo), non valutato qui.

### 2026-10-21 — Mini 3.2 soglia sul corpus (`03_similarita_coseno.py`) — **9/10**

- TODO 2–3 numeri: 0.70 → bloccati **2**, persi **7**; 0.85 → **6** e **20** (attesi ok).
- TODO 1: leave-one-out ok (`-np.inf` + top_k 1); consegna chiedeva `E[i]` + `top_k(..., 2)[1]` — equivalente.
- Manca sotto RISPOSTE la riga a parole del TODO 3 (trade-off). Nit: typo «pesi»; `f()` rifà embedda 4 volte.

### 2026-10-21 — Mini 3.3 rinforzo E8 (`03_similarita_coseno.py`) — **8.5/10**

- Mostra entrambi i segnali, senza vincitore: ok. Distingue classe+confidenza vs documento+coseno.
- Manca esplicito: entrambi sotto soglia → dichiarare «non lo so» / passa all’umano; i due strumenti misurano domande diverse (categoria vs vicinanza a un doc).

### 2026-10-21 — Mini 3.4 benchmark onesto / scelta soglia (`03_similarita_coseno.py`) — **9.5/10**

- Criterio esplicito: ≥ metà errori (3/6) → soglia **0.73** → bloccati 3, giusti persi 7. Numeri verificati. Ok.

### 2026-10-22 — Mini 3.5 grafico soglia (`03_similarita_coseno.py`) — **9/10**

- TODO 2: 6/6 bloccati, 20/24 persi — ok. TODO 3: trade-off chiaro, non azzerare l’errore a costo di buttare i giusti — ok.
- TODO 1: solo `axvline(0.85)`+`show`; meglio rifare l’istogramma con la linea a 0.85 (o entrambe 0.70 e 0.85 sullo stesso plot).

### 2026-10-22 — Mini 4.1 `precision_su_k` (`03_similarita_coseno.py`) — **8.5/10**

- TODO 1–2 assert ok (2/3 e 1/3); spiegazione TODO 2: non-risposte come errori / non premiare chi risponde poco — ok, allineata al manuale.
- Funzione: denominatore `k` corretto; manca `tipi_vicini[:k]` (conta tutta la lista). Nei mini con len≤k passa; con lista più lunga di k gonfia i giusti.
- Next: slice `[:k]` prima del conteggio (poi Mini 4.2).

### 2026-10-22 — Mini 4.1 `precision_su_k` — **post-feedback 10/10**

- Fix applicato: `tipi_vicini[:k]` prima del conteggio; denominatore resta `k`. Firma Regola 45 ok.
- Voto esame resta **8.5/10** (primo tentativo); questa voce è solo verifica del fix.

### 2026-10-22 — Mini 4.2 glossario precision@k (`03_similarita_coseno.py`) — **6.5/10**

- Pipeline query→top_k→tipi ok; precision@3 ≈ 0.667 assert ok.
- Manca precision@1 (consegna: entrambi; atteso 1.0). Pattern **#6**.
- Nome variabile `prec_su3`, non `precision_at_1` / `precision_at_3` (🔤 del mini).
- TODO 2: idea ok ma «tra quelle restituite» suona come denom=mostrati; meglio «quanti dei primi k posti sono del tipo giusto / k».

### 2026-10-22 — Mini 4.2 — **post-feedback 9/10**

- TODO 1: loop k=1 e k=3 con assert 1.0 e 0.667 — ok (Pattern #6 chiuso sul pezzo).
- Nit 🔤: variabile ancora `prec`, non `precision_at_1` / `precision_at_3`.
- TODO 2: meglio; «su k risultati» implica denom=k. Nit: se ne mostri meno di k, i posti vuoti contano comunque (come Mini 4.1).
- Voto esame resta **6.5/10**.

### 2026-10-22 — Mini 4.3 recall@k (`03_similarita_coseno.py`) — **8.5/10**

- TODO 1: n_bp=9 ok; nit: consegna «con pandas» → usato `sum` su lista (va `(df["tipo"]=="busta_paga").sum()`).
- TODO 2: 2/9 ≈ 0.222 assert ok; stampa anche tetto k/n_bp e recall sul tetto — ottimo. Dipende da `S`/`k` del Mini 4.2 (dopo il for, k=3): funziona, meglio `k=3` esplicito nel blocco.
- TODO 3: tetto k vs R=9 chiaro e corretto.

### 2026-10-22 — Mini 4.3 — **post-feedback 9.5/10**

- TODO 2: blocco autonomo (frase, S, k=3) — ok. TODO 3: refusi corretti.
- Resta nit TODO 1: conteggio ancora con `sum` su lista, non pandas.
- Voto esame resta **8.5/10**.

### 2026-10-22 — Mini 4.4 pagella leave-one-out (`03_similarita_coseno.py`) — **7.5/10**

- TODO 1–2: @1=0.8, @3≈0.667 — numeri ok; leave-one-out `top_k(k+1)[1:]` ok. Nit: non usa `precision_su_k`; `n_tipi` inutilizzato; nome `precision_at_3` anche per k=1.
- TODO 3: giusto che 0.75 (02b) ≠ ~0.667 (qui). Motivo debole: non è «il benchmark è più affidabile»; protocolli diversi (8 query BENCHMARK vs 30 note LOO). In 02b il benchmark era proprio il pezzo fragile (piccolo / autore). Nessuno «mente».

### 2026-10-22 — Mini 4.4 — **post-feedback 9.5/10**

- TODO 3: «nessuno mente / stessa formula / due esami diversi» — ok.
- Restano nit codice (precision_su_k, n_tipi morto). Voto esame resta **7.5/10**.

### 2026-10-22 — Mini 4.4 — **post-feedback #2 10/10**

- Tolto `n_tipi`; `precision_at_k` + `round(..., 3)`. Opzionale: chiamare `precision_su_k` (stesso risultato).
- Voto esame resta **7.5/10**.

### 2026-10-23 — Mini 5.1 rinforzo Micro #6 (`03_similarita_coseno.py`) — **8.5/10**

- a) Idea ok («non» quasi invisibile); manca meccanismo esplicito (pooling/media); typo «vedo»→«vede».
- b) Full-text + parola esatta = significato — ok (copre uso+perché).
- c) Senso/tema/dominio — ok. Micro #6 rinforzo sostanzialmente chiuso in questo pezzo.

### 2026-10-23 — Mini 5.2 rinforzo #69 (`03_similarita_coseno.py`) — **8/10**

- TODO 1: pipeline ok (`embedda` lista + dot). CF ≈ 0.992 ok. Netto: usato `"netto 1850"` senza `"euro"` → ≈0.90 invece di ≈0.935 (testo teoria).
- TODO 2: «valori» / «senso» — allineato alla regola ibrida (equiv. codici+cifre vs titoli/contenuti).
- Nel file RISPOSTA TODO 2 risulta vuota: se l’hai solo in chat, rimettila.

### 2026-10-23 — Mini 5.2 — **correzione voto → 9.5/10**

- Contestazione studente: consegna TODO 1 dice «netto 1850/1851» (senza euro); «euro» è solo nella teoria. Deduzione ritirata — ha seguito la consegna. 0.90 è coerente con quelle stringhe; atteso 0.93 del capitolo è allineato alla versione con euro (incongruenza del file, non dello studente).
- TODO 2 «valori, il senso» accettato; falso allarme «RISPOSTA vuota» (sync/lettura mentor).
- Voto d’esame aggiornato a **9.5/10**.

### 2026-10-23 — Mini 5.3 tokenizza/cifre (`03_similarita_coseno.py`) — **7/10**

- TODO 1: previsto ed eseguito `["netto", "euro"]` — ok.
- TODO 2: «placeholder se formato €, altrimenti scartate» — mezzo vero. Su `1850` plain: **scartate** (`RE_TOKEN` solo lettere). `<importo>` scatta solo se matcha `RE_IMPORTO` (es. `1.850,00` / `1850,00`), non il simbolo €. In TF-IDF: le cifre così **non sono feature**.

### 2026-10-23 — Mini 5.4 corto vs lungo (`03_similarita_coseno.py`) — **9/10**

- TODO 1: corta≈0.428, lunga≈0.658 vs «busta paga» — ok; vince la lunga.
- TODO 2: pooling = media; più pezzi del mondo paghe tirano il vettore — ok. Nit: «media di significato» → media dei vettori/token; e scrivi i due numeri anche in commento RISPOSTE (ora solo print).

### 2026-10-23 — Mini 5.5 strumento per caso (`03_similarita_coseno.py`) — **10/10**

- a SEMANTICO, b ESATTO, c ESATTO, d ENTRAMBI — allineato alle soluzioni (c ammette anche ENTRAMBI: esatto sul «non» + semantico sul tema).

### 2026-10-23 — Mini 6.1 RAM 10M×384 (`03_similarita_coseno.py`) — **6.5/10**

- Risultato numerico ≈15.4 ok (`4*384/100` = scorciatoia di `10e6*384*4/1e9`).
- Consegna: fare il conto in Python con i tre fattori. Manca `10_000_000` esplicito; formula opaca (da dove viene `/100`?). Meglio: `(10_000_000 * 384 * 4) / 1e9`.

### 2026-10-23 — Mini 6.2 resta/cambia vector DB (`03_similarita_coseno.py`) — **9.5/10**

- a) coseno, top-k, soglia, precision@k — ok.
- b) chi fa la matmul + quanti vettori confronti — ok (ANN). Nit opzionale: anche *dove vivono* i vettori (servizio/indice vs NumPy in RAM).

### 2026-10-23 — Quiz verifica V1 (`03_similarita_coseno.py`) — **10/10**

- `s.shape = (30,)` e `s[7]` = coseno tra `q` e `E[7]` — ok (norme 1 → dot = coseno).

### 2026-10-23 — Quiz verifica V2 (`03_similarita_coseno.py`) — **10/10**

- Falso: `argsort(-punteggi)[:5]` → 5 punteggi più alti — ok.

### 2026-10-23 — Quiz verifica V3 (`03_similarita_coseno.py`) — **10/10**

- Bug: `argsort` senza meno → k peggiori; fix `argsort(-punteggi)` — ok.

### 2026-10-23 — Quiz verifica V4 (`03_similarita_coseno.py`) — **9/10**

- Precision → denom `k`; recall → n pertinenti del tipo — ok.
- Nit: «n_vicini_restituiti» può suonare come len(lista); da manuale denom precision è **sempre k** (slot vuoti = errori).

### 2026-10-23 — Quiz verifica V5 (`03_similarita_coseno.py`) — **4/10**

- Blank: `[v for v in vicini if …]` → `v` è la **tupla** `(i, score)`, non il float. Serve `v[1] >= soglia` (o `v[1] > soglia` come nella sua fn con unpack).
- `v > soglia` confronta tupla vs float → sbagliato in questo scheletro. Nella sua `decidi_con_soglia` con `for i, v in vicini` il `v > soglia` invece è coerente.

### 2026-10-23 — Quiz verifica V5 — **post-feedback 9/10**

- Seconda formulazione: confronto sullo **score** con unpack — concetto ok (allineato alla sua `decidi_con_soglia`).
- Nit: `[v for _, v in vicini if v > soglia]` restituirebbe solo i float; per tenere le coppie serve `[(i, s) for i, s in vicini if s > soglia]` (o `v[1]` sullo scheletro originale).
- Nit minore: capitolo dice `>=`, lui usa `>`. Voto esame resta **4/10** (blank originale); post-feedback **9/10**.

### 2026-10-23 — Quiz verifica V6 (`03_similarita_coseno.py`) — **10/10**

- precision@2 = 2/2 = 1.0; precision@4 = 3/4 = 0.75 — ok.

### 2026-10-23 — Quiz verifica V7 (`03_similarita_coseno.py`) — **9.5/10**

- CF → non coseno, match/confronto esatto — ok (#69). Nit: «ricerca esatta» → uguaglianza stringa (dopo normalizzazione), non retrieval.

### 2026-10-23 — Quiz verifica V8 (`03_similarita_coseno.py`) — **10/10**

- Vero: soglia ↑ → più «non lo so»; trade-off meno FP — ok (lato B: anche più giusti persi).

### 2026-10-23 — Quiz verifica V9 (`03_similarita_coseno.py`) — **9.5/10**

- Bug: `i` da argsort = posizione 0..29, non colonna `id` 1..30; fix `iloc[i]` — ok (#68).
- Formulazione «sposta di 1» ok come effetto; più preciso: due indici diversi (riga vs id).

### 2026-10-23 — Quiz verifica V10 Feynman soglia (`03_similarita_coseno.py`) — **8.5/10**

- Idea ok: sotto soglia = rumore / non utile → lista vuota = «non lo so».
- Manca esplicito per collega web: top-k *sempre* restituisce qualcuno (anche spazzatura); mostrarlo = falso positivo fiducioso. «Non lo so» passa la palla all’umano / altro tool.
- Typo: sitamo→stiamo, abbiastanza→abbastanza.

### 2026-10-23 — E1 refactoring cerca_veloce (`03_similarita_coseno.py`) — **10/10**

- `embedda` + `E @ q` + `top_k` — ok, ≤4 righe, Regola 45. Indici identici: 28, 25, 15. Tempi ~uguali (domina encode).

### 2026-10-23 — E2 debug 3 bug (`03_similarita_coseno.py`) — **9/10**

- Bug1 normalizza, Bug2 `-argsort` top alti, Bug3 `iloc` non `id` — tutti trovati; fix ok.
- Nit Bug3/Atto2: IndexError quando `id==0` → DataFrame vuoto → `.iloc[0]`; «sfasa di 1» è l’effetto, il crash è la riga vuota. Silenzio Atto1: tre bug insieme senza eccezione — ok se compreso.

### 2026-10-23 — E3 retrieval coseno_mio (`03_similarita_coseno.py`) — **10/10**

- Formula `a@b/(||a||||b||)`, guardia `den==0 → 0.0`, assert vs `coseno` e vs zero — ok. Extra: check shape/ndim (non richiesti, utili). Typo docstring ValueError «devo»→«devono».

### 2026-10-23 — E4 interleaving TF-IDF vs MiniLM (`03_similarita_coseno.py`) — **8.5/10**

- Pipeline TF-IDF + `top_k` e confronto MiniLM ok. Output: TF-IDF 2×«PROSPETTO PAGA» + residenza; MiniLM busta/ricevuta/LUL.
- Confronto discorsivo nella direzione giusta (parole esatte vs senso/sinonimi).
- Nit: `vicini_mini = vicini_tfidf = [...]` sovrascrive il nome; `E = carica_vettori()` riassegna la E globale. Preferibile `X @ q` come da consegna senza necessariamente densificare tutto subito.

### 2026-10-23 — E4 — **post-feedback 9.5/10**

- Tolti doppio assign e `carica_vettori` su `E`. Resta solo nit opzionale: `.toarray()` su tutta X (ok funzionalmente). Voto esame resta **8.5/10**.

---

## Lacune e dubbi ancora aperti

- Bridge R02 es.1: attenzione a prevedere **tutti** gli output quando ci sono più `print`.

---

## Note per il capitolo successivo (mentor)

- _
