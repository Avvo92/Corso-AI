# M3 — Bridge quiz ripasso — dopo Cap.09 (transfer learning) → prima Cap.10 (Gradio)

**Focus:** ambienti virtuali idea, `requirements`, API REST vs demo locale, dizionari config, immagini da disco, privacy reminder.

---

### 1. Vero / Falso

“Posso committare su Git le buste paga anche anonimizzate senza controllare `.gitignore`.”

---

### 2. Completa — JSON come dict

```python
import json
s = '{"lr": 0.01, "model": "resnet18"}'
cfg = json.___(s)
print(cfg["model"])
```

---

### 3. Open file binario immagine

Apri `img.png` in **lettura binaria** e leggi tutti i byte in `data` (una riga `with open(...) as f:`).

---

### 4. Prevedi

```python
def apply_twice(f, x):
    return f(f(x))

apply_twice(lambda z: z + 1, 2)
```

---

### 5. requirements.txt idea

Perché si **pinna** una versione tipo `torch==2.2.0` prima del deploy (una frase)?

---

### 6. Dict merge (Python 3.9+)

Se hai `a = {"x": 1}` e `b = {"y": 2}`, come ottieni `{"x":1,"y":2}` con merge operator?

---

### 7. Gradio / Streamlit — confronto rapido

Una frase: cosa condividono Streamlit (M2) e Gradio (M7 M3) come **tipo di prodotto** per il developer?

---

### 8. Callable check

```python
def load_model(path): ...
m = load_model("w.pt")
```

Come verifichi che `m` sia invocabile tipo `m(x)` (funzione `callable`) ?

---

### 9. Spiega con parole tue

Perché il **transfer learning** riduce spesso tempo e dati rispetto ad allenare tutti i pesi da zero?

---

### 10. Mini-esercizio — argparse idea

Scrivi firma concettuale: perché uno script accetta `--epochs 10` da terminale (vantaggio in una frase)?

---

## Soluzioni — solo dopo il tentativo

1. **Falso** — policy corso M3: dati sensibili/non ripubblicabili fuori repo; `.gitignore` obbligatorio; anonimizzazione non è garanzia legale da sola.
2. `loads`.
3. `with open("img.png", "rb") as f: data = f.read()`.
4. `4` — `2+1+1`.
5. Riprodurre ambiente / evitare rotture API tra versioni (“dipendenze ripetibili”).
6. `a | b` oppure `{**a, **b}` per versioni precedenti.
7. Entrambi creano **UI web veloce** per prototipo/demo senza scrivere frontend completo.
8. `callable(m)`.
9. Parti da feature già apprese su dataset grande → adatti solo **pochi strati** / testa sul tuo dominio.
10. Cambi hyperparam senza editare codice; utile esperimenti e script riutilizzabili.

---

## Micro 09.A – 09.E — rinforzi dalla chiusura del cap.09

> Aggiunti il 14/09/2026. Mirati a #48, #52, #53, Pattern #6, AdaptiveAvgPool.
> Corti: 1–2 minuti ciascuno, a freddo, prima di aprire `10_progetto_gradio.py`.

### 09.A — tre leve (#48)

Metti V/F:
1. `model.eval()` congela i pesi (`requires_grad=False`).
2. `torch.no_grad()` evita di costruire il grafo di autograd.
3. Con backbone freezato il `forward` sul backbone **non** viene eseguito.

### 09.B — matmul (#52)

Errore: `(32×512) and (256×2)`. In **tre** bullet: cosa è 32, cosa è 512, perché 256 è sbagliato e come lo sistemi in modo portabile (resnet18/50).

### 09.C — obiezione numerica (#53 + Pattern #6)

30 bees vere, 25 TP, 5 FN, accuracy 0.89. Scrivi **UNA** frase di obiezione che cita un numero (FN o recall), non “l’accuracy non basta” generico.

### 09.D — AdaptiveAvgPool

Shape dopo `AdaptiveAvgPool2d((1,1))` su `(8, 512, 10, 10)`? Perché `Linear(512, 2)` non dipende da 10×10?

### 09.E — formato consegna (Pattern #6)

Consegna: “3 bullet + una riga di motivo ciascuno”. Scrivi uno scheletro vuoto corretto (solo struttura, senza contenuto).

---

## Soluzioni micro 09.A–E

**09.A:** 1 Falso · 2 Vero · 3 Falso (freeze ≠ skip forward).

**09.B:** 32 = batch; 512 = feature dopo avgpool ResNet18; 256 = `in_features` inventato → `nn.Linear(modello.fc.in_features, 2)` prima di sostituire.

**09.C:** es. “Accuracy 89% ma 5/30 bees perse (recall ≈ 83%): in produzione non accettabile se l’obiettivo è non perdere la classe positiva.”

**09.D:** `(8, 512, 1, 1)` → flatten `(8, 512)`; H×W collassati dal pool adattivo.

**09.E:**
```
- motivo:
- motivo:
- motivo:
```
