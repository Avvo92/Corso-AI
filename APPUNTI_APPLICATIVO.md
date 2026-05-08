# Appunti Applicativo - Controllo Documentale AI

> Documento vivo: aggiornalo a ogni decisione importante.
> Obiettivo: trasformare l'idea in specifiche chiare, implementabili e verificabili.
>
> **Componenti del prodotto** (unico applicativo end-to-end):
> - **Validator** (questo documento): rileva incoerenze e produce esito decisionale.
> - **Fixer** (vedi `APPUNTI_TOOL_FIXING.md`): propone correzioni motivate con
>   approvazione umana e ri-validazione automatica.
>
> I due componenti condividono terminologia, schema canonico (`DATA_CONTRACT_v0.1`),
> motore regole, base conoscenza RAG e UI.

---

## 1) Visione prodotto

Costruire un applicativo che supporti **operatori e intermediari** nel controllo della qualità e della coerenza dei documenti reddituali e fiscali che entrano in un **fascicolo cliente** (pratica mutuo, istuttoria creditizia, analoghi flussi document-heavy):

- analisi documentale automatica
- controlli incrociati multi-documento
- spiegazioni leggibili per operatore
- proposte di correzione assistite e ri-validazione automatica (vedi `APPUNTI_TOOL_FIXING.md`)
- tracciamento completo per audit/compliance

**Contesto operativo Gianluca**: intermediario nel campo mutui (banca); il primo utente del sistema è organizzazione/rete di cui fa parte. **Mercato esteso**: altri intermediari con funzioni analoghe (mediazione creditizia, reti broker, in parte outsourcing documentale) possono beneficiare dello **stesso nucleo** (ingest → classificazione → estrazione → regole configurabili → semaforo → audit), purché checklist e mapping campi restino **parametrizzabili** — non hard-coded solo sul primo cliente. Dettaglio strategico: §14.3 e checklist MVP “fuori casa”: §16.1.

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

- Operatore / consulente / **broker**: carica documenti per pratica, legge esito, gestisce richieste integrazioni al cliente.
- Rete o società di mediazione: admin configurazione checklist e soglie **per profilo prodotto** (template mutuo prima casa, switch, ecc.) quando si scala verso multi-organizzazione.
- Intermediario “esterno” (ipotetico cliente licenza): stessi ruoli sopra, con tenant/config separati — da progettare in M9-M10 se si persegue il riuso commerciale.
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
- Output del Fixer integrato (vedi `APPUNTI_TOOL_FIXING.md` sezione 5):
  - `proposte_fix` (lista `FixProposal`)
  - `fix_applicati` (lista `FixApplied`)
  - `stato_fixing` (`NESSUN_FIX_NECESSARIO` / `FIX_PROPOSTI` / `FIX_APPLICATI` /
    `NEEDS_REVIEW` / `BLOCCATO_FRODE_SOSPETTA`)
  - `re_validation` (delta semaforo dopo apply)
  - `audit_trail_fix`

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

### 6.7 Riparazione assistita (Fixer)

> Specifica completa in `APPUNTI_TOOL_FIXING.md`. Qui solo i requisiti che
> il prodotto principale deve esporre.

- generazione di `proposte_fix` per ogni `check_result` fallito o evidenza
  con `severity = fixable`
- approvazione esplicita dell'operatore (Approve/Reject) per ogni proposta
- override umano con fonte (es. "il nome corretto e Marlo") che genera
  proposte di uniformazione inter-documento
- ri-validazione automatica post-apply (loop `validate -> propose -> apply -> validate`)
- blocco fix sostanziali su segnali frode severi (`semaforo = rosso`):
  consentite solo richieste di originale/seconda fonte/revisione senior
- audit fix integrato nell'audit trail della pratica

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
  - **Fixer Engine** (vedi `APPUNTI_TOOL_FIXING.md` sezione 8):
    - `proposer` (genera `FixProposal` da `check_results` + RAG)
    - `applier` (applica fix approvati su record canonico e/o PDF)
    - `re_validator` (richiama il motore regole post-fix)
- Database operativo: pratiche, documenti, esiti, audit, **fix proposti/applicati**
- Vector DB: base conoscenza normativa/procedurale **condivisa Validator + Fixer**
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

### Decisione 30/04/2026 — Deliverable visivo M3 (busta paga vs altro)

