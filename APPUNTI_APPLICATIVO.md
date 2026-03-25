# Appunti Applicativo - Controllo Documentale AI

> Documento vivo: aggiornalo a ogni decisione importante.
> Obiettivo: trasformare l'idea in specifiche chiare, implementabili e verificabili.

---

## 1) Visione prodotto

Costruire un applicativo che aiuti un consulente bancario a valutare la genuinita dei documenti reddituali e fiscali dei clienti, con:

- analisi documentale automatica
- controlli incrociati multi-documento
- spiegazioni leggibili per operatore
- tracciamento completo per audit/compliance

---

## 2) Problema che vogliamo risolvere

Situazione attuale (as-is):

- verifica manuale lenta e soggetta a errori
- layout documenti diversi tra software/enti
- difficile trovare incoerenze nascoste tra documenti correlati

Situazione target (to-be):

- pre-screening automatico
- semaforo rischio (verde/giallo/rosso)
- motivazione chiara e verificabile per ogni esito

---

## 3) Utenti e ruoli

- Operatore/Consulente bancario: carica documenti, legge esito, decide azione.
- Revisore senior: valida casi dubbi, conferma/esclude anomalie.
- Admin: gestisce regole, permessi, versioni e monitoraggio.

---

## 4) Scope documenti (input)

Documenti da gestire (prima versione):

- Buste paga
- CU
- Modello UNILAV
- Estratto conto previdenziale
- Estratto conto corrente
- Lista movimenti
- Modello ISEE
- Modelli Unici
- F24
- Invii telematici

Note:

- supportare PDF nativi + PDF scansione + immagini
- gestire documenti incompleti o di bassa qualita

---

## 5) Output attesi (per pratica)

> Nomi campo tra parentesi = terminologia pipeline canonica (fonte: CONTESTO_CORSO.md, sezione "Pipeline ML del Prodotto").

- Punteggio genuinita 0-100 (`score_genuinita`, derivato da `prob_alterato`: `(1 - prob_alterato) * 100`)
- Probabilita di alterazione 0.0-1.0 (`prob_alterato`, output modello supervisionato)
- Score anomalia (`anomaly_score`, output modello non supervisionato)
- Semaforo (`semaforo`, derivato da `score_genuinita` con soglie calibrabili):
  - Verde: ok preliminare
  - Giallo: revisione manuale mirata
  - Rosso: blocco e audit completo
- Top 3 motivazioni dell'esito (`motivi_top3`)
- Controlli superati/falliti (`check_results`, lista strutturata regole deterministiche)
- Evidenze e fonti usate (`evidenze`)
- Azione consigliata all'operatore (`azione_consigliata`)

---

## 6) Requisiti funzionali

### 6.1 Ingestion documenti

- upload multiplo file per pratica
- classificazione tipo documento
- estrazione metadati base (nome file, data, hash, pagine)
- deduplica documenti

### 6.2 Estrazione dati

- OCR dove necessario
- parser campi chiave per tipo documento
- normalizzazione su schema canonico unico
- gestione confidence per campo estratto

### 6.3 Controlli e regole

- controlli deterministici (date, importi, codici, coerenze)
- controlli incrociati tra documenti stessa pratica
- regole versionate con validita temporale

### 6.4 Intelligenza AI

- rilevazione anomalie/pattern non noti (anomalia statistica + ML supervisionato quando possibile)
- assistenza LLM per spiegazione esiti
- RAG normativo/procedurale con citazioni fonte

### 6.5 Interfaccia operatore

- dashboard coda pratiche
- pagina dettaglio pratica con timeline controlli
- filtri, ricerca, esportazione report

### 6.6 Audit e feedback loop

- log decisioni complete (chi/cosa/quando/perche)
- revisione umana casi gialli/rossi
- active learning: feedback umano usato per migliorare modello

---

## 7) Requisiti non funzionali

- Sicurezza: cifratura dati a riposo/in transito, RBAC, audit accessi
- Privacy: minimizzazione, retention policy, mascheramento PII dove possibile
- Affidabilita: fallback se OCR/LLM non disponibili
- Prestazioni: tempo medio analisi pratica entro soglia target
- Osservabilita: metriche, alert, error tracking

---

## 8) Architettura (bozza)

- Frontend: React
- Backend business/API: Laravel o FastAPI (da confermare per fase finale)
- Servizi AI:
  - OCR + parsing
  - motore regole
  - scoring anomalia
  - RAG
- Database operativo: pratiche, documenti, esiti, audit
- Vector DB: base conoscenza normativa/procedurale
- Desktop wrapper (fase successiva): Electron/Tauri

