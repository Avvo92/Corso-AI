"""
============================================================================
 MODULO 1 — ESERCIZIO 04: Le Liste
 Liste, Slicing, List Comprehension, Lambda con le Liste
============================================================================

 TEORIA: Le Liste Python = Gli Array PHP e JavaScript

 Se conosci gli array PHP e JavaScript, le Liste Python sono lo stesso
 concetto con qualche superpotere in più.

 Confronto a tre — Le operazioni più comuni:

   Operazione          PHP                        JavaScript                  Python
   ─────────────────────────────────────────────────────────────────────────────────
   Creare              $frutti = ["mela","pera"];  let frutti = ["mela"];      frutti = ["mela", "pera"]
   Aggiungere          array_push($f, "banana");  frutti.push("banana");      frutti.append("banana")
   Lunghezza           count($frutti);            frutti.length;              len(frutti)
   Accedere            $frutti[0];                frutti[0];                  frutti[0]
   Ultimo elemento     end($frutti);              frutti[frutti.length-1];    frutti[-1]
   Rimuovere (pos.)    array_splice($f, 1, 1);   frutti.splice(1, 1);       frutti.pop(1)
   Cercare             in_array("mela", $f);      frutti.includes("mela");   "mela" in frutti
   Porzione            array_slice($f, 1, 3);     frutti.slice(1, 3);        frutti[1:3]

 Note sui metodi PHP:
   array_push()   → aggiunge uno o più elementi in fondo all'array
   count()        → restituisce il numero di elementi (come .length in JS)
   end()          → sposta il puntatore all'ultimo elemento e lo restituisce
   array_splice() → rimuove (e opzionalmente sostituisce) elementi dall'array
   in_array()     → controlla se un valore esiste nell'array (restituisce true/false)
   array_slice()  → estrae una porzione dell'array (senza modificare l'originale)

 Note sui metodi JavaScript:
   .push()        → aggiunge un elemento in fondo all'array
   .length        → proprietà (non metodo!) che dà il numero di elementi
   .splice(i, n)  → rimuove n elementi dalla posizione i (MODIFICA l'array)
   .includes()    → controlla se un valore esiste (restituisce true/false)
   .slice(i, j)   → estrae una porzione dall'indice i a j (SENZA modificare)

 IL SUPERPOTERE: lo Slicing
 In PHP usi array_slice($arr, inizio, lunghezza).
 In JavaScript usi arr.slice(inizio, fine).
 In Python puoi farlo direttamente con le parentesi quadre:
   lista[inizio:fine]           → come .slice() in JS / array_slice() in PHP
   lista[inizio:fine:passo]     → non esiste in JS o PHP! Puoi saltare elementi.

 Perché ti serve per l'AI?
 Quando lavorerai con dataset e immagini, lo slicing ti servirà OGNI GIORNO:
   - Prendere le prime 100 righe di un dataset
   - Selezionare un pezzo di un'immagine
   - Dividere i dati in training e test

 LAMBDA — Ripasso rapido:
 Ricordi le lambda dal capitolo 03? Sono mini-funzioni usa-e-getta, di una
 sola riga. In questo capitolo le userai MOLTO con le liste:
   - sorted(lista, key=lambda x: ...) per ordinamenti personalizzati
   - filter(lambda x: ..., lista)     per filtrare elementi
   - map(lambda x: ..., lista)        per trasformare elementi

 In JavaScript sarebbero le arrow function:
   lista.sort((a, b) => a.prezzo - b.prezzo)
   lista.filter(x => x > 10)
   lista.map(x => x * 2)

 In PHP sarebbero le short closure:
   usort($lista, fn($a, $b) => $a['prezzo'] - $b['prezzo'])
   array_filter($lista, fn($x) => $x > 10)
   array_map(fn($x) => $x * 2, $lista)

 Stessa idea, sintassi diversa. Vedile in azione negli esempi qui sotto.

============================================================================
"""

# ==========================================================================
# PARTE 1: Creare e Manipolare Liste
# ==========================================================================

# RIPASSO — f-string: ricordi? Sono le stringhe con la f davanti che ti
# permettono di mettere variabili dentro {} — come i template literal
# `${variabile}` in JS o "$variabile" in PHP.

# RIPASSO — len(): è una FUNZIONE (non un metodo!), si scrive len(lista),
# non lista.len(). In JS usi .length (proprietà), in PHP usi count() (funzione).

