from random import randint
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import intercluster_distance

data = pd.read_csv('./data/final/combined.csv')

data = data.dropna(subset=['SEED'])


mapa = {'Champions': 8, '2ND' : 7, 'F4' : 6, 'E8' : 5, 'S16' : 4, 'R32' : 3, 'R64' : 2, 'R68' : 1}
data['POSTSEASON_value'] = data['POSTSEASON'].map(mapa)
FEATURES = ['TP', 'OP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'DRB', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Pace', 'ORtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA']
#FEATURES = ['TP', 'OP', 'FG', 'FGA','FG%', '3P', '3P%', 'FT','FT%','AST','STL', 'BLK', 'PF', 'FTr', 'TRB%','AST%','TOV%']
#FEATURES = ['TP', 'OP', 'FG', '3P', 'FT', 'DRB', 'ORB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Pace', 'ORtg', 'TS%']


X = data[FEATURES]
X = X.sample(frac=1, random_state=42)
# X = StandardScaler().fit_transform(X)

pca = PCA(n_components=0.9)
X_p = pca.fit_transform(X)

# silhouette_scores = []
# for k in range(2, 30):
#     kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
#     labels = kmeans.fit_predict(X_p)
#     silhouette_scores.append(silhouette_score(X_p, labels))

# print(silhouette_scores.index(max(silhouette_scores)) + 2)
# print(silhouette_scores)


kelb = KElbowVisualizer(KMeans(random_state=42, n_init=10),
                  k=(2, 30),
                  timings=False)

# Save as png
kelb.fit(X_p)
kelb.show(outpath='./data/model/elbow.png')

k = 8
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)


data['CLUSTER'] = labels

cluster_data = data[['School', 'YEAR', 'CLUSTER']]

cluster_data.to_csv('./data/model/clusterData.csv', index=False)
