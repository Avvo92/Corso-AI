# M4 — R02 — Ripasso tra cap. 02b e cap. 03

Regola 40. **10 mini-esercizi facili** (5–10 minuti): riscaldano Python/Pandas,
riattivano M2 (soglie e metriche) e tengono caldi gli embeddings del 02b.
Nessun argomento nuovo del cap. 03.

- **Parte A** (1–3): Python / NumPy / Pandas a freddo
- **Parte B** (4–6): recall moduli precedenti (M2)
- **Parte C** (7–10): recall cap. 02/02b

> Se un esercizio ti prende più di 2 minuti, segnalo: è un punto da rinforzare
> nel cap. 03, non una colpa. Scrivi le risposte qui sotto, poi correggi con
> le soluzioni in fondo.

---

## Parte A — Python / NumPy / Pandas

### 1 · Prevedi output

```python
import numpy as np
punteggi = np.array([0.5, 0.9, 0.7])
ordine = np.argsort(-punteggi)
print(ordine)
print(punteggi[ordine[0]])
```

**RISPOSTA:**
[1,2,0]
0.9
---

### 2 · Prevedi output

```python
vicini = [("nota_4", 0.81), ("nota_7", 0.74), ("nota_1", 0.69)]
sopra = [nome for nome, p in vicini if p >= 0.70]
print(sopra)
print(len(sopra))
```
["nota_4", "nota_7"]
2
**RISPOSTA:**

---

### 3 · Completa il codice

Hai un DataFrame `note` con colonna `tipo`. Vuoi solo le righe delle buste paga.

```python
buste = note[________________________]
```

**RISPOSTA:**
buste = note[note['tipo'] == "busta_paga"]
---

## Parte B — Recall M2 (soglie e metriche)

> 🔁 RIPASSO PROPOSITIVO — soglia e semaforo (M2 cap.04): il classificatore dà una
> probabilità (0–1) e TU decidi da che punto in su dire "positivo". Alzare la soglia
> = meno falsi allarmi ma più casi veri persi. Qui sotto si riusa quella stessa idea.

### 4 · Vero o Falso (spiega in una riga)

"Alzare la soglia di accettazione riduce i falsi positivi ma aumenta i casi veri
che lasci fuori."

**RISPOSTA:**

Vero. Alzare la soglia, di fatto rende meno sensibile il modello, e questo si traduce in una precision più alta ma una recall più bassa. La scelta dipende dal dominio, e dalla risposta a "cosa costa di più, avere più falsi allarmi o perdere positivi?"

### 5 · Definizione con parole tue (una riga ciascuna)

Senza formule: cosa misurano **precision** e **recall**?

**RISPOSTA:**
Precision -> Su tutti i positivi segnalati dal modello, quanti erano veri positivi e quanti invece erano dei "falsi allarmi" ?
Recall -> Tra tutti i veri positivi presenti nel dataset, quanti ne ha scovati il modello e quanti gli sono sfuggiti?
---

### 6 · Trova l'errore (E8 del 02b, a freddo)

```python
proba = pipe.predict_proba(["bonifico in uscita"])[0]
classe = pipe.predict(["bonifico in uscita"])[0]
prob_classe_predetta = proba[0]
print(classe, prob_classe_predetta)
```

C'è un errore concettuale su come si legge la probabilità della classe predetta.
Quale?

**RISPOSTA:**
In questo modo non stampiamo la classe predetta, ma solo la prima che compare in ordine alfabetico.
indice = list(pipe.classes_).index(classe)
prob_classe_predetta = proba[indice]
print(classe, prob_classe_predetta)
---

## Parte C — Recall cap. 02 / 02b

### 7 · Vero o Falso (spiega in una riga)

"`embedda('una frase sola', modello)` restituisce un array di shape `(384,)`."

**RISPOSTA:**
Falso, restituisce una matrice di shape (1, 384)
---

### 8 · Completa la frase

"`E` è la mappa delle note (30×384) con tutte le righe a norma 1, `q` è la query
normalizzata. Allora `E @ q` restituisce ______________________ di shape ______."

**RISPOSTA:**
Restituisce il coseno, in una matrice di shape (30, )
---