# Creare una lista:
# PHP:        $frutti = ["mela", "banana", "arancia"];
# JavaScript: let frutti = ["mela", "banana", "arancia"];
# Python:
frutti = ["mela", "banana", "arancia", "kiwi", "pera"]
print(f"Lista frutti: {frutti}")
print(f"Numero di elementi: {len(frutti)}")   # len() = count() in PHP, .length in JS

# Accedere agli elementi (identico in tutti e tre i linguaggi):
print(f"\nPrimo elemento: {frutti[0]}")        # Uguale in PHP, JS e Python
print(f"Ultimo elemento: {frutti[-1]}")         # NOVITÀ! -1 = ultimo elemento
print(f"Penultimo: {frutti[-2]}")               # -2 = penultimo, ecc.

# In PHP per l'ultimo: end($frutti) oppure $frutti[count($frutti) - 1]
# In JS per l'ultimo: frutti[frutti.length - 1] oppure frutti.at(-1)
# In Python basta: frutti[-1]   ← Molto più comodo!

# Aggiungere elementi:
# PHP: array_push($frutti, "mango")  oppure  $frutti[] = "mango"
# JS:  frutti.push("mango")
frutti.append("mango")            # Python: .append() aggiunge in fondo

# PHP: array_splice($frutti, 1, 0, ["fragola"])  — inserisce senza rimuovere
# JS:  frutti.splice(1, 0, "fragola")            — splice(posizione, 0, elemento)
frutti.insert(1, "fragola")       # Python: .insert(posizione, elemento)
print(f"\nDopo append e insert: {frutti}")

# Rimuovere elementi:
# PHP: unset($frutti[array_search("banana", $frutti)]); — cerca e rimuove
# JS:  frutti.splice(frutti.indexOf("banana"), 1);      — trova indice e rimuove
frutti.remove("banana")           # Python: rimuove per VALORE direttamente!

# PHP: array_pop($frutti)         — rimuove e restituisce l'ultimo
# JS:  frutti.pop()               — rimuove e restituisce l'ultimo
ultimo = frutti.pop()             # Python: uguale a JS!
secondo = frutti.pop(1)           # Rimuove e restituisce alla posizione 1 (solo Python)
print(f"Rimossi: {ultimo}, {secondo}")
print(f"Lista attuale: {frutti}")

# Controllare se un elemento esiste:
# PHP:        in_array("mela", $frutti)    — nota: prima il valore, poi l'array!
# JavaScript: frutti.includes("mela")       — .includes() restituisce true/false
# Python:     "mela" in frutti              — il più leggibile dei tre!

print(f"\n'mela' è nella lista? {'mela' in frutti}")
print(f"'banana' è nella lista? {'banana' in frutti}")

# ==========================================================================
# PARTE 2: Lo Slicing — Il Superpotere
# ==========================================================================

numeri = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"\nLista originale: {numeri}")

# Sintassi: lista[inizio:fine]
# RIPASSO — ATTENZIONE: 'fine' è ESCLUSO! Proprio come range() — ricordi
# dal capitolo 02 che range(1, 20) arriva a 19? Stessa regola qui:
# lista[2:5] prende gli indici 2, 3, 4 — il 5 è escluso.

print(f"\nnumeri[2:5]   = {numeri[2:5]}")     # [2, 3, 4] — dal 2 al 4
print(f"numeri[:4]    = {numeri[:4]}")         # [0, 1, 2, 3] — dall'inizio al 3
print(f"numeri[6:]    = {numeri[6:]}")         # [6, 7, 8, 9] — dal 6 alla fine
print(f"numeri[-3:]   = {numeri[-3:]}")        # [7, 8, 9] — gli ultimi 3

# Con il PASSO (terzo parametro):
# lista[inizio:fine:passo]
print(f"\nnumeri[::2]   = {numeri[::2]}")      # [0, 2, 4, 6, 8] — ogni 2
print(f"numeri[1::2]  = {numeri[1::2]}")       # [1, 3, 5, 7, 9] — dispari
print(f"numeri[::-1]  = {numeri[::-1]}")       # [9, 8, 7, ...0] — AL CONTRARIO!

# Esempio pratico — dividere dati in training e test (preview del ML):
dati = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
training = dati[:7]    # primi 70% dei dati
test = dati[7:]        # ultimi 30% dei dati
print(f"\nDati training (70%): {training}")
print(f"Dati test (30%):     {test}")

