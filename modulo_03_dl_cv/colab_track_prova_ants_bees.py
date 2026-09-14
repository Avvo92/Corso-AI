

# ==========================================================================
# 🏗️ PROGETTO INCREMENTALE — ramo visivo (TRACK PROVA attivo)
# ==========================================================================
#
# ⚠️ DECISIONE 14/09/2026: per CHIUDERE il capitolo senza dataset buste
#    reali, usiamo il **TRACK PROVA** (Ants vs Bees). Il TRACK PRODOTTO
#    (buste anonimizzate → `busta_vs_altro.pt`) resta un debito esplicito
#    per dopo / cap.10 — stessa pipeline, altri file.
#
# --------------------------------------------------------------------------
# TRACK PROVA — Ants vs Bees (obbligatorio ORA)
# --------------------------------------------------------------------------
#
# Dataset ufficiale del tutorial PyTorch transfer learning (~120+120 train,
# val divisa in val+test dallo script). Zero privacy, zero anonimizzazione.
#
# Mapping mentale (NON sono documenti — dichiaralo nel README):
#     ants  ↔  classe 0   (come "altro")
#     bees  ↔  classe 1   (come "busta_paga" — classe positiva per le metriche)
#     ImageFolder: ordine alfabetico → ants=0, bees=1
#
# Setup locale (una volta):
#     python modulo_03_dl_cv/prepara_dataset_proxy_ants_bees.py
#     → crea modulo_03_dl_cv/dati/proxy_ants_bees/{train,val,test}/{ants,bees}
#
# Su Colab:
#     1) zippa `proxy_ants_bees` e caricalo (o riesegui lo script in Colab)
#     2) pipeline_addestramento(
#            cartella_base=".../proxy_ants_bees",
#            percorso_salvataggio="ants_vs_bees.pt",
#        )
#     3) Per le metriche: INDICE_BUSTA nel file vale 1 → qui = bees.
#        Opzionale: RandomHorizontalFlip è OK su formiche/api (a differenza
#        dei documenti). Puoi aggiungerlo in `transform_train` solo sul track prova.
#
# CHECKPOINT TRACK PROVA (spunta man mano):
#
#   [x] P1 — eseguito `prepara_dataset_proxy_ants_bees.py` (o equivalente Colab)
#   [x] P2 — stampato `class_to_idx` → {'ants': 0, 'bees': 1}
#   [x] P3 — conteggio train/val/test (Colab: ~244 / 108 / 45)
#   [x] P4 — training Colab due fasi (F2: train 96.7% / val 90.7%) → `.pt` su Colab
#   [x] P5 — test + tabella soglie (precision/recall/acc); CM/report ancora nice-to-have
#   [ ] P6 — 5 righe README nel diario (proxy ≠ busta)
#
# Deliverable track prova: `ants_vs_bees.pt` + numeri P5/P6 nel diario.
#
# --------------------------------------------------------------------------
# TRACK PRODOTTO — buste vs altro (DEBITO — non bloccante per chiudere C09)
# --------------------------------------------------------------------------
#
# Deliverable prodotto (quando avrai tempo): `busta_vs_altro.pt` su immagini
# anonimizzate. Nel cap.10 la demo Gradio "vera" punta qui; il proxy serve
# solo a non fermare l'apprendimento del transfer learning.
#
#   [ ] C1 — cartelle `data/buste_*` + `.gitignore` verificato
#   [ ] C2 — PDF → immagini, corrotti annotati
#   [ ] C3 — anonimizzazione + controllo a campione
#   [ ] C4 — dataset "altro" vario (non solo scansioni pulite)
#   [ ] C5 — split PER CLIENTE con `dividi_per_gruppo` + conteggi
#   [ ] C6 — training due fasi → `busta_vs_altro.pt`
#   [ ] C7 — test set una sola volta: report + CM + soglie
#   [ ] C8 — README: accuracy, recall busta, soglia, limite modello
#
# ⚠️ Sul track prodotto C7 (test) si guarda UNA volta sola alla fine.

from __future__ import annotations

import numpy as np
from pathlib import Path

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Esegui Sez. 1–5 e il training su Google Colab (GPU).\n"
    )

# torchvision: serve per Fashion-MNIST (su Colab è già tipicamente ok)
try:
    from torchvision import datasets, transforms, models
    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}\n"
            "         Su Colab: !pip install torchvision  (se manca)\n"
        )

try:
    import matplotlib.pyplot as plt
    PLOT_OK = True
except Exception:
    PLOT_OK = False

DIM_IMMAGINE = 224
MEDIA_IMAGENET = [0.485, 0.456, 0.406]
STD_IMAGENET = [0.229, 0.224, 0.225]
INDICE_BUSTA = 1


