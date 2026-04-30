# Appunti Tool di Fixing - Controllo Documentale AI

> Documento vivo: aggiornalo a ogni decisione importante.
> Obiettivo: formalizzare il **Tool di Fixing** come componente integrato del prodotto descritto in `APPUNTI_APPLICATIVO.md`.
> Insieme, Validator + Fixer formano un unico applicativo end-to-end di "Validazione e Riparazione assistita".

---

## 0) Posizionamento del Tool di Fixing nel prodotto

Il prodotto complessivo si compone di due motori cooperanti:

- **Validator** (vedi `APPUNTI_APPLICATIVO.md`): rileva incoerenze e produce
  `score_genuinita`, `prob_alterato`, `anomaly_score`, `semaforo`, `motivi_top3`,
  `check_results`, `evidenze`, `azione_consigliata`.
- **Fixer** (questo documento): a partire dagli output del Validator, propone
  correzioni motivate (guidate dalla **stessa knowledge base RAG** del Validator),
  che l'operatore approva o scarta. Dopo ogni fix applicato, la pratica viene
  **ri-validata** automaticamente.

Regola fondante:

- il Fixer **non altera mai contenuto sostanziale** (importi, date fiscali,
  anagrafica) senza una **prova forte** (fonte esterna o vincolo deterministico)
  o un **override umano esplicito**.
- il RAG e' fonte di **regole, vincoli e fix template**, non di **valori**.

---

## 1) Visione tool

Trasformare l'esito Validator (`semaforo` giallo/rosso con `motivi_top3` e
`check_results` falliti) in un percorso guidato, dove l'operatore puo:

- vedere chiaramente "perche" qualcosa non torna
- ricevere proposte di fix motivate dalla KB RAG
- approvare/scartare ogni proposta con un click
- riportare la pratica al `semaforo` verde **solo** se le correzioni applicate
  sono lecite e tracciate.

---

## 2) Problema che risolve

Situazione attuale (as-is) post-Validator:

- pratica gialla/rossa con motivazioni note ma nessun supporto operativo
  per correggere campi malformati o normalizzare formati
- l'operatore deve agire a mano, riaprire il documento, ricaricare, ripetere

Situazione target (to-be):

- proposte di fix per ogni `check_result` fallito quando esiste un fix lecito
- approvazione 1-click per i fix deterministici e grafici
- "needs_review" per i casi che richiedono fonte/prova esterna
- ri-validazione automatica fino a stato terminale (`PASS` / `NEEDS_REVIEW` / `FAIL`)

---

## 3) Utenti e ruoli

Coerenti con `APPUNTI_APPLICATIVO.md` sezione 3:

- Operatore/Consulente: vede le proposte, decide, fornisce eventuali prove
  (es. "il nome corretto e Marlo", documento aggiuntivo, conferma manuale).
- Revisore senior: gestisce fix `needs_review` e gli `override` con fonte.
- Admin: gestisce regole, fix template, soglie e versioni del Fixer.

---

## 4) Scope (input)

Input del Fixer:

- pratica gia processata dal Validator (campi canonici da `DATA_CONTRACT_v0.1`)
- `check_results` strutturati con `rule_id`, `evidenze`, `severity`
- (opzionale) "file di confronto" usati dal Validator per regole grafiche
  (font policy, layout policy)

Documenti coperti in P0:

- Buste paga, CU, Estratto conto corrente, F24, Lista movimenti
  (allineati a `MVP_SCOPE_v0.1`)

---

## 5) Output attesi (per pratica)

