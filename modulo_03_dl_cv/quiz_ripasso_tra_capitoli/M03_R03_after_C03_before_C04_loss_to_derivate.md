# M3 — Bridge quiz ripasso — dopo Cap.03 (loss) → prima Cap.04 (derivate e gradiente)

**Quando:** dopo chiusura cap.03 LOSS, **prima** di aprire `04_derivate_gradiente.py`.
**Tempo stimato:** 10–15 minuti.
**Regola:** `CONTESTO_CORSO.md` → Regola 40.

---

## Istruzioni

- Scrivi le risposte sotto ogni domanda (codice in blocchi ```python o una riga).
- **Non** leggere la sezione *Soluzioni* finché non hai finito.
- Difficoltà: **facile** — velocità e accuratezza sui fondamentali del cap.03.

---

### 1. Segno BCE — quale formula è corretta?

Quale riga calcola la BCE media su batch (con `p`, `y` array 1D)?

(a) `(y * np.log(p) + (1-y) * np.log(1-p)).mean()`  
(b) `(-y * np.log(p) - (1-y) * np.log(1-p)).mean()`  
(c) `(np.log(p) + np.log(1-p)).mean()`

**TUA RISPOSTA:**

(b)

### 2. Clip bilaterale — perché `(eps, 1-eps)`?

In 1 riga: cosa rompe `np.clip(p, eps, 1)` **senza** `1-eps`?

**TUA RISPOSTA:**

evita che la bce loss produca valore nan, per sigmoid(p) = 1. Dobbiamo proteggere entrambi gli estremi per evitare che la funzione di bce loss produca valori nan per p = 1 e inf per p = 0.

### 3. Ordine argomenti `bce_loss`

La firma del capitolo è `bce_loss(p, y)`. Se scrivi `bce_loss(y, p)`, cosa misuri di sbagliato?

**TUA RISPOSTA (1 riga):**

invertiamo i valori che compaiono nel calcolo della bce loss, che diventarebbe = - p * np.log(y) - (1 - p) * np.log(1 - y)


### 4. Soglia accuracy

Con `P = [0.2, 0.49, 0.51, 0.8]` e `y = [0, 1, 0, 1]`, qual è l'accuracy con soglia **0.5**? (numero decimale)

**TUA RISPOSTA:**

0.5

### 5. BCE a occhio

Con `y=1`, `p=0.01`: la BCE è più vicina a **0.01**, **0.69** o **4.6**?

**TUA RISPOSTA:**

4.6

### 6. Loss vs accuracy (training)

In 1 riga: perché addestriamo minimizzando la **loss** e non l'**accuracy**?

**TUA RISPOSTA:**

per avere un valore continuo che possa essere retroprogato tramite derivate e gradiente, piuttosto che una metrica discreta che ci da un idea di massimo dell'accuratezza del modello

### 7. Maschera etichette UNKNOWN

```python
y = np.array([1, 0, -1, 1])
p = np.array([0.9, 0.1, 0.5, 0.8])
```

Scrivi **una riga** che calcola la BCE solo sulle pratiche con `y in {0, 1}` (usa `bce_loss` del capitolo).

**TUA CODICE:**

bce_loss(p[(y == 0) | (y == 1)], y[(y == 0) | (y == 1)])

### 8. Recall forward 2-layer

Scrivi in 4 righe (o meno) la sequenza forward di `rete_2_layer` (shape concettuali ok).

**TUA RISPOSTA:**

Z1 = X @ W1 + b1 -> shape (N, h)
H = relu(Z1) -> shape (N, h)
Z2 = H @ W2 + b2 -> shape (N, k)
P = sigmoid(Z2) -> shape (N, k) -> k == 1 -> P.ravel() -> shape (N, )

### 9. Sigmoid — dove e perché

Perché la sigmoid va **solo** nell'ultimo layer (2 motivi brevi)?

**TUA RISPOSTA:**
perchè nei layer intermedi si usano funzioni non lineari come relu, che ci aiutano a rappresentare nel modello rapporti non lineri. Utilizzare sigmoid farebbe sparire il gradiente (vanishing gradient).
perchè è solo alla fine che ci serve trasformare i risultati in probabilita'

### 10. 💬 Feynman — pendenza

Spiega in 2 righe cos'è la **pendenza** di una curva a un collega web dev, **senza** usare le parole "derivata" o "gradiente".

**TUA RISPOSTA:**

Immagina di essere su una salita. La pendenza è rappresentata dal guadagno o la perdita in termini di altezza per piccoli spostamenti avanti o indietro.

## Soluzioni — solo dopo il tentativo

1. **(b)** — serve il `-` davanti ai log; altrimenti loss negativa con predizioni buone.
2. Con `(eps, 1)` puoi avere `p=1` → `log(1-p)=log(0)` → inf/NaN sul termine `(1-y)*log(1-p)`.
3. Non confronti probabilità con etichette nella formula giusta; numeri senza senso come loss.
4. `y_pred = (P >= 0.5)` → `[0,0,1,1]` vs `y = [0,1,0,1]` → 2/4 corrette (indici 1 e 2 sbagliati) → **0.5**.
5. **~4.6** (`-log(0.01)`).
6. La loss è continua e differenziabile → il gradiente guida i pesi; l'accuracy è discreta (soglia).
7. Esempio: `mask = np.isin(y, [0, 1]); bce_loss(p[mask], y[mask])`
8. `Z1=X@W1+b1` → `H=ReLU(Z1)` → `Z2=H@W2+b2` → `P=sigmoid(Z2).ravel()`
9. (a) Output probabilistico per classificazione binaria; (b) nei hidden la derivata sigmoid ≤0.25 → vanishing gradient (cap.04).
10. Esempio: "Se il grafico sale, ogni passo a destra fa salire il valore; la pendenza dice quanto sale per ogni passo orizzontale."
