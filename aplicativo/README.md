# Applicativi prodotto — Codice

Due applicativi **separati** (deploy distinti in M10):

| App | Cartella | Spec |
|-----|----------|------|
| **Validator** | [`validator/`](validator/) | [`docs/prodotto/APPUNTI_APPLICATIVO_VALIDATOR.md`](../docs/prodotto/APPUNTI_APPLICATIVO_VALIDATOR.md) |
| **Replicator** | [`replicator/`](replicator/) | [`docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md`](../docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md) |

Documentazione: [`docs/prodotto/README.md`](../docs/prodotto/README.md) · Architettura: [`ARCHITETTURA_PRODOTTO_DUE_APP.md`](../docs/prodotto/ARCHITETTURA_PRODOTTO_DUE_APP.md)

## Schemi (root repo)

`schema_canonico_v01.json`, `schema_geometry_template_v01.json`, `schema_transfer_route_v01.json`, `schema_imputation_profile_v01.json`, `schema_raster_reference_v01.json` (dual-channel QA V+R)

## Dataset locale (non in git)

- `dati/replica/{doc_type_id}/` — Replicator
- `dati/validator/` — fascicoli test Validator (TBD)
