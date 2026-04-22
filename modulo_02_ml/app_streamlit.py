"""
Demo Streamlit — Modulo 2 (Cap.06)

Questa è la "base di partenza" per gli esercizi del capitolo 06.
La completi passo-passo seguendo `06_progetto_streamlit.py`.
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def calcola_score_genuinita_da_prob_alterato(prob_alterato: float) -> float:
    return (1 - prob_alterato) * 100


def semaforo_da_score(score_genuinita: float) -> str:
    if score_genuinita >= 85:
        return "verde"
    if score_genuinita >= 60:
        return "giallo"
    return "rosso"


@st.cache_data
def carica_pratiche_mock() -> pd.DataFrame:
    path_csv = os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv")
    return pd.read_csv(path_csv)


st.set_page_config(page_title="Demo genuinità documenti (M2)", layout="wide")

st.title("Demo genuinità documenti (Modulo 2)")
st.write(
    "Seleziona una pratica e guarda `prob_alterato` (0–1), `score_genuinita` (0–100) e semaforo."
)

pratiche = carica_pratiche_mock()

with st.sidebar:
    st.header("Selezione pratica")
    pratica_id = st.selectbox("pratica_id", sorted(pratiche["pratica_id"].unique().tolist()))
    st.divider()
    st.header("Validazione (cap.05)")
    mostra_cv = st.checkbox("Mostra CV recall (media ± std)", value=True)


riga = pratiche.loc[pratiche["pratica_id"] == pratica_id].iloc[0]

st.subheader("Dati pratica (riga selezionata)")
st.dataframe(pd.DataFrame([riga]))

# TODO (Esercizio 3): sostituisci questo placeholder con una predizione vera
# usando LogisticRegression + StandardScaler.
#
# Per ora: simuliamo una probabilità finta solo per vedere la UI.
prob_alterato = 0.5

score_genuinita = calcola_score_genuinita_da_prob_alterato(prob_alterato)
semaforo = semaforo_da_score(score_genuinita)

col1, col2, col3 = st.columns(3)
col1.metric("prob_alterato (0–1)", f"{prob_alterato:.3f}")
col2.metric("score_genuinita (0–100)", f"{score_genuinita:.1f}")
col3.metric("semaforo", semaforo)

if mostra_cv:
    st.subheader("Stabilità (Cross-Validation) — recall sugli alterati")
    st.caption("CV fatta SOLO su train, con Pipeline per evitare leakage dello scaler dentro i fold.")

    X = pratiche.drop(columns=["pratica_id", "y_alterato"])
    y = pratiche["y_alterato"]

    X_train, _X_test, y_train, _y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    rec_scores = cross_val_score(pipe, X_train, y_train, cv=kfold, scoring="recall")

    st.write("Recall per fold:", np.round(rec_scores, 3))
    st.write(f"Media recall: {rec_scores.mean():.3f}  |  Dev std: {rec_scores.std():.3f}")

    # TODO (Esercizio 5): spiega in testo UI perché mostrare media±std è più onesto di un numero singolo.
    st.info(
        "Nota: la media ti dà una stima più stabile; la dev std ti dice quanto lo score varia tra split diversi."
    )

