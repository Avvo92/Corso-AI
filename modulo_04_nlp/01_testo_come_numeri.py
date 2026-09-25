"""
============================================================================
MODULO 4 (NLP, Embeddings & Transformers) — CAPITOLO 01
Il testo diventa numeri: tokenizzazione, Bag of Words, TF-IDF
============================================================================

DA DOVE VIENI
-------------
Nel M3 hai insegnato a una rete a guardare un'IMMAGINE. Un'immagine è già
numeri: un tensore (3, 224, 224) di intensità di pixel. Il lavoro era
normalizzare quei numeri e darli in pasto a una CNN.

Il testo no. Il testo è:

    "Cedolino paga marzo 2026 - netto in busta 1.703,45 EUR"

e un modello non sa cosa farsene. Non esiste "il pixel della parola".
Qualcuno deve DECIDERE come trasformare quella stringa in vettori.

Questo capitolo è quel "qualcuno". È il gradino più basso del M4, ma è
anche quello che regge tutto il resto: embeddings (cap.02), ricerca
semantica (cap.03), Transformer (cap.04), RAG (M6).


L'ANALOGIA DEL CAPITOLO
-----------------------
Immagina di dover archiviare mille pratiche senza poterle leggere.
Hai solo una scheda per pratica, con le caselle da barrare:

    [ ] "cedolino"   [ ] "IRPEF"   [ ] "saldo"   [ ] "canone" ...

Per ogni documento barri le caselle delle parole che compaiono e conti
quante volte. Alla fine ogni documento è una RIGA DI NUMERI.

Quella riga di numeri è il Bag of Words. È stupida (non sa che
"cedolino" e "busta paga" sono la stessa cosa, non sa l'ordine delle
parole), ma è misurabile, veloce e sorprendentemente utile.

TF-IDF è la stessa scheda, con una furbizia in più: le caselle che
risultano barrate in TUTTI i documenti valgono meno, perché non
distinguono niente.


PERCHÉ NON SALTIAMO DIRETTO AGLI EMBEDDINGS
-------------------------------------------
Tentazione legittima: "gli embeddings sono meglio, partiamo da lì".
Tre motivi per non farlo:

  1. Gli embeddings si spiegano come *superamento* di BoW/TF-IDF: se non
     senti il limite, la soluzione sembra magia.
  2. Il 100% dei sistemi NLP passa comunque da tokenizzazione e
     vocabolario — anche GPT. Cambia COME si tokenizza, non SE.
  3. In produzione TF-IDF è ancora una baseline seria: veloce, senza GPU,
     spiegabile. Se il modello grosso non batte la baseline, hai un
     problema di progetto, non di modello.


----------------------------------------------------------------------------
DEFINITION OF DONE (cosa devi saper fare a fine capitolo)
----------------------------------------------------------------------------
  1) Normalizzare e tokenizzare testo italiano sporco (OCR)      → Sez. 1
  2) Costruire un vocabolario e un vettore Bag of Words a mano   → Sez. 2
  3) Spiegare TF, IDF e perché IDF penalizza le parole comuni    → Sez. 3
  4) Usare CountVectorizer / TfidfVectorizer senza leakage       → Sez. 2-3
  5) Trovare il documento più simile con la similarità coseno    → Sez. 4
  6) Elencare 3 limiti del conteggio e perché servono embeddings → Sez. 5
  7) Consegnare `testo_utils.py` per il ramo testuale prodotto   → 🏗️

⚠️ HARDWARE: tutto su CPU. Nessuna installazione nuova: numpy, pandas,
   scikit-learn bastano. `transformers` serve dal cap.02.

⚠️ PRIVACY: si lavora su `dati/note_documenti.csv`, testi SINTETICI.
   Un OCR reale contiene nome, codice fiscale, IBAN: sono dati personali
   in chiaro, peggio dell'immagine. Mai in un servizio esterno.

============================================================================
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Import — uno per riga, con il motivo
# ---------------------------------------------------------------------------
import re                       # espressioni regolari: "trova i pezzi che sembrano parole"
import unicodedata              # per gestire accenti e caratteri strani dell'OCR
from collections import Counter  # conteggio di occorrenze, già visto nel M1
from pathlib import Path

import numpy as np
import pandas as pd

# scikit-learn: gli stessi oggetti del M2, ma applicati al testo.
# CountVectorizer  → testo  -> matrice di conteggi
# TfidfVectorizer  → testo  -> matrice di pesi TF-IDF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

QUI = Path(__file__).resolve().parent
PERCORSO_DATI = QUI / "dati" / "note_documenti.csv"


# ==========================================================================
# QUIZ D'INGRESSO — cosa ti porti dal M2 e dal M3
# ==========================================================================
#
# Scrivi la risposta sotto ogni domanda. Soluzioni in fondo al file.
# NON guardarle prima: servono a misurare cosa è rimasto, non a fare bella figura.
#
# --------------------------------------------------------------------------
# Q1 — fit / transform (M2) (formato: 2 righe)
# --------------------------------------------------------------------------
# Nel M2 usavi StandardScaler dentro una Pipeline. In una riga: cosa impara
# `fit`? In una riga: cosa fa `transform`?
# TUA RISPOSTA: fit serve per trovare media e varianza calcolata su tutto il set di train. transform invece serve per normalizzare i valori usando media e varianza prodotta dal fit. il fit va esclusivamente fatto con il set di train.
#
#
# --------------------------------------------------------------------------
# Q2 — leakage (M2 cap.05) (formato: V/F + motivazione)
# --------------------------------------------------------------------------
# "Faccio fit dello scaler su tutto il dataset, poi divido in train e test:
#  tanto lo scaler non vede le etichette."
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q3 — preprocess coerente (M3 cap.10) (formato: 2 righe)
# --------------------------------------------------------------------------
# Nel M3 il preprocess dell'inferenza doveva essere identico a quello del
# training (Resize/CenterCrop/Normalize con gli stessi mean/std).
# Cosa succedeva se erano diversi? E perché era un bug pericoloso?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q4 — shape (Ponte + M3) (formato: prevedi l'output)
# --------------------------------------------------------------------------
# Hai 30 documenti e un vocabolario di 400 parole.
# Che shape ha la matrice "documenti × parole"? Cosa rappresenta la cella [5, 12]?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q5 — similarità coseno (Ponte cap.01) (formato: 1 riga + intuizione)
# --------------------------------------------------------------------------
# Cosa misura la similarità coseno fra due vettori? Cosa significa un
# valore vicino a 1 e uno vicino a 0?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q6 — Python base (formato: prevedi l'output)
# --------------------------------------------------------------------------
#   testo = "Netto in busta 1.703,45 EUR"
#   print(testo.lower().split())
# Quante voci ha la lista? Ti sembrano tutte "parole"?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q7 — 💬 a naso, prima di studiare (formato: 3 righe)
# --------------------------------------------------------------------------
# Senza sapere ancora nulla: come faresti TU a trasformare mille documenti
# di testo in numeri utilizzabili da un modello? Scrivi la tua idea grezza.
# Alla fine del capitolo la rileggerai — serve proprio per quello.
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 0 — 🔁 RIPASSI PROPOSITIVI (Regola 43)
# ==========================================================================
#
# Questo capitolo riusa tre cose del passato. Prima di usarle, le rinfreschiamo.
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — fit / transform e leakage (M2 cap.03 e cap.05)
# --------------------------------------------------------------------------
# Nel M2 hai imparato che un trasformatore scikit-learn ha due momenti:
#
#     .fit(X_train)        → IMPARA dei parametri dai dati (es. media e
#                            deviazione standard di ogni colonna)
#     .transform(X)        → APPLICA quei parametri, senza reimpararli
#
# E la regola d'oro: si fa `fit` **solo sul train**. Se fai `fit` su tutto
# il dataset, informazioni del test entrano nel modello → **data leakage**:
# i numeri di validazione diventano bugiardi (troppo belli).
#
# Perché te lo ricordo adesso: in questo capitolo il "trasformatore" impara
# il **vocabolario**. Se lo impara anche dai documenti di test, il modello
# conosce parole che in produzione non avrebbe mai visto. È leakage, ma è
# molto più difficile da notare che con uno scaler.
#
# 🧩 Mini 0.1 — Una riga: cosa impara un vettorizzatore di testo nel `fit`?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — similarità coseno (Ponte Matematico cap.01)
# --------------------------------------------------------------------------
# Nel Ponte avevi scritto a mano la funzione `coseno(a, b)`:
#
#     coseno = (a · b) / (||a|| * ||b||)
#
# dove `a · b` è il dot product (somma dei prodotti elemento per elemento)
# e `||a||` è la norma (la "lunghezza" del vettore).
#
# L'intuizione che avevi fissato: il coseno guarda la **direzione**, non la
# lunghezza. Due frecce che puntano dalla stessa parte → coseno vicino a 1,
# anche se una è lunga il doppio.
#
# Perché conta qui: un documento lungo ha conteggi più grandi di un
# documento corto che parla della stessa cosa. Se confrontassi le lunghezze
# sbaglieresti; guardando la direzione, no.
#
# 🧩 Mini 0.2 — V/F + mezza riga: "Due documenti con lo stesso argomento ma
#   lunghezza molto diversa hanno per forza coseno basso."
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — preprocess coerente (M3 cap.10)
# --------------------------------------------------------------------------
# Nel cap.10 il punto centrale era: il preprocess dell'inferenza deve essere
# IDENTICO a quello del training, e i suoi parametri viaggiano nel contratto
# dentro il checkpoint. Se in training normalizzavi con certi mean/std e in
# demo con altri, il modello non crashava: dava risposte peggiori in
# silenzio ("il bug che non crasha").
#
# Qui è lo stesso, con un nome diverso: se in training tokenizzi in un modo
# (minuscolo, senza punteggiatura) e in produzione in un altro, le parole
# non combaciano più con il vocabolario e i vettori diventano quasi vuoti.
# Nessuna eccezione, solo predizioni scadenti.
#
# 🧩 Mini 0.3 — Due righe: qual è, in questo capitolo, l'equivalente del
#   "contratto di inferenza" del M3? Cosa deve viaggiare insieme al modello?
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 1 — Dal testo ai token
# ==========================================================================
#
# 1.1 Intuizione
# --------------
# Tokenizzare = tagliare il testo in pezzi elementari (i "token").
# Nel caso più semplice un token è una parola.
#
#     "netto in busta 1.703,45 EUR"  →  ["netto", "in", "busta", "1.703,45", "eur"]
#
# Sembra banale finché non ci provi sul serio.
#
#
# 1.2 Il confronto a tre lingue (lo conosci già)
# ----------------------------------------------
# Tagliare una stringa su spazi lo hai fatto mille volte:
#
#     JavaScript:   "a b c".split(" ")        // ["a","b","c"]
#     PHP:          explode(" ", "a b c");    // ["a","b","c"]
#     Python:       "a b c".split()           # ["a","b","c"]
#
# La versione Python senza argomenti è già più furba: taglia su QUALSIASI
# spazio (anche tab, a capo, spazi doppi) e scarta le stringhe vuote.
#
#
# 1.3 Perché split() non basta (il cuore della sezione)
# ------------------------------------------------------
# Prendi una riga realistica di OCR italiano:
#
#     "Cedolino  paga LUGLIO 2026 – dell'importo 1.703,45 EUR; però NETTO."
#
# Con split() ottieni token come:
#
#     "LUGLIO"        → maiuscolo: diverso da "luglio" per il computer
#     "dell'importo"  → due parole appiccicate dall'apostrofo
#     "EUR;"          → punto e virgola incollato
#     "NETTO."        → punto finale incollato
#     "–"             → trattino lungo, non è una parola
#
# Risultato: il vocabolario si riempie di doppioni ("netto", "NETTO.",
# "Netto,") e il modello li tratta come parole DIVERSE. È lo stesso tipo di
# guaio delle classi invertite del M3: non crasha, peggiora.
#
# I quattro passi della normalizzazione che useremo:
#
#     1. minuscolo            "NETTO" → "netto"
#     2. accenti/unicode      "però" resta "però", ma "però" scritto con
#                             caratteri combinanti diventa uniforme
#     3. taglio intelligente  con una regex, invece che su spazi
#     4. filtro               via i token inutili (lunghezza 1, solo simboli)
#
#
# 1.4 Cosa NON buttare via (scelta di dominio)
# ---------------------------------------------
# Tentazione: "tolgo tutti i numeri, sono rumore".
# Nel nostro dominio è un errore: gli importi e le date sono informazione.
# Ma "1.703,45" come token è inutile — comparirà una volta sola nella vita.
#
# Compromesso professionale: **sostituire, non cancellare**. Trasformiamo
# ogni importo in un segnaposto `<importo>` e ogni data in `<data>`.
# Così il modello impara "qui c'è un importo" senza imparare *quel* numero.
# È anche un regalo alla privacy: il numero specifico sparisce.


# Le regex del capitolo, definite una volta sola (compilate = più veloci).
# Non serve saperle scrivere a memoria: serve saperle LEGGERE.
RE_DATA = re.compile(r"\b\d{1,2}[/-]\d{1,2}([/-]\d{2,4})?\b")
#                      \b        = confine di parola
#                      \d{1,2}   = una o due cifre
#                      [/-]      = una barra o un trattino
#                      (...)?    = gruppo opzionale (l'anno può mancare)

RE_IMPORTO = re.compile(r"\b\d{1,3}(\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b")
#                       formato italiano: 1.703,45  oppure  650,00

RE_TOKEN = re.compile(r"[a-zàèéìòù<>]+")
#                      sequenze di lettere (accenti italiani inclusi);
#                      <> serve a tenere interi i segnaposto <importo>/<data>


def normalizza(testo: str) -> str:
    """Porta il testo in una forma stabile, prima di tagliarlo.

    Ordine dei passi scelto apposta:
      1) unicode      → caratteri uniformi
      2) minuscolo    → "NETTO" e "netto" sono la stessa parola
      3) segnaposto   → importi e date diventano <importo> / <data>

    I segnaposto si mettono DOPO il minuscolo e PRIMA della tokenizzazione,
    altrimenti la regex dei token spezzerebbe i numeri.
    """
    testo = unicodedata.normalize("NFC", testo)
    testo = testo.lower()
    testo = RE_IMPORTO.sub(" <importo> ", testo)
    testo = RE_DATA.sub(" <data> ", testo)
    return testo


# Parole grammaticali italiane: compaiono ovunque e non distinguono nulla.
# In gergo si chiamano "stopword". Lista volutamente corta e leggibile:
# una lista lunga si copia da una libreria, ma qui vogliamo capire la logica.
STOPWORD_IT = {
    "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "del", "dello", "della", "dei", "degli", "delle",
    "al", "allo", "alla", "ai", "agli", "alle",
    "dal", "dalla", "nel", "nella", "sul", "sulla",
    "e", "ed", "o", "che", "non", "si", "come", "anche",
}


def tokenizza(testo: str, togli_stopword: bool = True) -> list[str]:
    """Testo (già normalizzato o no) → lista di token puliti.

    Sceglie i token con una regex invece che con split():
    così punteggiatura, apostrofi e trattini non si appiccicano alle parole.
    """
    testo = normalizza(testo)
    token = RE_TOKEN.findall(testo)

    # Scarta i token di una sola lettera: quasi sempre residui di apostrofi
    # ("dell'importo" → "dell", "importo"; "l'iban" → "l", "iban").
    token = [t for t in token if len(t) > 1]

    if togli_stopword:
        token = [t for t in token if t not in STOPWORD_IT]

    return token


# 🧩 Mini 1.1 — Esegui mentalmente `tokenizza("Cedolino PAGA del 01/03/2026
#   per l'importo di 1.703,45 EUR")` e scrivi la lista che ti aspetti.
#   Poi eseguila davvero e confronta.
# TUA RISPOSTA (attesa):
#
# TUA RISPOSTA (reale):
#
#
# 🧩 Mini 1.2 — Trova l'errore: uno junior scrive
#       token = testo.lower().replace(".", "").split()
#   Elenca DUE problemi concreti che questa riga crea sul nostro dominio.
# TUA RISPOSTA:
# -
# -
#
# 🧩 Mini 1.3 — Scelta di dominio (2 righe): perché trasformiamo gli importi
#   in `<importo>` invece di cancellarli? Cita un motivo di modello e uno di
#   privacy.
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 2 — Vocabolario e Bag of Words
# ==========================================================================
#
# 2.1 Intuizione
# --------------
# Torna all'analogia della scheda con le caselle.
#
#   1. Raccogli TUTTE le parole che esistono nei tuoi documenti → VOCABOLARIO
#   2. Le metti in ordine e le numeri → ogni parola ha una POSIZIONE fissa
#   3. Per ogni documento crei un vettore lungo quanto il vocabolario,
#      con in ogni posizione il numero di volte che quella parola compare
#
# Esempio minuscolo con 3 documenti:
#
#     d1 = "netto busta netto"
#     d2 = "netto saldo"
#     d3 = "saldo saldo canone"
#
#   Vocabolario ordinato: ["busta", "canone", "netto", "saldo"]
#                            0         1         2        3
#
#           busta  canone  netto  saldo
#     d1 →     1      0      2      0
#     d2 →     0      0      1      1
#     d3 →     0      1      0      2
#
# Questa tabella è la matrice documenti × parole. Ogni RIGA è un documento
# diventato vettore. Da qui in poi è algebra: è esattamente quello che
# sapevi già fare nel M2 con le colonne di un DataFrame.
#
#
# 2.2 Il nome "bag" (sacco) non è casuale
# ----------------------------------------
# "il netto supera il lordo" e "il lordo supera il netto" producono lo
# STESSO vettore. L'ordine è perso: è come se avessi buttato le parole in
# un sacco e le avessi contate senza guardare la sequenza.
#
# È il limite numero uno del metodo, e lo pagheremo nel cap.02.
#
#
# 2.3 Sparsità
# ------------
# Su un corpus reale il vocabolario arriva a decine di migliaia di parole,
# ma un singolo documento ne usa qualche decina. Quindi la riga è quasi
# tutta zeri: si dice che la matrice è **sparsa**.
# scikit-learn per questo non restituisce un array NumPy normale ma una
# matrice sparsa (salva solo le celle diverse da zero). Per guardarla
# serve `.toarray()` — che su dati veri può far esplodere la RAM, quindi
# si usa solo su campioni piccoli come il nostro.


def costruisci_vocabolario(documenti: list[str]) -> dict[str, int]:
    """Lista di documenti → {parola: posizione}, in ordine alfabetico.

    L'ordine deve essere DETERMINISTICO: se cambia, cambiano le posizioni
    e i vettori salvati ieri non combaciano più con quelli di oggi.
    È lo stesso problema dell'ordine delle classi nel M3 cap.10.
    """
    parole = set()
    for doc in documenti:
        parole.update(tokenizza(doc))
    return {parola: i for i, parola in enumerate(sorted(parole))}


def bag_of_words(documento: str, vocabolario: dict[str, int]) -> np.ndarray:
    """Un documento → vettore di conteggi lungo quanto il vocabolario.

    Le parole non presenti nel vocabolario (Out Of Vocabulary) vengono
    IGNORATE: non c'è una casella dove metterle. È un limite vero, non una
    svista — tienilo a mente per il quiz.
    """
    vettore = np.zeros(len(vocabolario), dtype=float)
    for parola, quante in Counter(tokenizza(documento)).items():
        posizione = vocabolario.get(parola)
        if posizione is not None:
            vettore[posizione] = quante
    return vettore


def demo_bow_a_mano() -> None:
    """Esegue l'esempio dei 3 documenti e stampa la tabella."""
    documenti = ["netto busta netto", "netto saldo", "saldo saldo canone"]
    vocabolario = costruisci_vocabolario(documenti)
    matrice = np.vstack([bag_of_words(d, vocabolario) for d in documenti])

    print("Vocabolario:", vocabolario)
    print(pd.DataFrame(matrice, columns=list(vocabolario), index=["d1", "d2", "d3"]))


