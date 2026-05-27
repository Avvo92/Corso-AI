# M3 — Bridge quiz ripasso — dopo Cap.06 (backprop_training) → prima Cap.07 (PyTorch)

**Focus:** cicli, accumuli numerici stabili, liste vs array, **dtype**, introduzione leggera ai tensori (solo concetto), ambiente Colab.

> Nota: questo bridge era originariamente "dopo backprop → PyTorch" quando il modulo aveva 7 capitoli. Dopo lo split del vecchio cap.03 in 4 (03 loss, 04 derivate, 05 chain rule + gd, 06 backprop + training), questo bridge si trova ora dopo il cap.06 e prima del nuovo cap.07.

---

### 1. Prevedi l’output

```python
s = 0.0
for x in [0.1, 0.2, 0.3]:
    s += x
print(round(s, 1))
```

---

### 2. Vero / Falso

“In Python puro, `x += 1` dentro una funzione crea sempre una nuova variabile locale `x` senza toccare il `x` globale.”

---

### 3. Completa

Media di una lista `losses` senza NumPy:

```python
losses = [0.5, 0.4, 0.6]
media = ___ / len(losses)
```

---

### 4. Trova il bug

```python
import numpy as np
g = np.zeros(3)
for _ in range(1000):
    g += np.array([1e-9, 1e-9, 1e-9])
print(g[0] > 0)
```

Potrebbe stampare `False` non per matematica sbagliata ma per **precisione floating**. Cosa faresti per verificare somme molto piccole in modo più robusto (idea in una frase, anche “usare float64 / sommare su array grande”)?

---

### 5. Enumerazione + zip

Hai `epochs = [1, 2, 3]` e `train_loss = [0.5, 0.4, 0.35]`. Stampa righe `"epoch k: loss L"` con **un solo** `for` usando `zip`.

---

### 6. Shape / reshape concettuale

Spiega in una frase perché in DL si vuole spesso `X` di forma `(batch, features)` e non `(features, batch)` quando si moltiplica `X @ W`.

---

### 7. Dict: accesso sicuro

Senza far crashare se manca la chiave `"lr"`, leggi `cfg["lr"]` con default `0.01` usando `.get`.

---

### 8. Vero / Falso

“Google Colab mi obbliga a installare CUDA sul mio PC Windows per usare la GPU del notebook.”

---

### 9. Spiega con parole tue

Cos’è intuitivamente il **gradiente** di una loss rispetto a un peso? (metà frase + metafora tipo “pendenza”.)

---

### 10. List comprehension filtrata

Da `xs = [-1, 0, 2, -3]` ottieni solo i **non negativi** elevati al quadrato:

```python
ys = [___ for x in xs if ___]
```

---

## Soluzioni — solo dopo il tentativo

1. `0.6` (`0.6` float sum exact in this case — actually 0.1+0.2+0.3 can be 0.6000000000000001; round gives 0.6 — good teaching moment if student notices).
2. **Falso** — senza `global x`, `x += 1` **assegna** a locale se `x` è locale; il caso globale richiede `global` per modificare.
3. `sum(losses)`.
4. Accumulo 1000 volta 1e-9 in float32 potrebbe Underflow o restare 0; usare **float64**, o sommare in batch, o scalare i numeri — idea didattica sufficiency.
5. `for k, L in zip(epochs, train_loss): print(f"epoch {k}: loss {L}")`.
6. Convenzione **batch prima** allinea una riga = un esempio → moltiplicazioni e broadcasting sklearn/torch standard.
7. `cfg.get("lr", 0.01)`.
8. **Falso** — GPU è sul **runtime cloud**; il PC serve solo al browser.
9. Indica quanto cambierebbe la loss spostando leggermente quel peso — “pendenza” della superficie errore.
10. `ys = [x**2 for x in xs if x >= 0]` → `[0, 4]`.