> Output canonico del Fixer (estende l'output del Validator).

- `proposte_fix` (lista di `FixProposal`, vedi sezione 18.1)
- `fix_applicati` (lista di `FixApplied` con id, motivazione, prove)
- `stato_fixing` (enum):
  - `NESSUN_FIX_NECESSARIO`
  - `FIX_PROPOSTI`
  - `FIX_APPLICATI`
  - `NEEDS_REVIEW`
  - `BLOCCATO_FRODE_SOSPETTA`
- `re_validation` (output Validator dopo l'applicazione: `score_genuinita`,
  `semaforo`, `motivi_top3`, `check_results`)
- `audit_trail_fix` (vedi sezione 11)

---

## 6) Requisiti funzionali

### 6.1 Generazione proposte

- per ogni `check_result` fallito o `evidenza` con `severity = fixable`,
  generare una o piu `FixProposal`
- ogni proposta deve avere `rule_id`, motivazione (testo + citazione KB),
  `confidence`, `precondizioni`

### 6.2 Categorie di fix supportate (P0)

- **Normalizzazione formato**: date, numeri, separatori, spazi/maiuscole
- **OCR cleanup verificabile**: solo se confermato da vincoli (regex,
  check-digit, charset, range, cross-check)
- **Ricalcolo campi derivati**: totali / netto / IVA / saldo, **solo** quando
  tutte le componenti sono presenti e coerenti
- **Coerenza inter-documento**: uniformazione di un campo (es. `intestatario_nome`)
  rispetto agli altri documenti della stessa pratica
- **Fix grafici PDF**: font policy (sostituzione/embedding), relayout, glifi
  speciali, **senza alterare contenuto testuale**

### 6.3 Approvazione umana (Approve / Reject)

- ogni fix richiede approvazione esplicita dell'operatore (anche
  `confidence = high`)
- bottoni `Applica` / `Scarta` in UI
- batch opzionale: "Applica tutti i fix con evidenze forti", sempre con
  conferma riassuntiva
- `Undo` per l'ultima applicazione

### 6.4 Override umano con fonte

- l'operatore puo dichiarare un valore come "verita di fonte" (es. CF,
  IBAN, nome corretto), allegando la motivazione
- l'override genera proposte di **uniformazione** sugli altri documenti,
  sempre con approvazione
- ogni override scrive una **trace leggera** (vedi sezione 11) con i 5
  campi minimi: timestamp, campo, old, new, fonte. Nessun audit pesante in
  modalita single-user, ma riproducibilita garantita.

### 6.5 Loop ri-validazione

- dopo `Apply`: `validate(documento_fixato)` automatico
- mostra delta: `semaforo` prima/dopo, nuovi `check_results`
- termine: `PASS` oppure `NEEDS_REVIEW` (non si forza mai PASS)

### 6.6 Allineamento al RAG del Validator

- il Fixer interroga **la stessa base conoscenza** del Validator (sezione
  9 di `APPUNTI_APPLICATIVO.md`)
- query lato Fixer: regole + vincoli + fix template per `rule_id`
- divieto: il RAG non deve restituire **valori da inserire** in importi,
  date fiscali o dati anagrafici

### 6.7 Anti-abuso (segnali frode severi)

- se `semaforo = rosso` per segnali severi (forensics/regole), il Fixer
  **non propone fix sostanziali**
- propone solo: "richiedi originale", "richiedi seconda fonte", "manda a
  revisore senior"
- i fix grafici non possono essere usati per **nascondere** segnali di
  alterazione

---

## 7) Requisiti non funzionali

- Sicurezza: ogni `apply_fix` su PDF/file genera nuova versione, mai
  sovrascrittura distruttiva
- Privacy: stesse policy del Validator (PII, retention, mascheramento)
- Affidabilita: rollback automatico se la ri-validazione peggiora il `semaforo`
  rispetto allo stato pre-fix
- Osservabilita: metriche su tasso fix accettati, tasso rifiuto, tempo medio
  di sistemazione pratica

---

## 8) Architettura (bozza, integrata col Validator)

Componenti aggiunti al diagramma in `APPUNTI_APPLICATIVO.md` sezione 8:

- Servizio AI `Fixer Engine`:
  - `proposer` (genera FixProposal a partire da issues + RAG)
  - `applier` (applica fix approvati al documento canonico e/o al PDF)
  - `re_validator` (richiama il motore regole post-fix)
- API condivise con il Validator (stesso DB pratiche/documenti, stesso
  Vector DB per la KB)
- UI: pannello "Riparazione" nella pagina dettaglio pratica

