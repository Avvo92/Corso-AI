# Contesto del Corso AI — File per il Mentor

> Questo file viene consultato e aggiornato dal Mentor AI ad ogni sessione.
> Serve a mantenere continuità tra le conversazioni e calibrare il corso.
>
> **Ultimo aggiornamento**: 24/02/2026
>
> **Struttura di questo file**: le prime ~100 righe contengono TUTTO ciò che l'AI
> deve sapere immediatamente (stato, ultima sessione, priorità attive, prossimo capitolo).
> Il resto è contesto di supporto da consultare quando serve.

---

## ⚡ Stato Attuale — Leggere Per Primo

| Campo | Valore |
|-------|--------|
| **Capitolo in corso** | 06_file_csv.py (in corso avanzato: teoria + quiz completati, esercizi finali da completare) |
| **Ultimo completato** | 05_dizionari.py (17/02/2026) |
| **Modulo attuale** | 1 — Python & Dati |
| **Difficoltà media** | 5.8 (media di 2, 4, 6, 9, 8 — curva si stabilizza) |
| **Priorità attive** | ✅ Lambda quasi acquisita, ✅ enumerate+.items() consolidato, 🟡 Lettura consegne in miglioramento (nuovo formato esercizi inserito), 🟡 Slicing/range in miglioramento, 🟡 Dict comprehension migliorata, 🔴 Parsing CSV manuale vs DictReader da consolidare (passi operativi + output atteso) |
| **Sessione corrente** | Sessione 4 |

---

## 📝 Ultima Sessione — Continuità tra Chat

> Questa sezione viene aggiornata dall'agente alla FINE di ogni sessione di lavoro.
> Serve a dare continuità immediata quando si apre una nuova chat.

| Campo | Valore |
|-------|--------|
| **Data** | 24/02/2026 |
| **Cosa è stato fatto** | Avanzamento concreto su 06_file_csv.py: completati mini-esercizi 3-6 con feedback iterativo, completati rinforzi mirati (output concreto e variabile nelle comprehension), quiz di verifica completato (7/8 pienamente corretti, 1 parziale), chiariti dubbi su path/file (`os.path.join`, `os.makedirs`, `open`), introdotti 3 esercizi extra `.get()` vs `.items()`, aggiornata formulazione degli esercizi con formato esplicito anti-ambiguita (obiettivo/input/output/vincoli/checklist/criterio) sia in CONTESTO_CORSO.md sia nel capitolo 06. |
| **Errori emersi** | Nessun errore bloccante. Gap residuo: parsing CSV manuale spiegato in modo parziale (serve rinforzo sui passaggi operativi end-to-end) e distinzione "numero ordini" vs "somma quantita". |
| **Cosa fare nella prossima sessione** | Completare e correggere gli esercizi finali del capitolo 06 + progetto incrementale; inserire nel capitolo 07 un rinforzo mirato su parsing CSV (manuale vs `csv.DictReader`) con focus su pipeline operativa e output concreto. |
| **Stato motivazione** | Alto e stabile — approccio molto attivo, richieste di chiarezza precise, ottima metacognizione su ambiguita delle consegne. |

---

## 🔴 Priorità Attive — Errori e Lacune da Monitorare ORA

> Questa sezione raccoglie SOLO gli elementi con stato 🔴 o ⚠️ che l'agente deve
> tenere presenti ADESSO. È un "cruscotto" — il dettaglio completo è nelle sezioni
> dedicate più in basso.

### Pattern di errore attivi (🔴)

| # | Pattern | Ripetuto in |
|---|---------|-------------|
| 1 | Sintassi JS in Python (`? :` invece di ternario Python) | file 01 |
| 2 | `range()` / slicing fine escluso | file 02, 04, quiz 05 |
| 5 | Tipi nei dizionari: stringhe dove servono numeri | file 03, 05 |
| 6 | Lettura incompleta delle consegne | file 02, 03, 04, 05 |
| 10 | Vincoli esercizio ignorati | file 04 |
| 11 | Ordine parametri `filter()`: mette lista prima di lambda | file 05 |

### Concetti da rinforzare (⚠️)

| Concetto | Stato | Note breve |
|----------|-------|------------|
| Lambda | ⚠️ In miglioramento | Usata correttamente con sorted, ma ordine parametri filter fragile |
| Dict comprehension | ⚠️ Non interiorizzata | Tende a usare for classico quando la consegna chiede dict comprehension |
| Tuple/unpacking | ⚠️ → 🟡 In miglioramento | Ponte mentale `.items() = enumerate dei dizionari` ha funzionato |

### Lacune quiz aperte (🔴) — da rinforzare nel capitolo 06

| # | Concetto | Errore commesso |
|---|----------|-----------------|
| 1 | Slicing fine escluso | `numeri[1:4]` → 4 elementi invece di 3 |
| 2 | `.append()` restituisce None | Pensava restituisse la lista modificata |
| 3 | enumerate vs range | `range(frutti, len(frutti))` dove serviva `enumerate(frutti, 1)` |
| 4 | Indici liste (contare da 0) | `[1:]` invece di `[2:]` per ottenere [30,40,50] |
| 5 | sorted() nuova lista vs .sort() in-place | Non ha menzionato la differenza chiave |
| 6 | Output concreto vs descrizione | Descrive il concetto invece di dare il valore `["Marco"]` |
| 7 | Variabile corretta nelle comprehension | `x` invece di `n` (la variabile del for) |

---

## 📌 Prossimo Capitolo — Cosa Preparare

> L'agente DEVE leggere questa sezione PRIMA di creare un nuovo capitolo.

| Campo | Valore |
|-------|--------|
| **Prossimo capitolo** | 07_numpy_intro.py (dopo completamento esercizi finali 06) |
| **Rinforzi da inserire (🔁)** | Parsing CSV manuale vs `csv.DictReader` (passi operativi, differenze, quando usare cosa) + output concreto vs spiegazione se ricompare |
| **Concetti ⚠️ da ripassare** | Parsing end-to-end (apertura file -> header -> split -> dict -> append), dict comprehension (1 esercizio), `filter()` ordine parametri |
| **Pattern 🔴 da monitorare** | #5 (tipi nei dizionari/CSV), #6 (lettura consegne), #11 (ordine filter) |
| **Ponte mentale da riusare** | ".items() = enumerate dei dizionari" (ha funzionato al cap.05) |
| **Note** | La difficoltà è salita da 6 a 9 al cap.04. Il cap.05 (in corso) sembra stabilizzarsi. Monitorare attentamente il voto del 05. |

> **Per l'agente**: dopo aver letto queste 4 sezioni (Stato, Ultima Sessione, Priorità Attive, Prossimo Capitolo), hai il 90% del contesto necessario. Prosegui con le Regole Didattiche e il Profilo qui sotto prima di produrre qualsiasi contenuto.

---

## Profilo dello Studente

- **Nome**: Gianluca
- **Background**: Web Developer con esperienza in HTML, CSS, JavaScript, PHP, Laravel. Conoscenza di PHP/Laravel di livello base — i confronti PHP devono essere PARTICOLARMENTE spiegati, non dare per scontato che conosca fgetcsv, trim, explode ecc.
- **Sistema operativo**: Windows 10 (usa Git Bash come terminale in Cursor)
- **Python installato**: 3.14.3
- **IDE**: Cursor
- **Version control**: Git + GitHub (il corso è già in una repository)
- **Obiettivo finale**: Entrare nel mondo del lavoro tech con competenze solide in Python, AI/ML e web development. Il progetto finale deve essere il **diamante del portfolio**: una full web app (React + Laravel + FastAPI) con IA integrata — bella, reattiva, funzionale — da mostrare ai recruiter come prova concreta di competenza.
- **Obiettivo applicativo concreto**: Costruire un'app di **controllo documentale** per la sua società di consulenze. L'app deve verificare l'integrità di buste paga e documenti reddituali (CU, 730) dei clienti: OCR per leggere i documenti, NLP/LLM per estrarre i campi, regole fiscali per validazione incrociata, dashboard con semafori verde/giallo/rosso. Approccio ibrido: regole locali + API con dati anonimizzati o modello locale. Ha già molto materiale documentale a disposizione per il training/RAG. Questo obiettivo può influenzare gli esercizi dei moduli avanzati (M5-M6: usare dominio fiscale/documentale).