# ==========================================================================
# PARTE 3: Metodi Utili delle Liste
# ==========================================================================

voti = [75, 92, 88, 65, 95, 70, 85]

print(f"\n=== Metodi utili ===")
print(f"Lista: {voti}")
print(f"Lunghezza: {len(voti)}")
print(f"Somma: {sum(voti)}")
print(f"Minimo: {min(voti)}")
print(f"Massimo: {max(voti)}")
print(f"Media: {sum(voti) / len(voti):.1f}")

# Ordinare:
# PHP:  sort($voti)        — MODIFICA l'array originale, non ne crea uno nuovo
# JS:   voti.sort()        — MODIFICA l'array originale, e attenzione:
#                             sort() in JS ordina come STRINGHE per default!
#                             [10, 2, 1].sort() → [1, 10, 2] (sbagliato!)
#                             Devi fare: .sort((a,b) => a - b) per i numeri.
# Python: sorted(voti)     — crea una NUOVA lista ordinata (non modifica l'originale)
voti_ordinati = sorted(voti)           # Crea una NUOVA lista ordinata
print(f"Ordinati (crescente): {voti_ordinati}")

voti_decrescenti = sorted(voti, reverse=True)
print(f"Ordinati (decrescente): {voti_decrescenti}")

# .sort() modifica la lista ORIGINALE (attenzione!):
# voti.sort()  ← Questo MODIFICA voti, non crea una copia!

# Trovare la posizione di un elemento:
# PHP:  array_search(95, $voti)  — restituisce l'indice, o false se non trovato
# JS:   voti.indexOf(95)         — restituisce l'indice, o -1 se non trovato
# Python:
posizione = voti.index(95)  # Restituisce l'indice. Se non trovato: errore (ValueError)!
print(f"Il voto 95 è alla posizione: {posizione}")

# Contare le occorrenze:
# PHP:  array_count_values($array) — restituisce un array associativo con i conteggi
# JS:   non ha un metodo nativo, devi usare .filter().length o un reduce
# Python:
numeri_ripetuti = [1, 2, 3, 2, 1, 2, 4, 2]
print(f"\nIl 2 appare {numeri_ripetuti.count(2)} volte")

# ==========================================================================
# PARTE 4: List Comprehension — Il .map() e .filter() di Python
# ==========================================================================

# Trasformare o filtrare ogni elemento di una lista.
#
# In PHP usi array_map() e array_filter():
#   $doppi = array_map(fn($n) => $n * 2, $numeri);
#     // array_map() applica una funzione a ogni elemento dell'array
#     // fn($n) => $n * 2 è una arrow function che raddoppia ogni numero
#     // Nota: in PHP il PRIMO argomento è la funzione, il SECONDO l'array!
#   $pari = array_filter($numeri, fn($n) => $n % 2 === 0);
#     // array_filter() tiene solo gli elementi per cui la funzione ritorna true
#
# In JavaScript usi .map() e .filter():
#   const doppi = numeri.map(n => n * 2);
#     // .map() crea un NUOVO array applicando la funzione a ogni elemento
#     // n => n * 2 è una arrow function: prende n, restituisce n * 2
#   const pari = numeri.filter(n => n % 2 === 0);
#     // .filter() crea un NUOVO array con solo gli elementi che passano il test
#     // n % 2 === 0 controlla se n è pari (resto della divisione per 2 = 0)
#
# In Python usi le LIST COMPREHENSION — più concise e "Pythoniche":

numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# .map() equivalente — trasforma ogni elemento:
doppi = [n * 2 for n in numeri]
print(f"\n=== List Comprehension ===")
print(f"Originali: {numeri}")
print(f"Doppi:     {doppi}")

# .filter() equivalente — filtra gli elementi:
pari = [n for n in numeri if n % 2 == 0]
print(f"Solo pari: {pari}")

# .map() + .filter() insieme:
doppi_dei_pari = [n * 2 for n in numeri if n % 2 == 0]
print(f"Doppi dei pari: {doppi_dei_pari}")

# Lettura della sintassi (da sinistra a destra):
# [COSA_FARE  for ELEMENTO in LISTA  if CONDIZIONE]
#  ↑ output    ↑ ciclo                ↑ filtro (opzionale)

