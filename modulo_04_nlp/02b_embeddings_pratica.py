"""
============================================================================
MODULO 4 — CAPITOLO 02b (parte pratica)
Embeddings: farli funzionare con sentence-transformers
============================================================================

DA DOVE VIENI
-------------
In 02a hai CALCOLATO una mappa da 30 documenti: co-occorrenze -> PPMI -> SVD.
Quattro numeri per parola, zero download. Ha mostrato il fenomeno: parole
che si frequentano finiscono vicine, e "prospetto paga" trova "cedolino"
anche se non hanno una parola in comune.

Qui usi un modello GIÀ ADDESTRATO da qualcun altro su miliardi di frasi.
Le dimensioni non le scegli tu (sono 384), non hanno un nome, e la qualità
dipende dalla lingua su cui il modello è stato addestrato: un modello solo
inglese sull'italiano non crasha, peggiora in silenzio.

L'ANALOGIA
----------
02a = disegnare tu una cartina di 30 strade, a mano, col righello.
02b = aprire Google Maps: qualcuno ha già misurato il mondo intero.
Tu chiedi l'indirizzo di una frase e ti arrivano 384 numeri.

IL PONTE COL TUO MONDO (web)
----------------------------
Un modello di frasi è come un pacchetto maturo:

    JS       const modello = require("nome")        // npm: scarica, poi cache
    PHP      composer require vendor/nome           // vendor/ già pieno
    Python   SentenceTransformer("nome")            // cache Hugging Face

La "model card" (la scheda del modello su Hugging Face) è il suo README.
`encode()` è il suo unico metodo pubblico che ti serve. Sotto c'è un
Transformer vero: lo apriamo al cap.04. Oggi lo usi da utente, ma da utente
che sa cosa succede dentro la scatola (Sez. 2 e 3).

LA MAPPA DEL CAPITOLO (11 sezioni, ognuna con mini-esercizio di codice)
-----------------------------------------------------------------------
    1  Il modello come pacchetto: caricarlo UNA volta, la cache
    2  Dentro la scatola 1/2: le sottoparole (e perché non esistono più OOV)
    3  Dentro la scatola 2/2: il pooling, da tanti vettori a 384
    4  Da dove vengono quei numeri: apprendimento contrastivo
    5  Scegliere il modello: leggere la model card
    6  Stesso corpus, tre motori: TF-IDF vs mappa 02a vs MiniLM (la pagella)
    7  Quando il lessicale vince: cifre, IBAN, negazione
    8  Vettori lunghi 1: il prodotto scalare È il coseno
    9  Quanto costa: batch, memoria, il taglio a 128 pezzi
    10 Vedere le 30 note: la proiezione 2D (un'ombra, non la realtà)
    11 Salvare: il contratto dei vettori e il nome del modello

LE 3 PIPELINE DA TENERE A MEMORIA (le scriverai più volte, a mano)
-------------------------------------------------------------------
    P1  DA TESTI A VETTORI     carica modello -> embedda in batch -> normalizza
    P2  DA QUERY A RISULTATI   embedda query -> E @ q -> argsort -> top-k
    P3  DA VETTORI ALL'ARCHIVIO  embedda note -> dump -> contratto -> load
Il capitolo è costruito perché tu le scriva fino a non guardarle più.

TERMINI NUOVI (li userai dentro gli esercizi, non solo in teoria)
-----------------------------------------------------------------
    modello preaddestrato   model card          cache (dei pesi)
    sottoparola (subword)   pooling             normalizzare (norma 1)
    batch                   troncamento         top-k
    precision@k             benchmark           apprendimento contrastivo
    proiezione              dipendenza isolata

PREREQUISITO TECNICO (fatto il 08/10/2026)
------------------------------------------
`pip install sentence-transformers` nel venv del corso e primo download del
modello in cache (~470 MB). Se non l'hai fatto, il file si apre lo stesso:
il modello si carica solo dentro le funzioni, mai all'import. I quiz si
compilano anche senza.

Hardware: CPU va benissimo. MiniLM è piccolo apposta. `torch` nel venv è
la versione CPU: la RTX 3060 qui non serve e non verrebbe usata.
Privacy: solo `dati/note_documenti.csv` (testo sintetico). Nessun OCR reale.

📚 FONTI (riformulate DENTRO il capitolo, non devi aprire i PDF)
-----------------------------------------------------------------
[ALAMMAR cap. 2] "Tokens and Embeddings": sottoparole (Sez. 2), embedding di
frase (Sez. 3), word2vec e addestramento contrastivo (Sez. 4).
[ALAMMAR cap. 10] "What Is Contrastive Learning?": idea ripresa in Sez. 4
ed esercizio E9. [NLP-TRANS cap. 5+] per l'uso di sentence-transformers.
Scartato: addestrare un modello di frasi da zero (serve un corpus di coppie
e giorni di calcolo), fine-tuning (M8).
"""

from __future__ import annotations

import time
from collections import Counter   # serve all'esercizio E8
from pathlib import Path

import joblib                     # serve al progetto (T1, T2)
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Importati qui perché li usano gli esercizi E8 e il progetto: in un file
# di lavoro vero un import non usato si toglie, qui resta per te.
from testo_utils import (
    DIM,
    PERCORSO_CONTRATTO,
    PERCORSO_DATI,
    carica_mappa,
    classifica_tipo_documento,
    coseno,
    prepara_modello,
    tokenizza,
    vettore_frase,
)

QUI = Path(__file__).resolve().parent
PERCORSO_FIGURA = QUI / "dati" / "figure" / "note_minilm_2d.png"
PERCORSO_VETTORI = QUI / "dati" / "mappe" / "note_minilm.pkl"

MODELLO_ST = "paraphrase-multilingual-MiniLM-L12-v2"
# MiniLM multilingua: italiano compreso. 384 numeri per frase.
# "paraphrase" nel nome: addestrato apposta per riconoscere frasi che
# dicono la stessa cosa con parole diverse. È il nostro caso d'uso.

DIM_MINILM = 384
# Costante nostra. Se domani cambi modello questo numero cambia, e il
# contratto deve saperlo (Sezione 11).

# Banco di prova per la Sez. 6: (query, tipo di documento che DEVE uscire).
# Scritte da me, guardando i documenti: lo dico apertamente, è un limite
# (vedi Sez. 6, "vantaggio di casa").
BENCHMARK: list[tuple[str, str]] = [
    ("documento per la dichiarazione dei redditi", "cu"),
    ("certificato annuale dei redditi percepiti", "cu"),
    ("somma che ricevo dal datore di lavoro", "busta_paga"),
    ("foglio con retribuzione lorda e netto", "busta_paga"),
    ("elenco movimenti della banca", "estratto_conto"),
    ("saldo e movimenti del conto corrente", "estratto_conto"),
    ("quanto mi accreditano ogni mese", "busta_paga"),
    ("importo che arriva sul conto dal lavoro", "estratto_conto"),
]


# ==========================================================================
# QUIZ D'INGRESSO — sul 02a. Rispondi prima di scendere.
# ==========================================================================
#
# Q1. `costruisci_mappa` è più vicina a `fit` o a `transform`? E `vettore_frase`?
# costrusci_mappa è più vicino a fit, vettore_frase a transfrom.

# Q2. Vero o falso: se ricostruisco la mappa con dim=8, i vettori a 4 numeri
#     già in database restano confrontabili col coseno.
# No, il coseno confronta vettori di shape uguale. Se la mappa ha 8 dimensioni, i vettori nel database non possono essere utilizzati, e dobbiamo ricrearne di nuovi a 8 dimensioni. In particolare, questo non rende solo il coseno non utilizzabile per via della differenza di shape (non mancano solo 4 dimensioni), in realta sono proprio tutte coordinate diverse, che si riferiscono a mappe diverse.

# Q3. Una frase di sole parole sconosciute: `vettore_frase` cosa restituisce,
#     e il coseno con una frase vera quanto fa?
# vettore frase in questo caso restitutisce un vettore di soli 0, di shape = n_dimensioni_mappa. Il coseno prodotto dal confronto di questo vettore e una frase vera restituisce sempre 0 (è nell'impostazione della funzione coseno come guardia, perchè altrimenti nella formula divideremmo per 0). Il problema è che la risposta, che nel nostro caso dovremmo tradurre come "il modello non lo sa", diventa indistinguibile dalla risposta che il modello da quando due frasi hanno solo "significato effettivamente diverso".

# Q4. Perché in produzione si fa `carica_mappa` e non `costruisci_mappa`
#     a ogni query?
# Perchè ogni volta che usiamo il programma, ci troveremmo a dover ricalcolare la mappa, e questo ci fa sprecare calcoli e tempo. Con carica mappa, invece prendiamo una mappa già preparata. Inoltre, la mappa ricalcolata potrebbe non essere configurata per essere fruibile con i vettori che abbiamo in database.

# Q5. Completa: le dimensioni della SVD (e quelle di un modello vero) hanno
#     un nome di parola? Sì / no, in una riga.
# No, non hanno alcuna etichetta comprensibile da un operatore umano. Descrivono solo dei rapporti matematici, da cui sono estratte delle dimensioni che "funzionano" nel mappare delle parole in uno spazio multidimensionale.

# Q6. Tre job, tre righe (Pattern #6): (a) cosa guadagni con la mappa rispetto
#     al full-text; (b) cosa NON guadagni; (c) un caso in cui vince il match
#     esatto (CF, IBAN, ...).
# a) Guadagno la possibilità di trovare all'interno del database anche tramite ricerca di sinonimi, e non solo di parole esatte. Ricerca per significato.
# b) Non guadagni la possibilità di trovare cose specifiche e dettagliate in termini di scrittura assoluta, e la possibilità di selezionare frasi filtrandole anche in base all'ordine delle parole che vi compaiono
# c) Ricerca per nome proprio di persona, o codice preciso (es. Mario Rossi, pratica id A435bT)

# Q7. Type hint: il tipo di un vettore NumPy è `np.array` o `np.ndarray`?
# np.ndarray

# Q8. Una parola che compare UNA sola volta nei 30 documenti: finisce nella
#     mappa 02a? Quale costante lo decide, e quanto vale?
# No, non ci finisce. La costante che lo decide è MIN_CONTEGGIO, che abbiamo impostato a 2. Tutte le parole che compaiono una sola volta nel corpus, vengono scartate.
#
# TUE RISPOSTE:
#


# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — 02a + cap.01 (servono tutti e due)
# ==========================================================================
# 1) Coseno = quanto due frecce puntano nella stessa direzione. 1 = stesso
#    verso, 0 = indipendenti (o guardia: una delle due è tutta zeri).
# 2) TF-IDF = scheda pesata. Niente parole in comune -> coseno 0, anche se
#    le due frasi dicono la stessa cosa con sinonimi.
# 3) `costruisci_mappa` = fit (impari lo spazio). `vettore_frase` = transform
#    (leggi lo spazio già fatto). Il contratto annota `mappa_dim`: 4 e 8
#    non si mischiano.
# 4) La media dei punti-parola perde l'ordine (#62). Resta vero in generale,
#    ma qui cambia un pezzo: `encode()` legge la frase INTERA prima di
#    produrre i numeri. Come ci riesce è la Sezione 3: non è magia e non
#    lo diamo per scontato.


# ==========================================================================
# 🔁 RINFORZO MIRATO — Pattern #6 (E5 02a, esame 7/10: tre job, due coperti)
# ==========================================================================
# In E5 ti ho chiesto: cosa guadagni, cosa NON guadagni, quando vince il
# full-text. Hai coperto guadagno e full-text. Manca il "non guadagni"
# (cifre, IBAN, negazione, spiegabilità).
#
# ANTIDOTO, da usare in TUTTO questo capitolo: ogni consegna a più punti
# ha una riga "📋 PUNTI: N". PRIMA di scrivere, conta i punti e scrivi N
# nella riga "PUNTI CHE VEDO:". Poi rispondi a un punto alla volta e
# spuntalo. Se N non coincide, rileggi la consegna: è il passaggio che ti
# salva il voto.
#
# 🧩 Micro #6 — Senza codice. Tre righe:
#     📋 PUNTI: 3
#     PUNTI CHE VEDO: ___
#     1) Guadagno embedding vs TF-IDF
#     2) Cosa NON ti dà l'embedding
#     3) Un caso in cui il full-text vince
# TUA RISPOSTA:
#