Decisione da fissare:

- [ ] Backend unico Laravel con servizi AI esterni
- [ ] Backend ibrido Laravel + microservizio Python AI

---

## 9) Base conoscenza RAG - cosa salvare

Per ogni fonte:

- source_id
- ente/fonte
- url ufficiale
- data pubblicazione
- valid_from / valid_to
- versione
- hash contenuto
- testo pulito + chunk
- tags (tema, tipo norma, documento collegato)

Regola:

- mai usare solo testo non versionato
- ogni risposta RAG deve riportare citazione fonte

---

## 10) Dati e labeling

Stato iniziale noto:

- disponibili migliaia di documenti
- per parte dei documenti e nota almeno etichetta "originale/non originale"

Strategia:

- dataset gold iniziale piccolo ma pulito
- espansione progressiva con feedback umano
- separazione train/validation/test per tempo/pratica
- usare il dataset reale dello studente durante il corso, quando coerente con capitolo/esercizi deliverable
- lavorare per subset progressivi (non ingestione massiva iniziale)
- applicare anonimizzazione/pseudonimizzazione prima dell'uso didattico-operativo

---

## 11) Metriche di successo (KPI)

- Qualita estrazione campi (accuracy per campo)
- Precision/Recall/F1 su anomalia/frode
- Grounding rate risposte RAG (con citazioni valide)
- Tasso falsi positivi/falsi negativi
- Tempo medio analisi pratica
- Riduzione tempo revisione manuale

---

## 12) Roadmap incrementale (alto livello)

### Fase 1 - Fondazioni

- ingestion + OCR + schema canonico
- primi controlli deterministici
- dashboard minima pratica

### Fase 2 - Intelligence

- anomaly detection + scoring
- feedback loop revisore
- spiegazioni AI guidate

### Fase 3 - RAG e compliance

- base conoscenza versionata
- citazioni fonte obbligatorie
- audit trail completo

### Fase 4 - Prodotto

- hardening sicurezza/performance
- deploy stabile
- eventuale desktop wrapper

---

## 13) Benchmark mercato e lezioni operative (studio competitor)

Obiettivo di questa sezione:

- capire cosa fanno i player forti
- tradurre i pattern in funzionalita concrete per il nostro prodotto

### 13.1 Pattern comuni dei player leader

1. Verification waterfall (multi-fonte, non solo OCR):
   - payroll/direct-source
   - open banking
   - tax/docs upload
   - fallback manuale
2. Fraud forensics sul documento:
   - metadati, font, revisioni, struttura file
   - segnali visuali/evidenze per analista
3. Scoring + routing:
   - punteggio rischio
   - severita
   - coda revisione in base al rischio
4. Human-in-the-loop:
   - decisione finale ai casi dubbi
   - feedback riusato nel modello
5. API-first + eventi:
   - integrazione con sistemi esterni
   - webhook, audit e monitoring

### 13.2 Vendor osservati (riferimento strategico)

- Ocrolus: fraud signals, dashboard + API + webhook, evidenze visuali.
- Inscribe: trust score, severita, x-ray revisioni, metadata/pixel checks.
- Resistant AI: detection strutturale documenti, explainable verdict, policy per risk appetite.
- Truv / Argyle: verification waterfall e direct-source data.
- Point Predictive: scoring di plausibilita reddito dichiarato.
- Italia: Experian (verifica reddituale), CRIF (open banking, categorizzazione, KPI/scoring).

### 13.3 Traduzione in requisiti obbligatori per il nostro progetto

- [ ] Implementare verification waterfall reale (ordine fonti e fallback)
- [ ] Implementare fraud forensics (metadata/font/revisioni/duplicati)
- [ ] Implementare cross-check multi-documento per pratica
- [ ] Implementare score + severita + azione consigliata
- [ ] Implementare cockpit revisore (human-in-the-loop)
- [ ] Implementare audit trail completo e versioning regole/modelli
- [ ] Implementare metriche anti-frode e anti-false-positive

---

## 14) Strategia competitiva del prodotto (posizionamento)

### 14.1 Dove essere migliori dei competitor

- Focus Italia (documenti, flussi e norme locali)
- Spiegabilita operativa per consulente (non solo score)
- Cross-check profondo tra documenti eterogenei della stessa pratica
- Compliance-ready (audit forte + versioning + citazioni normative)

### 14.2 Value proposition sintetica

"Ridurre il rischio di accettare documenti non genuini, accelerando le decisioni creditizie con controlli spiegabili, auditabili e adatti al contesto normativo italiano."

---

## 15) Roadmap esecutiva (release-based)

