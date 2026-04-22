import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import (
    cross_val_score,
    StratifiedKFold,
    train_test_split
)



print("\nProgetto incrementale\n")

print("\n" + "="*60)
print("REGRESSORI")
print("="*60)
#carico il file "case.csv" e lo leggo come Dataframe Pandas
path_file_case = os.path.join(os.path.dirname(__file__), "dati", "case.csv")
case = pd.read_csv(path_file_case)

#Creo 2 nuove feature per descrivere in maniera più efficace i record del DataFrame case.
case['log_mq'] = np.log1p(case['metri_quadri'])
case['mq_per_stanze'] = case['metri_quadri'] / case['num_stanze'].replace(0, np.nan)

#Faccio one-hot encoding su case perchè il decision tree non legge feature categoriche
case_encoded = pd.get_dummies(case, columns=['citta'], dtype='int')

#Preparo le features e il target in modo da assicurarmi di evitare il leakage
cols_to_drop = (['prezzo_euro'] + [c for c in case_encoded.columns if ('prezzo' in c) or ('fascia' in c)])
X = case_encoded.drop(columns=cols_to_drop, errors='ignore')
y = case_encoded['prezzo_euro']

#Eseguo lo split del DataFrame in train e test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42
)

#Imposto lo scaler per il secondo modello
scaler = StandardScaler()
scaler.fit(X_train)

#preparo i dati scalati per il modello lineare
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

#assegno il modello alla variabile "modello",imposto gli iperparametri e lo addestro
modello = DecisionTreeRegressor(max_depth=6, random_state=42)
modello_lineare_scalato = LinearRegression()

modello.fit(X_train, y_train)
modello_lineare_scalato.fit(X_train_scaled, y_train)

y_pred_train_albero = modello.predict(X_train)
y_pred_test_albero = modello.predict(X_test)
y_pred_train_lineare_scl = modello_lineare_scalato.predict(X_train_scaled)
y_pred_test_lineare_scl = modello_lineare_scalato.predict(X_test_scaled)

#calcolo la baseline
y_baseline = np.full_like(y_test, y_train.mean())

#imposto le metriche per effettuare i confronti
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)
rmse_baseline = root_mean_squared_error(y_test, y_baseline)

mae_train_albero = mean_absolute_error(y_train, y_pred_train_albero)
r2_train_albero = r2_score(y_train, y_pred_train_albero)
rmse_train_albero = root_mean_squared_error(y_train, y_pred_train_albero)
mae_test_albero = mean_absolute_error(y_test, y_pred_test_albero)
r2_test_albero = r2_score(y_test, y_pred_test_albero)
rmse_test_albero = root_mean_squared_error(y_test, y_pred_test_albero)

mae_train_lineare_scl = mean_absolute_error(y_train, y_pred_train_lineare_scl)
r2_train_lineare_scl = r2_score(y_train, y_pred_train_lineare_scl)
rmse_train_lineare_scl = root_mean_squared_error(y_train, y_pred_train_lineare_scl)
mae_test_lineare_scl = mean_absolute_error(y_test, y_pred_test_lineare_scl)
r2_test_lineare_scl = r2_score(y_test, y_pred_test_lineare_scl)
rmse_test_lineare_scl = root_mean_squared_error(y_test, y_pred_test_lineare_scl)

#creo una lista di dizionari per il report delle metriche
report_metriche = [
    {
        'modello': 'Baseline',
        'mae_train': '-',
        'mae_test': round(mae_baseline, 2),
        'r2_train': '-',
        'r2_test': round(r2_baseline, 3),
        'rmse_train': '-',
        'rmse_test': round(rmse_baseline, 2),
        
    },
    {
        'modello': 'Decision Tree',
        'mae_train': round(mae_train_albero, 2),
        'mae_test': round(mae_test_albero, 2),
        'r2_train': round(r2_train_albero, 3),
        'r2_test': round(r2_test_albero, 3),
        'rmse_train': round(rmse_train_albero, 2),
        'rmse_test': round(rmse_test_albero, 2),
    },
    {
        'modello': 'Linear Regression',
        'mae_train': round(mae_train_lineare_scl, 2),
        'mae_test': round(mae_test_lineare_scl, 2),
        'r2_train': round(r2_train_lineare_scl, 3),
        'r2_test': round(r2_test_lineare_scl, 3),
        'rmse_train': round(rmse_train_lineare_scl, 2),
        'rmse_test': round(rmse_test_lineare_scl, 2), 
    }
]

