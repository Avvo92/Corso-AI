# Diario sessione — Capitolo 02a — Embeddings, l'idea

| Campo | Valore |
|-------|--------|
| **Modulo** | M04 — NLP, Embeddings & Transformers |
| **File capitolo** | `02a_embeddings_concetto.py` |
| **File diario** | `M04_C02a_embeddings_concetto_sessione.md` |
| **Stato** | chiuso 08/10/2026 |
| **Voto difficoltà** | **6**/10 |

---

## Obiettivi del capitolo (per il mentor)

- Embedding = punto sulla mappa, senza installazioni (solo numpy/pandas + `testo_utils`).
- **Mappa calcolata dai 30 documenti reali**, non coordinate inventate: co-occorrenze → PPMI → SVD.
- La promessa sui sinonimi va **misurata**, non raccontata: TF-IDF 0.000 vs mappa 0.960 su
  "prospetto paga di aprile" / "cedolino di marzo" (le due parole non co-occorrono mai).
- Risposta ai tre limiti del cap.01, con onestà: la media dei punti non legge l'ordine (#62).
- Rinforzi #60 (non rifare gli assi), #61 (vicinanza ≠ alterato / ≠ tipo).
- `coseno` è un **🧠 [RETRIEVAL]** in Sez. 3: il capitolo non misura finché non la scrive
  (chiude il termine "coseno" a 3/3 nel glossario).
- Task prodotto: `costruisci_mappa` + `vettore_frase` in `testo_utils.py`, contratto esteso,
  3 assert di regressione (Regola 37).

### Nota riscrittura — 05/10/2026

Prima versione del file (358 righe) usava coordinate inventate a mano: nessun meccanismo,
nessun coseno, nessun task prodotto, nessuna DoD. Riscritto integralmente (~1000 righe) su
richiesta dello studente, che ha scelto lo scope completo. Numeri del capitolo verificati
eseguendo il file prima della consegna.

---

## Domande durante lo studio

- _(2026-10-05)_ **Q:** Passo 3, PPMI: perché pesare l'incontro rispetto al caso?
  **Nota:** Un compagno che sta ovunque («totale») non è una notizia. Uno raro che torna («IRPEF» con «cedolino») sì. I valori sotto zero, «si evitano», su 30 frasi sono rumore e si azzerano. Poi: «è un IDF composto?» — stessa famiglia dell'IDF (chi sta ovunque pesa poco), in più c'è il conteggio dell'incontro di quella coppia.
- _(2026-10-05)_ **Q:** `Counter(parola for documento in corpus for parola in documento)` cosa fa?
  **Nota:** Appiattisce i documenti e conta i token. Due «cedolino» nella stessa busta contano 2. È il filtro del passo 1, non la tabella delle coppie.
- _(2026-10-05)_ **Q:** Perché il vocabolario tiene solo le parole viste almeno due volte?
  **Nota:** Un incontro solo è un aneddoto. La mappa impara la compagnia che si ripete. «Aprile» e «marzo» nei 30 documenti cadono per questo. Il filtro conta le occorrenze, non i documenti: due volte nella stessa busta passano, e la compagnia resta quella di un documento solo.

---

## Valutazioni esercizi / quiz / mini-esercizi

> Append-only. Il voto esame è il primo tentativo.

### [2026-10-05] — Quiz d'ingresso Q1–Q7

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 85–107
- **Valutazione (primo tentativo — voto esame):** **8.5/10**
- **Punti di forza:** Q1 coseno 1 con la stessa Bag of Words. Q2 e Q5: `fit` sul train, in produzione `transform`. Q3: vocabolario e IDF diversi se rifai il vettorizzatore, ponte giusto con media e deviazione standard del contratto di inferenza. Q4 parola mai vista scartata. Q6 il testuale dice il tipo.
- **Errori / lacune:** Q7: il valore 0.0 è giusto. Il perché mescola tre cose diverse: coseno 0 fra due frecce vere (direzioni indipendenti), la guardia sul vettore nullo (il conto è 0 diviso 0), e «non ho capito la domanda» (è il rischio in produzione, non il motivo della guardia). Lacuna **#63**.
- **Chiusure:** **#60** e **#61** verificate qui. **#62** resta aperta: Q1 non nomina l'ordine.

