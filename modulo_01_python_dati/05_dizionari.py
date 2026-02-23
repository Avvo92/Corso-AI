"""
============================================================================
 MODULO 1 — ESERCIZIO 05: I Dizionari
 Dizionari, Iterazione, Nesting, Metodi Utili
============================================================================

 TEORIA: Dizionari Python = Array Associativi PHP = Oggetti JavaScript

 Se conosci gli array associativi PHP o gli oggetti JavaScript,
 i dizionari Python sono lo stesso concetto: contenitori "chiave-valore".

 Confronto a tre:

   PHP (array associativo):
     $utente = ["nome" => "Luca", "eta" => 30];
     // Le chiavi sono stringhe tra virgolette
     // Si usa => (freccia grossa) per associare chiave e valore
     // Accesso: $utente["nome"]

   JavaScript (oggetto):
     const utente = { nome: "Luca", eta: 30 };
     // Le chiavi possono essere SENZA virgolette
     // Si usa : (due punti) per associare chiave e valore
     // Accesso: utente.nome  oppure  utente["nome"]

   Python (dizionario):
     utente = {"nome": "Luca", "eta": 30}
     // Le chiavi DEVONO avere le virgolette (se sono stringhe)
     // Si usa : (due punti) come JS
     // Accesso: utente["nome"]  oppure  utente.get("nome")
     // NON puoi fare utente.nome (quello è per gli oggetti/classi)

 RIASSUNTO SINTASSI:
   PHP:        ["chiave" => "valore"]    accesso: $arr["chiave"]
   JavaScript: { chiave: "valore" }      accesso: obj.chiave
   Python:     {"chiave": "valore"}      accesso: dict["chiave"]

 Perché servono per l'AI?
   - Un dataset è spesso una lista di dizionari (come un array di oggetti JSON)
   - I parametri di un modello AI sono organizzati in dizionari
   - Le risposte delle API (OpenAI, HuggingFace) sono dizionari
   - Un DataFrame Pandas è essenzialmente un dizionario di liste

============================================================================
"""

# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ D'INGRESSO — Rispondi PRIMA di leggere la teoria!              ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti del CAPITOLO 04 (Liste).
# Rispondi senza guardare il codice — servono a capire cosa hai interiorizzato.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — Prevedi l'output:
# Cosa stampa questo codice?
#   numeri = [10, 20, 30, 40, 50]
#   print(numeri[1:4])
# La tua risposta: [20, 30, 40, 50]

# DOMANDA 2 — Vero o Falso?
# "Il metodo .append() restituisce la lista modificata"
# La tua risposta (V/F): V

# DOMANDA 3 — Completa il codice:
# Voglio stampare ogni frutto con il suo numero (partendo da 1):
#   frutti = ["mela", "pera", "banana"]
#   for i, frutto in range(frutti, len(frutti)):
#       print(f"{i}. {frutto}")
# Riempi i due spazi: ok

# DOMANDA 4 — Trova l'errore:
#   prezzi = [10, 20, 30, 40, 50]
#   ultimi_tre = prezzi[3:]
#   print(ultimi_tre)   # Volevo [30, 40, 50] ma ottengo qualcos'altro
# Qual è il problema? il problema è che lo start dell slicing doveva essere [1:]

# DOMANDA 5 — Definizione:
# Cosa fa la funzione sorted() applicata a una lista?
# Che differenza c'è tra sorted(lista) e lista.sort()?
# La tua risposta: la funzione sorted serve per ordinare un lista secondo un determinato criterio
# nel primo caso è chiamata come funzione nel secondo come metodo, in ogni caso si una con la lambda function

# DOMANDA 6 — Prevedi l'output:
# Cosa stampa questo codice?
#   nomi = ["Marco", "Anna", "Luca"]
#   risultato = list(filter(lambda n: len(n) > 4, nomi))
#   print(risultato)
# La tua risposta: restituisce una lista (non sovrascrive l'originale) in cui
# i nomi hanno lunghezza maggiore di 4

# DOMANDA 7 — Vero o Falso?
# "La list comprehension [x*2 for x in lista if x > 3] prima filtra
#  gli elementi maggiori di 3, poi li raddoppia"
# La tua risposta (V/F): V

# DOMANDA 8 — Completa il codice:
# Voglio creare una lista con i quadrati dei numeri pari da 1 a 10:
#   quadrati_pari = [n*n  for n in range(1, 11)  if x % 2 == 0]
# Riempi i due spazi: ok

# 📝 CORREZIONE MENTOR — Quiz d'Ingresso (Cap. 04):
#
# D1: ❌ Hai scritto [20, 30, 40, 50] — sono 4 elementi.
#     Risposta corretta: [20, 30, 40] — l'indice 4 è ESCLUSO.
#     numeri[1:4] prende indici 1, 2, 3 → [20, 30, 40].
#     (Pattern #2 — range/slicing fine escluso: persiste)
#
# D2: ❌ Hai scritto V (Vero).
#     Risposta corretta: FALSO. .append() restituisce None.
#     Modifica la lista in-place ma non la restituisce.
#     In JS, .push() restituisce la nuova lunghezza — diverso!
#
# D3: ❌ Hai scritto "ok" ma il codice contiene errori.
#     Il codice ha range(frutti, len(frutti)) — doveva essere:
#     enumerate(frutti, 1). range() genera numeri, enumerate() dà
#     indice+valore. (Pattern #8 — enumerate vs range)
#
# D4: ⚠️ Parziale. Hai detto "doveva essere [1:]" — ma [1:] dà
#     [20,30,40,50], non [30,40,50]. L'indice di 30 è 2, non 1.
#     Corretto: prezzi[2:]. (Contare da 0: 10=indice0, 20=1, 30=2)
#
# D5: ⚠️ Parziale. Hai capito che sorted ordina, ma mancano due cose:
#     - sorted() crea una NUOVA lista, .sort() modifica l'originale
#     - lambda NON è obbligatoria: sorted([3,1,2]) funziona senza lambda
#
# D6: ⚠️ Hai descritto cosa fa, ma la domanda chiedeva l'OUTPUT concreto.
#     Risposta corretta: ["Marco"]. Devi dare il valore, non la spiegazione.
#
# D7: ✅ Corretto!
#
# D8: ❌ Hai scritto "ok" ma c'è un errore nel codice: la variabile nel
#     if è "x" ma nel for si chiama "n". Doveva essere: if n % 2 == 0
#     (Pattern #12 — variabile sbagliata nel contesto)
#
# Risultato: 1/8 corrette, 2/8 parziali, 5/8 sbagliate
# Lacune principali: slicing fine escluso, .append() restituisce None,
# enumerate vs range, output concreto vs descrizione, nomi variabili


# ==========================================================================
# PARTE 1: Creare e Accedere ai Dizionari
# ==========================================================================

# RIPASSO — f-string: ricordi? Sono le stringhe con la f davanti che ti
# permettono di mettere variabili dentro {} — come i template literal
# `${variabile}` in JS o "$variabile" in PHP. Le usiamo in tutto il file.

# Creare un dizionario:
utente = {
    "nome": "Marco",
    "cognome": "Rossi",
    "eta": 28,
    "citta": "Milano",
    "lingue": ["Python", "JavaScript", "PHP"],
    "is_developer": True
}

print("=== Dizionario utente ===")
print(utente)

# Accedere ai valori:
# PHP:         $utente["nome"]                — sempre con le parentesi quadre
# JavaScript:  utente.nome  o  utente["nome"] — col punto O con le parentesi
# Python:      utente["nome"]  o  utente.get("nome")

print(f"\nNome: {utente['nome']}")
print(f"Lingue: {utente['lingue']}")
print(f"Prima lingua: {utente['lingue'][0]}")  # Lista dentro dizionario!

# .get() — Accedere a una chiave che potrebbe NON esistere:
#
# PHP:  $utente["indirizzo"] ?? "Non specificato"
#       // L'operatore ?? (null coalescing) restituisce il valore a destra
#       // se la chiave non esiste o è null. Introdotto in PHP 7.
#       // Senza ??, accedere a una chiave inesistente dà un Warning.
#
# JS:   utente?.indirizzo ?? "Non specificato"
#       // ?. è l'optional chaining: se indirizzo non esiste, restituisce undefined
#       // ?? è il nullish coalescing: se il valore è null/undefined, usa il default
#
# Python: utente.get("indirizzo", "Non specificato")
#       // .get(chiave, default) restituisce il default se la chiave non esiste
#       // Se usi utente["indirizzo"] e la chiave non esiste → KeyError! (crash)

print(f"\nIndirizzo: {utente.get('indirizzo', 'Non specificato')}")
# Se usi utente["indirizzo"] e la chiave non esiste → KeyError! (crash)
# Con .get() invece ottieni il valore di default senza crash.