Decisione architetturale ereditata:

- backend finale (Laravel unico vs ibrido Python AI) - aperta D1 in
  `APPUNTI_APPLICATIVO.md`. Il Fixer segue la stessa scelta.

---

## 9) Base conoscenza RAG - cosa serve al Fixer

Estende sezione 9 di `APPUNTI_APPLICATIVO.md` con campi specifici per il fixing:

Per ogni regola del motore (`rule_id`):

- `rule_id`
- descrizione + scopo
- categoria (numeric / format / consistency / ocr / graphic / fraud)
- `severity_default`
- `is_fixable` (true/false)
- `fix_templates` (lista di pattern di correzione ammessi)
- `evidence_required` (forte / debole / nessuna)
- `versione`, `valid_from`, `valid_to`, `source_id`

Regole:

- il Fixer puo proporre **solo** fix conformi a `fix_templates` della regola
- se `is_fixable = false` o `evidence_required = forte` senza fonte, va in
  `needs_review`

---

## 10) Dati e labeling (per il Fixer)

- conservare per ogni proposta: `accepted` / `rejected` / `edited`,
  motivo, prove, `time_to_decide`
- alimentare un dataset di training per:
  - calibrazione `confidence` proposte
  - prioritizzazione fix piu utili
  - active learning su falsi positivi/negativi

Vincolo:

- nessun training su valori sostanziali "indovinati" - solo su decisioni e
  metadati delle proposte

---

## 11) Audit (modalita single-user del gioco)

In modalita "gioco / single-user" (`fac-simile`) si usa una **trace leggera**,
NON un audit completo. Scopo: riproducibilita, debug, coerenza tra casi
simili - non compliance.

### 11.1 Trace leggera per fix automatici

Per ogni fix applicato (deterministico o suggerito dal RAG):

- `fix_id`
- `pratica_id`, `documento_id`, `campo`
- `old_value`, `new_value`
- `rule_id`
- `applied_at` (timestamp)

### 11.2 Trace leggera per override umano (opzione 2 scelta)

Per ogni override dell'operatore: solo i 5 campi minimi.

- `applied_at` (timestamp)
- `pratica_id` / `documento_id`
- `field` (campo canonico)
- `old_value` -> `new_value`
- `fonte` (testo libero, anche solo "confermato manualmente")

Motivo: in single-user non serve "chi ha approvato" (sei sempre tu), ma
restano utili "quando", "cosa" e "perche".

### 11.3 Audit completo (riservato a pilot/prod)

L'audit completo del prodotto reale (sezione 6.6 di
`APPUNTI_APPLICATIVO.md`) si riattiva quando il Fixer entra in pilot.
Si controlla via flag `audit_override.enabled` in `FIX_POLICY_v0.1`:

- `false` -> trace leggera (default in modalita gioco)
- `true` -> audit completo (chi/quando/perche/versione_kb/versione_fixer)

---

## 12) Roadmap incrementale (alto livello, allineata a release `APPUNTI_APPLICATIVO.md`)

- **R0 - Fondazione fix**: scaffolding `FixProposal`, integrazione con
  `check_results`, 5 fix template iniziali (date, numeri, totale derivato,
  netto = lordo - trattenute, OCR semplice).
- **R1 - Fixing operativo**: UI Approve/Reject per pratica, ri-validazione
  automatica, override manuale con fonte, undo.
- **R2 - Fixing intelligente**: proposte di coerenza inter-documento,
  proposte grafiche (font policy), tasso accettazione fix come KPI.
- **R3 - Fixing compliance**: audit fix nel report pratica, citazioni KB
  obbligatorie nelle motivazioni, versioning fix template.
- **R4 - Hardening**: rollback automatico, batch apply, metriche di stabilita
  fix (regressioni post-apply).

---

## 13) Posizionamento competitivo

Aggiunta concreta rispetto ai vendor citati in `APPUNTI_APPLICATIVO.md`
sezione 13 (Ocrolus, Inscribe, Resistant AI, Truv/Argyle):

