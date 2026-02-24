"""
============================================================================
 MODULO 1 — ESERCIZIO 06: Leggere File CSV "A Mano"
 Capire il Dolore Prima di Scoprire Pandas
============================================================================

 TEORIA: Cos'è un File CSV?

 CSV = Comma Separated Values, cioè "Valori Separati da Virgola".
 È il formato più semplice per salvare dati tabellari in un file di testo.

 Se lavori con Laravel, hai sicuramente usato un database MySQL/PostgreSQL.
 Pensa al CSV come a una tabella del database esportata in un file di testo.

 Esempio di tabella SQL:
   id | nome    | prezzo | categoria
   ---|---------|--------|-----------
   1  | Mouse   | 29.99  | Elettronica
   2  | T-Shirt | 19.99  | Abbigliamento

 Lo stesso in CSV:
   id,nome,prezzo,categoria
   1,Mouse,29.99,Elettronica
   2,T-Shirt,19.99,Abbigliamento

 La prima riga è l'HEADER (i nomi delle colonne, come i campi di una tabella).
 Ogni riga successiva è un RECORD (una riga della tabella, un "row").
 I valori sono separati da virgole (ecco perché si chiama "Comma Separated").

 PERCHÉ LEGGERLO "A MANO"?
 Nel capitolo 09 userai Pandas, che legge un CSV in una sola riga di codice.
 Ma prima è utile capire cosa succede "sotto il cofano", così quando
 Pandas farà qualcosa di strano, saprai il perché.

 È come capire le query SQL prima di usare Eloquent in Laravel:
 puoi usare Eloquent senza sapere SQL, ma quando qualcosa non funziona,
 sapere SQL ti salva la vita.

 Confronto a tre — leggere un file:

   PHP:
     $file = fopen('dati.csv', 'r');
     $header = fgetcsv($file);          // legge la prima riga (intestazioni)
     while ($riga = fgetcsv($file)) {   // legge una riga alla volta
         // $riga è un array: ["1001", "2024-01-05", "Cuffie", ...]
     }
     fclose($file);
     // fopen() apre il file, fgetcsv() legge una riga CSV alla volta,
     // fclose() chiude il file quando hai finito.

   JavaScript (Node.js):
     const fs = require('fs');
     const contenuto = fs.readFileSync('dati.csv', 'utf8');
     const righe = contenuto.split('\\n');
     // require('fs') importa il modulo File System di Node.js
     // readFileSync() legge l'intero file come stringa
     // .split('\\n') divide la stringa in un array di righe

   Python:
     with open('dati.csv', 'r', encoding='utf-8') as file:
         contenuto = file.read()
     # 'with' chiude il file automaticamente — come un try-finally
     # 'r' = read (lettura). Altre modalità: 'w' (write), 'a' (append)
     # encoding='utf-8' gestisce correttamente accenti e caratteri speciali

 Perché serve per l'AI?
   - I dataset per Machine Learning (ML = Apprendimento Automatico) sono
     quasi sempre in formato CSV
   - Kaggle (la piattaforma principale per competizioni di ML) usa CSV
   - Prima di dare i dati a un modello AI, devi "pulirli" — e per pulirli
     devi saperli leggere e manipolare
   - Il tuo futuro applicativo documentale leggerà dati da file/export CSV

============================================================================
"""

# ==========================================================================
# PRIMA DI INIZIARE — Concetti Fondamentali
# ==========================================================================
#
# In questo capitolo lavoriamo con i FILE. Prima di toccare il codice,
# capiamo bene DI COSA STIAMO PARLANDO.
#
# --- Cos'è un file? ---
# Un file è un contenitore di dati salvato sul disco del computer.
# Pensa al disco del tuo PC come a un enorme archivio con cassetti.
# Ogni file è un cassetto con un'etichetta (il nome del file) e un
# contenuto (i dati dentro).
#
# Esistono due grandi famiglie di file:
#   1. FILE DI TESTO — contengono caratteri leggibili dall'uomo.
#      Esempi: .txt, .csv, .html, .py, .php, .js, .json
#      Se li apri con Blocco Note, vedi testo comprensibile.
#
#   2. FILE BINARI — contengono dati in formato macchina.
#      Esempi: .jpg, .mp3, .exe, .pdf, .zip
#      Se li apri con Blocco Note, vedi simboli incomprensibili.
#
# I file CSV sono FILE DI TESTO. Questo è importante perché significa
# che possiamo leggerli riga per riga, come se leggessimo un libro.
#
# --- Cos'è un "percorso" (path)? ---
# Per trovare un file, il computer ha bisogno del suo INDIRIZZO completo,
# che si chiama "percorso" o "path". È come l'indirizzo di una casa.
#
#   Windows: C:\Users\visaf\Desktop\Corso IA\dati\vendite.csv
#   Mac/Linux: /home/visaf/Desktop/Corso IA/dati/vendite.csv
#
# Nota: Windows usa la barra rovesciata \, Mac/Linux usa la barra /.
# Python gestisce entrambe, ma per evitare problemi usiamo os.path.join()
# che costruisce il percorso giusto per il tuo sistema operativo.
#
# In PHP: non hai questo problema perché i file di solito sono nella
# stessa cartella del progetto Laravel (storage/, public/, ecc.)
# In JS: in Node.js usi path.join() — stesso concetto di os.path.join().
#
# --- Cos'è la codifica (encoding)? ---
# I computer salvano i file come sequenze di numeri (0 e 1).
# La "codifica" è la TABELLA DI TRADUZIONE che dice al computer
# quale numero corrisponde a quale carattere.
#
#   UTF-8: lo standard moderno. Gestisce TUTTI i caratteri del mondo
#   (lettere accentate àèìòù, emoji 🎯, ideogrammi cinesi 中文, ecc.)
#
# Se non specifichi la codifica, Python potrebbe interpretare male
# i caratteri speciali — le lettere accentate diventano simboli strani.
# Per questo scriviamo SEMPRE encoding="utf-8" quando apriamo un file.
#
# In PHP: di solito non ti preoccupi perché PHP legge i byte grezzi.
# Ma se hai mai avuto problemi con le "è" che diventano "Ã¨", era
# proprio un problema di codifica!
#
# --- Cos'è il modulo 'os'? ---
# 'os' è un modulo built-in di Python (= già incluso, non serve
# installarlo con pip) che fornisce funzioni per interagire con il
# sistema operativo: creare cartelle, trovare percorsi, ecc.
#
# os.path.join("cartella", "file.csv") → "cartella/file.csv" (Mac)
#                                       → "cartella\\file.csv" (Windows)
#
# os.path.dirname(__file__) → restituisce la cartella in cui si trova
# il file Python che stai eseguendo. __file__ è una variabile speciale
# che contiene il percorso del file corrente.
#
# In PHP: l'equivalente è __DIR__ (la cartella del file PHP corrente).
# In JS (Node.js): l'equivalente è __dirname.
#
# --- Cos'è il modulo 'csv'? ---
# 'csv' è un altro modulo built-in di Python. Fornisce strumenti
# specializzati per leggere e scrivere file CSV. Lo vedremo nella PARTE 4.
# Per ora sappi solo che esiste e che lo importiamo all'inizio del file.
#
# "import" in Python è come:
#   PHP: require_once 'file.php';  oppure  use NomeClasse;
#   JS:  const modulo = require('modulo');  oppure  import modulo from 'modulo';
#
# La differenza è che in Python non devi specificare il percorso del file:
# Python sa già dove trovare i moduli built-in.

import os
import csv

# Costruiamo il percorso al file CSV.
# os.path.dirname(__file__) = la cartella dove si trova QUESTO file Python
# os.path.join() = unisce i pezzi del percorso con il separatore giusto
# Risultato finale: qualcosa come "C:\...\modulo_01_python_dati\dati"
percorso_dati = os.path.join(os.path.dirname(__file__), "dati")
percorso_csv = os.path.join(percorso_dati, "vendite_ecommerce.csv")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ D'INGRESSO — Rispondi PRIMA di leggere la teoria!              ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti del CAPITOLO 05 (Dizionari).
# Rispondi senza guardare il codice — servono a capire cosa hai interiorizzato.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — Prevedi l'output:
# Cosa stampa questo codice?
#   persona = {"nome": "Marco", "eta": 30}
#   persona["lavoro"] = "developer"
#   print(len(persona))
# La tua risposta: 3

# DOMANDA 2 — Prevedi l'output:
# Cosa stampa questo codice?
#   prezzi = {"mela": 1.50, "banana": 0.80, "kiwi": 2.00}
#   cari = {k: v for k, v in prezzi.items() if v >= 1.50}
#   print(cari)
# La tua risposta: {"mela": 1.50, "kiwi": 2.00}

# DOMANDA 3 — Vero o Falso?
# "Il metodo .get('chiave', default) restituisce il default se la chiave
#  non esiste, MA NON aggiunge la chiave al dizionario"
# La tua risposta (V/F): V

# DOMANDA 4 — Trova l'errore:
#   conteggio = {}
#   for parola in ["ciao", "mondo", "ciao"]:
#       conteggio[parola] = conteggio.items(parola, 0) + 1
# Qual è il problema? Come lo correggeresti?
# La tua risposta:
#   conteggio = {}
#   for parola in ["ciao", "mondo", "ciao"]:
#       conteggio[parola] = conteggio.get(parola, 0) + 1


# DOMANDA 5 — Completa il codice:
#   inventario = {"Maglietta": 20, "Jeans": 5, "Scarpe": 15}
#   for i, (prodotto, qty) in ___(inventario.___(), 1):
#       print(f"{i}. {prodotto}: {qty}")
# Riempi i due spazi: enumerates, items

# DOMANDA 6 — Prevedi l'output:
#   ordine = {"id": 1, "cliente": {"nome": "Anna", "citta": "Roma"}}
#   print(ordine["cliente"]["citta"])
# La tua risposta: Roma

# DOMANDA 7 — Definizione:
# Che differenza c'è tra .setdefault() e .update()?
# La tua risposta: .setdefault verifica che la chiave che sto mensionando esiste, e solo qualora non esistesse la crea e vi appone il valore di default che ho inserito, update invece aggiunge tutto le chiavi: valori che scrivo e se gia' esistevano le sovrascrive

# DOMANDA 8 — Prevedi l'output:
#   d = {"a": 1, "b": 2}
#   copia = d.copy()
#   copia["a"] = 99
#   print(d["a"])
# La tua risposta: 99


