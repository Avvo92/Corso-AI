"""
============================================================================
MODULO 4 (NLP, Embeddings & Transformers) — CAPITOLO 02a
Embeddings: le coordinate del significato
============================================================================

DA DOVE VIENI
-------------
Nel cap.01 ogni documento diventava una scheda: una casella per parola, un
conteggio dentro. Ha funzionato: il classificatore indovina il tipo.
Ma la Sez. 5 si chiudeva con tre buchi, e questo capitolo è la risposta.

  1. Sinonimi. "cedolino" e "prospetto paga" sono due caselle diverse.
     Per il coseno del cap.01 due frasi senza parole in comune valgono 0,
     anche se dicono la stessa identica cosa.
  2. Ordine. "il netto supera il lordo" e il contrario danno lo stesso vettore.
  3. Parola mai vista. Non è nel vocabolario: viene scartata, in silenzio.

QUESTO CAPITOLO NON CHIUDE TUTTI E TRE. Chiude il primo, e in modo
misurabile: alla fine avrai un numero, non una promessa.
Il secondo resta aperto, e te lo farò toccare con mano in Sez. 5: anche con
le coordinate del significato, due frasi invertite restano identiche. Si
chiude al cap.04. Il terzo resta aperto anche lui, e lo vedrai in faccia.

COSA NON SERVE
--------------
Nessuna installazione. Niente `sentence-transformers`, niente download.
Solo numpy, pandas, matplotlib e il tuo `testo_utils.py` del cap.01.
Il modello vero arriva in **02b**, e si installa prima di aprirlo, non durante.

L'ANALOGIA
----------
Un embedding è un INDIRIZZO. Non "via Roma 5": una manciata di numeri, come
le coordinate di una mappa. Parole vicine sulla mappa si somigliano, parole
lontane no. La differenza con la scheda del cap.01 è tutta qui: la scheda
chiede «c'è questa parola, sì o no?», la mappa chiede «dove sta il senso?».

Il ponte con quello che già fai:
  - in JavaScript, invece di `{ cedolino: 1, netto: 1 }` (un contatore per
    parola) avresti `[0.42, -1.07, 0.88, 0.15]` (un array di numeri);
  - in PHP/Laravel, invece di una tabella di tag per documento avresti una
    colonna di tipo vettore. In Postgres si chiama **pgvector** (un tipo di
    colonna che contiene una lista di numeri e sa dirti chi le somiglia).
    È esattamente la tecnologia che userai nel M6 per la torre di controllo.

LA DIFFERENZA CHE PAGHI SUL LAVORO
----------------------------------
Nella torre di controllo scriverai una nota: «chiedere il prospetto paga al
cliente». Fra due mesi cerchi «cedolino». Con la scheda del cap.01 quella
nota NON esce: nessuna parola in comune. Con la mappa esce. È tutta qui la
ricerca semantica, ed è il mattone di RAG (Retrieval-Augmented Generation:
prima si cercano i pezzi giusti, poi il modello risponde leggendoli).

📚 LETTURA PARALLELA — [ALAMMAR, Hands-On Large Language Models, cap. 2]
Il libro introduce i token e gli embedding con la stessa sequenza: prima le
parole come identificativi, poi come vettori densi. Preso da lì: l'idea di
"parola come compagnia che frequenta" e il fatto che le dimensioni non hanno
un nome leggibile. Scartato per ora: word2vec passo-passo e i modelli
pre-addestrati, che stanno in 02b. Le figure non si copiano: la mappa di
questo file la calcoli tu, sui tuoi 30 documenti.

Hardware: CPU. Il file gira in meno di due secondi.
"""

from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd

from testo_utils import tokenizza, PERCORSO_DATI


# Parametri della mappa. Spiegati nella Sez. 2 e nella Sez. 6.
MIN_CONTEGGIO = 2   # una parola vista una volta sola non ha "compagnia" osservabile
DIM = 4             # quanti numeri per parola nelle misure
DIM_DISEGNO = 2     # il foglio ha due assi: solo per il grafico


# ==========================================================================
# QUIZ D'INGRESSO — sul cap.01. Rispondi prima di scendere.
# ==========================================================================
#
# Q1. Due frasi con le stesse parole, ordine invertito. Il coseno dei loro
#     Bag of Words quanto fa, e perché?
# Q2. Vero o falso: in produzione posso rifare `fit_transform` sul testo in
#     arrivo, tanto il modello si adatta.
# Q3. Trova l'errore, in una frase: `joblib` ha salvato solo il
#     classificatore. A marzo si crea un `TfidfVectorizer` nuovo e si chiama
#     `fit_transform` sul testo in arrivo.
# Q4. Una parola mai vista nel vocabolario cosa diventa nel vettore?
# Q5. Completa: sul vettorizzatore già addestrato, in produzione si chiama
#     _______ e non `fit_transform`.
# Q6. Il ramo testuale del cap.01 risponde a quale domanda: il tipo del
#     documento, oppure «è alterato?».
# Q7. Nel cap.01 hai scritto una funzione che divide per le norme. Cosa
#     restituisce se uno dei due vettori è tutto zeri, e perché quella
#     scelta?
#
# TUE RISPOSTE:
# Q1. coseno = 1 -> perchè producona la stessa identica BoW
# Q2. Falso -> il fit si fa sul train, e poi la pipe (tfidf e modello) va usata in produzione senza riaddestrarla.
# Q3. E' simile all'errore dell M3: come nel contratto di inferenza è necessario sapere la mean e la std con cui ha normalizzato il modello in  train, qui il tfidfvectorizer deve trasformare le query nello stesso modo che ha usato nel train: altrimenti, il vocabolario e idf sarebbero diversi e se dessimo i dati in input al modello, in produzione sbaglierebbe.
# Q4. Nulla, viene scartata silenziosamente e non finisce nel vettore.
# Q5. transform
# Q6. il tipo di documento
# Q7. restituisce 0.0, perchè coseno 0 significa "non c'è una somiglianza ne una differenza", in pratica equivale a dire non ho capito la domanda.


# ==========================================================================
# 🔁 RIPASSO PROPOSITIVO — cosa ti porti dal cap.01 (serve tutto, qui sotto)
# ==========================================================================
# 1) Bag of Words = la scheda. Una casella per parola del vocabolario, dentro
#    quante volte compare. Documento lungo = scheda con tanti zeri.
#
# 2) TF-IDF = il conteggio pesato. Una parola che sta in TUTTI i documenti
#    non distingue niente, quindi vale poco. Una parola rara pesa di più.
#    Tieni a mente questo meccanismo: nella Sez. 2 lo rifarai sulle COPPIE
#    di parole invece che sulle singole, ed è la stessa identica idea.
#
# 3) Coseno = quanto due frecce puntano nella stessa direzione, a prescindere
#    da quanto sono lunghe. 1 = stessa direzione, 0 = indipendenti.
#    La norma è la LUNGHEZZA (radice della somma dei quadrati), non la somma:
#    [1, -1] somma zero ma è lungo radice di 2.
#    Se un vettore è tutto zeri la direzione non esiste e la tua funzione
#    restituisce 0.0 invece di dividere per zero.
#    (La formula la riscrivi tu dalla memoria nella Sez. 3: non la rileggere.)
#
# 4) `fit` impara, `transform` applica. Il vocabolario si impara una volta
#    sola, sul corpus di addestramento. Vale anche per la mappa di oggi.


# ==========================================================================
# 🔁 RINFORZO MIRATO — lacuna #62 (TODO 7 del cap.01, 05/10, esame 8.5)
# ==========================================================================
# Avevi misurato giusto: due frasi invertite danno coseno 1. Poi avevi
# scritto che serve «un modello che distingue il significato».
# Il limite che quelle due frasi isolano non è il significato in generale:
# è l'ORDINE. La scheda non sa chi viene prima.
#
# La prova che "significato" non basta la vedrai in Sez. 5 di questo file:
# lì ogni parola avrà un significato suo (le coordinate), le metteremo
# insieme facendo la media, e le due frasi invertite torneranno IDENTICHE.
# Un sacco di significati è sempre un sacco.
#
# 🧩 Micro #62 — In una riga: cosa deve saper fare un modello per dare un
#     risultato DIVERSO alle due frasi invertite?
# TUA RISPOSTA: Deve saper distinguere l'ordine


