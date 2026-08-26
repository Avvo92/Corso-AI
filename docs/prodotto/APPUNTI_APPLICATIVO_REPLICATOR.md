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
2. Leggere **[`CANONE_STRESS_TEST_LAB_VR.md`](CANONE_STRESS_TEST_LAB_VR.md)** (Validator solo PDF; `export_mode`; `metadata_mimic_y`).
3. Consultare [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) per il tipo documento.
4. Consultare [`schema_canonico_v01.json`](../../schema_canonico_v01.json) per i campi valori.
5. Se UI/UX conversazionale: **§7.3**. Se **fix**: **§3b**.

---

## 1) Visione prodotto

**Replicator** è un **software separato** dal Validator.

**Cosa fa l’operatore (flusso tipico):**

1. Sceglie il tipo di documento e il template software **Y** (es. busta paga formato software Y).
2. Fornisce i dati in uno di questi modi (vedi §3).
3. Il sistema produce un **PDF vettoriale** che, **a schermo**, assomiglia il più possibile agli esempi di training su Y (fedeltà visiva prioritaria — vedi §4.3).
4. Vede un **report** di cosa è stato preso dai dati forniti e cosa è stato **autocompletato** (stima statistica).
5. Può **correggere** i campi dubbi e rigenerare, poi **scaricare** il PDF.
6. Export **`stress_test`**: copia **solo il PDF** nella ingest Validator (stress test lab).  
7. Export **`internal`**: bundle + lineage per debug — **mai** in Validator.

**Alternativa UX:** chat (§7.3).

**Relazione antagonista:** Replicator produce PDF **indistinguibili** da Y; Validator li giudica **cieco** (solo file). Canone: [`CANONE_STRESS_TEST_LAB_VR.md`](CANONE_STRESS_TEST_LAB_VR.md) · loop §8b.

### 1.2 Priorità lab — stress test completo per Validator

| Priorità | Requisito |
|----------|-----------|
| 1 | `metadata_mimic_y` nel PDF export `stress_test` (no firma Replicator nel file) |
| 2 | Layout / vettoriale / raster QA **interno** prima dell’export |
| 3 | Profili `realistic_full` per alterate credibili |
| 4 | Cartella ingest Validator: **solo `.pdf`**, zero JSON sidecar |

### 1.1 Scenario obiettivo (North Star)

> *«Crea le buste paga Zucchetti e la **CU** (certificazione unica del reddito; talvolta indicata CUD) dell’anno precedente a partire da queste tre buste paga X.»*

Il Replicator **a regime** (M7+ agente, M10 prodotto) deve poter eseguire richieste **in linguaggio naturale** che implicano **più documenti** e **più template** nella stessa `pratica_id`:

| Input operatore | Sistema |
|-----------------|---------|
| 3× PDF busta software **X** | Extract + transfer verso template **Y** (Zucchetti) |
| Istruzione NL: gestionale Y, anno CU, quante BP | Agente risolve `doc_type_id`, `template_version`, periodo |
| Corpus già addestrato su Zucchetti + template CU | Render V + QA dual-channel per **ogni** PDF |
| Coerenza fascicolo | Payload `pratica_id` condiviso → Compute annuale → CU allineata alle BP |

**Sequenza canonica:**

```text
1. Parse intent (NL) → piano: [BP×N su zucchetti_v1] + [CU anno T-1]
2. Crea/aggiorna pratica_id
3. Per ogni busta X: Extract → Transfer(X→Zucchetti) → Impute → Compute → Render → Raster QA
4. Aggrega payload pratica (redditì mensili → annuali CU)
5. Genera CU su template CU_Y: partial da pratica + Impute → Compute → Render → Raster QA
6. Export fascicolo (tutti i PDF + report) → Validator cross-doc (opz./obbligatorio)
```

**Prerequisiti (non opzionali):** training completato per `busta_paga`/`zucchetti_*` e per `cu`/`cu_*`; `schema_canonico` con campi comuni; regole Compute cross-periodo; Validator con incrocio BP↔CU.