---

## Strategia Hardware e Piattaforme

> Questa sezione documenta l'hardware disponibile e le piattaforme alternative per i moduli che richiedono GPU.
> L'agente DEVE consultarla prima di preparare capitoli dei moduli avanzati.

### Hardware disponibile

| Componente | Dettaglio |
|------------|-----------|
| **GPU** | AMD Radeon Vega 10 Mobile (integrata, NO CUDA, NO VRAM dedicata) |
| **Supporto CUDA** | Nessuno — PyTorch/TensorFlow GPU non funzionano in locale |
| **Ollama** | Funziona su CPU — limitato a modelli fino a ~3B parametri (es. Phi-3 Mini, Qwen2 0.5B/1.5B) |
| **RAM** | Da verificare — Docker Desktop richiede almeno 8GB liberi |
| **OS** | Windows 10 con Git Bash |

### Piattaforma per modulo

| Modulo | Richiede GPU? | Piattaforma | Note |
|--------|---------------|-------------|------|
| M1 — Python & Dati | No | CPU locale | Tutto funziona in locale |
| M2 — ML | No | CPU locale | Scikit-Learn funziona su CPU |
| Ponte Matematico | No | CPU locale | Solo NumPy + Matplotlib |
| M3 — DL & CV | **Sì** | **Google Colab** (GPU gratuita) | Training PyTorch su CPU è 10-50x più lento — usare Colab |
| M4 — NLP & Embeddings | Parziale | CPU locale + Colab per modelli grandi | sentence-transformers funziona su CPU per modelli piccoli |
| M5 — LLM & Prompt Eng. | No | CPU locale + API | Ollama (CPU, modelli ≤3B) + API OpenAI per il resto |
| M6 — RAG | No | CPU locale + API | ChromaDB locale, LLM via API/Ollama |
| M7 — AI Agents | No | CPU locale + API | Come M5-M6 |
| M8 — Fine-Tuning | **Sì** | **Google Colab** (GPU gratuita) | QLoRA richiede GPU — impossibile in locale |
| M9 — MLOps & Docker | Parziale | CPU locale | Docker Desktop su Windows richiede WSL2 + RAM sufficiente |
| M10 — Progetto Finale | Parziale | CPU locale + Colab + Cloud | Deploy su cloud, training su Colab |

### Regole per l'agente

1. **Prima di ogni modulo che richiede GPU** (M3, M8): preparare un notebook Google Colab con le dipendenze pre-installate e le istruzioni per connettere il runtime GPU
2. **Ollama**: usare SOLO modelli fino a ~3B parametri (Phi-3 Mini, Qwen2 0.5B/1.5B). Modelli più grandi saranno troppo lenti su CPU
3. **Google Colab**: per M3 e M8, il workflow è: sviluppare il codice in locale (Cursor) → copiare nel notebook Colab per il training → riportare i risultati in locale
4. **Kaggle Notebooks**: backup se Google Colab non è disponibile (stesse GPU gratuite)
5. **Esercizi adattati**: quando un esercizio richiede training su GPU, dare SEMPRE un'alternativa CPU-friendly (modello più piccolo, dataset ridotto, meno epoch) per chi non può/vuole usare Colab

---

## Budget API — Monitoraggio Costi

> Budget totale disponibile: **30-50 EUR** per tutto il corso.
> L'agente DEVE monitorare i costi e dare SEMPRE l'alternativa gratuita (Ollama) dove possibile.

### Allocazione stimata per modulo

| Modulo | Costo stimato | Cosa costa | Strategia risparmio |
|--------|---------------|-----------|---------------------|
| M1-M4 | **0 EUR** | Niente — tutto locale/gratuito | — |
| M5 — LLM | ~8-12 EUR | API OpenAI (chat completions, vision) | Ollama per sviluppo/test, API solo per demo finale e esercizi che richiedono GPT-4 |
| M6 — RAG | ~3-5 EUR | Embedding API + RAG queries | Embedding locali con sentence-transformers (gratuito), API solo per generazione |
| M7 — Agents | ~8-12 EUR | Agent loops (molte chiamate API) | Ollama per loop di sviluppo, API per demo finale |
| M8 — Fine-Tuning | ~0-5 EUR | Training su Colab (gratuito), eval con API | Training su Colab gratis, eval con Ollama dove possibile |
| M9-M10 | ~5-10 EUR | Deploy demo, testing finale | Semantic caching per ridurre chiamate ripetute |
| **Riserva** | ~5-10 EUR | Imprevisti | — |

### Tracker costi (aggiornato dal mentor)

| Modulo | Speso | Residuo | Note |
|--------|-------|---------|------|
| M1 | 0 EUR | 30-50 EUR | — |
| M2 | — | — | — |
| M3 | — | — | — |
| M4 | — | — | — |
| M5 | — | — | — |
| M6 | — | — | — |
| M7 | — | — | — |
| M8 | — | — | — |
| M9 | — | — | — |
| M10 | — | — | — |

### Regole di gestione costi

1. **Ollama-first**: per ogni esercizio dei M5-M7, PRIMA provare con Ollama (gratuito), poi API a pagamento solo quando serve qualità superiore o funzionalità non disponibili localmente (vision, function calling avanzato)
2. **Monitoraggio**: dopo ogni sessione che usa API a pagamento, aggiornare il tracker e segnalare se si sta superando il budget allocato per quel modulo
3. **Skill professionale**: il monitoraggio costi è una competenza AI Engineer — insegnarlo come skill, non solo come vincolo economico
4. **Semantic caching**: dal M5 in poi, quando si ripete una query già fatta, NON richiamare l'API — usare la risposta precedente

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
4. **Confronto a tre lingue**: ogni spiegazione deve includere PHP + JavaScript + Python. Il confronto PHP deve essere PARTICOLARMENTE dettagliato perché Gianluca ha una conoscenza base di PHP — spiegare cosa fanno fopen, fgetcsv, explode, trim ecc. come se fosse un ripasso, non darli per scontati
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
21. **Matematica tradotta in codice**: i concetti matematici NON vanno evitati — vanno tradotti. Ogni formula o concetto matematico deve essere accompagnato da: (a) **analogia concreta** (es. "il gradiente è la pendenza della collina"), (b) **codice Python equivalente** che mostra l'operazione passo passo, (c) **visualizzazione Matplotlib** dove possibile (grafico, frecce, superfici). La formula simbolica arriva ULTIMA, solo come "etichetta" di ciò che il codice fa. Sequenza obbligatoria: analogia → codice → grafico → formula. Il "Ponte Matematico" (2 capitoli tra M2 e M3) introduce i 5-6 concetti fondamentali; nei moduli successivi, ogni nuovo concetto matematico segue la stessa sequenza.
22. **Esercizi di debug autonomo**: dal Modulo 2 in poi, ogni capitolo deve contenere almeno 1 esercizio etichettato `# 🔍 [DEBUG]` dove Gianluca riceve codice che produce un errore reale (con stack trace completo) e deve trovare il bug da solo. Il mentor **NON usa la scala progressiva** per questi esercizi — interviene SOLO dopo 2+ tentativi falliti. Il codice buggato deve contenere errori realistici (off-by-one, tipo sbagliato, variabile non definita, logica invertita, import mancante). L'obiettivo è costruire il "muscolo del debug" — la skill #1 che separa un junior produttivo da uno che chiede aiuto ogni 10 minuti.
23. **Esercizi real-world**: dal Modulo 5 in poi, almeno 1 esercizio per modulo etichettato `# 🌊 [REAL-WORLD]` con consegne deliberatamente vaghe, dati sporchi (encoding misto, colonne mancanti, duplicati, valori anomali), e nessuna soluzione unica. Il mentor valuta l'**approccio e il ragionamento**, non il risultato esatto. Questi esercizi preparano al divario tra esercizi puliti e il caos dei progetti reali. Esempio: "Ecco un CSV di 5000 recensioni con encoding misto e duplicati. Costruisci qualcosa di utile."
24. **Strategia costi API**: per ogni esercizio dei Moduli M5-M7 che usa LLM, dare SEMPRE l'opzione Ollama come fallback gratuito. Prima sviluppare e testare con Ollama (modelli locali, gratis), poi passare ad API a pagamento solo quando serve qualità superiore. Insegnare il monitoraggio costi come skill professionale: dopo ogni sessione con API, aggiornare il tracker nella sezione "Budget API". Budget totale: 30-50 EUR.
25. **Concetti durevoli prima, framework dopo**: per ogni modulo avanzato, prima costruire la soluzione "a mano" (puro Python + libreria minima), poi riscriverla con il framework. Esempio: nel M6, prima un RAG completo con puro Python + ChromaDB, poi la versione con LangChain. Nel M7, prima un agente con puro Python, poi con LangGraph. Così i concetti (che durano 10+ anni) si separano dai framework (che cambiano ogni 6 mesi). Se LangChain cambia API, i concetti restano solidi.
26. **Recall cross-modulo**: il primo capitolo di ogni nuovo modulo (dal M3 in poi) deve contenere almeno 1 esercizio etichettato `# 🔄 [RECALL CROSS-MODULO]` che richiede di usare competenze di un modulo precedente nel nuovo contesto. Questo colma il gap di retention tra moduli distanti. Esempi: al M5, riscrivere un endpoint FastAPI dal M1 prima di costruire l'API LLM. Al M6, ripulire un CSV con Pandas come si faceva al M1. Al M9, riscrivere un modello Scikit-Learn dal M2 prima di containerizzarlo.
27. **Mock interview mensili**: dal Modulo 4 in poi, 1 volta al mese l'AI simula un colloquio tecnico reale. 3 domande, 15 minuti ciascuna, nessun hint, valutazione severa (passeresti / borderline / non passeresti). È l'unico momento in cui l'AI abbandona il tono supportivo. I risultati sono tracciati nella sezione "Mock Interview" di questo file.
28. **Split file per moduli avanzati**: dal Modulo 2 in poi, se un capitolo supera le ~400 righe, splittare in due file: `XXa_teoria.py` (spiegazione + mini-esercizi) e `XXb_pratica.py` (quiz verifica + esercizi + progetto incrementale + soluzioni). Il quiz d'ingresso resta nel file `a`. Per i moduli M3-M4 dove la visualizzazione inline aiuta (output di training, grafici loss, immagini), valutare l'uso di **Jupyter Notebook** (`.ipynb`) al posto dei file `.py`. La scelta va fatta capitolo per capitolo in base al contenuto.
29. **Diversificazione dominio**: dal Modulo 5 in poi, almeno 1 esercizio per modulo usa un dominio diverso dall'e-commerce. Il progetto incrementale resta nel dominio e-commerce (per coerenza e riduzione del carico cognitivo), ma gli esercizi singoli ampliano il contesto per preparare ai colloqui dove il dominio può essere qualsiasi. Domini alternativi suggeriti: documenti legali (M6 — RAG), ticket di supporto tecnico (M7 — Agents), dati medici/sanitari (M5 — LLM), logistica/supply chain (M8), analisi finanziaria (M9).