# 🧩 Mini 2.1 — Prima di eseguire `demo_bow_a_mano()`: quante colonne avrà
#   la tabella? Perché "netto" nella riga d1 vale 2?
# TUA RISPOSTA:
#
#
# 🧩 Mini 2.2 — Prevedi l'output (formato: vettore):
#   Con il vocabolario dell'esempio, che vettore produce
#   "canone canone sconosciuto"?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 2.4 La versione scikit-learn (quella che userai davvero)
# --------------------------------------------------------------------------
# Scrivere BoW a mano serve a capirlo. In produzione si usa
# `CountVectorizer`, che fa le stesse cose in modo efficiente:
#
#     vec = CountVectorizer(tokenizer=..., lowercase=False)
#     X_train = vec.fit_transform(testi_train)   # impara vocabolario + trasforma
#     X_test  = vec.transform(testi_test)        # SOLO trasforma
#
# ⚠️ Attenzione al punto che pesa di più (ripasso 0.1):
#     fit_transform  → sul TRAIN
#     transform      → su test e su produzione
# Se fai `fit_transform` anche sul test, il vocabolario conosce parole che
# in produzione non esisterebbero: **leakage**.


def vettorizza_conteggi(testi_train: list[str], testi_test: list[str]):
    """CountVectorizer usato correttamente: fit solo sul train.

    Passiamo il NOSTRO tokenizer: così la pipeline del capitolo è coerente
    (segnaposto importi/date, stopword italiane, niente token di 1 lettera).
    """
    vec = CountVectorizer(
        tokenizer=tokenizza,   # la nostra funzione della Sez. 1
        lowercase=False,       # il minuscolo lo fa già normalizza()
        token_pattern=None,    # richiesto quando si passa un tokenizer custom
    )
    X_train = vec.fit_transform(testi_train)
    X_test = vec.transform(testi_test)
    return vec, X_train, X_test


