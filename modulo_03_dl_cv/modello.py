
from __future__ import annotations

from pathlib import Path

try:
    import torch
    import torch.nn as nn
    TORCH_OK = True
except Exception as errore_torch:
    TORCH_OK = False
    print(
        "[AVVISO] torch non utilizzabile in questo ambiente:\n"
        f"         {type(errore_torch).__name__}: {errore_torch}\n"
        "         Puoi leggere tutto il capitolo; per eseguire le funzioni\n"
        "         installa: pip install torch torchvision\n"
    )

try:
    from torchvision import models, transforms
    VISION_OK = True
except Exception as errore_vision:
    VISION_OK = False
    if TORCH_OK:
        print(
            "[AVVISO] torchvision non disponibile:\n"
            f"         {type(errore_vision).__name__}: {errore_vision}\n"
        )

try:
    from PIL import Image
    PIL_OK = True
except Exception:
    PIL_OK = False
    
MEAN_IMAGENET = [0.485, 0.456, 0.406]
STD_IMAGENET = [0.229, 0.224, 0.225]

VERSIONE_CONTRATTO = "1.0"

ROOT = Path(__file__).parent if "__file__" in globals() else Path.cwd()


def transform_eval(dimensione=224, mean=None, std=None, pipeline="imagenet"):
    """Pipeline di preprocessing per l'INFERENZA (deterministica).

    Nessuna casualità: stessa immagine → sempre stesso tensore.
    mean/std arrivano dal contratto. `pipeline` sceglie la ricetta usata
    in training (deve coincidere, altrimenti le probabilità sono rumore):

      - "imagenet"         Resize lato corto + CenterCrop (cap.10 / ImageNet)
      - "grayscale_doc"    Grayscale→3ch + Resize quadrato (dim+32) + CenterCrop
                           (= pipeline di `colab_track_prova_ants_bees.py`)
    """
    if not VISION_OK:
        raise RuntimeError("Serve torchvision: pip install torchvision")

    mean = list(mean) if mean is not None else list(MEAN_IMAGENET)
    std = list(std) if std is not None else list(STD_IMAGENET)

    if pipeline == "grayscale_doc":
        # Stessa catena del Colab track prova (pensata per documenti, usata
        # anche sul proxy ants/bees). Senza Grayscale le api sembrano formiche.
        return transforms.Compose([
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((dimensione + 32, dimensione + 32)),
            transforms.CenterCrop(dimensione),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ])

    if pipeline != "imagenet":
        raise ValueError(
            f"pipeline_eval sconosciuta: {pipeline!r}. "
            "Usa 'imagenet' oppure 'grayscale_doc'."
        )

    lato_resize = int(round(dimensione * 256 / 224))
    return transforms.Compose([
        transforms.Resize(lato_resize),      # lato corto, proporzioni salve
        transforms.CenterCrop(dimensione),   # quadrato centrale, deterministico
        transforms.ToTensor(),               # PIL → tensore (C,H,W) in [0,1]
        transforms.Normalize(mean=mean, std=std),
    ])

def costruisci_modello(nome_arch="resnet18", num_classi=2, pesi_pretrained=None):
    """Costruisce un modello torchvision con la testa adattata a num_classi.

    nome_arch: "resnet18", "resnet34", "resnet50", ...
    pesi_pretrained:
        None        → scheletro con pesi casuali (caso INFERENZA: i pesi
                      arrivano poi dal checkpoint)
        "DEFAULT"   → pesi pre-addestrati su ImageNet (caso TRAINING,
                      cioè quello che hai fatto nel cap.09)
    """
    if not VISION_OK:
        raise RuntimeError("Serve torchvision: pip install torchvision")

    costruttore = getattr(models, nome_arch, None)
    if costruttore is None:
        raise ValueError(
            f"Architettura '{nome_arch}' non trovata in torchvision.models. "
            "Esempi validi: resnet18, resnet34, resnet50."
        )

    modello = costruttore(weights=pesi_pretrained)

    # 🔁 #52: si LEGGE il numero dal modello, non si scrive a mano.
    # Su resnet18 vale 512, su resnet50 vale 2048: il codice non cambia.
    n_ingressi = modello.fc.in_features
    modello.fc = nn.Linear(n_ingressi, num_classi)
    return modello


