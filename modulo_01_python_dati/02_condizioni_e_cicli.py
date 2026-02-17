"""
============================================================================
 MODULO 1 — ESERCIZIO 02: Condizioni e Cicli
 if/else, for, while — La Traduzione da JavaScript
============================================================================

 TEORIA: L'Indentazione è il Nuovo Paio di Graffe

 In JavaScript i blocchi di codice sono delimitati dalle graffe {}:
     if (condizione) {
         // codice
     }

 In Python, le graffe NON ESISTONO. Al loro posto usi:
   1. I DUE PUNTI (:) alla fine della riga che apre il blocco
   2. L'INDENTAZIONE (4 spazi) per tutto il codice dentro il blocco

 Pensa all'indentazione come al layout di un sito web:
   - In HTML usi i tag per strutturare: <div>contenuto</div>
   - In Python usi gli spazi per strutturare: tutto ciò che è indentato
     "appartiene" al blocco sopra di esso.

 ATTENZIONE: Mischiare tab e spazi è un errore in Python!
 Usa sempre 4 spazi (Cursor lo fa automaticamente quando premi Tab).

============================================================================
"""

# ==========================================================================
# PARTE 1: if / elif / else — Le Condizioni
# ==========================================================================

# In JavaScript:
#   if (eta >= 18) {
#       console.log("Maggiorenne");
#   } else if (eta >= 14) {
#       console.log("Adolescente");
#   } else {
#       console.log("Bambino");
#   }
#
# In Python (nota: elif, non "else if"):

eta = 16

if eta >= 18:
    print("Maggiorenne")
elif eta >= 14:
    print("Adolescente")
else:
    print("Bambino")

# OPERATORI DI CONFRONTO — Identici a JavaScript:
#   ==  uguale a         (come === in JS, ma in Python == basta)
#   !=  diverso da
#   >   maggiore di
#   <   minore di
#   >=  maggiore o uguale
#   <=  minore o uguale

# OPERATORI LOGICI — Parole al posto dei simboli:
#   JavaScript:  &&    ||    !
#   Python:      and   or    not

temperatura = 25
piove = False

if temperatura > 20 and not piove:
    print("Bel tempo! Esci senza giacca.")
elif temperatura > 20 and piove:
    print("Caldo ma piove. Prendi l'ombrello.")
else:
    print("Fa freddo. Prendi la giacca.")

# OPERATORE TERNARIO:
# JavaScript:  let stato = eta >= 18 ? "adulto" : "minore";
# Python:      stato = "adulto" if eta >= 18 else "minore"

stato = "adulto" if eta >= 18 else "minore"
print(f"\nEtà {eta}: {stato}")

# CONFRONTO CON None (il null di JavaScript):
# JavaScript:  if (valore === null) { ... }
# Python:      if valore is None:    (usa 'is', non '==')

valore = None
if valore is None:
    print("Il valore è None (come null in JavaScript)")

# ==========================================================================
# PARTE 2: Il Ciclo for — Molto Più Elegante di JavaScript
# ==========================================================================

# In JavaScript (il for classico):
#   for (let i = 0; i < 5; i++) {
#       console.log(i);
#   }
#
# In Python — usi range() che genera una sequenza di numeri:

print("\n=== Ciclo for con range ===")
for i in range(5):     # range(5) genera: 0, 1, 2, 3, 4
    print(f"Iterazione: {i}")

# range() funziona come uno slice:
#   range(5)        → 0, 1, 2, 3, 4       (da 0 a 4)
#   range(2, 7)     → 2, 3, 4, 5, 6       (da 2 a 6)
#   range(0, 10, 2) → 0, 2, 4, 6, 8       (da 0 a 9, saltando di 2)

print("\n=== Numeri pari da 0 a 10 ===")
for numero in range(0, 11, 2):
    print(numero, end=" ")  # end=" " stampa sulla stessa riga
print()  # va a capo

# ITERARE SU UNA LISTA (come forEach in JavaScript):
# JavaScript:  ["Milano", "Roma", "Napoli"].forEach(c => console.log(c));
# Python:

