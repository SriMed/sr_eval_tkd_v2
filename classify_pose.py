import pickle
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from gen_kmeans import get_cluster_centroids

ks = pickle.load(open('xy_Static/ks-2021-03-11.p', 'rb'))

num_angles = 14
total_poses = (5*2*7)+(6*2*3)

X = np.zeros((total_poses, num_angles))
y = np.array([])

identifier2move = {}

identifiers = [i for i in range(len(ks.values()))]
random.shuffle(identifiers)

count = 0
for move in ks:
    moveid = identifiers.pop()
    identifier2move[moveid] = move
    vocab_poses = ks[move].cluster_centers_
    for pose in vocab_poses:
        X[count] = pose #where X is the collection of vocab poses that map
        y = np.append(y, [moveid])
        count += 1


# X = [[0], [1], [2], [3]]
#
# y = [0, 0, 1, 1]
#

neigh = KNeighborsClassifier(n_neighbors=5)
neigh.fit(X, y)

sample_kmeans = get_cluster_centroids(5, ['xy_Static/IMG_5002_si.npy'])

res = []
for pose in sample_kmeans.cluster_centers_:
    res.append(neigh.predict([pose]))

# print(identifier2move)
# print(res)

tally = {}
for r in res:
    m = identifier2move[r[0]]
    if m not in tally:
        tally[m] = 1
    else:
        tally[m] += 1

for w in sorted(tally, key=tally.get, reverse=True):
    print(w, tally[w])

#
# print(neigh.predict([[1.1]]))
#
# print(neigh.predict_proba([[0.9]]))