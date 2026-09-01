# Diario sessione — Capitolo 09 — Transfer learning e primo dataset reale

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `09_transfer_learning.py` |
| **File diario** | `M03_C09_transfer_learning_sessione.md` |
| **Stato** | in corso (aperto 01/09/2026) |
| **Voto difficoltà** | — |

---

## Obiettivi del capitolo (per il mentor)

- Far arrivare lo studente a un modello `busta_vs_altro.pt` allenato su Colab con transfer learning da ResNet18.
- Chiudere le lacune aperte dal cap.08: #47 `.item()`, #48 autograd/`requires_grad`, #49 canali, #50 formula `H_out`, #51 + Pattern #28 catena delle shape, #52 debug matmul, #53 metriche per classe.
- Far interiorizzare il vincolo privacy come **passo tecnico**, non come formalità: la Sez. 0 va eseguita prima di tutto.
- Verificare Pattern #6 (lettura consegne): il capitolo contiene 7 consegne con numero/formato esplicito in MAIUSCOLO. Se anche stavolta ne salta 3+, il pattern resta 🔴.

---

## Prerequisiti da verificare PRIMA di iniziare

- [ ] Bridge `M03_R08_after_C08_before_C09_cnn_to_transfer.md` completato e corretto
- [x] `.gitignore` con `data/buste_*/` (verificato 01/09/2026)
- [ ] Cartelle `data/buste_originali/`, `data/buste_anonimizzate/`, `data/altro/`
- [ ] Dataset "altro" (~200 immagini) raccolto e vario (non solo scansioni pulite)
- [ ] Colab con GPU verificata

---

## Domande durante lo studio

- _(data)_ **Q:** …
  **Nota / risposta sintetica:** …

---

## Valutazioni esercizi / quiz / mini-esercizi

> **Regole di registrazione (promemoria mentor):**
> - Voto = "primo tentativo" (esame); le correzioni successive si annotano come "Fix applicato" senza ricalcolo, salvo richiesta esplicita di nuovo tentativo.
> - Riferimento puntuale al blocco/righe del file.
> - Collegare ogni lacuna emersa al suo ID in `CONTESTO_CORSO.md`.

### [2026-09-01] — Creazione capitolo (nessuna valutazione)

- **Blocco:** file `09_transfer_learning.py` scritto integralmente (1955 righe) su richiesta dello studente subito dopo la chiusura del cap.08.
- **Contenuto:** Sez. 0 privacy → Sez. 6 metriche; Q1–Q8, V1–V8, TODO 1–8, 🏗️ C1–C8, soluzioni.
- **Nota mentor:** in fondo al file c'è il blocco **TRACCIA RINFORZI** con la mappa lacuna → posizione. Usarlo in chiusura per verificare che ogni rinforzo sia stato effettivamente esercitato e non solo scritto.

---

## Lacune e dubbi ancora aperti

Ereditate dal cap.08 (da chiudere qui):

- 🔴 **#48** — chi calcola i gradienti: autograd, non il criterio/optimizer → Sez. 2.4, mini 2.3/2.4
- 🔴 **#49** — il `1` di `(1,28,28)` è il canale → Sez. 3.3, mini 3.1/3.2, Q3
- 🔴 **#51** + **Pattern #28** — catena dei dimezzamenti → Sez. 2.3, mini 2.1/2.2, TODO 7
- 🔴 **#52** — debug numerico dell'errore matmul → TODO 3, V2
- 🟡 **#47** — `.item()` vs `backward` → Q1 (verifica a freddo)
- 🟡 **#50** — il `+1` nella formula `H_out` → Q2 (con stride 2), V7
- 🟡 **#53** — metriche per classe / macro-F1 → Sez. 6, mini 6.1–6.3
- 🔴 **Pattern #6** — lettura incompleta delle consegne → 7 consegne con vincolo numerico esplicito

---

## Note per il capitolo successivo (mentor)

- Il deliverable di questo capitolo (`busta_vs_altro.pt` + soglia scelta + metriche sul test) è l'input diretto del cap.10 (Gradio + deploy HuggingFace, portfolio piece #2).
- Se il modello risultasse debole (recall busta paga < 0.85), valutare se il problema è il dataset "altro" troppo omogeneo prima di cambiare architettura.
