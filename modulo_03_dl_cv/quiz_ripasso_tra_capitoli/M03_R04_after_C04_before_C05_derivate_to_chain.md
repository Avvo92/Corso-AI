# M3 — Bridge quiz ripasso — dopo Cap.04 (derivate_gradiente) → prima Cap.05 (chain_rule + gd)

**Quando:** dopo chiusura cap.04 derivate_gradiente, **prima** di aprire cap.05 chain_rule_gd.
**Tempo stimato:** 10–15 minuti.
**Regola:** `CONTESTO_CORSO.md` → Regola 40.

---

## Istruzioni

- Scrivi le risposte sotto ogni domanda (codice in blocchi ```python o una riga).
- **Non** leggere la sezione *Soluzioni* finché non hai finito.
- Difficoltà: **facile** — velocità e accuratezza sui fondamentali del cap.04.

---

### 1. Derivata in 1 riga

Cos'è una derivata (senza limiti, senza LaTeX)?

**TUA RISPOSTA:**
la derivata di una funzione f(x) è la pendenza della funzione nel punto x.


### 2. Sigmoid — derivata massima

Qual è il valore **massimo** di `derivata_sigmoid(z)` e in quale `z` si trova?

**TUA RISPOSTA:**
il valore massimo per la derivata di una funzione sigmoide è di 0.25, e la si trova in 0.


### 3. Vanishing — ordine di grandezza

Dopo **4** layer sigmoid in fila (peggiore caso ~0.25 per layer), quanto vale circa `0.25 ** 4`? (numero decimale)

**TUA RISPOSTA:**
0,00390625


### 4. ReLU — prevedi output

```python
z = np.array([-2.0, 0.0, 3.0])
print(derivata_relu(z))
```

Cosa stampa? (lista di 3 numeri)

**TUA RISPOSTA:**

[0, 0.5, 1]

### 5. Semplificazione miracolosa

Con `p = sigmoid(z)` e BCE, qual è `dL/dz` (un campione)?

**TUA RISPOSTA:**

p - y

### 6. dL/dp vs dL/dz

Per lo stesso setup, `dL/dp` è uguale a `p - y`? (Sì/No + 1 riga perché)

**TUA RISPOSTA:**
No. Perchè (p-y) / p(1-p) != p-y.


### 7. Gradiente in (1, 2)

Per `f(x,y) = x**2 + y**2`, qual è il gradiente in `(1, 2)`? (lista `[ , ]`)

**TUA RISPOSTA:**

[2, 4]



### 8. h numerico

Per `derivata_numerica`, quale `h` usa il corso di default? Perché **non** `1e-24`?

**TUA RISPOSTA:**

di default il corso usa eps = 1e-6. 1e-24 sarebbe troppo piccolo e il calcolo della derivata numerica diventerebbe troppo impreciso e inconfrontabile con la derivata analitica.

### 9. Feynman — derivata vs gradiente

In **2 righe** (senza jargon pesante): differenza tra derivata (1D) e gradiente (nD).

**TUA RISPOSTA:**

la derivata è la pendenza di una funzione. Il gradiente è un vettore di derivate parziali, ottenute muovendo un solo parametro della funzione alla volta e lasciando gli altri fissi.



### 10. Recall ordine BCE

Scrivi la chiamata corretta: `bce_loss(?, ?)` con probabilità `P` ed etichette `y`.

**TUA RISPOSTA:**
bce_loss(p, y)


---

## Soluzioni — solo dopo il tentativo

1. La derivata misura la **pendenza** di una funzione in un punto: quanto sale/scende per un piccolo spostamento.
2. Massimo **0.25** in **z = 0**.
3. `0.25**4` = **0.00390625** (~0.004).
4. `[0. 0. 1.]` (o equivalente float).
5. **`p - y`** (solo con sigmoid + BCE).
6. **No** — `dL/dp = (p-y)/(p(1-p))`; `p-y` è `dL/dz` dopo la sigmoid.
7. **`[2, 4]`** (`df/dx=2x`, `df/dy=2y`).
8. Default **`1e-6`**; valori troppo piccoli → cancellazione numerica / rumore float (~1e-16 precisione).
9. Esempio: derivata = pendenza su **una** variabile; gradiente = **lista** di pendenze (una per variabile), altre ferme.
10. **`bce_loss(P, y)`** — prima probabilità, poi etichette.