assert (mae_test_albero < mae_baseline) or (mae_test_lineare_scl < mae_baseline), "il modello deve battere la baseline"


#funzione per trovare i coefficienti più rilevanti
def motivi_top_3(modello, feature_names, n=3):    
    df_coef = pd.DataFrame({
        'nome': feature_names,
        'valore': modello.coef_.ravel()
    })
    df_coef['abs'] = df_coef['valore'].abs()
    df_coef_sorted = df_coef.sort_values(by='abs', ascending=False)
    report = []
    for _, row in df_coef_sorted.head(n).iterrows():
        report.append(f"{row['nome']} ({row['valore']:+.1f})")
    return report

#stampa del report e della lista prodotta dalla funzione
print(f"{pd.DataFrame(report_metriche)}\n")        
print(motivi_top_3(modello_lineare_scalato, X_train.columns, 3))

print("\n" + "="*60)
print("CLASSIFICATORI")
print("="*60)

# TASK:
# 1) Apri modello_base.py (usato nei cap.02-03 per la regressione)
# 2) Aggiungi una sezione CLASSIFICAZIONE che:
#    a) Carica pratiche_genuinita_mock.csv
#    b) Allena un DecisionTreeClassifier e una LogisticRegression
#    c) Stampa un DataFrame di confronto con colonne:
#       modello | accuracy | precision | recall | f1
#    d) Aggiungi una funzione semaforo(score) che restituisce
#       "verde" / "giallo" / "rosso" in base alle soglie del Blueprint
#    e) Stampa i motivi_top3 usando i coefficienti della LogisticRegression
# 3) Assert: recall di almeno un modello >= 0.5
#
# Definition of Done:
# - modello_base.py gira senza errori con `python modello_base.py`
# - Stampa confronto REGRESSIONE (dal cap.03) + CLASSIFICAZIONE (nuovo)
# - La funzione semaforo() restituisce valori coerenti
# - La funzione motivi_top3 funziona anche sul classificatore
#
# Impatto roadmap: R0 — primo classificatore binario + semaforo + scoring

pratiche = pd.read_csv(os.path.join(os.path.dirname(__file__), "dati", "pratiche_genuinita_mock.csv"))

X = pratiche.drop(columns=['pratica_id', 'y_alterato'])
y = pratiche['y_alterato']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=.2, random_state=42, stratify=y
)

scaler = StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf_tree = DecisionTreeClassifier(max_depth=4, random_state=42)
clf_log = LogisticRegression(max_iter=1000, random_state=42)

clf_tree.fit(X_train_scaled, y_train)
clf_log.fit(X_train_scaled, y_train)

y_pred_tree = clf_tree.predict(X_test_scaled)
y_pred_log = clf_log.predict(X_test_scaled)
y_proba_log = clf_log.predict_proba(X_test_scaled)

report_metriche = pd.DataFrame([
    {
        'modello': 'Decision Tree Classifier',
        'accuracy': accuracy_score(y_test, y_pred_tree),
        'precision': precision_score(y_test, y_pred_tree,zero_division=0),
        'recall': recall_score(y_test, y_pred_tree,zero_division=0),
        'f1': round(f1_score(y_test, y_pred_tree,zero_division=0), 3) 
    },
    {
        'modello': 'Logistic Regression',
        'accuracy': accuracy_score(y_test, y_pred_log),
        'precision': precision_score(y_test, y_pred_log, zero_division=0),
        'recall': recall_score(y_test, y_pred_log, zero_division=0),
        'f1': round(f1_score(y_test, y_pred_log, zero_division=0), 3) 
    }
])

