import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.preprocessing import StandardScaler

print("\nProgetto incrementale\n")
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
        'valore': modello.coef_
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