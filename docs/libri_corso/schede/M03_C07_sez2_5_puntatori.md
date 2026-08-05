# Scheda — M03 C07 · Sezioni 2–5 (puntatori lettura)

| Campo | Valore |
|-------|--------|
| Capitolo corso | `modulo_03_dl_cv/07_pytorch_intro.py` |
| Sezioni | 2 Autograd, 3 nn.Module, 4 DataLoader, 5 Training loop |
| Libri | `[PYTORCH]` 1ª ed. |
| Data | 2026-08-05 |
| Stato | **usata** (blocchi 📚 leggeri; scheda piena solo Sez. 6) |

## Fonti (lettura mirata, non riscrittura completa)

| Sez. corso | PYTORCH 1ª ed. | Focus |
|------------|----------------|-------|
| 2 Autograd | Cap. **5** *The mechanics of learning* | Gradienti, perché non derivare a mano |
| 3 nn.Module | Cap. **6** *Using a neural network…* | `nn.Linear`, parametri, sottoclassi |
| 4 DataLoader | Cap. **7** / pipeline cap. **1** overview | Batch, shuffle (idea “carrello”) |
| 5 Training loop | Cap. **5–6** + inizio **8.4** | `zero_grad` → forward → loss → `backward` → `step` |

## Da portare (già coperto dal capitolo; 📚 = conferma)

- Autograd = nastro / scontrino (allineato a cache cap.06).
- `nn.Module` contiene `parameters()`; `Linear` = Dense del Ponte.
- Loop identico al cap.06, API diversa.
- `.item()` sulla loss per non tenere il grafo (già Mini 5.1).

## Esercizi libro

Nessun esercizio aggiuntivo qui: il **📚 [LIBRO]** del capitolo è sulla Sez. 6 (scheda dedicata).