citta = ["Milano", "Roma", "Napoli", "Torino", "Firenze"]
print("\n=== Iterare su una lista ===")
for c in citta:
    print(f"Città: {c}")

# ITERARE CON L'INDICE (come for...of con entries() in JavaScript):
# JavaScript:  for (const [i, c] of citta.entries()) { ... }
# Python:      for i, c in enumerate(citta):

print("\n=== Iterare con indice (enumerate) ===")
for indice, nome_citta in enumerate(citta):
    print(f"{indice}: {nome_citta}")

# ITERARE SU UNA STRINGA (carattere per carattere):
print("\n=== Iterare su una stringa ===")
for lettera in "Python":
    print(lettera, end="-")
print()

# ==========================================================================
# PARTE 3: Il Ciclo while
# ==========================================================================

# Identico al concetto JavaScript, cambia solo la sintassi:
# JavaScript:  while (contatore < 5) { contatore++; }
# Python:

print("\n=== Ciclo while ===")
contatore = 0
while contatore < 5:
    print(f"Contatore: {contatore}")
    contatore += 1   # In Python non esiste ++ (contatore++ non funziona!)

# BREAK e CONTINUE funzionano come in JavaScript:
print("\n=== Break e Continue ===")
for numero in range(10):
    if numero == 3:
        continue  # Salta il 3
    if numero == 7:
        break     # Ferma tutto al 7
    print(numero, end=" ")
print()

# ==========================================================================
# PARTE 4: Cicli Annidati (Nested Loops)
# ==========================================================================

# Come in JavaScript, puoi mettere un ciclo dentro un altro.
# Esempio pratico: stampare una "griglia" (come una tabella HTML)

print("\n=== Griglia 3x3 (come una tabella HTML) ===")
for riga in range(3):
    for colonna in range(3):
        cella = f"[{riga},{colonna}]"
        print(cella, end=" ")
    print()  # va a capo alla fine della riga

# Esempio più utile: tabellina del 5
print("\n=== Tabellina del 5 ===")
for i in range(1, 11):
    print(f"5 x {i:2d} = {5 * i:2d}")
    # :2d = mostra il numero intero (d=digit) con almeno 2 caratteri


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Crea una variabile 'voto' con un numero da 0 a 100.
# Stampa il giudizio usando if/elif/else:
#   >= 90: "Eccellente"
#   >= 70: "Buono"
#   >= 60: "Sufficiente"
#   < 60:  "Insufficiente"
#
# Scrivi il tuo codice qui sotto:
voto = 60
if voto >= 90:
    print("\nEccellente")
elif voto >= 70:
    print("\nBuono")
elif voto >= 60:
    print("\nSufficiente")
else:
    print("\nInsufficiente")


# ESERCIZIO 2 (Medio):
# Usa un ciclo for per stampare tutti i numeri da 1 a 20.
# Per ogni numero, stampa:
#   - "Fizz"     se è divisibile per 3
#   - "Buzz"     se è divisibile per 5
#   - "FizzBuzz" se è divisibile per entrambi
#   - Il numero  altrimenti
# (Questo è il famoso "FizzBuzz" — classico esercizio da colloquio!)
# Suggerimento: l'operatore "modulo" è %, come in JS. 15 % 3 == 0 → divisibile.
#
# Scrivi il tuo codice qui sotto:
print("\n")
for numero in range(1, 21):
    if (numero % 15) == 0:
        print("fizzbuzz")
    elif numero % 5 == 0:
        print("buzz")
    elif numero % 3 == 0:
        print ("fizz")
    else:
        print(f"{numero}")


# ESERCIZIO 3 (Medio):
# Crea una lista di 5 temperature in Celsius:
#   temperature = [0, 15, 25, 30, 38]
# Usa un ciclo for per convertirle tutte in Fahrenheit (F = C * 9/5 + 32)
# e stampare: "0°C → 32.0°F"
# Alla fine, stampa la temperatura media in Celsius.
#
# Scrivi il tuo codice qui sotto:
print("\n")
temperature = [0, 15, 25, 30, 38]
somma_temperature = 0
for t in temperature:
    print(f"{t:.1f}°C => {t* 9/5 + 32:.1f}°F")
    somma_temperature += t
