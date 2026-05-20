# Archivio Modulo 01 — Python & Dati

> Questo file contiene il dettaglio storico del Modulo 1 (12 capitoli, 17/02/2026 – 25/03/2026).
> Migrato da [`CONTESTO_CORSO.md`](../CONTESTO_CORSO.md) (cartella [`archivi/`](README.md)).
>
> **Regola**: quando l'agente prepara un capitolo del M2+ e deve fare rinforzo su concetti del M1,
> DEVE consultare questo file per il contesto storico completo.
>
> **Data migrazione**: 25/03/2026

---

## Progresso Dettagliato M1 — 12 Capitoli

| File | Stato | Data | Difficoltà (1-10) | Note |
|------|-------|------|--------------------|------|
| 01_benvenuto_python.py | ✅ Completato + Corretto | 17/02/2026 | 2 | Buon primo approccio. Errori tipici da JS: ternario con `?:`, nomi variabili in inglese misto. Ha capito f-string, tipi, casting. |
| 02_condizioni_e_cicli.py | ✅ Completato + Corretto | 17/02/2026 | 4 | FizzBuzz: `range(1,20)` invece di `range(1,21)`. Password: `elif` dove servivano due `if`, `== True` ridondante. Scacchiera perfetta. Temperature incompleto (mancava la media). |
| 03_funzioni.py | ✅ Completato + Corretto | 17/02/2026 | 6 | Ha capito *args, return multipli, sorted. Lambda ancora poco chiare — da rinforzare nei prossimi capitoli. Errori: lista vs parametri separati a *args, count come stringa, mancava `reverse=True`, mancava parametro `decimali`. Tutti corretti. |
| 04_liste.py | ✅ Completato + Corretto | 19/02/2026 | 9 | Difficoltà alta. Ha capito slicing, list comprehension, sorted/filter/map con lambda. Punti deboli: enumerate+tuple non interiorizzati, range a 3 parametri nuovo, consegne non lette completamente. Lambda usate correttamente in ex.4/5/7 — miglioramento reale. |
| 05_dizionari.py | ✅ Completato + Corretto | 17/02/2026 | 8 | Quiz ingresso 1/8 corretto. Quiz verifica 4/8. Dict comprehension usata correttamente nell'ex.3. Lambda consolidate. Contatore + max() padroneggiati. Consegne incomplete persistono. Esercizio 4 (colloquio conta_parole) perfetto al primo tentativo. |
| 06_file_csv.py | ✅ Completato + Corretto | 24/02/2026 | 8 | Completato end-to-end. Quiz verifica 7/8. Esercizi 1-7 e progetto incrementale completati; forte miglioramento su `.get()`/`.items()`, parsing CSV, path handling e refactoring. |
| 07_numpy_intro.py | 🟡 In revisione | 03/03/2026 | — | Quiz d'ingresso + esercizi 1-5 svolti. Mancano correzione finale strutturata e voto difficoltà. ANOMALIA: capitolo senza chiusura formale. |
| 08_tensori_spiegati.py | ✅ Completato + Corretto | 05/03/2026 | 7 | Consolidamento su shape, axis, broadcasting e reshape; esercizi e progetto incrementale completati con correzioni iterative e buona autonomia nel debugging. |
| 09_pandas_intro.py | ✅ Completato + Corretto | 11/03/2026 | 8 | Buona autonomia su groupby/mask/report. Corrette confusioni su `quantita` vs ordini, `max` vs `idxmax`, distinzione Series/DataFrame in consolidamento; progetto incrementale chiuso. |
| 10_pandas_progetto.py | ✅ Completato + Corretto | 25/03/2026 | 7 | Workflow EDA completo. Report .agg corretto con ordini unici, export CSV, metriche complete. |
| 11_matplotlib_grafici.py | ✅ Completato + Corretto | 25/03/2026 | 7 | Grafici e dashboard completati. Rinforzi pre-plot su aggregazioni corrette applicati. |
| 12_web_bridge.py | ✅ Completato + Corretto | 25/03/2026 | 6 | FastAPI + Pandas: endpoint pratiche, stima prezzo, filtri query. Emersi: if var vs is not None, confusione Series/DataFrame, iterazione GroupBy. Endpoint /progetto/pratiche completato. |

**Media difficoltà M1**: 6.5 (cap 07 escluso — senza voto)

---

## Domande Fatte Durante i Capitoli M1

