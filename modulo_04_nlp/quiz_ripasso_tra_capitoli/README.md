# Quiz ripasso fondamentali — tra capitoli (Modulo 4)

Questi file implementano la **Regola 40** di `CONTESTO_CORSO.md`: blocchi brevi (~10 mini-esercizi facili) da fare **dopo** aver chiuso un capitolo e **prima** di aprire il successivo, così Python, NumPy, Pandas e il recall M2/M3 restano "muscolo vivo" mentre affronti NLP.

## Naming

`M04_R##_after_C##_before_C##_breve_descrizione.md`

- **R##**: numero progressivo del bridge nel modulo (01…06 per M4, 7 capitoli).
- **C##**: capitolo di partenza / arrivo.

## Elenco bridge Modulo 4

| Dopo capitolo | Prima capitolo | File | Stato |
|---------------|----------------|------|-------|
| 01 testo come numeri | 02 embeddings | `M04_R01_after_C01_before_C02_testo_to_embeddings.md` | ⬜ da popolare alla chiusura del cap.01 |
| 02 embeddings | 03 similarità coseno | `M04_R02_after_C02_before_C03_embeddings_to_similarita.md` | ⬜ |
| 03 similarità coseno | 04 transformer | `M04_R03_after_C03_before_C04_similarita_to_transformer.md` | ⬜ |
| 04 transformer | 05 HuggingFace | `M04_R04_after_C04_before_C05_transformer_to_hf.md` | ⬜ |
| 05 HuggingFace | 06 sentiment | `M04_R05_after_C05_before_C06_hf_to_sentiment.md` | ⬜ |
| 06 sentiment | 07 progetto | `M04_R06_after_C06_before_C07_sentiment_to_progetto.md` | ⬜ |

Non esiste bridge **dopo** il cap.07: il modulo si chiude con la sezione 🔄 CONFRONTO PRIMA/DOPO del capitolo finale.

## Contenuto tipico dei bridge M4

Ogni bridge mescola tre ingredienti:

1. **Python/Pandas di base** (2-3 esercizi): stringhe, `Counter`, comprehension, `groupby`.
2. **Recall M2** (2-3 esercizi): `fit`/`transform`, leakage, metriche, soglie.
3. **Recall del capitolo appena chiuso** (4-5 esercizi): i concetti nuovi, in forma facile.

Quando un bridge tocca un concetto di un modulo precedente, **Regola 43**: prima del richiamo va un blocco `# 🔁 RIPASSO PROPOSITIVO` di 3-8 righe.

## Come usarli

1. Completi il capitolo `XX` (quiz verifica + esercizi richiesti).
2. Apri il file bridge `..._after_CXX_before_CY...`.
3. Rispondi **senza** guardare le soluzioni.
4. Solo dopo confronti con la sezione in fondo al file.
5. Su dubbi: chiedi correzione al mentor.

Template vuoto: `_TEMPLATE_bridge_quiz.md`.