**Fasi corso:** P0 = singola busta `transfer_xy`; P1 = CU da partial; **North Star pieno** = orchestrazione multi-doc (M7–M10). Non promette perfezione fiscale/legal automatica — vedi §13 e Validator.

---

## 2) Stesso spettro documentale del Validator

I dieci tipi in [`DOCUMENT_SPECTRUM.md`](DOCUMENT_SPECTRUM.md) sono supportati **in spec**; l’implementazione segue fasi **P0 → P1 → P2** (non tutto in M10).

| Priorità | Replicator — obiettivo fine corso |
|----------|----------------------------------|
| **P0** | `busta_paga` con modalità **`transfer_xy`** (PDF software X → template Y) + corpus ampi X e Y |
| **P1** | Un secondo tipo (es. `cu`) con **`partial_inputs`** + imputazione |
| **P2** | Altri tipi (ISEE, modello unico, …) uno alla volta + **`controlled_fix`** completo (patch allowlist, §3b) |

---

## 3) Modalità di input (generazione + fix controllato)

Ogni `doc_type_id` dichiara quali modalità sono abilitate (`doc_type_registry.json`).

| Modalità | Input operatore | Corpus PDF software X | Corpus PDF template Y |
|----------|-----------------|----------------------|------------------------|
| **`transfer_xy`** | 1 PDF busta (o altro) prodotto da software **X** | Molti (decine/centinaia) | Molti |
| **`discursive`** | Testo libero (descrizione dati) | No | Molti |
| **`partial_inputs`** | Form con ~10–15 campi chiave che compili tu | No | Molti; resto **imputazione** |
| **`controlled_fix`** | PDF **già generato** da questo Replicator + bundle (`payload` + report) — vedi **§3b** | n/a | stesso Y del `template_version` originale |

**Regola conflitto:** se fornisci **partial** e **testo discorsivo**, i valori del form **partial** hanno priorità; il testo serve per note o campi non in form.

---

## 3b) Fixer controllato (`controlled_fix`) — reintrodotto

> **Decisione 2026-05-22:** oltre alla **generazione da zero** (§4.2), il Replicator supporta una modalità **Fixer** solo se **tracciabile** e **vincolata**, per ridurre attrito operativo senza aprire la porta a patch fraudolente su PDF terzi.

### Principi (non negoziabili)

| Regola | Motivo |
|--------|--------|
| **Lineage obbligatorio** | Il PDF deve risultare prodotto da una `replicator_run` nota (metadati PDF `ReplicatorRunId` / XMP custom **o** sidecar firmato **o** record DB interno). |
| **Bundle minimo** | Stesso `pratica_id` + `payload.json` (versione usata in generazione) + `imputation_report` + `dual_channel_qa_report` dell’ultimo run. |
| **Preferenza: rigenerazione** | Prima scelta: aggiornare `payload` → rieseguire Transfer (se serve) → Impute → **Compute** → Render → Raster QA. Massima auditabilità. |
| **Patch in-place solo P2** | Consentita solo su **allowlist** di `field_id` con bbox da `geometry_template`; operazioni PyMuPDF deterministiche; **mai** LLM per coordinate o importi. |
| **Post-fix** | Sempre **Compute** se cambiano numeri; sempre **Raster QA** + nuovo `dual_channel_qa_report`. |
| **Append-only** | `fix_report.json` (o array in audit store): timestamp, `user_id`, diff payload, `strategy` (`regenerate` \| `patch_allowlist`), hash PDF pre/post. |
| **Vietato** | “Apri un PDF qualsiasi e sistema” senza lineage; alterare metadati per fingere software Y; uso Fixer per eludere Validator su documenti non propri. |

### Flusso operativo (runtime)

```text
Upload PDF lineage + bundle
        │
        ▼
Validazione lineage + coerenza bundle
        │
        ├─ FAIL → blocco + messaggio operatore
        │
        ▼
Scelta strategia (default: regenerate)
        │
        ├─ regenerate: merge payload correzioni → … → Render → Raster QA
        │
        └─ patch_allowlist (P2): operazioni vettoriali consentite → Compute → Raster QA
        │
        ▼
Export: nuovo PDF + payload + report aggiornati + fix_report (append)
```

