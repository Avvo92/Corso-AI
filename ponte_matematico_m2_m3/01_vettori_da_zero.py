"""
============================================================================
PONTE MATEMATICO (bridge M2 -> M3) - CAPITOLO 01
"Vettori da zero": una pratica = una lista di numeri
============================================================================

----------------------------------------------------------------------------
QUANTO HAI GIA' FATTO (e non lo sapevi) NEL MODULO 2
----------------------------------------------------------------------------
Tu pensi che "i vettori" siano una novita'. Non e' vero. In M2 cap.06 hai gia'
scritto codice come questo:

    x_scaled = scaler.transform(X_una)[0]      # un VETTORE
    coef     = model.coef_[0]                  # un altro VETTORE
    contrib  = x_scaled * coef                 # operazione fra VETTORI
    z        = (x_scaled * coef).sum() + b     # questo e' un DOT PRODUCT

Quindi i vettori non sono un concetto nuovo: sono il NOME UFFICIALE di
quello che gia' usavi. In questo capitolo li chiamiamo per nome e
impariamo a maneggiarli con sicurezza, perche' da M3 in poi reggono tutto:
reti neurali (M3), embeddings (M4), RAG con coseno (M6).

----------------------------------------------------------------------------
COSA PORTI VIA DA QUESTO CAPITOLO (Definition of Done)
----------------------------------------------------------------------------
Alla fine sai rispondere "in 1 riga" a queste 5 domande:

  1) Differenza fra shape (n,), (1, n) e (n, 1)?               -> Sezione 1
  2) Cosa fa "scalare * vettore" e "vettore + vettore"?         -> Sezione 2
  3) Cosa calcola np.dot(a, w) e perche' e' = (a*w).sum()?      -> Sezione 3
  4) Cosa misura np.linalg.norm(v)?                              -> Sezione 4
  5) Cosa misura il coseno fra due vettori e perche' va in M4-M6? -> Sezione 5

Hai anche scritto 4 funzioni riutilizzabili: punteggio_lineare, norma,
coseno, e (opzionale) classifica_per_similarita.

----------------------------------------------------------------------------
MAPPA DEL CAPITOLO (da usare come indice)
----------------------------------------------------------------------------
   *  PRONTUARIO TRANELLI VETTORI       [T1] - [T10]
   *  QUIZ D'INGRESSO                   Q1 - Q5     (cerniera M2 -> Ponte)
   *  RINFORZO Lacuna #12               (NumPy shape/reshape)
   *  SEZIONE 1  Cos'e' un vettore           1.1 - 1.2
   *  SEZIONE 2  Operazioni base             2.1 - 2.2
   *  SEZIONE 3  Dot product                 3.1 - 3.2
   *  SEZIONE 4  Norma euclidea              4.1 - 4.2
   *  SEZIONE 5  Coseno fra vettori          5.1 - 5.2
   *  CHECKPOINT FINALE                  C1 - C5
   *  MINI-PROGETTO GUIDATO (opzionale)  classifica_per_similarita

----------------------------------------------------------------------------
COME USARE QUESTO FILE
----------------------------------------------------------------------------
   1. Leggi in ORDINE (i concetti di sezione N usano sezione N-1).
   2. Per ogni sezione: leggi ANALOGIA -> ESEMPIO NUMERICO -> CODICE,
      poi affronta TODO scrivendo nel blocco "TUO CODICE".
   3. Quando vuoi una valutazione, scrivi in chat:
         "valuta cap.01 ponte sezione 3.1"
      oppure
         "valuta @ponte_matematico_m2_m3/01_vettori_da_zero.py righe A-B"
   4. Le DOMANDE DI RIPASSO si rispondono come commento sotto la domanda.
   5. Se ti blocchi >10 min: "sono bloccato sezione X" -> ti do solo
      l'IDEA, mai la soluzione.

VINCOLI DI STILE (Regola 21 del corso):
   - sequenza analogia -> codice -> grafico -> formula in parole
   - niente LaTeX, niente notazione simbolica compressa
   - ponti web/PHP/JS quando aiutano
   - matplotlib solo per i mini-grafici (frecce 2D), tutto su CPU
"""


# ==========================================================================
# PRONTUARIO TRANELLI VETTORI - leggilo PRIMA di iniziare (10 minuti)
# ==========================================================================
# Sono i 10 errori in cui inciamperai. Non perche' sei sbadato, ma perche'
# tutti ci inciampano la prima volta. Conoscerli prima = 80% di tempo
# risparmiato dopo.
#
# [T1] SHAPE 1D vs 2D: (n,) NON e' (1, n) NON e' (n, 1).
#      np.array([1,2,3]).shape   -> (3,)     # 1D
#      np.array([[1,2,3]]).shape -> (1, 3)   # 2D vettore-riga
#      np.array([[1],[2],[3]]).shape -> (3, 1)   # 2D vettore-colonna
#      Sembrano uguali. NON LO SONO. predict_proba voleva (1, 5), non (5,).
#
# [T2] LISTA o NIENTE: np.array([1, 2, 3]) si', np.array(1, 2, 3) NO.
#      Le parentesi quadre sono OBBLIGATORIE: NumPy si aspetta UNA cosa,
#      che dentro contiene gli elementi.
#
# [T3] SOMMA/SOTTRAZIONE solo a STESSA shape.
#      np.array([1,2,3]) + np.array([1,2])  -> ValueError.
#      Pensa al bug del "named_steps": stesso tipo di errore "non
#      compatibile" che ti ha morso nel cap.06.
#
# [T4] "*" fra vettori NumPy = element-wise, NON dot product.
#      np.array([2, 3]) * np.array([4, 5]) -> array([8, 15])  (2*4, 3*5)
#      Per il dot product vero usi np.dot(a, b) o a @ b
#      (l'operatore "@" da Python 3.5 in poi e' il dot product).
#
# [T5] DOT richiede STESSA lunghezza:
#      np.dot(np.array([1,2,3]), np.array([1,2]))  -> ValueError
#      "shapes (3,) and (2,) not aligned"
#
# [T6] RESHAPE conserva il NUMERO totale di elementi.
#      np.arange(12).reshape(3, 4)  -> ok (3*4 = 12)
#      np.arange(12).reshape(2, 5)  -> ValueError (2*5 = 10 != 12)
#      Il messaggio di errore te lo dice: "cannot reshape array of size
#      12 into shape (2,5)". Leggilo SEMPRE.
#
# [T7] NORMA di un VETTORE NULLO = 0  -> coseno NON e' definito.
#      Se v = np.array([0, 0, 0]) allora coseno(v, w) divide per zero.
#      La tua funzione DEVE alzare ValueError, NON restituire nan o None.
#
# [T8] COSENO sta in [-1, +1], NON in [0, 1].
#      Se ti esce 1.5, hai sbagliato qualcosa (probabilmente non hai
#      diviso per le norme, o le hai sommate invece di moltiplicarle).
#
# [T9] AXIS in NumPy: axis=0 = righe (verso il basso),
#                     axis=1 = colonne (verso destra).
#      Per ora non serve, ma fissalo: in M3 ti serve per layer Dense
#      e batch ("operazioni su tutti i sample = axis=0").
#
# [T10] DTYPE: usa float (es. 1500.0 e non 1500). I modelli ML lavorano in
#       float; mescolare int e float crea conversioni invisibili e bug.
#       Controlla con  v.dtype  -> dovrebbe dirti float64.
#
# Riferimenti rapidi: nel resto del file scrivero' "-> [T3]" quando un
# punto richiama uno di questi tranelli. Se ti perdi, torna qui.