# 🧩 Mini 2.3 — Completa la frase:
#   "Sul train chiamo ____________, su test e produzione chiamo ____________,
#    perché altrimenti commetto ____________."
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 3 — TF-IDF: non tutte le parole valgono uguale
# ==========================================================================
#
# 3.1 Il problema del semplice conteggio
# ---------------------------------------
# Nel nostro corpus la parola "importo" compare quasi ovunque: buste paga,
# CU, estratti conto, fatture. Con il conteggio puro ha un peso alto.
# Ma se compare ovunque, **non distingue niente**: è come una casella
# barrata su tutte le schede.
#
# Le parole utili sono quelle che compaiono TANTO in pochi documenti:
# "cedolino", "irpef", "canone". Quelle ti dicono di che tipo è il documento.
#
#
# 3.2 Le due metà del nome
# -------------------------
# TF-IDF = Term Frequency × Inverse Document Frequency
#
#   TF  (quanto pesa qui)
#       Quante volte la parola compare IN QUESTO documento.
#       Se un documento è lungo si normalizza (es. diviso il totale dei
#       token), altrimenti i testi lunghi vincono sempre.
#
#   IDF (quanto è rara nel mondo)
#       Guarda in quanti documenti DIVERSI compare la parola.
#       - in tutti i documenti  → valore basso (quasi 0): inutile
#       - in pochi documenti    → valore alto: preziosa
#
#   Il prodotto premia: "compare spesso qui, ma raramente altrove".
#
#
# 3.3 Esempio numerico che puoi seguire a mente
# ----------------------------------------------
# Corpus di 4 documenti. Guardiamo due parole:
#
#   "importo"  compare in 4 documenti su 4
#   "cedolino" compare in 1 documento su 4
#
#   IDF ≈ log(numero_documenti / documenti_che_la_contengono)
#
#       importo   → log(4/4) = log(1) = 0        ← peso azzerato
#       cedolino  → log(4/1) = log(4) ≈ 1.39     ← peso alto
#
# Anche se in un documento "importo" compare 5 volte e "cedolino" 1 sola,
# dopo la moltiplicazione per IDF è "cedolino" a contare.
#
# (Le implementazioni reali aggiungono degli "+1" per non dividere per zero
#  e per non azzerare del tutto i pesi: `smooth_idf=True` in sklearn.
#  Il concetto non cambia.)
#
#
# 3.4 La formula, che arriva ULTIMA
# ----------------------------------
# Ora che sai cosa fa, l'etichetta:
#
#     tfidf(t, d) = tf(t, d) * log( N / df(t) )
#
#     t   = termine (la parola)
#     d   = documento
#     N   = numero totale di documenti
#     df  = document frequency = in quanti documenti compare t
#
# Se la formula ti dice meno del paragrafo 3.2, va bene così: la formula è
# il nome, non la cosa.


