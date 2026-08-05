# Scheda — M03 C07 · Sezione 6 `state_dict`

| Campo | Valore |
|-------|--------|
| Capitolo corso | `modulo_03_dl_cv/07_pytorch_intro.py` |
| Sezioni corso target | **Sez. 6** (e richiamo Colab→CPU in docstring) |
| Libri usati | `[PYTORCH]` 1ª ed. Stevens/Antiga/Viehmann (2020); `[GERON]` 3ª ed. |
| Data scheda | 2026-08-05 |
| Stato | **usata in capitolo** |

> **Nota edizione**: il PDF in `books/Deep-Learning-with-PyTorch.pdf` è la **1ª edizione** (ISBN 9781617295263), non la 2ª Manning 2026. I numeri di capitolo sotto si riferiscono a questa edizione.

---

## Fonti lette

| Codice | Capitolo / sezione | Cosa serve al corso |
|--------|--------------------|---------------------|
| PYTORCH | **§8.4.2** *Saving and loading our model* | `torch.save(model.state_dict(), …)` + `Net()` + `load_state_dict` — “solo pesi, niente struttura” |
| PYTORCH | **§8.4.3** *Training on the GPU* (fine) | `map_location=device` quando i pesi sono salvati da GPU e carichi altrove — **workflow Colab→Cursor** |
| PYTORCH | **§13.6.6** *Saving our model* | Preferire salvare **parametri** (non `pickle` del modello intero); checkpoint dict con `model_state` (+ opz. `optimizer_state` per riprendere il train) |
| GERON | Cap. 10 *Saving and Restoring a Model* | Contrasto: Keras `model.save` salva **architettura + pesi + optimizer**; in PyTorch tipicamente salvi solo `state_dict` → **devi avere la classe** |

---

## Concetti da portare nel corso

1. `state_dict` = dizionario `{nome_parametro: tensore}` — **solo le manopole**, non la macchina.
2. Ciclo deploy: `torch.save(state_dict)` → nuova istanza della **stessa** classe → `load_state_dict` → `eval()` + `no_grad` per inferenza.
3. `map_location="cpu"` (o `device`) obbligatoria nel tuo setup: pesi da Colab GPU, uso su PC senza CUDA.
4. Errore tipico: ricaricare in un modello con **shape diverse** (es. `h` diverso) → mismatch chiavi/`size mismatch` (già Mini 6.2).
5. (Stretch / colloquio) Checkpoint “pro”: dict con `model_state` + meta; più avanti anche `optimizer_state` per riprendere il training (cap.13 libro — **non** obbligatorio in cap.07).

---

## Analogie / ponti mentali

- Export `.env` / config: senza il codice dell’app i valori non bastano → senza `Rete2Layer` i pesi sono numeri senza casa.
- Colab = cantiere in affitto che si spegne; `.pt` = chiavi della cassaforte da riportare in ufficio (Cursor/CPU).
- Keras (Géron) “salva la casa arredata”; PyTorch “salva solo i mobili” → tu ricostruisci le mura (la classe).

---

## Esercizi del libro da ADATTARE

| Idea libro | Adattamento corso |
|------------|-------------------|
| PYTORCH §8.4.2 birds/airplanes: save → new Net → load → predizioni | Stesso ciclo su `Rete2Layer` / `nn.Linear` (già Mini 6.1) + verifica `allclose` |
| PYTORCH §8.4.3 `map_location` | Esplicito nel codice demo + domanda Feynman: “perché map_location nel tuo hardware?” |
| PYTORCH §13.6.6 dict `model_state` | **📚 [LIBRO]**: salva un dict con `model_state` + `note` (stringa), ricarica solo `['model_state']` — prepara M9/checkpoint senza complessità optimizer |
| GERON checkpoint `save_best_only` | Solo menzione in commento: “in futuro salverai il best su validation” — non implementare Keras |

---

## Tranelli da inserire

- Salvare `model` intero con pickle: scomodo e fragile (libro §13.6.6) → preferire `state_dict`.
- Dimenticare `map_location` dopo training GPU → errore o carico su device inesistente in locale.
- Cambiare definizione di `Rete2Layer` tra save e load → “All keys matched” fallisce o shape mismatch.
- Inferenza senza `eval()` / `no_grad()` (già visto in Sez. 5 — richiamare).

## Cosa saltare

- DataParallel / SHA1 / TensorBoard del cap.13 libro.
- SavedModel / HDF5 Keras (Géron) come API da usare — solo contrasto concettuale.
- Ripresa training con `optimizer_state` (rimandare a cap. successivi / M9).

---

## Blocchi iniettati nel `.py` (05/08/2026)

- `# 📚 LETTURA PARALLELA` dopo demo 6.2 / prima dei mini.
- `# 📚 [LIBRO]` checkpoint dict minimale dopo Mini 6.2.
- Arricchimento commenti Sez. 6 con contrasto Keras e `map_location`.

---

## Nota inventario PDF

Aggiornare mentalmente la mappa: per M3 usare **PYTORCH 1ª ed.** cap. **3** (tensori), **5–6** (learning / nn), **8.4** (save — anche se nel contesto CNN), **13.6.6** (checkpoint pro). Non cercare “Huang 2ª ed.” nel file attuale.
