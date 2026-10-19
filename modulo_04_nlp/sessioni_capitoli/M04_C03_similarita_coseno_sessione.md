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

---

## Lacune e dubbi ancora aperti

- Bridge R02 es.1: attenzione a prevedere **tutti** gli output quando ci sono più `print`.

---

## Note per il capitolo successivo (mentor)

- _