def idf_a_mano(documenti: list[str]) -> dict[str, float]:
    """Calcola l'IDF di ogni parola del corpus, senza librerie.

    Serve a vedere con i tuoi occhi che le parole comuni finiscono in fondo.
    """
    n_documenti = len(documenti)
    token_per_doc = [set(tokenizza(d)) for d in documenti]

    df = Counter()
    for insieme in token_per_doc:
        df.update(insieme)          # +1 per documento, non per occorrenza

    return {parola: float(np.log(n_documenti / quanti)) for parola, quanti in df.items()}


def mostra_idf_estremi(documenti: list[str], quante: int = 8) -> None:
    """Stampa le parole con IDF più basso (inutili) e più alto (distintive)."""
    idf = idf_a_mano(documenti)
    ordinate = sorted(idf.items(), key=lambda coppia: coppia[1])

    print(f"\n--- {quante} parole PIÙ COMUNI (IDF basso = poco utili) ---")
    for parola, valore in ordinate[:quante]:
        print(f"  {parola:<20} idf={valore:.3f}")

    print(f"\n--- {quante} parole PIÙ RARE (IDF alto = distintive) ---")
    for parola, valore in ordinate[-quante:]:
        print(f"  {parola:<20} idf={valore:.3f}")


def vettorizza_tfidf(testi_train: list[str], testi_test: list[str]):
    """TfidfVectorizer con la stessa disciplina anti-leakage della Sez. 2."""
    vec = TfidfVectorizer(
        tokenizer=tokenizza,
        lowercase=False,
        token_pattern=None,
    )
    X_train = vec.fit_transform(testi_train)
    X_test = vec.transform(testi_test)
    return vec, X_train, X_test


# 🧩 Mini 3.1 — Con 10 documenti, una parola che compare in tutti e 10 che
#   IDF ha (usando log(N/df))? E una che compare in 2?
# TUA RISPOSTA:
#
#
# 🧩 Mini 3.2 — V/F + motivazione: "TF-IDF capisce che 'cedolino' e
#   'busta paga' significano la stessa cosa."
# TUA RISPOSTA:
#
#
# 🧩 Mini 3.3 — Esegui `mostra_idf_estremi(...)` sul CSV del capitolo e
#   incolla qui le 3 parole con IDF più alto. Ti sembrano davvero
#   distintive del tipo di documento? Una riga di commento.
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 4 — Confrontare documenti: la similarità coseno torna utile
# ==========================================================================
#
# Ora che ogni documento è un vettore, "quanto si somigliano due documenti"
# diventa "quanto puntano nella stessa direzione questi due vettori".
#
# È esattamente la funzione del Ponte cap.01 (ripassata in Sez. 0), qui
# applicata a vettori di parole invece che a vettori di feature.
#
# Perché il coseno e non la distanza euclidea: un documento lungo ha
# conteggi grandi. In distanza euclidea sembrerebbe "lontano" da uno corto
# che parla della stessa identica cosa. Il coseno guarda la direzione e
# ignora la lunghezza — che è proprio quello che vogliamo.


def coseno(a: np.ndarray, b: np.ndarray) -> float:
    """Similarità coseno fra due vettori 1D.

    Ritorna un valore in [0, 1] per vettori non negativi come i nostri
    (conteggi e TF-IDF non sono mai negativi).
    """
    if a.shape != b.shape:
        raise ValueError(f"Shape diverse: {a.shape} vs {b.shape}")

    norma_a = float(np.linalg.norm(a))
    norma_b = float(np.linalg.norm(b))
    if norma_a == 0.0 or norma_b == 0.0:
        return 0.0                      # un vettore tutto zeri non ha direzione

    return float(np.dot(a, b) / (norma_a * norma_b))