# ==========================================================================
# QUIZ D'INGRESSO - 5 domande secche (cerniera M2 -> Ponte)
# ==========================================================================
# Obiettivo: verificare che le lacune del M2 siano chiuse e introdurre il
# vocabolario nuovo. Rispondi 1-3 righe per domanda, sotto "Risposta:".

# Q1) [Cerniera M2 - Lacuna #16] Hai una pratica con prob_alterato = 0.18.
#     Qual e' lo score_genuinita? Su che scala e'?
# Risposta:
# score_genuinita = (1 - 0.18) * 100 = 82
# La scale prob_alterato e 0-1, mentre per lo score_genuinita e 0-100

# Q2) [Cerniera M2 - Lacuna #17] In split_X_y droppi pratica_id e y_alterato.
#     Cosa succede al modello se per sbaglio NON droppi y_alterato?
#     (in 1 frase: il termine tecnico c'e' gia' nei tuoi appunti)
# Risposta:
# Se non droppo y_alterato, sto di fatto fornendo il target come feature per trovare se stesso. Per fare un esempio divertente: di che colore era il cavallo bianco di Napoleone? Dunque sto causando un leakage molto evidente

# Q3) [Cerniera M2 - Lacuna #18] Nel controllo documentale, perche' il
#     recall sulla classe "alterato" e' piu' importante della precision?
# Risposta:
# il Recall è TP / (TP + FN), dunque ci indica quante pratiche false sul totale delle pratiche false il modello è riuscito a segnalare correttamente. Precision invece è TP / (TP + FP), ossia quante delle segnalazione che ha fornito il modello consistevano effettivamente in pratiche alterato. Nel nostro caso, se il modello segnala un pratica genuina etichettandola come alterata, si avrà bisogno di un controllo manuale di un operatore per controllare una pratica che di fatto non era da controllare perchè genuina (un problema di perdita di efficienza e velocità nel controllo documentale). Ma se il modello non segnala una pratica alterata e la lascia passare tra le maglie del controllo, l'operatore non ha modo di correre ai ripari, e questo ci espone a gravi problemi (come possibili frodi a nostro danno).

# Q4) [Vocabolario nuovo - vettori] Spiega in 2 righe a un collega web
#     developer cosa intendi quando dici: "una pratica e' un vettore a 5
#     dimensioni".
#
#     Esempio di formato attesa (non la risposta):
#       "E' come un array PHP con 5 valori numerici, dove la posizione
#        conta. Ogni posizione e' una feature: [importo, giorni, ...]."
#     -> tu scrivi qualcosa di simile, NON identico.
# Risposta:
# una pratica, nel caso della nostra applicazione, è rappresentata come una lista di 5 numeri, che rappresentano feature numeriche o numerizzare (es. importo, cod_fisc, date, qualita_ocr, delta_netto_lordo), in cui ogni posizione conta poichè è univoca per il tipo di feature. 

# Q5) [Ponte mentale - shape] Nel cap.06 hai usato la riga
#         contrib = x_scaled * coef
#     Perche' in NumPy questa moltiplicazione "*" non e' il dot product
#     ma una moltiplicazione element-wise? E quale shape devono avere
#     x_scaled e coef perche' funzioni?    -> [T1] [T4]
# Risposta:
# Una moltiplicazione element-wise (come coef * x_scaled) in pratica moltiplica ogni elemento di un array per il corrispettivo alla stessa posizione di indice di un altro array. Entrambi gli array devono avere lo stesso numero di elementi e shape (n,), ossia entrambi devono essere vettori di egual lunghezza. Il dot product invece, eseguito sempre su due vettori, restituisce un solo numero dato dal risultato dell'espressione (arr_1*arr_2).sum().


# ==========================================================================
# RINFORZO MIRATO - Lacuna #12 (NumPy shape/reshape)
# Obiettivo: chiuderla qui (era 🟡 dopo M1 cap.07).
# ==========================================================================
# Micro-check (rispondi come commento; 1 riga ciascuna):
#
#   1) Hai una lista di 12 numeri. Scrivi la chiamata NumPy che produce
#      una matrice 3x4 a partire da quei numeri.
#      Risposta:
#      lista.reshape(3, 4)
#
#   2) Quale shape ha la matrice ottenuta?
#      Risposta:
#      (3, 4)
#
#   3) Cosa stamperebbe a.reshape(2, 5) sulla stessa lista? Errore o
#      risultato? Perche'?    -> [T6]
#      Risposta:
#      Produrrebbe un ValueError, poichè non è possibile ottenere 12 moltiplicando 2*5