# ==========================================================================
# PARTE 1: Leggere un File di Testo — open() e with
# ==========================================================================

# RIPASSO — f-string: ricordi? La f davanti alla stringa ti permette
# di inserire variabili dentro le graffe {}. Come i template literal
# `` `ciao ${nome}` `` in JS o "ciao $nome" in PHP.

# RIPASSO — len(): è una FUNZIONE, non un metodo (.length in JS).
# Si scrive len(cosa), non cosa.len(). Restituisce il numero di elementi
# di una lista, le chiavi di un dizionario, o i caratteri di una stringa.

# --- Come si legge un file? Il concetto generale ---
#
# Leggere un file è un'operazione in 3 PASSI, in QUALSIASI linguaggio:
#   1. APRIRE il file  → "Ehi sistema operativo, voglio accedere a questo file"
#   2. LEGGERE il contenuto  → "Dammi i dati che ci sono dentro"
#   3. CHIUDERE il file  → "Ho finito, puoi rilasciare la risorsa"
#
# Perché bisogna CHIUDERE il file?
# Quando apri un file, il sistema operativo "blocca" quella risorsa.
# È come quando prendi un libro dalla libreria: finché ce l'hai tu,
# nessun altro può usarlo. Se dimentichi di restituirlo (= chiudere),
# il libro resta bloccato. Con i file è uguale: se non chiudi, il file
# resta "occupato" e altri programmi potrebbero non poterlo usare.
# Inoltre, se il programma crasha prima di chiudere, i dati scritti
# potrebbero non essere salvati correttamente.
#
# --- I tre linguaggi a confronto: APERTURA e CHIUSURA ---
#
# PHP — apertura MANUALE, chiusura MANUALE:
#   $file = fopen('dati.csv', 'r');      // 1. Apri — fopen = "file open"
#   $contenuto = fread($file, filesize('dati.csv'));  // 2. Leggi
#   fclose($file);                       // 3. Chiudi — fclose = "file close"
#
#   // fopen() restituisce un "handle" (= una maniglia, un riferimento al file)
#   // Quel $file NON è il contenuto! È solo il "biglietto" che dice al
#   // sistema operativo QUALE file stai usando.
#   // fread($file, N) legge N byte dal file.
#   // filesize('dati.csv') restituisce la dimensione del file in byte.
#
#   // Alternativa più semplice (legge tutto in un colpo):
#   $contenuto = file_get_contents('dati.csv');
#   // file_get_contents() fa open + read + close in una sola funzione!
#   // È comoda ma non ti dà controllo su COME leggere (riga per riga, ecc.)
#
# JavaScript (Node.js) — apertura MANUALE, chiusura MANUALE:
#   const fs = require('fs');
#   // require('fs') importa il modulo "File System" di Node.js.
#   // 'fs' è un oggetto con tanti metodi per lavorare con i file.
#
#   const contenuto = fs.readFileSync('dati.csv', 'utf8');
#   // readFileSync() fa open + read + close in una sola funzione!
#   // "Sync" = sincrono → blocca l'esecuzione finché non ha finito di leggere.
#   // 'utf8' specifica la codifica (come encoding="utf-8" in Python).
#
#   // Alternativa asincrona (più comune in Node.js):
#   fs.readFile('dati.csv', 'utf8', (err, data) => {
#       // questa funzione callback viene eseguita DOPO che il file è stato letto
#       // 'err' contiene l'errore se qualcosa è andato storto, altrimenti null
#       // 'data' contiene il contenuto del file
#   });
#
# Python — apertura + chiusura AUTOMATICA con 'with':
#   with open('dati.csv', 'r', encoding='utf-8') as file:
#       contenuto = file.read()
#   # Quando il blocco 'with' finisce, Python chiude il file automaticamente.
#
# --- Scomposizione della riga Python ---
#
#   with open('dati.csv', 'r', encoding='utf-8') as file:
#   │    │              │              │              │
#   │    │              │              │              └─ 'file' è il NOME che diamo
#   │    │              │              │                 all'handle del file (come
#   │    │              │              │                 $file in PHP). Puoi chiamarlo
#   │    │              │              │                 come vuoi: f, file, mio_file...
#   │    │              │              │
#   │    │              │              └─ encoding='utf-8' = la codifica.
#   │    │              │                 Senza questo, su Windows potrebbe usare
#   │    │              │                 una codifica diversa e le lettere accentate
#   │    │              │                 (è, à, ù) diventano simboli strani.
#   │    │              │
#   │    │              └─ 'r' = modalità di apertura:
#   │    │                 'r' = read (lettura) — DEFAULT, puoi anche ometterlo
#   │    │                 'w' = write (scrittura) — ATTENZIONE: CANCELLA il contenuto!
#   │    │                 'a' = append (aggiunta) — scrive IN FONDO al file
#   │    │                 'r+' = lettura + scrittura
#   │    │                 Stesse modalità di fopen() in PHP: 'r', 'w', 'a', ecc.
#   │    │
#   │    └─ open() = la funzione Python per aprire un file.
#   │       Come fopen() in PHP.
#   │
#   └─ 'with' = il "gestore di contesto" (context manager).
#      È come un try-finally automatico. Garantisce che il file venga
#      chiuso anche se il codice dentro genera un errore.
#
#      Senza 'with' (stile PHP, SCONSIGLIATO in Python):
#        file = open('dati.csv', 'r')
#        contenuto = file.read()
#        file.close()    # Se dimentichi questa riga, il file resta aperto!
#
#      Con 'with' (stile Python, CONSIGLIATO):
#        with open('dati.csv', 'r') as file:
#            contenuto = file.read()
#        # file.close() avviene AUTOMATICAMENTE qui
#
# --- I metodi di lettura ---
#
# Una volta aperto il file, hai 3 modi per leggere il contenuto:
#
#   file.read()       → legge TUTTO il file in una STRINGA
#                       Come file_get_contents() in PHP.
#                       Esempio: "riga1\nriga2\nriga3" (tutto insieme)
#
#   file.readline()   → legge UNA SOLA riga
#                       Come fgets() in PHP.
#                       Ogni chiamata avanza alla riga successiva.
#
#   file.readlines()  → legge TUTTE le righe in una LISTA di stringhe
#                       Come file() in PHP (che restituisce un array di righe).
#                       Esempio: ["riga1\n", "riga2\n", "riga3\n"]
#                       Nota: ogni riga include il \n finale!
#
#   for riga in file: → legge UNA RIGA ALLA VOLTA (il più efficiente)
#                       Come while ($riga = fgets($file)) in PHP.
#                       Non carica tutto in memoria — perfetto per file enormi.

print("=== Leggere il file intero come testo ===")
with open(percorso_csv, "r", encoding="utf-8") as file:
    contenuto = file.read()

# RIPASSO — slicing: ricordi? lista[start:end] estrae una porzione.
# Lo slicing funziona anche sulle STRINGHE (che sono sequenze di caratteri).
# contenuto[:500] prende i primi 500 caratteri — il 500 è ESCLUSO.
print(contenuto[:500])
print(f"\nCaratteri totali: {len(contenuto)}")

# 🔁 RINFORZO MIRATO — Slicing: fine escluso
# Al quiz del cap. 05 hai scritto che numeri[1:4] dà [20,30,40,50] (4 elementi).
# Ma il secondo numero è ESCLUSO! numeri[1:4] dà [20,30,40] (3 elementi).
# Rivediamolo con le stringhe (nuovo contesto, stessa regola):
#   testo = "ABCDEFG"
#   print(testo[1:4])   # → "BCD" (indici 1, 2, 3 — il 4 è escluso!)
#   print(testo[:3])     # → "ABC" (dall'inizio, fino all'indice 2)
#   print(testo[5:])     # → "FG"  (dall'indice 5 alla fine)
#
# Prova subito:
# 1) Dalla variabile 'contenuto' qui sopra, estrai i caratteri dal 10° al 30°
#    (ricorda: il 30 è escluso, quindi ottieni 20 caratteri)
# 2) Quanti caratteri ottieni con contenuto[0:10]? (Conta: è 10 o 11?)
# Scrivi qui sotto:
porzione = contenuto[10:31]
# la risposta è 10


# --- MINI-ESERCIZIO 1 — Prova subito! ---
# 1) Apri il file "vendite_ecommerce.csv" con open() e stampa SOLO
#    le prime 3 righe (suggerimento: usa .readlines() per avere una lista
#    di righe, poi slicing [:3])
# 2) Stampa l'ultima riga del file (suggerimento: indice [-1])
# Scrivi qui sotto:
with open(percorso_csv, "r", encoding="utf-8") as file:
    prova = file.readlines()
print("\nMini Esercizio 1 , Open e Read\n")
for s in prova[:3]:
    print(f"{s}")
print(f"\n{prova[-1]}")


# ==========================================================================
# PARTE 2: Leggere Riga per Riga — enumerate() e .strip()
# ==========================================================================

