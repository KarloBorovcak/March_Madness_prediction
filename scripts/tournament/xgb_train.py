import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

TARGET_YEAR = 2023
SCORE = 0

# Read in the data
data = pd.read_csv('./data/model/processedData.csv')

# Split the data into training and testing sets
train = data[data['Year'] != TARGET_YEAR]
test = data[data['Year'] == TARGET_YEAR]



FEATURES = ['Team1Win', 'Team1', 'Team2', 'Year']

y_train = train['Team1Win']
X_train = train.drop(FEATURES, axis=1)

y_test = test['Team1Win']
X_test = test.drop(FEATURES, axis=1)

features = X_train.columns.to_list()

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Get the feature importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

with open('xgb_model.txt', 'a') as f:
    f.write(f"Features: {features}\n")
    f.write(f"Score: {np.mean(cross_val_score(xgb.XGBClassifier(), X_train, y_train))}\n")


temp = len(features)
for i in range(1, temp):
    # Remove worst feature
    X_train = np.delete(X_train, indices[-1], axis=1)
    X_test = np.delete(X_test, indices[-1], axis=1)
    features.pop(indices[-1])
    # Train the model
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    # Get the feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    # Write the results to a file
    with open('xgb_model.txt', 'a') as f:
        f.write(f"Features: {features}\n")
        f.write(f"Score: {np.mean(cross_val_score(xgb.XGBClassifier(), X_train, y_train))}\n")
    