def documento_piu_simile(query: str, documenti: list[str]) -> tuple[int, float]:
    """Trova l'indice del documento più simile alla query (BoW + coseno).

    Ritorna (indice, punteggio). Se nessuna parola combacia, punteggio 0.
    """
    vocabolario = costruisci_vocabolario(documenti + [query])
    vettore_query = bag_of_words(query, vocabolario)

    punteggi = [
        coseno(vettore_query, bag_of_words(doc, vocabolario))
        for doc in documenti
    ]
    migliore = int(np.argmax(punteggi))
    return migliore, float(punteggi[migliore])


# 🧩 Mini 4.1 — Due righe: perché usiamo il coseno e non la distanza
#   euclidea per confrontare documenti di lunghezza diversa?
# TUA RISPOSTA:
#
#
# 🧩 Mini 4.2 — Nella funzione `coseno` c'è una guardia su norma zero.
#   Quando può succedere davvero, nel nostro dominio?
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 5 — I tre limiti (e perché esiste il capitolo 02)
# ==========================================================================
#
# LIMITE 1 — I sinonimi sono estranei
#     "cedolino" e "busta paga" per BoW/TF-IDF sono parole diverse quanto
#     "cedolino" e "bicicletta". Nessuna nozione di significato: solo
#     stringhe che combaciano o no.
#
# LIMITE 2 — L'ordine non esiste
#     "il netto supera il lordo" e "il lordo supera il netto" → stesso
#     vettore. Nel nostro dominio è grave: la direzione del confronto
#     cambia il senso della frase.
#
# LIMITE 3 — Fuori vocabolario (OOV)
#     Una parola mai vista in training semplicemente non ha una casella.
#     Viene ignorata: informazione persa in silenzio. Con testo OCR, dove
#     un refuso genera parole nuove di continuo, capita spesso.
#
# COSA RISOLVONO GLI EMBEDDINGS (anticipazione onesta, cap.02)
#     Invece di una casella per parola, ogni parola diventa un punto in uno
#     spazio di poche centinaia di dimensioni, imparato dai dati, dove
#     parole usate in contesti simili finiscono VICINE.
#     "cedolino" e "busta paga" si ritrovano nella stessa zona senza che
#     nessuno gliel'abbia detto. Da lì nasce la ricerca semantica, e da
#     quella il RAG del M6.
#
# QUANDO TF-IDF RESTA LA SCELTA GIUSTA
#     - poche centinaia/migliaia di documenti, vocabolario stabile
#     - serve spiegabilità ("ha pesato molto la parola cedolino")
#     - serve velocità, niente GPU, niente dipendenze pesanti
#     - serve una BASELINE onesta contro cui misurare i modelli grossi
#
# 🧩 Mini 5.1 — Per ognuno dei 3 limiti, scrivi un esempio TUO preso dal
#   dominio documentale (non ricopiare i miei).
# TUA RISPOSTA:
# 1)
# 2)
# 3)
#
#
# --------------------------------------------------------------------------
# 📚 LETTURA PARALLELA (facoltativa, 20-30 minuti)
# --------------------------------------------------------------------------
# [NLP-TRANS] (Tunstall, von Werra, Wolf) cap. 1-2: il capitolo 2 mostra la
#   tokenizzazione "moderna" (subword/WordPiece), che è l'evoluzione di
#   quello che hai fatto a mano qui. Leggi solo la parte sulla
#   tokenizzazione: il resto arriva al cap.04-05.
# [ALAMMAR] cap. 2: token ed embedding spiegati con le figure.
#
# Cosa prendere: l'idea che la tokenizzazione è una SCELTA di progetto.
# Cosa lasciare (per ora): tutto ciò che riguarda attention e training.
#
# 🧩 Mini 5.2 — Dopo la lettura, una riga: che problema risolve la
#   tokenizzazione a sotto-parole (subword) rispetto alla nostra a parole?
#   (Suggerimento: rileggi il LIMITE 3.)
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 6 — Mettere tutto insieme sul CSV del capitolo
# ==========================================================================

def carica_dati() -> pd.DataFrame:
    """Legge il CSV sintetico del capitolo. Colonne: id, tipo, testo."""
    if not PERCORSO_DATI.exists():
        raise FileNotFoundError(
            f"Manca {PERCORSO_DATI}. Dovrebbe essere arrivato con il capitolo."
        )
    return pd.read_csv(PERCORSO_DATI)


def pipeline_dimostrativa() -> None:
    """Percorso completo: dati → token → BoW → TF-IDF → similarità.

    Esegui questa funzione DOPO aver letto le sezioni: serve a vedere in
    output le cose che hai appena studiato.
    """
    dati = carica_dati()
    testi = dati["testo"].tolist()

    print("=" * 70)
    print(f"Documenti caricati: {len(testi)} — tipi: {dati['tipo'].unique().tolist()}")

    print("\n--- 1. Tokenizzazione del primo documento ---")
    print("originale :", testi[0])
    print("normalizz.:", normalizza(testi[0]))
    print("token     :", tokenizza(testi[0]))

    print("\n--- 2. Vocabolario ---")
    vocabolario = costruisci_vocabolario(testi)
    print(f"parole distinte: {len(vocabolario)}")

    print("\n--- 3. Sparsità del primo vettore BoW ---")
    vettore = bag_of_words(testi[0], vocabolario)
    print(f"lunghezza vettore: {len(vettore)} — celle non zero: {int((vettore > 0).sum())}")

    print("\n--- 4. IDF: parole inutili vs parole distintive ---")
    mostra_idf_estremi(testi, quante=5)

    print("\n--- 5. Documento più simile a una query ---")
    query = "cedolino con netto in busta e trattenute irpef"
    indice, punteggio = documento_piu_simile(query, testi)
    print(f"query    : {query}")
    print(f"risposta : [{dati.loc[indice, 'tipo']}] {testi[indice]}")
    print(f"coseno   : {punteggio:.3f}")
    print("=" * 70)


# 🧩 Mini 6.1 — Esegui `pipeline_dimostrativa()`. Il documento restituito al
#   punto 5 è del tipo che ti aspettavi? Scrivi 2 righe: cosa ha funzionato
#   e quale parola secondo te ha pesato di più.
# TUA RISPOSTA:
#
#


