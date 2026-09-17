"""
Pipeline di ADDESTRAMENTO (simmetrica a modello.py = inferenza).

    dati/train|val|test/<classe>/*.jpg
            │
            ▼
    trasformazioni  →  DataLoader  →  ResNet (freeze → fine-tune layer4)
            │
            ▼
    checkpoint RICCO (.pt)  →  riusabile da ClassificatoreVisivo / Gradio

Uso tipico (Colab GPU consigliata; in locale su CPU è lentissimo)::

    from addestramento import addestra_classificatore_visivo

    esito = addestra_classificatore_visivo(
        cartella_base="dati/proxy_ants_bees",
        percorso_salvataggio="dati/pesi/ants_vs_bees.pt",
        nome_arch="resnet18",
        pipeline="grayscale_doc",   # deve combaciare con l'inferenza!
        epoche_fase1=4,
        epoche_fase2=4,
    )

Niente training all'import: tutto è dietro a funzioni o a ``python addestramento.py``.
"""

from __future__ import annotations

from pathlib import Path

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader

    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}"
    )

try:
    from torchvision import datasets, transforms

    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}"
        )

# Riuso dello scheletro modello (stesso file dell'inferenza).
try:
    from modello import (
        MEAN_IMAGENET,
        STD_IMAGENET,
        VERSIONE_CONTRATTO,
        costruisci_modello,
        transform_eval,
    )
except ImportError as err:
    raise ImportError(
        "Serve modello.py nella stessa cartella di addestramento.py"
    ) from err


DIM_IMMAGINE = 224
# Convenzione corso: ultima classe in ordine ImageFolder = positiva (bees / busta).
INDICE_CLASSE_POSITIVA = -1


# ---------------------------------------------------------------------------
# 1. Trasformazioni (train = augment; eval = deterministica)
# ---------------------------------------------------------------------------

