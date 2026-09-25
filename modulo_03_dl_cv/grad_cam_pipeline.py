"""
Wrapper CLI → capitolo 12 Grad-CAM.

La teoria, i quiz e gli esercizi sono in:
  modulo_03_dl_cv/12_grad_cam_interpretabilita.py

Questo file resta per compatibilità con i comandi già documentati:

  python grad_cam_pipeline.py --checkpoint ... --immagine ... --classe bees
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_CAPITOLO = Path(__file__).resolve().parent / "12_grad_cam_interpretabilita.py"


def _carica_capitolo():
    """Carica il cap.12 anche se il nome file inizia con una cifra."""
    spec = importlib.util.spec_from_file_location(
        "grad_cam_capitolo_12", _CAPITOLO
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Impossibile caricare {_CAPITOLO}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_cap = _carica_capitolo()

pipeline_grad_cam = _cap.pipeline_grad_cam
grad_cam = _cap.grad_cam
overlay_cam = _cap.overlay_cam
AttivazioniEGradienti = _cap.AttivazioniEGradienti

if __name__ == "__main__":
    _cap.main_cli()
