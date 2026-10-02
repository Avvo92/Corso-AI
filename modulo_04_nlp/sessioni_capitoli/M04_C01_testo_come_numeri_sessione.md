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

## Lacune e dubbi ancora aperti

- _(da compilare durante lo studio)_

---

## Note per il capitolo successivo (mentor)

- Il cap.02 apre con l'installazione di `transformers` / `sentence-transformers`: farla **prima** di iniziare il capitolo, non durante.
- Riprendere i 3 limiti della Sez. 5 come apertura del cap.02: gli embeddings vanno presentati come risposta a quei limiti, non come tecnologia a sé.
- Popolare il bridge `M04_R01_after_C01_before_C02_testo_to_embeddings.md` alla chiusura di questo capitolo (Regola 40).
- Debito M3 da non perdere di vista: portfolio #2 senza URL, `12_grad_cam_interpretabilita.py` da svolgere, TODO 7 e 🔄 CONFRONTO PRIMA/DOPO del cap.10, archivio M3 non creato.