#
# --------------------------------------------------------------------------
# MINI-ESERCIZIO OBBLIGATORIO (5 minuti) - "shape palestra"  -> [T1] [T6]
# --------------------------------------------------------------------------
# Questo e' IL punto che, se non lo chiudi subito, ti fa inciampare in tutto
# il resto del Ponte (e poi in M3). Quindi lo rendiamo *obbligatorio*.
#
# OBIETTIVO:
#   - fissare la differenza fra (n,), (1, n), (n, 1)
#   - vedere con i tuoi occhi cosa cambia e cosa NON cambia
#
# COSA FARE (tu):
#   1) crea un vettore 1D con 5 numeri: v1 = np.array([...])
#   2) crea "vettore-riga" 2D:        v_riga = v1.reshape(1, 5)
#   3) crea "vettore-colonna" 2D:     v_col  = v1.reshape(5, 1)
#   4) stampa:
#        - v1.shape, v_riga.shape, v_col.shape
#        - v1.ndim,  v_riga.ndim,  v_col.ndim
#   5) (domanda) quanti numeri ci sono in totale in OGNI oggetto?
#      Suggerimento: usa v1.size, v_riga.size, v_col.size
#
# REGOLE:
#   - NON cambiare i numeri, cambia solo la forma (reshape)
#   - se un reshape fallisce, spiega il motivo con "numero elementi" -> [T6]
#
# TUO CODICE (shape palestra):
import numpy as np
vettore = np.array([2, 4, 6, 8, 10])
print(f"Vettore 1D:           {vettore}")
vettore_riga = vettore.reshape(1, 5)
print(f"Vettore 2D (Riga):    {vettore_riga}")
vettore_colonne = vettore.reshape(5, 1)
print(f"Vettore 2D (Colonna):\n{vettore_colonne}")

print(vettore.ndim)
print(vettore_riga.ndim)
print(vettore_colonne.ndim)

print(vettore.shape)
print(vettore_riga.shape)
print(vettore_colonne.shape)

print(vettore.size)
print(vettore_riga.size)
print(vettore_colonne.size)
# La size è identica, poichè il numero di elementi è sempre identico, cambia la loro "organizzazione" in dimensioni, come si evince dalla stampa di .ndim (in entrambi i vettori 2D il numero di dimensioni è per l'appunto 2)


# ==========================================================================
# SEZIONE 1 - Cos'e' un vettore
# ==========================================================================
# ANALOGIA (web / dominio prodotto):
#   Pensa a una "pratica" del controllo documentale. Per il modello, NON
#   e' un PDF. E' una lista ORDINATA di numeri, esempio:
#
#       [importo_dichiarato, n_giorni_lavorati, tasse_pagate, irpef, contributi]
#       =        [1500.0,           220,             3200.0,    900,      400]
#
#   Quella lista ordinata si chiama VETTORE.
#     - "Ordinata" = la posizione conta (la 3a colonna e' SEMPRE tasse).
#     - "Numeri reali" = lavoriamo con float ([T10]).
#     - "Lunghezza" del vettore = quante feature ha (qui 5).
#
# COSI' LO SCRIVERESTI IN PHP / JS:
#   PHP: $pratica = [1500.0, 220, 3200.0, 900, 400];   // array indicizzato
#   JS:  const pratica = [1500.0, 220, 3200.0, 900, 400];
#   Python "puro": pratica = [1500.0, 220, 3200.0, 900, 400]
#
# COSI' LO SCRIVI IN NUMPY (e' diverso, ed e' meglio):
#   import numpy as np
#   pratica = np.array([1500.0, 220, 3200.0, 900, 400])
#
# Perche' NumPy e non lista Python "nuda"?
#   - operazioni vettoriali in 1 colpo (somma, dot, ...) senza for loop
#   - tipo dei dati uniforme (float64), niente sorprese
#   - shape esplicita (regge tutto da M3 in poi)
#
# REGOLA D'ORO SULLE SHAPE (-> [T1], scolpiscila):
#   shape (5,)   = vettore 1D, 5 elementi (non e' ne' riga ne' colonna)
#   shape (1, 5) = MATRICE 1 riga x 5 colonne ("vettore-riga")
#   shape (5, 1) = MATRICE 5 righe x 1 colonna ("vettore-colonna")
#   In M2 cap.06: predict_proba si rompeva con (5,), voleva (1, 5).
#
# ESEMPIO GUIDA (NON e' il TUO codice, e' un modello):
#
#   import numpy as np
#   v = np.array([10.0, 20.0, 30.0])     # vettore di 3 numeri
#   print(f"shape={v.shape}  dtype={v.dtype}  len={len(v)}")
#   # Output:  shape=(3,)  dtype=float64  len=3
#
# ATTENZIONE prima del TODO 1.1:
#   - dimentica le parentesi quadre dentro np.array() -> [T2]
#   - usa float, non int -> [T10]
#   - se la shape che stampi NON e' quella che ti aspetti: STOP, leggi
#     prima di andare avanti.

# ----------------------------------------------------------------------
# 1.1) TODO - crea 3 vettori NumPy:
#   - feature_pratica_A: 5 numeri (a tua scelta) come quelli sopra
#   - feature_pratica_B: 5 numeri DIVERSI da A
#   - pesi: 5 numeri come "coefficienti" del modello (puoi mettere
#           valori positivi e negativi, da -1 a +1, a tua fantasia)
#   Stampa shape e dtype di ognuno.
#
# REGOLE:
#   - usa np.array([...]) (mai liste Python "nude") -> [T2]
#   - preferisci float (1500.0 non 1500) -> [T10]
# SUGGERIMENTI:
#   - print(f"shape={vec.shape}  dtype={vec.dtype}") rende i bug visibili.
# ----------------------------------------------------------------------
# TUO CODICE (sezione 1.1):
print("\nMini-esercizio 1.1\n")
feature_pratica_A = np.array([1000, 2000, 3000, 4000, 5000])
feature_pratica_B = np.array([1500, 2500, 3500, 4500, 5500])
pesi = np.array([1, -1, 0.5, -0.5, 0.25])
lista = []
lista.extend([feature_pratica_A, feature_pratica_B, pesi])
lista = np.array(lista, dtype=float)
for l in lista:
   print(f"{l}")
   print(f"Shape: {l.shape}")
   print(f"Dtype: {l.dtype}\n")


