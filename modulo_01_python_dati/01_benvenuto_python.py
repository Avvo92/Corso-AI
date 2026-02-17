"""
============================================================================
 MODULO 1 — ESERCIZIO 01: Benvenuto in Python!
 Variabili, Tipi di Dato, Print e F-String
============================================================================

 TEORIA: Python vs JavaScript — Le Differenze che Contano

 Se conosci JavaScript, Python ti sembrerà una versione "più pulita" dello
 stesso linguaggio. Ecco le differenze principali da tenere a mente:

 1. NIENTE PUNTO E VIRGOLA
    JavaScript:  let nome = "Luca";
    Python:      nome = "Luca"

 2. NIENTE VAR/LET/CONST
    JavaScript:  let eta = 30;     const PI = 3.14;
    Python:      eta = 30          PI = 3.14
    In Python non dichiari il "tipo" di variabile. Python lo capisce da solo.
    (Si chiama "tipizzazione dinamica" — JS ce l'ha uguale, ma in Python
    non serve neanche la keyword let/const)

 3. NIENTE GRAFFE {} PER I BLOCCHI
    JavaScript:  if (eta > 18) { console.log("Maggiorenne"); }
    Python:      if eta > 18:
                     print("Maggiorenne")
    In Python usi i DUE PUNTI (:) e l'INDENTAZIONE (gli spazi) al posto
    delle graffe. L'indentazione NON è opzionale come in JS: è la sintassi.

 4. PRINT AL POSTO DI CONSOLE.LOG
    JavaScript:  console.log("Ciao");
    Python:      print("Ciao")

 5. F-STRING AL POSTO DEI TEMPLATE LITERAL
    JavaScript:  console.log(`Ciao ${nome}, hai ${eta} anni`);
    Python:      print(f"Ciao {nome}, hai {eta} anni")
    Nota la 'f' prima delle virgolette: sta per "formatted string".

============================================================================
"""

# ==========================================================================
# PARTE 1: Variabili — Creare e Assegnare Valori
# ==========================================================================

# In JavaScript scriveresti:
#   let nome = "Marco";
#   let eta = 28;
#   let altezza = 1.78;
#   let isStudente = true;
#
# In Python scrivi (senza let, senza punto e virgola):

nome = "Marco"
eta = 28
altezza = 1.78
is_studente = True  # Nota: True con la T maiuscola (in JS è 'true' minuscolo)

# Stampiamo a schermo (come console.log in JavaScript):
print("=== Le mie prime variabili Python ===")
print(nome)
print(eta)
print(altezza)
print(is_studente)

# ==========================================================================
# PARTE 2: Tipi di Dato — Python li Riconosce da Solo
# ==========================================================================

# In JavaScript puoi fare typeof(variabile). In Python usi type(variabile).
# Vediamo i tipi principali:

stringa = "Ciao mondo"        # str (string)    — stessa cosa di JS
intero = 42                    # int (integer)   — in JS è solo "number"
decimale = 3.14                # float           — in JS è solo "number"
booleano = True                # bool            — True/False (maiuscolo!)
niente = None                  # NoneType        — in JS è "null"

print("\n=== Tipi di dato ===")
print(f"'{stringa}' è di tipo: {type(stringa)}")
print(f"'{intero}' è di tipo: {type(intero)}")
print(f"'{decimale}' è di tipo: {type(decimale)}")
print(f"'{booleano}' è di tipo: {type(booleano)}")
print(f"'{niente}' è di tipo: {type(niente)}")

# DIFFERENZA IMPORTANTE: Python distingue int e float.
# In JavaScript, 42 e 42.0 sono entrambi "number".
# In Python, 42 è un int e 42.0 è un float. Sembrano uguali ma non lo sono:
print(f"\n42 == 42.0? {42 == 42.0}")          # True — il valore è uguale
print(f"type(42) == type(42.0)? {type(42) == type(42.0)}")  # False — il tipo no!

# ==========================================================================
# PARTE 3: F-String — Il Template Literal di Python
# ==========================================================================

# In JavaScript usi i backtick e ${}: `Ciao ${nome}`
# In Python usi la f davanti alle virgolette e {}: f"Ciao {nome}"

nome_prodotto = "Tastiera Meccanica"
prezzo = 89.99
quantita = 3

# Stringa semplice con variabili:
print(f"\nProdotto: {nome_prodotto}")
print(f"Prezzo: {prezzo}€")
print(f"Quantità: {quantita}")

# Puoi fare CALCOLI dentro le graffe (come in JS):
totale = prezzo * quantita
print(f"Totale: {prezzo} x {quantita} = {totale}€")

# Puoi anche formattare i numeri (questo in JS richiede toFixed()):
# :.2f significa "mostra 2 cifre decimali" (f = float)
print(f"Totale formattato: {totale:.2f}€")

# Allineare testo (utile quando stampi tabelle):
# :>20 = allinea a destra in 20 caratteri
# :<20 = allinea a sinistra in 20 caratteri
print(f"\n{'Prodotto':<20} {'Prezzo':>10}")
print(f"{'-'*20} {'-'*10}")
print(f"{'Tastiera':<20} {'89.99€':>10}")
print(f"{'Mouse':<20} {'29.99€':>10}")

# ==========================================================================
# PARTE 4: Conversione di Tipo (Casting)
# ==========================================================================

