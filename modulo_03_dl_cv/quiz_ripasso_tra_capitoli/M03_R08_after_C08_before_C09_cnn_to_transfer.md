# M3 — Bridge quiz ripasso — dopo Cap.08 (CNN) → prima Cap.09 (transfer learning)

**Focus:** dimensioni immagine come array, `matplotlib` base, directory walking idea, random seed riproducibilità, Pandas filtri.

---

### 1. Shape immagine

Un’immagine RGB 64×64 pixel come array NumPy in formato **height, width, channels** ha shape?

---

### 2. Vero / Falso

“In PyTorch `Conv2d`, di solito l’input è `(N, C, H, W)`.”

---

### 3. Prevedi output

```python
import numpy as np
img = np.zeros((4, 4))
img[1:3, 1:3] = 1
print(img.sum())
```

---

### 4. Matplotlib — ordine minimo

Scrivi le righe minime per: `import matplotlib.pyplot as plt`, creare figura, `imshow` su array 2D `img`, `plt.show()`.

---

### 5. Trova il problema

```python
import numpy as np
a = np.random.rand(3, 32, 32)
b = np.random.rand(3, 64, 64)
c = a + b
```

---

### 6. Path — listare file `.jpg`

Con `pathlib`, come ottieni tutti i `.jpg` in `cartella` (nome metodo tipico / pattern)?

---

### 7. Pandas filtro

DataFrame `df` con colonna `"label"`. Seleziona righe con `label == 1` in **`df_pos`**.

---

### 8. Seed

Perché si imposta `np.random.seed(42)` e `torch.manual_seed(42)` prima di training esperimenti?

---

### 9. Spiega con parole tue

Cos’è il **pooling** in una CNN in analogia “zoom out / sintesi delle zone”?

---

### 10. Try / except pattern

Scrivi mini-blocco: prova `open("x.txt")`, in caso di `FileNotFoundError` stampa `"manca file"` (senza far crashare).

---

## Soluzioni — solo dopo il tentativo

1. `(64, 64, 3)` per HWC; torch usa spesso NCHW ma domanda chiedeva HWC esplicitamente.
2. **Vero**.
3. `4.0` — blocco 2×2 di uni nella matrice 4×4.
4. `plt.figure(); plt.imshow(img, cmap="gray"); plt.show()` (cmap opzionale).
5. Shape diverse `(3,32,32)` vs `(3,64,64)` → broadcast invalido per somma diretta.
6. `list(Path("cartella").glob("*.jpg"))` o simile.
7. `df_pos = df[df["label"] == 1]` oppure `df.query("label == 1")`.
8. Riproducibilità confronti tra run / debug.
9. Riduce risoluzione spaziale aggregando vicini → meno pixel ma più contesto globale / meno parametri.
10. 
```python
try:
    open("x.txt")
except FileNotFoundError:
    print("manca file")
```
