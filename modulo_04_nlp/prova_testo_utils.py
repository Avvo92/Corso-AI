from testo_utils import carica_mappa, vettore_frase
mappa = carica_mappa()
print(vettore_frase("cedolino netto irpef", mappa).shape)