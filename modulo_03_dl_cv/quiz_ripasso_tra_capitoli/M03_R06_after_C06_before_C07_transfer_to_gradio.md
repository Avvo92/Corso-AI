# M3 — Bridge quiz ripasso — dopo Cap.06 (transfer learning) → prima Cap.07 (Gradio)

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