### [2026-10-05] — Micro #62

- **Esercizio / blocco:** `02a_embeddings_concetto.py` riga 149
- **Valutazione (primo tentativo — voto esame):** **9.5/10**
- **Punti di forza:** In una riga: per dare un risultato diverso alle due frasi invertite il modello deve distinguere l'ordine. È il pezzo che mancava nel TODO 7 del cap.01.
- **Errori / lacune:** Nessuna. La Sez. 5 misurerà che la media dei punti non lo fa ancora.
- **Chiusure:** lacuna **#62** → 🟢.

### [2026-10-05] — Mini 1.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 174–178
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** 20.000 − 30 = 19.970 zeri nella scheda. Nell'embedding da 384 numeri ha scritto 0: le caselle sono piene.
- **Errori / lacune:** Nessuna. La consegna chiedeva due numeri.

### [2026-10-06] — Mini 2.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 334–339
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** Con `min_conteggio=2` il vocabolario è 49. Alzandolo a 3 scende a 34. Direzione giusta e numeri verificati sul CSV.
- **Errori / lacune:** Il perché resta sulla soglia («il minimo è più alto»). Manca chi esce: le parole viste esattamente 2 volte, 15 su 49. Nessuna lacuna nuova.

### [2026-10-06] — Mini 2.2

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 340–345
- **Valutazione (primo tentativo — voto esame):** **7.5/10**
- **Punti di forza:** La diagonale sarebbe la parola con se stessa. La mappa vuole coppie di parole diverse. Direzione giusta.
- **Errori / lacune:** Il numero non è «è ovvio, quindi uguale per tutte». Il `set` conta una volta per documento: cedolino 4, totale 7, prospetto 2. Quei conteggi entrerebbero nelle somme di riga del passo 3. Precisione, non lacuna nuova.

### [2026-10-06] — Mini 2.2, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 344–345
- **Valutazione (post-feedback, non è il voto esame):** **8/10**. Il voto esame resta **7.5/10**.
- **Punti di forza:** Tolto «è ovvio per tutte». Aggiunto il documento. Resta giusto il motivo: servono le coppie con parole diverse.
- **Errori / lacune:** «In ogni documento» suona come un conteggio dentro la busta. La cella è un solo numero: in quanti documenti la parola sta (cedolino 4, totale 7). Manca ancora che quei numeri entrerebbero nelle somme di riga del passo 3.
- **Fix applicato (06/10, senza nuovo voto):** «nei vari documenti». Chiude il buco del conteggio dentro la busta. La cella è in quanti documenti la parola sta. Resta fuori l'effetto sulle somme di riga del passo 3.

### [2026-10-06] — Micro #60

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 370–375
- **Valutazione (primo tentativo — voto esame):** **7/10**
- **Punti di forza:** La mappa si rifà su tutto l'archivio più le 400 note, non sulle 400 sole. La versione 1.0 / 1.1 dice che le due mappe non si mischiano.
- **Errori / lacune:** «Li lascio salvati ma non li uso» ferma i vecchi vettori. Gli assi nuovi sono un'altra città: ogni vettore già in database va ricalcolato sulla mappa 1.1. Nel M6 si chiama reindicizzare. #60 non si riapre: il fit sull'archivio intero è giusto.

### [2026-10-06] — Micro #60, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 374–375
- **Valutazione (post-feedback):** **10/10**. Il voto esame resta **7/10**.
- **Punti di forza:** Archivio intero più 400 note. I vettori vecchi si ricalcolano tutti sulla mappa nuova. Due righe, tutte e due.
- **Errori / lacune:** Nessuna.

### [2026-10-06] — Retrieval `coseno` Sez. 3

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 417–427
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** Formula `(a @ b) / (norma × norma)`. Stesso vettore → 1, ortogonali → 0, stesso verso più lungo → 1. Norma zero → 0.0. Controllo 1D extra.
- **Errori / lacune:** Il messaggio di shape stampa i vettori (`{a}`), non `a.shape`. Si legge lo stesso, ma non è la shape. **#63**: il codice fa la guardia giusta; il perché (0/0 vs coseno 0 vs frase sconosciuta) non è stato riformulato, resta aperta.