# ==========================================================================
# QUIZ DI VERIFICA
# ==========================================================================
#
# V1 — Prevedi l'output
#   documenti = ["saldo saldo", "saldo netto"]
#   vocabolario = costruisci_vocabolario(documenti)
#   print(bag_of_words("saldo canone", vocabolario))
#   Cosa stampa e perché "canone" non compare?
# TUA RISPOSTA:
#
#
# V2 — V/F + motivazione
#   "Se una parola compare in tutti i documenti del corpus, con TF-IDF il suo
#    peso tende a zero."
# TUA RISPOSTA:
#
#
# V3 — Trova l'errore
#   vec = TfidfVectorizer()
#   X = vec.fit_transform(tutti_i_testi)          # train + test insieme
#   X_train, X_test = X[:24], X[24:]
#   Cosa c'è di sbagliato, come si chiama il problema, e come lo correggi?
# TUA RISPOSTA:
#
#
# V4 — Completa il codice
#   Vuoi la similarità fra due documenti già vettorizzati `v1` e `v2`:
#       similarita = np.dot(v1, v2) / ( __________ * __________ )
# TUA RISPOSTA:
#
#
# V5 — Definizione (2 righe, senza formule)
#   Cos'è l'IDF e a cosa serve?
# TUA RISPOSTA:
#
#
# V6 — 💬 Feynman (5-7 righe)
#   Spiega a un collega sviluppatore web, che non ha mai fatto NLP, come si
#   trasforma un testo in numeri e perché non basta contare le parole.
#   Vincoli: niente formule, niente parola "vettorializzazione", e almeno
#   un'analogia tua.
# TUA RISPOSTA:
#
#
# V7 — Ragionamento di dominio (3 bullet)
#   Il tuo classificatore di tipo documento va benissimo in test (95%) e
#   male in produzione. Indica TRE cause plausibili legate a questo
#   capitolo (non al modello). Una per bullet, con il controllo che faresti.
# TUA RISPOSTA:
# -
# -
# -
#
#
# V8 — Scelta tecnica motivata (2 righe)
#   Un collega propone: "togliamo tutti i numeri dal testo, tanto sono
#   rumore". Rispondi: sei d'accordo? Cosa proponi al posto suo?
# TUA RISPOSTA:
#
#


# ==========================================================================
# ESERCIZI
# ==========================================================================
#
# --------------------------------------------------------------------------
# TODO 1 — 🔄 [RECALL CROSS-MODULO] (Regola 26)
# --------------------------------------------------------------------------
# Senza guardare il M2: costruisci una baseline completa di classificazione
# del TIPO di documento, partendo dal CSV del capitolo.
#
# Passi richiesti:
#   a) carica il CSV, separa X (testo) e y (tipo)
#   b) train/test split stratificato (il M2 ti ha insegnato perché stratificato)
#   c) TfidfVectorizer + LogisticRegression, con `fit` SOLO sul train
#   d) stampa accuracy e le metriche per classe
#   e) una riga di commento: l'accuracy qui è affidabile? Perché?
#
# Vincolo: usa una `Pipeline` di scikit-learn, come nel M2 cap.05.
# Suggerimento anti-leakage: se il vettorizzatore sta dentro la Pipeline,
# il problema si risolve da solo. Spiega nel commento perché.
# TUO CODICE:


# --------------------------------------------------------------------------
# TODO 2 — 🎯 [COLLOQUIO] (formato: esattamente 4 bullet, uno per domanda)
# --------------------------------------------------------------------------
# ⚠️ Pattern #6 — leggi la consegna due volte: sono QUATTRO domande distinte
# e vogliono QUATTRO bullet separati. Prima di scrivere, elencale.
#
#   1. "Cos'è TF-IDF?" — spiegalo in 2 frasi a un tecnico
#   2. "Quando useresti TF-IDF invece degli embeddings?" — dai UN criterio
#      concreto, non "dipende"
#   3. "Che problema ha il Bag of Words?" — cita il limite che consideri
#      più grave e perché
#   4. "Come gestisci una parola mai vista in produzione?" — cosa succede
#      di default e cosa puoi fare
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)


# --------------------------------------------------------------------------
# TODO 3 — 🔧 [REFACTORING]
# --------------------------------------------------------------------------
# Codice che funziona ma è da riscrivere:
#
#     def prepara(testi):
#         risultato = []
#         for t in testi:
#             t = t.lower()
#             t = t.replace(",", "")
#             t = t.replace(".", "")
#             t = t.replace(";", "")
#             t = t.replace("-", "")
#             parole = t.split(" ")
#             pulite = []
#             for p in parole:
#                 if p != "" and p != "il" and p != "la" and p != "di":
#                     pulite.append(p)
#             risultato.append(pulite)
#         print("fatto", len(risultato))
#         return risultato
#
# Riscrivila. Devi risolvere almeno QUATTRO problemi diversi (non quattro
# volte lo stesso). Elencali prima in commento, poi scrivi il codice.
# Attenzione: uno dei problemi è di DOMINIO, non di stile — quel
# `replace(",", "")` sul nostro testo fa un danno preciso. Quale?
# TUA ANALISI:
# -
# -
# -
# -
# TUO CODICE:


# --------------------------------------------------------------------------
# TODO 4 — 🔍 [DEBUG] — nessun aiuto, trovalo da solo
# --------------------------------------------------------------------------
# Un collega ti manda questo codice e dice: "il modello in produzione
# risponde sempre con la stessa classe, ma in test andava benissimo".
#
#     # training (notebook di gennaio)
#     vec = TfidfVectorizer(tokenizer=tokenizza, lowercase=False, token_pattern=None)
#     X = vec.fit_transform(testi_train)
#     modello.fit(X, y_train)
#     joblib.dump(modello, "modello.pkl")
#
#     # produzione (servizio di marzo)
#     modello = joblib.load("modello.pkl")
#     vec = TfidfVectorizer(tokenizer=tokenizza, lowercase=False, token_pattern=None)
#     X_nuovo = vec.fit_transform([testo_in_arrivo])
#     predizione = modello.predict(X_nuovo)
#
# Domande:
#   a) qual è il bug? (una frase)
#   b) perché in test non si vedeva? (una frase)
#   c) come si ripara? (una frase operativa)
#   d) 🔁 collega: a quale errore del M3 cap.10 assomiglia questo?
# TUA RISPOSTA:
# a)
# b)
# c)
# d)


# --------------------------------------------------------------------------
# TODO 5 — 🧠 [RETRIEVAL] — a freddo, senza scorrere in su
# --------------------------------------------------------------------------
# Riscrivi da zero, senza guardare la Sez. 4, la funzione:
#
#     def coseno(a, b) -> float
#
# Requisiti: controllo delle shape, guardia sulla divisione per zero,
# nessun import oltre numpy. Poi verifica con un `assert` che il coseno di
# un vettore con se stesso sia 1.0 (a meno di errori di arrotondamento).
# TUO CODICE:


# --------------------------------------------------------------------------
# TODO 6 — 🔀 [INTERLEAVING] — testo + tabellare + visivo
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — cosa hai già in pipeline
#   M2: un classificatore su feature tabellari che produce `prob_alterato`
#       e, da lì, `score_genuinita` e il `semaforo`.
#   M3: un classificatore visivo che, sui documenti veri, produrrà
#       `prob_busta_paga_visivo` guardando il layout dell'immagine.
#   Entrambi restituiscono numeri fra 0 e 1, entrambi hanno una soglia
#   scelta sul validation, entrambi possono sbagliare.
#
# Ora arriva il ramo testuale di questo capitolo: `prob_tipo_doc_testuale`.
#
# Rispondi in 4 bullet:
#   1. I tre segnali (tabellare, visivo, testuale) possono essere in
#      disaccordo sullo stesso documento: fai un esempio concreto.
#   2. Chi vince? Proponi una regola e dichiara il criterio.
#   3. Quale dei tre è più facile da spiegare all'operatore, e perché?
#   4. Quale dei tre rischia di più con un documento fotografato storto?
# TUA RISPOSTA:
# 1)
# 2)
# 3)
# 4)


