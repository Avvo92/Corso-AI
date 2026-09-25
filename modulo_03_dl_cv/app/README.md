---
title: Classificatore Ants vs Bees
sdk: gradio
sdk_version: 6.27.0
app_file: app.py
---

Classificatore visivo — formiche vs api

1. A cosa serve (e a cosa no)
Distingue foto di **formiche** da foto di **api**.  
Non riconosce altri insetti, non identifica la specie, non è uno strumento medico o produttivo.

2. Su cosa è stato addestrato
Dataset **hymenoptera** (tutorial PyTorch transfer learning), circa  
**245 train / 108 val / 45 test**. Immagini pubbliche, zero dati personali.

3. Come è stato addestrato
**ResNet18** pre-addestrata su ImageNet, fine-tuning in due fasi:  
prima solo la testa (`fc`), poi anche `layer4` con learning rate più basso.

4. Quanto va
La classe positiva è **`bees`**: su questo set piccolo l’accuracy da sola non basta a giudicare il modello in produzione.
Sul **test set (45 immagini)** l’**accuracy** è circa **0.889**, il recall su classe positiva (bees) **0.875**, precision **0.913**.

5. Soglia
Soglia **0.5** su `p(bees)`:  
sopra → `bees`, sotto → `ants`. Scelta sul validation; se la sposti privilegi recall o precision.

6. Limiti
Dataset piccolo; fuori dominio (es. un gatto) il modello **risponde comunque** con una delle due classi e può sembrare molto sicuro.  
Le immagini caricate in demo non vengono conservate. Demo didattica, non garanzia su foto molto diverse dal training.