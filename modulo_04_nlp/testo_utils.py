from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path
import os
import joblib
import numpy as np
from numpy.typing import NDArray
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score
)
from datetime import datetime

# ===== PROGETTO INCREMENTALE CAPITOLO 1 =====

QUI = Path(__file__).resolve().parent
PERCORSO_DATI = QUI / "dati" / "note_documenti.csv"
PERCORSO_MAPPA = QUI / "dati" / "mappe" / "mappa.pkl"
PERCORSO_CONTRATTO =  QUI / "dati" / "contratti" / "contratto.pkl"
MIN_CONTEGGIO = 2
DIM = 4
DIM_DISEGNO = 2


RE_DATA = re.compile(r"\b\d{1,2}[/-]\d{1,2}([/-]\d{2,4})?\b")

RE_IMPORTO = re.compile(r"\b\d{1,3}(\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b")

RE_CF = re.compile(r"\b[a-z]{6}\d{2}[a-z]\d{2}[a-z]\d{3}[a-z]\b")

RE_IBAN = re.compile(r"\bit\d{2}[a-z]\d{10}[a-z0-9]{12}\b")

RE_TOKEN = re.compile(r"[a-zàèéìòù<>]+")

VERSIONE = "1.2"


STOPWORD_IT = {
    "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "del", "dello", "della", "dei", "degli", "delle",
    "al", "allo", "alla", "ai", "agli", "alle",
    "dal", "dalla", "nel", "nella", "sul", "sulla",
    "e", "ed", "o", "che", "non", "si", "come", "anche",
}

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
    testo = RE_CF.sub(" <cf> ", testo)
    testo = RE_IBAN.sub(" <iban> ", testo)
    return testo


def tokenizza(testo: str, togli_stopword: bool = True) -> list[str]:
    """Testo (già normalizzato o no) → lista di token puliti.

    Sceglie i token con una regex invece che con split():
    così punteggiatura, apostrofi e trattini non si appiccicano alle parole.
    """
    testo = normalizza(testo)
    token = RE_TOKEN.findall(testo)
    token = [t for t in token if len(t) > 1]
    if togli_stopword:
        token = [t for t in token if t not in STOPWORD_IT]
    return token

