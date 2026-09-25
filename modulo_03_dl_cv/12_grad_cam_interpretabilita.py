"""
============================================================================
MODULO 3 (DL & CV) — CAPITOLO 12
Grad-CAM / interpretabilità visiva: "dove ha guardato la rete?"
============================================================================

Nel M2, quando il modello tabellare diceva "pratica sospetta", potevi
mostrare i `motivi_top3`: feature CON NOME (es. "importo anomalo").

Nel M3 la rete guarda un'immagine. Lo SCORE (probabilità ants/bees) è
solo il verdetto numerico. La DOMANDA da colloquio e da prodotto è:

    Perché? Dove ha guardato?

Grad-CAM (Gradient-weighted Class Activation Mapping) risponde con una
HEATMAP: una mappa di calore sovrapposta alla foto. Zone calde = zone
che hanno spinto di più verso la classe che stai spiegando.

----------------------------------------------------------------------------
DOVE SI COLLOCA NEL MODULO
----------------------------------------------------------------------------

    Cap.08  feature map = "evidenziatori" dei filtri
    Cap.09  ResNet, layer4 = ultimo blocco conv (dove attacchiamo Grad-CAM)
    Cap.10  inferenza, contratto, eval / no_grad, Gradio
    Cap.12  <-- QUI: backward di LETTURA + heatmap (non è training)

Seed già usato in chat: `grad_cam_pipeline.py` (ora è il CLI leggero;
    la teoria e gli esercizi vivono QUI).

----------------------------------------------------------------------------
REGOLA 43 (ripasso propositivo)
----------------------------------------------------------------------------
Questo capitolo CITA continuamente cap.08/09/10. Ogni richiamo ha un
blocco `# 🔁 RIPASSO PROPOSITIVO` PRIMA di usarlo. Non saltarli.

----------------------------------------------------------------------------
DEFINITION OF DONE
----------------------------------------------------------------------------
  1) Distingui probabilità / feature map / Grad-CAM              → Sez. 1
  2) Sai cosa fanno forward hook e backward hook                 → Sez. 2
  3) Sai calcolare pesi per canale e CAM (formule in parole)     → Sez. 3
  4) Sai upsample + overlay sulla foto                           → Sez. 4
  5) Esegui la pipeline su un'immagine del track prova           → Sez. 5
  6) Spieghi perché serve backward SENZA optimizer.step          → Quiz/V
  7) 1 bullet prodotto: dove finisce la heatmap per il consulente → TODO

⚠️ HARDWARE: solo inferenza + 1 backward di lettura. CPU ok.
⚠️ PRIVACY: usa ants/bees o immagini sintetiche. Mai buste reali in demo pubblica.

============================================================================
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Import: cosa ci serve e perché (in una riga ciascuno)
# ---------------------------------------------------------------------------
import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

# Funzioni già costruite nel corso (cap.10 / modello.py):
# carica_checkpoint = ricostruisce ResNet + contratto dal .pt ricco
# transform_eval    = STESSO preprocess dell'inferenza (obbligatorio:
#                     se la CAM vede un'immagine "diversa" dal modello,
#                     la heatmap non ha senso)
from modello import carica_checkpoint, transform_eval


# ==========================================================================
# QUIZ D'INGRESSO — ripasso leggero (cap.08–10), non Grad-CAM ancora
# ==========================================================================
#
# Scrivi le risposte sotto ogni domanda. Soluzioni in fondo al file.
#
# --------------------------------------------------------------------------
# Q1 — Probabilità vs spiegazione (formato: 2 righe)
# --------------------------------------------------------------------------
# Il modello dice bees 0.93. Quella è la probabilità.
# In una riga: cosa ti dice. In una riga: cosa NON ti dice.
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q2 — Feature map (cap.08) (formato: V/F + mezza riga)
# --------------------------------------------------------------------------
# "Una feature map del primo Conv è già la probabilità delle classi."
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q3 — Tre leve (cap.10 / #48) (formato: completa)
# --------------------------------------------------------------------------
# In inferenza "normale" usi modello.____() e with torch.________():
# perché non ti serve il grafo. In Grad-CAM invece il grafo ______
# (serve / non serve), perché ti servono i __________.
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q4 — layer4 (cap.09) (formato: 1 riga)
# --------------------------------------------------------------------------
# Perché Grad-CAM su ResNet si attacca di solito a layer4 e non a conv1?
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q5 — a freddo, dal cap.10 (lacuna #56) (formato: elenco)
# --------------------------------------------------------------------------
# Elenca le 6 voci del contratto di inferenza. Poi una riga: dove vivono,
# e perché in `app.py` non riscrivi i nomi delle classi a mano.
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# Q6 — a freddo, dal cap.10 (lacuna #55) (formato: 4 punti)
# --------------------------------------------------------------------------
# Uno Space fermo da ore: la prima richiesta è lenta. Elenca le QUATTRO
# cose che succedono e che la seconda richiesta non rifà.
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 0 — 🔁 RIPASSI PROPOSITIVI (Regola 43) prima di Grad-CAM
# ==========================================================================
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — probabilità (cap.09/10)
# --------------------------------------------------------------------------
# Dopo softmax hai numeri tra 0 e 1 che sommano a 1: "quanto è convinta
# la rete che sia ants / bees". È il VERDETTO.
# Non ti dice QUALI PIXEL hanno contato. Per quello serve altro.
#
# 🧩 Mini 0.1 — Una riga: analogia giudice (verdetto vs dito sulla pagina).
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — feature map (cap.08)
# --------------------------------------------------------------------------
# Un Conv applica tanti filtri. Ogni filtro produce una mappa HxW:
# "dove si è acceso il mio pattern". 512 filtri → 512 evidenziatori.
# Quella è la FEATURE MAP (attivazioni). Ancora NON è Grad-CAM:
# Grad-CAM = pesare quegli evidenziatori rispetto a UNA classe.
#
# 🧩 Mini 0.2 — V/F: "Visualizzare 16 feature map del primo Conv = Grad-CAM."
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — layer4 ResNet (cap.09)
# --------------------------------------------------------------------------
# ResNet spezza la visione in layer1→2→3→4. layer4 è l'ultimo blocco
# convoluzionale: le mappe sono piccole (es. 7×7) ma più "semantiche"
# (parti di oggetto), meno grezze dei bordi di conv1. Grad-CAM classico
# si fa lì.
#
# 🧩 Mini 0.3 — Completa: Grad-CAM legge attivazioni e gradienti su ______.
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RIPASSO PROPOSITIVO — eval / no_grad / backward (cap.10, #48)
# --------------------------------------------------------------------------
# Tre leve diverse:
#   eval()              → Dropout off; BatchNorm usa running_mean/var
#   torch.no_grad()     → NON costruisce il grafo (risparmi RAM) — tipico
#                         in predizione "normale"
#   loss.backward()     → nel TRAINING: calcola gradienti sui pesi e poi
#                         optimizer.step() li aggiorna
#
# Grad-CAM fa un caso speciale:
#   - modello resta in eval()  (comportamento inferenza)
#   - Niente no_grad()         (ci SERVONO i gradienti)
#   - backward sullo SCORE di una classe
#   - NIENTE optimizer.step()  (i pesi NON si aggiornano: solo LETTURA)
#
# 🧩 Mini 0.4 — Due righe: perché no_grad spegne Grad-CAM; perché step
#               non va chiamato.
# TUA RISPOSTA:
#
#
#
# --------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Lacuna #57: BatchNorm in eval() (dal cap.10 V6)
# --------------------------------------------------------------------------
# Nel cap.10 hai scritto due volte che in `eval()` la rete "smette di usare
# BatchNorm". Non è così, ed è un errore che in colloquio si sente.
#
# BatchNorm normalizza le attivazioni: (x - media) / sqrt(varianza).
# La domanda non è SE lo fa, ma CON QUALI NUMERI:
#
#     modello.train()  →  usa media/varianza DEL BATCH CORRENTE
#                         (e intanto aggiorna running_mean / running_var)
#     modello.eval()   →  usa running_mean / running_var accumulate
#                         durante il training
#
# BatchNorm resta SEMPRE attiva. Cambia solo la fonte delle statistiche.
# Chi si spegne davvero in eval è **Dropout** (in inferenza non butti via
# neuroni a caso: vuoi una risposta deterministica).
#
# Perché conta qui: se lanci Grad-CAM su un modello lasciato in `train()`
# con batch da 1 immagine, la normalizzazione usa le statistiche di
# quell'unica foto → attivazioni diverse → heatmap diversa da quella che
# vedrebbe la tua demo. La CAM deve nascere nello stesso stato
# dell'inferenza: `modello.eval()`.
#
# 🧩 Micro 57.A — Completa senza guardare sopra:
#   In train BatchNorm usa ____________; in eval usa ____________.
#   Il layer che invece si disattiva del tutto in eval è ____________.
# TUA RISPOSTA:
#
#
# 🧩 Micro 57.B — V/F + una riga:
#   "Dimenticare eval() prima di Grad-CAM non cambia nulla: tanto i pesi
#    sono gli stessi."
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🔁 RINFORZO MIRATO — Lacuna #58: spiegazione visiva ≠ probabilità (cap.10 TODO 5)
# --------------------------------------------------------------------------
# Nel TODO 5 del cap.10 hai detto che lo score del modello visivo diventa
# "la probabilità di genuinità". Attenzione a non fondere due cose:
#
#     lo SCORE         = un numero (quanto è convinta la rete)
#     la SPIEGAZIONE   = dove ha guardato per arrivarci  ← Grad-CAM
#
# Nel M2 il modello tabellare dava `motivi_top3`: feature CON NOME
# ("importo anomalo"), perché ogni colonna aveva un significato umano.
# Un'immagine non ha colonne con nome: i "motivi" diventano una REGIONE
# dell'immagine, non una lista di parole. È questo il salto del capitolo.
#
# E quando affianchi i due mondi (tabellare + visivo) non sommi due
# probabilità a caso: dichiari il peso di ciascuna nel semaforo finale.
#
# 🧩 Micro 58.A — Tre righe, una per colonna: input / output / limite,
#   confrontando `motivi_top3` (M2) e Grad-CAM (M3).
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 1 — L'idea di Grad-CAM (senza codice ancora)
# ==========================================================================
#
# Analogia: il giudice dà un voto (probabilità) e poi indica con il dito
# la zona del documento che l'ha convinto (heatmap).
#
# Passi mentali:
#   1) Forward: salva la feature map A di layer4  → shape (C, H, W)
#   2) Backward dallo score della classe scelta → gradienti G sulla stessa A
#   3) Per ogni canale c: peso w_c = media di G sul piano H×W
#      (= "in media, quanto il filtro c ha spinto verso quella classe?")
#   4) CAM[i,j] = somma_c ( w_c * A[c,i,j] )
#   5) ReLU: tieni solo i contributi a favore
#   6) Normalizza 0..1, ingrandisci a 224×224, colora, fondi sulla foto
#
# 🧩 Mini 1.1 — Ordina i passi 1..6 in tre parole ciascuno (lista numerata).
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 2 — Gli HOOK: spie sul modulo
# ==========================================================================
#
# Problema: durante modello(batch) i tensori intermedi esistono un attimo
# e poi spariscono. Serve "intercettarli".
#
# Soluzione PyTorch: register_forward_hook / register_full_backward_hook.
# Sono callback: PyTorch le chiama in automatico al forward/backward
# di QUEL modulo.
#
# Analogia: microfono sul tubo layer4 — registri il passaggio in avanti
# (attivazioni) e l'eco all'indietro (gradienti).
#

class AttivazioniEGradienti:
    """Registra A (forward) e G (backward) sul modulo target (es. layer4)."""

    def __init__(self, modulo):
        # Contenitori vuoti: si riempiono solo quando passano forward/backward.
        self.attivazioni = None
        self.gradienti = None

        # Spia FORWARD: a fine forward di `modulo`, chiama _on_forward.
        # Restituisce un handle per scollegare dopo (igiene memoria).
        self._h_fwd = modulo.register_forward_hook(self._on_forward)

        # Spia BACKWARD: quando il gradiente attraversa `modulo`, chiama
        # _on_backward. "full" = API moderna con firma completa.
        self._h_bwd = modulo.register_full_backward_hook(self._on_backward)

    def _on_forward(self, _modulo, _ingressi, uscita):
        """PyTorch chiama questa funzione da solo.

        uscita = feature map di layer4, tipicamente (1, C, H, W)
        es. (1, 512, 7, 7) su ResNet18 con input 224.
        """
        self.attivazioni = uscita

    def _on_backward(self, _modulo, _grad_ingresso, grad_uscita):
        """PyTorch chiama questa durante backward.

        grad_uscita è una tupla; [0] è il tensore d(score)/d(uscita),
        stessa shape delle attivazioni.
        """
        self.gradienti = grad_uscita[0]

    def chiudi(self):
        """Toglie le spie dal modello (obbligatorio dopo l'uso)."""
        self._h_fwd.remove()
        self._h_bwd.remove()


def modulo_target_resnet(modello):
    """Restituisce layer4, o errore chiaro se non è una ResNet."""
    if not hasattr(modello, "layer4"):
        raise ValueError(
            "Questo capitolo assume una ResNet (attributo layer4). "
            "Altre architetture richiedono un altro blocco target."
        )
    return modello.layer4


# 🧩 Mini 2.1 — Due bullet: a cosa serve l'handle? Cosa salva _on_forward?
# TUA RISPOSTA:
# -
# -


# ==========================================================================
# SEZIONE 3 — Dal gradiente alla heatmap (cuore matematico in parole)
# ==========================================================================
#
# Schema (una sola immagine, una sola classe da spiegare):
#
#   foto → preprocess → ResNet
#                         │
#                    [layer4] ──hook──► A = attivazioni (C,H,W)
#                         │
#                      logits → prendi score della classe k
#                         │
#                    score.backward() ──hook──► G = gradienti su A
#                         │
#                    w_c = media(G[c]) sul piano H×W
#                    CAM = ReLU( somma_c w_c * A[c] )
#                         │
#                    upsample → overlay sulla foto
#
# Esempio numerico microscopico (3 canali, UNA cella della griglia):
#
#   canale | A (attivazione) | w (peso dal gradiente)
#   0      | 2.0             | 0.5
#   1      | 1.0             | -0.2
#   2      | 3.0             | 1.0
#
#   cam = 0.5*2 + (-0.2)*1 + 1.0*3 = 3.8
#   dopo ReLU resta 3.8 (era già > 0)
#
# Ripeti per ogni (i,j) della griglia 7×7 → ottieni la CAM piccola.
#

def grad_cam(modello, batch, indice_classe):
    """Calcola Grad-CAM per UNA classe su UNA immagine.

    modello : ResNet in eval(), stesso device del batch
    batch   : (1, 3, 224, 224) già preprocessato come in inferenza
    indice_classe : int (0=ants, 1=bees, … secondo il contratto)

    Ritorna: numpy (H, W) in [0, 1] — risoluzione della feature map (es. 7×7).
    """
    target = modulo_target_resnet(modello)
    hook = AttivazioniEGradienti(target)

    # Serve il grafo → NIENTE torch.no_grad() qui.
    batch = batch.detach().requires_grad_(True)

    logits = modello(batch)                 # (1, num_classi) — punteggi grezzi
    score = logits[0, indice_classe]        # scalare della classe da spiegare

    modello.zero_grad(set_to_none=True)     # igiene gradienti residui
    score.backward()                        # riempie hook.gradienti — NO step()

    A = hook.attivazioni[0]                 # (C, H, W) — togliamo il batch
    G = hook.gradienti[0]                   # (C, H, W)
    hook.chiudi()

    # Peso per canale = media spaziale del gradiente
    pesi = G.mean(dim=(1, 2))               # (C,)

    # Combinazione: somma_c w_c * A_c
    cam = (pesi[:, None, None] * A).sum(dim=0)  # (H, W)
    cam = F.relu(cam)                       # solo spinte "a favore"

    # Normalizza in [0, 1] per colorarla
    cam = cam - cam.min()
    if float(cam.max()) > 0:
        cam = cam / cam.max()

    return cam.detach().cpu().numpy()


# 🧩 Mini 3.1 — Con i numeri della tabella sopra, calcola cam PRIMA di ReLU.
# TUA RISPOSTA:
#
#
# 🧩 Mini 3.2 — V/F + perché: "pesi = G.mean(dim=0) è corretto."
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 4 — Dalla CAM piccola alla foto (upsample + overlay)
# ==========================================================================
#
# La CAM è 7×7; la foto del modello è 224×224. Serve:
#   1) denormalizzare il tensore → RGB visibile (stesso crop del modello)
#   2) interpolate bilineare 7×7 → 224×224
#   3) colormap semplice (rosso = alto)
#   4) blend: (1-alpha)*foto + alpha*heatmap
#

def denormalizza_per_plot(batch, mean, std):
    """Inverte Normalize: tensore modello → immagine RGB uint8."""
    x = batch[0].detach().cpu().clone()
    for c in range(3):
        x[c] = x[c] * std[c] + mean[c]
    x = x.clamp(0, 1).permute(1, 2, 0).numpy()
    return (x * 255).astype(np.uint8)


def overlay_cam(immagine_rgb_uint8, cam_piccola, alpha=0.45):
    """Sovrappone CAM (h,w) in [0,1] all'immagine (H,W,3) uint8."""
    h, w, _ = immagine_rgb_uint8.shape
    cam_t = torch.from_numpy(cam_piccola).float()[None, None]  # (1,1,h,w)
    cam_up = F.interpolate(
        cam_t, size=(h, w), mode="bilinear", align_corners=False
    )[0, 0].numpy()

    heat = np.zeros((h, w, 3), dtype=np.float32)
    heat[..., 0] = cam_up
    heat[..., 1] = cam_up * 0.3
    heat = (heat * 255).astype(np.uint8)

    base = immagine_rgb_uint8.astype(np.float32)
    out = (1 - alpha) * base + alpha * heat.astype(np.float32)
    return out.clip(0, 255).astype(np.uint8)


# 🧩 Mini 4.1 — Perché denormalizziamo PRIMA di salvare la foto di fondo?
# TUA RISPOSTA:
#
#


# ==========================================================================
# SEZIONE 5 — Pipeline end-to-end (eseguibile)
# ==========================================================================

def pipeline_grad_cam(
    percorso_checkpoint,
    percorso_immagine,
    nome_classe=None,
    percorso_out="cam_overlay.png",
    device="cpu",
):
    """Dal .pt + foto → PNG con overlay. Stesso contratto dell'inferenza."""
    modello, contratto = carica_checkpoint(percorso_checkpoint, device=device)
    classi = list(contratto["classi"])
    mean = list(contratto["mean"])
    std = list(contratto["std"])
    pipeline = contratto.get("pipeline_eval", "imagenet")

    img = Image.open(percorso_immagine).convert("RGB")
    tfm = transform_eval(
        dimensione=contratto["dimensione_input"],
        mean=mean,
        std=std,
        pipeline=pipeline,
    )
    batch = tfm(img).unsqueeze(0).to(device)

    # Predizione "normale" (qui SÌ no_grad): solo per stampare proba / argmax
    with torch.no_grad():
        logits = modello(batch)
        proba = torch.softmax(logits, dim=1)[0]

    if nome_classe is None:
        indice = int(proba.argmax().item())
        nome_classe = classi[indice]
    else:
        if nome_classe not in classi:
            raise ValueError(f"Classe {nome_classe!r} non in {classi}")
        indice = classi.index(nome_classe)

    print("Probabilità:", {c: round(float(p), 4) for c, p in zip(classi, proba)})
    print(f"Grad-CAM sulla classe: {nome_classe} (indice {indice})")

    cam = grad_cam(modello, batch, indice)
    rgb = denormalizza_per_plot(batch, mean, std)
    overlay = overlay_cam(rgb, cam)

    out = Path(percorso_out)
    Image.fromarray(overlay).save(out)
    print(f"Salvato: {out.resolve()}")
    return out


def main_cli():
    """Entry point da terminale (stesso uso del vecchio grad_cam_pipeline.py)."""
    parser = argparse.ArgumentParser(
        description="Grad-CAM — capitolo 12 (ResNet + checkpoint corso)"
    )
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--immagine", required=True)
    parser.add_argument("--classe", default=None)
    parser.add_argument("--out", default="cam_overlay.png")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    pipeline_grad_cam(
        percorso_checkpoint=args.checkpoint,
        percorso_immagine=args.immagine,
        nome_classe=args.classe,
        percorso_out=args.out,
        device=args.device,
    )


# 🧩 Mini 5.1 — Perché transform_eval deve usare mean/std del CONTRATTO?
# TUA RISPOSTA:
#
#


# ==========================================================================
# QUIZ DI VERIFICA
# ==========================================================================
#
# V1 — Completa (una riga di codice mentale)
#   pesi = G.mean(dim=(____, ____))
# TUA RISPOSTA:
#
#
# V2 — V/F + motivazione
#   "In Grad-CAM chiami optimizer.step() dopo backward."
# TUA RISPOSTA:
#
#
# V3 — Trova l'errore
#   with torch.no_grad():
#       cam = grad_cam(modello, batch, 1)
# TUA RISPOSTA:
#
#
# V4 — 💬 Feynman (4-6 righe)
#   Spiega a un collega web cosa è Grad-CAM, senza dire "si scalda".
# TUA RISPOSTA:
#
#
# V5 — Prodotto (2 bullet)
#   Dove metteresti la heatmap nel Validator per il consulente mutui?
#   Cosa NON deve promettere (limite onesto)?
# TUA RISPOSTA:
# -
# -


# ==========================================================================
# ESERCIZI
# ==========================================================================
#
# TODO 1 — 🎯 [COLLOQUIO] (3 bullet)
#   "Come spieghi una predizione di una CNN a un non tecnico?"
# TUA RISPOSTA:
# 1)
# 2)
# 3)
#
# TODO 2 — 🔧 [REFACTORING]
#   Uno junior ha messo print e percorso assoluto dentro grad_cam().
#   Elenca 3 problemi e come li risolveresti (senza riscrivere tutto).
# TUA RISPOSTA:
# -
# -
# -
#
# TODO 3 — 🔍 [DEBUG]
#   FileNotFound sul checkpoint in pipeline_grad_cam. 2 cause tipiche
#   (una è path, una è LFS 133 byte del cap.10). Diagnosi in 2 bullet.
# TUA RISPOSTA:
# -
# -
#
# TODO 4 — 🧠 [RETRIEVAL]
#   Senza guardare sopra, riscrivi in pseudo-codice i 6 passi di Grad-CAM.
# TUA RISPOSTA:
#
#
# TODO 5 — 🔀 [INTERLEAVING]
#   # 🔁 RIPASSO PROPOSITIVO — motivi_top3 (M2)
#   Nel M2 i motivi erano coefficienti di feature nominate.
#   Qui: confronta in 3 righe motivi_top3 vs Grad-CAM (input, output, limite).
# TUA RISPOSTA:
#
#
# TODO 6 — Esegui
#   Lancia su una foto del track prova (quando hai il .pt):
#     python 12_grad_cam_interpretabilita.py --checkpoint ... --immagine ...
#   Oppure: python grad_cam_pipeline.py ... (wrapper verso questo capitolo)
#   Incolla qui path del PNG e 1 riga: la heatmap "ha senso" a occhio? sì/no/perché
# TUA RISPOSTA:
#
#
# --------------------------------------------------------------------------
# 🏗️ PROGETTO INCREMENTALE — G-CAM
# --------------------------------------------------------------------------
# G1) Genera overlay per 2 immagini (una ants-like, una bees-like se puoi).
# G2) (Opz.) Tab Gradio: Image in → Label + Image overlay out.
# G3) 5 righe model card: "Come leggere la heatmap" + limiti.
# TUA RISPOSTA / checklist:
# [ ] G1
# [ ] G2
# [ ] G3
#


# ==========================================================================
# SOLUZIONI (solo dopo il tentativo)
# ==========================================================================
#
# --- Quiz ingresso -------------------------------------------------------
# Q1  Dice quanto è convinta la rete sulla classe.
#     NON dice quali zone dell'immagine hanno contato.
# Q2  Falso: feature map ≠ probabilità classi (cap.08).
# Q3  eval ; no_grad ; serve ; gradienti
# Q4  layer4 è più semantico / ultimo blocco conv (mappe piccole ma ricche).
# Q5  architettura · classi ORDINATE · dimensione input · mean/std · soglia
#     · versione. Vivono nel checkpoint `.pt` insieme al `state_dict`.
#     I nomi non si riscrivono a mano perché se l'ordine non combacia con
#     `class_to_idx` scambi le etichette e il bug NON crasha.
# Q6  (1) risveglio del container in sleep; (2) avvio processo + import di
#     torch; (3) lettura dei ~45 MB di pesi e costruzione del modello;
#     (4) primo forward (allocazione buffer, cache fredda).
#     Non è che "il modello si scalda": paghi il SETUP una volta sola.
#
# --- Rinforzi mirati ------------------------------------------------------
# 57.A  train → media/varianza del batch corrente; eval → running_mean /
#       running_var. Il layer che si disattiva in eval è Dropout.
# 57.B  Falso: i pesi sono gli stessi, ma in train BatchNorm normalizza con
#       le statistiche del batch (su 1 immagine!) → attivazioni e heatmap
#       diverse da quelle dell'inferenza.
# 58.A  motivi_top3 (M2): input = feature tabellari con nome → output = lista
#       di motivi leggibili → limite: solo ciò che hai messo in colonna.
#       Grad-CAM (M3): input = immagine → output = regione "dove ha guardato"
#       → limite: dice dove, non perché; non è una prova.
#
# --- Mini ----------------------------------------------------------------
# 0.1  Verdetto = score; dito sulla pagina = heatmap.
# 0.2  Falso.
# 0.3  layer4 (o "ultimo blocco conv").
# 0.4  no_grad spegne i gradienti → niente CAM; step aggiornerebbe i pesi
#      (qui vogliamo solo leggere).
# 1.1  forward A → backward G → pesi → somma → ReLU → upsample/overlay
# 2.1  handle = scollegare hook; _on_forward salva feature map
# 3.1  3.8
# 3.2  Falso: serve dim=(1,2) su (C,H,W), non dim=0
# 4.1  Il tensore è normalizzato (mean/std): senza inversione la foto è
#      illeggibile / non in 0..255 RGB.
# 5.1  Altrimenti input diverso dal training → CAM e proba senza senso.
#
# --- Quiz verifica -------------------------------------------------------
# V1  (1, 2)
# V2  Falso: niente step; solo lettura.
# V3  no_grad impedisce i gradienti: grad_cam non può funzionare.
# V4  Rubrica: verdetto vs dove; feature map pesata dai gradienti; non training.
# V5  Accanto allo score / tab "spiega"; non promettere "prova legale" —
#      è uno strumento di lettura, fallibile.
#
# --- TODO (tracce) -------------------------------------------------------
# TODO 1  score chiaro + heatmap + limiti/onestà
# TODO 2  effetti, print, mescolare I/O e calcolo → separare, Path, logging
# TODO 3  path sbagliato; puntatore LFS 133 B
# TODO 5  M2: nomi feature; M3: dove sullo spazio immagine; entrambi fallibili
#


if __name__ == "__main__":
    # Se lanci questo file CON argomenti CLI → pipeline.
    # Se lo apri solo per studiare, non serve eseguire nulla all'import.
    import sys
    if len(sys.argv) > 1:
        main_cli()
    else:
        print(
            "Capitolo 12 Grad-CAM caricato.\n"
            "Per generare un overlay:\n"
            "  python 12_grad_cam_interpretabilita.py "
            "--checkpoint percorso.pt --immagine foto.jpg\n"
            "Oppure usa il wrapper: python grad_cam_pipeline.py ..."
        )
