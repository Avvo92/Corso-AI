"""
Rigenera `pratiche_genuinita_mock.csv` — dataset didattico più ampio e più realistico.

Caratteristiche:
- ~640 pratiche (modificabile con N_RIGHE).
- Classe alterati ~34% (sbilanciamento tipico).
- **Casi limite**: una quota di genuini “sporchi” e alterati “lievi” (feature più ambigue).
- **Rumore sulle etichette**: una piccola frazione di righe ha y_alterato invertito
  (simula errori di revisione / etichettatura).

Dipendenze: solo libreria standard (niente numpy/pandas).

Uso (da questa cartella o con path assoluto):
  python genera_pratiche_genuinita_mock.py
"""
from __future__ import annotations

import csv
import math
import os
import random
from typing import Any

random.seed(42)

N_RIGHE = 640
FRAZIONE_ALTERATI = 0.34
# Quota di genuini/alterati resi “ambigui” a livello di feature (non flip etichetta).
FRAZIONE_GENUINO_AMBIGUO = 0.09
FRAZIONE_ALTERATO_LIEVE = 0.11
# Frazione di righe su cui applicare rumore sull’etichetta (dopo la generazione).
FRAZIONE_RUMORE_LABEL = 0.028


def _randn(rng: random.Random) -> float:
    """Gaussiana N(0,1) (Box–Muller)."""
    u = max(rng.random(), 1e-12)
    v = max(rng.random(), 1e-12)
    return math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.pi * v)


def _riga_genuina(rng: random.Random, idx: int) -> dict[str, Any]:
    delta = 155.0 + _randn(rng) * 55.0
    delta = max(5.0, min(280.0, delta))
    ratio = round(rng.uniform(0.17, 0.38), 2)
    ocr = round(rng.uniform(0.82, 0.96), 2)
    inc = rng.randrange(0, 3)
    acc = rng.choices([0, 1], weights=[0.06, 0.94])[0]
    return {
        "pratica_id": f"P2026-{idx:04d}",
        "delta_netto_lordo": round(delta),
        "ratio_trattenute": ratio,
        "match_cf_cross_doc": 1,
        "coerenza_date": 1,
        "accrediti_stipendio_presenti": acc,
        "confidence_ocr_media": ocr,
        "num_incoerenze_cross_doc": inc,
        "y_alterato": 0,
    }


def _riga_genuina_ambigua(rng: random.Random, idx: int) -> dict[str, Any]:
    """Genuino reale ma con segnali più vicini all’alterato (revisione, OCR basso, ecc.)."""
    delta = 35.0 + _randn(rng) * 55.0
    delta = max(-45.0, min(140.0, delta))
    ratio = round(rng.uniform(0.26, 0.45), 2)
    ocr = round(rng.uniform(0.74, 0.88), 2)
    inc = rng.randrange(2, 5)
    acc = rng.choices([0, 1], weights=[0.18, 0.82])[0]
    m = rng.choices([0, 1], weights=[0.12, 0.88])[0]
    coer = rng.choices([0, 1], weights=[0.1, 0.9])[0]
    return {
        "pratica_id": f"P2026-{idx:04d}",
        "delta_netto_lordo": round(delta),
        "ratio_trattenute": ratio,
        "match_cf_cross_doc": m,
        "coerenza_date": coer,
        "accrediti_stipendio_presenti": acc,
        "confidence_ocr_media": ocr,
        "num_incoerenze_cross_doc": inc,
        "y_alterato": 0,
    }


def _riga_alterata(rng: random.Random, idx: int) -> dict[str, Any]:
    delta = -120.0 + _randn(rng) * 90.0
    delta = min(-8.0, max(-400.0, delta))
    ratio = round(rng.uniform(0.44, 0.78), 2)
    ocr = round(rng.uniform(0.58, 0.79), 2)
    inc = rng.randrange(3, 8)
    acc = rng.choices([0, 1], weights=[0.45, 0.55])[0]
    m = rng.choices([0, 1], weights=[0.35, 0.65])[0]
    coer = rng.choices([0, 1], weights=[0.3, 0.7])[0]
    return {
        "pratica_id": f"P2026-{idx:04d}",
        "delta_netto_lordo": round(delta),
        "ratio_trattenute": ratio,
        "match_cf_cross_doc": m,
        "coerenza_date": coer,
        "accrediti_stipendio_presenti": acc,
        "confidence_ocr_media": ocr,
        "num_incoerenze_cross_doc": inc,
        "y_alterato": 1,
    }


