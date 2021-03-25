import pickle
import os
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from gen_kmeans import get_cluster_centroids

# identifiers = pickle.load(open('xy_Static/identifiers2move.p', 'rb'))

def get_data(path_to_ks, suffix):
    ks = pickle.load(open(path_to_ks, 'rb'))

    num_angles = 14
    total_poses = (5 * 2 * 7) + (6 * 2 * 3)

    X = np.empty((total_poses, num_angles))
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
    np.savez(f'xy_Static/{suffix}', X, y)
    pickle.dump(identifier2move, open('xy_Static/identifiers2move.p', 'wb'))
    return X,y, identifier2move

def classify_videos(ips, tech):
    path_to_ks = 'xy_Static/ks-h5k6.p'
    suffix = path_to_ks[path_to_ks.find('-')+1:path_to_ks.find('.p')]

    if not os.path.exists(f'xy_Static/{suffix}.npz'):
        X, y, identifier2move = get_data(path_to_ks, suffix)
    else:
        npzfile = np.load(f'xy_Static/{suffix}.npz')
        X,y = npzfile['arr_0'], npzfile['arr_1']
        identifier2move = pickle.load(open('xy_Static/identifiers2move.p', 'rb'))

    # neigh = KNeighborsClassifier(n_neighbors=5)
    neigh = KNeighborsClassifier(n_neighbors=10)
    # neigh = KNeighborsClassifier(n_neighbors=12)
    neigh.fit(X, y)

    final_res = []
    for i, ip in enumerate(ips):

        if tech[i] == 'h':
            vp = int(suffix[suffix.find('h') + 1:suffix.find('h') + 2])
        else:
            vp = int(suffix[suffix.find('k') + 1:suffix.find('k') + 2])

        sample_kmeans = get_cluster_centroids(vp, [ip])

        res = []
        for pose in sample_kmeans.cluster_centers_:
            res.append(neigh.predict([pose]))

        tally = {}
        for r in res:
            m = identifier2move[r[0]]
            if m not in tally:
                tally[m] = 1
            else:
                tally[m] += 1

        # for w in sorted(tally, key=tally.get, reverse=True):
            # print(w, tally[w])

        final_res.append(max(tally, key=tally.get))
    return final_res

def print_res(ips, final_res):
    for ip, fr in zip(ips, final_res):
        print(f'{ip}\t|\t{fr}')

ips = ['xy_Static/IMG_5002_si.npy', 'xy_Static/fk_rd_0_si.npy', 'xy_Static/fk_rd_1_si.npy']
tech = ['h', 'k', 'k']
res = classify_videos(ips, tech)
print_res(ips, res)