> Le domande spontanee rivelano quali concetti hanno bisogno di rinforzo.

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
- "Spiegami questa funzione (appiattisci_2 con list comprehension doppia)" → Il doppio `for` non era intuitivo
- "Ma elem cosa è?" → Non capiva che `elem` è un nome scelto dal programmatore
- "Non riesco a capire il funzionamento del ciclo for usando enumerate" → enumerate + unpacking non naturale
- "Non capisco dove era la tupla" → Non vedeva la tupla implicita creata da enumerate
- "La tupla ed enumerate non mi rendono molto sicuro" → Autodichiarato: punti deboli consapevoli
- "Perché range ha tre parametri?" → Non sapeva che range() accetta start, stop, step
- "Come fare per evitare che tu possa scordarti queste cose?" → Consapevolezza meta-cognitiva — ha portato alla creazione della Cursor Rule

### Capitolo 05 — dizionari
- "Il metodo zip cosa restituisce?" → Non conosceva zip(), spiegato come "cerniera"
- "prezzi.items() cosa restituisce?" → Distinzione liste vs dizionari non ancora ovvia. Ha portato al ponte mentale ".items() = enumerate dei dizionari"
- ".items() è il corrispettivo di enumerate per i dictionary?" → Ponte mentale confermato
- "Il metodo append funziona per le dictionary?" → Confusione sui metodi specifici
- "Operatore ternario in Python" → Chiesto 2 volte — la sintassi Python non è intuitiva venendo da JS/PHP
- "**p rispiegami questa sintassi" → Il doppio asterisco per spread non era chiaro
- Errore di sintassi su filter(): ordine parametri invertito
- Errore f-string: doppi apici dentro doppi apici
- Errore negazione: `if (!(n in lista))` → sintassi JS

---

## Pattern di Errore M1 — Storico Completo

| # | Pattern | Stato finale M1 | Note |
|---|---------|-----------------|------|
| 1 | Sintassi JS in Python (`? :` invece di ternario) | 🟡 Corretto | Visto al file 01, non ripetuto dopo |
| 2 | `range()` / slicing fine escluso | 🟡 In miglioramento | Visto file 02, ripetuto file 04. Errore persistente ma in calo |
| 3 | `== True` ridondante | 🟢 Superato | Corretto dopo feedback, non ripetuto |
| 4 | Calcoli dentro le f-string | 🟢 Superato | Corretto dopo feedback, non ripetuto |
| 5 | Tipi nei dizionari: stringhe dove servono numeri | 🟡 In miglioramento | Visto file 03, ripetuto file 05 |
| 6 | Lettura incompleta delle consegne | 🟡 In miglioramento | Persistito nel M1, da monitorare nel M2 |
| 7 | Lambda poco chiare | 🟢 Quasi acquisito | Usate correttamente dal file 05 in poi |
| 8 | enumerate/tuple/unpacking | 🟢 Superato | Miglioramento significativo al file 05 |
| 9 | Codice superfluo | 🟢 Superato | Corretto, non ripetuto |
| 10 | Vincoli esercizio ignorati | 🟡 | Collegato al pattern #6 |
| 11 | Ordine parametri filter() | 🟡 | Confonde con sorted() |
| 12 | Variabile sbagliata nel contesto | 🟢 Superato | Visto una volta, non ripetuto |
| 13 | Dict comprehension evitata | 🟡 In miglioramento | Usata nell'ex.3 ma non sempre |
| 14 | return print(...) | 🟡 | Visto più volte |
| 15 | Parametro funzione ignorato | 🟢 Superato | Visto una volta, non ripetuto |
| 16 | Docstring mancante quando richiesta | 🟡 | Collegato al pattern #6 |
| 17 | Diagnosi errore non precisa | 🟡 | Visto al quiz 09 |
| 18 | Confusione Series vs DataFrame | ⚠️ Portato al M2 | Rinforzato in cap.01 M2 |

---

## Competenze Acquisite nel M1 — "Cosa Sapevo Fare Dopo il Modulo 1"

### Dopo il Capitolo 01 — Python Base
- Dichiarare variabili, f-string, casting con `int()`, `float()`, `str()`, `type()`, differenza `=` vs `==`

### Dopo il Capitolo 02 — Controllo di Flusso
- `if/elif/else`, `for...in`, `range()`, `while`, `enumerate()`, `.isdigit()`, `.isupper()`

### Dopo il Capitolo 03 — Funzioni
- `def`, return multiplo, `*args`, `**kwargs`, `sorted()` con key, docstring. Lambda: sintassi nota ma non ancora naturale.