### [2026-10-06] — Mini 3.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 440–444
- **Valutazione (primo tentativo — voto esame):** **6.5/10**
- **Punti di forza:** I vicini di cedolino (pagare, retribuzione, lorda, mese) coincidono con la stampa. La compagnia di una busta paga torna.
- **Errori / lacune:** Chiesto una riga per **cedolino** e una per **saldo**. Manca saldo (finale, iniziale, accredito, conto). Pattern **#6**.

### [2026-10-06] — Mini 4.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 487–492
- **Valutazione (primo tentativo — voto esame):** **8.5/10**
- **Punti di forza:** No. Stesso 0, due conti diversi: TF-IDF non ha parole in comune, la mappa ha visto il significato e li ha trovati lontani.
- **Errori / lacune:** Manca il confronto con la coppia A. Il TF-IDF dà 0 anche ai sinonimi (0.000 vs mappa 0.960). Quello 0 è ignoranza, non una misura di lontananza. Nessuna lacuna nuova.

### [2026-10-06] — Mini 5.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 535–541
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** No, la media non cambia. Nome giusto: commutativa. #62 misurata: l'ordine della lista non sposta il centro.
- **Errori / lacune:** Commutativa è la somma degli addendi, non «la media» in sé. Precisione, non lacuna.

### [2026-10-06] — Mini 5.2

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 542–547
- **Valutazione (primo tentativo — voto esame):** **8/10**
- **Punti di forza:** Ignoranza e direzione diversa danno lo stesso risultato. È il pericolo in produzione. Chiude **#63**.
- **Errori / lacune:** Il vettore è `[0, 0, 0, 0]` (`DIM=4`), non `[0, 0]`. Il coseno vale **0.0** (guardia), non è stato scritto come numero.

### [2026-10-06] — Mini 6.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 588–592
- **Valutazione (primo tentativo — voto esame):** **8.5/10**
- **Punti di forza:** Le dimensioni non hanno nome. Sono direzioni che spiegano i dati, non etichette semantiche. Giusto.
- **Errori / lacune:** Chiesto due righe. Manca la seconda: il tono formale lo misuri a parte, non lo leggi dall'asse 3.

### [2026-10-06] — Mini 7.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 625–636
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** (a) mappa, (b) esatta, (c) mappa, (d) esatta. Mutuo e busta paga si cercano per significato. Pratica e IBAN sono identificatori: match esatto.
- **Errori / lacune:** Nessuna.

### [2026-10-06] — Mini 8.1

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 654–657
- **Valutazione (primo tentativo — voto esame):** **7.5/10**
- **Punti di forza:** «Visura» dal lavoro, due archivi diversi (CRIF e catasto). La mappa statica fonderebbe i due usi in un punto solo.
- **Errori / lacune:** Chiesto **due frasi**, scritte due etichette. I due mestieri restano vicini (estratto ufficiale in due banche dati), meno netto di «saldo» nome vs verbo.

### [2026-10-06] — Micro #61

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 680–686
- **Valutazione (primo tentativo — voto esame):** **9.5/10**
- **Punti di forza:** (c). Vicino ≠ tipo, vicino ≠ alterato. Stesso significato generale può stare in un documento diverso. #61 confermata.
- **Errori / lacune:** «Simili a una fattura»: X è simile a un **cedolino**. La fattura è l'esempio di documento diverso, non il bersaglio.

### [2026-10-06] — Quiz di verifica V1–V8

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 712–739
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** V1 denso vs sparso. V2 compagnia. V3 coseno 1 e ordine perso. V4 fit su una nota = altra mappa. V5 esatta. V6 direzione vs lunghezza. V7 dimensioni senza nome. V8 coordinate per note simili, senza jargon di libreria.
- **Errori / lacune:** V4 «dimensioni diverse»: gli assi sono un'altra città, il numero di caselle può restare 4. V3 non nomina il Bag of Words del cap.01. V8 manca il guadagno concreto (trovo «prospetto» cercando «cedolino»). Nessuna lacuna nuova.

### [2026-10-06] — Bridge R01 Q1

- **Esercizio / blocco:** `M04_R01_after_C01_before_C02_testo_to_embeddings.md` domanda 1
- **Valutazione (primo tentativo — voto esame):** **6/10**
- **Punti di forza:** `count("netto")` = 2. Il set toglie il duplicato.
- **Errori / lacune:** `print` stampa due numeri: `len(set(...))` è **2**, non la lista. Output vero: `2 2`.