# Esempio pratico — convertire una lista di prezzi in euro a dollari:
prezzi_eur = [10.00, 25.50, 99.99, 149.00]
tasso_cambio = 1.08
prezzi_usd = [prezzo * tasso_cambio for prezzo in prezzi_eur]
print(f"\nPrezzi EUR: {prezzi_eur}")
print(f"Prezzi USD: {[round(p, 2) for p in prezzi_usd]}")

# Esempio — estrarre le iniziali dai nomi:
nomi = ["Marco Rossi", "Laura Bianchi", "Giulia Verdi"]
iniziali = [nome[0] + cognome[0] for nome, cognome in [n.split() for n in nomi]]
# Troppo complicato? Facciamolo passo per passo:
iniziali_semplice = []
for nome_completo in nomi:
    parti = nome_completo.split()  # ["Marco", "Rossi"]
    iniziale = parti[0][0] + parti[1][0]  # "M" + "R" = "MR"
    iniziali_semplice.append(iniziale)
print(f"Iniziali: {iniziali_semplice}")

# ==========================================================================
# PARTE 5: Liste di Liste (Array Multidimensionali)
# ==========================================================================

# In AI lavorerai SPESSO con "liste di liste" (matrici).
# Pensa a una tabella HTML: ogni riga è una lista, e la tabella è una
# lista di righe.

tabella_voti = [
    ["Marco",  85, 92, 78],
    ["Laura",  95, 88, 90],
    ["Giulia", 70, 75, 80],
]

print(f"\n=== Liste di liste (matrice) ===")
print(f"Tabella: {tabella_voti}")
print(f"Prima riga: {tabella_voti[0]}")           # ["Marco", 85, 92, 78]
print(f"Nome prima riga: {tabella_voti[0][0]}")    # "Marco"
print(f"Secondo voto di Laura: {tabella_voti[1][2]}")  # 88

# Iterare su una matrice:
# RIPASSO — enumerate(): ricordi? Dà indice + valore insieme, come
# .forEach((val, index) => ...) in JS. Perfetto per numerare le righe.
print("\n=== Pagella ===")
for i, riga in enumerate(tabella_voti):
    nome = riga[0]
    voti = riga[1:]  # tutti gli elementi tranne il primo (slicing!)
    media = sum(voti) / len(voti)
    print(f"Studente {i + 1}: {nome} — voti {voti}, media {media:.1f}")


# ==========================================================================
# PARTE 6: Lambda con le Liste — Rinforzo
# ==========================================================================

# Le lambda sono mini-funzioni usa-e-getta. In JS sono le arrow function
# (() =>), in PHP sono le short closure (fn() =>). In Python: lambda x: ...
#
# Perché le rivediamo qui? Perché con le LISTE diventano potentissime.
# Tre usi principali: sorted(), filter(), map().

# --- USO 1: sorted() con lambda ---
# Ricordi sorted() dal capitolo 03? Crea una NUOVA lista ordinata.
# Con una lambda come "key", decidi TU in base a cosa ordinare.

prodotti = [
    {"nome": "Mouse", "prezzo": 25.99},
    {"nome": "Tastiera", "prezzo": 49.99},
    {"nome": "Monitor", "prezzo": 199.99},
    {"nome": "Cuffie", "prezzo": 35.00},
    {"nome": "Webcam", "prezzo": 59.90},
]

# Ordinare per prezzo (crescente):
# La lambda dice: "per ogni prodotto p, usa p["prezzo"] come valore di confronto"
# JS equivalente:  prodotti.sort((a, b) => a.prezzo - b.prezzo)
# PHP equivalente: usort($prodotti, fn($a, $b) => $a['prezzo'] <=> $b['prezzo'])
per_prezzo = sorted(prodotti, key=lambda p: p["prezzo"])

print("\n=== Prodotti per prezzo (crescente) ===")
for p in per_prezzo:
    print(f"  {p['nome']}: {p['prezzo']:.2f}€")

# Ordinare per nome (alfabetico):
per_nome = sorted(prodotti, key=lambda p: p["nome"])
print("\n=== Prodotti per nome (A-Z) ===")
for p in per_nome:
    print(f"  {p['nome']}: {p['prezzo']:.2f}€")

# Ordinare per prezzo (decrescente) — aggiungi reverse=True:
piu_cari = sorted(prodotti, key=lambda p: p["prezzo"], reverse=True)
print("\n=== Prodotti più cari prima ===")
for p in piu_cari:
    print(f"  {p['nome']}: {p['prezzo']:.2f}€")