# --- MINI-ESERCIZIO 1 — Prova subito! ---
# Crea un dizionario 'auto' con chiavi: marca, modello, anno, km.
# Poi:
# 1) Stampa marca e modello in una f-string
# 2) Accedi alla chiave "colore" con .get() usando un default "sconosciuto"
# Scrivi qui sotto:
# auto = {
#     "marca":"Fiat",
#     "modello":"500",
#     "anno":2020,
#     "km":30000
# }
# print(f"Marca: {auto['marca']}, Modello: {auto['modello']}")
# print(f"Colore: {auto.get('colore', 'sconosciuto')}")



# ==========================================================================
# PARTE 2: Modificare un Dizionario
# ==========================================================================

# Aggiungere o modificare una chiave:
utente["email"] = "marco@email.com"  # Aggiunge (non esisteva)
utente["eta"] = 29                   # Modifica (già esisteva)
print(f"\nDopo modifica: eta={utente['eta']}, email={utente['email']}")

# Rimuovere una chiave:
telefono = utente.pop("email", None)  # Rimuove e restituisce (come pop nelle liste)
print(f"Email rimossa: {telefono}")

# Aggiornare con più valori contemporaneamente:
# PHP:  $utente = array_merge($utente, ["citta" => "Roma", "ruolo" => "senior"]);
#       // array_merge() unisce due array. Se le chiavi esistono, le sovrascrive.
# JS:   utente = { ...utente, citta: "Roma", ruolo: "senior" }
#       // Lo spread ... copia tutte le chiavi e poi le nuove sovrascrivono
#       // Alternativa: Object.assign(utente, {citta: "Roma", ruolo: "senior"})
# Python:
utente.update({"citta": "Roma", "ruolo": "senior developer"})
print(f"Dopo update: {utente}")

# --- MINI-ESERCIZIO 2 — Prova subito! ---
# Usa il dizionario 'auto' che hai creato nel mini-esercizio 1.
# 1) Aggiungi la chiave "colore" con un valore a tua scelta
# 2) Modifica i km con un valore diverso
# 3) Rimuovi la chiave "anno" con .pop() e stampa il valore rimosso
# 4) Usa .update() per aggiungere "targa" e "proprietario" in un colpo solo
# Scrivi qui sotto:
# auto = {
#     "marca":"Fiat",
#     "modello":"500",
#     "anno":2020,
#     "km":30000
# }
# auto['colore'] ="rosso"
# auto['km'] = "10000"
# auto.pop('anno', None)
# auto.update({'targa':'vb546tr', 'proprietario':'Anna'})
# print(f"{auto}")

# 📝 CORREZIONE MENTOR — Mini-esercizio 2:
# ✅ Punto 1 (colore): Perfetto.
# ⚠️ Punto 2 (km): ATTENZIONE AI TIPI! Hai scritto "10000" (stringa con le
#    virgolette). I chilometri sono un NUMERO, non una stringa!
#    Sbagliato: auto['km'] = "10000"   ← stringa
#    Corretto:  auto['km'] = 10000     ← numero intero
#    Pensa a PHP: $auto['km'] = 10000; — scriveresti le virgolette?
#    Pensa a JS: auto.km = 10000; — idem.
#    Regola: se il valore rappresenta una QUANTITÀ (km, prezzo, età, voti),
#    deve essere un numero. Le stringhe sono per TESTI (nomi, indirizzi, email).
# ✅ Punto 3 (.pop): Perfetto, con default None — ottima pratica difensiva.
# ✅ Punto 4 (.update): Perfetto, sintassi corretta.
# ✅ Print finale: Funziona, ma potresti rendere l'output più leggibile con
#    più print separati invece di stampare tutto il dizionario grezzo.



# ==========================================================================
# PARTE 3: Iterare su un Dizionario
# ==========================================================================

prodotto = {
    "nome": "Tastiera Meccanica",
    "prezzo": 89.99,
    "categoria": "Elettronica",
    "disponibile": True,
    "voto_medio": 4.5
}

# Iterare sulle CHIAVI:
print("\n=== Solo chiavi ===")
for chiave in prodotto:  # oppure: for chiave in prodotto.keys():
    print(f"  {chiave}")

# Iterare sui VALORI:
print("\n=== Solo valori ===")
for valore in prodotto.values():
    print(f"  {valore}")

# Iterare su CHIAVI E VALORI (il più comune):
# PHP:  foreach($prodotto as $chiave => $valore) { echo "$chiave: $valore"; }
#       // La sintassi $chiave => $valore nello foreach è il modo PHP per
#       // accedere sia alla chiave sia al valore durante l'iterazione.
#
# JS:   Object.entries(prodotto).forEach(([k, v]) => console.log(k, v));
#       // Object.entries() trasforma l'oggetto in un array di coppie:
#       //   {nome:"Mouse", prezzo:29.99} → [["nome","Mouse"], ["prezzo",29.99]]
#       // .forEach() scorre ogni coppia
#       // ([k, v]) è il destructuring: scompone ["nome","Mouse"] in k e v

# RIPASSO — unpacking (spacchettamento): ricordi le tuple dal capitolo 04?
# .items() restituisce coppie (chiave, valore) — esattamente come enumerate()
# restituiva coppie (indice, elemento). Con `for chiave, valore in ...` le
# spacchetti in due variabili separate. È lo STESSO concetto, applicato
# ai dizionari invece che alle liste.

print("\n=== Chiavi e valori ===")
for chiave, valore in prodotto.items():
    print(f"  {chiave}: {valore}")

# RIPASSO — enumerate(): ricordi? Dà indice + valore insieme. Anche qui
# puoi usarlo se ti serve sapere a che punto sei nell'iterazione:
print("\n=== Con enumerate ===")
for i, (chiave, valore) in enumerate(prodotto.items(), 1):
    print(f"  {i}. {chiave}: {valore}")
# Nota: enumerate() avvolge .items(), che già produce tuple (chiave, valore).
# Quindi enumerate produce tuple annidate: (0, ("nome", "Tastiera Meccanica"))
# Per spacchettarle scrivi: i, (chiave, valore) — le parentesi interne
# dicono a Python "questa è una tupla dentro la tupla esterna".

# --- MINI-ESERCIZIO 3 — Prova subito! ---
# Usa il dizionario 'auto' dei mini-esercizi precedenti.
# 1) Stampa tutte le chiavi e i valori usando un for con .items()
# 2) Stampa una tabella numerata usando enumerate() con .items():
#    "1. marca: Fiat"
#    "2. modello: Panda"
#    ecc.
# Scrivi qui sotto:
auto = {
    "marca":"Fiat",
    "modello":"500",
    "anno":2020,
    "km":30000
}

for key,value in auto.items():
    print(f"{key} -> {value}")

for i, (key, value) in enumerate(auto.items(), 1):
    print(f"#{i} => {key} : {value}")

# 📝 CORREZIONE MENTOR — Mini-esercizio 3:
# ✅ Punto 1 (.items() con for): PERFETTO! Sintassi impeccabile.
# ✅ Punto 2 (enumerate + .items()): ECCELLENTE! Hai usato correttamente
#    enumerate(auto.items(), 1) con l'unpacking (i, (key, value)).
#    Questo è esattamente il pattern che al capitolo 04 ti dava problemi.
#    GRANDE MIGLIORAMENTO — il ponte ".items() = enumerate dei dizionari"
#    ha funzionato!


# ==========================================================================
# PARTE 4: Dizionari Annidati (Nested)
# ==========================================================================

# Esattamente come gli oggetti annidati in JavaScript/JSON.
# Esempio: la risposta di un'API e-commerce.

ordine = {
    "id": "ORD-2024-001",
    "data": "2024-01-15",
    "cliente": {
        "nome": "Laura Bianchi",
        "email": "laura@email.com",
        "indirizzo": {
            "via": "Via Roma 42",
            "citta": "Milano",
            "cap": "20121"
        }
    },
    "prodotti": [
        {"nome": "Cuffie Bluetooth", "prezzo": 49.99, "quantita": 1},
        {"nome": "Mouse Wireless", "prezzo": 29.99, "quantita": 2}
    ],
    "totale": 109.97
}

# Accedere ai dati annidati:
print("\n=== Ordine (dizionario annidato) ===")
print(f"ID Ordine: {ordine['id']}")
print(f"Cliente: {ordine['cliente']['nome']}")
print(f"Città: {ordine['cliente']['indirizzo']['citta']}")
print(f"Primo prodotto: {ordine['prodotti'][0]['nome']}")

# Iterare sui prodotti dell'ordine:
print("\nProdotti:")
for prod in ordine["prodotti"]:
    subtotale = prod["prezzo"] * prod["quantita"]
    print(f"  - {prod['nome']}: {prod['prezzo']}€ x{prod['quantita']} = {subtotale}€")

