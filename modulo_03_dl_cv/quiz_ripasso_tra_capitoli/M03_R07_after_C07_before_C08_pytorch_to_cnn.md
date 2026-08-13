# M3 — Bridge quiz ripasso — dopo Cap.07 (PyTorch intro) → prima Cap.08 (CNN)

**Focus:** file path su Windows, `torch` vs `numpy` mental model, batch, Pandas lettura CSV leggera, device (`cpu`/`cuda`) a parole.

**Aggiornato 13/08/2026 (chiusura anticipata cap.07):** esercizi 11–15 = residui #27 / #45 / #46 / `zero_grad` / progetto tabellare.

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

### 11. 🔁 Retrieval — 5 step backward (#45)

Elenca in **5 bullet** (a parole, senza codice lungo) la catena del backward 2-layer del cap.06:
`dZ2 → … → grad_W1`. Poi completa: “In PyTorch questi step li fa ______.”

---

### 12. Trova l’errore (Pattern #27 Micro 27.A)

Nella derivata della sigmoid usiamo spesso `p * (1 - p)`.
Quale delle due è corretta e perché l’altra è un bug tipico?

- A) `p * (1 - y)`
- B) `p * (1 - p)`

---

### 13. Vero / Falso + fix

“Basta chiamare `optimizer.zero_grad()` una sola volta all’inizio del training, prima del `for epoch`.”

---

### 14. Completa (device)

Hai salvato un checkpoint su Colab con GPU. Sul PC di casa (AMD, no CUDA) carichi con:

`torch.load(path, map_location=______)`

Cosa metti al posto dei blank e perché (una frase)?

---

### 15. Mini-progetto mentale (🏗️ M3-07 rinviato)

In 4 bullet: come useresti Dataset + DataLoader + `nn.Linear` (o un piccolo `nn.Module`) su un CSV di feature tabellari (stile M2) per classificazione binaria — senza scrivere tutto il codice, solo la pipeline.

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
11. Bullet tipici: (1) dZ2≈(P−y)/N (2) dW2/db2 (3) dH (4) dZ1 = dH ⊙ ReLU′ (5) dW1/db1. Fill-in: **`loss.backward()`** / **autograd** (non `auto_grad()`).
12. **B** — la derivata di sigmoid dipende da `p`, non dall’etichetta `y`. A è Pattern #27 (simbolo sbagliato).
13. **Falso** — `zero_grad()` **ogni** step/batch, altrimenti i `.grad` si accumulano.
14. `"cpu"` (o `torch.device("cpu")`) — rimappa i tensori salvati su CUDA verso CPU locale.
15. Pipeline: leggere CSV → tensori float/label → Dataset `__getitem__` → DataLoader batch → Module Linear/MLP → BCEWithLogits → loop zero_grad/forward/loss/backward/step → eval accuracy.