---

## Progresso del Corso

### Modulo 1 — Python & Dati

| File | Stato | Data | Difficoltà (1-10) | Note |
|------|-------|------|--------------------|------|
| 01_benvenuto_python.py | ✅ Completato + Corretto | 17/02/2026 | 2 | Buon primo approccio. Errori tipici da JS: ternario con `?:`, nomi variabili in inglese misto. Ha capito f-string, tipi, casting. |
| 02_condizioni_e_cicli.py | ✅ Completato + Corretto | 17/02/2026 | 4 | FizzBuzz: `range(1,20)` invece di `range(1,21)`. Password: `elif` dove servivano due `if`, `== True` ridondante. Scacchiera perfetta. Temperature incompleto (mancava la media). |
| 03_funzioni.py | ✅ Completato + Corretto | 17/02/2026 | 6 | Ha capito *args, return multipli, sorted. **Lambda ancora poco chiare** — da rinforzare nei prossimi capitoli. Errori: lista vs parametri separati a *args, count come stringa, mancava `reverse=True`, mancava parametro `decimali`. Tutti corretti. |
| 04_liste.py | ✅ Completato + Corretto | 19/02/2026 | 9 | Difficoltà alta. Ha capito slicing, list comprehension, sorted/filter/map con lambda. **Punti deboli**: enumerate+tuple non interiorizzati (molte domande), range a 3 parametri nuovo, consegne non lette completamente (ex.1 indice sbagliato, ex.2 formato incompleto, ex.3 senza funzione, ex.6 usa [::-1] vietato, ex.9 indice errato). Lambda usate correttamente in ex.4/5/7 — miglioramento reale. |
| 05_dizionari.py | ✅ Completato + Corretto | 17/02/2026 | 8 | Quiz ingresso 1/8 corretto (slicing, .append None, enumerate vs range persistono). Quiz verifica 4/8 (len con aggiunta chiavi, >= vs >, .get vs .items). Dict comprehension usata correttamente nell'ex.3 (miglioramento dai mini-ex). Lambda consolidate. Contatore città + max() con lambda padroneggiati. Consegne incomplete persistono (ex.1 manca voto, ex.2 manca punto a, ex.5 manca reverse, ex.6 mancano b/c, ex.7 append parziale, ex.8 manca prodotto_più_venduto). Esercizio 4 (colloquio conta_parole) risolto perfettamente al primo tentativo. |
| 06_file_csv.py | 🟡 In corso avanzato | 24/02/2026 | n.d. | Teoria completata, quiz verifica completato (7/8 pienamente corretti, 1 parziale). Esercizi finali in corso con nuovo formato consegne esplicite. |
| 07_numpy_intro.py | ⬜ Da fare | | | Da arricchire prima che ci arrivi |
| 08_tensori_spiegati.py | ⬜ Da fare | | | Da arricchire prima che ci arrivi |
| 09_pandas_intro.py | ⬜ Da fare | | | |
| 10_pandas_progetto.py | ⬜ Da fare | | | |
| 11_matplotlib_grafici.py | ⬜ Da fare | | | |
| 12_web_bridge.py | ⬜ Da fare | | | |

### Moduli Successivi

| Modulo | Focus | Librerie principali | Stato |
|--------|-------|---------------------|-------|
| 2 — Machine Learning Fundamentals | ML classico, Scikit-Learn, metriche, overfitting, Streamlit | scikit-learn, streamlit | ⬜ Da creare |
| **Ponte Matematico** (bridge M2→M3) | Vettori, matrici, dot product, coseno, gradiente, discesa — tutto in codice + Matplotlib | numpy, matplotlib | ⬜ Da creare |
| 3 — Deep Learning & Computer Vision | Reti neurali, PyTorch, CNN, transfer learning, Gradio | torch, torchvision, gradio | ⬜ Da creare |
| 4 — NLP, Embeddings & Transformers | Tokenizzazione, embeddings, Transformer, HuggingFace, sentence-transformers | transformers, sentence-transformers | ⬜ Da creare |
| 5 — LLM Integration & Prompt Engineering | API OpenAI, prompt engineering, structured output, function calling, Pydantic, Ollama, multimodale, sicurezza AI | openai, pydantic-ai, ollama | ⬜ Da creare |
| 6 — RAG Systems | ChromaDB, LangChain, chunking, hybrid search, RAGAS evaluation, LangSmith observability | langchain, chromadb, ragas, langsmith | ⬜ Da creare |
| 7 — AI Agents & Automation | LangGraph, tool use, multi-agent, MCP server custom, agentic RAG | langgraph, crewai | ⬜ Da creare |
| 8 — Fine-Tuning & Personalizzazione | LoRA, QLoRA, PEFT, dataset preparation, valutazione modello | peft, bitsandbytes, trl | ⬜ Da creare |
| 9 — MLOps, Testing, Docker & Deploy | Async Python, Docker, testing AI, CI/CD, deploy cloud, semantic caching | docker, redis, pytest | ⬜ Da creare |
| 10 — Progetto Finale: Full-Stack AI Product | React + FastAPI + RAG + Agent + Docker + Deploy live | Tutto il corso | ⬜ Da creare |

