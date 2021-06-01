import numpy as np
from scipy.spatial.distance import euclidean
from angles3 import get_angles
from fastdtw import fastdtw


def compare_sample(ips, oup):
    """
    Compares all the videos represented by .npy files in `ips` to the output `oup` using fastdtw
    :param ips: the list of strings of the names of input .npy files
    :param oup: the path to the ideal .npy file for this given move
    :return: the distance (similarity) between the ip and oup
    """
    d = []
    y = get_angles(np.load(oup))
    for i in ips:
        X = get_angles(np.load(i))
        distance, path = fastdtw(X, y, dist=euclidean)
        d.append(distance)
    return d


# Sample Run

# ips = ['xy_Static/IMG_5002_si.npy', 'xy_Static/fk_rd_0_si.npy']
# oup = 'xy_Static/fk_rd_1_si.npy'
#
# print(compare_sample(ips, oup))