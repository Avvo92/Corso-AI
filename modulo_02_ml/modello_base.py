import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

print("\nProgetto incrementale\n")
#carico il file file "case.csv" e lo leggo come Dataframe Pandas
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

#assegno il modello alla variabile "modello",imposto gli iperparametri e lo addestro
modello = DecisionTreeRegressor(max_depth=6, random_state=42)
modello.fit(X_train, y_train)
y_pred_train = modello.predict(X_train)
y_pred_test = modello.predict(X_test)

#calcolo la baseline
y_baseline = np.full_like(y_test, y_train.mean())

#imposto le metriche per effettuare i confronti
mae_baseline = mean_absolute_error(y_test, y_baseline)
r2_baseline = r2_score(y_test, y_baseline)

mae_train = mean_absolute_error(y_train, y_pred_train)
r2_train = r2_score(y_train, y_pred_train)

mae_test = mean_absolute_error(y_test, y_pred_test)
r2_test = r2_score(y_test, y_pred_test)

print(f"Reali Train      => {y_train[:5].values.astype(int)}")
print(f"Previsioni Train => {y_pred_train[:5].astype(int)}")
print(f"MAE Train        => {mae_train:.2f}")
print(f"R² Train         => {r2_train:.3f}\n")

print(f"Reali Test       => {y_test[:5].values.astype(int)}")
print(f"Previsioni Test  => {y_pred_test[:5].astype(int)}")
print(f"MAE Test         => {mae_test:.2f}")
print(f"R² Test          => {r2_test:.3f}\n")

print(f"Reali Test       => {y_test.values.astype(int)}")
print(f"Prev. Baseline   => {y_baseline.astype(int)}")
print(f"MAE Baseline     => {mae_baseline:.2f}")
print(f"R² Baseline      => {r2_baseline:.3f}\n")

assert mae_test < mae_baseline, "il modello deve battere la baseline"