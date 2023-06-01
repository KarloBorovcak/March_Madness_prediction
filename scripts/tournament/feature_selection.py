from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
import pandas as pd

data = pd.read_csv('./data/model/processedData.csv')
data = data[data['Year'] != 2023]
X = data.drop(['Team1', 'Team2', 'Team1Win', 'Year', 'ROUND'], axis=1)
y = data['Team1Win']



model = XGBClassifier() # Replace with your desired model

cv = StratifiedKFold(n_splits=5)  # Adjust the number of splits (n_splits) as desired


rfe = RFECV(estimator=model, cv=cv, scoring='accuracy')  # Replace 'accuracy' with your desired scoring metric

rfe.fit(X, y)


print("Selected Features:")
for i in range(len(rfe.support_)):
    if rfe.support_[i]:
        print(X.columns[i])  # Replace X.columns with your column names or feature identifiers

print("\nOptimal Number of Features: ", rfe.n_features_)

