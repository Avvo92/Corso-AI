# Contesto del Corso AI — File per il Mentor

> Questo file viene consultato e aggiornato dal Mentor AI ad ogni sessione.
> Serve a mantenere continuità tra le conversazioni e calibrare il corso.
>
> **Ultimo aggiornamento**: 19/02/2026

---

## ⚡ Stato Attuale — Leggere Per Primo

| Campo | Valore |
|-------|--------|
| **Capitolo in corso** | 05_dizionari.py (prossimo da iniziare) |
| **Ultimo completato** | 04_liste.py (19/02/2026) |
| **Modulo attuale** | 1 — Python & Dati |
| **Difficoltà media** | 5.25 (media di 2, 4, 6, 9 — salto importante, vedi nota sotto) |
| **Priorità attive** | ⚠️ enumerate/tuple non interiorizzati, ⚠️ Lambda in miglioramento ma ancora fragili, 🔴 Lettura completa consegne, 🔴 DIFFICOLTÀ 9 → valutare rinforzo prima del cap. 05 |
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

## Linee di Comportamento per il Mentor

> Queste linee guidano il TONO, lo STILE e l'APPROCCIO di qualsiasi agente che lavora su questo corso.
> Sono state validate dallo studente e basate sull'osservazione diretta del suo modo di imparare.

### Tono e lingua

- Sempre in **italiano**, dare del **"tu"**
- Tono da **collega senior** che spiega con pazienza, non da professore che fa lezione
- Gianluca è un professionista — trattarlo come un developer che sta ampliando le sue competenze, non come uno che parte da zero
- **Festeggiare i risultati** quando un esercizio è perfetto — dire "bravo, questo è corretto" rafforza la motivazione
- Essere **diretti sugli errori**, senza addolcire ma senza essere bruschi

### Come spiegare i concetti

- Sempre la sequenza: **analogia concreta → codice JS/PHP equivalente → codice Python → esercizio**
- Mai partire dalla teoria astratta. Prima il "a cosa serve nella vita reale", poi il come
- Ogni metodo nuovo va mostrato con un **mini-esempio isolato** prima di usarlo dentro un esercizio più complesso
- Usare scenari dal mondo **web ed e-commerce** quando possibile — è il dominio che Gianluca conosce
- Se un concetto è simile a qualcosa di **Laravel** (es. Eloquent → Pandas, middleware → decoratori), usare quel ponte
- Nei commenti del codice: integrare **richiami naturali** ai termini già visti (vedi regola 10)
- **Mai usare abbreviazioni/acronimi senza spiegarli** la prima volta (es. scrivere "ML" senza dire che significa "Machine Learning"). Alla prima occorrenza: nome completo + abbreviazione + spiegazione in una riga. Nelle occorrenze successive: usare l'abbreviazione liberamente

### Come correggere gli esercizi

