from random import randint
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score

data = pd.read_csv('./data/final/combined.csv')

data = data.dropna(subset=['SEED'])

mapa = {'Champions': 8, '2ND' : 7, 'F4' : 6, 'E8' : 5, 'S16' : 4, 'R32' : 3, 'R64' : 2, 'R68' : 1}
data['POSTSEASON_value'] = data['POSTSEASON'].map(mapa)
FEATURES = ['SRS', 'TP', 'OP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'DRB', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Pace', 'ORtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'SEED', 'POSTSEASON_value']


X = data[FEATURES]
X = X.sample(frac=1, random_state=42)
X = StandardScaler().fit_transform(X)

k_values = range(2, 36)
best_silhouette_score = -1  # Initialize with a low value
best_calinski_harabasz_score = -1  # Initialize with a low value
best_k = -1

# for k in k_values:
#     best_silhouette = -1  # Initialize with a low value
#     best_calinski_harabasz = -1  # Initialize with a low value

#     for _ in range(10):  # Run each k-means instance 10 times with different random seeds
#         kmeans = KMeans(n_clusters=k, random_state=randint(0, 1000), n_init=10)
#         kmeans.fit(X)

#         # Evaluate cluster validity using Silhouette score and Calinski-Harabasz index
#         silhouette = silhouette_score(X, kmeans.labels_)
#         calinski_harabasz = calinski_harabasz_score(X, kmeans.labels_)

#         # Update the best scores and k value if the current run performs better
#         if silhouette > best_silhouette:
#             best_silhouette = silhouette
#         if calinski_harabasz > best_calinski_harabasz:
#             best_calinski_harabasz = calinski_harabasz

#     # Update the overall best scores and k value if the current k performs better
#     if best_silhouette > best_silhouette_score:
#         best_silhouette_score = best_silhouette
#         best_k = k
#     if best_calinski_harabasz > best_calinski_harabasz_score:
#         best_calinski_harabasz_score = best_calinski_harabasz
#         best_k = k

# print("Best performing k values:")
# print("Silhouette Score: k =", best_k, "Silhouette =", best_silhouette_score)
# print("Calinski-Harabasz Index: k =", best_k, "CH Index =", best_calinski_harabasz_score)

k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)


data['CLUSTER'] = labels

cluster_data = data[['School', 'YEAR', 'CLUSTER']]

cluster_data.to_csv('./data/model/clusterData.csv', index=False)
