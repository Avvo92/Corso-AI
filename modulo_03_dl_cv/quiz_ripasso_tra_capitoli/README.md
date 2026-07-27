# Quiz ripasso fondamentali — tra capitoli (Modulo 3)

Questi file implementano la **Regola 40** di `CONTESTO_CORSO.md`: blocchi brevi (~10 mini-esercizi facili) da fare **dopo** aver chiuso un capitolo e **prima** di aprire il successivo, così Python, NumPy, Pandas e recall ML restano “muscolo vivo” mentre affronti Deep Learning.

## Naming

Pattern consigliato:

`M03_R##_after_C##_before_C##_breve_descrizione.md`

- **R##**: numero progressivo del bridge nel modulo (01…09 per M3 dopo split 27/05/2026).
- **C##**: numero capitolo di partenza / arrivo.

## Elenco bridge Modulo 3 (aggiornato dopo split 27/05/2026)

| Dopo capitolo | Prima capitolo | File |
|---------------|----------------|------|
| 01 neurone | 02 reti | `M03_R01_after_C01_before_C02_neurone_to_reti.md` |
| 02 reti | 03 loss | `M03_R02_after_C02_before_C03_reti_to_loss.md` |
| 03 loss | 04 derivate_gradiente | `M03_R03_after_C03_before_C04_loss_to_derivate.md` ✅ popolato 29/05/2026 |
| 04 derivate_gradiente | 05 chain_rule_gd | `M03_R04_after_C04_before_C05_derivate_to_chain.md` ✅ popolato 16/06/2026 |
| 05 chain_rule_gd | 06 backprop_training | `M03_R05_after_C05_before_C06_chain_to_backprop.md` ✅ popolato 27/07/2026 (11 esercizi) |
| 06 backprop_training | 07 PyTorch | `M03_R06_after_C06_before_C07_backprop_to_pytorch.md` |
| 07 PyTorch | 08 CNN | `M03_R07_after_C07_before_C08_pytorch_to_cnn.md` |
| 08 CNN | 09 transfer | `M03_R08_after_C08_before_C09_cnn_to_transfer.md` |
| 09 transfer | 10 Gradio | `M03_R09_after_C09_before_C10_transfer_to_gradio.md` |

Non esiste bridge **dopo** il cap.10: chiudi il modulo con la sezione confronto prima/dopo del capitolo finale.

> **Nota split**: i bridge R03/R04/R05 sono stati popolati alla chiusura dei rispettivi capitoli (29/05, 16/06, 27/07/2026). I bridge R06–R09 restano da popolare alla chiusura dei capitoli 06–09. Gli altri sono stati rinominati dalla numerazione pre-split (R02 da `_reti_to_backprop` → `_reti_to_loss`; R03..R06 → R06..R09).

## Come usarli

1. Completi il capitolo `XX` (quiz verifica + esercizi richiesti).
2. Apri il file bridge `..._after_CXX_before_CY...`.
3. Rispondi **senza** guardare le soluzioni.
4. Solo dopo confronti con la sezione in fondo al file.
5. Su dubbi: chiedi correzione al mentor (come per gli altri quiz).

Template vuoto per nuovi moduli: `_TEMPLATE_bridge_quiz.md`.
