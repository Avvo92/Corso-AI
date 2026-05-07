# Diario sessione — Capitolo 01 — Neurone artificiale da zero

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `01_neurone_artificiale.py` |
| **File diario** | `M03_C01_neurone_artificiale_sessione.md` |
| **Stato** | in corso (avvio: 07/05/2026) |
| **Voto difficoltà** | — (assegnato in chiusura) |

---

## Obiettivi del capitolo (per il mentor)

- Costruire il ponte concettuale **layer Dense (Ponte cap.02) → neurone (M3 cap.01)**: un neurone è un layer Dense con `h = 1` + attivazione.
- Far interiorizzare la sequenza **forward = `X @ w + b` → attivazione (sigmoid/ReLU)** come "due passi separati": prima i punteggi (logits), poi la decisione/probabilità.
- Chiudere definitivamente la **Lacuna #28** (logits vs probabilità): il neurone produce un punteggio, è la **sigmoid** che lo trasforma in probabilità tra 0 e 1.
- **Re-check delle lacune quiz aperte** dal cap.02 Ponte:
  - **#23** shape `(N,)` vs `(N, 1)` → quiz d'ingresso Q1 + esercizio E5.
  - **#24** tupla accidentale `(0.1,)` vs `0.1` → quiz d'ingresso Q3 (trova l'errore).
  - **#26** 2 motivi performance BLAS vs loop → quiz d'ingresso Q4.
  - **#27** Feynman "niente termini tecnici" → quiz d'ingresso Q6 + V8.
  - **#29** slicing `X[i]` vs `X[i:i+1]` → quiz d'ingresso Q5.
- Verificare il **recall cross-modulo** (Regola 26): il neurone ricostruisce `X @ W + b` di Ponte cap.02 con `W` collassato a un vettore.
- Preparare il terreno per il cap.02 M3 (rete neurale = neuroni in parallelo + attivazioni concatenate).

---

## Domande durante lo studio

- _(template — il mentor le aggiungerà man mano)_
- **Q:** …
  **Nota / risposta sintetica:** …

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" con nuovo voto solo se l'utente lo richiede esplicitamente.
> - Riferimento puntuale al blocco/righe del file `01_neurone_artificiale.py`.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [YYYY-MM-DD] — Quiz d'ingresso Q1-Q6 (cerniera cap.02 Ponte)

- **Blocco:** `01_neurone_artificiale.py` — Quiz d'ingresso (Q1: shape `X @ w` lacuna #23; Q2: layer Dense = h regressioni in parallelo, output = punteggi non probabilità lacuna #28; Q3: trova l'errore tupla `(0.1,)` lacuna #24; Q4: 2 motivi BLAS vs loop lacuna #26; Q5: `X[5]` vs `X[5:6]` lacuna #29 re-check; Q6: Feynman senza termini tecnici lacuna #27).
- **Valutazione (primo tentativo — "voto esame"):** —/10.
- **Pattern errore / ID contesto:** verifica chiusura lacune #23/#24/#26/#27/#28 e re-check #29.

---

## Lacune e dubbi ancora aperti

- _(da popolare durante il capitolo)_

---

## Note per il capitolo successivo (mentor)

- Se le lacune #23/#24/#26/#27/#28 risultano 🟢 al primo tentativo del quiz d'ingresso → marcarle `🟢 Superato` in `CONTESTO_CORSO.md` (Lacune dai Quiz).
- Se la #28 (logits vs probabilità) è ancora confusa nel quiz di verifica → riproporre nel cap.02 M3 un blocco esplicito sigmoid/softmax PRIMA di parlare di rete a 2 layer.
- Se il `🔄 [RECALL CROSS-MODULO]` (E6) viene completato senza aiuto → marcare il "ponte cap.02 Ponte → cap.01 M3" come consolidato in CONTESTO; altrimenti riprendere il punto in cap.02 M3.
- Per il cap.02 M3 (reti neurali): partire dall'output del progetto incrementale di questo capitolo (neurone manuale vs LogisticRegression M2 cap.04) e generalizzare a `h` neuroni in parallelo (matrice `W` (d, h)).