# 1.2) DOMANDA DI RIPASSO:
#   Tu scrivi np.array([1, 2, 3]).shape   -> (3,)
#   Tu scrivi np.array([[1, 2, 3]]).shape -> (1, 3)
#   D1) In entrambi i casi quanti numeri ci sono "dentro"?
#   D2) A quale dei due la pipeline scikit-learn dice "ok, posso fare
#       predict_proba"? Perche'?    -> [T1]
# Risposta:
# D1 => In entrambi i casi ci sono 3 elementi (cambia la loro disposizione in dimensioni)
# D2 => Solo al secondo la pipeline direbbe ok, perchè predict_proba in input accetta solo matrici (s_samples, n_features), in questo caso (1, 3)


# ==========================================================================
# SEZIONE 2 - Operazioni base (somma, sottrazione, scalare * vettore)
# ==========================================================================
# ANALOGIA (numeri reali del dominio):
#   - SOMMA: hai due pratiche con le stesse 5 feature. (A + B) ti da' un
#     vettore "consolidato": campo per campo, somma i due valori. E'
#     come unire i totali di due dichiarazioni.
#   - SOTTRAZIONE: A - B ti dice "di quanto la pratica A si discosta da B
#     campo per campo". Utile per capire "perche' A e' diversa".
#   - SCALARE * VETTORE: 0.5 * pesi e' come "alleggerire" l'importanza
#     di tutti i coefficienti del 50%, mantenendo le proporzioni.
#
# COSI' LE FAI IN PHP / JS:
#   PHP (somma, manuale):
#       $c = [];
#       for ($i = 0; $i < count($a); $i++) { $c[$i] = $a[$i] + $b[$i]; }
#   JS (somma, con map):
#       const c = a.map((x, i) => x + b[i]);
#
# COSI' LE FAI IN NUMPY (1 riga, niente loop):
#   c = a + b
#   d = a - b
#   e = 2 * a
#
# ESEMPIO GUIDA (NUMERI):
#   a = np.array([2.0, 4.0, 6.0])
#   b = np.array([1.0, 1.0, 1.0])
#   a + b   -> array([3.0, 5.0, 7.0])    # campo per campo: 2+1, 4+1, 6+1
#   a - b   -> array([1.0, 3.0, 5.0])    # campo per campo: 2-1, 4-1, 6-1
#   2 * a   -> array([4.0, 8.0, 12.0])   # ogni elemento moltiplicato per 2
#
# REGOLA SHAPE (-> [T3]):
#   - a + b funziona solo se a.shape == b.shape.
#   - a + b dove a ha shape (3,) e b ha shape (4,) -> ValueError. STOP.
#     NON forzare con reshape a caso: il problema e' nei DATI, non nello
#     shape.
#
# ATTENZIONE prima del TODO 2.1:
#   - non confondere "*" con dot product -> [T4]
#     a * b e' element-wise (campo per campo), non e' un numero solo.
#     Sara' importante in Sezione 3.

# ----------------------------------------------------------------------
# 2.1) TODO - sul tuo dominio:
#   - calcola somma e differenza fra feature_pratica_A e feature_pratica_B
#   - calcola 0.5 * pesi
#   - stampa i risultati con label leggibili (es. f"A+B = {...}")
#
# REGOLE:
#   - se ottieni un errore di shape: fermati, leggi il messaggio, ragiona.
#     NON usare reshape "a caso" per zittire l'errore -> [T3]
# SUGGERIMENTI:
#   - una stampa per ciascuna delle 3 operazioni: facilita il debug.
# ----------------------------------------------------------------------
# TUO CODICE (sezione 2.1):
print("\nMini-esercizio 2.1\n")
feature_pratica_A = np.array([1000, 2000, 3000, 4000, 5000])
feature_pratica_B = np.array([1500, 2500, 3500, 4500, 5500])
pesi = np.array([1, -1, 0.5, -0.5, 0.25])
somma = feature_pratica_A + feature_pratica_B
diff = feature_pratica_A - feature_pratica_B
half_pesi = pesi * 0.5
print(f"A+B =      {somma}")
print(f"A-B =      {diff}")
print(f"PESI / 2 = {half_pesi}")

# 2.2) DOMANDA DI RIPASSO:
#   Cosa rappresenta il vettore (A - B) nel tuo dominio "controllo
#   documentale", se A e' una pratica sospetta e B una pratica "tipo"
#   media-genuina? Spiegalo in 2 righe.
# Risposta:
# Rappresenta la deviazione di ogni feature di una pratica rispetto la media di genuinità della feature.
# se (A-B)>0, significa che la feature della pratica A presenta un valore maggiore rispetto a B , (A-B)<0, invece significa che la feature della pratica A ha un valore minore rispetto a B.