### Chat (§7.3)

La chat può invocare `controlled_fix` solo dopo che il sistema ha verificato lineage (stesso divieto: **no patch silenziosa** su file non provati Replicator).

### Fase corso

| Fase | Contenuto |
|------|-------------|
| **P0–P1** | Solo **rigenerazione** da payload (equivale a “fix” senza modulo dedicato). |
| **P2** | Modulo `aplicativo/replicator/fix/` + patch allowlist + UI “Correggi output”. |

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
| 4b Raster reference | `artifacts/raster_reference_v01.json` + PNG/maschere (§4.3) |
| 6 QA | `artifacts/qa_report.json` su hold-out (vettoriale **e** raster) |

**Corpus Y:** sempre necessario (≥20 PDF, ideale 50–100+).  
**Corpus X:** solo se `transfer_xy` è abilitato.

Per buste **PDF nativi** (es. Zucchetti): il corpus alimenta **entrambi** i canali — estrazione bbox (vettoriale) e raster di riferimento (visivo).

### 4.2 Runtime (ogni generazione)

```text
[transfer_xy] PDF X ──► Extract (vettoriale) ──► payload_source
[discursive]  testo ──► Interpret (LLM structured, M5+)
[partial]     form  ──► payload_partial
        │
        ▼
    Transfer → Impute → Compute (solo Python)
        │
        ▼
    Render (vettoriale A/B/C — §6) ──► PDF Y (unica uscita ufficiale)
        │
        ▼
    Rasterize (stesso DPI/engine del train) ──► Dual-channel QA (§4.3)
        │
        ├─ passed ──► release: PDF + reports
        └─ failed ──► micro-adjust opz. / HITL / blocco download
```

**Uscite:** `payload.json`, `imputation_report.json`, `dual_channel_qa_report.json` (schema dedicato). Se è stato eseguito un fix controllato: anche **`fix_report.json`** (append-only — §3b).

### 4.2b Runtime — solo `controlled_fix` (no generazione da X)

```text
PDF lineage + bundle ──► Validazione §3b
        │
        ▼
Merge correzioni payload (e opz. patch allowlist P2)
        │
        ▼
    Transfer? (se cambia mapping) → Impute → Compute → Render → Rasterize → Dual-channel QA
        │
        ▼
    PDF aggiornato + report + fix_report
```

> **Decisione prodotto 2026-05-21:** la fedeltà **visiva finale** è criterio primario; regole matematiche e bbox vettoriali sono necessari ma **non sufficienti**.

#### Principio

| Canale | Ruolo | Uscita |
|--------|--------|--------|
| **Vettoriale (V)** | Produzione: PDF nativo (testo selezionabile, zoom nitido); extract, placement, regole, compute | Un solo PDF |
| **Raster (R)** | Giudice visivo: rasterizza la stessa pagina e confronta con il reference del train | Derivato — **non** secondo PDF consegnato |

**Analogia:** HTML/CSS (V) + screenshot golden test in CI (R). Il JSON può essere valido mentre il layout è sbagliato — il canale R intercetta quel caso.

#### Obiettivo utente (chiarezza)

- **Sì:** identico **a schermo** rispetto al cluster di training (es. buste Zucchetti stesso `template_version`).
- **No:** clone forense byte-identico per frode su terzi in produzione.
- **Export `stress_test`:** metadati PDF profilo **`metadata_mimic_y`** (come Y) — canone [`CANONE_STRESS_TEST_LAB_VR.md`](CANONE_STRESS_TEST_LAB_VR.md).
- **Export `internal`:** metadati onesti Replicator ammessi solo in bundle/sidecar **non** inviati a Validator.

#### Training offline — due flussi paralleli

Per ogni `template_version` (cluster omogeneo di corpus Y):

1. **Flusso V:** `profile.json` → `geometry_template` (ancore relative + bbox) → `field_map` → `imputation_profile`.
2. **Flusso R:** raster pagina a **DPI fisso** (default **200**, stesso motore `pymupdf_pixmap` in train e runtime):
   - `static_mask` — zone fisse (logo, intestazione, griglia) **escluse** dal diff;
   - `dynamic_rois` — patch per `field_id` su hold-out;
   - `layout_fingerprint` — impronta per scegliere template o segnalare UNKNOWN;
   - reference PNG master o mediana del cluster.