### Release 0 - Fondazione dati (MVP tecnico interno)

- ingestion multi-file pratica
- OCR + parser base per 3 documenti core
- schema canonico unificato
- quality gate documento (leggibilita, completezza, duplicati)

Definition of Done R0:

- pipeline end-to-end funzionante su dataset campione
- output JSON normalizzato per pratica

### Release 1 - Controlli deterministici + dashboard operativa

- motore regole v1 (coerenza date/importi/codici)
- dashboard consulente con semaforo e motivazioni
- export report pratica

Definition of Done R1:

- almeno 20 regole implementate e testate
- esito pratica verde/giallo/rosso con evidenze

### Release 2 - Fraud intelligence

- anomaly detection su pattern non noti
- fraud forensics documento (metadati/font/revisioni dove disponibili)
- coda revisione prioritaria per severita

Definition of Done R2:

- modello anomalia in produzione interna
- revisore riceve top segnali con spiegazione

### Release 3 - RAG normativo e compliance by design

- base conoscenza normativa versionata
- retrieval con citazioni obbligatorie
- audit trail completo (decisioni + versioni)

Definition of Done R3:

- ogni spiegazione normativa contiene fonte e versione
- tracciamento completo praticabile in audit

### Release 4 - Hardening e rollout

- ottimizzazione performance/costi
- sicurezza e permessi avanzati
- deploy stabile + monitoraggio + alert
- opzionale: desktop wrapper

Definition of Done R4:

- SLA minimi rispettati
- readiness per pilot reale

---

## 16) MVP competitivo (must-have)

Per essere utile e competitivo gia in pilot:

- [ ] Semaforo decisionale + score + motivazioni top 3
- [ ] Evidence viewer (documento con punti sospetti evidenziati)
- [ ] Cross-check minimo su 5 documenti ad alta priorita
- [ ] Regole versionate con validita temporale
- [ ] Coda revisione e note revisore
- [ ] Audit export per pratica
- [ ] KPI operativi visibili in dashboard

---

## 17) KPI target iniziali (pilot)

Target da calibrare dopo i primi dati reali:

- tempo medio analisi pratica: < 5 minuti
- riduzione revisione manuale completa: >= 40%
- grounding risposte normative con fonte: >= 95% (target aspirazionale; la soglia minima DoD corso in CONTESTO_CORSO.md e >= 85%)
- tasso falsi positivi su casi verdi: soglia da definire in pilot
- copertura documentale MVP: >= 80% dei casi reali trattati

### Baseline iniziale (da compilare e aggiornare ogni settimana)

| KPI | Baseline (oggi) | Target pilot | Owner | Frequenza update |
|---|---|---|---|---|
| Tempo medio analisi pratica | n/a | < 5 minuti | Gianluca + Mentor | Settimanale |
| Riduzione revisione manuale completa | n/a | >= 40% | Gianluca + Mentor | Settimanale |
| Grounding risposte normative con fonte | n/a | >= 95% | Mentor | Settimanale |
| Tasso falsi positivi su casi verdi | n/a | da definire in pilot | Gianluca + Mentor | Settimanale |
| Copertura documentale MVP | n/a | >= 80% | Gianluca | Settimanale |

Regola:

- quando una baseline passa da `n/a` a valore numerico, registrare data e dataset di riferimento.

---

## 18) Governance del documento (come usarlo da oggi)

Regola di lavoro:

- ogni nuova decisione entra in "Decision log"
- ogni sezione con checkbox deve avere owner + data target
- niente sviluppo di feature fuori roadmap senza decisione scritta

Cadenza consigliata:

- review roadmap ogni 2 settimane
- review KPI ogni 1 settimana durante pilot

---

## 18.1 Allineamento con il corso (dual-track)

Da oggi questo documento guida anche la didattica:

- ogni capitolo deve avere un output "skill" (competenza) e un output "prodotto" (componente app)
- il task prodotto puo essere micro (15-30 minuti) ma deve lasciare un deliverable reale
- nessun capitolo "solo teoria/pratica astratta" se esiste un collegamento coerente al prodotto
- se il task tocca dati documentali, usare quando possibile il dataset reale dello studente (con campionamento e protezione dati)

Template rapido per capitolo:

```text
MODULO/CAPITOLO:
SKILL TARGET:
TASK PRODOTTO:
DELIVERABLE:
DEFINITION OF DONE:
IMPATTO SULLA ROADMAP (R0/R1/R2/R3/R4):
```

---

## 18.2 MVP_SCOPE_v0.1 (30% attuale)

Scopo:

