"""
============================================================================
 MODULO 1 — ESERCIZIO 06: Leggere File CSV "A Mano"
 Capire il Dolore Prima di Scoprire Pandas
============================================================================

 TEORIA: Cos'è un File CSV?

 CSV = Comma Separated Values (Valori Separati da Virgola).
 È il formato più semplice per salvare dati tabellari.

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

 La prima riga è l'HEADER (i nomi delle colonne).
 Ogni riga successiva è un RECORD (una riga della tabella).
 I valori sono separati da virgole.

 PERCHÉ LEGGERLO A MANO?
 Nel prossimo esercizio userai Pandas, che legge CSV in una riga.
 Ma prima è utile capire cosa succede "sotto il cofano", così quando
 Pandas farà qualcosa di strano, saprai il perché.

 È come capire le query SQL prima di usare Eloquent in Laravel:
 puoi usare Eloquent senza sapere SQL, ma quando qualcosa non funziona,
 sapere SQL ti salva la vita.

 IN PHP: probabilmente hai usato fgetcsv() per leggere CSV riga per riga,
 oppure librerie come League\Csv. Il concetto è identico a quello che
 faremo qui in Python.

 In PHP:
   $file = fopen('dati.csv', 'r');
   $header = fgetcsv($file);          // legge la prima riga (intestazioni)
   while ($riga = fgetcsv($file)) {   // legge una riga alla volta
       // $riga è un array: ["1001", "2024-01-05", "Cuffie", ...]
   }
   fclose($file);

============================================================================
"""

import os

# Costruiamo il percorso al file CSV in modo che funzioni ovunque
percorso_dati = os.path.join(os.path.dirname(__file__), "dati")
percorso_csv = os.path.join(percorso_dati, "vendite_ecommerce.csv")

# ==========================================================================
# PARTE 1: Leggere un File di Testo
# ==========================================================================

# In PHP:
#   $contenuto = file_get_contents('file.txt');
#   // file_get_contents() legge l'intero file in una stringa.
#   // È la funzione più semplice per leggere un file in PHP.
#   // Alternativa: fopen() + fread() + fclose() per più controllo.
#
# In JavaScript (Node.js):
#   const fs = require('fs');
#   const contenuto = fs.readFileSync('file.txt', 'utf8');
#   // require('fs') importa il modulo "File System" di Node.js
#   // readFileSync() legge il file in modo sincrono (blocca l'esecuzione)
#   // 'utf8' specifica la codifica dei caratteri
#
# In Python:
#   with open('file.txt', 'r') as f:
#       contenuto = f.read()
#
# 'with' è come un "try-finally" automatico: chiude il file quando hai finito.
# È come se facessi fopen() + fclose() automaticamente in PHP.
# 'r' sta per "read" (lettura). Altre modalità: 'w' (write), 'a' (append).
# Stesse modalità di fopen() in PHP: 'r', 'w', 'a', ecc.

print("=== Leggere il file intero come testo ===")
with open(percorso_csv, "r", encoding="utf-8") as file:
    contenuto = file.read()

# Stampiamo le prime 500 caratteri per vedere com'è fatto:
print(contenuto[:500])
print(f"\nCaratteri totali: {len(contenuto)}")

# ==========================================================================
# PARTE 2: Leggere Riga per Riga
# ==========================================================================

print("\n=== Leggere riga per riga ===")
with open(percorso_csv, "r", encoding="utf-8") as file:
    for numero_riga, riga in enumerate(file):
        riga = riga.strip()  # .strip() rimuove gli spazi e \n a inizio/fine
        if numero_riga < 5:  # Stampiamo solo le prime 5 righe
            print(f"Riga {numero_riga}: {riga}")

# ==========================================================================
# PARTE 3: Parsare il CSV "a Mano"
# ==========================================================================

# Ora facciamo il "parsing" — trasformare il testo in dati utilizzabili.
# È come JSON.parse() in JavaScript, ma per CSV dobbiamo farlo noi.

print("\n=== Parsing manuale del CSV ===")
dati = []

with open(percorso_csv, "r", encoding="utf-8") as file:
    righe = file.readlines()  # Legge TUTTE le righe in una lista

    # La prima riga è l'header (i nomi delle colonne)
    header = righe[0].strip().split(",")
    print(f"Colonne: {header}")

    # Le righe successive sono i dati
    for riga in righe[1:]:  # Slicing! Dalla seconda riga in poi
        valori = riga.strip().split(",")

        # Creiamo un dizionario per ogni riga (come un oggetto JSON)
        record = {}
        for i, colonna in enumerate(header):
            record[colonna] = valori[i]

        dati.append(record)

# Ora 'dati' è una lista di dizionari — come il risultato di un'API!
print(f"\nNumero di record: {len(dati)}")
print(f"\nPrimo record:")
for chiave, valore in dati[0].items():
    print(f"  {chiave}: {valore}")

print(f"\nUltimo record:")
for chiave, valore in dati[-1].items():
    print(f"  {chiave}: {valore}")

# ==========================================================================
# PARTE 4: Un Modo Più Elegante — Il Modulo csv di Python
# ==========================================================================

import csv

# Python ha un modulo built-in 'csv' che gestisce casi complessi
# (virgolette nei valori, separatori diversi, ecc.)

print("\n=== Usando il modulo csv ===")
dati_csv = []

with open(percorso_csv, "r", encoding="utf-8") as file:
    lettore = csv.DictReader(file)  # Trasforma ogni riga in un dizionario!

    for record in lettore:
        dati_csv.append(record)

# Risultato identico, ma il codice è molto più pulito:
print(f"Record totali: {len(dati_csv)}")
print(f"Primo record: {dict(dati_csv[0])}")