Artefatto: [`schema_raster_reference_v01.json`](../../schema_raster_reference_v01.json) (`RasterReference`).

#### Runtime — gate visivo

Dopo `Render`:

1. Rasterizza pagina generata (stesso DPI/engine).
2. Confronta con `raster_reference` del `template_version` attivo:
   - **layout_match_score** sulla pagina (peso zone dinamiche);
   - **roi_diff** per ogni `field_id` (SSIM o diff normalizzato sulle ROI);
3. Incrocia con **vector_qa** (`placement_score`, `rules_ok`).
4. `channels_agree = false` se vettoriale OK e raster KO (caso “matematica ok, visivo no”).
5. **Opzionale:** micro-adjust ±1–3 pt su coordinate vettoriali per ROI fallite → ri-rasterizza → ripeti (max N tentativi); salva offset in `geometry_template`.

Report: `dual_channel_qa_report.json` (`DualChannelQAReport` nello stesso schema).

#### Soglie (calibrare su hold-out)

| Metrica | Target iniziale P0 busta |
|---------|---------------------------|
| `placement_score` (V) | ≥ 0,98 |
| `layout_match_score` (R) | ≥ 0,95 |
| `roi_diff_max` (R) | ≤ 0,06 |
| Release PDF | solo se `passed` e `channels_agree` |

#### PDF nativi vs scansioni

| Input | Canale V | Canale R |
|-------|----------|----------|
| Busta Zucchetti nativa | Estrazione bbox + render A/B | Reference + diff ROI — **canale primario visivo** |
| PDF scansione | OCR + overlay su immagine | Reference raster obbligatorio; V debole |

#### Moduli corso

| Modulo | Contributo dual-channel |
|--------|-------------------------|
| M3 | Raster corpus; classificazione layout / busta vs altro |
| M4 | Primo `raster_reference` + ROI; extract vettoriale |
| M5–M6 | Soglie, report JSON, test golden |
| M7 | Agente: ordine Render → Raster QA → pass/fail |
| M10 | UI diff visivo su KO |

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

**Qualità “indistinguibile” (operativa):** stesso layout e posizioni campi degli esempi Y **a schermo**; gate **dual-channel** (§4.3): placement vettoriale ≥98% **e** raster QA su ROI dinamiche. Uscita sempre **PDF vettoriale** (strategie A/B preferite su buste native Zucchetti). Non è clone forense byte-identico.

---

## 7) Interfaccia grafica (due fasi)

### 7.1 Prototipo (M4–M7) — Streamlit

| Schermata | Funzione |
|-----------|----------|
| Home | Scelta `doc_type_id` / route |
| **Admin training** | Upload corpus, avvio learn, versione template attiva |
| Genera | Upload X / textarea / form partial → stepper pipeline |
| Risultato | Anteprima PDF, tabella provenance, filtro “solo imputati”, modifica, download |
| Export | PDF + `imputation_report.json` + `dual_channel_qa_report.json` |
| QA visivo | Anteprima diff ROI se raster QA fallisce (M7+) |

### 7.2 Produzione (M10) — React + FastAPI

Stesso flusso; **deploy URL separato** dal Validator (secondo pezzo portfolio). In M10 la chat (§7.3) può convivere con dashboard classica (upload, report, diff ROI).

> **Prerequisito didattico (25/08/2026):** prima di costruire queste schermate, attivare il ripasso React/Node in [`docs/ripasso_frontend_react/README.md`](../../ripasso_frontend_react/README.md) (impegno in `CONTESTO_CORSO.md`). Non saltare se lo studente è arrugginito su React.

### 7.3 Interfaccia conversazionale (chat) e ciclo di miglioramento

> **Decisione prodotto:** l’operatore può usare una **chat** come front-end principale: stesso motore di §4.2, orchestrato da **agente** (M7+). La conversazione guida intenti e correzioni; il **miglioramento duraturo** del modello/layout passa da **feedback strutturato e governance**, non da ogni messaggio in chat senza filtri.

