"""API FastAPI — stesso ClassificatoreVisivo della demo Gradio.

Avvio (dalla cartella modulo_03_dl_cv, con venv attivo):

    uvicorn api:app --reload

Poi apri http://127.0.0.1:8000/docs
"""

from __future__ import annotations

import io
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from PIL import Image

from modello import ClassificatoreVisivo

QUI = Path(__file__).resolve().parent
PERCORSO_PESI = QUI / "dati" / "pesi" / "ants_vs_bees.pt"

app = FastAPI(title="Classificatore visivo documenti")
classificatore = ClassificatoreVisivo(PERCORSO_PESI, device="cpu")


@app.get("/")
def home():
    """Root: manda alla documentazione interattiva."""
    return RedirectResponse(url="/docs")


@app.get("/info")
def info():
    """Espone il contratto di inferenza (senza i pesi)."""
    return classificatore.scheda()


@app.post("/classifica")
async def classifica(file: UploadFile = File(...)):
    contenuto = await file.read()
    try:
        immagine = Image.open(io.BytesIO(contenuto))
    except Exception:
        raise HTTPException(status_code=400, detail="File non è un'immagine")

    esito = classificatore.predict_etichetta(immagine)
    return {
        "etichetta": esito["etichetta"],
        "probabilita": esito["probabilita"],
        "soglia": esito["soglia"],
        "versione_modello": classificatore.scheda().get("versione_contratto"),
    }
