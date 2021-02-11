import os
import numpy as np
from Archive import angles as ang
from sklearn.cluster import KMeans

#this will be the 26-feature series of vectors
rows = []

directory = '../sample_data/left_middle_block_sample'
for f in os.listdir(directory):
    a = list(ang.get_angles(os.path.join(directory,f)).values())
    rows.append(a)

X = np.array(rows)

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

# print(kmeans.labels_)
print(kmeans.cluster_centers_)