def costruisci_resnet18(num_classi=2, congela_backbone=True):
    """ResNet18 pre-addestrata su ImageNet, con testa nuova a `num_classi`.

    Ordine importante:
      1) carico i pesi
      2) congelo TUTTO
      3) sostituisco la testa  ← nasce con requires_grad=True, quindi
                                 resta l'unica parte allenabile
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    pesi = models.ResNet18_Weights.DEFAULT
    modello = models.resnet18(weights=pesi)

    if congela_backbone:
        for parametro in modello.parameters():
            parametro.requires_grad = False

    n_feature = modello.fc.in_features
    modello.fc = nn.Linear(n_feature, num_classi)
    return modello


def conta_parametri(modello):
    """Ritorna (totali, allenabili). Utile per vedere l'effetto del freeze."""
    totali = sum(p.numel() for p in modello.parameters())
    allenabili = sum(p.numel() for p in modello.parameters() if p.requires_grad)
    return totali, allenabili

def costruisci_trasformazioni(dim=DIM_IMMAGINE):
    """Ritorna (transform_train, transform_eval) tarate su documenti."""
    if not VISION_OK:
        raise RuntimeError("Serve torchvision (usa Colab).")

    transform_train = transforms.Compose([
        # 3 canali: ResNet vuole RGB anche se il contenuto è grigio (🔁 #49)
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((dim + 32, dim + 32)),
        # fill=255 = bianco: ruotando resta "carta", non bordo nero
        transforms.RandomRotation(degrees=4, fill=255),
        transforms.RandomResizedCrop(dim, scale=(0.85, 1.0), ratio=(0.9, 1.1)),
        transforms.ColorJitter(brightness=0.25, contrast=0.25),
        transforms.ToTensor(),
        transforms.Normalize(MEDIA_IMAGENET, STD_IMAGENET),
        # NIENTE RandomHorizontalFlip: vedi 4.2
    ])

    transform_eval = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((dim + 32, dim + 32)),
        transforms.CenterCrop(dim),
        transforms.ToTensor(),
        transforms.Normalize(MEDIA_IMAGENET, STD_IMAGENET),
    ])
    return transform_train, transform_eval


def prepara_dataloader(cartella_base, batch=16, num_workers=2):
    """Crea i tre DataLoader da una cartella con train/ val/ test/."""
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    transform_train, transform_eval = costruisci_trasformazioni()
    base = Path(cartella_base)

    ds_train = datasets.ImageFolder(str(base / "train"), transform=transform_train)
    ds_val = datasets.ImageFolder(str(base / "val"), transform=transform_eval)
    ds_test = datasets.ImageFolder(str(base / "test"), transform=transform_eval)

    print("classi:", ds_train.class_to_idx)
    print(f"train={len(ds_train)}  val={len(ds_val)}  test={len(ds_test)}")

    dl_train = DataLoader(ds_train, batch_size=batch, shuffle=True,
                          num_workers=num_workers)
    dl_val = DataLoader(ds_val, batch_size=batch, shuffle=False,
                        num_workers=num_workers)
    dl_test = DataLoader(ds_test, batch_size=batch, shuffle=False,
                         num_workers=num_workers)
    return dl_train, dl_val, dl_test, ds_train.classes


def allena_una_epoca(modello, dataloader, criterio, optimizer, device):
    """Un passaggio completo sul training set. Ritorna (loss_media, accuracy)."""
    modello.train()                      # BatchNorm/Dropout in modalità training
    somma_loss = 0.0
    corretti = 0
    visti = 0

    for xb, yb in dataloader:
        xb, yb = xb.to(device), yb.to(device)

        optimizer.zero_grad()
        logits = modello(xb)
        loss = criterio(logits, yb)
        loss.backward()
        optimizer.step()

        # .item() stacca il numero dal grafo: se accumulassi `loss`
        # terresti in memoria il grafo di TUTTI i batch dell'epoca
        somma_loss += loss.item() * xb.size(0)
        corretti += (logits.argmax(1) == yb).sum().item()
        visti += xb.size(0)

    return somma_loss / visti, corretti / visti


def scongela_layer4(modello):
    """Fase 2: riapre i gradienti sull'ultimo blocco convoluzionale."""
    for parametro in modello.layer4.parameters():
        parametro.requires_grad = True
    return modello


def ottimizzatore_due_velocita(modello, lr_testa=1e-3, lr_backbone=1e-4):
    """Parameter group: la testa si muove 10 volte più del layer4."""
    return torch.optim.Adam([
        {"params": modello.layer4.parameters(), "lr": lr_backbone},
        {"params": modello.fc.parameters(), "lr": lr_testa},
    ])