# Nella PARTE 1 abbiamo letto TUTTO il file con .read() → una stringa unica.
# Ma spesso i file sono ENORMI (milioni di righe!). Caricare tutto in memoria
# sarebbe come cercare di bere un lago intero in un sorso.
#
# La soluzione è leggere UNA RIGA ALLA VOLTA. È come leggere un libro:
# non fotocopi tutte le pagine prima di leggere — le leggi una alla volta.
#
# In Python, un file aperto è "iterabile" — puoi metterlo direttamente
# nel ciclo for! Python ti dà una riga alla volta, senza caricarle tutte.
#
#   with open('file.csv', 'r') as file:
#       for riga in file:        # 'riga' è una stringa con il testo della riga
#           print(riga)
#
# In PHP, il pattern è quasi identico:
#   $file = fopen('file.csv', 'r');
#   while ($riga = fgets($file)) {    // fgets() = "file get string"
#       echo $riga;                   // legge una riga alla volta
#   }                                 // quando finiscono le righe, fgets() → false
#   fclose($file);                    // e il while si ferma
#
# In JS (Node.js), devi fare un po' più di lavoro:
#   const fs = require('fs');
#   const contenuto = fs.readFileSync('file.csv', 'utf8');
#   const righe = contenuto.split('\n');   // dividi per "a capo"
#   for (const riga of righe) {
#       console.log(riga);
#   }
#   // Nota: in JS non puoi iterare direttamente sul file come in Python.
#   // Devi prima leggerlo tutto e poi dividere. Per file enormi, useresti
#   // readline (un modulo di Node.js), ma è più complesso.
#
# --- Cos'è il carattere \n ? ---
# \n si chiama "newline" o "a capo". È un carattere INVISIBILE che dice
# "vai alla riga successiva". Quando premi INVIO nella tastiera, inserisci
# un \n. Nei file di testo, ogni riga termina con \n.
#
#   Contenuto reale del file (con \n visibili):
#   "id_ordine,data,prodotto\n1001,2024-01-05,Cuffie\n1002,..."
#
#   Cosa VEDI sullo schermo (il \n diventa "a capo"):
#   id_ordine,data,prodotto
#   1001,2024-01-05,Cuffie
#   1002,...
#
# Quando leggi riga per riga, ogni riga INCLUDE il \n finale!
# Per questo devi rimuoverlo con .strip().
#
# --- .strip() — Pulire le stringhe ---
# .strip() rimuove spazi bianchi e \n (caratteri "a capo") da ENTRAMBE
# le estremità della stringa (inizio e fine). NON tocca il centro.
#
#   "  ciao mondo  \n".strip()  → "ciao mondo"    (spazi + \n rimossi)
#   "ciao mondo".strip()        → "ciao mondo"    (niente da rimuovere)
#   "\n\n  hello  \n".strip()   → "hello"         (tutto pulito)
#
# Varianti utili:
#   .lstrip() → rimuove solo a SINISTRA (left strip)
#   .rstrip() → rimuove solo a DESTRA (right strip)
#   .strip(",") → rimuove le virgole dai bordi (puoi specificare quali caratteri)
#
# Confronto a tre:
#   Python: riga.strip()       → rimuove spazi e \n dai bordi
#   PHP:    trim($riga)        → identico! trim() fa esattamente la stessa cosa
#           ltrim($riga)       → solo a sinistra (come .lstrip())
#           rtrim($riga)       → solo a destra (come .rstrip())
#   JS:     riga.trim()        → identico! .trim() è universale
#           riga.trimStart()   → solo a sinistra
#           riga.trimEnd()     → solo a destra
#
# PERCHÉ .strip() È FONDAMENTALE PER I CSV?
# Se non lo usi, i tuoi dati avranno \n alla fine:
#   Senza strip: record["citta"] = "Milano\n"  → confronti falliranno!
#   Con strip:   record["citta"] = "Milano"     → tutto funziona

# RIPASSO — enumerate(): ricordi il ponte mentale? Come .items() è
# l'enumerate dei dizionari, enumerate() è il "numeratore" delle liste.
# Dà una coppia (indice, valore) che spacchetti in due variabili.
#   for i, elemento in enumerate(["a", "b", "c"]):
#       print(i, elemento)   # 0 a, 1 b, 2 c

# 🔁 RINFORZO MIRATO — enumerate vs range
# Al quiz del cap. 05, per stampare "1. mela, 2. pera" hai scritto
# range(frutti, len(frutti)) — ma range() genera solo NUMERI, non
# ti dà gli elementi! enumerate() ti dà ENTRAMBI: indice + elemento.
#
#   Quando usare range():
#     for i in range(5):         # Solo numeri: 0, 1, 2, 3, 4
#     for i in range(len(lista)):  # Indice, poi accedi con lista[i] — EVITA!
#
#   Quando usare enumerate():
#     for i, elemento in enumerate(lista):      # indice + elemento insieme
#     for i, elemento in enumerate(lista, 1):   # contatore parte da 1
#
# Regola: se ti serve l'elemento, usa enumerate(). Se ti servono solo numeri, usa range().
#
# Prova subito:
# 1) Scrivi un for che stampa le prime 5 righe del file con il numero di riga,
#    usando enumerate(). Esempio output: "Riga 1: id_ordine,data,prodotto,..."
# Scrivi qui sotto:
with open(percorso_csv, "r", encoding="utf-8") as file:
    for numero_riga, riga in enumerate(file):
        riga = riga.strip()
        if numero_riga < 5:
            print(f"Riga: {numero_riga} {riga}")

# print("\n=== Leggere riga per riga ===")
# with open(percorso_csv, "r", encoding="utf-8") as file:
#     for numero_riga, riga in enumerate(file):
#         riga = riga.strip()
#         if numero_riga < 5:
#             print(f"Riga {numero_riga}: {riga}")

# Analizziamo il codice qui sopra riga per riga:
#
#   with open(percorso_csv, "r", encoding="utf-8") as file:
#   → Apre il file CSV in lettura. 'file' è l'handle.
#
#   for numero_riga, riga in enumerate(file):
#   → enumerate(file) dà due cose per ogni riga:
#     - numero_riga = l'indice (0, 1, 2, 3, ...)
#     - riga = il testo della riga (es. "1001,2024-01-05,Cuffie\n")
#
#   riga = riga.strip()
#   → Rimuove il \n finale (e eventuali spazi). SOVRASCRIVE la variabile
#     'riga' con la versione pulita. Da "Cuffie\n" a "Cuffie".
#
#   if numero_riga < 5:
#   → Stampiamo solo le prime 5 righe (indici 0, 1, 2, 3, 4).
#     Se il file ha 30 righe, le legge TUTTE ma stampa solo le prime 5.


# --- MINI-ESERCIZIO 2 — Prova subito! ---
# 1) Leggi il file riga per riga e conta quante righe totali ha
#    (header incluso). Stampa: "Il file ha X righe (1 header + Y dati)"
# 2) Stampa solo le righe che contengono "Milano" (suggerimento: "Milano" in riga)
# Scrivi qui sotto:
with open(percorso_csv, "r", encoding="utf-8") as file:
    counter = 0
    milano = []
    for key, value in enumerate(file, 1):
        if "Milano" in value:
            milano.append(value.strip())
        counter = key
    print("\nMini esercizio 2\n")
    print(f"Il file ha {counter} Righe, di cui 1 Header e {counter -1} dati\n")
    print(f"Le righe che contengono milano sono {milano}")



# ==========================================================================
# PARTE 3: Parsare il CSV "a Mano" — Da Testo a Dati Strutturati
# ==========================================================================

# --- Cos'è il "parsing"? ---
# "Parsing" (o "parsare") = trasformare un testo grezzo (una stringa)
# in dati STRUTTURATI (liste, dizionari, oggetti) che il codice può usare.
#
# Pensa a un postino che riceve una busta con scritto:
#   "Mario Rossi, Via Roma 42, 20121, Milano"
#
# Il postino deve PARSARE (= interpretare) quella stringa per capire che:
#   nome = "Mario Rossi"
#   via = "Via Roma 42"
#   cap = "20121"
#   citta = "Milano"
#
# Noi facciamo lo stesso con il CSV: prendiamo una stringa di testo
# e la trasformiamo in un dizionario Python con chiavi e valori.
#
# In JavaScript hai già usato il parsing:
#   JSON.parse('{"nome": "Mario"}')  → restituisce un OGGETTO JavaScript
#   La stringa '{"nome": "Mario"}' diventa l'oggetto {nome: "Mario"}
#   Stessa idea! Da testo → a struttura dati.
#
# In PHP:
#   json_decode('{"nome": "Mario"}')  → restituisce un oggetto/array PHP
#   fgetcsv($file)  → parsare una riga CSV in un array PHP
#
# In Python non esiste un "CSV.parse()" — dobbiamo farlo noi!
# (Oppure usiamo il modulo csv, che vedremo nella PARTE 4)

# --- Il piano d'azione ---
# Ecco cosa faremo, passo per passo:
#
#   1. Leggiamo TUTTE le righe del file → lista di stringhe
#   2. Prendiamo la PRIMA riga → è l'header (nomi delle colonne)
#   3. Per OGNI riga successiva:
#      a. La dividiamo per virgola → lista di valori
#      b. Abbiniamo ogni valore al nome della colonna corrispondente
#      c. Creiamo un dizionario e lo aggiungiamo alla lista finale
#
# Risultato finale: una lista di dizionari. Identica a quello che ottieni
# con un'API REST o con Eloquent ->get()->toArray() in Laravel.

# RIPASSO — .split(): taglia una stringa in pezzi usando un separatore.
#   "ciao,mondo".split(",")     → ["ciao", "mondo"]     (2 pezzi)
#   "a-b-c-d".split("-")        → ["a", "b", "c", "d"]  (4 pezzi)
#   "ciao mondo bello".split()  → ["ciao", "mondo", "bello"]
#   # Senza argomento, .split() divide per SPAZI (uno o più)
#
# Confronto a tre:
#   Python: "ciao,mondo".split(",")        → ["ciao", "mondo"]
#   PHP:    explode(",", "ciao,mondo")      → ["ciao", "mondo"]
#           // ATTENZIONE: in PHP i parametri sono INVERTITI!
#           // Prima il separatore, poi la stringa. In Python è il contrario.
#   JS:     "ciao,mondo".split(",")         → ["ciao", "mondo"]
#           // Stessa sintassi di Python! È un metodo della stringa.

# 🔁 RINFORZO MIRATO — Indici: contare da 0
# Al quiz del cap. 05, per ottenere [30,40,50] da [10,20,30,40,50] hai
# scritto prezzi[1:] — ma quello dà [20,30,40,50] (parte dall'indice 1).
# Ricorda: in Python (come in JS), si conta da 0!
#   lista  = [10, 20, 30, 40, 50]
#   indice =   0   1   2   3   4
# Per avere [30,40,50] serve prezzi[2:], perché 30 è all'indice 2.
#
# Nel CSV, la riga 0 è l'header e le righe [1:] sono i dati:
#   righe[0]  = "id_ordine,data,prodotto,..."  (header)
#   righe[1]  = "1001,2024-01-05,Cuffie,..."   (primo dato)
#   righe[1:] = tutte le righe DOPO l'header

print("\n=== Parsing manuale del CSV ===")
dati = []    # lista vuota — ci metteremo dentro i dizionari