### [2026-10-06] — Bridge R01 Q1, post-feedback

- **Esercizio / blocco:** `M04_R01` domanda 1
- **Valutazione (post-feedback):** **9/10**. Il voto esame resta **6/10**.
- **Punti di forza:** I due numeri 2 e 2. Set = parole distinte, count = occorrenze.
- **Errori / lacune:** `print(a, b)` scrive `2 2` con uno spazio, non `2, 2`.

### [2026-10-06] — Bridge R01 Q2

- **Esercizio / blocco:** `M04_R01` domanda 2
- **Valutazione (primo tentativo — voto esame):** **5/10**
- **Punti di forza:** `sort` sul posto, secondo elemento `[1]`.
- **Errori / lacune:** La sintassi è `key=lambda x: x[1]`, non `lambda key x`. Manca `reverse=True` (dal più grande). `sort` restituisce `None`, quindi non si assegna.

### [2026-10-06] — Bridge R01 Q2, post-feedback

- **Esercizio / blocco:** `M04_R01` domanda 2
- **Valutazione (post-feedback):** **10/10**. Il voto esame resta **5/10**.
- **Punti di forza:** `key=lambda x: x[1]`, `reverse=True`, sul posto. Riga completa.
- **Errori / lacune:** Nessuna.

### [2026-10-06] — Bridge R01 Q3

- **Esercizio / blocco:** `M04_R01` domanda 3
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** `C` prima lettera. Lunghezza 30. Le due stringhe vicine si uniscono in una sola.
- **Errori / lacune:** Nessuna.

### [2026-10-06] — Bridge R01 Q4

- **Esercizio / blocco:** `M04_R01` domanda 4
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** Vero. Il vettorizzatore impara il vocabolario dentro `pipe.fit`, sui testi che gli passi, non a parte.
- **Errori / lacune:** Nessuna.

### [2026-10-06] — Bridge R01 Q5

- **Esercizio / blocco:** `M04_R01` domanda 5
- **Valutazione (primo tentativo — voto esame):** **7.5/10**
- **Punti di forza:** Precision: tra i segnalati come positivi, quanti lo erano. FN: detti negativi, erano positivi.
- **Errori / lacune:** Il recall non parte dai veri positivi (quelli già presi). Parte da tutti quelli che **erano** della classe: quanti hai preso. I veri positivi sono il numeratore, non il denominatore.

### [2026-10-06] — Bridge R01 Q6

- **Esercizio / blocco:** `M04_R01` domanda 6
- **Valutazione (primo tentativo — voto esame):** **8.5/10**
- **Punti di forza:** Il bug è `fit_transform` sul testo nuovo: vocabolario rifatto sulla query. Serve il `vec` salvato e `transform`. #60 tenuta.
- **Errori / lacune:** Il `dump` a coppie `(1, modello)` è un giro inutile. Basta salvare modello e vettorizzatore e caricarli. `TfidfVectorizer()` nuovo alla riga 2 è già il `fit` sbagliato.

### [2026-10-06] — Bridge R01 Q7

- **Esercizio / blocco:** `M04_R01` domanda 7
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** Falso. Se sta in tutti i documenti pesa meno: non distingue nulla. È l'IDF.
- **Errori / lacune:** Nessuna.

### [2026-10-07] — Bridge R01 Q8

- **Esercizio / blocco:** `M04_R01` domanda 8
- **Valutazione (primo tentativo — voto esame):** **10/10**
- **Punti di forza:** Norma `[3, 4]` = 5. Coseno con se stesso = 1. Vettore di zeri = 0 (guardia del capitolo).
- **Errori / lacune:** Nessuna.

### [2026-10-07] — Bridge R01 Q9

- **Esercizio / blocco:** `M04_R01` domanda 9
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** Si ferma dopo `rssmra85t`. Manca il giorno `\d{2}` e la lettera del comune. La regex giusta ce l'ha.
- **Errori / lacune:** Non dice perché: `\d{3}` vuole tre cifre e trova `10h`. Precisione, non lacuna.

### [2026-10-07] — Bridge R01 Q10