# --- MINI-ESERCIZIO 4 — Prova subito! ---
# Crea un dizionario annidato 'ristorante' con:
#   - "nome": il nome del ristorante
#   - "indirizzo": un dizionario con "via", "citta", "cap"
#   - "menu": una lista di dizionari, ognuno con "piatto" e "prezzo"
#     (metti almeno 3 piatti)
# Poi:
# 1) Stampa il nome e la città del ristorante
# 2) Stampa il nome del secondo piatto nel menu
# 3) Con un ciclo for, stampa tutti i piatti con il prezzo
# Scrivi qui sotto:
ristorante = {
    "nome" : "Rosso Ciliegino",
    "indirizzo" : {
        "citta" : "Roma",
        "via" : "via Fasulla 13",
        "cap" : "21345"
    },
    "menu" : [
        {
            "piatto" : "Amatriciana",
            "prezzo" : 12.99
        },
        {
            "piatto" : "Carbonara",
            "prezzo" : 11.99
        }
    ]
}

# 📝 CORREZIONE MENTOR — Mini-esercizio 4:
# ✅ Struttura dizionario: Ben fatta! Annidamento corretto con indirizzo
#    come sotto-dizionario e menu come lista di dizionari. Bravo!
# ⚠️ CONSEGNA INCOMPLETA (Pattern #6 — lettura consegne):
#    La consegna chiedeva:
#      - "metti almeno 3 piatti" → Ne hai messi solo 2 (Amatriciana, Carbonara)
#      - "1) Stampa il nome e la città" → Manca il print!
#      - "2) Stampa il nome del secondo piatto" → Manca il print!
#      - "3) Con un ciclo for, stampa tutti i piatti con prezzo" → Manca il for!
#
#    Ecco cosa mancava (NON copiare, prova a scriverlo tu):
#    - Aggiungi un terzo piatto al menu (es. "Cacio e Pepe")
#    - print(f"Ristorante: {ristorante['nome']}, Città: {ristorante['indirizzo']['citta']}")
#    - print(f"Secondo piatto: {ristorante['menu'][1]['piatto']}")
#    - for piatto in ristorante["menu"]:
#          print(f"  {piatto['piatto']}: {piatto['prezzo']}€")
#
#    CONSIGLIO: Prima di passare al prossimo esercizio, rileggi TUTTA la
#    consegna e conta i punti numerati (1, 2, 3). Se ne vedi 3, devi
#    scrivere almeno 3 blocchi di codice.


# ==========================================================================
# PARTE 5: Dictionary Comprehension
# ==========================================================================

# RIPASSO — list comprehension (dal capitolo 04): ricordi la sintassi
# [COSA for ELEMENTO in LISTA if CONDIZIONE]? Era come .map() + .filter()
# in JS. Le dict comprehension sono IDENTICHE, ma con le graffe {} e la
# coppia chiave:valore.
#
# Come le list comprehension, ma per i dizionari.
# Sintassi: {chiave: valore for elemento in iterabile}

# Esempio: creare un dizionario da due liste:
# zip() prende due liste e le "accoppia" elemento per elemento:
#   zip(["a","b"], [1,2]) → [("a",1), ("b",2)]
# PHP: array_combine($chiavi, $valori)
# JS:  Object.fromEntries(keys.map((k, i) => [k, values[i]]))
nomi = ["Marco", "Laura", "Giulia"]
voti = [85, 92, 78]

registro = {nome: voto for nome, voto in zip(nomi, voti)}
print(f"\n=== Dict Comprehension ===")
print(f"Registro: {registro}")

# Filtrare un dizionario:
prezzi = {"mela": 1.50, "banana": 0.80, "mango": 3.50, "kiwi": 2.00}
cari = {nome: prezzo for nome, prezzo in prezzi.items() if prezzo > 1.50}
print(f"Frutti cari (>1.50€): {cari}")

# Trasformare i valori:
prezzi_scontati = {nome: round(prezzo * 0.8, 2) for nome, prezzo in prezzi.items()}
print(f"Con sconto 20%: {prezzi_scontati}")

# --- MINI-ESERCIZIO 5 — Prova subito! ---
# Dato il dizionario:
#   temperature = {"Milano": 28, "Roma": 35, "Napoli": 33, "Torino": 25, "Palermo": 38}
# Usando le dict comprehension:
# 1) Crea un nuovo dizionario con solo le città sopra i 30°C
# 2) Crea un nuovo dizionario con le temperature convertite in Fahrenheit
#    (F = C * 9/5 + 32), arrotondate a 1 decimale
# Scrivi qui sotto:
temperature = {"Milano": 28, "Roma": 35, "Napoli": 33, "Torino": 25, "Palermo": 38}
nuove_temperature = {}
for key, value in temperature.items():
    if value > 30:
        nuove_temperature[key] = value
print("\n=== Temperature delle citta' sopra i 30° ===\n")  
print(f"{nuove_temperature}")

temperature_in_f = {}
for key, value in temperature.items():
    temperature_in_f[key] = round(value * 9/5 + 32, 1)
print("\n=== Temperature delle citta' in Fahrenheit ===\n")  
print(f"{temperature_in_f}")

# 📝 CORREZIONE MENTOR — Mini-esercizio 5:
# ✅ Logica: Entrambi i risultati sono CORRETTI — filtraggio > 30°C e
#    conversione in Fahrenheit con arrotondamento. La logica è giusta!
# ⚠️ MA: La consegna diceva "Usando le dict comprehension"!
#    Tu hai usato un ciclo for classico con dizionario vuoto — funziona,
#    ma non è quello che la consegna chiedeva.
#
#    Il tuo codice (for classico):
#      nuove_temperature = {}
#      for key, value in temperature.items():
#          if value > 30:
#              nuove_temperature[key] = value
#
#    Con dict comprehension (UNA sola riga!):
#      nuove_temperature = {k: v for k, v in temperature.items() if v > 30}
#
#    Per il Fahrenheit:
#      temperature_in_f = {k: round(v * 9/5 + 32, 1) for k, v in temperature.items()}
#
#    Confronta: è come la list comprehension [expr for x in lista if cond],
#    ma con le graffe {} e chiave:valore!
#
#    ESERCIZIO BONUS: prova a riscrivere entrambi i punti con dict
#    comprehension. Quando ti viene naturale, sarà un livello in più.


# ==========================================================================
# PARTE 6: Lambda con i Dizionari — Rinforzo
# ==========================================================================

# RIPASSO — lambda: ricordi? Sono mini-funzioni usa-e-getta, di una sola
# riga. In JS sono le arrow function (() =>), in PHP le short closure
# (fn() =>). Al capitolo 04 le hai usate con sorted(), filter() e map()
# sulle liste. Ora le usiamo con i dizionari — stessa logica!

# Ordinare una lista di dizionari con sorted() + lambda:
# sorted() crea una NUOVA lista ordinata. Con key=lambda dici "ordina
# in base a QUESTO campo del dizionario".

dipendenti = [
    {"nome": "Marco", "stipendio": 35000, "reparto": "Sviluppo"},
    {"nome": "Laura", "stipendio": 42000, "reparto": "Marketing"},
    {"nome": "Giulia", "stipendio": 38000, "reparto": "Sviluppo"},
    {"nome": "Luca", "stipendio": 45000, "reparto": "Direzione"},
    {"nome": "Anna", "stipendio": 33000, "reparto": "Marketing"},
]

# Ordinare per stipendio crescente:
per_stipendio = sorted(dipendenti, key=lambda d: d["stipendio"])
print("\n=== Dipendenti per stipendio (crescente) ===")
for d in per_stipendio:
    print(f"  {d['nome']}: {d['stipendio']:,}€ ({d['reparto']})")

# Filtrare con filter() + lambda:
sviluppatori = list(filter(lambda d: d["reparto"] == "Sviluppo", dipendenti))
print(f"\nSviluppatori: {[d['nome'] for d in sviluppatori]}")

# Trasformare con map() + lambda — estrarre solo i nomi:
solo_nomi = list(map(lambda d: d["nome"], dipendenti))
print(f"Solo nomi: {solo_nomi}")

# Trovare il massimo con max() + lambda:
# max() restituisce l'elemento "più grande". Con key=lambda decidi tu in
# base a cosa confrontare. Qui: chi ha lo stipendio più alto?
piu_pagato = max(dipendenti, key=lambda d: d["stipendio"])
print(f"Più pagato: {piu_pagato['nome']} ({piu_pagato['stipendio']:,}€)")