#### Portfolio — Demo deployate per modulo

> Ogni modulo produce un progetto deployabile. Alla fine del corso avrai 8 demo live nel portfolio.

| # | Progetto | Modulo | Piattaforma deploy | Cosa dimostra |
|---|----------|--------|---------------------|---------------|
| 1 | Predittore prezzo case | M2 | Streamlit Cloud | ML classico, data analysis, Streamlit |
| 2 | Classificatore immagini | M3 | HuggingFace Spaces | Deep Learning, transfer learning, Gradio |
| 3 | Analizzatore recensioni e-commerce | M4 | Streamlit Cloud | NLP, embeddings, sentiment analysis |
| 4 | Assistente e-commerce AI | M5 | Streamlit Cloud | LLM API, function calling, streaming |
| 5 | RAG documentale | M6 | Streamlit Cloud | RAG, vector DB, evaluation |
| 6 | Agente di ricerca e analisi | M7 | Streamlit Cloud | AI agents, tool use, LangGraph |
| 7 | Demo fine-tuning comparativa | M8 | HuggingFace Spaces | Fine-tuning, LoRA, comparazione base vs fine-tunato |
| 8 | Prodotto full-stack AI (diamante portfolio) | M10 | Cloud (Railway/Render) | Full-stack: React + FastAPI + RAG + Agent + Docker |

#### Evoluzione del Progetto Incrementale "Catalogo E-commerce"

> Il progetto incrementale evolve naturalmente attraverso i moduli, diventando progressivamente il progetto finale.

| Fase | Moduli | Il progetto diventa... |
|------|--------|-----------------------|
| **Data Tool** | M1-M2 | Catalogo prodotti con analisi dati, statistiche, previsioni prezzi |
| **Smart Tool** | M3-M4 | + classificazione immagini prodotto, analisi sentiment recensioni |
| **AI-Powered** | M5-M6 | + chatbot AI sul catalogo (RAG), ricerca semantica prodotti, function calling |
| **Autonomous** | M7-M8 | + agente che gestisce ordini/inventario, modello personalizzato per generazione descrizioni |
| **Production** | M9-M10 | + containerizzato, deployato, testato, monitorato, con CI/CD — il diamante del portfolio |

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
| 05_dizionari | 8 | -1 ↓ (buon segno: la curva si stabilizza dopo il picco) |

**Media attuale**: 5.8 (media di 2, 4, 6, 9, 8). Il calo da 9 a 8 è positivo: il picco al cap.04 era dovuto all'accumulo di concetti nuovi (enumerate, tuple, lambda). Al cap.05 questi concetti si sono consolidati — lambda quasi acquisita, enumerate+.items() padroneggiato. Il problema principale resta la lettura incompleta delle consegne, non la comprensione tecnica.

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
| `lambda` | Mini-funzione usa-e-getta, una riga sola — migliorata significativamente al cap.05 | `() =>` / `fn() =>` | 03 | 2/3 | 🔄 |
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
| tupla / unpacking | Coppia di valori `(i, val)` — si spacchetta con `a, b = tupla` — migliorato al cap.05 | Destructuring `[a, b] = arr` / `list($a, $b) = $arr` | 04 | 1/3 | ⚠️ |

### Dizionari e Metodi (File 05)

