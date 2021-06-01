# Purpose: to calculate angles between joints
# Note: math returns angles in radians
import numpy as np
import math
import json
import pickle

h36m_num_joints = 17
h36m_joints = {
    0: [7, 8, 9],
    1: [14, 8, 11],
    2: [8, 14, 15],
    3: [14, 15, 16],
    4: [8, 11, 12],
    5: [11, 12, 13],
    6: [7, 1, 2],
    7: [1, 2, 3],
    8: [7, 4, 5],
    9: [4, 5, 6],
    10: [16, 7, 13],
    11: [3, 7, 6],
    12: [8, 7, 16],
    13: [8, 7, 13]
}


def calc_angle(angle_jgroup, coordinates):
    """
    Calculates all the angles as specified by angle_jgroup and coordinates
    :param angle_jgroup: a dictionary which references which 3 joints make which angle
    :param coordinates: a numpy array which represents all the x,y,z coordinates of the joints
    :return: a numpy array of angles between joints in radians
    """
    angles = np.array([])
    for i in angle_jgroup:
        s, c, e = angle_jgroup[i]
        s_hat = coordinates[s] - coordinates[c]
        c_hat = coordinates[c] - coordinates[c]
        e_hat = coordinates[e] - coordinates[c]

        dot_product = s_hat @ e_hat
        alpha = math.acos((dot_product) / (np.linalg.norm(s_hat) * np.linalg.norm(e_hat)))

        angles = np.append(angles, alpha)
    return angles

def get_angles(data):
    """
    Calculates angles between joints for each frame in a given video, represented as `data`
    :param data: the .npy file containing a numpy array of coordinates of joints for each frame in video
    :return: all the angles, a series of numpy arrays (each array is one frame)
    """
    ang = np.empty((len(data), len(h36m_joints)))
    for i, frame in enumerate(data):
        f_ang = ang = calc_angle(h36m_joints, frame)
        ang[i] = f_ang
    return ang

#Sample Run

# data = np.load('../xy_Static/hb_ll_9.npy')
# print(data)
# ang = get_angles(data)
# print(ang)