# --- MINI-ESERCIZIO 6 — Prova subito! ---
# Usa la lista 'dipendenti' qui sopra.
# 1) Con sorted() + lambda, ordina per nome in ordine alfabetico e stampa
# 2) Con filter() + lambda, trova chi guadagna più di 36.000€
# 3) Con max() + lambda, trova chi ha il nome più lungo
#    (suggerimento: len(d["nome"]) dà la lunghezza del nome)
# Scrivi qui sotto:
dipendenti = [
    {"nome": "Marco", "stipendio": 35000, "reparto": "Sviluppo"},
    {"nome": "Laura", "stipendio": 42000, "reparto": "Marketing"},
    {"nome": "Giulia", "stipendio": 38000, "reparto": "Sviluppo"},
    {"nome": "Luca", "stipendio": 45000, "reparto": "Direzione"},
    {"nome": "Anna", "stipendio": 33000, "reparto": "Marketing"},
]
print("\nDipendenti ordinati per ordine alfabetico\n")
ordine_alfabetico = sorted(dipendenti, key=lambda a: a['nome'])
for d in ordine_alfabetico:
    print(f"{d['nome']}")

print("\nDipendenti che guadagnao più di 36.000,00 €\n")
dipendenti_su_sorted = sorted(filter((lambda d: d['stipendio'] > 36000), dipendenti), key=lambda d: d['stipendio'])
for d in dipendenti_su_sorted:
    print(f"{d['nome']} => Reddito : {d['stipendio']:.2f} €")

# 📝 CORREZIONE MENTOR — Mini-esercizio 6:
# ✅ Punto 1 (sorted per nome): PERFETTO! sorted() + lambda con key corretto.
# ✅ Punto 2 (filter > 36000): ECCELLENTE! Hai combinato filter() + sorted()
#    autonomamente — non era richiesto ma dimostra iniziativa e comprensione.
#    La sintassi filter(lambda, lista) è CORRETTA questa volta — bravo!
#    Nota: le parentesi intorno a lambda non sono necessarie ma non fanno danno.
# ⚠️ Punto 3 (max per nome più lungo): MANCA!
#    La consegna chiedeva: "Con max() + lambda, trova chi ha il nome più lungo"
#    Ecco la soluzione (prova prima a farla tu!):
#      nome_lungo = max(dipendenti, key=lambda d: len(d["nome"]))
#      print(f"Nome più lungo: {nome_lungo['nome']} ({len(nome_lungo['nome'])} caratteri)")
#
#    max() funziona come sorted(): con key=lambda gli dici "confronta in base
#    a QUESTO valore". Qui: len(d["nome"]) = la lunghezza del nome.


# ==========================================================================
# PARTE 7: Metodi Utili
# ==========================================================================

config = {"tema": "dark", "lingua": "it", "font_size": 14}

print(f"\n=== Metodi utili ===")
print(f"Chiavi: {list(config.keys())}")
print(f"Valori: {list(config.values())}")
print(f"Coppie: {list(config.items())}")
print(f"Ha 'tema'? {'tema' in config}")          # Controlla se la chiave esiste
print(f"Ha 'colore'? {'colore' in config}")

# setdefault — imposta un valore solo se la chiave NON esiste:
config.setdefault("colore", "blu")
config.setdefault("tema", "light")  # NON sovrascrive perché "tema" esiste già
print(f"Dopo setdefault: {config}")

# Copiare un dizionario (attenzione! = non copia, crea un riferimento):
# PHP:  $copia = $config;   — in PHP gli array vengono COPIATI automaticamente!
# JS:   const copia = {...config};  — lo spread ... crea una copia "superficiale"
# Python: = NON copia! Crea solo un secondo nome per lo STESSO dizionario.
#         Devi usare .copy() per fare una copia vera:
config_copia = config.copy()  # Come {...config} in JS
config_copia["tema"] = "light"
print(f"Originale: {config['tema']}")   # Rimane "dark"
print(f"Copia: {config_copia['tema']}")  # "light"

# --- MINI-ESERCIZIO 7 — Prova subito! ---
# Crea un dizionario 'preferenze' con: "lingua": "it", "notifiche": True
# 1) Usa "in" per verificare se la chiave "tema" esiste
# 2) Usa .setdefault() per aggiungere "tema" con default "auto"
#    (solo se non esiste già)
# 3) Crea una copia con .copy(), modifica "lingua" nella copia a "en",
#    e verifica che l'originale non sia cambiato stampando entrambi
# Scrivi qui sotto:
preferenze = {
    "lingua": "it",
    "notifiche": True    
}
print("\nEsercizi sui Metodi Utili\n")
print(f"Ha un 'tema' => {'tema' in preferenze}")
preferenze.setdefault("tema", "blu")
print("\nDopo il setdefault()\n")
print(f"Ha un 'tema' => {'tema' in config}")
copia_preferenze = preferenze.copy()
print(f"\nCopia della dictionary 'preferenza'\n")
print(f"{copia_preferenze}")
print(f"{preferenze}")

# 📝 CORREZIONE MENTOR — Mini-esercizio 7:
# ✅ Punto 1 ("tema" in preferenze): Corretto! Sintassi `in` giusta.
# ✅ Punto 2 (.setdefault): Corretto! Aggiunge "tema" solo se non esiste.
#    Nota: hai usato "blu" come default — la consegna suggeriva "auto", ma
#    il concetto è giusto.
# ⚠️ Punto 3 (.copy + modifica + verifica): INCOMPLETO!
#    La consegna diceva:
#      "modifica 'lingua' nella copia a 'en', e verifica che l'originale
#       non sia cambiato stampando entrambi"
#    Tu hai:
#      - Creato la copia ✅
#      - NON hai modificato "lingua" nella copia ❌
#      - Hai stampato entrambi ✅ ma senza la modifica non dimostri nulla
#
#    Cosa mancava:
#      copia_preferenze["lingua"] = "en"  # Modifica SOLO la copia
#      print(f"Originale: {preferenze['lingua']}")  # Deve restare "it"
#      print(f"Copia: {copia_preferenze['lingua']}")  # Deve essere "en"
#
# ⚠️ BUG DISTRAZIONE: alla riga 524 hai scritto:
#      'tema' in config    ← ma 'config' è la variabile della TEORIA!
#    Doveva essere:
#      'tema' in preferenze  ← la TUA variabile dell'esercizio
#    Funziona lo stesso perché 'config' esiste, ma stai controllando il
#    dizionario sbagliato! Attenzione ai nomi delle variabili.



# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  QUIZ DI VERIFICA — Hai capito la teoria?                            ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# Queste domande verificano i concetti di QUESTO capitolo (Dizionari).
# Rispondi DOPO aver letto la teoria, PRIMA di fare gli esercizi.
# Le risposte corrette sono in fondo al file nella sezione SOLUZIONI.

# DOMANDA 1 — Prevedi l'output:
# Cosa stampa questo codice?
#   persona = {"nome": "Luca", "eta": 25}
#   persona["eta"] = 26
#   persona["citta"] = "Roma"
#   print(len(persona))
# La tua risposta: 2

# DOMANDA 2 — Trova l'errore:
#   config = {"tema": "dark", "lingua": "it"}
#   print(config["font_size"])
# Qual è il problema? Come lo risolveresti? print(f"{'font_size' in config}")

# DOMANDA 3 — Vero o Falso?
# "Quando fai copia = dizionario (senza .copy()), modificare 'copia'
#  modifica anche 'dizionario'"
# La tua risposta (V/F): V, credi di si perchè di fa una copia del riferimento 

# DOMANDA 4 — Definizione:
# Che differenza c'è tra dizionario.keys(), dizionario.values()
# e dizionario.items()?
# La tua risposta: il primo restituisce le chiavi, il secondo il valore, e items restituisce le tuple (chiave, valore)

# DOMANDA 5 — Completa il codice:
# Voglio iterare su un dizionario stampando chiave e valore:
#   prodotto = {"nome": "Mouse", "prezzo": 29.99}
#   for chiave, valore in prodotto.items():
#       print(f"{chiave}: {valore}")
# Riempi i tre spazi: ___

# DOMANDA 6 — Prevedi l'output:
# Cosa stampa questo codice?
#   voti = {"Marco": 7, "Laura": 9, "Giulia": 5}
#   bravi = {n: v for n, v in voti.items() if v >= 7}
#   print(bravi)
# La tua risposta: {"Laura": 9}

# DOMANDA 7 — Vero o Falso?
# ".setdefault('chiave', valore) sovrascrive il valore se la chiave
#  esiste già nel dizionario"
# La tua risposta (V/F): F

# DOMANDA 8 — Completa il codice:
# Voglio contare quante volte appare ogni lettera nella parola "banana":
#   conteggio = {}
#   for lettera in "banana":
#       conteggio[lettera] = conteggio.items(lettera, totale) + 1
#   print(conteggio)
# Riempi i due spazi: items, totale

