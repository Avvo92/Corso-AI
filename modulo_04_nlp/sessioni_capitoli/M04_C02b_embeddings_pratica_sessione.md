# Diario sessione — Capitolo 02b — Embeddings in pratica

| Campo | Valore |
|-------|--------|
| **Modulo** | M04 — NLP, Embeddings & Transformers |
| **File capitolo** | `02b_embeddings_pratica.py` |
| **File diario** | `M04_C02b_embeddings_pratica_sessione.md` |
| **Stato** | in corso (aperto in chiusura 02a, 08/10/2026) |
| **Voto difficoltà** | — / 10 |

---

## Obiettivi del capitolo (per il mentor)

- `sentence-transformers`: `encode()` → vettore di lunghezza fissa (384).
- Dentro la scatola: sottoparole (Sez. 2) e pooling (Sez. 3), con numeri veri.
- Apprendimento contrastivo riformulato dal libro (Sez. 4) + E9 toy.
- Pagella a 3 motori (TF-IDF 0.62 / mappa 0.83 / MiniLM 0.75): onestà su vantaggio di casa e benchmark minuscolo.
- Il coseno non ha scala universale: conta la classifica (Sez. 4, Mini 4.1).
- Caso in cui TF-IDF / full-text vince (codici, cifre, negazione).
- Troncamento silenzioso a 128 pezzi (Sez. 9).
- Non mischiare vettori 02a (dim=4) e MiniLM (384); nome modello nel contratto.
- Installazione **prima** della sessione (fatta 08/10).
- Rinforzi: Pattern **#6** (tre job + antidoto "PUNTI CHE VEDO"), direzione senza nome (ex T5), `np.ndarray`.

## Revisione 08/10/2026 (su richiesta dello studente)

Prima stesura 395 righe giudicata scarna. Riscritto a ~1.680 righe seguendo la nuova **Regola 44**:
pipeline a memoria (E7), cross-capitolo (E8 mini-torre cap.01+02a+02b), glossario in codice (E10),
libro riformulato (E9), guardrail (E11), grafico 2D (Sez. 10), progetto `embed_utils.py` (T1-T5).
Tutte le soluzioni e i numeri citati nel file sono stati eseguiti e verificati prima della consegna.
Errori miei scoperti in verifica e corretti: query di Mini 4.1/E4 (la prima scelta non distingueva TF-IDF da MiniLM), "scala" dei coseni (non esiste), conteggi pezzi.

---

## Domande durante lo studio

_(vuoto)_

---

## Valutazioni esercizi / quiz / mini-esercizi

> Append-only. Il voto esame è il primo tentativo.

### 2026-10-08 — Quiz ingresso Q1 (`02b_embeddings_pratica.py`) — **9/10**

- Corretto: `costruisci_mappa` = fit, `vettore_frase` = transform. Conferma lacuna #60 (resta 🟢).
- Due refusi nei nomi: `costrusci_mappa`, `transfrom`. Il senso non cambia.
- Next: Q2–Q8. Nessuna lacuna nuova.

### 2026-10-08 — Quiz ingresso Q2 (`02b_embeddings_pratica.py`) — **8/10**

- Corretto: Falso. Il coseno vuole la stessa forma; con `dim=8` i vettori a 4 numeri già salvati vanno ricalcolati.
- Manca: anche rifacendo la mappa con la stessa `dim`, gli assi della SVD cambiano. Lacuna **#64** 🔴, da rivedere in V10.
- Refusi: «utilizza», «ricrearni», «data base».

### 2026-10-08 — Quiz ingresso Q2, post-feedback (non è il voto esame) — **9.5/10**

- Il voto che conta resta **8/10**.
- Ora c'è anche il secondo motivo: non mancano 4 numeri, le coordinate sono di un'altra mappa.
- Resta da dire a freddo, in V10: la stessa cosa succede anche tenendo `dim=4`. Lacuna **#64** → 🟡.

### 2026-10-08 — Quiz ingresso Q3 (`02b_embeddings_pratica.py`) — **9.5/10**

- Corretto: vettore di zeri con la shape della mappa; coseno 0.0 per la guardia (divisione per zero); quel 0.0 è indistinguibile da due frasi con significato diverso. Conferma #63 (resta 🟢).
- Mezzo punto: ha chiamato «modello» la mappa del 02a.
- Refusi: «restitutisce», «perchè», «da» al posto di «dà».

### 2026-10-08 — Quiz ingresso Q4 (`02b_embeddings_pratica.py`) — **7/10**

- Corretto: `costruisci_mappa` a ogni query ricalcola e costa; `carica_mappa` legge la mappa già fatta.
- Manca il motivo di correttezza: ricostruire cambia lo spazio, i vettori già salvati non restano confrontabili. Stessa lacuna **#64**, resta 🟡.
- Ha detto «ogni volta che usiamo il programma»; la domanda è «a ogni query».

### 2026-10-08 — Quiz ingresso Q4, post-feedback (non è il voto esame) — **8.5/10**

