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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


# ESERCIZIO 3 (Medio — Dict Comprehension):
# Dato il dizionario:
#   voti_studenti = {"Marco": 75, "Laura": 92, "Giulia": 58, "Luca": 88, "Anna": 45}
# a) Crea un nuovo dizionario con solo gli studenti promossi (voto >= 60)
# b) Crea un nuovo dizionario con i giudizi:
#    {"Marco": "Buono", "Laura": "Eccellente", ...}
#    (>=90: Eccellente, >=70: Buono, >=60: Sufficiente, <60: Insufficiente)
#
# Scrivi il tuo codice qui sotto:
# ...


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
# ...


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
# ...


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
# ...


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
# ...


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
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

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