# 📝 CORREZIONE MENTOR — Quiz di Verifica (Cap. 05):
#
# D1: ❌ Hai scritto 2.
#     Risposta corretta: 3. Parte con 2 chiavi, modifica "eta" (resta 2),
#     poi AGGIUNGE "citta" → diventa 3. Aggiungere una chiave nuova
#     incrementa len().
#
# D2: ⚠️ Parziale. Hai identificato che c'è un problema, ma la risposta
#     corretta è: KeyError! Python crasha se accedi a una chiave inesistente.
#     La soluzione è .get("font_size", default) — non 'font_size' in config.
#     Il tuo "in" controlla se esiste ma non risolve il crash.
#
# D3: ✅ Corretto! E ottima la spiegazione: "copia del riferimento".
#
# D4: ✅ Corretto! Spiegazione chiara e sintetica.
#
# D5: ✅ Corretto! (il codice era già completo, dovevi confermarlo)
#
# D6: ❌ Hai scritto {"Laura": 9}.
#     Risposta corretta: {"Marco": 7, "Laura": 9}. La condizione è
#     v >= 7, e Marco ha voto 7 — passa il filtro! >= include il 7.
#
# D7: ✅ Corretto!
#
# D8: ❌ Hai scritto "items, totale".
#     Risposta corretta: get, 0. Il metodo è .get(chiave, default),
#     non .items(). .items() restituisce tutte le coppie, .get() cerca
#     UNA chiave con valore di default se non esiste.
#
# Risultato: 4/8 corrette, 1/8 parziale, 3/8 sbagliate
# Lacune: len() con aggiunta chiavi, >= vs >, .get() vs .items()


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Crea un dizionario 'film' con queste chiavi: titolo, regista, anno, genere,
# voto (da 1 a 10). Stampalo in modo formattato:
#   "Titolo: Inception"
#   "Regista: Christopher Nolan"
#   ecc.
# Poi aggiungi la chiave "attore_principale" e stampa di nuovo.
#
# Scrivi il tuo codice qui sotto:
film = {
    "titolo" : "Inception",
    "regista": "Christopher Nolan",
    "anno": "2019",
    "genere": "Thriller"
}
print("\n=== Esercizio 1===\n")
def stampa(dizionario):
    for key,value in film.items():
        print(f"{key.title()}: {value.title()}")

stampa(film)

film.update({"attore": "Leonardo"})

stampa(film)

# 📝 CORREZIONE MENTOR — Esercizio 1:
# ✅ Buona idea creare una funzione riutilizzabile per stampare!
# ⚠️ La funzione accetta 'dizionario' come parametro ma dentro usa 'film'
#    direttamente (riga 722: film.items() invece di dizionario.items()).
#    Funziona perché film esiste, ma se passi un altro dizionario non funziona.
# ⚠️ "anno" è scritto come "2019" (stringa) — dovrebbe essere un numero 2019.
#    (Pattern #5 — tipi nei dizionari)
# ⚠️ Manca la chiave "voto" — la consegna diceva "voto (da 1 a 10)".
#    (Pattern #6 — consegna incompleta)
# ⚠️ .title() su anno (numero come stringa) funziona ma non ha senso.
#    Se anno fosse un int (come dovrebbe), .title() crasherebbe.
# ⚠️ La chiave è "attore" ma la consegna diceva "attore_principale".
# ✅ Uso di .update() corretto.


# ESERCIZIO 2 (Medio):
# Data questa lista di prodotti (lista di dizionari):
#   prodotti = [
#       {"nome": "Laptop", "prezzo": 999.99, "categoria": "Elettronica"},
#       {"nome": "Libro Python", "prezzo": 35.00, "categoria": "Libri"},
#       {"nome": "Cuffie", "prezzo": 79.99, "categoria": "Elettronica"},
#       {"nome": "Zaino", "prezzo": 59.99, "categoria": "Accessori"},
#       {"nome": "Libro AI", "prezzo": 42.00, "categoria": "Libri"},
#   ]
# a) Stampa solo i prodotti di categoria "Elettronica"
# b) Calcola il prezzo totale di tutti i prodotti
# c) Trova il prodotto più costoso (usa max con key=lambda)
# d) Crea un dizionario che raggruppa i prodotti per categoria:
#    {"Elettronica": [...], "Libri": [...], "Accessori": [...]}
#
# Scrivi il tuo codice qui sotto:
prodotti = [
      {"nome": "Laptop", "prezzo": 999.99, "categoria": "Elettronica"},
      {"nome": "Libro Python", "prezzo": 35.00, "categoria": "Libri"},
      {"nome": "Cuffie", "prezzo": 79.99, "categoria": "Elettronica"},
      {"nome": "Zaino", "prezzo": 59.99, "categoria": "Accessori"},
      {"nome": "Libro AI", "prezzo": 42.00, "categoria": "Libri"},
  ]

print("\n=== Esercizio 2===\n")

def conta_totale(lista):
    totale = sum(p['prezzo'] for p in lista)
    return print(f"Totale dei prezzi: {totale} €\n")

def trova_max(lista):
    massimo =  max(lista, key=lambda p: p['prezzo'])
    return print(f"Prodotto più costoso:\n- {massimo['nome']} => {massimo['prezzo']} €\n")

def raggruppa_per_categoria(lista):
    lista_per_categoria = {}
    for p in lista:        
        lista_per_categoria.setdefault(p['categoria'], []).append(p['nome'])
    return print(f"{lista_per_categoria}")

conta_totale(prodotti)
trova_max(prodotti)
raggruppa_per_categoria(prodotti)

# 📝 CORREZIONE MENTOR — Esercizio 2:
# ✅ Punto a) manca! Non hai stampato i prodotti di categoria "Elettronica".
#    (Pattern #6 — consegna incompleta)
# ✅ Punto b) conta_totale: Logica perfetta! sum() con generator expression.
# ✅ Punto c) trova_max: max() con lambda — perfetto!
# ✅ Punto d) raggruppa_per_categoria: ECCELLENTE! Hai usato .setdefault()
#    con lista vuota + .append() — è la soluzione più elegante.
#    Questo è esattamente il pattern dell'esercizio 7 (colloquio).
# ⚠️ return print(...): ricorda che print() restituisce None. Se vuoi
#    restituire il valore E stamparlo, separa le due operazioni.
#    Il concetto funzionale è giusto, ma il return è inutile.


# ESERCIZIO 3 (Medio — Dict Comprehension):
# Dato il dizionario:
#   voti_studenti = {"Marco": 75, "Laura": 92, "Giulia": 58, "Luca": 88, "Anna": 45}
# a) Crea un nuovo dizionario con solo gli studenti promossi (voto >= 60)
# b) Crea un nuovo dizionario con i giudizi:
#    {"Marco": "Buono", "Laura": "Eccellente", ...}
#    (>=90: Eccellente, >=70: Buono, >=60: Sufficiente, <60: Insufficiente)
#
# Scrivi il tuo codice qui sotto:
voti_studenti = {
    "Marco": 75, 
    "Laura": 92, 
    "Giulia": 58, 
    "Luca": 88, 
    "Anna": 45
}

print("\n=== Esercizio 3===\n")

studenti_promossi = {nome: voto for nome, voto in voti_studenti.items() if voto >= 60}

def giudizio(voto):
    if voto >= 90: return "Eccellente"
    if voto >= 70: return "Buono" 
    if voto >= 60: return "Sufficiente" 
    if voto < 60: return "Insufficiente" 

giudizi_studenti = {}
for nome, voto in sorted(voti_studenti.items(), key=lambda x: x[1], reverse=True):
    giudizi_studenti.update({nome : giudizio(voto)})

print(f"{giudizi_studenti}")

# 📝 CORREZIONE MENTOR — Esercizio 3:
# ✅ Punto a) dict comprehension: PERFETTO! Sintassi corretta al primo
#    tentativo. Dopo il mini-esercizio 5 dove avevi usato il for classico,
#    qui hai usato la dict comprehension — GRANDE MIGLIORAMENTO!
# ✅ Punto b) funzione giudizio(): Logica corretta, if a cascata ben fatti.
#    L'ultimo if (voto < 60) potrebbe essere solo "return" senza condizione
#    (se non è >=60 è per forza <60), ma funziona ugualmente.
# ⚠️ Hai usato .update() dentro un for — funziona ma è più verboso.
#    Potevi usare dict comprehension anche qui:
#    giudizi = {n: giudizio(v) for n, v in voti_studenti.items()}
# ✅ Il sorted con reverse=True non era richiesto ma mostra iniziativa.



# 🎯 [COLLOQUIO] — ESERCIZIO 4 (Sfida — Conta Parole):
# Questa è una domanda CLASSICA dei colloqui tecnici, sia per junior che
# per mid-level. Viene chiesta in varianti diverse ma il concetto è sempre:
# "conta le frequenze di qualcosa usando un dizionario".
#
# Scrivi una funzione 'conta_parole(testo)' che:
#   1. Prende una stringa di testo
#   2. Restituisce un dizionario con ogni parola e quante volte appare
#   3. Le parole devono essere tutte in minuscolo
#   4. La funzione deve avere una docstring
# Es: conta_parole("ciao mondo ciao") → {"ciao": 2, "mondo": 1}
# Suggerimento: testo.lower().split() divide il testo in parole minuscole.
# Suggerimento 2: .get(chiave, default) è PERFETTO per contare frequenze.
# Testa con: "Ciao mondo ciao a tutto il mondo" e con una stringa vuota ""
#
# Scrivi il tuo codice qui sotto:

testo_di_prova = "Ciao mondo ciao a tutto il mondo"
testo_di_prova_2 = ""

def conta_parole(testo):
    testo_preparato = testo.lower().split() #restituisce un array con tutto le parole in minuscolo, dividendole usando gli spazi
    conta_parole = {} # si inizia con un contatore vuoto
    for parola in testo_preparato: # iteriamo su ogni elemento dell'array
        conta_parole[parola] = conta_parole.get(parola, 0) + 1  #assegna una chiave per ogni parole, e controlla :
    return conta_parole                                         # se esiste, aggiunge 1 al contatore, partendo dal
                                                                # che in questo caso è 0
print("\n=== Esercizio 4===\n")
print(f"{conta_parole(testo_di_prova)}")
print(f"{conta_parole(testo_di_prova_2)}")

# 📝 CORREZIONE MENTOR — Esercizio 4 (🎯 COLLOQUIO — Conta Parole):
# ✅ ECCELLENTE! Risolto perfettamente al primo tentativo.
# ✅ .lower().split() — corretto per normalizzare e dividere
# ✅ .get(parola, 0) + 1 — il pattern perfetto per contare frequenze!
#    Questo è esattamente quello che serviva nel quiz di verifica D8
#    (dove avevi confuso .get() con .items()). Qui lo usi correttamente.
# ✅ Testato con stringa vuota — buona pratica difensiva.
# ⚠️ Manca la docstring — la consegna diceva "La funzione deve avere
#    una docstring". (Pattern #6)
# ⚠️ Il nome della funzione e della variabile interna sono uguali
#    (conta_parole). Funziona in Python perché la variabile locale
#    "ombreggia" la funzione, ma è confuso. Meglio usare "conteggio"
#    per la variabile interna.
# ✅ Da colloquio: questa soluzione passerebbe. Bravo!


# ESERCIZIO 5 (Medio — Lambda con Dizionari — Rinforzo):
# Hai questa lista di film:
#   film_lista = [
#       {"titolo": "Inception", "anno": 2010, "voto": 8.8},
#       {"titolo": "Interstellar", "anno": 2014, "voto": 8.6},
#       {"titolo": "The Matrix", "anno": 1999, "voto": 8.7},
#       {"titolo": "Parasite", "anno": 2019, "voto": 8.5},
#       {"titolo": "Oppenheimer", "anno": 2023, "voto": 8.3},
#   ]
#
# Usando sorted(), filter(), map() con lambda (come hai fatto al cap. 04):
#   a) Ordina i film per voto decrescente (i migliori prima)
#   b) Filtra solo i film usciti dal 2010 in poi
#   c) Crea una lista di stringhe tipo: ["Inception (2010) — ⭐ 8.8", ...]
#   d) Trova il film più vecchio (usa min con lambda)
#   e) Ordina per anno crescente e stampa con enumerate numerato da 1
#
# Scrivi il tuo codice qui sotto:
film_lista = [
    {"titolo": "Inception", "anno": 2010, "voto": 8.8},
    {"titolo": "Interstellar", "anno": 2014, "voto": 8.6},
    {"titolo": "The Matrix", "anno": 1999, "voto": 8.7},
    {"titolo": "Parasite", "anno": 2019, "voto": 8.5},
    {"titolo": "Oppenheimer", "anno": 2023, "voto": 8.3},
]


film_per_valutazione = sorted(film_lista, key=lambda v: v['voto']) #come chiave usiamo un lamda che per ogni elemento ci restituisce il valore di voto
film_a_partire_da_anno = list(filter(lambda a: a['anno'] >=2010, film_lista))
stringhe_film = list(map(lambda a: f"{a['titolo']} => voto ⭐ {a.get("voto", "nessun voto")}", film_lista))
film_più_vecchio = min(film_lista, key=lambda a: a.get('anno'))
anno_crescente = enumerate(list(sorted(film_lista, key=lambda a: a['anno'])),1)


print("\n=== Esercizio 5===\n")
# print(f"{film_a_partire_da_anno}")
# print(f"{stringhe_film}")
# print(f"{film_più_vecchio}")
for key, value in anno_crescente:
    print(f"#{key}: {value['titolo']}")

# 📝 CORREZIONE MENTOR — Esercizio 5:
# ✅ a) sorted per voto: Corretto! Ma manca reverse=True — la consegna
#    chiedeva "decrescente (i migliori prima)". Senza reverse, i peggiori
#    sono in cima. (Pattern #6 — consegna incompleta)
# ✅ b) filter dal 2010: Perfetto! filter + lambda + list() — tutto giusto.
# ⚠️ c) map per stringhe: Errore di sintassi! Hai doppi apici dentro
#    doppi apici nell'f-string: a.get("voto"...) dentro f"...".
#    Usa apici singoli: a.get('voto', 'nessun voto')
#    (Pattern ricorrente — f-string con doppi apici annidati)
#    Inoltre .get() non serviva: "voto" esiste in tutti i film.
# ✅ d) min per film più vecchio: Perfetto! min() + lambda.
# ✅ e) enumerate con anno crescente: Corretto e ben fatto!
#    Nota: enumerate() restituisce (indice, elemento), e tu usi
#    key/value — funziona ma "indice, film" sarebbe più chiaro.
# ⚠️ Hai commentato con # i print dei punti a-d — li hai fatti e poi
#    commentati? Se sì, OK. Se non li hai stampati, la consegna non è completa.


# ESERCIZIO 6 (Medio — enumerate + dizionari):
# Hai questo dizionario di inventario:
#   inventario = {
#       "T-shirt": 45,
#       "Jeans": 12,
#       "Sneakers": 8,
#       "Cappello": 30,
#       "Giacca": 3,
#   }
#
# a) Usando enumerate() e .items(), stampa una tabella numerata:
#    "1. T-shirt: 45 pezzi"
#    "2. Jeans: 12 pezzi"
#    ecc.
# b) Trova e stampa i prodotti con scorta bassa (meno di 10 pezzi),
#    usando enumerate per mostrare la posizione nella lista originale
# c) Crea un NUOVO dizionario con solo i prodotti che hanno più di 15 pezzi,
#    usando dict comprehension
#
# Scrivi il tuo codice qui sotto:
inventario = {
    "T-shirt": 45,
    "Jeans": 12,
    "Sneakers": 8,
    "Cappello": 30,
    "Giacca": 3,
}

intentario_numerato = enumerate(inventario.items(), 1)

print("\n=== Esercizio 6===\n")
for key, (k, value) in intentario_numerato:
    print(f"#{key} => {k}: {value}")

# 📝 CORREZIONE MENTOR — Esercizio 6:
# ✅ Punto a) enumerate + .items(): PERFETTO! Unpacking (key, (k, value))
#    corretto — ormai questo pattern è consolidato!
# ❌ Punto b) MANCA: scorta bassa (<10 pezzi) con enumerate.
#    (Pattern #6 — consegna incompleta)
# ❌ Punto c) MANCA: dict comprehension per prodotti > 15 pezzi.
#    (Pattern #6 + #13 — dict comprehension evitata)
# ⚠️ Typo: "intentario_numerato" — manca la 'v' (inventario).






# 🎯 [COLLOQUIO] — ESERCIZIO 7 (Sfida — Raggruppare per Chiave):
# Questo è un altro classico da colloquio: raggruppare dati per una proprietà.
# È la versione Python del GROUP BY di SQL o del groupBy di Laravel/Eloquent.
#
# Scrivi una funzione 'raggruppa_per(lista_dizionari, chiave)' che:
#   1. Prende una lista di dizionari e il nome di una chiave
#   2. Restituisce un dizionario dove ogni valore unico della chiave
#      diventa una chiave del risultato, e il valore è la lista degli
#      elementi originali che avevano quel valore
#   3. La funzione deve avere una docstring
#
# Es: raggruppa_per(
#   [{"nome": "Marco", "citta": "Milano"}, {"nome": "Laura", "citta": "Roma"},
#    {"nome": "Giulia", "citta": "Milano"}],
#   "citta"
# ) → {"Milano": [{"nome":"Marco",...}, {"nome":"Giulia",...}], "Roma": [...]}
#
# Testa con i prodotti dell'esercizio 2 raggruppati per "categoria".
#
# Scrivi il tuo codice qui sotto:
lista_dizionari = [
    {"nome": "Marco", "citta": "Milano"},
    {"nome": "Laura", "citta": "Roma"},
    {"nome": "Giulia", "citta": "Milano"}
]