with open(percorso_csv, "r", encoding="utf-8") as file:
    righe = file.readlines()
    # .readlines() legge TUTTE le righe e le mette in una LISTA.
    # Ogni elemento della lista è una stringa (una riga del file).
    # Esempio:
    #   righe[0] = "id_ordine,data,prodotto,categoria,prezzo,quantita,citta,metodo_pagamento\n"
    #   righe[1] = "1001,2024-01-05,Cuffie Bluetooth,Elettronica,49.99,2,Milano,Carta di Credito\n"
    #   ...
    # Nota il \n alla fine di ogni riga!

    # PASSO 1: Prendiamo l'header (la riga con i nomi delle colonne)
    header = righe[0].strip().split(",")
    # Cosa fa questa riga, pezzo per pezzo:
    #   righe[0]         → "id_ordine,data,prodotto,...,metodo_pagamento\n"
    #   .strip()         → "id_ordine,data,prodotto,...,metodo_pagamento"  (via il \n)
    #   .split(",")      → ["id_ordine", "data", "prodotto", ..., "metodo_pagamento"]
    # Risultato: una LISTA con i nomi delle colonne.
    print(f"Colonne: {header}")

    # PASSO 2: Per ogni riga di dati (dalla seconda in poi)
    for riga in righe[1:]:    # righe[1:] = tutte le righe TRANNE la prima
        valori = riga.strip().split(",")
        # Stessa operazione dell'header:
        #   "1001,2024-01-05,Cuffie Bluetooth,Elettronica,49.99,2,Milano,Carta di Credito\n"
        #   → ["1001", "2024-01-05", "Cuffie Bluetooth", "Elettronica", "49.99", "2", "Milano", "Carta di Credito"]

        # PASSO 3: Creiamo un dizionario abbinando header → valori
        # È come ZIP: "chiudi la cerniera" tra i nomi delle colonne e i valori.
        # Se header = ["id_ordine", "data", "prodotto"] e valori = ["1001", "2024-01-05", "Cuffie"]
        # Il risultato sarà: {"id_ordine": "1001", "data": "2024-01-05", "prodotto": "Cuffie"}
        record = {}
        for i, colonna in enumerate(header):
            # enumerate(header) dà: (0, "id_ordine"), (1, "data"), (2, "prodotto"), ...
            # Usiamo l'indice i per prendere il valore corrispondente da 'valori'
            record[colonna] = valori[i]
            # Ciclo 1: record["id_ordine"] = valori[0] = "1001"
            # Ciclo 2: record["data"] = valori[1] = "2024-01-05"
            # Ciclo 3: record["prodotto"] = valori[2] = "Cuffie Bluetooth"
            # ... e così via per tutte le colonne

        dati.append(record)
        # Aggiungiamo il dizionario alla lista 'dati'.
        # Dopo il primo ciclo: dati = [{"id_ordine": "1001", "data": "2024-01-05", ...}]
        # Dopo il secondo: dati = [{...primo...}, {...secondo...}]
        # E così via per ogni riga del file.

# RISULTATO FINALE: 'dati' è una lista di dizionari.
#
# È IDENTICO a quello che otterresti con:
#   PHP:    $ordini = DB::table('ordini')->get()->toArray();
#   JS:     const ordini = await fetch('/api/ordini').then(r => r.json());
#   Python: dati = [{"id_ordine": "1001", ...}, {"id_ordine": "1002", ...}, ...]
#
# Ogni record è un dizionario (come un oggetto JSON) con le chiavi
# che sono i nomi delle colonne e i valori che sono i dati della riga.
#
# ATTENZIONE IMPORTANTE: tutti i valori sono STRINGHE!
# Anche il prezzo "49.99" e la quantità "2" sono stringhe, non numeri.
# Per fare calcoli matematici, dovrai convertire: float("49.99"), int("2").

print(f"\nNumero di record: {len(dati)}")
print(f"\nPrimo record:")
for chiave, valore in dati[0].items():
    print(f"  {chiave}: {valore}")

print(f"\nUltimo record:")
for chiave, valore in dati[-1].items():
    print(f"  {chiave}: {valore}")


# 🔁 RINFORZO MIRATO — .append() restituisce None
# Al quiz del cap. 05, pensavi che .append() restituisse la lista modificata.
# In realtà, .append() modifica la lista ma restituisce SEMPRE None.
# Guarda il codice qui sopra: facciamo dati.append(record) — non assegniamo
# il risultato a niente perché il risultato sarebbe None!
#
#   # SBAGLIATO — lista sarà None!
#   lista = [].append("ciao")    # → lista = None
#
#   # CORRETTO — prima crei la lista, poi ci appendi
#   lista = []
#   lista.append("ciao")         # → lista = ["ciao"]
#
# In JS, .push() restituisce la nuova LUNGHEZZA dell'array (non l'array!).
# In PHP, array_push() restituisce il nuovo conteggio (non l'array!).
# In Python, .append() restituisce None. Tutti diversi — attenzione!
#
# Prova subito:
# 1) Cosa stampa questo codice? Rispondi PRIMA di eseguirlo:
#    risultato = [1, 2, 3].append(4)
#    print(risultato)
# La tua risposta: ___
# Scrivi qui sotto:
# ...


# --- MINI-ESERCIZIO 3 — Prova subito! ---
# Usando la lista 'dati' creata qui sopra:
# 1) Stampa il prodotto e il prezzo del record con indice 5
#    (suggerimento: dati[5]["prodotto"])
# 2) Stampa quante colonne ha ogni record (suggerimento: len() sulle chiavi)
# 3) Stampa i primi 3 record in formato tabella:
#    "1001 | Cuffie Bluetooth | 49.99 | Milano"
# Scrivi qui sotto:
# ...


# ==========================================================================
# PARTE 4: Un Modo Più Elegante — Il Modulo csv di Python
# ==========================================================================

# Nella PARTE 3 abbiamo parsato il CSV "a mano" con .split(",").
# Funziona, ma ha un GROSSO LIMITE: cosa succede se un dato contiene
# una virgola? Esempio:
#
#   nome,indirizzo,citta
#   Mario,"Via Roma 42, interno 3",Milano
#
# Il nostro .split(",") dividerebbe "Via Roma 42, interno 3" in DUE pezzi!
# Il parsing andrebbe in errore perché avremmo più valori che colonne.
#
# I file CSV "professionali" gestiscono questo caso mettendo i valori
# problematici tra virgolette. Ma il nostro codice manuale non sa
# gestire le virgolette!
#
# Il modulo 'csv' di Python risolve TUTTI questi problemi:
#   - Valori che contengono virgole (li gestisce grazie alle virgolette)
#   - Separatori diversi dalla virgola (punto e virgola, tab, pipe |)
#   - Virgolette dentro i valori (le "escape" automaticamente)
#   - Righe vuote o con dati mancanti
#
# In PHP, fgetcsv() fa la stessa cosa — gestisce virgolette e separatori.
# In JS (Node.js), non c'è un modulo built-in: devi installare la
# libreria 'csv-parse' con npm install csv-parse. Un motivo in più per
# apprezzare il fatto che Python ce l'ha già incluso!
#
# --- Gli strumenti del modulo csv ---
#
# Il modulo csv offre diversi strumenti. I più importanti sono:
#
#   csv.reader(file)       → legge ogni riga come una LISTA di valori
#                            Esempio: ["1001", "2024-01-05", "Cuffie"]
#                            Come fgetcsv() in PHP (restituisce un array)
#
#   csv.DictReader(file)   → legge ogni riga come un DIZIONARIO
#                            Esempio: {"id_ordine": "1001", "data": "2024-01-05"}
#                            Usa automaticamente la prima riga come chiavi!
#                            NON esiste un equivalente diretto in PHP.
#
#   csv.writer(file)       → scrive righe nel file CSV (dalle liste)
#                            Come fputcsv() in PHP
#
#   csv.DictWriter(file)   → scrive righe nel file CSV (dai dizionari)
#
# Noi useremo DictReader per leggere (più comodo) e writer per scrivere.
#
# DictReader è fantastico perché fa ESATTAMENTE quello che abbiamo fatto
# a mano nella PARTE 3 (header → chiavi, valori → valori del dizionario),
# ma in 3 righe di codice invece di 15!

# 🔁 RINFORZO MIRATO — sorted() crea nuova lista vs .sort() in-place
# Al quiz del cap. 05, non avevi menzionato la differenza chiave tra
# sorted() e .sort(). Rivediamola:
#
#   numeri = [3, 1, 2]
#   ordinati = sorted(numeri)  # → ordinati = [1, 2, 3], numeri resta [3, 1, 2]
#   numeri.sort()              # → numeri diventa [1, 2, 3], restituisce None
#
# sorted() = FUNZIONE → crea una NUOVA lista, l'originale non cambia
# .sort()  = METODO   → modifica la lista originale, restituisce None
# Lambda NON è obbligatoria! sorted([3,1,2]) funziona benissimo senza lambda.
# Lambda serve solo quando vuoi ordinare in base a un CRITERIO personalizzato,
# come sorted(prodotti, key=lambda p: p["prezzo"]).

print("\n=== Usando il modulo csv ===")
dati_csv = []

with open(percorso_csv, "r", encoding="utf-8") as file:
    lettore = csv.DictReader(file)
    # csv.DictReader(file) crea un "lettore" che sa come interpretare il CSV.
    # NON legge il file subito! È un oggetto "pigro" (lazy): legge una riga
    # solo quando gliela chiedi nel ciclo for. Efficiente per file enormi.
    #
    # La PRIMA riga del file viene usata automaticamente come header
    # (i nomi delle chiavi dei dizionari). Non devi fare niente!

    for record in lettore:
        # Ad ogni iterazione, 'record' è un dizionario OrderedDict:
        #   {"id_ordine": "1001", "data": "2024-01-05", "prodotto": "Cuffie", ...}
        # È IDENTICO a quello che abbiamo costruito a mano nella PARTE 3!
        dati_csv.append(record)

# Confronto: PARTE 3 (manuale) vs PARTE 4 (csv.DictReader)
#
#   PARTE 3 — 15 righe di codice:
#     righe = file.readlines()
#     header = righe[0].strip().split(",")
#     for riga in righe[1:]:
#         valori = riga.strip().split(",")
#         record = {}
#         for i, colonna in enumerate(header):
#             record[colonna] = valori[i]
#         dati.append(record)
#
#   PARTE 4 — 3 righe di codice:
#     lettore = csv.DictReader(file)
#     for record in lettore:
#         dati_csv.append(record)
#
# Risultato identico. Ma csv.DictReader gestisce anche i casi complessi
# (virgole nei valori, virgolette, ecc.) che il nostro codice manuale non può.

print(f"Record totali: {len(dati_csv)}")
print(f"Primo record: {dict(dati_csv[0])}")