def prepara_modello(percorso_csv: str, versione: str = VERSIONE):
    dati = pd.read_csv(percorso_csv)
    
    X = dati.drop(columns=["id","tipo"])
    y = dati['tipo']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state=42,
        test_size=.2,
        stratify=y)

    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(tokenizer=tokenizza, token_pattern=None, lowercase=False)),
        ('clf', LogisticRegression(random_state=42, max_iter=1_000))
    ])

    pipe.fit(X_train['testo'], y_train)
    y_pred = pipe.predict(X_test['testo'])

    acc_score = accuracy_score(y_test, y_pred)
    classi = y_test.unique()
    rec_prec_classi = {}
    for c in classi:
        tp = len(y_test[(y_pred == c) & (y_test == c)])
        fn = len(y_test[(y_pred != c) & (y_test == c)])
        fp = len(y_test[(y_pred == c) & (y_test != c)])
        rec = tp / (tp + fn) if (tp + fn) != 0 else 0.0
        prec = tp / (tp + fp) if (tp + fp) != 0 else 0.0
        rec_prec_classi[c] = {"recall": rec, "precision": prec}
        
    return {
        "pipe": pipe,
        "accuracy": acc_score,
        "metriche_per_classe": rec_prec_classi,
        "versione": versione,
        "classi": sorted(pipe.named_steps["clf"].classes_),
        "tokenizer": tokenizza.__name__,
        "data_training": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    

def classifica_tipo_documento(query: str, pipe: Pipeline) -> dict[str, str | float]:
    
    y_pred = pipe.predict([query])
    y_pred_proba = pipe.predict_proba([query])
    
    tipo = y_pred[0]
    classi = list(pipe.named_steps["clf"].classes_)
    i = classi.index(tipo)
    prob = float(y_pred_proba[0, i])
    nomi = pipe.named_steps["tfidf"].get_feature_names_out()
    pesi = pipe.named_steps["clf"].coef_[i]
    presenti = set(tokenizza(query))
    coppie = [
        (nomi[j], pesi[j])
        for j in range(len(nomi))
        if nomi[j] in presenti
    ]
    coppie.sort(key=lambda t: t[1], reverse=True)
    parole_decisive = [parola for parola, _peso in coppie[:3]]
        
    return {
        "tipo": tipo,
        "prob_tipo_doc_testuale": prob,
        "parole_decisive": parole_decisive
        
    }

query = (
    "Cedolino paga di Mario Rossi, CF RSSMRA85T10H501Z, IBAN IT60X0542811101000000123456, netto 1.850,00 EUR il 01/03/2026."
)

# ===== PROGETTO INCREMENTALE CAPITOLO 2 =====


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
    conteggi = Counter(parola for documento in corpus for parola in documento)
    return sorted(p for p, c in conteggi.items() if c >= min_conteggio)


def matrice_co_occorrenze(corpus: list[list[str]], vocabolario: list[str]) -> np.ndarray:
    """Passo 2 — in quanti documenti ogni coppia di parole compare insieme."""
    posizione = {parola: i for i, parola in enumerate(vocabolario)}

    conteggi = np.zeros((len(vocabolario), len(vocabolario)))
    
    for documento in corpus:
        presenti = sorted({p for p in documento if p in posizione})
        for a in presenti:
            for b in presenti:
                if a != b:
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
    U, valori_singolari, _ = np.linalg.svd(pesata, full_matrices=False)
    return U[:, :dim] * valori_singolari[:dim]


def costruisci_mappa(percorso=PERCORSO_DATI,
                     dim: int = DIM,
                     min_conteggio: int = MIN_CONTEGGIO) -> dict[str, np.ndarray]:
    """I quattro passi in fila. Restituisce {parola: vettore}.

    Questa è la funzione da portare in `testo_utils.py` nel progetto.
    """
    corpus = carica_corpus(percorso)
    vocabolario = costruisci_vocabolario(corpus, min_conteggio)
    coppie = matrice_co_occorrenze(corpus, vocabolario)
    pesata = pesa_ppmi(coppie)
    coordinate = riduci(pesata, dim)
    
    return {parola: coordinate[i] for i, parola in enumerate(vocabolario)}

def vettore_frase(testo: str, mappa: dict[str, np.ndarray]) -> np.ndarray:
    """Punto medio delle parole conosciute. Vettore di zeri se non ne trova.
    È il `transform` della mappa: LEGGE la mappa, non la ricalcola.
    """
    dim = len(next(iter(mappa.values())))
    punti = [mappa[parola] for parola in tokenizza(testo) if parola in mappa]
    if not punti:
        return np.zeros(dim)
    return np.mean(punti, axis=0)

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


def salva_mappa(mappa, percorso_mappa = PERCORSO_MAPPA):
    joblib.dump(mappa, percorso_mappa)

def carica_mappa(percorso_mappa = PERCORSO_MAPPA):
    return joblib.load(percorso_mappa)

def salva_contratto(contratto_vecchio: dict[str, object], percorso_contratto = PERCORSO_CONTRATTO):
    contratto_nuovo = {}
    for k, v in contratto_vecchio.items():
        if k not in ["pipe", "accuracy", "metriche_per_classe"]:
            contratto_nuovo[k] = v
    # se si ricostruisce a 8 dimensioni, i vettori presenti nel database vanno ricalcolati (sono a 4 dimensioni). 
    contratto_nuovo['mappa_dim'] = DIM
    contratto_nuovo['mappa_min_conteggio'] = MIN_CONTEGGIO
    mappa = carica_mappa()
    contratto_nuovo['mappa_n_parole'] = len(mappa)
    joblib.dump(contratto_nuovo, percorso_contratto)
        

if __name__ == "__main__":
    mappa = carica_mappa()
    frase = "cedolino netto irpef"
    v = vettore_frase(frase, mappa)

    assert v.shape == (DIM,)
    assert abs(coseno(v, v) - 1.0) < 1e-9
    vuoto = vettore_frase("xyzzyq qwxzplm", mappa)
    assert coseno(vuoto, v) == 0.0
    