- fissare cosa entra davvero nel primo pilot
- evitare dispersione su funzionalita premature

### In scope pilot (P0)

- Documenti:
  - Buste paga
  - CU
  - Estratto conto corrente
  - Lista movimenti (se fornita separata)
  - F24 (solo controlli base presenza/coerenza campi chiave)
- Output obbligatori per pratica:
  - score genuinita (0-100)
  - semaforo (verde/giallo/rosso)
  - top 3 motivazioni
  - evidenze principali
  - azione consigliata operatore
- Workflow operativo:
  - coda pratiche
  - dettaglio pratica
  - revisione umana su giallo/rosso

### Out of scope temporaneo (P1/P2)

- Modello UNILAV (parser completo)
- Estratto conto previdenziale (parser completo)
- Modello ISEE (parser completo)
- Modelli Unici e invii telematici avanzati
- Automazioni enterprise (integrazioni CRM complesse, orchestrazioni multi-tenant)

### Definition of Done MVP Scope v0.1

- esiste una lista ufficiale P0/P1/P2 condivisa
- i prossimi capitoli lavorano solo su P0 salvo eccezioni deliberate

---

## 18.3 DATA_CONTRACT_v0.1

Scopo:

- definire uno schema canonico minimo per normalizzare i dati estratti
- usare lo stesso contratto in parser, regole, scoring e UI

Formato record canonico (campi comuni):

- `pratica_id` (string, obbligatorio, sistema, confidence 1.0)
- `documento_id` (string, obbligatorio, sistema, confidence 1.0)
- `tipo_documento` (enum, obbligatorio, classificatore, confidence 0-1)
- `data_documento` (date, obbligatorio, estrazione, confidence 0-1)
- `intestatario_nome` (string, obbligatorio, estrazione, confidence 0-1)
- `intestatario_cf` (string, obbligatorio se presente nel documento, estrazione, confidence 0-1)
- `importo_netto` (float, opzionale per documenti non salariali, estrazione, confidence 0-1)
- `fonte_estrazione` (enum: ocr/parser/manuale, obbligatorio, sistema, confidence 1.0)

### Documento: Busta paga (v0.1)

Campi minimi:

- `datore_lavoro` (string, obbligatorio, parser, conf)
- `periodo_competenza` (string/date, obbligatorio, parser, conf)
- `retribuzione_lorda` (float, obbligatorio, parser, conf)
- `retribuzione_netta` (float, obbligatorio, parser, conf)
- `trattenute_totali` (float, opzionale, parser, conf)

### Documento: CU (v0.1)

Campi minimi:

- `anno_fiscale` (int, obbligatorio, parser, conf)
- `sostituto_imposta` (string, obbligatorio, parser, conf)
- `redditi_lavoro_dipendente` (float, obbligatorio, parser, conf)
- `ritenute_irpef` (float, opzionale, parser, conf)

### Documento: Estratto conto corrente (v0.1)

Campi minimi:

- `iban_parziale` (string, obbligatorio, parser, conf)
- `periodo_da` (date, obbligatorio, parser, conf)
- `periodo_a` (date, obbligatorio, parser, conf)
- `saldo_iniziale` (float, opzionale, parser, conf)
- `saldo_finale` (float, opzionale, parser, conf)
- `accrediti_stipendio_count` (int, derivato, regole, conf n/a)

### Definition of Done Data Contract v0.1

- schema canonico usato in almeno 1 parser P0
- output JSON coerente per i 3 documenti core

---

## 18.4 WATERFALL_POLICY_v0.1

Scopo:

- decidere in modo coerente come verificare una pratica senza blocchi operativi

### Logica decisionale iniziale

1. Se direct-source disponibile (payroll/open banking affidabile), usarlo come fonte primaria.
2. Se direct-source non disponibile, usare OCR + parser documentale.
3. Se confidence media estrazione < 0.75, inviare a revisione umana.
4. Se ci sono incoerenze critiche cross-documento, forzare almeno stato giallo.
5. Se segnali frode severi (forensics/regole), stato rosso + audit.

### Routing semaforo (v0.1)

- Verde:
  - nessuna incoerenza critica
  - confidence media >= 0.85
  - zero segnali severi
- Giallo:
  - incoerenze non bloccanti o confidence tra 0.75 e 0.84
- Rosso:
  - incoerenze critiche o segnali severi di manipolazione

### Output obbligatorio per decisione

> Nomi campo allineati alla terminologia pipeline in CONTESTO_CORSO.md.

- `score_genuinita` (0-100)
- `semaforo` (verde/giallo/rosso)
- `motivi_top3`
- `evidenze`
- `azione_consigliata`

