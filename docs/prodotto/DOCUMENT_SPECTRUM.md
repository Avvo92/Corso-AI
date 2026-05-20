# Perimetro documentale condiviso — Validator e Replicator

> **Fonte unica** per l’elenco dei tipi documento supportati da entrambi gli applicativi.
> Aggiornare questo file quando si aggiunge un tipo; poi allineare Validator e Replicator.

**Spec prodotto:**

- Validator: [`APPUNTI_APPLICATIVO_VALIDATOR.md`](APPUNTI_APPLICATIVO_VALIDATOR.md)
- Replicator: [`APPUNTI_APPLICATIVO_REPLICATOR.md`](APPUNTI_APPLICATIVO_REPLICATOR.md)

**Schema dati valori:** [`schema_canonico_v01.json`](../../schema_canonico_v01.json) (estensione progressiva per tipo).

---

## Tabella spettro (10 tipi)

| `tipo_documento` | Validator | Replicator | Fase implementazione | Modalità Replicator tipiche |
|------------------|-----------|------------|----------------------|---------------------------|
| `busta_paga` | Sì | Sì | **P0** | `transfer_xy` (PDF X→template Y), `discursive`, `partial_inputs` |
| `cu` | Sì | Sì | **P0** Validator / **P1** Replicator | `discursive`, `partial_inputs` |
| `estratto_conto_corrente` | Sì | Sì | **P0** Validator / **P1** Replicator | `discursive`, `partial_inputs` |
| `unilav` | Sì | Sì | P1 | `discursive`, `partial_inputs` |
| `estratto_conto_previdenziale` | Sì | Sì | P1 | `discursive`, `partial_inputs` |
| `lista_movimenti` | Sì | Sì | P1 | `discursive`, `partial_inputs` |
| `isee` | Sì | Sì | P2 | `discursive`, `partial_inputs` |
| `modello_unico` | Sì | Sì | P2 | `discursive`, `partial_inputs` |
| `f24` | Sì | Sì | P1 (Validator controlli base) / P2 Replicator | `partial_inputs` |
| `invio_telematico` | Sì | Sì | P2 | `discursive`, `partial_inputs` |

### Legenda fasi

| Fase | Significato |
|------|-------------|
| **P0** | Must-have fine corso (priorità massima) |
| **P1** | Subito dopo P0 |
| **P2** | Roadmap post-M10 |

### Legenda modalità Replicator

| Modalità | Descrizione breve |
|----------|-------------------|
| `transfer_xy` | Carichi PDF software **X** → generi PDF template software **Y** (richiede corpus X e Y) |
| `discursive` | Descrivi a parole → PDF sul template Y |
| `partial_inputs` | Compili ~10–15 campi chiave → il resto è completato in modo statistico dal training su Y |

---

## Regola di parità

Ogni nuovo `tipo_documento` aggiunto al Validator **deve** avere una riga in questa tabella e una strategia Replicator documentata prima dello sviluppo.

---

## Decision log

| Data | Decisione |
|------|-----------|
| 2026-05-21 | Creato registro condiviso; P0 Validator = busta + CU + estratto; P0 Replicator = busta transfer_xy; P1 = CU Replicator. |