# --------------------------------------------------------------------------
# TODO 7 — Esperimento guidato (serve a vedere, non a scrivere molto)
# --------------------------------------------------------------------------
# Prendi due frasi con le stesse parole ma ordine invertito:
#
#     a = "il netto supera il lordo"
#     b = "il lordo supera il netto"
#
# a) calcola il coseno fra i loro vettori BoW e incolla il risultato
# b) spiega in una riga perché esce quel numero
# c) in una riga: che tipo di modello servirebbe per distinguerle?
# TUA RISPOSTA:
# a)
# b)
# c)


# --------------------------------------------------------------------------
# 🏗️ PROGETTO INCREMENTALE — il ramo testuale nasce qui
# --------------------------------------------------------------------------
#
# Contesto prodotto: "Controllo Documentale AI" ha già il cuore tabellare
# (M2) e il ramo visivo (M3). Questo modulo aggiunge il ramo TESTUALE:
# capire cosa c'è scritto dentro un documento OCR.
#
# Il capitolo 01 posa le fondamenta: la normalizzazione del testo.
# Se questa è fragile, tutto il modulo lo sarà.
#
#   [ ] T1 — Crea `modulo_04_nlp/testo_utils.py` e spostaci, ripulite:
#            `normalizza`, `tokenizza`, `STOPWORD_IT` e le regex.
#            DoD: `from testo_utils import tokenizza` funziona, e il file
#                 non stampa nulla quando viene importato.
#
#   [ ] T2 — Aggiungi due segnaposto in più, utili sul dominio reale:
#            `<cf>` per qualcosa che sembra un codice fiscale (16 caratteri
#            alfanumerici) e `<iban>` per una stringa che inizia con IT.
#            DoD: un testo con un CF finto produce il token `<cf>` e il
#                 codice originale NON compare fra i token.
#            Nota privacy: questo è anche un mini-anonimizzatore.
#
#   [ ] T3 — Scrivi `classifica_tipo_documento(testo) -> dict` che usa la
#            Pipeline del TODO 1 e restituisce:
#                {"tipo": "busta_paga", "prob_tipo_doc_testuale": 0.87,
#                 "parole_decisive": ["cedolino", "irpef", "netto"]}
#            DoD: le tre chiavi ci sono; `parole_decisive` contiene parole
#                 che compaiono davvero nel testo in input.
#
#   [ ] T4 — Spiegabilità onesta: `parole_decisive` è l'equivalente
#            testuale dei `motivi_top3` del M2. Scrivi 3 righe nel diario
#            del capitolo: cosa promette all'operatore e cosa NON promette.
#
#   [ ] T5 — Salva accanto al modello un piccolo **contratto** (dizionario
#            o JSON) con: versione, elenco classi ordinate, nome del
#            tokenizer usato, data di training.
#            DoD: lo stesso ragionamento del contratto di inferenza del M3
#                 cap.10, applicato al testo. Se cambi tokenizer, la
#                 versione cambia.
#
# Deliverable del capitolo: `testo_utils.py` + funzione di classificazione
# + contratto. Diventeranno la base del matching semantico (cap.03) e
# dell'estrazione campi (cap.05-06).