print(f"La media delle temperature e di {somma_temperature / len(temperature)}°C")
    

    



# ESERCIZIO 4 (Sfida):
# Crea un "validatore di password" senza usare funzioni esterne.
# Data una password (stringa), controlla con un ciclo:
#   - Ha almeno 8 caratteri?
#   - Contiene almeno un numero? (suggerimento: carattere.isdigit())
#   - Contiene almeno una lettera maiuscola? (carattere.isupper())
# Stampa un messaggio per ogni controllo superato o fallito.
#
# password = "MiaPassword123"
# Scrivi il tuo codice qui sotto:
password = "Ciao1234"

contiene_numero = False
contiene_maiuscola = False

if len(password) < 8:
    print ("La password deve avere almeno 8 caratteri")

else:
    for carattere in password:
        if carattere.isdigit() == True :
            contiene_numero = True
        if carattere.isupper() == True:
            contiene_maiuscola = True
        
    if contiene_numero == True and contiene_maiuscola == True:
        print("\nPassword valida")
    else:
        print("\nLa password scelta non va bene")



# ESERCIZIO 5 (Sfida — Griglia):
# Crea una scacchiera 8x8 usando due cicli for annidati.
# Stampa '#' per le caselle nere e '.' per le bianche.
# Suggerimento: una casella è "nera" se (riga + colonna) è pari.
# Output atteso:
# # . # . # . # .
# . # . # . # . #
# # . # . # . # .
# ...
#
# Scrivi il tuo codice qui sotto:
for riga in range(8):
    for colonna in range(8):
        if (riga + colonna) % 2 == 0:
            print("#", end=" ")
        else:
            print(".", end=" ")
    print()
    


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# --- SOLUZIONE ESERCIZIO 1 ---
# voto = 85
# if voto >= 90:
#     print(f"Voto {voto}: Eccellente")
# elif voto >= 70:
#     print(f"Voto {voto}: Buono")
# elif voto >= 60:
#     print(f"Voto {voto}: Sufficiente")
# else:
#     print(f"Voto {voto}: Insufficiente")

# --- SOLUZIONE ESERCIZIO 2 ---
# for n in range(1, 21):
#     if n % 3 == 0 and n % 5 == 0:
#         print("FizzBuzz")
#     elif n % 3 == 0:
#         print("Fizz")
#     elif n % 5 == 0:
#         print("Buzz")
#     else:
#         print(n)

# --- SOLUZIONE ESERCIZIO 3 ---
# temperature = [0, 15, 25, 30, 38]
# somma = 0
# for celsius in temperature:
#     fahrenheit = celsius * 9/5 + 32
#     print(f"{celsius}°C → {fahrenheit:.1f}°F")
#     somma += celsius
# media = somma / len(temperature)
# print(f"\nTemperatura media: {media:.1f}°C")

# --- SOLUZIONE ESERCIZIO 4 ---
# password = "MiaPassword123"
# ha_lunghezza = len(password) >= 8
# ha_numero = False
# ha_maiuscola = False
# for carattere in password:
#     if carattere.isdigit():
#         ha_numero = True
#     if carattere.isupper():
#         ha_maiuscola = True
# print(f"Password: '{password}'")
# print(f"  Almeno 8 caratteri: {'✓' if ha_lunghezza else '✗'}")
# print(f"  Contiene un numero: {'✓' if ha_numero else '✗'}")
# print(f"  Contiene maiuscola: {'✓' if ha_maiuscola else '✗'}")
# if ha_lunghezza and ha_numero and ha_maiuscola:
#     print("  → Password VALIDA!")
# else:
#     print("  → Password NON valida!")

# --- SOLUZIONE ESERCIZIO 5 ---
# for riga in range(8):
#     for colonna in range(8):
#         if (riga + colonna) % 2 == 0:
#             print("#", end=" ")
#         else:
#             print(".", end=" ")
#     print()