# ==========================================================================
# 🔁 RINFORZO MIRATO — direzione senza nome (T5 02a tolto: noioso)
# ==========================================================================
# In 02a le 4 dimensioni della SVD non si chiamano "stipendio" o "IRPEF".
# MiniLM ne ha 384: stesso discorso. All'operatore puoi dire "questo
# documento punta vicino alla query". Non puoi dire "ha deciso la parola X"
# come facevi con `parole_decisive`.
#
# 🧩 Mini 0.1 — Una riga all'operatore quando la ricerca restituisce una nota,
#     e una riga su cosa NON prometti.
#     📋 PUNTI: 2        PUNTI CHE VEDO: 2
# TUA RISPOSTA:
# 1) La nota restituita è simile in termini di significato generale alla query.
# 2) Non possiamo definire quali parole hanno inciso di più per arrivare alla risposta.


# ==========================================================================
# SEZIONE 1 — Il modello come pacchetto: caricarlo UNA volta
# ==========================================================================
# `SentenceTransformer` è una classe: le dai il NOME di un modello, lei
# scarica i pesi (i miliardi di numeri imparati in addestramento) la prima
# volta e poi legge la CACHE su disco.
#
#   1a volta   rete -> download (~470 MB) -> cache su disco -> RAM
#   2a volta   cache su disco -> RAM            (niente rete)
#   stesso processo, 2a chiamata di encode      già in RAM (millisecondi)
#
# Tre tempi diversi, tre colpe diverse. Il primo lo paghi una volta nella
# vita del PC. Il secondo (caricare dalla cache alla RAM) lo paghi ad ogni
# AVVIO del programma: su questo PC, 15-22 secondi (misurato). Il terzo è
# il costo vero di una query: 30-90 millisecondi.
#
# La regola che ne discende è la stessa del Laravel che conosci: il modello
# si carica UNA volta all'avvio del servizio (come un singleton nel service
# container), mai dentro la richiesta. Caricarlo a ogni query è come
# riaprire la connessione al database a ogni riga di codice.
#
#   PHP     $this->app->singleton(Modello::class, fn() => new Modello(...));
#   JS      let modello; async function get() { return modello ??= await load(); }
#   Python  un dizionario a livello di modulo, o `functools.lru_cache`
#
# In Python il pattern più leggibile per un principiante è il dizionario
# di cache: lo scrivi tu nel Mini 1.2.
#
# DUE DETTAGLI DA NON SBAGLIARE
#   - Import DENTRO la funzione: l'import del capitolo non deve scaricare
#     400 MB solo perché stai leggendo i quiz. (Come un lazy `require`.)
#   - `embedda` accetta una stringa O una lista, e restituisce SEMPRE una
#     matrice (n, 384): chi chiama non gestisce due casi diversi.

def carica_modello_frasi(nome: str = MODELLO_ST):
    """Carica il modello. Import dentro la funzione, così leggere il file è
    gratis. La prima chiamata scarica i pesi nella cache di Hugging Face
    (su Windows: C:\\Users\\<tu>\\.cache\\huggingface). Le chiamate dopo
    leggono da lì: niente rete, niente attese lunghe.
    """
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(nome)


def embedda(testi, modello, normalizza: bool = False) -> np.ndarray:
    """Una frase -> una riga di 384 numeri. Lista di frasi -> matrice (n, 384).

    `normalizza=True` chiede vettori di lunghezza 1: serve in Sezione 8,
    dove il coseno diventa un semplice prodotto scalare.
    """
    if isinstance(testi, str):
        testi = [testi]
    vettori = modello.encode(
        testi,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=normalizza,
    )
    return np.asarray(vettori)


def carica_note(percorso=PERCORSO_DATI) -> pd.DataFrame:
    """Le 30 note sintetiche del cap.01: colonne id, tipo, testo."""
    return pd.read_csv(percorso)


# 🧩 Mini 1.1 — Due print, dopo aver caricato il modello una volta:
#     (a) shape di embedda("cedolino di marzo", modello);
#     (b) tempo (time.perf_counter) del SECONDO encode della stessa frase.
#     Non misurare il primo: include il caricamento dei pesi.
#     📋 PUNTI: 2        PUNTI CHE VEDO: ___
# TUO CODICE:

# if __name__ == "__main__":
    
#     print("Mini-esercizio 1.1\n")
    
#     frase = "cedolino di Marzo"
#     modello = carica_modello_frasi()   

    
#     t1 = time.perf_counter()
#     emb_frase = embedda(frase, modello)
#     t2 = time.perf_counter()
    
#     print(f"Shape di embedda: {emb_frase.shape}")
#     print(f"Tempo Secondo Encode: {t2 - t1}")
    
#
#
# PRIMA DI SCRIVERE — la cache in RAM (non è la cache su disco)
# ------------------------------------------------------------------------
# Due cache diverse, stesso nome, due posti.
#   - Su disco (Hugging Face, il sito da cui arrivano i pesi): i file del
#     modello. Sopravvive al riavvio del programma. `carica_modello_frasi`
#     li legge comunque, e quel passaggio costa i 15-22 secondi di avvio.
#   - In RAM, questo mini: un dizionario che vive finché il processo è
#     acceso. La seconda chiamata non ricarica: ti ridà lo stesso oggetto.
#
# Analogia. In Laravel un singleton nel container costruisce l'oggetto una
# volta sola; la richiesta dopo riceve quello. In JS:
#     let modello; function get() { return modello ??= await load(); }
# In Python il cassetto è un dizionario a livello di modulo (scritto fuori
# dalla funzione, accanto alle altre costanti). Chiave: il nome del modello.
# Valore: l'oggetto già costruito.
#
# Se il dizionario nasce DENTRO la funzione, ogni chiamata lo trova vuoto
# e paghi il caricamento un'altra volta.
#
# Schema, con nomi diversi dai tuoi (la funzione del mini la scrivi tu):
#     _CASSETTO = {}
#     def cosa_una_volta(chiave):
#         if chiave not in _CASSETTO:
#             _CASSETTO[chiave] = costruisci(chiave)   # questo costa
#         return _CASSETTO[chiave]
#
# `a is b` chiede: sono lo stesso oggetto in memoria?
# `==` chiederebbe: il contenuto conta come uguale?
# Due caricamenti separati fanno due oggetti: `is` è falso anche se i pesi
# sono gli stessi. La cache restituisce il primo oggetto: `is` è vero.
# Per un modello `==` non è il test di questo mini.
#
# 🧩 Mini 1.2 — Scrivi `modello_una_volta(nome=MODELLO_ST)`: usa un
#     dizionario di cache a livello di modulo (`_CACHE = {}`). Se il nome è
#     già nella cache restituisce lo STESSO oggetto, altrimenti lo carica
#     con `carica_modello_frasi`, lo salva e lo restituisce. Test:
#         a = modello_una_volta(); b = modello_una_volta(); assert a is b
#     Spiega in una riga cosa significa `is` qui e perché non `==`.
#     📋 PUNTI: 3        PUNTI CHE VEDO: 3
# TUO CODICE:

_MODELLO = {}
def modello_una_volta(nome: str):
    if nome not in _MODELLO:
        _MODELLO[nome] = carica_modello_frasi()   # questo costa
    return _MODELLO[nome]

# if __name__ == "__main__":
#     a = modello_una_volta(MODELLO_ST); b = modello_una_volta(MODELLO_ST);
#     assert a is b, "Ops, qualcosa è andato storto!"
#     print("Tutto ok!")
    
# Usiamo is perchè == vede se il contenuto delle due variabili conta come uguale, is invece ci dice se è proprio lo stesso iscritto nello stesso "cassetto" in ram.


# ==========================================================================
# SEZIONE 2 — Dentro la scatola 1/2: le sottoparole
# ==========================================================================
# Quando chiami `encode("cedolino di marzo")` dentro la scatola succedono
# TRE cose in fila. Le prime due sono sezioni 2 e 3, la terza è il risultato:
#
#   1) TOKENIZZA in sottoparole    <- questa sezione
#   2) TRANSFORMER + POOLING        <- Sezione 3
#   3) 384 numeri
#
# 🔁 RIPASSO PROPOSITIVO — OOV del cap.01 e 02a
# Nel cap.01 la tua `tokenizza` spezza in PAROLE. Una parola mai vista in
# training (OOV, Out Of Vocabulary: "fuori vocabolario") non ha casella e
# viene scartata. Nella mappa 02a è la stessa cosa: una parola con meno di
# MIN_CONTEGGIO=2 occorrenze non entra, e se TUTTA la frase è fatta di
# parole così il vettore è tutto zeri (Mini 5.2 di 02a, lacuna #63).
#
# I modelli moderni NON lavorano a parole. Lavorano a SOTTOPAROLE
# (subword): pezzi di parola scelti in modo statistico, i più frequenti
# in miliardi di testi. Misurato su questo modello:
#
#     "cedolino"    ->  _ce  do  lino            (3 pezzi)
#     "stipendio"   ->  _stipendi  o             (2 pezzi)
#     "irpef"       ->  _ir  pe  f               (3 pezzi)
#     "emolumenti"  ->  _em  olu  menti          (3 pezzi)
#     "cedolino di marzo" -> _ce do lino _di _marzo   (5 pezzi)
#
# Il segno `_` davanti a un pezzo (nel file originale è un segno speciale
# a forma di trattino basso) significa "qui comincia una parola nuova". Il
# pezzo senza `_` è la continuazione della parola di prima.
#
# ANALOGIA — i mattoncini. Il tokenizer di parole ha un mattoncino per
# ogni parola intera: se la parola non c'è, resti a mani vuote. Il
# tokenizer di sottoparole ha mattoncini più piccoli e comuni: non ha il
# pezzo "cedolino", ma lo costruisce con tre pezzi che ha. Una parola mai
# vista si scompone in pezzi già noti. In pratica: NIENTE PIÙ OOV secco.
#
# IL VOCABOLARIO DEL TOKENIZER (questo modello)
# Circa 250.000 pezzi, scelti una volta per tutte prima dell'addestramento.
# Ogni pezzo ha il suo vettore di partenza da 384 numeri: sono circa 96
# milioni dei 118 milioni di parametri del modello. Oltre l'80% del modello
# è questa tabella di indirizzi, uno per pezzo (verificalo: Mini 5.1).
#
# QUATTRO MODI DI SPEZZARE (riformulato da [ALAMMAR cap. 2]):
#
#   unità         esempio           pro                       contro
#   parola        cedolino          pezzi significativi        vocabolario enorme,
#                                                              OOV, plurali separati
#   sottoparola   _ce do lino       vocabolario medio,         una parola = più
#                                   nessun OOV                 pezzi (frasi più lunghe)
#   carattere     c e d o l i ...   vocabolario minuscolo       sequenze lunghissime,
#                                                              significato debole
#   byte          0x63 0x65 ...     copre QUALSIASI testo      ancora più lungo
#                                   (anche emoji, cinese)
#
# I modelli di oggi stanno quasi tutti sulla riga 2 (sottoparola) o 4
# (byte, per i modelli più grandi). La riga 2 è il compromesso vincente.
#
# CONSEGUENZA PRATICA, quella che ti riguarda: il costo e il limite di
# lunghezza non si contano in PAROLE ma in PEZZI. "Cedolino di marzo" sono
# 3 parole e 5 pezzi (7 con i due pezzi speciali, Sezione 3). In media un
# testo italiano ha circa 1,5-2,5 pezzi per parola, di più per le parole
# tecniche e lunghe (una nota con 300 parole da "retribuzione lorda mensile"
# fa 700 pezzi). Ricordalo alla Sezione 9 (il taglio).

def sottoparole(frase: str, modello) -> list[str]:
    """I pezzi in cui il tokenizer spezza la frase. Il segno speciale che
    marca l'inizio di parola è sostituito da "_" per leggerlo in console."""
    pezzi = modello.tokenizer.tokenize(frase)
    return [p.replace("\u2581", "_") for p in pezzi]


# 🧩 Mini 2.1 — Con `sottoparole`, conta i pezzi di: "cedolino", "stipendio",
#     "emolumenti", "xyzzyq" (una parola inventata). Stampa i quattro numeri.
#     Poi una riga: la parola inventata crasha o viene spezzata comunque?
#     📋 PUNTI: 3        PUNTI CHE VEDO: 3
# TUO CODICE:

if __name__ == "__main__":
    modello = modello_una_volta(MODELLO_ST)
    token_cedolino = sottoparole("cedolino", modello)
    token_stipendio = sottoparole("stipendio", modello)
    token_emolumenti = sottoparole("emolumenti", modello)
    token_xyzzyq = sottoparole("xyzzyq", modello)
    print(len(token_cedolino), len(token_stipendio), len(token_emolumenti), len(token_xyzzyq))

