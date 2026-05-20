# Archivio Ponte Matematico (M2 → M3)

> Bridge **2 capitoli** tra Machine Learning e Deep Learning.
> Migrato da `CONTESTO_CORSO.md` il **20/05/2026** (Passo 13).
>
> **Regola**: per rinforzi su vettori, matrici, `X @ W + b`, coseno, shape — consultare questo file.
> **Codice**: `ponte_matematico_m2_m3/` · **Diari**: `ponte_matematico_m2_m3/sessioni_capitoli/`

---

## Riepilogo

| Campo | Valore |
|-------|--------|
| Capitoli | 2/2 completati |
| Periodo | ~30/04/2026 – 07/05/2026 |
| Media difficoltà | **9/10** (entrambi i capitoli) |
| Obiettivo | Algebra lineare in codice prima di M3 (neuroni, Dense, backprop in arrivo) |

---

## Progresso per capitolo

| File | Voto | Note |
|------|------|------|
| `01_vettori_da_zero.py` | **9**/10 | Norma, coseno, normalizzazione, mini-progetto top-k similarità; 5 PNG in `figures/`; lacuna #12 NumPy shape **chiusa** |
| `02_matrici_e_layer_dense.py` | **9**/10 | `X @ w + b`, matrici come batch, Dense = regressione multivariata + attivazioni; rinforzo Pattern #23–#25; mini-progetto `classifica_batch` |

---

## Ponti mentali (da riusare in M3+)

- Vettore = istruzioni di spostamento / punto se ancorato all'origine
- Norma = lunghezza; Coseno = direzione (non confonderli)
- Normalizzare = versore (norma 1), utile per similarità
- Pratica simile = coseno alto tra feature vectors
- `X @ W + b` = h regressioni lineari in parallelo → rete con attivazioni

---

## Pattern emersi al Ponte (stato post-M3 cap.01)

| # | Pattern | Chiusura |
|---|---------|----------|
| 23 | Virgole finali `func(),` → tuple | 🟡 → molti punti chiusi in M3 quiz |
| 24 | `iloc` con stringa | 🟡 → rinforzato PM02 Q7, M3 |
| 25 | `np.array` vs `np.ndarray` in type hint | 🟡 |
| 23–29 (lacune quiz Ponte-02) | Shape matmul, tuple bias, Dense=regressione, velocità BLAS, Feynman, logit vs prob, slicing 2D | **🟢** chiuse in quiz ingresso M3 cap.01 (07/05/2026) |

---

## Domande cap.01 (10 entry — sintesi)

Norma `||V||`, norma vs coseno, perché quadrati, coseno su vettore nullo, normalizzazione, direzione in alta dimensione, collegamento RAG, `np.array` vs `ndarray`, `iloc` vs `loc`, algebra lineare in una frase.

---

## Competenze cap.01 (sintesi)

Vettori NumPy, dot product, norma L2, coseno robusto, distanza euclidea, mini-progetto similarità pratiche, Matplotlib `quiver`.

## Competenze cap.02 (sintesi)

Matrici `(N, d)`, prodotto matrice-vettore batch, `layer_dense`, confronto con regressione lineare, ripasso 5 blocchi cap.01, checkpoint C1–C4 (shape, Feynman, slicing).

---

## Diari sessione

| Capitolo | File |
|----------|------|
| 01 | `PM_C01_vettori_da_zero_sessione.md` |
| 02 | `PM_C02_matrici_e_layer_dense_sessione.md` (valutazioni quiz dettagliate) |

---

## Deliverable

- `01_vettori_da_zero.py` (~1020 righe)
- `02_matrici_e_layer_dense.py`
- `genera_infografiche_png.py` + figure PNG didattiche
- `img/dense_shapes_broadcast.png`

---

## Nota per il mentor

Non era previsto un cap.03 Ponte: dopo PM02 si è entrati in **M3 cap.01**. Eventuale cap.03 (gradiente, discesa) resta opzionale post-M3 se serve rinforzo prima di backprop.

---

## Decision log archivio

| Data | Nota |
|------|------|
| 20/05/2026 | Creato archivio; completamento PM02 confermato da diario (chiusura 07/05/2026). |