### Dopo il Capitolo 04 — Liste
- `.append()`, `.insert()`, `.remove()`, `.pop()`, slicing, `in`, list comprehension, `sorted()` + lambda, `filter()`, `map()`, liste di liste, `.count()`, `max()` con lambda, training/test split con slicing.

### Dopo il Capitolo 05 — Dizionari
- Creazione, accesso, iterazione con `.keys()`, `.values()`, `.items()`. `.get()` con default, `.setdefault()`, `.copy()`, `in`, ordinamento lista di dizionari, filter con lambda. `.items()` + `enumerate()` padroneggiato.

### Dopo i Capitoli 06-12 — Dati e Web
- Lettura/scrittura CSV, NumPy (array, shape, broadcasting, reshape), tensori (2D/3D/4D, normalizzazione, flatten), Pandas (DataFrame, groupby, mask, agg, report, EDA, merge), Matplotlib (plot, bar, pie, subplot), FastAPI (endpoint, query parameters, JSON response, CORSMiddleware).

---

## Ritmo di Studio M1

- **Sessione 1 (17/02/2026)**: File 01, 02, 03 completati in una sessione
- **Sessione 2 (19/02/2026)**: File 04 completato. Difficoltà 9
- **Sessione 3 (17/02/2026)**: File 05 in corso. Miglioramento su enumerate+.items()
- **Sessione 4 (24/02/2026)**: File 06 in corso avanzato. Forte miglioramento su .get()/.items()
- **Sessione 5 (24/02/2026)**: File 06 completato. Pronto per NumPy
- **Sessione 6 (03-05/03/2026)**: File 07 (quiz + esercizi 1-5), file 08 avviato
- **Sessione 7-9**: File 08-12 completati, avvio M2
- **Ritmo effettivo**: ~1 file ogni 2-3 giorni
- **Durata totale M1**: 17/02/2026 – 25/03/2026 (~5 settimane)

---

## Lacune Quiz M1 — Snapshot alla Chiusura del Modulo

> **ATTENZIONE**: lo stato "live" delle lacune è tracciato in `CONTESTO_CORSO.md` (sezione "Lacune dai Quiz").
> Questa tabella è uno snapshot al momento della chiusura del M1. Per lo stato aggiornato, consultare sempre il file principale.

| # | Concetto | Quiz | Errore | Stato alla chiusura M1 |
|---|----------|------|--------|-------------|
| 1 | Slicing — fine escluso | Ingresso/05 | `numeri[1:4]` → scritto 4 elementi invece di 3 | 🟡 Rinforzato |
| 2 | .append() restituisce None | Ingresso/05 | Pensava restituisse la lista modificata | 🟡 Rinforzato |
| 3 | enumerate vs range | Ingresso/05 | Scritto `range(frutti, len(frutti))` dove serviva `enumerate(frutti, 1)` | 🟡 Rinforzato |
| 4 | Indici delle liste (contare da 0) | Ingresso/05 | `[1:]` invece di `[2:]` per ottenere [30,40,50] | 🟡 Rinforzato |
| 5 | sorted() crea nuova lista | Ingresso/05 | Non menzionata differenza sorted/sort, lambda non obbligatoria | 🟡 Rinforzato |
| 6 | Output concreto vs descrizione | Ingresso/05 | Descritto concetto invece di dare valore `["Marco"]` | 🟡 Rinforzato |
| 7 | Variabile corretta nelle comprehension | Ingresso/05 | Scritto `x` invece di `n` (variabile del for) | 🟡 Rinforzato |
| 8 | len() con aggiunta chiavi | Verifica/05 | Scritto 2 invece di 3 (non contata chiave aggiunta) | 🟡 Rinforzato |
| 9 | >= vs > | Verifica/05 | Escluso Marco (voto 7) con `>= 7` | 🟡 Rinforzato |
| 10 | .get() vs .items() | Verifica/05 | Confuso .items() con .get() per contare frequenze | 🟡 Rinforzato |
| 11 | Parsing CSV manuale | Verifica/06 | Descritto in modo generale, senza sequenza operativa | 🟢 Superato (verificato quiz cap.07) |

---

## Punti di Forza Confermati nel M1

1. Capisce velocemente le analogie PHP/JS → Python
2. Corregge subito dopo il feedback
3. Chiede chiarimenti quando non capisce
4. Sa ragionare in termini di funzioni, parametri, return (background Laravel)
5. Motivato e orientato al risultato
6. Verifica proattivamente formule e logica
7. Sa creare funzioni riutilizzabili spontaneamente
8. Pattern contatore padroneggiato (.get(chiave, 0) + 1)