# ==========================================================================
# PARTE 5: Analizzare i Dati
# ==========================================================================

# Ora che abbiamo i dati come lista di dizionari, possiamo "interrogarli"
# come faremmo con delle query SQL... ma usando Python.

print("\n=== Analisi dei dati ===")

# QUERY 1: Quanti ordini per città? (come GROUP BY citta, COUNT(*))
conteggio_citta = {}
for record in dati_csv:
    citta = record["citta"]
    conteggio_citta[citta] = conteggio_citta.get(citta, 0) + 1

print("Ordini per città:")
for citta, conteggio in sorted(conteggio_citta.items(), key=lambda x: x[1], reverse=True):
    print(f"  {citta}: {conteggio}")

# QUERY 2: Fatturato totale (SUM(prezzo * quantita))
fatturato = 0
for record in dati_csv:
    fatturato += float(record["prezzo"]) * int(record["quantita"])
print(f"\nFatturato totale: {fatturato:.2f}€")

# QUERY 3: Prodotto più venduto (per quantità)
vendite_prodotto = {}
for record in dati_csv:
    prodotto = record["prodotto"]
    vendite_prodotto[prodotto] = vendite_prodotto.get(prodotto, 0) + int(record["quantita"])

prodotto_top = max(vendite_prodotto, key=vendite_prodotto.get)
print(f"Prodotto più venduto: {prodotto_top} ({vendite_prodotto[prodotto_top]} unità)")

# QUERY 4: Fatturato per categoria
fatturato_cat = {}
for record in dati_csv:
    cat = record["categoria"]
    totale = float(record["prezzo"]) * int(record["quantita"])
    fatturato_cat[cat] = fatturato_cat.get(cat, 0) + totale

print("\nFatturato per categoria:")
for cat, tot in sorted(fatturato_cat.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {tot:.2f}€")

# Hai notato quanto codice serve per fare queste "query"?
# Nel prossimo file (09_pandas_intro.py) scoprirai Pandas,
# che fa tutto questo in 1-2 righe. Ma ora capisci COSA fa sotto il cofano!


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  ESERCIZI — Ora Prova Tu!                                             ║
# ╚═════════════════════════════════════════════════════════════════════════╝

# ESERCIZIO 1 (Facile):
# Usando la lista 'dati_csv' già caricata, scrivi il codice per:
# a) Stampare tutti gli ordini pagati con "PayPal"
# b) Contare quanti sono gli ordini PayPal vs Carta di Credito vs Bonifico
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 2 (Medio):
# Scrivi una funzione 'cerca_ordini(dati, **filtri)' che filtra la lista
# dati in base ai parametri passati. Esempio:
#   cerca_ordini(dati_csv, citta="Milano")
#   cerca_ordini(dati_csv, categoria="Elettronica", citta="Roma")
# Deve restituire tutti i record che corrispondono a TUTTI i filtri.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 3 (Medio):
# Leggi il file 'case.csv' (nella cartella dati/) e:
# a) Calcola il prezzo medio delle case per ogni città
# b) Trova la casa più costosa e stampa tutte le sue caratteristiche
# c) Calcola la correlazione prezzo/metri_quadri:
#    le case più grandi costano di più? Stampa i dati ordinati per mq
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 4 (Sfida):
# Scrivi una funzione 'csv_to_html_table(percorso_file)' che:
#   - Legge un file CSV
#   - Genera una stringa HTML con una <table> completa
#   - Include <thead> con i nomi colonne e <tbody> con i dati
# Questo è un vero "ponte" tra il mondo dei dati e il web!
#
# Scrivi il tuo codice qui sotto:
# ...


# ╔═════════════════════════════════════════════════════════════════════════╗
# ║  SOLUZIONI — Guardale Solo DOPO Aver Provato!                         ║
# ╚═════════════════════════════════════════════════════════════════════════╝

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
# for metodo, cnt in conteggio_metodo.items():
#     print(f"  {metodo}: {cnt} ordini")

# --- SOLUZIONE ESERCIZIO 2 ---
# def cerca_ordini(dati, **filtri):
#     """Filtra i dati in base ai parametri passati."""
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

# --- SOLUZIONE ESERCIZIO 3 ---
# percorso_case = os.path.join(percorso_dati, "case.csv")
# case = []
# with open(percorso_case, "r", encoding="utf-8") as f:
#     lettore = csv.DictReader(f)
#     for r in lettore:
#         case.append(r)
#
# # a) Prezzo medio per città
# somma_citta = {}
# conteggio_citta = {}
# for casa in case:
#     c = casa["citta"]
#     p = float(casa["prezzo_euro"])
#     somma_citta[c] = somma_citta.get(c, 0) + p
#     conteggio_citta[c] = conteggio_citta.get(c, 0) + 1
# print("Prezzo medio per città:")
# for c in somma_citta:
#     print(f"  {c}: {somma_citta[c]/conteggio_citta[c]:,.0f}€")
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

# --- SOLUZIONE ESERCIZIO 4 ---
# def csv_to_html_table(percorso_file):
#     html = '<table border="1" style="border-collapse: collapse;">\n'
#     with open(percorso_file, "r", encoding="utf-8") as f:
#         lettore = csv.reader(f)
#         header = next(lettore)
#         html += "  <thead><tr>\n"
#         for col in header:
#             html += f"    <th>{col}</th>\n"
#         html += "  </tr></thead>\n  <tbody>\n"
#         for riga in lettore:
#             html += "    <tr>\n"
#             for val in riga:
#                 html += f"      <td>{val}</td>\n"
#             html += "    </tr>\n"
#         html += "  </tbody>\n</table>"
#     return html
#
# html = csv_to_html_table(percorso_csv)
# print(html[:500])
