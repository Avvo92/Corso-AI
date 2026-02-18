# Contesto del Corso AI — File per il Mentor

> Questo file viene consultato e aggiornato dal Mentor AI ad ogni sessione.
> Serve a mantenere continuità tra le conversazioni e calibrare il corso.
>
> **Ultimo aggiornamento**: 17/02/2026

---

## ⚡ Stato Attuale — Leggere Per Primo

| Campo | Valore |
|-------|--------|
| **Capitolo in corso** | 04_liste.py (prossimo da iniziare) |
| **Ultimo completato** | 03_funzioni.py (17/02/2026) |
| **Modulo attuale** | 1 — Python & Dati |
| **Difficoltà media** | 4.0 (trend: +2 per capitolo, monitorare) |
| **Priorità attive** | Lambda da rinforzare (⚠️), lettura completa delle consegne (🔴) |
| **Sessione corrente** | Sessione 2 |

> **Per l'agente**: dopo aver letto questa tabella, leggi le "Regole Didattiche" e i "Pattern di Errore" prima di produrre qualsiasi contenuto. Aggiorna questa tabella ad ogni fine capitolo.

---

## Profilo dello Studente

- **Nome**: Gianluca
- **Background**: Web Developer con esperienza in HTML, CSS, JavaScript, PHP, Laravel
- **Sistema operativo**: Windows 10 (usa Git Bash come terminale in Cursor)
- **Python installato**: 3.14.3
- **IDE**: Cursor
- **Version control**: Git + GitHub (il corso è già in una repository)
- **Obiettivo finale**: Entrare nel mondo del lavoro tech con competenze solide in Python, AI/ML e web development. Il progetto finale deve essere il **diamante del portfolio**: una full web app (React + Laravel + FastAPI) con IA integrata — bella, reattiva, funzionale — da mostrare ai recruiter come prova concreta di competenza.

---

## Regole Didattiche Concordate

1. **Nessun termine tecnico senza spiegazione pratica** — ogni termine nuovo va spiegato con esempio prima di procedere
2. **Nessun concetto dato per scontato** — anche quelli "già noti" (API REST, database, MVC) vanno rinfrescati
3. **Sempre la sequenza: Ripasso → Traduzione → Pratica** per ogni concetto
4. **Confronto a tre lingue**: ogni spiegazione deve includere PHP + JavaScript + Python
5. **Spiegare i metodi usati negli esempi**: se un esempio usa `.reduce()`, `array_map()`, ecc., spiegare cosa fanno
6. **Essere esaustivi, mai sintetici**: meglio una spiegazione in più che una in meno
7. **File 07-08 (NumPy/Tensori) e Modulo 4 (Deep Learning)**: livello di dettaglio extra con più esempi visivi, analogie e mini-esercizi intermedi
8. **Suggerimenti autocomplete disattivati** durante lo studio per favorire la memorizzazione
9. **Voto difficoltà obbligatorio**: dopo ogni capitolo Gianluca deve dare un voto da 1 a 10. Se dimentica, **ricordarglielo esplicitamente**
10. **Ripasso intelligente dei termini appresi**: nei capitoli successivi, quando si usa un termine già visto (es. `enumerate`, `lambda`, `*args`), non limitarsi a usarlo — reinserire una breve spiegazione contestuale come se fosse un "richiamo naturale". Non deve sembrare una ripetizione forzata, ma un promemoria organico integrato nel flusso della lezione. Esempio: invece di scrivere solo `sorted(lista, key=lambda x: x["prezzo"])`, aggiungere un commento tipo: *"Usiamo `sorted()` — ricordi? Crea una NUOVA lista ordinata senza modificare l'originale — con una `lambda` come chiave: una mini-funzione usa-e-getta che dice 'ordina in base a questo campo'"*
11. **Tag `[COLLOQUIO]` sugli esercizi**: gli esercizi che replicano domande reali da colloqui tecnici devono essere segnati con il tag `# 🎯 [COLLOQUIO]` nel commento. Questo aiuta Gianluca a sapere quali esercizi meritano attenzione extra e pratica ripetuta, perché potrebbe trovarseli davanti in un'intervista reale.

