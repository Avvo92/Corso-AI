# Replicator — generazione PDF fedele

Spec: [`docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md`](../../docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md)

## Struttura

```
replicator/
├── ingest/      # profilo corpus (Fase 1)
├── learn/       # geometry, field_map, imputation_profile (Fasi 2-3)
├── extract/     # PDF X → payload (transfer_xy)
├── transfer/    # mapping X → Y
├── interpret/   # testo discorsivo (M5+)
├── compute/     # totali e vincoli (solo Python)
├── render/      # strategie A/B/C
├── qa/          # hold-out
└── templates/   # doc_type_registry.json.example
```

## Comandi (futuri, M10)

```bash
python -m aplicativo.replicator.cli learn --doc-type busta_paga
python -m aplicativo.replicator.cli replicate --doc-type busta_paga --mode transfer_xy --input path.pdf
```
