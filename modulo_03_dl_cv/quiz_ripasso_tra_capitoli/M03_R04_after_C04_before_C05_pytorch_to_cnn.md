# M3 — Bridge quiz ripasso — dopo Cap.04 (PyTorch intro) → prima Cap.05 (CNN)

**Focus:** file path su Windows, `torch` vs `numpy` mental model, batch, Pandas lettura CSV leggera, device (`cpu`/`cuda`) a parole.

---

### 1. Vero / Falso

“Un tensore PyTorch `x` con `requires_grad=True` è sempre sulla GPU.”

---

### 2. Completa (concettuale)

In PyTorch, dopo `loss.backward()`, i gradienti si trovano tipicamente in `___` per ogni parametro del modello (nome dell’attributo).

---

### 3. Path Windows / Python

```python
from pathlib import Path
root = Path("modulo_03_dl_cv") / "dati"
print(str(root))
```

È preferibile a concatenare stringhe con `\` a mano — perché (una frase)?

---

### 4. Prevedi (numpy vs tensor idea)

```python
import numpy as np
a = np.array([1.0, 2.0])
b = a * 2
b[0] = 99
print(a[0])
```

---

### 5. Pandas — leggere CSV

Scrivi **due righe**: import `pandas`, poi leggi `"train.csv"` in DataFrame `df`.

---

### 6. Trova l’errore logico

```python
import torch
model = torch.nn.Linear(10, 1)
x = torch.randn(32, 10)
y = model(x)
loss = (y - torch.randn(32)).mean()
loss.backward()
```

Training tipico confronta output con target corretto; qui il target è casuale ogni volta — che problema didattico c’è?

---

### 7. Device check pattern

Scrivi l’idioma tipico:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Perché su **Mac/AMD locale** spesso `cuda.is_available()` è False anche se il codice è “corretto”?

---

### 8. Dict di hyperparameter

Crea `hp = {"lr": 1e-3, "epochs": 5}` e recupera `epochs` con tipo **int** sicuro.

---

### 9. Spiega con parole tue

Differenza tra **dataset** (cosa contiene) e **DataLoader** (cosa fa nel training loop).

---

### 10. Mini-esercizio slicing tensor

`x.shape == (32, 3, 28, 28)` è batch di immagini (N,C,H,W). Come selezioni **solo il primo esempio** del batch mantenendo dimensioni utili per visualizzare shape `(3,28,28)`?

---

## Soluzioni — solo dopo il tentativo

1. **Falso** — `requires_grad` riguarda **autograd**, non il device; GPU è `.to("cuda")` ecc.
2. `.grad` (su leaf tensor / parametri — sintassi richiesta: `.grad`).
3. `pathlib` normalizza separatori ed è portabile (Linux/Windows/Mac).
4. `1.0` — `b` è nuovo array; modifica `b` non tocca `a`.
5. `import pandas as pd` ; `df = pd.read_csv("train.csv")`.
6. Target random ≠ supervisione reale; loss non misura apprendimento significativo.
7. CUDA è NVIDIA; hardware diverso → usa CPU o backend diverso (es. Colab NVIDIA).
8. `int(hp["epochs"])`.
9. Dataset espone campioni; DataLoader **batch**, shuffle, worker parallel — feed al loop di training.
10. `x[0]` oppure `x[0, ...]` → shape `(3,28,28)`.