# ==========================================================================
# SEZIONE 1 — Sparso contro denso
# ==========================================================================
# Nel cap.01, con 30 documenti, il vocabolario era di poche centinaia di
# parole. Ogni documento accendeva una decina di caselle e lasciava tutte le
# altre a zero. Quella matrice si chiama SPARSA: quasi tutta vuota. Infatti
# scikit-learn non la salva per intero, usa una `csr_matrix` che tiene solo
# i valori diversi da zero.
#
# Su un archivio vero il problema esplode: 20.000 parole di vocabolario
# vogliono dire 20.000 caselle per documento, di cui 19.980 a zero.
#
# L'embedding è l'opposto: poche caselle, quasi tutte piene. Si dice DENSO.
#
#   scheda (sparso)   cedolino → [0, 0, 1, 0, 0, ..., 0]   20.000 caselle
#   mappa  (denso)    cedolino → [0.42, -1.07, 0.88, 0.15]  4 numeri
#
# Il punto non è il risparmio di spazio. È che nella scheda ogni casella è
# una parola diversa, quindi due parole diverse non si toccano MAI: caselle
# diverse, prodotto zero. Nella mappa due parole diverse possono finire
# vicine, perché le caselle non sono le parole: sono direzioni condivise.
#
# 🧩 Mini 1.1 — Hai 20.000 parole di vocabolario. Un documento ne contiene 30.
#     Quante caselle sono a zero nella sua scheda? E in un embedding da 384
#     numeri, quante caselle sono a zero? Due numeri, una riga.
# TUA RISPOSTA:
# scheda -> 19.970; embedding -> 0


# ==========================================================================
# SEZIONE 2 — Il meccanismo: una parola è la compagnia che frequenta
# ==========================================================================
# Fin qui è un'immagine. Adesso le coordinate le CALCOLI, dai tuoi documenti.
#
# L'idea si chiama ipotesi distribuzionale e sta in una frase:
#
#     parole che compaiono negli stessi contesti hanno significati simili.
#
# Non serve che un umano decida «cedolino è una busta paga». Basta notare che
# "cedolino" si presenta sempre in compagnia di "paga", "lordo", "netto",
# "IRPEF" — e che "saldo" si presenta in compagnia di "conto", "accredito",
# "finale". Due compagnie diverse, due zone diverse della mappa.
#
# I QUATTRO PASSI (li esegue il codice qui sotto, uno per funzione)
#
#   Passo 1 — Vocabolario.
#     Tokenizzi i 30 documenti con la TUA `tokenizza` del cap.01 (stesse
#     regole, stessi segnaposto <importo> e <data>) e tieni le parole viste
#     almeno due volte. Una parola vista una volta sola non ha compagnia
#     osservabile: sarebbe solo rumore.
#
#   Passo 2 — Chi frequenta chi.
#     Costruisci una tabella quadrata: righe = parole, colonne = parole.
#     Nella cella (riga "cedolino", colonna "netto") scrivi in quanti
#     documenti le due parole compaiono INSIEME. La diagonale resta a zero:
#     non ci interessa che una parola frequenti se stessa.
#
#   Passo 3 — Pesa i conteggi.
#     Qui torna esattamente l'idea dell'IDF che hai ripassato sopra.
#     "totale" sta ovunque: incontrarla accanto a "cedolino" non è una
#     notizia. "IRPEF" sta in poche righe: incontrarla accanto a "cedolino"
#     è una notizia grossa. Quindi non conta il conteggio grezzo, conta
#     quanto quell'incontro è PIÙ FREQUENTE del previsto se le due parole
#     fossero indipendenti. Il nome tecnico è PPMI (Positive Pointwise Mutual
#     Information: informazione reciproca punto per punto, tenendo solo i
#     valori positivi). I valori negativi — «queste due si evitano» — su un
#     corpus piccolo sono rumore e si azzerano.
#
#   Passo 4 — Schiaccia.
#     Dopo il passo 3 ogni parola è ancora descritta da 49 numeri (uno per
#     ogni altra parola). Troppi e ridondanti: "netto" e "lordo" dicono quasi
#     la stessa cosa. La SVD (Singular Value Decomposition: scomposizione in
#     valori singolari) trova le poche direzioni che spiegano la maggior
#     parte della tabella e butta il resto. Da 49 numeri a 4.
#
#     In una riga: la SVD è un compressore. Come un JPEG tiene l'immagine
#     e butta i dettagli che l'occhio non nota, la SVD tiene le direzioni
#     grosse e butta quelle piccole. Non devi saperla derivare: `numpy` la
#     calcola con una chiamata, e nel M8 la ritroverai sotto il nome di LoRA.
#
# ATTENZIONE, ONESTÀ: questo giocattolo non è word2vec e non è BERT. È il
# nonno di quei metodi, e si comporta abbastanza bene da farti VEDERE il
# fenomeno sui tuoi dati. Il modello vero, addestrato su miliardi di parole,
# arriva in 02b.


def carica_corpus(percorso=PERCORSO_DATI) -> list[list[str]]:
    """Legge il CSV del cap.01 e restituisce un documento per riga, tokenizzato."""
    dati = pd.read_csv(percorso)
    return [tokenizza(testo) for testo in dati["testo"]]


def costruisci_vocabolario(corpus: list[list[str]],
                           min_conteggio: int = MIN_CONTEGGIO) -> list[str]:
    """Passo 1 — parole viste almeno `min_conteggio` volte, in ordine alfabetico.

    L'ordine alfabetico non è estetica: fissa la posizione di ogni parola.
    Se l'ordine cambiasse, cambierebbero le righe della tabella e la mappa
    non sarebbe più confrontabile con quella salvata prima.
    """
    # Ogni token di ogni documento. "aprile" scritto una volta vale 1 e dopo cade.
    conteggi = Counter(parola for documento in corpus for parola in documento)
    # Almeno 2 occorrenze: un incontro solo non è una compagnia.
    # Ordine alfabetico: la riga 12 è sempre la stessa parola, anche domani.
    return sorted(p for p, c in conteggi.items() if c >= min_conteggio)


def matrice_co_occorrenze(corpus: list[list[str]], vocabolario: list[str]) -> np.ndarray:
    """Passo 2 — in quanti documenti ogni coppia di parole compare insieme."""
    # Indice di riga e di colonna. "cedolino" -> 12, "irpef" -> 7.
    posizione = {parola: i for i, parola in enumerate(vocabolario)}
    # Tabella quadrata, tutta a zero. conteggi[12, 7] = volte in cui cedolino e irpef
    # stanno nello stesso documento. La diagonale resta 0: una parola non incontra se stessa.
    conteggi = np.zeros((len(vocabolario), len(vocabolario)))
    for documento in corpus:
        # set: "netto" tre volte nella stessa busta conta una volta sola.
        # Chi non è nel vocabolario (visto una volta sola) non entra.
        presenti = sorted({p for p in documento if p in posizione})
        for a in presenti:
            for b in presenti:
                if a != b:
                    # +1 in questa direzione. Il ciclo farà anche il contrario,
                    # quindi la tabella è simmetrica: cedolino-irpef e irpef-cedolino.
                    conteggi[posizione[a], posizione[b]] += 1
    return conteggi


def pesa_ppmi(conteggi: np.ndarray) -> np.ndarray:
    """Passo 3 — da conteggi grezzi a "quanto questo incontro è una notizia".

    Si confronta quante volte due parole si incontrano davvero con quante
    volte si incontrerebbero per puro caso (quanto è frequente la prima,
    moltiplicato per quanto è frequente la seconda). Il logaritmo rende il
    rapporto leggibile; i valori negativi si azzerano.
    """
    # Somma di tutte le celle. Nel giocattolo a 4 documenti era 36.
    totale = conteggi.sum()
    # Somma di ogni riga, forma (n, 1): cedolino valeva 6, i suoi incontri con chiunque.
    # keepdims lascia la colonna, così dopo si stende su tutta la tabella.
    per_riga = conteggi.sum(axis=1, keepdims=True)
    # Somma di ogni colonna, forma (1, n). La tabella è simmetrica, quindi il valore
    # di "irpef" qui è lo stesso della sua riga. Serve la forma diversa per il prodotto.
    per_colonna = conteggi.sum(axis=0, keepdims=True)
    # Atteso = riga * colonna / totale.  Per cedolino-irpef: 6 * 6 / 36 = 1.
    # Rapporto = conteggio / atteso, scritto (conteggio * totale) / (riga * colonna).
    # Poi il logaritmo naturale: log(1) = 0, nessuna notizia. log(2) ≈ 0,69.
    with np.errstate(divide="ignore", invalid="ignore"):
        pesata = np.log((conteggi * totale) / (per_riga * per_colonna))
    # Cella a zero: si divide per zero o si fa log(0). Esce infinito o nan: li mettiamo a 0.
    pesata[~np.isfinite(pesata)] = 0.0
    # Rapporto sotto 1: log negativo, "si incontrano meno del caso".
    # Con pochi documenti è rumore, quindi si azzera. Resta solo la notizia.
    pesata[pesata < 0] = 0.0
    return pesata


