import pickle
from sklearn.neighbors import KNeighborsClassifier

ks = pickle.load(open('xy_Static/ks-2021-03-11.p', 'rb'))

for move in ks:
    jk = ks[move]

# X = [[0], [1], [2], [3]]
#
# y = [0, 0, 1, 1]
#
# neigh = KNeighborsClassifier(n_neighbors=3)
# neigh.fit(X, y)
#
# print(neigh.predict([[1.1]]))
#
# print(neigh.predict_proba([[0.9]]))