#### Cosa fa la chat (runtime)

| Ruolo chat | Cosa esegue il sistema sotto |
|------------|------------------------------|
| Richiesta in **NL** (Natural Language — linguaggio naturale) | Parse intent → piano multi-step (come §1.1), chiarimenti se mancano `pratica_id`, anno, template |
| Upload allegati | Stesso ingresso `transfer_xy` / partial; i file non “stanno nella memoria LLM” come training — vanno in storage pratica |
| “Correggi il netto di marzo / cambia template / rigenera CU” | Aggiorna **payload** o `template_version` su `pratica_id` → riesegue Transfer → Impute → Compute → Render → Raster QA |
| “Perché è giallo?” | Legge `imputation_report` + `dual_channel_qa_report` + provenance; **non** inventa calcoli — spiega gate falliti |

La chat è **UI + orchestrazione**; i **calcoli** restano in **Compute (Python)**; coordinate e totali **mai** delegati a LLM (allineato a §4.2–§4.3).

#### Tre livelli di “progressione” (evitare confusione)

| Livello | Origine | Effetto | Frequenza |
|---------|---------|---------|-----------|
| **A — Sessione / pratica** | Messaggi operatore nella chat | Aggiorna stato `pratica_id`, payload, rigenerazioni | Ogni conversazione |
| **B — Prodotto (governance)** | Segnalazioni esplicite (“layout 2025 nuovo”, “ROI campo X sempre KO”) | Eventi strutturati → backlog → revisione umana → aggiornamento soglie QA, ROI, registry | Settimanale / on-demand |
| **C — Riaddestramento** | Nuovi PDF in corpus approvati + rilancio learn | Nuovi `geometry_template`, `raster_reference`, `imputation_profile`, versione template | Job offline (admin), non in tempo reale per ogni messaggio |

**Regola:** la stringa di chat **non** sostituisce il corpus; **non** ogni battuta diventa training. Solo dati/versioni **approvati** alimentano il livello C.

#### Eventi di feedback (opzionale, consigliato per tracciabilità)

Per collegare chat a miglioramento (livello B→C), persistere JSON minimi (esempio concettuale):

- `feedback_type`: `correction_payload` | `qa_false_positive` | `layout_drift` | `template_request`
- `pratica_id`, `field_id` opzionale, `template_version`, `user_id`, `timestamp`
- `approved_for_corpus`: boolean (solo se true → ammissibile a cartella corpus dopo anonimizzazione)

Integrazione con **Validator**: esiti rossi/gialli possono generare lo stesso tipo di evento verso una coda condivisa (dataset errori).

#### Rischi e mitigazioni

| Rischio | Mitigazione |
|---------|-------------|
| **GDPR** / log sensibili | Retention chat, minimizzazione, no PII in log LLM dove evitabile; buste mai in git |
| **Deriva** del modello | Nessun fine-tuning “live” da chat; solo payload + versioni artefatti |
| **Allucinazione** intent | Conferma operatore su piano prima di generare (toggle “esegui piano”) |
| **Scope Fixer libero** | La chat **non** patcha PDF **senza lineage** Replicator; la modalità **`controlled_fix`** (§3b) impone bundle + audit. Fix “libero” su terzi resta **vietato** in architettura. |

#### Moduli corso

| Modulo | Contributo |
|--------|-------------|
| M5 | NL → structured output per intent e slot-filling (non calcoli) |
| M7 | Agente con tool: `run_pipeline`, `update_payload`, `attach_pdf`, `export_bundle` |
| M10 | React: thread chat + anteprima PDF + diff ROI + approvazione piano |

---

## 8) Integrazione con Validator

> **Canone:** [`CANONE_STRESS_TEST_LAB_VR.md`](CANONE_STRESS_TEST_LAB_VR.md)

### 8.1 Export verso Validator (`export_mode: stress_test`)

- **Un solo file:** PDF in cartella ingest Validator.
- **Nessun** bundle, report o lineage nella stessa path ingest.
- PDF con `metadata_mimic_y` + layout indistinguibile da export Y reale.