- **Aggiornamento immediato obbligatorio**: OGNI volta che si corregge qualcosa (quiz, mini-esercizi, esercizi, progetto — qualsiasi cosa), DOPO il feedback aggiornare subito CONTESTO_CORSO.md: lacune dai quiz (🔴), pattern di errore, contatori glossario, ripasso programmato. Non aspettare la fine del capitolo per registrare le lacune.
- **Mai dare la soluzione completa subito**. Gianluca corregge rapidamente dopo il feedback — ha solo bisogno che gli si indichi *dove* e *perché* c'è il problema
- **Scala di aiuto progressiva** (seguire quest'ordine):
  1. **Indicare la zona**: "guarda la riga X, c'è qualcosa che non torna"
  2. **Spiegare il perché**: "questo `elif` fa sì che se un carattere è un numero, non controlla più se è maiuscolo"
  3. **Dare un esempio analogo**: "in JS faresti due `if` separati, non un `else if`"
  4. **Solo se ancora bloccato**: mostrare la soluzione commentata riga per riga
- Controllare sempre che **tutti i requisiti** dell'esercizio siano stati implementati (errore ricorrente #6)
- Quando un errore è stato corretto, **confermarlo**: "questo ora è giusto, bravo"
- Usare la **Checklist di Auto-Revisione** come guida per il feedback: scorrere i punti e verificare se lo studente ha commesso quegli errori

### Come gestire "sono bloccato"

- **Non dare la soluzione**. Prima chiedere: "cosa hai provato finora?" e "cosa ti aspettavi che succedesse?"
- Dare un **suggerimento direzionale**: "prova a stampare il valore di X prima di quella riga — cosa esce?"
- Se è bloccato su un concetto: **rispiegarlo con un'analogia diversa**, non con le stesse parole
- Se è bloccato dopo 2+ tentativi: dare un **esempio analogo più semplice** che usa lo stesso pattern, e lasciarlo risolvere quello prima di tornare all'esercizio originale
- Se è frustrante: riconoscerlo ("questo esercizio è tosto, è normale faticarci") e ricordare che la difficoltà è dove avviene l'apprendimento

### Cosa NON fare mai

1. **Non rispondere in inglese** — tutto il corso è in italiano
2. **Non saltare il confronto PHP** — anche se sembra "ovvio", per chi sta imparando non lo è mai
3. **Non usare notazione matematica** senza tradurla in codice (es. non scrivere Σ senza mostrare `sum()`)
4. **Non dare per acquisito** un concetto che nel glossario ha ancora stato 🔄 o ⚠️
5. **Non scrivere blocchi di codice lunghi** senza commenti esplicativi integrati
6. **Non creare file o capitoli** senza seguire la struttura dei capitoli esistenti
7. **Non dare la soluzione completa** al primo tentativo di correzione (seguire la scala progressiva)
8. **Non ignorare la checklist** di auto-revisione quando si correggono gli esercizi
9. **Non usare abbreviazioni/acronimi** (ML, NLP, CV, API, ecc.) senza averli spiegati almeno una volta nel contesto corrente

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
12. **Mini-esercizi inline dopo ogni sezione di teoria**: dopo OGNI Parte/sezione di spiegazione, inserire un piccolo esercizio pratico (etichettato `# --- MINI-ESERCIZIO X — Prova subito! ---`) che fissa il singolo concetto appena spiegato. Devono essere brevi (2-4 cose da fare), focalizzati solo su quella sezione, e separati dagli esercizi finali più complessi. Questo approccio è stato richiesto dallo studente al capitolo 05 perché aiuta a fissare concetto per concetto prima di affrontare gli esercizi combinati.
13. **Quiz a inizio e fine teoria in ogni capitolo**: ogni capitolo deve avere DUE sezioni quiz:
    - **Quiz d'ingresso** (subito dopo il docstring di apertura, prima della PARTE 1): 5-8 domande rapide sui concetti del **capitolo precedente**, per verificare che siano stati interiorizzati.
    - **Quiz di verifica** (tra l'ultima PARTE di teoria e la sezione ESERCIZI): 5-8 domande sui concetti appena studiati in **questo** capitolo, per verificare la comprensione prima di praticare.
    - I 5 formati di domanda da mescolare in ogni quiz:
      - **Prevedi l'output**: dato un blocco di codice, scrivere cosa stampa
      - **Vero/Falso**: affermazioni su metodi, comportamenti, differenze
      - **Trova l'errore**: codice con un bug da individuare e spiegare
      - **Definizione**: cosa fa un metodo, a cosa corrisponde in JS/PHP
      - **Completa il codice**: codice con parti mancanti (___) da riempire
    - Formato: domande nei commenti, lo studente scrive la risposta sotto ogni domanda. Le risposte corrette vanno nella sezione SOLUZIONI in fondo al file.
    - Approccio richiesto dallo studente al capitolo 05 per avere più dati sui punti deboli.
14. **Rinforzo mirato dai quiz**: le risposte sbagliate o parziali ai quiz vengono registrate nella sezione "Lacune dai Quiz" di questo file. Quando si prepara il capitolo successivo, il Mentor **DEVE** inserire un blocco `# 🔁 RINFORZO MIRATO` per ogni lacuna aperta (stato 🔴), posizionandolo nel punto della teoria dove il concetto debole si collega naturalmente al nuovo argomento. Il rinforzo include una spiegazione con un esempio diverso da quello del quiz + 1-2 micro-esercizi. L'obiettivo è che il concetto venga verificato di nuovo nel quiz d'ingresso del capitolo dopo: se corretto → 🟢, se sbagliato di nuovo → nuovo ciclo di rinforzo.
15. **Tecnica Feynman (spiega con parole tue)**: nei quiz di verifica, includere almeno 1 domanda di tipo **"Spiega con parole tue"** dove Gianluca deve riformulare un concetto come se lo stesse insegnando a un collega. Se non riesce a spiegarlo in modo chiaro e semplice, il concetto non è interiorizzato. Questo è il 6° formato di domanda (aggiunto ai 5 esistenti). Nei quiz d'ingresso è opzionale. Esempio: *"Spiega con parole tue cosa fa `.items()` su un dizionario e perché serve l'unpacking nel for."*
16. **Progetto mini incrementale**: un progetto unico che attraversa tutto il corso, crescendo capitolo dopo capitolo. Ogni capitolo aggiunge una funzionalità nuova usando i concetti appena appresi. Il progetto è definito nella sezione "Progetto Incrementale" di questo file. Alla fine di ogni capitolo, dopo gli esercizi e prima delle soluzioni, c'è una sezione `# 🏗️ PROGETTO INCREMENTALE` con il task specifico per quel capitolo. Questo collega i concetti isolati in qualcosa di concreto e reale, e diventa un pezzo del portfolio.
17. **Esercizi di refactoring**: ogni capitolo (dal 3° in poi) deve contenere almeno 1 esercizio etichettato `# 🔧 [REFACTORING]` dove Gianluca riceve codice funzionante ma scritto male (ripetitivo, con cicli inutili, variabili confuse, pattern inefficienti) e deve riscriverlo usando i concetti del capitolo. Non inventa logica, la migliora. Questo prepara al lavoro reale dove si legge e migliora codice altrui più spesso di quanto se ne scriva da zero.
18. **Interleaving (esercizi mescolati)**: dal capitolo 4° in poi, ogni capitolo deve contenere almeno 1 esercizio etichettato `# 🔀 [INTERLEAVING]` che mescola concetti del capitolo corrente con concetti di 1-2 capitoli precedenti. Costringono il cervello a *scegliere* quale strumento usare, non solo a usare quello appena studiato. La ricerca mostra che l'interleaving è più faticoso ma produce ricordi più duraturi.
19. **Retrieval practice (scrivi da zero dalla memoria)**: dal capitolo 4° in poi, ogni capitolo deve contenere almeno 1 esercizio etichettato `# 🧠 [RETRIEVAL]` dove Gianluca deve riscrivere da zero, senza guardare il codice originale, una funzione o esercizio di un capitolo precedente. L'esercizio specifica COSA riscrivere e da QUALE capitolo. Richiamare dalla memoria è il modo più potente per consolidare.
20. **Confronto "prima e dopo" a fine modulo**: alla fine dell'ULTIMO capitolo di ogni modulo, inserire una sezione `# 🔄 CONFRONTO PRIMA/DOPO` dove Gianluca riguarda il proprio codice del primo capitolo del modulo e lo riscrive con le competenze acquisite. Motivazionale (vede il progresso) e consolidante (applica concetti avanzati a problemi già risolti).

---

## Progresso del Corso

### Modulo 1 — Python & Dati

| File | Stato | Data | Difficoltà (1-10) | Note |
|------|-------|------|--------------------|------|
| 01_benvenuto_python.py | ✅ Completato + Corretto | 17/02/2026 | 2 | Buon primo approccio. Errori tipici da JS: ternario con `?:`, nomi variabili in inglese misto. Ha capito f-string, tipi, casting. |
| 02_condizioni_e_cicli.py | ✅ Completato + Corretto | 17/02/2026 | 4 | FizzBuzz: `range(1,20)` invece di `range(1,21)`. Password: `elif` dove servivano due `if`, `== True` ridondante. Scacchiera perfetta. Temperature incompleto (mancava la media). |
| 03_funzioni.py | ✅ Completato + Corretto | 17/02/2026 | 6 | Ha capito *args, return multipli, sorted. **Lambda ancora poco chiare** — da rinforzare nei prossimi capitoli. Errori: lista vs parametri separati a *args, count come stringa, mancava `reverse=True`, mancava parametro `decimali`. Tutti corretti. |
| 04_liste.py | ✅ Completato + Corretto | 19/02/2026 | 9 | Difficoltà alta. Ha capito slicing, list comprehension, sorted/filter/map con lambda. **Punti deboli**: enumerate+tuple non interiorizzati (molte domande), range a 3 parametri nuovo, consegne non lette completamente (ex.1 indice sbagliato, ex.2 formato incompleto, ex.3 senza funzione, ex.6 usa [::-1] vietato, ex.9 indice errato). Lambda usate correttamente in ex.4/5/7 — miglioramento reale. |
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
| 04_liste | 9 | +3 ↑ (salto preoccupante — enumerate/tuple/combinazione concetti) |

**Media attuale**: 5.25 — Salto da 6 a 9 (+3). La curva accelera. Causa principale: combinazione di concetti nuovi (slicing, list comprehension, lambda con liste, enumerate+tuple). Valutare esercizi di rinforzo su enumerate/tuple prima del capitolo 05.

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
| `f-string` | Stringa con variabili inline `f"ciao {nome}"` | `` `ciao ${nome}` `` / `"ciao $nome"` | 01 | 1/3 | 🔄 |
| `type()` | Restituisce il tipo di una variabile | `typeof` / `gettype()` | 01 | 0/3 | 🔄 |
| `int()`, `float()`, `str()` | Casting esplicito tra tipi | `parseInt()`, `parseFloat()` / `(int)`, `(float)` | 01 | 0/3 | 🔄 |
| `range()` | Genera sequenza di numeri — **il secondo numero è ESCLUSO!** | Non diretto / `range()` PHP | 02 | 0/3 | 🔄 |
| `enumerate()` | Itera dando indice + valore insieme | `.forEach((val, i))` / Non diretto | 02 | 0/3 | 🔄 |
| `for...in` | Itera sugli elementi di una lista | `for...of` / `foreach` | 02 | 1/3 | 🔄 |
| `while` | Ciclo finché la condizione è vera | Identico | 02 | 0/3 | 🔄 |
| `if/elif/else` | Condizionali — nota: `elif` non `else if` | `if/else if/else` | 02 | 0/3 | 🔄 |
| `def` | Definisce una funzione | `function` | 03 | 1/3 | 🔄 |
| `return` multiplo | Restituisce più valori come tupla — si "spacchettano" con `a, b = funzione()` | Non diretto (array/oggetto) | 03 | 0/3 | 🔄 |
| `*args` | Parametri variabili posizionali — come spread `...args` | `...args` / `...$args` | 03 | 0/3 | 🔄 |
| `**kwargs` | Parametri con nome variabili — come passare un oggetto di opzioni | Destructuring / Array associativo | 03 | 0/3 | 🔄 |
| `lambda` | Mini-funzione usa-e-getta, una riga sola — ⚠️ **DA RINFORZARE** | `() =>` / `fn() =>` | 03 | 1/3 | ⚠️ |
| `sorted()` | Ordina creando una NUOVA lista (l'originale resta intatta!) | `.sort()` (attenzione: in JS modifica in-place!) / `usort()` | 03 | 1/3 | 🔄 |
| `isinstance()` | Verifica se un valore è di un certo tipo | `instanceof` / `instanceof` | 03 | 0/3 | 🔄 |
| `docstring` | Commento `"""..."""` dentro una funzione per documentarla | JSDoc `/** */` / PHPDoc `/** */` | 03 | 1/3 | 🔄 |
| `.isdigit()` | True se il carattere è un numero | Regex o `!isNaN()` / `ctype_digit()` | 02 | 0/3 | 🔄 |
| `.isupper()` | True se il carattere è maiuscolo | Regex / `ctype_upper()` | 02 | 0/3 | 🔄 |
| `min()`, `max()`, `sum()` | Funzioni aggregate su liste | `Math.min()`, `.reduce()` / `min()`, `array_sum()` | 03 | 1/3 | 🔄 |
| `len()` | Lunghezza di lista/stringa — è una funzione, non un `.length`! | `.length` / `count()`, `strlen()` | 02 | 1/3 | 🔄 |

### Liste e Iterazione (File 04)

| Termine | Significato sintetico | Equivalente JS/PHP | Cap. | Ripassi | Stato |
|---------|-----------------------|--------------------|------|---------|-------|
| `.append()` | Aggiunge UN elemento in fondo alla lista | `.push()` / `array_push()` | 04 | 0/3 | 🔄 |
| `.insert(pos, elem)` | Inserisce un elemento a una posizione specifica | `.splice(pos, 0, elem)` / `array_splice()` | 04 | 0/3 | 🔄 |
| `.remove(val)` | Rimuove la prima occorrenza per valore | `.splice(indexOf(val), 1)` / `unset()` | 04 | 0/3 | 🔄 |
| `.pop(i)` | Rimuove e restituisce l'elemento alla posizione i | `.splice(i, 1)` / `array_pop()` | 04 | 0/3 | 🔄 |
| slicing `[start:end:step]` | Estrae una porzione di lista — end è ESCLUSO! | `.slice(start, end)` / `array_slice()` | 04 | 0/3 | 🔄 |
| `in` (operatore) | Verifica se un elemento esiste nella lista | `.includes()` / `in_array()` | 04 | 0/3 | 🔄 |
| list comprehension | `[expr for x in lista if cond]` — crea liste in modo compatto | `.map()` + `.filter()` / `array_map()` + `array_filter()` | 04 | 0/3 | 🔄 |
| `filter()` | Filtra elementi con una funzione — restituisce oggetto pigro, serve `list()` | `.filter()` / `array_filter()` | 04 | 0/3 | 🔄 |
| `map()` | Trasforma ogni elemento con una funzione — restituisce oggetto pigro, serve `list()` | `.map()` / `array_map()` | 04 | 0/3 | 🔄 |
| `.count(val)` | Conta quante volte un valore appare nella lista | `.filter().length` / `array_count_values()` | 04 | 0/3 | 🔄 |
| `.index(val)` | Restituisce la posizione di un valore (errore se non trovato!) | `.indexOf()` / `array_search()` | 04 | 0/3 | 🔄 |
| tupla / unpacking | Coppia di valori `(i, val)` — si spacchetta con `a, b = tupla` — ⚠️ **NON INTERIORIZZATO** | Destructuring `[a, b] = arr` / `list($a, $b) = $arr` | 04 | 0/3 | ⚠️ |

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

### Capitolo 04 — liste
- "Spiegami questa funzione (appiattisci_2 con list comprehension doppia)" → Il doppio `for` in una list comprehension non era intuitivo
- "Ma elem cosa è?" → Non capiva che `elem` è solo un nome di variabile scelto dal programmatore, non una keyword
- "Il primo elem rappresenta gli elementi che entrano nell'array?" → Aveva bisogno di capire che l'espressione a sinistra è l'output della list comprehension
- "Non riesco a capire il funzionamento del ciclo for usando enumerate" → enumerate + unpacking ancora non naturale
- "Non capisco dove era la tupla" → Non vedeva la tupla nel codice perché è enumerate a crearla implicitamente — concetto astratto
- "La tupla ed enumerate non mi rendono molto sicuro" → **Autodichiarato**: tuple ed enumerate sono punti deboli consapevoli
- "Perché range ha tre parametri?" → Non sapeva che range() accetta start, stop, step
- "Come funziona enumerate?" → Ha chiesto una spiegazione completa da zero
- "Funzione per lunghezza lista python" → Aveva bisogno di ricordare `len()` — ponte da `.length` e `count()`
- "La tupla la decidiamo noi, basta dividere in due variabili?" → Stava capendo l'unpacking, ma serviva conferma
- "Come fare per evitare che tu possa scordarti queste cose?" → Consapevolezza meta-cognitiva, buon segno — ha portato alla creazione della Cursor Rule

---

## Pattern di Errore Ricorrenti

Questi sono gli errori che Gianluca tende a ripetere. Da monitorare nei prossimi esercizi:

| # | Pattern | Stato | Note |
|---|---------|-------|------|
| 1 | **Sintassi JS in Python**: usa `? :` invece di `if...else` ternario | 🔴 Attivo | Visto al file 01 |
| 2 | **`range()` / slicing fine escluso**: dimentica che il secondo numero è escluso | 🔴 Attivo | Visto al file 02. Ripetuto al file 04: `dati[17:]` invece di `dati[16:]` |
| 3 | **`== True` ridondante**: scrive `if valore == True` | 🟡 Corretto una volta | Visto al file 02, corretto dopo feedback |
| 4 | **Calcoli dentro le f-string**: espressioni troppo lunghe nelle `{}` | 🟡 Corretto una volta | Visto al file 01, corretto dopo feedback |
| 5 | **Tipi nei dizionari**: mette stringhe dove servono numeri | 🟡 Corretto una volta | Visto al file 03 (`count` come stringa) |
| 6 | **Lettura incompleta delle consegne**: non implementa tutti i requisiti | 🔴 Attivo | Visto ai file 02, 03 e 04. Al file 04: ex.1 mesi alterni con indice sbagliato, ex.2 formato stringa incompleto, ex.3 senza funzione, ex.6 usa [::-1] vietato, ex.9 variabile sbagliata |
| 7 | **Lambda poco chiare**: non ha ancora interiorizzato la sintassi e l'uso delle funzioni lambda | 🟡 In miglioramento | Autodichiarato dopo file 03. Al file 04: usate correttamente in ex.4/5/7 con sorted, filter, map. Miglioramento reale ma da consolidare |
| 8 | **enumerate/tuple/unpacking**: non capisce che enumerate crea tuple e che l'unpacking le spacchetta | 🔴 Attivo | Autodichiarato al file 04: "la tupla ed enumerate non mi rendono molto sicuro". Molte domande su questo |
| 9 | **Codice superfluo**: aggiunge espressioni inutili (`== l` dopo `.insert()`) | 🟡 Corretto una volta | Visto al file 04 ex.6 |
| 10 | **Vincoli esercizio ignorati**: usa metodi vietati dalla consegna (es. `[::-1]` quando esplicitamente proibito) | 🔴 Attivo | Visto al file 04 ex.6. Collegato al pattern #6 (lettura consegne) |

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
- **Sessione 2 (19/02/2026)**: File 04 completato. Difficoltà 9 — il salto maggiore finora. Enumerate/tuple e combinazione di concetti sono stati i punti più difficili
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
| "Array.slice()" | Slicing `lista[1:3]` estrae una porzione di lista | `.slice(1, 3)` in JS / `array_slice($arr, 1, 2)` in PHP | 04 | Slicing su stringhe, slicing su array NumPy, selezione righe DataFrame |
| ".push()/.pop()" | `.append()` aggiunge in fondo, `.pop()` rimuove e restituisce | `.push()` / `.pop()` in JS (identico!) | 04 | Strutture dati stack, gestione code |
| ".map() + .filter()" | List comprehension `[expr for x in lista if cond]` fa entrambi | `.map().filter()` in JS / `array_map()` + `array_filter()` in PHP | 04 | `.apply()` su DataFrame Pandas, trasformazione dati |

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

### Dopo il Capitolo 04 — Liste
- So creare, modificare e accedere a elementi di una lista con `.append()`, `.insert()`, `.remove()`, `.pop()`
- So estrarre porzioni con lo slicing `[start:end:step]`, incluso il reverse `[::-1]`
- So usare `in` per verificare se un elemento è nella lista
- So usare list comprehension per trasformare e filtrare: `[expr for x in lista if cond]`
- So ordinare con `sorted()` + `lambda` come key, anche con `reverse=True`
- So usare `filter()` e `map()` con lambda (avvolgendo con `list()`)
- So lavorare con liste di liste (matrici) e accedere con doppio indice `lista[r][c]`
- So usare `.count()` per contare occorrenze e `max()` con lambda per trovare l'elemento più frequente
- So dividere dati in training/test con slicing e creare batch con `range(start, stop, step)`
- ⚠️ enumerate() e tuple/unpacking: capisco il concetto ma non mi viene ancora naturale
- ⚠️ Lambda: in miglioramento — usate correttamente con sorted, filter, map, ma serve ancora pratica

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
- [ ] **Ho rispettato TUTTI i vincoli?** Se dice "senza usare X", ho davvero evitato X? (es. "senza [::-1]" significa che NON posso usarlo)
- [ ] **L'esercizio chiede una funzione?** Se dice "scrivi una funzione", devo usare `def`, non scrivere il codice libero
- [ ] **Ho usato slicing?** Ricorda: il secondo indice è ESCLUSO, come `range()`. `dati[16:]` parte dall'indice 16, non dal 17!

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
| f-string, tipi, casting | 17/02 | ✅ file 04 (usato correttamente) | file 06 | file 09 | OK |
| if/elif/else, for, while | 17/02 | ✅ file 04 (usato correttamente) | file 06 | file 09 | OK |
| range() fine escluso | 17/02 | ❌ file 04 (errore ripetuto: dati[17:]) | ❌ quiz ingresso 05 (numeri[1:4]→4 elem, prezzi[1:]→indice sbagliato) | file 09 | 🔴 Errore persistente — 3 occorrenze |
| enumerate() unpacking | 17/02 | ❌ file 04 (molte domande, non autonomo) | ❌ quiz ingresso 05 (ha usato range invece di enumerate) | file 09 | 🔴 Non interiorizzato — conferma al quiz |
| def, return, *args, **kwargs | 17/02 | file 05 | file 07 | file 10 | Da verificare |
| lambda | 17/02 | 🟡 file 04 (usata correttamente in ex.4/5/7 ma con aiuto teoria) | file 05 ⚠️ | file 07 | In miglioramento |
| sorted() con key | 17/02 | ✅ file 04 (usato correttamente con lambda) | ⚠️ quiz ingresso 05 (non sa che sorted crea nuova lista, pensa lambda obbligatoria) | file 07 | ⚠️ Uso corretto ma teoria incompleta |
| slicing, list comprehension | 19/02 | file 05 | file 07 | file 10 | Da verificare |
| tuple/unpacking | 19/02 | file 05 ⚠️ | file 07 ⚠️ | file 10 | ⚠️ Rinforzo prioritario |
| filter(), map() | 19/02 | file 05 | file 07 | file 10 | Da verificare |

⚠️ = Il concetto richiede rinforzo attivo (non solo uso passivo, ma esercizio dedicato)

---

## Lacune dai Quiz — Rinforzo nel Prossimo Capitolo

> Dopo la correzione dei quiz (ingresso o verifica), le risposte sbagliate o parziali vengono registrate qui.
> Il Mentor **DEVE** consultare questa tabella quando prepara un nuovo capitolo e inserire
> un blocco `# 🔁 RINFORZO MIRATO` per ogni lacuna con stato 🔴, al punto della teoria dove il
> concetto si collega naturalmente al nuovo argomento.
>
> **Ciclo di vita di una lacuna**:
> 1. Gianluca sbaglia una domanda al quiz → si aggiunge una riga con stato 🔴
> 2. Nel capitolo successivo si inserisce un blocco RINFORZO MIRATO → stato passa a 🟡
> 3. Al quiz d'ingresso del capitolo dopo, se risponde correttamente → stato passa a 🟢
> 4. Se sbaglia di nuovo → torna a 🔴 con un nuovo rinforzo programmato

| # | Concetto | Quiz (tipo/cap.) | Errore commesso | Rinforzo in | Stato |
|---|----------|-------------------|-----------------|-------------|-------|
| 1 | Slicing — fine escluso | Ingresso/05 | `numeri[1:4]` → ha scritto [20,30,40,50] invece di [20,30,40]. Non applica "il secondo numero è escluso" | 06 | 🔴 |
| 2 | .append() restituisce None | Ingresso/05 | Pensava che .append() restituisse la lista modificata (come .push() in JS restituisce la lunghezza). In Python modifica in-place e restituisce None | 06 | 🔴 |
| 3 | enumerate vs range | Ingresso/05 | Ha scritto `range(frutti, len(frutti))` dove serviva `enumerate(frutti, 1)`. Non distingue quando usare enumerate e quando range | 06 | 🔴 |
| 4 | Indici delle liste (contare da 0) | Ingresso/05 | Per ottenere [30,40,50] da [10,20,30,40,50] ha scritto `[1:]` invece di `[2:]`. Sa che 3 era troppo ma non conta da 0 correttamente | 06 | 🔴 |
| 5 | sorted() crea nuova lista vs .sort() in-place | Ingresso/05 | Sa che uno è funzione e l'altro metodo, ma non ha menzionato la differenza chiave: sorted() crea una NUOVA lista, .sort() modifica in-place e restituisce None. Dice anche che lambda è obbligatoria (è opzionale) | 06 | 🔴 |
| 6 | Output concreto vs descrizione concettuale | Ingresso/05 | Alla domanda "cosa stampa" ha descritto il concetto invece di dare il valore concreto `["Marco"]`. Capisce il meccanismo ma non sa prevedere l'output esatto | 06 | 🔴 |
| 7 | Variabile corretta nelle comprehension | Ingresso/05 | Ha scritto `x % 2 == 0` quando la variabile del for era `n`. Causerebbe NameError. Disattenzione sui nomi delle variabili nel contesto della comprehension | 06 | 🔴 |

Stato: 🔴 Da rinforzare | 🟡 Rinforzato (da verificare al quiz successivo) | 🟢 Superato

### Formato del blocco RINFORZO MIRATO nei capitoli

Quando l'agente prepara un capitolo e ci sono lacune 🔴 nella tabella, inserisce blocchi con questo formato nei punti strategici della teoria:

```
# 🔁 RINFORZO MIRATO — [nome concetto]
# Al quiz del cap. XX hai confuso/sbagliato [breve descrizione errore].
# Rivediamolo con un esempio diverso:
# [spiegazione breve con nuovo esempio, diverso da quello del quiz]
#
# Prova subito:
# 1) [micro-esercizio focalizzato sulla lacuna]
# 2) [secondo micro-esercizio, opzionale]
# Scrivi qui sotto:
# ...
```

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
| Rimuovi duplicati da lista | 04 | Junior — classico | Iterazione, `not in`, costruzione lista di appoggio | ✅ Risolto (logica corretta, mancava incapsulamento in funzione) |
| Inverti lista senza .reverse() | 04 | Junior — classico | Cicli, `.insert(0)`, `range()` con passo negativo | ✅ Risolto (con errori: `== l` superfluo, seconda versione usa [::-1] vietato) |
| Elemento più frequente | 04 | Junior/Mid — frequente | `max()` con lambda, `.count()` | ✅ Risolto perfettamente al primo tentativo |

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

## Progetto Incrementale — "Catalogo E-commerce"

> Un progetto unico che cresce capitolo dopo capitolo. Ogni capitolo aggiunge una funzionalità
> usando i concetti appena appresi. Alla fine del modulo, Gianluca avrà costruito un sistema
> completo di gestione catalogo prodotti — applicabile direttamente al mondo e-commerce che conosce.
>
> Il progetto è pensato per il dominio che Gianluca padroneggia (e-commerce/web), così il contesto
> non aggiunge carico cognitivo e può concentrarsi sulla tecnica Python.

### Tema del progetto

**"Catalogo E-commerce"** — Un sistema per gestire prodotti, ordini, statistiche e visualizzazioni di un negozio online. Parte semplice (una lista di prodotti) e cresce fino a diventare un piccolo tool di analisi dati con output grafici.

### Roadmap per capitolo

| Capitolo | Funzionalità da aggiungere | Concetti esercitati |
|----------|----------------------------|---------------------|
| 04 — Liste | Lista prodotti: aggiungere, rimuovere, cercare, ordinare per nome/prezzo | Liste, slicing, sorted + lambda, list comprehension |
| 05 — Dizionari | Prodotti come dizionari con proprietà (nome, prezzo, categoria, stock). Carrello come dizionario. | Dizionari, .get(), .items(), dict comprehension, nesting |
| 06 — File CSV | Caricare il catalogo da file CSV e salvare gli aggiornamenti su file | Lettura/scrittura CSV, parsing, gestione errori |
| 07 — NumPy | Calcoli statistici su prezzi: media, deviazione standard, normalizzazione, percentili | Array NumPy, operazioni vettoriali, aggregazioni |
| 08 — Tensori | Rappresentare immagini prodotto come tensori, operazioni base su batch di immagini | Tensori 2D/3D, reshape, operazioni su assi |
| 09 — Pandas | Caricare catalogo in DataFrame, filtrare, raggruppare per categoria, pivot table | DataFrame, query, groupby, merge |
| 10 — Pandas Progetto | Report completo: top seller, margini, trend, export HTML | Analisi completa, apply, multi-aggregation |
| 11 — Matplotlib | Dashboard visuale: grafico prezzi per categoria, trend vendite, pie chart stock | plot, bar, pie, subplot, styling |
| 12 — Web Bridge | API endpoint FastAPI che espone il catalogo e le statistiche | FastAPI, endpoint, JSON response |

### Progresso del progetto

| Capitolo | Stato | Note |
|----------|-------|------|
| 04 — Liste | ⬜ Non ancora assegnato (il cap. 04 era già completato prima dell'introduzione del progetto) | |
| 05 — Dizionari | ⬜ Da fare | Prima volta con il progetto incrementale |
| 06 — File CSV | ⬜ Da fare | |
| 07 — NumPy | ⬜ Da fare | |
| 08 — Tensori | ⬜ Da fare | |
| 09 — Pandas | ⬜ Da fare | |
| 10 — Pandas Progetto | ⬜ Da fare | |
| 11 — Matplotlib | ⬜ Da fare | |
| 12 — Web Bridge | ⬜ Da fare | |

### Regole per il progetto incrementale

1. La sezione `# 🏗️ PROGETTO INCREMENTALE` va alla fine degli esercizi, prima delle soluzioni
2. Deve richiedere 15-25 minuti (non troppo lungo, non troppo breve)
3. Il task deve usare SOLO concetti visti fino a quel capitolo (niente anticipazioni)
4. Ogni capitolo costruisce sul codice del capitolo precedente — lo studente può copiare e estendere
5. La soluzione va nella sezione SOLUZIONI come gli altri esercizi
6. Se è il primo capitolo con il progetto, fornire il codice base da cui partire

---

## Note per il Mentor

### Promemoria automatici
- **Dopo ogni capitolo completato**: chiedere il voto di difficoltà (1-10) se non lo dà spontaneamente
- **Dopo ogni capitolo**: aggiornare glossario, domande, pattern di errore, progresso
- **Prima del file 07**: arricchire con più esempi visivi e mini-esercizi intermedi
- **Prima del file 08**: aggiungere rappresentazioni ASCII di tensori 2D/3D/4D
- **⚠️ Al completamento del file 08** (o quando il file supera ~1000 righe): AVVISARE Gianluca che è il momento di separare CONTESTO_CORSO.md in due file — uno snello con stato attuale, regole e comportamenti (che l'agente legge sempre), e uno di archivio con storico dettagliato (glossario acquisito, capitoli vecchi, domande passate). Questo previene problemi di contesto troppo lungo per gli agenti futuri.

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

---

## Template Struttura File Capitolo

> Quando l'agente crea un NUOVO file di capitolo (.py), DEVE seguire questa struttura.
> Basata sui file 01-03 già creati e validati dallo studente.

```python
"""
============================================================================
 MODULO X — ESERCIZIO XX: Titolo del Capitolo
 Sottotitolo con concetti chiave
============================================================================

 TEORIA: Nome del Concetto — Analogia con il Mondo Web

 [Analogia iniziale con qualcosa che Gianluca conosce: Laravel, JS, HTML, ecc.]
 [Spiegazione del concetto in termini pratici, NON astratti]

 Confronto a tre — lo stesso concetto in PHP, JavaScript e Python:

   PHP:
     [codice PHP con commento che spiega cosa fa ogni parte]

   JavaScript:
     [codice JS con commento che spiega cosa fa ogni parte]

   Python:
     [codice Python con commento che spiega cosa fa ogni parte]

 [Se ci sono termini nuovi: spiegarli qui con esempio PRIMA di usarli nel codice]

============================================================================
"""

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ D'INGRESSO — Rispondi PRIMA di leggere la teoria!              ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti del capitolo PRECEDENTE.
# Rispondi senza guardare il codice — servono a capire cosa hai interiorizzato.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — Prevedi l'output:
# Cosa stampa questo codice?
#   [codice]
# La tua risposta: ___

# DOMANDA 2 — Vero o Falso?
# "[affermazione]"
# La tua risposta (V/F): ___

# [... 5-8 domande, mescolando i 5 formati ...]


# ============================================================
# SEZIONE 1: Concetto Base — con esempi commentati
# ============================================================

# [Spiegazione inline del concetto]
# [Confronto JS/PHP inline dove utile]

# Esempio 1 — [Descrizione]
# [Codice con commenti che spiegano ogni passaggio]

# Esempio 2 — [Descrizione]
# [Codice con commenti]

# RIPASSO: [termine già visto] — ricordi? [breve richiamo con parole diverse]
# [Esempio che riusa il termine in questo nuovo contesto]

# 🔁 RINFORZO MIRATO — [concetto debole dal quiz precedente]
# Al quiz del cap. XX hai confuso/sbagliato [breve descrizione errore].
# Rivediamolo con un esempio diverso:
# [spiegazione con nuovo esempio, collegato al contesto della sezione corrente]
#
# Prova subito:
# 1) [micro-esercizio focalizzato sulla lacuna]
# 2) [secondo micro-esercizio, opzionale]
# Scrivi qui sotto:
# ...
# (Questo blocco viene inserito SOLO se ci sono lacune 🔴 nella tabella
#  "Lacune dai Quiz" di CONTESTO_CORSO.md. Va posizionato dove il concetto
#  debole si collega naturalmente al nuovo argomento della sezione.)

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# [2-4 task brevi e focalizzati SOLO sul concetto di questa sezione]
# [Non devono essere complessi — servono a fissare prima di proseguire]
# Scrivi qui sotto:
# ...

# ============================================================
# SEZIONE 2: Concetto Intermedio
# ============================================================

# [Stessa struttura della sezione 1, incluso mini-esercizio alla fine]

# ============================================================
# SEZIONE 3: Concetto Avanzato (se presente)
# ============================================================

# [Stessa struttura]

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ DI VERIFICA — Hai capito la teoria?                            ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti di QUESTO capitolo.
# Rispondi DOPO aver letto la teoria, PRIMA di fare gli esercizi.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — [formato tra i 5 classici]
# [domanda]
# La tua risposta: ___

# [... 5-8 domande, mescolando i 5 formati classici ...]

# DOMANDA X — 💬 Spiega con parole tue (Tecnica Feynman):
# Spiega come se lo stessi insegnando a un collega: [concetto chiave del capitolo].
# Non usare codice — solo parole. Se non riesci a spiegarlo chiaramente,
# quel concetto ha bisogno di rinforzo.
# La tua spiegazione: ___
# (Almeno 1 domanda Feynman obbligatoria nel quiz di verifica)


# ============================================================
# ESERCIZI PRATICI
# ============================================================

# --- ESERCIZIO 1 (Livello 1 — Leggi e Modifica): ---
# [Descrizione chiara di cosa fare]
# [Requisiti numerati: 1. ..., 2. ..., 3. ...]

# --- ESERCIZIO 2 (Livello 2 — Scrivi da Zero): ---
# [Descrizione + requisiti]

# --- ESERCIZIO 3 (Livello 2): ---
# # 🎯 [COLLOQUIO] — Questo esercizio replica una domanda reale da colloquio tecnico
# [Descrizione + requisiti]

# --- ESERCIZIO 4 (Livello 2 — Lambda): ---
# [Esercizio che usa lambda per rinforzo — obbligatorio fino a che lambda è ⚠️]

# --- ESERCIZIO 5 (Livello 3 — Web Bridge): ---
# [Esercizio che collega il concetto al mondo web/API]

# --- ESERCIZIO X — 🔧 [REFACTORING]: ---
# Il codice qui sotto FUNZIONA, ma è scritto male.
# Riscrivilo usando i concetti di questo capitolo per renderlo più pulito,
# leggibile e Pythonico.
# [Codice brutto ma funzionante da riscrivere]
# Requisiti: [cosa deve migliorare]

# --- ESERCIZIO X — 🔀 [INTERLEAVING]: ---
# (dal capitolo 04 in poi)
# Questo esercizio mescola concetti di capitoli diversi.
# [Descrizione che richiede concetti del capitolo corrente + 1-2 precedenti]

# --- ESERCIZIO X — 🧠 [RETRIEVAL]: ---
# (dal capitolo 04 in poi)
# Senza guardare il codice del capitolo XX, riscrivi da zero la funzione
# [nome_funzione] che [descrizione di cosa faceva].
# Requisiti: [stessi dell'originale, riportati qui]

# Scrivi il tuo codice sotto ogni esercizio ↓


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  🏗️ PROGETTO INCREMENTALE — Catalogo E-commerce                      ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# In questo capitolo aggiungi al progetto: [funzionalità specifica]
# Parti dal codice del capitolo precedente (oppure dal codice base
# fornito se è la prima volta).
#
# Task:
# 1) [cosa fare, passo passo]
# 2) [...]
# 3) [...]
#
# Questo progetto attraversa tutto il corso — ogni capitolo aggiunge
# un pezzo. Alla fine avrai un sistema completo di gestione catalogo.

# Scrivi il tuo codice qui sotto:
# ...


# ============================================================
# 🔄 CONFRONTO PRIMA/DOPO (solo nell'ultimo capitolo di ogni modulo)
# ============================================================

# (Questa sezione compare SOLO nell'ultimo capitolo di un modulo)
# Riguarda il tuo codice del capitolo XX (il primo di questo modulo).
# Riscrivilo usando TUTTO quello che hai imparato in questo modulo.
# Confronta il "prima" e il "dopo" — vedrai quanto sei migliorato!


# ============================================================
# SOLUZIONI (NON SBIRCIARE!)
# ============================================================

# --- RISPOSTE QUIZ D'INGRESSO ---
# 1. [risposta con spiegazione breve]
# 2. [risposta con spiegazione breve]
# [ecc.]

# --- RISPOSTE QUIZ DI VERIFICA ---
# 1. [risposta con spiegazione breve]
# 2. [risposta con spiegazione breve]
# [ecc.]

# --- SOLUZIONE ESERCIZIO 1 ---
# [Codice commentato]

# --- SOLUZIONE ESERCIZIO 2 ---
# [Codice commentato]

# [ecc.]
```

### Regole per i contenuti dei capitoli

1. **Minimo 5 esercizi** per capitolo (almeno 1 Livello 1, almeno 2 Livello 2, almeno 1 con lambda finché è ⚠️, almeno 1 Livello 3)
2. **Almeno 1 esercizio** con tag `🎯 [COLLOQUIO]`
3. **Teoria**: massimo 30% del file, il resto è codice ed esercizi
4. **Ogni metodo/funzione nuova**: mini-esempio isolato PRIMA dell'uso in un esercizio
5. **Confronto PHP + JS**: obbligatorio nella teoria, consigliato nei commenti degli esercizi
6. **Soluzioni**: sempre in fondo, commentate (con `#`), con commenti che spiegano il perché
7. **Ripasso**: inserire almeno 2 richiami a termini del glossario con stato 🔄 o ⚠️
8. **Difficoltà crescente**: gli esercizi devono salire gradualmente, non fare salti bruschi
9. **Mini-esercizi inline obbligatori**: dopo OGNI sezione di teoria, aggiungere un mini-esercizio (etichettato `# --- MINI-ESERCIZIO X — Prova subito! ---`) con 2-4 task brevi focalizzati SOLO sul concetto appena spiegato. Servono a fissare il singolo concetto prima di proseguire. Sono SEPARATI dagli esercizi finali che combinano più concetti. Approccio richiesto dallo studente al capitolo 05.
10. **Due sezioni quiz per capitolo**: (a) Quiz d'ingresso prima della teoria (5-8 domande sul capitolo precedente), (b) Quiz di verifica dopo la teoria e prima degli esercizi (5-8 domande su questo capitolo). 5 formati: prevedi output, V/F, trova errore, definizione, completa codice. Risposte in fondo con le soluzioni.
11. **Blocchi RINFORZO MIRATO obbligatori**: se nella tabella "Lacune dai Quiz" di CONTESTO_CORSO.md ci sono righe con stato 🔴, il capitolo **DEVE** contenere un blocco `# 🔁 RINFORZO MIRATO — [concetto]` per ciascuna lacuna aperta. Il blocco va posizionato nella sezione di teoria dove il concetto debole si collega naturalmente al nuovo argomento. Formato: etichetta, descrizione dell'errore commesso, spiegazione con esempio diverso da quello del quiz, 1-2 micro-esercizi focalizzati. Questi blocchi sono SEPARATI dai mini-esercizi e dagli esercizi finali.
12. **Almeno 1 esercizio di refactoring** per capitolo (dal cap. 03 in poi), etichettato `# 🔧 [REFACTORING]`. Fornire codice funzionante ma scritto male, che lo studente deve riscrivere usando i concetti del capitolo. Il codice "brutto" deve contenere pattern riconoscibili (cicli inutili, variabili poco chiare, ripetizioni) migliorabili con gli strumenti appena appresi.
13. **Almeno 1 esercizio di interleaving** per capitolo (dal cap. 04 in poi), etichettato `# 🔀 [INTERLEAVING]`. L'esercizio deve mescolare concetti del capitolo corrente con concetti di 1-2 capitoli precedenti, costringendo a scegliere lo strumento giusto.
14. **Almeno 1 esercizio di retrieval practice** per capitolo (dal cap. 04 in poi), etichettato `# 🧠 [RETRIEVAL]`. Lo studente deve riscrivere da zero, senza guardare il codice originale, una funzione/esercizio di un capitolo precedente. L'esercizio specifica cosa riscrivere e da quale capitolo.
15. **Almeno 1 domanda Feynman** nel quiz di verifica, etichettata `# 💬 Spiega con parole tue`. Lo studente deve riformulare un concetto chiave del capitolo con parole proprie, senza usare codice. Se la spiegazione è confusa o incompleta, il concetto va registrato come lacuna.
16. **Sezione Progetto Incrementale** obbligatoria in ogni capitolo (dal cap. 05 in poi), etichettata `# 🏗️ PROGETTO INCREMENTALE`. Il task specifico per ogni capitolo è definito nella roadmap della sezione "Progetto Incrementale" di CONTESTO_CORSO.md. Deve durare 15-25 minuti e usare solo concetti visti fino a quel punto.
17. **Sezione Confronto Prima/Dopo** obbligatoria nell'ULTIMO capitolo di ogni modulo, etichettata `# 🔄 CONFRONTO PRIMA/DOPO`. Lo studente riguarda il proprio codice del primo capitolo del modulo e lo riscrive con le competenze acquisite.
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

### Passo 10 — Lacune dai Quiz
- [ ] Se in questa sessione sono stati corretti dei quiz (ingresso o verifica): per ogni risposta **sbagliata o parziale**, aggiungere una riga alla tabella "Lacune dai Quiz" con stato 🔴 e il capitolo target per il rinforzo (= il prossimo da preparare)
- [ ] Se una lacuna già registrata è stata rinforzata in questo capitolo (blocco 🔁 inserito): aggiornare lo stato a 🟡
- [ ] Se al quiz d'ingresso Gianluca ha risposto correttamente a un concetto che era 🟡: aggiornare lo stato a 🟢 Superato
- [ ] Se al quiz d'ingresso Gianluca ha sbagliato di nuovo un concetto che era 🟡: riportare lo stato a 🔴 e programmare un nuovo rinforzo
- [ ] Se una domanda Feynman (💬 "Spiega con parole tue") ha ricevuto una risposta confusa o incompleta: registrarla come lacuna con nota "Feynman — non sa riformulare"

### Passo 11 — Progetto Incrementale e Metodi Avanzati
- [ ] Se il capitolo conteneva la sezione 🏗️ PROGETTO INCREMENTALE: aggiornare la tabella "Progresso del progetto" nella sezione "Progetto Incrementale" (stato ✅/⚠️ + note)
- [ ] Se il capitolo conteneva un esercizio 🔧 [REFACTORING]: annotare nelle Note del Progresso se Gianluca ha migliorato effettivamente il codice e come
- [ ] Se il capitolo conteneva un esercizio 🧠 [RETRIEVAL]: se Gianluca è riuscito a riscrivere la funzione senza errori, incrementare il contatore ripasso del concetto corrispondente nel Glossario. Se ha avuto difficoltà, annotare e programmare un nuovo retrieval nel capitolo dopo
- [ ] Se è l'ultimo capitolo del modulo e conteneva 🔄 CONFRONTO PRIMA/DOPO: annotare le osservazioni di Gianluca sul proprio miglioramento nella sezione "Cosa So Fare Adesso"

---

## Esempio Completo di Aggiornamento — Template per l'Agente

> Questo esempio mostra ESATTAMENTE come deve apparire ogni aggiornamento.
> L'agente DEVE seguire questi formati. Scenario: Gianluca ha completato il file 04_liste.py
> con voto difficoltà 5, ha fatto un errore nuovo (indici negativi), ha usato lambda correttamente
> una volta, e ha chiesto "cos'è lo slicing?".

### Passo 1 — Aggiornamento Stato Attuale

```markdown
| Campo | Valore |
|-------|--------|
| **Capitolo in corso** | 05_dizionari.py (prossimo da iniziare) |
| **Ultimo completato** | 04_liste.py (18/02/2026) |
| **Modulo attuale** | 1 — Python & Dati |
| **Difficoltà media** | 4.25 (media di 2, 4, 6, 5) |
| **Priorità attive** | Lambda in miglioramento (⚠️→🟡), slicing da rinforzare |
| **Sessione corrente** | Sessione 3 |
```

### Passo 2 — Riga nella tabella Progresso

```markdown
| 04_liste.py | ✅ Completato + Corretto | 18/02/2026 | 5 | Ha capito append/extend/slicing. Errore: confusione indici negativi. Lambda usata correttamente in un esercizio con sorted(). |
```

### Passo 2b — Riga nella tabella Valutazioni

```markdown
| 04_liste | 5 | -1 ↓ (buon segno, la curva si stabilizza) |
```

### Passo 3 — Nuovi termini nel Glossario (formato esatto della riga)

```markdown
| `.append()` | Aggiunge UN elemento in fondo alla lista | `.push()` / `array_push()` | 04 | 0/3 | 🔄 |
| `.extend()` | Aggiunge TUTTI gli elementi di un'altra lista | `.concat()` o spread `[...a, ...b]` / `array_merge()` | 04 | 0/3 | 🔄 |
| slicing `[1:3]` | Estrae una porzione di lista — il secondo indice è ESCLUSO | `.slice(1, 3)` / `array_slice()` | 04 | 0/3 | 🔄 |
```

### Passo 3b — Incremento contatore per termine GIÀ esistente

Quando incrementare: Gianluca ha USATO il termine nel suo codice CORRETTAMENTE e senza aiuto.

```markdown
PRIMA:  | `lambda` | Mini-funzione usa-e-getta... | `() =>` / `fn() =>` | 03 | 0/3 | ⚠️ |
DOPO:   | `lambda` | Mini-funzione usa-e-getta... | `() =>` / `fn() =>` | 03 | 1/3 | ⚠️ |
```

NON incrementare se:
- L'agente ha scritto il codice con lambda e Gianluca l'ha solo letto
- Gianluca ha usato lambda ma con errori che l'agente ha dovuto correggere

Quando cambiare stato:
- **0/3 → 1/3**: primo uso corretto autonomo
- **2/3 → 3/3**: terzo uso corretto → cambiare stato a ✅
- Se dopo ✅ fa un errore: tornare a 🔄 con contatore 0/3

### Passo 4 — Domande (formato esatto)

```markdown
### Capitolo 04 — liste
- "Cos'è lo slicing?" → Non conosceva il concetto di estrarre porzioni di lista. In JS usa `.slice()` ma non sapeva che Python usa la sintassi `[1:3]`
- "Posso usare indici negativi?" → Curiosità proattiva, buon segno. Concetto spiegato, da rinforzare
```

### Passo 5 — Nuovo pattern di errore (formato esatto)

```markdown
| 8 | **Confusione indici negativi**: non intuisce che `lista[-1]` è l'ultimo elemento | 🔴 Attivo | Visto al file 04 |
```

### Passo 6 — Competenze (formato esatto)

```markdown
### Dopo il Capitolo 04 — Liste
- So creare, modificare e accedere a elementi di una lista
- So usare `.append()`, `.extend()`, `.insert()`, `.remove()`, `.pop()`
- So estrarre porzioni con lo slicing `[start:end:step]`
- So iterare con `for`, `enumerate()` e usare `in` per verificare appartenenza
- So ordinare con `sorted()` e `.sort()`, e conosco la differenza
- ⚠️ Indici negativi: capisco il concetto ma devo fare più pratica
```

### Passo 6b — Nuovo ponte mentale (formato esatto)

```markdown
| "Array.slice()" | Slicing `lista[1:3]` estrae una porzione | `.slice(1, 3)` in JS / `array_slice($arr, 1, 2)` in PHP | 04 | Slicing su stringhe, slicing su array NumPy, selezione righe DataFrame |
```

### Passo 7 — Esercizio colloquio (formato esatto)

```markdown
| Rimuovere duplicati da lista | 04 | Junior — classico | Comprensione set(), list comprehension, ordine elementi | ✅ Risolto |
```

### Passo 8 — Nuova riga checklist (formato esatto)

```markdown
- [ ] **Ho usato indici negativi?** Ricorda: `lista[-1]` è l'ultimo, `lista[-2]` è il penultimo
```

### Criteri per le decisioni dell'agente

| Situazione | Azione |
|------------|--------|
| Gianluca usa un termine nel codice senza errori e senza suggerimenti | Incrementare contatore ripasso (+1) |
| Gianluca usa un termine ma con errore, poi corregge dopo feedback | NON incrementare, ma annotare nelle Note |
| Gianluca chiede "cos'è X?" per un termine già nel glossario | Il termine NON è acquisito, azzerare contatore se necessario |
| Un errore non si ripresenta per 3 capitoli consecutivi | Cambiare stato da 🔴/🟡 a 🟢 Superato |
| Gianluca completa un esercizio 🎯 [COLLOQUIO] al primo tentativo senza errori | Segnare "✅ Risolto" nella tabella colloquio |
| Gianluca completa un esercizio 🎯 [COLLOQUIO] con errori poi corretti | Segnare "✅ Risolto (con errori, poi corretto)" |
| La difficoltà media supera 7 | Creare esercizi di rinforzo PRIMA del prossimo capitolo |
| La difficoltà media scende sotto 4 | Aggiungere esercizi bonus/sfida al prossimo capitolo |
