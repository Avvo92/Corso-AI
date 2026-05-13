# M3 — Bridge quiz ripasso — dopo Cap.02 (reti) → prima Cap.03 (backprop)

**Focus:** funzioni, tuple unpacking, NumPy (`reshape`, broadcasting leggero), organizzazione liste di array, recall loss binaria a parole.

---

### 1. Prevedi l’output

```python
def f(x):
    return x * 2, x + 1

a, b = f(3)
print(a, b)
```

---

### 2. Completa

Per ottenere una matrice `W` di shape `(4, 3)` piena di zeri:

```python
import numpy as np
W = np.___((4, 3))
```

---

### 3. Vero / Falso

“In NumPy, `A + b` dove `A.shape == (5, 7)` e `b.shape == (7,)` fallisce sempre.”

---

### 4. Trova l’errore

```python
layers_W = []
for h in [8, 4, 1]:
    layers_W.append(np.random.randn(h, h))
```

Si vogliono pesi da `d_in` neuroni a `d_out`. Perché questo codice è semanticamente sbagliato per una lista di layer?

---

### 5. Prevedi shape

```python
import numpy as np
X = np.ones((10, 5))
W = np.ones((5, 3))
b = np.ones((3,))
Z = X @ W + b
print(Z.shape)
```

---

### 6. Dict comprehension

Da `names = ["a", "b"]` e `vals = [1, 2]` costruisci `{"a": 1, "b": 2}` con **dict comprehension** (o `zip`) in una riga.

---

### 7. Liste vs copia

```python
a = [1, 2, 3]
b = a
b[0] = 99
print(a[0])
```

Output? Come creeresti **`b` copia indipendente** di `a` (lista di numeri)?

---

### 8. Recall M2 / ML

Nome di **due metriche** diverse adatte alla classificazione binaria su dataset sbilanciato (solo nomi + quando guardarle in una frase).

---

### 9. Spiega con parole tue

Perché una rete con più layer **non lineari** può separare pattern che un singolo neurone (una frontiera lineare nel piano delle feature trasformate linearmente) non può?

---

### 10. Mini-refactor

Scrivi equivalente più leggibile usando **enumerate**:

```python
i = 0
for w in lista_pesi:
    print(i, w.shape)
    i += 1
```

---

## Soluzioni — solo dopo il tentativo

1. `6 4` — la funzione restituisce una tupla.
2. `zeros`.
3. **Falso** — broadcasting lungo l’ultima dimensione: `(5,7) + (7,)` → `(5,7)`.
4. Usa dimensioni **ingresso/uscita** diverse per layer; `h,h` ripete la stessa shape senza legame a `d`, sequenza corretta tipo `(d, h1)`, `(h1, h2)`, …
5. `(10, 3)` — bias `(3,)` si espande sulle righe.
6. `{n: v for n, v in zip(names, vals)}`.
7. `99` — `b` è alias; copia: `b = list(a)` o `a.copy()` o slice `a[:]`.
8. Esempio: **recall** (cattura positivi) e **precision** (affidabilità dei positivi predetti); **F1** combina; PR-AUC / ROC-AUC per soglia-free — sceglierne due con uso dichiarato va bene.
9. Ogni layer introduce **non-linearità** → composizione di regioni; combinazioni di confini non lineari vs un solo iperpiano in input originale (intuizione va bene).
10. `for i, w in enumerate(lista_pesi): print(i, w.shape)`.