def carica_checkpoint(percorso, device="cpu"):
    """Ricostruisce il modello dal checkpoint ricco e lo mette in eval().

    Ritorna (modello, contratto). Il modello è già pronto per predire:
    sul device richiesto e in modalità valutazione.
    """
    if not TORCH_OK:
        raise RuntimeError("Serve torch: pip install torch")
    
    pacchetto = torch.load(percorso, map_location=device, weights_only=True)

    if not isinstance(pacchetto, dict) or "model_state" not in pacchetto:
        raise ValueError(
            f"{percorso} non è un checkpoint ricco: sembra un semplice "
            "state_dict. Ricostruisci il contratto a mano (arch, classi, "
            "size, mean/std, soglia) e risalvalo con salva_checkpoint()."
        )

    modello = costruisci_modello(
        nome_arch=pacchetto["nome_arch"],
        num_classi=len(pacchetto["classi"]),
        pesi_pretrained=None,          # i pesi arrivano dal checkpoint
    )
    modello.load_state_dict(pacchetto["model_state"])
    modello.to(device)
    modello.eval()                     # 🔁 #48: BatchNorm in modalità inferenza
    return modello, pacchetto


class ClassificatoreVisivo:
    """Modello + contratto insieme, pronto per essere riusato.

    Uso:
        clf = ClassificatoreVisivo("dati/pesi/ants_vs_bees.pt")
        clf.predict_proba(immagine_pil)     # {"ants": 0.07, "bees": 0.93}
        clf.predict_etichetta(immagine_pil) # + etichetta e soglia applicata
    """

    def __init__(self, percorso_checkpoint, device="cpu"):
        self.percorso = Path(percorso_checkpoint)
        self.device = device
        self._modello = None
        self._contratto = None
        self._trasformazione = None

    # -- caricamento -------------------------------------------------------

    def carica(self):
        """Carica pesi e contratto la PRIMA volta; poi non fa nulla."""
        if self._modello is None:
            if not self.percorso.exists():
                raise FileNotFoundError(
                    f"Checkpoint non trovato: {self.percorso}\n"
                    "Su HuggingFace Spaces ricordati che la working dir è "
                    "la radice dello Space: usa percorsi relativi al file app.py."
                )
            self._modello, self._contratto = carica_checkpoint(
                self.percorso, device=self.device
            )
            self._trasformazione = transform_eval(
                dimensione=self._contratto["dimensione_input"],
                mean=self._contratto["mean"],
                std=self._contratto["std"],
                # Se manca nel .pt, default ImageNet; il tuo ants/bees Colab
                # salva "grayscale_doc" (vedi migrazione checkpoint).
                pipeline=self._contratto.get("pipeline_eval", "imagenet"),
            )
        return self

    # -- lettura del contratto --------------------------------------------

    @property
    def classi(self):
        """Nomi delle classi nell'ordine degli indici (dal checkpoint)."""
        return list(self.carica()._contratto["classi"])

    @property
    def soglia(self):
        return float(self.carica()._contratto["soglia"])

    @property
    def classe_positiva(self):
        """Convenzione del corso: l'ultima classe è la positiva.

        Con ImageFolder alfabetico: altro=0 / busta_paga=1, ants=0 / bees=1.
        La convenzione è dichiarata qui, in un solo posto.
        """
        return self.classi[-1]

    def scheda(self):
        """Contratto senza i pesi: utile da mostrare in UI o in un /info."""
        contratto = dict(self.carica()._contratto)
        contratto.pop("model_state", None)
        return contratto

    # -- predizione --------------------------------------------------------

    def predict_proba(self, immagine_pil):
        """Probabilità per classe. Ritorna {nome_classe: probabilità}."""
        self.carica()

        # convert("RGB") non è decorativo: vedi Sez. 5.1. Gestisce PNG con
        # canale alfa (4 canali) e scansioni in scala di grigi (1 canale),
        # che altrimenti fanno esplodere il primo Conv2d che vuole 3 canali.
        immagine_rgb = immagine_pil.convert("RGB")

        tensore = self._trasformazione(immagine_rgb)      # (3, H, W)
        batch = tensore.unsqueeze(0).to(self.device)      # (1, 3, H, W)

        with torch.no_grad():                             # 🔁 #48
            logits = self._modello(batch)                 # (1, num_classi)
            probabilita = torch.softmax(logits, dim=1)[0]  # (num_classi,)

        return {
            nome: float(valore)
            for nome, valore in zip(self.classi, probabilita)
        }

    def predict_etichetta(self, immagine_pil, soglia=None):
        """Applica la soglia del contratto e restituisce la decisione."""
        probabilita = self.predict_proba(immagine_pil)
        soglia_usata = self.soglia if soglia is None else float(soglia)

        nome_positiva = self.classe_positiva
        p_positiva = probabilita[nome_positiva]
        etichetta = nome_positiva if p_positiva >= soglia_usata else self.classi[0]

        return {
            "etichetta": etichetta,
            "probabilita": probabilita,
            "classe_positiva": nome_positiva,
            "p_positiva": p_positiva,
            "soglia": soglia_usata,
        }