"""
============================================================================
 MODULO 1 — ESERCIZIO 03: Le Funzioni
 def vs function, Parametri, Return Multipli
============================================================================

 TEORIA: Le Funzioni in Python — Il Tuo "Controller" Personale

 Se lavori con Laravel, conosci i Controller: ricevono una richiesta,
 elaborano dati, restituiscono una risposta. Le funzioni Python sono
 esattamente questo, ma senza il framework attorno.

 Confronto a tre — la stessa funzione in PHP, JavaScript e Python:

   PHP:
     function saluta($nome) {
         return "Ciao $nome!";
     }
     // In PHP usi 'function', il $ davanti alle variabili,
     // e le graffe {} per il corpo della funzione.

   JavaScript:
     function saluta(nome) {
         return `Ciao ${nome}!`;
     }
     const saluta = (nome) => `Ciao ${nome}!`;  // arrow function
     // In JS puoi anche usare le arrow function (=>) per funzioni brevi.
     // I backtick `` con ${} sono i template literal per interpolare variabili.

   Python:
     def saluta(nome):
         return f"Ciao {nome}!"
     # 'def' al posto di 'function'
     # Due punti (:) al posto della graffa {
     # Indentazione (4 spazi) al posto del corpo tra graffe
     # f"..." è la f-string, equivalente dei template literal JS
     #   e dell'interpolazione "...$variabile..." di PHP
     # Non esiste la arrow function (=>) in Python

 Differenze chiave:
   PHP        → function, $variabili, graffe {}
   JavaScript → function o =>, template literal `${}`, graffe {}
   Python     → def, niente $, f-string f"{}", indentazione al posto di {}

============================================================================
"""

# ==========================================================================
# PARTE 1: Definire e Chiamare una Funzione
# ==========================================================================

# Funzione semplice senza parametri:
def saluta():
    print("Ciao! Benvenuto nel Modulo 1!")

saluta()  # Chiamata — identica a JavaScript e PHP: saluta();

# Funzione con parametri:
# PHP:        function salutaPersona($nome) { echo "Ciao $nome!"; }
# JavaScript: function salutaPersona(nome) { console.log(`Ciao ${nome}!`); }
# Python:
def saluta_persona(nome):
    print(f"Ciao {nome}! Come stai?")

saluta_persona("Marco")
saluta_persona("Laura")

