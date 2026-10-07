# Diario sessione — Capitolo 01 — Il testo diventa numeri

| Campo | Valore |
|-------|--------|
| **Modulo** | M04 — NLP, Embeddings & Transformers |
| **File capitolo** | `01_testo_come_numeri.py` |
| **File diario** | `M04_C01_testo_come_numeri_sessione.md` |
| **Stato** | chiuso 05/10/2026 |
| **Voto difficoltà** | 4/10 |

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

### [2026-09-30] — Mini 3.1 (IDF a mano)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 3.1 (righe ~665–670)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `log(10/10) = 0` per la parola in tutti i documenti; `log(10/2) = log(5) ≈ 1.609` per quella in 2 su 10. Rapporto e logaritmo giusti.
- **Errori / lacune:** nessuno.
- **Correzione / suggerimento:** —
- **Pattern errore / ID contesto:** —

---

### [2026-09-30] — Mini 3.2 (TF-IDF e sinonimi)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 3.2 (righe ~671–675)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** V/F corretto (Falso). Motivo giusto: TF-IDF non ha nozione di significato, "cedolino" e "busta paga" restano stringhe diverse.
- **Errori / lacune:** La formula è scritta con una barra (`TF / log(...)`), che si legge come divisione. Il peso è il **prodotto** `TF * log(N/df)`.
- **Correzione / suggerimento:** Tenere il prodotto esplicito. Il limite (niente sinonimi) è il ponte verso gli embeddings.
- **Pattern errore / ID contesto:** soft su formula→codice (Pattern #27, già 🟡); concetto del limite 1 acquisito.

---

### [2026-09-30] — Mini 3.3 (IDF alti sul CSV)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 3.3 (righe ~680–685)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Parole allineate all'output (`interessato`, `sensi`, `ottobre`, IDF ≈ 3.40). Commento giusto: IDF alto qui è rarità, non un segnale del tipo di documento.
- **Errori / lacune:** Il commento resta generico. Manca il perché operativo: compaiono in un solo documento (`log(30/1)`), quindi "distintivo" e "capita una volta" qui coincidono.
- **Correzione / suggerimento:** `ottobre` è un mese di una busta; `sensi`/`interessato` vengono da una frase legale. Non classificano busta vs CU.
- **Pattern errore / ID contesto:** giudizio di dominio solido. Codice di prova ancora a livello modulo (già segnalato in chat).

---

### [2026-09-30] — Mini 4.1 (coseno vs distanza euclidea)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 4.1 (righe ~749–753)
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** Il coseno è descritto bene: direzione, non grandezza; documenti di lunghezza diversa possono restare simili. Allineato a #59 (1 = stessa direzione).
- **Errori / lacune:** «La distanza euclidea è la grandezza di un vettore» è falso. Quella è la **norma** `||v||`. La distanza euclidea fra due vettori è `||a - b||`, la lunghezza della differenza.
- **Correzione / suggerimento:** Un testo lungo ha conteggi grandi: in distanza euclidea risulta lontano da uno corto sullo stesso argomento. Il coseno divide per le norme e quel effetto sparisce.
- **Pattern errore / ID contesto:** confusione norma vs distanza; #59 resta 🟡 (direzione ok, da chiudere a freddo al quiz).

---

### [2026-10-01] — Mini 4.1 — **post-feedback**

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 4.1 (righe ~750–753), dopo correzione
- **Valutazione (post-feedback):** **8.5/10**
- **Punti di forza:** Definizione corretta: distanza euclidea = tratto fra le punte. Coseno = stessa direzione, indipendente dalla grandezza.
- **Residuo:** Manca il caso concreto che motiva la scelta: un documento lungo e uno corto sullo stesso argomento hanno le punte lontane solo per i conteggi più grandi.
- **Nota:** voto esame resta **7/10** (1° tentativo).

---

### [2026-10-01] — Mini 4.1 — **post-feedback 2**

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 4.1 (righe ~749–753), dopo il secondo ritocco
- **Valutazione (post-feedback):** **9.5/10**
- **Punti di forza:** Definizione delle punte ok; coseno = direzione. Ora c'è il caso di dominio: testo con parole ripetute vs testo sintetico, stesso contenuto, lunghezze diverse.
- **Residuo:** typo ("abbiamo", "ripeto"). La frase «i vettori possono avere distanze diverse» resta un po' ambigua: la distanza è fra due punte, non una proprietà di un vettore solo.
- **Nota:** voto esame resta **7/10**.

---

### [2026-10-01] — Mini 4.2 (guardia norma zero)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 4.2 (righe ~755–759)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Condizione giusta: nessuna parola del vocabolario → vettore tutto zeri → norma 0 → denominatore del coseno a 0. Ha visto anche che il numeratore (dot) è 0, quindi 0/0.
- **Errori / lacune:** Manca un esempio di dominio: testo vuoto, OCR fallito, oppure solo stopword/numeri che dopo `tokenizza` non lasciano token nel vocabolario.
- **Correzione / suggerimento:** La guardia `return 0.0` evita il NaN e dice «nessuna direzione, quindi nessuna similarità».
- **Pattern errore / ID contesto:** —

---

### [2026-10-01] — Mini 5.1 (tre limiti BoW, esempi di dominio)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 5.1 (righe ~794–800)
- **Valutazione (primo tentativo — "voto esame"):** **9/10**
- **Punti di forza:** Tre esempi suoi, uno per limite. Sinonimi retributivi (`paga base` / `retribuzione base`); ordine perso (`nome cognome` vs `cognome nome`); OOV (`Progressivo` scartato se in vocabolario c'è solo `prog`).
- **Errori / lacune:** `minimale` non è lo stesso concetto di paga base (è un'altra grandezza). L'ordine nome/cognome è un buon esempio meccanico, ma il senso della frase quasi non cambia: il caso grave è un confronto invertito («il netto supera il lordo»).
- **Correzione / suggerimento:** Tenere gli esempi. Al colloquio, sul limite dell'ordine, usare una frase il cui significato si rovescia.
- **Pattern errore / ID contesto:** —

---

### [2026-10-01] — Mini 6.1 (pipeline: documento più simile)

- **Esercizio / blocco:** `01_testo_come_numeri.py` Mini 6.1 (righe ~872–878)
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** Meccanismo corretto per questa funzione, che è BoW + coseno e non TF-IDF: non vince una parola magica, vince la sovrapposizione tra le parole della query e quelle del documento. Ha riconosciuto che il risultato è pertinente.
- **Errori / lacune:** Non nomina il tipo (`busta_paga`). Non dice quali sovrapposizioni lo separano dalle altre buste: `cedolino` e `irpef` stanno in pochi documenti; `netto` e `busta` stanno in quasi tutte le buste e da sole non basterebbero.
- **Correzione / suggerimento:** Due righe: tipo atteso = busta paga; hanno pesato di più le parole della query che le altre buste non hanno.
- **Pattern errore / ID contesto:** soft Pattern #6 (la consegna chiedeva tipo + parola che ha pesato). Chiamata `pipeline_dimostrativa()` ancora a livello modulo.

---

### [2026-10-01] — Quiz verifica V1 (BoW e parola fuori vocabolario)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V1 (righe ~885–891)
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Output giusto: `[0, 1]`. Motivo giusto per `canone`: non sta nel vocabolario, quindi `bag_of_words` la ignora.
- **Errori / lacune:** Nel commento ha scritto `{netto: 1, saldo: 2}`. L'ordine alfabetico con `enumerate` parte da 0: `{netto: 0, saldo: 1}`. Con indici 1 e 2 la scrittura in posizione 2 uscirebbe da un vettore lungo 2.
- **Correzione / suggerimento:** La stampa NumPy reale è `[0. 1.]` (stessi valori). `saldo` della query vale 1 perché nella frase da convertire compare una volta; il doppio `saldo` del primo documento serve solo a mettere la parola nel vocabolario.
- **Pattern errore / ID contesto:** —

---

### [2026-10-01] — Quiz verifica V1 (post-feedback)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V1 (righe ~885–891), seconda valutazione richiesta
- **Valutazione (post-feedback, non sostituisce l'8.5):** **10/10**
- **Punti di forza:** Vocabolario corretto `{netto: 0, saldo: 1}`. Vettore `[0, 1]`: zero `netto`, un `saldo`. `canone` fuori vocabolario, quindi ignorata.
- **Errori / lacune:** —
- **Correzione / suggerimento:** In console NumPy stampa `[0. 1.]`: stessi valori, tipo float.
- **Pattern errore / ID contesto:** —

---

### [2026-10-01] — Quiz verifica V2 (parola in tutti i documenti)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V2 (righe ~893–897)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** Vero, con il conto giusto: `12 * log(5/5) = 12 * 0 = 0`. Ha usato il prodotto TF × IDF e un esempio numerico suo.
- **Errori / lacune:** —
- **Correzione / suggerimento:** Con la formula del capitolo il peso è esattamente 0. In `TfidfVectorizer` con `smooth_idf=True` lo stesso caso resta un numero molto piccolo.
- **Pattern errore / ID contesto:** —

---

### [2026-10-01] — Quiz verifica V3 (fit su train+test)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V3 (righe ~899–909)
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** Nome giusto (preprocessing leakage) e causa giusta: lo split arriva dopo `fit_transform`, quindi vocabolario e IDF hanno già visto il test.
- **Errori / lacune:** Il codice di correzione non gira. `X` a quel punto non esiste: va spezzato `tutti_i_testi`. Manca `X_test = vec.transform(testi_test)`; rifare il fit sul test rimetterebbe il leakage.
- **Correzione / suggerimento:** Prima lo split dei testi grezzi, poi `fit_transform` sul train e `transform` sul test.
- **Pattern errore / ID contesto:** —

---

### [2026-10-02] — Quiz verifica V3 (post-feedback)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V3 (righe ~906–914), seconda valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 7):** **10/10**
- **Punti di forza:** Split sui testi grezzi (`tutti_i_testi`, 80/20). `fit_transform` solo sul train, `transform` sul test. Diagnosi e nome del leakage restano quelli giusti.
- **Errori / lacune:** —
- **Correzione / suggerimento:** In un progetto vero il vettorizzatore sta dentro una Pipeline valutata in cross-validation, così il fit non può rivedere il test per sbaglio.
- **Pattern errore / ID contesto:** —

---

### [2026-10-02] — Quiz verifica V4 (formula del coseno)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V4 (righe ~917–921)
- **Valutazione (primo tentativo — "voto esame"):** **10/10**
- **Punti di forza:** `np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))`, la stessa formula di `coseno()`.
- **Errori / lacune:** —
- **Correzione / suggerimento:** Se una delle due norme è 0, questa riga divide per zero. In `coseno()` quel caso ritorna `0.0`.
- **Pattern errore / ID contesto:** formula del coseno ok; #59 resta da chiudere a freddo (TODO 5 / quiz), non su questo riempimento.

---

### [2026-10-02] — Quiz verifica V5 (definizione di IDF)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V5 (righe ~924–927)
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Effetto giusto: parola in molti documenti → IDF basso, poco indicativa; parola in pochi documenti → IDF alto.
- **Errori / lacune:** La domanda «in quanti documenti c'è questa parola?» è la document frequency (`df`), il conteggio grezzo. L'IDF è il peso di rarità che si ricava da quel conteggio: `log(N / df)`.
- **Correzione / suggerimento:** Due righe: l'IDF dice quanto la parola è rara nel corpus; serve ad abbassare le parole ovunque e ad alzare quelle che distinguono il tipo di documento.
- **Pattern errore / ID contesto:** —

---

### [2026-10-02] — Quiz verifica V6 (Feynman: testo in numeri)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V6 (righe ~929–935)
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Pipeline dei conteggi chiara e giusta: pulizia, segnaposto, stopword, vocabolario alfabetico, borse della stessa lunghezza e dello stesso ordine, conteggi diversi. Nessuna formula, niente parola vietata.
- **Errori / lacune:** Manca la seconda domanda («perché non basta contare»: le parole ovunque non distinguono, quindi si abbassa il loro peso). Manca un'analogia sua. «Borsa di parole» è il nome tecnico, non l'analogia.
- **Correzione / suggerimento:** Aggiungere 2–3 frasi: un'analogia da web (schede con caselle, filtri di un catalogo) e il caso `importo` contro `cedolino`.
- **Pattern errore / ID contesto:** Pattern **#6** (job espliciti saltati). Concetto TF-IDF già ok in V2/V5: qui è consegna incompleta, non lacuna nuova.

---

### [2026-10-02] — Quiz verifica V7 (test 95%, produzione no)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V7 (righe ~937–944)
- **Valutazione (primo tentativo — "voto esame"):** **6/10**
- **Punti di forza:** Tre cause nel pezzo giusto (vocabolario, normalizzazione, token), non nel modello. La prima è la più vicina: in produzione compaiono parole che il vocabolario del train non ha.
- **Errori / lacune:** Nessun bullet ha il controllo chiesto dalla consegna. La terza («tokenizzato male») non spiega perché il test resta al 95%: se l'errore è identico in test e in produzione, il test non crolla. La seconda parla di similarità e query, che è la ricerca, non il classificatore di tipo.
- **Correzione / suggerimento:** Ogni bullet = differenza tra i due ambienti + un controllo. Esempio sul primo: prendi 20 testi reali e conta quante parole finiscono fuori vocabolario.
- **Pattern errore / ID contesto:** Pattern **#6** di nuovo (manca il controllo).

---

### [2026-10-02] — Quiz verifica V8 (numeri nel testo)

- **Esercizio / blocco:** `01_testo_come_numeri.py` V8 (righe ~947–951)
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Posizione giusta: il valore esatto è rumore, cancellare i numeri no. Al posto della cancellazione propone i segnaposto, come fa `normalizza`.
- **Errori / lacune:** Non dice quali (`<importo>` e `<data>`, separati) né perché la presenza resta informativa: un testo con un importo non è lo stesso di un testo senza.
- **Correzione / suggerimento:** Due segnaposto distinti. Effetto collaterale utile: il valore vero (stipendio, data) non resta nel testo.
- **Pattern errore / ID contesto:** —

---

### [2026-10-02] — TODO 1 (baseline tipo documento)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 1 (righe ~977–1015)
- **Valutazione (primo tentativo — "voto esame"):** **7/10**
- **Punti di forza:** Pipeline giusta, `fit` solo sul train, split stratificato con `random_state=42`. Recall per classe calcolato bene: su questo split `altro` 0, le altre classi 1. Commento sul leakage corretto (il `fit` del tubo non riallena in `predict`).
- **Errori / lacune:** `acc_score` calcolato e non stampato. Manca il commento (e): l'accuracy è affidabile? Le metriche per classe sono solo il recall. `TfidfVectorizer()` di default non usa `tokenizza`.
- **Correzione / suggerimento:** Stampare l'accuracy. Accanto al recall, precision per classe (o `classification_report`). Il commento parte dal recall 0 di `altro`: nel test quella classe è un documento solo.
- **Pattern errore / ID contesto:** Pattern **#6** (punti d ed e della consegna incompleti).

---

### [2026-10-02] — TODO 1 (post-feedback)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 1 (righe ~977–1019), seconda valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 7):** **8/10**
- **Punti di forza:** Accuracy stampata (0.833). Formula di precision e recall giuste, con la guardia sullo zero. `tokenizer=tokenizza` nel tubo. Commento sul leakage invariato e corretto.
- **Errori / lacune:** La riga «Precision» stampa `{rec}`, quindi il recall. Su `busta_paga` la precision vera è 2/3: il documento `altro` è stato chiamato busta. Manca ancora il commento (e). Warning: `token_pattern` va messo a `None` quando si passa `tokenizer`.
- **Correzione / suggerimento:** Stampare `prec`. Il commento (e) può partire da lì: accuracy 5/6, ma una busta in più è un `altro` scambiato, e nel test `altro` è un documento solo.
- **Pattern errore / ID contesto:** Pattern **#6** ancora aperto sul punto (e).

---

### [2026-10-02] — TODO 1 (terza valutazione)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 1 (righe ~977–1021), terza valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 7):** **9.5/10**
- **Punti di forza:** Precision stampata con `prec` (busta paga 0.667). `token_pattern=None` e `lowercase=False`. Commento (e) presente: accuracy poco affidabile perché il test è piccolo e la composizione dipende dallo split. Warning di scikit-learn sparito.
- **Errori / lacune:** Il commento non usa i numeri di questo run: 6 documenti in test, `altro` è un solo esempio e viene chiamato busta. «Randomizzazione dei file» è la randomizzazione delle righe.
- **Correzione / suggerimento:** Una mezza riga in più sul commento, con il 5/6 e la precision 2/3 delle buste.
- **Pattern errore / ID contesto:** punto (e) chiuso in forma generica.

---

### [2026-10-02] — TODO 2 (colloquio, 4 domande)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 2 (righe ~1038–1044)
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Quattro bullet, formato rispettato. (1) formula TF × log(N/df) giusta. (2) criterio concreto: se bastano parole spia e non i sinonimi, TF-IDF; esempio cedolino. Commento leakage del TODO 1 era corretto.
- **Errori / lacune:** (1) «Inverted» non è il nome: è Inverse; manca l'effetto in una frase. (3) il limite citato è l'OOV, che è la domanda 4; il limite grave della BoW è l'assenza di significato (o l'ordine). (4) il rimedio «metti nel vocabolario anche i documenti della query» è il leakage: rifà il fit su dati che non sono il train.
- **Correzione / suggerimento:** Default: la parola si scarta. Rimedi: segnaposto per i pattern noti, token a sotto-parole, oppure riaddestrare il vettorizzatore su un nuovo train, non sul documento appena arrivato.
- **Pattern errore / ID contesto:** formato #6 ok. Il rimedio del punto 4 contraddice il commento anti-leakage del TODO 1.

---

### [2026-10-02] — TODO 2 (post-feedback)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 2 (righe ~1038–1044), seconda valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 6.5):** **8.5/10**
- **Punti di forza:** (3) ora cita significato e ordine, non più l'OOV. (4) default giusto (si scarta); rimedi giusti: pezzi, segnaposto, riaddestramento su un train che contiene quelle parole. Non propone più di rifare il vocabolario sulla query.
- **Errori / lacune:** (1) e (2) invariati: «Inverted», manca l'effetto in una frase; «busta» è una spia debole e la lunghezza del documento non decide. (3) elenca due limiti e non dice quale è il più grave, né perché. (4) «spezzare le parole più importanti» è impreciso: si spezzano le parole mai viste, non solo le importanti.
- **Correzione / suggerimento:** Al colloquio, sul punto 3, sceglierne uno e chiudere con la conseguenza (sinonimi estranei, oppure il confronto che si rovescia).
- **Pattern errore / ID contesto:** il rimedio leakage del punto 4 è corretto dopo il feedback. Verifica a freddo ancora nel TODO 4.

---

### [2026-10-02] — TODO 3 (refactoring di `prepara`)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 3 (righe ~1072–1127)
- **Valutazione (primo tentativo — "voto esame"):** **6.5/10**
- **Punti di forza:** Struttura a tre funzioni. Date → `<data>`. Stopword in un set. Token con regex, niente `split(" ")` e niente `print` dentro la funzione. NFC presente.
- **Errori / lacune:** L'analisi non dice il danno del `replace`: `1.703,45` diventa `170345`. `MY_RE_IMPORTO` ha una virgola al posto di `|`, quindi non aggancia nessun importo dei testi di prova. In output non c'è nessun `<importo>`: le cifre spariscono perché `MY_RE_TOKEN` tiene solo le lettere.
- **Correzione / suggerimento:** Il secondo ramo della regex va separato con `|`, come in `RE_IMPORTO` del capitolo. Nell'analisi mancano anche `split(" ")` e il `print` nella funzione.
- **Pattern errore / ID contesto:** soft Pattern **#6** (il danno preciso del replace non è scritto).

---

### [2026-10-02] — TODO 3 (post-feedback)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 3 (righe ~1072–1127), seconda valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 6.5):** **6/10**
- **Punti di forza:** L'analisi ora nomina lo `split` e il fatto che gli importi vengono smontati. Date, stopword e struttura delle funzioni erano già a posto.
- **Errori / lacune:** `MY_RE_IMPORTO` ha il `|` dopo `(\.\d{3})*`, quindi il primo ramo è «1–3 cifre» senza virgola né decimali. Su `01/03/2026` produce tre `<importo>` e lascia il `6`. Su `1.703,45` spezza in due segnaposto. Il danno preciso (`1.703,45` → `170345`) non è ancora scritto. Manca il `print` nella lista dei problemi.
- **Correzione / suggerimento:** Il `|` sta tra i due importi completi: `...,\d{2}\b|\b\d+,\d{2}\b`.
- **Pattern errore / ID contesto:** soft Pattern **#6** ancora sul danno del replace.

---

### [2026-10-02] — TODO 3 (terza valutazione)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 3 (righe ~1072–1127), terza valutazione richiesta
- **Valutazione (post-feedback, non sostituisce il 6.5):** **8.5/10**
- **Punti di forza:** `MY_RE_IMPORTO` è quella del capitolo. Sui testi di prova ogni importo è un solo `<importo>` (`1.703,45`, `2450,00`, `512,30`, `750,00`) e ogni data è un solo `<data>`. Stopword in un set, niente `split` e niente `print` nella funzione.
- **Errori / lacune:** L'analisi dice ancora «spezzati e rincollati», non che `1.703,45` diventa `170345`. Il quarto problema elencato è la normalizzazione Unicode; il `print` dentro la funzione non è nominato.
- **Correzione / suggerimento:** Nel commento, una riga sul numero inventato. Il `print` è il quarto problema di stile: una funzione di preparazione non deve stampare.
- **Pattern errore / ID contesto:** soft Pattern **#6** sul danno preciso, ancora aperto nell'analisi.

---

### [2026-10-05] — TODO 4 (debug produzione)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 4 (righe ~1132–1164), primo tentativo
- **Valutazione (primo tentativo — "voto esame"):** **8/10**
- **Punti di forza:** (a) il secondo `vec` rifà il vocabolario sul testo in arrivo. (b) in test si usava lo stesso vettorizzatore del train. (d) collegato alle mean/std non salvate nel contratto di inferenza del M3 cap.10. Chiude a freddo il punto 4 del TODO 2.
- **Errori / lacune:** (c) l'idea «salva anche il vec» è giusta, ma manca `transform` al posto di `fit_transform`. I file non coincidono: `model_vec.pkl` in scrittura, `modello_vec.pkl` in lettura. Senza `transform`, ricaricare il vec e rifare `fit` rimette il bug.
- **Correzione / suggerimento:** `joblib.dump((modello, vec), "modello_vec.pkl")`, poi `transform` sul testo nuovo.
- **Pattern errore / ID contesto:** lacuna **#60**. Soft Pattern **#6**: la frase operativa copre il salvataggio e non la chiamata in produzione.

---

### [2026-10-05] — TODO 5 (retrieval coseno)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 5 (righe ~1169–1195), primo tentativo
- **Valutazione (primo tentativo — "voto esame"):** **9.5/10**
- **Punti di forza:** Formula `(a @ b) / (||a|| * ||b||)`, `np.linalg.norm`, shape diverse e matrici rifiutate, norma zero → `0.0`, `assert` con `np.isclose` sul vettore con se stesso. Provato: se stesso → 1, zeri → 0, ortogonali → 0. Chiude la lacuna **#59**.
- **Errori / lacune:** Il messaggio di errore parla solo di «uguale dimensione» e copre anche il caso 2D. Nessun buco sulla formula.
- **Correzione / suggerimento:** Nel `ValueError`, separare «shape diverse» da «non sono vettori 1D».
- **Pattern errore / ID contesto:** **#59** → 🟢.

---

### [2026-10-05] — TODO 6 (interleaving tre segnali)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 6 (righe ~1209–1224), primo tentativo
- **Valutazione (primo tentativo — "voto esame"):** **7.5/10**
- **Punti di forza:** (4) il visivo soffre di più su una foto storta, con il limite degli angoli di rotazione in training. (3) la heatmap è «dove ha guardato», e il testuale si può ridurre a un top di parole. (2) il criterio c’è: errori di conti e codice fiscale pesano più della varietà dei layout.
- **Errori / lacune:** (1) il disaccordo non è un documento concreto, e il testuale è un’altra `prob_busta` spinta a 0.5 dalle parole mai viste. (2) i tre segnali corrono la stessa gara; il testuale di questo capitolo dice il tipo. (3) vince il tabellare, mentre all’operatore si mostrano le parole, non il vettore da centinaia di posizioni.
- **Correzione / suggerimento:** Un foglio solo: il testo dice cedolino, il layout no, i conti tornano. Regola: il testuale decide il tipo; visivo e tabellare, con pesi, l’alterazione.
- **Pattern errore / ID contesto:** lacuna **#61**.

---

### [2026-10-05] — TODO 7 (ordine perso nel BoW)

- **Esercizio / blocco:** `01_testo_come_numeri.py` TODO 7 (righe ~1238–1253), primo tentativo
- **Valutazione (primo tentativo — "voto esame"):** **8.5/10**
- **Punti di forza:** Il run stampa `1.0000000000000002`, riportato come 1. (b) i due vettori sono identici perché le parole sono le stesse. `.toarray()` sulla `csr_matrix` dopo un primo crash su `.to_numpy()`.
- **Errori / lacune:** Il codice usa `TfidfVectorizer`, non i conteggi BoW: qui il numero non cambia, le due righe restano uguali. (b) non dice che l'ordine non entra nel vettore. (c) «un modello che distingue il significato» è la zona giusta; il limite isolato da queste due frasi è l'ordine.
- **Correzione / suggerimento:** In (c), un modello che legge la frase in sequenza. Un sacco di significati, senza ordine, darebbe ancora 1.
- **Pattern errore / ID contesto:** lacuna **#62**.

---

### [2026-10-05] — Progetto incrementale T1–T5 (check DoD)

- **Esercizio / blocco:** `testo_utils.py` + note T4 in `01_testo_come_numeri.py` (~1285–1288)
- **Valutazione (primo tentativo — "voto esame"):** **7/10** sul deliverable
- **Punti di forza:** T2 ok (`<cf>` e `<iban>`, i codici non restano nei token). T3 ha le tre chiavi e le parole escono dal testo. T5 ha versione, classi, tokenizer e data.
- **Errori / lacune:** T1: in fondo al file il training e il `print` partono all'import. T4 è nel capitolo, non nel diario, e il «non promette» è vago. T5: `named_step` (manca la s) fa crashare il `return` del contratto.
- **Correzione / suggerimento:** Spostare query/print sotto `if __name__`. Tre righe nel diario. `named_steps`.
- **Pattern errore / ID contesto:** soft Pattern **#6** (DoD di T1 e sede di T4).

---

### [2026-10-05] — Progetto incrementale T1–T5 (post-feedback)

- **Esercizio / blocco:** `testo_utils.py` dopo `if __name__`, `named_steps`, `VERSIONE`; T4 ancora in `01_testo_come_numeri.py` (~1288–1289)
- **Valutazione (post-feedback, non sostituisce il 7/10):** **9/10**
- **Punti di forza:** L'import di `tokenizza` non stampa. Il run dà `busta_paga`, probabilità circa 0.50, parole `netto`/`eur`/`paga` presenti nel testo. Il contratto ha versione, classi ordinate, `tokenizza` e data. Il testo di T4 dice cosa promette e cosa no.
- **Errori / lacune:** T4 è nel capitolo, non nel diario. Manca una terza riga, c'è un `# #` vuoto.
- **Correzione / suggerimento:** Spostare quelle due frasi nel diario del capitolo.
- **Pattern errore / ID contesto:** soft Pattern **#6**, solo sulla sede di T4.

### [2026-10-05] — Chiusura capitolo (voto difficoltà)

- **Esercizio / blocco:** chiusura formale C01. T4 copiato qui dal capitolo (`01_testo_come_numeri.py` ~1288–1289). Il file del capitolo non è stato modificato.
- **Valutazione:** voto difficoltà studente **4/10**. Gli esami restano quelli già registrati (progetto 7, post-feedback 9, non sostituisce il 7).
- **Testo T4 (sue parole):** «parole_decisive promette all'operatore le tre parole di questo testo che hanno spinto di più verso il tipo scelto. Sono parole davvero presenti nel documento, non un vettore da centinaia di caselle. Non promette che quelle tre parole siano la causa del verdetto, né che il tipo sia giusto. Il resto del vocabolario ha pesato comunque, e l'elenco non dice niente sull'ordine della frase.»
- **Errori / lacune:** la sede era il capitolo, non il diario (Pattern #6, già contato nel post-feedback). Manca la terza riga, c'è un `# #` vuoto.
- **Next step:** bridge R01, poi `02a`. Installazione di `sentence-transformers` solo prima di 02b.

---

## Lacune e dubbi ancora aperti

- TODO 2 punto 4: verifica a freddo **passata** nel TODO 4 (05/10, esame 8/10). Ha riconosciuto da solo che rifare il vocabolario sul testo in arrivo stacca il modello dal training.
- Residuo TODO 4 (c): salva il vettorizzatore, ma non scrive `transform` al posto di `fit_transform`, e i due nomi file non coincidono. Lacuna **#60**.
- TODO 6 (05/10, esame 7.5/10): i tre segnali messi sulla stessa domanda. Il testuale di C01 dice il tipo; le parole mai viste si scartano, non producono 0.5. Lacuna **#61**.
- TODO 7 (05/10, esame 8.5/10): il coseno 1 è giusto. In (c) manca la parola «ordine». Lacuna **#62**.

---

## Note per il capitolo successivo (mentor)

- `02a_embeddings_concetto.py` è già scritto. Zero installazioni. I rinforzi #60 #61 #62 sono dentro.
- `sentence-transformers` solo prima di **02b**.
- Bridge `M04_R01_after_C01_before_C02_testo_to_embeddings.md` popolato il 05/10/2026.
- Debito M3: portfolio #2 senza URL, `12_grad_cam_interpretabilita.py` da svolgere, TODO 7 e 🔄 CONFRONTO PRIMA/DOPO del cap.10, archivio M3 non creato.