- Il voto che conta resta **7/10**.
- Ora c'è anche il secondo motivo: la mappa ricalcolata non sta coi vettori già in database.
- Wording ancora morbido: «potrebbe», «configurata», «fruibile». Manca «cambia gli assi / lo spazio». **#64** resta 🟡.

### 2026-10-08 — Quiz ingresso Q5 (`02b_embeddings_pratica.py`) — **9/10**

- Corretto: No. Nessuna etichetta che un operatore possa leggere (né «stipendio» né «IRPEF»).
- La frase in più inverte l'ordine: i rapporti sono la tabella in ingresso, le dimensioni sono le direzioni che ne escono.
- Nessuna lacuna nuova.

### 2026-10-08 — Quiz ingresso Q6 (`02b_embeddings_pratica.py`) — **7.5/10**

- (a) ok: sinonimi / significato, non solo la parola esatta.
- (b) parziale: «scrittura assoluta» è la direzione giusta, senza nominare cifre, IBAN, negazione, nome della dimensione. L'ordine è un limite della media 02a, non il contrasto col full-text.
- (c) l'id pratica è un buon match esatto; «Mario Rossi» è più debole di CF/IBAN. Pattern #6: tre righe scritte, resta 🔴 sul contenuto del (b).

### 2026-10-08 — Quiz ingresso Q7 (`02b_embeddings_pratica.py`) — **10/10**

- `np.ndarray` giusto. `np.array` è la funzione che costruisce, il tipo dell'oggetto è `ndarray`.
- Pattern #25 resta 🟡 finché non lo scrive lui in un type hint del capitolo.

### 2026-10-08 — Quiz ingresso Q8 (`02b_embeddings_pratica.py`) — **10/10**

- No. Costante `MIN_CONTEGGIO = 2`. Una parola vista una volta non entra.
- Tre punti della domanda, tre coperti.
- Ingresso Q1–Q8 chiuso. Media dei primi tentativi: (9+8+9.5+7+9+7.5+10+10) / 8 = **8.75**.

### 2026-10-08 — Mini 0.1 (`02b_embeddings_pratica.py`) — **9.5/10**

- `PUNTI CHE VEDO: 2` prima di scrivere. Due righe, due punti.
- (1) «simile per significato» è un filo più forte di «punta vicino alla query».
- (2) giusto, ed è la spiegabilità mancata in Q6 (b): non si può dire quale parola ha inciso. Pattern #6 resta 🔴 sulla negazione.

### 2026-10-08 — Mini 1.1, esecuzione (`02b_embeddings_pratica.py`) — **10/10**

- (a) shape `(1, 384)`. (b) secondo encode ~0.027 s, il primo fuori dal cronometro.
- `PUNTI CHE VEDO: 2`. Nessuna lacuna nuova.
- Il voto è su quella corsa. Nel file, dopo, la chiamata non cronometrata non c'è più.

### 2026-10-08 — Mini 1.2 (`02b_embeddings_pratica.py`) — **7/10**

- Cassetto ok: `_MODELLO` fuori dalla funzione, seconda chiamata non ricarica. Esecuzione: un solo load, `assert a is b` verde («tutto ok!»).
- La chiave non entra in `carica_modello_frasi()` e manca il default `nome=MODELLO_ST`: `modello_una_volta()` senza argomenti non parte.
- Frase su `is`/`==` invertita su `==`. Lacuna **#65** 🔴. `PUNTI CHE VEDO` lasciato vuoto.

### 2026-10-08 — Mini 1.2, post-feedback (non è il voto esame) — **8.5/10**

- Il voto che conta resta **7/10**.
- Frase sistemata: `==` = contenuto, `is` = stesso oggetto nel cassetto. `PUNTI CHE VEDO: 3`. **#65** → 🟡.
- Resta: `carica_modello_frasi()` non riceve `nome`, e manca `nome=MODELLO_ST`. Il test chiama `modello_una_volta(MODELLO_ST)`, non `modello_una_volta()`.

### 2026-10-08 — Mini 2.1 (`02b_embeddings_pratica.py`) — **7.5/10**

- Esecuzione: cedolino 3 pezzi, stipendio 2, xyzzyq spezzata (`_x y zzy q`), niente crash. La riga finale è giusta.
- `emolumenti` è calcolato e non stampato. La consegna chiedeva quattro numeri: in stampa ci sono tre liste.
- `PUNTI CHE VEDO: 3`. Pattern #6: un elemento dei quattro non arriva al print.

### 2026-10-08 — Mini 2.1, post-feedback (non è il voto esame) — **9.5/10**

- Il voto che conta resta **7.5/10**.
- Ora stampa i quattro `len`, `emolumenti` compreso. La riga sulla parola inventata c'era già ed è giusta.
- Refuso rimasto: «La parole».

### 2026-10-09 — Mini 3.1, esecuzione (`02b_embeddings_pratica.py`) — **9.5/10**