# --- USO 2: filter() con lambda ---
# filter() tiene solo gli elementi per cui la lambda restituisce True.
# Restituisce un oggetto "filter" — lo avvolgiamo con list() per vederlo.
#
# JS equivalente:  prodotti.filter(p => p.prezzo < 50)
# PHP equivalente: array_filter($prodotti, fn($p) => $p['prezzo'] < 50)

economici = list(filter(lambda p: p["prezzo"] < 50, prodotti))
print("\n=== Prodotti sotto 50€ (filter + lambda) ===")
for p in economici:
    print(f"  {p['nome']}: {p['prezzo']:.2f}€")

# Lo stesso risultato con list comprehension (spesso più leggibile):
economici_v2 = [p for p in prodotti if p["prezzo"] < 50]
# Entrambi funzionano! La list comprehension è più "Pythonica",
# ma filter + lambda è utile quando passi funzioni ad altre funzioni.

# --- USO 3: map() con lambda ---
# map() applica la lambda a OGNI elemento e crea un nuovo risultato.
#
# JS equivalente:  prodotti.map(p => p.nome)
# PHP equivalente: array_map(fn($p) => $p['nome'], $prodotti)

solo_nomi = list(map(lambda p: p["nome"], prodotti))
print(f"\nSolo i nomi: {solo_nomi}")

# Aggiungere l'IVA a tutti i prezzi:
con_iva = list(map(lambda p: {**p, "prezzo_iva": round(p["prezzo"] * 1.22, 2)}, prodotti))
# {**p, "prezzo_iva": ...} crea un NUOVO dizionario con tutto quello che c'era in p
# PIÙ un campo "prezzo_iva". Il ** è come lo spread operator (...) in JS!
print("\n=== Prezzi con IVA (map + lambda) ===")
for p in con_iva:
    print(f"  {p['nome']}: {p['prezzo']:.2f}€ → con IVA: {p['prezzo_iva']:.2f}€")

# --- RIEPILOGO LAMBDA CON LE LISTE ---
# sorted(lista, key=lambda x: ...)  → ordina in base a un criterio
# filter(lambda x: ..., lista)      → tiene solo chi soddisfa la condizione
# map(lambda x: ..., lista)         → trasforma ogni elemento
#
# Ricorda: filter() e map() restituiscono oggetti "pigri" — usa list() per
# ottenere una lista vera. Oppure usa le list comprehension che sono più leggibili!


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile — Slicing):
# Data la lista: mesi = ["Gen","Feb","Mar","Apr","Mag","Giu","Jul","Ago","Set","Ott","Nov","Dic"]
# Usando SOLO lo slicing (senza cicli), stampa:
#   a) I primi 3 mesi (Q1)
#   b) I mesi estivi (Giu, Jul, Ago)
#   c) L'ultimo trimestre (Ott, Nov, Dic)
#   d) I mesi al contrario
#   e) I mesi alterni (Gen, Mar, Mag, Jul, Set, Nov)
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio — List Comprehension):
# Data la lista di temperature:
#   temperature_f = [32, 50, 68, 77, 86, 95, 104]
# a) Crea una nuova lista con le temperature convertite in Celsius
#    (C = (F - 32) * 5/9), arrotondate a 1 decimale.
# b) Crea una lista con solo le temperature Celsius sopra i 25°C.
# c) Crea una lista di stringhe tipo: ["32°F = 0.0°C", "50°F = 10.0°C", ...]
#
# Scrivi il tuo codice qui sotto:
# ...