# ==========================================================================
# SEZIONE 3 - Dot product (prodotto scalare): il cuore dei modelli lineari
# ==========================================================================
# Questa sezione vale doppio. Tutto cio' che farai da M3 (reti neurali) in
# poi e' una pila di dot product. Capirlo bene QUI = volare dopo.
#
# ANALOGIA (web / scoring):
#   Hai un dizionario "valori" e un dizionario "pesi" con le STESSE chiavi.
#   Vuoi un punteggio totale che "pesa ogni valore col suo peso".
#   In PHP / JS scriveresti un loop:
#
#     PHP:
#       $totale = 0;
#       foreach ($valori as $k => $v) { $totale += $v * $pesi[$k]; }
#
#     JS (con reduce):
#       const totale = valori.reduce((s, v, i) => s + v * pesi[i], 0);
#
#   Il dot product e' ESATTAMENTE quello, ma fatto su tutto il vettore in
#   un colpo solo, in modo super veloce.
#
# COSI' LO FAI IN NUMPY (3 modi equivalenti):
#   np.dot(x, w)         # esplicito
#   x @ w                # operatore '@' = dot (Python 3.5+)
#   (x * w).sum()        # mostra il "perche'": moltiplichi e poi sommi
#
# ESEMPIO NUMERICO PASSO PASSO:
#   x = np.array([2.0, 4.0, 6.0])
#   w = np.array([0.5, -1.0, 0.25])
#   step 1: x * w           = [2*0.5, 4*(-1), 6*0.25] = [1.0, -4.0, 1.5]
#   step 2: (x * w).sum()   = 1.0 + (-4.0) + 1.5     = -1.5
#   step 3: np.dot(x, w)    = -1.5  (stesso identico risultato)
#
# AUTO-CHECK RAPIDO (30 secondi, consigliato):
#   1) calcola z1 = np.dot(x, w)
#   2) calcola z2 = (x * w).sum()
#   3) verifica che z1 e z2 siano uguali (o quasi uguali)
#      Suggerimento: abs(z1 - z2) < 1e-9
#   -> se NON tornano, hai confuso dot con element-wise (-> [T4])
#
# COLLEGAMENTO M2 (importantissimo!):
#   La regressione logistica del cap.04/06 calcolava prima un punteggio:
#       z = somma_su_i ( x_scaled[i] * coef[i] ) + intercept
#         = np.dot(x_scaled, coef) + intercept
#   Poi la sigmoide trasformava z in prob_alterato.
#   QUINDI: la riga "contrib = x_scaled * coef" che hai scritto in
#   motivi_top3 e' la SCOMPOSIZIONE per feature dello stesso prodotto
#   scalare. Sommando contrib otterresti (quasi) z. Hai gia' usato i
#   vettori, solo che non lo sapevi.
#
# REGOLA SHAPE per il dot (-> [T5]):
#   - np.dot(a, b) richiede stessa lunghezza: a (5,) e b (5,) -> ok.
#   - mismatch -> ValueError ("shapes (3,) and (2,) not aligned")
#
# ATTENZIONE prima del TODO 3.1:
#   - "*" non e' dot product, e' element-wise -> [T4]
#   - NON usare for loop: usa np.dot o "@"
#   - se shape mismatch, NON nascondere l'errore con reshape -> [T3]
#
# ESEMPIO GUIDA (NON e' il tuo TODO):
#
#   def somma_pesata(valori, pesi, bias):
#       """Restituisce dot(valori, pesi) + bias come float."""
#       return float(np.dot(valori, pesi) + bias)
#   # somma_pesata(np.array([1,2,3]), np.array([1,1,1]), 0) -> 6.0

# ----------------------------------------------------------------------
# 3.1) TODO - scrivi una funzione "punteggio_lineare(x, w, b) -> float":
#   - calcola z = dot(x, w) + b
#   - ritorna float(z)
#   - test 1: usala con feature_pratica_A, pesi, b=0 -> stampa il risultato
#   - test 2: verifica "a mano" che (feature_pratica_A * pesi).sum() + 0
#     dia lo STESSO numero (sanity check del concetto di dot)
#
# REGOLE:
#   - NIENTE for loop: usa np.dot o l'operatore "@"  -> [T4]
#   - se shape mismatch, NON ignorare l'errore        -> [T5]
# SUGGERIMENTI:
#   - pensa a b come "intercept" della regressione logistica.
#   - extra (non richiesto): stampa anche 1 / (1 + np.exp(-z)) e nota
#     che e' la "sigmoide" -> da' un numero fra 0 e 1, come prob_alterato.
# ----------------------------------------------------------------------
# TUO CODICE (sezione 3.1):
print("\nMini-esercizio 3.1\n")
feature_pratica_A = np.array([1000.0, 2000.0, 3000.0, 4000.0, 5000.0])
pesi = np.array([1.0, -1.0, 0.5, -0.5, 0.25])
def punteggio_lineare(x, w, b) -> float:
   return float(np.dot(x, w) + b)
print(f"{punteggio_lineare(feature_pratica_A, pesi, 0)}")


# 3.2) DOMANDA DI RIPASSO:
#   Senza riguardare il cap.06: nella riga "contrib = x_scaled * coef",
#   D1) cosa rappresenta CIASCUN elemento del vettore "contrib"
#       (in 1 frase)?
# Ogni elemento rappresenta il valore pesato della feature scalata utilizzando la deviazione std, in modo da avere una rappresentazione chiara del suo contributo nel determinare la classe.
#   D2) perche' la SOMMA di tutti i contrib si avvicina molto a "z"
#       del modello logistico?
# Perchè il dot product, che è la somma di tutte le moltiplicazione element-wise, effettivamente è praticamente equivalente a sommare i contrib che si ottengono tramite operazione element-wise coef * x_scaled. Differisce solo per la mancanza dell intercetta che viene inserita dalla Logistic Regression nel calcolare Z.


