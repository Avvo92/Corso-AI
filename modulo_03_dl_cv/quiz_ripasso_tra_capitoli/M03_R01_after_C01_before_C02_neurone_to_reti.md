# M3 — Bridge quiz ripasso — dopo Cap.01 (neurone) → prima Cap.02 (reti)

**Focus:** liste, dizionari, slicing, NumPy base (`shape`, `@`, maschere), recall sklearn **Pipeline** / probabilità. Nessun argomento nuovo delle reti multi-layer.

**Tempo:** ~15–20 min • **Regola 40** (`CONTESTO_CORSO.md`)

---

### 1. Prevedi l’output

```python
a = [1, 2, 3, 4, 5]
print(a[1:4])
print(a[::-1][:3])
```

Scrivi cosa stampa e perché (limite destro dello slice incluso/escluso?).

---

### 2. Vero / Falso

“In Python, `d = {}; d[[1,2]] = 3` è valido perché le liste sono chiavi comuni nei dizionari.”  
Motiva in una riga.

---

### 3. Completa il codice

Data una lista di dizionari `rows`, crea una **lista** con solo i valori della chiave `"score"` usando una **list comprehension**:

```python
rows = [{"id": 1, "score": 0.9}, {"id": 2, "score": 0.3}]
scores = ___ 
```

---

### 4. Trova l’errore (concettuale)

```python
import numpy as np
X = np.array([[1.0, 2.0], [3.0, 4.0]])  # shape (2, 2)
w = np.array([0.5, -1.0])             # shape (2,)
z = w @ X
```

Cosa va storto? Come ottieni `z` di shape `(2,)` come **`X @ w`** (un logit per riga)?

---

### 5. Prevedi il risultato

```python
import numpy as np
y = np.array([0, 1, 0, 1])
p = np.array([0.1, 0.9, 0.2, 0.8])
print(p[y == 1])
print((p >= 0.5).sum())
```

---

### 6. Definizione rapida

Cosa restituisce `predict_proba(X)[:, 1]` in un classificatore binario sklearn (forma dell’output + significato della colonna 1)?

l'output ha shape (N, ). Il significato della colonna 1, ad esempio nel nostro dominio, è la percentuale di appartenenza alla classe alterato.
---

### 7. Completa

Per leggere pesi e bias da un `Pipeline` con step `"model"` che è una `LogisticRegression`:

```python
w = pipe.named_steps["model"].coef_.___() => .ravel()
b = float(pipe.named_steps["model"].intercept_[___]) => 0
```

---

### 8. Vero / Falso

“Dopo `pipe.fit(X_train, y_train)`, posso valutare su `X_train` per decidere se il modello è buono.”  
Rispondi in una frase richiamando un anti-pattern del M2.
Falso, la valutazione va effettuata sul Test Set, che si tiene separato dalla fase di addestramento e valdazione (eseguita tramite la pipe), per poter essere l'arbitro finale che ci fornisce un giudizio imparziale. Altrimenti commetteremmo l'errore di leakage.
---

### 9. Spiega con parole tue (Feynman leggero)

Senza scrivere codice: che differenza c’è tra il **logit** grezzo (`z = X @ w + b`) e la **probabilità** che esce dalla sigmoid?
logit e il dato grezzo, ossia il la somma pesata dei valori di X per i pesi di w (più eventuale bias). La probabilità la estrapoliamo con la sigmoide, ossia l'attivazione che trasforma il dato grezzo in un valore tra 0 e 1, e dunque trasformabile in probabilità
---

### 10. Mini-debug

```python
def conta_positivi(p):
    return p[p >= 0.5].len()

    return len(p[p>= 0.5]) => len va chiamato come funzione e non come metodo
```

Perché in NumPy questo rompe? Scrivi la correzione in una riga (usa ciò che useresti davvero su un array 1D).

---

## Soluzioni — solo dopo il tentativo

1. `[2, 3, 4]` — lo slice `stop` è **escluso**. Seconda riga: inverti → `[5,4,3,2,1]`, primi 3 → `[5, 4, 3]`.
2. **Falso** — le liste **non** sono *hashable* → non possono essere chiavi di `dict`.
3. `scores = [r["score"] for r in rows]` → `[0.9, 0.3]`.
4. `w @ X` moltiplica nel senso sbagliato per questo uso; per un logit per riga: **`z = X @ w`** shape `(2,)`.
5. `p[y == 1]` → `[0.9 0.8]`; `(p >= 0.5).sum()` → **3** (True conta come 1).
6. Colonna delle probabilità della **classe con etichetta “la seconda”** secondo `classes_`; shape `(n_campioni,)`.
7. `ravel()`, `[0]` (o indexing coerente se intercept è array 1D).
8. **Falso** — misura ottimistica; rischio overfitting; si usa hold-out / CV sul **validation/test**, non sul train per giudizi definitivi.
9. Logit = punteggio su scala (−∞,+∞); probabilità = trasformazione **sigmoid** che comprime in (0,1) “grado di confidenza” sulla classe positiva.
10. Gli `ndarray` non hanno `.len()`; usare **`len(p[p >= 0.5])`** o **`(p >= 0.5).sum()`**.