- la maggior parte segnala anomalie ma **non propone correzioni** strutturate
  e auditabili dentro la stessa UI
- la nostra value prop si estende a:
  "Ridurre il rischio E ridurre il tempo medio di sistemazione pratica con
  proposte di fix spiegabili, approvate dall'operatore, e ri-validate."

---

## 14) MVP competitivo del Fixer (must-have v0.1)

- [ ] Lista `FixProposal` per pratica (con motivazione e prove)
- [ ] Bottoni Approve / Reject per ogni proposta
- [ ] Ri-validazione automatica post-fix
- [ ] Stato `stato_fixing` esposto in dashboard
- [ ] Audit fix base (chi/quando/perche)
- [ ] Override manuale con fonte
- [ ] Blocco su `semaforo = rosso` per frodi severe (no fix sostanziali)

---

## 15) KPI target del Fixer

- tempo medio di sistemazione pratica gialla: < 2 minuti
- tasso fix proposti accettati al primo colpo: >= 70%
- tasso pratiche che tornano `verde` dopo fixing approvato: >= 60% delle
  pratiche gialle iniziali
- regressioni post-fix (semaforo peggiora dopo apply): < 2%
- grounding motivazioni fix con citazione KB: >= 95%

---

## 16) Governance del documento

Stesse regole di `APPUNTI_APPLICATIVO.md` sezione 18:

- decisioni in "Decision log" con data/motivo/impatto
- niente feature fuori roadmap senza decisione scritta
- review ogni 2 settimane

---

## 17) Allineamento col corso (dual-track)

Il Fixer arriva concettualmente con i moduli M5-M7:

- M5 (LLM): generazione spiegazioni motivazione fix
- M6 (RAG): retrieval di regole + fix template dalla KB versionata
- M7 (Agents): orchestrazione del loop `validate -> propose -> apply -> validate`

Compatibile con il **progetto incrementale** del corso (Catalogo E-commerce
o controllo documentale, vedi `CONTESTO_CORSO.md` sezione "Progetto Incrementale").

---

## 18) Contratti dati

### 18.1 FIX_CONTRACT_v0.1

Scopo:

- definire la struttura unica di una `FixProposal` usabile tra Fixer Engine,
  motore regole e UI

Formato `FixProposal` (record canonico):