# 🎯 [COLLOQUIO] — ESERCIZIO 3 (Medio — Rimuovi Duplicati):
# Questo esercizio replica una domanda CLASSICA dei colloqui tecnici.
#
# Scrivi una funzione 'rimuovi_duplicati(lista)' che prende una lista e
# restituisce una nuova lista SENZA elementi duplicati, mantenendo l'ordine.
# Es: rimuovi_duplicati([3, 1, 2, 3, 1, 4]) → [3, 1, 2, 4]
#
# Requisiti:
#   1. La funzione deve avere una docstring (ricordi? """ ... """)
#   2. L'ordine originale deve essere mantenuto
#   3. La lista originale NON deve essere modificata
#   4. Testa con: [3, 1, 2, 3, 1, 4] e con una lista vuota []
#
# Suggerimento: usa una lista di appoggio e 'if elemento not in ...'
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Medio — Lambda con sorted):
# Hai questa lista di studenti:
#   studenti = [
#       {"nome": "Marco", "voto": 72, "eta": 22},
#       {"nome": "Laura", "voto": 95, "eta": 20},
#       {"nome": "Giulia", "voto": 88, "eta": 23},
#       {"nome": "Luca", "voto": 65, "eta": 21},
#       {"nome": "Anna", "voto": 91, "eta": 22},
#   ]
#
# Usando sorted() con una lambda come key:
#   a) Ordina per voto decrescente (i migliori prima) e stampa la classifica
#   b) Ordina per età crescente e stampa
#   c) Ordina per nome alfabetico e stampa
#   d) Usa filter() con una lambda per trovare chi ha voto >= 80
#   e) Usa map() con una lambda per creare una lista di sole stringhe
#      tipo: ["Marco: 72", "Laura: 95", ...]
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Medio — Lambda con filter e map):
# Hai questa lista di prodotti del tuo e-commerce:
#   catalogo = [
#       {"nome": "T-shirt", "prezzo": 19.99, "disponibile": True},
#       {"nome": "Jeans", "prezzo": 59.99, "disponibile": False},
#       {"nome": "Sneakers", "prezzo": 89.99, "disponibile": True},
#       {"nome": "Cappello", "prezzo": 14.99, "disponibile": True},
#       {"nome": "Giacca", "prezzo": 129.99, "disponibile": False},
#   ]
#
# a) Usa filter + lambda per ottenere solo i prodotti disponibili
# b) Usa filter + lambda per ottenere solo i prodotti sotto 50€
# c) Usa map + lambda per creare una lista di stringhe tipo:
#    "T-shirt — 19.99€ (disponibile)" o "Jeans — 59.99€ (esaurito)"
# d) Usa sorted + lambda per ordinare per prezzo crescente
# e) Combina: prendi solo i disponibili, ordinali per prezzo, e stampa
#
# Scrivi il tuo codice qui sotto:
# ...


# 🎯 [COLLOQUIO] — ESERCIZIO 6 (Sfida — Inverti senza .reverse()):
# Questo è un altro classico da colloquio tecnico.
#
# Scrivi una funzione 'inverti_lista(lista)' che inverte l'ordine degli
# elementi SENZA usare .reverse(), reversed() o lo slicing [::-1].
# Es: inverti_lista([1, 2, 3, 4, 5]) → [5, 4, 3, 2, 1]
#
# Requisiti:
#   1. Docstring obbligatoria
#   2. NON usare .reverse(), reversed(), o [::-1]
#   3. La lista originale NON deve essere modificata
#   4. Testa con: [1, 2, 3, 4, 5], ["a", "b", "c"], e una lista vuota []
#
# Suggerimento: pensa a come faresti con un ciclo for e range()
# (ricordi? range(inizio, fine, passo) — il passo può essere negativo!)
#
# Scrivi il tuo codice qui sotto:
# ...