- **Esercizio / blocco:** `M04_R01` domanda 10
- **Valutazione (primo tentativo — voto esame):** **8.5/10**
- **Punti di forza:** Stesse parole, stessi conteggi. #62 tenuta.
- **Errori / lacune:** «Stesso tipo di parole» è vago: sono le **stesse** parole. Manca la frase: l'ordine non entra nella scheda.

### [2026-10-07] — E1 `lontani`

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 749–773
- **Valutazione (primo tentativo — voto esame):** **6.5/10**
- **Punti di forza:** `sort` senza `reverse`: i coseni più bassi in cima. `k` taglia i primi. La funzione, lanciata, farebbe il mestiere.
- **Errori / lacune:** Copia di `vicini` (la consegna chiedeva di evitarlo: un parametro `inverti`). Stampa `"movimenti"`, non i 3 lontani da `"cedolino"`. Default `k=5` invece di 3. `np.array` non è il tipo (`np.ndarray`). `map` copre la funzione builtin.

### [2026-10-07] — E1 `lontani`, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 754–773
- **Valutazione (post-feedback):** **8/10**. Il voto esame resta **6.5/10**.
- **Punti di forza:** Stampa i 3 lontani da `"cedolino"`. `sort` crescente, `k=3` in chiamata.
- **Errori / lacune:** Resta la copia di `vicini`. Un parametro `inverti` sulla stessa funzione evita due corpi identici. Default ancora 5. `np.ndarray`, non `np.array`. Non chiamare la variabile `map`.

### [2026-10-07] — E2 due mappe min 2 e 3

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 774–801
- **Valutazione (primo tentativo — voto esame):** **9.5/10**
- **Punti di forza:** 49 vs 34 parole. Coseno su entrambe. «prospetto» ha conteggio 2, a soglia 3 esce: vettore di zeri, coseno 0.0. L'`if` sulla chiave verifica il fatto. Ignoranza ≠ significato diverso. Il commento-soluzione in fondo al capitolo (coseno resta alto) su questo CSV è sbagliato.
- **Errori / lacune:** `in mappa_min_3` basta, `.keys()` è ridondante. Due `if __name__`. Niente lacuna nuova.

### [2026-10-07] — E3 `cerca`

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 803–836
- **Valutazione (primo tentativo — voto esame):** **8/10**
- **Punti di forza:** Mappa una volta, `vettore_frase` su ogni nota, coseno, `sort` decrescente, `[:k]`. Sulla domanda escono tre `estratto_conto` (id 15, 13, 12), il 13 ha «accredito stipendio». Motore giusto.
- **Errori / lacune:** La consegna chiede tuple `(id, tipo, coseno)`. Restituisci `(id, [tipo, cos, testo])`. Il dizionario in mezzo non serve: una lista di tuple si ordina direttamente. Type hint `list[int, list[...]]` non descrive una lista di triple.

### [2026-10-07] — E3, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 810–828
- **Valutazione (post-feedback):** **9/10**. Il voto esame resta **8/10**.
- **Punti di forza:** Tuple affiancate `(id, tipo, coseno, testo)`, `key` su `x[2]`. Niente dizionario, niente lista innestata. Testo solo per il quadro visivo.
- **Errori / lacune:** Il type hint parla ancora di `tuple[int, list[...]]`. Ora è `list[tuple[int, str, float, str]]`.

### [2026-10-07] — E3, type hint

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 811–832
- **Valutazione (post-feedback):** **9.5/10**. Il voto esame resta **8/10**.
- **Punti di forza:** Hint allineato: `list[tuple[int, str, float, str]]`. Motore, ordine, print.
- **Errori / lacune:** `mappa: dict[str, np.array]` resta `np.ndarray`. Quarto campo extra rispetto alla consegna, scelto apposta.

### [2026-10-07] — E4 tre limiti

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 847–854
- **Valutazione (primo tentativo — voto esame):** **9/10**
- **Punti di forza:** Tre limiti diversi: ignoranza silenziosa, ordine perso, parole tutte pari nella media. Non tre parafrasi. Pattern **#6** rispettato qui.
- **Errori / lacune:** Il punto 3 non nomina la media: ogni parola pesa `1/n`, la nota lunga diluisce quella importante.

### [2026-10-07] — E4, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 847–854
- **Valutazione (post-feedback):** **10/10**. Il voto esame resta **9/10**.
- **Punti di forza:** Il punto 3 noma la media e la diluizione. Tre limiti distinti, completi.
- **Errori / lacune:** Nessuna.