def riduci(pesata: np.ndarray, dim: int) -> np.ndarray:
    """Passo 4 — da una riga lunga quanto il vocabolario a `dim` numeri."""
    # Ogni parola è ancora una riga lunga (una cella per ogni altra parola).
    # La SVD trova le poche direzioni che spiegano la tabella e butta il resto.
    U, valori_singolari, _ = np.linalg.svd(pesata, full_matrices=False)
    # Prime `dim` direzioni, ciascuna allungata dal suo peso.
    # Da 49 numeri a 4. Le direzioni non hanno un nome: vedi Sez. 6.
    return U[:, :dim] * valori_singolari[:dim]


def costruisci_mappa(percorso=PERCORSO_DATI,
                     dim: int = DIM,
                     min_conteggio: int = MIN_CONTEGGIO) -> dict[str, np.ndarray]:
    """I quattro passi in fila. Restituisce {parola: vettore}.

    Questa è la funzione da portare in `testo_utils.py` nel progetto.
    """
    corpus = carica_corpus(percorso)
    vocabolario = costruisci_vocabolario(corpus, min_conteggio)          # passo 1
    coppie = matrice_co_occorrenze(corpus, vocabolario)                  # passo 2, conteggi
    pesata = pesa_ppmi(coppie)                                           # passo 3, notizia
    coordinate = riduci(pesata, dim)                                     # passo 4, 4 numeri
    # La riga i di `coordinate` è la parola vocabolario[i].
    return {parola: coordinate[i] for i, parola in enumerate(vocabolario)}


# 🧩 Mini 2.1 — Lancia il file (in fondo c'è il `__main__`) e guarda la riga
#     "vocabolario". Quante parole sopravvivono con min_conteggio=2?
#     Poi prova a immaginare: alzandolo a 3, il numero sale o scende? Perché?
# TUA RISPOSTA:
# Se alziamo il conteggio minimo le parole contenute nel vocabolario diminuirebbero. Con conteggio minimo 2 le parole del vocabolario sono 49, con conteggio minimo 3 le parole contenute scendono a 34.


# 🧩 Mini 2.2 — Nel Passo 2 c'è `if a != b`. Togli quel controllo con la
#     testa (non serve eseguire): cosa finirebbe sulla diagonale della
#     tabella, e perché non ci serve?
# TUA RISPOSTA:
# Finirebbe quante volte una parola compare con se stessa nei vari documenti, ma a noi non serve saperlo. Noi vogliamo capire le occorrenze di parole con altre diverse da loro. A quel punto i conteggi entrerebbero nel passo 3, andando a spostare i pesi, perchè anche le occorrenze della parola con se stessa verrebbero conteggiate.


# ==========================================================================
# 🔁 RINFORZO MIRATO — lacuna #60 (TODO 4 del cap.01, 05/10, esame 8)
# ==========================================================================
# Nel TODO 4 avevi diagnosticato giusto il bug: in produzione veniva creato
# un `TfidfVectorizer` nuovo e rifatto il vocabolario sul testo in arrivo.
# Nel riparo però avevi salvato il vettorizzatore senza scrivere la riga che
# conta: in produzione si chiama `transform`, non `fit_transform`.
#
# Qui il rischio è lo stesso, con un nome diverso. Guarda
# `costruisci_mappa`: legge il CORPUS e produce gli assi. Se domani arriva
# una nota nuova e tu richiami `costruisci_mappa` su quella sola nota, il
# vocabolario sarà fatto di quelle poche parole, la SVD troverà altre
# direzioni, e le coordinate non avranno NIENTE a che vedere con quelle di
# ieri. Confronteresti indirizzi di due città diverse.
#
# La regola, in tre parole: la mappa si costruisce una volta, si SALVA, e
# una frase nuova si POSIZIONA sulla mappa salvata. Posizionare è
# `vettore_frase` (Sez. 5): legge la mappa, non la ricalcola.
#
#   costruisci_mappa(corpus)  ← è il `fit`.  Una volta. Si salva.
#   vettore_frase(testo, mappa) ← è il `transform`. Ogni volta. Non tocca gli assi.
#
# 🧩 Micro #60 — La torre di controllo gira da sei mesi con una mappa salvata.
#     Oggi aggiungi 400 note nuove e vuoi che la mappa le conosca.
#     Ricostruisci la mappa sulle 400 note nuove, oppure su tutto l'archivio?
#     E cosa devi fare dei vettori già salvati nel database? Due righe.
# TUA RISPOSTA:
# Ricostruisco la mappa su tutto l'archivio, arricchito delle 400 nuove note. I vettori delle vecchie note vanno ricalcolati tutti sulla base della nuova mappa.


# ==========================================================================
# SEZIONE 3 — Misurare la vicinanza
# ==========================================================================
# Hai le coordinate. Adesso serve un numero che dica quanto due parole sono
# vicine. Ci sono due strumenti e NON sono la stessa cosa.
#
#   Distanza euclidea — quanto sono lontani i due punti, in linea retta.
#     Risente della lunghezza: un vettore lungo è lontano da uno corto anche
#     se puntano nella stessa direzione.
#
#   Coseno — quanto puntano nella stessa direzione, ignorando la lunghezza.
#
# Nella ricerca per significato si usa quasi sempre il COSENO, e il motivo è
# pratico: la lunghezza di un vettore di frase dipende da quante parole hai
# messo dentro, cioè da quanto è lunga la frase. Una nota di tre righe e una
# di trenta possono dire la stessa cosa: non vuoi che la lunghezza del testo
# decida la somiglianza. Vuoi la direzione.
#
# Nota per il M6: i database vettoriali conservano i vettori già NORMALIZZATI
# (divisi per la propria norma, quindi tutti di lunghezza 1). Su vettori di
# lunghezza 1 il coseno è solo il prodotto scalare: un'operazione invece di
# tre. È la stessa normalizzazione del Ponte cap.01, applicata per velocità.


# --- 🧠 [RETRIEVAL] — da fare ADESSO, senza riaprire il cap.01 -------------
#
# Riscrivi `coseno` dalla memoria. Senza guardare `01_testo_come_numeri.py`
# e senza guardare `ponte_matematico_m2_m3/`. Il concetto l'hai ripassato in
# cima (direzione, 1 e 0); la formula e le protezioni le devi tirare fuori tu.
#
# Deve:
#   (a) restituire il coseno fra due array numpy 1D;
#   (b) alzare un errore chiaro se le due shape non coincidono;
#   (c) restituire 0.0 se uno dei due vettori ha norma zero — ti servirà
#       davvero: in Sez. 5 una frase fatta di sole parole sconosciute
#       produce proprio un vettore di zeri.
#
# Finché non la scrivi, il file gira ma non misura niente: te lo dirà.

def coseno(a: np.ndarray, b: np.ndarray) -> float:
    """Similarità coseno fra due vettori. SCRIVILA TU (retrieval, Sez. 3)."""
    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("I vettori devono essere 1D!!")
    if a.shape != b.shape:
        raise ValueError(f"Shape di a: {a} != Shape di b: {b}!!!")
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return (a @ b) / (norm_a * norm_b)


def vicini(parola: str, mappa: dict[str, np.ndarray], k: int = 5) -> list[tuple[str, float]]:
    """Le `k` parole più vicine a `parola`, per coseno. Usa la tua `coseno`."""
    if parola not in mappa:
        return []
    punteggi = [(altra, coseno(mappa[parola], vettore))
                for altra, vettore in mappa.items() if altra != parola]
    punteggi.sort(key=lambda coppia: coppia[1], reverse=True)
    return [(p, round(s, 3)) for p, s in punteggi[:k]]