# ==========================================================================
# SEZIONE 4 - Norma euclidea (la "lunghezza" di un vettore)
# ==========================================================================
# ANALOGIA GEOMETRICA (Pitagora, prima media):
#   In 2D un vettore [3, 4] e' una "freccia" che parte da (0,0) e arriva
#   al punto (3, 4). La sua "lunghezza" e' la distanza dal centro:
#
#       norma([3, 4]) = sqrt(3*3 + 4*4) = sqrt(9 + 16) = sqrt(25) = 5
#
#   Pitagora ti dice 5. La norma euclidea e' Pitagora generalizzato: vale
#   anche con 100 dimensioni, mica solo 2.
#
# IN PHP / JS (manuale):
#   PHP:
#       $somma_quadrati = 0;
#       foreach ($v as $x) { $somma_quadrati += $x * $x; }
#       $norma = sqrt($somma_quadrati);
#   JS:
#       const norma = Math.sqrt(v.reduce((s, x) => s + x * x, 0));
#
# IN NUMPY (1 chiamata):
#   np.linalg.norm(v)    # un float
#
# ESEMPIO NUMERICO PASSO PASSO:
#   v = np.array([3.0, 4.0])
#   step 1: v * v          -> array([9.0, 16.0])
#   step 2: (v * v).sum()  -> 25.0
#   step 3: np.sqrt(25.0)  -> 5.0
#   step 4: np.linalg.norm(v)  -> 5.0   (stesso risultato, in 1 riga)
#
# AUTO-CHECK RAPIDO (30 secondi, consigliato):
#   - verifica che np.linalg.norm(np.array([3.0, 4.0])) dia 5.0 (o molto vicino)
#   - se non lo da', c'e' un errore di input oppure stai passando una shape strana
#     (es. (1,2) invece di (2,)) -> [T1]
#
# ANALOGIA (dominio prodotto):
#   La norma di una pratica vista come vettore di feature e' una specie
#   di "scala/intensita' globale" della pratica. Se due pratiche hanno
#   norma molto diversa, "vivono in scale diverse" -> di solito si
#   normalizzano (ricordi StandardScaler?) prima di confrontarle.
#
# REGOLA MENTALE:
#   - norma piccola (~0): vettore "vicino al centro", quasi nullo.
#   - norma grande:       feature con valori "grandi" in modulo.
#   - DUE vettori con norma uguale NON sono uguali:
#     [3, 4] e [4, 3] hanno entrambi norma 5 ma puntano in DIREZIONI
#     diverse. Per la "direzione" servira' il coseno (Sezione 5).
#
# ATTENZIONE prima del TODO 4.1:
#   - cast a float: np.linalg.norm restituisce gia' un float NumPy
#     (np.float64); per coerenza con la firma fai float(...).
#   - vettore nullo: norma = 0. Nel coseno questo creera' un guaio
#     (-> [T7], ne riparliamo in Sezione 5).
#
# ESEMPIO GUIDA (NON e' il TUO TODO):
#
#   def lunghezza_segmento(v: np.ndarray) -> float:
#       """Distanza dall'origine al punto descritto da v."""
#       return float(np.linalg.norm(v))

# ----------------------------------------------------------------------
# 4.1) TODO:
#   - scrivi una funzione "norma(v) -> float" che restituisce
#     np.linalg.norm(v) come float.
#   - calcola norma di feature_pratica_A, feature_pratica_B, pesi.
#   - stampa i 3 valori con label leggibili.
#
# REGOLE:
#   - usa np.linalg.norm, NON scrivere il loop a mano.
#   - cast esplicito a float() per pulizia (-> [T10]).
# ----------------------------------------------------------------------
# TUO CODICE (sezione 4.1):
#


# ----------------------------------------------------------------------
# 4.2) GRAFICO 2D - "vedere" la norma con Pitagora
#
# Obiettivo: disegnare 2 vettori 2D come frecce dall'origine, mostrare
# che lunghezze diverse = norme diverse, e che [3,4] e [4,3] hanno la
# stessa lunghezza ma direzioni diverse.
#
# ESEMPIO GUIDA matplotlib (PIACE? RIUSALA, NON COPIARLA TALE E QUALE
# perche' i tuoi vettori sono diversi):
#
#   import matplotlib.pyplot as plt
#   v_demo = np.array([2.0, 1.0])
#   fig, ax = plt.subplots()
#   ax.quiver(0, 0, v_demo[0], v_demo[1],
#             angles="xy", scale_units="xy", scale=1, color="C0")
#   ax.set_xlim(-1, 5); ax.set_ylim(-1, 5)
#   ax.set_aspect("equal")     # importante: lunghezze fedeli
#   ax.grid(True)
#   ax.set_title(f"||v_demo|| = {np.linalg.norm(v_demo):.2f}")
#   # plt.show()  oppure  plt.savefig("01_norma_demo.png")
#
# COSA FAI TU (sezione 4.2):
#   - prendi v1 = np.array([3.0, 4.0]) e v2 = np.array([4.0, 3.0])
#   - disegnali entrambi come frecce dall'origine, su uno SOLO grafico
#   - imposta set_aspect("equal") cosi' la lunghezza e' fedele
#   - aggiungi un titolo che mostra le 2 norme calcolate (devono essere
#     uguali, == 5.0!) -> verifica visiva: stesse lunghezze, direzioni
#     diverse.
#
# REGOLE:
#   - 8-12 righe massimo
#   - non chiamare plt.show() in CI/script: usa savefig se serve
# ----------------------------------------------------------------------
# TUO CODICE (sezione 4.2):
#


