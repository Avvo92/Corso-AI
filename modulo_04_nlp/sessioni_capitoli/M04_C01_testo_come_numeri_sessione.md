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

### [2026-09-25] — Quiz ingresso Q3 (preprocess coerente) — **post-feedback**

- **Esercizio / blocco:** `01_testo_come_numeri.py` Q3 (righe ~124–132), dopo correzione
- **Valutazione (post-feedback):** **9/10**
- **Punti di forza:** Ora c’è il nucleo: predizioni peggiori + **non crasha** = bug silenzioso. Esempi resize/mean-std restano coerenti col contratto.
- **Residuo:** ancora più lungo delle 2 righe richieste; typo “silenzionsi”.
- **Nota:** voto esame resta **6.5/10** (1° tentativo); questo è consolidamento dopo hint.

---

## Lacune e dubbi ancora aperti

- _(da compilare durante lo studio)_

---

## Note per il capitolo successivo (mentor)

- Il cap.02 apre con l'installazione di `transformers` / `sentence-transformers`: farla **prima** di iniziare il capitolo, non durante.
- Riprendere i 3 limiti della Sez. 5 come apertura del cap.02: gli embeddings vanno presentati come risposta a quei limiti, non come tecnologia a sé.
- Popolare il bridge `M04_R01_after_C01_before_C02_testo_to_embeddings.md` alla chiusura di questo capitolo (Regola 40).
- Debito M3 da non perdere di vista: portfolio #2 senza URL, `12_grad_cam_interpretabilita.py` da svolgere, TODO 7 e 🔄 CONFRONTO PRIMA/DOPO del cap.10, archivio M3 non creato.