def costruisci_trasformazioni(
    dim=DIM_IMMAGINE,
    pipeline="grayscale_doc",
    mean=None,
    std=None,
    flip_orizzontale=False,
):
    """Ritorna (transform_train, transform_eval).

    ``pipeline`` deve essere la STESSA che userai in inferenza
    (``pipeline_eval`` nel checkpoint). Opzioni allineate a ``modello.transform_eval``:
      - grayscale_doc  → documenti / proxy Colab C09
      - imagenet       → Resize lato corto + CenterCrop
    """
    if not VISION_OK:
        raise RuntimeError("Serve torchvision")

    mean = list(mean) if mean is not None else list(MEAN_IMAGENET)
    std = list(std) if std is not None else list(STD_IMAGENET)

    t_eval = transform_eval(dimensione=dim, mean=mean, std=std, pipeline=pipeline)

    if pipeline == "grayscale_doc":
        pezzi_train = [
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((dim + 32, dim + 32)),
            transforms.RandomRotation(degrees=4, fill=255),
            transforms.RandomResizedCrop(dim, scale=(0.85, 1.0), ratio=(0.9, 1.1)),
            transforms.ColorJitter(brightness=0.25, contrast=0.25),
        ]
        if flip_orizzontale:
            pezzi_train.append(transforms.RandomHorizontalFlip())
        pezzi_train.extend([
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
        t_train = transforms.Compose(pezzi_train)
    elif pipeline == "imagenet":
        lato = int(round(dim * 256 / 224))
        pezzi_train = [
            transforms.Resize(lato),
            transforms.RandomResizedCrop(dim),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
        ]
        if flip_orizzontale:
            pezzi_train.append(transforms.RandomHorizontalFlip())
        pezzi_train.extend([
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
        t_train = transforms.Compose(pezzi_train)
    else:
        raise ValueError(f"pipeline sconosciuta: {pipeline!r}")

    return t_train, t_eval


# ---------------------------------------------------------------------------
# 2. Dati
# ---------------------------------------------------------------------------

def prepara_dataloader(
    cartella_base,
    batch=16,
    num_workers=2,
    dim=DIM_IMMAGINE,
    pipeline="grayscale_doc",
    flip_orizzontale=False,
):
    """Crea train/val/test DataLoader da ``cartella/{train,val,test}/<classe>/``.

    Ritorna ``(dl_train, dl_val, dl_test, classi)``.
    ``classi`` è la lista ordinata ImageFolder (indice 0, 1, ...).
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision")

    t_train, t_eval = costruisci_trasformazioni(
        dim=dim,
        pipeline=pipeline,
        flip_orizzontale=flip_orizzontale,
    )
    base = Path(cartella_base)
    for split in ("train", "val", "test"):
        if not (base / split).is_dir():
            raise FileNotFoundError(
                f"Manca {base / split}. Atteso layout ImageFolder "
                f"con sottocartelle per classe."
            )

    ds_train = datasets.ImageFolder(str(base / "train"), transform=t_train)
    ds_val = datasets.ImageFolder(str(base / "val"), transform=t_eval)
    ds_test = datasets.ImageFolder(str(base / "test"), transform=t_eval)

    print("class_to_idx:", ds_train.class_to_idx)
    print(f"train={len(ds_train)}  val={len(ds_val)}  test={len(ds_test)}")

    dl_train = DataLoader(
        ds_train, batch_size=batch, shuffle=True, num_workers=num_workers
    )
    dl_val = DataLoader(
        ds_val, batch_size=batch, shuffle=False, num_workers=num_workers
    )
    dl_test = DataLoader(
        ds_test, batch_size=batch, shuffle=False, num_workers=num_workers
    )
    return dl_train, dl_val, dl_test, list(ds_train.classes)


# ---------------------------------------------------------------------------
# 3. Modello per il training (pesi ImageNet + freeze)
# ---------------------------------------------------------------------------

def prepara_modello_training(
    nome_arch="resnet18",
    num_classi=2,
    congela_backbone=True,
):
    """ResNet (o altra arch) con pesi ImageNet e testa nuova.

    Ordine equivalente al cap.09: costruisci con DEFAULT, poi congela tutto
    tranne ``fc`` (la testa sostituita resta allenabile).
    """
    modello = costruisci_modello(
        nome_arch=nome_arch,
        num_classi=num_classi,
        pesi_pretrained="DEFAULT",
    )
    if congela_backbone:
        for nome, parametro in modello.named_parameters():
            parametro.requires_grad = nome.startswith("fc.")
    return modello


def conta_parametri(modello):
    """Ritorna (totali, allenabili)."""
    totali = sum(p.numel() for p in modello.parameters())
    allenabili = sum(p.numel() for p in modello.parameters() if p.requires_grad)
    return totali, allenabili


def scongela_layer4(modello):
    """Fase 2: riapre i gradienti sull'ultimo blocco convoluzionale (ResNet)."""
    if not hasattr(modello, "layer4"):
        raise AttributeError(
            f"{type(modello).__name__} non ha layer4: "
            "scongela_layer4 vale per le ResNet."
        )
    for parametro in modello.layer4.parameters():
        parametro.requires_grad = True
    return modello


def ottimizzatore_due_velocita(modello, lr_testa=1e-3, lr_backbone=1e-4):
    """Adam a due velocità: testa più aggressiva, layer4 più cauto."""
    return torch.optim.Adam([
        {"params": modello.layer4.parameters(), "lr": lr_backbone},
        {"params": modello.fc.parameters(), "lr": lr_testa},
    ])


# ---------------------------------------------------------------------------
# 4. Un'epoca / valutazione
# ---------------------------------------------------------------------------

def allena_una_epoca(modello, dataloader, criterio, optimizer, device):
    """Un passaggio sul training set. Ritorna (loss_media, accuracy)."""
    modello.train()
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

        somma_loss += loss.item() * xb.size(0)
        corretti += (logits.argmax(1) == yb).sum().item()
        visti += xb.size(0)

    return somma_loss / visti, corretti / visti


def valuta(modello, dataloader, criterio, device, indice_positiva=None):
    """Valutazione senza gradienti.

    Ritorna ``(loss, accuracy, y_veri, y_pred, prob_positiva)``.
    ``prob_positiva`` = softmax sulla classe positiva (default: ultima).
    """
    modello.eval()
    somma_loss = 0.0
    visti = 0
    tutti_veri, tutti_pred, tutte_prob = [], [], []

    with torch.no_grad():
        for xb, yb in dataloader:
            xb, yb = xb.to(device), yb.to(device)
            logits = modello(xb)
            loss = criterio(logits, yb)

            somma_loss += loss.item() * xb.size(0)
            visti += xb.size(0)

            n_classi = logits.size(1)
            idx = (
                n_classi + INDICE_CLASSE_POSITIVA
                if indice_positiva is None
                else int(indice_positiva)
            )
            probabilita = torch.softmax(logits, dim=1)[:, idx]
            tutti_veri.append(yb.cpu())
            tutti_pred.append(logits.argmax(1).cpu())
            tutte_prob.append(probabilita.cpu())

    y_veri = torch.cat(tutti_veri).numpy()
    y_pred = torch.cat(tutti_pred).numpy()
    prob_pos = torch.cat(tutte_prob).numpy()
    accuratezza = float((y_veri == y_pred).mean())
    return somma_loss / visti, accuratezza, y_veri, y_pred, prob_pos


def tabella_soglie(y_veri, prob_positiva, soglie=(0.3, 0.4, 0.5, 0.6, 0.7)):
    """Stampa precision / recall / accuracy per soglie sulla classe positiva."""
    import numpy as np

    y_veri = np.asarray(y_veri)
    prob_positiva = np.asarray(prob_positiva)
    print(f"{'soglia':>8}  {'prec':>7}  {'rec':>7}  {'acc':>7}")
    risultati = []
    for s in soglie:
        y_hat = (prob_positiva >= s).astype(int)
        tp = int(((y_hat == 1) & (y_veri == 1)).sum())
        fp = int(((y_hat == 1) & (y_veri == 0)).sum())
        fn = int(((y_hat == 0) & (y_veri == 1)).sum())
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        acc = float((y_hat == y_veri).mean())
        print(f"{s:8.2f}  {prec:7.3f}  {rec:7.3f}  {acc:7.3f}")
        risultati.append(
            {"soglia": float(s), "precision": prec, "recall": rec, "accuracy": acc}
        )
    return risultati


# ---------------------------------------------------------------------------
# 5. Checkpoint ricco (compatibile con modello.carica_checkpoint)
# ---------------------------------------------------------------------------

def salva_checkpoint(
    modello,
    percorso,
    *,
    nome_arch,
    classi,
    dimensione_input=224,
    mean=None,
    std=None,
    soglia=0.5,
    pipeline_eval="grayscale_doc",
    metriche=None,
    note="",
):
    """Salva pesi + contratto di inferenza in un unico .pt."""
    if not TORCH_OK:
        raise RuntimeError("Serve torch")

    pacchetto = {
        "versione_contratto": VERSIONE_CONTRATTO,
        "model_state": modello.state_dict(),
        "nome_arch": nome_arch,
        "classi": list(classi),
        "dimensione_input": int(dimensione_input),
        "mean": list(mean) if mean is not None else list(MEAN_IMAGENET),
        "std": list(std) if std is not None else list(STD_IMAGENET),
        "soglia": float(soglia),
        "pipeline_eval": pipeline_eval,
        "metriche": dict(metriche) if metriche else {},
        "note": note,
        "torch_version": str(torch.__version__),
    }
    percorso = Path(percorso)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    torch.save(pacchetto, percorso)
    return percorso


# ---------------------------------------------------------------------------
# 6. Pipeline completa (due fasi)
# ---------------------------------------------------------------------------

def addestra_classificatore_visivo(
    cartella_base,
    percorso_salvataggio,
    *,
    nome_arch="resnet18",
    pipeline="grayscale_doc",
    epoche_fase1=4,
    epoche_fase2=4,
    batch=16,
    num_workers=2,
    dim=DIM_IMMAGINE,
    lr_testa=1e-3,
    lr_backbone=1e-4,
    flip_orizzontale=False,
    soglia=0.5,
    device=None,
    valuta_test=True,
    note="",
):
    """Addestra in due fasi e salva un checkpoint ricco.

    Fase 1: solo testa (``fc``).
    Fase 2: testa + ``layer4`` (due learning rate).
    Tiene il best sulla validation accuracy.

    Ritorna un dict con modello, classi, path, metriche val/test.
    """
    if not (TORCH_OK and VISION_OK):
        raise RuntimeError("Servono torch e torchvision (usa Colab GPU).")

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device)

    dl_train, dl_val, dl_test, classi = prepara_dataloader(
        cartella_base,
        batch=batch,
        num_workers=num_workers,
        dim=dim,
        pipeline=pipeline,
        flip_orizzontale=flip_orizzontale,
    )

    modello = prepara_modello_training(
        nome_arch=nome_arch,
        num_classi=len(classi),
        congela_backbone=True,
    ).to(device)
    criterio = nn.CrossEntropyLoss()

    totali, allenabili = conta_parametri(modello)
    print(f"parametri: {totali:,} totali / {allenabili:,} allenabili")

    migliore_val = -1.0
    storia = []

    def _salva_se_migliore(acc_va, fase):
        nonlocal migliore_val
        if acc_va > migliore_val:
            migliore_val = acc_va
            salva_checkpoint(
                modello,
                percorso_salvataggio,
                nome_arch=nome_arch,
                classi=classi,
                dimensione_input=dim,
                soglia=soglia,
                pipeline_eval=pipeline,
                metriche={"acc_val": float(acc_va), "fase": fase},
                note=note or f"best val fase {fase}",
            )
            print(f"  → salvato best val={acc_va:.3f} in {percorso_salvataggio}")

    # --- FASE 1 -----------------------------------------------------------
    optimizer = torch.optim.Adam(
        [p for p in modello.parameters() if p.requires_grad], lr=lr_testa
    )
    for epoca in range(epoche_fase1):
        loss_tr, acc_tr = allena_una_epoca(
            modello, dl_train, criterio, optimizer, device
        )
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(
            f"[F1 {epoca + 1}/{epoche_fase1}] "
            f"train {loss_tr:.4f}/{acc_tr:.3f} | val {loss_va:.4f}/{acc_va:.3f}"
        )
        storia.append({"fase": 1, "epoca": epoca + 1, "acc_val": acc_va})
        _salva_se_migliore(acc_va, fase=1)

    # --- FASE 2 -----------------------------------------------------------
    modello = scongela_layer4(modello)
    optimizer = ottimizzatore_due_velocita(
        modello, lr_testa=lr_testa, lr_backbone=lr_backbone
    )
    _, allenabili = conta_parametri(modello)
    print(f"dopo unfreeze: {allenabili:,} parametri allenabili")

    for epoca in range(epoche_fase2):
        loss_tr, acc_tr = allena_una_epoca(
            modello, dl_train, criterio, optimizer, device
        )
        loss_va, acc_va, *_ = valuta(modello, dl_val, criterio, device)
        print(
            f"[F2 {epoca + 1}/{epoche_fase2}] "
            f"train {loss_tr:.4f}/{acc_tr:.3f} | val {loss_va:.4f}/{acc_va:.3f}"
        )
        storia.append({"fase": 2, "epoca": epoca + 1, "acc_val": acc_va})
        _salva_se_migliore(acc_va, fase=2)

    print(f"migliore accuracy validation: {migliore_val:.3f}")

    # Ricarica i pesi migliori (potrebbero non essere l'ultima epoca).
    from modello import carica_checkpoint

    modello_best, contratto = carica_checkpoint(percorso_salvataggio, device=device)

    esito = {
        "percorso": str(percorso_salvataggio),
        "classi": classi,
        "acc_val_best": migliore_val,
        "contratto": {k: v for k, v in contratto.items() if k != "model_state"},
        "storia": storia,
        "modello": modello_best,
        "dl_test": dl_test,
    }

    if valuta_test:
        loss_te, acc_te, y_veri, y_pred, prob_pos = valuta(
            modello_best, dl_test, criterio, device
        )
        print(f"TEST loss={loss_te:.4f}  acc={acc_te:.3f}")
        print("--- tabella soglie (classe positiva = ultima) ---")
        esito["acc_test"] = acc_te
        esito["tabella_soglie"] = tabella_soglie(y_veri, prob_pos)
        esito["y_veri"] = y_veri
        esito["prob_positiva"] = prob_pos

    return esito


# ---------------------------------------------------------------------------
# Esempio eseguibile (non parte all'import)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent
    cartella = ROOT / "dati" / "proxy_ants_bees"
    out = ROOT / "dati" / "pesi" / "ants_vs_bees.pt"

    print(
        "Avvio training proxy ants/bees.\n"
        "Su CPU locale sarà LENTO: preferisci Colab GPU.\n"
        f"dati: {cartella}\n"
        f"out:  {out}\n"
    )
    addestra_classificatore_visivo(
        cartella_base=cartella,
        percorso_salvataggio=out,
        nome_arch="resnet18",
        pipeline="grayscale_doc",
        epoche_fase1=4,
        epoche_fase2=4,
        flip_orizzontale=True,  # ok su formiche/api; NO su documenti testo
        note="track prova ants/bees — checkpoint ricco C10",
    )
