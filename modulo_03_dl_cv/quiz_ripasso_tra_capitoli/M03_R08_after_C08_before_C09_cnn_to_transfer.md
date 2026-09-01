# M3 — Bridge quiz ripasso — dopo Cap.08 (CNN) → prima Cap.09 (transfer learning)

**Focus:** dimensioni immagine come array, `matplotlib` base, directory walking idea, random seed riproducibilità, Pandas filtri.

---

### 1. Shape immagine

Un’immagine RGB 64×64 pixel come array NumPy in formato **height, width, channels** ha shape?

(64, 64, 3)

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

## Micro 08.A – 08.E — rinforzi dalla chiusura del cap.08

> Aggiunti il 01/09/2026. Mirati alle lacune emerse nel cap.08 (#48, #49, #50, #51, #52) e al Pattern #6.
> Sono volutamente corti: 1–2 minuti ciascuno, a freddo, senza riaprire il capitolo.

### 08.A — catena dei pool (lacuna #51 / Pattern #28)

Parti da `(8, 16, 32, 32)` e applica **tre** volte `nn.MaxPool2d(2)` di seguito.
Scrivi la shape **dopo ogni pool**, una riga per pool (tre righe in totale).

---

### 08.B — che cos'è il primo numero (lacuna #49)

In un tensore immagine `(1, 28, 28)` il primo `1` è: batch, canale o righe?
E in `(3, 64, 64)`: cosa devi fare **prima** di passarlo a `plt.imshow`?

---

### 08.C — chi calcola i gradienti (lacuna #48)

Metti `requires_grad=False` su tutti i parametri di un modello e poi chiami `loss.backward()`.
Cosa trovi in `.grad` di quei parametri, e **chi** è il componente di PyTorch che li avrebbe calcolati?

---

### 08.D — leggi l'errore, non indovinare (lacuna #52)

```
RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x2048 and 512x2)
```

Sapendo che l'ultimo blocco convoluzionale produce **128 canali**, da `2048` ricava `H` e `W` delle mappe.
Rispondi in **esattamente 3 bullet**: (1) cosa dicono i due numeri, (2) la decomposizione, (3) il fix.

---

### 08.E — formula shape, versione con stride (lacuna #50)

`H = 32`, `kernel = 5`, `padding = 0`, `stride = 2`. Quanto vale `H_out`?
Scrivi la formula completa prima del risultato.

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

### Micro 08.A – 08.E

- **08.A** — `(8, 16, 16, 16)` → `(8, 16, 8, 8)` → `(8, 16, 4, 4)`. Ogni pool dimezza **una volta** H e **una volta** W; `C` non cambia mai. Tre pool = tre dimezzamenti, non sei.
- **08.B** — Il primo `1` è il **canale** (`C`): convenzione PyTorch `(C, H, W)`, grayscale = 1 canale. Per `imshow` su `(1,28,28)` serve `squeeze()` → `(28,28)`. Su `(3,64,64)` serve `permute(1, 2, 0)` → `(64,64,3)`, perché Matplotlib vuole i canali **per ultimi**.
- **08.C** — `.grad` resta `None`: senza `requires_grad=True` le operazioni su quei tensori non vengono tracciate, quindi non entrano nel grafo. Il componente che calcola i gradienti è **autograd** (non la loss, non l'optimizer: la loss è il punto di partenza, l'optimizer usa i `.grad` già calcolati). È esattamente il meccanismo del **freezing del backbone** nel transfer learning.
- **08.D** — (1) `mat1` = `(batch=32, feature=2048)` è ciò che esce dal flatten; `mat2` = `(512, 2)` è il `Linear` che si aspetta **512** feature in ingresso e 2 classi in uscita. (2) `2048 / 128 canali = 16 = 4 × 4`, quindi le mappe sono `4×4` e il flatten dà `128·4·4 = 2048`, mentre il `Linear` è tarato su `512` (es. `128·2·2`). (3) Fix: allineare `in_features` del `Linear` a `128*4*4` **oppure** ripristinare il downsampling mancante se la geometria voluta era davvero `2×2`.
- **08.E** — `H_out = (H + 2*pad - k) / stride + 1 = (32 + 0 - 5) / 2 + 1 = floor(13.5) + 1 = 13 + 1 = **14**`. Il `+ 1` finale non si dimentica mai.