| Termine | Significato sintetico | Equivalente JS/PHP | Cap. | Ripassi | Stato |
|---------|-----------------------|--------------------|------|---------|-------|
| dizionario `{}` | Struttura chiave-valore — come un oggetto JS o array associativo PHP | `{}` oggetto / `[]` array associativo | 05 | 0/3 | 🔄 |
| `.keys()` | Restituisce tutte le chiavi del dizionario | `Object.keys()` / `array_keys()` | 05 | 0/3 | 🔄 |
| `.values()` | Restituisce tutti i valori del dizionario | `Object.values()` / `array_values()` | 05 | 0/3 | 🔄 |
| `.items()` | Restituisce tuple `(chiave, valore)` — l'`enumerate()` dei dizionari! | `Object.entries()` / `foreach($arr as $k => $v)` | 05 | 0/3 | 🔄 |
| `.get(chiave, default)` | Accede a una chiave con valore di default se non esiste — evita errori | `obj?.key ?? default` / `$arr['key'] ?? default` | 05 | 0/3 | 🔄 |
| `.setdefault(k, v)` | Aggiunge la chiave solo se non esiste, altrimenti restituisce il valore corrente | Non diretto / Non diretto | 05 | 0/3 | 🔄 |
| `.update(dict2)` | Unisce un altro dizionario dentro il primo (modifica in-place) | `Object.assign()` / `array_merge()` | 05 | 0/3 | 🔄 |
| `.copy()` | Crea una copia superficiale del dizionario (modifiche alla copia non toccano l'originale) | `{...obj}` spread / Non diretto (`array_merge()` crea nuovo) | 05 | 0/3 | 🔄 |
| `zip()` | Accoppia elementi di due liste come una "cerniera" → lista di tuple | Non diretto / Non diretto | 05 | 0/3 | 🔄 |
| `**dizionario` | Spread operator per dizionari — spacchetta le coppie chiave-valore | `...obj` / `...` + `array_merge()` | 05 | 0/3 | 🔄 |
| dict comprehension | `{k: v for k, v in ...}` — crea dizionari in modo compatto — ⚠️ **DA RINFORZARE** | Non diretto / Non diretto | 05 | 0/3 | ⚠️ |
| `in` (su dizionari) | Verifica se una CHIAVE esiste nel dizionario (non i valori!) | `"key" in obj` / `array_key_exists()` | 05 | 0/3 | 🔄 |

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

### Capitolo 05 — dizionari (mini-esercizi, teoria in corso)
- "Il metodo zip cosa restituisce?" → Non conosceva zip(), spiegato come "cerniera" che accoppia due liste
- "prezzi.items() cosa restituisce? Lo stesso metodo poteva essere usato nelle liste?" → Distinzione liste vs dizionari non ancora ovvia. Ha portato al ponte mentale ".items() = enumerate dei dizionari"
- ".items() è il corrispettivo di enumerate per i dictionary?" → **Ponte mentale confermato**: ha capito l'analogia e chiesto di registrarla
- "Il metodo append funziona per le dictionary?" → Confusione sui metodi specifici di liste vs dizionari
- "Metodo per inserire un elemento alla fine di una lista" → Cercava `.append()` — lo conosce ma non lo ricorda al volo
- "Operatore ternario in Python" → Chiesto 2 volte — la sintassi `valore if condizione else altro` non è intuitiva venendo da `? :` in JS/PHP
- "**p rispiegami questa sintassi" → Il doppio asterisco `**` per spread dei dizionari non era chiaro
- "Come inserire chiave e valore in una lista python?" → Confusione tra lista e dizionario — ha capito che le liste non hanno chiavi
- Errore di sintassi su filter(): `filter(studenti, lambda s: ...)` — ordine parametri invertito, confonde con sorted(lista, key=lambda)
- Errore f-string: doppi apici dentro doppi apici `f"{s["nome"]}"` → errore già visto al cap.03
- Errore negazione: `if (!(n in lista))` → sintassi JS, in Python è `if n not in lista`

---

## Pattern di Errore Ricorrenti

Questi sono gli errori che Gianluca tende a ripetere. Da monitorare nei prossimi esercizi:

| # | Pattern | Stato | Note |
|---|---------|-------|------|
| 1 | **Sintassi JS in Python**: usa `? :` invece di `if...else` ternario | 🔴 Attivo | Visto al file 01 |
| 2 | **`range()` / slicing fine escluso**: dimentica che il secondo numero è escluso | 🔴 Attivo | Visto al file 02. Ripetuto al file 04: `dati[17:]` invece di `dati[16:]` |
| 3 | **`== True` ridondante**: scrive `if valore == True` | 🟡 Corretto una volta | Visto al file 02, corretto dopo feedback |
| 4 | **Calcoli dentro le f-string**: espressioni troppo lunghe nelle `{}` | 🟡 Corretto una volta | Visto al file 01, corretto dopo feedback |
| 5 | **Tipi nei dizionari**: mette stringhe dove servono numeri | 🔴 Attivo | Visto al file 03 (`count` come stringa). **Ripetuto al file 05** mini-ex.2: `auto['km'] = "10000"` (stringa invece di numero) |
| 6 | **Lettura incompleta delle consegne**: non implementa tutti i requisiti | 🔴 Attivo | Visto ai file 02, 03, 04, **05**. Al file 05: mini-ex.4 (2 piatti invece di 3, mancano i print), mini-ex.6 (manca punto 3 max), mini-ex.7 (manca modifica lingua nella copia) |
| 7 | **Lambda poco chiare**: non ha ancora interiorizzato la sintassi e l'uso delle funzioni lambda | 🟡 → quasi 🟢 | Al file 05: usate correttamente in ex.2 (max), ex.3 (sorted), ex.5 (sorted/filter/min/map), ex.7 (contatore), ex.8 (max .items()). Glossario 2/3. Ordine parametri filter corretto. **Quasi acquisita** |
| 8 | **enumerate/tuple/unpacking**: non capisce che enumerate crea tuple e che l'unpacking le spacchetta | 🟡 In miglioramento | **Miglioramento significativo al file 05**: mini-ex.3 usato correttamente `for i, (key, value) in enumerate(.items(), 1)`. Ponte mentale ".items() = enumerate dei dizionari" ha fatto click |
| 9 | **Codice superfluo**: aggiunge espressioni inutili (`== l` dopo `.insert()`) | 🟡 Corretto una volta | Visto al file 04 ex.6 |
| 10 | **Vincoli esercizio ignorati**: usa metodi vietati dalla consegna (es. `[::-1]` quando esplicitamente proibito) | 🔴 Attivo | Visto al file 04 ex.6. Collegato al pattern #6 (lettura consegne) |
| 11 | **Ordine parametri filter()**: mette la lista prima della lambda (`filter(lista, lambda)` invece di `filter(lambda, lista)`) | 🔴 Attivo | Visto al file 05 durante le domande. Confonde con sorted() che ha `key=lambda` come parametro con nome |
| 12 | **Variabile sbagliata nel contesto**: usa una variabile di un altro scope/esempio | 🟡 Visto una volta | Al file 05 mini-ex.7: `'tema' in config` invece di `'tema' in preferenze` |
| 13 | **Dict comprehension evitata**: quando la consegna chiede dict comprehension, usa il ciclo for classico | 🟡 In miglioramento | Mini-ex.5: usato for classico. Ma ex.3a: usata correttamente! Miglioramento parziale |
| 14 | **return print(...)**: usa return con print, che restituisce sempre None | 🟡 Visto più volte | Al file 05 ex.2: tutte le funzioni hanno `return print(...)`. Il print funziona ma il return è inutile |
| 15 | **Parametro funzione ignorato**: la funzione accetta un parametro ma dentro usa la variabile globale | 🟡 Visto una volta | Al file 05 ex.1: `def stampa(dizionario)` ma dentro usa `film.items()` invece di `dizionario.items()` |
| 16 | **Docstring mancante quando richiesta**: la consegna chiede "la funzione deve avere una docstring" e non la scrive | 🔴 Attivo | Al file 05 ex.4 e ex.8. Collegato al pattern #6 (lettura consegne) |

Legenda: 🔴 Attivo (si ripete) | 🟡 Visto e corretto (da monitorare) | 🟢 Superato

---

## Punti di Forza

1. **Capisce velocemente le analogie** PHP/JS → Python
2. **Corregge subito** dopo il feedback — non ripete lo stesso errore due volte
3. **Chiede chiarimenti** quando non capisce (enumerate, *args, reduce)
4. **Sa già ragionare in termini di funzioni, parametri, return** — il background Laravel si sente
5. **Motivato e orientato al risultato** — vuole capire il perché, non solo il come
6. **Verifica proattivamente** — controlla formule e logica prima di fidarsi
7. **Sa creare funzioni riutilizzabili** — nell'ex.1 del cap.05 ha creato spontaneamente una funzione stampa() invece di ripetere il codice
8. **Pattern contatore padroneggiato** — .get(chiave, 0) + 1 e not in + inizializzazione usati correttamente

---

## Ritmo di Studio

- **Sessione 1 (17/02/2026)**: File 01, 02, 03 completati in una sessione
- **Sessione 2 (19/02/2026)**: File 04 completato. Difficoltà 9 — il salto maggiore finora. Enumerate/tuple e combinazione di concetti sono stati i punti più difficili
- **Sessione 3 (17/02/2026)**: File 05 in corso. Mini-esercizi teoria completati. Miglioramento significativo su enumerate+.items(). Dict comprehension ancora da interiorizzare
- **Sessione 4 (24/02/2026)**: File 06 in corso avanzato. Rinforzi mirati completati e quiz verifica quasi pieno. Forte miglioramento su `.get()`/`.items()`, sorting con `key`, e gestione path/file. Da consolidare parsing CSV manuale vs `DictReader` e definizione precisa degli output.
- **Ritmo stimato**: 1 file ogni 2 giorni (aggiornato dallo studente)
- **Tempo totale stimato per il corso**: 5-6 mesi (corso) + 2-3 mesi (MVP app documentale)
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
| ".items() = enumerate dei dizionari" | `.items()` restituisce tuple `(chiave, valore)` da spacchettare — stessa meccanica di `enumerate()` che dà `(indice, valore)` | `Object.entries()` in JS / `foreach($arr as $k => $v)` in PHP | 05 | `.iterrows()` su DataFrame Pandas, iterazione su qualsiasi struttura chiave-valore |
| "** = spread per dizionari" | `{**dict1, **dict2}` unisce dizionari | `{...obj1, ...obj2}` in JS / `array_merge()` in PHP | 05 | Merging config, parametri opzionali, kwargs |

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

### Dopo il Capitolo 05 — Dizionari (parziale — mini-esercizi teoria)
- So creare dizionari con `{}` e accedere ai valori con `dizionario["chiave"]`
- So aggiungere/modificare valori: `dizionario["nuova_chiave"] = valore`
- So iterare con `.keys()`, `.values()`, `.items()`
- ✅ So combinare `.items()` + `enumerate()` per avere indice + chiave + valore — **grande miglioramento**
- So usare `.get()` con valore di default per evitare errori su chiavi inesistenti
- So usare `.setdefault()` per aggiungere solo se la chiave non esiste
- So usare `.copy()` per creare copie indipendenti
- So usare `in` per verificare l'esistenza di una chiave
- So ordinare una lista di dizionari con `sorted()` + `lambda` per una chiave specifica
- So filtrare dizionari con `filter()` + `lambda` (⚠️ ordine parametri: prima lambda, poi lista)
- ⚠️ Dict comprehension: conosco il concetto ma tendo ancora a usare il for classico
- ⚠️ Dizionari annidati: so accedervi ma dimentico di implementare tutti i livelli richiesti

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
- [ ] **Ho usato `filter()`?** Il primo parametro è la funzione lambda, il secondo la lista: `filter(lambda x: ..., lista)`. NON al contrario!
- [ ] **La consegna chiede dict comprehension?** Se sì, devo usare `{chiave: valore for ... in ...}`, non un ciclo for con dizionario vuoto
- [ ] **I valori nel dizionario sono del tipo giusto?** Un chilometraggio è un numero `10000`, non una stringa `"10000"`

- [ ] **Ho scritto `return print(...)`?** Se sì, togli il return — print() restituisce None, quindi il return è inutile
- [ ] **Il parametro della funzione è usato?** Se la funzione accetta `dizionario`, dentro uso `dizionario`, non il nome della variabile globale
- [ ] **Ho contato bene `>=` vs `>`?** Se la condizione è `>= 7`, il 7 è INCLUSO. Se è `> 7`, il 7 è ESCLUSO

### Controlli Bonus (buone pratiche)
- [ ] La funzione ha una docstring? (se la consegna la chiede, è OBBLIGATORIA)
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
| enumerate() unpacking | 17/02 | ❌ file 04 (molte domande, non autonomo) | ❌ quiz 05 / ✅ mini-ex.3 cap.05 (usato con .items()!) | file 09 | 🟡 In miglioramento |
| def, return, *args, **kwargs | 17/02 | ✅ file 05 (4 funzioni create: stampa, conta_parole, raggruppa_per, processa_ordini) | file 07 | file 10 | ✅ Consolidato |
| lambda | 17/02 | 🟡 file 04 (usata correttamente in ex.4/5/7 ma con aiuto teoria) | ✅ file 05 ex.2/4/5/7/8 (usata correttamente con sorted, filter, max, min) | file 07 | 🟡 → ✅ quasi acquisita |
| sorted() con key | 17/02 | ✅ file 04 (usato correttamente con lambda) | ⚠️ quiz ingresso 05 (non sa che sorted crea nuova lista, pensa lambda obbligatoria) | file 07 | ⚠️ Uso corretto ma teoria incompleta |
| slicing, list comprehension | 19/02 | file 05 | file 07 | file 10 | Da verificare |
| tuple/unpacking | 19/02 | file 05 ⚠️ | file 07 ⚠️ | file 10 | ⚠️ Rinforzo prioritario |
| filter(), map() | 19/02 | 🟡 file 05 mini-ex.6 (filter+sorted combinati, ma ordine param fragile) | file 07 | file 10 | ⚠️ Ordine parametri filter da rinforzare |
| dict comprehension | 17/02 (cap.05) | ✅ file 05 ex.3a (usata correttamente per filtrare promossi!) | file 08 | file 11 | 🟡 Migliorata — usata nell'ex.3 ma non nell'ex.6c |
| .items() + unpacking | 17/02 (cap.05) | file 06 | file 08 | file 11 | ✅ Usato correttamente al primo tentativo |

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
| 1 | Slicing — fine escluso | Ingresso/05 | `numeri[1:4]` → ha scritto [20,30,40,50] invece di [20,30,40]. Non applica "il secondo numero è escluso" | 06 | 🟡 |
| 2 | .append() restituisce None | Ingresso/05 | Pensava che .append() restituisse la lista modificata (come .push() in JS restituisce la lunghezza). In Python modifica in-place e restituisce None | 06 | 🟡 |
| 3 | enumerate vs range | Ingresso/05 | Ha scritto `range(frutti, len(frutti))` dove serviva `enumerate(frutti, 1)`. Non distingue quando usare enumerate e quando range | 06 | 🟡 |
| 4 | Indici delle liste (contare da 0) | Ingresso/05 | Per ottenere [30,40,50] da [10,20,30,40,50] ha scritto `[1:]` invece di `[2:]`. Sa che 3 era troppo ma non conta da 0 correttamente | 06 | 🟡 |
| 5 | sorted() crea nuova lista vs .sort() in-place | Ingresso/05 | Sa che uno è funzione e l'altro metodo, ma non ha menzionato la differenza chiave: sorted() crea una NUOVA lista, .sort() modifica in-place e restituisce None. Dice anche che lambda è obbligatoria (è opzionale) | 06 | 🟡 |
| 6 | Output concreto vs descrizione concettuale | Ingresso/05 | Alla domanda "cosa stampa" ha descritto il concetto invece di dare il valore concreto `["Marco"]`. Capisce il meccanismo ma non sa prevedere l'output esatto | 06 | 🟡 |
| 7 | Variabile corretta nelle comprehension | Ingresso/05 | Ha scritto `x % 2 == 0` quando la variabile del for era `n`. Causerebbe NameError. Disattenzione sui nomi delle variabili nel contesto della comprehension | 06 | 🟡 |
| 8 | len() con aggiunta chiavi al dizionario | Verifica/05 | Ha scritto 2 invece di 3. Non ha contato che `persona["citta"] = "Roma"` aggiunge una NUOVA chiave (da 2 a 3) | 06 | 🟡 |
| 9 | >= vs > (include o esclude il valore limite) | Verifica/05 | Dict comprehension `if v >= 7`: ha escluso Marco (voto 7) dalla risposta. Non distingue >= (include) da > (esclude) | 06 | 🟡 |
| 10 | .get() vs .items() — metodi diversi | Verifica/05 | Per contare frequenze ha scritto `.items(lettera, totale)` invece di `.get(lettera, 0)`. Confonde .items() (tutte le coppie) con .get() (una chiave con default) | 06 | 🟡 |
| 11 | Parsing CSV manuale vs spiegazione astratta | Verifica/06 | Alla domanda Feynman ha descritto il concetto in modo generale ma senza sequenza operativa completa (apertura file -> lettura righe -> header -> split -> dizionario -> append). Richiesto rinforzo esplicito su "come" e non solo "cos'e". | 07 | 🔴 |

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
| Conta frequenze parole | 05 | Junior/Mid — classico | Dizionari, `.get()` per contare, `.lower().split()`, iterazione | ✅ Risolto perfettamente al primo tentativo |
| Raggruppare per chiave (GROUP BY) | 05 | Mid — data manipulation | `not in` + lista vuota + `.append()`, funzione generica con parametro chiave | ✅ Risolto (append parziale: solo nome invece di dizionario intero) |

### Cosa aspettarsi nei prossimi capitoli e moduli

| Capitolo/Modulo | Esercizi colloquio previsti |
|------------------|-----------------------------|
| 05 — Dizionari | Contare frequenze di parole, raggruppare dati per chiave, merge di due dizionari, anagrammi |
| 06 — File CSV | Parsing manuale di CSV, trovare anomalie nei dati, aggregazioni per gruppo |
| 07 — NumPy | Normalizzazione di un array, distanza euclidea, operazioni su matrici |
| 09 — Pandas | Pulizia dati con valori mancanti, group by + aggregazione, pivot table |
| M2 — ML | Train/test split manuale, calcolo accuratezza, feature scaling, "spiega overfitting" |
| M3 — DL & CV | Spiegare backpropagation a parole, costruire un modello semplice, leggere una loss curve |
| M4 — NLP | "Cos'è un embedding?", "Come funziona un Transformer?", similarità coseno a mano |
| M5 — LLM | "Progetta un chatbot con function calling", prompt engineering sotto pressione, "cos'è il prompt injection?" |
| M6 — RAG | "Progetta un RAG per 10M documenti", "che chunking strategy useresti?", "come valuti la qualità del RAG?" |
| M7 — Agents | "Progetta un agente che gestisce ordini", "quando workflow vs agente?", "cos'è il MCP?" |
| M8 — Fine-Tuning | "Quando fine-tuning vs RAG vs prompt engineering?", "cos'è LoRA e perché funziona?" |
| M9 — MLOps | "Come deployeresti un servizio LLM?", "come gestisci i costi?", "come testi un'app AI?" |

### Domini alternativi per esercizi (dal M5 in poi)

> Almeno 1 esercizio per modulo esce dal dominio e-commerce per ampliare il contesto.

| Modulo | Dominio alternativo | Esempio esercizio |
|--------|---------------------|-------------------|
| M5 — LLM | Dati sanitari | Chatbot che risponde a domande su sintomi/farmaci da un dataset medico |
| M6 — RAG | Documenti legali | RAG su contratti e normative: chunking di testi lunghi, ricerca per clausola |
| M7 — Agents | Ticket supporto tecnico | Agente che classifica, prioritizza e assegna ticket di supporto IT |
| M8 — Fine-Tuning | Logistica/supply chain | Fine-tuning per generare descrizioni di spedizioni nel tono dell'azienda |
| M9 — MLOps | Analisi finanziaria | Deploy di un servizio che analizza report trimestrali |
| M10 — Finale | A scelta dello studente | Il progetto finale resta e-commerce, ma il mock interview può usare qualsiasi dominio |

### Come ripassarli

1. Una volta a settimana, scegli 2-3 esercizi dalla lista "Già incontrati"
2. Riscrivili da zero su un file vuoto, senza guardare la soluzione
3. Cronometrati: un junior ha circa 15-20 minuti per esercizio in un colloquio
4. Se non riesci entro il tempo, ristudia il capitolo e riprova dopo 2 giorni

---

## Mock Interview — Validazione Esterna

> Dal Modulo 4 in poi, 1 volta al mese (a metà o fine modulo), l'AI simula un colloquio tecnico reale.
> Questo è l'UNICO momento in cui l'AI abbandona il tono supportivo e diventa un intervistatore freddo.
> L'obiettivo è calibrare la preparazione reale e prevenire il "senso di competenza inflato".

### Formato

1. **3 domande** da colloquio reale (mix di coding, teoria, system design dove applicabile)
2. **Timer**: 15 minuti per domanda (Gianluca si cronometra)
3. **Nessun hint**: il mentor NON usa la scala progressiva — simula un intervistatore che aspetta la risposta
4. **Valutazione severa**: voto secco per ogni domanda
   - **Passeresti** — risposta corretta, completa, nei tempi
   - **Borderline** — risposta parziale o con errori minori
   - **Non passeresti** — risposta sbagliata, incompleta, o fuori tempo
5. **Feedback finale**: dopo le 3 domande, il mentor torna al tono normale e spiega dove migliorare

### Risultati Mock Interview

| # | Data | Modulo | D1 | D2 | D3 | Esito globale | Note |
|---|------|--------|----|----|----|---------------|------|
| 1 | — | M4 | — | — | — | — | — |
| 2 | — | M5 | — | — | — | — | — |
| 3 | — | M6 | — | — | — | — | — |
| 4 | — | M7 | — | — | — | — | — |
| 5 | — | M8 | — | — | — | — | — |
| 6 | — | M9 | — | — | — | — | — |
| 7 | — | M10 | — | — | — | — | — |

### Quando attivare

- L'agente propone il mock interview quando Gianluca è a metà o fine di un modulo (dal M4 in poi)
- Gianluca può anche chiedere "facciamo un mock interview" in qualsiasi momento
- Le domande devono coprire il modulo corrente + 1-2 concetti dei moduli precedenti

---

## Progetto Incrementale — "Catalogo E-commerce"

> Un progetto unico che cresce capitolo dopo capitolo e attraversa **tutto il corso** (10 moduli).
> Ogni capitolo aggiunge una funzionalità usando i concetti appena appresi.
> Alla fine del corso, Gianluca avrà costruito un **prodotto AI completo e deployato** —
> il diamante del portfolio.
>
> Il progetto è pensato per il dominio che Gianluca padroneggia (e-commerce/web), così il contesto
> non aggiunge carico cognitivo e può concentrarsi sulla tecnica.

### Tema del progetto

**"Catalogo E-commerce"** — Un sistema che parte come semplice lista di prodotti e cresce fino a diventare un prodotto AI full-stack con RAG, agenti, modello personalizzato, e deploy su cloud.

### Roadmap per capitolo — Modulo 1 (Python & Dati)

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

### Roadmap per modulo — Moduli 2-10

| Modulo | Funzionalità da aggiungere al Catalogo | Concetti esercitati |
|--------|-----------------------------------------|---------------------|
| M2 — ML | Predittore prezzi prodotti basato su caratteristiche (categoria, brand, stagione) + prima demo Streamlit | Scikit-Learn, train/test, metriche, Streamlit |
| M3 — DL & CV | Classificatore immagini prodotto (es. categoria da foto) con transfer learning + demo Gradio | PyTorch, CNN, transfer learning, Gradio |
| M4 — NLP | Analisi sentiment recensioni clienti + ricerca semantica prodotti per significato | Embeddings, sentence-transformers, similarità coseno |
| M5 — LLM | Chatbot AI del catalogo: risponde a domande sui prodotti, usa function calling per cercare/filtrare/calcolare | OpenAI API, prompt engineering, structured output, function calling |
| M6 — RAG | Knowledge base del catalogo: carica documentazione/FAQ e risponde con contesto reale, non allucinato | ChromaDB, LangChain, chunking, RAGAS evaluation |
| M7 — Agents | Agente autonomo che gestisce ordini, controlla inventario, suggerisce riordini, genera report | LangGraph, tool use, agentic RAG, MCP |
| M8 — Fine-Tuning | Modello personalizzato per generare descrizioni prodotto nel "tono" del brand | LoRA, QLoRA, PEFT, dataset curation |
| M9 — MLOps | Tutto containerizzato e deployato: Docker + CI/CD + monitoring + semantic caching | Docker, GitHub Actions, Redis, testing |
| M10 — Finale | Frontend React/Next.js + Backend FastAPI + tutti i servizi AI integrati → deploy live | Full-stack, architettura microservizi, deploy cloud |

### Progresso del progetto

| Capitolo/Modulo | Stato | Note |
|-----------------|-------|------|
| 04 — Liste | ⬜ Non ancora assegnato (il cap. 04 era già completato prima dell'introduzione del progetto) | |
| 05 — Dizionari | ⬜ Da fare | Prima volta con il progetto incrementale |
| 06 — File CSV | ⬜ Da fare | |
| 07 — NumPy | ⬜ Da fare | |
| 08 — Tensori | ⬜ Da fare | |
| 09 — Pandas | ⬜ Da fare | |
| 10 — Pandas Progetto | ⬜ Da fare | |
| 11 — Matplotlib | ⬜ Da fare | |
| 12 — Web Bridge | ⬜ Da fare | |
| M2 — ML | ⬜ Da fare | |
| M3 — DL & CV | ⬜ Da fare | |
| M4 — NLP | ⬜ Da fare | |
| M5 — LLM | ⬜ Da fare | |
| M6 — RAG | ⬜ Da fare | |
| M7 — Agents | ⬜ Da fare | |
| M8 — Fine-Tuning | ⬜ Da fare | |
| M9 — MLOps | ⬜ Da fare | |
| M10 — Finale | ⬜ Da fare | Il diamante del portfolio |

### Regole per il progetto incrementale

1. La sezione `# 🏗️ PROGETTO INCREMENTALE` va alla fine degli esercizi, prima delle soluzioni
2. Deve richiedere 15-25 minuti (non troppo lungo, non troppo breve)
3. Il task deve usare SOLO concetti visti fino a quel capitolo (niente anticipazioni)
4. Ogni capitolo costruisce sul codice del capitolo precedente — lo studente può copiare e estendere
5. La soluzione va nella sezione SOLUZIONI come gli altri esercizi
6. Se è il primo capitolo con il progetto, fornire il codice base da cui partire
7. Nei moduli avanzati (M2-M10): il progetto incrementale di fine modulo produce una **demo deployabile** (Streamlit, Gradio, o cloud). Il deploy è parte del task.

---

## Note per il Mentor

### Promemoria automatici
- **Dopo ogni capitolo completato**: chiedere il voto di difficoltà (1-10) se non lo dà spontaneamente
- **Dopo ogni capitolo**: aggiornare glossario, domande, pattern di errore, progresso
- **Prima del Modulo 3 (DL & CV)**: preparare un notebook Google Colab con PyTorch + torchvision pre-installati, istruzioni per connettere GPU, e un test rapido per verificare che CUDA funzioni su Colab. Idem per il Modulo 8 (Fine-Tuning) con PEFT + bitsandbytes
- **Prima del file 07**: arricchire con più esempi visivi e mini-esercizi intermedi
- **Prima del file 08**: aggiungere rappresentazioni ASCII di tensori 2D/3D/4D
- **⚠️ A FINE MODULO 1** (completamento file 12_web_bridge.py): creare `ARCHIVIO_MODULO_01.md` e migrare il dettaglio storico del M1:
  - Progresso dettagliato dei 12 capitoli (tabella con date, voti, note)
  - Pattern di errore con stato 🟢 (risolti)
  - Lacune quiz con stato 🟢 (superate)
  - Domande fatte nei capitoli del M1 (storico)
  - Glossario: i termini ✅ (acquisiti con 3/3) vengono COPIATI (non spostati) nell'archivio. Restano anche nel file principale per il ripasso naturale, ma contrassegnati come acquisiti
  - Competenze M1 complete → archiviate come "Cosa Sapevo Fare Dopo il Modulo 1"
  - **Regola**: quando l'agente prepara un capitolo del M2+ e deve fare rinforzo su concetti del M1, DEVE consultare `ARCHIVIO_MODULO_01.md` per il contesto storico completo
  - **Regola**: il file principale CONTESTO_CORSO.md mantiene: sezioni in cima (Stato, Ultima Sessione, Priorità Attive, Prossimo Capitolo), Profilo, Regole Didattiche, Glossario completo, Pattern attivi, Lacune attive, e tutto ciò che è ATTIVO. Obiettivo: mantenerlo sotto le ~800 righe dopo la migrazione
  - Ripetere questo processo a fine di ogni modulo successivo (ARCHIVIO_MODULO_02.md, ecc.)
- **A inizio di ogni nuovo modulo (M2-M10)**: creare la cartella del modulo (`modulo_XX_nome/`) con un `README.md` che segue la struttura del README del Modulo 1
- **Per i moduli M2-M10**: ogni modulo finale produce una demo deployabile. Il Mentor deve guidare il deploy e verificare che il link sia funzionante
- **Al modulo M5**: quando i confronti PHP/JS non hanno equivalente diretto (es. embedding, backpropagation), usare analogie dal mondo web/e-commerce. Registrare i nuovi ponti mentali nella sezione apposita
- **Al modulo M7**: guidare la costruzione di un MCP server custom. Questo è un meta-skill: Gianluca capirà come funziona Cursor stesso
- **Al modulo M9**: il primo deploy live. Verificare che il link funzioni e sia inseribile nel CV
- **Al modulo M10**: guidare la creazione del profilo GitHub professionale (README, pinned repos, link demo)
- **Al modulo M10 — Simulazione team workflow**: il progetto finale simula un flusso di lavoro in team:
  - **Feature branches**: ogni fase del progetto (AI service, backend, frontend, deploy) ha il suo branch
  - **Pull Request con descrizione strutturata**: ogni merge richiede una PR con titolo, descrizione, checklist
  - **Code review dall'AI**: il mentor fa code review come un collega senior — commenti su naming, struttura, edge case, performance. Può richiedere modifiche prima dell'approvazione
  - **Conventional commits**: obbligatori per tutto il M10 (es. `feat:`, `fix:`, `refactor:`, `docs:`, `test:`)
  - Questo prepara al lavoro reale dove si collabora con PR, code review, e branching strategy

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
- **Dal M2 in poi**: ogni modulo produce una demo deployabile (Streamlit o Gradio)
- **Dal M5 in poi**: includere almeno 1 esercizio di **system design** dove Gianluca progetta un'architettura su carta prima di scrivere codice
- **Al M10**: guidare la creazione del profilo GitHub professionale e assicurarsi che almeno 5 demo siano live

### Adattamento didattico per i moduli AI (M2-M10)
- **Confronti PHP/JS/Python**: restano obbligatori dove esiste un equivalente (es. `fetch()` → `requests`, `Array.map()` → `map()`, Eloquent → Pandas)
- **Concetti puramente AI** (embedding, backpropagation, attention, chunking, ecc.): il confronto a tre lingue è sostituito da **analogie dal mondo web/e-commerce** che Gianluca conosce. Esempio:
  - Embedding → "Come le coordinate GPS catturano una posizione, un embedding cattura il significato di un testo"
  - Backpropagation → "Come il GPS ricalcola il percorso dopo una svolta sbagliata"
  - ChromaDB → "Come un database SQL, ma cerca per significato invece che per query esatta"
  - RAG → "Come una ricerca su Google: prima trovi i risultati rilevanti, poi li leggi per rispondere"
  - Docker → "Come `node_modules` ma per l'intero sistema operativo"
  - LoRA → "Invece di ristrutturare tutta la casa, aggiungi solo una stanza"
- Registrare i nuovi ponti mentali nella sezione "Ponti Mentali" quando funzionano
- **Concetti durevoli prima, framework dopo**: in ogni modulo avanzato, la soluzione viene prima costruita "a mano" (puro Python + libreria minima), poi riscritta con il framework. Questo garantisce che i concetti sopravvivano ai cambi di API dei framework
- **Approccio "visualizzazione-prima" per la matematica**: quando un concetto AI richiede una base matematica (gradienti, spazi vettoriali, decomposizione matriciale), seguire sempre la sequenza: analogia concreta → codice Python → grafico Matplotlib → formula (solo come etichetta finale). Mai partire dalla formula. I 2 capitoli del Ponte Matematico (tra M2 e M3) stabiliscono le fondamenta; nei moduli successivi si richiamano e si estendono
- **Esercizi `[SYSTEM DESIGN]`** (dal M5 in poi): nuovo tag per esercizi dove Gianluca progetta un'architettura AI. Formato: scenario reale → requisiti → disegno architettura → discussione trade-off. Non c'è una sola soluzione giusta — l'obiettivo è ragionare sui compromessi

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

### Formato obbligatorio consegne (anti-ambiguita)

Per ogni esercizio dei prossimi capitoli, la consegna deve essere scritta con questa struttura fissa:

1. **Obiettivo in 1 frase**: cosa devo ottenere alla fine (risultato concreto).
2. **Input disponibili**: quali variabili/file posso usare (es. `dati_csv`, `percorso_output`), con i campi realmente presenti.
3. **Output atteso**: cosa deve essere stampato/salvato/restituito (formato preciso, esempio incluso).
4. **Vincoli obbligatori**: cosa DEVO usare e cosa NON posso usare (es. "usa `enumerate` + `if`, non slicing").
5. **Checklist di verifica**: 3-5 checkbox finali per auto-controllo ("ho filtrato Milano?", "ho scritto header?", "ho contato righe?").
6. **Criterio di valutazione**: esplicitare se si valuta
   - aderenza alla consegna (default),
   - oppure estensioni creative (solo se dichiarato).

Regole aggiuntive per ridurre ambiguita:
- Se una parola puo creare confusione, specificarla: **"numero ordini" != "somma quantita"**.
- Se i dati non contengono un campo citato (es. `stato`), la consegna va corretta PRIMA di proporre l'esercizio.
- Ogni consegna deve includere almeno un esempio mini "input -> output" in 1-2 righe.
- Nei mini-esercizi, separare chiaramente: **modalita debug** (1 record) vs **modalita consegna** (requisiti completi).

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

# --- ESERCIZIO X — 🔄 [RECALL CROSS-MODULO]: ---
# (nel primo capitolo di ogni modulo, dal M3 in poi)
# Prima di affrontare i nuovi concetti, riprendiamo una competenza
# del Modulo X che ti servirà in questo modulo.
# [Task che richiede di usare una competenza di un modulo precedente
#  nel contesto del modulo corrente]
# Scrivi qui sotto:
# ...

# --- ESERCIZIO X — 🌊 [REAL-WORLD]: ---
# (dal Modulo 5 in poi — almeno 1 per modulo)
# ⚠️ Questo esercizio simula un task reale: la consegna è vaga,
# i dati sono sporchi, e non c'è una sola soluzione corretta.
# Il Mentor valuta il tuo APPROCCIO, non il risultato esatto.
# [Consegna deliberatamente vaga con dati problematici]
# Il tuo approccio:
# ...

# --- ESERCIZIO X — 🔍 [DEBUG]: ---
# (dal Modulo 2 in poi)
# Il codice qui sotto DOVREBBE funzionare, ma produce un errore.
# Eseguilo, leggi lo stack trace, trova il bug e correggilo.
# Il Mentor interviene SOLO dopo 2+ tentativi falliti.
# [Codice buggato con errore realistico]
# Stack trace atteso: [descrizione dell'errore che vedrai]
# La tua correzione:
# ...

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
18. **Almeno 1 esercizio di debug autonomo** per capitolo (dal M2 in poi), etichettato `# 🔍 [DEBUG]`. Fornire codice buggato con stack trace reale. Il mentor NON usa la scala progressiva — lo studente deve trovare il bug da solo. Intervento solo dopo 2+ tentativi falliti.
19. **Almeno 1 esercizio real-world** per modulo (dal M5 in poi), etichettato `# 🌊 [REAL-WORLD]`. Consegne vaghe, dati sporchi, nessuna soluzione unica. Il mentor valuta l'approccio e il ragionamento, non il risultato esatto.
20. **Almeno 1 esercizio recall cross-modulo** nel primo capitolo di ogni modulo (dal M3 in poi), etichettato `# 🔄 [RECALL CROSS-MODULO]`. Richiede di usare competenze di un modulo precedente nel nuovo contesto, colmando il gap di retention tra moduli distanti.
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