# ==========================================================================
# SOLUZIONI — leggile solo dopo aver scritto le tue
# ==========================================================================
#
# Dove c'è una rubrica non esiste una formulazione unica giusta: conta che
# compaiano gli elementi elencati.
#
# --- Quiz d'ingresso ------------------------------------------------------
# Q1  `fit` impara i parametri dai dati (es. media e deviazione standard);
#     `transform` li applica ai dati, senza reimpararli.
# Q2  Falso. Anche senza etichette, le statistiche del test entrano nel
#     preprocessing → leakage: la valutazione diventa ottimistica.
# Q3  Il modello riceveva input diverso da quello su cui è stato addestrato:
#     nessun errore, solo predizioni peggiori. Pericoloso perché silenzioso.
# Q4  (30, 400). La cella [5, 12] = quante volte la parola numero 12 del
#     vocabolario compare nel documento numero 5.
# Q5  Quanto due vettori puntano nella stessa direzione. Vicino a 1 =
#     direzione quasi identica; vicino a 0 = direzioni indipendenti.
# Q6  5 voci: ['netto', 'in', 'busta', '1.703,45', 'eur'].
#     "1.703,45" non è una parola: è un importo, e da solo è inutile.
# Q7  Nessuna risposta sbagliata: serve solo come confronto a fine capitolo.
#
# --- Mini ----------------------------------------------------------------
# 0.1  Il vocabolario: quali parole esistono e in che posizione stanno.
# 0.2  Falso: il coseno normalizza per la lunghezza, quindi la differenza di
#      lunghezza da sola non abbassa il punteggio.
# 0.3  La pipeline di testo (normalizzazione, tokenizer, stopword) +
#      il vocabolario: devono viaggiare insieme al modello, altrimenti in
#      produzione i vettori non combaciano.
# 1.1  ['cedolino', 'paga', '<data>', 'importo', '<importo>', 'eur']
#      (l'ordine segue il testo; "del"/"per"/"di" sono stopword, "l" cade
#      perché lungo 1).
# 1.2  (a) `replace(".", "")` distrugge il separatore delle migliaia:
#          "1.703,45" → "1703,45" e comunque resta un token inutile;
#      (b) split(" ") lascia attaccata la punteggiatura rimanente
#          ("eur;", "netto.") creando doppioni nel vocabolario.
# 1.3  Modello: la presenza di un importo è informativa, il valore esatto no
#      (comparirebbe una volta sola → inutile e rumoroso).
#      Privacy: il numero specifico sparisce dal vocabolario e dai log.
# 2.1  4 colonne (busta, canone, netto, saldo). "netto" vale 2 in d1 perché
#      compare due volte in quel documento.
# 2.2  [0, 2, 0, 0] — "sconosciuto" non è nel vocabolario e viene ignorato.
# 2.3  fit_transform ; transform ; data leakage.
# 3.1  Compare in tutti e 10 → log(10/10) = 0. Compare in 2 → log(10/2) ≈ 1.61.
# 3.2  Falso: sono due stringhe diverse, TF-IDF non ha nozione di significato.
#      È il LIMITE 1 della Sez. 5 e il motivo del cap.02.
# 3.3  Rubrica: va bene qualunque risposta che noti se le parole con IDF alto
#      sono davvero legate a un solo tipo di documento (es. "canone",
#      "visura") oppure solo rumore raro.
# 4.1  Perché il coseno guarda la direzione e non la lunghezza: un documento
#      lungo ha conteggi grandi, e con la distanza euclidea risulterebbe
#      lontano da uno corto sullo stesso argomento.
# 4.2  Quando un documento, dopo normalizzazione e stopword, non ha nessun
#      token nel vocabolario: testo vuoto, OCR fallito, o solo numeri.
# 5.1  Rubrica: 3 esempi di dominio, uno per limite. Esempi accettabili —
#      sinonimi: "cedolino" vs "prospetto paga"; ordine: "saldo supera il
#      fido" vs "il fido supera il saldo"; OOV: refuso OCR "cedoIino" con
#      la I maiuscola al posto della elle.
# 5.2  La tokenizzazione a sotto-parole non ha (quasi) parole fuori
#      vocabolario: una parola mai vista viene spezzata in pezzi noti.
# 6.1  Rubrica: dovrebbe rispondere una busta paga; le parole che pesano
#      sono quelle con IDF alto presenti nella query (cedolino, irpef).
#
# --- Quiz di verifica -----------------------------------------------------
# V1  Vocabolario = {netto: 0, saldo: 1} → stampa [0. 1.].
#     "canone" non ha una casella: è fuori vocabolario, viene ignorato.
# V2  Vero: df = N → log(N/N) = 0 → il peso si annulla (con smooth_idf resta
#     molto piccolo ma non esattamente zero).
# V3  `fit_transform` su train + test insieme: il vocabolario e gli IDF
#     vedono anche il test. È data leakage. Fix: `fit_transform` solo sul
#     train, `transform` sul test — o meglio, vettorizzatore dentro una
#     Pipeline valutata in cross-validation.
# V4  np.linalg.norm(v1) * np.linalg.norm(v2)
# V5  Rubrica: misura quanto una parola è rara nel corpus; serve ad abbassare
#     il peso delle parole che compaiono ovunque (che non distinguono nulla)
#     e ad alzare quello delle parole distintive.
# V6  Rubrica (almeno 4 elementi): (1) il computer lavora su numeri, non su
#     lettere; (2) si fa una lista di tutte le parole e si conta quante volte
#     compaiono → ogni documento diventa una riga di numeri; (3) contare non
#     basta perché le parole comuni compaiono ovunque e non distinguono;
#     (4) si pesano le parole rare; (5) resta il problema che sinonimi e
#     ordine non vengono capiti; (6) analogia personale presente.
#     Se compare la parola "vettorializzazione" o una formula: vincolo violato.
# V7  Rubrica (3 cause di preprocessing, non di modello):
#     - tokenizer diverso fra training e produzione → controllo: tokenizza lo
#       stesso testo nei due ambienti e confronta le liste;
#     - vocabolario rifatto in produzione invece che caricato → controllo:
#       verifica che il vettorizzatore sia quello salvato (stessa dimensione
#       di vocabolario);
#     - testo di produzione più sporco del corpus di training (OCR peggiore,
#       refusi, maiuscole) → controllo: campiona 20 testi reali e guarda
#       quante parole finiscono fuori vocabolario;
#     - variante accettabile: distribuzione delle classi diversa (ma è più
#       vicina al modello che al preprocessing).
# V8  Rubrica: non d'accordo in blocco. Il valore esatto è rumore, ma la
#     PRESENZA di importi e date è informativa → sostituire con segnaposto
#     `<importo>` / `<data>`, che tra l'altro aiuta la privacy.
#
# --- TODO (tracce) --------------------------------------------------------
# TODO 1  Impianto atteso:
#           Pipeline([("tfidf", TfidfVectorizer(tokenizer=tokenizza,
#                                               lowercase=False,
#                                               token_pattern=None)),
#                     ("clf", LogisticRegression(max_iter=1000))])
#         train_test_split(..., stratify=y, random_state=42);
#         `pipe.fit(X_train, y_train)`; poi `classification_report`.
#         Commento (e): con 30 documenti e 4 classi l'accuracy è
#         indicativa, non affidabile — il test ha pochissimi esempi per
#         classe. Sul leakage: con il vettorizzatore dentro la Pipeline,
#         `fit` lo vede solo sul train, anche dentro la cross-validation.
# TODO 2  1) TF-IDF pesa le parole in base a quanto sono frequenti nel
#            documento e rare nel corpus. 2) Criterio concreto: corpus
#            piccolo/stabile, serve spiegabilità o CPU-only → TF-IDF; serve
#            capire sinonimi e parafrasi → embeddings. 3) Limite più grave:
#            nessuna nozione di significato (sinonimi) — oppure la perdita
#            dell'ordine, se motivata. 4) Di default la parola viene
#            ignorata (OOV); si può ridurre il problema con segnaposto,
#            tokenizzazione a sotto-parole o riaddestramento periodico.
# TODO 3  I quattro problemi: (a) catena di `replace` → una regex sola;
#         (b) `split(" ")` → tokenizzazione con regex; (c) stopword in una
#         catena di `!=` → un `set` (ricerca O(1), estendibile);
#         (d) `print` dentro una funzione di libreria → va rimosso, la
#         funzione deve solo restituire. Problema di DOMINIO: togliendo
#         virgole e punti, "1.703,45" diventa "170345" — un numero inventato
#         che non esiste nel documento.
# TODO 4  a) In produzione viene creato un NUOVO vettorizzatore e rifatto il
#            `fit` su un solo testo: vocabolario e IDF sono completamente
#            diversi da quelli del training, quindi le colonne non
#            corrispondono più ai pesi del modello.
#         b) In test vettorizzatore e modello venivano dallo stesso
#            processo, quindi combaciavano.
#         c) Salvare il vettorizzatore insieme al modello (o l'intera
#            Pipeline) e in produzione fare solo `transform`.
#         d) È il gemello testuale del preprocess incoerente del cap.10
#            (mean/std diversi) e dell'ordine classi riscritto a mano:
#            un bug che non crasha.
# TODO 5  Rubrica: controllo shape, guardia norma zero, uso di
#         `np.linalg.norm`, assert con `np.isclose(coseno(v, v), 1.0)`.
# TODO 6  Rubrica: (1) esempio concreto di disaccordo, es. testo che dice
#         "cedolino" ma layout anomalo perché il PDF è stato rigenerato;
#         (2) regola dichiarata, es. il testuale decide il TIPO, il visivo e
#         il tabellare concorrono all'alterazione, con pesi espliciti;
#         (3) il testuale è il più spiegabile (parole con un nome umano,
#         come i motivi_top3 del M2); (4) il visivo soffre di più con foto
#         storte — ma anche l'OCR peggiora, ed è una risposta accettabile
#         se motivata.
# TODO 7  a) 1.0 (o 0.999…). b) Le due frasi hanno esattamente le stesse
#         parole con le stesse frequenze: BoW non vede l'ordine, quindi i
#         vettori sono identici. c) Serve un modello che tenga conto della
#         sequenza e del contesto: da qui embeddings contestuali e
#         Transformer (cap.02 e cap.04).


if __name__ == "__main__":
    # Esegui il file per vedere la pipeline in azione:
    #     python 01_testo_come_numeri.py
    #
    # Studiare il capitolo però si fa leggendo dall'alto e scrivendo le
    # risposte: l'output serve solo a confermare quello che hai capito.
    demo_bow_a_mano()
    print()
    pipeline_dimostrativa()