# TUA RISPOSTA:
# La parole inventata non crasha, viene comunque spezzata in sotto-parole.
#
#
# 🧩 Mini 2.2 — Una riga: perché con le sottoparole non serve più il
#     passaggio "scarta le parole non nel vocabolario" che avevi in 02a?
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 3 — Dentro la scatola 2/2: il pooling (da tanti vettori a 384)
# ==========================================================================
# Dopo la tokenizzazione, il modello ha una lista di pezzi. Per ogni pezzo
# ha un vettore di 384 numeri. Una frase da 5 pezzi ha 5 vettori. Una da 40
# pezzi ne ha 40. Ma noi vogliamo UN vettore per frase, sempre lungo 384.
#
# Come? In tre mosse:
#
#   (a) due pezzi SPECIALI ai bordi: uno in apertura e uno in chiusura.
#       "cedolino di marzo" = 5 pezzi + 2 speciali = 7 vettori.
#   (b) il TRANSFORMER fa "parlare" i vettori tra loro: ogni pezzo guarda
#       gli altri e aggiusta il proprio vettore in base al contesto. Il
#       "marzo" di "cedolino di marzo" non è il "marzo" di "marzo caldo
#       record". Questo meccanismo si chiama attention: lo apriamo al cap.04.
#   (c) il POOLING (da "pool", mettere insieme): si fa la MEDIA dei 7 vettori
#       riga per riga e si ottiene UN solo vettore di 384 numeri.
#
#   forma:  (7, 384)  -- media sulle righe -->  (384,)
#
# 🔁 RIPASSO PROPOSITIVO — la media del 02a (Sez. 5 di 02a)
# In 02a `vettore_frase` faceva la MEDIA dei punti-parola: sommi le
# coordinate di ogni parola e dividi. Era commutativa: scambi l'ordine delle
# parole e la media non cambia (#62, misurato: coseno 1.000 fra le due
# frasi invertite).
#
# Ecco la differenza che conta:
#
#   02a:    parola -> punto GIÀ FISSATO -> MEDIA
#           la media arriva su punti che non si parlano più.
#
#   MiniLM: pezzo -> vettore -> il Transformer li fa PARLARE -> MEDIA
#           la media arriva su vettori che si sono già "guardati".
#
# ANALOGIA — la media dei voti. In 02a facevi la media dei voti di studenti
# che hanno fatto l'esame da soli. Qui fai la media dei voti di studenti
# che hanno potuto discutere il compito prima di consegnare: i voti sono già
# influenzati dall'ordine e dal contesto. La media è la stessa operazione,
# ma gli ingredienti non sono più gli stessi.
#
# CONSEGUENZE (misurate nel demo in fondo):
#   - la shape del risultato è SEMPRE (384,), qualunque sia la lunghezza
#   - "banca conto" e "conto banca": coseno ~0.96, NON 1.000 come in 02a:
#     l'ordine lascia una traccia
#   - una frase passiva e una attiva con parole diverse dicono la stessa
#     cosa: coseno ~0.95
#   - una parola mai vista non azzera tutto: è spezzata in pezzi noti

def token_vettori(frase: str, modello) -> np.ndarray:
    """I vettori PRIMA del pooling: forma (n_pezzi_con_speciali, 384).
    Ogni riga è un pezzo, dopo che il Transformer li ha fatti parlare."""
    v = modello.encode(frase, output_value="token_embeddings",
                       convert_to_numpy=True, show_progress_bar=False)
    return np.asarray(v)


# 🧩 Mini 3.1 — Con `token_vettori`, stampa la shape per "cedolino di marzo"
#     e per una frase di 40 parole (inventala, ripeti "la busta paga" più
#     volte). Poi stampa la shape di `embedda` per le stesse due frasi.
#     Una riga: dove è sparita la differenza di lunghezza?
#     📋 PUNTI: 3        PUNTI CHE VEDO: 3
# TUO CODICE:

# print("\nMini 3.1 - 3.2\n")

# if __name__ == "__main__":
#     modello = modello_una_volta(MODELLO_ST)
#     frase_1 = "cedolino di marzo"
#     frase_2 = "La busta paga del mago arriva ogni mese con monete d'oro, detrazioni del drago e un netto che il cassiere elfo versa sul conto della torre dopo aver letto il cedolino incantato della gilda dei prestigiatori stamattina prima del tramonto."
#     token_emb_frase_1 = token_vettori(frase_1, modello)
#     token_emb_frase_2 = token_vettori(frase_2, modello)
#     emb_frase_1 = embedda(frase_1, modello)
#     emb_frase_2 = embedda(frase_2, modello)
#     print(token_emb_frase_1.shape)
#     print(token_emb_frase_2.shape)
#     print(emb_frase_1.shape)
#     print(emb_frase_2.shape)

# TUA RISPOSTA:
# La differenza è sparita con embedda, perchè token vettori restituisce i vettori dei token prima del pooling finale.
#
# 🧩 Mini 3.2 — Verifica TU che il pooling è una media: calcola
#     `token_vettori(f, modello).mean(axis=0)` e confrontala con
#     `embedda(f, modello)[0]` usando np.allclose. Stampa True o False.
#     📋 PUNTI: 2        PUNTI CHE VEDO: 2
# TUO CODICE:
#
    # token_emb_frase_1_mean = token_emb_frase_1.mean(axis=0)    
    # assert np.allclose(token_emb_frase_1_mean, emb_frase_1, atol=1e-9), "Ops, i valori dei due vettori non coincidono!"
    # print("Tutto ok, i vettori coincidono!")

# ==========================================================================
# SEZIONE 4 — Da dove vengono quei numeri: apprendimento contrastivo
# ==========================================================================
# Fin qui: come si usa il modello. Ora: come ha imparato. Non serve per
# usarlo, serve per capire PERCHÉ si comporta così e dove sbaglia.
# (Riformulato da [ALAMMAR cap. 2, sez. "word2vec" e cap. 10, "contrastive
# learning"]: non devi aprire il libro.)
#
# L'IDEA IN UNA RIGA
# Il modello impara guardando COPPIE: "queste due frasi dicono la stessa
# cosa, avvicinale" e "queste due no, allontanale".
#
# ANALOGIA — la riunione di condominio. Non hai la piantina del palazzo.
# Ti danno solo coppie: "il 3A e il 3B sono vicini di pianerottolo" e "il
# 3A e il 9F non c'entrano niente". Dopo milioni di coppie dai una posizione
# a ogni appartamento, e senza che nessuno ti abbia mai dato coordinate la
# planimetria viene fuori da sola.
#
# I TRE INGREDIENTI
#   1) COPPIE POSITIVE   "cedolino di marzo" / "busta paga di marzo"
#                         (parafrasi: da qui "paraphrase" nel nome)
#   2) COPPIE NEGATIVE   "cedolino di marzo" / "pizza margherita"
#   3) UNA REGOLA        positive: avvicinale. Negative: allontanale,
#                         ma solo finché non sono GIÀ lontane abbastanza
#                         (il "margine"): se spingessi sempre, i punti
#                         scapperebbero all'infinito.
#
# Questa è la versione più semplice, quella che scriverai tu nell'E9 con
# punti 2D, una dozzina di righe. Quella vera ha un nome (loss contrastiva)
# e una formula, ma il movimento è lo stesso: tira e spingi.
#
# E IL MULTILINGUA? Questo modello è stato ottenuto facendo imitare a un
# modello inglese (il "maestro") lo stesso significato in 50+ lingue, usando
# frasi tradotte a coppie. Risultato: la stessa frase in italiano e in
# inglese cade VICINA. Valori misurati:
#
#     "busta paga di marzo"     vs "march payslip"    -> 0.865
#     "estratto conto bancario" vs "bank statement"   -> 0.822
#     "busta paga di marzo"     vs "bank statement"   -> 0.230
#     "cedolino di marzo"       vs "pizza margherita" -> 0.167
#
# ATTENZIONE: NON esiste una scala universale del coseno. Guarda questi
# altri numeri, tutti misurati, e senti che cosa NON torna se provi a
# leggerli "in assoluto":
#
#   STESSA QUERY "cedolino di marzo", quattro candidati
#       "prospetto paga di aprile"      0.546   <- quello giusto
#       "dichiarazione dei redditi"     0.213
#       "pizza margherita"              0.167
#       "estratto conto bancario"       0.160
#
#   ALTRA QUERY "bonifico dello stipendio", quattro candidati
#       "dichiarazione dei redditi"     0.736   <- argomento DIVERSO
#       "accredito della retribuzione"  0.715   <- stesso significato
#       "salary transfer"               0.688   <- traduzione esatta
#       "pizza margherita"              0.094
#
# Un 0.736 è una frase su un argomento diverso; un 0.546 è una frase
# gemella. Dentro lo stesso dominio (soldi, documenti, importi) molte coppie
# stanno fra 0.5 e 0.75. Solo fuori dominio (la pizza) si scende a ~0.1-0.2.
#
# LA LEZIONE DA PORTARTI A CASA, IN UNA RIGA:
#       in una ricerca conta la CLASSIFICA (chi sta davanti, per la STESSA
#       query), non il numero assoluto. Confrontare il coseno di due coppie
#       diverse è come confrontare lo stipendio di due paesi senza il costo
#       della vita.
# Le SOGLIE ("sotto X rispondo: nessun risultato") non si copiano da un
# libro: si calibrano sui tuoi dati. Lo faremo nel M6.
#
# 🧩 Mini 4.1 — PREVEDI (alto / medio / basso), poi misura:
#       a) "bonifico dello stipendio"  /  "salary transfer"
#       b) "bonifico dello stipendio"  /  "dichiarazione dei redditi"
#       c) "bonifico dello stipendio"  /  "pizza margherita"
#     Calcola i tre coseni con `embedda` + `coseno`. Poi UNA riga: il numero
#     (b) è più alto o più basso di (a)? Cosa ti dice sul leggere un
#     coseno "in assoluto"?
#     📋 PUNTI: 4        PUNTI CHE VEDO: 4

# TUA PREVISIONE:
# a) alto b) medio c) basso

# TUO CODICE:

# if __name__ == "__main__":
#     print("\nMini 4.1\n")
#     modello = modello_una_volta(MODELLO_ST)
#     main_phrase = "bonifico dello stipendio"
#     other_phrases_list = [
#         "salary transfer",
#         "dichiarazione dei redditi",
#         "pizza margherita"        
#     ]
#     emb_main_phrase = embedda(main_phrase, modello)[0]
#     coseni = []
#     for p in other_phrases_list:
#         emb = embedda(p, modello)[0]
#         coseni.append(coseno(emb, emb_main_phrase))
#     results = {k: v for k, v in zip(other_phrases_list, coseni)}
#     print(results)    


# MISURA E RISPOSTA:
# b è più alto di a: questo a riprova del fatto che il coseno di due coppie non è un valore misurabile in termini assoluti.


# ==========================================================================
# SEZIONE 5 — Scegliere il modello: leggere la model card
# ==========================================================================
# Un MiniLM addestrato solo sull'inglese "capisce" l'italiano per analogia
# debole, o non lo capisce affatto. Non crasha: i numeri escono comunque, il
# coseno è basso o casuale. Bug silenzioso, stessa famiglia del mean/std
# sbagliato nel contratto visivo del M3: la pipeline gira, i numeri mentono.
#
# Come si sceglie senza scaricare a caso? Si legge la MODEL CARD: la pagina
# del modello su Hugging Face. È il README del pacchetto. Tre cose da
# guardare, in quest'ordine:
#
#   1) LINGUE — cerca "languages" / "multilingual". Il nostro modello è
#      addestrato su 50+ lingue, italiano compreso. Un "all-MiniLM-L6-v2"
#      (senza "multilingual") è solo inglese: più veloce, ma non per noi.
#
#   2) COMPITO — "paraphrase" / "semantic search" nel nome: addestrato su
#      coppie di frasi equivalenti. Esistono modelli fatti per altro
#      (classificazione, domanda-risposta): stesso motore, altro assetto.
#
#   3) TAGLIA — parametri, dimensione del vettore, lunghezza massima.
#      Questo modello: ~118 milioni di parametri, 384 numeri per frase,
#      lunghezza massima 128 pezzi. Gira su CPU. Modelli più grossi
#      (768 numeri) sono più precisi e più lenti. Su 30 note non si vede la
#      differenza; su 3 milioni forse sì. Si misura, non si indovina.
#
# Una quarta cosa, che non sta nella scheda: LA LICENZA. Prima di mettere un
# modello in un prodotto per clienti, leggi la riga "license". In questo
# percorso stiamo su modelli usabili per studio e prototipi.
#
# 🧩 Mini 5.1 — Scrivi `scheda_modello(modello) -> dict` con quattro chiavi:
#     "dimensioni", "max_seq_length", "parametri_milioni", "pezzi_vocabolario".
#     Aiuto sui nomi (sono la parte da imparare a cercare nella documentazione):
#       - `modello.get_embedding_dimension()` (il vecchio nome
#         `get_sentence_embedding_dimension` è stato rinominato: se lo vedi
#         in un tutorial, funziona ma ti dà un avviso)
#       - `modello.max_seq_length`
#       - `sum(p.numel() for p in modello.parameters())` (poi / 1e6)
#       - `modello.tokenizer.vocab_size`
#     Stampa il dizionario.
#     📋 PUNTI: 3        PUNTI CHE VEDO: 3
# TUO CODICE:

def scheda_modello(model) -> dict[str, int | float]:
    dimensioni = model.get_embedding_dimension()
    max_seq_lenght = model.max_seq_length
    milion_parameters = round(sum(p.numel() for p in model.parameters()) / 1e6, 2)
    vocabulary_pieces = model.tokenizer.vocab_size
    return {
        "dimensioni": dimensioni,
        "max_seq_length": max_seq_lenght,
        "parametri_milioni": milion_parameters,
        "pezzi_vocabolario": vocabulary_pieces
    }

if __name__ == "__main__":
    modello = modello_una_volta(MODELLO_ST)
    model_card = scheda_modello(modello)
    print(model_card)


# 🧩 Mini 5.2 — Un collega propone un modello inglese "perché è più
#     veloce e tanto i numeri escono lo stesso". Rispondi in due righe:
#     (1) il rischio, (2) UNA misura per dimostrarlo, con quale coppia.
#     📋 PUNTI: 2        PUNTI CHE VEDO: 2
# TUA RISPOSTA:
# Il rischio è una perdita silenziosa di precisione. Il modello darebbe lo stesso una risposta, ma produrrebbe risposte basate su affinità debole tra i token in inglese e in italiano.
# due frasi italiane che dicono la stessa cosa con parole diverse, come «cedolino di marzo» e «prospetto paga di aprile» nel capitolo 02a, e lo stesso coseno calcolato due volte, una col modello multilingua e una col modello solo inglese. Il primo resta alto. Il secondo crolla, senza eccezioni.

# ==========================================================================
# SEZIONE 6 — Stesso corpus, tre motori: la pagella
# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — i tre motori che hai già (cap.01, 02a)
#   cap.01  TF-IDF       conta parole pesate: "cedolino" cerca "cedolino".
#   02a     la mappa     4 numeri per parola da 30 documenti: cerca per
#                        compagnia di parole, ma solo sul vocabolario noto.
#   02b     MiniLM       384 numeri per frase da miliardi di frasi.
#
# Hanno tutti la stessa interfaccia: prendono una QUERY e danno i k documenti
# più vicini. Cambia solo come trasformano il testo in numeri.
#
# Prima le due frasi del 02a, poi la prova vera sui 30 documenti.
#
# PRIMO TEST — la coppia di sempre. "prospetto paga di aprile" e "cedolino
# di marzo": TF-IDF 0.000, mappa 02a ~0.96, MiniLM ~0.55. Il numero di
# MiniLM è PIÙ BASSO della tua mappa: per ora ricordalo, ci torniamo.
#
# SECONDO TEST — la pagella. Otto query (BENCHMARK, in cima al file),
# ognuna con il tipo di documento che DEVE uscire. Per ogni motore si
# guardano i primi tre risultati e si conta quanti sono del tipo giusto:
# questa misura si chiama PRECISION@K (precisione ai primi k: qui k=3).
#
#   una query con 3 risultati giusti    -> 3/3 = 1.00
#   una con 1 giusto su 3                -> 0.33
#   media su tutte le query               -> il voto del motore
#
# Termini: TOP-K = "i primi k". BENCHMARK = un banco di prova fisso con
# domande e risposte attese, per confrontare motori sullo stesso terreno.
#
# RISULTATO (misurato con il tuo mappa.pkl; il tuo può differire di poco):
#
#       TF-IDF   0.62      mappa 02a   0.83      MiniLM   0.75
#
# Sorpresa: la mappa fatta in casa BATTE il modello da 118 milioni di
# parametri. Non è un errore, e non è una vittoria da festeggiare. Tre
# motivi, in ordine di peso:
#
#   (1) VANTAGGIO DI CASA. La mappa è stata costruita SUGLI STESSI 30
#       documenti in cui poi cerca. Ha imparato il loro vocabolario e le
#       loro compagnie di parole. MiniLM non ha mai visto questi documenti.
#       È il data leakage del M2: valutare un modello sugli stessi dati su
#       cui ha imparato gonfia il voto. Per un confronto onesto la mappa
#       andrebbe costruita su un pezzo del corpus e valutata sull'altro.
#
#   (2) BENCHMARK MINUSCOLO. Otto query: ognuna pesa il 12,5% della media.
#       Cambiare il risultato di UNA query sposta la pagella di 4 punti.
#       Con otto query non si dichiarano vincitori, si formulano ipotesi.
#
#   (3) BENCHMARK SCRITTO DALL'AUTORE. Le query le ho scritte io guardando i
#       documenti. Un banco di prova serio si scrive PRIMA, e lo scrivono
#       persone che cercano davvero (i colleghi, con le loro parole).
#
# DOVE MiniLM VINCE DAVVERO: sulle parole NUOVE. La mappa e TF-IDF possono
# parlare solo del vocabolario visto in training. Misurato:
#
#   query "remunerazione del lavoratore subordinato"
#       TF-IDF   tutti i punteggi 0.0  (nessuna parola in comune)
#       mappa    vettore tutto zeri    (nessuna parola nel vocabolario)
#       MiniLM   risponde con tre note, senza essere "cieco"
#
# Attenzione a non esagerare: "non essere cieco" NON è "avere ragione".
# MiniLM risponde SEMPRE, anche quando dovrebbe dire "non lo so" (prova
# "pizza margherita": ti dà comunque tre note, con punteggi molto bassi,
# 0.11-0.16). Serve una SOGLIA: sotto il punteggio X si risponde "nessun
# risultato". La soglia la scegliamo al M6 con dati veri (vedi Sez. 4:
# il coseno non ha una scala universale).
#
# E il TF-IDF e la mappa ora? Se TUTTI i punteggi sono 0.0 le funzioni
# restituiscono lista vuota: un podio di zeri non è una risposta, e senza
# questo filtro `argsort` ti restituirebbe tre indici a caso (i primi o gli
# ultimi, a seconda dell'ordine) che sembrano un risultato. È lo stesso
# principio della guardia del coseno 0.0 del 02a (#63): 0.0 può significare
# "ignoranza", non "diverso".
#
# 🧩 Mini 6.1 — Lancia `confronto_due_frasi(modello)` e scrivi i due numeri
#     (TF-IDF e MiniLM). Poi una riga: il numero di MiniLM è più basso di
#     quello della mappa 02a (~0.96). Vuol dire che MiniLM sbaglia?
#     Aiuto: rileggi "la lezione in una riga" della Sezione 4.
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUA RISPOSTA:

def confronto_due_frasi(modello) -> dict[str, float]:
    """Coseno TF-IDF vs coseno MiniLM sulle due parafrasi del 02a."""
    a = "prospetto paga di aprile"
    b = "cedolino di marzo"
    vec = TfidfVectorizer(tokenizer=tokenizza, token_pattern=None, lowercase=False)
    X = vec.fit_transform([a, b]).toarray()
    cos_tfidf = float(coseno(X[0], X[1]))
    E = embedda([a, b], modello)
    cos_st = float(coseno(E[0], E[1]))
    return {"tfidf": round(cos_tfidf, 3), "minilm": round(cos_st, 3)}

if __name__ == "__main__":
    print("\nMini 6.1\n")
    print(confronto_due_frasi(modello_una_volta(MODELLO_ST)))


def _top_k(punteggi: np.ndarray, k: int, soglia: float = 0.0) -> list[tuple[int, float]]:
    """Gli indici dei k punteggi più alti, con il loro punteggio.
    Scarta i punteggi <= soglia: un podio di zeri non è una risposta."""
    ordine = np.argsort(punteggi)[::-1][:k]
    return [(int(i), round(float(punteggi[i]), 3)) for i in ordine if punteggi[i] > soglia]


def vicini_tfidf(query: str, k: int = 3, percorso=PERCORSO_DATI) -> list[tuple[int, float]]:
    """Motore 1 (cap.01): TF-IDF. Restituisce [(indice, coseno)] ordinato."""
    testi = carica_note(percorso)["testo"].tolist()
    vec = TfidfVectorizer(tokenizer=tokenizza, token_pattern=None, lowercase=False)
    X = vec.fit_transform(testi).toarray()
    q = vec.transform([query]).toarray()[0]
    punteggi = np.array([coseno(q, X[i]) for i in range(len(testi))])
    return _top_k(punteggi, k)


def vicini_mappa(query: str, k: int = 3, mappa: dict | None = None,
                 percorso=PERCORSO_DATI) -> list[tuple[int, float]]:
    """Motore 2 (02a): la mappa fatta in casa, vettore_frase + coseno."""
    mappa = mappa if mappa is not None else carica_mappa()
    testi = carica_note(percorso)["testo"].tolist()
    q = vettore_frase(query, mappa)
    punteggi = np.array([coseno(q, vettore_frase(t, mappa)) for t in testi])
    return _top_k(punteggi, k)


def vicini_minilm(query: str, modello, k: int = 3, E: np.ndarray | None = None,
                  percorso=PERCORSO_DATI) -> list[tuple[int, float]]:
    """Motore 3 (02b): MiniLM. E = vettori dei documenti GIÀ calcolati e
    normalizzati (consigliato). Se E è None li ricalcola: comodo per una
    prova, sbagliato in produzione (Sezione 11).

    Con vettori di lunghezza 1 il coseno di tutti i documenti è UNA
    moltiplicazione di matrice (Sezione 8):  (30, 384) @ (384,) -> (30,)
    """
    testi = carica_note(percorso)["testo"].tolist()
    if E is None:
        E = embedda(testi, modello, normalizza=True)
    q = embedda(query, modello, normalizza=True)[0]
    return _top_k(E @ q, k)


def pagella(modello, k: int = 3) -> dict[str, float]:
    """Precision@k media sui BENCHMARK, per i tre motori."""
    dati = carica_note()
    testi, tipi = dati["testo"].tolist(), dati["tipo"].tolist()
    mappa = carica_mappa()
    E = embedda(testi, modello, normalizza=True)
    somme = {"tfidf": 0.0, "mappa": 0.0, "minilm": 0.0}
    for query, atteso in BENCHMARK:
        trovati = {
            "tfidf": vicini_tfidf(query, k),
            "mappa": vicini_mappa(query, k, mappa),
            "minilm": vicini_minilm(query, modello, k, E),
        }
        for motore, lista in trovati.items():
            giusti = sum(1 for i, _ in lista if tipi[i] == atteso)
            somme[motore] += giusti / k
    return {m: round(s / len(BENCHMARK), 3) for m, s in somme.items()}


def copertura_query(query: str, mappa: dict) -> float:
    """Quota delle parole della query che la mappa 02a conosce (0.0 - 1.0).
    0.0 = la mappa è cieca; 1.0 = conosce tutte le parole."""
    parole = tokenizza(query)
    if not parole:
        return 0.0
    return sum(1 for p in parole if p in mappa) / len(parole)