# 🧩 Mini 3.1 — Dopo aver scritto `coseno`, lancia il file e leggi i vicini di
#     "cedolino" e di "saldo". Scrivi una riga per ciascuno: la compagnia che
#     esce ha senso per un documento di quel tipo?
# TUA RISPOSTA:
# si hanno molto senso (es. cedolino -> pagare, retribuzione, lorda, mese)

# ==========================================================================
# SEZIONE 4 — LA PROVA: il buco dei sinonimi, misurato
# ==========================================================================
# Questa sezione è il cuore del capitolo. Tutto il resto è contorno.
#
# Prendiamo tre coppie di frasi che NON hanno nessuna parola in comune
# (dopo la tua tokenizzazione, "di" e "del" sono stopword e spariscono):
#
#   A. "prospetto paga di aprile"   vs  "cedolino di marzo"       → sinonimi
#   B. "prospetto paga di aprile"   vs  "saldo del conto corrente" → mondi diversi
#   C. "netto in busta"             vs  "totale trattenute"        → stesso mondo
#
# Per il TF-IDF del cap.01 tutte e tre valgono ZERO. Non perché siano
# diverse: perché il coseno di due schede senza caselle in comune è zero, e
# basta. Il cap.01 dà la stessa risposta a tre situazioni molto diverse, e
# quella risposta non distingue niente.
#
# La mappa invece le separa. Esegui il file e guarda la tabella.
#
# Il dettaglio che devi notare: "cedolino" e "prospetto" non compaiono MAI
# nello stesso documento. La loro casella di co-occorrenza è zero. Eppure
# finiscono quasi nello stesso punto — perché frequentano la stessa
# compagnia: paga, lordo, netto, trattenute. Non si sono mai incontrate e si
# somigliano lo stesso. Questa è l'ipotesi distribuzionale che funziona.


