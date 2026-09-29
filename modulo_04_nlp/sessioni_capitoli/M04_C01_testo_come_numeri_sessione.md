# Diario sessione — Capitolo 01 — Il testo diventa numeri

| Campo | Valore |
|-------|--------|
| **Modulo** | M04 — NLP, Embeddings & Transformers |
| **File capitolo** | `01_testo_come_numeri.py` |
| **File diario** | `M04_C01_testo_come_numeri_sessione.md` |
| **Stato** | aperto 25/09/2026 — da svolgere |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

1. Far sentire il salto di dominio: nel M3 l'input era già numerico (pixel), qui la conversione in numeri è una **scelta di progetto**.
2. Tokenizzazione robusta su testo italiano sporco (apostrofi, accenti, importi `1.703,45`, date `01/03/2026`), con la scelta di dominio "segnaposto invece di cancellazione" (`<importo>`, `<data>`) — che è anche una mossa di privacy.
3. Bag of Words costruito a mano prima di `CountVectorizer`, per far vedere vocabolario, posizioni fisse e sparsità.
4. TF-IDF spiegato con la sequenza obbligata: intuizione → esempio numerico a mente → codice (`idf_a_mano`) → formula per ultima.
5. Riportare in vita la **similarità coseno** del Ponte cap.01, applicata a vettori di parole.
6. Chiudere sui 3 limiti (sinonimi, ordine, OOV) come ponte esplicito verso gli embeddings del cap.02.
7. Ripartenza morbida dopo il cap.10 M3 (voto difficoltà 8-9): capitolo più corto, senza nuove installazioni, tutto su CPU.

---

## Scelte didattiche di apertura modulo

- **Regola 43** applicata in Sez. 0 con tre ripassi propositivi: `fit`/`transform` + leakage (M2 cap.03/05), similarità coseno (Ponte cap.01), preprocess coerente train/inferenza (M3 cap.10). Servono tutti e tre più avanti nello stesso file.
- **Regola 26** (RECALL CROSS-MODULO obbligatorio nel primo capitolo del modulo): è il TODO 1 — baseline TF-IDF + LogisticRegression in `Pipeline`, ricostruita senza riaprire il M2.
- **Pattern #6** (lettura consegne) rinforzato nel TODO 2: formato dichiarato in modo esplicito ("esattamente 4 bullet") con avviso in testa.
- **Lacune #57 (BatchNorm in `eval()`) e #58 (explainability ≠ probabilità)** non sono state forzate qui: sono argomenti di visione e restano assegnate ai rinforzi già scritti in `12_grad_cam_interpretabilita.py`. Il tema "spiegabilità onesta" torna comunque nel task T4 del progetto incrementale, in versione testuale (`parole_decisive` vs `motivi_top3`).
- **Filo con il M3 cap.10**: il TODO 4 (DEBUG) è il gemello testuale del preprocess incoerente — vettorizzatore rifatto in produzione invece che caricato. Stessa famiglia di bug: non crasha, peggiora.

---

## Verifica tecnica del capitolo (mentor, 25/09/2026)

Eseguito con il venv del corso, tutto verde:

- `demo_bow_a_mano()` e `pipeline_dimostrativa()` girano senza errori (30 documenti, 152 parole di vocabolario, 11 celle non zero sul primo vettore).
- `CountVectorizer` e `TfidfVectorizer` con `tokenizer=tokenizza`, `lowercase=False`, `token_pattern=None`: nessun warning, shape `(24, 130)` / `(6, 130)`.
- Soluzioni verificate contro l'esecuzione reale: Mini 1.1, V1 (`[0. 1.]`), TODO 7 (coseno = 1.0).
- Baseline del TODO 1 fattibile: accuracy ≈ 0.89 sul test split stratificato (numeri piccoli, non affidabili — ed è proprio il punto del sotto-esercizio (e)).
- Nessuna dipendenza nuova: il capitolo gira con numpy/pandas/scikit-learn già installati.

---

## Domande durante lo studio

- _(da compilare)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato".
> - Riferimento puntuale al blocco/righe del file.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.
> - Append-only.

