# Appunti Applicativo — Replicator (Generazione PDF fedele)

> **Documento master** per lo sviluppo del secondo applicativo del corso.
>
> **Prodotto gemello:** Validator → [`APPUNTI_APPLICATIVO_VALIDATOR.md`](APPUNTI_APPLICATIVO_VALIDATOR.md)  
> **Indice:** [`README.md`](README.md)  
> **Spettro documenti:** [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md)  
> **Codice:** [`../../aplicativo/replicator/`](../../aplicativo/replicator/)

---

## 0) Regola per agenti e sviluppo futuro

Prima di proporre codice o architettura sul Replicator:

1. Leggere **questo file** per intero.
2. Consultare [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) per il tipo documento.
3. Consultare [`schema_canonico_v01.json`](../../schema_canonico_v01.json) per i campi valori.

---

## 1) Visione prodotto

**Replicator** è un **software separato** dal Validator.

**Cosa fa l’operatore (flusso tipico):**

1. Sceglie il tipo di documento e il template software **Y** (es. busta paga formato software Y).
2. Fornisce i dati in uno di questi modi (vedi §3).
3. Il sistema produce un **PDF** che assomiglia il più possibile agli esempi di training su Y.
4. Vede un **report** di cosa è stato preso dai dati forniti e cosa è stato **autocompletato** (stima statistica).
5. Può **correggere** i campi dubbi e rigenerare, poi **scaricare** il PDF.
6. (Opzionale) Passa il PDF al **Validator** per un controllo qualità.

**Relazione antagonista con Validator:** Replicator cerca la massima fedeltà visiva; Validator cerca errori e incoerenze. I due prodotti si migliorano a vicenda (§12).

---

## 2) Stesso spettro documentale del Validator

I dieci tipi in [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) sono supportati **in spec**; l’implementazione segue fasi **P0 → P1 → P2** (non tutto in M10).

| Priorità | Replicator — obiettivo fine corso |
|----------|----------------------------------|
| **P0** | `busta_paga` con modalità **`transfer_xy`** (PDF software X → template Y) + corpus ampi X e Y |
| **P1** | Un secondo tipo (es. `cu`) con **`partial_inputs`** + imputazione |
| **P2** | Altri tipi (ISEE, modello unico, …) uno alla volta |

---

## 3) Tre modalità di input

Ogni `doc_type_id` dichiara quali modalità sono abilitate (`doc_type_registry.json`).

| Modalità | Input operatore | Corpus PDF software X | Corpus PDF template Y |
|----------|-----------------|----------------------|------------------------|
| **`transfer_xy`** | 1 PDF busta (o altro) prodotto da software **X** | Molti (decine/centinaia) | Molti |
| **`discursive`** | Testo libero (descrizione dati) | No | Molti |
| **`partial_inputs`** | Form con ~10–15 campi chiave che compili tu | No | Molti; resto **imputazione** |

**Regola conflitto:** se fornisci **partial** e **testo discorsivo**, i valori del form **partial** hanno priorità; il testo serve per note o campi non in form.

---

## 4) Pipeline tecnica

### 4.1 Training (offline, per ogni `doc_type_id`)

| Fase | Output |
|------|--------|
| 0 Registrazione | `doc_type_id`, path `dati/replica/{doc_type_id}/` |
| 1 Profilo | `artifacts/profile.json` |
| 2 Layout | `artifacts/geometry_template_v01.json` |
| 3 Campi | `artifacts/field_map.json` |
| 3b Imputazione | `artifacts/imputation_profile.json` (distribuzioni + regole condizionate su corpus Y) |
| 6 QA | `artifacts/qa_report.json` su hold-out |

**Corpus Y:** sempre necessario (≥20 PDF, ideale 50–100+).  
**Corpus X:** solo se `transfer_xy` è abilitato.

### 4.2 Runtime (ogni generazione)

```text
[transfer_xy] PDF X ──► Extract ──► payload_source
[discursive]  testo ──► Interpret (LLM structured, M5+)
[partial]     form  ──► payload_partial
        │
        ▼
    Transfer (allineamento campi verso template Y)
        │
        ▼
    Impute (riempie campi mancanti — statistico, §5)
        │
        ▼
    Compute (Python: totali, vincoli fiscali — MAI LLM)
        │
        ▼
    Render (strategia A/B/C — §6)
        │
        ▼
    PDF Y + imputation_report.json + payload.json
```

---

## 5) Imputazione statistica (campi mancanti)

Quando il template Y richiede campi che **non** arrivano da X, dal testo o dal partial:

1. Si usa `imputation_profile.json` appreso dal corpus Y.
2. Regole **condizionate** (es. dato il lordo estratto, trattenute INPS in intervallo plausibile visto su Y).
3. Fallback **marginale** sulla distribuzione del campo su Y.
4. Ogni campo riceve `provenance`:
   - `extracted_from_x` | `extracted_discursive` | `provided_partial`
   - `imputed_conditional` | `imputed_marginal_y` | `computed`
5. `confidence` 0–1 per campo.

**UI (decisione prodotto):** generazione **quasi automatica** + **report** con badge sui campi imputati + **modifica** prima del download (non silenzioso totale).

**Disclaimer obbligatorio in UI:** i campi autocompletati sono **stime coerenti con il training**, non attestazioni ufficiali del software Y.

**Vincoli hard (sempre Python dopo imputazione):** netto ≤ lordo; somme tabella; formati data/CF.

---

## 6) Rendering PDF

| Strategia | Quando |
|-----------|--------|
| **A fill_master** | Esiste PDF vuoto/master ufficiale Y |
| **B overlay** | Coordinate stabili (preferita se possibile) |
| **C reportlab** | Ricostruzione Platypus da `geometry_template` |

**Metadati:** `Creator` / `Producer` = motore Replicator (onesti). **Vietato** copiare metadati del software Y originale.

**Qualità “indistinguibile” (operativa):** stesso layout e posizioni campi degli esempi Y; soglia QA ≥98% field placement su hold-out. Non è clone forense byte-identico.

---

## 7) Interfaccia grafica (due fasi)

### 7.1 Prototipo (M4–M7) — Streamlit

| Schermata | Funzione |
|-----------|----------|
| Home | Scelta `doc_type_id` / route |
| **Admin training** | Upload corpus, avvio learn, versione template attiva |
| Genera | Upload X / textarea / form partial → stepper pipeline |
| Risultato | Anteprima PDF, tabella provenance, filtro “solo imputati”, modifica, download |
| Export | `imputation_report.json` + PDF |

### 7.2 Produzione (M10) — React + FastAPI

Stesso flusso; **deploy URL separato** dal Validator (secondo pezzo portfolio).

---

## 8) Integrazione con Validator

**Bundle export minimo:**

- `pdf_generato`
- `payload.json`
- `imputation_report.json`
- `pratica_id` (stesso fascicolo)

Il Validator analizza il PDF e può usare il report per evidenziare campi imputati (vedi Validator §6.7).

**Metriche antagonista (da tracciare):** % campi imputati; errori regole post-generazione; miglioramento versione template.

---

## 9) Contratti dati e schemi

| Artefatto | File schema |
|-----------|-------------|
| Valori campi | [`schema_canonico_v01.json`](../../schema_canonico_v01.json) |
| Layout | [`schema_geometry_template_v01.json`](../../schema_geometry_template_v01.json) |
| Route X→Y | [`schema_transfer_route_v01.json`](../../schema_transfer_route_v01.json) |
| Imputazione | [`schema_imputation_profile_v01.json`](../../schema_imputation_profile_v01.json) |
| Registry tipi | [`doc_type_registry.json.example`](../../aplicativo/replicator/templates/doc_type_registry.json.example) |

---

## 10) Campi partial (10–15 per tipo) — da completare

Per ogni `tipo_documento` definire in questa sezione (o file dedicato) l’elenco campi che l’operatore compila a mano in modalità `partial_inputs`.

| `tipo_documento` | Campi partial (bozza — TBD dettaglio) | Stato |
|------------------|---------------------------------------|-------|
| `busta_paga` | periodo, CF, lordo, netto, datore, … | TBD |
| `cu` | anno_fiscale, CF, redditi_lavoro, sostituto_imposta, … | TBD |
| `estratto_conto_corrente` | IBAN parziale, periodo, saldi, … | TBD |
| Altri | vedi DOCUMENT_SPECTRUM P1/P2 | TBD |

---

## 11) Stack e moduli corso

| Modulo | Contributo |
|--------|------------|
| M1 | Path `dati/replica/`, JSON |
| M2 | Metriche QA, pytest golden |
| M3 | OCR/deskew scansioni |
| M4 | Learn layout, extract |
| M5 | Interpret discorsivo |
| M6 | RAG regole testo (opzionale) |
| M7 | Agente tool pipeline |
| M8 | Fine-tuning Interpret (opzionale) |
| M9 | Docker, CI |
| **M10** | App deployata: P0 busta transfer_xy + P1 un altro tipo |