def confronto(testo_a: str, testo_b: str, mappa: dict[str, np.ndarray]) -> dict[str, float]:
    """Stessa coppia di frasi, misurata con il cap.01 e con la mappa."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    dati = pd.read_csv(PERCORSO_DATI)
    vettorizzatore = TfidfVectorizer(tokenizer=tokenizza, token_pattern=None,
                                     lowercase=False)
    vettorizzatore.fit(dati["testo"])          # fit sul corpus...
    a, b = vettorizzatore.transform([testo_a, testo_b]).toarray()   # ...transform sulle frasi
    return {
        "tfidf": round(coseno(a, b), 3),
        "mappa": round(coseno(vettore_frase(testo_a, mappa),
                              vettore_frase(testo_b, mappa)), 3),
    }


# 🧩 Mini 4.1 — Nella coppia B la mappa dà un numero vicino a zero. Il TF-IDF
#     dà zero anche lui. Allora in quel caso sono equivalenti?
#     Rispondi sì o no e spiega in una riga cosa cambia davvero.
# TUA RISPOSTA:
# Non sono equivalenti. L'equivalenze nasce da una caso numerico, ma il modo in cui si è prodotto il rispettivo risultato è completamente diverso: nel tfidf, lo 0 è dato dal fatto che le due frasi non condividono nessuna parola, quindi per lui le frasi sono completamente diverse. Per la mappa invece, lo 0 indica che ha livello di significato le frasi non parlano dello stesso argomento.

# ==========================================================================
# SEZIONE 5 — Dalla parola alla frase, e l'ordine che resta perso
# ==========================================================================
# La mappa dà un punto per PAROLA. Ma tu cerchi note e documenti, cioè frasi.
# Il modo più semplice di mettere insieme le parole è la media: il punto
# medio delle parole che compongono la frase. È il centro del gruppo.
#
# Funziona sorprendentemente bene per la ricerca, e ha tre crepe. Guardale
# tutte e tre, perché due le vedrai sbattere nei capitoli successivi.
#
#   Crepa 1 — L'ORDINE. È la lacuna #62, e qui la tocchi con mano:
#       vettore_frase("netto supera lordo") e vettore_frase("lordo supera
#       netto") sono IDENTICI. La media non guarda chi viene prima.
#       Ogni parola ha un significato suo, eppure il risultato è lo stesso:
#       un sacco di significati è sempre un sacco. Serve un modello che
#       legga la SEQUENZA, ed è il cap.04 (i Transformer).
#
#   Crepa 2 — LE PAROLE SCONOSCIUTE. Una parola che non è nella mappa viene
#       saltata. Se la frase è fatta solo di parole sconosciute, il punto
#       medio non esiste e la funzione restituisce un vettore di zeri. A quel
#       punto il coseno non ha una direzione da confrontare: è esattamente il
#       caso che la tua guardia in `coseno` protegge, e il risultato è 0.0.
#       Silenzioso, non un errore. Come nel cap.01: il bug che non crasha.
#
#   Crepa 3 — LA DILUIZIONE. In una nota lunga la parola importante pesa
#       quanto tutte le altre. Media di cento parole: il punto finisce nel
#       mezzo di tutto. Per questo nel M6 i documenti si tagliano a pezzi
#       (chunking) prima di cercarli: pezzi corti, punti più nitidi.


def vettore_frase(testo: str, mappa: dict[str, np.ndarray]) -> np.ndarray:
    """Punto medio delle parole conosciute. Vettore di zeri se non ne trova.

    È il `transform` della mappa: LEGGE la mappa, non la ricalcola.
    """
    dim = len(next(iter(mappa.values())))
    punti = [mappa[parola] for parola in tokenizza(testo) if parola in mappa]
    if not punti:
        return np.zeros(dim)
    return np.mean(punti, axis=0)


# 🧩 Mini 5.1 — Verifica la crepa 1 senza eseguire: `vettore_frase` fa
#     `np.mean` su una lista di punti. Se la lista fosse nell'ordine inverso,
#     la media cambierebbe? Una riga, e di': quale proprietà della media lo
#     garantisce?
# TUA RISPOSTA:
# No non cambiarebbe, per via della proprietà commutativa.

# 🧩 Mini 5.2 — "pizza margherita" non ha parole nella mappa. Che vettore
#     esce, e quanto vale il coseno fra quel vettore e il vettore di
#     "cedolino di marzo"? Perché è pericoloso in produzione?
# TUA RISPOSTA:
# il vettore esce [0, 0] -> in produzione è pericoloso perchè a livello di significato nasconde il fatto che il modello non ha mappato di fatto il significato della frase, ma produce la stessa risposta di un vettore che invece è stato mappato in "direzione diversa". Ignoranza e direzione diversa producono lo stesso risultato.


# ==========================================================================
# SEZIONE 6 — Quante dimensioni, e cosa NON è una dimensione
# ==========================================================================
# Perché 4 e non 2? Perché 384 nei modelli veri e non 10?
#
# Con poche dimensioni lo spazio è stretto: le parole non hanno posto per
# stare distanti, e cose diverse finiscono per somigliarsi. Non è teoria,
# si misura sui tuoi dati — il file stampa questa tabella:
#
#   dim | cedolino–prospetto | cedolino–certificazione
#       |    (sinonimi)      |    (tipi diversi)
#   ----+--------------------+------------------------
#     2 |       alto         |        alto      ← non distingue niente
#     4 |       alto         |        quasi 0   ← funziona
#     8 |       medio-basso  |        quasi 0   ← i sinonimi si allontanano
#
# Con 2 dimensioni i sinonimi sono vicini, ma lo sono anche due tipi di
# documento diversi: tutto è vicino a tutto, la mappa non serve a niente.
# Con 4 lo spazio basta a tenere separate le tre famiglie.
# Con 8 la cosa si rovescia: il corpus è di 30 documenti corti, non c'è
# abbastanza materiale per riempire 8 direzioni e le ultime raccolgono
# rumore. Più dimensioni servono solo se hai abbastanza testo per riempirle.
# Un modello vero usa 384 o 768 numeri perché è stato addestrato su miliardi
# di parole. Noi ne abbiamo trenta frasi: quattro.
#
# IL GRAFICO: il file disegna una mappa a 2 dimensioni, non a 4. Non perché
# 2 bastino — hai appena visto che non bastano — ma perché un foglio ha due
# assi. Il disegno serve a vedere le famiglie, le misure usano 4.
#
# COSA NON È UNA DIMENSIONE
# Nel vecchio esempio didattico si dice «l'asse x è quanto è una busta».
# Falso, ed è importante che tu non ci creda: nessuno ha deciso cosa
# significa l'asse 1. È uscito dalla SVD come direzione che spiega molti
# dati, e mescola tanti aspetti insieme. In un modello vero nessuna delle
# 384 dimensioni ha un nome, e non puoi aprirle per spiegare una decisione.
# Non è un dettaglio: è la ragione per cui la ricerca semantica è difficile
# da spiegare a un cliente, mentre le `parole_decisive` del cap.01, che sono
# parole vere del documento, si mostrano e si capiscono.
#
# 🧩 Mini 6.1 — Un collega dice: «la terza dimensione dell'embedding è il
#     tono formale del testo». Rispondigli in due righe.
# TUA RISPOSTA:
# Non è cosi': le dimensioni non hanno un nome, sono direzioni che spiegano i dati, ma non sono legate a features spiegamili in termini semantici!


# ==========================================================================
# SEZIONE 7 — Cosa la mappa non cattura, e quando NON usarla
# ==========================================================================
# COSA NON CATTURA
#
#   La negazione. «è un cedolino» e «non è un cedolino» stanno quasi nello
#   stesso punto: "non" è una stopword, e anche se non lo fosse sposterebbe
#   la media di pochissimo. Per la mappa parlano della stessa cosa — ed è
#   vero, parlano della stessa cosa. Dicono l'opposto, e quello si perde.
#
#   La cifra esatta. Nel cap.01 hai sostituito gli importi con <importo>:
#   scelta giusta, e qui se ne vede la conseguenza. 1.703,45 e 50,00 cadono
#   nello stesso punto. Se devi verificare un importo, la mappa non è lo
#   strumento: è un confronto fra numeri, non una questione di significato.
#
#   L'identità. «il cliente Rossi» e «il cliente Bianchi» sono vicinissimi.
#   Il nome proprio è un'etichetta, non un significato.
#
# QUANDO NON USARLA (e il cap.01 resta la scelta giusta)
#
#   Devi trovare il documento con QUEL codice fiscale, o la pratica numero
#   2026/118. Qui non vuoi "qualcosa di simile", vuoi la corrispondenza
#   esatta. La ricerca per significato ti restituirà codici fiscali simili,
#   che è il risultato peggiore possibile: plausibile e sbagliato.
#   Per questi casi servono il match esatto o una ricerca per parola chiave.
#
#   Nella torre di controllo useremo entrambe le strade, ed è la norma nei
#   sistemi veri: la ricerca per parola esatta per i codici e i numeri di
#   pratica, la ricerca per significato per le note scritte a mano. Si
#   chiama ricerca ibrida ed è un capitolo del M6.
#
# 🧩 Mini 7.1 — Per ognuna, scrivi "mappa" o "esatta":
#     (a) «trova la nota dove parlavo del rinnovo del mutuo di quel cliente»
#     (b) «trova la pratica 2026/118»
#     (c) «trova i documenti che assomigliano a questa busta paga»
#     (d) «trova il documento con IBAN IT60X0542811101000000123456»
# TUA RISPOSTA:

# a) mappa;
# b) esatta;
# c) mappa;
# d) esatta;


# ==========================================================================
# SEZIONE 8 — Statico e contestuale (anticipo del cap.04)
# ==========================================================================
# La mappa di questo file è STATICA: ogni parola ha un punto e sempre quello.
# "saldo" dell'estratto conto e "saldo la fattura" (il verbo saldare) sono
# la stessa casella, quindi lo stesso punto. Sono due parole diverse che si
# scrivono uguale, e la mappa le fonde in una.
#
# Un embedding CONTESTUALE calcola il punto guardando la frase intorno: in
# «saldo finale del conto» e in «saldo la fattura domani» la parola riceve
# due punti diversi. Per farlo il modello deve leggere la sequenza — ed è
# lo stesso meccanismo che risolverà la crepa 1 della Sez. 5.
# È il cap.04, i Transformer. Lo nomino adesso perché le due cose si
# chiudono insieme, non per anticipare la teoria.
#
# 🧩 Mini 8.1 — Nel tuo lavoro, una parola che cambia mestiere a seconda
#     della frase. Scrivine una con due frasi che la usano diversamente.
# TUA RISPOSTA:
# "visura in crif" -> "visura catastale"


# ==========================================================================
# 🔁 RINFORZO MIRATO — lacuna #61 (TODO 6 del cap.01, 05/10, esame 7.5)
# ==========================================================================
# Nel TODO 6 avevi messo i tre segnali sulla stessa domanda. Non corrono la
# stessa gara, e adesso i segnali sono quattro:
#
#   Tabellare (M2)      → i conti tornano? Risponde: è alterato.
#   Visivo (M3)         → il layout sembra una busta? Risponde: è alterato.
#   Testuale (cap.01)   → quali parole ci sono? Risponde: che TIPO è.
#   Mappa (questo cap.) → in che zona di significato cade? Risponde: a cosa
#                         ASSOMIGLIA. Non dà un tipo e non dà un verdetto.
#
# La mappa restituisce un ordinamento: questi documenti sono i più simili.
# Il più simile a un cedolino può benissimo essere una fattura genuina che
# parla di importi e trattenute. "Vicino" non vuol dire "stesso tipo", e
# tantomeno "alterato".
#
# E l'altro pezzo che era scivolato: le parole mai viste. Non producono
# un 0.5 e non producono un dubbio. Vengono SALTATE. Lo vedi in
# `vettore_frase`: `if parola in mappa`. Chi non c'è, non entra.
#
# 🧩 Micro #61 — La mappa dice che la nota X è la più simile a un cedolino,
#     con coseno 0.91. Quali di queste conclusioni puoi trarre?
#     (a) X è una busta paga   (b) X è alterata   (c) X parla di temi simili
#     Scegli e motiva in una riga.
# TUA RISPOSTA:
# La mia risposta è c) : se il significato del testo estratto parla di temi simili a una fattura, non significa che il documento sia alterato, e X non deve per forza essere una busta paga, perchè lo stesso significato generale può trovarsi anche in un documento diverso da una busta paga.

# ==========================================================================
# CHECKLIST CONCETTUALE — rileggila prima degli esercizi
# ==========================================================================
# 1. Sparso = una casella per parola, quasi tutte zero. Denso = pochi numeri,
#    quasi tutti pieni. Nel denso due parole diverse possono toccarsi.
# 2. Le coordinate non le decide un umano: escono dalla compagnia che le
#    parole frequentano nel corpus.
# 3. I conteggi grezzi vanno pesati, per la stessa ragione dell'IDF: ciò che
#    sta ovunque non è una notizia.
# 4. La mappa si costruisce UNA volta e si salva. Una frase nuova si
#    posiziona sulla mappa salvata. Costruire = fit, posizionare = transform.
# 5. Si misura col coseno, non con la distanza: la lunghezza del vettore
#    dipende da quanto è lungo il testo, e non è quello che vuoi confrontare.
# 6. La media delle parole perde l'ordine, salta le parole sconosciute e
#    diluisce i testi lunghi.
# 7. Le dimensioni non hanno un nome. Poche: tutto si somiglia. Troppe per il
#    materiale che hai: rumore.
# 8. Per i codici esatti la mappa è lo strumento sbagliato.


# ==========================================================================
# QUIZ DI VERIFICA — su questo capitolo
# ==========================================================================
#
# V1. Vero o falso: in un embedding denso quasi tutte le caselle sono a zero.
# V2. "cedolino" e "prospetto" non compaiono mai nello stesso documento, e la
#     mappa li mette vicini. Come fa? Due righe.
# V3. Prevedi l'output. `a = vettore_frase("netto supera lordo", mappa)` e
#     `b = vettore_frase("lordo supera netto", mappa)`. Quanto fa
#     `coseno(a, b)`? E quale limite del cap.01 stai rivedendo?
# V4. Trova l'errore: «la mappa è salvata; arriva una nota nuova, chiamo
#     `costruisci_mappa` su quella nota e confronto il risultato con i
#     vettori nel database». Cosa succede?
# V5. Completa: per cercare la pratica numero 2026/118 non uso la mappa, uso
#     _______, perché mi serve _______ e non qualcosa di simile.
# V6. Perché nella ricerca semantica si preferisce il coseno alla distanza
#     euclidea? Una riga.
# V7. Vero o falso: la terza dimensione di un embedding si può interpretare
#     come "quanto il testo parla di soldi". Motiva.
# V8. 💬 Spiega con parole tue, senza usare la parola "vettore" e senza
#     nominare nessuna libreria: cos'è un embedding e a cosa ti serve nella
#     torre di controllo. Come lo diresti a un collega che fa siti Laravel.
#
# TUE RISPOSTE:
# V1. Falso è il contrario. Un embedding è denso proprio perchè quasi nessuna casella è a 0 (è denso di significato): La BoW è sparsa, e ha la maggior parte delle caselle a 0.
# V2. Ci riesce perche se cedolino e prospetto condividono la stessa "compagnia", la mappa le mette vicine in termini di significato. E' la messa in pratica del detto "dimmi con chi vai, e ti dirò chi sei"
# V3. coseno(a, b) = 1. La mappa non riesce a distinguere l'ordine in cui compaiono le parole, perchè di fatto producono una media di significato identica.
# V4. La mappa si addestra una volta e si salva. Poi la si utilizza per trasformare in vettori densi le nuove note che arrivano. Altrimenti, costruiamo una mappa a partire dalle sole parole dell'ultima nota. Vettorizzando poi la nota su quella mappa, avremmo delle dimensioni diverse rispetto a quello su cui sono iscritte le precedenti note che abbiamo nel database, e il confronto sarebbe inutile.
# V5. la ricerca esatta, proprio quella pratica
# V6. La ricerca semantica usa il coseno perchè questo restituisce una similitudine di direzione (significato), e non una distanza tra due grandezze diverse. Anche se due testi hanno lunghezze (e quindi grandezze) diverse, posso parlare della stessa cosa, e quindi essere di fatto molto simili.
# V7. Falso. Le dimensioni sono create a partire da numeri che non hanno un significato interpretabili, ma sono delle posizioni in "dimensioni" utili per trovare le coordinate di una parola o una frase in uno spazio multidimensionale.
# V8. Un embedding è un insieme di coordinate. Nella torre di controllo ci serve per trovare nel database delle note e record simili alla nostra richiesta.


# ==========================================================================
# ESERCIZI
# ==========================================================================
# I tag 🔧 [REFACTORING], 🔍 [DEBUG] e 🔀 [INTERLEAVING] stanno nel 02b, dove
# c'è il modello vero: è la divisione decisa il 29/09. Qui il 🧠 [RETRIEVAL]
# l'hai già fatto in Sez. 3.

# --- E1. Scrivi `lontani(parola, mappa, k=3)`: le k parole col coseno più
#         BASSO. Poi stampa i tre più lontani da "cedolino".
#         Una funzione sola, niente copia-incolla di `vicini` se puoi evitarlo.
# TUO CODICE:

def lontani(parola: str, mappa: dict[str, np.array], k: int = 5)-> list[tuple[str, float]]:
    if parola not in mappa:
        return []
    punteggi = [(altra, coseno(mappa[parola], vettore)) for altra, vettore in mappa.items() if parola != altra]
    punteggi.sort(key=lambda x: x[1])
    return [(p, round(c, 3)) for p, c in punteggi[:k]]

# if __name__ == "__main__":
    
#     print("\nEsercizio 1\n")

#     mappa = costruisci_mappa()

#     lontani_cedolino = lontani(
#         "cedolino",
#         mappa,
#         3
#     )

#     print(lontani_cedolino)

# --- E2. Costruisci due mappe, una con `min_conteggio=2` e una con
#         `min_conteggio=3`. Stampa quante parole ha ciascuna e il coseno
#         fra "cedolino" e "prospetto" in entrambe.
#         Una riga di commento: cosa è cambiato e perché.
# TUO CODICE:

if __name__ == "__main__":
    
    print("\nEsercizio 2\n")

    mappa_min_2 = costruisci_mappa(
        min_conteggio = 2
    )

    mappa_min_3 = costruisci_mappa(
        min_conteggio = 3
    )

    print(f"Mappa min_2 n_parole = {len(mappa_min_2)} parole\nMappa min_3 n_parole = {len(mappa_min_3)} parole\n")

    coseno_min_2 = coseno(vettore_frase("Cedolino", mappa_min_2), vettore_frase("Prospetto", mappa_min_2))
    coseno_min_3 = coseno(vettore_frase("Cedolino", mappa_min_3), vettore_frase("Prospetto", mappa_min_3))
    
    print(coseno_min_2)
    print(coseno_min_3, "\n")
    
    print(mappa_min_3['prospetto'] if 'prospetto' in mappa_min_3.keys() else "Il coseno è 0 perchè nella mappa con sbarramento ad almeno 3 occorrenze prospetto non è riuscito ad entrare, e dunque ci troviamo nel caso in cui 'ignoranza' da parte del modello che non conosce un parola rischia di essere scambiata per 'significato differente'\n")


# --- E3. Cerca nel corpus. Scrivi `cerca(domanda, mappa, k=3)` che
#         restituisce i 3 documenti del CSV più vicini alla domanda, come
#         lista di tuple (id, tipo, coseno), ordinati dal più simile.
#         Provala con "quanto mi è arrivato di stipendio" e guarda i tipi
#         che escono. Questo è, in miniatura, il motore di ricerca del M6.
# TUO CODICE:

def cerca(domanda: str,
        mappa: dict[str, np.ndarray],
        k: int = 3,
        percorso_dati = PERCORSO_DATI,
        verbose: bool = True) -> list[tuple[int, str, float, str]]:
    
    corpus = pd.read_csv(percorso_dati)
    vettore_domanda = vettore_frase(
        domanda,
        mappa
    )
    lista_vettori_corpus = [vettore_frase(nota, mappa) for nota in corpus['testo']]
    
    pertinenza = [coseno(vettore_domanda, vettore_nota) for vettore_nota in lista_vettori_corpus]
    
    out = sorted(
        [(int(idx), tipo, float(cos), testo) for idx, tipo, cos, testo in zip(corpus['id'], corpus['tipo'], pertinenza, corpus['testo'])],
        key=lambda x: x[2],
        reverse=True
        )
    
    if verbose:
        print(f"Query -> {domanda}\n")
        print("Documenti più pertinenti:\n")
        for o in out[:k]:
            print(f"Id documento: {o[0]}\nTipo: {o[1]}\nCoseno: {round(o[2], 4)}\nTesto: {o[3]}\n")
    return out[:k]
    
if __name__ == "__main__":
    
    print("\nEsercizio 3\n")
    
    mappa = costruisci_mappa()
    
    risposta = cerca("quanto mi è arrivato di stipendio", mappa)    


# --- E4. Esattamente 3 bullet, non 2 e non 4. Cosa questa mappa NON
#         promette a chi la usa. Tre limiti DIVERSI, non tre modi di dire
#         la stessa cosa.
# TUA RISPOSTA:
# 1. La mappa restituisce vettori di significato limitatamente agli esempi che conosce e alle parole che ho visto. Se una frase mandata come query non contiene nessuna parola che conosce, nel confronto non comunica la sua ignoranza, ma da come risultato "significato diverso".
# 2. Non riconosce l'ordine delle parole, quindi "il lordo è più importante del netto" e "il netto è più importante del lordo" per lei hanno significato identico.
# 3. Non sa dare un importanza relativa alle parole che compongono una frase. Nelle frasi lunghe il valore delle parole davvero importante si diluisce, Poichè ogni colonna dell'embedding di una frase è prodotto dalla media tra tutte le parole che la compongono.


# --- E5. 🎯 [COLLOQUIO] «Abbiamo già una ricerca full-text sul database.
#         Perché dovremmo aggiungere gli embedding?»
#         Rispondi in 4-6 righe: cosa guadagni, cosa NON guadagni, e un caso
#         concreto in cui la ricerca full-text resta migliore.
# TUA RISPOSTA:
# La ricerca full-text è utile, e in alcuni casi insostituibile: se abbiamo bisogno ad esempio di cercare un libro di un autore preciso, basta digitare il nome corretto e la ricerca produrrà i risultati cercati. Ma se non abbiamo idea di come si chiama un autore, ma vogliamo comunque avere possibilità di individuarlo, gli embedding ci danno un grande aiuto. La ricerca potrebbe diventare : libri dove si parla di un burattino e di un falegname. Gli embedding, tracciando il significato della nostra richiesta, sarebbero in grado di capire a quale libro di quale autore ci stiamo riferendo, anche se non digitiamo letteralemtne in nome dell'autore.


# --- E6. 📚 [LIBRO] [ALAMMAR cap. 2] Il libro mostra l'aritmetica dei
#         vettori: re − uomo + donna finisce vicino a regina.
#         Provala sui tuoi dati: calcola `mappa["cedolino"] - mappa["netto"]
#         + mappa["saldo"]` e stampa le 3 parole più vicine al risultato.
#         Poi, due righe oneste: il risultato ha senso? E se non ce l'ha,
#         è colpa del metodo o del corpus da 30 frasi?
# TUO CODICE:

if __name__ == "__main__":

    print("\nEsercizio 6\n")

    mappa = costruisci_mappa()
    mappa['prova'] = mappa['cedolino'] - mappa['netto'] + mappa["saldo"]
    
    prova = vicini(
        "prova",
        mappa,
        3
    )
    
    print(prova)
    
# TUA RISPOSTA:

# No il metodo non funziona, e produce risultati senza senso: non è colpa del metodo, ma del corpus estramamente ridotto, che non ha una stabilità tale da permettere risultati veri.


# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — il ramo testuale impara a cercare
# ==========================================================================
# Nel cap.01 `testo_utils.py` sa dire CHE TIPO è un documento. Adesso impara
# a dire A COSA ASSOMIGLIA. È il pezzo di pipeline che nel M6 diventa la
# ricerca della torre di controllo.
#
# Il codice di questo capitolo è didattico: il deliverable è TUO, in
# `testo_utils.py`. Non copiare e incollare senza leggere: la firma delle
# funzioni e il contratto cambiano.
#
#   [V] T1 — Porta in `testo_utils.py` le funzioni della mappa:
#            `costruisci_mappa(percorso, dim, min_conteggio) -> dict`
#            e `vettore_frase(testo, mappa) -> np.ndarray`.
#            DoD: `from testo_utils import costruisci_mappa` non stampa
#            niente e non costruisce niente all'import (come il T1 del cap.01).
#
#   [V] T2 — Salva la mappa su disco con `joblib`, accanto al modello.
#            DoD: esiste un file `mappa.pkl`; una funzione lo ricarica e
#            `vettore_frase` funziona SENZA ricostruire la mappa.
#
#   [V] T3 — Estendi il contratto del cap.01 (T5). Oltre a versione, classi,
#            tokenizer e data di training, deve contenere: `mappa_dim`,
#            `mappa_min_conteggio`, `mappa_n_parole`.
#            E alza `VERSIONE`: la ricetta è cambiata.
#            DoD: se domani ricostruisci la mappa con `dim=8`, dal contratto
#            si capisce che i vettori vecchi nel database non sono più
#            confrontabili. Scrivi in una riga di commento PERCHÉ.
#
#   [V] T4 — Un test di regressione, in fondo al file, dentro il `__main__`.
#            Tre `assert`: (a) `vettore_frase` restituisce la shape giusta;
#            (b) il coseno di una frase con se stessa è circa 1;
#            (c) una frase di sole parole sconosciute dà coseno 0.0 e non
#            solleva eccezioni.
#            DoD: lanciando `testo_utils.py` i tre assert passano in silenzio.
#
#   T5 — TOGLIO (08/10/2026, richiesta studente: «parte finale noiosa»).
#        Non è più un deliverable. Il tema (direzione senza nome vs
#        parole_decisive) torna in 02b come mini breve, non come saggio.


# ==========================================================================
# DEFINITION OF DONE — il capitolo è chiuso quando
# ==========================================================================
# [ ] Quiz d'ingresso e quiz di verifica compilati (V8 Feynman compreso)
# [ ] `coseno` riscritta dalla memoria e funzionante (il file gira e misura)
# [ ] Tutti i 🧩 mini e i tre 🧩 micro dei rinforzi (#60, #61, #62) risposti
# [ ] E1–E6 svolti, E4 con esattamente 3 bullet
# [V] T1–T4 del progetto, con i tre assert del T4 che passano (T5 tolto)
# [ ] Sai rispondere a voce: perché la mappa si costruisce una volta sola


# ==========================================================================
# CODICE DI SERVIZIO — la dimostrazione che gira
# ==========================================================================

def tabella_dimensioni(coppie: list[tuple[str, str]],
                       dimensioni: tuple[int, ...] = (2, 4, 8)) -> pd.DataFrame:
    """Lo stesso confronto con mappe di dimensione diversa (Sez. 6)."""
    righe = []
    for dim in dimensioni:
        mappa = costruisci_mappa(dim=dim)
        riga = {"dim": dim}
        for a, b in coppie:
            riga[f"{a}-{b}"] = round(coseno(mappa[a], mappa[b]), 3)
        righe.append(riga)
    return pd.DataFrame(righe)


def disegna(parole: list[str] | None = None) -> None:
    """Mappa a 2 dimensioni. Il foglio ha due assi: le misure però usano DIM."""
    import matplotlib.pyplot as plt

    mappa2d = costruisci_mappa(dim=DIM_DISEGNO)
    if parole is None:
        parole = ["cedolino", "busta", "prospetto", "paga", "netto", "lordo",
                  "irpef", "trattenute", "saldo", "conto", "estratto",
                  "accredito", "bonifico", "certificazione", "unica",
                  "redditi", "ritenute", "sostituto"]
    parole = [p for p in parole if p in mappa2d]

    plt.figure(figsize=(9, 7))
    for parola in parole:
        x, y = mappa2d[parola]
        plt.scatter(x, y, s=40)
        plt.annotate(parola, (x, y), xytext=(4, 4), textcoords="offset points")
    plt.title("Mappa a 2 dimensioni — le coordinate escono dai 30 documenti")
    plt.xlabel("direzione 1 (non ha un nome: vedi Sez. 6)")
    plt.ylabel("direzione 2 (non ha un nome)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def demo() -> None:
    """Tutto quello che il capitolo afferma, misurato."""
    corpus = carica_corpus()
    vocabolario = costruisci_vocabolario(corpus)
    mappa = costruisci_mappa()

    print(f"documenti: {len(corpus)}")
    print(f"vocabolario (viste almeno {MIN_CONTEGGIO} volte): {len(vocabolario)} parole")
    print(f"ogni parola è {DIM} numeri. Esempio, cedolino: "
          f"{np.round(mappa['cedolino'], 3)}\n")

    print("-- Sez. 3: la compagnia che frequentano --")
    for parola in ("cedolino", "saldo", "certificazione"):
        print(f"  vicini di {parola:15s} {vicini(parola, mappa, 4)}")

    print("\n-- Sez. 4: la prova. Nessuna di queste coppie ha parole in comune --")
    coppie = [
        ("prospetto paga di aprile", "cedolino di marzo", "sinonimi"),
        ("prospetto paga di aprile", "saldo del conto corrente", "mondi diversi"),
        ("netto in busta", "totale trattenute", "stesso mondo"),
    ]
    print(f"  {'':58s}{'TF-IDF':>8s}{'mappa':>8s}")
    for a, b, etichetta in coppie:
        r = confronto(a, b, mappa)
        print(f"  {a!r} vs {b!r}".ljust(60) + f"{r['tfidf']:>8.3f}{r['mappa']:>8.3f}"
              f"   ({etichetta})")
    print("  Il cap.01 dà 0.000 a tutte e tre: non le distingue.")

    print("\n-- Sez. 5: l'ordine resta perso (lacuna #62) --")
    a = vettore_frase("netto supera lordo", mappa)
    b = vettore_frase("lordo supera netto", mappa)
    print(f"  coseno fra le due frasi invertite: {coseno(a, b):.3f}")
    print(f"  frase di sole parole sconosciute: {vettore_frase('pizza margherita', mappa)}")

    print("\n-- Sez. 6: quante dimensioni servono --")
    print(tabella_dimensioni([("cedolino", "prospetto"),
                              ("cedolino", "certificazione")]).to_string(index=False))
    print("  Con 2 non distingue i sinonimi dai tipi diversi. Con 4 sì.")


# ==========================================================================
# SOLUZIONI — solo dopo il tuo tentativo
# ==========================================================================
#
# QUIZ D'INGRESSO
# Q1  1 (o 1.0). Stesse parole, stessi conteggi: l'ordine non entra nel vettore.
# Q2  Falso. È il bug del TODO 4: vocabolario nuovo, colonne diverse dai pesi.
# Q3  Manca il vettorizzatore salvato; in produzione va chiamato `transform`.
# Q4  Viene scartata. Non diventa una casella nuova e non segnala niente.
# Q5  `transform`
# Q6  Il tipo del documento. Non «è alterato?».
# Q7  0.0. Un vettore di zeri non ha direzione: il coseno sarebbe 0 diviso 0.
#     Restituire 0.0 evita il nan e dice "nessuna somiglianza misurabile".
#
# MICRO E MINI
# #62   Deve leggere la frase in sequenza: tenere conto di quale parola viene
#       prima e quale dopo, non solo di quali parole ci sono.
# 1.1   19.970 caselle a zero nella scheda. Nell'embedding, in pratica zero:
#       i 384 numeri sono tutti pieni (qualcuno può capitare a 0, ma non è
#       "assenza di parola", è solo un valore).
# 2.1   49 parole. Alzando a 3 il numero SCENDE: il filtro diventa più
#       severo e taglia le parole viste solo due volte.
# 2.2   Sulla diagonale finirebbe quante volte ogni parola compare insieme a
#       se stessa, cioè in quanti documenti sta. Non dice niente sulla
#       compagnia, e nel passo 3 falserebbe i totali di riga.
# #60   Ricostruisci su TUTTO l'archivio: la mappa deve conoscere il
#       vocabolario intero. E poi devi RICALCOLARE tutti i vettori già
#       salvati, perché gli assi sono cambiati: i vecchi e i nuovi non sono
#       più confrontabili. Nel M6 questa operazione si chiama reindicizzare.
# 3.1   cedolino → pagare, retribuzione, lorda, mese. saldo → finale,
#       iniziale, accredito, conto. Sì: è esattamente la compagnia di quel
#       tipo di documento, e nessuno gliel'ha detto. Nota che diverse coppie
#       danno 1.000 o quasi: su 30 frasi certe parole compaiono sempre negli
#       stessi documenti, quindi la mappa non ha modo di distinguerle. È il
#       limite del corpus piccolo, non un errore.
# 4.1   No. Il TF-IDF dà zero perché non ha parole in comune — darebbe zero
#       anche ai sinonimi. La mappa dà quasi zero perché ha GUARDATO il
#       significato e ha concluso che sono lontani. Stesso numero, informazione
#       diversa: una è ignoranza, l'altra è una misura.
# 5.1   No, non cambierebbe. La somma è commutativa, quindi la media non
#       dipende dall'ordine degli addendi.
# 5.2   Esce un vettore di zeri, e il coseno vale 0.0 grazie alla guardia.
#       È pericoloso perché non è un errore: il sistema risponde "nessuna
#       somiglianza" sia quando non c'è, sia quando non ha capito la domanda.
#       Due situazioni diverse, stessa risposta silenziosa.
# 6.1   Nessuno ha assegnato un significato alle dimensioni: escono da una
#       scomposizione numerica e mescolano più aspetti insieme. Se vuoi
#       sapere se un testo è formale, lo misuri a parte: non lo leggi da un
#       asse.
# 7.1   (a) mappa — (b) esatta — (c) mappa — (d) esatta.
# 8.1   Esempi buoni: "saldo" (saldo del conto / saldare una fattura),
#       "interesse" (interesse bancario / avere interesse), "pratica"
#       (fascicolo / fare pratica), "conto" (conto corrente / fare i conti).
# #61   (c). La vicinanza dice solo che i due testi parlano di temi simili.
#       Non assegna il tipo (quello lo fa il classificatore del cap.01) e
#       non dice niente sull'alterazione (quello è il ramo tabellare e visivo).
#
# QUIZ DI VERIFICA
# V1  Falso. Denso vuol dire caselle piene. Gli zeri sono della scheda sparsa.
# V2  Perché le coordinate non vengono dal fatto che si incontrano, ma dalla
#     compagnia che tengono: tutt'e due stanno vicino a paga, lordo, netto,
#     trattenute. Avere la stessa compagnia basta per finire nella stessa zona.
# V3  1.0 (identici: lo stesso vettore). Rivedi la lacuna #62: la media perde
#     l'ordine, esattamente come lo perdeva il Bag of Words.
# V4  `costruisci_mappa` su una nota sola rifà vocabolario e assi su quelle
#     poche parole. Le coordinate che escono non sono confrontabili con
#     quelle nel database: stessi numeri, significato diverso. È lo stesso
#     errore del `fit_transform` in produzione del cap.01 (#60).
# V5  ...uso la ricerca esatta (o full-text per parola chiave), perché mi
#     serve la corrispondenza esatta e non qualcosa di simile.
# V6  Perché la lunghezza del vettore dipende da quante parole ha il testo,
#     e non voglio che un testo lungo risulti diverso da uno corto che dice
#     la stessa cosa. Il coseno guarda la direzione e ignora la lunghezza.
# V7  Falso. Le dimensioni non hanno un nome: nascono da una scomposizione
#     numerica e ciascuna mescola più aspetti.
# V8  Accettabile se dice, con parole sue, qualcosa come: «a ogni testo do un
#     indirizzo; testi che dicono cose simili finiscono vicini, così cerco
#     per senso e non per parola esatta». Deve emergere il guadagno concreto
#     (trovo la nota sul "prospetto" cercando "cedolino"). Se resta sul nome
#     tecnico, o se scivola a descrivere il conteggio delle parole del
#     cap.01, è una lacuna Feynman: registrarla.
#
# ESERCIZI
# E1  Stessa logica di `vicini` con l'ordinamento al contrario. La via pulita
#     è un parametro: `def vicini(parola, mappa, k=5, inverti=False)` e
#     `reverse=not inverti`. Due funzioni quasi identiche sono il tipo di
#     duplicazione che il refactoring del 02b ti chiederà di togliere.
# E2  Con 3 il vocabolario si accorcia. Il coseno cedolino-prospetto resta
#     alto: quelle due parole hanno compagnia abbondante e sopravvivono al
#     filtro. Quello che si perde sono le parole di coda.
# E3  Il nucleo è: `mappa` costruita una volta, `vettore_frase` su ogni
#     documento del CSV, `coseno` con la domanda, `sort` decrescente, primi 3.
#     Con "quanto mi è arrivato di stipendio" devono uscire buste paga o
#     estratti conto con accredito: entrambi sono risposte sensate, e il
#     fatto che non ci sia una sola risposta giusta è esattamente la natura
#     della ricerca semantica.
# E4  Tre limiti distinti. Per esempio: l'ordine delle parole, la negazione,
#     la cifra esatta. Oppure: identità delle persone, codici, diluizione nei
#     testi lunghi. Un solo bullet, o tre parafrasi dello stesso limite:
#     Pattern #6.
# E5  Guadagni: trovi documenti che non contengono le parole cercate ma
#     parlano della stessa cosa (sinonimi, modi di dire diversi).
#     Non guadagni: precisione sui codici, sulle cifre e sulle negazioni;
#     e perdi la spiegabilità, perché non puoi mostrare la parola che ha
#     deciso. Caso in cui il full-text vince: cercare un codice fiscale, un
#     IBAN o un numero di pratica. Risposta forte se nomina la ricerca ibrida.
# E6  Su 30 frasi l'aritmetica dei vettori quasi sicuramente NON funziona: il
#     risultato cade vicino a parole generiche. La risposta giusta è che il
#     metodo in sé non è sbagliato, ma serve un corpus enorme perché quelle
#     regolarità emergano. Dire "non funziona quindi è falso" è troppo
#     veloce; dire "funziona" senza guardare l'output è peggio.
#
# PROGETTO
# T3  Se cambi `dim`, cambia il numero di assi e cambiano tutti i valori: un
#     vettore a 4 numeri e uno a 8 non si confrontano nemmeno come forma, e
#     anche a parità di numeri le direzioni sono altre. Il contratto serve a
#     scoprirlo PRIMA di confrontare, non dopo.
# T4  (b) il coseno di una frase con se stessa è 1 a meno dell'errore di
#     virgola mobile: usa `abs(x - 1) < 1e-9`, non `== 1`.


if __name__ == "__main__":
    try:
        demo()
    except NotImplementedError as errore:
        print(errore)
        print("\nIl resto del capitolo funziona: la mappa si costruisce lo stesso.")
        mappa = costruisci_mappa()
        print(f"parole nella mappa: {len(mappa)} — esempio cedolino: "
              f"{np.round(mappa['cedolino'], 3)}")
        print("Scrivi coseno() e rilancia: da lì in poi il capitolo misura.")
