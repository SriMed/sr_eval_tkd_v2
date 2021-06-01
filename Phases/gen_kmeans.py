import numpy as np
from angles3 import get_angles
from sklearn.cluster import KMeans


def get_cluster_centroids(k, ips):
    """
    Returns `k` cluster centroids for videos represented by `ips`, a bunch of NumPy archives
    :param k: number of clusters
    :param ips: all the input files, a list of .npy files
    :return: scikit-learn's kmeans object, which contains .cluster_centers_
    """
    X = get_angles(np.load(ips[0]))
    i = 1
    while i < len(ips):
        data = get_angles(np.load(ips[i]))
        X = np.concatenate((X, data))
        i += 1

    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

    # print(kmeans.labels_)
    # cc = kmeans.cluster_centers_
    # print(cc)
    return kmeans
