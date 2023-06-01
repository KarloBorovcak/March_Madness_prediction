import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import xgboost as xgb

def bracket_score(bracket, model, features):
    score = 0
    rounds = ['R64', 'R32', 'S16', 'E8', 'F4', 'Champions']
    for index, row in bracket.iterrows():
        if row["ROUND"] == 'R68':
            row["ROUND"] = 'R64'
        prediction = model.predict(row[features].values.reshape(1, -1))
        if prediction == row['Team1Win']:
            score += 2 ** rounds.index(row['ROUND']) * 10

        print(row['Team1'], row['Team2'], row['ROUND'], prediction, row['Team1Win'], score)
        
    return score

        


TARGET_YEAR = 2023

# Read in the data
data = pd.read_csv('./data/model/processedData.csv')

clusters = pd.read_csv('./data/model/clusterData.csv')

data = data.merge(clusters, how='left', left_on=['Team1', 'Year'], right_on=['School', 'YEAR'])
data = data.rename(columns={'CLUSTER': 'Team1Cluster'})
data = data.drop(['School', 'YEAR'], axis=1)   

data = data.merge(clusters, how='left', left_on=['Team2', 'Year'], right_on=['School', 'YEAR'])
data = data.rename(columns={'CLUSTER': 'Team2Cluster'})
data = data.drop(['School', 'YEAR'], axis=1)


bracket = data[data['Year'] == TARGET_YEAR]

# Shuffle the training data
data = data.sample(frac=1, random_state=42)
print(data.columns)
FEATURES = ['OP', 'FGA', 'FG%', 'FT', 'FTA', 'ORB', 'STL', 'BLK', 'TOV', 'PF', 'ORtg', '+-', 'SEED']
FEATURES = ['SRS', 'SEED', 'Team1Cluster', 'Team2Cluster']

FEATURES = ['TP', 'OP', 'FG', 'FGA','FG%', '3P', '3P%', 'FT','FT%','AST','STL', 'BLK', 'PF', 'FTr', 'TRB%','AST%','TOV%', '+-', 'SEED', 'SRS']

print(len(FEATURES))

# ALL DATA
X = data[FEATURES]
y = data['Team1Win']


# YEAR SPLIT
X_train_year = data[data['Year'] != TARGET_YEAR]
y_train_year = X_train_year['Team1Win']
X_train_year = X_train_year[FEATURES]



X_test_year = data[data['Year'] == TARGET_YEAR]
y_test_year = X_test_year['Team1Win']
X_test_year = X_test_year[FEATURES]


# Normalize
# scaler = StandardScaler()
# columns_scale = FEATURES[:-2]

# X.loc[:, columns_scale] = scaler.fit_transform(X.loc[:, columns_scale])
# X_train_year.loc[:, columns_scale] = scaler.fit_transform(X_train_year.loc[:, columns_scale])
# X_test_year.loc[:, columns_scale] = scaler.fit_transform(X_test_year.loc[:, columns_scale])




# Train the models
param_grid_svc = {'C': [0.1, 1, 10, 100, 1000], 
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf', 'sigmoid', 'linear']}

param_grid_xgb = {'max_depth': [3, 5, 7, 10],
              'learning_rate': [0.01, 0.1, 0.3],
              'n_estimators': [50, 100, 200, 500],
              'subsample': [0.5, 0.75, 1.0],
              'colsample_bytree': [0.5, 0.75, 1.0],
              'gamma': [0, 0.1, 0.5],
              'reg_alpha': [0, 1, 10],
              'reg_lambda': [0, 1, 10]}

param_grid_lr = {'penalty': ['l1', 'l2', 'elasticnet', 'none'],
              'C': [0.1, 0.5, 1, 5, 10],
              'fit_intercept': [True, False],
              'class_weight': [None, 'balanced'],
              'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}
  
grid = GridSearchCV(SVC(), param_grid_svc, refit = True, verbose = 3, n_jobs=-1)


# # fitting the model for grid search
# grid.fit(X, y)

# # Print the best hyperparameters and the corresponding score
# print("Best hyperparameters: ", grid.best_params_)
# print("Best score: ", grid.best_score_)


lr = LogisticRegression(C=0.01, class_weight='balanced', penalty='l1', solver='saga')
lr.fit(X_train_year, y_train_year)

print("Bracket score Logistic:", bracket_score(bracket, lr, FEATURES))

svc = SVC(kernel='rbf', gamma=0.001)
svc.fit(X_train_year, y_train_year)

print("Bracket score SVC:", bracket_score(bracket, svc, FEATURES))

xgbM = xgb.XGBClassifier(colsample_bytree=1.0, gamma=0.1, learning_rate=0.01, max_depth=10, n_estimators=50, reg_alpha=10, reg_lambda=10, subsample=0.5)
xgbM.fit(X_train_year, y_train_year)

print("Bracket score XGB:", bracket_score(bracket, xgbM, FEATURES))
print('------------------------------------')

# Test the models

print(f"{TARGET_YEAR} scores:")
print("Logistic regression:",lr.score(X_test_year, y_test_year))
print("SVC:",svc.score(X_test_year, y_test_year))
print("XGBoost:",xgbM.score(X_test_year, y_test_year))


lr_model = LogisticRegression()
svc_model = SVC(kernel='rbf', gamma=0.001)
xgb_model = xgb.XGBClassifier()

kf = KFold(n_splits=5, shuffle=True, random_state=42)

lr_scores = cross_val_score(lr_model, X, y, cv=kf)
svc_scores = cross_val_score(svc_model, X, y, cv=kf)
xgb_scores = cross_val_score(xgb_model, X, y, cv=kf)

print('------------------------------------')
print("Cross validation scores:")

print("Logistic regression:", lr_scores.mean())
print("SVC:", svc_scores.mean())
print("XGBoost:", xgb_scores.mean())
