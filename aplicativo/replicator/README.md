# Replicator — generazione PDF fedele

Spec: [`docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md`](../../docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md) (§4.3 dual-channel V+R, **§7.3 chat**)

Artefatti: `artifacts/raster_reference_v01.json`, `dual_channel_qa_report.json` — schema [`schema_raster_reference_v01.json`](../../schema_raster_reference_v01.json)

**Chat (M7+):** front-end conversazionale sopra la stessa pipeline; sessioni e feedback strutturato — dettaglio in APPUNTI §7.3.

## Struttura

```
replicator/
├── ingest/      # profilo corpus (Fase 1)
├── learn/       # geometry, field_map, imputation_profile (Fasi 2-3)
├── extract/     # PDF X → payload (transfer_xy)
├── transfer/    # mapping X → Y
├── interpret/   # testo discorsivo (M5+)
├── compute/     # totali e vincoli (solo Python)
├── render/      # strategie A/B/C (uscita PDF vettoriale)
├── fix/         # controlled_fix: validazione lineage + merge payload / patch allowlist (P2) — §3b APPUNTI
├── qa/          # hold-out vettoriale + raster QA (dual-channel §4.3 REPLICATOR)
└── templates/   # doc_type_registry.json.example
```

## Comandi (futuri, M10)

```bash
python -m aplicativo.replicator.cli learn --doc-type busta_paga
python -m aplicativo.replicator.cli replicate --doc-type busta_paga --mode transfer_xy --input path.pdf
```