---

## Progresso del Corso

### Modulo 1 — Python & Dati

| File | Stato | Data | Difficoltà (1-10) | Note |
|------|-------|------|--------------------|------|
| 01_benvenuto_python.py | ✅ Completato + Corretto | 17/02/2026 | 2 | Buon primo approccio. Errori tipici da JS: ternario con `?:`, nomi variabili in inglese misto. Ha capito f-string, tipi, casting. |
| 02_condizioni_e_cicli.py | ✅ Completato + Corretto | 17/02/2026 | 4 | FizzBuzz: `range(1,20)` invece di `range(1,21)`. Password: `elif` dove servivano due `if`, `== True` ridondante. Scacchiera perfetta. Temperature incompleto (mancava la media). |
| 03_funzioni.py | ✅ Completato + Corretto | 17/02/2026 | 6 | Ha capito *args, return multipli, sorted. **Lambda ancora poco chiare** — da rinforzare nei prossimi capitoli. Errori: lista vs parametri separati a *args, count come stringa, mancava `reverse=True`, mancava parametro `decimali`. Tutti corretti. |
| 04_liste.py | ⬜ Da fare | | | |
| 05_dizionari.py | ⬜ Da fare | | | |
| 06_file_csv.py | ⬜ Da fare | | | |
| 07_numpy_intro.py | ⬜ Da fare | | | Da arricchire prima che ci arrivi |
| 08_tensori_spiegati.py | ⬜ Da fare | | | Da arricchire prima che ci arrivi |
| 09_pandas_intro.py | ⬜ Da fare | | | |
| 10_pandas_progetto.py | ⬜ Da fare | | | |
| 11_matplotlib_grafici.py | ⬜ Da fare | | | |
| 12_web_bridge.py | ⬜ Da fare | | | |

### Moduli Successivi

| Modulo | Stato |
|--------|-------|
| 2 — Machine Learning (Scikit-Learn) | ⬜ Da creare |
| 3 — Computer Vision (OpenCV, YOLO) | ⬜ Da creare |
| 4 — Deep Learning (PyTorch) | ⬜ Da creare (dettaglio extra richiesto) |
| 5 — NLP & LLM (HuggingFace, OpenAI) | ⬜ Da creare |
| 6 — Progetto Finale (React + Laravel + FastAPI) | ⬜ Da creare |

---

## Valutazioni Difficoltà — Riepilogo

> Scala: 1 (facilissimo) → 10 (molto difficile)
> Servono per calibrare il ritmo: se la media sale troppo, rallento e aggiungo esercizi di rinforzo.

| Capitolo | Voto | Trend |
|----------|------|-------|
| 01_benvenuto_python | 2 | — |
| 02_condizioni_e_cicli | 4 | +2 ↑ |
| 03_funzioni | 6 | +2 ↑ |

**Media attuale**: 4.0 — Curva in salita costante (+2 per capitolo). Ritmo ok ma da monitorare: se continua a salire di 2 punti per capitolo, al file 06 sarebbe a 10.

---

## Glossario dei Termini Appresi

> Termini che Gianluca ha incontrato e che il Mentor deve rinforzare nei capitoli successivi.
>
> **Regola di ripasso**: quando un termine di questa lista compare in un nuovo capitolo, il Mentor
> NON lo dà per scontato. Inserisce un breve richiamo naturale nel commento del codice o nella
> spiegazione, riformulando il concetto con parole diverse o con un nuovo esempio.
> Dopo 3 ripassi riusciti (= Gianluca lo usa correttamente senza aiuto), il termine passa a stato ✅ Acquisito.
>
> Stato: 🔄 Da rinforzare | ✅ Acquisito (usato correttamente 3+ volte senza aiuto)

### Python Base (File 01-03)