- `fix_id` (string, sistema)
- `pratica_id` (string, sistema)
- `documento_id` (string, sistema)
- `issue_id` (string, riferimento all'issue del Validator)
- `rule_id` (string, dalla KB)
- `category` (enum: numeric / format / consistency / ocr / graphic)
- `target` (campo canonico oppure elemento grafico/pagina)
- `operation` (enum: set_field / normalize / recompute / replace_font /
  embed_fonts / relayout)
- `old_value` (qualsiasi tipo, opzionale)
- `new_value` (qualsiasi tipo, opzionale)
- `rationale_text` (string, motivazione breve presa dalla KB)
- `kb_citation` (string, riferimento al chunk/regola KB)
- `precondizioni_passate` (lista di check automatici superati)
- `evidence_required` (forte / debole / nessuna)
- `confidence` (high / medium / low)
- `requires_human` (bool, sempre `true` in v0.1)
- `status` (proposed / approved / rejected / applied / failed)

Formato `FixApplied` (post-apply, modalita single-user / gioco):

Campi minimi (trace leggera, sezione 11):

- `fix_id`, `applied_at`, `field`, `old_value`, `new_value`, `result_status`,
  `re_validation_summary` (delta semaforo + check_results)

Campi opzionali (auto-fix derivato da RAG):

- `rule_id`, `kb_citation`

Campi opzionali (override umano):

- `fonte` (testo libero)

Campi attivati solo se `audit_override.enabled = true` (pilot/prod):

- `applied_by`, `pre_state` (snapshot completo), `post_state` (snapshot
  completo), `versione_kb`, `versione_fixer`

Definition of Done v0.1:

- contratto usato in almeno 1 fix template P0 e in 1 endpoint UI di approvazione

### 18.2 FIX_POLICY_v0.1

Scopo:

- decidere in modo coerente quando un fix puo essere proposto, applicato o
  bloccato

Logica decisionale:

1. Se `severity = fixable` e fix template ammesso dalla KB -> proposta.
2. Se `evidence_required = forte` e nessuna fonte -> `needs_review`.
3. Se l'issue e di categoria `fraud` o `forensics` con severita alta -> il
   Fixer **non propone fix sostanziali**, propone solo richieste di originale
   o revisione.
4. I fix grafici (font/layout) non possono essere applicati su issue di
   categoria `fraud` (no "ripulisci segnale").
5. **Eccezione single-user ultra-rapida (falso positivo)**: l'operatore puo
   sbloccare un fix grafico su una issue `fraud` SOLO tramite un'azione
   esplicita di declassamento (1 click) chiamata:
   `OPERATOR_FALSE_POSITIVE_OVERRIDE`.
   
   - Effetto: la issue passa da `category = fraud` a `category = graphic`
     (oppure `severity` viene abbassata a `needs_review`), e i fix grafici
     diventano applicabili.
   - Trace leggera obbligatoria (sezione 11.2): timestamp, pratica/documento,
     elemento, `fraud -> graphic`, `fonte` (testo libero; puo essere anche
     \"confermato manualmente\").
   - Senza questo passaggio, il bottone \"Applica fix grafico\" resta
     disabilitato.
6. I fix sostanziali (importi, date fiscali, anagrafica) richiedono **sempre**
   approvazione umana, anche con `confidence = high`.

Routing post-apply:

- se `re_validation` migliora il semaforo -> stato `FIX_APPLICATI`
- se neutro e residui `needs_review` -> stato `NEEDS_REVIEW`
- se peggiora -> rollback automatico + alert

Definition of Done v0.1:

- policy applicata in almeno 1 flusso end-to-end con 5 fix template P0

Versioning:

- `fix_policy_version`: `v0.1`
- `effective_date`: `2026-04-30`
- `owner`: `Gianluca + Mentor`

### 18.3 FIX_TEMPLATE_v0.1 (set iniziale)

Set minimo di fix ammessi (legati a `rule_id` del motore regole):

- `NORMALIZE_DATE_ISO` (formato date)
- `NORMALIZE_NUMBER_IT_TO_FLOAT` (parsing importi `1.234,00` -> `1234.00`)
- `RECOMPUTE_NETTO_FROM_COMPONENTS` (netto = lordo - trattenute, se complete)
- `OCR_FIX_DIGIT_LETTER_CONFUSION` (`O`/`0`, `I`/`1`) con vincoli regex/checksum
- `UNIFORM_FIELD_ACROSS_DOCS` (es. `intestatario_nome`) - sempre con override
- `REPLACE_NON_POLICY_FONT` (sostituzione font con embedding obbligatorio)
- `EMBED_FONTS_PDF` (embedding font mancanti)
- `RELAYOUT_OUT_OF_MARGIN` (riposizionamento testo entro area stampabile)
- `OPERATOR_FALSE_POSITIVE_OVERRIDE` (1 click: `fraud -> graphic` + trace
  leggera; abilita fix grafici su segnale inizialmente forense)

Azioni non-modificanti (non cambiano il documento; cambiano solo lo stato
operativo della pratica):

- `REQUEST_ORIGINAL_DOCUMENT`
- `REQUEST_ALTERNATIVE_SOURCE`
- `ESCALATE_SENIOR_REVIEWER`

Vincoli:

- ogni template ha `precondizioni` espresse come funzioni booleane verificabili
- ogni template ha `evidence_required` esplicito
- nessun template "free-form" (no LLM che genera valori)

### 18.4 ROADMAP_90_GIORNI_FIXER_v0.1 (focus R0-R1)

Settimane 1-2 (R0):

- definizione `FixProposal` + endpoint generazione proposte da `check_results`
- 3 fix template (date, importi, netto)

DoD:

- pratica gialla genera almeno 1 proposta corretta nei casi test

Settimane 3-4 (R0):

- UI Approve/Reject + ri-validazione automatica + undo

DoD:

- operatore applica almeno 5 fix end-to-end con delta semaforo registrato

Settimane 5-6 (R1):

- override umano con fonte + uniformazione inter-documento
- audit fix base

DoD:

- 10 pratiche P0 portate da giallo a verde con audit completo

Settimane 7-8 (R1):

- fix grafici (font policy) sui PDF di confronto del Validator
- KPI Fixer in dashboard

DoD:

- 5 pratiche con fix grafici applicati senza alterazioni di contenuto

Settimane 9-12 (buffer):

- stabilizzazione + tuning soglie `confidence` proposte
- chiusura decisioni aperte sul Fixer

DoD:

- readiness per pilot interno integrato (Validator + Fixer)

### 18.5 OPEN_DECISIONS_FIXER_v0.1

| ID | Decisione | Owner | Target date | Stato | Impatto |
|---|---|---|---|---|---|
| F1 | Set definitivo fix template P0 (numero e priorita) | Gianluca + Mentor | 2026-05-15 | todo | R0 Fixer |
| F2 | Soglie `confidence` per proporre / classificare needs_review | Gianluca + Mentor | 2026-05-15 | todo | UX e KPI |
| F3 | Modalita rollback (sempre automatica vs configurabile) | Mentor | 2026-05-22 | todo | Affidabilita |
| F4 | Politica audit fix in modalita single-user / pilot | Gianluca + Mentor | 2026-05-25 | todo | Compliance / coerenza prodotto reale |
| F5 | Strategia fix grafici PDF (libreria: pikepdf vs PyMuPDF vs reportlab) | Gianluca | 2026-06-05 | todo | Implementazione R1 |

Regola:

- nessuna decisione bloccante resta `todo` oltre la target date senza nuova
  data esplicita.

---

## 19) Vincoli, rischi e mitigazioni

- Rischio: dual-use (il Fixer riusato per falsificare).
  Mitigazione: `FIX_POLICY_v0.1` (no fix su valori sostanziali senza fonte),
  blocco su `fraud severi`, audit fix.

- Rischio: il RAG genera proposte basate su valori "simili".
  Mitigazione: KB indicizza solo regole/vincoli/fix template, mai valori
  da copiare; precondizioni sempre verificate prima dell'apply.

- Rischio: regressioni post-fix.
  Mitigazione: rollback automatico se `semaforo` peggiora.

- Rischio: utente che approva tutto senza leggere.
  Mitigazione: motivazione + prove visibili in UI; richiesta conferma su
  fix sostanziali.

---

## 20) Open questions (da chiudere)

Fonte unica di verita:

- tutte le decisioni aperte sono in `18.5 OPEN_DECISIONS_FIXER_v0.1` con
  owner, target date e impatto.

---

## 21) Decision log

Formato:

```text
DATA:
DECISIONE:
MOTIVO:
IMPATTO:
NEXT STEP:
```

### Storico

- 2026-04-30: Creato `APPUNTI_TOOL_FIXING.md` come spec del Tool di Fixing
  integrato col Validator. Output canonico (`proposte_fix`, `stato_fixing`,
  `re_validation`, `audit_trail_fix`) allineato a terminologia
  `APPUNTI_APPLICATIVO.md`. Introdotti contratti `FIX_CONTRACT_v0.1`,
  `FIX_POLICY_v0.1`, `FIX_TEMPLATE_v0.1` e roadmap 90 giorni dedicata.
- 2026-04-30: Adottata **trace leggera** per override umano in modalita
  single-user (gioco). Sezione 11 ridefinita con tre livelli (auto-fix,
  override umano 5 campi, audit completo riattivabile via flag
  `audit_override.enabled` in pilot/prod). Aggiornato `FixApplied` in
  `FIX_CONTRACT_v0.1`. Motivo: lo studente e l'unico operatore in modalita
  gioco, non serve audit pesante; riproducibilita garantita dai 5 campi
  minimi. L'audit completo resta requisito del prodotto reale
  (`APPUNTI_APPLICATIVO.md` 6.6) e si riattiva al pilot.