- Shape: `token_vettori` (7, 384) e (62, 384); `embedda` (1, 384) e (1, 384). Tre punti coperti, `PUNTI CHE VEDO: 3`.
- La riga è giusta: la lunghezza sparisce nel pooling, e `token_vettori` è prima di quella media.
- Refuso: «perchè». 40 parole sono diventate 62 righe (pezzi + i due speciali): non era chiesto, il numero lo mostra.

### 2026-10-09 — Mini 3.2 (`02b_embeddings_pratica.py`) — **8.5/10**

- `mean(axis=0)` giusto. L'esecuzione stampa «Tutto ok»: la media delle righe coincide con `embedda`, anche con `atol=1e-9`.
- Confronta `emb_frase_1` di shape `(1, 384)` e non `[0]` di shape `(384,)`. NumPy allinea lo stesso le due forme, per questo l'assert passa.
- Stampa una frase, non `True`/`False` come chiesto. `PUNTI CHE VEDO: 2`.

### 2026-10-09 — Mini 4.1 (`02b_embeddings_pratica.py`) — **8.5/10**

- Previsione: a alto, b medio, c basso. Misura: 0.688, 0.736, 0.094. Codice ok (`embedda` + `[0]` + `coseno`).
- Dopo la misura: (b) più alto di (a), niente scala assoluta. È il punto del mini.
- Manca il perché: stesso dominio (soldi) tiene vicine anche frasi di argomento diverso; la traduzione può stare sotto. «Non misurabile» è forte: si misura, non si legge da solo.

### 2026-10-09 — Mini 5.1, esecuzione (`02b_embeddings_pratica.py`) — **7/10**

- Stampato: dimensioni 384, parametri 117.65, pezzi vocabolario 250002. Chiavi del dizionario giuste. `PUNTI CHE VEDO: 3`.
- `max_seq_length` è 384, deve essere 128. Ha chiamato `get_sentence_embedding_dimension()` (il vecchio nome della dimensione): il FutureWarning lo dice. L'attributo è `max_seq_length`.
- Pattern #6: l'aiuto nel mini elencava già l'attributo giusto e avvisava del metodo rinominato.

### 2026-10-09 — Mini 5.1, post-feedback (non è il voto esame) — **10/10**

- Il voto che conta resta **7/10**.
- Ora `max_seq_length` legge `model.max_seq_length` (128). Le altre tre chiavi erano già giuste: 384, 117.65, 250002.
- I nomi interni `max_seq_lenght` e `milion_parameters` restano storti. Le chiavi del dizionario stampato sono quelle chieste.

### 2026-10-09 — Mini 5.2 (`02b_embeddings_pratica.py`) — **7.5/10**

- (1) giusto: perdita silenziosa, i numeri escono lo stesso, affinità debole. `PUNTI CHE VEDO: 2`.
- (2) la misura è un coseno, ma la coppia è italiano-inglese. Per il bug del collega servono due parafrasi italiane, e il coseno va calcolato sui due modelli.
- Nessuna coppia nominata (es. «cedolino di marzo» / «prospetto paga di aprile»).

### 2026-10-09 — Mini 6.1 (`02b_embeddings_pratica.py`) — **8/10**

