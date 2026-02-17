"""
============================================================================
 MODULO 1 — ESERCIZIO 03: Le Funzioni
 def vs function, Parametri, Return Multipli
============================================================================

 TEORIA: Le Funzioni in Python — Il Tuo "Controller" Personale

 Se lavori con Laravel, conosci i Controller: ricevono una richiesta,
 elaborano dati, restituiscono una risposta. Le funzioni Python sono
 esattamente questo, ma senza il framework attorno.

 La sintassi cambia così:

   JavaScript:
     function saluta(nome) {
         return `Ciao ${nome}!`;
     }

     const saluta = (nome) => `Ciao ${nome}!`;  // arrow function

   Python:
     def saluta(nome):
         return f"Ciao {nome}!"

 Nota:
   - 'def' al posto di 'function'
   - Due punti (:) al posto della graffa {
   - Indentazione al posto del corpo tra graffe
   - Non esiste la arrow function (=>) in Python

============================================================================
"""

# ==========================================================================
# PARTE 1: Definire e Chiamare una Funzione
# ==========================================================================

# Funzione semplice senza parametri:
def saluta():
    print("Ciao! Benvenuto nel Modulo 1!")

saluta()  # Chiamata — identica a JavaScript

# Funzione con parametri:
def saluta_persona(nome):
    print(f"Ciao {nome}! Come stai?")

saluta_persona("Marco")
saluta_persona("Laura")

# Funzione con return:
def calcola_iva(prezzo, aliquota=22):
    """
    Calcola il prezzo con IVA inclusa.
    'aliquota=22' è un PARAMETRO DEFAULT: se non lo passi, vale 22.
    In JavaScript sarebbe: function calcolaIva(prezzo, aliquota = 22) { ... }
    """
    iva = prezzo * aliquota / 100
    totale = prezzo + iva
    return totale

# Usiamo la funzione:
print("\n=== Calcolo IVA ===")
print(f"100€ + IVA 22% = {calcola_iva(100)}€")
print(f"100€ + IVA 10% = {calcola_iva(100, 10)}€")  # Override del default

# ==========================================================================
# PARTE 2: Return Multipli — Un Superpotere di Python!
# ==========================================================================

# In JavaScript, se vuoi restituire più valori, devi usare un oggetto o array:
#   function analizza(testo) {
#       return { lunghezza: testo.length, parole: testo.split(" ").length };
#   }
#
# In Python puoi restituire più valori direttamente (sotto il cofano,
# Python li mette in una "tupla" — per ora pensa a un array immutabile):

def analizza_testo(testo):
    """Analizza un testo e restituisce più informazioni."""
    lunghezza = len(testo)
    num_parole = len(testo.split())  # split() divide per spazi, come .split(" ") in JS
    num_vocali = sum(1 for c in testo.lower() if c in "aeiou")
    return lunghezza, num_parole, num_vocali

# Posso "spacchettare" i risultati in variabili separate:
caratteri, parole, vocali = analizza_testo("Ciao mondo, sto imparando Python!")

print("\n=== Return Multipli ===")
print(f"Caratteri: {caratteri}")
print(f"Parole: {parole}")
print(f"Vocali: {vocali}")

# ==========================================================================
# PARTE 3: Parametri con Nome (Keyword Arguments)
# ==========================================================================

# In JavaScript, quando hai molti parametri, usi un oggetto:
#   function creaUtente({ nome, eta, citta = "Roma" }) { ... }
#
# In Python, puoi semplicemente chiamare i parametri per nome:

def crea_profilo(nome, eta, citta="Roma", ruolo="developer"):
    """Crea un profilo utente."""
    return f"{nome}, {eta} anni, {citta} — {ruolo}"

print("\n=== Parametri con nome ===")
# Chiamata posizionale (l'ordine conta):
print(crea_profilo("Marco", 28))

# Chiamata con keyword (l'ordine NON conta):
print(crea_profilo(eta=30, nome="Laura", ruolo="designer"))