| Termine | Significato sintetico | Equivalente JS/PHP | Cap. | Ripassi | Stato |
|---------|-----------------------|--------------------|------|---------|-------|
| `f-string` | Stringa con variabili inline `f"ciao {nome}"` | `` `ciao ${nome}` `` / `"ciao $nome"` | 01 | 0/3 | 🔄 |
| `type()` | Restituisce il tipo di una variabile | `typeof` / `gettype()` | 01 | 0/3 | 🔄 |
| `int()`, `float()`, `str()` | Casting esplicito tra tipi | `parseInt()`, `parseFloat()` / `(int)`, `(float)` | 01 | 0/3 | 🔄 |
| `range()` | Genera sequenza di numeri — **il secondo numero è ESCLUSO!** | Non diretto / `range()` PHP | 02 | 0/3 | 🔄 |
| `enumerate()` | Itera dando indice + valore insieme | `.forEach((val, i))` / Non diretto | 02 | 0/3 | 🔄 |
| `for...in` | Itera sugli elementi di una lista | `for...of` / `foreach` | 02 | 0/3 | 🔄 |
| `while` | Ciclo finché la condizione è vera | Identico | 02 | 0/3 | 🔄 |
| `if/elif/else` | Condizionali — nota: `elif` non `else if` | `if/else if/else` | 02 | 0/3 | 🔄 |
| `def` | Definisce una funzione | `function` | 03 | 0/3 | 🔄 |
| `return` multiplo | Restituisce più valori come tupla — si "spacchettano" con `a, b = funzione()` | Non diretto (array/oggetto) | 03 | 0/3 | 🔄 |
| `*args` | Parametri variabili posizionali — come spread `...args` | `...args` / `...$args` | 03 | 0/3 | 🔄 |
| `**kwargs` | Parametri con nome variabili — come passare un oggetto di opzioni | Destructuring / Array associativo | 03 | 0/3 | 🔄 |
| `lambda` | Mini-funzione usa-e-getta, una riga sola — ⚠️ **DA RINFORZARE** | `() =>` / `fn() =>` | 03 | 0/3 | ⚠️ |
| `sorted()` | Ordina creando una NUOVA lista (l'originale resta intatta!) | `.sort()` (attenzione: in JS modifica in-place!) / `usort()` | 03 | 0/3 | 🔄 |
| `isinstance()` | Verifica se un valore è di un certo tipo | `instanceof` / `instanceof` | 03 | 0/3 | 🔄 |
| `docstring` | Commento `"""..."""` dentro una funzione per documentarla | JSDoc `/** */` / PHPDoc `/** */` | 03 | 0/3 | 🔄 |
| `.isdigit()` | True se il carattere è un numero | Regex o `!isNaN()` / `ctype_digit()` | 02 | 0/3 | 🔄 |
| `.isupper()` | True se il carattere è maiuscolo | Regex / `ctype_upper()` | 02 | 0/3 | 🔄 |
| `min()`, `max()`, `sum()` | Funzioni aggregate su liste | `Math.min()`, `.reduce()` / `min()`, `array_sum()` | 03 | 0/3 | 🔄 |
| `len()` | Lunghezza di lista/stringa — è una funzione, non un `.length`! | `.length` / `count()`, `strlen()` | 02 | 0/3 | 🔄 |

### Concetti Generali

| Termine | Significato | Capitolo |
|---------|-------------|----------|
| Tensor | Array multidimensionale — il "mattoncino" dei dati nell'AI | Spiegato in teoria, pratica al file 08 |
| Dataset | Insieme di dati organizzati (come una tabella SQL) | Spiegato in teoria |
| Feature | Una colonna/proprietà dei dati (come un campo di un form) | Spiegato in teoria |
| Target | Il valore che vogliamo prevedere | Spiegato in teoria |
| Overfitting | Quando il modello "memorizza" i dati invece di imparare il pattern | Spiegato in teoria |

---

## Domande Fatte Durante i Capitoli

> Le domande che Gianluca fa spontaneamente durante gli esercizi.
> Rivelano quali concetti hanno bisogno di rinforzo.

### Capitolo 01 — benvenuto_python
- "A cosa serve `\n`?" → Concetto di caratteri di escape, non ovvio per chi viene da HTML
- "Come fare il simbolo dell'euro in Cursor?" → Questione pratica di tastiera/encoding

### Capitolo 02 — condizioni_e_cicli
- "Spiegami meglio `enumerate()`" → L'idea che una funzione restituisca indice+valore insieme non era intuitiva
- "Se al metodo passo due parametri, lui capisce da solo quale è l'indice e quale il valore?" → Confusione su unpacking/destructuring automatico
- "Esiste un metodo per avere la lunghezza di una lista?" → Non conosceva `len()` — veniva da `.length` e `count()`
- "Serve effettivamente un ciclo per questo esercizio?" → Buon istinto: stava cercando approcci più semplici
- "Come gestire lo scope delle variabili?" → Lo scope in Python (senza `{}`) è meno visibile che in JS/PHP

### Capitolo 03 — funzioni
- "Che differenza c'è tra passare `[1,2,3]` e `1,2,3` a *args?" → Confusione lista vs parametri separati
- Chiarimenti su f-string con doppi apici annidati
- "Questa formula è corretta? K = C + 273.15" → Verifica proattiva delle formule, buon segno

---

## Pattern di Errore Ricorrenti

Questi sono gli errori che Gianluca tende a ripetere. Da monitorare nei prossimi esercizi:

| # | Pattern | Stato | Note |
|---|---------|-------|------|
| 1 | **Sintassi JS in Python**: usa `? :` invece di `if...else` ternario | 🔴 Attivo | Visto al file 01 |
| 2 | **`range()` fine escluso**: dimentica che il secondo numero è escluso | 🔴 Attivo | Visto al file 02 |
| 3 | **`== True` ridondante**: scrive `if valore == True` | 🟡 Corretto una volta | Visto al file 02, corretto dopo feedback |
| 4 | **Calcoli dentro le f-string**: espressioni troppo lunghe nelle `{}` | 🟡 Corretto una volta | Visto al file 01, corretto dopo feedback |
| 5 | **Tipi nei dizionari**: mette stringhe dove servono numeri | 🟡 Corretto una volta | Visto al file 03 (`count` come stringa) |
| 6 | **Lettura incompleta delle consegne**: non implementa tutti i requisiti | 🔴 Attivo | Visto ai file 02 e 03 |

| 7 | **Lambda poco chiare**: non ha ancora interiorizzato la sintassi e l'uso delle funzioni lambda | 🔴 Attivo | Autodichiarato dopo file 03. Inserire lambda in esercizi futuri (liste, dizionari, sorted, filter, map) per rinforzo graduale |

Legenda: 🔴 Attivo (si ripete) | 🟡 Visto e corretto (da monitorare) | 🟢 Superato

---

## Punti di Forza

1. **Capisce velocemente le analogie** PHP/JS → Python
2. **Corregge subito** dopo il feedback — non ripete lo stesso errore due volte
3. **Chiede chiarimenti** quando non capisce (enumerate, *args, reduce)
4. **Sa già ragionare in termini di funzioni, parametri, return** — il background Laravel si sente
5. **Motivato e orientato al risultato** — vuole capire il perché, non solo il come
6. **Verifica proattivamente** — controlla formule e logica prima di fidarsi

---

## Ritmo di Studio

- **Sessione 1 (17/02/2026)**: File 01, 02, 03 completati in una sessione
- **Ritmo stimato**: 1-2 file al giorno
- **Tempo totale stimato per il corso**: 3-4 mesi
- **Momento migliore per studiare**: ❓ Da chiedere

---

## Ponti Mentali — Analogie che Hanno Funzionato

> Quando un concetto "fa click" grazie a un'analogia, lo registro qui.
> Il Mentor riusa questi ponti per spiegare concetti più avanzati, costruendo su ciò che è già solido.

| Ponte | Concetto Python | Collegamento JS/PHP | Capitolo | Riusabile per |
|-------|-----------------|---------------------|----------|---------------|
| "Spread operator" | `*args` raccoglie parametri variabili | `...args` in JS / `...$args` in PHP | 03 | NumPy broadcasting, unpacking di liste, destructuring |
| "Template literal" | `f"ciao {nome}"` interpola variabili | `` `ciao ${nome}` `` in JS | 01 | Qualsiasi output formattato, logging, debug |
| "foreach" | `for elemento in lista` itera sugli elementi | `for...of` in JS / `foreach` in PHP | 02 | Iterazione su array NumPy, righe DataFrame, batch di dati |
| "Database in RAM" | Pandas DataFrame = tabella SQL in memoria | Query Eloquent / tabella MySQL | Teoria | Pandas, feature engineering, EDA |
| "Pixel = numero" | Un'immagine è una griglia di numeri | — | Teoria | OpenCV, tensori immagine, input delle reti neurali |

### Come usare questa sezione
Quando il Mentor deve spiegare un concetto nuovo, cerca prima un ponte esistente:
- "Ricordi come `*args` funziona come lo spread? Ecco, il broadcasting di NumPy è la stessa idea applicata ai calcoli..."
- "Ricordi che un DataFrame è come una tabella SQL in RAM? Bene, `.apply()` è come fare un `UPDATE ... SET colonna = funzione(colonna)`"

---

## Cosa So Fare Adesso — Competenze Acquisite

> Dopo ogni capitolo, una descrizione concreta di cosa Gianluca sa fare.
> Diventa la base per il CV tecnico e per misurare il progresso reale.

### Dopo il Capitolo 01 — Python Base
- So dichiarare variabili in Python senza `let`/`var`/`$`
- So usare f-string per stampare output formattati
- So convertire tra tipi con `int()`, `float()`, `str()`
- So verificare il tipo di una variabile con `type()`
- Conosco la differenza tra `=` (assegnazione) e `==` (confronto)

### Dopo il Capitolo 02 — Controllo di Flusso
- So scrivere condizionali `if/elif/else` senza parentesi graffe
- So usare `for...in` per iterare su liste (equivalente di `foreach`)
- So usare `range()` per generare sequenze numeriche (ricordando: fine escluso!)
- So usare `while` con condizione di uscita
- So usare `enumerate()` per avere indice + valore contemporaneamente
- So verificare proprietà dei caratteri con `.isdigit()`, `.isupper()`

### Dopo il Capitolo 03 — Funzioni
- So definire funzioni con `def`, parametri obbligatori e opzionali (default)
- So restituire più valori con `return` multiplo (tuple unpacking)
- So usare `*args` per parametri variabili (come lo spread operator)
- So usare `**kwargs` per parametri con nome variabili
- So ordinare liste con `sorted()` e una funzione `key`
- So scrivere docstring per documentare le funzioni
- ⚠️ Lambda: conosco la sintassi ma non mi viene ancora naturale usarle

---

## Checklist di Auto-Revisione (prima di consegnare il codice)

> Gianluca: scorri questa lista PRIMA di dire "ho finito".
> Costruita sui tuoi errori reali — si aggiorna man mano.

### Controlli Obbligatori

- [ ] **Ho letto TUTTA la consegna?** Conto i requisiti: se dice "calcola A, B e C", li ho fatti tutti e tre?
- [ ] **I tipi sono giusti?** Se il risultato deve essere un numero, non l'ho messo come stringa `"42"` invece di `42`?
- [ ] **Ho usato `== True` o `== False`?** Se sì, posso toglierlo: `if valore` basta
- [ ] **Ho calcoli lunghi dentro le f-string?** Se sì, calcolo prima in una variabile e poi stampo
- [ ] **Ho usato `range()`?** Il secondo numero è escluso: `range(1, 20)` arriva a 19!
- [ ] **Ho usato la sintassi JS per sbaglio?** Niente `? :` per il ternario, niente `===`, niente `{}`

### Controlli Bonus (buone pratiche)
- [ ] La funzione ha una docstring?
- [ ] I nomi delle variabili sono in italiano coerente O in inglese coerente (non misti)?
- [ ] Ho testato con almeno 2-3 input diversi?

---

## Ripasso Programmato (Spaced Repetition)

> I concetti si dimenticano se non si rivedono. Questa tabella traccia quando un concetto
> è stato appreso e quando va rivisto. Il Mentor inserisce micro-esercizi di ripasso nei capitoli giusti.

| Concetto | Appreso il | Rivisto (3gg) | Rivisto (7gg) | Rivisto (14gg) | Stato |
|----------|-----------|---------------|---------------|----------------|-------|
| f-string, tipi, casting | 17/02 | file 04 | file 06 | file 09 | Da verificare |
| if/elif/else, for, while | 17/02 | file 04 | file 06 | file 09 | Da verificare |
| range() fine escluso | 17/02 | file 04 ⚠️ | file 06 | file 09 | Da rinforzare |
| enumerate() unpacking | 17/02 | file 04 | file 06 | file 09 | Da verificare |
| def, return, *args, **kwargs | 17/02 | file 05 | file 07 | file 10 | Da verificare |
| lambda | 17/02 | file 04 ⚠️ | file 05 ⚠️ | file 07 | ⚠️ Non chiaro — rinforzo prioritario |
| sorted() con key | 17/02 | file 04 | file 05 | file 07 | Da verificare |

⚠️ = Il concetto richiede rinforzo attivo (non solo uso passivo, ma esercizio dedicato)

---

## Esercizi da Colloquio 🎯

> Registro degli esercizi che replicano domande reali da colloqui tecnici.
> Gianluca dovrebbe saperli risolvere a memoria, senza aiuto, sotto pressione.
> Consiglio: riprovare quelli segnati ⚠️ una volta a settimana finché diventano automatici.

### Già incontrati

| Esercizio | Capitolo | Tipo di colloquio | Cosa testa | Stato |
|-----------|----------|-------------------|------------|-------|
| FizzBuzz | 02 | Junior/Mid — classico filtro iniziale | Modulo `%`, condizionali, ordine delle condizioni (15 prima di 3 e 5) | ✅ Risolto (con errore su range, poi corretto) |
| Validatore password | 02 | Junior — string processing | Iterazione carattere per carattere, controlli multipli indipendenti | ✅ Risolto (con errori su elif e == True, poi corretti) |
| Funzione con *args e return multiplo | 03 | Junior/Mid — comprensione funzioni | Parametri variabili, tuple unpacking, aggregazioni (min/max/media) | ✅ Risolto |
| Ordinamento con sorted + lambda | 03 | Mid — manipolazione dati | Lambda come key function, ordinamento personalizzato | ✅ Risolto (mancava reverse=True, poi corretto) |
| Costruire una risposta API JSON-like | 03 | Junior/Mid — backend developer | Dizionari, isinstance, struttura dati consistente | ✅ Risolto (count come stringa, poi corretto) |

### Cosa aspettarsi nei prossimi capitoli

| Capitolo | Esercizi colloquio previsti |
|----------|-----------------------------|
| 04 — Liste | Rimuovere duplicati, invertire una lista senza `.reverse()`, trovare l'elemento più frequente, two-sum problem |
| 05 — Dizionari | Contare frequenze di parole, raggruppare dati per chiave, merge di due dizionari, anagrammi |
| 06 — File CSV | Parsing manuale di CSV, trovare anomalie nei dati, aggregazioni per gruppo |
| 07 — NumPy | Normalizzazione di un array, distanza euclidea, operazioni su matrici |
| 09 — Pandas | Pulizia dati con valori mancanti, group by + aggregazione, pivot table |
| Mod. 2 — ML | Train/test split manuale, calcolo accuratezza, feature scaling |
| Mod. 4 — DL | Spiegare backpropagation a parole, costruire un modello semplice, leggere una loss curve |

### Come ripassarli

1. Una volta a settimana, scegli 2-3 esercizi dalla lista "Già incontrati"
2. Riscrivili da zero su un file vuoto, senza guardare la soluzione
3. Cronometrati: un junior ha circa 15-20 minuti per esercizio in un colloquio
4. Se non riesci entro il tempo, ristudia il capitolo e riprova dopo 2 giorni

---

## Note per il Mentor

### Promemoria automatici
- **Dopo ogni capitolo completato**: chiedere il voto di difficoltà (1-10) se non lo dà spontaneamente
- **Dopo ogni capitolo**: aggiornare glossario, domande, pattern di errore, progresso
- **Prima del file 07**: arricchire con più esempi visivi e mini-esercizi intermedi
- **Prima del file 08**: aggiungere rappresentazioni ASCII di tensori 2D/3D/4D

### Calibrazione del corso
- Se la media difficoltà supera 7: rallentare, aggiungere esercizi di rinforzo
- Se la media difficoltà è sotto 4: accelerare o aggiungere sfide bonus
- Se un pattern di errore persiste per 3+ capitoli: creare un mini-esercizio mirato
- **Trend attuale**: curva +2 per capitolo (2→4→6). Monitorare: se al file 04 il voto è ≥7, aggiungere esercizi di rinforzo prima di proseguire

### Rinforzo lambda
- **File 04 (liste)**: inserire almeno 2 esercizi che usano lambda con `sorted()`, `filter()`, `map()`
- **File 05 (dizionari)**: inserire almeno 1 esercizio che ordina dizionari con lambda come key
- **File 07+ (NumPy/Pandas)**: usare lambda con `.apply()` su DataFrame
- Obiettivo: entro il file 06, lambda deve passare da 🔴 a 🟢

### Orientamento portfolio/lavoro
- Gli esercizi devono progressivamente assomigliare a task reali da colloquio
- Il codice deve essere pulito, ben strutturato, commentato con docstring
- Il progetto finale deve avere: README professionale, deploy, demo live, codice su GitHub
- Nei moduli avanzati: introdurre best practice di produzione (logging, error handling, testing)

### Ripresa contesto
- Se apre una nuova chat: fargli dire "sono al file X" e leggere questo file
- Sul secondo PC: aiutarlo a clonare la repo e ricreare il venv

---

## Protocollo di Aggiornamento — Checklist per l'Agente

> Dopo OGNI capitolo completato e corretto, l'agente DEVE eseguire tutti questi aggiornamenti
> in un'unica operazione. Non saltare nessun punto.

### Passo 1 — Stato Attuale (sezione in cima)
- [ ] Aggiornare "Capitolo in corso" al prossimo file
- [ ] Aggiornare "Ultimo completato" con nome file e data
- [ ] Ricalcolare "Difficoltà media" con il nuovo voto
- [ ] Aggiornare "Priorità attive" se cambiate
- [ ] Aggiornare "Ultimo aggiornamento" con la data odierna

### Passo 2 — Progresso
- [ ] Nella tabella Progresso: cambiare stato a ✅, inserire data e voto difficoltà
- [ ] Nella tabella Valutazioni: aggiungere riga con voto e trend
- [ ] Scrivere le Note sintetiche (errori fatti, cosa ha capito, cosa resta debole)

### Passo 3 — Glossario
- [ ] Aggiungere i NUOVI termini introdotti nel capitolo (con stato 🔄 e contatore 0/3)
- [ ] Per i termini GIÀ nel glossario che sono stati usati/ripassati: incrementare contatore (es. 0/3 → 1/3)
- [ ] Se un termine raggiunge 3/3: cambiare stato a ✅ Acquisito

### Passo 4 — Domande
- [ ] Aggiungere sezione "Capitolo XX — nome" con le domande fatte durante la sessione
- [ ] Per ogni domanda: annotare cosa rivela (concetto debole, curiosità, buon istinto)

### Passo 5 — Pattern di Errore
- [ ] Nuovi errori: aggiungere riga con stato 🔴
- [ ] Errori visti ma corretti: aggiornare stato a 🟡
- [ ] Errori non più ripetuti per 3+ capitoli: aggiornare stato a 🟢

### Passo 6 — Competenze e Ponti
- [ ] Aggiungere sezione "Dopo il Capitolo XX" in "Cosa So Fare Adesso"
- [ ] Se un'analogia ha funzionato particolarmente bene: aggiungerla ai "Ponti Mentali"

### Passo 7 — Colloquio e Ripasso
- [ ] Se il capitolo conteneva esercizi con tag 🎯 [COLLOQUIO]: aggiungerli alla tabella "Già incontrati"
- [ ] Aggiornare la tabella "Ripasso Programmato" se un concetto è stato rivisto

### Passo 8 — Checklist Auto-Revisione
- [ ] Se è emerso un NUOVO tipo di errore: aggiungere un punto alla checklist di Gianluca

### Passo 9 — Voto Difficoltà
- [ ] Se Gianluca NON ha dato il voto spontaneamente: **chiederglielo esplicitamente** prima di chiudere