Dipendenze: blocco **Applicativo / Replicator** in `requirements.txt` (scommentare da M4).

---

## 12) Definition of Done M10 (Replicator)

- [ ] UI Streamlit o React funzionale (upload → report → download)
- [ ] UI **admin training** (corpus + learn)
- [ ] P0: `transfer_xy` busta paga dimostrata (hold-out QA ≥98% placement)
- [ ] P1: un secondo tipo con `partial_inputs` + imputazione
- [ ] Audit: provenance + `imputation_report` su ogni generazione
- [ ] Integrazione test con Validator su almeno 1 caso end-to-end

---

## 13) Compliance e rischi

| Rischio | Mitigazione |
|---------|-------------|
| Campi imputati presentati come reali | Report UI + disclaimer + export audit |
| Dual-use / falsificazione | Route registrate, uso interno, metadati onesti |
| Scope 10 tipi in M10 | Fasi P0/P1/P2 — vedi DOCUMENT_SPECTRUM |
| Drift software emittente | `template_version` incrementale |

---

## 14) API e CLI (bozza)

- `POST /api/v1/replicate/{doc_type_id}` — body: `natural_language` | `partial` | upload PDF (transfer)
- `POST /api/v1/admin/learn/{doc_type_id}` — rilancia training
- CLI: `python -m aplicativo.replicator.cli replicate --doc-type ...`

---

## 15) Gap e prontezza implementativa

Dettaglio esteso (checklist G1–G8, diagrammi, DoD): [`ARCHITETTURA_PRODOTTO_DUE_APP.md`](ARCHITETTURA_PRODOTTO_DUE_APP.md) §6–§8.

**Sintesi operativa prima di codificare un nuovo `doc_type_id`:**

1. Riga in `DOCUMENT_SPECTRUM.md` con fase P0/P1/P2.
2. Campi in `schema_canonico_v01.json` + elenco **partial** (§10 sopra).
3. Entry in `doc_type_registry.json` con modalità abilitate.
4. Corpus Y (e X se `transfer_xy`) sotto `dati/replica/{doc_type_id}/`.
5. `imputation_profile` e QA hold-out prima di aprire agli operatori.

---

## 16) Dettaglio pipeline Fasi 0–7 (training e runtime)

### Prerequisiti corpus

| Requisito | Dettaglio |
|-----------|-----------|
| Volume Y | ≥ 20 PDF (ideale 50–100+) |
| Omogeneità | Stesso tipo + stesso software emittente Y |
| Hold-out | 10–20 PDF solo per QA (Fase 6) |
| Storage | `dati/replica/{doc_type_id}/` — mai in git se PII |

### Fasi offline

| Fase | Output | Tool tipici |
|------|--------|-------------|
| 0 Registrazione | `doc_type_id`, path corpus | — |
| 1 Profilo | `profile.json` | PyMuPDF, pdfplumber |
| 2 Layout | `geometry_template_v01.json` | pdfplumber, cluster bbox |
| 3 Campi | `field_map.json` | etichette + review umana |
| 3b Imputazione | `imputation_profile.json` | statistiche su corpus Y |
| 6 QA | `qa_report.json` | hold-out ≥ 98% field placement |

### Fasi runtime (dopo training)

| Step | Input | Output |
|------|-------|--------|
| Extract | PDF X | `payload_source` (solo `transfer_xy`) |
| Interpret | testo discorsivo | `payload_draft` (M5+, LLM structured) |
| Transfer | payload sorgente | payload allineato a Y |
| Impute | campi mancanti | valori + provenance |
| Compute | payload | totali/vincoli (**solo Python**) |
| Render | payload + template | PDF (A fill_master / B overlay / C reportlab) |

**Stack:** pdfplumber, PyMuPDF, reportlab, pypdf; OCR opzionale M3. **Mai** LLM per coordinate o totali.

### Checklist nuovo `doc_type_id`

1. Riga in `DOCUMENT_SPECTRUM.md` + registry
2. Corpus Y (+ X se transfer) e hold-out
3. Fasi 1–3 + imputation_profile
4. Renderer + QA
5. Documentare in decision log `README.md` se entra in P0

---

## 17) Decision log

| Data | Decisione |
|------|-----------|
| 2026-05-20 | Input discorsivo; pipeline Fasi 0–7; Fixer rimosso. |
| 2026-05-21 | Master file; transfer X→Y; imputazione; tre modalità; split due app; doc in `docs/prodotto/`. |
