# Quiz ripasso — Modulo 04 — dopo Cap.01, prima del Cap.02

**Quando:** capitolo 01 chiuso (05/10/2026), prima di aprire `02a_embeddings_concetto.py`.
**Tempo stimato:** 15–25 minuti.
**Regola:** `CONTESTO_CORSO.md` → Regola 40.

## Istruzioni

- Scrivi le risposte sotto ogni domanda.
- Non leggere le soluzioni finché non hai finito.
- Difficoltà: facile.

---

## Parte A — Python

### 1. [Prevedi output]

```python
parole = ["netto", "lordo", "netto"]
print(len(set(parole)), parole.count("netto"))
```
2, 2

### 2. [Completa]

Una lista di coppie va ordinata per il secondo elemento, dal più grande. `sort` restituisce `None`. Scrivi la riga che ordina `coppie` sul posto.

coppie.sort(key=lambda x: x[1], reverse=True)

### 3. [Prevedi output]

```python
query = ("Cedolino paga. " "Netto 1.850,00.")
print(query[0], len(query))
```
C 30
---

## Parte B — Recall M2

> 🔁 RIPASSO PROPOSITIVO — `fit` e `transform` (M2)
> `fit` impara i parametri solo sui dati che gli passi (la media, oppure il vocabolario).
> `transform` applica quei parametri a dati nuovi, senza reimpararli.
> Rifare `fit` sul test, o sul testo appena arrivato, è leakage: le colonne non sono più quelle del modello.

### 4. [Vero / Falso]

In una `Pipeline`, il `fit` del vettorizzatore avviene dentro `pipe.fit`, sui testi che gli passi. Vero o falso?

Vero

### 5. [Definizione]

Precision e recall, una frase ciascuno. Il recall di una classe usa i falsi negativi. Quali sono?

recall = di tutti i veri_positivi, quanti ne ha individuati il modello e quanti gli sono sfuggiti?
precision = di tutti quelli che il modello ha segnalato come positivi, quanti erano davvero positivi e quanti invece non lo erano?

i falsi negativi sono quegli elementi che il modello ha identificato come negativi, ma che in realtà erano positivi.

### 6. [Trova errore]

```python
modello = joblib.load("modello.pkl")
vec = TfidfVectorizer()
X = vec.fit_transform([testo_nuovo])
modello.predict(X)
```
X = vec.fit_transform([testo_nuovo]) -> stiamo vettorizzando a partire dal solo testo della query. La soluzione:
joblib.dump([(1, modello), (2, vec)], "model_vec.pkl") -> modello, vec = [e[1] for e in joblib.load("modello_vec.pkl")] -> X = vec.transform([testo_nuovo])
---

## Parte C — Cap.01

### 7. [Vero / Falso]

TF-IDF di una parola presente in tutti i documenti è alto, perché è importante. Vero o falso?

Falso -> Se una parola è presente in tutti i documenti avrà meno peso rispetto a una che compare poche volte.

### 8. [Completa]

La norma di `[3, 4]` è ____ -> 5. Il coseno di un vettore con se stesso è ____ -> 1. Il coseno di un vettore di soli zeri, nella funzione del capitolo, è ____ -> 0.

### 9. [Trova errore]

La regex del codice fiscale `[a-z]{6}\d{2}[a-z]\d{3}[a-z]` su `rssmra85t10h501z`. Dove si ferma? -> Risposta: `rssmra85t` -> regex giusta `\b[a-z]{6}\d{2}[a-z]\d{2}[a-z]\d{3}[a-z]\b`

### 10. [Spiega con parole tue]

Perché «il netto supera il lordo» e «il lordo supera il netto» hanno lo stesso Bag of Words?

Perchè entrambe le note hanno lo stesso tipo di parole, e tutte compaiono lo stesso numero di volte.

---

## Soluzioni — solo dopo il tentativo

1. `2 2`. Il set toglie il duplicato. `count` conta i due «netto».
2. `coppie.sort(key=lambda t: t[1], reverse=True)`.
3. `C` e la lunghezza dell'intera stringa. Le due virgolette vicine si uniscono. `query[0]` è la prima lettera.
4. Vero.
5. Precision: tra quelli che hai chiamato così, quanti lo erano. Recall: tra quelli che lo erano davvero, quanti hai preso. Il falso negativo è un documento della classe che hai chiamato altrimenti.
6. `fit_transform` sul testo nuovo ricostruisce il vocabolario. Servono il vettorizzatore salvato e `transform`.
7. Falso. Se è in tutti i documenti, l'IDF la abbassa: non distingue nulla.
8. `5`. `1`. `0` (la guardia, non la divisione).
9. Dopo `rssmra` `85` `t` chiede tre cifre e trova `10h`. Manca il giorno (`\d{2}`) e la lettera del comune.
10. Stesse parole, stessi conteggi. L'ordine non entra nel vettore.