def raggruppa_per(lista_dizionari, chiave):
    """Prende una lista di dizionari e il nome di una chiave e
       Restituisce un dizionario dove ogni valore unico della chiave
       diventa una chiave del risultato, e il valore è la lista degli
       elementi originali che avevano quel valore"""
    lista_nuova= {}   
    for l in lista_dizionari:
        valore_chiave = l[chiave]
        if valore_chiave not in lista_nuova:
            lista_nuova[valore_chiave] = []
        lista_nuova[valore_chiave].append(l['nome'])
    return lista_nuova

print("\n=== Esercizio 7===\n")
print(f"{raggruppa_per(lista_dizionari, "citta")}")

# 📝 CORREZIONE MENTOR — Esercizio 7 (🎯 COLLOQUIO — Raggruppare per Chiave):
# ✅ Docstring: Presente e chiara — bravo!
# ✅ Logica: not in + lista vuota + append — pattern corretto!
# ⚠️ Riga 967: appendi l['nome'] invece di l (l'intero dizionario).
#    La consegna diceva che il valore deve essere "la lista degli elementi
#    originali", non solo i nomi. Doveva essere:
#    lista_nuova[valore_chiave].append(l)  ← l'intero dizionario
#    Così il risultato sarebbe: {"Milano": [{"nome":"Marco",...}, ...]}
# ⚠️ F-string con doppi apici annidati alla riga di print — stesso
#    errore del cap.03. In questo contesto non crasha perché Python 3.12+
#    li gestisce, ma è una pratica fragile.
# ⚠️ Non hai testato con i prodotti dell'esercizio 2 come richiesto.
#    (Pattern #6)
# ✅ Da colloquio: la struttura passa, ma l'errore sull'append parziale
#    (solo nome vs dizionario intero) verrebbe notato.


# ESERCIZIO 8 (Sfida — Simula API):
# Crea una funzione 'processa_ordini(ordini)' che prende una lista di
# ordini (come il dizionario 'ordine' della Parte 4) e restituisce un
# dizionario "report" con:
#   - "totale_ordini": numero di ordini — usa len()
#   - "fatturato_totale": somma di tutti i totali — usa sum() con una
#     list comprehension (ricordi? [expr for x in lista])
#   - "citta_piu_ordini": la città con più ordini — usa un dizionario
#     per contare (come in conta_parole), poi max() con lambda
#   - "prodotto_piu_venduto": il prodotto che appare più volte
# La funzione deve avere una docstring.
# Puoi creare una lista di 3-4 ordini di esempio per testarla.
#
# Scrivi il tuo codice qui sotto:

ordini = [
    {
        "id": "ORD-2024-001",
        "data": "2024-01-15",
        "cliente": {
            "nome": "Laura Bianchi",
            "email": "laura@email.com",
            "indirizzo": {
                "via": "Via Roma 42",
                "citta": "Milano",
                "cap": "20121"
            }
        },
        "prodotti": [
            {"nome": "Cuffie Bluetooth", "prezzo": 49.99, "quantita": 1},
            {"nome": "Mouse Wireless", "prezzo": 29.99, "quantita": 2}
        ],
    },
    
    {
        "id": "ORD-2024-002",
        "data": "2024-02-03",
        "cliente": {
            "nome": "Marco Verdi",
            "email": "marco.verdi@email.com",
            "indirizzo": {
                "via": "Corso Garibaldi 18",
                "citta": "Roma",
                "cap": "00184"
            }
        },
        "prodotti": [
            {"nome": "Tastiera Meccanica", "prezzo": 89.99, "quantita": 1},
            {"nome": "Webcam HD", "prezzo": 59.99, "quantita": 1},
            {"nome": "Hub USB-C", "prezzo": 34.99, "quantita": 1}
        ],
    },
    
    {
        "id": "ORD-2024-003",
        "data": "2024-03-22",
        "cliente": {
            "nome": "Anna Russo",
            "email": "anna.russo@email.com",
            "indirizzo": {
                "via": "Via Dante 7",
                "citta": "Roma",
                "cap": "80134"
            }
        },
        "prodotti": [
            {"nome": "Monitor 27 pollici", "prezzo": 299.99, "quantita": 1},
            {"nome": "Cavo HDMI", "prezzo": 12.99, "quantita": 2}
        ],
    }
]
def processa_ordini(ordini):
    totale_ordini = len(ordini)
    totale_fatturato = round(sum(sum(x['prezzo']*x['quantita'] for x in t['prodotti']) for t in ordini),2)
    contatore = {}
    for c in ordini:
        valore_chiave = c['cliente']['indirizzo']['citta']
        if valore_chiave not in contatore:
            contatore[valore_chiave] = 0
        contatore[valore_chiave] += 1
    citta_max_ordini = max(contatore.items(), key=lambda x: x[1])   
    
    print(f"Numero ordini: {totale_ordini}\nTotale fatturato: {totale_fatturato} €\nCitta' con piu' ordini: {citta_max_ordini[0].upper()} => {citta_max_ordini[1]}")

print("\n=== Esercizio 8===\n")
processa_ordini(ordini)

# 📝 CORREZIONE MENTOR — Esercizio 8 (Simula API):
# ✅ Struttura funzione: def con corpo ben organizzato.
# ✅ len(ordini): Corretto.
# ✅ sum() annidato con generator expression: Corretto dopo la correzione
#    (aggiunto * x['quantita']).
# ✅ Contatore città con not in + inizializzazione a 0: Perfetto!
#    (Corretto dopo feedback: era "not in ordini" → "not in contatore")
# ✅ max() con .items() e lambda x: x[1]: Corretto!
# ✅ .upper() su citta_max_ordini[0]: Accesso corretto alla tupla.
# ⚠️ Manca la docstring — la consegna la chiedeva.
# ⚠️ Manca "prodotto_piu_venduto" — la consegna chiedeva anche quello.
#    (Pattern #6 — consegna incompleta)
# ⚠️ print() senza return: OK per stampare, ma la consegna diceva
#    "restituisce un dizionario report". Sarebbe meglio return {...}
#    e stampare fuori dalla funzione.
# ✅ Nel complesso: buona funzione, dimostra navigazione in strutture
#    annidate, conteggio con dizionari, e max() con lambda. Bravo!


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- RISPOSTE QUIZ D'INGRESSO (Cap. 04 — Liste) ---
#
# 1. [20, 30, 40]
#    → numeri[1:4] prende gli indici 1, 2, 3 (il 4 è ESCLUSO).
#
# 2. FALSO
#    → .append() modifica la lista ma restituisce None, non la lista.
#      Se fai x = lista.append("a"), x sarà None.
#
# 3. enumerate(frutti, 1)
#    → enumerate() dà indice + valore; il secondo parametro (1) dice
#      da che numero partire per il contatore.
#
# 4. L'indice di partenza è sbagliato: prezzi[3:] dà [40, 50] (indici 3 e 4).
#    Per avere [30, 40, 50] serve prezzi[2:] (l'indice di 30 è 2, non 3).
#
# 5. sorted() crea una NUOVA lista ordinata senza modificare l'originale.
#    lista.sort() invece MODIFICA la lista originale e restituisce None.
#    In JS .sort() modifica l'array originale (come .sort() di Python).
#
# 6. ["Marco"]
#    → filter() con lambda n: len(n) > 4 tiene solo i nomi con più di 4
#      caratteri. "Marco" ha 5 lettere, "Anna" 4, "Luca" 4.
#
# 7. VERO
#    → Nella list comprehension, il "if" viene valutato prima: filtra gli
#      elementi che soddisfano la condizione, poi applica l'espressione
#      (x*2) solo a quelli che passano il filtro.
#
# 8. n**2  e  n % 2 == 0
#    → [n**2 for n in range(1, 11) if n % 2 == 0] dà [4, 16, 36, 64, 100]
#      Prima filtra i pari (2,4,6,8,10), poi eleva al quadrato.

# --- RISPOSTE QUIZ DI VERIFICA (Cap. 05 — Dizionari) ---
#
# 1. 3
#    → Parte con 2 chiavi ("nome", "eta"). Modifica "eta" (resta 2 chiavi),
#      poi aggiunge "citta" (diventa 3 chiavi). len() conta le chiavi.
#
# 2. KeyError! La chiave "font_size" non esiste nel dizionario.
#    Soluzione: usare config.get("font_size", valore_default) per evitare
#    il crash, oppure controllare prima con "font_size" in config.
#
# 3. VERO
#    → In Python, = NON copia un dizionario: crea solo un secondo nome
#      che punta allo STESSO oggetto. Per copiare serve .copy().
#      Attenzione: in PHP $copia = $array copia automaticamente!
#
# 4. .keys() restituisce solo le chiavi (es. ["nome", "prezzo"])
#    .values() restituisce solo i valori (es. ["Mouse", 29.99])
#    .items() restituisce coppie (chiave, valore) come tuple:
#    [("nome", "Mouse"), ("prezzo", 29.99)]
#
# 5. chiave, valore, items
#    → for chiave, valore in prodotto.items():
#      .items() restituisce tuple (chiave, valore) che vengono
#      spacchettate nelle due variabili.
#
# 6. {"Marco": 7, "Laura": 9}
#    → La dict comprehension filtra con if v >= 7, quindi tiene
#      Marco (7) e Laura (9), esclude Giulia (5).
#
# 7. FALSO
#    → .setdefault() imposta il valore SOLO se la chiave NON esiste.
#      Se la chiave c'è già, non fa nulla e restituisce il valore esistente.
#
# 8. get, 0
#    → conteggio.get(lettera, 0) + 1
#      .get(lettera, 0) restituisce il conteggio attuale della lettera,
#      oppure 0 se non è ancora stata contata. Poi si aggiunge 1.

