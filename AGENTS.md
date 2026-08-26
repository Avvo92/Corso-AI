# AGENTS — Hard Gate Operativo (Corso IA)

Questa repository usa un checkpoint bloccante di avvio sessione.

## Handshake obbligatorio

Se il PRIMO messaggio utente in una nuova chat contiene (case-insensitive) una variante tra:

- `jarvis pronto per iniziare`
- `jarvis pronto a iniziare`
- `jarvis pronto per incominciare`
- `jarvis pronto a incominciare`

l'agente DEVE:

1. Leggere `CONTESTO_CORSO.md` integralmente.
2. Non avviare nessuna attivita tecnica/didattica prima della lettura completa.
3. Rispondere **esattamente** e **solo** con:

`Jarvis pienamente operativo Sig. Stark`

4. Procedere con il lavoro solo dal messaggio successivo.

Dal messaggio successivo (e in tutte le chat corso): applicare il **Profilo linguistico** descritto in `CONTESTO_CORSO.md` → Profilo → **Profilo linguistico — chiarezza + glossario inline** (italiano semplice; acronimi sempre con spiegazione facile inline).

## Fail-safe

Se `CONTESTO_CORSO.md` non e leggibile/completo:
- NON eseguire handshake
- segnalare il blocco
- chiedere come procedere.

## Prodotto applicativo (due app)

Dopo il gate corso, per task sul **prodotto Validator/Replicator**:

1. [`CONTESTO_CORSO.md`](CONTESTO_CORSO.md) — stato attivo (M3)
2. Se serve storico: [`archivi/README.md`](archivi/README.md) (M1, M2, Ponte)
3. [`APPUNTI_APPLICATIVO.md`](APPUNTI_APPLICATIVO.md) — stub indice prodotto
4. [`docs/prodotto/README.md`](docs/prodotto/README.md) — indice completo prodotto
5. [`docs/prodotto/CANONE_STRESS_TEST_LAB_VR.md`](docs/prodotto/CANONE_STRESS_TEST_LAB_VR.md) — fonte di verita stress test (Validator solo PDF)
6. [`docs/prodotto/ARCHITETTURA_PRODOTTO_DUE_APP.md`](docs/prodotto/ARCHITETTURA_PRODOTTO_DUE_APP.md) — piano, gap, DoD M10
7. [`docs/prodotto/DOCUMENT_SPECTRUM.md`](docs/prodotto/DOCUMENT_SPECTRUM.md) — 10 tipi, P0/P1/P2
8. Validator → `docs/prodotto/APPUNTI_APPLICATIVO_VALIDATOR.md` + `aplicativo/validator/`
9. Replicator → `docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md` + `aplicativo/replicator/`
10. **Pre-M10 UI React:** [`docs/ripasso_frontend_react/README.md`](docs/ripasso_frontend_react/README.md) — ripasso Node/React (parcheggiato; attivare fine M9 / inizio M10). Dettaglio in `CONTESTO_CORSO.md` → Profilo → Impegno canonico.
