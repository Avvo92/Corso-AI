"""
============================================================================
 MODULO 1 — ESERCIZIO 04: Le Liste
 Liste, Slicing, List Comprehension
============================================================================

 TEORIA: Le Liste Python = Gli Array JavaScript

 Se conosci gli Array JavaScript, le Liste Python sono lo stesso concetto
 con qualche superpotere in più.

 Confronto rapido:

   JavaScript:                    Python:
   let frutti = ["mela","pera"];  frutti = ["mela", "pera"]
   frutti.push("banana");         frutti.append("banana")
   frutti.length;                 len(frutti)
   frutti[0];                     frutti[0]
   frutti.splice(1, 1);           frutti.pop(1)
   frutti.includes("mela");       "mela" in frutti

 IL SUPERPOTERE: lo Slicing
 In JavaScript, per prendere una porzione di array usi .slice(start, end).
 In Python puoi farlo direttamente con le parentesi quadre:
   lista[inizio:fine]           → come .slice(inizio, fine)
   lista[inizio:fine:passo]     → non esiste in JS! Puoi saltare elementi.

 Perché ti serve per l'AI?
 Quando lavorerai con dataset e immagini, lo slicing ti servirà OGNI GIORNO:
   - Prendere le prime 100 righe di un dataset
   - Selezionare un pezzo di un'immagine
   - Dividere i dati in training e test

============================================================================
"""

# ==========================================================================
# PARTE 1: Creare e Manipolare Liste
# ==========================================================================

# Creare una lista (come un array JS):
frutti = ["mela", "banana", "arancia", "kiwi", "pera"]
print(f"Lista frutti: {frutti}")
print(f"Numero di elementi: {len(frutti)}")   # len() = .length in JS

# Accedere agli elementi:
print(f"\nPrimo elemento: {frutti[0]}")        # Come JS
print(f"Ultimo elemento: {frutti[-1]}")         # NOVITÀ! -1 = ultimo elemento
print(f"Penultimo: {frutti[-2]}")               # -2 = penultimo, ecc.

# In JavaScript per l'ultimo elemento devi fare: frutti[frutti.length - 1]
# In Python basta: frutti[-1]   ← Molto più comodo!

# Aggiungere elementi:
frutti.append("mango")            # Come .push() in JS — aggiunge in fondo
frutti.insert(1, "fragola")       # Inserisce alla posizione 1 (come splice)
print(f"\nDopo append e insert: {frutti}")

# Rimuovere elementi:
frutti.remove("banana")           # Rimuove per VALORE (non esiste in JS)
ultimo = frutti.pop()             # Rimuove e restituisce l'ultimo (come JS)
secondo = frutti.pop(1)           # Rimuove e restituisce alla posizione 1
print(f"Rimossi: {ultimo}, {secondo}")
print(f"Lista attuale: {frutti}")

# Controllare se un elemento esiste:
# JavaScript:  frutti.includes("mela")
# Python:      "mela" in frutti

print(f"\n'mela' è nella lista? {'mela' in frutti}")
print(f"'banana' è nella lista? {'banana' in frutti}")

# ==========================================================================
# PARTE 2: Lo Slicing — Il Superpotere
# ==========================================================================

numeri = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"\nLista originale: {numeri}")

# Sintassi: lista[inizio:fine]
# ATTENZIONE: 'fine' è ESCLUSO (come .slice() in JS)

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
voti_ordinati = sorted(voti)           # Crea una NUOVA lista ordinata
print(f"Ordinati (crescente): {voti_ordinati}")

voti_decrescenti = sorted(voti, reverse=True)
print(f"Ordinati (decrescente): {voti_decrescenti}")

# .sort() modifica la lista ORIGINALE (attenzione!):
# voti.sort()  ← Questo MODIFICA voti, non crea una copia!

# Trovare la posizione di un elemento:
posizione = voti.index(95)  # Come .indexOf() in JS
print(f"Il voto 95 è alla posizione: {posizione}")

# Contare le occorrenze:
numeri_ripetuti = [1, 2, 3, 2, 1, 2, 4, 2]
print(f"\nIl 2 appare {numeri_ripetuti.count(2)} volte")

# ==========================================================================
# PARTE 4: List Comprehension — Il .map() e .filter() di Python
# ==========================================================================

# In JavaScript per trasformare un array usi:
#   const doppi = numeri.map(n => n * 2);
#   const pari = numeri.filter(n => n % 2 === 0);
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
print("\n=== Pagella ===")
for riga in tabella_voti:
    nome = riga[0]
    voti = riga[1:]  # tutti gli elementi tranne il primo (slicing!)
    media = sum(voti) / len(voti)
    print(f"{nome}: voti {voti}, media {media:.1f}")


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


# ESERCIZIO 3 (Medio):
# Scrivi una funzione 'rimuovi_duplicati(lista)' che prende una lista e
# restituisce una nuova lista SENZA elementi duplicati, mantenendo l'ordine.
# Es: rimuovi_duplicati([3, 1, 2, 3, 1, 4]) → [3, 1, 2, 4]
# Suggerimento: usa una lista di appoggio e 'if elemento not in ...'
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida):
# Crea una funzione 'appiattisci(lista_di_liste)' che prende una lista
# di liste e restituisce una singola lista con tutti gli elementi.
# Es: appiattisci([[1,2], [3,4], [5]]) → [1, 2, 3, 4, 5]
# Prova a farlo sia con un ciclo normale, sia con una list comprehension.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Preview AI):
# Simula la divisione di un dataset in training e test.
# Hai questa lista di 20 numeri:
#   dati = list(range(1, 21))  # [1, 2, 3, ..., 20]
# a) Dividi in 80% training (primi 16) e 20% test (ultimi 4) usando slicing
# b) Dividi il training in "batch" (gruppi) da 4 elementi ciascuno
#    Suggerimento: usa slicing con range → training[i:i+4] per ogni batch
# c) Stampa ogni batch numerato: "Batch 1: [1, 2, 3, 4]", ecc.
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

# --- SOLUZIONE ESERCIZIO 3 ---
# def rimuovi_duplicati(lista):
#     """Rimuove duplicati mantenendo l'ordine originale."""
#     risultato = []
#     for elemento in lista:
#         if elemento not in risultato:
#             risultato.append(elemento)
#     return risultato
#
# print(rimuovi_duplicati([3, 1, 2, 3, 1, 4]))

# --- SOLUZIONE ESERCIZIO 4 ---
# def appiattisci(lista_di_liste):
#     """Appiattisce una lista di liste in una singola lista."""
#     # Metodo 1: ciclo for
#     risultato = []
#     for sotto_lista in lista_di_liste:
#         for elemento in sotto_lista:
#             risultato.append(elemento)
#     return risultato
#
# # Metodo 2: list comprehension
# # def appiattisci(lista_di_liste):
# #     return [elem for sotto in lista_di_liste for elem in sotto]
#
# print(appiattisci([[1,2], [3,4], [5]]))

# --- SOLUZIONE ESERCIZIO 5 ---
# dati = list(range(1, 21))
# training = dati[:16]
# test = dati[16:]
# print(f"Training (80%): {training}")
# print(f"Test (20%): {test}")
#
# batch_size = 4
# for i in range(0, len(training), batch_size):
#     batch = training[i:i+batch_size]
#     batch_num = i // batch_size + 1
#     print(f"Batch {batch_num}: {batch}")
