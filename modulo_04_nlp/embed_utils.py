"""Embedding MiniLM — progetto incrementale 02b (T1–T5)."""

from __future__ import annotations

from pathlib import Path

from testo_utils import (
    PERCORSO_DATI,
    PERCORSO_CONTRATTO,
    tokenizza
)

import numpy as np
import joblib
import pandas as pd
import sys

QUI = Path(__file__).resolve().parent
PERCORSO_VETTORI = QUI / "dati" / "mappe" / "note_minilm.pkl"
MODELLO_ST = "paraphrase-multilingual-MiniLM-L12-v2"
DIM_MINILM = 384


def carica_modello_frasi(nome: str = MODELLO_ST):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(nome)


def embedda(testi, modello, normalizza: bool = False) -> np.ndarray:    
    if isinstance(testi, str):
        testi = [testi]
    vettori = modello.encode(
        testi,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=normalizza,
    )
    return np.asarray(vettori)

def rischio_troncamento(modello, testi)-> None:
    tokenizer = modello.tokenizer
    max_token = int(modello.max_seq_length)
    token = []
    for i, t in enumerate(testi):
        n_token = len(tokenizer.tokenize(t))
        if n_token + 2 > max_token:            
            token.append((i, n_token))
            print(f"Indice nota troncata: {i} -> troncati {n_token - max_token + 2} n token")
    if len(token) == 0:
        print("Nessuna nota troncata")    


def embedda_note(modello, percorso = PERCORSO_DATI, normalizza: bool = True) -> np.ndarray:
    testi = pd.read_csv(percorso)['testo'].tolist()
    rischio_troncamento(modello, testi)
    return embedda(testi, modello, normalizza=normalizza)


def salva_vettori(E, percorso_vettore=PERCORSO_VETTORI) -> None:
    percorso_vettore.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(E, percorso_vettore)
    
    
def carica_vettori(percorso_vettore=PERCORSO_VETTORI) -> np.ndarray:
    return joblib.load(percorso_vettore)


def aggiorna_contratto_minilm(E, nome_modello, max_seq_length) -> None:
    """
    Non si confrontano per perchè sono coordianate di spazi diversi,
    oltre ad essere inconfrontabili per via della differenza di shape.
    Il nome del modello va salvato perchè, anche se due modelli producono
    vettori di uguale dimensione, ogni modello crea delle coordinate diverse,
    e rappresentano lo spazio semantico multidimensionale in modo diverso.
    """ 
    contratto = joblib.load(PERCORSO_CONTRATTO)
    contratto['modello_minilm'] = nome_modello
    contratto['mappa_dim_minilm'] = E.shape[1]
    contratto['minilm_max_seq_length'] = max_seq_length
    contratto['minilm_n_note'] = E.shape[0]
    joblib.dump(contratto, PERCORSO_CONTRATTO)
    
def cerca_note(
    query: str,
    E: np.ndarray,
    testi: list[str],
    modello,
    k: int = 3
) -> list[int]:    
    E_1 = np.stack([
        e / np.linalg.norm(e) if np.linalg.norm(e) != 0 else e
        for e in E ])
    query_embs = embedda(query, modello)[0]
    query_embs_norm = query_embs / np.linalg.norm(query_embs)
    vicini = [(idx, float(value))for idx, value in enumerate(E_1 @ query_embs_norm)]
    top_3 = sorted(vicini, key=lambda x: x[1], reverse=True)[:k]
    top_3_idx = []
    for i, v in top_3:
        top_3_idx.append(i)    
    return top_3_idx  
    

if __name__ == "__main__":
    import time
    modello = carica_modello_frasi()
    note = pd.read_csv(PERCORSO_DATI)['testo'].tolist()
    t_1 = time.perf_counter()
    embedda(note, modello)
    t_2 = time.perf_counter()
    E = embedda_note(modello)
    E_kilobyte = E.nbytes / 1024
    print(f"\nEncode delle 30 note: {round(t_2 - t_1, 4)}")
    print(f"\nKB di E: {E_kilobyte}")
    assert E.shape == (30, 384)
    salva_vettori(E) 
    E_2 = carica_vettori()
    assert E_2.shape == E.shape and np.allclose(E_2, E)
    if not hasattr(sys.modules["__main__"], "tokenizza"):
        sys.modules["__main__"].tokenizza = tokenizza
    aggiorna_contratto_minilm(E, MODELLO_ST, modello.max_seq_length)
    note = pd.read_csv(PERCORSO_DATI)['testo']
    q = note[5]
    in_cima = cerca_note(q, E, note, modello=modello, k=3)[0]
    assert q == note[in_cima]
    assert E.shape[1] == DIM_MINILM
    contratto_nuovo = joblib.load(PERCORSO_CONTRATTO)
    chiavi_nuove = ['modello_minilm', 'mappa_dim_minilm', 'minilm_max_seq_length', 'minilm_n_note']
    for c in chiavi_nuove:
        assert c in contratto_nuovo.keys()
    norme = np.linalg.norm(E, axis=1)
    assert np.allclose(norme, 1, atol=1e-5)
    