# Mix (prima posizionali, poi keyword):
print(crea_profilo("Giulia", 25, ruolo="AI engineer"))

# ==========================================================================
# PARTE 4: *args e **kwargs — I Parametri "Liberi"
# ==========================================================================

# A volte non sai quanti parametri riceverai. Come quando fai:
#   function somma(...numeri) { return numeri.reduce((a,b) => a+b, 0); }
#
# In Python:

# *args = cattura tutti i parametri posizionali in una tupla
def somma(*numeri):
    """Somma qualsiasi quantità di numeri."""
    totale = 0
    for n in numeri:
        totale += n
    return totale

print("\n=== *args (parametri variabili) ===")
print(f"somma(1, 2): {somma(1, 2)}")
print(f"somma(1, 2, 3, 4, 5): {somma(1, 2, 3, 4, 5)}")
print(f"somma(10, 20, 30): {somma(10, 20, 30)}")

# **kwargs = cattura i parametri con nome in un dizionario
def stampa_info(**info):
    """Stampa qualsiasi informazione passata come keyword."""
    for chiave, valore in info.items():
        print(f"  {chiave}: {valore}")

print("\n=== **kwargs (keyword variabili) ===")
stampa_info(nome="Marco", eta=28, linguaggio="Python")
print("---")
stampa_info(progetto="Corso AI", modulo=1, stato="in corso")

# ==========================================================================
# PARTE 5: Le Funzioni Lambda — Le Arrow Function di Python
# ==========================================================================

# In JavaScript: const doppio = (x) => x * 2;
# In Python:     doppio = lambda x: x * 2
#
# Le lambda sono funzioni "usa e getta" di una sola riga.
# Non le userai spesso da sole, ma sono utilissime con sorted(), map(), filter().

doppio = lambda x: x * 2
print(f"\n=== Lambda ===")
print(f"doppio(5) = {doppio(5)}")

# Esempio pratico: ordinare una lista di dizionari per un campo specifico
# (come ORDER BY in SQL):
prodotti = [
    {"nome": "Mouse", "prezzo": 29.99},
    {"nome": "Tastiera", "prezzo": 89.99},
    {"nome": "Cuffie", "prezzo": 49.99},
]

# Ordina per prezzo (crescente):
prodotti_ordinati = sorted(prodotti, key=lambda p: p["prezzo"])
print("\nProdotti ordinati per prezzo:")
for p in prodotti_ordinati:
    print(f"  {p['nome']}: {p['prezzo']}€")

# ==========================================================================
# PARTE 6: Docstring — Documentare le Funzioni
# ==========================================================================

# In Python si usa una stringa con triple virgolette subito dopo 'def':
# Si chiama "docstring" e serve a documentare cosa fa la funzione.
# È come i commenti JSDoc in JavaScript.

def calcola_sconto(prezzo, percentuale):
    """
    Calcola il prezzo scontato di un prodotto.

    Parametri:
        prezzo (float): il prezzo originale del prodotto
        percentuale (float): la percentuale di sconto (es. 20 per il 20%)

    Restituisce:
        float: il prezzo finale dopo lo sconto
    """
    sconto = prezzo * percentuale / 100
    return prezzo - sconto

