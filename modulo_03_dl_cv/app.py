
"""Demo Gradio — classificatore visivo (track prova ants/bees)."""

from pathlib import Path

import gradio as gr

# In questo capitolo le funzioni stanno nel file del corso; nello Space
# copiale in un modulo `modello.py` accanto a app.py e importalo così:
from modello import ClassificatoreVisivo

QUI = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()         # ⚠️ mai percorsi assoluti: lo Space
                                     #    non ha le tue cartelle
PERCORSO_PESI = QUI / "dati" / "pesi" / "ants_vs_bees.pt"
CARTELLA_ESEMPI = QUI / "esempi"

TITOLO = "Classificatore visivo — formiche vs api"
DESCRIZIONE = (
    "Demo didattica di transfer learning (ResNet18 fine-tuned). "
    "Carica una foto: il modello restituisce la probabilità per classe."
)
DISCLAIMER = (
    "⚠️ Demo didattica, non uno strumento di produzione. "
    "Il modello è addestrato su un dataset piccolo (circa 250 immagini) "
    "e può sbagliare su foto molto diverse da quelle di addestramento. "
    "Le immagini caricate non vengono conservate."
)


# --- BLOCCO 2: MODELLO ---------------------------------------------------

# UNA istanza a livello di modulo: il caricamento pigro dentro la classe
# fa sì che i pesi si leggano alla prima predizione e restino in memoria.
classificatore = ClassificatoreVisivo(PERCORSO_PESI, device="cpu")


# --- BLOCCO 3: IL CORE (nessuna dipendenza da Gradio) --------------------

def analizza(immagine):
    """immagine: PIL.Image → (dict per gr.Label, stringa di riepilogo)."""
    if immagine is None:
        return {}, "Carica un'immagine per iniziare."

    esito = classificatore.predict_etichetta(immagine)

    riepilogo = (
        f"Decisione: {esito['etichetta']}  "
        f"(p({esito['classe_positiva']}) = {esito['p_positiva']:.3f}, "
        f"soglia = {esito['soglia']:.2f})"
    )
    return esito["probabilita"], riepilogo


# --- BLOCCO 4: INTERFACCIA (l'unico pezzo che conosce Gradio) ------------

esempi = sorted(str(p) for p in CARTELLA_ESEMPI.glob("*.jpg"))

demo = gr.Interface(
    fn=analizza,
    inputs=gr.Image(type="pil", label="Immagine"),
    outputs=[
        gr.Label(num_top_classes=2, label="Probabilità per classe"),
        gr.Textbox(label="Decisione e soglia applicata"),
    ],
    title=TITOLO,
    description=DESCRIZIONE,
    article=DISCLAIMER,          # testo sotto la demo
    examples=esempi or None,
    cache_examples=False,        # True = predizioni calcolate al build
    flagging_mode="never",       # Gradio 6+: ex allow_flagging; niente raccolta immagini
)

if __name__ == "__main__":
    demo.launch()                # su Spaces non serve: ci pensa la piattaforma
