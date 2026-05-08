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
