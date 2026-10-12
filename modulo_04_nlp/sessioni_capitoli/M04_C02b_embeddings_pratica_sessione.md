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

---

## Lacune e dubbi ancora aperti

- Pattern **#6**: Q6 ha 3/3 righe (7.5/10), (b) senza negazione. Mini 0.1: `PUNTI CHE VEDO` usato. **Mini 2.1 esame 7.5/10** (stampa di tre), post-feedback **9.5/10**. **Mini 5.1 7/10:** ha usato il metodo dell'avviso al posto di `max_seq_length`. **Mini 6.2 9/10:** tre punti consegnati; nella riga manca il contrasto con TF-IDF. **Mini 6.3 esame 7.5/10, post-feedback 8.5 poi 9.5/10:** lo spezzamento in pezzi noti c'è. Resta da dire che quei pezzi danno un vettore e il podio si riempie. **Mini 6.3b esame 6.5/10, post-feedback 9.5/10:** la pagella ora stampa 0.625 / 0.833 / 0.75. **Mini 6.4 6.5/10:** come motivo più forte indica il benchmark dell'autore; il primo in ordine di peso è il vantaggio di casa, e la verifica che ha scritto misura le parole nuove. Mini 2.2 ancora vuoto, da dire a freddo. Resta la negazione, in V6 / Micro #6.
- Contratto: `mappa_dim` 4 vs `mappa_dim_minilm` 384.
- **#64** 🟡 (Q2 esame 8/10, post-feedback 9.5/10; Q4 esame 7/10, post-feedback 8.5/10): da ridire a freddo in V10, con «assi / spazio», anche a `dim` invariata.
- **#65** 🟡 Mini 1.2 esame 7/10, post-feedback 8.5/10: frase `is`/`==` giusta. Aperto: passare `nome` a `carica_modello_frasi`.
- **Mini 7.1 7.5/10:** per le cifre ha indicato TF-IDF. Il match esatto è lo strumento; `tokenizza` scarta i numeri.

---

## Note per il capitolo successivo (mentor)

- Bridge **R02** si popola alla chiusura di **02b** (non c'è bridge 02a→02b).
- **12/10, su richiesta:** `pagella` tolta dal corpo del 02b. Mini **6.3b** la fa scrivere prima del Mini 6.4, che la lancia. Il riferimento sta solo nelle soluzioni in fondo. Non rimetterla nel corpo.
