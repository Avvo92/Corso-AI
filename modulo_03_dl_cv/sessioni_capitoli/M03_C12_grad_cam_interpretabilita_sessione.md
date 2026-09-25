# Diario sessione — Capitolo 12 — Grad-CAM / interpretabilità visiva

| Campo | Valore |
|-------|--------|
| **Modulo** | M03 — Deep Learning & Computer Vision |
| **File capitolo** | `12_grad_cam_interpretabilita.py` |
| **File diario** | `M03_C12_grad_cam_interpretabilita_sessione.md` |
| **Stato** | creato 25/09/2026 — da svolgere (dopo C10 o in ripresa; studente ha chiesto il capitolo ora) |
| **Voto difficoltà** | — |
| **Seed** | ex `grad_cam_pipeline.py` (ora wrapper CLI verso il cap.12) |

---

## Obiettivi del capitolo (per il mentor)

- Distinguere probabilità / feature map / Grad-CAM
- Hook forward/backward; pesi×A; ReLU; upsample/overlay
- Regola 43: ripassi cap.08/09/10 prima dei richiami
- Collegamento prodotto: heatmap al posto di `motivi_top3` per il consulente
- Backward di lettura ≠ training (`no_grad` spegne; niente `step`)

---

## Domande durante lo studio

- _(sessione pre-capitolo)_ Hook `register_forward_hook` / `register_full_backward_hook` spiegati in chat.

---

## Valutazioni esercizi / quiz / mini-esercizi

> Nessuna valutazione ancora (capitolo appena creato).

---

## Lacune e dubbi ancora aperti

- Da verificare nello svolgimento: #48 (no_grad vs backward lettura); Regola 43 nei mini.

### Rinforzi mirati inseriti alla chiusura C10 (25/09/2026)

| Lacuna | Dove nel capitolo | Cosa verifica |
|--------|-------------------|---------------|
| 🔴 **#57** BatchNorm in eval (“si spegne” vs running_*) | Sez. 0 — `🔁 RINFORZO MIRATO` + Micro 57.A / 57.B | train = stats del batch, eval = `running_mean/var`; a spegnersi è Dropout |
| 🔴 **#58** explainability visiva ≠ probabilità | Sez. 0 — `🔁 RINFORZO MIRATO` + Micro 58.A | `motivi_top3` (M2) vs Grad-CAM: input / output / limite |
| 🟡 **#56** contratto di inferenza | Quiz d'ingresso **Q5** (a freddo) | 6 voci + “vivono nel checkpoint, non riscritte a mano” |
| 🟡 **#55** cold start | Quiz d'ingresso **Q6** (a freddo) | 4 cause, senza “il modello si scalda” |

---

## Note per il capitolo successivo (mentor)

- Fine modulo formale resta C10 (Spaces). Questo cap.12 è coda interpretabilità / ripresa.
- Bridge R11 o R10→12: valutare se serve file in `quiz_ripasso_tra_capitoli/` quando C10 è chiuso.