# dict(dati_csv[0]) converte l'OrderedDict in un dizionario normale.
# È solo per rendere la stampa più leggibile — funzionalmente è uguale.

# Da qui in poi useremo dati_csv (creato con csv.DictReader) perché
# è più affidabile del parsing manuale. Ma ora SAI cosa fa sotto il cofano!


# --- MINI-ESERCIZIO 4 — Prova subito! ---
# 1) Usando dati_csv, stampa tutti i record come dizionari in un ciclo for,
#    ma solo i primi 3 (usa enumerate e un if)
# 2) Verifica che il primo record di dati_csv sia identico al primo record
#    di 'dati' (la versione manuale). Sono uguali? Stampa entrambi.
# Scrivi qui sotto:
# ...


# ==========================================================================
# PARTE 5: Analizzare i Dati — Le "Query" in Python
# ==========================================================================

# Ora che abbiamo i dati come lista di dizionari, possiamo "interrogarli"
# come faremmo con delle query SQL... ma usando Python puro.
#
# Questo è un concetto FONDAMENTALE per la tua app documentale:
# quando leggerai le buste paga o i documenti reddituali, i dati
# arriveranno come liste di dizionari (da CSV, da JSON, da un database).
# E dovrai fare esattamente questo tipo di analisi:
#   - Contare quanti documenti per tipo
#   - Sommare importi
#   - Trovare il massimo/minimo
#   - Raggruppare per categoria
#
# Pensa a queste operazioni come alle query SQL che usi in Laravel:
#
#   SQL/Eloquent                    →  Python puro
#   ─────────────────────────────────────────────────
#   SELECT COUNT(*) GROUP BY citta  →  pattern contatore con .get()
#   SELECT SUM(prezzo * qty)        →  ciclo for con += o sum()
#   SELECT MAX(prezzo)              →  max() con lambda
#   WHERE citta = 'Milano'          →  if record["citta"] == "Milano"
#   ORDER BY prezzo DESC            →  sorted() con lambda e reverse=True
#
# La differenza è che in SQL scrivi COSA vuoi e il database capisce da solo
# COME ottenerlo. In Python devi scrivere tu il COME, passo per passo.
# Questo è più lungo, ma ti dà il CONTROLLO TOTALE su ogni passaggio.

# 🔁 RINFORZO MIRATO — .get() vs .items()
# Al quiz del cap. 05, per contare le frequenze hai confuso .items() con .get().
# Ricorda la differenza — sono due cose COMPLETAMENTE diverse:
#
#   .items()          → restituisce TUTTE le coppie (chiave, valore) del dizionario
#                       Si usa per ITERARE: for k, v in dizionario.items()
#                       NON accetta parametri!
#
#   .get(chiave, 0)   → restituisce il valore di UNA SOLA chiave
#                       Se la chiave non esiste, restituisce il default (0)
#                       Accetta 1 o 2 parametri: .get(chiave) o .get(chiave, default)
#
# Per contare frequenze, il pattern è sempre:
#   conteggio[chiave] = conteggio.get(chiave, 0) + 1
#
#   Scomposizione riga per riga (esempio: contare "Milano" per la prima volta):
#     conteggio.get("Milano", 0)   → "Milano" non esiste nel dizionario → restituisce 0
#     0 + 1                        → fa 1
#     conteggio["Milano"] = 1      → ora il dizionario ha {"Milano": 1}
#
#   Seconda volta che incontra "Milano":
#     conteggio.get("Milano", 0)   → "Milano" esiste e vale 1 → restituisce 1
#     1 + 1                        → fa 2
#     conteggio["Milano"] = 2      → ora il dizionario ha {"Milano": 2}
#
# Per iterare su un dizionario, il pattern è:
#   for chiave, valore in dizionario.items():
#   # .items() → "dammi tutte le coppie una alla volta"

# --- ATTENZIONE CRITICA: tutti i dati dal CSV sono STRINGHE! ---
#
# Quando leggi un CSV (sia a mano che con csv.DictReader), OGNI valore
# è una stringa. Anche i numeri! Questo è il "tranello" principale del CSV.
#
#   record["prezzo"]   → "49.99"  (stringa, NON un numero!)
#   record["quantita"] → "2"      (stringa, NON un numero!)
#
# Se provi a moltiplicare senza convertire:
#   "49.99" * 2   → "49.9949.99"   (ripete la stringa! Come in JS)
#   "49.99" + "2" → "49.992"       (concatena le stringhe!)
#
# Per fare calcoli matematici, DEVI convertire:
#   float("49.99")  → 49.99   (numero decimale, per prezzi/importi)
#   int("2")        → 2       (numero intero, per quantità/conteggi)
#
# Confronto a tre — conversione di tipo:
#   Python:  float("49.99")         int("2")
#   PHP:     (float)"49.99"         (int)"2"
#            floatval("49.99")      intval("2")
#   JS:      parseFloat("49.99")    parseInt("2")
#            Number("49.99")        Number("2")
#
# Errore che succede spesso: se provi int("49.99") Python dà ERRORE!
# int() funziona solo con numeri interi ("2", "100"), non con decimali.
# Per i decimali usa sempre float().

print("\n=== Analisi dei dati ===")

# QUERY 1: Quanti ordini per città? (come GROUP BY citta, COUNT(*) in SQL)
#
# In SQL scriveresti:
#   SELECT citta, COUNT(*) as conteggio FROM ordini GROUP BY citta
#
# In Laravel/Eloquent:
#   $conteggio = Order::select('citta', DB::raw('count(*) as totale'))
#                     ->groupBy('citta')->get();
#
# In Python, dobbiamo farlo "a mano" con il pattern contatore:

conteggio_citta = {}    # dizionario vuoto — ci metteremo le città e i conteggi
for record in dati_csv:
    citta = record["citta"]    # es. "Milano", "Roma", "Napoli"
    conteggio_citta[citta] = conteggio_citta.get(citta, 0) + 1
    # Prima iterazione con "Milano": .get("Milano", 0) → 0, poi 0+1=1 → {"Milano": 1}
    # Seconda "Roma": .get("Roma", 0) → 0, poi 0+1=1 → {"Milano": 1, "Roma": 1}
    # Terza "Milano" di nuovo: .get("Milano", 0) → 1, poi 1+1=2 → {"Milano": 2, "Roma": 1}
    # ...e così via per tutte le righe del CSV

# Stampiamo ordinato per conteggio decrescente (la città con più ordini prima)
# sorted() + lambda + .items(): vediamolo pezzo per pezzo
#
#   conteggio_citta.items()  → [("Milano", 5), ("Roma", 4), ("Napoli", 3), ...]
#   key=lambda x: x[1]      → ordina per il SECONDO elemento della tupla (il conteggio)
#                               x è una tupla ("Milano", 5), x[1] è 5
#   reverse=True             → dal più grande al più piccolo (decrescente)
#
#   Senza reverse, sorted() ordina dal più piccolo al più grande (crescente).

print("Ordini per città:")
for citta, conteggio in sorted(conteggio_citta.items(), key=lambda x: x[1], reverse=True):
    print(f"  {citta}: {conteggio}")

# QUERY 2: Fatturato totale (come SELECT SUM(prezzo * quantita) in SQL)
#
# In SQL: SELECT SUM(prezzo * quantita) as fatturato FROM ordini
# In Laravel: Order::sum(DB::raw('prezzo * quantita'))

fatturato = 0    # accumulatore — partiamo da 0
for record in dati_csv:
    # RICORDA: i dati dal CSV sono STRINGHE! Devi convertire.
    prezzo = float(record["prezzo"])       # "49.99" → 49.99
    quantita = int(record["quantita"])     # "2" → 2
    fatturato += prezzo * quantita         # += è "aggiungi al totale"
    # += è un'abbreviazione: fatturato = fatturato + (prezzo * quantita)
    # Come $fatturato += $prezzo * $qty; in PHP — stessa sintassi!

print(f"\nFatturato totale: {fatturato:.2f}€")
# :.2f dentro le graffe dell'f-string è un FORMATO DI STAMPA:
#   :    → "adesso specifico il formato"
#   .2   → "2 cifre dopo la virgola"
#   f    → "tipo float (numero decimale)"
# Esempio: 1234.5 → "1234.50" (aggiunge lo zero mancante)
#          1234.5678 → "1234.57" (arrotonda a 2 decimali)
#
# In PHP: number_format(1234.5, 2) → "1,234.50"
# In JS:  (1234.5).toFixed(2) → "1234.50"

# QUERY 3: Prodotto più venduto (per quantità totale)
#
# In SQL: SELECT prodotto, SUM(quantita) as totale FROM ordini
#         GROUP BY prodotto ORDER BY totale DESC LIMIT 1

vendite_prodotto = {}
for record in dati_csv:
    prodotto = record["prodotto"]
    vendite_prodotto[prodotto] = vendite_prodotto.get(prodotto, 0) + int(record["quantita"])
    # Stessa logica del contatore, ma invece di +1 aggiungiamo la quantità.
    # Se un ordine ha 3 Cuffie Bluetooth, aggiungiamo 3 (non 1).

# max() su un dizionario — ATTENZIONE, concetto importante!
# max(vendite_prodotto) → restituisce la CHIAVE con il valore alfabeticamente più grande
# max(vendite_prodotto, key=vendite_prodotto.get) → restituisce la CHIAVE il cui
#   VALORE è il più grande. vendite_prodotto.get è il metodo usato come funzione:
#   per ogni chiave, Python chiama vendite_prodotto.get(chiave) per ottenere il valore,
#   e poi sceglie la chiave con il valore più alto.
prodotto_top = max(vendite_prodotto, key=vendite_prodotto.get)
print(f"Prodotto più venduto: {prodotto_top} ({vendite_prodotto[prodotto_top]} unità)")

# 🔁 RINFORZO MIRATO — >= vs > (include o esclude il valore limite)
# Al quiz del cap. 05, hai escluso Marco (voto 7) dal filtro >= 7.
# Rivediamolo con i dati reali:
#   Pensa alla query SQL: SELECT * FROM prodotti WHERE prezzo >= 50
#   Questo INCLUDE i prodotti che costano esattamente 50€!
#
#   >= 50  → "maggiore O uguale a 50" → 50 è INCLUSO (50, 51, 100...)
#   >  50  → "strettamente maggiore di 50" → 50 è ESCLUSO (51, 100...)
#
# In PHP/JS è identico: >= include, > esclude. Nessuna differenza.