### 8.2 Export interno (`export_mode: internal`)

- `payload.json`, `imputation_report.json`, `dual_channel_qa_report.json`, `fix_report.json`, lineage.
- Path: `dati/lab/antagonist/runs/{run_id}/internal/`.
- Uso: QA Replicator, debug, manifest ops — **vietato** a pipeline Validator.

**Metriche build (interno):** placement vettoriale, raster QA, % imputati, ROI fallite.

### 8b) Loop antagonista (red team lab)

> [`PROTOCOLLO_LOOP_ANTAGONISTA_VR.md`](PROTOCOLLO_LOOP_ANTAGONISTA_VR.md)

| Esito Validator (solo PDF) | Azione Replicator |
|----------------------------|-------------------|
| Alterata **bloccata** | OK — profilo realistico o aumentare difficoltà numerica |
| **Evasion** | Input rule discovery — **non** abbassare soglie Validator |
| QA interno fail | Fix template/render prima di nuovo `stress_test` export |

**Divieto:** massimizzare pass rate Validator; pulire PDF cliente; lasciare inghippo “Replicator” nei metadati PDF.

---

## 9) Contratti dati e schemi

| Artefatto | File schema |
|-----------|-------------|
| Valori campi | [`schema_canonico_v01.json`](../../schema_canonico_v01.json) |
| Layout | [`schema_geometry_template_v01.json`](../../schema_geometry_template_v01.json) |
| Route X→Y | [`schema_transfer_route_v01.json`](../../schema_transfer_route_v01.json) |
| Imputazione | [`schema_imputation_profile_v01.json`](../../schema_imputation_profile_v01.json) |
| Raster + QA dual-channel | [`schema_raster_reference_v01.json`](../../schema_raster_reference_v01.json) |
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
| M3 | OCR/scansioni; raster corpus; layout fingerprint |
| M4 | Learn layout (V) + `raster_reference` (R), extract |
| M5 | Interpret discorsivo |
| M6 | RAG regole testo (opzionale) |
| M7 | Agente tool pipeline + **primi flussi chat** (piano → tool → report) |
| M8 | Fine-tuning Interpret (opzionale) |
| M9 | Docker, CI |
| **M10** | App deployata: P0 busta transfer_xy + P1 un altro tipo; **chat** opzionale come UX primaria (§7.3) |

Dipendenze: blocco **Applicativo / Replicator** in `requirements.txt` (scommentare da M4).

---

## 12) Definition of Done M10 (Replicator)

- [ ] UI Streamlit o React funzionale (upload → report → download)
- [ ] (Opzionale M10) **Chat** conversazionale: piano visibile, conferma prima di generare, storico per `pratica_id` (§7.3)
- [ ] UI **admin training** (corpus + learn)
- [ ] P0: `transfer_xy` busta paga — dual-channel QA documentato (V ≥98% placement + R soglie §4.3)
- [ ] P1: un secondo tipo con `partial_inputs` + imputazione
- [ ] Audit: provenance + `imputation_report` + `dual_channel_qa_report` su ogni generazione
- [ ] **Fixer controllato** (`controlled_fix`): almeno **rigenerazione** da bundle con `fix_report` + QA V+R (§3b); patch allowlist opzionale P2

---

## 13) Compliance e rischi

| Rischio | Mitigazione |
|---------|-------------|
| Campi imputati presentati come reali | Report UI + disclaimer + export audit |
| Dual-use / falsificazione | Route registrate, uso interno, metadati onesti |
| Scope 10 tipi in M10 | Fasi P0/P1/P2 — vedi DOCUMENT_SPECTRUM |
| Drift software emittente | `template_version` + nuovo `raster_reference` |
| Layout alterato / reflow | `layout_fingerprint` UNKNOWN + dual-channel fail |
| Solo QA matematico | Gate raster obbligatorio §4.3 |
| Log chat con PII | Retention, crittografia, accesso RBAC; export audit senza duplicare dati sensibili in chiaro |

---

## 14) API e CLI (bozza)

