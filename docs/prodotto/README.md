# Applicativi prodotto — Indice (due software)

> **Traccia organizzativa** del prodotto fine corso: **Validator** e **Replicator** (applicativi separati, stesso dominio documentale).

---

## Documenti canonici

| Documento | Contenuto |
|-----------|-----------|
| **[`CANONE_STRESS_TEST_LAB_VR.md`](CANONE_STRESS_TEST_LAB_VR.md)** | **Fonte di verità** stress test: Validator solo PDF, export stress_test/internal, metadata_mimic_y |
| [`APPUNTI_APPLICATIVO_VALIDATOR.md`](APPUNTI_APPLICATIVO_VALIDATOR.md) | Controllo fascicoli, regole, semaforo, audit |
| [`APPUNTI_APPLICATIVO_REPLICATOR.md`](APPUNTI_APPLICATIVO_REPLICATOR.md) | Transfer X→Y, imputazione, PDF, dual-channel V+R, **chat §7.3** |
| [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) | 10 tipi documento; fasi P0/P1/P2 |
| [`ARCHITETTURA_PRODOTTO_DUE_APP.md`](ARCHITETTURA_PRODOTTO_DUE_APP.md) | Piano, gap G1–G11, DoD M10, integrazione §5 |
| [`PROTOCOLLO_LOOP_ANTAGONISTA_VR.md`](PROTOCOLLO_LOOP_ANTAGONISTA_VR.md) | Ciclo 8 step, evasion, rule discovery |

## Documenti NON canonici (parcheggio)

| Documento | Contenuto |
|-----------|-----------|
| [`IDEA_POST_CORSO_MENTOR_ENGINE.md`](IDEA_POST_CORSO_MENTOR_ENGINE.md) | **Post-M10.** Canonizzare in applicativo il sistema di apprendimento del corso. **Non compete con Validator/Replicator**: da riprendere solo a M10 chiuso |

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
| 2026-05-22 | **Loop antagonista V↔R:** `PROTOCOLLO_LOOP_ANTAGONISTA_VR.md`; gap G11; esempi `evasion_report` / `rule_candidates`. |
| 2026-05-22 | **`CANONE_STRESS_TEST_LAB_VR.md`:** Validator solo PDF; Replicator `stress_test` vs `internal`; `metadata_mimic_y`; contraddizioni bundle/metadati risolte. |
| 2026-07-28 | **Mentor Engine parcheggiato come idea post-M10** (`IDEA_POST_CORSO_MENTOR_ENGINE.md`). Motivo: riusa lo stack del M10 (memoria agente, retrieval, structured output, LLM-as-judge, FastAPI/Docker) quindi costa poco **dopo**, ma aprirlo ora spaccherebbe il focus sul prodotto del corso. Tre nodi aperti: economia dei token per studente, chi scrive i contenuti, prova di efficacia oltre n=1. |
