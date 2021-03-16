import pickle
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier

ks = pickle.load(open('xy_Static/ks-2021-03-11.p', 'rb'))

num_angles = 14
total_poses = 5*2*5+6*2*3

X = np.empty((total_poses, num_angles))
y = np.array([])
identifiers = [i for i in range(len(ks.values()))]
random.shuffle(identifiers)

count = 0
for move in ks:
    moveid = identifiers.pop()
    vocab_poses = ks[move].cluster_centers_
    for pose in vocab_poses:
        X[count] = pose
        y = np.append(y, [moveid])
        count += 1


# X = [[0], [1], [2], [3]]
#
# y = [0, 0, 1, 1]
#
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)

neigh.predict()
#
# print(neigh.predict([[1.1]]))
#
# print(neigh.predict_proba([[0.9]]))