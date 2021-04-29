import pickle
import os
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from gen_kmeans import get_cluster_centroids

# identifiers = pickle.load(open('xy_Static/identifiers2move.p', 'rb'))

hand_vp = 20
kick_vp = 24

hand_techniques = ["High block", "Middle block (in-to-out)", "Middle block (out-to-in)", "Knife hand block", "Low block", "Punch (middle-level)", "High punch (face-level)"]
kicking_techniques = ["Front kick", "Round kick", "Side kick"]

lu = 'xy_Static'

def get_data(path_to_ks, suffix, new_identifiers=False):
    ks = pickle.load(open(path_to_ks, 'rb'))

    num_angles = 14
    total_poses = (hand_vp * 2 * len(hand_techniques)) + (kick_vp * 2 * len(kicking_techniques))

    X = np.empty((total_poses, num_angles))
    y = np.array([])

    if new_identifiers == True:
        identifier2move = {}
        move2identifier = {}
        identifiers = [i for i in range(len(ks.values()))]
        random.shuffle(identifiers)
    else:
        identifier2move, move2identifier = pickle.load(open(os.path.join(lu, f'moveids.p'), 'rb'))

    count = 0
    for move in ks:
        if new_identifiers == True:
            moveid = identifiers.pop()
            identifier2move[moveid] = move
            move2identifier[move] = moveid
        else:
            moveid = move2identifier[move]
        vocab_poses = ks[move].cluster_centers_
        for pose in vocab_poses:
            X[count] = pose #where X is the collection of vocab poses that map
            y = np.append(y, [moveid])
            count += 1
    np.savez(os.path.join(lu, suffix), X, y)
    if new_identifiers == True:
        pickle.dump((identifier2move, move2identifier), open(os.path.join(lu, f'moveids.p'), 'wb'))
    return X,y, identifier2move, move2identifier

def classify_videos(ips, tech, ks_name, new_ids=False):
    path_to_ks = os.path.join(lu, ks_name)
    suffix = path_to_ks[path_to_ks.find('-')+1:path_to_ks.find('.p')]

    if not os.path.exists(os.path.join(lu, f'{suffix}.npz')):
        X, y, identifier2move, move2identifier = get_data(path_to_ks, suffix, new_identifiers=new_ids)
    else:
        npzfile = np.load(os.path.join(lu, f'{suffix}.npz'))
        X,y = npzfile['arr_0'], npzfile['arr_1']
        identifier2move, move2identifier = pickle.load(open(os.path.join(lu, f'moveids.p'), 'rb'))

    # neigh = KNeighborsClassifier(n_neighbors=5)
    neigh = KNeighborsClassifier(n_neighbors=10)
    # neigh = KNeighborsClassifier(n_neighbors=12)
    neigh.fit(X, y)

    final_res = []
    for i, ip in enumerate(ips):
        if tech[i] == 'h':
            num_vp = int(suffix[suffix.find('h')+1:suffix.find('k')])
        else:
            num_vp = int(suffix[suffix.find('k')+1:])

        sample_kmeans = get_cluster_centroids(num_vp, [ip])

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
        #     print(w, tally[w])
            # final_res.append(tally.values())
        maxvote_move = max(tally, key=tally.get)
        final_res.append((maxvote_move, f'{tally[maxvote_move]}/{sum(tally.values())}'))
    return final_res

def print_res(ips, final_res):
    for ip, fr in zip(ips, final_res):
        print(f'{ip}\t|\t{fr[0]}\t{fr[1]}')

# ips = ['xy_Static/IMG_5002_si.npy', 'xy_Static/fk_rd_0_si.npy', 'xy_Static/fk_rd_1_si.npy']
# tech = ['h', 'k', 'k']
# res = classify_videos(ips, tech, f'ks-h{hand_vp}k{kick_vp}.p', new_ids=True)
# print_res(ips, res)

def get_f1(prefix, pr):  # searching in pr for this prefix
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for pred, res in pr:
        if pred == res == prefix:
            tp += 1
        elif pred == prefix and res != prefix:
            fp += 1
        elif pred != prefix and res != prefix:
            tn += 1
        elif pred != prefix and res == prefix:
            fn += 1
    try:
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        precision = float("nan")
    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        recall = float("nan")
    print(f'Precision: {precision}')
    print(f'Recall: {recall}')
    try:
        f1 = 2 * (precision * recall) / (precision + recall)
    except:
        f1 = float("nan")
    print(f'F1: {f1}')
    return f1

pr = pickle.load(open('../xy_Static/pr.p', 'rb'))
f1 = get_f1('hb_l', pr)