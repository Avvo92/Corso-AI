# Scheda libro → capitolo: M4 cap.02b (embeddings in pratica)

> Appunto del mentor. Il capitolo sta in piedi senza aprire il PDF (Regola 44d):
> la materia è riformulata dentro `02b_embeddings_pratica.py`. Qui resta la
> traccia di cosa è stato preso, cosa scartato e perché.
> **Regola**: parafrasi + citazione capitolo/sezione. Mai incollare pagine dal PDF.

---

## Metadati

| Campo | Valore |
|-------|--------|
| Capitolo corso | `modulo_04_nlp/02b_embeddings_pratica.py` |
| Sezioni corso target | Sez. 2 (sottoparole), Sez. 3 (pooling), Sez. 4 (contrastivo), Sez. 10 (proiezione 2D), E9 |
| Libri usati | `[ALAMMAR]` (Hands-On Large Language Models) |
| Data scheda | 2026-10-08 |
| Stato | usata in capitolo |

---

## Fonti lette (citazione precisa)

Letto l'indice del PDF (598 pagine) e verificati i titoli delle sezioni; la
materia è stata poi scritta con parole e dominio del corso.

| Codice | Capitolo / sezione PDF | Titolo § |
|--------|------------------------|----------|
| ALAMMAR | cap. 2 "Tokens and Embeddings" | "Word Versus Subword Versus Character Versus Byte Tokens" |
| ALAMMAR | cap. 2 | "Text Embeddings (for Sentences and Whole Documents)" |
| ALAMMAR | cap. 2 | "The Word2vec Algorithm and Contrastive Training" |
| ALAMMAR | cap. 10 "Creating Text Embedding Models" | "What Is Contrastive Learning?" |
| ALAMMAR | cap. 5 (clustering) | "Reducing the Dimensionality of Embeddings" |

---

## Concetti da portare nel corso

1. Tokenizzazione a sottoparole (parola / sottoparola / carattere / byte) e perché elimina l'OOV secco.
2. Pooling: da n vettori di pezzi a un solo vettore di frase (qui: media, dopo che il Transformer li ha fatti "parlare").
3. Apprendimento contrastivo: coppie positive avvicinate, negative allontanate, con un margine.
4. Riduzione a 2D per guardare i dati: perdita di informazione (l'ombra).

---

## Analogie / ponti mentali (stile Gianluca)

- Sottoparole → mattoncini più piccoli: se non c'è il pezzo "cedolino" lo costruisci con tre pezzi che hai.
- Pooling → media dei voti di studenti che hanno discusso il compito prima di consegnare.
- Contrastivo → riunione di condominio: non hai la piantina, solo coppie "vicini di pianerottolo / non c'entrano".
- Proiezione 2D → l'ombra di una sedia sul muro.
- Modello da caricare una volta → singleton nel service container di Laravel.

---

## Esercizi del libro da ADATTARE (non copiare)

| Idea libro | Adattamento corso |
|------------|-------------------|
| Word2vec con vicini/non vicini | E9: tira-e-spingi in 2D su 4 frasi del dominio (cedolino, busta paga, estratto conto, saldo) con margine |
| Raccomandazione per vicinanza di embedding | E8: mini-torre, classificatore (cap.01) + mappa (02a) + MiniLM (02b) sulla stessa query |
| Ridurre le dimensioni per visualizzare | Sez. 10: `proietta_2d` (centrare + SVD) e scatter delle 30 note colorate per tipo |

---

## Tranelli da inserire nei commenti

- Il coseno non ha una scala universale: nello stesso dominio frasi su argomenti diversi stanno a 0.5–0.75 (misurato). Conta la classifica per la stessa query.
- Il troncamento a `max_seq_length` è silenzioso: nessun errore da `encode()`.
- Vantaggio di casa: la mappa 02a è costruita sui documenti in cui cerca (leakage del M2); su 8 query la differenza con MiniLM non è significativa.

## Cosa saltare (troppo avanzato / fuori scope)

- Formula della loss contrastiva vera (InfoNCE, triplet loss): servirebbe solo come etichetta. Nel M8 (fine-tuning) tornerà con il codice.
- Costruzione di un dataset di coppie e fine-tuning di un modello di embedding (cap. 10 intero): M8.
- Embedding multimodali (CLIP): fuori dal ramo testuale.
- Raccomandazione di canzoni: stessa idea, altro dominio.

---

## Blocchi iniettati nel `.py`

- Docstring di apertura: "📚 FONTI (riformulate DENTRO il capitolo, non devi aprire i PDF)".
- Sez. 2 tabella parola/sottoparola/carattere/byte (riformulata).
- Sez. 4 apprendimento contrastivo (riformulato) + esercizio **E9** `📚 [LIBRO RIFORMULATO]` (⭐ facoltativo).

---

## Note mentor (cosa ho scartato e perché)

- Nessun "vai a leggere la sezione X": Regola 44d (richiesta dello studente 08/10/2026).
- Il PDF è stato consultato solo per verificare titoli e struttura; le formulazioni sono mie.
- Non ho promesso che MiniLM sia "meglio" della mappa 02a: misurato 0.75 contro 0.83 su 8 query. La scheda registra la scelta di mostrarlo.