def _riga_alterata_lieve(rng: random.Random, idx: int) -> dict[str, Any]:
    """Alterazione più “soft”: più facile confonderla con un genuino borderline."""
    delta = -35.0 + _randn(rng) * 35.0
    delta = min(-10.0, max(-160.0, delta))
    ratio = round(rng.uniform(0.32, 0.52), 2)
    ocr = round(rng.uniform(0.72, 0.84), 2)
    inc = rng.randrange(2, 5)
    acc = rng.choices([0, 1], weights=[0.25, 0.75])[0]
    return {
        "pratica_id": f"P2026-{idx:04d}",
        "delta_netto_lordo": round(delta),
        "ratio_trattenute": ratio,
        "match_cf_cross_doc": rng.choices([0, 1], weights=[0.2, 0.8])[0],
        "coerenza_date": rng.choices([0, 1], weights=[0.15, 0.85])[0],
        "accrediti_stipendio_presenti": acc,
        "confidence_ocr_media": ocr,
        "num_incoerenze_cross_doc": inc,
        "y_alterato": 1,
    }


def main() -> None:
    rng = random.Random(42)
    n_alt = int(round(N_RIGHE * FRAZIONE_ALTERATI))
    n_gen = N_RIGHE - n_alt
    indici = list(range(1, N_RIGHE + 1))
    rng.shuffle(indici)

    righe: list[dict[str, Any]] = []
    gen_pool = indici[:n_gen]
    alt_pool = indici[n_gen:]

    n_amb = max(1, int(round(len(gen_pool) * FRAZIONE_GENUINO_AMBIGUO)))
    amb_set = set(rng.sample(gen_pool, min(n_amb, len(gen_pool))))

    n_lieve = max(1, int(round(len(alt_pool) * FRAZIONE_ALTERATO_LIEVE)))
    lieve_set = set(rng.sample(alt_pool, min(n_lieve, len(alt_pool))))

    for idx in gen_pool:
        if idx in amb_set:
            righe.append(_riga_genuina_ambigua(rng, idx))
        else:
            righe.append(_riga_genuina(rng, idx))

    for idx in alt_pool:
        if idx in lieve_set:
            righe.append(_riga_alterata_lieve(rng, idx))
        else:
            righe.append(_riga_alterata(rng, idx))

    righe.sort(key=lambda r: r["pratica_id"])

    n_flip = max(1, int(round(N_RIGHE * FRAZIONE_RUMORE_LABEL)))
    flip_idx = set(rng.sample(range(len(righe)), min(n_flip, len(righe))))
    for i in flip_idx:
        righe[i]["y_alterato"] = 1 - int(righe[i]["y_alterato"])

    out = os.path.join(os.path.dirname(__file__), "pratiche_genuinita_mock.csv")
    colonne = [
        "pratica_id",
        "delta_netto_lordo",
        "ratio_trattenute",
        "match_cf_cross_doc",
        "coerenza_date",
        "accrediti_stipendio_presenti",
        "confidence_ocr_media",
        "num_incoerenze_cross_doc",
        "y_alterato",
    ]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colonne)
        w.writeheader()
        w.writerows(righe)

    print(f"Scritto {out} ({len(righe)} righe)")
    n0 = sum(1 for r in righe if r["y_alterato"] == 0)
    n1 = sum(1 for r in righe if r["y_alterato"] == 1)
    print(f"  y=0: {n0} | y=1: {n1} (dopo rumore etichette)")
    print(f"  Righe con etichetta flip: {n_flip} (circa {100 * FRAZIONE_RUMORE_LABEL:.1f}%)")


if __name__ == "__main__":
    main()