- **Scopo didattico**: deliverable cap.07 M3 = classificatore CNN binario "busta paga vs non-busta paga" + demo Gradio + deploy HuggingFace Spaces (portfolio piece #2).
- **Scopo prodotto**: l'output diventa una feature aggiuntiva nel modello supervisionato M2 per smistamento iniziale dei documenti caricati dall'operatore (`prob_busta_paga_visivo`).
- **Dataset (confermato dallo studente)**:
  - ~200 buste paga reali del proprio archivio professionale
  - ~200 immagini "altro" da raccogliere da dataset pubblici (fatture, contratti, foto generiche) prima del cap.05 M3
- **Vincoli operativi BLOCCANTI (privacy/GDPR)**:
  1. Le buste paga reali NON si caricano mai su Colab/cloud nello stato originale.
  2. Pipeline di anonimizzazione PRIMA del training: script locale che applica maschere nere o blur su nome/CF/IBAN/indirizzi con `cv2.rectangle` (per il classificatore busta-paga-vs-altro interessa il **layout grafico**, non il testo).
  3. La cartella con le buste paga (anche anonimizzate) va in `.gitignore` PRIMA di iniziare il cap.05 M3. Mai committare nel repo.
  4. Su Colab si caricano SOLO le immagini anonimizzate.
- **Step a livello di capitolo**:
  - Cap.05 M3 — primo training su dataset pubblico low-stakes (Fashion-MNIST/CIFAR), niente buste paga.
  - Cap.06 M3 — transfer learning con ResNet pre-addestrata + script `anonimizza_buste.py` + setup dataset.
  - Cap.07 M3 — fine-tuning ResNet su busta-paga-vs-altro + Gradio + deploy.
- **Estensione futura (M3 bonus o M8)**: una volta acquisita la classificazione "busta paga vs altro", estendere a "alterato vs genuino" (segnali grafici di alterazione: font incoerenti, pixel editati, artefatti compressione) come fine-tuning aggiuntivo.

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

### 14.3 Contesto broker / intermediari e riuso verso terzi

**Ruolo di riferimento**: Gianluca opera come **broker di mutui** (intermediazione creditizia): il fascicolo unisce reddito dichiarato, stabilità lavorativa, coerenza tra fonti ed elementi di rischio documentale. Il Validator copre lo stesso “tipo di dolore” che in consulenza fiscale classica (incoerenze CU/buste/estratti), ma il **messaggio commerciale** verso terzi intermediari enfatizza: meno **tempo di preparazione fascicolo**, meno **integrazioni richieste** dall’istruttoria, **tracciabilità** delle decisioni.

**Matrice di posizionamento (semplificata)**:

| | Bassa profondità documentale | Alta profondità (incrocio multi-fonte) |
|--|------------------------------|----------------------------------------|
| **Bassa automazione** | Checklist manuali / Excel | Revisione solo umana (costosa) |
| **Alta automazione** | Solo OCR / DAM generico | **Sweet spot prodotto**: ingest strutturato + regole + ML/tabular + (opz.) vision + audit |

**Modelli di offerta verso terzi** (da definire con legale/commerciale): licenza d’uso, fee **setup + onboarding checklist**, abbonamento per volume pratiche, white-label per reti. Il corso arriva al livello **MVP deployabile + portfolio**; contratti, SLA e limitazione responsabilità sono fuori dal perimetro didattico ma vanno pianificati prima di una vendita “seria”.

**Da NON promettere** in pitch o materiale marketing senza review legale: sostituzione del compliance officer; garanzia esito positivo in banca; copertura illimitata di tutti i prodotti e istituti day-one.

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
- [ ] Fixer integrato (vedi `APPUNTI_TOOL_FIXING.md` sezione 14):
  - [ ] `proposte_fix` per pratica con motivazione e prove
  - [ ] Approve/Reject per ogni proposta + ri-validazione automatica
  - [ ] Blocco fix sostanziali su `semaforo = rosso` per frodi severe
  - [ ] Audit fix base (chi/quando/perche/prove)

### 16.1 MVP "vendibile fuori casa" (checklist corso — allineamento progetto incrementale)

Obiettivo: ogni task sul **progetto incrementale** (M5→M10) dovrebbe avvicinare a questo nucleo, così il deliverable M10 è **tecnica vendibile** (deploy + ripetibilità), non solo demo interna.

**Must-have commerciale** (ordine logico, non strettamente cronologico di sviluppo):

1. **Ingest universale** — caricamento multi-file per pratica (ZIP / drag-drop / API opzionale).
2. **Classificazione tipo documento** — almeno rule-based + miglioramento progressivo (ML/LLM dove previsto dal modulo).
3. **OCR + estrazione campi “minimum viable”** — insieme **ristretto** di campi ad alta leva (reddito, periodo, anagrafica base, IBAN se nel perimetro), non “tutti i campi del monso” al giorno 1.
4. **Motore regole configurabile** — soglie, checklist, mapping campi **senza** ricompilare tutto il codice per un nuovo intermediario.
5. **Semaforo pratica + lista azioni** — output actionable (cosa manca, cosa contraddice cosa).
6. **Export report** — PDF o equivalente riutilizzabile verso cliente o verso revisione interna.
7. **Audit minimale** — chi / quando / cosa caricato / esito controllo (anche log essenziale all’inizio).
8. **Privacy-by-design narrativo** — retention, anonimizzazione dove previsto (corso: buste M3, dati sensibili), documentazione per il decisore acquisti.

**Stretch**: webhook/API verso gestionale esterno; template multipli “profilo prodotto” (prima casa vs switch); multi-tenant.

**Collegamento corso**: `CONTESTO_CORSO.md` — Profilo → **Strategia prodotto**; Regola mentor su progetto incrementale.

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
- traccia sessione per capitolo: file `sessioni_capitoli/M##_CNN_*_sessione.md` nel modulo (vedi **Regola 39** e sezione **J** in `CONTESTO_CORSO.md`) — in chiusura capitolo il mentor integra quel diario con questo documento per task prodotto e priorità

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
| D6 | Adozione `APPUNTI_TOOL_FIXING.md` come spec ufficiale del Fixer integrato | Gianluca + Mentor | 2026-05-15 | in_progress | Architettura R0-R2, MVP, KPI |

Regola:

- nessuna decisione bloccante resta `todo` oltre la target date senza nuova data esplicita.
- le decisioni aperte specifiche del Fixer (F1-F5) sono in `APPUNTI_TOOL_FIXING.md`
  sezione 18.5 - non duplicarle qui.

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
- 2026-04-30: Integrato il **Tool di Fixing** come componente del prodotto:
  creato `APPUNTI_TOOL_FIXING.md` (spec v0.1) e aggiornate le sezioni 1, 5, 6,
  8, 16, 18.6 per esporre output canonico del Fixer (`proposte_fix`,
  `stato_fixing`, `re_validation`, `audit_trail_fix`), Fixer Engine in
  architettura, MVP must-have e decisione aperta D6. Validator + Fixer
  costituiscono ora un unico applicativo end-to-end di "Validazione e
  Riparazione assistita" con KB RAG e schema canonico condivisi.