print(f"{report_metriche}\n")

def semaforo(proba):
    prob_gen = proba[:, 0]*100
    semaforo = np.select(
        [prob_gen >= 85, prob_gen >= 60],
        ['verde', 'giallo'],
        default='rosso'
    )
    return semaforo

np_arr_test = y_test.to_numpy()
gen_reale = np.select(
    [np_arr_test == 0, np_arr_test == 1],
    ['genuino', 'alterato'],
    default='?'
)

gen_prev = np.select(
    [y_pred_log == 0, y_pred_log == 1],
    ['genuino', 'alterato'],
    default='?'
)
    
report_test = pd.DataFrame({
    'pratica_id': pratiche.loc[y_test.index, 'pratica_id'],
    'classe_reale': gen_reale,
    'classe_prevista': gen_prev,
    'score_genuinita': (y_proba_log[:, 0]*100).round(2),
    'semaforo': semaforo(y_proba_log)
})

print(report_test.sort_values(by='score_genuinita', ascending=False))

coefficienti = pd.DataFrame({
    'nome': X_train.columns,
    'valore': clf_log.coef_.ravel()
})
coefficienti['abs'] = coefficienti['valore'].abs()

print(motivi_top_3(clf_log, X_train.columns, 3))

assert max(recall_score(y_test, y_pred_tree),recall_score(y_test, y_pred_log)) >= 0.5, 'recall di uno dei modelli deve essere >= 0.5'


# TASK (ordine consigliato):
# 1) Importa ciò che serve (es. `cross_val_score`, `StratifiedKFold`, e per
#    evitare leakage nello scaler dentro ogni fold: `sklearn.pipeline.Pipeline`).
# 2) Costruisci una `Pipeline` con `StandardScaler` + `LogisticRegression`
#    (stessi iperparametri sensati che usi già: max_iter, random_state).
# 3) Esegui `cross_val_score` sulla porzione **train** della classificazione
#    (gli stessi `X_train`, `y_train` che già usi dopo lo split), con:
#    - `cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
#    - `scoring="recall"`
# 4) Stampa: array dei recall per fold, **media** e **deviazione standard**.
# 5) Aggiungi un commento (2–4 righe): cosa ti dice la CV che un solo
#    `recall_score(y_test, y_pred)` sul test **non** ti dice?
#
# Definition of Done:
# - `python modello_base.py` termina senza errori
# - In output compare almeno una riga con **media recall** dalla CV
# - Il commento al punto 5 è presente
#
# Non usare il **test set** per la cross-validation (solo `X_train`, `y_train`).
#
# Impatto roadmap: R0 — non fidarsi di un solo split; base per monitoring e retuning.
#
# Scrivi tutto il codice in `modello_base.py` (sotto l’assert della sezione classificazione).

#imposto lo StdScaler e lo alleno solo sul train
print("\nTask Capitolo 5\n")

kfold = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)

clf_log_pipe = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, random_state=42))
])

rec_scores = cross_val_score(
    clf_log_pipe,
    X_train,
    y_train,
    cv=kfold,
    scoring="recall"
)

print(f"Array dei Recall => {rec_scores.round(3)}")
print(f"Media dei Recall => {rec_scores.mean().round(3)}")
print(f"Dev. Std Recall  => {rec_scores.std().round(4)}")

# Rispetto al solo valore del recall effettuato sul test set, con la cross_validation e l'utilizzo di una pipeline sul train abbiamo la possibilità di avere una media ripulita dalla variabilità della composizione del set, e quindi un risultato più stabile di questo scoring. Nel test, essendo una prova "secca", avremo un risultato utile ma inevitabilmente legato in parte anche alla composizione dello specifico set di dati che abbiamo utilizzato.


