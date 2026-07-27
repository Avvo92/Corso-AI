# M3 — Bridge quiz ripasso — dopo Cap.05 (chain_rule_gd) → prima Cap.06 (backprop_training)

**Quando:** dopo chiusura cap.05 chain_rule_gd, prima di aprire cap.06 backprop_training.
**Tempo stimato:** 15–20 minuti (cap.06 e' tosto, conviene arrivare freschi sui fondamentali).
**Regola:** `CONTESTO_CORSO.md` → Regola 40.

> Questo bridge e' il **piu' importante** del modulo: introduce il capitolo piu' difficile.
> Focus: chain rule numerica, direzione del GD, learning rate, shape della rete 2-layer,
> `dL/dp` vs `dL/dz`, ReLU in `z=0`, catena verso `W1`, sanity check numerico.

---

## Istruzioni

- Scrivi le risposte sotto ogni domanda (codice in blocchi ```python o una riga).
- **Non** leggere la sezione *Soluzioni* finché non hai finito.
- Difficoltà: **facile-media** — fondamenti che ti servono assolutamente
  per non perdere la bussola nel cap.06.

---

### 1. [Chain rule numerica] Prevedi il valore

Hai `h(x) = (2x + 3)^2`.

(a) Scrivi `h'(x)` con la chain rule.
(b) Quanto vale in `x = 1`?

TUA RISPOSTA:

---

### 2. [Direzione del GD] Vero / Falso + correzione

> "Per **minimizzare** la loss aggiorno il peso con `w = w + lr * grad`."

Vero o falso? Se falso, scrivi la formula corretta e spiega in una riga *perché*.

TUA RISPOSTA:

---

### 3. [Learning rate] Abbina sintomo → causa

Abbina ogni sintomo alla causa (`lr troppo grande` / `lr troppo piccolo`):

| Sintomo | Causa |
|---------|-------|
| Dopo 500 epoche la loss è scesa solo da 0.69 a 0.65 | ? |
| La loss sale, oscilla e poi diventa `nan` | ? |
| L'accuracy resta a 0.5 e i pesi si muovono di pochissimo | ? |

TUA RISPOSTA:

---

### 4. [🔁 Recall #37 — ReLU in zero] Prevedi output

```python
z = np.array([-2.0, 0.0, 3.0])
print(derivata_relu(z))
```

Con la convenzione del corso (la stessa di PyTorch). Scrivi l'output esatto.

TUA RISPOSTA:

---

### 5. [🔁 Recall #38 — `dL/dp` vs `dL/dz`] Completa la tabella

Con `p = sigmoid(z)` e loss BCE, per **un** campione:

| Derivata | Formula |
|----------|---------|
| `dL/dp` | ? |
| `dp/dz` | ? |
| `dL/dz` | ? |

Poi rispondi in una riga: **quale delle tre** è `p - y`, e perché le altre due no.

TUA RISPOSTA:

---

### 6. [🔁 Recall #39 — catena verso W1] Ordina la catena

Rete: `Z1 = X @ W1 + b1` → `H = ReLU(Z1)` → `Z2 = H @ W2 + b2` → `P = sigmoid(Z2)` → `L = BCE(P, y)`.

Ordina questi 5 anelli per ottenere `dL/dW1` (scrivi la sequenza corretta):

```
dZ1/dW1     dP/dZ2     dH/dZ1     dL/dP     dZ2/dH
```

Poi rispondi: **perché `W2` non è uno degli anelli** della catena verso `W1`?

TUA RISPOSTA:

---

### 7. [Recall cap.02 — shape] Completa

Rete con `N = 12`, `d = 4`, `h = 6`, output 1. Scrivi la shape di:

`X`, `W1`, `b1`, `Z1`, `H`, `W2`, `b2`, `Z2`, `P`

TUA RISPOSTA:

---

### 8. [Regola shape del gradiente] Vero / Falso

> "`grad_W1` può avere shape diversa da `W1`, tanto poi NumPy fa broadcasting."

Vero o falso? Spiega in una riga perché questa regola è il tuo miglior
rilevatore di bug nel backward.

TUA RISPOSTA:

---

### 9. [Sanity check numerico] Trova l'errore

```python
def derivata_numerica(f, x, h=1e-18):
    return (f(x + h) - f(x)) / h
```

Ci sono **due** problemi rispetto allo standard del corso. Quali? Scrivi la versione corretta.

TUA RISPOSTA:

---

### 10. [Python/NumPy base] Prevedi output

```python
A = np.array([[1., 2.],
              [3., 4.],
              [5., 6.]])          # (3, 2)
d = np.array([[0.5],
              [-1.0],
              [2.0]])             # (3, 1)

print((A.T @ d).shape)
print(d.sum(axis=0).shape)
```

TUA RISPOSTA:

---

### 11. [💬 Feynman] Spiega con parole tue

In 3-4 righe, a un collega web dev: **perché il backpropagation è "la chain rule
applicata a una rete"?**

VIETATO: derivata, gradiente, chain rule, layer.
Suggerimento: analogia "passare la colpa indietro lungo la catena di reparti".

TUA RISPOSTA:

---

## Soluzioni — solo dopo il tentativo

**1.** (a) `g(x) = 2x + 3`, `g'(x) = 2`; `f(u) = u²`, `f'(u) = 2u` →
`h'(x) = 2·(2x + 3)·2 = 4·(2x + 3)`.
(b) In `x = 1`: `4 · 5 = 20`.

**2.** **Falso.** Corretto: `w = w - lr * grad`. Il gradiente punta nella direzione
di **massima salita**; per far scendere la loss ti muovi nella direzione **opposta**.

**3.**
- "0.69 → 0.65 in 500 epoche" → **lr troppo piccolo** (scende, ma a passi minuscoli).
- "loss sale, oscilla, `nan`" → **lr troppo grande** (supera il minimo e diverge).
- "accuracy 0.5, pesi quasi fermi" → **lr troppo piccolo**.

Nota: lento ≠ bloccato. Con lr piccolo la loss **scende ancora**, solo pianissimo.

**4.** `[0. 0. 1.]` — regola: **1 se z > 0, 0 se z ≤ 0**. In `z = 0` vale **0**
(non 0.5: quello è `sigmoid(0)`).

**5.**

| Derivata | Formula |
|----------|---------|
| `dL/dp` | `(p - y) / (p · (1 - p))` |
| `dp/dz` | `p · (1 - p)` |
| `dL/dz` | `p - y` |

`p - y` è **`dL/dz`**: nasce dal prodotto delle prime due, dove `p(1-p)` si cancella.
`dL/dp` ha ancora il denominatore; `dp/dz` è solo la derivata della sigmoid.

**6.** Ordine corretto:

```
dL/dP · dP/dZ2 · dZ2/dH · dH/dZ1 · dZ1/dW1
```

`W2` **non** è un anello: è un altro **parametro** (ramo parallelo, serve per `dL/dW2`).
Nel percorso verso `W1`, `W2` compare solo come **valore** dentro `dZ2/dH = W2`,
non come tappa della catena.

**7.**

| Tensor | Shape |
|--------|-------|
| `X` | (12, 4) |
| `W1` | (4, 6) |
| `b1` | (6,) |
| `Z1` | (12, 6) |
| `H` | (12, 6) |
| `W2` | (6, 1) |
| `b2` | (1,) |
| `Z2` | (12, 1) |
| `P` | (12,) |

**8.** **Falso.** `grad_W1.shape` deve essere **identica** a `W1.shape`, altrimenti
`W1 - lr * grad_W1` aggiorna la cosa sbagliata (o esplode via broadcasting silenzioso).
È il rilevatore di bug migliore perché una trasposta dimenticata o un `axis` sbagliato
si vedono **subito** nella shape.

**9.** Due problemi:
1. differenza **in avanti** invece che **centrata** (meno precisa);
2. `h = 1e-18` è **troppo piccolo** → cancellazione numerica, il float64 ha precisione ~1e-16.

Versione corretta:

```python
def derivata_numerica(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2.0 * h)
```

**10.**
```
(2, 1)
(1,)
```
`A.T` è (2, 3), `d` è (3, 1) → prodotto (2, 1). `sum(axis=0)` collassa le righe → (1,).

**11.** Esempio: "Un ordine sbagliato arriva al cliente. Il reparto spedizioni chiede al
magazzino quanto ha contribuito all'errore, il magazzino lo chiede alla produzione, e così
via all'indietro fino al primo reparto. Ogni reparto riceve la sua **quota di colpa** e
corregge il proprio processo di un pochino. Il backprop fa esattamente questo: parte
dall'errore finale e distribuisce la responsabilità all'indietro, fino ai primi pesi."