def pipeline_addestramento(cartella_base, epoche_fase1=4, epoche_fase2=4,
                           percorso_salvataggio="bees_vs_ants.pt"):
    """Le due fasi, con salvataggio del modello migliore in validation.

    Da lanciare su Colab con GPU. In locale (CPU) è lentissimo.
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab).")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device)

    dl_train, dl_val, dl_test, classi = prepara_dataloader(cartella_base)
    modello = costruisci_resnet18(num_classi=len(classi), congela_backbone=True)
    modello = modello.to(device)
    criterio = nn.CrossEntropyLoss()

    totali, allenabili = conta_parametri(modello)
    print(f"parametri: {totali:,} totali / {allenabili:,} allenabili")

    # --- FASE 1: solo la testa -------------------------------------------
    optimizer = torch.optim.Adam(
        [p for p in modello.parameters() if p.requires_grad], lr=1e-3
    )
    migliore_val = 0.0

    for epoca in range(epoche_fase1):
        loss_tr, acc_tr = allena_una_epoca(modello, dl_train, criterio, optimizer, device)
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(f"[F1 {epoca+1}/{epoche_fase1}] train {loss_tr:.4f}/{acc_tr:.3f} "
              f"| val {loss_va:.4f}/{acc_va:.3f}")
        if acc_va > migliore_val:
            migliore_val = acc_va
            torch.save({"model_state": modello.state_dict(), "classi": classi,
                        "arch": "resnet18", "img_size": DIM_IMMAGINE,
                        "fase": 1, "acc_val": acc_va}, percorso_salvataggio)

    # --- FASE 2: testa + layer4 ------------------------------------------
    modello = scongela_layer4(modello)
    optimizer = ottimizzatore_due_velocita(modello)
    totali, allenabili = conta_parametri(modello)
    print(f"dopo unfreeze: {allenabili:,} parametri allenabili")

    for epoca in range(epoche_fase2):
        loss_tr, acc_tr = allena_una_epoca(modello, dl_train, criterio, optimizer, device)
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(f"[F2 {epoca+1}/{epoche_fase2}] train {loss_tr:.4f}/{acc_tr:.3f} "
              f"| val {loss_va:.4f}/{acc_va:.3f}")
        if acc_va > migliore_val:
            migliore_val = acc_va
            torch.save({"model_state": modello.state_dict(), "classi": classi,
                        "arch": "resnet18", "img_size": DIM_IMMAGINE,
                        "fase": 2, "acc_val": acc_va}, percorso_salvataggio)

    print(f"migliore accuracy validation: {migliore_val:.3f} → {percorso_salvataggio}")
    return modello, dl_test, classi


ROOT = Path(__file__).resolve().parent
cartella_base = ROOT / "dati" / "proxy_ants_bees"
percorso_pesi = ROOT / "dati" / "pesi"

pipeline_addestramento(cartella_base, percorso_salvataggio=percorso_pesi / "bees_vs_ants.pt")
modello = costruisci_resnet18(num_classi=2, congela_backbone=True)
device = "cuda" if torch.cuda.is_available() else "cpu"
ckpt = torch.load(percorso_pesi / "bees_vs_ants.pt", map_location=device)
modello.load_state_dict(ckpt["model_state"])
dl_train, dl_val, dl_test, classes = prepara_dataloader(cartella_base)


def valuta(modello, dataloader, criterio, device):
    """Valutazione senza gradienti. Ritorna (loss, accuracy, y_veri, y_pred, prob_busta)."""
    modello.eval()                       # BatchNorm usa le statistiche salvate
    somma_loss = 0.0
    visti = 0
    tutti_veri, tutti_pred, tutte_prob = [], [], []

    with torch.no_grad():                # niente grafo: meno memoria, più veloce
        for xb, yb in dataloader:
            xb, yb = xb.to(device), yb.to(device)
            logits = modello(xb)
            loss = criterio(logits, yb)

            somma_loss += loss.item() * xb.size(0)
            visti += xb.size(0)

            probabilita = torch.softmax(logits, dim=1)[:, INDICE_BUSTA]
            tutti_veri.append(yb.cpu())
            tutti_pred.append(logits.argmax(1).cpu())
            tutte_prob.append(probabilita.cpu())

    y_veri = torch.cat(tutti_veri).numpy()
    y_pred = torch.cat(tutti_pred).numpy()
    prob_busta = torch.cat(tutte_prob).numpy()
    accuratezza = float((y_veri == y_pred).mean())
    return somma_loss / visti, accuratezza, y_veri, y_pred, prob_busta

loss, accuratezza, y_veri, y_pred, prob_bees = valuta(modello, dl_test, nn.CrossEntropyLoss(), device)

for s in [0.3, 0.4, 0.5, 0.7]:
    y_pred = (prob_bees >= s).astype(int)
    accuracy = float((y_veri == y_pred).mean())
    tp = ((y_pred == 1) & (y_veri == 1)).sum()
    fp = ((y_pred == 1) & (y_veri == 0)).sum()
    fn = ((y_pred == 0) & (y_veri == 1)).sum()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    print(f"Soglia: {s} -> Precision = {precision}, Accuracy = {accuracy}, Recall = {recall}")