# ==========================================================================
# SEZIONE 5 - Coseno tra vettori: "quanto si somigliano due pratiche"
# ==========================================================================
# Questa e' LA sezione che ti regge da M4 in poi. Tutto il "cercare
# documenti simili", "embedding piu' vicino", "RAG" e' coseno.
#
# ANALOGIA (intuitiva):
#   Pensa a 2 frecce sullo stesso piano:
#     - puntano nella STESSA direzione   -> coseno ~ 1   (molto simili)
#     - puntano PERPENDICOLARI            -> coseno ~ 0   (nessuna affinita')
#     - puntano in DIREZIONI OPPOSTE      -> coseno ~ -1  (opposti)
#
#   E' la stessa idea che usano gli embeddings nei sistemi RAG (M6): si
#   misura quanto un documento e' simile alla domanda dell'utente
#   confrontando i loro vettori col coseno. Stessa formula. Stessa idea.
#
# FORMULA IN PAROLE (niente LaTeX):
#   coseno(a, b) = dot(a, b) DIVISO ( norma(a) MOLTIPLICATO norma(b) )
#
#   Esce un numero fra -1 e +1. NON dipende dalla "lunghezza" di a e b
#   (per quello e' meglio della distanza euclidea quando vuoi misurare
#   "direzione" senza farti distrarre dalla scala).      -> [T8]
#
# INTERPRETAZIONE "DA PRODOTTO" (policy di lettura, non matematica pura):
#   Nel tuo dominio (controllo documentale), ti serve una regola pratica
#   per leggere i numeri senza confonderti. Ecco una policy *ragionevole*:
#
#     - coseno >= 0.95  -> "quasi identiche" (stessa direzione)
#     - 0.80 - 0.95     -> "molto simili"
#     - 0.50 - 0.80     -> "abbastanza simili"
#     - < 0.50          -> "poco simili" (probabilmente casi diversi)
#     - coseno < 0      -> "tendono in direzioni opposte" (segnale forte)
#
#   IMPORTANTISSIMO: e' una policy come il semaforo del cap.06:
#   - NON cambia la matematica
#   - ti aiuta a comunicare e prendere decisioni operative
#   - le soglie si tarano sui dati veri (quando li avrai), non a sentimento
#
# ESEMPI NUMERICI PASSO PASSO (fissali in testa):
#
#   ESEMPIO 1 - stessa direzione:
#     a = [1, 0], b = [1, 0]
#     dot = 1*1 + 0*0 = 1
#     norma(a) = 1, norma(b) = 1
#     coseno = 1 / (1 * 1) = 1.0     -> identici come direzione
#
#   ESEMPIO 2 - perpendicolari:
#     a = [1, 0], b = [0, 1]
#     dot = 1*0 + 0*1 = 0
#     norma(a) = 1, norma(b) = 1
#     coseno = 0 / (1 * 1) = 0.0     -> nessuna affinita'
#
#   ESEMPIO 3 - opposti:
#     a = [1, 0], b = [-1, 0]
#     dot = 1*(-1) + 0*0 = -1
#     norma(a) = 1, norma(b) = 1
#     coseno = -1 / (1 * 1) = -1.0   -> opposti
#
#   ESEMPIO 4 - simili ma non identici (caso reale):
#     a = [3, 4], b = [4, 3]
#     dot = 3*4 + 4*3 = 24
#     norma(a) = 5,  norma(b) = 5
#     coseno = 24 / (5*5) = 24/25 = 0.96   -> molto simili in direzione
#
# IN PHP / JS (per riferimento, dovresti scrivere ~10 righe, in NumPy 3):
#   PHP:
#       $dot = 0; $sa = 0; $sb = 0;
#       foreach ($a as $i => $x) {
#           $dot += $x * $b[$i]; $sa += $x*$x; $sb += $b[$i]*$b[$i];
#       }
#       $coseno = $dot / (sqrt($sa) * sqrt($sb));
#
# ATTENZIONE prima del TODO 5.1:
#   - se norma(a) o norma(b) sono 0 -> divisione per 0 -> [T7]:
#     la tua funzione DEVE alzare ValueError (NON restituire None,
#     NON restituire nan).
#     -> Pattern #19: in italiano si dice "None", non "null".
#   - shape: a e b devono avere stessa lunghezza, altrimenti ValueError.
#   - non usare scipy o sklearn: solo np.dot e np.linalg.norm.
#
# ESEMPIO GUIDA (NON e' il TUO codice):
#
#   def somiglianza_coseno(a: np.ndarray, b: np.ndarray) -> float:
#       """Restituisce un float in [-1, +1]."""
#       # ... (la firma e' chiara; il corpo lo scrivi tu nel TODO 5.1)
#       ...

# ----------------------------------------------------------------------
# 5.1) TODO - scrivi una funzione "coseno(a, b) -> float":
#   - calcola dot(a, b)
#   - calcola norma di a e di b
#   - ritorna dot / (norma_a * norma_b) come float
#   - controllo robusto: se una delle due norme e' 0 -> raise ValueError
#     ("vettore nullo: il coseno non e' definito")
#   - controllo robusto: se a.shape != b.shape -> raise ValueError
#
# REGOLE:
#   - NIENTE scipy o sklearn: solo np.dot e np.linalg.norm
#   - cast esplicito a float()
# SUGGERIMENTI:
#   - testa la funzione sui 4 esempi numerici qua sopra: i risultati
#     devono uscire 1.0, 0.0, -1.0, 0.96.
# ----------------------------------------------------------------------
# TUO CODICE (sezione 5.1):
#

#
# AUTO-TEST MINIMO (consigliato, 2 minuti):
#   Dopo aver scritto coseno(a, b), provalo su questi casi:
#     - coseno([1,0], [1,0])    -> 1.0
#     - coseno([1,0], [0,1])    -> 0.0
#     - coseno([1,0], [-1,0])   -> -1.0
#     - coseno([3,4], [4,3])    -> 0.96 (circa)
#   Suggerimento: usa np.array([...], dtype=float).
#   Se i risultati sono fuori da [-1, +1] -> hai un bug (-> [T8]).
#


# ----------------------------------------------------------------------
# 5.2) MINI-TASK PRODOTTO (collegamento M2):
#   Hai gia' feature_pratica_A e feature_pratica_B (sezione 1).
#   - Definisci feature_pratica_C "molto simile" ad A (es. campi quasi
#     uguali ad A, magari +/- 5%).
#   - Calcola coseno(A, B) e coseno(A, C).
#   - Stampa i 2 valori con un commento "interpretazione" in linguaggio
#     naturale, tipo:
#         "A vs C: coseno=0.99 -> molto simili (stessa direzione)"
#         "A vs B: coseno=0.84 -> abbastanza simili ma non identiche"
#
# DOMANDA: questo e' lo stesso TIPO di operazione che farai negli
# embeddings RAG (cap.M6) per dire "il documento X risponde alla
# domanda Y"? S/N. Se si', spiega in 1 riga il parallelo.
# Risposta:
#
#
# TUO CODICE (sezione 5.2):
#


