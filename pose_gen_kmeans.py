import numpy as np
import angles3 as angles3
from sklearn.cluster import KMeans

#input - a bunch of NumPy archives of a given move

ips = ['xy_Static/hb_ll_9.npy', 'xy_Static/fk_rd_0_si.npy']

X = angles3.get_angles(np.load(ips[0]))
i = 1
while i < len(ips):
    data = angles3.get_angles(np.load(ips[i]))
    X = np.concatenate((X, data))
    i+=1

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

# print(kmeans.labels_)
print(kmeans.cluster_centers_)