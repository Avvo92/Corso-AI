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

## Regola 43 — Ripasso propositivo (vincolante)

Se in un capitolo o in chat si **cita / riusa** un concetto di un capitolo precedente: **prima** del richiamo inserire un ripasso propositivo (`# 🔁 RIPASSO PROPOSITIVO` nei file; 2–5 frasi in chat). Dettaglio: [`CONTESTO_CORSO.md`](CONTESTO_CORSO.md) → Regole Didattiche **43**. Rule file: [`.cursor/rules/43-ripasso-propositivo.mdc`](.cursor/rules/43-ripasso-propositivo.mdc). **Non ignorabile.**

## Regola 44 — Esercizi di memoria operativa e libri riformulati (vincolante)

Dal 08/10/2026, per richiesta dello studente: ogni capitolo nuovo ha esercizi di **pipeline a memoria** (`⌨️`), **termini nuovi dentro gli esercizi** (`🔤`), almeno 1 esercizio **cross-capitolo** (`🌐`, 3+ pezzi di capitoli diversi) e i **libri riformulati nel capitolo**, mai “vai a leggere la sezione X”. Dettaglio: [`CONTESTO_CORSO.md`](CONTESTO_CORSO.md) → Regole Didattiche **44**. Rule file: [`.cursor/rules/mentor-ai-corso.mdc`](.cursor/rules/mentor-ai-corso.mdc) (regola chiave 21).

## Fail-safe

Se `CONTESTO_CORSO.md` non e leggibile/completo:
- NON eseguire handshake
- segnalare il blocco
- chiedere come procedere.

## Prodotto applicativo

**Attivo dal 05/10/2026:** torre di controllo (pratiche, meeting, scadenze). Brief: [`briefing_progetto_ia.md`](briefing_progetto_ia.md) e [`recap_progetto_ia.md`](recap_progetto_ia.md). Hardware e regole in [`CONTESTO_CORSO.md`](CONTESTO_CORSO.md) → Profilo e Strategia hardware. Interfaccia prevista in Laravel. Audio e telefonia del brief non sono capitoli del corso.

**In standby:** Validator e Replicator. Non assegnare task. Se lo studente li riapre, la mappa è questa:

1. [`CONTESTO_CORSO.md`](CONTESTO_CORSO.md) — stato attivo (M4 cap.01)
2. Se serve storico: [`archivi/README.md`](archivi/README.md) (M1, M2, Ponte)
3. [`APPUNTI_APPLICATIVO.md`](APPUNTI_APPLICATIVO.md) — stub indice prodotto
4. [`docs/prodotto/README.md`](docs/prodotto/README.md) — indice Validator/Replicator
5. [`docs/prodotto/CANONE_STRESS_TEST_LAB_VR.md`](docs/prodotto/CANONE_STRESS_TEST_LAB_VR.md) — fonte di verita stress test (Validator solo PDF)
6. [`docs/prodotto/ARCHITETTURA_PRODOTTO_DUE_APP.md`](docs/prodotto/ARCHITETTURA_PRODOTTO_DUE_APP.md) — piano, gap, DoD M10
7. [`docs/prodotto/DOCUMENT_SPECTRUM.md`](docs/prodotto/DOCUMENT_SPECTRUM.md) — 10 tipi, P0/P1/P2
8. Validator → `docs/prodotto/APPUNTI_APPLICATIVO_VALIDATOR.md` + `aplicativo/validator/`
9. Replicator → `docs/prodotto/APPUNTI_APPLICATIVO_REPLICATOR.md` + `aplicativo/replicator/`
10. **Ripasso React/Node:** parcheggiato. Non è il frontend del prodotto attivo (quello è Laravel). Si riapre solo se si torna a Validator/Replicator. Dettaglio in `CONTESTO_CORSO.md` → Profilo → Impegno canonico.