# ==========================================================================
# CHECKPOINT FINALE - "so fare adesso?"
# ==========================================================================
# Senza guardare il codice sopra, rispondi in 1 riga ciascuna (commento).
# Dopo, segna anche un AUTO-RATING di sicurezza per ogni concetto.
#
# C1) Differenza fra np.array([1,2,3]).shape e np.array([[1,2,3]]).shape?
#     Risposta:
#     #
#
# C2) Quanto fa np.dot(np.array([1,2,3]), np.array([1,1,1])) e perche'?
#     Risposta:
#     #
#
# C3) Se norma(a) = 0, perche' coseno(a, b) non e' definito?
#     Risposta:
#     #
#
# C4) Spiega in 1 frase il legame fra "x_scaled * coef" del cap.06
#     e il dot product.
#     Risposta:
#     #
#
# C5) Nel tuo prodotto (controllo documentale), 1 motivo concreto per
#     cui il coseno tra pratiche (vettori di feature) sara' utile in
#     M4-M6:
#     Risposta:
#     #
#
# AUTO-RATING (1 = mi sento perso, 5 = potrei spiegarlo a un collega):
#
#   - Vettori e shape (Sezione 1):              ___ / 5
#   - Operazioni base (Sezione 2):              ___ / 5
#   - Dot product (Sezione 3):                  ___ / 5
#   - Norma euclidea (Sezione 4):               ___ / 5
#   - Coseno (Sezione 5):                       ___ / 5
#
# (questi voti li uso per calibrare il cap.02 del Ponte: se un punto e'
#  sotto 3, ci torno con un mini-rinforzo)


# ==========================================================================
# MINI-PROGETTO GUIDATO (OPZIONALE, ma altamente consigliato)
# "Trova le 3 pratiche piu' simili" - aggancio diretto a M4-M6 (RAG)
# ==========================================================================
# Idea: prendi il CSV mock del cap.06 (modulo_02_ml/dati/pratiche_genuinita_mock.csv).
# Ogni riga e' una pratica = un vettore di feature numeriche. Data una
# pratica "query" (es. pratica_id = 5), trova le 3 pratiche piu' simili
# usando il coseno fra vettori.
#
# Perche' e' un PRELUDIO al RAG (M6):
#   In RAG: data una DOMANDA -> trasformi in vettore (embedding) ->
#   confronti col vettore di ogni DOCUMENTO -> scegli i K piu' simili
#   (cosine similarity). Stessa identica idea, ma su parole invece che
#   su feature numeriche.
#
# ----------------------------------------------------------------------
# TODO opzionale - scrivi una funzione "classifica_per_similarita":
#
#   def classifica_per_similarita(
#       pratiche: pd.DataFrame,
#       pratica_id_query: int,
#       k: int = 3,
#   ) -> list[tuple[int, float]]:
#       """
#       Restituisce i k pratica_id piu' simili a quella query, ordinati
#       per coseno DECRESCENTE, esclusa la pratica_id_query stessa.
#       Forma del risultato: [(pratica_id, coseno), ...] di lunghezza k.
#       """
#       ...
#
# Step suggeriti (no soluzione, fai tu):
#   1) carica il CSV (riusa la tua funzione carica_pratiche del cap.06
#      o un pd.read_csv "manuale" qui).
#   2) costruisci X = pratiche.drop(columns=["pratica_id", "y_alterato"])
#      (ricordi Lacuna #17? -> [drop COLONNE reali])
#   3) recupera la riga della query: x_query = X.loc[<indice giusto>].values
#   4) loop su tutte le altre righe: per ogni x_i, calcola coseno(x_query, x_i)
#      (tieni la coppia (pratica_id, coseno))
#   5) ordina per coseno decrescente, prendi i primi k, ESCLUDI la query
#   6) ritorna la lista di tuple
#
# REGOLE:
#   - usa la TUA funzione coseno (sezione 5.1)
#   - shape coerenti: x_query e x_i devono essere 1D (n,)   -> [T1]
#   - se k > numero di pratiche disponibili, alza ValueError
#
# DOMANDA al termine: come cambierebbe questa funzione se al posto delle
# feature numeriche avessi gli "embeddings" (vettori a 384 o 768
# dimensioni) di un sentence-transformer? Risposta in 1 riga.
# Risposta:
#
#
# TUO CODICE (mini-progetto):
#


# ==========================================================================
# CHIUSURA - cosa hai imparato in concreto
# ==========================================================================
# Se sei arrivato qui:
#   - Sai che "una pratica = un vettore" non e' una metafora ma il modo
#     in cui i modelli ML vedono i dati.
#   - Sai distinguere shape (n,), (1, n), (n, 1) e perche' e' importante.
#   - Sai calcolare e interpretare: somma, sottrazione, scalare * vettore,
#     dot product, norma euclidea, coseno fra vettori.
#   - Hai collegato "contrib = x_scaled * coef" del cap.06 al dot product.
#   - Sai che il coseno tra vettori e' lo stesso strumento che sta sotto
#     il RAG (M6) e gli embeddings (M4).
#
# Cosa viene dopo (cap.02 Ponte): MATRICI. Una matrice e' "tante pratiche
# in una volta" o "tanti pesi insieme" (un layer di rete neurale = una
# matrice di pesi). Il prodotto matrice-vettore e' la generalizzazione
# del dot product e ti permette di classificare tutto un BATCH in un
# solo calcolo. Senza vettori solidi, le matrici diventano un incubo;
# con vettori solidi, sono un passo naturale.


# ==========================================================================
# NOTE FINALI (mentor)
# ==========================================================================
# - Per chiedere una valutazione:
#       "valuta cap.01 ponte sezione 3.1"
#   oppure
#       "valuta @ponte_matematico_m2_m3/01_vettori_da_zero.py righe A-B"
# - Niente soluzioni anticipate: ti spiego l'errore quando lo trovi tu.
# - Se ti senti bloccato per > 10 minuti su una sezione:
#       "sono bloccato sezione X" -> ti do solo l'IDEA, mai il codice.
# - Vuoi un challenge a fine capitolo (oltre il mini-progetto)? Chiedi:
#       "dammi un esercizio colloquio sui vettori"