### 9 · Trova l'errore (Mini 5.1 del 02b, a freddo)

```python
# corpus ha una colonna 'id' numerica da 1 a 30, indici di riga da 0 a 29
for i in range(len(corpus)):
    riga = corpus[corpus['id'] == i]   # voglio la riga numero i
    print(riga['testo'])
```

Perché questo ciclo stampa la riga sbagliata (e salta del tutto una riga)?

**RISPOSTA:**
Gli id della colonna "id" vanno a 1 a 30, mentre gli indici di len(corpus) vanno da 0 a 29, quindi ogni riga si trova spostata avanti di 1. Per stampare la riga giusta, dobbiamo compensare questa differenza, ad es. riga = corpus[corpus['id'] == i + 1] 
---

### 10 · Spiega con parole tue (2 righe a risposta)

a) Che differenza c'è tra una **parola**, un **token** e una **sottoparola**?
b) In una ricerca che restituisce 3 risultati, cosa conta la **precision@3**?

**RISPOSTA:**
a) Parola è una parola intera. Token pezzo base che il modello legge e conta, la sottoparole è un frammento di parola.
b) La precision@3, nel caso descritto, calcola la percentuale di tipi positivi sulle 3 previsioni consegnate dal modello. es. se tipo corretto = "bp", e top_3 = ["bp", "cu", "bp"], 
allora precision_top_k = 2 / 3
---

## Soluzioni

1. `[1 2 0]` e `0.9`. Il segno meno rovescia l'ordine: `argsort(-punteggi)` dà gli
   indici dal punteggio più alto al più basso. `ordine[0]` è l'indice del massimo (1),
   e `punteggi[1]` è 0.9.
2. `['nota_4', 'nota_7']` e `2`. La comprensione filtra le coppie con punteggio
   `>= 0.70`; 0.69 resta fuori.
3. `note['tipo'] == 'busta_paga'` — maschera booleana dentro le quadre
   (come in E2 del 02b: `corpus[corpus['tipo'] == 'altro']`).
4. **Vero.** È il trade-off soglia: soglia alta = entri solo se sei sicuro → pochi
   falsi positivi, ma alcuni veri sotto soglia vengono rifiutati. La soglia si sceglie
   guardando i dati, non a sentimento.
5. Precision = *tra le risposte che ho dato positive, quante erano giuste*;
   recall = *tra i casi veramente positivi, quanti ne ho presi*. (Pagella del 02b:
   "quante bandierine giuste tra quelle piantate" vs "quante ne ho trovate del totale".)
6. `proba[0]` è la probabilità della **prima classe in ordine alfabetico**, non della
   classe predetta. La classe predetta può essere un'altra posizione del vettore
   (nel 02b: `proba[0] = 0.41` ma la classe predetta aveva 0.51). Va trovato l'indice
   della classe predetta dentro `pipe.classes_` (o usato `proba.max()` + la sua classe).
7. **Falso.** Restituisce `(1, 384)`: `embedda` restituisce **sempre una matrice**,
   una riga per testo, anche con un solo testo (E9/E10 del 02b lo imponevano con gli
   assert). `(384,)` sarebbe UNA riga estratta, non l'output della funzione.
8. "…restituisce **i coseni tra la query e ogni nota** (uno per riga) di shape
   **(30,)**". Con norme 1, dot product e coseno coincidono: è la scorciatoia usata
   in `cerca_note` (embed_utils).
9. Gli indici di riga vanno da 0 a 29 ma gli `id` da 1 a 30: con `id == i` la riga
   con `id` 30 non viene mai stampata e la riga `i`-esima che prendi è quella con
   `id = i`, non la riga in posizione `i`. Per la posizione si usa `.iloc[i]`.
10. a) Parola = unità del linguaggio; token = pezzo numerabile che il modello legge;
    sottoparola = frammento di parola (un token può essere una parola intera o un
    pezzo come `##mente`). Nel 02b: "internazionalizzazione" = 1 parola, 7 token,
    di cui 5 sottoparole.
    b) Quanti dei 3 risultati restituiti sono pertinenti: `giusti / 3`
    (es. 2 su 3 → 0.67, come nel quiz di verifica del 02b).