# 🎯 [COLLOQUIO] — ESERCIZIO 7 (Sfida — Elemento più frequente):
# Domanda frequente nei colloqui di livello junior/mid.
#
# Scrivi una funzione 'piu_frequente(lista)' che restituisce l'elemento
# che appare più volte nella lista.
# Es: piu_frequente([1, 3, 2, 1, 4, 1, 3]) → 1
# Es: piu_frequente(["a", "b", "a", "c", "a"]) → "a"
#
# Requisiti:
#   1. Docstring obbligatoria
#   2. Usa .count() — ricordi? Conta quante volte un elemento appare
#   3. Restituisci l'elemento (non il conteggio)
#   4. Testa con: [1, 3, 2, 1, 4, 1, 3] e ["mela", "pera", "mela"]
#
# Suggerimento avanzato: puoi usare max() con una lambda!
#   max(lista, key=lambda x: ...) restituisce l'elemento con il valore
#   più alto di "qualcosa". Quel "qualcosa" lo decidi tu con la lambda.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 8 (Sfida — Appiattisci):
# Crea una funzione 'appiattisci(lista_di_liste)' che prende una lista
# di liste e restituisce una singola lista con tutti gli elementi.
# Es: appiattisci([[1,2], [3,4], [5]]) → [1, 2, 3, 4, 5]
#
# Requisiti:
#   1. Docstring obbligatoria
#   2. Fallo in DUE modi: uno con ciclo for, uno con list comprehension
#   3. Testa con: [[1,2], [3,4], [5]] e con [["a","b"], ["c"]]
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 9 (Sfida — Preview AI):
# Simula la divisione di un dataset in training e test.
# Hai questa lista di 20 numeri:
#   dati = list(range(1, 21))  # [1, 2, 3, ..., 20]
#     (ricordi range()? Il 21 è ESCLUSO, quindi ottieni da 1 a 20)
#
# a) Dividi in 80% training (primi 16) e 20% test (ultimi 4) usando slicing
# b) Dividi il training in "batch" (gruppi) da 4 elementi ciascuno
#    Suggerimento: usa slicing con range → training[i:i+4] per ogni batch
# c) Stampa ogni batch numerato: "Batch 1: [1, 2, 3, 4]", ecc.
#    (usa enumerate() per avere il numero del batch!)
# Questo è ESATTAMENTE come funziona il training di una rete neurale!
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# mesi = ["Gen","Feb","Mar","Apr","Mag","Giu","Jul","Ago","Set","Ott","Nov","Dic"]
# print(f"Q1: {mesi[:3]}")
# print(f"Estivi: {mesi[5:8]}")
# print(f"Ultimo trimestre: {mesi[9:]}")    # oppure mesi[-3:]
# print(f"Al contrario: {mesi[::-1]}")
# print(f"Alterni: {mesi[::2]}")

# --- SOLUZIONE ESERCIZIO 2 ---
# temperature_f = [32, 50, 68, 77, 86, 95, 104]
# celsius = [round((f - 32) * 5/9, 1) for f in temperature_f]
# print(f"Celsius: {celsius}")
# calde = [c for c in celsius if c > 25]
# print(f"Sopra 25°C: {calde}")
# stringhe = [f"{f}°F = {round((f-32)*5/9, 1)}°C" for f in temperature_f]
# print(f"Formattate: {stringhe}")

# --- SOLUZIONE ESERCIZIO 3 (Rimuovi Duplicati) ---
# def rimuovi_duplicati(lista):
#     """Rimuove duplicati mantenendo l'ordine originale.
#     La lista originale non viene modificata."""
#     risultato = []
#     for elemento in lista:
#         if elemento not in risultato:
#             risultato.append(elemento)
#     return risultato
#
# print(rimuovi_duplicati([3, 1, 2, 3, 1, 4]))  # [3, 1, 2, 4]
# print(rimuovi_duplicati([]))                    # []

# --- SOLUZIONE ESERCIZIO 4 (Lambda con sorted) ---
# studenti = [
#     {"nome": "Marco", "voto": 72, "eta": 22},
#     {"nome": "Laura", "voto": 95, "eta": 20},
#     {"nome": "Giulia", "voto": 88, "eta": 23},
#     {"nome": "Luca", "voto": 65, "eta": 21},
#     {"nome": "Anna", "voto": 91, "eta": 22},
# ]
#
# # a) Per voto decrescente
# per_voto = sorted(studenti, key=lambda s: s["voto"], reverse=True)
# print("\n=== Classifica per voto ===")
# for i, s in enumerate(per_voto, 1):
#     print(f"  {i}° {s['nome']}: {s['voto']}")
#
# # b) Per età crescente
# per_eta = sorted(studenti, key=lambda s: s["eta"])
# print("\n=== Per età ===")
# for s in per_eta:
#     print(f"  {s['nome']}: {s['eta']} anni")
#
# # c) Per nome alfabetico
# per_nome = sorted(studenti, key=lambda s: s["nome"])
# print("\n=== Per nome ===")
# for s in per_nome:
#     print(f"  {s['nome']}")
#
# # d) Filter: voto >= 80
# bravi = list(filter(lambda s: s["voto"] >= 80, studenti))
# print("\n=== Voto >= 80 ===")
# for s in bravi:
#     print(f"  {s['nome']}: {s['voto']}")
#
# # e) Map: lista di stringhe
# stringhe = list(map(lambda s: f"{s['nome']}: {s['voto']}", studenti))
# print(f"\nStringhe: {stringhe}")

