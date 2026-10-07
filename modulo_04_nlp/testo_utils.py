from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path
import os

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

QUI = Path(__file__).resolve().parent
PERCORSO_DATI = QUI / "dati" / "note_documenti.csv"


RE_DATA = re.compile(r"\b\d{1,2}[/-]\d{1,2}([/-]\d{2,4})?\b")

RE_IMPORTO = re.compile(r"\b\d{1,3}(\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b")

RE_CF = re.compile(r"\b[a-z]{6}\d{2}[a-z]\d{2}[a-z]\d{3}[a-z]\b")

RE_IBAN = re.compile(r"\bit\d{2}[a-z]\d{10}[a-z0-9]{12}\b")

RE_TOKEN = re.compile(r"[a-zàèéìòù<>]+")

# Ricetta del testo. Se cambi tokenizza, le regex o le stopword, alza il numero.
VERSIONE = "1.1"

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

if __name__ == "__main__":

    pipe = prepara_modello(PERCORSO_DATI)

    prova = classifica_tipo_documento(query, pipe["pipe"])

    print(prova)