### [2026-10-07] — E5 colloquio full-text vs embedding

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 856–862
- **Valutazione (primo tentativo — voto esame):** **7/10**
- **Punti di forza:** Guadagno chiaro: parafrasi («burattino e falegname» senza il nome). Full-text vince sul nome esatto dell'autore.
- **Errori / lacune:** Manca **cosa NON guadagni**: cifre, IBAN, negazioni, spiegabilità (quale parola ha deciso). Tre job, due coperti. Pattern **#6**.

### [2026-10-07] — E6 aritmetica vettori [ALAMMAR]

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 864–890
- **Valutazione (primo tentativo — voto esame):** **6/10**
- **Punti di forza:** Conto giusto, riuso di `vicini` con una chiave finta. I 3 vicini (stipendio, bonifico, movimenti) non sono un'analogia. «Non ha senso» è onesto.
- **Errori / lacune:** Ha incolpato il **metodo**. Su miliardi di parole (re − uomo + donna) funziona. Qui fallisce per le **30 frasi**, non perché l'aritmetica sia falsa.

### [2026-10-07] — E6, post-feedback

- **Esercizio / blocco:** `02a_embeddings_concetto.py` righe 864–890
- **Valutazione (post-feedback):** **9.5/10**. Il voto esame resta **6/10**.
- **Punti di forza:** Non ha senso sui 30 documenti. Colpa del corpus piccolo, non dell'aritmetica. Stabilità = abbastanza incontri perché la sottrazione significhi una cosa sola.
- **Errori / lacune:** La prima proposizione («il metodo non funziona») è ancora netta; il dopo la corregge.

### [2026-10-08] — 🏗️ Progetto T1–T4 (`testo_utils.py`)

- **Esercizio / blocco:** `modulo_04_nlp/testo_utils.py` (T1–T4). **T5 tolto** dalla consegna (richiesta studente, 08/10: parte finale noiosa).
- **Valutazione (primo tentativo — voto esame):** **7/10**
- **Punti di forza:** T1: `costruisci_mappa` / `vettore_frase` portate, import silenzioso sulla mappa. T2: `salva_mappa` / `carica_mappa` su `mappa.pkl` fisso. T3: contratto senza `pipe`, chiavi `mappa_dim` / `min_conteggio` / `n_parole`, `VERSIONE` 1.2, commento su dim 4 vs 8. T4 finale: tre assert su `vettore_frase` + `carica_mappa`, `python testo_utils.py` esce 0 e muto. Intuito giusto su libreria vs programma di rilascio (contatore, `allclose`) — parcheggiato fuori dal modulo.
- **Errori / lacune (primo tentativo):** T3: mappa dentro il contratto, chiavi non allineate (`mappa_n_dim`), `dump` di formati diversi, `prepara_modello` a ogni salvataggio, versione = contatore lanci. T4 primo giro: ciclo sulla mappa, `shape != (DIM,)` invertito. Assert finali copiati dopo esempio del mentor. `query =` a livello modulo è un residuo C01 (non stampa). Type hint `np.array` in 02a resta Pattern #25.
- **Next step:** 02b. Installare `sentence-transformers` **prima** della sessione. Mini breve in 02b su direzione senza nome (ex T5).

---

## Lacune e dubbi ancora aperti

- #60 e #61 verificate all'ingresso (05/10, esame 8.5). #62 chiusa nel micro (05/10, 9.5).
- **#63** chiusa in Mini 5.2 (06/10, 8/10): ignoranza e direzione diversa, stesso 0.0.

---

## Note per il capitolo successivo (mentor)

- 02b: installare `sentence-transformers` prima della sessione, non durante.
- Pattern **#6** ancora 🔴 (E5: tre job, due coperti; Mini 3.1 una riga sola).
- T5 spiegabilità: non rifare un saggio. Mini corto: cosa puoi/non puoi dire all'operatore; le 384 dimensioni di MiniLM non hanno nome.
- Contratto: `mappa_dim` del giocattolo (4) ≠ dim del modello vero (384). Non mischiare i vettori.
- Libreria (`carica_mappa`) vs script di rilascio: non rimettere il versioning nel modulo.