# --- SOLUZIONE ESERCIZIO 5 (Lambda con filter e map) ---
# catalogo = [
#     {"nome": "T-shirt", "prezzo": 19.99, "disponibile": True},
#     {"nome": "Jeans", "prezzo": 59.99, "disponibile": False},
#     {"nome": "Sneakers", "prezzo": 89.99, "disponibile": True},
#     {"nome": "Cappello", "prezzo": 14.99, "disponibile": True},
#     {"nome": "Giacca", "prezzo": 129.99, "disponibile": False},
# ]
#
# # a) Solo disponibili
# disponibili = list(filter(lambda p: p["disponibile"], catalogo))
# print("\n=== Disponibili ===")
# for p in disponibili:
#     print(f"  {p['nome']}: {p['prezzo']:.2f}€")
#
# # b) Sotto 50€
# economici = list(filter(lambda p: p["prezzo"] < 50, catalogo))
# print("\n=== Sotto 50€ ===")
# for p in economici:
#     print(f"  {p['nome']}: {p['prezzo']:.2f}€")
#
# # c) Stringhe formattate
# desc = list(map(
#     lambda p: f"{p['nome']} — {p['prezzo']:.2f}€ ({'disponibile' if p['disponibile'] else 'esaurito'})",
#     catalogo
# ))
# for d in desc:
#     print(d)
#
# # d) Ordinati per prezzo
# per_prezzo = sorted(catalogo, key=lambda p: p["prezzo"])
# print("\n=== Per prezzo ===")
# for p in per_prezzo:
#     print(f"  {p['nome']}: {p['prezzo']:.2f}€")
#
# # e) Combo: disponibili, ordinati per prezzo
# combo = sorted(
#     filter(lambda p: p["disponibile"], catalogo),
#     key=lambda p: p["prezzo"]
# )
# print("\n=== Disponibili per prezzo ===")
# for p in combo:
#     print(f"  {p['nome']}: {p['prezzo']:.2f}€")

# --- SOLUZIONE ESERCIZIO 6 (Inverti senza .reverse()) ---
# def inverti_lista(lista):
#     """Inverte l'ordine senza usare .reverse(), reversed() o [::-1]."""
#     risultato = []
#     for i in range(len(lista) - 1, -1, -1):
#         risultato.append(lista[i])
#     return risultato
#
# print(inverti_lista([1, 2, 3, 4, 5]))  # [5, 4, 3, 2, 1]
# print(inverti_lista(["a", "b", "c"]))  # ["c", "b", "a"]
# print(inverti_lista([]))                # []

# --- SOLUZIONE ESERCIZIO 7 (Elemento più frequente) ---
# def piu_frequente(lista):
#     """Restituisce l'elemento che appare più volte nella lista."""
#     return max(lista, key=lambda x: lista.count(x))
#
# # Spiegazione: max() prende l'elemento "più grande". Ma più grande in base
# # a cosa? La lambda dice: "confronta in base a quante volte appare nella
# # lista". Quindi max restituisce quello che appare più volte.
# # È come usare .sort((a,b) => ...) in JS ma per trovare il massimo.
#
# print(piu_frequente([1, 3, 2, 1, 4, 1, 3]))   # 1
# print(piu_frequente(["mela", "pera", "mela"]))  # "mela"

# --- SOLUZIONE ESERCIZIO 8 (Appiattisci) ---
# # Metodo 1: ciclo for
# def appiattisci(lista_di_liste):
#     """Appiattisce una lista di liste in una singola lista."""
#     risultato = []
#     for sotto_lista in lista_di_liste:
#         for elemento in sotto_lista:
#             risultato.append(elemento)
#     return risultato
#
# # Metodo 2: list comprehension
# def appiattisci_v2(lista_di_liste):
#     """Appiattisce con list comprehension."""
#     return [elem for sotto in lista_di_liste for elem in sotto]
#
# print(appiattisci([[1,2], [3,4], [5]]))       # [1, 2, 3, 4, 5]
# print(appiattisci_v2([["a","b"], ["c"]]))      # ["a", "b", "c"]

# --- SOLUZIONE ESERCIZIO 9 (Preview AI — Train/Test Split) ---
# dati = list(range(1, 21))
# training = dati[:16]
# test = dati[16:]
# print(f"Training (80%): {training}")
# print(f"Test (20%): {test}")
#
# batch_size = 4
# for i, start in enumerate(range(0, len(training), batch_size)):
#     batch = training[start:start + batch_size]
#     print(f"Batch {i + 1}: {batch}")