# 🧩 Mini 6.2 — Lancia `vicini_tfidf` e `vicini_minilm` sulla query
#     "documento per la dichiarazione dei redditi". Per ognuno stampa i tre
#     indici e il TIPO di ciascuno (usa `carica_note()["tipo"]`).
#     Poi una riga: chi ha capito cosa cercavi?
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#
#
# 🧩 Mini 6.3 — Calcola `copertura_query` per queste tre query, con la
#     mappa 02a: "remunerazione del lavoratore subordinato", "compenso
#     mensile per il dipendente", "pizza margherita". Scrivi i tre numeri.
#     Poi: perché la prima ti dà un podio vuoto con TF-IDF e un podio
#     pieno con MiniLM? Una riga.
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#
#
# 🧩 Mini 6.4 — Lancia `pagella(modello)` e scrivi i tre numeri. Poi UNA
#     riga: quale dei tre motivi (vantaggio di casa / benchmark minuscolo /
#     scritto dall'autore) è il più forte e come lo verificheresti?
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 7 — Quando il lessicale vince: cifre, IBAN, negazione
# ==========================================================================
# Query: un codice fiscale, un IBAN, un numero di pratica. L'embedding
# "arrotonda" il senso: RSSMRA80A01H501U e RSSMRA80A02H501U per lui sono
# quasi la stessa stringa, quindi quasi lo stesso vettore. Il full-text (o
# TF-IDF sulla stringa esatta) trova la riga giusta e basta.
#
# TRE TRAPPOLE DEL SENSO (misurate)
#
#   CIFRE      "sconto 10%" vs "sconto 90%"      -> coseno 0.83
#              Per il modello: quasi gemelle. Per la torre: molto diverse.
#
#   NEGAZIONE  "contratto valido" vs "contratto non valido" -> coseno 0.78
#              Quasi tutto il lessico è lo stesso. I modelli moderni la
#              trattano meglio di una media di punti, ma resta un punto
#              debole noto: non promettere all'operatore che la ricerca
#              "capisce il non".
#
#   CODICI     un IBAN o un CF: serie di cifre e lettere senza senso. Il
#              match esatto vince perché non c'è "significato" da
#              catturare, c'è una chiave.
#
# Nella torre la risposta non è scegliere: è la ricerca IBRIDA (arriva
# nel M6) = lessicale + semantica, fusi in un unico punteggio. Tu oggi
# costruisci il braccio semantico; il braccio lessicale ce l'hai dal cap.01.
#
# 🧩 Mini 7.1 — Scrivi una query (sintetica) per cui useresti il match
#     esatto e NON MiniLM, e il motivo in mezza riga.
#     📋 PUNTI: 2        PUNTI CHE VEDO: ___
# TUA RISPOSTA:
#
#
# 🧩 Mini 7.2 — PREVEDI (alto/basso) e POI misura il coseno MiniLM di:
#       a) "sconto 10%" / "sconto 90%"
#       b) "contratto valido" / "contratto non valido"
#     Quale delle due coppie, secondo te, è più pericolosa per la torre
#     e perché? Una riga.
#     📋 PUNTI: 4        PUNTI CHE VEDO: ___
# TUA PREVISIONE:
# TUO CODICE:
# MISURA E RISPOSTA:
#


# ==========================================================================
# SEZIONE 8 — Vettori lunghi 1: il prodotto scalare È il coseno
# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — coseno (Ponte, poi 02a Sez. 3)
# coseno(a, b) = prodotto scalare / (lunghezza di a x lunghezza di b).
# La tua `coseno` in testo_utils fa esattamente questo, più la guardia
# sul vettore nullo.
#
# NORMALIZZARE un vettore = dividerlo per la sua lunghezza, così che la
# lunghezza diventi 1 (norma 1). Direzione identica, lunghezza fissata. Un
# `encode` normale ti dà vettori di lunghezza ~3.7 (misurato); con
# `normalize_embeddings=True` sono tutti 1.0.
#
# Se la lunghezza è già 1, il denominatore è 1 x 1 = 1. Resta solo il
# prodotto scalare. Niente divisioni, niente radici quadrate.
#
# Perché ci interessa? Velocità e semplicità. Il coseno fra UNA query e
# TRENTA documenti diventa una riga di NumPy:
#
#     punteggi = E @ q        # E è (30, 384), q è (384,)  ->  (30,)
#
# Trenta coseni in una moltiplicazione di matrice. Su 30 documenti non
# cambia niente; su 3 milioni è la differenza fra "subito" e "dopo
# pranzo". È lo stesso trucco che userà pgvector (l'estensione di
# PostgreSQL per i vettori) nel M6 dentro il database.
#
# REGOLA D'ORO: se normalizzi i documenti, normalizza ANCHE la query. Una
# sola delle due non fa fallire niente, dà numeri sbagliati. (È lo stesso
# bug silenzioso di mean/std sbagliato nel contratto visivo del M3.)
#
# 🧩 Mini 8.1 — Calcola la norma (np.linalg.norm) di un vettore ottenuto con
#     `normalizza=False` e di uno con `normalizza=True` (stessa frase).
#     Stampa i due numeri.
#     📋 PUNTI: 2        PUNTI CHE VEDO: ___
# TUO CODICE:
#
#
# 🧩 Mini 8.2 — Prendi due vettori con normalizza=True, calcola
#     `coseno(a, b)` con la tua funzione e poi `a @ b`. Stampa la
#     differenza assoluta: deve essere quasi zero (errori di arrotondamento
#     dei float, ordine 1e-7). Una riga: perché sono uguali?
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 9 — Quanto costa: batch, memoria, il taglio a 128 pezzi
# ==========================================================================
# "Il modello è veloce" non è un'informazione. I numeri sì. Tre cose da
# misurare una volta sola, e poi sai ragionare.
#
# A) BATCH. Cento frasi in UNA chiamata costano MOLTO meno di cento chiamate
#    singole. Motivo: a ogni chiamata paghi un costo fisso (preparazione,
#    trasferimento dati) più il lavoro vero. In batch il costo fisso si
#    paga una volta sola. È la differenza fra una INSERT multipla e cento
#    INSERT singole: stessa tabella, tempi diversi. Misurato sulle tue 30
#    note: batch ~0.3-0.4s vs singole ~1s, cioè 2,5-3 volte (il numero
#    oscilla da una esecuzione all'altra: misuralo più volte). Più note,
#    più il rapporto tende a crescere.
#
# B) MEMORIA. 30 vettori x 384 numeri x 4 byte (float32) = 46 KB. Niente.
#    Ma scala: 3 milioni di documenti x 384 x 4 byte = 4,6 GB. Anche per
#    questo nel M6 i vettori finiscono in un database fatto apposta, non in
#    un pickle.
#
# C) IL TAGLIO. Il modello ha un limite di lunghezza: questo ne vede 128
#    PEZZI (non parole, Sez. 2), compresi i due speciali. Il resto viene
#    TAGLIATO IN SILENZIO. Nessun errore, nessun avviso da `encode()`.
#    Misurato: una nota di 245 pezzi e la stessa nota con in coda altri sei
#    pezzi (una clausola importante) hanno coseno 1.000000. La coda è
#    sparita: per il modello è come se non esistesse.
#
#    In pratica: un contratto incollato intero in una nota, la clausola di
#    recesso alla fine NON viene trovata. Il bug non si vede nei test con
#    note brevi: lo scopri in produzione, quando un cliente lamenta che "la
#    ricerca non trova niente".
#
#    Si risolve spezzando il testo in porzioni (chunking, M6). Per ora basta
#    saper RICONOSCERE il rischio: confronta il numero di pezzi col limite.
#    Il conto è: pezzi della frase + 2 speciali > `max_seq_length`?
#
#    Sulle tue 30 note oggi il rischio è zero: la più lunga ha 38 pezzi,
#    ben sotto 128. Il giorno in cui arriveranno note vere (OCR di intere
#    pagine) il rischio ci sarà: per questo il controllo entra nel progetto
#    come guardia (T4) prima ancora che serva.

def rischio_troncamento(testo: str, modello) -> dict[str, object]:
    """Il testo supera la lunghezza massima del modello? {n_pezzi, limite, troncato}."""
    n = len(modello.tokenizer.tokenize(testo))
    limite = int(modello.max_seq_length)
    return {"n_pezzi": n, "limite": limite, "troncato": n + 2 > limite}


