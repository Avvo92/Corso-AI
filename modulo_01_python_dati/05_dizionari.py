"""
============================================================================
 MODULO 1 — ESERCIZIO 05: I Dizionari
 Dizionari, Iterazione, Nesting, Metodi Utili
============================================================================

 TEORIA: Dizionari Python = Oggetti JavaScript

 Se conosci gli oggetti JavaScript, i dizionari Python sono lo stesso
 concetto. Sono contenitori "chiave-valore":

   JavaScript:  const utente = { nome: "Luca", eta: 30 };
   Python:      utente = {"nome": "Luca", "eta": 30}

 DIFFERENZA IMPORTANTE:
 In JavaScript le chiavi dell'oggetto possono essere senza virgolette.
 In Python le chiavi del dizionario DEVONO essere tra virgolette (se stringhe).

   JavaScript:  { nome: "Luca" }      ← senza virgolette sulla chiave
   Python:      {"nome": "Luca"}      ← virgolette obbligatorie sulla chiave

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
# JavaScript:  utente.nome     oppure  utente["nome"]
# Python:      utente["nome"]  oppure  utente.get("nome")

print(f"\nNome: {utente['nome']}")
print(f"Lingue: {utente['lingue']}")
print(f"Prima lingua: {utente['lingue'][0]}")  # Lista dentro dizionario!

# .get() — L'equivalente dell'Optional Chaining (?.) di JavaScript:
# JavaScript:  utente?.indirizzo ?? "Non specificato"
# Python:      utente.get("indirizzo", "Non specificato")

print(f"\nIndirizzo: {utente.get('indirizzo', 'Non specificato')}")
# Se usi utente["indirizzo"] e la chiave non esiste → KeyError! (crash)
# Con .get() invece ottieni il valore di default senza crash.

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
# Come Object.assign() o spread in JavaScript:
#   utente = { ...utente, citta: "Roma", ruolo: "senior" }

utente.update({"citta": "Roma", "ruolo": "senior developer"})
print(f"Dopo update: {utente}")

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
# È come Object.entries() in JavaScript:
#   Object.entries(prodotto).forEach(([k, v]) => console.log(k, v));

print("\n=== Chiavi e valori ===")
for chiave, valore in prodotto.items():
    print(f"  {chiave}: {valore}")

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

# ==========================================================================
# PARTE 5: Dictionary Comprehension
# ==========================================================================

# Come le list comprehension, ma per i dizionari.
# Sintassi: {chiave: valore for elemento in iterabile}

# Esempio: creare un dizionario da due liste (come zip in JS):
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

# ==========================================================================
# PARTE 6: Metodi Utili
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
config_copia = config.copy()  # Come {...config} in JS (spread)
config_copia["tema"] = "light"
print(f"Originale: {config['tema']}")   # Rimane "dark"
print(f"Copia: {config_copia['tema']}")  # "light"


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


# ESERCIZIO 4 (Sfida):
# Scrivi una funzione 'conta_parole(testo)' che:
#   - Prende una stringa di testo
#   - Restituisce un dizionario con ogni parola e quante volte appare
#   - Le parole devono essere tutte in minuscolo
# Es: conta_parole("ciao mondo ciao") → {"ciao": 2, "mondo": 1}
# Suggerimento: testo.lower().split() divide il testo in parole minuscole.
#
# Scrivi il tuo codice qui sotto:
# ...


# ESERCIZIO 5 (Sfida — Simula API):
# Crea una funzione 'processa_ordini(ordini)' che prende una lista di
# ordini (come il dizionario 'ordine' della Parte 4) e restituisce un
# dizionario "report" con:
#   - "totale_ordini": numero di ordini
#   - "fatturato_totale": somma di tutti i totali
#   - "citta_piu_ordini": la città con più ordini
#   - "prodotto_piu_venduto": il prodotto che appare più volte
# Puoi creare una lista di 3-4 ordini per testarla.
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

# --- SOLUZIONE ESERCIZIO 4 ---
# def conta_parole(testo):
#     """Conta le occorrenze di ogni parola nel testo."""
#     conteggio = {}
#     for parola in testo.lower().split():
#         conteggio[parola] = conteggio.get(parola, 0) + 1
#     return conteggio
# print(conta_parole("Ciao mondo ciao a tutto il mondo"))

# --- SOLUZIONE ESERCIZIO 5 ---
# def processa_ordini(ordini):
#     conteggio_citta = {}
#     conteggio_prodotti = {}
#     fatturato = 0
#     for ordine in ordini:
#         fatturato += ordine["totale"]
#         citta = ordine["cliente"]["indirizzo"]["citta"]
#         conteggio_citta[citta] = conteggio_citta.get(citta, 0) + 1
#         for prod in ordine["prodotti"]:
#             nome = prod["nome"]
#             conteggio_prodotti[nome] = conteggio_prodotti.get(nome, 0) + prod["quantita"]
#     return {
#         "totale_ordini": len(ordini),
#         "fatturato_totale": round(fatturato, 2),
#         "citta_piu_ordini": max(conteggio_citta, key=conteggio_citta.get),
#         "prodotto_piu_venduto": max(conteggio_prodotti, key=conteggio_prodotti.get)
#     }