### Definition of Done Waterfall v0.1

- policy documentata e applicata in almeno 1 flusso end-to-end
- ogni pratica test produce uno dei 3 esiti con motivazione

### Versioning policy

- `waterfall_policy_version`: `v0.1`
- `effective_date`: `2026-03-19`
- `owner`: `Gianluca + Mentor`
- ogni modifica a soglie o logica richiede nuova versione (`v0.2`, `v0.3`, ...)

---

## 18.5 ROADMAP_90_GIORNI_v0.1 (focus R0-R1)

### Settimane 1-2 (R0)

Owner: Gianluca + Mentor

- definizione schema canonico v0.1
- parser base su 3 documenti core
- quality gate minimo (leggibilita, duplicati)

Deliverable:

- `schema_canonico_v01.json`
- parser P0 con output JSON uniforme

DoD:

- 20 pratiche campione processate senza crash

### Settimane 3-4 (R0)

Owner: Gianluca + Mentor

- classificazione tipo documento base
- dashboard minima elenco pratiche + dettaglio essenziale

Deliverable:

- endpoint/API o file output per elenco pratiche
- vista dettaglio con campi estratti

DoD:

- operatore vede pratica e dati estratti in modo consistente

### Settimane 5-6 (R1)

Owner: Gianluca + Mentor

- regole deterministiche v1 (date/importi/coerenza minima)
- semaforo + score + motivazioni top3

Deliverable:

- motore regole v1
- output decisionale standard

DoD:

- almeno 20 regole attive e testate su dataset campione

### Settimane 7-8 (R1)

Owner: Gianluca + Mentor

- coda revisione giallo/rosso
- audit export pratica (decisione + evidenze)

Deliverable:

- vista coda revisione
- report esportabile per pratica

DoD:

- revisore completa il flusso su almeno 10 casi gialli/rossi

### Settimane 9-12 (buffer controllato)

Owner: Gianluca + Mentor

- stabilizzazione bug
- tuning soglie confidence/semaforo
- chiusura decisioni aperte bloccanti

Deliverable:

- release note pilot v0.1

DoD:

- readiness per test pilot interno

---

## 18.6 OPEN_DECISIONS_v0.1 (max 5)

| ID | Decisione | Owner | Target date | Stato | Impatto |
|---|---|---|---|---|---|
| D1 | Scelta backend finale (Laravel unico vs ibrido con servizio Python AI) | Gianluca + Mentor | 2026-04-15 | todo | Architettura R0-R2 |
| D2 | Soglie iniziali ufficiali semaforo e confidence | Gianluca + Mentor | 2026-04-20 | todo | Decision engine |
| D3 | Lista definitiva documenti P0 pilot | Gianluca | 2026-04-10 | in_progress | Scope MVP |
| D4 | Modalita audit export minima (formato e contenuti) | Mentor | 2026-04-25 | todo | Compliance operativa |
| D5 | Priorita integrazione esterna (se presente) | Gianluca + Mentor | 2026-05-05 | todo | Roadmap R1-R3 |

Regola:

- nessuna decisione bloccante resta `todo` oltre la target date senza nuova data esplicita.

---

## 19) Vincoli, rischi e mitigazioni

- Rischio: dati eterogenei troppo sporchi  
  Mitigazione: pipeline quality gate + fallback manuale.

- Rischio: modello non spiegabile  
  Mitigazione: separare regole deterministiche da punteggio AI e mostrare evidenze.

- Rischio: costi API elevati  
  Mitigazione: local-first dove possibile + caching + budget monitorato.

- Rischio: deriva normativa  
  Mitigazione: pipeline aggiornamento fonti e versioning.

---

## 20) Open questions (da chiudere)

Fonte unica di verita:

- tutte le decisioni aperte sono tracciate in `18.6 OPEN_DECISIONS_v0.1` con owner, target date, stato e impatto
- questa sezione resta solo come promemoria e non va popolata con una lista parallela

---

## 21) Decision log

Usa questo formato a ogni decisione:

```text
DATA:
DECISIONE:
MOTIVO:
IMPATTO:
NEXT STEP:
```

### Storico

- 2026-03-19: Creato file appunti operativo con struttura completa.
- 2026-03-19: Integrato studio competitor e trasformato il file in roadmap esecutiva competitiva (waterfall, forensics, HITL, score+routing, audit, release plan).
- 2026-03-19: Migliorata governabilita v0.1: owner aggiunti alla roadmap 90 giorni, sezione Open questions allineata a OPEN_DECISIONS, versioning policy Waterfall introdotta.