- `POST /api/v1/replicate/{doc_type_id}` — body: `natural_language` | `partial` | upload PDF (transfer)
- `POST /api/v1/fix/{doc_type_id}` — body: PDF lineage + bundle correzioni; risposta: nuovo PDF + report + `fix_report` append (§3b)
- `POST /api/v1/sessions/{session_id}/message` — turno chat: body testo + allegati; risposta = piano aggiornato, `run_id`, link report (M7+)
- `POST /api/v1/feedback` — evento strutturato livello B (§7.3), dopo autenticazione
- `POST /api/v1/admin/learn/{doc_type_id}` — rilancia training
- CLI: `python -m aplicativo.replicator.cli replicate --doc-type ...`

WebSocket o SSE (Server-Sent Events — stream eventi dal server) opzionali per streaming token piano/risposta chat.

---

## 15) Gap e prontezza implementativa

Dettaglio esteso (checklist G1–G10, diagrammi, DoD): [`ARCHITETTURA_PRODOTTO_DUE_APP.md`](ARCHITETTURA_PRODOTTO_DUE_APP.md) §6–§8.

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
| 2 Layout | `geometry_template_v01.json` | pdfplumber, cluster bbox, ancore relative |
| 2b Raster | `raster_reference_v01.json` + PNG/maschere | PyMuPDF pixmap, ROI, SSIM |
| 3 Campi | `field_map.json` | etichette + review umana |
| 3b Imputazione | `imputation_profile.json` | statistiche su corpus Y |
| 6 QA | `qa_report.json` + `dual_channel_qa_report` | hold-out V+R (§4.3) |

### Fasi runtime (dopo training)

| Step | Input | Output |
|------|-------|--------|
| Extract | PDF X | `payload_source` (solo `transfer_xy`) |
| Interpret | testo discorsivo | `payload_draft` (M5+, LLM structured) |
| Transfer | payload sorgente | payload allineato a Y |
| Impute | campi mancanti | valori + provenance |
| Compute | payload | totali/vincoli (**solo Python**) |
| Render | payload + template | PDF vettoriale (A / B / C) |
| Raster QA | PDF generato | `dual_channel_qa_report.json` |

**Percorso `controlled_fix`:** ingresso alternativo — §4.2b (dopo validazione lineage: merge payload → … → stessa tabella da Transfer in giù).

**Stack:** pdfplumber, PyMuPDF, reportlab, pypdf; OCR opzionale M3; raster QA PyMuPDF (DPI fisso). **Mai** LLM per coordinate o totali. **Mai** uscita finale “solo immagine” per buste native se esiste percorso vettoriale A/B.

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
| 2026-05-20 | Input discorsivo; pipeline Fasi 0–7; Fixer “libero” escluso (sostituito 2026-05-22 da **§3b controllato**). |
| 2026-05-21 | Master file; transfer X→Y; imputazione; tre modalità; split due app; doc in `docs/prodotto/`. |
| 2026-05-21 | **Dual-channel QA (V+R):** fedeltà visiva prioritaria; raster come gate/calibrazione; `schema_raster_reference_v01.json`; obiettivo a schermo (non clone forense). |
| 2026-05-21 | **North Star §1.1:** richiesta NL multi-doc (es. 3 buste X → BP Zucchetti + CU anno precedente) nella stessa `pratica_id`. |
| 2026-05-21 | **§7.3 REPLICATOR — Chat + ciclo miglioramento:** UI conversazionale sulla stessa pipeline; livelli A/B/C (sessione → feedback approvato → retrain offline); eventi strutturati; divieto apprendimento live non governato dalla chat. |
| 2026-05-22 | **Fixer controllato §3b:** modalità `controlled_fix`; lineage + bundle; preferenza rigenerazione; patch allowlist P2; `fix_report`; divieto fix libero su PDF terzi. |
| 2026-05-22 | **Loop antagonista §8b:** protocollo 8 step V↔R; `stress_profile_id`; evasion alimenta rule discovery; successo = Validator più forte. |
| 2026-05-22 | **Canone stress test §1.2 / §8:** `CANONE_STRESS_TEST_LAB_VR.md`; export stress_test (solo PDF) vs internal; `metadata_mimic_y`; Validator cieco. |
