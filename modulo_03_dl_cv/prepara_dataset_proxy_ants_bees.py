"""Prepara il dataset proxy Ants vs Bees per il M3 cap.09 (track prova).

Scarica lo zip ufficiale del tutorial PyTorch transfer learning, crea
train/val/test in formato ImageFolder sotto:

    modulo_03_dl_cv/dati/proxy_ants_bees/
        train/ants  train/bees
        val/ants    val/bees
        test/ants   test/bees

Il dataset originale ha solo train+val: lo script sposta ~30% del val
in test (seme fisso), così puoi fare C7 sul test senza riusare la val.

Uso (dalla root del repo o da questa cartella):
    python modulo_03_dl_cv/prepara_dataset_proxy_ants_bees.py

Poi su Colab punta `pipeline_addestramento` a quella cartella base
(o zippa `proxy_ants_bees` e caricalo).
"""

from __future__ import annotations

import random
import shutil
import urllib.request
import zipfile
from pathlib import Path

URL = "https://download.pytorch.org/tutorial/hymenoptera_data.zip"
SEME = 42
FRAZIONE_TEST_DA_VAL = 0.30

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "dati" / "proxy_ants_bees"
CACHE = ROOT / "dati" / "_cache"
ZIP_PATH = CACHE / "hymenoptera_data.zip"
EXTRACTED = CACHE / "hymenoptera_data"


def scarica_se_manca() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    if EXTRACTED.is_dir() and (EXTRACTED / "train").is_dir():
        print(f"[ok] già estratto: {EXTRACTED}")
        return
    if not ZIP_PATH.is_file():
        print(f"[download] {URL}")
        urllib.request.urlretrieve(URL, ZIP_PATH)
        print(f"[ok] salvato {ZIP_PATH}")
    print(f"[unzip] -> {CACHE}")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(CACHE)
    if not EXTRACTED.is_dir():
        raise RuntimeError(
            f"Dopo l'unzip non trovo {EXTRACTED}. "
            "Controlla il contenuto di dati/_cache/"
        )


def _svuota(cartella: Path) -> None:
    if cartella.exists():
        shutil.rmtree(cartella)
    cartella.mkdir(parents=True, exist_ok=True)


def _copia_albero(src: Path, dst: Path) -> int:
    """Copia tutte le immagini; ritorna il conteggio file."""
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for percorso in sorted(src.iterdir()):
        if percorso.is_file():
            shutil.copy2(percorso, dst / percorso.name)
            n += 1
    return n


def costruisci_imagefolder() -> None:
    train_src = EXTRACTED / "train"
    val_src = EXTRACTED / "val"
    if not train_src.is_dir() or not val_src.is_dir():
        raise RuntimeError("Struttura hymenoptera inattesa (manca train/ o val/).")

    _svuota(DEST)
    rng = random.Random(SEME)
    riepilogo: dict[str, dict[str, int]] = {
        "train": {},
        "val": {},
        "test": {},
    }

    for classe in ("ants", "bees"):
        # train: copia intera
        n_train = _copia_albero(train_src / classe, DEST / "train" / classe)
        riepilogo["train"][classe] = n_train

        # val originale → spezza in val + test
        files = sorted(
            p for p in (val_src / classe).iterdir() if p.is_file()
        )
        rng.shuffle(files)
        n_test = max(1, int(len(files) * FRAZIONE_TEST_DA_VAL))
        test_files = files[:n_test]
        val_files = files[n_test:]

        (DEST / "val" / classe).mkdir(parents=True, exist_ok=True)
        (DEST / "test" / classe).mkdir(parents=True, exist_ok=True)
        for p in val_files:
            shutil.copy2(p, DEST / "val" / classe / p.name)
        for p in test_files:
            shutil.copy2(p, DEST / "test" / classe / p.name)

        riepilogo["val"][classe] = len(val_files)
        riepilogo["test"][classe] = len(test_files)

    print("\n=== proxy_ants_bees pronto ===")
    print(f"cartella: {DEST}")
    for split, per_classe in riepilogo.items():
        totale = sum(per_classe.values())
        dettaglio = ", ".join(f"{k}={v}" for k, v in per_classe.items())
        print(f"  {split:5s}: {totale:3d}  ({dettaglio})")
    print(
        "\nImageFolder (ordine alfabetico): ants=0, bees=1\n"
        "Per le metriche 'classe positiva' usa indice 1 (bees),\n"
        "oppure stampa sempre ds.class_to_idx.\n"
    )


def main() -> None:
    scarica_se_manca()
    costruisci_imagefolder()


if __name__ == "__main__":
    main()
