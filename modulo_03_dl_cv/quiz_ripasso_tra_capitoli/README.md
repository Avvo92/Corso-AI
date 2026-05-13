# Quiz ripasso fondamentali — tra capitoli (Modulo 3)

Questi file implementano la **Regola 40** di `CONTESTO_CORSO.md`: blocchi brevi (~10 mini-esercizi facili) da fare **dopo** aver chiuso un capitolo e **prima** di aprire il successivo, così Python, NumPy, Pandas e recall ML restano “muscolo vivo” mentre affronti Deep Learning.

## Naming

Pattern consigliato:

`M03_R##_after_C##_before_C##_breve_descrizione.md`

- **R##**: numero progressivo del bridge nel modulo (01…06 per M3).
- **C##**: numero capitolo di partenza / arrivo.

## Elenco bridge Modulo 3

| Dopo capitolo | Prima capitolo | File |
|---------------|----------------|------|
| 01 neurone | 02 reti | `M03_R01_after_C01_before_C02_neurone_to_reti.md` |
| 02 reti | 03 backprop | `M03_R02_after_C02_before_C03_reti_to_backprop.md` |
| 03 backprop | 04 PyTorch | `M03_R03_after_C03_before_C04_backprop_to_pytorch.md` |
| 04 PyTorch | 05 CNN | `M03_R04_after_C04_before_C05_pytorch_to_cnn.md` |
| 05 CNN | 06 transfer | `M03_R05_after_C05_before_C06_cnn_to_transfer.md` |
| 06 transfer | 07 Gradio | `M03_R06_after_C06_before_C07_transfer_to_gradio.md` |

Non esiste bridge **dopo** il cap.07: chiudi il modulo con la sezione confronto prima/dopo del capitolo finale.

## Come usarli

1. Completi il capitolo `XX` (quiz verifica + esercizi richiesti).
2. Apri il file bridge `..._after_CXX_before_CY...`.
3. Rispondi **senza** guardare le soluzioni.
4. Solo dopo confronti con la sezione in fondo al file.
5. Su dubbi: chiedi correzione al mentor (come per gli altri quiz).

Template vuoto per nuovi moduli: `_TEMPLATE_bridge_quiz.md`.