# Funzione con return:
def calcola_iva(prezzo, aliquota=22):
    """
    Calcola il prezzo con IVA inclusa.
    'aliquota=22' è un PARAMETRO DEFAULT: se non lo passi, vale 22.

    Parametri default nelle tre lingue:
      PHP:        function calcolaIva($prezzo, $aliquota = 22) { ... }
      JavaScript: function calcolaIva(prezzo, aliquota = 22) { ... }
      Python:     def calcola_iva(prezzo, aliquota=22):
    Stessa idea in tutti e tre: se non passi il secondo parametro, usa 22.
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

# In PHP, se vuoi restituire più valori, devi usare un array associativo:
#   function analizza($testo) {
#       return [
#           'lunghezza' => strlen($testo),    // strlen() conta i caratteri
#           'parole' => str_word_count($testo) // str_word_count() conta le parole
#       ];
#   }
#   $risultato = analizza("Ciao mondo");
#   echo $risultato['lunghezza'];  // Accedi con la chiave
#
# In JavaScript, usi un oggetto:
#   function analizza(testo) {
#       return {
#           lunghezza: testo.length,           // .length = proprietà, dà la lunghezza
#           parole: testo.split(" ").length     // .split(" ") divide la stringa per spazi
#       };                                      //   e restituisce un array di parole
#   }                                           // .length su quell'array = numero di parole
#   const risultato = analizza("Ciao mondo");
#   console.log(risultato.lunghezza);  // Accedi con il punto
#
# In Python puoi restituire più valori DIRETTAMENTE, senza creare
# un oggetto o array wrapper. Sotto il cofano Python li mette in una
# "tupla" — per ora pensa a un array che non puoi modificare dopo averlo creato:

def analizza_testo(testo):
    """Analizza un testo e restituisce più informazioni."""
    lunghezza = len(testo)  # len() = strlen() in PHP, .length in JS
    num_parole = len(testo.split())  # split() divide per spazi, restituisce una lista
    # PHP:  explode(" ", $testo) → divide una stringa e restituisce un array
    # JS:   testo.split(" ")     → divide una stringa e restituisce un array
    # Python: testo.split()      → stessa cosa! Senza argomento divide per spazi
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

# Quando una funzione ha tanti parametri, ricordare l'ordine diventa difficile.
#
# In PHP, non c'è un modo nativo per passarli "per nome" (fino a PHP 8).
# Da PHP 8 in poi puoi fare:
#   creaProfilo(nome: "Marco", eta: 28, ruolo: "designer");
#   // I "named arguments" di PHP 8 funzionano come in Python!
#
# In JavaScript, il trucco è passare un oggetto con destructuring:
#   function creaUtente({ nome, eta, citta = "Roma" }) { ... }
#   // Le graffe {} nei parametri "scompongono" l'oggetto.
#   // citta = "Roma" è il valore default se non lo passi.
#   creaUtente({ nome: "Marco", eta: 28 });
#   // Devi sempre creare un oggetto {} quando chiami la funzione.
#
# In Python, è nativo — puoi chiamare i parametri per nome direttamente:

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

# A volte non sai quanti parametri riceverai.
#
# In PHP usi il variadic ... (da PHP 5.6):
#   function somma(...$numeri) {
#       return array_sum($numeri);
#       // array_sum() è una funzione built-in che somma tutti gli elementi
#       // di un array. $numeri diventa un array: [1, 2, 3, 4, 5]
#   }
#   somma(1, 2, 3);  // $numeri = [1, 2, 3] → restituisce 6
#
# In JavaScript usi il rest operator ... (stessa sintassi di PHP!):
#   function somma(...numeri) {
#       return numeri.reduce((acc, n) => acc + n, 0);
#       // .reduce() scorre l'array e "accumula" un risultato.
#       //   acc = accumulatore (il risultato parziale, parte da 0)
#       //   n = l'elemento corrente dell'array
#       //   acc + n = ad ogni giro, somma n al totale
#       // Esempio con [1, 2, 3]: 0+1=1, 1+2=3, 3+3=6 → restituisce 6
#       // JS non ha un equivalente di array_sum(), quindi serve reduce.
#   }
#   somma(1, 2, 3);  // numeri = [1, 2, 3] → restituisce 6
#
# In Python usi l'asterisco * (concetto identico, simbolo diverso):

# *args = cattura tutti i parametri posizionali in una tupla
# (una tupla è come un array PHP, ma non puoi modificarla dopo averla creata)
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
#
# Non esiste un equivalente diretto in PHP o JS. In PHP faresti:
#   function stampaInfo($info) {             // $info è un array associativo
#       foreach($info as $chiave => $valore) {
#           echo "$chiave: $valore\n";
#       }
#   }
#   stampaInfo(["nome" => "Marco", "eta" => 28]);  // devi creare l'array a mano
#
# In JavaScript, passeresti un oggetto:
#   function stampaInfo(info) {
#       Object.entries(info).forEach(([k, v]) => console.log(`${k}: ${v}`));
#       // Object.entries() trasforma {nome:"Marco", eta:28} in
#       // [["nome","Marco"], ["eta",28]] — un array di coppie [chiave, valore]
#       // .forEach() scorre ogni coppia, e ([k, v]) la "scompone" in k e v
#   }
#   stampaInfo({ nome: "Marco", eta: 28 });  // devi creare l'oggetto a mano
#
# In Python con **kwargs NON devi creare nessun dizionario — Python lo fa per te:
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

# Le funzioni lambda sono funzioni "usa e getta" di una sola riga.
#
# In PHP (da PHP 7.4) si chiamano "arrow functions":
#   $doppio = fn($x) => $x * 2;
#   echo $doppio(5);  // 10
#   // fn() è la keyword, => separa parametri dal corpo
#   // Prima di PHP 7.4 si usava: $doppio = function($x) { return $x * 2; };
#
# In JavaScript si chiamano "arrow functions":
#   const doppio = (x) => x * 2;
#   console.log(doppio(5));  // 10
#   // (x) sono i parametri, => è la "freccia", x * 2 è il corpo
#   // Se il corpo è una sola espressione, il return è implicito
#
# In Python si chiamano "lambda":
#   doppio = lambda x: x * 2
#   print(doppio(5))  // 10
#   // lambda è la keyword, x è il parametro, : separa dal corpo
#
# Non le userai spesso da sole, ma sono utilissime con sorted(), map(), filter().

doppio = lambda x: x * 2
print(f"\n=== Lambda ===")
print(f"doppio(5) = {doppio(5)}")

# Esempio pratico: ordinare una lista di dizionari per un campo specifico
# (come ORDER BY in SQL, come usort() in PHP).
prodotti = [
    {"nome": "Mouse", "prezzo": 29.99},
    {"nome": "Tastiera", "prezzo": 89.99},
    {"nome": "Cuffie", "prezzo": 49.99},
]

# In PHP ordineresti con usort() e una funzione di confronto:
#   usort($prodotti, function($a, $b) {
#       return $a['prezzo'] <=> $b['prezzo'];
#       // <=> è lo "spaceship operator": restituisce -1, 0 o 1
#       // a seconda che $a sia minore, uguale o maggiore di $b
#   });
#
# In JavaScript ordineresti con .sort() e una funzione di confronto:
#   prodotti.sort((a, b) => a.prezzo - b.prezzo);
#   // .sort() modifica l'array originale (attenzione!)
#   // La funzione dice: se il risultato è negativo, a viene prima di b
#
# In Python usi sorted() con key=lambda:
#   sorted() crea una NUOVA lista ordinata (non modifica l'originale)
#   key=lambda p: p["prezzo"] dice "ordina in base al prezzo di ogni prodotto"

prodotti_ordinati = sorted(prodotti, key=lambda p: p["prezzo"])
print("\nProdotti ordinati per prezzo:")
for p in prodotti_ordinati:
    print(f"  {p['nome']}: {p['prezzo']}€")

# ==========================================================================
# PARTE 6: Docstring — Documentare le Funzioni
# ==========================================================================

# In Python si usa una stringa con triple virgolette subito dopo 'def':
# Si chiama "docstring" e serve a documentare cosa fa la funzione.
#
# In PHP usi i commenti PHPDoc (che conosci da Laravel):
#   /**
#    * Calcola il prezzo scontato di un prodotto.
#    * @param float $prezzo Il prezzo originale
#    * @param float $percentuale La percentuale di sconto
#    * @return float Il prezzo finale
#    */
#   function calcolaSconto($prezzo, $percentuale) { ... }
#
# In JavaScript usi JSDoc (molto simile):
#   /**
#    * @param {number} prezzo - Il prezzo originale
#    * @param {number} percentuale - La percentuale di sconto
#    * @returns {number} Il prezzo finale
#    */
#   function calcolaSconto(prezzo, percentuale) { ... }
#
# In Python usi le docstring (più semplici, dentro la funzione stessa):

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
def converti_celsius_fahrenheit(gradi_celsius):
    gradi_fahrenheit = gradi_celsius * 9/5 + 32
    return gradi_fahrenheit

print(f"\n\nPrimo Esercizio")
print(f"\n{converti_celsius_fahrenheit(13)}°F")


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
def analizza_lista_prezzi(*prezzi):
    prezzo_minimo = min(prezzi)
    prezzo_massimo = max(prezzi)
    prezzo_medio = sum(prezzi) / len(prezzi)
    return prezzo_minimo, prezzo_massimo, prezzo_medio

print(f"\n\nSecondo Esercizio")
minimo, massimo, medio  = analizza_lista_prezzi(1,2,3,4,5)
print(f"\nPrezzo minimo: {minimo:.2f} €;\nPrezzo massimo: {massimo:.2f} €;\nPrezzo medio: {medio:.2f} €")



# ESERCIZIO 3 (Medio):
# Crea una funzione 'formatta_valuta(importo, valuta="EUR", decimali=2)'
# che formatta un importo come stringa:
#   formatta_valuta(1234.5)              → "1234.50 EUR"
#   formatta_valuta(1234.5, "USD")       → "1234.50 USD"
#   formatta_valuta(1234.5678, "GBP", 3) → "1234.568 GBP"
#
# Scrivi il tuo codice qui sotto:
def formatta_valuta(importo, valuta="EUR", decimali=2):
    stringa = f"{float(importo):.{decimali}f} {valuta.upper()}"
    return stringa
    
print(f"\n\nTerzo Esercizio")
print(formatta_valuta(12, "USD"))


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
def crea_risposta_api(dati, successo=True, messaggio="OK"):
    return{
        "success": successo,
        "message": messaggio,
        "data": dati,
        "count": len(dati) if isinstance(dati, list) else 1
    }


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
studenti = [
    {"nome": "Anna", "voto": 85},
    {"nome": "Marco", "voto": 92},
    {"nome": "Giulia", "voto": 78},
    {"nome": "Luca", "voto": 95},
]
studenti_ordinati = sorted(studenti, key=lambda v: v["voto"], reverse=True)
print(f"\n\nQuinto Esercizio")
for s in studenti_ordinati:
    print(f"{s['nome']}: {s['voto']}")



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
