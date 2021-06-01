# Purpose: to classify a pose into its vocabulary poses
import pickle
import os
import numpy as np
import random
from sklearn.neighbors import KNeighborsClassifier
from gen_kmeans import get_cluster_centroids

# number of vocabulary poses for hand and kicking techniques

num_angles = 14

hand_vp = 10
kick_vp = 12

hand_techniques = ["High block", "Middle block (in-to-out)", "Middle block (out-to-in)", "Knife hand block",
                   "Low block", "Punch (middle-level)", "High punch (face-level)"]
kicking_techniques = ["Front kick", "Round kick", "Side kick"]

# base path
lu = '../xy_Static'


def get_data(path_to_ks, suffix, new_identifiers=False):
    """
    Given previously identified number of angles, vocabulary poses for hand techniques, and vocabulary poses for kicking techniques,
    this method takes all vocabulary poses for each move from a `path_to_ks` pickle file, which contains a dictionary that maps prefix to vocab poses, and generates
    a random identifier for each of the 20 possibilities (randomly chosen, to avoid any mixup with similar moves being assigned close numbers), and generates and saves the X,y arrays for KNN training
    :param path_to_ks: the path to the ks pickle file
    :param suffix: the identifier for a specific number of vocabulary poses, ex. h10k12 means 10 vocab poses for hand techniques and 12 vocab poses for kicking techniques
    :param new_identifiers: whether or not to create new identifiers, or use the existing pickle file (defaults to false)
    :return: X (the angles representations of the vocabulary poses), y (the identifier of the prefix the corresponding vocab pose belongs to), the dictionary that maps the random int indentifier to the prefix, and the dictionary that maps the prefix to the identifier
    """
    ks = pickle.load(open(path_to_ks, 'rb'))

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
            X[count] = pose  # where X is the collection of vocab poses that map
            y = np.append(y, [moveid])
            count += 1
    np.savez(os.path.join(lu, suffix), X, y)
    if new_identifiers == True:
        pickle.dump((identifier2move, move2identifier), open(os.path.join(lu, f'moveids.p'), 'wb'))
    return X, y, identifier2move, move2identifier


def classify_videos(ips, tech, ks_name, new_ids=False):
    """
    Classifies all videos in `ips` according to whether its a hand or foot technique and to the kmeans objects containing vocabulary poses into one of the 20 possibilities (10 moves, each side)
    :param ips: list of strings for the names of all .npy files that should be classified into a technique
    :param tech: list of strings, either 'h' for hand technique or 'k' for kicking technique, that match up with the list of filenames in `ips` #obsolete in sample runs since we just assume its the technique which requires the largest number of vocabulary poses (so kicking techniques)
    :param ks_name: the name of the pickle file where the kmeans objects from training are stored (containing the vocabulary poses for each of the 20 possibilities), ex. ks-h10k12.p
    :param new_ids: boolean for whether or not new identifiers should be generated, assumed to already be stored in `moveids.p`
    :return: an array of tuples, the first value is the string abbreviation for which move the given video has been classified into and a string for how many out of the total vocabulary poses led to that conclusion
    """
    path_to_ks = os.path.join(lu, ks_name)
    suffix = path_to_ks[path_to_ks.find('-') + 1:path_to_ks.find('.p')]

    if not os.path.exists(os.path.join(lu, f'{suffix}.npz')):
        X, y, identifier2move, move2identifier = get_data(path_to_ks, suffix, new_identifiers=new_ids)
    else:
        npzfile = np.load(os.path.join(lu, f'{suffix}.npz'))
        X, y = npzfile['arr_0'], npzfile['arr_1']
        identifier2move, move2identifier = pickle.load(open(os.path.join(lu, f'moveids.p'), 'rb'))

    neigh = KNeighborsClassifier(n_neighbors=10)
    neigh.fit(X, y)

    final_res = []
    for i, ip in enumerate(ips):
        if tech[i] == 'h':
            num_vp = int(suffix[suffix.find('h') + 1:suffix.find('k')])
        else:
            num_vp = int(suffix[suffix.find('k') + 1:])

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


# Sample Run

# ips = ['xy_Static/IMG_5002_si.npy', 'xy_Static/fk_rd_0_si.npy', 'xy_Static/fk_rd_1_si.npy']
# tech = ['h', 'k', 'k']
# res = classify_videos(ips, tech, f'ks-h{hand_vp}k{kick_vp}.p', new_ids=True)
# print_res(ips, res)