- Esecuzione: `{'tfidf': 0.0, 'minilm': 0.546}`. Numeri giusti. `PUNTI CHE VEDO: 3`.
- MiniLM non sbaglia: vede il legame. Il vantaggio della mappa (stessi documenti, leakage) è vero.
- Manca la lezione della Sezione 4: 0.546 e 0.96 non sono la stessa scala. Conta la classifica sulla stessa query (0.55 contro ~0.17 di una frase che non c'entra).

### 2026-10-12 — Mini 6.2 (`02b_embeddings_pratica.py`) — **9/10**

- Esecuzione: TF-IDF `17 altro`, `6 cu`, `28 altro`. MiniLM `6 cu`, `7 cu`, `9 cu`. Indici e tipi giusti. `PUNTI CHE VEDO: 3`.
- Conclusione giusta: MiniLM ha capito, tre CU. Refuso in etichetta: «tdidf».
- Nella riga manca il contrasto: TF-IDF mette un `altro` al primo posto e una sola CU in mezzo.

### 2026-10-12 — Mini 6.3 (`02b_embeddings_pratica.py`) — **7.5/10**

- Copertura stampata: `0.0`, `0.667`, `0.0`. Giusta. Podio TF-IDF vuoto, MiniLM tre vicini `[(9, 0.627), (1, 0.606), (22, 0.599)]`.
- La riga spiega solo il vuoto: nessuna parola della query 1 sta nel vocabolario TF-IDF. `PUNTI CHE VEDO` lasciato vuoto.
- Manca l'altra metà: MiniLM spezza quelle parole in pezzi noti, quindi ha comunque un vettore e il podio si riempie. Stesso punto del Mini 2.2, ancora vuoto.

### 2026-10-12 — Mini 6.3, post-feedback (non è il voto esame) — **8.5/10**

- Il voto che conta resta **7.5/10**.
- Ora la riga parla di entrambi i motori. `PUNTI CHE VEDO: 3`. Il vuoto di TF-IDF resta giusto: nessuna parola in comune.
- La metà MiniLM dice «addestrato su milioni di frasi, quindi trova il significato». Il motivo di questo podio pieno, con copertura 0.0, è un altro: le parole vengono spezzate in pezzi noti. Mini 2.2 ancora vuoto.

### 2026-10-12 — Mini 6.3, seconda rilettura (non è il voto esame) — **9.5/10**

- Il voto che conta resta **7.5/10**.
- Ora la metà MiniLM è quella giusta: lo spezzamento in token evita il vocabolario vuoto. Il vuoto di TF-IDF resta giusto.
- Manca solo il collegamento esplicito: quei pezzi noti producono un vettore, quindi i punteggi non sono tutti zero e il podio si riempie. Refusi: «perchè», «nessuna parole», «tdidf».

### 2026-10-12 — Mini 6.3b (`02b_embeddings_pratica.py`) — **6.5/10**

- Il voto esame è la prima stesura, prima dei suggerimenti in chat. I tre blocchi c'erano.
- Non girava: colonne `testi`/`tipi`, chiave `tdidf`, `E` al posto di `k`, `somme[motore] =` che tiene solo l'ultima query, divisione per `len(vicini)`, niente `return`.

### 2026-10-12 — Mini 6.3b, post-feedback (non è il voto esame) — **9.5/10**

- Il voto che conta resta **6.5/10**.
- Esecuzione: `tfidf 0.625`, `mappa 0.833`, `minilm 0.75`. Sono i 0.62 / 0.83 / 0.75 della sezione, tenuti a 3 decimali. `PUNTI CHE VEDO: 3`.
- `carica_note()` è chiamata due volte. Il risultato non cambia.

### 2026-10-12 — Mini 6.4 (`02b_embeddings_pratica.py`) — **6.5/10**

- I tre numeri ci sono, dalla pagella sopra. `PUNTI CHE VEDO: 3`.
- Come motivo più forte indica il benchmark scritto dall'autore. La sezione li mette in ordine di peso e il primo è il vantaggio di casa: la mappa è costruita sulle stesse 30 note su cui viene misurata.
- La verifica proposta (query con parole fuori vocabolario) misura l'altro caso, quello in cui MiniLM non è cieco. Il controllo del vantaggio di casa è costruire la mappa su una parte delle note e misurarla sulle note lasciate fuori.

### 2026-10-12 — Mini 7.1 (`02b_embeddings_pratica.py`) — **7.5/10**

- Query sullo sconto 90%: il fenomeno è quello della sezione (le cifre si assomigliano, coseno 0.83 tra 10% e 90%). `PUNTI CHE VEDO: 2`.
- Il motore che indica è TF-IDF. La consegna chiede il match esatto. Con `tokenizza` del cap.01 la regex tiene solo le lettere: «90» non diventa un token, e TF-IDF non isola quello sconto.
- La riga è un paragrafo. Il senso c'è.

### 2026-10-12 — Mini 7.2 (`02b_embeddings_pratica.py`) — **8/10**

- Misura: `0.829` e `0.783`. Sono gli 0.83 e 0.78 della sezione. Codice ok. `PUNTI CHE VEDO: 4`.
- Previsione: (b) alto, giusto. (a) ha scritto «altro», la consegna chiede alto/basso. Il valore misurato è alto (0.83).
- La coppia più pericolosa è la negazione, giusto. Ha scritto «firmato» al posto di «valido». Manca che entrambi i coseni sono alti: il danno è che per il lavoro sono opposti e il numero sembra un buon match.

### 2026-10-12 — Mini 8.1 (`02b_embeddings_pratica.py`) — **10/10**

- Stessa frase, `normalizza=False` poi `True`, `[0]`, `np.linalg.norm`. `PUNTI CHE VEDO: 2`.
- Stampato `3.099` e `1.0`. Il `~3.7` della sezione è un'altra frase: la lunghezza non normalizzata dipende dal testo. Con `normalizza=True` la norma è 1.

### 2026-10-12 — Mini 8.2 (`02b_embeddings_pratica.py`) — **10/10**

- Differenza stampata `0.0` tra `coseno` e `a @ b`, con `normalizza=True`. Assert a `1e-7` passato. `PUNTI CHE VEDO: 3`.
- La riga è giusta: le norme valgono 1, il denominatore del coseno è 1, resta il prodotto scalare.
- In più confronta il prodotto dei vettori normalizzati con il coseno di quelli non normalizzati: è la stessa identità. Nel run si vede un solo `0.0`.

### 2026-10-12 — Mini 9.1 (`02b_embeddings_pratica.py`) — **10/10**

- Batch `0.932 s`, ciclo `1.576 s`, rapporto `1.7`. `perf_counter` attorno alle due encode, 30 note in una chiamata e 30 chiamate da una. `PUNTI CHE VEDO: 3`.
- La frase sul rapporto è giusta: il batch è 1.7 volte più veloce. Il `2,5-3` della sezione è un'altra esecuzione: il testo dice che il numero oscilla.

### 2026-10-12 — Mini 9.2 (`02b_embeddings_pratica.py`) — **8/10**

- (a) il ciclo sulle 30 note è giusto: nessuna è troncata (la più lunga ha 38 pezzi). (b) «retribuzione lorda mensile » ripetuta 100 volte fa 300 parole e 700 pezzi. L'avviso del run dice `700 > 128`. `PUNTI CHE VEDO: 3`.
- A schermo, dopo l'avviso, compare `1`, non `0` e `True`.
- (c) dice che l'encode taglia oltre i 128 token. Manca l'effetto: la coda della nota non entra nel vettore, per la ricerca non esiste. Refusi: «lo nota», «passandolo».

### 2026-10-13 — Mini 10.1 (`02b_embeddings_pratica.py`) — **8.5/10**

- (a) varianza stampata `0.274` (sezione ~0.27). (b) il tipo più sparso è `cu`, giusto. `PUNTI CHE VEDO: 3`.
- I quattro scarti stanno nel dizionario e non escono in stampa: la consegna chiedeva la dispersione di ogni tipo.
- (c) indice `13`: estratto conto in mezzo alle buste, in basso a sinistra. Vale.

### 2026-10-13 — Quiz di verifica V1–V9 (`02b_embeddings_pratica.py`) — **8.5/10**

- V1 `384`, V3 shape 384 contro 4 (e aggiunge che a shape uguale gli spazi restano diversi), V5 peggiora in silenzio, V7 `np.ndarray`. V2 il falso è giusto.
- V4 «prodotto scolare»: il concetto è il prodotto scalare. V6 tre bullet: il guadagno semantico e il TF-IDF sui codici ci sono; il «non guadagni» è solo la negazione, mancano le cifre.
- V8: i pezzi si guardano e il contesto sposta il punto. Manca che la media c'è ancora, ma arriva dopo. V9: shape `(3, 384)` e `(1, 384)` giuste; il motivo «iterabile» no. `embedda` mette la stringa in una lista così l'uscita è sempre una matrice.

### 2026-10-13 — Quiz di verifica V10–V13 (`02b_embeddings_pratica.py`) — **8.5/10**

- V10 a freddo: la dimensione è la forma, il modello decide lo spazio, 384 uguali non coincidono. Chiude **#64**. Manca: i vettori già salvati sono del modello vecchio e vanno ricalcolati.
- V11: la clausola a pagina 3 non si trova, il taglio a 128 pezzi butta il resto. V12: leakage, il voto si gonfia perché le risposte sono già viste.
- V13: pooling, normalizzare, benchmark giusti. (a) `token` al posto di sottoparola. (e) `pagella` al posto di precision@k. Lacuna **#67**.

### 2026-10-14 — E2 debug (`02b_embeddings_pratica.py`) — **10/10**

- Bug A: shape diversa (384 contro 4), il coseno non parte. Aggiunge che a shape uguale gli spazi resterebbero diversi.
- Bug B: tetto 128 pezzi, di cui 126 di testo più 2 speciali. La clausola in fondo non entra nel vettore. È l'effetto che in Mini 9.2 mancava.
- `PUNTI CHE VEDO` lasciato vuoto. I due bug ci sono entrambi. Refusi: «generalo», «cosiderazione».

### 2026-10-14 — E1 refactoring (`02b_embeddings_pratica.py`) — **9/10**

- Un solo `embedda` sulla lista dei testi. Shape in uscita `(n, 384)`, senza `stack` e senza `[0]`. `PUNTI CHE VEDO: 2`.
- `modello_una_volta(MODELLO_ST)` va bene qui: il nome coincide col default.
- La riga sulla velocità dice «operazioni vettorizzate» e «3-5 volte». La sezione 9 dice un costo fisso per chiamata, pagato una volta nel batch. Il rapporto misurato nel Mini 9.1 era 1.7; la sezione indica 2,5-3.

### 2026-10-14 — E3 retrieval (`02b_embeddings_pratica.py`) — **10/10**

- A freddo: `carica_mappa`, `vettore_frase`, `coseno` della frase con se stessa.
- Il run stampa `1.0000000000000002`. La frase scelta ha almeno una parola nella mappa, quindi il vettore non è tutto zeri.

### 2026-10-14 — E4 interleaving (`02b_embeddings_pratica.py`) — **6.5/10**

- Le chiamate `vicini_tfidf(query, 1)` e `vicini_minilm(...)` sono giuste. Indici stampati: 17 e 6. `PUNTI CHE VEDO: 3`.
- Il tipo è letto con `corpus['id'] == indice`. L'id parte da 1. La riga 6 è una CU; come id 6 esce una busta paga. Il commento dice che MiniLM ha capito perché ha trovato una busta.
- TF-IDF: indice 17, coseno 0.269, tipo «altro» anche sulla riga giusta (è un altro documento «altro»). Lacuna **#68**.

### 2026-10-14 — E5 colloquio (`02b_embeddings_pratica.py`) — **8/10**

- I tre obbligatori ci sono: vettore, vicinanza = senso simile, non è un conteggio di parole. `PUNTI CHE VEDO: 3`, l'opzionale è scritto lo stesso.
- Opzionale a metà. L'idea delle sottoparole (parole mai viste spezzate) è giusta; ha scritto «token». La mappa del 02a ha 4 dimensioni, non 2: il 2 è il disegno. «Almeno 384» non è un effetto dei milioni di documenti: 384 è la larghezza del modello.

### 2026-10-14 — E5 colloquio, post-feedback (`02b_embeddings_pratica.py`) — **9/10**

- Non sostituisce l'esame **8/10**. Ora la mappa è a 4 dimensioni e MiniLM a 384, senza «almeno».
- Resta «funziona a token»: il termine del capitolo è sottoparola. Il resto dell'opzionale regge, rumore compreso se si sale oltre le 4 dimensioni su 30 frasi.

### 2026-10-15 — E6 `cerca_note` (`02b_embeddings_pratica.py`) — esame **6.5/10**, post-feedback **9.5/10**

- Esame (primo tentativo): `embedda` sulla colonna `tipo`, riuso di `vicini_minilm` sulla query già embeddata, `vicini[:, 0]` su una lista. Non partiva.
- Post-feedback: `E` dai testi fuori, dentro solo encode della query, normalizzazione riga per riga con guardia su norm 0, `E_1 @ q`, top-k indici. `PUNTI CHE VEDO: 3`.
- Test «rimborso spese» → indici `[24, 25, 20]` (ricevuta, cedolino, preventivo di spesa): c'entrano sul corpus sintetico. Normalizza `E` a ogni chiamata: ok su 30 note.

### 2026-10-15 — E7 `pipeline_ricerca` (`02b_embeddings_pratica.py`) — **9/10**

- Esame: P1+P2 completi — `carica_note`, `modello_una_volta`, `embedda(testi, …, normalizza=True)`, `q = embedda(query, …)[0]`, `E @ q`, `_top_k`, lista di dict con `punteggio` e `anteprima[:60]`. `PUNTI CHE VEDO: 7/7`.
- Allineato a E6: embedding sui **testi**, non sui tipi. Type hint `list[dict[str, object]]` coerente.
- Stampa solo `[0]['tipo']`: la consegna chiede l’intero risultato leggibile (indice, punteggio, anteprima).
- Le quattro liste + `zip` funzionano; si può compattare in un solo comprehension su `k_migliori` (stesso contratto, meno rumore).

### 2026-10-15 — E8 `cartellino` (`02b_embeddings_pratica.py`) — **5.5/10**

- Esame: dict con le 7 chiavi, 4 query con `pprint`, `Counter` usato per l’allineamento, commento finale su copertura 0 / punteggio basso (spirito torre ok). `PUNTI CHE VEDO: 7`.
- **Vicini 02b:** `modello` e `E` non usati; top-k rifatto con TF-IDF + `coseno` sul corpus. La consegna chiede MiniLM (`vicini_minilm` o `E @ q` + `_top_k`).
- **`tipo_vicini`:** in uscita è una **lista** di tipi; deve essere la stringa più frequente (`most_common(1)[0][0]`, come in soluzione).
- **`prob_classificatore`:** `predict_proba[0][0]` = prima classe in ordine sklearn, non probabilità del tipo predetto → usare `classifica_tipo_documento` o `classi.index(tipo)`.
- **`copertura_mappa`:** reinventata; esiste `copertura_query(query, mappa)` (02a). Attenzione divisione se `token_query` vuota.
- **Prove:** `BENCHMARK[0]` è una tupla `(query, atteso)` — va passato `BENCHMARK[0][0]` (o solo la stringa benchmark).
- Manca blocco «TUA RISPOSTA»: una riga per query con `allineato` False (prob vs `punteggio_max`).

### 2026-10-15 — E8 `cartellino`, post-feedback (`02b_embeddings_pratica.py`) — **7.5/10**

- Non sostituisce l'esame **5.5/10**. Ora usa `E` + `embedda` per i vicini, `copertura_query`, prob colonna giusta, `tipo_vicini` = stringa da `Counter`.
- Resta: `BENCHMARK[0]` è tupla → passare `BENCHMARK[0][0]`; codice morto (`vec`, `token_query`, `cosine_similarity`, `carica_note` dentro la funzione); preferibile `vicini_minilm(..., E=E)` o `q` normalizzato + `_top_k(E @ q)`.
- `embedda(query, modello)` senza `normalizza=True`: con `coseno` a mano i punteggi restano ok, ma non allineato al motore 02b del file.
- Discorso finale generico ok; manca «TUA RISPOSTA» riga-per-query se `allineato` False.

### 2026-10-16 — E8 `cartellino`, terzo giro (`02b_embeddings_pratica.py`) — **8/10**

- Funzione: contratto 7 chiavi ok; `_top_k(E @ q, k)` + `E` passato; `copertura_query`; prob sulla classe predetta; `tipo_vicini` stringa da `Counter`. Codice pulito.
- **`normalizza=True` sulla query** manca: l’ordine dei vicini spesso coincide, ma `punteggio_max` non è coseno in [0,1] → confronto debole con `prob_classificatore`.
- Prove: ancora `BENCHMARK[0]` (tupla). «TUA RISPOSTA» vuota; commento generico sotto resta.
- Edge: se `_top_k` restituisce lista vuota, `vicini[0][1]` esplode (guardia opzionale).

### 2026-10-16 — E9 contrastivo 2D (`02b_embeddings_pratica.py`) — **8.5/10**

- Esame: `passo_contrastivo` con `d = b - a`, tre rami e margine; seme 0, ciclo 100× (positive poi negative), aggiornamento `pos[i]/pos[j]`; distanze positive/negative stampate prima e dopo. `PUNTI CHE VEDO: 4`.
- Codice allineato a Sez. 4 e soluzione attesa (positive → ~0, negative si fermano oltre margine).
- Risposta margine: idea «se spingi sempre le negative scappano lontano» c’è; manca il meccanismo operativo «quando dist ≥ margine smetti di spingere» (stop, non accelerazione). Testo confuso (cluster / frasi vicine).

### 2026-10-16 — E10 glossario in codice (`02b_embeddings_pratica.py`) — **8/10**

- Esame: 6 funzioni nominate, assert consegna passano; `pooling_medio(axis=0)`, `normalizza_righe`, `coseno_batch` (q, E) con `@`, `n_sottoparole` via `tokenizer.tokenize`, `ha_troncamento` (+2 speciali). `PUNTI CHE VEDO: 6`.
- **`precisione_a_k`:** divide per `len(tipi)` invece che per `len(indici)` — l’assert passa solo perché la lista indici copre tutto il mock; la metrica corretta è «quanti degli indici dati hanno tipo atteso / k» (rinforzo **#67**).

### 2026-10-16 — E10 glossario, post-fix `precisione_a_k` (`02b_embeddings_pratica.py`) — **9.5/10**

- Non sostituisce l’esame **8/10**. Denominatore `len(indici)` corretto; tutte e 6 le funzioni + assert ok. Opzionale: `return E @ q`, guardia `indici` vuota.

### 2026-10-16 — E11 `verifica_compatibilita` (`02b_embeddings_pratica.py`) — **7.5/10**

- Esame: due check (a)(b), `-> None`, tre contratti mock, loop try/except; messaggio dim con valori E vs contratto. `PUNTI CHE VEDO: 3`.
- **SyntaxError** riga 2º `ValueError`: f-string con `contratto["modello_minilm"]` e virgolette doppie annidate — usare `contratto['modello_minilm']` o variabile.
- Test: ok stampare errori sui fasulli; meglio anche assert che il contratto giusto **non** alza. Messaggi: aggiungere esplicito «atteso / trovato» per (b).

### 2026-10-16 — E11 post-fix (`02b_embeddings_pratica.py`) — **9/10**

- Non sostituisce l’esame **7.5/10**. f-string corretta; messaggio (b) con inserito vs atteso; (a)(b)(c) e tre contratti ok. Opzionale: assert silenzioso su `contratto_giusto`, messaggio dim con etichette «trovato/atteso» simmetriche al (b).

### 2026-10-19 — Progetto incrementale T1–T5 (`embed_utils.py`) — **8.5/10**

- T1: `embedda_note` + `salva_vettori`/`carica_vettori` su `note_minilm.pkl`, assert shape `(30,384)` e `allclose` al reload. Ok.
- T2: `aggiorna_contratto_minilm` scrive le 4 chiavi MiniLM e fa `dump`; docstring 384 vs 4 + nome modello. Ok. Manca assert esplicito `mappa_dim == 4` (DoD «vecchie e nuove»).
- T3: `cerca_note` + assert (a) nota 5 in cima, (b) dim + norme ~1, (c) chiavi nuove. Ok. Parametro `testi` non usato; rinormalizza `E` a ogni chiamata.
- T4: guardia in `embedda_note`, stampa «Nessuna nota troncata». Funzione batch/`None` invece del contratto capitolo `{n_pezzi, limite, troncato}` per testo.
- T5: tempo su `embedda` puro + KB di `E` — due print. Ok.
- Libreria separata da `02b`, `testo_utils` non toccato. Patch `__main__.tokenizza` per pickle contratto legacy.

### 2026-10-19 — 🏁 CHIUSURA CAPITOLO 02b — voto difficoltà **8/10**

- **Voto difficoltà: 8/10** (dato studente). Motivo lettura: integrazione di molti pezzi (11 sezioni, ~2.400 righe), non i singoli concetti — come M3-10.
- **Decisione studente:** i 4 punti lasciati in bianco (Micro #6 guadagno/non guadagno, Mini 2.2 sottoparole/OOV, Mini 11.1 contratto, E8 segnali discordanti) **non vengono corretti**: diventano blocchi `# 🔁 RINFORZO MIRATO` nel cap.03 (Sez. 5.1+Mini 5.1, Sez. 5.2, Mini 2.4, Mini 3.3).
- **Pagella riassuntiva:** quiz ingresso media 8.75; verifica 8.5/8.5. Top: E2 debug 10, E3 retrieval `coseno` 10, E7 pipeline a memoria 9, E10 glossario 9.5 (post-fix), E5 colloquio 8→9. Deboli: E8 5.5→8, E4 6.5 (#68), E6 6.5→9.5. Progetto T1–T5 **8.5/10**.
- **Lacune:** **#69 NUOVA** (cifre/codici → match esatto; `tokenizza` scarta i numeri); #66/#67/#68 → 🟡 con rinforzo inserito nel cap.03 (da verificare a freddo al quiz d'ingresso del **cap.04**); #64 🟢 (frase operativa → Mini 2.4 cap.03).
- **Pattern #6:** 4 episodi nel capitolo; antidoto «PUNTI CHE VEDO» funziona quando dichiarato. Resta 🔴 attivo, monitorato nel cap.03.
- **Pattern #25 → 🟢:** type hint `NDArray[np.float64]` scritti autonomamente (E9/E10).
- Trend voti M4: 4 → 6 → 8 ↑. Media corso: ~7.05 (34 capitoli).

---

## Lacune e dubbi ancora aperti

- Pattern **#6**: Q6 ha 3/3 righe (7.5/10), (b) senza negazione. Mini 0.1: `PUNTI CHE VEDO` usato. **Mini 2.1 esame 7.5/10** (stampa di tre), post-feedback **9.5/10**. **Mini 5.1 7/10:** ha usato il metodo dell'avviso al posto di `max_seq_length`. **Mini 6.2 9/10:** tre punti consegnati; nella riga manca il contrasto con TF-IDF. **Mini 6.3 esame 7.5/10, post-feedback 8.5 poi 9.5/10:** lo spezzamento in pezzi noti c'è. Resta da dire che quei pezzi danno un vettore e il podio si riempie. **Mini 6.3b esame 6.5/10, post-feedback 9.5/10:** la pagella ora stampa 0.625 / 0.833 / 0.75. **Mini 6.4 6.5/10:** come motivo più forte indica il benchmark dell'autore; il primo in ordine di peso è il vantaggio di casa, e la verifica che ha scritto misura le parole nuove. Mini 2.2 ancora vuoto, da dire a freddo. Resta la negazione, in V6 / Micro #6.
- Contratto: `mappa_dim` 4 vs `mappa_dim_minilm` 384.
- **#64** 🟢 V10 (13/10) a freddo: forma contro spazio, anche a 384 uguali. Manca solo la frase «ricalcola i vettori già salvati».
- **#67** 🔴 V13 (13/10): (a) `token` invece di sottoparola; (e) `pagella` invece di precision@k.
- **#65** 🟡 Mini 1.2 esame 7/10, post-feedback 8.5/10: frase `is`/`==` giusta. Aperto: passare `nome` a `carica_modello_frasi`.
- **Mini 7.1 7.5/10:** per le cifre ha indicato TF-IDF. Il match esatto è lo strumento; `tokenizza` scarta i numeri.
- **Quiz V6 (13/10):** tre bullet; il «non guadagni» è solo la negazione. Le cifre (10% vs 90%) non ci sono.
- **#66** 🔴 Quiz V9 (13/10): shape giuste. Il motivo è «encode la tratterebbe come un iterabile». `embedda` mette la stringa in lista così la shape è sempre `(n, 384)`.
- **#68** 🔴 E4 (14/10) **6.5/10:** indice di `vicini_*` usato come colonna `id`. Riga 6 = CU, id 6 = busta paga.

---

## Note per il capitolo successivo (mentor)

- Bridge **R02** si popola alla chiusura di **02b** (non c'è bridge 02a→02b).
- **12/10, su richiesta:** `pagella` tolta dal corpo del 02b. Mini **6.3b** la fa scrivere prima del Mini 6.4, che la lancia. Il riferimento sta solo nelle soluzioni in fondo. Non rimetterla nel corpo.
- **19/10 — FATTO in chiusura:** bridge `M04_R02` popolato (10 mini-esercizi) e `03_similarita_coseno.py` scritto (Regola 45: `top_k`, `decidi_con_soglia`, `precision_su_k` dello studente; riferimenti solo nelle soluzioni). Rinforzi inseriti per #66 (Mini 1.2), #67 (Mini 4.2 + Sez. 5.2), #68 (Mini 2.3 + V9), #69 (Sez. 5.2 + Mini 5.2/5.3 + V7 + 🏗️ T1/T4) e per i 4 punti vuoti (Micro #6 → Mini 5.1; Mini 2.2 → Sez. 5.2; Mini 11.1 → Mini 2.4; E8 → Mini 3.3). Numeri degli esempi verificati in esecuzione (scheda `docs/libri_corso/schede/M04_C03_similarita_coseno.md`). **Verifica a freddo di #66–#69: quiz d'ingresso del cap.04.** Progetto del cap.03: `match_utils.py` NUOVO (non tocca `embed_utils.py`).
