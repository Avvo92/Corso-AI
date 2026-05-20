# Applicativi prodotto — Indice (due software)

> **Traccia organizzativa** del prodotto fine corso: **Validator** e **Replicator** (applicativi separati, stesso dominio documentale).

---

## Documenti canonici

| Documento | Contenuto |
|-----------|-----------|
| [`APPUNTI_APPLICATIVO_VALIDATOR.md`](APPUNTI_APPLICATIVO_VALIDATOR.md) | Controllo fascicoli, regole, semaforo, audit |
| [`APPUNTI_APPLICATIVO_REPLICATOR.md`](APPUNTI_APPLICATIVO_REPLICATOR.md) | Transfer X→Y, imputazione, PDF, dual-channel V+R, **chat §7.3** |
| [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) | 10 tipi documento; fasi P0/P1/P2 |
| [`ARCHITETTURA_PRODOTTO_DUE_APP.md`](ARCHITETTURA_PRODOTTO_DUE_APP.md) | Piano, gap G1–G10, DoD M10, dual-channel V+R, ramo Fix §4b |

---

## Codice

| App | Path |
|-----|------|
| Validator | [`../../aplicativo/validator/`](../../aplicativo/validator/) |
| Replicator | [`../../aplicativo/replicator/`](../../aplicativo/replicator/) |

---

## Contratti dati (root repo)

- [`../../schema_canonico_v01.json`](../../schema_canonico_v01.json)
- [`../../schema_geometry_template_v01.json`](../../schema_geometry_template_v01.json)
- [`../../schema_transfer_route_v01.json`](../../schema_transfer_route_v01.json)
- [`../../schema_imputation_profile_v01.json`](../../schema_imputation_profile_v01.json)
- [`../../schema_raster_reference_v01.json`](../../schema_raster_reference_v01.json) — raster reference train + `dual_channel_qa_report`

---

## Per agenti

1. [`../../CONTESTO_CORSO.md`](../../CONTESTO_CORSO.md) — gate sessione
2. Task Validator → `APPUNTI_APPLICATIVO_VALIDATOR.md` + `DOCUMENT_SPECTRUM.md`
3. Task Replicator → `APPUNTI_APPLICATIVO_REPLICATOR.md` + `DOCUMENT_SPECTRUM.md`
4. Cross-app → `ARCHITETTURA_PRODOTTO_DUE_APP.md`

---

## Decision log

| Data | Decisione |
|------|-----------|
| 2026-05-20 | Fixer rimosso; nato Replicator. |
| 2026-05-21 | Split due app; documentazione in `docs/prodotto/`. |
| 2026-05-21 | Dual-channel QA (vettoriale + raster): fedeltà visiva Replicator; gap G9. |
| 2026-05-21 | Replicator: interfaccia **chat** + ciclo miglioramento (§7.3 APPUNTI) — opzionale M10. |
| 2026-05-22 | **Fixer controllato** (`controlled_fix`, §3b REPLICATOR): gap G10; bundle + `fix_report`; divieto fix libero su terzi. |