# Puoi leggere la docstring con help():
# help(calcola_sconto)   # Decommentala per provare!


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Crea una funzione 'converti_celsius_fahrenheit(celsius)' che:
#   - Riceve una temperatura in Celsius
#   - Restituisce la temperatura in Fahrenheit (F = C * 9/5 + 32)
#   - Ha una docstring che spiega cosa fa
# Testala con i valori: 0, 100, 36.6
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio):
# Crea una funzione 'analizza_lista_prezzi(*prezzi)' che riceve un numero
# qualsiasi di prezzi e restituisce (return multiplo):
#   - Il prezzo minimo
#   - Il prezzo massimo
#   - La media dei prezzi
# Suggerimento: min(), max() e sum() sono funzioni built-in di Python.
# Testala con: analizza_lista_prezzi(29.99, 49.99, 89.99, 149.99, 19.99)
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio):
# Crea una funzione 'formatta_valuta(importo, valuta="EUR", decimali=2)'
# che formatta un importo come stringa:
#   formatta_valuta(1234.5)              → "1234.50 EUR"
#   formatta_valuta(1234.5, "USD")       → "1234.50 USD"
#   formatta_valuta(1234.5678, "GBP", 3) → "1234.568 GBP"
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida):
# Crea una funzione 'crea_risposta_api(dati, successo=True, messaggio="OK")'
# che simula la costruzione di una risposta API JSON-like.
# Deve restituire un dizionario (vedremo i dizionari in dettaglio nel file 05,
# ma per ora: un dizionario è come un oggetto JS):
#   {
#       "success": True,
#       "message": "OK",
#       "data": dati,
#       "count": len(dati) se dati è una lista, altrimenti 1
#   }
# Suggerimento: isinstance(dati, list) controlla se dati è una lista.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Lambda):
# Data questa lista di studenti:
#   studenti = [
#       {"nome": "Anna", "voto": 85},
#       {"nome": "Marco", "voto": 92},
#       {"nome": "Giulia", "voto": 78},
#       {"nome": "Luca", "voto": 95},
#   ]
# Usa sorted() con una lambda per ordinarli per voto decrescente.
# Poi stampa la "classifica".
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# def converti_celsius_fahrenheit(celsius):
#     """Converte una temperatura da Celsius a Fahrenheit."""
#     return celsius * 9/5 + 32
#
# print(f"0°C = {converti_celsius_fahrenheit(0)}°F")
# print(f"100°C = {converti_celsius_fahrenheit(100)}°F")
# print(f"36.6°C = {converti_celsius_fahrenheit(36.6)}°F")

# --- SOLUZIONE ESERCIZIO 2 ---
# def analizza_lista_prezzi(*prezzi):
#     """Analizza una lista di prezzi e restituisce min, max, media."""
#     prezzo_min = min(prezzi)
#     prezzo_max = max(prezzi)
#     media = sum(prezzi) / len(prezzi)
#     return prezzo_min, prezzo_max, media
#
# minimo, massimo, media = analizza_lista_prezzi(29.99, 49.99, 89.99, 149.99, 19.99)
# print(f"Minimo: {minimo:.2f}€ | Massimo: {massimo:.2f}€ | Media: {media:.2f}€")

# --- SOLUZIONE ESERCIZIO 3 ---
# def formatta_valuta(importo, valuta="EUR", decimali=2):
#     """Formatta un importo con valuta e numero di decimali."""
#     return f"{importo:.{decimali}f} {valuta}"
#
# print(formatta_valuta(1234.5))
# print(formatta_valuta(1234.5, "USD"))
# print(formatta_valuta(1234.5678, "GBP", 3))

# --- SOLUZIONE ESERCIZIO 4 ---
# def crea_risposta_api(dati, successo=True, messaggio="OK"):
#     """Simula una risposta API in formato dizionario."""
#     conteggio = len(dati) if isinstance(dati, list) else 1
#     return {
#         "success": successo,
#         "message": messaggio,
#         "data": dati,
#         "count": conteggio
#     }
#
# risposta = crea_risposta_api(["prodotto1", "prodotto2", "prodotto3"])
# print(risposta)
# risposta_errore = crea_risposta_api(None, successo=False, messaggio="Non trovato")
# print(risposta_errore)

# --- SOLUZIONE ESERCIZIO 5 ---
# studenti = [
#     {"nome": "Anna", "voto": 85},
#     {"nome": "Marco", "voto": 92},
#     {"nome": "Giulia", "voto": 78},
#     {"nome": "Luca", "voto": 95},
# ]
# classifica = sorted(studenti, key=lambda s: s["voto"], reverse=True)
# print("\n=== Classifica ===")
# for posizione, studente in enumerate(classifica, 1):
#     print(f"{posizione}° — {studente['nome']}: {studente['voto']}/100")