### [2026-09-28] — Quiz ingresso Q7 (idea a naso)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Q7 (righe ~159–168)
- **Valutazione (primo tentativo — "voto esame"):** **9/10** (rubrica aperta: nessuna risposta “sbagliata”)
- **Punti di forza:** Ha già in testa il filo del capitolo: **vocabolario** di tutte le parole + per ogni documento un vettore di **conteggi**. È esattamente Bag of Words.
- **Errori / lacune:** Nome: “hot encoding” / one-hot di solito = presenza 0/1 (una casella attiva), non i conteggi. Quello che ha descritto è **count vector / BoW**, non one-hot classico.
- **Correzione / suggerimento:** A fine capitolo rileggi questa risposta: TF-IDF = stessa idea + peso per rarità; embeddings = superamento dei limiti. Nessuna lacuna da aprire.
- **Pattern errore / ID contesto:** terminologia M2 (one-hot) riusata sul testo — utile da precisare, non bloccante.

---

### [2026-09-28] — Mini 1.3 (segnaposto importo: modello + privacy)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 1.3 (righe ~403–408)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Entrambi i motivi: (modello) valore esatto quasi unico/inutile in BoW ma la **presenza** conta → placeholder; (privacy) non mettere retribuzioni reali nel vocabolario/log.
- **Errori / lacune:** nessuno (un filo più lungo delle 2 righe chieste, contenuto completo).
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

---

### [2026-09-29] — Mini 2.1 (colonne BoW e conteggio "netto")

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 2.1 (righe ~501–506)
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** 4 colonne corrette; "netto" = 2 perché compare due volte in d1. Il vettore `2, 1, 0, 0` è coerente con l'ordine che ha scritto lui.
- **Errori / lacune:** L'ordine delle colonne non è quello del codice: `costruisci_vocabolario` ordina in **alfabetico** → `busta, canone, netto, saldo`. La riga d1 stampata è quindi `1, 0, 2, 0`, non `2, 1, 0, 0`.
- **Correzione / suggerimento:** Il conteggio è giusto; a fissare le posizioni è `sorted()`, non l'ordine di comparsa nel testo.
- **Pattern errore / ID contesto:** ordine del vocabolario (stesso tema "posizione fissa" del contratto classi M3); nessuna lacuna 🔴 nuova.

---

### [2026-09-29] — Mini 2.1 — **post-feedback**

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 2.1 (righe ~502–507), dopo correzione
- **Valutazione (post-feedback):** **9/10**
- **Punti di forza:** Il vettore d1 è ora `1, 0, 2, 0`, cioè l'ordine alfabetico reale (`busta, canone, netto, saldo`). "netto" = 2 resta corretto.
- **Residuo:** tra parentesi le colonne sono ancora scritte `(netto, busta, saldo, canone)`, che non corrisponde a quel vettore.
- **Nota:** voto esame resta **8/10** (1° tentativo).

---

### [2026-09-29] — Mini 2.2 (OOV nel vettore BoW)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 2.2 (righe ~508–513)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `[0, 2, 0, 0]` con ordine alfabetico (`busta, canone, netto, saldo`): `canone` due volte in posizione 1, `sconosciuto` ignorato perché fuori vocabolario.
- **Errori / lacune:** nessuno.
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** ordine colonne del Mini 2.1 applicato correttamente qui.

---

### [2026-09-29] — Mini 2.3 (fit_transform / transform / leakage)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 2.3 (righe ~548–553)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `fit_transform` sul train, `transform` su test/produzione, e il nome preciso **preprocessing leakage** (sottotipo del data leakage: il vocabolario/IDF vedono il test).
- **Errori / lacune:** nessuno.
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** recall leakage M2 solido, applicato al vettorizzatore.

---

## Lacune e dubbi ancora aperti

- _(da compilare durante lo studio)_

---

## Note per il capitolo successivo (mentor)

- Il cap.02 apre con l'installazione di `transformers` / `sentence-transformers`: farla **prima** di iniziare il capitolo, non durante.
- Riprendere i 3 limiti della Sez. 5 come apertura del cap.02: gli embeddings vanno presentati come risposta a quei limiti, non come tecnologia a sé.
- Popolare il bridge `M04_R01_after_C01_before_C02_testo_to_embeddings.md` alla chiusura di questo capitolo (Regola 40).
- Debito M3 da non perdere di vista: portfolio #2 senza URL, `12_grad_cam_interpretabilita.py` da svolgere, TODO 7 e 🔄 CONFRONTO PRIMA/DOPO del cap.10, archivio M3 non creato.