# --- SOLUZIONE ESERCIZIO 1 ---
# film = {
#     "titolo": "Inception",
#     "regista": "Christopher Nolan",
#     "anno": 2010,
#     "genere": "Sci-Fi",
#     "voto": 9
# }
# for chiave, valore in film.items():
#     print(f"{chiave.capitalize()}: {valore}")
# film["attore_principale"] = "Leonardo DiCaprio"
# print(f"\nAggiunto: attore_principale = {film['attore_principale']}")

# --- SOLUZIONE ESERCIZIO 2 ---
# prodotti = [
#     {"nome": "Laptop", "prezzo": 999.99, "categoria": "Elettronica"},
#     {"nome": "Libro Python", "prezzo": 35.00, "categoria": "Libri"},
#     {"nome": "Cuffie", "prezzo": 79.99, "categoria": "Elettronica"},
#     {"nome": "Zaino", "prezzo": 59.99, "categoria": "Accessori"},
#     {"nome": "Libro AI", "prezzo": 42.00, "categoria": "Libri"},
# ]
# # a)
# print("Elettronica:")
# for p in prodotti:
#     if p["categoria"] == "Elettronica":
#         print(f"  {p['nome']}: {p['prezzo']}€")
# # b)
# totale = sum(p["prezzo"] for p in prodotti)
# print(f"Totale: {totale:.2f}€")
# # c)
# piu_costoso = max(prodotti, key=lambda p: p["prezzo"])
# print(f"Più costoso: {piu_costoso['nome']} ({piu_costoso['prezzo']}€)")
# # d)
# per_categoria = {}
# for p in prodotti:
#     cat = p["categoria"]
#     if cat not in per_categoria:
#         per_categoria[cat] = []
#     per_categoria[cat].append(p["nome"])
# print(f"Per categoria: {per_categoria}")

# --- SOLUZIONE ESERCIZIO 3 ---
# voti_studenti = {"Marco": 75, "Laura": 92, "Giulia": 58, "Luca": 88, "Anna": 45}
# # a)
# promossi = {nome: voto for nome, voto in voti_studenti.items() if voto >= 60}
# print(f"Promossi: {promossi}")
# # b)
# def giudizio(voto):
#     if voto >= 90: return "Eccellente"
#     if voto >= 70: return "Buono"
#     if voto >= 60: return "Sufficiente"
#     return "Insufficiente"
# giudizi = {nome: giudizio(voto) for nome, voto in voti_studenti.items()}
# print(f"Giudizi: {giudizi}")

# --- SOLUZIONE ESERCIZIO 4 (Conta Parole 🎯) ---
# def conta_parole(testo):
#     """Conta le occorrenze di ogni parola nel testo.
#     Le parole vengono convertite in minuscolo."""
#     if not testo.strip():
#         return {}
#     conteggio = {}
#     for parola in testo.lower().split():
#         conteggio[parola] = conteggio.get(parola, 0) + 1
#     return conteggio
#
# print(conta_parole("Ciao mondo ciao a tutto il mondo"))
# # {'ciao': 2, 'mondo': 2, 'a': 1, 'tutto': 1, 'il': 1}
# print(conta_parole(""))  # {}

# --- SOLUZIONE ESERCIZIO 5 (Lambda con Dizionari) ---
# film_lista = [
#     {"titolo": "Inception", "anno": 2010, "voto": 8.8},
#     {"titolo": "Interstellar", "anno": 2014, "voto": 8.6},
#     {"titolo": "The Matrix", "anno": 1999, "voto": 8.7},
#     {"titolo": "Parasite", "anno": 2019, "voto": 8.5},
#     {"titolo": "Oppenheimer", "anno": 2023, "voto": 8.3},
# ]
#
# # a) Per voto decrescente
# per_voto = sorted(film_lista, key=lambda f: f["voto"], reverse=True)
# print("\n=== Film per voto ===")
# for f in per_voto:
#     print(f"  {f['titolo']}: ⭐ {f['voto']}")
#
# # b) Film dal 2010 in poi
# recenti = list(filter(lambda f: f["anno"] >= 2010, film_lista))
# print(f"\nDal 2010: {[f['titolo'] for f in recenti]}")
#
# # c) Lista di stringhe formattate
# stringhe = list(map(lambda f: f"{f['titolo']} ({f['anno']}) — ⭐ {f['voto']}", film_lista))
# for s in stringhe:
#     print(s)
#
# # d) Film più vecchio
# piu_vecchio = min(film_lista, key=lambda f: f["anno"])
# print(f"\nPiù vecchio: {piu_vecchio['titolo']} ({piu_vecchio['anno']})")
#
# # e) Per anno con enumerate
# per_anno = sorted(film_lista, key=lambda f: f["anno"])
# print("\n=== Cronologia ===")
# for i, f in enumerate(per_anno, 1):
#     print(f"  {i}. {f['titolo']} ({f['anno']})")

# --- SOLUZIONE ESERCIZIO 6 (enumerate + dizionari) ---
# inventario = {
#     "T-shirt": 45,
#     "Jeans": 12,
#     "Sneakers": 8,
#     "Cappello": 30,
#     "Giacca": 3,
# }
#
# # a) Tabella numerata
# print("\n=== Inventario ===")
# for i, (prodotto, quantita) in enumerate(inventario.items(), 1):
#     print(f"  {i}. {prodotto}: {quantita} pezzi")
#
# # b) Scorta bassa
# print("\n=== Scorta bassa (<10 pezzi) ===")
# for i, (prodotto, quantita) in enumerate(inventario.items(), 1):
#     if quantita < 10:
#         print(f"  ⚠️ Posizione {i}: {prodotto} — solo {quantita} pezzi!")
#
# # c) Dict comprehension — solo prodotti con più di 15 pezzi
# abbondanti = {prod: qty for prod, qty in inventario.items() if qty > 15}
# print(f"\nBen forniti (>15): {abbondanti}")

# --- SOLUZIONE ESERCIZIO 7 (Raggruppare per Chiave 🎯) ---
# def raggruppa_per(lista_dizionari, chiave):
#     """Raggruppa una lista di dizionari per il valore di una chiave.
#     Come il GROUP BY di SQL o il groupBy() di Laravel/Eloquent."""
#     risultato = {}
#     for elemento in lista_dizionari:
#         valore_chiave = elemento[chiave]
#         if valore_chiave not in risultato:
#             risultato[valore_chiave] = []
#         risultato[valore_chiave].append(elemento)
#     return risultato
#
# prodotti = [
#     {"nome": "Laptop", "prezzo": 999.99, "categoria": "Elettronica"},
#     {"nome": "Libro Python", "prezzo": 35.00, "categoria": "Libri"},
#     {"nome": "Cuffie", "prezzo": 79.99, "categoria": "Elettronica"},
#     {"nome": "Zaino", "prezzo": 59.99, "categoria": "Accessori"},
#     {"nome": "Libro AI", "prezzo": 42.00, "categoria": "Libri"},
# ]
# per_cat = raggruppa_per(prodotti, "categoria")
# for cat, items in per_cat.items():
#     print(f"\n{cat}:")
#     for p in items:
#         print(f"  - {p['nome']}: {p['prezzo']}€")

# --- SOLUZIONE ESERCIZIO 8 (Simula API) ---
# def processa_ordini(ordini):
#     """Processa una lista di ordini e restituisce un report riassuntivo.
#     Simula l'elaborazione di dati da un'API e-commerce."""
#     conteggio_citta = {}
#     conteggio_prodotti = {}
#     for ordine in ordini:
#         citta = ordine["cliente"]["indirizzo"]["citta"]
#         conteggio_citta[citta] = conteggio_citta.get(citta, 0) + 1
#         for prod in ordine["prodotti"]:
#             nome = prod["nome"]
#             conteggio_prodotti[nome] = conteggio_prodotti.get(nome, 0) + prod["quantita"]
#     return {
#         "totale_ordini": len(ordini),
#         "fatturato_totale": round(sum(o["totale"] for o in ordini), 2),
#         "citta_piu_ordini": max(conteggio_citta, key=conteggio_citta.get),
#         "prodotto_piu_venduto": max(conteggio_prodotti, key=conteggio_prodotti.get)
#     }
