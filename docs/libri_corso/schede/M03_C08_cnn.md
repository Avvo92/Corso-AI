# Scheda — M03 C08 · CNN e Computer Vision

| Campo | Valore |
|-------|--------|
| Capitolo corso | `modulo_03_dl_cv/08_cnn_computer_vision.py` |
| Sezioni corso target | Sez. 1–5 (tensori immagine, conv, pool, CNN, feature maps) |
| Libri usati | `[PYTORCH]` 1ª ed.; `[GERON]` 3ª ed. |
| Data scheda | 2026-08-13 |
| Stato | **usata in capitolo** |

> PDF PyTorch = **1ª edizione** (Stevens et al. 2020). Cap. 7–8 = immagini + convoluzioni (non “cap. 10–11” della 2ª ed.).

---

## Fonti lette

| Codice | Capitolo / sezione | Cosa serve al corso |
|--------|--------------------|---------------------|
| PYTORCH | **Cap. 7** *Telling birds from airplanes* | Dataset CV (`torchvision`), tensore immagine **C×H×W**, normalizzazione, limite delle reti **fully connected** su immagini |
| PYTORCH | **Cap. 8** *Using convolutions to generalize* §8.1–8.2 | Perché la conv: località + pesi condivisi; `nn.Conv2d`; profondità (canali); **pooling** per “guardare più lontano” riducendo H×W |
| GERON | **Cap. 14** *Deep Computer Vision Using CNNs* (intro + Convolutional Layers) | Intuizione filtri/feature maps; max-pooling; perché CNN ≫ dense su pixel |

---

## Concetti da portare nel corso

1. Convenzione PyTorch: batch **`(N, C, H, W)`** (non H×W×C come in Matplotlib/PIL).
2. Conv = filtro locale che scorre: meno parametri di un dense su tutti i pixel; sensibile a pattern locali (bordi, texture).
3. `nn.Conv2d(in_ch, out_ch, kernel_size)` → `out_ch` = numero di filtri = canali della feature map.
4. Max-pool riduce H/W (tipico 2×2 stride 2) tenendo il picco locale.
5. Training loop identico al cap.07; cambia solo il `nn.Module` (Conv→ReLU→Pool→…→Linear).
6. Dataset corso: **Fashion-MNIST** (28×28 grayscale) — low-stakes; niente buste paga (privacy → cap.09).

---

## Analogie / ponti mentali

- Conv = filtro Photoshop / selettore CSS che cerca un pattern **in una zona**, non su tutta la pagina.
- Feature map = “mappa di attivazione”: dove il filtro ha “visto” qualcosa di simile al pattern.
- Pool = thumbnail che tiene il contrasto più forte (max) → meno pixel, stessa idea grossolana.
- Dense su immagine flatten = leggere un PDF pixel per pixel in ordine di lettura senza layout — funziona male e costa parametri.

---

## Esercizi del libro da ADATTARE

| Idea libro | Adattamento corso |
|------------|-------------------|
| PYTORCH Cap.7 CIFAR birds/airplanes | Fashion-MNIST 10 classi abbigliamento (più leggero, 1 canale) |
| PYTORCH Cap.8 prima CNN con Conv+Pool | CNN piccola 2×(Conv+ReLU+Pool) + Linear; train poche epoche su Colab |
| GERON feature maps | Mini: visualizzare uscite del primo `Conv2d` su 1 immagine test |
| PYTorch fully-connected su flatten | Commento + domanda Feynman: perché la CNN ha senso |

---

## Tranelli da inserire

- Plot Matplotlib vuole H×W o H×W×C: fare `.permute(1,2,0)` o `squeeze` sul canale grayscale.
- Dimenticare `zero_grad` ogni batch (residuo cap.07).
- `CrossEntropyLoss` vuole **logits** `(N, num_classes)` e target **long** `(N,)` — non one-hot float.
- Shape dopo pool: calcolare a mano prima di mettere il `Linear`.
- `map_location="cpu"` se salvi da Colab GPU.

## Cosa saltare

- Data augmentation pesante / ResNet (→ cap.09).
- BatchNorm dettagliati, depthwise separable, YOLO/R-CNN (Géron avanzato).
- CIFAR a colori come dataset principale (opzionale menzione).

---

## Blocchi da iniettare

- `# 📚 LETTURA PARALLELA` dopo Sez. 2 e Sez. 4
- `# 📚 [LIBRO]` (max 1): confrontare a parole FC-flatten vs Conv (ispirato Cap.7→8 PYTORCH)

---

## Note mentor

- Mappa moduli diceva “PYTORCH cap. 10–11”: **scartato** per 1ª ed. → usare **cap. 7–8**.
- Prodotto Validator/buste: **fuori scope** di questo capitolo (confermato chiusura 13/08).