# QUERY 4: Fatturato per categoria
#
# In SQL: SELECT categoria, SUM(prezzo * quantita) as fatturato
#         FROM ordini GROUP BY categoria ORDER BY fatturato DESC
#
# Qui combiniamo due pattern che già conosci:
#   - Il pattern contatore con .get() (come nella QUERY 1)
#   - La conversione di tipo float()/int() (come nella QUERY 2)

fatturato_cat = {}
for record in dati_csv:
    cat = record["categoria"]                                  # es. "Elettronica"
    totale = float(record["prezzo"]) * int(record["quantita"]) # es. 49.99 * 2 = 99.98
    fatturato_cat[cat] = fatturato_cat.get(cat, 0) + totale    # accumula per categoria
    # Prima volta "Elettronica": .get("Elettronica", 0) → 0, poi 0 + 99.98 = 99.98
    # Seconda volta "Elettronica": .get("Elettronica", 0) → 99.98, poi 99.98 + 29.99 = 129.97

print("\nFatturato per categoria:")
for cat, tot in sorted(fatturato_cat.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {tot:.2f}€")

# --- Riepilogo dei pattern Python vs SQL ---
#
# Hai notato quanti PATTERN si ripetono? Sono sempre gli stessi:
#
#   1. CONTATORE:        dizionario.get(chiave, 0) + 1
#   2. ACCUMULATORE:     dizionario.get(chiave, 0) + valore
#   3. ORDINAMENTO:      sorted(diz.items(), key=lambda x: x[1], reverse=True)
#   4. MASSIMO:          max(diz, key=diz.get)
#   5. CONVERSIONE:      float(stringa), int(stringa)
#
# Se impari questi 5 pattern, puoi fare QUALSIASI analisi su dati CSV.
# Ritroverai questi stessi pattern in Pandas, ma sotto il cofano
# fanno esattamente queste operazioni.
#
# Nel capitolo 09 (Pandas) scoprirai che tutto questo si fa in 1-2 righe:
#   df.groupby("categoria")["prezzo"].sum()   → fatturato per categoria
# Ma ora capisci COSA fa sotto il cofano!


# --- MINI-ESERCIZIO 5 — Prova subito! ---
# Usando dati_csv e il pattern contatore con .get():
# 1) Conta quanti ordini ci sono per ogni metodo di pagamento
# 2) Trova il metodo di pagamento più usato (usa max() con lambda o .get)
# 3) Filtra solo gli ordini con prezzo >= 50 (attenzione: il prezzo è una
#    stringa nel CSV! Devi convertirlo con float())
#    Quanti ordini hanno prezzo >= 50?
# Scrivi qui sotto:
# ...


# ==========================================================================
# PARTE 6: Scrivere un File CSV — Salvare i Risultati
# ==========================================================================

# Finora abbiamo solo LETTO. Ma nella tua app documentale, vorrai anche
# SCRIVERE risultati su file: report di analisi, export per il cliente,
# log delle anomalie trovate, ecc.
#
# Scrivere un file è concettualmente l'opposto di leggere:
#   Leggere:  FILE → Python (i dati entrano nel programma)
#   Scrivere: Python → FILE (i dati escono dal programma e vanno sul disco)
#
# --- Le modalità di apertura per la scrittura ---
#
# Quando apri un file per scrivere, devi scegliere la modalità:
#
#   'w' = write (scrittura) — CANCELLA tutto il contenuto del file e
#         ricomincia da zero. Se il file non esiste, lo CREA.
#         ATTENZIONE: è distruttivo! Tutto ciò che c'era prima viene perso.
#         Come quando in Laravel fai php artisan migrate:fresh — riparti da zero.
#
#   'a' = append (aggiunta) — AGGIUNGE in fondo al file senza cancellare
#         quello che c'era prima. Se il file non esiste, lo CREA.
#         Come quando fai INSERT INTO in SQL — aggiungi righe alla tabella.
#
#   'x' = exclusive creation — crea il file, ma dà ERRORE se esiste già.
#         Utile per evitare di sovrascrivere file importanti per sbaglio.
#
# --- Confronto a tre — scrivere un file ---
#
# PHP:
#   $file = fopen('output.csv', 'w');              // apre in scrittura
#   fputcsv($file, ['colonna1', 'colonna2']);       // scrive una riga CSV
#   // fputcsv() prende un array e lo scrive come riga CSV con le virgole
#   // ['colonna1', 'colonna2'] diventa "colonna1,colonna2\n" nel file
#   fputcsv($file, ['valore1', 'valore2']);         // scrive un'altra riga
#   fclose($file);                                 // chiude il file
#
#   // Alternativa semplice:
#   file_put_contents('output.csv', "colonna1,colonna2\nvalore1,valore2");
#   // Scrive tutto in un colpo. Come file_get_contents() ma al contrario.
#
# JavaScript (Node.js):
#   const fs = require('fs');
#   fs.writeFileSync('output.csv', 'colonna1,colonna2\nvalore1,valore2');
#   // writeFileSync() scrive l'intera stringa nel file in un colpo.
#   // Non ha un equivalente di fputcsv() — devi costruire la stringa a mano
#   // o usare una libreria come 'csv-stringify'.
#
# Python:
#   with open('output.csv', 'w', encoding='utf-8', newline='') as file:
#       scrittore = csv.writer(file)
#       scrittore.writerow(['colonna1', 'colonna2'])   # scrive una riga
#       scrittore.writerow(['valore1', 'valore2'])     # scrive un'altra riga
#
# --- Cos'è newline=""? ---
# Su Windows, andare a capo è rappresentato da DUE caratteri: \r\n
# Su Mac/Linux, è un solo carattere: \n
# Il modulo csv aggiunge già i suoi "a capo". Se non metti newline="",
# su Windows ottieni DOPPI "a capo" → righe vuote tra una riga e l'altra!
# newline="" dice a Python: "non aggiungere a capo automatici, lascia
# fare al modulo csv". È un problema solo su Windows.
#
# --- round() — arrotondare i numeri ---
# round(numero, decimali) arrotonda un numero.
#   round(3.14159, 2)  → 3.14
#   round(49.999, 2)   → 50.0
#   round(100.5)       → 100 (senza il secondo parametro, arrotonda all'intero)
#
# In PHP: round(3.14159, 2) → identica sintassi!
# In JS:  (3.14159).toFixed(2) → "3.14" (restituisce una STRINGA, attenzione!)
#         oppure Math.round(3.14159 * 100) / 100 → 3.14 (come numero)

percorso_output = os.path.join(percorso_dati, "report_categorie.csv")

with open(percorso_output, "w", encoding="utf-8", newline="") as file:
    scrittore = csv.writer(file)
    # csv.writer(file) crea un oggetto "scrittore" che sa come formattare
    # i dati in formato CSV (aggiunge virgole, virgolette se servono, ecc.)

    # Scriviamo l'header (la riga con i nomi delle colonne)
    scrittore.writerow(["categoria", "fatturato_totale", "num_ordini"])
    # .writerow() prende una LISTA e la scrive come riga CSV.
    # ["categoria", "fatturato_totale", "num_ordini"]
    # diventa nel file: "categoria,fatturato_totale,num_ordini\n"

    # Calcoliamo i dati — usiamo i dizionari calcolati nella PARTE 5
    conteggio_cat = {}
    for record in dati_csv:
        cat = record["categoria"]
        conteggio_cat[cat] = conteggio_cat.get(cat, 0) + 1

    # Scriviamo una riga per ogni categoria
    for cat in fatturato_cat:
        scrittore.writerow([cat, round(fatturato_cat[cat], 2), conteggio_cat.get(cat, 0)])
        # Esempio: ["Elettronica", 1249.75, 8]
        # diventa nel file: "Elettronica,1249.75,8\n"

print(f"\nReport salvato in: {percorso_output}")

# Vai nella cartella dati/ e apri "report_categorie.csv" per vedere il risultato!
# Puoi anche aprirlo con Excel o Google Sheets — è un CSV valido.


# --- MINI-ESERCIZIO 6 — Prova subito! ---
# 1) Crea un file CSV chiamato "ordini_milano.csv" nella cartella dati/
#    che contenga solo gli ordini della città "Milano"
#    (header + righe filtrate)
# 2) Verifica che il file sia stato creato leggendolo e stampando
#    il numero di righe
# Scrivi qui sotto:
# ...


# 🔁 RINFORZO MIRATO — Output concreto vs descrizione concettuale
# Al quiz del cap. 05, alla domanda "cosa stampa?" hai DESCRITTO cosa fa
# il codice ("restituisce una lista in cui...") invece di dare il VALORE
# concreto (["Marco"]). Quando una domanda chiede "cosa stampa/cosa
# restituisce", devi dare il RISULTATO ESATTO, non la spiegazione.
#
# Esempio:
#   Domanda: "Cosa stampa print([1,2,3][1:])?"
#   ❌ "Stampa una sotto-lista dal secondo elemento in poi"
#   ✅ [2, 3]
#
# Prova subito — dai la risposta CONCRETA:
# 1) Cosa stampa: print({"a": 1, "b": 2}["a"])
#    La tua risposta: ___
# 2) Cosa stampa: print(len([10, 20, 30, 40]))
#    La tua risposta: ___
# 3) Cosa stampa: print("ciao mondo".split(" "))
#    La tua risposta: ___
# Scrivi qui sotto:
# ...


# 🔁 RINFORZO MIRATO — Variabile corretta nelle comprehension
# Al quiz del cap. 05, hai scritto [n*n for n in range(1,11) if x % 2 == 0]
# La variabile del for era "n" ma nell'if hai usato "x" — errore!
# La variabile deve essere LA STESSA in tutto il ciclo.
#
# Regola: guarda il "for X in ..." — la X è il nome della variabile.
# Tutto il resto (espressione a sinistra, condizione a destra) deve
# usare quella STESSA variabile.
#
#   ✅ [n*2 for n in range(10) if n > 3]     ← tutto "n"
#   ❌ [n*2 for n in range(10) if x > 3]     ← "x" non esiste!
#   ✅ [r["citta"] for r in dati_csv if r["prezzo"] == "49.99"]  ← tutto "r"
#
# Prova subito:
# 1) Scrivi una list comprehension che crea una lista con i nomi dei prodotti
#    dal CSV che costano più di 40€ (ricorda: float() per convertire)
# Scrivi qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ DI VERIFICA — Hai capito la teoria?                            ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti di QUESTO capitolo (File CSV).
# Rispondi DOPO aver letto la teoria, PRIMA di fare gli esercizi.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — Vero o Falso?
# "with open('file.csv', 'r') as f: apre il file e lo chiude automaticamente
#  quando il blocco with finisce"
# La tua risposta (V/F): ___

# DOMANDA 2 — Prevedi l'output:
# Cosa stampa questo codice?
#   riga = "  ciao mondo  \n"
#   print(riga.strip())
# La tua risposta: ___

# DOMANDA 3 — Completa il codice:
# Voglio leggere un CSV e trasformare ogni riga in un dizionario:
#   with open('file.csv', 'r') as f:
#       lettore = csv.___(f)
#       for record in lettore:
#           print(record)
# Riempi lo spazio: ___

# DOMANDA 4 — Trova l'errore:
#   with open('dati.csv', 'r') as f:
#       righe = f.readlines()
#       for riga in righe:
#           valori = riga.split(",")
#           prezzo = valori[2] * 2   # voglio raddoppiare il prezzo
# Qual è il problema?
# La tua risposta: ___

# DOMANDA 5 — Prevedi l'output:
#   header = "nome,prezzo,citta"
#   colonne = header.strip().split(",")
#   print(len(colonne))
# La tua risposta: ___

# DOMANDA 6 — Vero o Falso?
# "I dati letti da un file CSV con csv.DictReader sono già del tipo
#  giusto: i numeri sono int/float e le stringhe sono str"
# La tua risposta (V/F): ___

# DOMANDA 7 — Definizione:
# Cosa fa il metodo .split(",") applicato a una stringa?
# A cosa corrisponde in PHP?
# La tua risposta: ___

# DOMANDA 8 — 💬 Spiega con parole tue (Tecnica Feynman):
# Spiega a un collega che non sa Python come funziona il parsing manuale
# di un file CSV: dall'apertura del file fino ad avere una lista di
# dizionari. Non usare codice, solo parole.
# La tua spiegazione: ___


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- ESERCIZIO 1 (Livello 1 — Leggi e Modifica): ---
# Usando la lista 'dati_csv' già caricata:
# a) Stampa tutti gli ordini pagati con "PayPal"
# b) Conta quanti ordini ci sono per ogni metodo di pagamento
#    (usa il pattern contatore con .get())
# c) Stampa il risultato ordinato per conteggio decrescente
#    (usa sorted() con lambda e reverse=True)
#
# Scrivi il tuo codice qui sotto:
# ...


# --- ESERCIZIO 2 (Livello 2 — Scrivi da Zero): ---
# Scrivi una funzione 'cerca_ordini(dati, **filtri)' che:
#   1. Prende una lista di dizionari e dei filtri con **kwargs
#   2. Restituisce tutti i record che corrispondono a TUTTI i filtri
#   3. La funzione deve avere una docstring
#
# RIPASSO — **kwargs: ricordi? Come lo spread operator {...} in JS.
# **filtri raccoglie tutti i parametri con nome in un dizionario:
#   cerca_ordini(dati, citta="Milano")  → filtri = {"citta": "Milano"}
#   cerca_ordini(dati, citta="Roma", categoria="Libri")
#     → filtri = {"citta": "Roma", "categoria": "Libri"}
#
# Testa con:
#   cerca_ordini(dati_csv, citta="Milano")
#   cerca_ordini(dati_csv, categoria="Elettronica", citta="Roma")
#
# Scrivi il tuo codice qui sotto:
# ...


# 🎯 [COLLOQUIO] — ESERCIZIO 3 (Livello 2 — Analisi dati):
# Questo tipo di esercizio è molto comune nei colloqui per posizioni
# che richiedono analisi dati: "dato un CSV, trovami queste informazioni".
#
# Leggi il file 'case.csv' (nella cartella dati/) e:
# a) Calcola il prezzo medio delle case per ogni città
#    (suggerimento: ti servono due dizionari — somma_prezzi e conteggio)
# b) Trova la casa più costosa e stampa TUTTE le sue caratteristiche
#    (suggerimento: max() con lambda su float(casa["prezzo_euro"]))
# c) Stampa le case ordinate per metri quadri crescenti in formato:
#    "45mq → 125.000€ (Milano)"
#    (suggerimento: sorted() con lambda su int(casa["metri_quadri"]))
# La funzione deve avere una docstring.
#
# Scrivi il tuo codice qui sotto:
# ...


# --- ESERCIZIO 4 (Livello 3 — Web Bridge): ---
# Scrivi una funzione 'csv_to_html_table(percorso_file)' che:
#   - Legge un file CSV
#   - Genera una stringa HTML con una <table> completa
#   - Include <thead> con i nomi colonne e <tbody> con i dati
#   - La funzione deve avere una docstring
# Questo è un vero "ponte" tra il mondo dei dati e il web!
# In Laravel, faresti una view Blade con un @foreach. Qui generi
# l'HTML direttamente in Python — utile per report email o PDF.
#
# Testa con: csv_to_html_table(percorso_csv)
# Stampa i primi 500 caratteri del risultato.
#
# Scrivi il tuo codice qui sotto:
# ...


# --- ESERCIZIO 5 — 🔧 [REFACTORING]: ---
# Il codice qui sotto FUNZIONA, ma è scritto male.
# Riscrivilo usando i concetti di questo capitolo per renderlo più
# pulito, leggibile e Pythonico.
#
# Codice da migliorare:
#   f = open(percorso_csv, "r")
#   lines = f.readlines()
#   f.close()
#   h = lines[0].strip().split(",")
#   result = []
#   i = 1
#   while i < len(lines):
#       v = lines[i].strip().split(",")
#       d = {}
#       j = 0
#       while j < len(h):
#           d[h[j]] = v[j]
#           j = j + 1
#       result.append(d)
#       i = i + 1
#   tot = 0
#   for x in result:
#       tot = tot + float(x["prezzo"]) * float(x["quantita"])
#   print(tot)
#
# Requisiti del refactoring:
# 1. Usa 'with open(...)' invece di open() + close()
# 2. Usa csv.DictReader invece del parsing manuale
# 3. Usa sum() con generator expression invece del ciclo per il totale
# 4. Usa nomi di variabili descrittivi (non f, h, v, d, j, x)
# 5. Usa for invece di while dove possibile
#
# Scrivi il tuo codice qui sotto:
# ...


# --- ESERCIZIO 6 — 🔀 [INTERLEAVING]: ---
# Questo esercizio mescola concetti del cap. 06 (CSV) con cap. 04 (liste)
# e cap. 05 (dizionari).
#
# Usando dati_csv:
# a) Crea una LISTA con solo i nomi dei prodotti unici (senza duplicati)
#    usando il pattern "if not in" dal cap. 04
# b) Crea un DIZIONARIO che mappa ogni prodotto al suo prezzo medio
#    (usa due dizionari: somma e conteggio, come nell'ex. 3)
# c) Ordina il dizionario per prezzo medio decrescente con sorted() + lambda
# d) Stampa il risultato con enumerate numerato da 1:
#    "1. Cuffie Bluetooth: prezzo medio 49.99€"
#
# Scrivi il tuo codice qui sotto:
# ...


# --- ESERCIZIO 7 — 🧠 [RETRIEVAL]: ---
# Senza guardare il codice del capitolo 05, riscrivi da zero la funzione
# 'conta_parole(testo)' dell'esercizio 4 del cap. 05.
# Requisiti (gli stessi dell'originale):
#   1. Prende una stringa di testo
#   2. Restituisce un dizionario con ogni parola e quante volte appare
#   3. Le parole devono essere tutte in minuscolo
#   4. La funzione deve avere una docstring
# Testa con: "Il gatto e il cane e il pesce"
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  🏗️ PROGETTO INCREMENTALE — Catalogo E-commerce                      ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# In questo capitolo aggiungi al progetto: CARICAMENTO DA FILE CSV
# Invece di scrivere i prodotti nel codice, li carichi da un file CSV!
#
# Task:
# 1) Crea un file "catalogo.csv" nella cartella dati/ con queste colonne:
#    id,nome,prezzo,categoria,stock
#    Mettici almeno 8 prodotti di categorie diverse (Elettronica, Libri,
#    Abbigliamento, Accessori)
#
# 2) Scrivi una funzione 'carica_catalogo(percorso)' che:
#    - Legge il CSV con csv.DictReader
#    - Converte prezzo a float e stock a int
#    - Restituisce una lista di dizionari
#    - Ha una docstring
#
# 3) Scrivi una funzione 'salva_catalogo(catalogo, percorso)' che:
#    - Prende la lista di dizionari e un percorso file
#    - Scrive il CSV con csv.writer (header + dati)
#    - Ha una docstring
#
# 4) Scrivi una funzione 'report_catalogo(catalogo)' che stampa:
#    - Numero totale di prodotti
#    - Valore totale dell'inventario (somma di prezzo * stock per ogni prodotto)
#    - Prodotto più costoso
#    - Categorie disponibili con conteggio prodotti
#
# Questo progetto attraversa tutto il corso — ogni capitolo aggiunge
# un pezzo. Alla fine avrai un sistema completo di gestione catalogo.

# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- RISPOSTE QUIZ D'INGRESSO (Cap. 05 — Dizionari) ---
#
# 1. 3
#    → Parte con 2 chiavi, poi aggiunge "lavoro" → diventa 3.
#
# 2. {"mela": 1.50, "kiwi": 2.00}
#    → >= 1.50: mela (1.50) e kiwi (2.00) passano, banana (0.80) no.
#    Nota: 1.50 è INCLUSO perché usiamo >= (maggiore O UGUALE).
#
# 3. VERO
#    → .get() restituisce il default ma NON modifica il dizionario.
#    .setdefault() invece aggiunge la chiave se non esiste.
#
# 4. Il metodo sbagliato: .items() invece di .get()
#    → .items() restituisce tutte le coppie, non accetta parametri così.
#    Corretto: conteggio.get(parola, 0) + 1
#
# 5. enumerate, items
#    → enumerate(inventario.items(), 1)
#
# 6. Roma
#    → Si accede ai dizionari annidati con le parentesi quadre a catena.
#
# 7. .setdefault(k, v) aggiunge k con valore v SOLO se k non esiste.
#    .update(dict2) aggiunge/sovrascrive TUTTE le chiavi di dict2.
#    setdefault è "cauto" (non tocca l'esistente), update è "aggressivo".
#
# 8. 1
#    → .copy() crea una copia indipendente. Modificare la copia
#    non tocca l'originale. d["a"] resta 1.

# --- RISPOSTE QUIZ DI VERIFICA (Cap. 06 — File CSV) ---
#
# 1. VERO
#    → with ... as f: chiude il file automaticamente. Come try-finally.
#
# 2. ciao mondo
#    → .strip() rimuove spazi e \n a inizio e fine, ma non in mezzo.
#
# 3. DictReader
#    → csv.DictReader(f) trasforma ogni riga in un dizionario.
#
# 4. valori[2] è una STRINGA (tutti i dati CSV sono stringhe)!
#    "29.99" * 2 in Python dà "29.9929.99" (ripete la stringa).
#    Serve: float(valori[2]) * 2 per fare la moltiplicazione numerica.
#
# 5. 3
#    → "nome,prezzo,citta".split(",") dà ["nome", "prezzo", "citta"],
#    che ha 3 elementi.
#
# 6. FALSO
#    → csv.DictReader restituisce TUTTO come stringhe! Anche i numeri.
#    "49.99" è una stringa, non un float. Devi convertire con float()/int().
#
# 7. .split(",") divide la stringa in una lista usando la virgola come
#    separatore. In PHP è explode(",", $stringa). In JS è stringa.split(",").
#
# 8. (Risposta libera — valutata dal mentor sulla chiarezza)
#    Un buon esempio: "Apri il file, leggi tutte le righe. La prima riga
#    sono i nomi delle colonne. Per ogni riga successiva, dividi il testo
#    in pezzi usando la virgola. Poi crea un dizionario abbinando ogni
#    nome di colonna al pezzo corrispondente. Alla fine hai una lista
#    di dizionari — come un array di oggetti in JavaScript."

# --- SOLUZIONE ESERCIZIO 1 ---
# # a) Ordini PayPal
# print("Ordini PayPal:")
# for r in dati_csv:
#     if r["metodo_pagamento"] == "PayPal":
#         print(f"  #{r['id_ordine']} - {r['prodotto']} ({r['citta']})")
#
# # b) Conteggio per metodo
# conteggio_metodo = {}
# for r in dati_csv:
#     metodo = r["metodo_pagamento"]
#     conteggio_metodo[metodo] = conteggio_metodo.get(metodo, 0) + 1
#
# # c) Ordinato
# for metodo, cnt in sorted(conteggio_metodo.items(), key=lambda x: x[1], reverse=True):
#     print(f"  {metodo}: {cnt} ordini")

# --- SOLUZIONE ESERCIZIO 2 ---
# def cerca_ordini(dati, **filtri):
#     """Filtra una lista di dizionari in base ai filtri passati.
#     Restituisce solo i record che corrispondono a TUTTI i filtri.
#     Come un WHERE con AND in SQL."""
#     risultati = []
#     for record in dati:
#         corrisponde = True
#         for chiave, valore in filtri.items():
#             if record.get(chiave) != valore:
#                 corrisponde = False
#                 break
#         if corrisponde:
#             risultati.append(record)
#     return risultati
#
# ordini_milano = cerca_ordini(dati_csv, citta="Milano")
# print(f"Ordini a Milano: {len(ordini_milano)}")
# ordini_elett_roma = cerca_ordini(dati_csv, categoria="Elettronica", citta="Roma")
# print(f"Elettronica a Roma: {len(ordini_elett_roma)}")

# --- SOLUZIONE ESERCIZIO 3 (Analisi case.csv 🎯) ---
# percorso_case = os.path.join(percorso_dati, "case.csv")
# case = []
# with open(percorso_case, "r", encoding="utf-8") as f:
#     lettore = csv.DictReader(f)
#     for r in lettore:
#         case.append(r)
#
# # a) Prezzo medio per città
# somma_citta = {}
# conteggio_citta_case = {}
# for casa in case:
#     c = casa["citta"]
#     p = float(casa["prezzo_euro"])
#     somma_citta[c] = somma_citta.get(c, 0) + p
#     conteggio_citta_case[c] = conteggio_citta_case.get(c, 0) + 1
# print("Prezzo medio per città:")
# for c in somma_citta:
#     print(f"  {c}: {somma_citta[c]/conteggio_citta_case[c]:,.0f}€")
#
# # b) Casa più costosa
# piu_cara = max(case, key=lambda c: float(c["prezzo_euro"]))
# print(f"\nCasa più costosa:")
# for k, v in piu_cara.items():
#     print(f"  {k}: {v}")
#
# # c) Ordinati per mq
# case_ordinate = sorted(case, key=lambda c: int(c["metri_quadri"]))
# print("\nCase ordinate per mq:")
# for c in case_ordinate:
#     print(f"  {c['metri_quadri']}mq → {int(c['prezzo_euro']):,}€ ({c['citta']})")

# --- SOLUZIONE ESERCIZIO 4 (Web Bridge — CSV to HTML) ---
# def csv_to_html_table(percorso_file):
#     """Legge un file CSV e genera una tabella HTML completa.
#     Come una view Blade con @foreach, ma in Python puro."""
#     html = '<table border="1" style="border-collapse: collapse; font-family: sans-serif;">\n'
#     with open(percorso_file, "r", encoding="utf-8") as f:
#         lettore = csv.reader(f)
#         header = next(lettore)
#         html += "  <thead><tr>\n"
#         for col in header:
#             html += f'    <th style="padding: 8px; background: #f0f0f0;">{col}</th>\n'
#         html += "  </tr></thead>\n  <tbody>\n"
#         for riga in lettore:
#             html += "    <tr>\n"
#             for val in riga:
#                 html += f'      <td style="padding: 8px;">{val}</td>\n'
#             html += "    </tr>\n"
#         html += "  </tbody>\n</table>"
#     return html
#
# html = csv_to_html_table(percorso_csv)
# print(html[:500])

# --- SOLUZIONE ESERCIZIO 5 (Refactoring 🔧) ---
# with open(percorso_csv, "r", encoding="utf-8") as file:
#     lettore = csv.DictReader(file)
#     ordini = list(lettore)
#
# fatturato_totale = sum(float(o["prezzo"]) * int(o["quantita"]) for o in ordini)
# print(f"Fatturato totale: {fatturato_totale:.2f}€")

# --- SOLUZIONE ESERCIZIO 6 (Interleaving 🔀) ---
# # a) Prodotti unici
# prodotti_unici = []
# for r in dati_csv:
#     if r["prodotto"] not in prodotti_unici:
#         prodotti_unici.append(r["prodotto"])
#
# # b) Prezzo medio per prodotto
# somma_prezzi = {}
# conteggio_prezzi = {}
# for r in dati_csv:
#     nome = r["prodotto"]
#     prezzo = float(r["prezzo"])
#     somma_prezzi[nome] = somma_prezzi.get(nome, 0) + prezzo
#     conteggio_prezzi[nome] = conteggio_prezzi.get(nome, 0) + 1
#
# prezzo_medio = {nome: round(somma_prezzi[nome] / conteggio_prezzi[nome], 2)
#                 for nome in somma_prezzi}
#
# # c) Ordinato per prezzo decrescente
# ordinati = sorted(prezzo_medio.items(), key=lambda x: x[1], reverse=True)
#
# # d) Stampa con enumerate
# for i, (nome, media) in enumerate(ordinati, 1):
#     print(f"{i}. {nome}: prezzo medio {media}€")

# --- SOLUZIONE ESERCIZIO 7 (Retrieval 🧠 — conta_parole dal cap.05) ---
# def conta_parole(testo):
#     """Conta le occorrenze di ogni parola nel testo.
#     Le parole vengono convertite in minuscolo."""
#     conteggio = {}
#     for parola in testo.lower().split():
#         conteggio[parola] = conteggio.get(parola, 0) + 1
#     return conteggio
#
# print(conta_parole("Il gatto e il cane e il pesce"))
# # {'il': 3, 'gatto': 1, 'e': 2, 'cane': 1, 'pesce': 1}

# --- SOLUZIONE PROGETTO INCREMENTALE ---
# # 1) Il file catalogo.csv va creato manualmente nella cartella dati/
# # Contenuto esempio:
# # id,nome,prezzo,categoria,stock
# # 1,Cuffie Bluetooth,49.99,Elettronica,25
# # 2,T-Shirt Nera,19.99,Abbigliamento,50
# # 3,Mouse Wireless,29.99,Elettronica,30
# # 4,Libro Python,35.00,Libri,15
# # 5,Zaino Laptop,65.00,Accessori,10
# # 6,Tastiera Meccanica,89.99,Elettronica,12
# # 7,Felpa Grigia,39.99,Abbigliamento,20
# # 8,Libro AI,42.00,Libri,8
#
# # 2) Carica catalogo
# def carica_catalogo(percorso):
#     """Carica un catalogo prodotti da file CSV.
#     Converte prezzo a float e stock a int."""
#     catalogo = []
#     with open(percorso, "r", encoding="utf-8") as f:
#         lettore = csv.DictReader(f)
#         for prodotto in lettore:
#             prodotto["prezzo"] = float(prodotto["prezzo"])
#             prodotto["stock"] = int(prodotto["stock"])
#             catalogo.append(prodotto)
#     return catalogo
#
# # 3) Salva catalogo
# def salva_catalogo(catalogo, percorso):
#     """Salva il catalogo su file CSV."""
#     if not catalogo:
#         return
#     with open(percorso, "w", encoding="utf-8", newline="") as f:
#         scrittore = csv.DictWriter(f, fieldnames=catalogo[0].keys())
#         scrittore.writeheader()
#         scrittore.writerows(catalogo)
#
# # 4) Report catalogo
# def report_catalogo(catalogo):
#     """Stampa un report riassuntivo del catalogo."""
#     print(f"Prodotti totali: {len(catalogo)}")
#     valore = sum(p["prezzo"] * p["stock"] for p in catalogo)
#     print(f"Valore inventario: {valore:.2f}€")
#     piu_costoso = max(catalogo, key=lambda p: p["prezzo"])
#     print(f"Più costoso: {piu_costoso['nome']} ({piu_costoso['prezzo']}€)")
#     categorie = {}
#     for p in catalogo:
#         categorie[p["categoria"]] = categorie.get(p["categoria"], 0) + 1
#     for cat, cnt in categorie.items():
#         print(f"  {cat}: {cnt} prodotti")