# A volte devi convertire un tipo in un altro. In JavaScript:
#   Number("42")  →  42
#   String(42)    →  "42"
#
# In Python:
#   int("42")     →  42
#   str(42)       →  "42"
#   float("3.14") →  3.14

eta_stringa = "25"
print(f"\n=== Conversione di tipo ===")
print(f"eta_stringa è: '{eta_stringa}' (tipo: {type(eta_stringa).__name__})")

eta_numero = int(eta_stringa)
print(f"eta_numero è: {eta_numero} (tipo: {type(eta_numero).__name__})")

# Attenzione: se provi a convertire qualcosa di non valido, Python dà errore:
# int("ciao")  → ValueError! (come NaN in JS, ma Python è più severo)

# ==========================================================================
# PARTE 5: Input dall'Utente
# ==========================================================================

# In JavaScript nel browser usi prompt(). In Python usi input().
# input() restituisce SEMPRE una stringa (come prompt() in JS).

# Decommenta queste righe per provarle (togliendo il #):
# nome_utente = input("Come ti chiami? ")
# eta_utente = input("Quanti anni hai? ")
# print(f"Ciao {nome_utente}! Tra 10 anni avrai {int(eta_utente) + 10} anni.")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Crea tre variabili: il tuo nome, la tua città e il tuo linguaggio
# di programmazione preferito. Poi stampale con un'unica f-string.
# Esempio output: "Mi chiamo Luca, vivo a Roma e programmo in JavaScript"
#
# Scrivi il tuo codice qui sotto:
my_name = "Gianluca"
my_city = "Roma"
my_language = "Python"

print(f"\nMi chiamo {my_name}, vengo da {my_city}, e il mio linguaggio di programmazione preferito è {my_language}")






# ESERCIZIO 2 (Medio):
# Crea un "calcolatore di sconto". Definisci due variabili:
#   - prezzo_originale = 150.00
#   - percentuale_sconto = 20
# Calcola il prezzo scontato e stampa il risultato formattato con 2 decimali.
# Esempio output: "Prezzo originale: 150.00€ | Sconto: 20% | Prezzo finale: 120.00€"
#
# Scrivi il tuo codice qui sotto:
prezzo_originale = 150.00
percentuale_sconto = 20
print(f"\nPrezzo originale: {prezzo_originale:.2f} € | Sconto: {percentuale_sconto}% | Prezzo finale: {(prezzo_originale - ((prezzo_originale * percentuale_sconto) /100)):.2f} €")


# ESERCIZIO 3 (Sfida):
# Crea un convertitore di temperatura. Definisci una variabile:
#   - celsius = 36.6
# Convertila in Fahrenheit con la formula: F = (C × 9/5) + 32
# Poi convertila in Kelvin con la formula: K = C + 273.15
# Stampa tutte e tre le temperature formattate con 1 decimale.
# Esempio output: "36.6°C = 97.9°F = 309.8K"
#
# Scrivi il tuo codice qui sotto:
celsius = 36.6
fahrenheit = (celsius * 9/5) +32
kelvin = celsius + 273.15
print(f"\nCelsius: {celsius:.1f}°C | Fahrenheit: {fahrenheit:.1f}°F | Kelvin: {kelvin:.1f}°K ")


# ESERCIZIO 4 (Web Bridge Mentale):
# Immagina di ricevere questi dati da un form HTML (arrivano come stringhe):
#   larghezza_str = "800"
#   altezza_str = "600"
# Convertili in numeri, calcola l'area e il perimetro, e stampa i risultati.
# Poi crea una variabile 'is_landscape' che sia True se larghezza > altezza.
#
# Scrivi il tuo codice qui sotto:
larghezza_str = "800"
altezza_str = "600"
perimeter = (int(larghezza_str) * 2) + (int(altezza_str)*2)
area = int(larghezza_str) * int(altezza_str)
is_landscape = int(larghezza_str) > int(altezza_str) 
print(f"\nPerimetro: {perimeter} m | Area: {area} mq")
print(f"{bool(is_landscape)}")


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# nome = "Luca"
# citta = "Roma"
# linguaggio = "JavaScript"
# print(f"Mi chiamo {nome}, vivo a {citta} e programmo in {linguaggio}")

# --- SOLUZIONE ESERCIZIO 2 ---
# prezzo_originale = 150.00
# percentuale_sconto = 20
# importo_sconto = prezzo_originale * percentuale_sconto / 100
# prezzo_finale = prezzo_originale - importo_sconto
# print(f"Prezzo originale: {prezzo_originale:.2f}€ | Sconto: {percentuale_sconto}% | Prezzo finale: {prezzo_finale:.2f}€")

# --- SOLUZIONE ESERCIZIO 3 ---
# celsius = 36.6
# fahrenheit = (celsius * 9/5) + 32
# kelvin = celsius + 273.15
# print(f"{celsius:.1f}°C = {fahrenheit:.1f}°F = {kelvin:.1f}K")

# --- SOLUZIONE ESERCIZIO 4 ---
# larghezza_str = "800"
# altezza_str = "600"
# larghezza = int(larghezza_str)
# altezza = int(altezza_str)
# area = larghezza * altezza
# perimetro = 2 * (larghezza + altezza)
# is_landscape = larghezza > altezza
# print(f"Dimensioni: {larghezza}x{altezza}")
# print(f"Area: {area} pixel²")
# print(f"Perimetro: {perimetro} pixel")
# print(f"È landscape? {is_landscape}")
