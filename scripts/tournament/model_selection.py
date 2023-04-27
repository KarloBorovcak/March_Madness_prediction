import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Read in the data
train = pd.read_csv('./data/model/trainingData.csv')
test = pd.read_csv('./data/model/testData.csv')

y_train = train['Team1Win']
X_train = train.drop(['Team1Win', 'Team1', 'Team2', 'Year'], axis=1)

y_test = test['Team1Win']
X_test = test.drop(['Team1Win', 'Team1', 'Team2', 'Year'], axis=1)

# Train the models
param_grid = {'C': [0.1, 1, 10, 100, 1000], 
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf', 'sigmoid']} 
  
grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3, n_jobs=-1)
  
# fitting the model for grid search
grid.fit(X_train, y_train)

# Print the best hyperparameters and the corresponding score
print("Best hyperparameters: ", grid.best_params_)
print("Best score: ", grid.best_score_)



# xgb = xgb.XGBClassifier()
# xgb.fit(X_train, y_train)

# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)

# lr = LogisticRegression()
# lr.fit(X_train, y_train)


# # Test the models
# print("XGBoost:",xgb.score(X_test, y_test))

# scaler = StandardScaler()
# X_test = scaler.fit_transform(X_test)
# print("Logistic regression:",lr.score(X_test, y_test))