# 🧩 Mini 9.1 — Misura (4-5 righe): tempo di encode delle 30 note in UNA
#     chiamata batch, poi tempo di 30 encode singole in ciclo. Stampa i due
#     tempi e il rapporto. (time.perf_counter, come nella demo.)
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# RISULTATO:
#
#
# 🧩 Mini 9.2 — Con `rischio_troncamento`: (a) controlla le 30 note e
#     stampa quante sono troncate; (b) costruisci una nota artificiale di
#     300 parole (ripeti "retribuzione lorda mensile ") e controllala.
#     (c) una riga: cosa significa "troncato = True" per quella nota?
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 10 — Vedere le 30 note: la proiezione 2D (un'ombra)
# ==========================================================================
# I numeri non si guardano. Quando hai 384 dimensioni, "vedere" sembra
# impossibile: come disegni uno spazio a 384 assi? Non lo disegni. Ne fai
# una PROIEZIONE: la sua ombra su un foglio a due assi.
#
# ANALOGIA — l'ombra. Una sedia a tre dimensioni proiettata su un muro è
# un'ombra piatta. Due sedie lontane, messe una dietro l'altra rispetto alla
# lampada, hanno ombre sovrapposte pur essendo lontane. L'ombra perde
# informazione: quello che vedi sovrapposto sul grafico non è detto sia
# vicino nei 384 assi, e due punti lontani nel disegno possono essere
# vicini nello spazio vero.
#
# COME SI FA, e ti è già noto
# 🔁 RIPASSO PROPOSITIVO — la SVD del 02a (Sez. 2, passo 4)
# In 02a hai usato `np.linalg.svd` per comprimere 49 numeri in 4. Qui la
# stessa SVD comprime 384 numeri in 2, ma con un passo in più: PRIMA si
# sottrae a ogni colonna la sua media (si "centrano" i dati), poi si prende
# la SVD, poi si tengono le prime due direzioni. Questa ricetta ha un
# nome: PCA (Analisi delle Componenti Principali). Stessa famiglia, stessa
# idea: tieni le direzioni lungo cui i dati variano di più.
#
# QUANTO INFORMAZIONE SI SALVA? Quantità misurabile: la "varianza
# spiegata" dai due assi, cioè la quota di variazione totale che le due
# direzioni conservano. Sulle tue 30 note: circa il 27%. Vuol dire che il
# disegno racconta poco più di un quarto della storia. Basta per vedere
# raggruppamenti larghi, non per leggere distanze fini. Per questo il
# grafico è un aiuto per l'occhio, non una prova.
#
# COSA ASPETTARSI
# Tre tipi di nota (busta paga, CU, estratto conto) più un quarto "altro".
# I tre centri sono distinti ma le nuvole si sovrappongono un po'. Non è
# un difetto del modello: sono documenti simili fra loro (tutti parlano di
# soldi, importi, date) e il disegno ha solo 2 assi.

def proietta_2d(E: np.ndarray) -> tuple[np.ndarray, float]:
    """(n, 384) -> (n, 2) e quota di varianza spiegata dai 2 assi."""
    C = E - E.mean(axis=0)                      # centra: sottrai la media colonna per colonna
    U, s, _ = np.linalg.svd(C, full_matrices=False)
    P = U[:, :2] * s[:2]                        # stessa ricetta del 02a: U x s, prime 2 colonne
    varianza = float((s[:2] ** 2).sum() / (s ** 2).sum())
    return P, varianza


def disegna_note(E: np.ndarray, tipi: list[str], percorso: Path = PERCORSO_FIGURA,
                 mostra: bool = False) -> Path:
    """Salva uno scatter 2D delle note, un colore per tipo di documento."""
    import matplotlib
    if not mostra:
        matplotlib.use("Agg")      # nessuna finestra: salva soltanto
    import matplotlib.pyplot as plt

    P, var = proietta_2d(E)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for tipo in sorted(set(tipi)):
        idx = [i for i, t in enumerate(tipi) if t == tipo]
        ax.scatter(P[idx, 0], P[idx, 1], s=70, label=tipo, alpha=0.85)
        for i in idx:
            ax.annotate(str(i), (P[i, 0], P[i, 1]), fontsize=8,
                        xytext=(4, 4), textcoords="offset points")
    ax.set_title(f"30 note proiettate su 2 assi ({var:.0%} dell'informazione)")
    ax.set_xlabel("asse 1 (senza nome)")
    ax.set_ylabel("asse 2 (senza nome)")
    ax.legend(title="tipo di nota")
    ax.grid(alpha=0.25)
    fig.savefig(percorso, dpi=140, bbox_inches="tight")
    if mostra:
        plt.show()
    plt.close(fig)
    return percorso


# 🧩 Mini 10.1 — Con `proietta_2d` e le 30 note (E normalizzati):
#     (a) stampa la varianza spiegata dai 2 assi;
#     (b) per ogni tipo, stampa la DISPERSIONE (deviazione standard di P per
#         quel tipo, `P[maschera].std()`). Quale tipo è più sparso?
#     (c) lancia `disegna_note(...)` e apri il file PNG che stampa: scrivi
#         l'indice di UN punto che sta in mezzo a un gruppo di un altro tipo.
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#


# ==========================================================================
# SEZIONE 11 — Salvare: il contratto dei vettori e il nome del modello
# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — contratto (M3, poi T3 del 02a)
# Nel M3 il contratto annotava mean/std delle immagini: chi carica il
# modello deve sapere come erano preparati i dati, altrimenti i numeri
# mentono. Nel 02a hai esteso il contratto con `mappa_dim`, `min_conteggio`,
# `n_parole`: chi carica `mappa.pkl` sa che spazio sta leggendo.
#
# Con MiniLM il rischio è lo stesso con un nome in più: il MODELLO.
# I 384 numeri di `paraphrase-multilingual-MiniLM-L12-v2` NON sono
# confrontabili con i 384 numeri di un altro modello a 384 dimensioni:
# stessa forma, spazi diversi. Come due cartine entrambe in scala
# 1:100.000 ma con proiezioni diverse: le coordinate sembrano uguali, non
# lo sono. LA DIMENSIONE DICE LA FORMA, IL NOME DEL MODELLO DICE LO SPAZIO.
#
# Regola della torre: nel contratto, accanto ai vettori salvati, si annota
# SEMPRE il nome del modello che li ha prodotti. Cambi modello -> ricalcoli
# TUTTI i vettori. Non si mischiano mai, nemmeno "per provare".
#
# CHE COSA SI SALVA (e perché conviene)
#   - I VETTORI delle note (30 x 384), calcolati una volta. Ricalcolarli a
#     ogni avvio costa 0.4s su 30 note; su 3 milioni costa ore.
#   - Il CONTRATTO: nome del modello, dimensioni, lunghezza massima, quante
#     note, quando.
#   - NON il modello: è in cache. Salvare i 118 milioni di parametri nel
#     pickle sarebbe uno spreco e una trappola di versioni.
#
# DIPENDENZA ISOLATA (termine nuovo, concetto vecchio)
# `testo_utils.py` si importa SENZA sentence-transformers: usa solo numpy,
# pandas, sklearn. Se ci infilassi anche il codice che carica MiniLM, ogni
# script che importa `testo_utils` dipenderebbe da un pacchetto da 400 MB.
# Per questo il codice nuovo vive in un modulo SEPARATO, `embed_utils.py`
# (lo scrivi nel progetto). In Laravel è la stessa scelta di un pacchetto
# `composer` separato: chi non ne ha bisogno non lo installa.
#
# 🧩 Mini 11.1 — Scrivi la riga (o le righe) che aggiungono al dizionario
#     `contratto` le chiavi `"modello_minilm"`, `"mappa_dim_minilm"` e
#     `"minilm_max_seq_length"`. Poi UNA riga: perché non basta
#     `mappa_dim_minilm = 384`?
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
# TUO CODICE:
# TUA RISPOSTA:
#
#
# LE TRE PIPELINE, IN UNA PAGINA (da imparare a memoria)
#
#   P1  da testi a vettori
#         modello = carica_modello_frasi()
#         E = embedda(testi, modello, normalizza=True)       # (n, 384), norma 1
#
#   P2  da query a risultati
#         q = embedda(query, modello, normalizza=True)[0]    # (384,)
#         punteggi = E @ q                                    # (n,)
#         top = np.argsort(punteggi)[::-1][:k]                # i k più alti
#
#   P3  dall'archivio al contratto
#         joblib.dump(E, PERCORSO_VETTORI)
#         contratto["modello_minilm"] = MODELLO_ST
#         contratto["mappa_dim_minilm"] = E.shape[1]
#         # ... joblib.dump(contratto, PERCORSO_CONTRATTO)
#         # in un altro processo: E = joblib.load(PERCORSO_VETTORI)


def demo() -> None:
    """Primo giro visibile. Non gira all'import. Stampa a passi, così sai
    sempre a che punto è (il load può richiedere 10-30 secondi)."""
    print("[1/9] Carico il modello (primo giro: download possibile)...")
    t0 = time.perf_counter()
    modello = carica_modello_frasi()
    t1 = time.perf_counter()
    print(f"  load: {t1 - t0:.1f} s")

    print("[2/9] Primo encode: shape e tempi")
    v = embedda("cedolino di marzo", modello)
    t2 = time.perf_counter()
    _ = embedda("cedolino di marzo", modello)
    t3 = time.perf_counter()
    print(f"  shape: {v.shape}  encode1: {t2 - t1:.3f}s  encode2: {t3 - t2:.3f}s")
    print(f"  max_seq_length: {modello.max_seq_length} pezzi | "
          f"dim: {modello.get_embedding_dimension()}")

    print("[3/9] Sottoparole e pooling")
    for parola in ("cedolino", "stipendio", "irpef", "emolumenti"):
        print(f"  {parola:11s} -> {sottoparole(parola, modello)}")
    tv = token_vettori("cedolino di marzo", modello)
    diff = float(np.abs(tv.mean(axis=0) - embedda("cedolino di marzo", modello)[0]).max())
    print(f"  token_vettori shape {tv.shape} | media dei pezzi vs encode: differenza max {diff:.1e}")

    print("[4/9] Quattro coseni misurati (multilingua): NON è una scala universale")
    coppie = [
        ("busta paga di marzo", "march payslip"),
        ("estratto conto bancario", "bank statement"),
        ("busta paga di marzo", "bank statement"),
        ("cedolino di marzo", "pizza margherita"),
    ]
    for a, b in coppie:
        x, y = embedda([a, b], modello)
        print(f"  {a!r} vs {b!r}: {float(coseno(x, y)):.3f}")

    print("[5/9] Due frasi e tre motori")
    print("  confronto parafrasi:", confronto_due_frasi(modello))
    print("  pagella (precision@3 su 8 query):", pagella(modello))
    mappa = carica_mappa()
    for q in ("remunerazione del lavoratore subordinato", "pizza margherita"):
        print(f"  {q!r}: copertura mappa {copertura_query(q, mappa):.2f} | "
              f"tfidf {vicini_tfidf(q)} | minilm {vicini_minilm(q, modello)}")

    print("[6/9] Trappole del senso")
    for a, b in (("sconto 10%", "sconto 90%"), ("contratto valido", "contratto non valido")):
        x, y = embedda([a, b], modello)
        print(f"  {a!r} vs {b!r}: {float(coseno(x, y)):.3f}")

    print("[7/9] Norma e prodotto scalare")
    grezzo = embedda("cedolino di marzo", modello)[0]
    pulito = embedda("cedolino di marzo", modello, normalizza=True)[0]
    print(f"  norma senza normalize: {np.linalg.norm(grezzo):.3f} | con normalize: {np.linalg.norm(pulito):.3f}")

    print("[8/9] Costi: batch, memoria, taglio")
    testi = carica_note()["testo"].tolist()
    t4 = time.perf_counter()
    E = embedda(testi, modello, normalizza=True)
    t5 = time.perf_counter()
    for t in testi:
        embedda(t, modello)
    t6 = time.perf_counter()
    print(f"  batch 30 note: {t5 - t4:.3f}s | 30 singole: {t6 - t5:.3f}s | "
          f"rapporto {(t6 - t5) / max(t5 - t4, 1e-9):.1f}x | memoria {E.nbytes / 1024:.0f} KB")
    lunga = "cedolino di marzo " + "lorem ipsum " * 120
    con_coda = lunga + " certificazione unica redditi dichiarazione"
    print("  rischio_troncamento(nota lunga):", rischio_troncamento(lunga, modello))
    coda = float(coseno(embedda(lunga, modello)[0], embedda(con_coda, modello)[0]))
    print(f"  coseno fra nota lunga e nota lunga + clausola in coda: {coda:.6f} (la coda è sparita)")

    print("[9/9] Disegno 2D delle note")
    tipi = carica_note()["tipo"].tolist()
    percorso = disegna_note(E, tipi)
    _, var = proietta_2d(E)
    print(f"  salvato: {percorso}  (2 assi spiegano il {var:.0%})")

    giocattolo = vettore_frase("cedolino di marzo", mappa)
    print(f"  mappa 02a: shape {giocattolo.shape} (DIM={DIM}) - NON confrontare con i {DIM_MINILM}")


# ==========================================================================
# QUIZ DI VERIFICA
# ==========================================================================
#
# V1. Prevedi: encode di una frase. Quante dimensioni ha il vettore MiniLM
#     di questo capitolo?
# V2. Vero o falso: il primo encode è lento perché ricalcola la SVD sui 30
#     documenti.
# V3. Trova l'errore: salvo i vettori MiniLM (384) e li confronto col coseno
#     ai vettori della mappa 02a (4).
# V4. Completa: se i vettori sono normalizzati a norma 1, il coseno è ____.
# V5. Un modello inglese su note italiane: crasha o peggiora in silenzio?
# V6. Pattern #6, tre bullet: guadagno / non guadagno / quando TF-IDF.
# V7. Type hint del vettore: np.ndarray, non np.array. Vero o falso?
# V8. 💬 Spiega con parole tue (niente codice): perché encode di una FRASE
#     intera non è la media dei punti-parola del 02a. (La teoria è in
#     Sezione 3: usala.)
# V9. Prevedi l'output: `embedda(["a", "b", "c"], modello).shape`?
#     E `embedda("a", modello).shape`? Perché il wrapper tratta la stringa
#     in modo speciale?
# V10. Nel contratto salvi `mappa_dim_minilm = 384` ma non il nome del
#     modello. Tre mesi dopo cambi modello (sempre 384 dimensioni) e la
#     ricerca peggiora. Cos'è successo, in due righe?
# V11. Una nota contiene 400 parole. Il modello vede 128 pezzi. La clausola
#     importante è a pagina 3 della nota. La ricerca la trova? Perché?
# V12. In 02a la mappa è stata costruita sui 30 documenti e valutata sugli
#     stessi. Con quale termine del M2 si chiama questo problema e perché
#     gonfia il voto?
# V13. 🔤 Completa le definizioni con il termine giusto (da questo capitolo):
#       a) "Il pezzo in cui il tokenizer spezza una parola" = ____
#       b) "La media che riduce n vettori a uno solo" = ____
#       c) "Dividere un vettore per la sua lunghezza" = ____
#       d) "Una lista di domande con risposte attese per confrontare
#           motori" = ____
#       e) "Quota delle risposte giuste nei primi k risultati" = ____
#
# TUE RISPOSTE:
#


# ==========================================================================
# ESERCIZI
# ==========================================================================
# Lettura: i tag ti dicono il tipo. ⭐ = APPROFONDIMENTO (facoltativi, per
# chi ha energia). Tutti gli altri sono nella DoD.
#
# E1  🔧 [REFACTORING] — Questo pezzo funziona ma è brutto: encode in un
#     ciclo Python, un vettore alla volta. Riscrivi con un solo encode
#     sulla lista. Stessa shape in uscita (n_doc, 384). Poi una riga:
#     perché la tua versione è anche più veloce, non solo più corta?
#     (La risposta è in Sezione 9, A.)
#     📋 PUNTI: 2        PUNTI CHE VEDO: ___
#
#         modello = carica_modello_frasi()
#         testi = pd.read_csv(PERCORSO_DATI)["testo"].tolist()
#         righe = []
#         for t in testi:
#             righe.append(embedda(t, modello)[0])
#         M = np.stack(righe)
#
# TUO CODICE:
#
#
# E2  🔍 [DEBUG] — Due bug, due traceback. Trova entrambi da solo.
#     (Il mentor non usa la scala progressiva.)
#
#     BUG A.
#         v_query = embedda("cedolino", modello)[0]
#         v_mappa = vettore_frase("cedolino", carica_mappa())
#         print(coseno(v_query, v_mappa))
#
#       ValueError: Shape di a: [...] != Shape di b: [...]
#
#     BUG B. Un collega dice: "ho incollato il contratto intero in una nota
#     e la ricerca non trova la clausola di recesso, che è in fondo. Ma
#     `encode` non dà errore!". Qual è il bug?
#
#     📋 PUNTI: 2        PUNTI CHE VEDO: ___
# TUA RISPOSTA (una frase per bug: qual è il bug, non come silenziare):
#
#
# E3  🧠 [RETRIEVAL] — A freddo, senza scorrere 02a: scrivi 4 righe che
#     caricano la mappa giocattolo e stampano il coseno di una frase con
#     se stessa. Deve essere ~1.
#
# TUO CODICE:
#
#
# E4  🔀 [INTERLEAVING] — Ripasso: TF-IDF del cap.01 + encode di ora.
#     Stessa query "documento per la dichiarazione dei redditi". Trova
#     indice e TIPO del documento col punteggio più alto per TF-IDF e per
#     MiniLM. Sono lo stesso? Due indici, due tipi, una riga di commento:
#     chi ha capito cosa cercavi? (Hai le funzioni `vicini_*`: usarle va
#     bene, capirle è il punto.)
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
#
# TUO CODICE:
#
#
# E5  🎯 [COLLOQUIO] — «Cos'è un embedding?» in 4-6 righe, tono da
#     colloquio (niente emoji). Deve entrare: vettore, vicinanza = senso
#     simile, non è un conteggio di parole. Opzionale: differenza fra la
#     mappa fatta in casa del 02a e un modello preaddestrato.
#     📋 PUNTI: 3 (obbligatori) + 1 opzionale
#     PUNTI CHE VEDO: ___
#
# TUA RISPOSTA:
#
#
# E6  La funzione che manca alla torre: `cerca_note(query, E, testi, modello,
#     k=3)` che restituisce i k INDICI più simili alla query usando i
#     vettori GIÀ calcolati (E), senza rifare encode dei documenti.
#
#         def cerca_note(query: str, E: np.ndarray, testi: list[str],
#                        modello, k: int = 3) -> list[int]:
#
#     Vincoli: encode dei documenti VIETATO dentro la funzione (E arriva da
#     fuori); la query sì, va embeddata; usa il trucco della Sezione 8.
#     Test: cerca_note("rimborso spese", E, testi, modello). Guarda tu
#     stesso se le note trovate c'entrano.
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
#
# TUO CODICE:
#
#
# E7  ⌨️ [PIPELINE A MEMORIA] — A libro CHIUSO (non scorrere le sezioni).
#     Scrivi una sola funzione `pipeline_ricerca(query, k=3)` che fa P1 + P2
#     (vedi "LE TRE PIPELINE" in Sezione 11) e restituisce una lista di
#     dizionari, uno per risultato:
#         {"indice": int, "tipo": str, "punteggio": float, "anteprima": str}
#     dove "anteprima" è il testo della nota tagliato ai primi 60 caratteri.
#     Punti obbligatori, nell'ordine:
#       1. carica le note dal CSV (carica_note)
#       2. carica il modello
#       3. embedda le note in batch, normalizzate
#       4. embedda la query, normalizzata, prendi la riga [0]
#       5. punteggi = prodotto scalare
#       6. indici dei k più alti
#       7. costruisci i dizionari
#     📋 PUNTI: 7        PUNTI CHE VEDO: ___
#     Test: pipeline_ricerca("elenco movimenti della banca")[0]["tipo"]
#     deve essere "estratto_conto". Stampa il risultato in modo leggibile.
#
# TUO CODICE:
#
#
# E8  🌐 [CROSS-CAPITOLO] — La mini-torre. Unisci TRE capitoli in una
#     funzione sola: `cartellino(query, modello, E, pipe, mappa, k=3)`.
#
#     🔁 RIPASSO PROPOSITIVO — cap.01 (classificatore del tipo)
#     `prepara_modello(PERCORSO_DATI)` restituisce un dizionario con la
#     chiave "pipe": una Pipeline scikit-learn (TF-IDF + regressione
#     logistica). `classifica_tipo_documento(query, pipe)` restituisce
#     {"tipo": ..., "prob_tipo_doc_testuale": ..., "parole_decisive": [...]}.
#     Dice di che TIPO è una nota. Già scritto da te nel cap.01.
#
#     🔁 RIPASSO PROPOSITIVO — 02a (mappa e copertura)
#     `carica_mappa()` e `copertura_query(query, mappa)` dicono quante
#     parole della query la mappa conosce.
#
#     La funzione restituisce un dizionario con le chiavi:
#         "tipo_classificatore"   (dal cap.01)
#         "prob_classificatore"   (dal cap.01)
#         "copertura_mappa"       (dal 02a, 0.0-1.0)
#         "vicini"                (da 02b: lista [(indice, punteggio)] top-k)
#         "punteggio_max"         (il punteggio del primo vicino: quanto è
#                                  "sicura" la ricerca; 0.0 se non c'è)
#         "tipo_vicini"           (il tipo PIÙ FREQUENTE fra i k vicini,
#                                  usa collections.Counter)
#         "allineato"             (True se tipo_classificatore == tipo_vicini)
#     📋 PUNTI: 7        PUNTI CHE VEDO: ___
#     Poi PROVA su 4 query: una del BENCHMARK, "pizza margherita", una con
#     CF e IBAN, e "remunerazione del lavoratore subordinato".
#     Una riga finale per ogni query dove allineato è False: di chi ti
#     fidi, e perché? Guarda `prob_classificatore` e `punteggio_max`: sono
#     i due "livelli di sicurezza". (Domanda sul lavoro: nella torre, cosa
#     fai se i due segnali discordano?)
#
# TUO CODICE:
# TUA RISPOSTA:
#
#
# E9  ⭐ 📚 [LIBRO RIFORMULATO] — Il tira-e-spingi in 2D. Ispirato
#     all'apprendimento contrastivo di [ALAMMAR cap. 2 e 10], adattato al
#     nostro dominio (Sezione 4). Non devi aprire il libro: la teoria è
#     sopra.
#
#     Prendi quattro frasi con una posizione 2D casuale (seme fisso):
#         0 "cedolino di marzo"       1 "busta paga di marzo"
#         2 "estratto conto"          3 "saldo del conto"
#     Coppie POSITIVE (vicine):   (0,1) e (2,3)
#     Coppie NEGATIVE (lontane):  (0,2) (0,3) (1,2) (1,3)
#
#     Scrivi `passo_contrastivo(a, b, vicini, passo=0.1, margine=2.0)`:
#       - se vicini: sposta a e b l'uno verso l'altro (ognuno di `passo`
#         della distanza fra loro)
#       - se NON vicini E la distanza è SOTTO il margine: allontanali
#       - se NON vicini E la distanza è GIÀ sopra il margine: non fare
#         nulla (se spingessi sempre, scapperebbero all'infinito)
#       - restituisce (a_nuovo, b_nuovo)
#     Poi un ciclo di 100 giri su tutte le coppie e due righe di stampa:
#     distanze delle coppie positive PRIMA e DOPO, idem per le negative.
#     📋 PUNTI: 4        PUNTI CHE VEDO: ___
#     Domanda finale (una riga): perché serve il margine?
#
# TUO CODICE:
# TUA RISPOSTA:
#
#
# E10 🔤 [GLOSSARIO IN CODICE] — Il lessico nuovo, scritto a mano. Sei
#     funzioni minuscole (1-3 righe l'una). Il nome della funzione È il
#     termine: lo impari scrivendolo.
#
#         pooling_medio(vettori_token)        -> media sulle righe, shape (384,)
#         normalizza_righe(M)                 -> ogni riga divisa per la sua norma
#         coseno_batch(q, E)                  -> punteggi di E (n, d) contro q (d,)
#                                                supponendo E e q normalizzati
#         precisione_a_k(indici, tipi, atteso) -> quota di indici il cui tipo è
#                                                `atteso`, dentro la lista data
#         n_sottoparole(frase, modello)       -> quanti pezzi (senza speciali)
#         ha_troncamento(n_pezzi, limite)     -> True se n_pezzi + 2 > limite
#
#     📋 PUNTI: 6        PUNTI CHE VEDO: ___
#     Verifica con questi assert (devono passare in silenzio):
#         M = np.array([[3.0, 4.0], [0.0, 5.0]])
#         assert np.allclose(normalizza_righe(M), [[0.6, 0.8], [0.0, 1.0]])
#         assert np.allclose(pooling_medio(np.array([[1.0, 3.0], [3.0, 5.0]])), [2.0, 4.0])
#         assert np.allclose(coseno_batch(np.array([1.0, 0.0]), np.array([[1.0, 0.0], [0.0, 1.0]])), [1.0, 0.0])
#         assert precisione_a_k([0, 1, 2], ["cu", "cu", "busta_paga"], "cu") == 2 / 3
#         assert ha_troncamento(127, 128) is True and ha_troncamento(126, 128) is False
#
# TUO CODICE:
#
#
# E11 ⭐ 🛡️ [GUARDRAIL] — Nel contratto la dimensione e il nome del modello
#     servono a QUALCOSA: a impedire che qualcuno confronti vettori che non
#     si possono confrontare. Scrivi `verifica_compatibilita(E, contratto,
#     nome_modello)` che:
#       (a) alza ValueError se E.shape[1] != contratto["mappa_dim_minilm"]
#       (b) alza ValueError se contratto["modello_minilm"] != nome_modello
#       (c) non fa nulla e non restituisce niente se tutto torna
#     Messaggi di errore che DICONO cosa non torna (valori trovati e
#     attesi). Test con tre contratti fasulli: giusto, dimensione sbagliata,
#     nome sbagliato.
#     📋 PUNTI: 3        PUNTI CHE VEDO: ___
#
# TUO CODICE:
#
#


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE
# ==========================================================================
# Componente: ramo testuale della torre — primi vettori "veri" delle note.
#
# 🔁 RIPASSO PROPOSITIVO — modulo riusabile del 02a
# `testo_utils.py` è la tua libreria: import silenzioso, nomi stabili,
# asserzioni nel blocco `__main__`. Nel 02a hai scelto di tenere il codice
# di rilascio FUORI dalla libreria. Qui fai la stessa scelta per le
# dipendenze: `embed_utils.py` è un modulo NUOVO e `testo_utils.py` resta
# com'è (senza sentence-transformers).
#
# Deliverable: file NUOVO `modulo_04_nlp/embed_utils.py`. Importa da
# `testo_utils` solo ciò che esiste già (PERCORSO_DATI, PERCORSO_CONTRATTO)
# e RISCRIVE le due funzioni che gli servono (`carica_modello_frasi`,
# `embedda`). Una libreria non importa mai un file di esercizi: oltre alla
# ragione di stile, `02b_embeddings_pratica` comincia con una cifra e non è
# nemmeno importabile con un normale `import`.
#
#   [ ] T1 — `embedda_note(percorso, modello) -> np.ndarray`: encode batch
#            delle 30 note, normalizzati, shape (n_doc, 384). Funzioni
#            `salva_vettori(E)` e `carica_vettori()` con joblib su
#            `dati/mappe/note_minilm.pkl`. Poi load e assert sulla shape:
#            i vettori si ricaricano SENZA rifare encode.
#   [ ] T2 — Contratto: funzione `aggiorna_contratto_minilm(E, nome_modello,
#            max_seq_length)` che CARICA il contratto esistente, aggiunge le
#            chiavi NUOVE `modello_minilm`, `mappa_dim_minilm`,
#            `minilm_max_seq_length`, `minilm_n_note` e lo risalva. NON
#            sovrascrivere `mappa_dim = 4`. Una riga di commento: perché
#            384 e 4 non si confrontano e perché il nome del modello va
#            salvato.
#   [ ] T3 — Porta `cerca_note` (E6) in `embed_utils.py` e aggiungi nel
#            blocco `__main__` tre assert silenziosi nello stile del 02a:
#            (a) la query uguale al testo della nota 5 la trova in cima;
#            (b) `E.shape[1] == DIM_MINILM` e le norme sono ~1;
#            (c) il contratto ha tutte le chiavi nuove.
#   [ ] T4 — Porta `rischio_troncamento` come guardia: `embedda_note`
#            stampa un avviso con gli indici delle note troncate (nessuna,
#            sulle 30 di oggi: verificalo).
#   [ ] T5 — Due righe di stampa (non un saggio) per il diario tecnico della
#            torre: tempo di encode batch delle 30 note, memoria in KB.
#            Serviranno nel M6 per decidere dove tenere i vettori.
#
# DoD: `carica_vettori()` restituisce i 30 vettori senza rifare encode;
# `v.shape[1] == 384`; il contratto ha ENTRAMBE le chiavi (vecchie e nuove);
# gli assert passano in silenzio; `testo_utils.py` non è stato toccato.
# Non mischiare questi vettori con `mappa.pkl` del 02a.


# ==========================================================================
# DEFINITION OF DONE
# ==========================================================================
# [ ] Quiz ingresso (Q1-Q8) e verifica (V1-V13, V8 Feynman compreso)
# [ ] Micro #6 e Mini 0.1
# [ ] Mini 1.1-1.2, 2.1-2.2, 3.1-3.2, 4.1, 5.1-5.2, 6.1-6.4, 7.1-7.2,
#     8.1-8.2, 9.1-9.2, 10.1, 11.1
# [ ] E1-E8, E10
# [ ] E9 e E11 (⭐ facoltativi)
# [ ] T1-T5 progetto
# [ ] demo() gira e i numeri tornano con quelli che vedi tu
# [ ] Per ogni consegna a più punti hai scritto PUNTI CHE VEDO prima di
#     rispondere (antidoto Pattern #6)


# ==========================================================================
# SOLUZIONI — dopo il tentativo
# ==========================================================================
# Q1  costruisci_mappa = fit; vettore_frase = transform.
# Q2  Falso. Forma diversa; anche a parità di n, assi SVD diversi.
# Q3  Zeri; coseno 0.0 (guardia).
# Q4  Ricostruire cambia lo spazio e costa. Load = stesso spazio.
# Q5  No.
# Q6  (a) parafrasi; (b) cifre/IBAN/negazione/nome della dimensione;
#     (c) CF o IBAN.
# Q7  np.ndarray.
# Q8  No: MIN_CONTEGGIO = 2, una parola vista una volta non entra.
#
# Mini 1.1 (a) (1, 384); (b) circa 0.03 s (dipende dal PC).
# Mini 1.2
#         _CACHE = {}
#         def modello_una_volta(nome=MODELLO_ST):
#             if nome not in _CACHE:
#                 _CACHE[nome] = carica_modello_frasi(nome)
#             return _CACHE[nome]
#         a = modello_una_volta(); b = modello_una_volta(); assert a is b
#     `is` = stesso oggetto in memoria. `==` confronterebbe il contenuto (e
#     per un modello non è definito in modo utile).
# Mini 2.1 cedolino 3, stipendio 2, emolumenti 3, xyzzyq: spezzata comunque
#     in più pezzi, nessun errore.
# Mini 2.2 Perché ogni parola, anche mai vista, ha dei pezzi noti: OOV non
#     esiste più come caso a parte.
# Mini 3.1 (7, 384) e (n, 384) con n molto più grande; poi sempre (1, 384).
#     La differenza è assorbita dal pooling (la media sulle righe).
# Mini 3.2 np.allclose(token_vettori(f, m).mean(axis=0), embedda(f, m)[0])
#     -> True.
# Mini 4.1 a) 0.69 (medio-alto); b) 0.74 (medio-alto); c) 0.09 (basso).
#     (b) è PIÙ ALTO di (a): nello stesso dominio (soldi) frasi su argomenti
#     diversi restano vicine, mentre una traduzione esatta può scendere. Il
#     coseno non ha una scala universale: si confrontano i candidati per la
#     STESSA query (la classifica), e le soglie si calibrano sui tuoi dati.
# Mini 5.1 {"dimensioni": 384, "max_seq_length": 128, "parametri_milioni":
#     ~117.7, "pezzi_vocabolario": 250002}. (La tabella dei pezzi pesa ~96M
#     dei 118M: il vocabolario è la parte più grossa del modello.)
# Mini 5.2 (1) peggioramento silenzioso; (2) coppia di parafrasi italiane
#     del 02a, confronta i coseni dei due modelli.
# Mini 6.1 TF-IDF 0.0; MiniLM ~0.55. No, MiniLM non sbaglia. Il valore
#     assoluto non è confrontabile fra motori: la mappa 02a ha solo 4 assi
#     e viene dagli stessi documenti, quindi quasi tutte le coppie escono
#     alte. Conta la CLASSIFICA per la stessa query: "cedolino di marzo" vs
#     "prospetto paga di aprile" 0.55, contro 0.17-0.21 per frasi che non
#     c'entrano. Un distacco netto. Un coseno alto non è automaticamente
#     "meglio".
# Mini 6.2 TF-IDF: primo risultato è 'altro' (indice 17); MiniLM: tre CU
#     (6, 7, 9). MiniLM ha capito che cercavi un documento fiscale.
# Mini 6.3 Copertura: 0.0, ~0.67, 0.0 (le cifre dipendono dal tuo mappa.pkl).
#     La prima ha tutte parole fuori vocabolario: TF-IDF e mappa non hanno
#     nulla da confrontare; MiniLM scompone in sottoparole note.
# Mini 6.4 tfidf 0.62, mappa 0.83, minilm 0.75 (circa). Il più forte è
#     il vantaggio di casa: lo verifichi costruendo la mappa su 20
#     documenti e valutando sui 10 che non ha visto.
# Mini 7.2 a) alto (0.83); b) alto (0.78). La negazione è più pericolosa:
#     "valido" e "non valido" sono opposte per il lavoro, e l'errore non si
#     vede nei numeri.
# Mini 8.1 ~3.7 e 1.0.
# Mini 8.2 differenza ~1e-8. Perché le norme valgono 1: il denominatore del
#     coseno diventa 1.
# Mini 9.1 batch ~0.4 s, singole ~1 s, rapporto ~2.5 (dipende dal PC).
# Mini 9.2 (a) 0 su 30 (la più lunga ha 38 pezzi); (b) n_pezzi circa 700,
#     troncato True; (c) il modello vede solo i primi ~126 pezzi: il resto
#     non esiste per la ricerca.
# Mini 10.1 (a) ~0.27; (b) CU è il più sparso (std ~0.30), busta paga il
#     meno (~0.19); (c) indice a tua scelta.
# Mini 11.1  contratto["modello_minilm"] = MODELLO_ST
#            contratto["mappa_dim_minilm"] = E.shape[1]
#            contratto["minilm_max_seq_length"] = modello.max_seq_length
#     Non basta la dimensione perché due modelli diversi possono avere 384
#     assi: la dimensione dice la FORMA, il nome del modello dice lo SPAZIO.
#
# V1  384.
# V2  Falso: è il download / il load dei pesi.
# V3  384 vs 4: il coseno richiede la stessa shape.
# V4  il prodotto scalare (dot / @).
# V5  Peggiora in silenzio.
# V7  Vero.
# V8  encode fa parlare i vettori dei pezzi tra loro (contesto) PRIMA della
#     media. La media 02a somma punti già fissati, commutativa: l'ordine
#     sparisce del tutto.
# V9  (3, 384) e (1, 384): la stringa singola viene messa in lista, così
#     l'uscita è sempre una matrice e chi chiama non gestisce due casi.
# V10 Stessa forma (384) ma spazio diverso: i vettori vecchi e quelli nuovi
#     non sono confrontabili. Il contratto deve annotare il modello, non
#     solo la dimensione.
# V11 No: il modello taglia in silenzio a 128 pezzi. Una clausola dopo il
#     taglio non influenza il vettore. Serve chunking (M6).
# V12 Data leakage. Valutare sugli stessi dati su cui ha imparato gonfia il
#     voto: il modello conosce già le risposte.
# V13 a) sottoparola (subword); b) pooling; c) normalizzare; d) benchmark;
#     e) precision@k.
#
# E1  M = embedda(testi, modello)  # già accetta una lista; un solo costo
#     fisso invece di 30 (Sezione 9, A).
# E2  A) Stai confrontando 384 con 4: due spazi diversi, il coseno richiede
#     la stessa shape.  B) Il troncamento: la clausola in fondo è oltre i
#     128 pezzi, non è mai arrivata al modello.
# E3  mappa = carica_mappa(); v = vettore_frase("cedolino di marzo", mappa);
#     print(coseno(v, v))
# E4  vicini_tfidf(...)[0] punta a un 'altro'; vicini_minilm(...)[0] a un
#     CU. MiniLM ha capito che la query parla di dichiarazione dei redditi.
# E6  def cerca_note(query, E, testi, modello, k=3):
#         q = embedda(query, modello, normalizza=True)[0]
#         punteggi = E @ q
#         return [int(i) for i in np.argsort(punteggi)[::-1][:k]]
# E7  def pipeline_ricerca(query, k=3):
#         dati = carica_note()
#         testi, tipi = dati["testo"].tolist(), dati["tipo"].tolist()
#         modello = carica_modello_frasi()
#         E = embedda(testi, modello, normalizza=True)
#         q = embedda(query, modello, normalizza=True)[0]
#         punteggi = E @ q
#         top = np.argsort(punteggi)[::-1][:k]
#         return [{"indice": int(i), "tipo": tipi[i],
#                  "punteggio": round(float(punteggi[i]), 3),
#                  "anteprima": testi[i][:60]} for i in top]
# E8  def cartellino(query, modello, E, pipe, mappa, k=3):
#         cl = classifica_tipo_documento(query, pipe)
#         vicini = vicini_minilm(query, modello, k, E)
#         tipi = carica_note()["tipo"].tolist()
#         tipo_vicini = Counter(tipi[i] for i, _ in vicini).most_common(1)[0][0]
#         return {
#             "tipo_classificatore": cl["tipo"],
#             "prob_classificatore": round(cl["prob_tipo_doc_testuale"], 3),
#             "copertura_mappa": round(copertura_query(query, mappa), 2),
#             "vicini": vicini,
#             "punteggio_max": vicini[0][1] if vicini else 0.0,
#             "tipo_vicini": tipo_vicini,
#             "allineato": cl["tipo"] == tipo_vicini,
#         }
#     Setup: pipe = prepara_modello(str(PERCORSO_DATI))["pipe"]
#     Esiti misurati sulle 4 query (il classificatore è insicuro quasi
#     ovunque, perché ha imparato su 24 note e 4 classi):
#       - "documento per la dichiarazione dei redditi": classificatore "altro"
#         (prob 0.37) vs vicini "cu" (punteggio ~0.7). NON allineato. Qui di
#         chi ti fidi? Della ricerca: ha il punteggio alto e il classificatore
#         è sotto 0.4 con 4 classi, cioè quasi un "non so".
#       - "pizza margherita": classificatore "altro" (0.32) vs vicini
#         "busta_paga" ma con punteggio_max 0.16. NON allineato, ma qui ha
#         ragione il classificatore: i vicini sono rumore (punteggio bassissimo).
#       - Query con CF e IBAN: allineato su "busta_paga": entrambi i segnali
#         concordano e le probabilità sono medie (0.58). Qui sta il caso in
#         cui il match esatto (CF, IBAN) dovrebbe fare la parte principale.
#       - "remunerazione del lavoratore subordinato": copertura 0.0 per la
#         mappa; classificatore "altro" (0.32), vicini "cu". Nessuno dei due
#         è sicuro: serve l'operatore.
#     Risposta sul lavoro: se discordano non decide nessuno dei due in
#     automatico: la nota va all'operatore con entrambi i segnali visibili
#     ("il classificatore dice X con 0.37, la ricerca punta a Y con 0.70").
#     La discordanza è essa stessa un'informazione, e i due livelli di
#     sicurezza (prob e punteggio) ti dicono quale segnale pesa di più.
# E9  def passo_contrastivo(a, b, vicini, passo=0.1, margine=2.0):
#         d = b - a
#         if vicini:
#             return a + passo * d, b - passo * d
#         if np.linalg.norm(d) < margine:
#             return a - passo * d, b + passo * d
#         return a, b
#     Risultato atteso (seme 0, 100 giri): le due coppie positive scendono a
#     distanza ~0.0 (si sono sovrapposte) e tutte le negative si fermano a
#     ~2.08, appena sopra il margine 2.0. Serve il margine perché senza di
#     esso le coppie negative verrebbero spinte sempre più lontano,
#     all'infinito: basta che siano "abbastanza" distanti.
#     Limite del giocattolo: in un modello vero le coppie positive non
#     collassano in un punto solo, perché altre coppie le tengono distinte.
# E10 def pooling_medio(v): return v.mean(axis=0)
#     def normalizza_righe(M): return M / np.linalg.norm(M, axis=1, keepdims=True)
#     def coseno_batch(q, E): return E @ q
#     def precisione_a_k(indici, tipi, atteso):
#         return sum(1 for i in indici if tipi[i] == atteso) / len(indici)
#     def n_sottoparole(frase, modello): return len(modello.tokenizer.tokenize(frase))
#     def ha_troncamento(n_pezzi, limite): return n_pezzi + 2 > limite
# E11 def verifica_compatibilita(E, contratto, nome_modello):
#         if E.shape[1] != contratto["mappa_dim_minilm"]:
#             raise ValueError(f"dimensione {E.shape[1]} != contratto {contratto['mappa_dim_minilm']}")
#         if contratto["modello_minilm"] != nome_modello:
#             raise ValueError(f"modello {nome_modello!r} != contratto {contratto['modello_minilm']!r}")
# T2  Commento: dim diversa -> forma; modelli diversi -> assi diversi; il
#     nome del modello identifica lo spazio, la dimensione no.


# if __name__ == "__main__":
#     try:
#         demo()
#     except ImportError:
#         print(
#             "Installa prima: pip install sentence-transformers\n"
#             "Poi rilancia. I quiz sopra si compilano anche senza."
#         )
